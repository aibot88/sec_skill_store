---
name: assetcore-audit
description: >
  Audit, tái cấu trúc và sửa lỗi AssetCore — kiểm tra production-readiness toàn module
  (BE 3-tier, FE views, workflow, fixtures, tests, docs, permissions, audit trail),
  đồng thời review security (RBAC, DocPerm, whitelist hygiene, SQL injection, CSRF,
  vendor isolation, compliance NĐ98/WHO HTM).
  Dùng khi user nói "audit module", "module IMM-XX sẵn sàng chưa", "thiếu gì",
  "module gap analysis", "release checklist", "kiểm tra module", "tái cấu trúc",
  "refactor", "code bị lỗi", "fix bug IMM-XX", "phân quyền sai", "permission", "role",
  "audit trail", "security review", "vendor không được thấy data", "SQL injection",
  "CSRF", "rò rỉ data", "compliance". Ưu tiên skill này trước mọi deployment module mới.
---

# AssetCore Audit — Module Readiness & Security

Skill này bao 2 nhiệm vụ: **Module Audit** (production-readiness) + **Security Review**.

---

## Phần 1 — Module Audit (8-pillar checklist)

## NGUYÊN TẮC BẤT BIẾN — UI Completeness

### UC-1: Mọi module PHẢI có Create button

Mỗi list page phải có button tạo mới (không chỉ hiển thị danh sách). Kiểm tra:
- List view có "Tạo mới" / "+ New" / "+ [Tên bản ghi]" button
- Button gọi được modal hoặc navigate đến form mới
- Form tạo mới có đủ fields và submit được

**Ngoại lệ duy nhất**: các page chỉ đọc thuần túy (vd: audit trail, reports).

### UC-2: Mọi bản ghi PHẢI có trang chi tiết với workflow actions

Mỗi bản ghi trong list phải:
- Có link/button "Chi tiết" hoặc click row dẫn đến URL chi tiết (vd: `/capas/:id`)
- Trang chi tiết hiển thị tất cả fields
- Trang chi tiết có workflow action buttons phù hợp với state
- State transitions phải khép kín (Draft → Approved → Active → Closed; không để bản ghi "kẹt" ở một state không có action)

**Khi audit FE**: navigate đến trang chi tiết của 1 bản ghi ở mỗi state → verify buttons.

### UC-3: Asset detail — tất cả tabs phải có dữ liệu hoặc empty state rõ ràng

Trang `/assets/:id` có các tabs: Thông tin, Khấu hao, Lịch sử, KPI, Audit Trail. Mỗi tab phải:
- Hiển thị dữ liệu nếu có
- Hiển thị "Chưa có dữ liệu" rõ ràng nếu chưa có — không để trống hoàn toàn
- Widget Ngừng máy: hiển thị số liệu thực (0 nếu chưa có event, không blank)

### UC-4: Tất cả Link fields phải hiển thị human-readable name

Các trường Link hiển thị cho user phải dùng display name, không phải DocType ID:
- Vendor/Supplier: tên công ty, không phải `SUP-2026-XXXXX`
- Asset: asset_name || asset_code, không phải `ACC-ASS-2026-XXXXX`
- User: full_name, không phải `email@domain.com`
- Department: tên khoa, không phải mã khoa

BE phải enrich `*_name` trong response; FE dùng `x.xxx_name || x.xxx`.

### UC-5: Naming series PHẢI đúng format

DocType có naming series phải:
- `"naming_rule": "Naming Series"` (không phải `"Expression (old style)"`)
- `"autoname": "PREFIX-.YYYY.-.#####"` (không có `format:` prefix)
- Verify bằng cách tạo bản ghi mới và check tên trả về — nếu trả về literal `"PREFIX-.YYYY.-.#####"` thì sai

---

### Mục đích
Dùng trước:
- Tag release (`v3.x.y`)
- Promote module Wave-Planned → Wave-Live
- Cut deployment ticket
- Đóng sprint deliver IMM-XX

Skill này **chỉ verify** — không implement. Khi phát hiện gap, chuyển sang `assetcore-be`, `assetcore-fe`, `assetcore-test`, `assetcore-deploy`.

