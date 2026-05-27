---
name: chatbot-multilingual
description: Architecture for locale-routed chatbot system prompts and per-locale context files in this portfolio. Use when modifying src/app/api/chat/route.ts, when the chatbot is producing off-register or wrong-language replies, when adding a new locale to the chatbot, when authoring or translating src/content/chatbot-context*.md files, or when debugging why the chatbot "sounds English" in non-EN locales.
---

# Chatbot Multilingual Architecture (Portfolio-Specific)

## When to invoke

- Touching `src/app/api/chat/route.ts`.
- Touching `src/components/chat/chat-widget.tsx` locale-handling.
- Touching `src/content/chatbot-context*.md`.
- Adding or reviewing a new locale's chatbot behavior.
- Debugging reports like "the chatbot replied in English when I asked in Arabic" or "the tone feels wrong in Spanish."

## Architecture in one diagram

```
ChatWidget (client)
  │  locale from useLocale()
  │  messages from useState
  ▼
POST /api/chat
  body: { messages, locale }  ← locale is NEW (was missing)
  │
  ▼
route.ts
  ├─ validateLocale(locale) → fallback to 'en' if missing/invalid
  ├─ loadLocaleContext(locale) → reads src/content/chatbot-context.{locale}.md (fallback EN)
  ├─ buildSystemPrompt(locale, context) → locale-routed preamble + persona + context
  ├─ streamText(model, systemPrompt, messages) → model response
  ▼
streamed response back to client
```

## System prompt structure per locale

Every locale gets the same five-section system prompt, with the content per section varying by locale.

### Section 1 — Persona (uniform brand voice, locale-specific realization)

Example for AR:
> أنت مساعد رئبال الشخصي. نبرتك: عصرية، مباشرة، ودودة، لكن مهنية ومتمكنة. تتحدث بالعربية الفصحى الحديثة بمفردات الأعمال الخليجية. لا تستخدم اللهجات. لا تستخدم الفصحى الكلاسيكية الأدبية.

Example for ES:
> Eres el asistente personal de Reebal. Tu tono es moderno, directo, amigable, pero profesional y competente. Hablas en español de España, con calidez andaluza en el fraseo cuando encaja. Usas "tú", nunca "usted" (salvo que el usuario lo use primero).

Example for DE:
> Du bist Reebals persönlicher Assistent. Dein Ton ist modern, direkt, freundlich, aber professionell und kompetent. Du sprichst Deutsch, Du-Form mit großem D (Du, Dir, Dich). Keine Siezen-Form, es sei denn der Nutzer siezt Dich zuerst.

### Section 2 — Grounding rules (uniform content, translated)

> Respond only based on the provided context about Reebal. If a question is not covered by the context, say so clearly and suggest the visitor contact Reebal directly. Do not fabricate specifics.

### Section 3 — Language handling

> Respond in the same language the user wrote in. If the user mixes two languages in one message, respond primarily in [current locale] and briefly acknowledge the other-language phrase. Do not translate the user's message back to them unless they ask.

### Section 4 — Context (from the locale-specific context file)

```
<context>
{{ contents of src/content/chatbot-context.{locale}.md }}
</context>
```

### Section 5 — Scope guard

> Only answer questions about Reebal (background, projects, skills, availability, relocation, contact). For general programming questions, AI industry opinions, or unrelated topics, gently redirect to Reebal's actual areas.

## The `locale` parameter — wiring it through

### Frontend (ChatWidget)

```typescript
// src/components/chat/chat-widget.tsx
import { useLocale } from 'next-intl';

const locale = useLocale();

// In the POST body:
body: JSON.stringify({ messages: sanitized, locale }),
```

### API (route.ts)

```typescript
// src/app/api/chat/route.ts
const { messages, locale } = await req.json();
const validLocale = ['en', 'de', 'es', 'ar'].includes(locale) ? locale : 'en';
const context = await loadLocaleContext(validLocale);
const systemPrompt = buildSystemPrompt(validLocale, context);
```

### loadLocaleContext

```typescript
async function loadLocaleContext(locale: string): Promise<string> {
  const primary = path.join(process.cwd(), 'src/content', `chatbot-context.${locale}.md`);
  const fallback = path.join(process.cwd(), 'src/content', 'chatbot-context.md');
  try {
    return await fs.promises.readFile(primary, 'utf-8');
  } catch {
    return await fs.promises.readFile(fallback, 'utf-8');
  }
}
```

## Per-locale context files

Structure:
- `src/content/chatbot-context.md` — EN (source of truth for content; always exists).
- `src/content/chatbot-context.de.md` — DE transcreation.
- `src/content/chatbot-context.es.md` — ES transcreation.
- `src/content/chatbot-context.ar.md` — AR transcreation.

Rules for the translated context files:
1. Content structure (headings, section order) matches EN exactly.
2. Locked glossary terms (brand, tech, job titles) render per `glossary-brandbook`.
3. Factual claims (years, metrics, project counts) match EN exactly.
4. Narrative paragraphs (bio, strengths) go through deep transcreation per `tone-routing` About-row rules.
5. Each file has a `<!-- last-synced: YYYY-MM-DD from chatbot-context.md -->` HTML comment at the top to track drift.

## Scope guard behavior

If the user asks something out-of-scope, the bot's response (in the user's language) should:

1. Acknowledge the question briefly.
2. Say that its scope is only Reebal's profile.
3. Redirect: "For that topic, I'd suggest [general resource / talking to Reebal directly]."

Example in Arabic:
> سؤال جيد، لكن مجالي محدود بمعلومات رئبال (خلفيته، مشاريعه، مهاراته). بالنسبة لهذا الموضوع، الأفضل أن تسأل رئبال مباشرة أو تبحث في مصادر مختصة.

## Anti-patterns

- Don't send a single EN system prompt with an instruction "respond in the user's language." The model will respond in the right language but with EN-register semantics — which is the current failure mode.
- Don't use `gpt-4o-mini` as the runtime model and expect it to do HIGH-QUALITY transcreation — it's fine for mid-register conversation with a well-built system prompt, but it can't compensate for a prompt that itself ignores locale.
- Don't leak internal routing decisions into the user-facing response ("Since you're in locale 'ar', I'll respond in Arabic" — never say this).
- Don't let the context file drift from the EN source. If you update the EN context, run a drift check against all locale copies and regenerate (or at minimum flag) the outdated ones.

## Integration

This skill pairs with:
- `tone-routing` skill — the Chatbot row defines the per-locale register.
- `glossary-brandbook` skill — enforces locked terms across context files.
- `transcreation-audit` skill — audit the context files after regeneration.

## Testing

After any change to locale routing or system prompts:
1. Manual: open each of /en, /de, /es, /ar in the browser, ask 3 sample questions (simple factual, nuanced opinion, out-of-scope). Verify language, register, scope guard behavior.
2. For AR: additionally verify RTL rendering of markdown lists and code blocks in the streaming response.
3. Log + inspect the first few `system` messages at runtime to confirm the per-locale prompt structure is being built correctly.
