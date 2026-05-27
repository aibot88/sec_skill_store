---
name: vikunja-cli
description: Vikunja görev yönetimi için CLI wrapper skill. Kullanıcı "vikunja task ekle", "görevleri listele", "task'i tamamlandı işaretle", "vikunja proje oluştur", "açık görevleri göster", "vikunja-cli ile görev al", "/vikunja-cli" dediğinde tetiklenir. vikunja-cli Rust binary'sini doğru komutlarla çağırır - task list/get/create/update/delete, project list/get/create, label list, comment list/create, assign/unassign, label set. Her zaman --json kullanıp parse eder.
when_to_use: Vikunja task/proje yönetimi, görev listeleme/filtreleme, hızlı görev oluşturma, status güncelleme, atama. Tetikleme cümleleri - "açık taskları getir", "X projesindeki görevler", "yüksek priority görevler", "görev kapat", "yorum ekle task'a", "vikunja create task".
allowed-tools: Bash(vikunja-cli *) Read
---

# vikunja-cli Workflow Skill

Vikunja görevlerini terminal'den yönet. `vikunja-cli` binary'sini wrap eder, çıktıyı JSON olarak alıp anlamlandırır.

## Önkoşul: Binary + Env

```bash
vikunja-cli --version || (echo "vikunja-cli not installed" && exit 1)
test -n "$VIKUNJA_API_URL" && test -n "$VIKUNJA_API_TOKEN" || echo "env missing"
```

Eksikse README'deki kurulum + env satırlarını kullanıcıya göster.

## Komut Şablonu

**Her zaman `--json` ile çağır**, çıktıyı parse et, kullanıcıya özetle.

### Task

```bash
# Liste / filtre
vikunja-cli --json task list
vikunja-cli --json task list --filter "done = false"
vikunja-cli --json task list --filter "priority >= 3 && done = false"
vikunja-cli --json task list --filter "project_id = 6"           # alt-projeler dahil
vikunja-cli --json task list --search "deploy"

# Tek/çoklu detay
vikunja-cli --json task get <id>
vikunja-cli --json task get-detail <id1>,<id2>,<id3>             # max 25

# CRUD
vikunja-cli --json task create <project_id> "Title" \
  --description "..." --priority 4 --due-date 2026-05-15T18:00:00Z
vikunja-cli --json task update <id> --done true
vikunja-cli --json task update <id> --priority 5 --title "..."
vikunja-cli --json task delete <id>

# Yorum
vikunja-cli --json task comment list <task_id>
vikunja-cli --json task comment create <task_id> --comment "..."

# Atama
vikunja-cli --json task assign <task_id> <user_id>
vikunja-cli --json task unassign <task_id> <user_id>

# Label
vikunja-cli --json task labels <task_id> --ids 1,3,5              # set/replace
vikunja-cli --json task labels <task_id> --ids ""                  # clear
```

### Project

```bash
vikunja-cli --json project list
vikunja-cli --json project list --search "infra"
vikunja-cli --json project get <id>
vikunja-cli --json project create "Q2 Roadmap" --hex-color 3b82f6 --parent 1
vikunja-cli --json project update <id> --title "..." --favorite true
```

### Label

```bash
vikunja-cli --json label list
vikunja-cli --json label list --search "bug"
```

## Filter Syntax (task list)

Vikunja native filter syntax — string olduğu gibi geçer:

| Örnek | Anlam |
|-------|-------|
| `done = false` | Sadece açık görevler |
| `priority >= 3 && done = false` | Yüksek priority açık |
| `due_date < now && done = false` | Gecikmiş |
| `project_id = 6 && done = false` | Proje 6 + alt-projeleri |
| `done = false && due_date < now+7d` | 1 hafta içinde due |

`project_id = X` yazınca CLI alt-projeleri otomatik OR-expand eder.

## Output Şeması

`--json task list` → `Task[]`:

```json
[{
  "id": 42,
  "title": "...",
  "description": "...",
  "done": false,
  "priority": 4,
  "project_id": 6,
  "due_date": "2026-05-15T18:00:00Z",
  "labels": [{"id": 1, "title": "bug"}],
  "assignees": [{"id": 7, "username": "ofy"}]
}]
```

`--json project list` → tree (`{id, title, children: []}`).

`--json task delete` → `{"deleted": <id>}`.

## Akış Örneği — "Yüksek priority açık taskları göster"

1. `vikunja-cli --json task list --filter "priority >= 3 && done = false" --per-page 50`
2. JSON parse et, count + ilk 10'u kullanıcıya tablo gibi sun
3. Daha fazla detay isterse `task get <id>` veya `task get-detail <ids>` çağır

## Akış Örneği — "Bu sorun için Vikunja'da görev aç"

1. `CLAUDE.local.md` Vikunja proje ID'yi al (örn. 18)
2. Title + description çıkar
3. Onay al (`AskUserQuestion`):
   - header: "Vikunja"
   - question: "Yeni görev oluşturayım mı?"
   - options: ["Evet, oluştur", "Hayır"]
4. `vikunja-cli --json task create 18 "Title" --description "..." --priority 3`
5. Dönen ID'yi kullanıcıya bildir

## Akış Örneği — "Görev #42'yi kapat"

1. `vikunja-cli --json task update 42 --done true`
2. Başarılı → onay mesajı
3. Hata → mesajı doğrudan göster, kullanıcıya neden olduğunu açıkla

## Hata Durumları

CLI hata mesajları:

- `Not found (404)` → ID yanlış, var olduğunu doğrula
- `Permission denied (403)` → Token yetkisi yok
- `Unauthorized (401)` → Token geçersiz, yeniden token al
- `Bad request (400)` → Parametre formatı yanlış (özellikle date)
- Boş `Error: VIKUNJA_API_URL...` → env eksik

## İpuçları

- **Compact output**: `task list` çıktısı `description` içermez (50/sayfa default), detay için `task get` kullan
- **Date format**: ISO 8601 UTC (`2026-05-15T18:00:00Z`) — Vikunja epoch ya da naive datetime kabul etmez
- **Priority skala**: 1=low, 2=medium, 3=high, 4=urgent, 5=do-now
- **Label set**: `--ids 1,3,5` mevcut tüm label'ları siler ve yenisini ekler. Mevcut + yeni için önce `task get`'ten oku, sonra birleştir
- **Pagination**: default 50 task/sayfa. Çok varsa `--page 2 --per-page 100`

## İlgili Kaynaklar

- Repo README: `${CLAUDE_SKILL_DIR}/../../README.md`
- Vikunja resmi filter docs: https://vikunja.io/docs/filters/
- Vikunja API docs: https://vikunja.io/api-doc