### 8 pillars audit

#### Pillar 1 — DocType schema
- [ ] `module: "AssetCore"` set
- [ ] `autoname` dùng prefix có ý nghĩa
- [ ] `track_changes: 1`
- [ ] Status fields: `read_only: 1` + `no_copy: 1`
- [ ] Timestamp fields: `read_only: 1` + `no_copy: 1`
- [ ] DocPerm đủ 2+ operational roles
- [ ] Không có field service dùng nhưng không có trong JSON

```bash
# Verify fields tồn tại
grep -n "doc\." services/immXX.py | grep -v "frappe\|get_doc\|db\." | head -20
```

#### Pillar 2 — Service layer
- [ ] 3-tier tách đúng (không có business logic trong API, không có HTTP trong service)
- [ ] Mọi mutating function có permission check ở đầu
- [ ] `require_role(...)` dùng constant từ `Roles`, không hardcode
- [ ] Không có `except: pass` hay `except Exception: pass`
- [ ] Không gọi `frappe.db.*` trực tiếp từ service (đi qua repo)

```bash
# Tìm bare except
grep -n "except:" services/immXX.py | grep -v "ServiceError\|Exception as\|frappe"
# Tìm direct DB calls trong service
grep -n "frappe\.db\." services/immXX.py | grep -v "set_value\|commit"
```

#### Pillar 3 — Repository
- [ ] `<Name>Repo(BaseRepository)` tồn tại
- [ ] Không có raw SQL trừ khi thực sự cần join phức tạp
- [ ] Import từ `assetcore/repositories/__init__.py`, không trực tiếp từ `_repo.py`

#### Pillar 4 — API layer
- [ ] Tất cả endpoints có `@frappe.whitelist()`
- [ ] Mutating endpoints có `methods=["POST"]`
- [ ] Function names khớp với `docs/imm-XX/05_API_Specification.md`
- [ ] Không có business logic trong API handlers
- [ ] Pagination params cast: `int(page)`, `int(page_size)`
- [ ] **Display name enrichment**: mọi `list_*` endpoint có Link field hiển thị → phải gọi `_enrich(items, field, doctype, display_field)` để thêm `*_name`; mọi `get_*` detail endpoint phải enrich tương tự (không chỉ list)

```bash
# Verify whitelist endpoints
grep -n "@frappe.whitelist" api/immXX.py
# Compare với spec
grep "endpoint\|POST\|GET" docs/imm-XX/05_API_Specification.md | head -20
# Tìm get_* endpoint thiếu enrich (trả frappe.get_doc().as_dict() nhưng có Link field user-visible)
grep -n "frappe.get_doc.*as_dict\|get_doc.*as_dict" api/immXX.py
```

#### Pillar 5 — Workflow
- [ ] Workflow JSON tồn tại trong `assetcore/assetcore/workflow/imm_XX_<name>_workflow.json`
- [ ] `name == workflow_name` trong JSON
- [ ] `is_active: 1` set
- [ ] docstatus transitions valid (`0→0`, `0→1`, `1→1`, `1→2` only)
- [ ] Workflow trong `hooks.py` fixtures — đủ CẢ 3 lists (Workflow + State + Action)
- [ ] `EXPECTED_WORKFLOWS` updated trong `tests/test_workflows.py`

```bash
# Verify 3 fixture lists — workflow name trong từng list phải match JSON
grep -A20 '"dt": "Workflow"' assetcore/hooks.py
grep -A50 '"dt": "Workflow State"' assetcore/hooks.py
grep -A30 '"dt": "Workflow Action Master"' assetcore/hooks.py

# Đếm states + transitions từ workflow JSON (không đoán)
python3 -c "import json; d=json.load(open('assetcore/assetcore/workflow/imm_XX_<name>_workflow.json')); print('states:', len(d['states']), 'transitions:', len(d['transitions']))"

# Verify tất cả state names trong hooks.py Workflow State list
python3 -c "import json; d=json.load(open('assetcore/assetcore/workflow/imm_XX_<name>_workflow.json')); [print(s['state']) for s in d['states']]"
```

