---
name: line-script-app
description: >
  Master skill cho dự án Line Script App — web app làm phim dành cho Script Supervisor và đoàn phim độc lập.
  Dùng skill này cho BẤT KỲ tác vụ nào liên quan đến project này: viết code mới, sửa bug, thêm tính năng,
  thiết kế database, setup Cloudflare, cấu hình auth, xử lý PDF, vẽ line script, tạo shotlist, hay deploy.
  Trigger khi người dùng nhắc đến: line script, script lining, shotlist, kịch bản phim, PDF viewer,
  Fabric.js, Cloudflare Workers/D1/R2, Google Sheets sync, storyboard, Google Drive,
  hoặc bất kỳ phần nào của app này.
---

# Line Script App — Master Skill

## Tổng quan dự án

Web app chuyên dụng cho **Script Supervisor** và đoàn phim độc lập Việt Nam. Cho phép:
- Upload và xem kịch bản PDF
- Kẻ tuyến (Script Lining) chuẩn ngành trực tiếp lên PDF
- Tự động tạo Shotlist từ các đường kẻ tuyến (auto-extract text từ PDF)
- Quản lý nhiều dự án phim
- Làm việc nhóm với phân quyền Admin / Member

**Người dùng chính:** Đạo diễn, Script Supervisor, đoàn phim ~5 người.
**Thiết bị:** Desktop, iPad (Apple Pencil), iPhone, Android — tất cả qua trình duyệt (PWA).

---

## Tech Stack — ĐÃ CHỐT, KHÔNG THAY ĐỔI

| Layer | Công nghệ | Ghi chú |
|---|---|---|
| Frontend | React 18 + Vite + TypeScript | PWA enabled |
| PDF Viewer | PDF.js (Mozilla) | Render PDF lên canvas |
| Canvas / Drawing | Fabric.js | Vẽ line, annotation lên PDF |
| Apple Pencil | Pointer Events API | Qua Fabric.js, pressure-aware |
| Backend API | Cloudflare Workers (TypeScript) | Serverless |
| Database | Cloudflare D1 (SQLite) | Lưu users, projects, shots, annotations |
| File Storage | Cloudflare R2 | Lưu file PDF kịch bản |
| Auth | JWT tự build (bcrypt + jose) | Không dùng OAuth cho login |
| Hosting | Cloudflare Pages | Frontend deploy |
| Dev workflow | VS Code → GitHub → Cloudflare | Quy trình bất biến |
| Google Sheets Sync | Google Sheets API v4 | Sync shotlist 2 chiều (opt-in) |
| Storyboard Storage | Google Drive API v3 | Lưu ảnh storyboard, app chỉ dùng URL |

**Nguyên tắc quan trọng:**
- Ưu tiên công cụ **miễn phí hoàn toàn** — Cloudflare free tier đủ dùng cho team ~5 người
- KHÔNG dùng Supabase, Firebase, Vercel, hay bất kỳ service có thể bị pause/charge
- KHÔNG thêm dependency mới nếu không cần thiết — keep it lean
- Google Sheets/Drive là tính năng **opt-in** — user phải chủ động kết nối, không bắt buộc

---

## Kiến trúc hệ thống

```text
┌─────────────────────────────────────────┐
│           Cloudflare Pages              │
│    React + Vite + TypeScript (PWA)      │
│  PDF.js viewer + Fabric.js canvas       │
└────────────────┬────────────────────────┘
                 │ fetch / REST API
┌────────────────▼────────────────────────┐
│         Cloudflare Workers              │
│       TypeScript API endpoints          │
│   Auth (JWT) + Business Logic           │
└──────┬───────────┬──────────────┬───────┘
       │           │              │
┌──────▼──────┐ ┌──▼──────┐ ┌────▼──────────────┐
│ Cloudflare  │ │Cloudflare│ │  Google APIs       │
│     D1      │ │    R2    │ │  (opt-in)          │
│  (Database) │ │  (PDFs)  │ │  Sheets API v4     │
└─────────────┘ └─────────┘ │  Drive API v3      │
                             └────────┬───────────┘
                                      │ Apps Script
                                      │ onEdit() webhook
                             ┌────────▼───────────┐
                             │  Google Sheets      │
                             │  (Shotlist sync)    │
                             │  Google Drive       │
                             │  (Storyboard imgs)  │
                             └────────────────────┘
```

