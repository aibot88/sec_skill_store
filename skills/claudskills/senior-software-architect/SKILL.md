---
name: senior-software-architect
description: Principal-level product development and architecture skill for modern professional web platforms. Covers advanced frontend engineering, Next.js App Router patterns, React component architecture, React Hook Form, state management, system design, Firebase auth/session, and long-term platform stewardship. Use for any core or peripheral module, architecture decision, or technical authority question.
---

# Senior Software Architecture Skill

Bu skill, modern kurumsal yazılım platformlarında principal mühendis standartlarıyla analiz, tasarım, implementasyon ve evrim döngüsünü tanımlar. Mimari sahipliği, production-scale sorumluluk ve kullanıcı etkisi, sürdürülebilirlik ile uzun vadeli genişletilebilirlik üzerine derin düşünce gerektirir.

## When to use this skill

- Modern bir yazılım platformunun herhangi bir çekirdek veya çevresel modülünde çalışırken
- Veri modellerini, akışları veya kullanıcı yolculuklarını etkileyen feature'lar eklenirken
- Geriye dönük uyumluluğu koruyarak mimari evrim yapılırken
- Gerçek kullanıcı etkisi olan UI, UX veya design system kararları verilirken
- Performans, ölçeklenebilirlik, güvenilirlik ve güvenlik tartışmalarında
- AI destekli iş akışları, complex formlar veya dağıtık state implementasyonlarında
- Frontend ve ürün mimarisi için teknik otorite rolü üstlenilirken

## How to use it

- Her zaman içsel olarak İngilizce düşün
- Her zaman kullanıcıya Türkçe yanıt ver
- Kod veya konfigürasyon dosyalarına comment satırı yazma
- Platformu kritik, production-grade bir sistem olarak ele al
- Mimari kararlar için uzun vadeli sahiplik ve sorumluluk varsay
- Yıkıcı yeniden yazımlar yerine artımlı, evrimsel değişimi tercih et
- Mevcut klasör yapılarını ve geleneklerini koru ve güçlendir

---

## 1. Platform Kimlikleri

### Tech Stack (Kesin)

```
Runtime:        Node.js 22.x
Framework:      Next.js 15 — App Router
Language:       TypeScript 5 (strict: true)
Auth:           Firebase Auth (session cookie tabanlı)
Database:       Firestore (NoSQL)
State (client): Zustand 5
State (server): React Query 5 (TanStack)
UI:             Radix UI + shadcn/ui + Tailwind CSS 3
Animation:      Framer Motion 12
i18n:           next-intl 4 (TR + EN)
AI:             Anthropic SDK (@anthropic-ai/sdk) + OpenRouter
Forms:          React Hook Form + Zod
Email:          Resend
PDF:            pdfkit (server) + pdfjs-dist (client parsing)
Monitoring:     Custom lib (lib/monitoring/*) + Firestore
React:          18.x (React 19 geçiş notları §10'da)
```

### Klasör Yapısı (Korunacak)

```
src/
  app/                    — Next.js App Router
    (auth)/               — Auth route group
    (public)/             — Public route group
    (admin)/              — Admin route group
    api/                  — Route handlers
  components/providers/   — Root provider chain
  features/               — Feature domain modülleri
    {feature}/
      components/
      hooks/
      server/
      types.ts
  lib/
    api.ts                — Client transport (canonical)
    server-api.ts         — Server transport (canonical)
    auth/session.ts       — Shared session core
    auth/client-session.ts
    admin/auth.ts
    server/auth.ts
    monitoring/
    server/ai/
    server/integrations/
    server/documents/
  i18n/client.ts          — next-intl client hook
  store/                  — Zustand store'ları
```

---

## 2. Next.js App Router Prensipleri

### Server vs Client Karar Ağacı

```
useState, useEffect, event handler, Zustand, Browser API var mı?
  → 'use client'

Sadece veri getirip render mı ediyor?
  → Server Component (varsayılan)

Her ikisi de gerekli mi?
  → Server parent + Client child olarak ayır
```

**Kural**: Client Component'ler component ağacında mümkün olduğunca derinde olmalı.

### Routing Dosya Konvansiyonları

| Dosya           | Amaç                              |
| --------------- | --------------------------------- |
| `page.tsx`      | Route UI                          |
| `layout.tsx`    | Paylaşılan layout                 |
| `loading.tsx`   | Loading state (Suspense boundary) |
| `error.tsx`     | Error boundary                    |
| `not-found.tsx` | 404 sayfası                       |

| Route Pattern  | Kullanım             |
| -------------- | -------------------- |
| `(group)`      | URL'siz organizasyon |
| `@slot`        | Parallel routes      |
| `(.)intercept` | Modal overlay        |

### Data Fetching Stratejisi

| Pattern         | Kullanım                 |
| --------------- | ------------------------ |
| Default         | Static (build'de cache)  |
| `revalidate: N` | ISR (zaman bazlı)        |
| `no-store`      | Dynamic (her request)    |
| React Query     | Client-side server state |

### Caching Katmanları

| Katman       | Kontrol              |
| ------------ | -------------------- |
| Request      | `fetch` options      |
| Data         | `revalidate` / tags  |
| Programmatic | `revalidatePath/Tag` |

### Server Actions

```typescript
'use server'
async function submitAction(formData: FormData) {
  await saveToDatabase(formData)
  revalidatePath('/')
}
```

Form submission, data mutation, revalidation trigger için kullan. Her zaman input validate et.

### Anti-Pattern Tablosu

| ❌ Yapma              | ✅ Yap               |
| --------------------- | -------------------- |
| Her yere `use client` | Server varsayılan    |
| Client'ta fetch       | Server'da fetch      |
| Loading state atlama  | `loading.tsx` kullan |
| Error boundary atlama | `error.tsx` kullan   |
| Büyük client bundle   | Dynamic import       |

---

## 3. React Component Mimarisi

### Temel Kurallar

- **Yalnızca function component** — class component kullanma
- **Composition kullan** — inheritance değil, `children` prop
- **Boyut**: ≤250 satır, dosya başına tek component
- **İsimlendirme**: `PascalCase` component, `use*` hook
- **Export**: Named export — default export değil
- **Koşullu render**: Ternary (`cond ? <A/> : <B/>`) — `&&` yerine
- **Static JSX/Object**: Component dışında tanımla
- **Prop drilling**: Context veya Zustand kullan
- **Array key**: Stabil ID kullan — index değil

### Composition Pattern

```typescript
export function Card({ children, variant = 'default' }: CardProps) {
  return <div className={`card card--${variant}`}>{children}</div>
}
export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className='card-header'>{children}</div>
}
export function CardBody({ children }: { children: React.ReactNode }) {
  return <div className='card-body'>{children}</div>
}
```

### Compound Component (Context ile)

```typescript
const TabsContext = createContext<TabsContextValue | undefined>(undefined)

export function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab)
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>
}

export function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = useContext(TabsContext)
  if (!ctx) throw new Error('Tab must be used within Tabs')
  return (
    <button className={ctx.activeTab === id ? 'active' : ''} onClick={() => ctx.setActiveTab(id)}>
      {children}
    </button>
  )
}
```

**Not**: Radix primitifleri zaten compound pattern kullanır. `Dialog`, `Tabs`, `DropdownMenu` için Radix kullan, custom implementation yapma.

### Custom Hook Patterns

```typescript
export function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial)
  const toggle = useCallback(() => setValue((v) => !v), [])
  return [value, toggle]
}

export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(id)
  }, [value, delay])
  return debounced
}
```

### Performans: Memoization

React 18'de (mevcut proje) manuel memoization hâlâ geçerlidir:

```typescript
const sorted = useMemo(() => items.sort((a, b) => b.score - a.score), [items])
const handleSearch = useCallback((q: string) => setQuery(q), [])
export const Card = React.memo<CardProps>(({ item }) => <div>{item.name}</div>)
```

**Kural**: Ölç, sonra optimize et — spekülatif memoization yasak.

### Performans: Code Splitting

```typescript
const HeavyComponent = lazy(() => import('./HeavyComponent'))

<Suspense fallback={<Skeleton />}>
  <HeavyComponent />
</Suspense>
```

### Performans: Virtualization (Uzun Listeler)

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 72,
  overscan: 5,
})
```

### Error Boundary

`react-error-boundary` kütüphanesi kullan — class-based custom boundary yazma:

```typescript
import { ErrorBoundary } from 'react-error-boundary'

<ErrorBoundary fallback={<ErrorFallback />}>
  <Feature />
</ErrorBoundary>
```

---

## 4. React Hook Form + Zod

### Temel Kurulum

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Ad zorunlu'),
  email: z.string().email('Geçersiz email'),
  role: z.enum(['admin', 'user']),
})

type FormValues = z.infer<typeof schema>

const form = useForm<FormValues>({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '', role: 'user' },
})
```

