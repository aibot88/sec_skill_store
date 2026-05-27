---
name: hora-deps
description: Dependency audit and smart update — scan outdated packages, check vulnerabilities, update with automatic testing. Use when user says deps, dependencies, outdated, update packages, npm audit, vulnerabilities, security audit deps, upgrade, bump versions. Do NOT use for security code audit — use hora-security. Do NOT use for installing new packages — just npm install.
metadata:
  author: HORA
  version: 1.0.0
compatibility: Claude Code. npm/pnpm/yarn/bun. Node.js 18+. Cross-platform.
---

# Skill: hora-deps

> "Un package outdated non surveille est une CVE qui attend d'etre publiee."

Scan des packages obsoletes, audit de securite, mise a jour intelligente par batch avec tests automatiques. Update safe (patch/minor) d'abord, major avec evaluation du risque.

## Invocation

```
/hora-deps <commande> [options]
```

| Commande | Description |
|----------|-------------|
| `scan` | Liste tous les packages obsoletes avec current/wanted/latest |
| `audit` | Audit de securite — vulnerabilites classees par severite |
| `update-safe` | Met a jour uniquement les patch et minor (sans breaking changes) |
| `update-all` | Met a jour tout y compris les major (avec evaluation risque) |
| `check <package>` | Analyse un package specifique : changelog, breaking changes, popularite |

| Flag | Description |
|------|-------------|
| `--dev` | Inclure les devDependencies uniquement |
| `--prod` | Inclure les dependencies uniquement |
| `--dry-run` | Affiche ce qui serait fait sans modifier package.json |
| `--skip-tests` | Ne pas lancer les tests apres update (deconseille) |

---

## Protocol

### Phase 1 — SCAN

1. Executer `scripts/scan-deps.ts` sur le projet
2. Detecter le package manager (npm / pnpm / yarn / bun)
3. Lire `package.json` pour la liste des deps
4. Executer `<pm> outdated --json` pour les versions
5. Afficher le rapport : current / wanted / latest par package

### Phase 2 — AUDIT

Executer l'audit de securite du package manager :
- **npm** : `npm audit --json`
- **pnpm** : `pnpm audit --json`
- **yarn** : `yarn npm audit --json`
- **bun** : `bun audit` (output texte, pas de JSON)

Classifier par severite : `critical` > `high` > `moderate` > `low`.
Pour chaque vulnerabilite : nom, severite, titre, URL advisory, fix disponible.

### Phase 3 — ANALYZE

Pour les major updates, evaluer le risque avant de proposer :
- Verifier si un `CHANGELOG.md` ou `RELEASES.md` existe dans le package
- Classer : breaking = changement de major version
- Afficher les packages groupes par risque : safe (patch/minor) / risque (major)

### Phase 4 — UPDATE

Sequence d'update recommandee :
1. **Patch updates** — sans risque, appliquer en masse
2. **Minor updates** — compatibles semver, appliquer par groupe logique
3. **Major updates** — evaluer un par un, proposer une migration guide

Pour chaque batch :
1. Mettre a jour les packages
2. Lancer `npm run build` (ou equivalent) pour detecter les erreurs de compilation
3. Lancer les tests si disponibles
4. En cas d'echec : rollback du batch et signaler

### Phase 5 — TEST

Apres chaque batch d'updates :
- Chercher le script de test dans `package.json` (`test`, `test:unit`, `vitest`)
- Si trouve : executer et verifier le resultat
- Si echec : rollback automatique (`git checkout package.json && <pm> install`)
- Signaler les packages qui ont fait echouer les tests

---

## Exemples

### 1. Scanner les packages obsoletes

```
/hora-deps scan
```

Sortie : tableau avec nom / current / wanted / latest / type (dep ou devDep) / breaking (boolean).

### 2. Audit de securite seul

```
/hora-deps audit
```

Sortie : vulnerabilites classees par severite avec lien advisory et statut du fix.

### 3. Update safe avec dry-run d'abord

```
/hora-deps update-safe --dry-run
/hora-deps update-safe
```

Voir d'abord ce qui sera mis a jour, puis appliquer avec tests automatiques.

---

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/scan-deps.ts` | `npx tsx scripts/scan-deps.ts [project-dir]` |

---

## Troubleshooting

### `outdated` ne retourne rien malgre des packages obsoletes

- npm `outdated` sort sur stderr avec exit code 1 quand des packages sont obsoletes — c'est normal
- Le script capture stderr ET stdout pour contourner ce comportement
- Verifier que `node_modules` est installe : `npm install` d'abord

### L'audit echoue avec pnpm

- `pnpm audit` necessite pnpm >= 7.0.0 : `pnpm --version` pour verifier
- Le format JSON de pnpm audit differe de npm — le script gere les deux formats
- Si `pnpm audit` n'est pas disponible, le script tombe en fallback sur `npm audit`

### Les tests echouent apres update-safe

- Un patch update peut quand meme introduire une regression (violation semver du maintainer)
- Le script rollback automatiquement via `git checkout package.json && <pm> install`
- Consulter le changelog du package incrimine avec `/hora-deps check <package>`

---

## Regles

1. **Safe d'abord** — Toujours `update-safe` avant `update-all`
2. **Tests obligatoires** — Ne jamais skipper les tests apres un update (sauf `--skip-tests` explicite)
3. **Dry-run disponible** — Toujours proposer le dry-run pour les major updates
4. **Un batch = un commit** — Chaque batch d'updates merite un commit separe pour bisect facile
