---
name: zammad-cli
description: Zammad helpdesk için CLI wrapper skill. Kullanıcı "ticket ara", "ticket aç", "ticket kapat", "müşteri tickets", "destek talepleri", "support ticket oluştur", "zammad'da güncelle", "/zammad-cli" dediğinde tetiklenir. zammad-cli Rust binary'sini doğru komutlarla çağırır - ticket search/list/get/create/update/articles/article add/overview, org list/search, user search, system groups/states/priorities. Her zaman --json kullanıp parse eder.
when_to_use: Zammad ticket yönetimi, destek talebi yaratma/güncelleme, organizasyon/kullanıcı arama, ticket overview. Tetikleme cümleleri - "açık tickets", "yüksek priority destek", "X organizasyonun ticketları", "ticket #61234", "ticket'a not ekle", "support'a yanıt yaz".
allowed-tools: Bash(zammad-cli *) Read
---

# zammad-cli Workflow Skill

Zammad helpdesk ticketlarını terminal'den yönet. `zammad-cli` binary'sini wrap eder, `--json` çıktısını parse edip kullanıcıya özetler.

## Önkoşul: Binary + Env

```bash
zammad-cli --version || (echo "zammad-cli not installed" && exit 1)
test -n "$ZAMMAD_URL" && test -n "$ZAMMAD_TOKEN" || echo "env missing"
```

Eksikse README'deki kurulum + env satırlarını kullanıcıya göster.

## Ticket ID Semantiği

- `#61234` → ticket number (kullanıcının gördüğü 5+ hane numara) — API'da `number:` ile arar
- `42` → internal ID (DB primary key) — direkt kullanır

Kullanıcı "#" prefix kullanmadıysa düşük sayı = internal ID, yüksek sayı = muhtemelen ticket number — dikkat et, gerekirse `AskUserQuestion` ile sor.

## Komut Şablonu

**Her zaman `--json` ile çağır**, çıktıyı parse et, kullanıcıya özetle.

### Ticket

```bash
# Search
zammad-cli --json ticket search "performance"
zammad-cli --json ticket search "state.name:open AND priority.name:\"3 high\"" --limit 50

# List (filter)
zammad-cli --json ticket list --state open
zammad-cli --json ticket list --state new --priority "3 high"
zammad-cli --json ticket list --customer info@example.com
zammad-cli --json ticket list --group "Destek Ekibi"

# Get / articles
zammad-cli --json ticket get #61234         # by number
zammad-cli --json ticket get 42             # by internal ID
zammad-cli --json ticket articles #61234

# Create (DESTRUCTIVE — onay al)
zammad-cli --json ticket create \
  --title "..." --body "..." \
  --group "Destek Ekibi" \
  --customer info@example.com \
  --priority "3 high" --state new

# Update (DESTRUCTIVE — onay al)
zammad-cli --json ticket update #61234 --state closed
zammad-cli --json ticket update #61234 --priority "3 high" --owner agent@example.com

# Article add (DESTRUCTIVE — onay al, public yorum müşteriye gider)
zammad-cli --json ticket article add #61234 --body "..."           # internal default
zammad-cli --json ticket article add #61234 --body "..." --public  # müşteriye e-posta!

# Overview (5 state için paralel sayım)
zammad-cli --json ticket overview
```

### Org / User / System

```bash
zammad-cli --json org list
zammad-cli --json org search "diji"
zammad-cli --json user search "info@example.com"
zammad-cli --json user search "0532123"          # phone
zammad-cli --json user search "John Doe"
zammad-cli --json system groups
zammad-cli --json system states
zammad-cli --json system priorities
```

## Search Syntax (ticket list / ticket search)

Zammad search syntax — string olduğu gibi geçer:

| Örnek | Anlam |
|-------|-------|
| `state.name:open` | Açık ticketlar |
| `state.name:"pending reminder"` | Hatırlatma bekleyen |
| `priority.name:"3 high"` | Yüksek priority |
| `group.name:"Destek Ekibi"` | Belirli grup |
| `owner.email:agent@example.com` | Sahip filtresi |
| `customer.email:info@example.com` | Müşteri filtresi |
| `organization.name:"Acme Corp"` | Organizasyon |
| `state.name:open AND priority.name:"3 high"` | Combine |

