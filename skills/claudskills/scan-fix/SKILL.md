---
name: scan-fix
description: Diagnose en fix scanner problemen. Gebruik bij "scanner", "scan", "OAuth", "tokens".
argument-hint: "[probleem beschrijving]"
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

Diagnose en fix scanner problemen. Probleem: $ARGUMENTS

## Scanner bestanden
- `scanner-content.tsx`: hoofdcomponent (~5000 regels)
- `ScannerCard.tsx`: card component (React.memo)
- `ScannerEditPanel.tsx`: edit panel (React.memo)
- `useVirtualGrid.ts`: virtual scrolling
- `scanner-session.ts`: split storage v2
- `scan-proxy/route.ts`: AI scan API + OAuth
- `scanner-types.ts`: types + constants
- `scanner-image-utils.ts`: canvas/image helpers

## Veelvoorkomende scanner bugs
- OOM op mobiel: image semaphore (28 slots), freeCanvas() na elke operatie
- Ghost slots: activeCountRef uit sync → Math.max(0, ...) safety
- Retry storm: retryAfter timestamp met exponential backoff
- Session corrupt: ?clean URL param → wist alles
- OAuth 401: wis in-memory → verse blob → probeer → dan refresh

## Token check
```bash
curl -s "https://gameshopenter.com/api/admin/sync-tokens?key=gameshop-admin-2024"
```

Lees het relevante bestand, fix het probleem, build, commit, push.
