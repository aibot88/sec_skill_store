---
name: agentic-skill-authoring-standard
description: Yeni agentic-* veya proje skill eklerken frontmatter, bölüm sırası ve katalog uyumunu denetlerken kullan.
---

## Amaç

Tüm Faz 2 skill’leri `SKILL_CATALOG_PHASE2.md` şartnamesine uyar: YAML **frontmatter** (`name`, `description`), gövde **Türkçe başlıkları** sabit sıra ile. Yeni skill ekleme: önce katalog satırı, sonra dosya **`cli/skills/<id>/SKILL.md`**. **Review checklist**: çapraz linkler göreli yol, Faz 1 çelişkisi yok, güvenlik maddeleri dolu.

## Kapsam

### Dahil

- Faz 1 örnek (`../../skills/juju-model-cos/SKILL.md`) ile **ton farkı**: Faz 2’de zorunlu bölümler daha yapılandırılmış; içerik birleştirilebilir.

### Hariç

- Otomatik skill linter aracı (yoksa manuel review).

## Kurallar

- `name:` frontmatter klasör adı ile birebir aynı.
- İngilizce komut/charm adları korunur; açıklama Türkçe.
- “Sıfır varsayım”: belgede yoksa uydurma, “proje kararı” yaz.

## Kontrol listesi

- [ ] Katalogda skill satırı var mı?
- [ ] Altı zorunlu bölüm eksiksiz mi?
- [ ] `## İlgili belgeler ve skill'ler` göreli yol kurallarına uygun mu?
- [ ] Güvenlik (shell/MCP) maddeleri atlandı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Kırık göreli link | Path from cli/skills | Düzelt |
| COS çelişkisi | Faz 1 skill | Faz 1 kazanır |

## İlgili belgeler ve skill'ler

- `../documantations/SKILL_CATALOG_PHASE2.md`
- `../../skills/juju-model-cos/SKILL.md`
- `../agentic-project-charter/SKILL.md`