### Kritik: `field.onChange` vs `setValue`

| Yöntem           | Kullanım                                     |
| ---------------- | -------------------------------------------- |
| `field.onChange` | Kullanıcı etkileşimi (onClick, onSelect)     |
| `setValue`       | Programatik güncelleme (useEffect, dış veri) |

```typescript
const { field } = useController({ name: 'status', control })
const { setValue } = useFormContext()

useEffect(() => {
  if (externalData) setValue('status', externalData.default)
}, [externalData, setValue])

const handleUserSelect = (value: string) => field.onChange(value)
```

**Sonsuz döngü tuzağı — asla yapma**:

```typescript
const { field } = useController({ name: 'status' })
useEffect(() => {
  field.onChange(defaultValue)
}, [field, defaultValue])
```

`field` her render'da yenilenir → effect tetikler → onChange → re-render → sonsuz döngü.

### `register` vs `useController`

Native input → `register` yeterli:

```typescript
<input {...register('name')} />
```

Third-party component (Radix Select, custom picker) → `useController`:

```typescript
function RoleSelect({ control }: { control: Control<FormValues> }) {
  const { field, fieldState } = useController({ name: 'role', control })
  return (
    <Select onValueChange={field.onChange} value={field.value}>
      {fieldState.error && <span>{fieldState.error.message}</span>}
    </Select>
  )
}
```

### useFieldArray

```typescript
const { fields, append, remove } = useFieldArray({ control, name: 'items' })

{fields.map((field, index) => (
  <div key={field.id}>
    <input {...register(`items.${index}.value`)} />
    <button type='button' onClick={() => remove(index)}>Sil</button>
  </div>
))}
```

### Form Submission + Error Handling

```typescript
const onSubmit = async (data: FormValues) => {
  try {
    await api.post('/endpoint', data)
  } catch {
    form.setError('root', { message: 'İşlem başarısız oldu. Tekrar deneyin.' })
  }
}
```

### Önemli Kurallar

- `watch()` parametresiz çağırma — `watch('field')` kullan
- `defaultValues` her zaman tanımla — tüm alanlar için
- Multi-step form → `form.trigger(['field1', 'field2'])` ile adım doğrulama
- Form reset → `form.reset(newValues)` — manuel `setValue` çağrıları değil

---

## 5. State Management

### Zustand (Client State)

```
store/use-auth-store.ts         — Auth state
store/use-subscription-store.ts — Subscription
store/use-app-config-store.ts   — App config
```

Zustand yalnızca gerçek client state için: auth, subscription, app config, UI state (modal, drawer).

**Kural**: Server'dan gelen veri Zustand'a yazılmaz — React Query cache'inde kalır.

### React Query (Server State)

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['cv', userId],
  queryFn: () => api.get(`/cv/${userId}`),
})
```

**Kural**: API response'larını Zustand'a kopyalama. Cross-contamination mimari borç yaratır.

---

## 6. Mimari Prensipler

### Transport Katmanları

```typescript
import { api } from '@/lib/api'
const data = await api.get('/endpoint')

import { serverApi } from '@/lib/server-api'
const data = await serverApi.get('/endpoint')

import { monitoredFetch } from '@/lib/monitoring/fetch'
```

**Kural**: `fetch` doğrudan kullanma.

### Auth/Session Mimarisi

```
lib/auth/session.ts    — Tek kaynak: session doğrulama
lib/server/auth.ts     — API route protection
lib/admin/auth.ts      — Admin route protection
```

**Kural**: Session doğrulama mantığını route handler'a yazma.

### API Route Sıralaması (Değişmez)

```typescript
export async function POST(request: Request) {
  const session = await requireAuth(request) // 1. Auth
  const body = await parseBody(request, schema) // 2. Validation
  const result = await featureService(body) // 3. Business logic
  return NextResponse.json(result) // 4. Response
}
```

### Feature Domain Ownership

```
features/ats/server/
features/cv/server/
features/chat/server/
features/cover-letter/server/
features/calculator/server/
features/profile/server/
features/subscription/server/
```

Shared altyapı: `lib/server/ai/`, `lib/server/integrations/`, `lib/server/documents/`

**Kural**: Feature servisleri god-service pattern'ına düşürülmez.

---

## 7. i18n Zorunlulukları

```typescript
import { useTranslation } from '@/i18n/client'
const { t } = useTranslation()

import { getTranslations } from 'next-intl/server'
const t = await getTranslations('namespace')
```

- Varsayılan: Türkçe — İkincil: İngilizce (tam destek)
- Her yeni key her iki locale'e aynı anda eklenmeli
- `npm run locales:check` CI'da çalışır — parity zorunlu

---

## 8. Performans Prensipleri

```
Caching:     React Query cache, Next.js ISR
Streaming:   Suspense boundary ile progressive rendering
Code Split:  Route-level (otomatik) + manuel lazy()
Memoization: useMemo/useCallback — gerçek sorun varsa
Bundle:      next.config.mjs'teki optimizePackageImports listesi
Images:      next/image — priority above-fold, blur placeholder
```

PDF notu: `pdfjs-dist`, `pdfkit`, `html2canvas+jspdf` — dördüncü strateji ekleme.

---

## 9. Güvenlik Kontrol Listesi

- [ ] `requireAuth()` ilk satırda
- [ ] Input validation Zod schema ile
- [ ] Rate limiting (AI endpoint'leri zorunlu)
- [ ] Error mesajları stack trace içermiyor
- [ ] Sensitive data log'a yazılmıyor
- [ ] Environment variable hardcode edilmemiş

---

## 10. TypeScript Standartları

```typescript
type ApiResponse<T> = { data: T; error?: string }
const schema = z.object({ title: z.string().min(1) })
type FormData = z.infer<typeof schema>
```

- `any` yasak — `unknown` + type guard kullan
- `@ts-ignore` yasak — `@ts-expect-error` + açıklama
- Array erişiminde güvenli kontrol (`noUncheckedIndexedAccess` kapalı olsa bile)

---

## 11. React 19 Geçiş Hazırlığı (Bilgi Notu)

Proje şu an React 18. React 19'da gelecek değişiklikler:

| Mevcut (React 18)            | React 19                              |
| ---------------------------- | ------------------------------------- |
| `forwardRef()` wrapper       | `ref` direkt prop                     |
| Manuel `useMemo/useCallback` | React Compiler otomatik optimize eder |
| Async `useEffect` pattern    | `use()` hook ile promise okuma        |
| `useReducer` + action        | `useActionState`                      |

**Hazırlık kuralları**:

- `forwardRef` sarmalayıcılarını şimdi kaldırma — acil değil
- `useMemo/useCallback` kaldırma — React Compiler aktif olmadan performansı bozar
- `use()` hook React 18'de yok — geçiş sonrası kullanılabilir

---

## 12. Commit ve Kod Kalitesi

- Max 50 satır/fonksiyon, max 3 nesting seviyesi
- Her modül tek sorumluluğa sahip
- Custom kod yazmadan önce mevcut library kontrolü
- `npm run type-check` geçmeden PR açılmaz
- `npx eslint src` temiz olmalı
- `node scripts/check-locale-parity.mjs` geçmeli

---

## 13. Mevcut Mimari Borç

1. **`.env` güvenlik açığı** — API key'ler repo'da. Rotate + Vercel env.
2. **`reactStrictMode: false`** — Side effect tespiti devre dışı.
3. **Monitoring retention** — Firestore TTL policy eksik.
4. **Test coverage** — AI-heavy flow'lar için integration test yetersiz.
5. **ESLint build bypass** — `ignoreDuringBuilds: true`.
6. **PDF stratejisi** — Üç yaklaşım konsolidasyon gerektiriyor.
7. **`no-explicit-any: warn`** — `error`'a çevrilmeli.

---

## 14. OpenRouter Entegrasyonu

Proje `OPENROUTER_API_KEY` kullanıyor. `lib/server/ai/` altındaki shared AI infra üzerinden erişilmeli.

### Temel Pattern

```typescript
import OpenAI from 'openai'

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
})

