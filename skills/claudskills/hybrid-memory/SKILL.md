---
name: hybrid-memory
description: LLM Wiki pattern + Cognee tarzı hibrit hafıza — Vector (ChromaDB) + Graph (Neo4j/NetworkX) + Relational (SQLite) üçlüsü. Oturumlar arası kalıcı bellek için kullan; kullanıcı "hatırla", "not al", "önceki sohbet", "ne konuşmuştuk" dediğinde. Retrieve-based RAG'den farklı — periyodik **compile** ederek Obsidian uyumlu wiki üretir.
---

# Hybrid Memory Skill

## Mimari
```
Kaynak (sohbet, kod, mail) ──→ Ingestor
                                   │
            ┌──────────────────────┼──────────────────────┐
            ↓                      ↓                      ↓
      Vector (Chroma)        Graph (NetworkX)     Relational (SQLite)
      semantik              entity↔entity            zaman/metadata
            └──────────────────────┬──────────────────────┘
                                   ↓
                          Wiki Compiler (günlük)
                                   ↓
                       <workspace>/.memory/compiled/*.md
                                   ↓
                      Claude Code oturum başında yükler
```

## İlk kurulum

```bash
mkdir -p <workspace>/.memory/{vectors,graph,compiled}
pip install chromadb networkx
```

## Kullanım

```python
from hybrid_memory import remember, recall, compile_wiki

remember("kullanıcı Mustafa AI engineer olmak istiyor", tags=["user", "goal"])
hits = recall("kullanıcı hedefi nedir")
compile_wiki()  # periyodik — cron ile günlük
```

## Obsidian Entegrasyonu

`<workspace>/.memory/compiled/` bir Obsidian vault. Her `compile_wiki()` çağrısı:
- Entity'leri `[[wiki-link]]` ile bağlar
- Tarih bazlı günlük notlar üretir
- Tag index'i günceller

## Mevcut sistem ile köprü

Claude Code'un otomatik belleği (`C:/Users/kesif/.claude/.../memory/MEMORY.md`) bu hibrit sisteme **feed eder**: her memory yazımında Ingestor'a da bildirilir.
