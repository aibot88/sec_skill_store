---
name: robot-bi-dev
version: 1.0.0
description: >
  Master skill cho dự án Robot Bi. Kết hợp TDD, diagnosis loop, security audit,
  git safety, UI prototyping, và session hygiene — tất cả được calibrate cho
  codebase Python/FastAPI/SQLite/Groq của Robot Bi. Trigger khi: implement feature
  mới, debug bug, security review, làm UI frontend/robot display, hoặc bắt đầu
  session dev bất kỳ.
---

# Robot Bi — Master Dev Skill

Skill này là bộ quy trình chuẩn cho mọi session phát triển Robot Bi.
Đọc từ đầu đến cuối lần đầu. Sau đó nhảy thẳng vào phần phù hợp với task.

---

## 0. Session Start — Bắt buộc mỗi session

Trước khi chạm bất kỳ file nào, thực hiện đủ 3 bước sau:

```bash
# 1. Đọc nguồn sự thật
cat PROJECT.md          # hoặc CLAUDE.md / AGENTS.md nếu trong Claude Code / Codex
cat .claude/handoff.md  # snapshot trạng thái gần nhất

# 2. Kiểm tra baseline — phải PASS 100% trước khi bắt đầu
python tests/run_tests.py

# 3. Kiểm tra PROTECTED FIXES trong PROJECT.md
# Nếu task đụng đến bất kỳ module nào trong danh sách PROTECTED FIXES → đọc kỹ lại
```

**Nếu baseline không phải 374/374 PASS: dừng lại, báo cho user, fix trước.**

---

## 1. Implement Feature Mới — TDD Loop

*Từ `tdd` (mattpocock) + `diagnose` (mattpocock)*

### Nguyên tắc cốt lõi

- Test verify **behavior qua public interface**, không test implementation details.
- **Vertical slices**: một test → một implementation → repeat. Không viết 5 test rồi mới implement.
- Test name phải đọc như spec: `test_homework_marked_when_child_mentions_bai_tap`, không phải `test_function_x`.

### Workflow

**Bước 1 — Identify seam**

Trước khi viết bất kỳ code nào, xác định:
- Public interface mới là gì? (function signature, API endpoint, WebSocket event)
- Behavior nào cần test nhất? (happy path, failure mode, edge case)
- Module nào trong `src/` sẽ bị chạm? Có trong PROTECTED FIXES không?

**Bước 2 — Tracer bullet**

```python
# Viết 1 test đơn giản nhất xác nhận end-to-end path hoạt động
# Đặt vào tests/run_tests.py, group mới: # == GROUP N: [Feature Name] ===
def test_N_1_[feature]_basic():
    from src.[module] import [Class]
    obj = [Class]()
    result = obj.[method]([input])
    assert result == [expected]

test("N.1 [Feature] basic smoke", test_N_1_[feature]_basic)
```

Chạy: `python tests/run_tests.py` → phải thấy FAIL rõ ràng.

**Bước 3 — Implement minimal**

Viết đủ code để test pass. Không thêm feature chưa có test.

**Bước 4 — Repeat**

Lặp lại cho mỗi behavior. Thêm test → FAIL → implement → PASS.

**Bước 5 — Regression check**

```bash
python tests/run_tests.py
# Phải >= số test trước đó. Nếu có test cũ fail → FIX TRƯỚC KHI TIẾP TỤC.
```

### Robot Bi — Patterns thường gặp

```python
# Test FastAPI endpoint
def test_endpoint_exists():
    from src.api.server import app
    paths = [r.path for r in app.routes]
    assert "/api/your/endpoint" in paths

# Test module import không crash
def test_import():
    from src.module.submodule import ClassName
    assert ClassName is not None

# Test behavior qua public interface (không mock internal)
def test_behavior():
    from src.infrastructure.database.db import init_db
    # dùng DB riêng — không bao giờ dùng runtime/robot_bi.db trong test
    obj = YourClass()
    result = obj.do_thing("input")
    assert "expected" in result
```

### Quy tắc test Robot Bi

- Không bao giờ dùng `runtime/robot_bi.db` trong test — luôn dùng temp DB như `run_tests.py` đã setup.
- Mỗi group test mới: comment header `# == GROUP N: [Name] ===` + `print("\n[Group N] [Name]")`.
- Test không được require mic, camera, loa, Ollama, internet — chạy offline hoàn toàn.
- Nếu test cần LLM: mock response hoặc test logic không phụ thuộc LLM output cụ thể.

