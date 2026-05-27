---
name: allergen-detection
description: Phát hiện 14 chất gây dị ứng theo luật EU 1169/2011 trong menu PDF và xuất PDF mới đã gắn nhãn allergen chuẩn. Trigger ngay khi user upload/mention một file menu PDF và muốn: gắn nhãn allergen, kiểm tra compliance EU, "check dị ứng", "allergen menu", "EU 1169", "label menu", "đánh dấu chất gây dị ứng", hoặc cần chuẩn bị menu cho thị trường châu Âu. Dùng khi user paste đường dẫn PDF và nói "check allergen", "label này", "scan menu" — kể cả khi không đề cập tên skill.
---

# Allergen Detection — EU 1169/2011

Phát hiện và đánh dấu 14 chất gây dị ứng bắt buộc theo Regulation (EU) No 1169/2011 trực tiếp trong menu PDF. Output là file PDF gốc được giữ nguyên layout, chỉ thêm số EU allergen dạng plain text cùng màu/size với tên món bên cạnh mỗi món có allergen.

## Pipeline tổng quan

```
Menu PDF → [Extract text + positions + font info] → [Parse menu legend] → [AI detect allergens] → [Annotate PDF] → Output PDF
```

---

## Bước 1 — Kiểm tra dependencies

Trước khi bắt đầu, cài đặt PyMuPDF nếu chưa có:

```bash
pip3 install pymupdf
```

---

## Bước 2 — Extract text từ PDF

Chạy script extraction để lấy text kèm vị trí **và font info**:

```bash
python3 <skill-path>/scripts/annotate_pdf.py extract \
  --input "<path-to-menu.pdf>" \
  --output "<workspace>/menu_extracted.json"
```

Script xuất JSON gồm danh sách text blocks, mỗi block có: `text`, `page`, `bbox`, `dom_size` (font size lớn nhất), và `spans` (từng span với fontname, fontsize, color).

---

## Bước 3 — Parse menu allergen legend (QUAN TRỌNG)

> ⚠️ **Nhiều nhà hàng (đặc biệt ở Đức, Áo) dùng hệ thống đánh số allergen RIÊNG** (ví dụ: 1=Gluten, 2=Milch, 3=Eier, 4=Soja...) khác hoàn toàn với EU standard (EU-7=Milk, EU-6=Soybeans...). Nếu bỏ qua bước này sẽ map sai allergen ID.

**Trước khi detect**, scan `menu_extracted.json` để tìm trang "Zusatzstoffe", "Allergene", "Additives", hoặc bảng chú thích allergen của nhà hàng.

Ví dụ typical German menu legend:
```
1 Gluten    →  EU #1
2 Milch     →  EU #7   ← KHÁC!
3 Eier      →  EU #3
4 Soja      →  EU #6   ← KHÁC!
5 Senf      →  EU #10  ← KHÁC!
6 Erdnuss   →  EU #5   ← KHÁC!
7 Fisch     →  EU #4   ← KHÁC!
8 Schalenfrüchte → EU #8
9 Sesamsamen    → EU #11  ← KHÁC!
10 Sellerie     → EU #9   ← KHÁC!
11 Lupine       → EU #13  ← KHÁC!
12 Weichtiere   → EU #14  ← KHÁC!
13 Krebstiere   → EU #2   ← KHÁC!
14 Schwefeldioxid/Sulfite → EU #12 ← KHÁC!
```

Xây dựng `menu_to_eu` mapping trước khi detect:
```json
{
  "menu_to_eu": {
    "1": 1, "2": 7, "3": 3, "4": 6,
    "5": 10, "6": 5, "7": 4, "8": 8,
    "9": 11, "10": 9, "11": 13,
    "12": 14, "13": 2, "14": 12
  }
}
```

Nếu menu **không có** bảng chú thích riêng → dùng EU standard trực tiếp (bỏ qua mapping).

---

## Bước 4 — AI detect allergens (inline)

Đọc file `references/eu_allergens.md` để nắm toàn bộ 14 allergen EU và danh sách nguyên liệu liên quan.

Phân tích `menu_extracted.json`: với **mỗi món ăn** (dish name + description), xác định allergen nào có mặt:

1. **Đọc số allergen nhà hàng tự ghi** cạnh tên món (ví dụ: "Nem ran 3, 6, 7") → dùng `menu_to_eu` mapping để chuyển sang EU IDs
2. **Suy ra từ ingredients** trong mô tả (ví dụ: "Teigtaschen" → wheat → EU#1 Gluten)
3. **Suy ra từ cuisine context** (ví dụ: Pho luôn có Quẩy → EU#1; "nước mắm" → EU#4 Fish)

> **Lưu ý quan trọng:**
> - Coconut milk (`Kokosmilch`) **KHÔNG** phải EU#7 Milk — đây là nguồn gốc thực vật, không cần khai báo
> - Số lượng (`3 stk.`, `4 Stk.`) **KHÔNG** phải allergen code — phân biệt với số allergen
> - Khi một món có nhiều allergen từ menu code VÀ từ suy luận: gộp tất cả, phân biệt confidence

Xuất kết quả dưới dạng `allergen_map.json`:

```json
{
  "source": "<filename>",
  "restaurant": "<tên nhà hàng nếu có>",
  "menu_to_eu": { "1": 1, "2": 7, ... },
  "dishes": [
    {
      "dish_name": "Tên món như trong PDF (kể cả số menu nếu có)",
      "page": 1,
      "allergen_ids": [1, 3, 7],
      "confidence": "high",
      "notes": "Lý do: menu code 3=Eier(EU3), 6=Erdnuss(EU5)..."
    }
  ]
}
```

> **Confidence levels:**
> - `high` — allergen rõ ràng có trong tên/mô tả hoặc từ menu code chính xác
> - `medium` — allergen có thể có (theo recipe thông thường, nhưng không được ghi rõ)
> - `low` — chỉ nghi ngờ, cần xác nhận với nhà hàng

Lưu vào `<workspace>/allergen_map.json`.

---

## Bước 5 — Annotate PDF

```bash
python3 <skill-path>/scripts/annotate_pdf.py annotate \
  --input "<path-to-menu.pdf>" \
  --allergens "<workspace>/allergen_map.json" \
  --output "<workspace>/menu_allergen_labeled.pdf"
```

Script sẽ:
1. Tìm từng món trong PDF theo tên (clean name → fuzzy match)
2. Đọc font size và color thực của tên món từ PDF
3. Thêm số EU allergen dạng plain text ngay sau tên món, **cùng màu và size** với chữ gốc — không circle, không highlight
4. Thêm trang cuối: **Legend** + **Disclaimer** chuẩn pháp lý

---

## Bước 6 — Trình bày kết quả

Sau khi script chạy xong, báo cáo với user:

```
✅ Allergen detection hoàn tất
📄 Output: <workspace>/menu_allergen_labeled.pdf
🔍 Tổng số món: X
⚠️  Món có allergen: Y
❗ Món confidence=low (cần xác nhận): Z
```

Liệt kê các món `confidence=low` để user xem xét thủ công.

---

## Disclaimer bắt buộc (thêm vào output PDF)

Script tự động thêm trang cuối với nội dung sau (giữ nguyên ngôn ngữ theo menu hoặc dùng tiếng Anh làm default):

> **ALLERGEN INFORMATION — EU Regulation No 1169/2011**
>
> This document has been generated by an AI system to assist in allergen identification. While every effort has been made to ensure accuracy, the information provided is indicative only and may not reflect actual preparation methods, cross-contamination risks, or ingredient substitutions.
>
> **This document does not constitute legal compliance certification.** Restaurant operators remain solely responsible for verifying allergen information with ingredient suppliers and ensuring compliance with applicable food labeling regulations. Customers with severe allergies should always consult staff directly before ordering.

---

## Edge cases cần xử lý

- **Số lượng vs Số allergen**: `"Gyoza Chicken 4 Stk."` — "4 Stk." = 4 miếng, KHÔNG phải allergen code 4
- **Phần "Drinks" / "Beverages"**: Vẫn scan — sulphites có trong wine/beer
- **Coconut milk**: KHÔNG phải EU#7 Milk — không cần tag
- **Combo/Set menu**: Tag allergens của tất cả các thành phần trong combo
- **"May contain" / "traces"**: Không tag bằng số — ghi chú riêng `(†)` với footnote "may contain traces"
- **Món không có mô tả**: Chỉ dùng tên món, đặt confidence=low, flag cho user

---

## Tham khảo thêm

Đọc `references/eu_allergens.md` để tra cứu:
- Danh sách đầy đủ 14 allergens với ID chuẩn EU
- Common ingredients và tên thay thế (EN + VI)
- Các trường hợp ngoại lệ theo annex II của EU 1169/2011
