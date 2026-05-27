---
description: Audit de sécurité complet de l'authentification d'une application (backend + frontend + infra)
argument-hint: [chemin du projet à auditer]
model: opus
---

# Audit Auth — Audit de sécurité d'authentification

Réalise un audit de sécurité complet du système d'authentification d'une application. Analyse le backend, le frontend et l'infrastructure pour identifier les vulnérabilités, les mauvaises pratiques et les améliorations possibles. Produit un rapport structuré avec sévérité et correctifs.

## Variables

CHEMIN_PROJET: $ARGUMENTS

## Instructions

- Si aucun `CHEMIN_PROJET` n'est fourni, STOP et demande à l'utilisateur de le fournir (AskUserQuestion).
- **Utilise le mode team** : crée une équipe avec les agents décrits ci-dessous pour paralléliser l'audit.
- Chaque agent produit ses findings. Le chef d'équipe compile le rapport final.
- Le rapport final doit être sauvegardé dans `CHEMIN_PROJET/audit-auth-report.md`.

## Équipe d'audit

Crée une équipe via `TeamCreate` avec les membres suivants. Chaque agent est un `builder` ou `general-purpose`.

### Agent 1 : `backend-auditor`
**Subagent type** : `general-purpose`
**Mission** : Auditer tout le code backend lié à l'authentification.

Checklist à vérifier :
1. **JWT Configuration**
   - Algorithme (HS256 minimum, RS256 préféré pour microservices)
   - Longueur de la clé secrète (>= 32 chars pour HS256, >= 2048 bits pour RS256)
   - TTL des tokens (access <= 30 min, refresh <= 7 jours)
   - Validation du type de token (access vs refresh vs totp_pending)
   - Présence du claim `exp` vérifié automatiquement
   - Présence du claim `sub` avec UUID valide

2. **Stockage des tokens**
   - Cookies HttpOnly (pas localStorage)
   - Attributs : `secure=True`, `samesite=lax|strict`, paths scopés
   - Refresh token avec path restreint (`/api/auth` pas `/api`)

3. **Hachage des mots de passe**
   - Algorithme : Argon2id (recommandé) ou bcrypt (acceptable)
   - Pas de MD5, SHA1, SHA256 nu, ou stockage en clair
   - `passlib` déprécié — vérifier la lib utilisée

4. **Rate limiting**
   - Présent sur login, register, refresh, reset password, magic link
   - Limites raisonnables (5-10/min par IP)
   - Handler HTTP 429 configuré

5. **Protection mass assignment**
   - `_ALLOWED_FIELDS` ou `extra="forbid"` sur chaque endpoint d'update
   - Pas de `setattr()` sans whitelist

6. **CORS**
   - Pas de `allow_origins=["*"]` avec credentials
   - Méthodes et headers explicites (pas `["*"]`)

7. **Injection SQL**
   - Utilisation d'un ORM (SQLModel/SQLAlchemy)
   - Échappement des wildcards LIKE (`%`, `_`)
   - Pas de requêtes SQL brutes avec f-strings

