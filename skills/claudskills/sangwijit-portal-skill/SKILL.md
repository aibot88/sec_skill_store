---
name: sangwijit-portal
description: |
  ระบบความรู้ครบวงจรสำหรับโปรเจกต์ Sangwijit ERP Web Portal — ระบบ Frontend Portal เชื่อมต่อกับ Dynamics 365 Business Central
  ครอบคลุม: สถาปัตยกรรมระบบ, 8+ Core Modules, Shared Components SC1-SC9, UI Design Pattern, BC365 API Integration, RBAC, Thailand Compliance

  ใช้ Skill นี้ทุกครั้งที่:
  - ถามหรือออกแบบ Module ใด ๆ ใน Sangwijit Portal (Sales, WH, Purchase, Finance, Service, Promotion, Master, Claims)
  - ออกแบบหน้าจอใหม่หรือ Flow ใหม่ตาม ERP Transaction Form Standard
  - เขียน Spec, Data Dictionary, หรือ Workflow สำหรับ Developer
  - ถามเรื่อง BC365 API Endpoint, RBAC Role, หรือ Status Flow
  - วางแผน Phase การพัฒนาหรือประเมิน Task ใหม่
  - ถามเรื่อง Shared Component SC1-SC9 — ใช้ที่ไหน, Props คืออะไร
  - ออกแบบ Module ใหม่: e-Tax, Marketplace, Mobile App, HRM Hook
  - ตรวจสอบ Open Questions ก่อน Implement
---

# Sangwijit ERP Web Portal Skill — Knowledge Base (v2.1)

**Last Updated:** เมษายน 2026
**เจ้าของโปรเจกต์:** Peerapat (พีรพัฒน์) — GM, กลุ่มแสงวิจิตร
**ธุรกิจ:** จำหน่ายเครื่องใช้ไฟฟ้า (ยอดขาย 450M+/ปี) — ค้าปลีก, ค้าส่ง, ส่งออก, ศูนย์บริการ
**Reference Folder:** `/Design Ai/` ใน Workspace

---

## ⚙️ กฎการทำงาน (RULES — บังคับทุกครั้ง)

### Rule 1: อ่าน Flowchart ก่อนออกแบบทุก Module

ก่อนออกแบบหน้าจอ หรือเขียน Spec ใด ๆ ต้องอ่าน Flowchart ที่เกี่ยวข้องจาก folder ก่อนเสมอ

**Flow Design Folder:** `/Design Ai/Flow Design/`

| Module | Subfolder | ประเภทไฟล์ |
|---|---|---|
| Sales | `Sales/Flow/` | Flow PDF (00–09) |
| Sales Documents | `Sales/Document/` | Document Template PDF |
| Purchase | `Purchase/Flow/` | Flow PDF (00–06) |
| Purchase Documents | `Purchase/Document/` | Document Template PDF |
| Warehouse | `Warehouse Inventory/Flow/` | Flow PDF (00–02) |
| Warehouse Documents | `Warehouse Inventory/Document/` | Document Template PDF |
| Finance (Cash/Bank) | `Finance/Flow/` | Flow PDF (01–03) |
| Finance Documents | `Finance/Document/` | Voucher Template PDF |
| Account (AR/AP/GL/Tax) | `Account/Flow/` | Flow PDF (00–12) |
| Account Documents | `Account/Document/` | Voucher Template PDF (01–10) |
| Service | `Service/` | Flow PDF (00–06) |
| Promotion | `Promotion/` | Flow PDF (00–02) |
| Master Data | `Master/` | Master Flow PDF (7 ไฟล์) |
| Data Transfer | `Data Transfer/` | Transfer Flow PDF (01–06) |

**ขั้นตอนการอ่านก่อนออกแบบ:**
```
1. ระบุ Module ที่จะทำ
2. เปิด Flow PDF ที่เกี่ยวข้องจาก subfolder ด้านบน
3. ทำความเข้าใจ Status Flow + BC365 Entity ใน Flow
4. ตรวจ Document Template PDF (ถ้ามี) เพื่อดู Field ที่ต้องแสดง
5. จึงเริ่ม Spec / Screen Design
```

---

### Rule 2: ไฟล์ซ้ำ — ถามก่อนเสมอ

ถ้าพบว่า folder มีไฟล์ชื่อคล้ายกันหรือเลขซ้ำกัน ต้องหยุด เปรียบเทียบ และถามผู้ใช้ก่อน ห้ามเลือกเองโดยไม่แจ้ง

**ไฟล์ซ้ำที่ตัดสินใจแล้ว (ห้ามถามซ้ำ):**

| Module | ไฟล์ที่ซ้ำ | การตัดสินใจ |
|---|---|---|
| Service / Claims | `06 Service - Claim Intake รับเรื่องเคลม ตรวจสอบสินค้า คืนของ Vendor.pdf` vs `06 Service - Claim Intake รับเรื่องเคลมและตรวจสอบสินค้า.pdf` | ✅ ใช้ **"คืนของ Vendor"** เป็น Reference หลัก (Flow ครบกว่า) |
| Sales / Document | `Credit Note (ใบลดหนี้ ใบกำกับภาษี).pdf` vs `Credit Note (ใบลดหนี้).pdf` | ✅ **คนละ Case**: ใบลดหนี้ ใบกำกับภาษี = **ในประกัน** / ใบลดหนี้ = **นอกประกัน** |

---

## 🧠 Mental Model ที่ถูกต้อง (CRITICAL — อ่านก่อนทุกอย่าง)

### Portal = UI Layer เท่านั้น — BC365 = System of Record

```
User (Browser)
    ↓
Sangwijit Web Portal  ← React/Vue + TypeScript + Tailwind CSS
    ↓ REST API
BC365 Business Central ← Ledger, Posting, Stock, Document Number
    ↓
Azure / SQL (BC Database)
```

**WRONG (ห้ามคิดแบบนี้):**
- ❌ Portal มี Database ของตัวเอง (ไม่มี — ดึงข้อมูลจาก BC ทั้งหมด)
- ❌ Portal Post Transaction เองโดยไม่ผ่าน BC
- ❌ UI ออกแบบอิสระโดยไม่ดู BC Entity / Field

**CORRECT:**
- ✅ Portal = Smart Frontend + Workflow Engine ที่ call BC REST API
- ✅ ทุก Post / Confirm → ส่งไป BC แล้วค่อย Refresh หน้าจอ
- ✅ Status, เลขที่เอกสาร, ราคา → มาจาก BC เสมอ

### Service Account Strategy
- ใช้ BC Service Account **1 บัญชี** (ลดค่า License)
- Portal ทำ RBAC เอง (ไม่พึ่ง BC Permission ต่อ User)
- Retry + Queue เมื่อ BC API ช้าหรือ Error

---

## 📦 Modules Overview

### 9 Core Modules + Extensions (v2.1 — Confirmed)

