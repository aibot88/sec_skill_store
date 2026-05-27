---
name: icerik-uret
description: "mertkagancetin.com icin topical authority stratejisine uygun hukuki icerik uretir. Blog yazisi, sozluk terimi veya icerik analizi yapar. /icerik-uret komutuyla calistirilir."
argument-hint: "[blog|sozluk|analiz] [kira|bosanma] [konu]"
---

# mertkagancetin.com Hukuki İçerik Üretici

Bu skill, Mert Kağan Çetin Hukuk Bürosu web sitesi (mertkagancetin.com) için topical authority stratejisine uygun içerik üretir.

## Kullanım

```
/icerik-uret                              → Eksik içerik analizi, öneriler
/icerik-uret analiz                       → Tüm cluster'ları tarayıp eksik konuları listeler
/icerik-uret blog kira "Depozito İadesi"  → Spesifik blog yazısı üretir
/icerik-uret sozluk bosanma "Velayet"     → Sözlük terimi üretir
```

Argüman verilmezse veya `analiz` komutu verilirse: mevcut içerikleri tara, eksik konuları listele, hangi cluster'da eksik var göster, öncelik sıralaması sun.

---

## Proje Yapısı

- **Blog dosyaları:** `src/content/blog/*.mdx`
- **Sözlük verileri:** `src/lib/glossary.ts` (TypeScript dizisi)
- **Blog utils:** `src/lib/blog/utils.ts` (getAllPosts, getPostBySlug)

---

## Blog Yazısı Üretim Kuralları

### Frontmatter Formatı (YAML)

```yaml
---
title: "SEO odaklı başlık"
date: "YYYY-MM-DD"
dateModified: "YYYY-MM-DD"
excerpt: "160 karakterlik meta description"
tags: ["tag1", "tag2", "tag3"]
coverImage: "https://images.unsplash.com/photo-xxx?q=80&w=1200&auto=format&fit=crop"
faqs:
  - question: "Soru 1?"
    answer: "3-4 cümlelik detaylı cevap."
  - question: "Soru 2?"
    answer: "3-4 cümlelik detaylı cevap."
  - question: "Soru 3?"
    answer: "3-4 cümlelik detaylı cevap."
  - question: "Soru 4?"
    answer: "3-4 cümlelik detaylı cevap."
---
```

### İçerik Yapısı

```
## [Ana Başlık]

[Giriş paragrafı - konuyu özetle, pillar sayfaya link ver]

[İkinci paragraf - konunun önemini ve güncelliğini vurgula]

---

## Özet

- [Hap bilgi 1]
- [Hap bilgi 2]
- [Hap bilgi 3]
- [Hap bilgi 4]

---

## [Alt Başlık 1 - Hukuki Dayanak]

[Detaylı paragraflar, kanun maddeleri, Yargıtay kararları...]

---

## [Alt Başlık 2 - Süreç/Uygulama]

[Pratik senaryo 1]
[Pratik senaryo 2]

---

![Alt metin](https://images.unsplash.com/photo-xxx)

---

## [Alt Başlık 3 - Dikkat Edilmesi Gerekenler]

[Detaylı paragraflar...]

---

## Sık Sorulan Sorular

### [Soru 1]
[3-4 cümlelik detaylı cevap - frontmatter'daki ile AYNI OLMALI]

### [Soru 2]
[3-4 cümlelik detaylı cevap]

### [Soru 3]
[3-4 cümlelik detaylı cevap]

### [Soru 4]
[3-4 cümlelik detaylı cevap]

---

## Profesyonel Hukuki Destek

[CTA paragrafı - pillar sayfaya ve iletişim'e link ver]

---

*Bu makale genel bilgilendirme amaçlıdır ve hukuki tavsiye niteliği taşımamaktadır. Somut durumunuz için mutlaka bir avukata danışmanız önerilir.*
```

### İçerik Kuralları