---

## 2. Debug Bug — Diagnosis Loop

*Từ `diagnose` (mattpocock)*

### Phase 1 — Build feedback loop (đây là kỹ năng chính)

Trước khi đọc bất kỳ dòng code nào, xây dựng signal pass/fail tự động.

Thử theo thứ tự:

1. **Failing test** trong `tests/run_tests.py` — preferred vì tích hợp vào CI.
2. **Script curl/HTTP** gọi FastAPI endpoint đang có vấn đề:
   ```bash
   curl -X POST https://localhost:8443/api/your/endpoint \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key": "value"}' -k 2>&1
   ```
3. **Throwaway harness** cho audio/STT/TTS bugs:
   ```python
   # prototype/debug_audio.py — xóa sau khi fix
   import asyncio
   from src.audio.output.mouth_tts import MouthTTS
   tts = MouthTTS()
   asyncio.run(tts.speak("test", chunk_index=0))
   print("OK")
   ```
4. **Log diff** cho non-deterministic bugs (threading, audio queue):
   ```python
   # Thêm tag debug vào log — xóa sau fix
   import logging
   logger.debug("[DEBUG-a4f2] audio_queue size=%d", audio_queue.qsize())
   ```

**Nếu không tạo được feedback loop → dừng, báo user, không đoán mò.**

### Phase 2 — Hypothesise (trước khi test bất kỳ hypothesis nào)

Liệt kê 3-5 hypothesis theo format:

> "Nếu [X] là nguyên nhân, thì [thay đổi Y] sẽ làm bug biến mất / [thay đổi Z] sẽ làm bug tệ hơn."

Check PROTECTED FIXES: nếu hypothesis liên quan đến audio mom talk, camera delay, SafetyFilter, RAG threshold, JWT flow → xem kỹ implementation hiện tại trước khi thay đổi.

### Phase 3 — Instrument & Fix

- Thay đổi **một biến một lần**.
- Tag tất cả debug log: `[DEBUG-xxxx]` để cleanup dễ sau fix.
- Viết regression test trước fix — nếu có seam phù hợp.

### Phase 4 — Cleanup

```bash
grep -r "DEBUG-" src/   # phải trả về 0 kết quả
python tests/run_tests.py  # phải >= baseline trước khi debug
```

### Robot Bi — Bug patterns đã gặp

| Symptom | Nguyên nhân thường gặp | Kiểm tra |
|---|---|---|
| Audio bị echo / delay | Thread audio queue không drain | `audio_queue.qsize()` + `pygame.Channel` |
| STT không nhận | Mic device không đúng | `MIC_DEVICE` trong `.env` |
| API 401 | JWT expired / missing Bearer | `verify_access_token()` trong `auth.py` |
| Test fail sau refactor | Import path `src_brain.*` cũ | `grep -r "src_brain" src/` |
| Camera freeze | `CAP_PROP_BUFFERSIZE` | Thread riêng + queue bridge |
| RAG nhớ sai | family_id filter bị bỏ qua | `where={"family_id": fid}` trong query |

---

## 3. Security Review

*Từ `security-best-practices` (openai/Codex)*

### Chỉ trigger khi

- User yêu cầu security review rõ ràng.
- Thêm endpoint mới expose ra internet.
- Thay đổi auth flow, JWT, rate limiting.
- Chuẩn bị deploy lên Ubuntu thật (public).

### Stack Robot Bi cần kiểm tra

**Backend (Python + FastAPI):**
- JWT: `create_access_token` HS256, secret từ `.env` — không hardcode, không có default value.
- Argon2id: `verify_password(hash, plaintext)` — check thứ tự đúng.
- Rate limiting: `login_attempts` table — 5 lần sai → lock 15 phút.
- SQL: tất cả query dùng parameterized, không string format.
- Family isolation: mọi DB query có `family_id` filter.
- Logging: không log nội dung hội thoại ở INFO/WARNING — chỉ DEBUG.

**Frontend (JavaScript thuần):**
- `Authorization: Bearer <token>` attach vào mọi API call.
- Token lưu `localStorage` — không expose qua URL.
- WebSocket connect với `?token=` query param.
- XSS: không dùng `innerHTML` với user input.

### Report format

Khi viết security report → lưu vào `docs/security_report_YYYY-MM-DD.md`:

```markdown
# Security Review — [Date]

## Executive Summary
[2-3 câu tóm tắt]

## CRITICAL
### [C1] [Tên vấn đề]
**File**: `src/path/file.py`, line [N]
**Impact**: [1 câu impact]
**Fix**: [code snippet]

## HIGH
### [H1] ...

## MEDIUM / LOW
...
```

Sau khi viết report → fix từng issue một, chạy `python tests/run_tests.py` sau mỗi fix.

### Không report là security issue

- Thiếu TLS trong môi trường dev (Robot Bi dùng self-signed + Cloudflare tunnel).
- PIN auth chạy song song JWT — đây là design có chủ đích.

---

## 4. UI / Frontend — Robot Display & Parent App

*Từ `frontend-design` (anthropics) + `prototype` (mattpocock) + `webapp-testing` (anthropics)*

### Khi làm UI mới

**Bước 1 — Xác định question trước khi code**

- "Logic/state machine có đúng không?" → **prototype logic** (terminal app nhỏ, throwaway).
- "Giao diện trông thế nào?" → **prototype UI** (nhiều variants, toggle bằng URL param).
- "Feature đã hoạt động chưa?" → **test với Playwright**.

**Bước 2 — Prototype nếu cần (throwaway)**

```
frontend/robot_display/prototype_[feature].html  ← đặt gần nơi sẽ dùng
```

Rules prototype:
- Một lệnh để chạy: `python -m http.server 8080` rồi mở file.
- Không có DB, không có API call thật — state trong memory.
- Không test, không error handling.
- Xóa sau khi answer câu hỏi, hoặc absorb vào production code.

**Bước 3 — Design direction**

Trước khi viết production code, commit rõ aesthetic direction:

- **Robot Display** (`frontend/robot_display/index.html`): Playful, futuristic, dành cho trẻ em 5-12 tuổi. Màu sắc sống động. Animation mượt. SVG eyes có expressiveness cao. Không generic "AI dashboard" style.
- **Parent App** (`frontend/parent_app/index.html`): Clean, functional, tin tưởng được. Dành cho phụ huynh. Thông tin rõ ràng. Dark/light mode. Không cluttered.

Tránh: Inter font, purple gradient trên white, uniform rounded corners — đây là "AI slop".

**Bước 4 — Test với Playwright**

```python
# tests/test_ui_[feature].py — chạy riêng, không phải part của run_tests.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Robot Display: file:// URL (static HTML)
    page.goto(f"file:///path/to/frontend/robot_display/index.html")
    page.wait_for_load_state("networkidle")
    
    # Parent App: cần server chạy
    # Chạy: uvicorn src.api.server:app --port 8443 trước
    page.goto("https://localhost:8443")
    page.wait_for_load_state("networkidle")
    
    # Reconnaissance: screenshot trước khi interact
    page.screenshot(path="/tmp/debug_ui.png", full_page=True)
    
    # Interact
    page.locator("button#[id]").click()
    page.wait_for_selector("[selector]")
    
    # Assert
    assert page.locator("[result_selector]").is_visible()
    
    browser.close()
```

**Robot Display patterns quan trọng:**

```javascript
// Thêm mode mới vào robot_display/index.html
const MODES = {
  your_mode() {
    clearAll();              // luôn gọi trước
    setAccent('#color');     // màu accent cho mode
    stage.classList.add('your_mode');
    // animation logic
    registerFaceTimeout(() => setMode('idle'), 3000);  // auto-return về idle
  }
};

// Test mode mới từ console:
// RobotDisplay.setMode('your_mode')
// RobotDisplay.setEmotion('happy')
```

### Animation guidelines Robot Display

- Dùng CSS `@keyframes` cho loop animations (idle, breathing, pulse).
- Dùng `registerFaceTimeout()` không phải `setTimeout()` trực tiếp — quản lý cleanup.
- SVG eye: `transform-box: fill-box; transform-origin: center` cho scale animations.
- Không dùng physics engine hay heavy library — pure CSS + vanilla JS.

---

## 5. Git Safety — Bảo vệ khỏi lệnh nguy hiểm

*Từ `git-guardrails-claude-code` (mattpocock)*

### Cài đặt (một lần)