#### Pillar 6 — FE (Frontend)
- [ ] `api/immXX.ts` — all functions typed `Promise<T>`, không `Promise<ApiResponse<T>>`
- [ ] `stores/immXX.ts` — Pinia setup syntax; không re-export API namespace
- [ ] Views: tri-branch `v-if="loading"` / `v-else-if="error"` / `v-else`
- [ ] `catch (e: unknown)` + `e instanceof Error ? e.message : String(e)` — không `catch (e: any)`
- [ ] Routes đúng trong `router/index.ts` với `meta.moduleId`
- [ ] Launcher tile `disabled: false` + route tồn tại

**FE Display Quality (bắt buộc kiểm tra):**
- [ ] **Display names, không phải system codes**: mọi trường Link hiển thị cho user phải dùng human-readable name, không phải DocType id:
  - Supplier/Vendor: dùng `supplier_name || supplier`, không phải `SUP-2026-XXXXX`
  - Asset: dùng `asset_name || asset`, không phải `ACC-ASS-2026-XXXXX`
  - User: dùng `full_name || user`, không phải `email@domain`
  - BE phải enrich `*_name` vào response; FE dùng pattern `x.xxx_name || x.xxx`
- [ ] **Status values FE = BE constants**: grep `_STATUS_*` trong service layer, verify mọi `STATUS_COLOR`, `STATUS_LABEL`, `allowed_transitions.includes(...)`, `canXxx computed` dùng ĐÚNG string đó
  - Lỗi hay gặp: FE dùng `"Under Investigation"` nhưng BE constant là `"In Progress"` → tất cả workflow buttons ẩn
- [ ] **`allowed_transitions.includes()` dùng exact BE string**: lấy từ `_VALID_TRANSITIONS` dict, không đặt tên thân thiện
- [ ] **Select options FE = DocType JSON options**: grep DocType JSON field `options`, so với `<select>` options trong form — mismatch gây validation error
- [ ] **`useFormDraft` cache**: sau khi fix options, test với fresh browser session hoặc clear localStorage — draft cache giữ giá trị cũ không hợp lệ
- [ ] **Sidebar không che content**: test viewport ≥ 1280px; sidebar fixed z-40 intercept clicks ở viewport nhỏ

**UI Completeness (bắt buộc audit):**
- [ ] **List page có Create button**: không có → 🟠 HIGH gap
- [ ] **Detail page có workflow buttons**: mỗi non-terminal state phải có ≥ 1 action button → không có → 🔴 CRITICAL (user bị kẹt)
- [ ] **KPI/stats tabs có data thực**: nếu có work orders nhưng uptime = 0/null → 🟠 HIGH (KPI service broken)
- [ ] **Audit trail tab hiển thị events**: empty khi có actions → 🟠 HIGH
- [ ] **Tabs không empty giả**: tất cả tabs phải fetch từ API, không hardcode empty

**Procurement Plans — kiểm tra thêm:**
- [ ] `/procurement-plans` list page có Create button → tạo plan mới được
- [ ] Detail page `/procurement-plans/:id` có đủ: tổng ngân sách, tỷ lệ sử dụng (allocated/budget), danh sách NR đã gắn vào plan
- [ ] Tỷ lệ sử dụng không hiển thị 0% khi đã có NR gắn vào plan — nếu 0% → kiểm tra BE roll-up logic
- [ ] Workflow buttons đúng state: Draft → Submit → Approve → Active → Close

**Asset Detail — kiểm tra thêm:**
- [ ] Tab Thông tin: tất cả fields điền đầy đủ, vendor hiển thị tên công ty (không mã SUP-XXXX)
- [ ] Tab Khấu hao: hiển thị schedule nếu purchase_price ≠ 0; hiển thị "Chưa có dữ liệu" nếu chưa nhập giá
- [ ] Tab Lịch sử: ít nhất 1 lifecycle event sau khi asset được tạo/cài đặt
- [ ] Tab KPI: uptime%, MTBF, MTTR hiển thị số liệu hoặc "Chưa đủ dữ liệu để tính" — không để trống hoàn toàn
- [ ] Widget Ngừng máy: hiển thị "0 sự kiện ngừng máy" nếu chưa có downtime log (không blank, không error)
- [ ] Audit Trail tab: có ít nhất 1 entry từ lúc tạo asset — empty hoàn toàn → 🟠 HIGH

