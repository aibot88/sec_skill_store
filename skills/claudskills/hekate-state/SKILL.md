---
name: hekate-state
description: Inspect and reset Hekate SQLite and Redis runtime state
---

# Hekate State

## Durable State

Use SQLite-backed services and scripts to inspect epics, tasks, and progress.

```bash
./scripts/hekate-analyze.py
```

## Transient State

Use Redis only for claims, heartbeats, and quota counters.

```bash
redis-cli keys "task:*:claim"
redis-cli keys "agent:*:heartbeat"
redis-cli keys "quota:*"
```