`ticket list` flag'leri otomatik bu syntax'a çevirir + boşluklu değerleri quote eder. Karmaşık query için `ticket search "..."` ile raw string geç.

## Output Şeması

`--json ticket list/search` → `Ticket[]`:

```json
[{
  "id": 42,
  "number": "61234",
  "title": "...",
  "state": "open",
  "priority": "3 high",
  "group": "Destek Ekibi",
  "owner": "agent@example.com",
  "customer": "info@example.com",
  "organization": "Acme Corp",
  "created_at": "...",
  "updated_at": "..."
}]
```

`--json ticket articles` → `Article[]` (id, created_at, sender, from, subject, body, internal).

`--json ticket overview` → `{state: count, ...}`.

## Akış Örneği — "Açık high-priority tickets"

1. `zammad-cli --json ticket list --state open --priority "3 high" --per-page 50`
2. Tablo gibi sun (id, number, title, customer, group)
3. Detay isterse `ticket get #X`

## Akış Örneği — "Bu sorun için ticket aç"

1. Title + body çıkar (sorun özetinden)
2. `AskUserQuestion`:
   - header: "Ticket"
   - question: "Yeni Zammad ticket'ı oluşturayım mı?"
   - options: ["Evet, oluştur (DESTRUCTIVE)", "Hayır"]
3. Onay → `zammad-cli --json ticket create --title "..." --body "..." --priority "2 normal"`
4. Dönen `number` + `id`'yi kullanıcıya bildir

## Akış Örneği — "Ticket'a yanıt yaz" (PUBLIC)

PUBLIC yanıt **müşteriye e-posta gider** — destructive!

1. Body hazırla
2. `AskUserQuestion`:
   - header: "Public Reply"
   - question: "Bu yanıt müşteriye e-posta olarak gidecek. Onaylıyor musun?"
   - options: ["Evet, public gönder", "Internal note olarak ekle", "İptal"]
3. Onaya göre:
   - Public: `zammad-cli --json ticket article add #X --body "..." --public`
   - Internal: `zammad-cli --json ticket article add #X --body "..."`

## Akış Örneği — "Ticket #61234 kapat"

1. Önce mevcut state'i kontrol et: `zammad-cli --json ticket get #61234`
2. Onay: `AskUserQuestion` "Ticket #61234 kapansın mı?"
3. `zammad-cli --json ticket update #61234 --state closed`

## Hata Durumları

- `Not found (404)` → Ticket/org/user yok
- `Unauthorized (401)` → ZAMMAD_TOKEN geçersiz, profile'dan yenisini al
- `Permission denied (403)` → Token'ın `ticket.agent` veya `admin` izni yok
- `Bad request (400)` → Parametre formatı (özellikle state/priority adları)
- `Unprocessable (422)` → Geçersiz alan değeri (örn. owner email yok)
- Boş `Error: ZAMMAD_URL...` → env eksik

## İpuçları

- **State doğru yaz**: `new`, `open`, `closed`, `pending reminder`, `pending close` (boşluklu olanlar quote'lu)
- **Priority doğru yaz**: `1 low`, `2 normal`, `3 high` (sayı + boşluk + isim)
- **Group default**: `ticket create` default `"Destek Ekibi"` (Diji-spesifik, başka instance'larda override gerekli)
- **Article internal default true**: `--public` flag olmadan dahili not olarak eklenir, müşteri görmez
- **Overview 100 cap**: `ticket overview` her state için `per_page=100` ile sayar — 100+ ticket varsa undercount, raporlarken belirt

## İlgili Kaynaklar

- Repo README: `${CLAUDE_SKILL_DIR}/../../README.md`
- Zammad API docs: https://docs.zammad.org/en/latest/api/
- Search syntax: https://docs.zammad.org/en/latest/admin/settings/search.html
