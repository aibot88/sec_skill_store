---
name: qa-tester-skill
description: Systematically test web applications for functionality, security, and usability issues using browser automation. Reports findings by severity (CRITICAL/HIGH/MEDIUM/LOW) with immediate alerts for critical failures. Use when testing web apps, validating user flows, conducting security checks, or performing pre-deployment audits.
---

# QA Tester Skill — Browser Automation

Web uygulamalarını sistematik olarak test etme ve bulguları önem derecesine göre raporlama rehberi.

## When to use this skill

- Web uygulamaları fonksiyonel test edilirken
- Pre-deployment security audit yapılırken
- Kullanıcı akışları doğrulanırken
- Accessibility veya responsive tasarım kontrol edilirken

---

## 1. KRİTİK HATA PROTOKOLÜ

**Aşağılardan birini bulursan TÜM TESTİ HEMEN DURDUR:**

- Server çöktü veya tamamen başarısız
- Veritabanı bağlantı hataları
- API key, token, şifre HTML/JS'te görünür
- Authentication bypass — girişsiz korunan alanlara erişim
- Veri bozulması veya kayıp

**Kritik hata formatı:**

```
🚨 KRİTİK HATA BULUNDU — TEST DURDURULDU

Başlık: [Kısa açıklama]
Önem: KRİTİK
Bileşen: [Hangi bölüm]

NE OLDU:
[Hatayı açıkla]

YENİDEN OLUŞTURMA ADIMLARI:
1. [Adım 1]
2. [Adım 2]
3. [Hata oluştu]

KONSOL LOGLARI:
[Tüm console error'ları yapıştır]

HİPOTEZ VE ANALİZ:
- Olası neden: [Teori 1]
- Nereye bakılmalı: [Spesifik dosya/alan]
- Hızlı çözüm önerisi: [Varsa]

SONRAKİ ADIMLAR:
- Bu sorun düzeltilmeden test devam edemez
```

---

## 2. Test Fazları

| Faz       | Durum               | Süre     | Odak                           |
| --------- | ------------------- | -------- | ------------------------------ |
| **Faz 1** | MVP / Yeni uygulama | 30-60 dk | Temel çalışıyor mu?            |
| **Faz 2** | Beta / Pre-launch   | 2-4 saat | Kapsamlı fonksiyon + güvenlik  |
| **Faz 3** | Production hazır    | 4-8 saat | Edge case, stress, final audit |

---

## 3. Faz 1 — Erken Aşama Test Listesi (30-60 dk)

### A. İlk Yükleme (5 dk)

```typescript
await page.goto(url)
// Console error kontrol
page.on('console', (msg) => {
  if (msg.type() === 'error') console.log('ERROR:', msg.text())
})
```

Kontrol et:

- [ ] Sayfa yükleniyor mu?
- [ ] Console'da kırmızı hata var mı? (Kritikse DURDUR)
- [ ] Metin görünür ve okunabilir mi?

### B. Navigasyon (10 dk)

```typescript
const buttons = await stagehand.observe('tüm navigasyon butonlarını ve linkleri bul')
for (const button of buttons) {
  await stagehand.act(button)
}
```

- [ ] Tüm nav butonları/linkleri çalışıyor
- [ ] Her link bir şey yapıyor (kırmızı hata → KRİTİK)

### C. Core Fonksiyon (20 dk)

```typescript
await stagehand.act('ana özelliği kullan')
```

- [ ] Birincil kullanıcı aksiyonu çalışıyor
- [ ] Tüm görünür butonlar bir şey yapıyor
- [ ] Form input'ları validate ediliyor

### D. Güvenlik Hızlı Kontrol (10 dk)

```typescript
const html = await page.content()
const secretPatterns = [
  /AKIA[0-9A-Z]{16}/g,          // AWS Key
  /sk_live_[a-zA-Z0-9]{24,}/g,  // Stripe Secret
  /api[_-]?key['"]?\s*[:=]/gi,  // Generic API key
  /eyJ[a-zA-Z0-9_-]*\.eyJ/g,    // JWT token
]
for (const pattern of secretPatterns) {
  const matches = html.match(pattern)
  if (matches) {
    console.log('🚨 KRİTİK: HTML'de secret bulundu!', matches)
  }
}
```

- [ ] HTML'de secret yok (API key, token, şifre)
- [ ] localStorage'da sensitive veri yok
- [ ] Cookie'ler güvenli

### E. Responsive Kontrol (5 dk)

```typescript
await page.setViewportSize({ width: 375, height: 667 })
await page.screenshot({ path: '/tmp/mobile.png' })
```

- [ ] Mobil görünümde içerik görünür
- [ ] Yatay scroll yok

---

## 4. Faz 2 — Kapsamlı Test Ek Listesi

### Authentication ve Authorization

```typescript
// Korunan sayfaya girişsiz erişim dene
await page.goto(`${url}/dashboard`)
const redirected = page.url().includes('/login')
if (!redirected) console.log('⚠️ Auth bypass: /dashboard girişsiz erişilebilir!')
```

- [ ] Korunan sayfalara girişsiz erişim engelleniyor
- [ ] Admin sayfaları normal kullanıcıdan erişilemiyor
- [ ] Session logout'ta temizleniyor

