---
name: ai-kesfet
description: GitHub, Anthropic blog ve topluluk kaynaklarını tarayarak yeni Claude skill/MCP/tool keşfeder. REPO_CATALOG.md'ye ekler, /ai-upgrade'e hazır hale getirir.
---

# AI Keşif — Yeni Araç Tarama Sistemi

Her çalıştırmada güncel kaynakları tara, zaten katalogda olmayanları değerlendir, ekle.

---

## AŞAMA 1: Mevcut Katalog Snapshot

`_agents/ai-research/REPO_CATALOG.md`'yi oku.
Mevcut repo URL'lerini listeye al — duplikasyon kontrolü için.

---

## AŞAMA 2: Kaynak Tarama

Aşağıdaki kaynakları **paralel WebFetch/WebSearch** ile tara:

### 2.1 — Resmi Kaynaklar
```
WebFetch: https://raw.githubusercontent.com/anthropics/skills/main/README.md
WebFetch: https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md
WebSearch: "claude code new skills site:github.com 2026"
WebSearch: "claude mcp server new 2026 site:github.com"
```

### 2.2 — Küratörlü Listeler
```
WebFetch: https://raw.githubusercontent.com/travisvn/awesome-claude-skills/main/README.md
WebSearch: "awesome claude code skills 2026"
WebSearch: "awesome mcp servers claude 2026"
```

### 2.3 — Anthropic Duyuruları
```
WebSearch: "anthropic claude code update 2026 new feature"
WebSearch: site:anthropic.com/news 2026 claude
```

### 2.4 — Topluluk (HN / Reddit)
```
WebSearch: "claude code tips tricks hacker news 2026"
WebSearch: "site:reddit.com/r/ClaudeAI claude code skill 2026"
```

---

## AŞAMA 3: Filtreleme

Her bulgu için şu soruları sor:

1. **Zaten katalogda var mı?** → URL veya isim eşleşmesi kontrolü → varsa atla
2. **Claude Code ile kullanılabilir mi?** → SKILL.md formatı veya MCP protokolü → hayırsa atla
3. **MMEpanel için değer katıyor mu?** → Aşağıdaki kriterlere bak:
   - Backend geliştirme (FastAPI, Python, PostgreSQL)
   - Frontend geliştirme (Next.js, React, Tailwind)
   - AI agent altyapısı (memory, reasoning, orchestration)
   - DevOps / deploy otomasyonu
   - Veri analizi / görselleştirme

**Uyum değerlendirmesi:**
- ⭐⭐⭐ Direkt MMEpanel iş akışlarını geliştirir
- ⭐⭐ Genel faydalı, adaptasyon gerekebilir
- ⭐ Düşük öncelik, gelecekte incelenebilir

---

## AŞAMA 4: REPO_CATALOG.md'ye Ekle

Her yeni bulgu için standart format:

```markdown
### [N]. [repo-adı]
- **URL:** https://github.com/...
- **Kategori:** SKILLS / MCP / TOOL / TEMPLATE
- **Öncelik:** 🔴 / 🟡 / 🟢
- **Durum:** `yeni`
- **Yıldız:** ~X (varsa)
- **İçerik:** [Kısa açıklama — ne içeriyor]
- **MMEpanel Uyumu:** [Hangi iş akışını geliştirir]
- **Keşif tarihi:** [YYYY-MM-DD]
```

`REPO_CATALOG.md` başlığını güncelle:
```
**Son güncelleme:** [bugün]
**Toplam repo:** [N]
**Yeni eklenen:** [bu oturumda kaç tane]
```

---

## AŞAMA 5: Özet Rapor

Kullanıcıya şu formatı sun:

```
## /ai-kesfet Sonuçları — [YYYY-MM-DD]

### Taranan Kaynaklar: X
### Yeni Bulgu: Y (Z tanesi zaten katalogda vardı)

### 🔴 Yüksek Öncelikli Yeni Araçlar
1. **[repo-adı]** — [tek cümle açıklama]
   → `/ai-upgrade` ile kurulabilir

### 🟡 Orta Öncelikli
...

### 🟢 Kaydedildi, Düşük Öncelik
...

### REPO_CATALOG.md güncellendi: [önceki] → [yeni] repo
```

---

## Kurallar

```
TARAMA SIRASINDA: Paralel WebFetch/WebSearch kullan — sıralı değil.
DUPLIKASYON: URL eşleşmesi varsa kesinlikle atla.
KALITE: "yıldız sayısı yüksek ama MMEpanel'e uygun değil" → kataloğa ekleme.
SONUÇ: En az 1, en fazla 10 yeni repo per oturum. Fazlası gürültü.
ZAMAN: Katalog tarihini her zaman güncelle — stale katalog işe yaramaz.
```

---

## Hızlı Referans — Öncelikli Arama Terimleri

```
"claude code skill" site:github.com
"mcp server" fastapi site:github.com
"claude hooks" site:github.com
"anthropic claude code" new 2026
awesome-claude site:github.com
```