```bash
cd frontend && npx tsc --noEmit 2>&1 | head -30
# Grep để verify status strings:
grep -n "_STATUS_\|STATUS_COLOR\|STATUS_LABEL\|allowed_transitions" services/immXX.py views/immXX/*.vue
```

#### Pillar 7 — Tests
- [ ] `test_immXX.py` tồn tại
- [ ] Mỗi BR-XX-NN có ≥ 1 happy + 1 negative test
- [ ] Workflow smoke test pass
- [ ] Tests chạy được trên fresh site

```bash
bench --site miyano run-tests --module assetcore.tests.test_immXX
bench --site miyano run-tests --module assetcore.tests.test_workflows
```

#### Pillar 8 — Docs & Audit trail
- [ ] `docs/imm-XX/` có đủ 9 files (README + 02→09)
- [ ] `07_Testing_QA.md` có bảng UAT scenarios
- [ ] Mọi state transition gọi `log_audit_event(...)` — không bypass
- [ ] Không có module-local `_log_audit` hay `_create_lifecycle_event` (phải dùng canonical)

**Realistic data check (dùng trong UAT, không chỉ unit test):**
- [ ] Test data dùng tên thiết bị y tế thực, không phải "_Test", "sample"
- [ ] Work orders có complete fields: asset, technician, description thực tế
- [ ] KPI/stats được generate từ data thực (không mock 0)
- [ ] Audit trail có events thực sau khi tạo/sửa/chuyển trạng thái

### Severity grading
- 🔴 **Critical** — app crashes, data corruption, security hole. Block release.
- 🟠 **High** — feature broken hoặc audit gap. Fix before Wave goes Live.
- 🟡 **Medium** — UX degraded, missing validation. Fix in next sprint.
- 🟢 **Low** — code smell, doc gap. Backlog.

### Audit report format
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Module Audit — IMM-XX
  Date: YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pillar 1 DocType   : ✅ / ❌ [gaps]
Pillar 2 Service   : ✅ / ❌ [gaps]
Pillar 3 Repo      : ✅ / ❌ [gaps]
Pillar 4 API       : ✅ / ❌ [gaps]
Pillar 5 Workflow  : ✅ / ❌ [gaps]
Pillar 6 FE        : ✅ / ❌ [gaps]
Pillar 7 Tests     : ✅ / ❌ [gaps]
Pillar 8 Docs/Audit: ✅ / ❌ [gaps]

VERDICT: ✅ PRODUCTION-READY / ❌ NOT READY
Critical gaps: [list]
Action items: [list với owner]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phần 2 — Security Review

### Threat model
1. **Privilege escalation** — Technician trigger admin-only action
2. **Vendor data leakage** — Hospital A thấy data Hospital B
3. **Audit trail tampering** — backdating hoặc xóa lifecycle record
4. **Session hijacking** — CSRF, stale token
5. **Injection** — SQL via raw `frappe.db.sql`, XSS in descriptions
6. **Mass exfiltration** — unbounded list endpoint dump toàn bộ table

### Security checklist

#### Layer 1 — Service permission gate
```python
from assetcore.services.shared.permissions import require_role
from assetcore.services.shared.constants import Roles

def assign_technician(name: str, *, technician: str):
    require_role(Roles.CAN_CREATE_WO, "Không đủ quyền giao việc")
    # ...
```
- [ ] Mọi mutating service function có `require_role(...)` ở đầu
- [ ] Roles từ `Roles` constant, không hardcode string
- [ ] Permission check TRƯỚC khi đọc record (không để data leak qua error message)