### XSS Testi

```typescript
const xssPayloads = ['<script>alert("XSS")</script>', '<img src=x onerror=alert("XSS")>', 'javascript:alert("XSS")']
for (const payload of xssPayloads) {
  await stagehand.act(`input alanına '${payload}' yaz`)
}
```

- [ ] Script execute edilmiyor (HIGH → KRİTİK eğer user-facing)

### SQL Injection Testi

```typescript
const sqlPayloads = ["' OR '1'='1", "'; DROP TABLE users--", "1' UNION SELECT NULL--"]
```

- [ ] SQL injection çalışmıyor (KRİTİK)

### Performans

```typescript
const start = Date.now()
await page.goto(url, { waitUntil: 'networkidle' })
const loadTime = Date.now() - start
if (loadTime > 3000) console.log(`⚡ MEDIUM: Yükleme süresi ${loadTime}ms (>3s)`)
if (loadTime > 10000) console.log(`⚠️ HIGH: Yükleme süresi ${loadTime}ms (>10s)`)
```

### Security Header'ları

```typescript
const response = await page.goto(url)
const headers = response.headers()
const required = ['content-security-policy', 'x-frame-options', 'strict-transport-security']
for (const header of required) {
  if (!headers[header]) console.log(`⚡ MEDIUM: Eksik header: ${header}`)
}
```

### Accessibility

```typescript
// Alt text kontrol
const images = await page.evaluate(() => Array.from(document.images).map((img) => ({ src: img.src, alt: img.alt })))
const missingAlt = images.filter((img) => !img.alt)
if (missingAlt.length) console.log('ℹ️ LOW: Alt text eksik görseller:', missingAlt)
```

---

## 5. Önem Derecesi Kılavuzu

### 🚨 KRİTİK — Testi Hemen Durdur

- Server çöktü / başlamıyor
- Database bağlantı hatası
- Authentication bypass
- API key/secret HTML'de görünür
- SQL injection açığı var
- Veri kaybı veya bozulması

### ⚠️ YÜKSEK — Acil Raporla, Testi Sürdür

- Core feature tamamen çalışmıyor
- XSS, CSRF güvenlik açığı
- Login bozuk bazı kullanıcılar için
- Admin yetkisizken erişilebilir
- HTTPS zorunlu değil

### ⚡ ORTA — Belgele, Sürdür

- Kritik olmayan feature bozuk
- Kötü error mesajları
- Performans >3 saniye
- Büyük UI hizalama sorunu
- Eksik input validation

### ℹ️ DÜŞÜK — Raporda Not Et

- Yazım hataları
- Küçük renk kontrast sorunları
- Eksik tooltip
- Minor responsive sorun
- Non-blocking console uyarıları

---

## 6. Rapor Şablonu

### Tekil Bulgu Formatı

```markdown
## Bulgu #[N]: [Kısa Başlık]

**Önem**: [KRİTİK/YÜKSEK/ORTA/DÜŞÜK]
**Bileşen**: [Login, Checkout, Navigation...]
**Kategori**: [Güvenlik/Fonksiyon/UX/Performans/Erişilebilirlik]

### Açıklama

[Net açıklama]

### Yeniden Oluşturma

1. [Adım 1]
2. [Adım 2]
3. [Sorun oluşur]

### Beklenen Davranış

[Ne olmalıydı]

### Gerçekleşen Davranış

[Ne oldu]

### Analiz ve Hipotez

- Olası neden: [Teori]
- Nereye bakılmalı: [Dosya/bileşen]

### Öneri

[Nasıl düzeltilir — spesifik olun]
```

### Final Rapor Formatı

```markdown
# QA Test Raporu — [Uygulama Adı]

**Tarih**: [Tarih]
**Faz**: [1/2/3]
**URL**: [Test URL]

## Özet

- Toplam Bulgu: [N]
- Kritik: [N] 🚨
- Yüksek: [N] ⚠️
- Orta: [N] ⚡
- Düşük: [N] ℹ️

**Öneri**: [DEVAM / HAYIR / KOŞULLU DEVAM]

## Kritik Bulgular 🚨

[Varsa listele]

## Yüksek Öncelikli Bulgular ⚠️

[Varsa listele]

## Orta Öncelikli Bulgular ⚡

[Varsa listele]

## Düşük Öncelikli Bulgular ℹ️

[Varsa listele]

## Test Kapsamı

### ✅ Test Edilen Alanlar

- [Alan 1]

### ❌ Test Edilmeyen Alanlar

- [Alan 1]

## Öneriler

### Acil (Launch Öncesi)

1. ...

### Kısa Vadeli (1 ay)

1. ...
```

---

## 7. Hızlı Başvuru

```
Karar ağacı:
- Uygulama çöktü?    → KRİTİK, DURDUR
- Secret açık?        → KRİTİK, DURDUR
- Core feature bozuk? → YÜKSEK
- Güvenlik açığı?    → YÜKSEK
- Feature kısmen çalışıyor? → ORTA
- UI sorunu?          → DÜŞÜK/ORTA
- Yazım hatası?       → DÜŞÜK

KRİTİK HATA = TÜM TEST DURUR
```