| Module | ย่อ | Phase | หน้าจอหลัก |
|---|---|---|---|
| Sales | SL | P1 | Quotation, SO, Invoice, Credit Memo, Deposit, Cash Sale |
| Warehouse | WH | P1 | GRN, Issue, Transfer, Adjust, Stock Card, Serial |
| Purchase | PO | P1 | PR, PO, GRN, AP Invoice, Credit Memo, Vendor Return, **Sale-In Accrual (PO-7)**, **PO บิลฝาก (PO-8)** |
| Finance | FI | P1+P2+P3 | AR Receive, AP Payment, Expense Voucher (P2), Bank Recon, Credit Control (P2), Period Close, **Fixed Asset (FI-9/10/11)**, **WHT (FI-12)**, **Dual-Book (FI-13)** |
| Service & Delivery | SV | P2 | Service Queue, Job Card, QA Close, Delivery & Installation (4.x), Mobile (Group A) |
| Promotion/Pricing | PM | P1+P3 | Price List, Step Discount, Bundle, Promotion Scheme, Quota, Simulator |
| Master Data | MD | P1 | Item, Customer, Vendor, Employee (ใหม่), Branch & Warehouse (ใหม่) |
| System Config | CF | P1 | Tax Setup, Number Series, Customer/Vendor Config, Bin Policy, Item Config |
| Claims | CL | P2 | Claims List, CN, AP CM, Approval |
| Integration/API | IA | P2+P3 | API Monitor, Webhook, BC Sync Status, Error Log |
| e-Tax Invoice | TX | P2 | XML Generator, Digital Signature, RD API, WHT |
| Marketplace | MK | P3 | Order Inbox, SKU Map, Stock Sync, Tab ออนไลน์ใน Sales |
| Mobile App | MB | P2/P4 | Group A: Service Tech (P2), Group B: Manager (P4) |
| HRM Hook | HR | P3 | Employee Directory, Leave Status, Commission Hook |

**กฎแยก Master Data vs System Config:**
- **Master Data (MD)** = ข้อมูลอ้างอิงที่ User สร้างขึ้น (Item, Customer, Vendor, Employee, Branch)
- **System Config (CF)** = ตั้งค่าระบบโดย Admin (Tax Code, Number Series, Posting Group, Bin Policy)
- **Promotion Scheme** อยู่ใน Promotion module ไม่ใช่ Config → เพราะเกี่ยวข้องกับ Business Logic การขาย

---

## 🎨 UI Design Principles (7 หลักการ — ห้ามละเมิด)

1. **BC-First Data** — ทุก Field ต้องมาจาก BC Entity ที่ระบุในเอกสาร
2. **Progressive Disclosure** — แสดงข้อมูลตาม Role และ Context
3. **Status-Driven UI** — สีและ ActionBar เปลี่ยนตาม Document Status เสมอ
4. **Shared Component First** — ดู SC1-SC9 ก่อนสร้าง Component ใหม่
5. **Bilingual Ready** — ทุก Label มี Key ทั้งไทยและอังกฤษ
6. **Error Recovery** — ทุก API Error ต้องมี User-readable Message + Retry
7. **RBAC Everywhere** — Field, Button, Route ต้องเช็ค Permission

---

## 📐 ERP Transaction Form — Standard Structure (7 Sections)

**ห้ามเปลี่ยนลำดับ Section เด็ดขาด**

```
┌─────────────────────────────────────────────────┐
│  1. PAGE HEADER                                  │
│     Module Title | Document Type | Status Badge  │
│     Breadcrumb | Action Bar (context-sensitive)  │
├─────────────────────────────────────────────────┤
│  2. DOC HEADER                                   │
│     Document No. | Date | Reference | Branch     │
│     (Read-only ถ้า Posted/Confirmed)             │
├─────────────────────────────────────────────────┤
│  3. PARTY                                        │
│     SC1/CustomerSearch หรือ Vendor Search        │
│     Auto-fill: Price Group, Credit, Address      │
├─────────────────────────────────────────────────┤
│  4. LINE ITEMS                                   │
│     SC2/ItemSearch | Qty | Price | Discount | VAT│
│     Serial Panel (SC8) | Inline Edit | Add Row   │
├─────────────────────────────────────────────────┤
│  5. TABS (ตามประเภทเอกสาร)                      │
│     Payment | Delivery | Reference | Notes | Log │
├─────────────────────────────────────────────────┤
│  6. SUMMARY                                      │
│     Subtotal | Discount | VAT 7% | Total (THB)   │
│     Deposit Applied | Net Due                    │
├─────────────────────────────────────────────────┤
│  7. ACTION BAR (ล่าง — sticky)                  │
│     ปุ่มตาม Status + Role Permission             │
└─────────────────────────────────────────────────┘
```

### ActionBar Modes ตาม Status

| Status | ปุ่มที่แสดง |
|---|---|
| Draft | Save Draft, Submit for Approval, Delete |
| Pending Approval | (Maker: รอ) / (Approver: Approve, Reject) |
| Confirmed | Post, Edit (ถ้า Role อนุญาต), Cancel |
| Posted | Print, Duplicate, View GL Entries |
| Cancelled | View Only |

---

## 🏷️ Status System — สีมาตรฐาน (ห้ามใช้สีอื่น)

| Status | สี | Hex | ใช้กับ |
|---|---|---|---|
| Draft | Gray | #6B7280 | ทุกเอกสาร |
| Pending Approval | Orange/Amber | #F59E0B | เอกสารที่ต้องอนุมัติ |
| Confirmed | Blue | #3B82F6 | อนุมัติแล้ว รอ Post |
| Posted | Green | #10B981 | Post สู่ BC แล้ว |
| Cancelled | Red | #EF4444 | ยกเลิก |
| Scheduled | Purple | #8B5CF6 | งานที่นัดไว้ล่วงหน้า |
| Live | Bright Green | #22C55E | Promotion ที่ Active |
| Expired | Brown/Warm Gray | #92400E | Promotion หมดอายุ |

---

## 🔧 Shared Components SC1-SC9 (Full Spec)

### ตาราง Usage Matrix — 130+ Screens (v2.1)