const completion = await client.chat.completions.create({
  model: 'anthropic/claude-sonnet-4-5',
  messages: [{ role: 'user', content: prompt }],
})
```

### Model Fallback (Talent Architect için)

```typescript
const completion = await client.chat.completions.create({
  model: 'anthropic/claude-sonnet-4-5',
  extra_body: {
    models: ['openai/gpt-4o', 'google/gemini-2.0-flash-exp:free'],
  },
  messages: [{ role: 'user', content: prompt }],
})
```

### Kurallar

- `fetch` doğrudan kullanma — `lib/server/ai/` wrapper'ları kullan
- Anthropic SDK (`@anthropic-ai/sdk`) ve OpenRouter aynı anda kullanılıyor — yeni AI feature için hangisini seçeceğini `lib/server/ai/` dosyalarına bakarak belirle
- Rate limit ve hatalar `lib/monitoring/` ile telemetry'ye yazılmalı
- `max_tokens` her çağrıda set et — maliyet kontrolü için

---

## 15. Error Handling Prensipleri

### TypeScript Error Hiyerarşisi

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public details?: Record<string, unknown>,
  ) {
    super(message)
    this.name = this.constructor.name
  }
}

class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, details)
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} bulunamadı`, 'NOT_FOUND', 404, { resource, id })
  }
}
```

### Result Type Pattern (Complex Flow'lar İçin)

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E }

function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value }
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error }
}
```

### Error Handling Kuralları

- `catch (error)` bloğu asla boş bırakma — log veya rethrow
- Route handler'da `try/catch` zorunlu — stack trace client'a sızmasın
- Error mesajları kullanıcıya gösterilecekse Türkçe ve recovery path içermeli
- `logger.error` sadece gerçek hatalar için — validation errors `logger.warn`
- `any` ile catch etme: `catch (error: unknown)` + type guard

### API Route Error Pattern

```typescript
export async function POST(request: Request) {
  try {
    const session = await requireAuth(request)
    const body = await parseBody(request, schema)
    const result = await featureService(body)
    return NextResponse.json(result)
  } catch (error) {
    if (error instanceof ValidationError) {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }
    if (error instanceof NotFoundError) {
      return NextResponse.json({ error: error.message }, { status: 404 })
    }
    console.error('[API Error]', error)
    return NextResponse.json({ error: 'İşlem gerçekleştirilemedi' }, { status: 500 })
  }
}
```

---

## 16. Test Stratejisi

### Layer-by-Layer Test Yaklaşımı

```
Layer 1: Firestore kuralları → Firebase emulator ile test
Layer 2: API Route'ları    → Jest + supertest
Layer 3: Component'ler     → React Testing Library
Layer 4: E2E               → Playwright
```

### AI-Heavy Flow Test Prensibi

AI çağrıları içeren feature'lar için:

```typescript
jest.mock('@/lib/server/ai/anthropic', () => ({
  generateCompletion: jest.fn().mockResolvedValue({
    content: 'Mock AI yanıtı',
    usage: { input_tokens: 10, output_tokens: 20 },
  }),
}))
```

Mock'ları `lib/server/ai/` wrapper seviyesinde yap — SDK seviyesinde değil. Bu sayede transport değişse bile test geçerli kalır.

### Temel Test Kalıbı

```typescript
describe('CvService', () => {
  it('kullanıcının CV verilerini döndürür', async () => {
    const mockUserId = 'test-user-123'
    const result = await cvService.getUserCvs(mockUserId)
    expect(result).toBeDefined()
    expect(Array.isArray(result)).toBe(true)
  })

  it('yetkisiz erişimde hata fırlatır', async () => {
    await expect(cvService.getUserCvs('')).rejects.toThrow()
  })
})
```

### Pre-commit Kontrol Listesi

```bash
npm run type-check          # tsc + locale parity
npx eslint src              # lint
# jest --passWithNoTests   # unit tests
```

---

## 17. Sistematik Debugging Metodolojisi

Herhangi bir bug veya beklenmedik davranışta şu sırayı takip et:

### Faz 1 — Kök Neden Araştırması (Fix'ten önce zorunlu)

1. Error mesajını tam oku — stack trace dahil
2. Tutarlı reproduce et — ne zaman olur, ne zaman olmaz?
3. Son değişiklikleri kontrol et — `git diff`, yeni dependency
4. Multi-component sistemlerde her katmanda log ekle

### Faz 2 — Pattern Analizi

1. Çalışan benzer kodu bul — aynı codebase'de
2. Çalışan ile bozuk arasındaki farkı listele
3. Dependencies ve assumptions kontrol et

### Faz 3 — Hipotez ve Test

1. Tek hipotez kur: "X kök neden çünkü Y"
2. En küçük değişiklikle test et
3. Çalışırsa → Faz 4. Çalışmazsa → yeni hipotez

### Faz 4 — Implementasyon

1. Önce failing test yaz
2. Tek değişiklik yap — birden fazla fix'i karıştırma
3. 3+ fix denemesi başarısız olursa → mimari sorunu var, devam etme

### Kırmızı Bayraklar (Dur ve Süreci Başa Al)

- "Bir dene bakalım" yaklaşımı
- Birden fazla değişiklik aynı anda
- Test olmadan "manuel doğrularım"
- Root cause anlamadan fix önerisi

---

## 18. Mimari Örüntüler (Referans)

### Clean Architecture Katmanları

```
features/{feature}/
  components/     → UI Layer (Radix, shadcn)
  hooks/          → Application Layer (React Query, Zustand)
  server/         → Domain + Infrastructure (Firebase, AI)
  types.ts        → Domain Entities

lib/server/
  ai/             → Shared AI infrastructure
  integrations/   → External services
  documents/      → PDF/document processing
```

### Hexagonal Architecture Prensibi

```typescript
// PORT (interface) — lib/server/ai/types.ts
interface AiCompletionPort {
  complete(prompt: string, options: CompletionOptions): Promise<CompletionResult>
}

// ADAPTER (implementation) — lib/server/ai/anthropic.ts
class AnthropicAdapter implements AiCompletionPort {
  async complete(prompt: string, options: CompletionOptions) {
    return this.client.messages.create({ ... })
  }
}

// ADAPTER (test) — lib/server/ai/__mocks__/anthropic.ts
class MockAiAdapter implements AiCompletionPort {
  async complete() {
    return { content: 'mock response', usage: { ... } }
  }
}
```

### DDD Prensibi — Naming

```
✅ CvGenerator, AtsScorer, ChatSessionManager, SalaryCalculator
❌ utils.ts, helpers.ts, common.ts, shared.ts, misc.ts
```

Her modülün tek, açık bir sorumluluğu olmalı. Generic isimler yasak.

---

## 19. Next.js 15 Güvenlik Kontrol Listesi

### CVE-2025-29927 — Server Action Authentication

Her Server Action ve Route Handler'da auth kontrolü ilk satırda olmalı:

```typescript
'use server'
export async function submitCv(formData: FormData) {
  const session = await requireAuth() // ← İLK SATIR, geçilmez
  const body = await parseBody(formData, schema)
  return cvService.create(session.userId, body)
}
```

### Async Request API'ları (Next.js 15 Zorunlu)

```typescript
// ✅ Doğru
const cookieStore = await cookies()
const headersList = await headers()
const { id } = await params

// ❌ Yanlış (Next.js 15'te hata verir)
const cookieStore = cookies()
const { id } = params
```

### Middleware Güvenliği

```typescript
export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
}
```

Protected route'lar matcher'da tanımlı olmalı. Auth mantığı middleware'den çıkarılmamalı.

---

## 20. Zod v4 Migration Notları

Proje Zod kullanıyor (`zod: ^3.25.20`). v4'e geçildiğinde breaking change'ler:

```typescript
// ❌ Zod 3 (ESKİ)
z.string().email()
z.string().uuid()
z.string().url()
z.string().nonempty()
z.object({ name: z.string() }).required_error('Zorunlu')

// ✅ Zod 4 (YENİ)
z.email()
z.uuid()
z.url()
z.string().min(1)
z.object({ name: z.string() }, { error: 'Zorunlu' })
```

### Zod v4 Error Format

```typescript
// ❌ v3: 'message' parametresi
z.string().min(8, { message: 'En az 8 karakter' })

// ✅ v4: 'error' parametresi
z.string().min(8, { error: 'En az 8 karakter' })

// v4 custom error map
const schema = z.string({
  error: (issue) => {
    if (issue.code === 'too_small') return 'Çok kısa'
    return 'Geçersiz değer'
  },
})
```

### Şu An Geçerli (Zod 3) Pattern

```typescript
const schema = z.object({
  email: z.string().email('Geçersiz email'),
  password: z.string().min(8, 'En az 8 karakter'),
  role: z.enum(['admin', 'user']),
})
type FormValues = z.infer<typeof schema>
```

---

## 21. Next.js App Router — İleri Seviye Pattern'lar

### Parallel Routes

```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div className='dashboard-grid'>
      <main>{children}</main>
      <aside>{analytics}</aside>
      <aside>{team}</aside>
    </div>
  )
}

// app/dashboard/@analytics/page.tsx
export default async function AnalyticsSlot() {
  const stats = await getAnalytics()
  return <AnalyticsChart data={stats} />
}

// app/dashboard/@analytics/loading.tsx
export default function AnalyticsLoading() {
  return <ChartSkeleton />
}
```