```bash
mkdir -p .claude/hooks
cat > .claude/hooks/block-dangerous-git.sh << 'EOF'
#!/usr/bin/env bash
input=$(cat)
cmd=$(echo "$input" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

BLOCKED=(
  "git push"
  "git reset --hard"
  "git clean -f"
  "git branch -D"
  "git checkout ."
  "git restore ."
)

for pattern in "${BLOCKED[@]}"; do
  if echo "$cmd" | grep -qF "$pattern"; then
    echo "[BLOCKED] Lệnh nguy hiểm: $pattern" >&2
    echo "Hãy xác nhận với user trước khi chạy lệnh git này." >&2
    exit 2
  fi
done
exit 0
EOF
chmod +x .claude/hooks/block-dangerous-git.sh
```

Thêm vào `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

### Git workflow Robot Bi

```bash
# Trước khi commit
python tests/run_tests.py     # phải 100% PASS
python sync.py                # sync CLAUDE.md + AGENTS.md

# Commit message format
git commit -m "feat(module): mô tả ngắn

- Thêm: X
- Fix: Y
- Tests: Group N (M tests)"

# Không push trực tiếp từ Claude Code — xác nhận với user
```

---

## 6. Session End — Bắt buộc trước khi kết thúc

```bash
# 1. Chạy full test suite lần cuối
python tests/run_tests.py
# Phải >= baseline đầu session

# 2. Update PROJECT.md
# - Session gần nhất: ngày, những gì đã làm, test count
# - Nếu có thay đổi stack/architecture → update bảng stack
# - Nếu có bug mới phát hiện → thêm vào "Vấn đề đã biết"

# 3. Update handoff.md
# - TRẠNG THÁI HIỆN TẠI: cập nhật test count
# - VIỆC CẦN LÀM TIẾP: cập nhật nếu có thay đổi

# 4. Tạo changelog
# changelog/YYYY-MM-DD-[tên-session].md
# Format: ## Summary, ## Changes (per file), ## Verification

# 5. Sync
python sync.py
```

---

## 7. Quick Reference — Robot Bi Cheat Sheet

### Entry points & files quan trọng

| Mục đích | File |
|---|---|
| Chạy robot | `python src/main.py` |
| Chạy test | `python tests/run_tests.py` |
| Sync docs | `python sync.py` |
| AI engine | `src/ai/ai_engine.py` — `stream_chat(messages)` |
| STT | `src/audio/input/ear_stt.py` |
| TTS | `src/audio/output/mouth_tts.py` |
| Safety | `src/safety/safety_filter.py` — luôn post-LLM, pre-TTS |
| API server | `src/api/server.py` + `src/api/routers/` |
| Database | `src/infrastructure/database/db.py` → `runtime/robot_bi.db` |
| RAG | `src/memory/rag_manager.py` → `runtime/chroma_db/` |
| Robot UI | `frontend/robot_display/index.html` |
| Parent App | `frontend/parent_app/index.html` |
| Nguồn sự thật | `PROJECT.md` → đọc trước mọi thứ |

### LLM stack (không thay đổi trừ khi có lệnh rõ ràng)

- Primary: Groq `llama-3.3-70b-versatile` (~400 tok/s)
- Fallback: Gemini `gemini-2.5-flash-lite`
- Call qua: `stream_chat(messages)` trong `src/ai/ai_engine.py`

### Quy tắc tuyệt đối (không bao giờ vi phạm)

1. `PROJECT.md` là nguồn sự thật duy nhất — không sửa `CLAUDE.md`/`AGENTS.md` trực tiếp.
2. `python tests/run_tests.py` phải PASS 100% sau mỗi thay đổi.
3. Không bao giờ hardcode `JWT_SECRET_KEY` hay API key.
4. `SafetyFilter` phải chạy post-LLM, pre-TTS — không bỏ qua.
5. Mọi DB query có `family_id` filter — không query toàn bộ data.
6. Test không được require hardware (mic, camera, loa).
7. Không sửa PROTECTED FIXES mà không đọc kỹ implementation hiện tại.

### Lệnh debug nhanh

```bash
# Kiểm tra import path còn src_brain không
grep -r "src_brain" src/ tests/

# Kiểm tra debug log còn không
grep -r "DEBUG-" src/

# Kiểm tra hardcoded secrets
grep -rn "secret\|password\|api_key" src/ --include="*.py" | grep -v ".env" | grep -v "os.getenv"

# List tất cả API routes
python -c "from src.api.server import app; [print(r.path) for r in app.routes if hasattr(r,'path')]"

# Test DB sạch
python -c "from src.infrastructure.database.db import init_db; init_db(); print('DB OK')"
```
