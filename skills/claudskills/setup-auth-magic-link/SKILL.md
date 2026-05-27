---
description: Met en place un système d'authentification Magic Link (passwordless) complet pour FastAPI + React
argument-hint: [description du projet ou contexte]
model: opus
---

# Setup Auth Magic Link — Authentification sans mot de passe

Implémente un système d'authentification **Magic Link** (passwordless) complet et sécurisé pour une application FastAPI + React. Le principe : l'utilisateur saisit son email, reçoit un lien unique par email, clique dessus et est authentifié. Aucun mot de passe n'est stocké ni transmis.

## Variables

CONTEXTE_PROJET: $ARGUMENTS

## Instructions

- Lis le `CONTEXTE_PROJET` pour adapter l'implémentation au projet cible.
- **Utilise le mode team** : invoque le skill `plan-with-team` pour planifier, puis `build` pour exécuter avec des agents spécialisés (backend, frontend, email, validation).
- Suis la checklist ci-dessous comme référence. Chaque point est essentiel.

## Architecture Magic Link - Checklist

### 1. Flow d'authentification

```
1. L'utilisateur saisit son email sur /login
2. POST /auth/magic-link { email }
   → Génère un token unique, single-use
   → Envoie un email avec le lien : https://app.example.com/auth/verify?token=xxx
   → Retourne toujours HTTP 200 (même si email inconnu — anti-énumération)
3. L'utilisateur clique sur le lien dans son email
4. GET /auth/verify?token=xxx (ou POST /auth/verify { token })
   → Valide le token (existe, non expiré, non utilisé)
   → Marque le token comme utilisé (single-use)
   → Génère access_token + refresh_token en cookies HttpOnly
   → Redirige vers l'app
5. Les requêtes suivantes utilisent les cookies JWT (identique à l'auth classique)
```

### 2. Génération du token Magic Link

- Utiliser `secrets.token_urlsafe(32)` — 256 bits d'entropie, URL-safe
- **Ne jamais utiliser UUID** comme token — prévisible, seulement 122 bits d'entropie
- Stocker le **hash** du token en BD (SHA-256), pas le token en clair — si la BD est compromise, les tokens ne sont pas exploitables
- Stocker avec : `email`, `token_hash`, `created_at`, `expires_at`, `used_at` (null si non utilisé)

```python
import secrets
import hashlib

token = secrets.token_urlsafe(32)
token_hash = hashlib.sha256(token.encode()).hexdigest()
# Stocker token_hash en BD, envoyer token par email
```

### 3. Modèle BD — MagicLinkToken

```python
class MagicLinkToken(SQLModel, table=True):
    __tablename__ = "magic_link_tokens"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, index=True)
    token_hash: str = Field(max_length=64, unique=True, index=True)  # SHA-256 hex
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime  # created_at + 15 min
    used_at: datetime | None = Field(default=None)  # null = non utilisé
    ip_address: str | None = Field(default=None, max_length=45)  # IP du demandeur
```

### 4. Endpoints Backend (FastAPI)

```
POST /auth/magic-link      → demande un magic link (email) — rate limited
POST /auth/verify-magic    → vérifie le token, crée la session JWT
POST /auth/refresh         → refresh token (identique à l'auth classique)
POST /auth/logout          → supprime les cookies
GET  /auth/me              → retourne l'utilisateur courant
```

### 5. Sécurité du token

- **Expiration courte** : 15 minutes maximum (10 min recommandé)
- **Single-use** : marquer `used_at` dès la première vérification (dans la même transaction SQL)
- **Anti-énumération** : toujours retourner le même message ("Si cet email existe, un lien a été envoyé") — même timing de réponse
- **Anti-brute-force** : rate limiting strict sur `/auth/magic-link` (3 req/min par email, 10 req/min par IP)
- **Nettoyage** : supprimer les tokens expirés périodiquement (tâche cron ou à chaque requête)
- **IP logging** : stocker l'IP du demandeur pour audit

### 6. Anti-énumération — Timing constant

```python
@router.post("/magic-link")
@limiter.limit("10/minute")
async def request_magic_link(data: MagicLinkRequest, request: Request, session: DbSession):
    # Toujours faire le même travail, que l'email existe ou non
    user = await get_user_by_email(session, data.email)

    if user and user.is_active:
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        # Stocker en BD + envoyer email
        await store_magic_token(session, data.email, token_hash, request.client.host)
        await send_magic_link_email(data.email, token)
    else:
        # Simuler le même délai pour empêcher le timing attack
        await asyncio.sleep(random.uniform(0.1, 0.3))

    # Toujours la même réponse
    return {"message": "Si cet email est associé à un compte, un lien de connexion a été envoyé."}
```

### 7. Vérification du token

```python
@router.post("/verify-magic")
async def verify_magic_link(data: VerifyMagicRequest, session: DbSession, response: Response):
    token_hash = hashlib.sha256(data.token.encode()).hexdigest()

    # Requête atomique : sélectionner ET marquer comme utilisé
    result = await session.execute(
        select(MagicLinkToken)
        .where(
            MagicLinkToken.token_hash == token_hash,
            MagicLinkToken.used_at.is_(None),
            MagicLinkToken.expires_at > datetime.utcnow(),
        )
        .with_for_update()  # Verrou pessimiste — empêche la double utilisation
    )
    magic_token = result.scalar_one_or_none()

    if not magic_token:
        raise HTTPException(status_code=401, detail="Lien invalide ou expiré")

    magic_token.used_at = datetime.utcnow()

    user = await get_user_by_email(session, magic_token.email)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Compte inactif")

    # Créer la session JWT (identique à l'auth classique)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    _set_auth_cookies(response, access_token, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}
```