| SC | ชื่อ Component | หน้าจอที่ใช้หลัก |
|---|---|---|
| SC1 | SharedCustomerSearch | บิลขาย, ใบจอง, ใบเสนอราคา, ใบมัดจำ, ใบลดหนี้, Service Intake, รับเรื่องเคลม, อนุมัติวงเงิน, ประกบบิล AR |
| SC2 | SharedItemSearch | บิลขาย, ใบจอง, ใบเสนอราคา, PR, PO, RFQ, โอนสินค้า, GRN, เบิกอะไหล่, Stock Count |
| SC3 | SharedPaymentPanel | บิลขาย, ใบมัดจำ, ใบจอง, ใบลดหนี้ขาย, ตัดชำระเจ้าหนี้, PO-8 Deposit Bill |
| SC4 | SharedDeliveryPanel | บิลขาย (③ จัดส่ง/ติดตั้ง), ใบจอง, Transfer Order (ปลายทาง) |
| SC5 | SharedDocRefPanel | ทุกเอกสารที่มี Reference: บิลขาย←Quote/จอง/มัดจำ, PO←PR/RFQ, Service←บิล, GR←PO, PO-8←PO |
| SC6 | SharedDepositPanel | บิลขาย (Payment Section), ใบจอง |
| SC7 | SharedTimeline | **ทุกเอกสาร** — Queue/Dashboard, Sales, WH, Purchase, Service, Finance, Claims, FA |
| SC8 | SharedSerialPanel | GRN, โอนสินค้า, ใส่ Serial หลังขาย, Stock Count, Service รับซ่อม, เบิกอะไหล่, Item Master |
| SC9 | SharedPromoPrice | ใบเสนอราคา, ใบจอง, บิลขาย (④ โปรฯ Auto-Match), Employee Master (Commission), Sales Price List |
| **SC10** | **SharedVendorSearch** *(NEW)* | **PR, PO, AP Invoice, PO-7 Accrual, PO-8 Deposit Bill, FI-2 AP Payment, FI-12 WHT** |

---

### SC1 — SharedCustomerSearch

```
Search Fields (v2 — เพิ่มจากเดิม):
  รหัสลูกค้า, ชื่อ (TH), นามสกุล (TH), ชื่อ (EN), เบอร์โทร, Email,
  เลขผู้เสียภาษี, รหัสบัตรประชาชน (ID Card), ที่อยู่ (partial search)

Filter:
  ประเภทลูกค้า: บุคคลธรรมดา / นิติบุคคล / ราชการ / Walk-in
  กลุ่มลูกค้า:  ค้าปลีก / ค้าส่ง / ดีลเลอร์ / ออนไลน์
  กลุ่มราคา:    A / B / C / VIP (Price List Group)
  สาขาที่สังกัด: HQ / สาขา 1 / สาขา 2 / ...
  สถานะ:        Active / Blocked / Overdue
  มียอดค้าง:    All / มี AR ค้าง / ไม่มี

Search:   Real-time ≥ 2 ตัวอักษร; Keyboard + ID Card Scan (Post GoLive)
Result:   รหัส, ชื่อ-นามสกุล, ประเภท, กลุ่มราคา, วงเงิน, คงเหลือ, เบอร์, สาขา, Overdue Badge
Auto-fill: Party Section + ดึง Price List/โปร ตามกลุ่มลูกค้า
Blocked:  สถานะ Blocked → Warning + ขออนุมัติก่อนเปิดบิล (ห้ามผ่าน)
Quick-Create: สร้างลูกค้าใหม่จาก popup (Draft status, รอ KYC ภายหลัง)
Customer 3 Address: ที่อยู่บัตรปชช / ที่อยู่จัดส่ง / ที่อยู่ออกใบกำกับ
API:  GET /customers?$filter=..., GET /customers/{id}, POST /customers
```

### SC2 — SharedItemSearch

```
Search Fields (v2 — เพิ่มจากเดิม):
  รหัสสินค้า, ชื่อ (TH), ชื่อ (EN), ยี่ห้อ/แบรนด์, รุ่น/Model, Barcode/QR

Filter:
  หมวดสินค้า:    แอร์ / พัดลม / เครื่องซักผ้า / ตู้เย็น / TV / เครื่องครัว / อื่นๆ
  ยี่ห้อ/แบรนด์:  Daikin / Mitsubishi / Samsung / LG / Toshiba / ...
  ช่วงราคา:      0-5K / 5K-15K / 15K-50K / 50K+
  สถานะ:         Active / Discontinued / Pending
  สต็อก:         All / มี Stock > 0 / หมดสต็อก / สต็อกต่ำ (< Min)
  สาขา/คลัง:     เฉพาะคลังที่ระบุ (Stock by Location)
  Serial Flag:   All / มี Serial / ไม่มี Serial

Search:   Keyboard + Barcode Scan; แสดงสต๊อก real-time แยกตามคลัง
Result:   รหัส, ชื่อ, หมวด, ยี่ห้อ, รุ่น, UOM, ราคาตามกลุ่มลูกค้า, สต๊อก, สต๊อกจอง, Serial Flag
Alt Items: แสดงสินค้าทดแทน + Bundle แนะนำเมื่อสต๊อกหมด
Serial:   Serial Flag = true → เปิด SC8 อัตโนมัติใน line
Inline Edit: แก้ไขข้อมูล line ได้เลย ห้ามใช้ Popup
Import/Export: Serial No. Import/Export CSV ที่ระดับ Line
API:  GET /items?$expand=itemVariants, GET /items/{id}/stockByLocation
      GET /priceLists?customerId=&date=
      GET /itemCategories → ดึงหมวดสินค้า
```

### SC3 — SharedPaymentPanel

```
ยอด:     ยอดสุทธิ, ยอดมัดจำที่หัก, ยอดคงเหลือ, VAT, ส่วนลดท้ายบิล
VAT Options: รวม VAT / ไม่รวม VAT / ไม่แสดง VAT (กลมยอด) — เลือกต่อเอกสาร
วิธีชำระ: เงินสด, โอน, เช็ค, บัตรเครดิต/เดบิต, QR Payment, เครดิต, บางส่วน
Split:   เลือกหลายวิธีต่อบิลได้ (split payment)
เครดิต:  ตรวจวงเงิน real-time → เกิน → Auto trigger Approval Flow
Status:  ยังไม่ชำระ / ชำระบางส่วน / ชำระครบ / เกินกำหนด / รออนุมัติวงเงิน

QR Payment (2 layers) — EMVCo PromptPay via Biller ID (SWT):
  • ชั้น 1 — Invoice QR  : Ref1 = เลขที่บิล, ยอด fix → ลูกค้าจ่ายตรงบิลเดียว
  • ชั้น 2 — Customer QR : Ref1 = รหัสลูกค้า, ยอด open/ค้างรวม/ระบุ
    → ส่งลูกค้าทาง LINE, จ่ายได้หลายบิลพร้อมกัน, แยก FI-1Q Apply Queue
  • เงินเข้า → bank statement → IA-Q sync → URC → FI-1Q Queue → auto-apply
```

### SC4 — SharedDeliveryPanel

```
จัดส่ง: ที่อยู่จัดส่ง, ผู้รับ, เบอร์, วันที่-ช่วงเวลา, วิธีจัดส่ง
ติดตั้ง: ต้องการติดตั้ง (Y/N) → auto-create Service Work Order หลัง Post
Status:  รอจัดส่ง → กำลังจัดส่ง → ส่งแล้ว → ติดตั้งเสร็จ
QR Track: ลูกค้าดูสถานะผ่าน QR Code บนใบเสร็จ
```

### SC5 — SharedDocRefPanel