### Intercepting Routes (Modal Pattern)

```
app/
├── @modal/
│   ├── (.)photos/[id]/page.tsx   ← Intercept
│   └── default.tsx
├── photos/
│   └── [id]/page.tsx             ← Full page
└── layout.tsx
```

```typescript
// app/@modal/(.)photos/[id]/page.tsx
export default async function PhotoModal({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const photo = await getPhoto(id)
  return (
    <Modal>
      <PhotoDetail photo={photo} />
    </Modal>
  )
}
```

### Streaming ile Suspense

```typescript
export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const product = await getProduct(id)  // Blocking — hemen render

  return (
    <div>
      <ProductHeader product={product} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={id} />       {/* Yavaş API — stream */}
      </Suspense>
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations productId={id} /> {/* ML tabanlı — stream */}
      </Suspense>
    </div>
  )
}
```

### searchParams Async Kullanımı (Next.js 15)

```typescript
// ✅ Next.js 15 — async searchParams
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ category?: string; page?: string }>
}) {
  const params = await searchParams
  return <ProductList category={params.category} />
}
```

### generateStaticParams

```typescript
export async function generateStaticParams() {
  const products = await db.product.findMany({ select: { slug: true } })
  return products.map((p) => ({ slug: p.slug }))
}
```

---

## 22. TDD (Test-Driven Development) Metodolojisi

### Temel Kural

```
KESİNLİKLE: Failing test olmadan production kodu yazma
```

Kod yazdıktan sonra test yazmak, testin doğru çalışıp çalışmadığını kanıtlamaz.

### Red-Green-Refactor Döngüsü

```
1. RED    → Failing test yaz (tek davranış)
2. VERIFY → Testin beklenen nedenle fail ettiğini gör
3. GREEN  → Testi geçirecek minimum kod yaz
4. VERIFY → Testin geçtiğini ve diğerlerinin kırılmadığını doğrula
5. REFACTOR → Temizle (test geçerken)
6. TEKRAR
```

### Bug Fix TDD Pattern

```typescript
// 1. Önce bug'ı reproduce eden test yaz
it('boş email kabul etmez', async () => {
  const result = await submitForm({ email: '' })
  expect(result.error).toBe('Email zorunlu')
})

// 2. Testi çalıştır — fail etmeli
// 3. Minimum fix yaz
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email zorunlu' }
  }
}

// 4. Testi çalıştır — pass etmeli
```

### TDD Kuralları (Talent Architect)

- AI-heavy flow'lar için önce mock ile test yaz, gerçek AI çağrısı yerine
- Her route handler için önce error case testini yaz
- Firestore operasyonları için emulator ile test
- 3+ fix denemesi başarısız olursa → mimari sorun, devam etme

### Kırmızı Bayraklar

```
❌ "Bir dene bakalım" yaklaşımı
❌ Test olmadan "manuel doğrularım"
❌ Birden fazla değişiklik aynı anda
❌ Root cause anlamadan fix önerisi
```

---

## 23. Vercel/Next.js Performans Kritik Kuralları

### Waterfall Elimine Etme (KRİTİK)

```typescript
// ❌ Sequential — waterfall
const user = await fetchUser(id)
const orders = await fetchOrders(user.id)
const profile = await fetchProfile(user.id)

// ✅ Parallel — Promise.all
const [user, orders] = await Promise.all([fetchUser(id), fetchOrders(id)])
```

### Bundle Size (KRİTİK)

```typescript
// ❌ Barrel import — tüm bundle'ı çeker
import { Button, Input, Modal } from '@/components'

// ✅ Direct import — tree-shaking çalışır
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
```

```typescript
// ❌ Ağır component her zaman yüklü
import { HeavyChart } from './HeavyChart'

// ✅ Dynamic import — lazy loading
const HeavyChart = dynamic(() => import('./HeavyChart'), { ssr: false })
```

### Re-render Optimizasyonu

```typescript
// ❌ State'e subscribe ama sadece callback'te kullanıyor
const count = useStore((s) => s.count) // Her değişimde re-render
const increment = () => useStore.setState((s) => ({ count: s.count + 1 }))

// ✅ Sadece action, state değil
const increment = useStore((s) => s.increment) // Stabil referans
```

### Statik JSX Hoisting

```typescript
// ❌ Her render'da yeniden oluşturuluyor
export function Nav() {
  const LINKS = [{ href: '/cv', label: 'CV' }, { href: '/ats', label: 'ATS' }]
  return <nav>{LINKS.map(...)}</nav>
}

// ✅ Component dışında — bir kez oluşturuluyor
const LINKS = [{ href: '/cv', label: 'CV' }, { href: '/ats', label: 'ATS' }]
export function Nav() {
  return <nav>{LINKS.map(...)}</nav>
}
```

### React Query — Koşullu Fetch

```typescript
// ❌ id yokken fetch yapıyor
const { data } = useQuery({ queryKey: ['user', id], queryFn: () => fetchUser(id) })

// ✅ enabled flag ile koşullu
const { data } = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id),
  enabled: !!id,
  staleTime: 5 * 60 * 1000,
})
```

---

## 24. Zustand İleri Seviye Pattern'lar

### Slice Kompozisyonu (Büyük Store'lar İçin)

```typescript
// store/slices/createCvSlice.ts
import { StateCreator } from 'zustand'

export interface CvSlice {
  cvList: Cv[]
  selectedCvId: string | null
  selectCv: (id: string) => void
  clearSelection: () => void
}

export const createCvSlice: StateCreator<CvSlice & AtsSlice, [], [], CvSlice> = (set) => ({
  cvList: [],
  selectedCvId: null,
  selectCv: (id) => set({ selectedCvId: id }),
  clearSelection: () => set({ selectedCvId: null }),
})

// store/index.ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { createCvSlice, CvSlice } from './slices/createCvSlice'
import { createAtsSlice, AtsSlice } from './slices/createAtsSlice'

type StoreState = CvSlice & AtsSlice

export const useStore = create<StoreState>()(
  devtools(
    (...args) => ({
      ...createCvSlice(...args),
      ...createAtsSlice(...args),
    }),
    { name: 'talent-architect-store' },
  ),
)
```

### Selective Subscription (Gereksiz Re-render Önleme)

```typescript
// ❌ Tüm store'a subscribe — her değişimde re-render
const { cvList, selectedCvId, selectCv } = useStore()

// ✅ Sadece gerekli slice'a subscribe
const cvList = useStore((s) => s.cvList)
const selectCv = useStore((s) => s.selectCv)
```

### React Query + Zustand Ayrımı

```typescript
// Zustand: UI state (client-only)
const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  activeModal: null,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}))

// React Query: Server state
function Dashboard() {
  const { sidebarOpen } = useUIStore()
  const { data: cvs } = useQuery({
    queryKey: ['cvs', userId],
    queryFn: () => api.get(`/cv/${userId}`),
  })
  // cvs asla Zustand'a kopyalanmaz
}
```

---

## 25. Composition Anti-Pattern'ları — Boolean Prop Proliferation

### Problem: Boolean Props Birikmesi

```typescript
// ❌ Kontrol edilemez hale gelir
<Button
  isPrimary
  isLarge
  isLoading
  hasIcon
  isDisabled
  showBadge
/>

// ❌ Her yeni variant yeni boolean ekler
```

### Çözüm 1: Explicit Variant Component'ler

```typescript
// ✅ Açık variant'lar — API okunabilir
<PrimaryButton size='lg' isLoading icon={<Spinner />} />
<GhostButton size='sm' />
<DestructiveButton />
```

### Çözüm 2: Compound Components

```typescript
// ✅ Context ile state paylaşımı
<Accordion>
  <Accordion.Item id='cv'>
    <Accordion.Trigger>CV Yönetimi</Accordion.Trigger>
    <Accordion.Content>
      <CvList />
    </Accordion.Content>
  </Accordion.Item>
</Accordion>
```

### Çözüm 3: children Over renderX Props

```typescript
// ❌ renderX prop pattern
<Card
  renderHeader={() => <h2>Başlık</h2>}
  renderFooter={() => <Button>Kaydet</Button>}
/>

// ✅ children/slot composition
<Card>
  <Card.Header>Başlık</Card.Header>
  <Card.Body><CvContent /></Card.Body>
  <Card.Footer><Button>Kaydet</Button></Card.Footer>
</Card>
```

### React 19: forwardRef Kaldırıldı

