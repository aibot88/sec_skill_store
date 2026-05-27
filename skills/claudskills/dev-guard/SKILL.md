---
name: dev-guard
description: "Watchdog automatico per file critici: avvisa prima di modificare .env, migrations, CI, secrets. Usa questa skill quando l'utente vuole protezione automatica, o dice guard, watchdog, proteggi file, guardia, sentinel, file critici."
---

# /dev-guard — Watchdog File Critici

Watchdog automatico che monitora le modifiche a file universalmente critici. A differenza di `/dev-freeze` (che blocca directory scelte dall'utente), `/dev-guard` protegge una lista predefinita di file sensibili con avviso e conferma.

## Attivazione

```
/dev-guard                    # Attiva con lista default
/dev-guard --show             # Mostra file monitorati
/dev-guard --add "*.secret"   # Aggiungi pattern custom
/dev-guard --off              # Disattiva
```

Quando attivato:
```
GUARD attivo — Watchdog file critici

Monitoro modifiche a file sensibili in 6 categorie:
  [SECRETS]    .env, *.key, *.pem, credentials.*
  [DATABASE]   migrations/, schema.prisma, *.sql (DDL)
  [CI/CD]      .github/workflows/, Dockerfile, docker-compose*
  [DEPS]       package.json (solo dependencies), requirements.txt, Gemfile
  [CONFIG]     tsconfig.json, vite.config.*, next.config.*, webpack.*
  [SECURITY]   auth/, middleware/auth*, *.crt, *.p12, cors config

Ogni modifica a questi file richiede conferma con spiegazione del rischio.
```

## Lista file monitorati

### SECRETS — Rischio CRITICO
| Pattern | Motivo |
|---------|--------|
| `.env`, `.env.*` | Variabili ambiente, API keys, connection string |
| `*.key`, `*.pem`, `*.p12`, `*.crt` | Certificati e chiavi private |
| `credentials.*`, `secrets.*` | File credenziali espliciti |
| `**/service-account*.json` | Google Cloud service account |
| `.npmrc`, `.pypirc` | Token registry pacchetti |

### DATABASE — Rischio ALTO
| Pattern | Motivo |
|---------|--------|
| `migrations/**` | Schema change irreversibili in produzione |
| `prisma/schema.prisma` | Modello dati — change cascade su tutto il codice |
| `**/schema.sql`, `**/seed.sql` | DDL e dati iniziali |
| `alembic/versions/**` | Migration Python |
| `knex/migrations/**` | Migration Knex.js |

### CI/CD — Rischio ALTO
| Pattern | Motivo |
|---------|--------|
| `.github/workflows/*.yml` | Pipeline CI — errore = deploy rotto |
| `Dockerfile`, `docker-compose*` | Container build — errore = ambiente rotto |
| `.gitlab-ci.yml`, `Jenkinsfile` | Pipeline altri CI |
| `vercel.json`, `netlify.toml` | Config deployment |
| `fly.toml`, `render.yaml` | Config hosting |

### DEPS — Rischio MEDIO
| Pattern | Motivo |
|---------|--------|
| `package.json` (campo `dependencies`) | Dipendenze runtime — supply chain risk |
| `package-lock.json` | Lockfile — modifica manuale rischiosa |
| `requirements.txt`, `pyproject.toml` | Dipendenze Python |
| `Gemfile`, `Gemfile.lock` | Dipendenze Ruby |

### CONFIG — Rischio MEDIO
| Pattern | Motivo |
|---------|--------|
| `tsconfig.json`, `tsconfig.*.json` | Config TypeScript — errore = build rotto |
| `vite.config.*`, `next.config.*` | Config bundler/framework |
| `webpack.config.*`, `rollup.config.*` | Config build |
| `jest.config.*`, `vitest.config.*` | Config test — errore = test falsi positivi |
| `.eslintrc*`, `.prettierrc*` | Config linting |

### SECURITY — Rischio ALTO
| Pattern | Motivo |
|---------|--------|
| `**/auth/**`, `**/middleware/auth*` | Logica autenticazione |
| `**/cors*` | Configurazione CORS |
| `**/helmet*`, `**/csp*` | Security headers |
| `**/rbac*`, `**/permissions*` | Controllo accessi |

## Formato avviso

Quando un'operazione tocca un file monitorato:

```
GUARD: File critico in fase di modifica

  File:      .github/workflows/deploy.yml
  Categoria: CI/CD
  Rischio:   ALTO
  Motivo:    Modifica alla pipeline di deploy. Un errore puo bloccare i rilasci.

  Modifiche rilevate:
  - Riga 15: aggiunta step "npm run build"
  - Riga 22: rimossa condizione "if: github.ref == 'refs/heads/main'"

Procedere con la modifica? (si/no)
```

## Differenze con /dev-careful e /dev-freeze

| Aspetto | /dev-careful | /dev-freeze | /dev-guard |
|---------|-------------|-------------|------------|
| **Scope** | Tutte le operazioni distruttive | Directory scelte dall'utente | File critici predefiniti |
| **Azione** | Conferma | Blocco assoluto | Conferma con contesto |
| **Personalizzabile** | No | Si (path utente) | Si (--add pattern) |
| **Default attivo** | No | No | No (attivare con /dev-guard) |

Tutti e 3 si sommano quando attivi contemporaneamente.

## Pattern custom

L'utente puo aggiungere pattern personalizzati:

```
/dev-guard --add "src/billing/**"     # Aggiungi directory billing
/dev-guard --add "*.config.mjs"       # Aggiungi pattern glob
/dev-guard --remove "*.prettierrc*"   # Rimuovi pattern (troppo rumore)
```

## Regole

1. **Avviso, non blocco** — a differenza di `/dev-freeze`, `/dev-guard` chiede conferma ma non impedisce
2. **Contesto nel messaggio** — spiega sempre PERCHE il file e critico, non solo "attenzione"
3. **Mostra diff** — quando possibile, mostra cosa sta per cambiare nel file
4. **Log** — registra ogni avviso in `specs/_changelog.md` con esito (approvato/rifiutato)
5. **Non persiste** — si resetta a fine sessione
6. **Bassa frizione** — un solo "si" basta per procedere (non doppia conferma)