---

## Database Schema (D1 SQLite)

```sql
-- Users & Auth
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT DEFAULT 'pending' CHECK (role IN ('super_admin', 'owner', 'member', 'pending')),
  created_at INTEGER DEFAULT (unixepoch())
);

-- Invite tokens
CREATE TABLE invite_tokens (
  token TEXT PRIMARY KEY,
  project_id TEXT REFERENCES projects(id),
  created_by TEXT REFERENCES users(id),
  email TEXT,
  used_by TEXT REFERENCES users(id),
  expires_at INTEGER NOT NULL,
  created_at INTEGER DEFAULT (unixepoch())
);

-- Dự án phim
CREATE TABLE projects (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  owner_id TEXT REFERENCES users(id),
  created_at INTEGER DEFAULT (unixepoch())
);

-- Thành viên dự án
CREATE TABLE project_members (
  project_id TEXT REFERENCES projects(id),
  user_id TEXT REFERENCES users(id),
  PRIMARY KEY (project_id, user_id)
);

-- File kịch bản PDF
CREATE TABLE scripts (
  id TEXT PRIMARY KEY,
  project_id TEXT REFERENCES projects(id),
  name TEXT NOT NULL,
  r2_key TEXT NOT NULL,
  page_count INTEGER,
  uploaded_by TEXT REFERENCES users(id),
  created_at INTEGER DEFAULT (unixepoch())
);

-- Đường kẻ tuyến (Script Lines) — SCHEMA MỚI (migration 0006)
CREATE TABLE script_lines (
  id TEXT PRIMARY KEY,
  script_id TEXT REFERENCES scripts(id),
  user_id TEXT REFERENCES users(id),
  page_number INTEGER NOT NULL,
  x_position REAL NOT NULL,           -- % trục X (0-1), có thể update khi move ngang
  y_start REAL NOT NULL,              -- % trục Y điểm bắt đầu (0-1)
  y_end REAL NOT NULL,                -- % trục Y điểm kết thúc (0-1)
  color TEXT DEFAULT '#000000',
  segments_json TEXT,                 -- JSON: [{ type: 'straight'|'zigzag', y_start: 0.1, y_end: 0.3 }, ...]
                                      -- Mỗi segment là một đoạn trên line với kiểu riêng
                                      -- Bracket mark tự động chèn tại điểm chuyển tiếp giữa segments
  continues_to_next_page BOOLEAN DEFAULT FALSE,  -- true → hiển thị ↓ arrow thay End Bracket
  continues_from_prev_page BOOLEAN DEFAULT FALSE, -- true → không có Start Bracket trên (hoặc ↑ indicator)
  setup_number TEXT,                  -- e.g. '24', '24A', '24B'
  created_at INTEGER DEFAULT (unixepoch())
);
-- GHI CHÚ line_type cũ đã bị loại bỏ — thay bằng segments_json
-- Mỗi line có thể có nhiều đoạn straight/zigzag trên cùng 1 đường

-- Scene markers (T-shaped, dùng để đánh dấu ranh giới cảnh)
CREATE TABLE scene_markers (
  id TEXT PRIMARY KEY,
  script_id TEXT REFERENCES scripts(id),
  user_id TEXT REFERENCES users(id),
  page_number INTEGER NOT NULL,
  y_position REAL NOT NULL,
  x_offset REAL DEFAULT 0,
  created_at INTEGER DEFAULT (unixepoch())
);

-- Shots (Shotlist)
CREATE TABLE shots (
  id TEXT PRIMARY KEY,
  script_id TEXT REFERENCES scripts(id),
  line_id TEXT REFERENCES script_lines(id),
  user_id TEXT REFERENCES users(id),
  shot_number INTEGER NOT NULL,
  scene_number TEXT,
  location TEXT,
  int_ext TEXT CHECK (int_ext IN ('INT', 'EXT', 'INT/EXT')),
  day_night TEXT CHECK (day_night IN ('DAY', 'NIGHT', 'DAWN', 'DUSK')),
  description TEXT,     -- AUTO-EXTRACTED từ PDF (chỉ đoạn STRAIGHT, bỏ qua zigzag)
                        -- Hiển thị blur/mờ trong shotlist, max-height giới hạn
  user_notes TEXT,      -- Do người dùng tự viết — đây là phần CHÍNH trong shotlist
  dialogue TEXT,
  subjects TEXT,
  script_time TEXT,
  shot_size TEXT,
  shot_type TEXT,
  side TEXT,
  angle TEXT,
  movement TEXT,
  lens TEXT,
  notes TEXT,
  storyboard_drive_id TEXT,
  storyboard_view_url TEXT,
  sheets_row_index INTEGER,
  updated_at INTEGER DEFAULT (unixepoch()),
  created_at INTEGER DEFAULT (unixepoch())
);

-- Google OAuth tokens
CREATE TABLE google_tokens (
  user_id TEXT PRIMARY KEY REFERENCES users(id),
  access_token TEXT NOT NULL,
  refresh_token TEXT NOT NULL,
  expiry INTEGER NOT NULL,
  sheets_id TEXT,
  drive_folder_id TEXT,
  updated_at INTEGER DEFAULT (unixepoch())
);
```