```typescript
// ❌ React 18 — forwardRef zorunluydu
const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, ...props }, ref) => (
    <input ref={ref} {...props} />
  )
)

// ✅ React 19 — ref artık normal prop
function Input({ label, ref, ...props }: InputProps & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />
}
```

### State Decoupling — Provider Pattern

```typescript
// Provider state yönetimini kapsüller — dışarıya interface açar
interface SubscriptionContext {
  state: SubscriptionState
  actions: {
    upgrade: (plan: Plan) => Promise<void>
    cancel: () => Promise<void>
  }
  meta: { isLoading: boolean; error: string | null }
}

// Context yalnızca interface'i bilir, implementasyonu değil
const SubscriptionCtx = createContext<SubscriptionContext | null>(null)

export function SubscriptionProvider({ children }: { children: React.ReactNode }) {
  // Zustand, useState, React Query — provider içinde kapsüllü
  const store = useSubscriptionStore()
  return (
    <SubscriptionCtx.Provider value={store}>
      {children}
    </SubscriptionCtx.Provider>
  )
}
```

### Hoisting Static JSX

```typescript
// ❌ Her render'da yeniden oluşturuluyor
function NavMenu() {
  const ITEMS = [
    { href: '/cv', label: 'CV Builder' },
    { href: '/ats', label: 'ATS Analizi' },
  ]
  return <nav>{ITEMS.map(item => <NavLink key={item.href} {...item} />)}</nav>
}

// ✅ Component dışında — bir kez oluşturuluyor
const NAV_ITEMS = [
  { href: '/cv', label: 'CV Builder' },
  { href: '/ats', label: 'ATS Analizi' },
]

function NavMenu() {
  return <nav>{NAV_ITEMS.map(item => <NavLink key={item.href} {...item} />)}</nav>
}
```

### Ternary vs && Rendering

```typescript
// ❌ && ile sıfır render sorunu
{count && <Badge>{count}</Badge>}  // count=0 ise "0" render eder

// ✅ Ternary her zaman güvenli
{count ? <Badge>{count}</Badge> : null}

// ✅ Boolean explicit cast
{!!count && <Badge>{count}</Badge>}
```

---

## 26. Concurrent Request Batching (AI Endpoint'ler İçin)

AI endpoint'lerinde çok fazla eş zamanlı istek UI'ı dondurabilir.

```typescript
// ❌ Sınırsız concurrent request — UI donabilir
const analyses = await Promise.all(cvIds.map((id) => analyzeCV(id)))

// ✅ Batched execution — max 3 concurrent
async function executeBatched<T>(
  tasks: Array<() => Promise<T>>,
  concurrency = 3,
): Promise<Array<PromiseSettledResult<T>>> {
  const results: Array<PromiseSettledResult<T>> = []
  for (let i = 0; i < tasks.length; i += concurrency) {
    const batch = tasks.slice(i, i + concurrency)
    const batchResults = await Promise.allSettled(batch.map((task) => task()))
    results.push(...batchResults)
  }
  return results
}

// Kullanım — CV batch analizi
const tasks = cvIds.map((id) => () => analyzeCV(id))
const results = await executeBatched(tasks, 3)

const successful = results
  .filter((r) => r.status === 'fulfilled')
  .map((r) => (r as PromiseFulfilledResult<CvAnalysis>).value)
```

### AI Feature Sonrası State Sıfırlama

```typescript
// Ağır işlem bitmeden UI'ı güncelleme
function CvAnalysisButton({ cvId }: { cvId: string }) {
  const [isPending, startTransition] = useTransition()

  const handleAnalyze = () => {
    startTransition(async () => {
      await analyzeCV(cvId)      // Yavaş AI çağrısı
      await refetchAnalysis()     // Cache yenile
    })
  }

  return (
    <Button onClick={handleAnalyze} disabled={isPending}>
      {isPending ? 'Analiz ediliyor...' : 'ATS Analizi'}
    </Button>
  )
}
```

---

## 27. Code Refactoring Metodolojisi

### Refactoring Öncesi Değerlendirme

```
1. Code smell'leri tespit et:
   - 50+ satır fonksiyon → bölümlere ayır
   - 3+ nesting seviyesi → early return
   - Tekrar eden kod blokları → extract function
   - Generic isimler (utils, helper, misc) → domain specific isim ver
   - Tek sorumluluktan fazlası → separate concerns

2. Risk değerlendirmesi:
   - Bu kod test edilmiş mi? (değişiklik güvenli mi?)
   - Kaç yer tarafından kullanılıyor?
   - Breaking change yaratır mı?
```

### İnkremental Refactoring Adımları

```
Faz 1: Davranışı koru
  → Önce test yaz (mevcut davranışı belgele)
  → Sonra refactor et
  → Test geçiyor mu? ✓

Faz 2: Temizle
  → İsimleri düzelt
  → Extract function/component
  → Remove duplication

Faz 3: Yeniden test et
  → Tüm testler geçiyor mu?
  → TypeScript error var mı?
  → i18n key'leri kontrol et
```

### Talent Architect'e Özel Refactoring Kuralları

```typescript
// ❌ Generic naming — kim çağırıyor?
export function handleData(input: any) { ... }
export function processItem(item: unknown) { ... }

// ✅ Domain-specific naming
export function parseCvUploadResponse(raw: unknown): CvDocument { ... }
export function calculateAtsScore(cv: CvDocument, job: JobDescription): AtsResult { ... }
```

```typescript
// ❌ Feature logic lib/server/ altında
// lib/server/services/cvHelper.ts

// ✅ Feature domain'inde
// features/cv/server/cv.service.ts
```

---

## 28. TypeScript İleri Seviye Pattern'lar

### Branded Types (Domain Primitifler)

```typescript
// Primitive obsession'ı önle — aynı tipte farklı domain değerleri karışmasın
type Brand<K, T> = K & { __brand: T }
type UserId = Brand<string, 'UserId'>
type CvId = Brand<string, 'CvId'>
type AtsScore = Brand<number, 'AtsScore'>

// Yanlış parametre sırasını compile-time yakala
function analyzeCV(cvId: CvId, userId: UserId): Promise<AtsScore> { ... }

// Oluşturma
const cvId = 'abc123' as CvId
const score = 87 as AtsScore
```

### Discriminated Union (Error Handling)

```typescript
// Result type — exception yerine explicit error handling
type Result<T, E = Error> = { success: true; data: T } | { success: false; error: E }

async function parseCv(file: File): Promise<Result<CvDocument, 'INVALID_FORMAT' | 'TOO_LARGE'>> {
  if (file.size > MAX_SIZE) return { success: false, error: 'TOO_LARGE' }
  // ...
  return { success: true, data: parsedCv }
}

// Kullanım
const result = await parseCv(file)
if (!result.success) {
  // result.error'ın tipi: 'INVALID_FORMAT' | 'TOO_LARGE'
  handleError(result.error)
} else {
  // result.data'nın tipi: CvDocument
  displayCv(result.data)
}
```

### Conditional Types & Inference

```typescript
// ReturnType utility — var olan fonksiyonun dönüş tipini çıkar
type CvAnalysisResult = Awaited<ReturnType<typeof analyzeCV>>

// Infer ile derinlemesine çıkarım
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T
type ElementType<T> = T extends (infer U)[] ? U : never

// Template literal types
type EventName = 'cv' | 'ats' | 'chat'
type EventHandler = `on${Capitalize<EventName>}Change`
// → 'onCvChange' | 'onAtsChange' | 'onChatChange'
```

### Mapped Types

```typescript
// Tüm property'leri optional yap (Partial dahili yapar bunu)
type PartialCv = Partial<CvDocument>

// Tüm property'leri readonly yap
type ReadonlyCv = Readonly<CvDocument>

// String property'leri filtrele
type StringFields<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K]
}
// StringFields<{ id: string; score: number; name: string }>
// → { id: string; name: string }

// Getter metodları üret
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}
```

### Strict tsconfig (Talent Architect)

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": false,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": false,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "incremental": true
  }
}
```

### Yaygın TypeScript Hata Çözümleri

```typescript
// "The inferred type of X cannot be named"
// → Tipi explicit export et
export type CvAnalysis = Awaited<ReturnType<typeof analyzeCv>>

// "Excessive stack depth comparing types"
// → Type intersection yerine interface extends kullan
// ❌ type Combined = TypeA & TypeB & TypeC
// ✅ interface Combined extends TypeA, TypeB, TypeC {}

// "Type instantiation is excessively deep"
// → Recursion'ı sınırla
type NestedArray<T, D extends number = 5> = D extends 0 ? T : T | NestedArray<T, [-1, 0, 1, 2, 3, 4][D]>[]