1. **Uzunluk:** 1500-2000 kelime
2. **Stil:** Akıcı, profesyonel paragraflar. Her paragraf 3-5 cümle. Hukuki ama anlaşılır dil.
3. **Emoji KULLANMA.** Sadece düz metin.
4. **Kanun referansları:** Spesifik kanun maddelerini belirt (TBK, İş Kanunu 4857, TMK, SGK 5510, vb.)
5. **Yargıtay kararları:** Gerçekçi daire ve yıl bilgisi ile atıf yap.
6. **Pratik senaryolar:** En az 2 gerçekçi örnek/senaryo ekle.
7. **FAQ:** Frontmatter'da 4+ soru-cevap. İçerikte de aynı soruları "Sık Sorulan Sorular" bölümünde tekrarla.
8. **Bölüm ayracı:** Her bölüm arasında `---` kullan.
9. **Görsel:** Makale ortasına 1 Unsplash görseli ekle. `![alt](url)` formatı.
10. **Dosya adı:** Türkçe slug formatında `.mdx` uzantılı. Örnek: `depozito-iadesi-davasi-kiracinin-haklari-ve-surec.mdx`
11. **Kaydetme yeri:** `src/content/blog/{slug}.mdx`

---

## Sözlük Terimi Üretim Kuralları

Sözlük terimleri `src/lib/glossary.ts` dosyasındaki `glossaryTerms` dizisine eklenir.

### GlossaryTerm Interface

```typescript
{
    term: "Terim Adı",
    slug: "terim-adi",
    shortDescription: "Tek cümlelik kısa açıklama.",
    definition: "1-2 paragraf resmi tanım. Kanun maddesi referansı içermeli.",
    detailedExplanation: `Detaylı açıklama (3-5 paragraf).
Pratik örnekler, uygulama detayları, dikkat edilmesi gerekenler.
Yargıtay kararı referansı içerebilir.`,
    legalBasis: "TBK m. XXX",
    category: "bosanma",  // tahliye | kira-bedeli | sozlesme | haklar | bosanma
    relatedTermSlugs: ["ilgili-terim-1", "ilgili-terim-2"],
    relatedBlogSlugs: ["ilgili-blog-slug"],
    relatedServiceAnchor: "#ilgili-hizmet",
    faqs: [
        { question: "Soru?", answer: "Cevap." },
        { question: "Soru?", answer: "Cevap." },
        { question: "Soru?", answer: "Cevap." }
    ],
    keywords: ["anahtar kelime 1", "anahtar kelime 2", "anahtar kelime 3"],
    lastUpdated: "YYYY-MM-DD",
}
```

### Sözlük Kuralları

1. Mevcut terimleri oku (`src/lib/glossary.ts`) ve çakışma olmamasını sağla.
2. `relatedTermSlugs` ile mevcut terimlere çapraz bağlantı kur.
3. `relatedBlogSlugs` ile ilgili blog yazılarına bağlantı ekle.
4. `category` doğru hukuk alanıyla eşleşmeli.
5. `keywords` SEO odaklı, "... nedir", "... nasıl hesaplanır" gibi long-tail varyasyonlar içermeli.

---

## İç Link Kuralları (Topical Authority)

Her üretilen blog yazısında aşağıdaki iç link kurallarına MUTLAKA uyulmalı:

### Zorunlu Linkler

| Tür | Minimum | Açıklama |
|-----|---------|----------|
| Pillar sayfaya link | 1 | İlgili cluster'ın ana sayfasına |
| Sibling (kardeş) makale | 2 | Aynı cluster'daki diğer blog yazılarına |
| Sözlük terimi | 1 | `/sozluk/xxx/` formatında terim linki |
| Cross-cluster (opsiyonel) | 0-1 | Diğer hukuk alanı pillar sayfasına |
| **TOPLAM** | **5+** | Minimum 5 iç link |

### Linklerin doğal yerleşimi

- Linkleri paragraf içinde doğal ve akıcı şekilde yerleştir.
- Link anchor text'i açıklayıcı olmalı (URL değil, anlamlı metin).
- Aynı URL'ye birden fazla link vermekten kaçın (pillar sayfa hariç, o 2-3 kez olabilir).
- Trailing slash kullan: `/izmir-kira-avukati/` (sonunda `/` olmalı).

---

## 2 Topic Cluster Tanımı

### CLUSTER 1: KİRA HUKUKU

- **Pillar Sayfa:** `/izmir-kira-avukati/`
- **Anchor:** "İzmir kira avukatı"
- **Kategori:** Kira Hukuku
- **Tags:** `["kira hukuku", "İzmir kira avukatı", "kiracı hakları"]`