8. **Gestion des erreurs & anti-énumération**
   - Messages génériques vers le client (pas de stack traces, pas de détails d'API externes)
   - **Énumération d'utilisateurs** : le login doit retourner un message identique que l'email existe ou non (ex: "Identifiants invalides") — jamais "Email inconnu" vs "Mot de passe incorrect"
   - Même principe sur reset password / magic link : "Si cet email existe, un lien a été envoyé"
   - Vérifier que le timing de réponse est constant (pas de shortcut si l'email n'existe pas)

9. **Logs d'authentification**
   - Les tentatives de login échouées sont-elles loggées ? (avec IP, email, timestamp)
   - Les mots de passe ne sont **PAS** loggés (grep `password` dans les appels logger/print)
   - Les tokens JWT ne sont **PAS** loggés en clair
   - Les événements de sécurité (changement MDP, activation 2FA, logout) sont-ils loggés ?

10. **Sessions concurrentes**
    - Existe-t-il une limite sur le nombre de sessions actives par utilisateur ?
    - Si refresh tokens sont stockés en BD : combien peut-on en avoir simultanément ?
    - Pour les apps métier sensibles : envisager une limite (ex: 5 sessions max) avec invalidation de la plus ancienne

12. **Refresh token**
    - Rotation à chaque usage
    - Révocation possible (blacklist ou token family)
    - Vérification user en BD à chaque refresh

13. **2FA / TOTP**
    - Secret stocké (idéalement chiffré)
    - `valid_window` raisonnable (1-2)
    - Rate limiting sur verify-totp

14. **Logout**
    - Suppression des cookies côté serveur
    - Idéalement : invalidation côté serveur (blacklist)

15. **Dépendances Python vulnérables**
    - Lancer `pip-audit` ou `uv run pip-audit` (si disponible)
    - Vérifier les versions de PyJWT, cryptography, bcrypt/argon2-cffi

### Agent 2 : `frontend-auditor`
**Subagent type** : `general-purpose`
**Mission** : Auditer tout le code frontend lié à l'authentification.

Checklist à vérifier :
1. **Stockage des tokens**
   - Aucun token dans localStorage, sessionStorage, ou variable JS
   - `credentials: "include"` sur tous les fetch/axios
   - Pas de header `Authorization: Bearer xxx` construit manuellement depuis le client

2. **Protection XSS**
   - Pas de `dangerouslySetInnerHTML` sans DOMPurify
   - Pas d'`eval()`, `new Function()`, ou `innerHTML` avec données dynamiques
   - CSP header configuré

3. **Validation des URLs**
   - `isValidDownloadUrl()` ou équivalent avant `window.open()`
   - Blocage des protocoles `javascript:`, `data:`, `file://`
   - `encodeURIComponent()` sur tous les IDs dans les URLs API

4. **Route guards**
   - Vérification auth sur chaque route protégée
   - Redirection vers /login si non authentifié
   - Pas de contenu flash avant redirection

5. **Refresh flow**
   - Interception des 401 → refresh → retry
   - Déduplication des appels refresh parallèles
   - Redirection /login si refresh échoue + appel logout serveur

6. **Vérification HTTPS**
   - Warning ou blocage si protocole != https en production

7. **Cache React Query / state**
   - `queryClient.clear()` au logout
   - Pas de données sensibles persistées dans le state après logout

8. **Dépendances JS vulnérables**
   - Lancer `pnpm audit` ou `npm audit`
   - Vérifier les versions de dompurify, react, etc.

### Agent 3 : `infra-auditor`
**Subagent type** : `general-purpose`
**Mission** : Auditer la configuration infrastructure et les headers de sécurité.

Checklist à vérifier :
1. **Headers HTTP**
   - `Strict-Transport-Security` (HSTS) avec max-age >= 1 an
   - `Content-Security-Policy` configuré (pas `unsafe-inline` sauf nécessité documentée)
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY` ou `SAMEORIGIN`
   - `Permissions-Policy` restrictif
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - Pas de header `Server` exposé (version du serveur)

2. **Docker**
   - Conteneurs non-root (`USER appuser`)
   - Images pinnées sur des versions exactes (pas `latest`)
   - Ports non-privilégiés pour nginx/frontends
   - Limites CPU/mémoire définies
   - Pas de secrets dans les Dockerfiles ou docker-compose.yml
   - Multi-stage builds (pas d'outils de build en production)

3. **Secrets**
   - Pas de `.env` versionné (vérifier .gitignore)
   - Pas de secrets en dur dans le code (grep pour `password=`, `secret=`, `api_key=`)
   - **Historique Git** : lancer `gitleaks detect` — un secret supprimé du code mais encore dans l'historique Git est toujours exploitable
   - Variables d'environnement injectées via CI/CD
   - Secret key JWT suffisamment longue

4. **TLS / Reverse Proxy**
   - HTTPS forcé (redirection HTTP → HTTPS)
   - TLS 1.2+ uniquement
   - Certificats valides et auto-renouvelés (Let's Encrypt / Caddy auto)

5. **CI/CD**
   - GitHub Actions pinnées sur des versions exactes (pas `@main`)
   - Pas de secrets dans les logs de CI
   - Images Docker tagguées (pas `latest`)

6. **Fichiers sensibles exposés**
   - Pas de `.env`, `.git/`, `__pycache__/`, `node_modules/` accessibles via HTTP
   - Pas de page de debug/admin exposée en production

## Commandes automatiques

L'agent chef d'équipe doit lancer ces commandes au début de l'audit pour collecter des données :

```bash
# Dépendances Python vulnérables
cd CHEMIN_PROJET/backend && uv run pip-audit 2>/dev/null || echo "pip-audit non disponible"

# Dépendances JS vulnérables (pour chaque frontend)
cd CHEMIN_PROJET/frontend-client && pnpm audit 2>/dev/null || npm audit 2>/dev/null || echo "audit non disponible"
cd CHEMIN_PROJET/frontend-admin && pnpm audit 2>/dev/null || npm audit 2>/dev/null || echo "audit non disponible"

# Secrets en dur dans le code
grep -rn "password\s*=" --include="*.py" --include="*.ts" --include="*.tsx" CHEMIN_PROJET/ | grep -v node_modules | grep -v __pycache__ | grep -v ".env.example"
grep -rn "secret.*=.*['\"]" --include="*.py" --include="*.ts" CHEMIN_PROJET/ | grep -v node_modules | grep -v __pycache__

# Secrets dans l'historique Git (un secret supprimé du code reste dans l'historique)
cd CHEMIN_PROJET && gitleaks detect --source . 2>/dev/null || echo "gitleaks non disponible — installer avec: brew install gitleaks"

# Fichiers .env versionnés
find CHEMIN_PROJET -name ".env" -not -path "*/node_modules/*" -not -path "*/.git/*"

# Vérifier .gitignore
cat CHEMIN_PROJET/.gitignore 2>/dev/null | grep -E "\.env|secret|credential"

# Vérifier que les mots de passe ne sont pas loggés
grep -rn "log.*password\|print.*password\|logger.*password" --include="*.py" CHEMIN_PROJET/ | grep -v node_modules | grep -v __pycache__
```

## Patterns dangereux à chercher (grep)

Chaque agent doit rechercher ces patterns dans son périmètre :

**Note** : ces patterns sont des **heuristiques** — un match ne signifie pas forcément une vulnérabilité, et l'absence de match ne garantit pas la sécurité. Par exemple, `dangerouslySetInnerHTML` avec DOMPurify sur une ligne différente ne sera pas détecté. Chaque match doit être vérifié manuellement dans son contexte.

### Backend
```
localStorage                    # Ne devrait pas apparaître côté backend
eval(                           # Exécution dynamique de code
exec(                           # Exécution dynamique de code
__import__                      # Import dynamique
setattr.*request                # Mass assignment potentiel
.format(.*password              # Log de mot de passe
f".*password                    # Log de mot de passe
log.*password|print.*password   # Password dans les logs
allow_origins.*\*               # CORS wildcard
MD5\(|md5\(|sha1\(             # Hachage faible
"SELECT.*".*\+|f"SELECT        # SQL brut avec concaténation
email.*(inconnu|not found|unknown)  # Énumération utilisateurs
```

### Frontend
```
localStorage.*token             # Token dans localStorage
sessionStorage.*token           # Token dans sessionStorage
dangerouslySetInnerHTML         # Vérifier manuellement que DOMPurify est utilisé (peut être sur une autre ligne)
eval\(                          # Exécution dynamique
new Function\(                  # Exécution dynamique
window\.open\(                  # Vérifier manuellement que l'URL est validée
innerHTML\s*=                   # XSS potentiel
document\.cookie                # Accès direct aux cookies
```

## Format du rapport

Le rapport final (`audit-auth-report.md`) doit suivre ce format :

```markdown
# Rapport d'Audit d'Authentification
**Projet** : [nom]
**Date** : [date]
**Auditeur** : Claude Code — Audit Auth Skill

## Résumé exécutif
- X vulnérabilités critiques
- X vulnérabilités élevées
- X vulnérabilités moyennes
- X points d'amélioration

## Score global : X/100

## Findings

### [CRITIQUE] Titre du finding
**Composant** : backend | frontend | infra
**Fichier** : chemin:ligne
**Description** : Description claire du problème
**Impact** : Ce qui pourrait arriver si exploité
**Correctif** :
\```python
# Code correctif concret
\```
**Référence** : OWASP / CWE / CVE si applicable

### [ÉLEVÉ] ...
### [MOYEN] ...
### [FAIBLE] ...

## Audit des dépendances
### Python (pip-audit)
[résultat]
### JavaScript (pnpm audit)
[résultat]

## Checklist OWASP Auth
| Contrôle | Statut | Détail |
|----------|--------|--------|
| Hachage mots de passe | ✅/⚠️/❌ | ... |
| Protection brute-force | ✅/⚠️/❌ | ... |
| ... | ... | ... |

## Recommandations prioritaires
1. [Action immédiate — critique]
2. [Action court terme — élevé]
3. [Action moyen terme — moyen]
```

## Scoring

Le score global est calculé sur 100 points :

| Catégorie | Points | Critères |
|-----------|--------|----------|
| Stockage tokens | /15 | HttpOnly cookies, pas localStorage, scope, secure, samesite |
| Hachage MDP | /10 | Argon2id/bcrypt, pas de clair/MD5/SHA |
| Rate limiting | /10 | Présent sur endpoints sensibles, limites raisonnables |
| CORS | /5 | Pas de wildcard, headers explicites |
| XSS protection | /10 | DOMPurify, CSP, pas d'eval/innerHTML |
| Injection SQL | /5 | ORM, pas de requêtes brutes, LIKE échappé |
| Refresh token | /10 | Rotation, révocation, vérif user BD |
| Headers HTTP | /10 | HSTS, CSP, X-Content-Type, X-Frame |
| Secrets | /10 | Pas de secrets en dur, .env ignoré, clé JWT longue, gitleaks clean |
| Docker/Infra | /5 | Non-root, versions pinnées, limites resources |
| Dépendances | /5 | Pas de CVE connues |
| Mass assignment | /5 | ALLOWED_FIELDS ou extra=forbid |

### Règle de plafonnement

**Un seul finding CRITIQUE plafonne le score à 40/100 maximum**, quel que soit le score des autres catégories. Cela évite un faux sentiment de sécurité (ex: score 85 alors qu'un mot de passe est stocké en clair).

- 1+ finding **CRITIQUE** → score plafonné à **40/100**
- 3+ findings **ÉLEVÉ** → score plafonné à **60/100**
- Les plafonds sont cumulatifs : le plus bas s'applique

## Sévérité

| Niveau | Définition | Exemples |
|--------|-----------|----------|
| **CRITIQUE** | Exploitable immédiatement, impact majeur | Token dans localStorage, MDP en clair, SQL injection, CORS wildcard avec credentials |
| **ÉLEVÉ** | Exploitable avec effort modéré, impact significatif | Pas de rate limiting sur login, pas de refresh token rotation, secrets en dur |
| **MOYEN** | Exploitation indirecte ou impact limité | Headers HTTP manquants, TOTP secret non chiffré, pas de blacklist token |
| **FAIBLE** | Bonne pratique non respectée, risque théorique | Docker en root, images non pinnées, warning HTTPS au lieu de blocage |
