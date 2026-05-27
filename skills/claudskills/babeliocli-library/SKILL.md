---
name: babeliocli-library
description: "Read the authenticated user's Babelio shelves (lus, à lire, en cours, pense-bête, abandonnés, critiqués, non critiqués) using babeliocli. Use this skill whenever a user wants to list their books, count books they've read, group reads by month or year, extract their reading history, compute statistics about their library, find a book they own, or export their Babelio shelves as JSON."
---

# babeliocli — Read Shelves and Books

`babeliocli` exposes the logged-in user's library. It is read-only and never modifies Babelio state.

## Preconditions

A session must exist. If needed, see the `babeliocli-setup` skill or run:

```bash
babeliocli whoami   # confirms the session
```

## Shelves

```bash
babeliocli shelves          # JSON (default)
babeliocli shelves -f text  # human view
```

Supported shelf keys:

| Key | Label | Babelio filter |
|---|---|---|
| `all` | Mes livres | `?action=toute` |
| `lus` | Lus | `?s1=1` |
| `a-lire` | À lire | `?s1=2` |
| `en-cours` | En cours | `?s1=0` |
| `pense-bete` | Pense-bête | `?s1=3` |
| `abandonnes` | Abandonnés | `?s1=4` |
| `critiques` | Critiqués | `?s3=10` |
| `non-critiques` | Non critiqués | `?s3=11` |

## Books

```bash
babeliocli books --shelf lus              # all "read" books, JSON
babeliocli books --shelf lus --limit 10   # first 10 books
babeliocli books --shelf a-lire -f text   # human view
```

Flags:

- `--shelf` (required, default `all`): one of the keys above.
- `--limit N` (default `0` = no limit): stop after N books.
- `--max-pages N` (default `50`): safety cap on HTTP pagination.

Pagination is handled automatically. The CLI requests the first page with the filter, then follows `pageN=N` because Babelio stores the active filter in the PHP session.

## Book JSON schema (per shelf entry)

```json
{
  "id_biblio": "90486207",
  "book_id": "1917163",
  "title": "Une espèce en voie de disparition",
  "author": "Lavie Tidhar",
  "author_id": "271314",
  "book_url": "https://www.babelio.com/livres/Tidhar-Une-espece-en-voie-de-disparition/1917163",
  "status": "Lu",
  "rating": 4,
  "readers": 259,
  "tags": [],
  "read_start": "2025-09-01",
  "read_end": "2025-09-05"
}
```

Notes:

- `id_biblio` is the per-user shelf entry (useful for debugging Babelio URLs); `book_id` is the globally-shared identifier used in `/livres/.../BOOK_ID`.
- `rating` is an integer 0–5 (0 = not rated).
- `read_start` / `read_end` are the user-entered dates (`YYYY-MM-DD`). Empty when the user has never filled them.
- `status` matches Babelio's French labels: `Lu`, `À lire`, `En cours`, `Pense bête`, `Abandonné`, `Possédé`.

## Common agent recipes

### Group read books by month

```bash
babeliocli books --shelf lus |
  jq -r '.books[] | select(.read_end != "") | "\(.read_end[0:7])\t\(.title)"' |
  sort
```

### Count read books per year

```bash
babeliocli books --shelf lus |
  jq -r '.books[] | select(.read_end != "") | .read_end[0:4]' |
  sort | uniq -c | sort -rn
```

### Top-rated books in your library

```bash
babeliocli books --shelf all |
  jq '.books | map(select(.rating == 5)) | map({title, author})'
```

### Find a book you own by partial title

```bash
babeliocli books --shelf all |
  jq --arg q "hyperion" '.books[] | select(.title | ascii_downcase | contains($q))'
```

## Gotchas

- If a book has no `read_end`, do not assume "not read yet"; it may mean the user never filled the date.
- Babelio's status `"Lu"` is authoritative; dates are metadata.
- Shelves `critiques` and `non-critiques` intersect `lus`, so summing counts would double-count.
- A session expiry returns `session expired: …` on stderr with a non-zero exit code — your script should detect this and trigger a re-auth path.