#### Layer 2 — DocPerm (defense in depth)
```bash
# Verify permissions trong JSON
grep -A10 '"permissions"' assetcore/assetcore/doctype/<name>/<name>.json
```
- [ ] `delete: 0` cho mọi role trên audit trail DocTypes
- [ ] Không có `System Manager` trong non-admin DocType permissions
- [ ] `read: 1` tối thiểu cho operational roles

#### Whitelist hygiene
```bash
# Tìm endpoints thiếu permission gate
grep -B2 "@frappe.whitelist" api/immXX.py | grep -v "require_role\|#"
```
- [ ] Mọi POST endpoint có `methods=["POST"]`
- [ ] Mọi endpoint đọc data nhạy cảm có `require_role` hoặc filter theo `frappe.session.user`
- [ ] Pagination params bounded: `min(int(page_size), 200)` — không cho dump unlimited

#### Audit trail integrity
```bash
# Tìm bypass (insert trực tiếp thay vì log_audit_event)
grep -rn "doctype.*IMM Audit Trail" assetcore/ | grep -v "log_audit_event\|test_"
```
- [ ] Không có code insert `IMM Audit Trail` trực tiếp
- [ ] Không có `frappe.delete_doc("IMM Audit Trail", ...)` ngoài test teardown
- [ ] `delete: 0` trong DocPerm cho `IMM Audit Trail`

#### Input validation & Injection
```bash
# Tìm raw SQL với string interpolation
grep -n "frappe\.db\.sql" assetcore/ -r | grep -v "?.*%s\|:%(.*)" | grep "%\|format\|f\""
```
- [ ] Raw SQL dùng parameterized queries (`%s`, không f-string)
- [ ] User-entered text không render as HTML (escape hoặc dùng Jinja `{{ value | e }}`)
- [ ] File upload qua `@frappe.whitelist(methods=["POST"])` với MIME type check

#### Vendor isolation (multi-tenant)
```python
# Mọi list query phải filter theo tenant
filters["hospital_site"] = frappe.local.site
# Hoặc check ownership:
if doc.created_by_hospital != frappe.local.site:
    frappe.throw("Không có quyền truy cập")
```
- [ ] Mọi `list_*` endpoint filter theo `hospital_site` hoặc user scope
- [ ] Vendor Engineer không thấy data của hospital khác

### Security report format
```
Security Review — IMM-XX / [endpoint/feature]
🔴 CRITICAL: [issue + exploit path + fix]
🟠 HIGH: [issue + fix]
🟡 MEDIUM: [issue + fix]
Verdict: SECURE / NEEDS FIX
```

---

## Khi nào dùng skill nào tiếp theo

| Audit phát hiện | Skill tiếp |
|---|---|
| BE layer gap (service, repo, API) | `assetcore-be` |
| FE layer gap (views, store, types) | `assetcore-fe` |
| Test missing | `assetcore-test` |
| Deployment issue | `assetcore-deploy` |
| Doc gap | `assetcore-doc` |

---

## Lessons Learned 2026-05 — Audit checklist mở rộng

Khi audit 1 module, bắt buộc check các pattern bug đã gặp:

### A. Backend audit checks

```bash
# A1. Frappe 417 risk — int|None trong GET whitelist
grep -rn "int | None\|float | None" assetcore/api/ \
  | xargs -I{} grep -B2 "@frappe.whitelist" {} 2>/dev/null

# A2. Schema mismatch — service ref field không có trong DocType
# Cho mỗi service file, list field assignments rồi cross-check với DocType JSON
grep -E "doc\.\w+ =" assetcore/services/<module>.py | sort -u

# A3. Workflow action label inconsistency
diff <(python3 -c "import json; d=json.load(open('workflow.json')); print(sorted(t['action'] for t in d['transitions']))") \
     <(grep -E "transition.*action" assetcore/api/<module>.py)

# A4. Response enrichment — Link field phải có _name companion
grep -E "doctype.*Link" <doctype>.json
# Verify api/<module>.py có batch _enrich() cho từng Link field

# A5. Gate validator existence — mỗi gate G0X phải có function _validate_gate_g0X
grep -E "^def _validate_gate_g" assetcore/services/<module>.py
```