```
ดึงเอกสาร: แต่ละประเภทกำหนด Source ที่ดึงได้:
  บิลขาย ← Quote, ใบจอง, มัดจำ
  PO ← PR, RFQ
  Service ← บิลขาย (serial ref)
  GR ← PO
Partial:  ดึงบางส่วนได้; ติดตามยอดที่ดึงไปแล้ว vs. เหลือ
Cascade:  ดึงมา → auto-fill รายการสินค้า + ลูกค้า
Chain Link: กด PO → เห็น PR ต้นทาง / กด Invoice → เห็น Shipment ปลายทาง
```

### SC6 — SharedDepositPanel

```
ค้นหา:   เลขมัดจำ / เลขจอง / ลูกค้า — แสดงเฉพาะที่ยังตัดได้
ตัดมัดจำ: ยอดทั้งหมด, ใช้แล้ว, คงเหลือ, จะตัดในบิลนี้
หลายใบ:  รองรับหลายใบมัดจำต่อบิลเดียว
Auto:    ตัดครบ → สถานะมัดจำ = Fully Applied → บันทึก AR Ledger
สร้างใหม่: จากใบจองหรือ Stand-alone → auto generate เลขที่, พิมพ์ได้ทันที
```

### SC7 — SharedTimeline (Audit Log)

```
Document Chain: แสดง Quote→จอง→มัดจำ→Invoice→Shipment→Payment
                คลิกเอกสารใดก็ข้ามไปได้
Reverse Link:  บิลขายรู้ว่ามี Shipment/Payment ไหนอ้างอิงมา
Activity Log:  ทุก Action อัตโนมัติ (สร้าง/แก้/อนุมัติ/ปฏิเสธ/พิมพ์) — ลบไม่ได้
Comment:       Internal note + mention @พนักงาน → Notification; ไม่แสดงลูกค้า
PDPA:          Phase 1 ต้องมี Audit Log ทุก Access
```

### SC8 — SharedSerialPanel

```
กรอก/สแกน: กรอก Manual หรือ Scan Barcode; validate ไม่ซ้ำ real-time
Bulk:      Upload CSV (กรณีจำนวนมาก)
ประวัติ:   กด "ดูประวัติ" → lifecycle ทั้งหมด: รับเข้า→ขาย→ซ่อม→เคลม
Status:    ว่าง / ใช้งานอยู่ / ซ่อม / เคลม
Serial Policy: ไม่บังคับตอนขาย — บังคับตอนคลัง "เบิก" เท่านั้น
```

### SC9 — SharedPromoPrice

```
ราคา:     ดึง Price List ตามกลุ่มลูกค้า + ช่องทาง + วันที่บิล; ใช้ Priority สูงสุด
โปร Badge: แสดง badge บน line item; คลิกดูเงื่อนไขได้
ของแถม:   auto-add Free Item Line (ราคา 0, flag Gift) เมื่อครบเงื่อนไข
Price Alert: แจ้งเมื่อราคาจะเปลี่ยนภายใน N วัน
Override:  แก้ราคาต่ำกว่า Floor → Auto Approval Flow + บันทึก Override Log
Accrual:   ขายสินค้าที่มี Vendor Sale-In → บันทึก Accrual Entry อัตโนมัติ
Commission: บันทึก PC Commission record แนบกับบิล
Priority:  Contract Price > Step Discount > Bundle > Trade-in > Normal
Block [T6]: คำนวณที่ Portal หรือ BC? — ยังไม่ตัดสินใจ
```

### SC10 — SharedVendorSearch (NEW)

```
Search Fields:
  รหัส Vendor, ชื่อบริษัท (TH/EN), เบอร์โทร, Email, เลขผู้เสียภาษี,
  ชื่อผู้ติดต่อ (Contact Person)

Filter:
  ประเภท Vendor:  สินค้า / บริการ / ค่าเช่า / ค่าขนส่ง / อื่นๆ
  WHT Category:   1% / 2% / 3% / 5% / ไม่หัก
  สถานะ:          Approved / Pending Approval / Blocked
  Credit Term:    Cash / 30 วัน / 60 วัน / 90 วัน
  มี AP ค้าง:     All / มี AP ค้าง / ไม่มี

Search:    Real-time ≥ 2 ตัวอักษร
Result:    รหัส, ชื่อ, ประเภท, WHT Category, Credit Term, AP Outstanding, สถานะ
Auto-fill: Vendor Section + ดึง WHT Rate + Credit Term + Price List
Blocked:   Vendor ยังไม่ Approve → ห้ามสร้าง PO (ต้องผ่าน PO-3 Onboarding ก่อน)

ใช้ใน:
  PO-1 (PR), PO-4 (PO), PO-6 (AP Invoice), PO-7 (Accrual), PO-8 (Deposit Bill)
  FI-2 (AP Payment), FI-12 (WHT)

API:  GET /vendors?$filter=..., GET /vendors/{id}, POST /vendors
      GET /vendorLedgerEntries?vendorId=&open=true → AP ค้าง
```

---

## 🔌 BC365 API — Endpoints หลัก

### Pattern มาตรฐาน

```
Base: https://{tenant}.api.businesscentral.dynamics.com/v2.0/{tenant}/Production/api/v2.0/
Auth: OAuth2 Client Credentials (Service Account)
Retry: Exponential Backoff (3 ครั้ง), Queue เมื่อ Timeout
```

### Sales Module

```
GET    /salesQuotes              → SO Draft list
POST   /salesOrders              → สร้าง SO
PATCH  /salesOrders/{id}         → แก้ไข SO (ก่อน Post)
POST   /salesOrders/{id}/post    → Post SO → Invoice + Stock
POST   /salesCreditMemos         → CN
POST   /salesOrders/{id}/shipmentLines → Delivery
```

### Warehouse

```
GET    /locations                → คลังทั้งหมด
GET    /items/{id}/stockByLocation
POST   /purchaseReceipts         → GRN
POST   /inventoryAdjustments     → Adjust
POST   /itemTransferOrders       → Transfer
GET    /serialNumbers?itemId=    → Serial Lookup
```

### Purchase

```
POST   /purchaseOrders           → PO
POST   /purchaseOrders/{id}/receive → GRN (ตัด Stock)
POST   /purchaseInvoices/{id}/post  → AP + GL
POST   /purchaseCreditMemos      → Vendor Return/CN
```

### Finance

```
POST   /cashReceiptJournals      → AR Receive
POST   /vendorPaymentJournals    → AP Payment
POST   /generalJournals          → JV / Accrual
POST   /bankAccounts/{id}/reconcile → Bank Recon
POST   /accountingPeriods/{id}/close → ปิดงวด
```

### Service (BC Extension Required)

```
GET    /serviceOrders            → [?] Standard BC มีหรือต้อง Custom?
POST   /serviceOrders            → สร้าง Job Card
PATCH  /serviceOrders/{id}       → อัปเดตสถานะ
POST   /serviceOrders/{id}/complete → ปิดงาน → Auto AP ช่าง
```

---

## 👥 RBAC — Permission Matrix (28 Functions × 9 Roles)