---

## Line Script — Spec Chi Tiết (ĐÃ CHỐT 2026-03-31, CẬP NHẬT 2026-03-31)

### Input / Device Compatibility — QUAN TRỌNG

App phải hoạt động đồng nhất trên cả 3 thiết bị:

| Thiết bị | Click/Tap | Context menu | Move |
|---|---|---|---|
| Desktop (mouse) | click chuột trái | right-click | drag chuột |
| iPad (touch) | tap | long-press ~500ms | drag ngón tay |
| iPad (Apple Pencil) | tap bút | long-press bút | drag bút |

**Nguyên tắc xử lý event:**
- Dùng **Pointer Events API** thống nhất (`pointerdown`, `pointermove`, `pointerup`) — không dùng riêng touch/mouse events
- Context menu: `contextmenu` event cho desktop, `long-press` (pointerdown hold > 500ms, không move) cho iPad
- Fabric.js: `canvas.allowTouchScrolling = false` trên iPad để tránh cuộn trang khi vẽ
- KHÔNG phân biệt `pointerType === 'mouse'` vs `'touch'` vs `'pen'` trừ khi cần thiết

---

### Drawing Model: Click-Click (không phải drag)

1. **Click/Tap lần 1** → Label box (1/1, 1A...) xuất hiện ở đầu line, là điểm bắt đầu (không có start bracket riêng — label box ĐÃ là marker đầu)
2. **Di chuột/ngón tay** → Ghost line preview theo chiều dọc (X cố định)
3. **Tab key / nút Split trên toolbar** → toggle segment type straight ↔ zigzag → Bracket Mark tự chèn
4. **Click/Tap lần 2** → Line hoàn thành + End Bracket ở dưới
   - Nếu y_end > ~95% page → ↓ arrow thay End Bracket, `continues_to_next_page = true`

### Continuation Across Pages

- x_position ±3% match với line `continues_to_next_page = true` trang trước → auto-detect continuation
- Line continuation: không có label box trên đầu (hoặc ↑ nhỏ)

### Post-Draw Editing — Select Mode

- **Move ngang**: kéo line trái/phải (lockMovementY) — PATCH API `x_position`
  - Desktop: drag chuột; iPad: drag ngón tay/bút
- **Visual khi chọn line**: Hiển thị dashed circular handles tại endpoint đầu và cuối (giống tham chiếu ảnh). Opacity ring xung quanh endpoint.
- **Split**: 
  - Desktop: right-click → "Split" trong context menu
  - iPad: long-press → context menu → "Split"
  - Toolbar: nút "Split" → click vào điểm trên line → tách segment tại đó
