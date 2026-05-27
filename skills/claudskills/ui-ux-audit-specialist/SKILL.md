---
name: ui-ux-audit-specialist
description: Audit UI components and pages for accessibility, design system compliance, responsive design, UX writing quality, and performance. Use when asked to review, audit, or check any UI file, component, or page against platform standards.
---

# UI/UX Audit Specialist Skill

Modern web uygulamalarının UI bileşenlerini ve sayfalarını profesyonel standartlara, accessibility kurallarına ve design system uyumuna göre denetleme skill'i.

## When to use this skill

- "Şu component'i gözden geçir" isteklerinde
- PR review öncesi UI denetimi yapılırken
- Accessibility audit istendiğinde
- Design system uyumu kontrol edilirken
- UX copy kalitesi değerlendirilirken
- Responsive davranış test edilirken

## How to use it

- Her zaman içsel olarak İngilizce düşün
- Her zaman kullanıcıya Türkçe yanıt ver
- Kod veya konfigürasyon dosyalarına comment satırı yazma
- Bulguları `dosya:satır` formatında raporla

---

## Audit Süreci

Belirtilen dosya(lar)ı şu sırayla denetle:

1. **Design Token Uyumu** — Hardcoded değer var mı?
2. **Accessibility** — WCAG AA gereksinimleri karşılanıyor mu?
3. **Dark Mode Parity** — Her token dark modda test edildi mi?
4. **Responsive** — Tüm breakpoint'ler kapsanıyor mu?
5. **UX Writing** — Microcopy kalite standartları karşılanıyor mu?
6. **Component Pattern** — CVA, compound component, asChild doğru kullanılıyor mu?
7. **Performance** — Gereksiz re-render, animasyon sorunu var mı?
8. **TypeScript** — `any` tipi, eksik tip annotation var mı?

---

## Output Format

Her bulgu şu formatla raporlanmalı:

```
[R-KURAL-NO] dosya/yolu:satır_no
  SORUN: Kısa açıklama
  MEVCUT: Sorunlu kod snippet'i
  BEKLENEN: Düzeltilmiş hali
  ÖNCELİK: Kritik | Yüksek | Orta | Düşük
```

**Öncelik Tanımları**:

- **Kritik**: Accessibility kırık, dark mode tamamen bozuk, console error
- **Yüksek**: WCAG AA uyumsuzluk, hardcoded renk, generic error mesajı
- **Orta**: Responsive eksiklik, UX copy kalitesi, loading state eksik
- **Düşük**: Minor token tutarsızlığı, stil iyileştirmesi