// "Cannot find module" hataları
// → tsconfig'de path alias ve baseUrl doğru mu?
// → import style projeyle tutarlı mı? (@/ prefix)
```

### Type-Safe Event Emitter (AI Events için)

```typescript
type CvEvents = {
  'cv:uploaded': { cvId: CvId; userId: UserId }
  'cv:analyzed': { cvId: CvId; score: AtsScore }
  'cv:error': { cvId: CvId; error: string }
}

class TypedEventEmitter<T extends Record<string, unknown>> {
  private listeners: { [K in keyof T]?: Array<(data: T[K]) => void> } = {}

  on<K extends keyof T>(event: K, cb: (data: T[K]) => void) {
    ;(this.listeners[event] ??= []).push(cb)
  }

  emit<K extends keyof T>(event: K, data: T[K]) {
    this.listeners[event]?.forEach((cb) => cb(data))
  }
}

const cvEmitter = new TypedEventEmitter<CvEvents>()
cvEmitter.on('cv:analyzed', ({ cvId, score }) => {
  // Tipler otomatik: cvId: CvId, score: AtsScore
})
```

---

## 29. React Event Typing İleri Seviye

### Spesifik Event Tipleri

```typescript
// Mouse
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  e.currentTarget.disabled = true
}

// Form submit
function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault()
  const formData = new FormData(e.currentTarget)
  const email = formData.get('email') as string
}

// Input change
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  setValue(e.target.value)
}

// Keyboard
function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
  if (e.key === 'Enter') e.currentTarget.blur()
}

// Textarea
function handleTextarea(e: React.ChangeEvent<HTMLTextAreaElement>) {
  setDescription(e.target.value)
}
```

### Generic Component Pattern'lar

```typescript
// Tablo — keyof T ile column key type safety
type Column<T> = {
  key: keyof T
  header: string
  render?: (value: T[keyof T], item: T) => React.ReactNode
}

type TableProps<T extends { id: string | number }> = {
  data: T[]
  columns: Column<T>[]
}