| ฟังก์ชัน | Super Admin | บัญชี | จัดซื้อ | ฝ่ายขาย | คลัง | ศูนย์บริการ | ช่าง | ฝ่ายเคลม | ผู้บริหาร |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| จัดการ User/Role | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| เปิดบิลขาย | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| ใบจอง / ใบเสนอราคา | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| สร้างลูกค้า | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| รับสินค้าเข้า (GRN) | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | 🔍 |
| โอนสินค้าคลัง | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | 🔍 |
| สร้าง Vendor | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| เสนอราคา Supplier (RFQ) | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| ตั้งหนี้สินค้า (AP Invoice) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| ตั้งหนี้โปร/รีเบต | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| อนุมัติ PO | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| รับสินค้าซ่อม | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | 🔍 |
| นัดหมายคิวช่าง | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | 🔍 |
| ช่างรับงาน (Mobile) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| เบิกอะไหล่ซ่อม | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | 🔍 |
| เบิกค่าแรงช่าง | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | 🔍 |
| รับเรื่องเคลม | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | 🔍 |
| ส่งเคลม Supplier | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | 🔍 |
| ติดตามสถานะเคลม | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | 🔍 |
| ใบตั้งหนี้ / ใบจ่ายเงิน | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| ตัดหนี้เจ้าหนี้ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| ประกบบิลลูกหนี้ (AR) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| วงเงินลูกค้า / Credit | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| คืนเงินลูกค้า (CN) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| บันทึกค่าใช้จ่าย | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| กระทบยอดธนาคาร | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔍 |
| Field-Level Permission | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ดูรายงานรวม | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> 🔍 = View Only (ผู้บริหาร) | ✅ = Full Access | ❌ = No Access

**กฎ RBAC ที่ห้ามละเมิด:**
- Maker ≠ Checker: ห้าม Approve งานตัวเอง (บังคับทุกโมดูลที่มี Approval)
- Field-Level: ราคาต้นทุน, วงเงิน Credit → ซ่อนตาม Role
- Route Guard: ป้องกัน URL ที่ไม่มีสิทธิ์
- Approval Matrix: กำหนดใน System Config ว่า Tier ไหน → Approver คนไหน

---

## 📅 Phase Plan

### Phase 1 — Run ASAP
**โมดูล:** Sales, Warehouse, Purchase Basic, Price List P1, Finance Basic (AR/AP/JV), Master Data, System Config
**เงื่อนไข Go-Live:** Master Data พร้อม + BC Sandbox ผ่าน
**Key Deliverables:** SC1-SC9 ครบ → Sales SO/Invoice → WH GRN/Issue → PO/GRN/AP → AR/AP Basic

### Phase 2 — Scale & Control
**โมดูล:** Step Discount/Bundle, Credit Memo, Service+Delivery (4.x), Claims, Finance 2.5 Expense Voucher, Finance 2.6 Credit Control, Bank Recon, Integration/API Monitor, e-Tax Invoice, Mobile App Group A (ช่าง)
**เงื่อนไข:** Phase 1 UAT ผ่าน
**Key Deliverables:**
- Service Queue/JobCard + Delivery & Installation sub-module (4.1-4.3)
- Expense & Payment Voucher (จ่ายค่าใช้จ่ายทั่วไป)
- Credit Control Dashboard (ติดตามวงเงิน + Alert ลูกหนี้เกิน)
- Integration API Monitor (สถานะ Sync BC / Error Log)
- e-Tax XML + RD API, Mobile Service Tech

### Phase 3 — Automate
**โมดูล:** Finance Full (Period Close / Tax Report), Promotion Full, Accrual Auto, Real-time, Service Notification+Performance, Marketplace (Shopee/Lazada)
**เงื่อนไข:** Phase 2 Stable
**Key Deliverables:** Marketplace Tab ออนไลน์ใน Sales, Order Inbox, Stock Sync, Technician Performance Dashboard

### Phase 4 — Optimize
**โมดูล:** Trade-in, Promo Simulator, Advanced SLA, Mobile App Group B (ผู้บริหาร), Marketplace Dashboard, BI/KPI Full, PDPA
**เงื่อนไข:** Phase 3 Stable

---

## 🇹🇭 Thailand Compliance

### e-Tax Invoice (Phase 2)

| Component | รายละเอียด |
|---|---|
| XML Generator | ออก Tax Invoice XML ตาม RD Standard |
| Digital Signature | Sign ด้วย Certificate ขององค์กร |
| RD API Connector | ส่ง XML ไป RD Portal + รับผลกลับ |
| Status Tracker | Pending → Submitted → Accepted / Rejected |
| WHT Certificate | ภ.ง.ด.3 / 53 — ตาม B10 (Auto/Manual TBD) |
| e-Filing Dashboard | รายการที่ส่งแล้ว, ยังไม่ส่ง, Rejected |

> ⚠️ [T9] ต้องตรวจก่อนว่า BC365 Standard Thailand Extension ครอบคลุมหรือต้อง Custom

### VAT & WHT
- VAT 7% บังคับทุกใบกำกับภาษี
- WHT (ภ.ง.ด.3/53) ตัดเมื่อ AP Payment
- ทุก Posted Document ต้องมี Tax Invoice No. ที่ถูกต้อง

### PDPA (Phase 4)
- Consent Record + Withdrawal Flow
- Data Retention Policy + Auto-Delete Hook
- Audit Log ทุก Access — SC7 ต้องมีตั้งแต่ Phase 1

---

## 🛒 Marketplace Integration (Phase 3)

### Concept: POS-Style Tab ใน Sales Module

```
Sales Module
├── Tab: ขายหน้าร้าน   ← Sales Order ปกติ
└── Tab: ออนไลน์       ← Marketplace Orders (ใหม่ Phase 3)
    ├── Order Inbox (Shopee + Lazada)
    ├── SKU Mapping Manager
    ├── Auto-Create SO in BC
    ├── Stock Sync (BC → Marketplace)
    └── Shipping Tracking
```

### Business Rules
- คำสั่งซื้อ Marketplace → Auto-create SO ใน BC (ยืนยันหรือ Auto)
- Stock Sync: BC คือ Source of Truth → Push ไป Marketplace [T12]
- Return จาก Marketplace → Credit Memo Flow ปกติ

> ⚠️ [T10] Shopee/Lazada Partner Account และ Production Key พร้อมหรือยัง?

---

## 📱 Mobile App (2 Groups)

### Group A — Service Tech (Phase 2, เร่งด่วน)
- รับ Job Card / นัดหมาย
- บันทึกผลงาน + รูปถ่าย Before/After
- Check-in/out ที่หน้างาน
- บันทึกอะไหล่ที่ใช้
- [T1] Native / PWA / Responsive Web?
- [T2] Offline Mode?

### Group B — Manager/Sales (Phase 4)
- Sales Dashboard + KPI ส่วนตัว
- อนุมัติ Quotation / SO จากมือถือ
- ดูสต็อก Real-time
- Service Performance Report