- **Xóa**: right-click/long-press → "Xóa line + shot"
- **Undo/Redo**: Cmd+Z / Cmd+Shift+Z (desktop) + 2 nút visual trên toolbar

### Shot Label Box — Visual Design

```
┌─────┐
│ 1/1 │  ← nền trắng, border màu line, text màu line, font lớn hơn (14px+)
│  W  │  ← shot_size (nếu có)
└──┬──┘
   │    ← line bắt đầu từ đây (label IS the start point)
   │
```

- Nằm TRÊN ĐỈNH line (không có start bracket riêng)
- Di chuyển CÙNG với line khi kéo ngang
- Format: `sceneNum/shotNum` (e.g. "1/1") trên canvas
- Bên Shotlist tab: vẫn hiển thị đầy đủ scene info
- Bên line script canvas: chỉ hiện shot order number

### Visual Rendering

| Element | Mô tả |
|---|---|
| Line stroke | strokeWidth: **~2px** (mỏng, giống chuẩn ngành) |
| Straight segment | Đường thẳng liền nét |
| Zigzag segment | Custom SVG path `/\/\/\/` |
| Start | Label box (không có bracket riêng) |
| End Bracket | Gạch ngang ~10px tại y_end |
| Transition Bracket | Gạch ngang ~10px tại điểm chuyển |
| Continues ↓ | Mũi tên xuống khi `continues_to_next_page = true` |
| Selection visual | Dashed circular handle (opacity ring) tại endpoints khi selected |

### Zigzag = Không lấy text vào description

- Extract text chỉ từ **straight** segments — zigzag bị bỏ qua

---

### Toolbar Tools (ĐÃ CHỐT)

| Tool | Phím tắt | Mô tả |
|---|---|---|
| Select | V | Chọn/move line, hiện handles. Ẩn straight/zigzag buttons. |
| Draw | L | Click-click vẽ line |
| Split | - | Click vào line đang có → tách segment tại điểm đó |
| Scene | S | Thêm scene marker ngang |
| Text | T | Thêm text annotation box (draggable, resizable, color options) |
| Straight | - | Initial segment type = straight (ẩn khi Select mode) |
| Zigzag | - | Initial segment type = zigzag (ẩn khi Select mode) |
| Colors | - | 6 preset + custom color picker |
| Undo | Cmd+Z | Undo action cuối |
| Redo | Cmd+Shift+Z | Redo |

### Scene Marker — Visual Design

Đường ngang chạy ngang trang, gồm:
- Dashed horizontal line suốt chiều rộng trang
- Bên trái: box nhỏ "1/1 W" (scene/shot + shot size) có thể drag ngang
- Kế đó: số cảnh (1, 2...)  
- Kế đó: tên cảnh auto-extract từ PDF (INT./EXT. format)

### Text Annotation Tool

- Thêm text box tự do lên PDF canvas
- Draggable (kéo bất cứ đâu)
- Resizable (kéo góc để resize)
- Chọn được màu chữ
- Gõ text vào trong
- Lưu vào `annotations` table (type = 'drawing', fabric_json)
- Có thể xóa qua right-click/long-press

---

## Shotlist — Spec Chi Tiết (ĐÃ CHỐT 2026-03-31, CẬP NHẬT 2026-03-31)

### Shot numbering

- **Canvas label**: hiện `sceneNum/shotNum` theo vị trí line trên trang (computed client-side)
- **Shotlist tab (ShotlistPanel)**: hiện đầy đủ scene info (scene_number, location, INT/EXT...)
- Khi vẽ line xong, shot tự động được tạo với shot_number đúng thứ tự — không hiện "Untitled" nữa
  - Header shotlist item hiện: `Shot [shot_number]` nếu chưa có scene_number
  - Khi user fill vào scene_number → hiện đầy đủ

### Description 2 phần

**Phần 1 — Auto (từ PDF, chỉ straight segments):**
- Field `description` (DB) — hiển thị blur/mờ, read-only, max-height giới hạn, hover để unblur

**Phần 2 — User notes (phần chính):**
- Field `user_notes` (DB) — editable, hiển thị nổi bật