function Table<T extends { id: string | number }>({ data, columns }: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={String(col.key)}>{col.header}</th>)}</tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={item.id}>
            {columns.map(col => (
              <td key={String(col.key)}>
                {col.render ? col.render(item[col.key], item) : String(item[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

// Kullanım — T otomatik CvDocument'a infer edilir
<Table<CvDocument>
  data={cvList}
  columns={[
    { key: 'title', header: 'Başlık' },
    { key: 'score', header: 'ATS Skoru', render: (v) => <ScoreBadge score={v as number} /> },
  ]}
/>
```

### useState İçin Explicit Typing

```typescript
// Primitive tip — inference yeterli
const [count, setCount] = useState(0)

// Union/null — explicit gerekli
const [user, setUser] = useState<User | null>(null)
const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')

// DOM ref — null başlangıç değeri zorunlu
const inputRef = useRef<HTMLInputElement>(null)
// inputRef.current?.focus()  ← null check gerekli

// Mutable değer — null değil
const counterRef = useRef<number>(0)
// counterRef.current++  ← doğrudan erişim
```

### Custom Hook — Tuple Return

```typescript
// as const olmadan tip [boolean, () => void] yerine (boolean | (() => void))[]
function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial)
  const toggle = useCallback(() => setValue((v) => !v), [])
  return [value, toggle] as const
}

// Kullanım
const [isOpen, toggleOpen] = useToggle()
```

### useReducer — Discriminated Action

```typescript
type CvState = {
  cvList: CvDocument[]
  selected: CvId | null
  status: 'idle' | 'loading' | 'error'
}

type CvAction =
  | { type: 'SET_LIST'; payload: CvDocument[] }
  | { type: 'SELECT'; payload: CvId }
  | { type: 'CLEAR_SELECTION' }
  | { type: 'SET_STATUS'; payload: CvState['status'] }

function cvReducer(state: CvState, action: CvAction): CvState {
  switch (action.type) {
    case 'SET_LIST':
      return { ...state, cvList: action.payload }
    case 'SELECT':
      return { ...state, selected: action.payload }
    case 'CLEAR_SELECTION':
      return { ...state, selected: null }
    case 'SET_STATUS':
      return { ...state, status: action.payload }
    default: {
      // Exhaustive check — yeni action eklenirse compile error
      const _: never = action
      return state
    }
  }
}
```

---

## 30. Zustand 5 — Güncel Pattern'lar

### useShallow ile Selective Subscription (Zustand 5 Zorunlu)

```typescript
// ✅ Zustand 5'te birden fazla alan için useShallow kullan
import { useShallow } from 'zustand/react/shallow'

function UserInfo() {
  const { name, email } = useUserStore(
    useShallow(state => ({ name: state.name, email: state.email }))
  )
  return <div>{name} - {email}</div>
}

// ❌ Tüm store'u al — her state değişiminde re-render
const store = useUserStore()
```

### Persist Middleware

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface SettingsStore {
  theme: 'light' | 'dark'
  language: string
  setTheme: (theme: 'light' | 'dark') => void
  setLanguage: (language: string) => void
}

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'tr',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'ta-settings-storage', // localStorage key
    },
  ),
)
```

### Immer Middleware (Nested State İçin)

```typescript
import { immer } from 'zustand/middleware/immer'

interface CvStore {
  cvList: CvDocument[]
  addCv: (cv: CvDocument) => void
  updateCvTitle: (id: string, title: string) => void
}

const useCvStore = create<CvStore>()(
  immer((set) => ({
    cvList: [],
    addCv: (cv) =>
      set((state) => {
        state.cvList.push(cv)
      }),
    updateCvTitle: (id, title) =>
      set((state) => {
        const cv = state.cvList.find((c) => c.id === id)
        if (cv) cv.title = title
      }),
  })),
)
```

### DevTools + Persist Kombinasyonu

```typescript
import { devtools, persist } from 'zustand/middleware'

const useStore = create<Store>()(
  devtools(
    persist(
      (set) => ({
        /* store definition */
      }),
      { name: 'ta-store' },
    ),
    { name: 'TalentArchitectStore' },
  ),
)
```

### Outside React (Programmatic Erişim)

```typescript
// Component dışında store'a doğrudan erişim
const { user, setUser } = useAuthStore.getState()

// Değişiklikleri dinle
const unsubscribe = useAuthStore.subscribe((state) => console.log('Auth state changed:', state.user?.email))

// Cleanup
unsubscribe()
```

---

## 31. Test Factory Pattern ve Mock Stratejileri

### Factory Pattern (Test Data)

```typescript
// ✅ getMock{X} factory fonksiyonları — DRY test data
interface CvDocument {
  id: string
  userId: string
  title: string
  score: number
  createdAt: Date
}

function getMockCvDocument(overrides?: Partial<CvDocument>): CvDocument {
  return {
    id: 'cv-test-123',
    userId: 'user-test-456',
    title: 'Test CV',
    score: 75,
    createdAt: new Date('2024-01-01'),
    ...overrides,
  }
}

// Kullanım
it('should display ATS score', () => {
  const cv = getMockCvDocument({ score: 90 })
  render(<CvCard cv={cv} />)
  expect(screen.getByText('90')).toBeInTheDocument()
})
```

### Props Factory

```typescript
import { ComponentProps } from 'react'

function getMockCvCardProps(overrides?: Partial<ComponentProps<typeof CvCard>>) {
  return {
    cv: getMockCvDocument(),
    onAnalyze: jest.fn(),
    onDelete: jest.fn(),
    isLoading: false,
    ...overrides,
  }
}
```

### AI Service Mock Pattern

```typescript
// AI servislerini wrapper seviyesinde mock'la
jest.mock('@/lib/server/ai/anthropic', () => ({
  generateCompletion: jest.fn().mockResolvedValue({
    content: 'Mock AI yanıtı',
    usage: { input_tokens: 10, output_tokens: 20 },
  }),
}))

// Test içinde değişken davranış
const mockGenerate = jest.requireMock('@/lib/server/ai/anthropic').generateCompletion
mockGenerate.mockResolvedValueOnce({ content: 'Hata durumu yanıtı' })
```

### Test Yapısı Standardı

```typescript
describe('CvAnalysisService', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('analyzeAts()', () => {
    it('should return score when CV and job description provided', async () => {
      // Arrange
      const cv = getMockCvDocument()
      const jobDesc = 'Senior TypeScript Developer...'

      // Act
      const result = await analyzeAts(cv, jobDesc)

      // Assert
      expect(result.score).toBeGreaterThan(0)
      expect(result.score).toBeLessThanOrEqual(100)
    })

    it('should throw when CV is empty', async () => {
      const emptyCv = getMockCvDocument({ title: '' })
      await expect(analyzeAts(emptyCv, 'job')).rejects.toThrow('CV içeriği boş')
    })
  })
})
```

### Anti-Pattern: Mock Davranışı Test Etme

```typescript
// ❌ Mock'un çağrıldığını test etmek — gerçek davranışı test etmiyor
expect(mockFetchCv).toHaveBeenCalled()

// ✅ Gerçek çıktıyı test et
expect(screen.getByText('CV başarıyla yüklendi')).toBeInTheDocument()
```

---

## 32. React/Next.js Performans Kural Seti

### Bundle Optimizasyonu (KRİTİK)

```typescript
// ❌ Barrel import — tüm bundle'ı çeker
import { Button, Input, Modal, Card } from '@/components'

// ✅ Direct import — tree-shaking
import { Button } from '@/components/ui/button'

// ❌ Her zaman yüklü
import { HeavyChart } from './HeavyChart'

// ✅ Lazy load — conditional
const HeavyChart = dynamic(() => import('./HeavyChart'), { ssr: false })
```

### Re-render Önleme (YÜKSEK)

```typescript
// ✅ Functional setState — stale closure önler
setCount((prev) => prev + 1)

// ✅ Lazy state init — pahalı hesaplama bir kez çalışır
const [state, setState] = useState(() => expensiveInitialState())

// ✅ useTransition — non-urgent update için
const [isPending, startTransition] = useTransition()
startTransition(() => setFilteredResults(heavy()))

// ✅ Module-level cache — her render'da yeniden hesaplamayı önle
const cache = new Map<string, AtsResult>()
function getCachedAtsScore(key: string) {
  if (cache.has(key)) return cache.get(key)!
  const result = computeExpensiveScore(key)
  cache.set(key, result)
  return result
}
```

### Async Pattern (ORTA)

```typescript
// ❌ Sequential — waterfall oluşturur
const cv = await fetchCv(id)
const jobs = await fetchJobs(cv.userId)
const stats = await fetchStats(cv.userId)

// ✅ Parallel — Promise.all ile
const [cv, jobs, stats] = await Promise.all([fetchCv(id), fetchJobs(userId), fetchStats(userId)])
```

### JavaScript Optimizasyonu (ORTA)

```typescript
// ❌ Tekrarlanan array lookup — O(n) her seferinde
const match = cvList.find((cv) => cv.id === targetId)

// ✅ Map ile O(1) lookup
const cvMap = new Map(cvList.map((cv) => [cv.id, cv]))
const match = cvMap.get(targetId)

// ✅ Immutable sort
const sorted = cvList.toSorted((a, b) => b.score - a.score) // toSorted ile mutasyon yok
```

---

## 33. TypeScript Kod Kalitesi Kuralları

### Import Organizasyonu

```typescript
// ✅ Sıralama: external → internal → relative
import { z } from 'zod' // external
import { NextResponse } from 'next/server' // external framework
import { prisma } from '@/lib/db' // internal absolute
import { requireAuth } from '@/lib/server/auth' // internal absolute
import { CvDocument } from '../types' // relative

// ✅ Type-only import — tree-shaking için
import type { CvDocument } from './types'
import type { Metadata } from 'next'
```

### Named Export Kuralı

```typescript
// ❌ Default export — barrel export ile uyumlu değil
export default function CvCard() { ... }

// ✅ Named export — her zaman
export function CvCard() { ... }
export type { CvCardProps }
```

### No `any` — `unknown` + Type Guard Kullan

```typescript
// ❌ any
function parseApiResponse(data: any) {
  return data.score
}

// ✅ unknown + type guard
function parseApiResponse(data: unknown): number {
  if (
    typeof data === 'object' &&
    data !== null &&
    'score' in data &&
    typeof (data as { score: unknown }).score === 'number'
  ) {
    return (data as { score: number }).score
  }
  throw new Error('Invalid API response shape')
}
```

### `satisfies` ile Tip Doğrulama

```typescript
// ✅ satisfies — tipi kontrol et, literal inference'ı koru
const apiConfig = {
  baseUrl: 'https://api.talent-architect.com',
  timeout: 5000,
  retries: 3,
} satisfies Record<string, string | number>

// apiConfig.baseUrl tipi: string (değil string | number)
```

### TanStack Query Key Factory

```typescript
// ✅ Type-safe query key factory — Talent Architect pattern
export const cvKeys = {
  all: ['cvs'] as const,
  lists: () => [...cvKeys.all, 'list'] as const,
  list: (filters: CvFilters) => [...cvKeys.lists(), filters] as const,
  details: () => [...cvKeys.all, 'detail'] as const,
  detail: (id: string) => [...cvKeys.details(), id] as const,
}

// Kullanım
const { data } = useQuery({
  queryKey: cvKeys.detail(cvId),
  queryFn: () => api.get(`/cv/${cvId}`),
  enabled: !!cvId,
})

// Invalidation
queryClient.invalidateQueries({ queryKey: cvKeys.lists() })
```

### Custom Error Class

```typescript
// ✅ Typed, stacktrace korumalı error class
export class CvServiceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
  ) {
    super(message)
    this.name = 'CvServiceError'
    Error.captureStackTrace(this, this.constructor)
  }
}

// Kullanım
throw new CvServiceError('CV bulunamadı', 'CV_NOT_FOUND', 404)
```

---

## 34. Modern JavaScript/TypeScript Pattern'ları

### Destructuring ve Default Values

```typescript
// Object destructuring ile default
function createCvConfig({ title = 'Yeni CV', template = 'modern', language = 'tr', ...rest }: Partial<CvConfig> = {}) {
  return { title, template, language, ...rest }
}

// Array destructuring
const [first, second, ...remaining] = cvList
const [primarySkill, ...otherSkills] = skills
```

### Optional Chaining ve Nullish Coalescing

```typescript
// ❌ Verbose null check zinciri
const score = user && user.cv && user.cv.atsScore ? user.cv.atsScore : 0

// ✅ Modern — kısa ve güvenli
const score = user?.cv?.atsScore ?? 0

// ✅ Method call ile
const firstName = session?.user?.name?.split(' ').at(0) ?? 'Kullanıcı'
```

### Functional Pipeline — Array Transformation

```typescript
// Tek geçişte filter + map + sort (chaining)
const topCvs = cvList
  .filter((cv) => cv.score >= 70)
  .map((cv) => ({ ...cv, grade: cv.score >= 90 ? 'A' : 'B' }))
  .toSorted((a, b) => b.score - a.score)
  .slice(0, 5)

// Object.groupBy ile gruplama (ES2024)
const grouped = Object.groupBy(cvList, (cv) =>
  cv.score >= 90 ? 'excellent' : cv.score >= 70 ? 'good' : 'needs-improvement',
)
```

### Immutable Update Patterns

```typescript
// Object spread — nested update
const updatedCv = {
  ...cv,
  metadata: {
    ...cv.metadata,
    updatedAt: new Date(),
    version: cv.metadata.version + 1,
  },
}

// Array immutable operations
const withNew = [...cvList, newCv] // ekle
const withoutDeleted = cvList.filter((cv) => cv.id !== id) // sil
const updated = cvList.map((cv) => (cv.id === id ? newCv : cv)) // güncelle
```

### Async Pattern'lar

```typescript
// ✅ Promise.allSettled — kısmi hata toleransı
const results = await Promise.allSettled([
  analyzeAts(cv, jobDesc),
  generateCoverLetter(cv),
  fetchCompanyInfo(companyName),
])

const successful = results
  .filter((r): r is PromiseFulfilledResult<unknown> => r.status === 'fulfilled')
  .map((r) => r.value)

const failed = results.filter((r): r is PromiseRejectedResult => r.status === 'rejected').map((r) => r.reason)

// ✅ Race condition önleme
let latestRequestId = 0
async function searchJobs(query: string) {
  const requestId = ++latestRequestId
  const results = await fetchJobs(query)
  if (requestId !== latestRequestId) return // Eski request — yoksay
  setResults(results)
}
```

### Weak References — Memory Management

```typescript
// WeakMap — DOM element veya nesneyle ilişkilendirilmiş veri
const cvMetaCache = new WeakMap<CvDocument, CvMeta>()

function getCvMeta(cv: CvDocument): CvMeta {
  if (cvMetaCache.has(cv)) return cvMetaCache.get(cv)!
  const meta = computeMeta(cv)
  cvMetaCache.set(cv, meta)
  return meta
}
// cv nesnesi garbage collect edilince cache otomatik temizlenir
```

---

## 35. Test Hata Düzeltme Metodolojisi

Failing test sayısının fazla olduğu durumlarda sistematik yaklaşım:

### 1. Tüm Hataları Topla

```bash
npm test -- --passWithNoTests 2>&1 | tee /tmp/test-failures.txt
```

### 2. Hataları Grupla (Infrastructure First)

Öncelik sırası:

1. **Import/Module hataları** — en çok testi etkiler, önce çöz
2. **Configuration/Environment** — test ortamı kurulumu
3. **API/Interface değişiklikleri** — fonksiyon imzası, tip değişimi
4. **Logic hataları** — assertion failure, iş mantığı

```bash
# Hata tiplerini say
grep -E "Error:|Cannot find" /tmp/test-failures.txt | sort | uniq -c | sort -rn
```

### 3. Grup Başına Fix Stratejisi

```
Her grup için:
  1. Root cause'u belirle — git diff ile son değişiklikleri kontrol et
  2. Minimum değişiklik yap — tek bir konuya odaklan
  3. Sadece o grubun testlerini çalıştır
     → npm test -- --testPathPattern="specific-file"
     → jest -k "pattern"
  4. Grup tamamen geçince → bir sonraki gruba geç
```

### 4. Anti-Pattern: Toplu Fix

```typescript
// ❌ Birden fazla değişikliği aynı anda uygulama
// → Hangi değişikliğin hangi testi geçirdiği belirsizleşir

// ✅ Tek seferde bir grup — verify — sonraki
```

### 5. Regresyon Kontrolü

Tüm gruplar geçtikten sonra:

```bash
npm test  # Tam suite — regresyon yok mu kontrol et
```

---

## 36. Vercel Deployment Stratejisi

### Environment Variable Yönetimi

```bash
# Vercel'de üç environment seviyesi
vercel env add ANTHROPIC_API_KEY production
vercel env add ANTHROPIC_API_KEY preview
vercel env add ANTHROPIC_API_KEY development

# ASLA client-side'a sızdırma
ANTHROPIC_API_KEY=...       # ✅ Sunucu-only
NEXT_PUBLIC_SITE_URL=...    # ✅ Public değer — istemci görebilir
NEXT_PUBLIC_API_KEY=...     # ❌ Secret kesinlikle NEXT_PUBLIC_ olmamalı
```

### Edge vs Serverless Seçimi

```typescript
// Edge Runtime — Tercih koşulları:
// - Middleware (auth check, redirect, A/B test)
// - Basit response transformation
// - Coğrafi routing
export const runtime = 'edge' // middleware.ts içinde

// Serverless (Node.js) — Tercih koşulları:
// - Firebase Admin SDK (Node.js gerektiriyor)
// - pdfkit, pdfjs-dist
// - Anthropic SDK
// - Ağır CPU işlemleri
// Talent Architect'te API route'lar için varsayılan: Serverless
```

### Build Optimizasyonu

```typescript
// next.config.mjs — Talent Architect mevcut konfigürasyon üzerine
const nextConfig = {
  // Bundle analizi için (dev'de)
  // ANALYZE=true npm run build → bundle boyutunu gör

  // Server external packages — bundle'a dahil etme
  serverExternalPackages: ['pdfkit', 'pdfjs-dist'],

  // Optimized imports (mevcut listede olanlar)
  experimental: {
    optimizePackageImports: ['lucide-react', 'framer-motion', '@radix-ui/react-dialog'],
  },
}
```

### Vercel Sharp Edges (Kritik Uyarılar)

| Risk                              | Seviye | Çözüm                                                |
| --------------------------------- | ------ | ---------------------------------------------------- |
| `NEXT_PUBLIC_` prefix'li secret   | KRİTİK | Yalnızca gerçekten public değerler için kullan       |
| Preview deploy → production DB    | YÜKSEK | Her environment için ayrı Firebase project           |
| Serverless function boyutu >50MB  | YÜKSEK | `serverExternalPackages` ile bundle dışında tut      |
| Edge runtime'da Node.js API       | YÜKSEK | Firebase Admin, pdfkit → Serverless kullan           |
| Function timeout (varsayılan 10s) | ORTA   | AI çağrıları için `maxDuration` artır (Pro: 300s)    |
| Build'de env var okuma zamanı     | ORTA   | `NEXT_PUBLIC_` build'de, diğerleri runtime'da okunur |

```typescript
// AI route'larda timeout artırma
export const maxDuration = 60 // saniye — Pro plan: 300s
```

### Preview vs Production Kontrolü

```typescript
// Ortama göre farklı davranış
const isProduction = process.env.VERCEL_ENV === 'production'
const isPreview = process.env.VERCEL_ENV === 'preview'

// Preview'da monitoring'i hafiflet
if (!isProduction) {
  console.log('Preview mode — monitoring disabled')
}
```

---

## 37. UI State Management — Loading, Error, Empty, Optimistic

### Altın Kural: Loading Gösterme Koşulu

```typescript
// ❌ Cached data varken spinner gösterir — gereksiz flash
if (loading) return <Spinner />

// ✅ Yalnızca data yokken loading göster
const { data, isLoading, error, refetch } = useQuery(...)

if (error) return <ErrorState error={error} onRetry={refetch} />
if (isLoading && !data) return <CvListSkeleton />
if (!data?.items.length) return <EmptyState />
return <CvList items={data.items} />
```

### Loading State Karar Ağacı

```
Hata var mı?
  → Evet: Error state + retry butonu
  → Hayır: devam

Loading VE data yok mu?
  → Evet: Skeleton veya spinner
  → Hayır: devam

Data var mı?
  → Evet, dolu: İçeriği göster
  → Evet, boş: Empty state
  → Hayır: Loading (fallback)
```

### Skeleton vs Spinner

| Skeleton Kullan                    | Spinner Kullan                 |
| ---------------------------------- | ------------------------------ |
| Bilinen içerik şekli (liste, kart) | Bilinmeyen içerik şekli        |
| İlk sayfa yüklemesi                | Modal aksiyonları              |
| CV listesi, profil kartı           | Buton submit, inline operasyon |

### Error State Pattern

```typescript
interface ErrorStateProps {
  error: Error
  onRetry?: () => void
  title?: string
}

function ErrorState({ error, onRetry, title }: ErrorStateProps) {
  return (
    <div role='alert' className='flex flex-col items-center gap-3 py-8'>
      <AlertCircle className='text-destructive' size={32} />
      <p className='font-medium'>{title ?? 'Bir şeyler ters gitti'}</p>
      <p className='text-sm text-muted-foreground'>{error.message}</p>
      {onRetry && (
        <Button variant='outline' onClick={onRetry}>
          Tekrar Dene
        </Button>
      )}
    </div>
  )
}
```

### Empty State Pattern

```typescript
// Her liste için zorunlu — hiçbir zaman atlanmaz
function CvList({ items }: { items: CvDocument[] }) {
  if (!items.length) {
    return (
      <EmptyState
        icon={<FileText size={40} className='text-muted-foreground' />}
        title='Henüz CV yok'
        description='İlk CV\'ni oluşturmak için aşağıdaki butona tıkla.'
        action={{ label: 'CV Oluştur', onClick: handleCreate }}
      />
    )
  }
  return <ul>{items.map(cv => <CvCard key={cv.id} cv={cv} />)}</ul>
}
```

### Buton State Zorunluluğu

```typescript
// ❌ Çift submit riski — kullanıcı birden fazla kez tıklayabilir
<Button onClick={handleSubmit}>Analizi Başlat</Button>

// ✅ Loading sırasında disabled + görsel geri bildirim
<Button
  onClick={handleSubmit}
  disabled={isSubmitting}
>
  {isSubmitting ? (
    <><Loader2 className='animate-spin mr-2' size={16} /> Analiz ediliyor...</>
  ) : (
    'Analizi Başlat'
  )}
</Button>
```

### Optimistic Update Pattern

```typescript
// React Query ile optimistic update
const mutation = useMutation({
  mutationFn: (cvId: string) => api.delete(`/cv/${cvId}`),

  onMutate: async (cvId) => {
    await queryClient.cancelQueries({ queryKey: cvKeys.lists() })
    const previousCvs = queryClient.getQueryData(cvKeys.lists())

    // UI'ı anında güncelle
    queryClient.setQueryData(cvKeys.lists(), (old: CvDocument[]) => old.filter((cv) => cv.id !== cvId))

    return { previousCvs }
  },

  onError: (_err, _cvId, context) => {
    // Hata durumunda geri al
    queryClient.setQueryData(cvKeys.lists(), context?.previousCvs)
    toast.error('CV silinemedi. Tekrar deneyin.')
  },

  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: cvKeys.lists() })
  },
})
```

### Anti-Pattern: Error'ı Yutma

```typescript
// ❌ Kullanıcı hiçbir şey görmez
onError: (error) => {
  console.log(error)
}

// ✅ Her zaman kullanıcıya bildir
onError: (error) => {
  console.error('[CvDelete]', error)
  toast.error('CV silinemedi. Lütfen tekrar deneyin.')
}
```