**Mevcut Blog Yazıları:**
- `/blog/ev-sahibi-hangi-durumlarda-kiraciyi-hemen-cikarabilir/` → anchor: "kiracıyı çıkarma koşulları"
- `/blog/hangi-durumlarda-kira-tespit-davasi-acilabilir/` → anchor: "kira tespit davası"
- `/blog/ihtiyac-nedeniyle-tahliye-davasi-nasil-acilir/` → anchor: "ihtiyaç nedeniyle tahliye"
- `/blog/isyeri-kira-sozlesmelerinde-dikkat-edilmesi-gereken-hususlar/` → anchor: "işyeri kira sözleşmesi"
- `/blog/kiracinin-tahliyesi-icin-iki-hakli-ihtar-nedir/` → anchor: "iki haklı ihtar"
- `/blog/kira-hukukunda-zorunlu-arabuluculuk-sureci/` → anchor: "zorunlu arabuluculuk"
- `/blog/izmir-gayrimenkul-piyasasinda-guncel-hukuki-gelismeler/` → anchor: "gayrimenkul hukuki gelişmeler"
- `/blog/kira-sozlesmesi-fesih-sebepleri-ve-hukuki-surec/` → anchor: "kira sözleşmesi fesih sebepleri"
- `/blog/depozito-iadesi-davasi-kiracinin-haklari-ve-surec/` → anchor: "depozito iadesi davası"
- `/blog/kiracinin-aidat-borcu-ve-ev-sahibinin-sorumluluklari/` → anchor: "kiracının aidat borcu"

**Sözlük Terimleri:**
- `/sozluk/tahliye-taahhutnamesi/` → "tahliye taahhütnamesi"
- `/sozluk/kira-tespit-davasi/` → "kira tespit davası"
- `/sozluk/ihtiyac-nedeniyle-tahliye/` → "ihtiyaç nedeniyle tahliye"
- `/sozluk/fuzuli-isgal/` → "fuzuli işgal"
- `/sozluk/kira-artis-orani/` → "kira artış oranı"
- `/sozluk/depozito/` → "depozito"
- `/sozluk/kiraci-haklari/` → "kiracı hakları"

**Yazılabilecek Konular:**
1. Kira Sözleşmesi Fesih Sebepleri ve Hukuki Süreç
2. Depozito İadesi Davası: Kiracının Hakları ve Süreç
3. Kiracının Aidat Borcu ve Ev Sahibinin Sorumlulukları
4. Kira Uyarlama Davası: Şartlar ve Yargıtay Kararları
5. Alt Kiracı ve Devir Yasağı: Kiracının Sözleşme İhlali
6. Fuzuli İşgal ve Haksız Kullanım Tazminatı Davası
7. Kentsel Dönüşümde Kiracı Hakları ve Tahliye Süreci
8. 10 Yıllık Uzama Süresi Dolan Kiracının Tahliyesi
9. Kira Artış Oranı Sınırı 2026: Güncel Hesaplama Rehberi
10. Eşya Hasarı Nedeniyle Kiracıya Tazminat Davası

---

### CLUSTER 2: BOŞANMA HUKUKU

- **Pillar Sayfa:** `/izmir-bosanma-avukati/`
- **Anchor:** "İzmir boşanma avukatı"
- **Kategori:** Boşanma Hukuku
- **Tags:** `["boşanma hukuku", "İzmir boşanma avukatı", "aile hukuku"]`

**Mevcut Blog Yazıları:**
- `/blog/anlasmali-bosanma-nasil-acilir/` → anchor: "anlaşmalı boşanma rehberi"
- `/blog/velayet-davasi-sureci-ve-mahkeme-kriterleri/` → anchor: "velayet davası süreci"
- `/blog/nafaka-hesaplama-yoksulluk-istirak-nafakasi/` → anchor: "nafaka hesaplama"
- `/blog/cekismeli-bosanma-davasi-sureci-ve-kusur-tespiti/` → anchor: "çekişmeli boşanma davası"
- `/blog/bosanmada-mal-paylasimi-edinilmis-mallara-katilma-rejimi/` → anchor: "boşanmada mal paylaşımı"
- `/blog/bosanmada-tazminat-davasi-maddi-ve-manevi-tazminat/` → anchor: "boşanmada tazminat davası"
- `/blog/velayet-degisikligi-davasi-sartlari-ve-mahkeme-kriterleri/` → anchor: "velayet değişikliği davası"

