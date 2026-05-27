---
name: claude-plugins-marketplace
description: Claude Code'u tam bir dev ekibine dönüştüren 6 plugin yönetimi - Planning, Design, Code Review, Security, Memory, Team Coordination. Kullanıcı "claude plugin, dev team, claude takım, planlama ajanı" dediğinde tetiklenir.
triggers:
  - claude plugin
  - claude plugins
  - dev team
  - dev takım
  - claude takım
  - planlama ajanı
  - code review plugin
  - security plugin
  - memory plugin
  - team coordination
---

# Claude Code 6 Plugin Marketplace

Claude Code'u tek başına değil, 6 plugin ile tam bir yazılım geliştirme ekibine dönüştüren skill.

## 6 Plugin Rolü

| Plugin | Rol | Açıklama |
|--------|-----|----------|
| `planner` | Proje Yöneticisi | PRD → task breakdown → sprint planı |
| `designer` | UI/UX Tasarımcı | Figma/Stitch → komponent → CSS token |
| `reviewer` | Senior Developer | Kod kalite + diff review + best practices |
| `guardian` | Güvenlik Uzmanı | OWASP tarama + dependency audit + secret tespiti |
| `memorian` | Bilgi Yöneticisi | Obsidian vault + session memory + decision log |
| `captain` | Takım Kaptanı | Plugin'ler arası koordinasyon + çıktı birleştirme |

## Kurulum

```bash
# Plugin dizinini oluştur
mkdir -p "%USERPROFILE%\.claude\plugins"

# Her plugin için ayrı klasör
cd "%USERPROFILE%\.claude\plugins"
# NOT: Aşağıdaki repolar şablon/örnek niteliğindedir.
# Kendi plugin koleksiyonunuzu oluşturun veya
# Awesome Claude Code (https://github.com/hesreallyhim/awesome-claude-code) listesinden
# uyumlu plugin'ler bulun.
git clone https://github.com/<your-org>/claude-plugin-planner planner
git clone https://github.com/<your-org>/claude-plugin-designer designer
git clone https://github.com/<your-org>/claude-plugin-reviewer reviewer
git clone https://github.com/<your-org>/claude-plugin-guardian guardian
git clone https://github.com/<your-org>/claude-plugin-memorian memorian
git clone https://github.com/<your-org>/claude-plugin-captain captain
```

## Kullanım Akışı

### Tek Komutla Tüm Takımı Çalıştır

```bash
# Örnek: Yeni özellik geliştirme
/team-feature "Kullanıcı profil sayfası ekle"

# Arka planda sırayla:
# 1. planner → task'ları böler
# 2. designer → UI oluşturur
# 3. captain → reviewer ve guardian'a paralel gönderir
# 4. memorian → kararları vault'a yazar
```

### Tekil Plugin Çağrısı

```bash
/planner "Checkout akışını planla"
/reviewer "Son commit'i incele"
/guardian "Güvenlik taraması yap"
```

## KEŞİF Entegrasyonu

- **memorian** → `hybrid-memory` skill ile bağlanır (Vector + Graph + Relational)
- **designer** → `stitch`, `21st-dev`, `figma` MCP'lerini kullanır
- **guardian** → `etik-hacker`, `sonarqube` MCP'lerini tetikler
- **captain** → `kesif-orkestrator` skill'i ile eşgüdüm sağlar

## Neden Önemli?

Tek Claude prompt'u yerine 6 uzman rol aynı anda çalışır. Her rol kendi bağlamını taşır, kendi araç setini kullanır. Paralel yürütme ile 3-5x hızlanma sağlar.