### Nút "→ Đến kịch bản"
- Click → navigate đến đúng page + flash highlight line trên canvas

### Undo/Redo
- Cmd+Z / Cmd+Shift+Z
- 2 nút visual (↩ ↪) trên toolbar
- Stack lưu: thêm line, xóa line, move line, add segment break, add annotation

---

## Quy tắc AI khi làm việc với project này

1. **Luôn thảo luận và confirm trước** khi generate code (theo CLAUDE.md)
2. **Update skill file này** ngay sau khi chốt spec/tính năng mới — để bất kỳ AI nào cũng nắm context
3. Không thay đổi tech stack đã chốt
4. Ưu tiên công cụ miễn phí
5. Quy trình: VS Code → GitHub → Cloudflare

---

## Files quan trọng

| File | Chức năng |
|---|---|
| `frontend/src/components/viewer/ScriptCanvas.tsx` | Fabric.js canvas, vẽ line, drag, context menu |
| `frontend/src/components/viewer/LineToolbar.tsx` | Toolbar tool selection, color picker |
| `frontend/src/components/viewer/PDFViewer.tsx` | PDF render, text extraction, zoom/page |
| `frontend/src/components/viewer/ShotlistPanel.tsx` | Shotlist UI, edit, export |
| `frontend/src/components/viewer/viewer.css` | Tất cả styles cho viewer |
| `workers/src/routes/lines.ts` | CRUD API cho script_lines |
| `workers/src/routes/shots.ts` | CRUD API cho shots + Google Sheets sync |
| `workers/src/routes/scenes.ts` | CRUD API cho scene_markers |
| `workers/migrations/` | D1 SQLite migrations |

---

## Pseudocode — Drawing Logic (Fabric.js)

```typescript
// State khi đang vẽ
type DrawingState = {
  phase: 'idle' | 'preview'  // idle: chưa click, preview: đã click 1 lần
  startX: number             // X cố định (normalized 0-1)
  startY: number             // Y điểm click 1 (normalized 0-1)
  currentSegments: Array<{ type: 'straight' | 'zigzag', y_start: number, y_end: number }>
  currentSegmentType: 'straight' | 'zigzag'  // type của đoạn đang kéo
}

// Click 1: đặt start point
onClick_first(y, x) {
  drawShotBox(x, y)           // ô vuông label shot
  drawStartBracket(x, y)      // gạch ngang ~12px
  state.phase = 'preview'
  state.startX = x
  state.startY = y
  state.currentSegmentType = selectedToolType  // straight hoặc zigzag
}

// Di chuột: ghost line
onMouseMove(y) {
  if (state.phase !== 'preview') return
  renderGhostLine(state.startX, state.startY, y, state.currentSegments, state.currentSegmentType)
}

// Tab: toggle segment type mid-draw
onTabKey(currentY) {
  if (state.phase !== 'preview') return
  state.currentSegments.push({ type: state.currentSegmentType, y_start: lastSegmentEnd, y_end: currentY })
  drawBracketAt(state.startX, currentY)   // bracket tại điểm chuyển
  state.currentSegmentType = toggle(state.currentSegmentType)
}

// Click 2: kết thúc
onClick_second(y) {
  state.currentSegments.push({ type: state.currentSegmentType, y_start: lastSegmentEnd, y_end: y })
  const continuesNext = y > 0.95
  if (continuesNext) {
    drawArrowDown(state.startX, y)
  } else {
    drawEndBracket(state.startX, y)
  }
  saveToDB({ x_position: state.startX, y_start: state.startY, y_end: y,
             segments_json: state.currentSegments, continues_to_next_page: continuesNext })
  state.phase = 'idle'
}

// Auto-detect continuation khi tạo line mới
onLineSaved(newLine) {
  const prevPageLine = linesOnPrevPage.find(l =>
    l.continues_to_next_page && Math.abs(l.x_position - newLine.x_position) < 0.03
  )
  if (prevPageLine) {
    newLine.continues_from_prev_page = true
    // Update DB
  }
}
```