---

## ⚠️ Open Questions — ห้าม Implement จนกว่าจะได้คำตอบ

### Technical
| # | คำถาม | Phase |
|---|---|---|
| T1 | Mobile: Native / PWA / Responsive Web? | P2 |
| T2 | Offline Mode ช่าง: Sync ยังไง? | P2 |
| T5 | BC Extension: Standard หรือ Custom AL? | P1 |
| T6 | Promotion Engine: คำนวณที่ Portal หรือ BC? | P1 |
| T9 | e-Tax: BC365 Standard Thailand Extension ครอบคลุมไหม? | P2 |
| T10 | Marketplace: Partner Account พร้อมหรือยัง? | P3 |
| T11 | Customer Notification: SMS หรือ LINE Notify? | P3 |
| T12 | Stock Sync Marketplace: Real-time หรือ Batch? | P3 |

### Business Rules
| # | คำถาม | Phase |
|---|---|---|
| ~~B1~~ | ~~Promotion Conflict Priority~~ ✅ **RESOLVED** — Priority Number + Stack ≤ 2 ชั้น (ดู PM_promotion.md) | P1 |
| ~~B5~~ | ~~Credit Approval Tier~~ ✅ **RESOLVED** — ทั้งฝั่งขาย (SL-F1) + ฝั่งซื้อ (PO) ตั้งใน CF-7 | P1 |
| B6 | Deposit GL Account | P1 |
| B9 | SLA กี่ชั่วโมงต่อ Doc Type? | P2 |
| ~~B10~~ | ~~WHT Certificate: Auto หรือ Manual?~~ ✅ **RESOLVED** — Auto จาก FI-2 AP Payment → WHT List (FI-12) → Release → Print | P1 |
| C1 | ⚠️ COA Mapping ระหว่าง 4 บริษัท (SWT/SWE/VMN/WPS) → ใช้ COA เดียวกันหรือต่างกัน? | P3 |
| C2 | ⚠️ Intercompany Transaction Threshold → จำนวนเท่าไหร่ถึง Auto-detect? | P3 |

---

## 🤖 วิธีออกแบบ Module ใหม่ (Template)

เมื่อขอออกแบบ Module หรือหน้าจอใหม่ ให้ตอบครอบคลุม:

### 1. Module Brief
```
Module: [ชื่อ]
Phase: [P1/P2/P3/P4]
BC Entity: [API Endpoint ที่เชื่อม]
Trigger: [อะไร trigger หน้าจอนี้]
Output: [เอกสารหรือ Action ที่เกิดขึ้น]
```

### 2. Screen List
```
[Module Code]-1: [ชื่อหน้า List/Queue]
[Module Code]-2: [ชื่อหน้า Form/Detail]
[Module Code]-3: [หน้า Approval/Review ถ้ามี]
```

### 3. ERP Transaction Form Breakdown
ระบุ Field ทั้ง 7 Sections ว่ามีอะไรบ้าง + BC Field Mapping

### 4. Status Flow
```
Draft → Submitted → Approved → Posted/Confirmed → (Cancelled)
```

### 5. Shared Components ที่ใช้
ระบุ SC ที่ต้องใช้พร้อม Config

### 6. RBAC
ระบุ Role + Permission (Create/Edit/Approve/Post/Cancel)

### 7. BC API Calls
ระบุ GET/POST/PATCH ที่ต้องใช้

### 8. Open Questions ที่ Block
ระบุ Question Number จาก Section Open Questions

---

## 📂 Module Spec Files (รายละเอียดทีละเมนู)

| ไฟล์ | Module | เมนูที่ครอบคลุม |
|---|---|---|
| `modules/SL_sales.md` | งานขาย (SL) | Quotation, Reservation, Deposit, **Invoice (5 ส่วน: สินค้า/ชำระ/จัดส่ง/โปรฯ/ใบกำกับ)**, Credit Memo, Credit Approval |
| `modules/PO_purchase.md` | งานจัดซื้อ (PO) | PR, RFQ, Vendor Onboarding, PO, GRN, AP Invoice, **Sale-In Accrual (PO-7)**, **PO บิลฝาก (PO-8)** |
| `modules/WH_warehouse.md` | งานคลัง (WH) | Queue, GRN, Transfer, Sales Issue, Stock Count, Stock Card, **Non-Move Report (WH-NM)** |
| `modules/FI_finance.md` | งานการเงิน (FI) | AR Receipt, AP Payment, Bank Recon, JV, Expense Voucher (P2), Credit Control (P2), Period Close (P3), **Accrual Monitor (FI-8)**, **Fixed Asset (FI-9/10/11)**, **WHT (FI-12)**, **Dual-Book (FI-13)** |
| `modules/SV_service.md` | งานบริการ + เคลม (SV+CL) | Service Intake, Job Card, Parts, QA Close, Delivery & Install, Claims 3 ประเภท |
| `modules/PM_promotion.md` | โปรโมชั่น (PM) | Price List, Promotion Scheme, Bundle/Step Discount, Quota, Simulator *(PM-6 Accrual ย้ายไป PO-7)* |
| `modules/MD_master.md` | ข้อมูลหลัก (MD) | Item, Customer, Vendor, Employee (NEW), Branch & Warehouse (NEW), Price List |
| `modules/CF_config.md` | ตั้งค่าระบบ (CF) | Tax, Number Series, RBAC, Posting Groups, Bin Policy, Technician Template, Approval Matrix |
| `modules/IA_integration.md` | Integration & API (IA) | BC Sync Monitor, Error Log, Webhook, Marketplace Connector (P3), Entity Explorer (P3) |

> อ่าน Module Spec ก่อนออกแบบหน้าจอใด ๆ ในโมดูลนั้น

---

## 📁 Reference Files ใน Workspace

| ไฟล์ | ใช้เพื่อ |
|---|---|
| `research.md` | ภาพรวมระบบ, Open Questions, Module Spec ครบ |
| `plan.md` | Task Breakdown ทุก Phase, สถานะ Task |
| `ui_design_pattern_guideline.md` | Design Rules, ERP Form 7 Sections, SC Spec, RBAC |
| `README.md` | Project Overview, 68 Screens, Phase Overview |
| `uxui_field_knowledge.docx` | Field Spec ทีละหน้าจอ |
| `1_component_fw_clean.docx` | Technical Spec SC1-SC9 |
| `sangwijit_reference_rev2.docx` | Business Reference + Gap Analysis |
| `dd_sales_phase1.docx` | Data Dictionary Phase 1 (Sales) |
| `dd_wh_pur_phase2.docx` | Data Dictionary Phase 2 (WH + Purchase) |
| `dd_finance_phase3.docx` | Data Dictionary Phase 3 (Finance) |
| `dd_svc_promo_master_phase4.docx` | Data Dictionary Phase 4 (Service/Claims/Promo/Master) |
| `sales-invoice-compact.html` | HTML Prototype — ตัวอย่าง UAT ชุดแรก |