**Sözlük Terimleri:**
- `/sozluk/anlasmali-bosanma/` → "anlaşmalı boşanma"
- `/sozluk/cekismeli-bosanma/` → "çekişmeli boşanma"
- `/sozluk/velayet/` → "velayet"
- `/sozluk/nafaka/` → "nafaka"
- `/sozluk/mal-paylasimi/` → "mal paylaşımı"
- `/sozluk/evlilik-birliginin-temelden-sarsilmasi/` → "evlilik birliğinin temelden sarsılması"

**Yazılabilecek Konular:**
1. Çekişmeli Boşanma Davası Süreci ve Kusur Tespiti
2. Boşanmada Mal Paylaşımı: Edinilmiş Mallara Katılma Rejimi
3. Boşanmada Tazminat Davası: Maddi ve Manevi Tazminat
4. Velayet Değişikliği Davası: Şartlar ve Mahkeme Kriterleri
5. Aile İçi Şiddet ve Koruma Kararı Süreci (6284 Sayılı Kanun)
6. Düğün Takılarının İadesi Davası: Yargıtay Kararları
7. Nafaka Artırım ve Nafaka Kaldırma Davası Şartları
8. Boşanma Davasında Sosyal Medya Delilleri ve Hukuki Geçerlilik
9. Yabancı Uyruklu Eşle Boşanma: Milletlerarası Özel Hukuk
10. Çocukla Kişisel İlişki Kurulması ve Teslim İcra Takibi

---

## Cross-Cluster Link Havuzu

Kira ve boşanma cluster'ları arasında cross-link verirken kullan. İş ve tazminat sayfaları da sitede mevcut, gerektiğinde cross-link verilebilir:

- `/izmir-kira-avukati/` → "kira avukatı"
- `/izmir-bosanma-avukati/` → "boşanma avukatı"
- `/izmir-is-avukati/` → "iş avukatı" (cross-link)
- `/izmir-tazminat-avukati/` → "tazminat avukatı" (cross-link)
- `/hizmetler/` → "hizmetlerimiz"
- `/hakkimda/` → "hakkımızda"
- `/iletisim/` → "iletişim"

---

## Analiz Modu

`/icerik-uret analiz` komutu verildiğinde veya argümansız çağrıldığında:

1. `src/content/blog/` dizinindeki tüm `.mdx` dosyalarını tara.
2. `src/lib/glossary.ts` dosyasındaki mevcut terimleri oku.
3. Yukarıdaki 20 topic'i kontrol et: hangisi yazılmış, hangisi yazılmamış?
4. Her cluster'daki blog yazısı sayısını göster.
5. Dengeli büyüme için hangi cluster'a öncelik verilmesi gerektiğini öner.
6. Sözlük'te eksik terimler var mı kontrol et.

Çıktı formatı:

```
## İçerik Durumu Analizi

### Blog Yazıları (Mevcut / Toplam Hedef)
| Cluster | Mevcut | Hedef | Eksik |
|---------|--------|-------|-------|
| Kira    | 9/19   | ...   | ...   |
| Boşanma | 6/16   | ...   | ...   |

### Öncelik Sıralaması
1. [En az içeriğe sahip cluster] — [önerilen konu]
2. ...

### Yazılmamış Konular
[Liste]
```

---

## Yeni Blog Yazısı Üretim Sonrası Kontrol Listesi

Üretilen her blog yazısı için şunları doğrula:

- [ ] Frontmatter'da `title`, `date`, `excerpt`, `tags`, `coverImage`, `faqs` (4+) var mı?
- [ ] İçerikte pillar sayfaya link var mı?
- [ ] En az 2 sibling (kardeş) makale linki var mı?
- [ ] En az 1 sözlük terimi linki var mı?
- [ ] Toplam 5+ iç link var mı?
- [ ] **ARAŞTIRMA:** Kanun maddeleri ve Yargıtay kararları WebSearch ile doğrulandı mı?
- [ ] Kanun maddesi referansı var mı?
- [ ] Gerçek Yargıtay kararı referansı var mı (daire, esas/karar no, yıl)?
- [ ] En az 2 pratik senaryo/örnek var mı?
- [ ] FAQ bölümü var mı (4+ soru)?
- [ ] "Profesyonel Hukuki Destek" CTA bölümü var mı?
- [ ] Disclaimer var mı?
- [ ] Dosya `src/content/blog/{slug}.mdx` olarak kaydedildi mi?
- [ ] Trailing slash'lar doğru mu? (URL sonlarında `/`)
- [ ] **SÖZLÜK:** Yazıda geçen kavramlar için yeni sözlük terimi gerekiyor mu?
- [ ] **SÖZLÜK:** Mevcut ilgili terimlerin `relatedBlogSlugs`'ına yeni yazı eklendi mi?
- [ ] **SÖZLÜK:** Yeni terim eklendiyse SKILL.md "Sözlük Terimleri" bölümü güncellendi mi?
- [ ] **PILLAR SAYFA:** Yeni yazı, ilgili pillar sayfanın "İlgili Makaleler" bölümüne eklendi mi?
- [ ] **PILLAR SAYFA:** Pillar sayfada "İlgili Makaleler" bölümü yoksa oluşturuldu mu?
- [ ] **SKILL.md:** "Mevcut Blog Yazıları" bölümüne yeni yazı eklendi mi?

---

## ÖNEMLİ NOTLAR

1. **ZORUNLU — Derin Araştırma:** İçerik üretmeden önce WebSearch ile kapsamlı araştırma yap. Her yazıda:
   - **Gerçek kanun maddeleri:** Spesifik madde numaralarını araştırarak doğrula (TBK, İK 4857, TMK, SGK 5510 vb.).
   - **Gerçek Yargıtay kararları:** Doğru daire, esas/karar numarası ve yıl bilgisiyle atıf yap. Uydurma karar numarası KULLANMA. WebSearch ile "Yargıtay [daire] [konu] kararı" şeklinde araştır ve doğrulanmış kararları kullan.
   - **Güncel mevzuat değişiklikleri:** Yazı konusuyla ilgili son yasal düzenlemeleri araştır.
   - Araştırma yapılmadan, doğrulanmamış bilgiyle içerik üretme. Her hukuki iddia bir kaynağa dayanmalı.
2. **Yeni bir blog yazısı yazıldığında:** Bu SKILL.md'deki "Mevcut Blog Yazıları" bölümüne yeni yazıyı elle ekle veya kullanıcıya hatırlat.
3. **Yeni bir sözlük terimi eklendiğinde:** "Sözlük Terimleri" bölümünü güncelle.
4. **İçerik üretirken mevcut dosyaları MUTLAKA oku** — tekrar eden içerik üretme.
5. **Her zaman Türkçe yaz.** İngilizce terim kullanma (zorunlu hukuki terimler hariç: mobbing, malpraktis vb.)
6. **Unsplash görselleri için:** `?q=80&w=1200&auto=format&fit=crop` parametrelerini kullan.
7. **ZORUNLU — Her blog yazısı üretildikten sonra sözlük güncellemesi yap:**
   - Yazıda link verilen mevcut sözlük terimlerinin `relatedBlogSlugs` alanına yeni blog slug'ını ekle.
   - Yazıda sıkça geçen ama sözlükte bulunmayan kavramlar varsa yeni terim oluştur.
   - Bu adım atlanMAZ; blog + sözlük birlikte üretilir.
8. **ZORUNLU — Her blog yazısı üretildikten sonra pillar sayfa güncellemesi yap:**
   - İlgili cluster'ın pillar sayfasındaki "İlgili Makaleler" bölümüne yeni yazının linkini ekle.
   - Pillar sayfada "İlgili Makaleler" bölümü yoksa SSS bölümünden önce oluştur.
   - Pillar sayfa dosyaları: `src/app/izmir-kira-avukati/page.tsx`, `src/app/izmir-bosanma-avukati/page.tsx`
   - Bu adım atlanMAZ; blog + sözlük + pillar sayfa tek bir iş olarak ele alınır.
