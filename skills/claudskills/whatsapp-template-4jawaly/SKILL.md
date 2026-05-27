---
name: whatsapp-template-4jawaly
description: إرسال قوالب واتساب (Meta-approved templates) عبر 4jawaly مع تثبيت كل العوامل (endpoint، auth، namespace، language) وتغيير body/parameters فقط. استخدمها عند ذكر "قالب واتساب"، "template"، "OTP"، "إشعار" أو أي إرسال خارج نافذة الـ 24 ساعة.
---

# 4jawaly WhatsApp Templates

## الثابت في كل الطلبات
- Endpoint: `POST https://api-users.4jawaly.com/api/v1/whatsapp/{PROJECT_ID}` — `PROJECT_ID` متغيّر حسب الحساب (مثال: `591`)، اقرأه من env `JAWALY_WA_PROJECT_ID`.
- Headers: `accept: application/json`, `Content-Type: application/json`, `Authorization: Basic {{TOKEN}}` (نفس التوكن للقوالب الثلاثة).
- `path`: دائماً `"message/template"`.
- `language`: `{"policy":"deterministic","code":"ar"}`.
- `namespace`: `"d62f7444_aa0b_40b8_8f46_0bb55ef2862e"`.

## المتغيرات في كل طلب
- `phone`: رقم المستلم دولي بدون `+`.
- `template`: اسم القالب المفعّل من Meta.
- `params`: مصفوفة المكوّنات (body/button/header) — تعتمد على متغيرات القالب.

## الشكل العام
```json
{
  "path": "message/template",
  "params": {
    "phone": "{{PHONE}}",
    "template": "{{TEMPLATE_NAME}}",
    "language": {"policy":"deterministic","code":"ar"},
    "namespace": "d62f7444_aa0b_40b8_8f46_0bb55ef2862e",
    "params": [ /* مكوّنات */ ]
  }
}
```

## الحالة 1 — قالب بدون متغيرات
`params: []` فقط. مثال (`not4j2`):
```json
{"path":"message/template","params":{
  "phone":"{{PHONE}}","template":"not4j2",
  "language":{"policy":"deterministic","code":"ar"},
  "namespace":"d62f7444_aa0b_40b8_8f46_0bb55ef2862e",
  "params":[]}}
```

## الحالة 2 — قالب بـ body متغيّر متعدد (مثال `account_pricing_update_notification` بـ 4 متغيرات)
```json
"params": [
  {"type":"body","parameters":[
    {"type":"text","text":"{{BODY_1}}"},
    {"type":"text","text":"{{BODY_2}}"},
    {"type":"text","text":"{{BODY_3}}"},
    {"type":"text","text":"{{BODY_4}}"}
  ]}
]
```

## الحالة 3 — body + زر URL ديناميكي (مثال OTP `gocode`)
```json
"params": [
  {"type":"body","parameters":[{"type":"text","text":"{{OTP_CODE}}"}]},
  {"type":"button","index":0,"sub_type":"URL",
   "parameters":[{"type":"text","text":"{{OTP_CODE}}"}]}
]
```

## القاعدة المستنتجة
> ثبّت كل العوامل (endpoint, auth, namespace, language, path) واملأ فقط: `phone`, `template`, ومحتوى `params`. عدد عناصر `parameters` داخل `body` = عدد المتغيرات `{{1}}..{{N}}` المعتمَدة في القالب من Meta. أي إضافة/نقصان يُعيد الخطأ من Meta.

## curl موحّد
```bash
curl -X POST "https://api-users.4jawaly.com/api/v1/whatsapp/$PROJECT_ID" \
  -H "accept: application/json" -H "Content-Type: application/json" \
  -H "Authorization: Basic $TOKEN" \
  -d @template.json
```

## تلميحات للوكيل
- لا تخمّن أسماء القوالب — يجب أن تكون موافَقاً عليها من Meta لنفس `namespace`.
- ترتيب `parameters` يجب أن يطابق ترتيب `{{1}}..{{N}}` في القالب.
- للأزرار: `index` يبدأ من 0 ويطابق ترتيب الأزرار في القالب، و `sub_type` ∈ `URL` | `QUICK_REPLY`.
- لا تُسجّل `Authorization` في اللوقات.