### ลำดับการอ่านเอกสาร (Document Reading Order)
1. `research.md` — เริ่มที่นี่เสมอ
2. `plan.md` — Task Status + Blocked Items
3. `ui_design_pattern_guideline.md` — Design Rules
4. `uxui_field_knowledge.docx` — Field Detail ทีละหน้าจอ
5. `1_component_fw_clean.docx` — SC Technical Spec
6. Data Dictionary ตาม Phase
7. Workflow PDF — BC365 Mapping จริง

---

## 🔄 Status Transition Diagrams (ทุก Module)

### Sales / Invoice / Promotion / Claims
```
Draft → รออนุมัติวงเงิน → อนุมัติ → ออกใบกำกับแล้ว → ชำระเงินแล้ว → ปิดงาน
              ↓
           ปฏิเสธ → Draft (แก้ไข/ส่งใหม่)
```

### Purchasing (PR → PO → GRN → AP)
```
Draft → รออนุมัติ → อนุมัติแล้ว → PO Open → สินค้าเข้าแล้ว → รอวางบิล → ปิดรายการ
           ↓
       Rejected → Draft (แก้ไข/ส่งใหม่)
```

### Warehouse
```
Draft → รอตรวจสอบ → อนุมัติ → สินค้าเข้า/ออกแล้ว → ปิดงาน
```

### Service / ศูนย์บริการ
```
Draft → นัดหมายแล้ว → รอช่าง → ดำเนินงาน → ส่งงาน/รออนุมัติ → ปิดงาน
                                                                    ↓ (ช่างนอก)
                                                              ตั้งหนี้ช่าง
```

### Promotion / Accrual Claim (Supplier)
```
Draft → รออนุมัติ → Active → Claim → รอเงินเข้า → รับเงินแล้ว
                     ↓
                  Expired
           ↓
       Rejected → Draft
```

### AR / Credit
```
Draft → รออนุมัติ → อนุมัติ → วางบิล → ค้างชำระ → รับชำระแล้ว → ปิดบัญชี
           ↓
        ปฏิเสธ → Draft
```

### Finance / Expense / AP / Tax
```
Draft → รออนุมัติ → อนุมัติ → จ่ายแล้ว → ปิดงาน
           ↓
        ปฏิเสธ → Draft
```

### Online / Marketplace
```
Draft → รอตรวจสอบ → อนุมัติ → จัดส่งแล้ว → ปิดงาน
```

---

## 🎨 UX Rules — Confirmed Patterns (Oct 2025)

กฎ UX ที่ confirm แล้ว ห้ามละเมิด:

| # | กฎ | รายละเอียด |
|---|---|---|
| UX1 | **Inline Edit** | แก้ไข Line Items ได้เลยที่บรรทัด — ห้ามใช้ Popup |
| UX2 | **Barcode Scan** | ทุกช่องที่เหมาะสม (Item, Serial) รองรับ Barcode Scan |
| UX3 | **Serial Import/Export** | ที่ Line Level — ปุ่ม Import/Export CSV |
| UX4 | **Document Chain** | กดจาก PO → เห็น PR ต้นทาง ย้อนกลับได้ (SC5) |
| UX5 | **Show More/Less** | ซ่อน Field ที่ไม่ใช้บ่อย — ปุ่มขยาย/ย่อ |
| UX6 | **3 Address Types** | ลูกค้ามีที่อยู่ 3 แบบ: บัตรปชช / จัดส่ง / ใบกำกับภาษี |
| UX7 | **VAT Options** | ต่อเอกสาร: รวม VAT / ไม่รวม VAT / ไม่แสดง VAT |
| UX8 | **Bundle Item** | ต้องมีหน้าจอรองรับสินค้าชุด |
| UX9 | **QR Status Track** | ลูกค้าดูสถานะสินค้า/จัดส่งผ่าน QR Code บนใบเสร็จ |
| UX10 | **QR Payment (2 layers)** | (1) Invoice QR (Ref1=INV, ยอด fix) บน SL-3/SL-4 · (2) Customer QR (Ref1=CustCode, ยอด open) บนหน้าค้นลูกค้า + MD-2 → ส่ง LINE → FI-1Q Apply Queue |
| — | ID Card Scan | Post Go-Live |
| — | Document Flow Visual | Post Go-Live |
| — | Web Filter ละเอียด | ใช้ Power BI แทน |

---

## 🗄️ BC365 API — Table Numbers Reference

| Module | Endpoint | BC Table |
|---|---|---|
| Sales Invoice | POST /salesOrders | Sales Header (36), Sales Line (37) |
| Sales Quote / Reservation | POST /salesQuotes | Sales Quote Header (6660), Sales Quote Line (6661) |
| Sales Prepayment (Deposit) | Custom API | Sales Prepayment Header (Custom) |
| Customer Create | POST /customers | Customer (18) |
| WH Transfer Order | POST /transferOrders | Transfer Header (5740), Transfer Line (5741) |
| Serial Entry | PATCH /itemLedgerEntries | Item Ledger Entry (32) |
| Vendor Create | POST /vendors | Vendor (23) |
| Purchase Order | POST /purchaseOrders | Purchase Header (38), Purchase Line (39) |
| Item Approve | POST /items | Item (27) |
| Service Receive | POST /serviceOrders | Service Header (5900), Service Line (5901) |
| Parts Requisition | POST /serviceItemComponents | Service Item Components (5943) |
| Claim | Custom API | Claim Custom Table |
| AP Invoice | POST /purchaseInvoices | Purchase Invoice Header (122), Purchase Invoice Line (123) |
| Payment Journal | POST /paymentJournals | Gen. Journal Line (81) |
| AR Match | POST /salesInvoices | Sales Invoice Header (112), Sales Invoice Line (113) |
| Credit Limit | PATCH /customers | Customer (18) — CreditLimit field |
| Sales Credit Memo | POST /creditMemos | Sales Credit Memo Header (114) |

---

## 🚚 Service Module — Delivery & Installation Sub-module (Phase 2)

### Sub-module 4.x — บริการจัดส่งและติดตั้ง

| หน้าจอ | รหัส | รายละเอียด |
|---|---|---|
| Delivery Queue | SV-4.1 | คิวงานจัดส่ง/ติดตั้ง แสดงตาม Branch + วันที่ + สถานะ |
| Delivery Job Card | SV-4.2 | Form บันทึกงานจัดส่ง/ติดตั้ง (Serial, Address, Technician) |
| Delivery Completion | SV-4.3 | ปิดงาน: รูปถ่าย Before/After, ลูกค้าเซ็นรับ, Rating |

**Business Rules:**
- ทริก: Sales Invoice ที่มี Delivery Flag = true → สร้าง Delivery Job อัตโนมัติ
- Serial ต้องบันทึกก่อนปิดงาน (SC8)
- Address ใช้ SC1 → 3 Address Types (ที่อยู่จัดส่ง)
- ช่างใช้ Mobile App Group A เพื่อ Check-in / ถ่ายรูป
- Status Flow: `ใบแจ้งงาน → นัดหมาย → จัดส่ง → ติดตั้งสำเร็จ → ปิดงาน`