### 8. Session JWT après vérification

- Après vérification du magic link, le système bascule sur des **cookies HttpOnly JWT** identiques à l'auth classique
- Appliquer toutes les mêmes règles que le skill `setup-auth` :
  - Cookies HttpOnly, Secure, SameSite=Lax
  - Scope `/api` pour access, `/api/auth` pour refresh
  - Rotation du refresh token
  - Révocation (token family ID ou blacklist)
  - Rate limiting sur `/auth/refresh`

### 9. Envoi d'email

- Utiliser un service SMTP ou un provider transactionnel (Resend, SendGrid, Postmark)
- **HTML + texte brut** : toujours envoyer les deux versions
- Le lien doit pointer vers le **frontend** (pas directement l'API) : `https://app.example.com/auth/verify?token=xxx`
- Le frontend récupère le token depuis l'URL et appelle `POST /auth/verify-magic`
- **Ne jamais inclure le token dans le sujet** de l'email (visible dans les aperçus)
- Configurer SPF, DKIM, DMARC pour éviter que les emails atterrissent en spam

### 10. Frontend React

- **Page /login** : formulaire email uniquement, message de confirmation après soumission
- **Page /auth/verify** : lit le token depuis `searchParams`, appelle l'API, redirige vers `/`
- Afficher un état de chargement pendant la vérification
- Gérer les erreurs : token expiré, déjà utilisé, invalide — avec messages clairs
- **Pas de stockage du token** côté client (il vient de l'URL, est envoyé une fois, puis c'est les cookies JWT)
- Route guard identique à l'auth classique (`__root.tsx`)
- `credentials: "include"` sur tous les fetch

```typescript
// /auth/verify page
function VerifyMagicLink() {
  const { token } = useSearch({ from: "/auth/verify" })
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) { navigate({ to: "/login" }); return }

    fetch(`${API_BASE}/auth/verify-magic`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ token }),
    })
      .then(res => {
        if (res.ok) navigate({ to: "/" })
        else navigate({ to: "/login", search: { error: "expired" } })
      })
      .catch(() => navigate({ to: "/login", search: { error: "network" } }))
  }, [token])

  return <Loader2 className="animate-spin" />
}
```

### 11. Rate Limiting spécifique

| Endpoint | Limite | Raison |
|----------|--------|--------|
| `POST /auth/magic-link` | 3/min par email | Anti-spam email |
| `POST /auth/magic-link` | 10/min par IP | Anti-abus global |
| `POST /auth/verify-magic` | 10/min par IP | Anti-brute-force token |
| `POST /auth/refresh` | 5/min par IP | Standard |

Le rate limiting par email nécessite un limiter custom (pas juste l'IP) :
```python
def get_email_key(request: Request) -> str:
    """Rate limit key based on email in request body."""
    # Attention : nécessite de parser le body, utiliser un middleware ou cache
    return f"magic_link:{request.state.email}"
```

### 12. Headers de sécurité HTTP

Identique au skill `setup-auth` : HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Permissions-Policy.

### 13. CORS

Identique au skill `setup-auth` : whitelist explicite, credentials=True, méthodes/headers explicites.

## Points souvent oubliés

- **Hasher le token en BD** (SHA-256) — ne jamais stocker le token brut
- **Verrou pessimiste** (`with_for_update()`) lors de la vérification pour empêcher la race condition double-utilisation
- **Timing constant** sur la demande de magic link — ne pas révéler si l'email existe
- **Réponse identique** que l'email existe ou non
- **Expiration des tokens** : nettoyer régulièrement les tokens expirés (cron job ou cleanup lazy)
- **Le lien pointe vers le frontend**, pas vers l'API directement
- **Ne pas logger le token** dans les logs applicatifs (logger le hash uniquement)
- **Email en HTML + texte brut** — certains clients email n'affichent pas le HTML
- **Créer l'utilisateur automatiquement ?** — décision métier. Si oui, seulement pour les domaines autorisés
- **Throttle par email** en plus de l'IP — sinon un attaquant peut spammer la boîte de réception d'un utilisateur

## Paquets Python nécessaires

```
pyjwt[cryptography]
argon2-cffi          # pour les API keys si besoin (pas les magic tokens)
slowapi
python-multipart
aiosmtplib           # ou httpx pour les API email (Resend, SendGrid)
```

## Paquets Frontend nécessaires

```
@tanstack/react-query
```

## Comparaison Magic Link vs Mot de passe

| Aspect | Magic Link | Mot de passe |
|--------|-----------|--------------|
| UX | Plus simple (pas de MDP à retenir) | Familier |
| Sécurité stockage | Rien à stocker côté serveur (pas de hash MDP) | Hash bcrypt/Argon2 |
| Dépendance | Email fiable requis | Aucune |
| Vitesse login | Plus lent (attente email) | Instantané |
| Phishing | Résistant (le token est unique) | Vulnérable |
| Offline | Impossible | Possible |
| 2FA | Le magic link EST le 2FA (possession email) | Nécessite TOTP/SMS en plus |