### B. Frontend audit checks

```bash
# B1. TRANSITIONS_BY_STATE completeness — đếm states vs entries trong map
states=$(python3 -c "import json; d=json.load(open('workflow.json')); print(len(d['states']))")
entries=$(grep -c "':\\s*\\[" frontend/src/views/<module>/DetailView.vue)
echo "States: $states | Map entries: $entries"  # phải bằng nhau (trừ terminal)

# B2. List page thiếu create button
for f in frontend/src/views/**/[A-Z]*ListView.vue; do
  grep -L "Tạo\|+ \|create\|new" "$f"
done

# B3. Hardcoded internal codes trong template
grep -rn "AC-SUP-\|AC-DEPT-\|AC-ASSET-\|IMM-MDL-" frontend/src/views/ \
  | grep -v "\.test\.\|\.spec\."

# B4. Link field as text input (bug pattern)
# Tìm <input type="text"> bind v-model có tên trùng Link field
grep -E "<input.*type=\"text\".*supplier|department|vendor|model" frontend/src/views/

# B5. StatusBadge sync — mỗi BE state có entry trong formatters
grep -E "^\s+'[A-Z][a-zA-Z\s]+':" assetcore/assetcore/workflow/*.json
grep "STATUS_LABEL\|STATUS_COLOR" frontend/src/utils/formatters.ts
```

### C. UI audit checks (Playwright)

Cho mỗi page trong module:

```
1. browser_navigate → list page
2. browser_snapshot → grep "Tạo" || "+ "  # phải có button create
3. browser_console_messages(error)  # phải 0 errors
4. browser_evaluate: tìm regex /AC-(SUP|DEPT|ASSET)-\d+/g  # phải 0 matches in user-facing text
5. browser_evaluate: tìm regex /\b[a-z0-9]{10}\b/g  # phải 0 matches (Frappe auto-name leak)

6. Click row → detail page
7. browser_snapshot → count workflow buttons  # phải >= 1 cho non-terminal state
8. Traverse all states → mỗi state phải có forward button
```

### D. New audit verdict items

Thêm vào audit report:

```
== Frappe API hygiene ==
- [ ] No int|None params trong GET endpoints (LL-BE-1)
- [ ] All Link fields enriched với _name companion (LL-BE-2)
- [ ] Service code ref fields verified vs DocType JSON (LL-BE-3)
- [ ] All gate validators implemented as functions (LL-BE-5)

== FE-BE contract sync ==
- [ ] Workflow action labels match exact (LL-BE-4, LL-FE-2)
- [ ] TRANSITIONS_BY_STATE covers all states (LL-FE-1)
- [ ] StatusBadge sync với BE workflow states (LL-FE-3)
- [ ] Form Select options = DocType options (LL-FE-8)
- [ ] Form Link fields use dropdown (LL-FE-9)

== UI completeness ==
- [ ] Every list has create button (LL-FE-4)
- [ ] Every detail has workflow buttons for current state (LL-FE-5)
- [ ] No code/email leaks user-facing (LL-FE-6)
- [ ] No Frappe auto-name leaks (LL-FE-7)
```

### E. Audit cross-reference

Khi audit bắt được pattern X → recommend fix theo skill tương ứng:

| Pattern phát hiện | Skill fix | Reference |
|---|---|---|
| 417 EXPECTATION FAILED | `assetcore-be` | LL-BE-1 |
| Unknown column 1054 | `assetcore-be` | LL-BE-3 |
| Workflow action 422 | `assetcore-be` + `assetcore-fe` | LL-BE-4 + LL-FE-2 |
| Code/email leak UI | `assetcore-be` + `assetcore-fe` | LL-BE-2 + LL-FE-6 |
| List thiếu create | `assetcore-fe` | LL-FE-4 |
| State stuck | `assetcore-fe` | LL-FE-1 |
| Auto-name leak | `assetcore-fe` | LL-FE-7 |
| Form Link as text | `assetcore-fe` | LL-FE-9 |
| Gate enforced muộn | `assetcore-be` | LL-BE-5 |
