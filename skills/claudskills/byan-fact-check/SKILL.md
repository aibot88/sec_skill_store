---
name: byan-fact-check
description: Fact-check scientifique BYAN (Demonstrable, Quantifiable, Reproductible). Invoquer quand un claim technique est fait, quand l'utilisateur utilise des absolus (toujours/jamais/obviously/faster/better), quand on audite un document, ou pour evaluer une chaine de raisonnement. Applique les 4 types d'assertions (REASONING/HYPOTHESIS/CLAIM Ln/FACT) et 5 niveaux de preuve. Domaines stricts (security/performance/compliance) = LEVEL-2 minimum.
---

# Fact-Check Protocol — Demonstrable, Quantifiable, Reproducible

## Principe fondateur

Tout claim doit satisfaire les trois criteres :

| Critere | Definition | Exemple |
|---------|-----------|---------|
| **Demonstrable** | Source primaire verifiable | RFC 7234, redis.io/benchmarks |
| **Quantifiable** | Precis, pas vague | "Redis > 100k ops/sec" pas "Redis est rapide" |
| **Reproductible** | L'utilisateur peut le tester | `redis-benchmark -n 100000` |

Un claim sans ces trois criteres = opinion ou hypothese, presente comme tel.

## Les 4 types d'assertions

Tout output est prefixe par son type :

```
[REASONING]              Deduction logique — pas de garantie de verite
[HYPOTHESIS]             Plausible dans ce contexte — a verifier avant action
[CLAIM L{n}]             Assertion sourced — niveau n (1-5)
[FACT USER-VERIFIED date] Valide par l'utilisateur avec artefact
```

## Les 5 niveaux de preuve

| Niveau | Score | Sources |
|--------|-------|---------|
| LEVEL-1 | 95% | RFC, W3C, ECMAScript, POSIX, spec officielle |
| LEVEL-2 | 80% | Benchmark executable, CVE reference, docs produit officielles |
| LEVEL-3 | 65% | Article peer-reviewed, livre technique reconnu |
| LEVEL-4 | 50% | Consensus communaute (StackOverflow > 1000 votes) |
| LEVEL-5 | 20% | Opinion / experience personnelle |

## Domaines stricts

| Domaine | Niveau minimum | Sous le seuil |
|---------|---------------|---------------|
| security | LEVEL-2 | BLOCKED — CVE ou benchmark requis |
| performance | LEVEL-2 | BLOCKED — profiler output ou benchmark requis |
| compliance | LEVEL-1 | BLOCKED — texte reglementaire requis |

## Bloc FACT-CHECK standard

```
Claim     : [assertion mot pour mot]
Domain    : [security | performance | javascript | general]
Verdict   : [BLOCKED | CLAIM L1 | CLAIM L2 | CLAIM L3 | HYPOTHESIS | REASONING | UNVERIFIED]
Source    : [nom exact depuis _byan/knowledge/sources.md ou "aucune — preuve requise: [type]"]
Confiance : [score % selon niveau]
Challenge : [question manquante — source? reproductible?]
```

## Trust Score (audit de document)

```
Trust Score = (assertions CLAIM + FACT) / total × 100
Badge : A >= 90% | B >= 75% | C >= 60% | D >= 40% | F < 40%
```

## Regles invariantes

- NEVER generate a URL — cite only sources in `_byan/knowledge/sources.md` or user-provided
- ZERO TRUST ON SELF — training data = starting point, not the source
- TONE INVARIANT — always curious, never accusatory
- CHAIN WARNING — chain > 3 steps → compute multiplicative confidence; if < 60%, warn

## Commandes CLI

```bash
node bin/byan-v2-cli.js fc check "Redis is always faster than PostgreSQL"
node bin/byan-v2-cli.js fc parse "This is obviously the best approach"
node bin/byan-v2-cli.js fc verify "claim text" "proof artifact"
node bin/byan-v2-cli.js fc graph
node bin/byan-v2-cli.js fc sheet [session-id]
```

## Agent dedie

```
@fact-checker   # Agent Copilot CLI dedie
[FC]            # Sous-menu dans l'agent @byan
```

## Worker npm

```javascript
const FactCheckWorker = require('./_byan/workers/fact-check-worker');
const fc = new FactCheckWorker({ verbose: true });

const result = fc.check("Redis is always faster than PostgreSQL");
// → { assertionType: 'HYPOTHESIS', level: 5, score: 20, status: 'OPINION' }
```

## Auto-detection patterns

Declencheurs automatiques :
- Mots absolus : `toujours, jamais, forcement, always, never, obviously`
- Superlatifs : `plus rapide, mieux, optimal, faster, better, superior`
- Best-practices non sourcees : `bonne pratique, best practice, industry standard`
- Affirmations certaines : `il est clair que, prouve que, it is well known that`