---

## 💰 Finance Module — ส่วนที่เพิ่มใหม่ (Phase 2)

### Finance 2.5 — Expense & Payment Voucher

```
วัตถุประสงค์: บันทึกค่าใช้จ่ายทั่วไป (ที่ไม่ผ่าน AP/PO) และออก Payment Voucher

หน้าจอ:
- Expense List: รายการค่าใช้จ่าย + สถานะ
- Expense Form: เจ้าหนี้ / ประเภทค่าใช้จ่าย / GL Account / Amount
- Payment Voucher: เลขที่ใบสำคัญ / วันที่จ่าย / วิธีชำระ (เช็ค/โอน)

Status Flow: Draft → รออนุมัติ → อนุมัติ → จ่ายแล้ว → ปิดงาน

BC API: POST /paymentJournals, POST /generalLedgerEntries
RBAC: Accountant (Create), Finance Manager (Approve+Post)
```

### Finance 2.6 — Credit Control Dashboard

```
วัตถุประสงค์: ติดตามลูกหนี้ที่เกินวงเงินหรือเกินกำหนดชำระ

หน้าจอ:
- Credit Control List: ลูกหนี้ทั้งหมด + ยอดค้าง + เกินกำหนดกี่วัน + Alert
- Customer Credit Profile: ประวัติชำระ, วงเงิน, เอกสารค้าง
- Alert Actions: ปล่อยให้ขายต่อ / Hold / ส่ง Notice

Business Rules:
- ถ้า Outstanding > Credit Limit → ขึ้น Alert สีแดงทุก Module
- ถ้า Overdue > 30 วัน → Email/LINE Notify อัตโนมัติ (B5)
- SC1 ต้องแสดง Credit Status ก่อน User เปิดบิลใหม่

BC API: GET /customerLedgerEntries?customerId=, PATCH /customers (credit fields)
```

---

## 🔌 Integration & API Module (Phase 2+3) — Module #8

### วัตถุประสงค์
ศูนย์กลางติดตามการเชื่อมต่อระหว่าง Portal ↔ BC365 ↔ ระบบภายนอก

### หน้าจอหลัก

| หน้าจอ | Phase | รายละเอียด |
|---|---|---|
| API Sync Monitor | P2 | แสดงสถานะการ Sync แต่ละ Module: ล่าสุดเมื่อ, Success/Fail Count |
| Error Log | P2 | รายการ API Error + Response Code + Retry Button |
| Webhook Config | P2 | กำหนด Webhook URL ที่รับ Event จาก BC (Post, Approve, etc.) |
| Marketplace Connector | P3 | ตั้งค่า Shopee/Lazada API Key, Sync Status |
| BC Entity Explorer | P3 | ดู BC Entity ที่ Portal ใช้ + Field Mapping Summary |

### Business Rules
- ทุก API Call ต้องมี Retry (3 ครั้ง) ก่อน Error Log
- Error ร้ายแรง → Alert Admin ผ่าน LINE Notify
- Log เก็บ 90 วัน (PDPA)
- Admin Only — ซ่อน Module นี้จาก Non-Admin Role

---

## 📂 Master Data vs System Config — แนวทางออกแบบ

### Master Data Module (MD) — ข้อมูลอ้างอิง
**ใครสร้าง:** User ทั่วไปที่มีสิทธิ์ (Sales Coordinator, Admin)
**ลักษณะ:** เปลี่ยนบ่อย ตามธุรกิจ

| หน้าจอ | รายละเอียด |
|---|---|
| Item Master | สินค้า: รหัส, ชื่อ TH/EN, หมวด, UOM, Serial Flag, ราคาต้นทุน |
| Customer Master | ลูกค้า: ข้อมูล KYC, กลุ่มราคา, วงเงิน, 3 Address |
| Vendor Master | ผู้จัดจำหน่าย: ข้อมูล + เงื่อนไขการค้า |
| Employee Master (ใหม่) | พนักงาน: รหัส, ชื่อ, ตำแหน่ง, Branch, Commission Rate |
| Branch & WH Master (ใหม่) | สาขา: ที่อยู่, Warehouse ที่สังกัด, Contact, Manager |
| Price List | ราคาตามกลุ่มลูกค้า / ช่วงเวลา |

### System Config Module (CF) — ตั้งค่าระบบ
**ใครสร้าง:** System Admin เท่านั้น
**ลักษณะ:** เปลี่ยนน้อย เป็น Base Setting ของระบบ

| หน้าจอ | รายละเอียด |
|---|---|
| Tax Setup | VAT Code, WHT Category (ภ.ง.ด.3/53) |
| Number Series | เลขที่เอกสารแต่ละประเภท (SO, PO, SI, etc.) |
| Item Config | Default Posting Group, Location Policy |
| Customer/Vendor Config | Credit Term Template, Payment Method Default |
| WH Bin Policy | กฎการจัดวางสินค้าในคลัง |
| Technician Template | Template การคิดค่าแรงช่าง |
| User & Role | RBAC Matrix, Permission Assignment |

---

## 🔨 Development Checklist (ก่อนเริ่ม Implement ทุกหน้าจอ)

```
[ ] ⚠️ ตรวจ folder ว่ามีไฟล์ซ้ำไหม → ถ้ามี ต้องถามก่อนเสมอ
    (ดูตาราง "ไฟล์ซ้ำที่ตัดสินใจแล้ว" ใน Rule 2 เพื่อเทียบว่าเคยตัดสินใจแล้วหรือยัง)

[ ] 📄 อ่าน Flowchart ใน Flow Design/ ของ Module นั้นก่อน
    → ดู Status Flow, BC Entity, Document Format

[ ] อ่าน research.md + plan.md → ตรวจ Open Questions ที่เกี่ยวข้อง
    ⛔ ห้าม Implement ส่วนที่มี [?] จนกว่าจะตัดสินใจ

[ ] ดู Data Dictionary (dd_*.docx) — Field ครบหรือยัง?

[ ] ตรวจ Component Usage Matrix — SC ที่ยังไม่มีต้องพัฒนาก่อน Page

[ ] ยืนยัน RBAC: Role, Field Permission, ปุ่ม Disable

[ ] พัฒนาตาม ERP Form 7 Sections — ห้ามเปลี่ยนลำดับ

[ ] ใช้ StatusBadge สีตาม Standard — ห้ามใช้สีอื่น

[ ] ทุก Label มีทั้งไทยและอังกฤษ

[ ] Unit Test Coverage > 80%

[ ] TypeScript Strict + ESLint Airbnb + Prettier ก่อน PR
```

---

*Sangwijit Group © 2024–2026 | Proprietary — ห้ามเผยแพร่ภายนอก*
*Skill Version: 1.0 | เมษายน 2026*
