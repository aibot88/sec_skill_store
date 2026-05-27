---
name: braintrust-trace-analysis
description: Analyze recent Braintrust traces from the Elçi AI Odoo agent. Use when the user asks to "analyze traces", "review last N runs", "check trace comments", or wants prompt/agent improvement evidence from real runs. Fetches trace metadata, per-step user/assistant/tool messages (excluding the repeated system prompt in each step to save context), span-level comments, and — most importantly — the `metadata.eval` Human Review note which is the user's authoritative evaluation of the trace.
---

# Braintrust Trace Analysis

Bu skill Elçi AI agent'ın Braintrust'a loglanan Odoo run trace'lerini analiz eder. Amaç: prompt mühendisliği ve agent mimari iyileştirmeleri için gerçek run verisinden kanıt çıkarmak.

## When to use

Tetikleyici ifadeler:
- "son N trace'i analiz et"
- "Braintrust loglarına bak"
- "trace yorumlarını oku"
- "prompt iyileştirme için trace incele"
- "son run'larda ne ters gitti"

## Hardcoded references — DO NOT search for these

| Field | Value |
|---|---|
| Braintrust project name | `browser-agent` (NOT `elci-ai` — `BRAINTRUST_PROJECT` env override aktif) |
| Braintrust project ID | `158d767d-faf1-4a17-a39d-baf59e7877f6` |
| Root span name | `elci-agent-execute` (type `task`) |
| Step span name pattern | `step-{N}` (type `llm`) |
| Tracing source code | `packages/server/src/agent/braintrustTracing.ts` |
| Agent loop source | `packages/server/src/agent/ElciAgentLoop.ts` |
| **System prompt source** | `packages/server/src/agent/prompts/elciSystemPrompt.ts` |

> **Context-saving rule (iki ayrı kural):**
>
> 1. **Step span'larındaki system messages'ları okuma.** Her step'in `input.messages[0]` slotunda system prompt'un **tam** kopyası vardır ve 20 step × 3KB = ~60KB boşuna context harcar. Step data çekerken bunları **tamamen atla** (Step 3 filtresi bunu zorunlu kılar).
>
> 2. **`elciSystemPrompt.ts` dosyasını okuma izni VAR** — fakat **zamanlama kritik:** önce step data'yı çek ve failure mode'ları belirle, SONRA eğer analiz gerçekten prompt'un içeriğine bağlıysa (örn. "system prompt'taki X kuralı yeterince net mi?", "Y davranışı prompt'tan mı kaynaklanıyor?") o zaman `elciSystemPrompt.ts`'yi Read et. Peşinen okuma — çoğu trace analizi prompt içeriğine bakmadan sonuca varabilir.

## Workflow

### Step 1 — Fetch last N traces (root spans)

`mcp__braintrust__sql_query` çağır:
- `object_type`: `project_logs`
- `object_ids`: `["158d767d-faf1-4a17-a39d-baf59e7877f6"]`
- `shape`: `summary`
- `select`: `id, span_id, root_span_id, input, output, metrics, scores, metadata, created`
- `where`: `span_attributes.name = 'elci-agent-execute'`
- `order_by`: `created DESC`
- `preview_length`: `-1` (metadata.eval için tam metin gerekli)
- `limit`: N (kullanıcı istediği sayı, default 5)

Her satırdan çıkarılacak metadata:
- `input.task` → kullanıcı task'ı (Türkçe komut)
- `input.model` → kullanılan LLM (örn. `google/gemini-3-flash-preview`)
- `input.maxSteps` → step bütçesi
- `metrics.llm_calls` → toplam step sayısı
- `metrics.total_tokens`, `metrics.prompt_tokens`, `metrics.completion_tokens`
- `metrics.estimated_cost` (USD)
- `metrics.duration` (saniye)
- `scores.success` (0 veya 1), `scores.stepCount`
- `output.message`, `output.finalPageUrl`
- **`metadata.eval` → human review notu (bkz. Step 4)**
- `created`, `root_span_id` (Step 2'de kullanılacak)

### Step 2 — Per-trace step spans

Her root_span_id için ayrı sorgu:
- `object_type`: `project_logs`
- `object_ids`: `["158d767d-faf1-4a17-a39d-baf59e7877f6"]`
- `shape`: `spans`
- `select`: `span_id, span_attributes, input, output, metrics, metadata, comments`
- `where`: `root_span_id = '<root_span_id>' AND span_attributes.type = 'llm'`
- `order_by`: `metadata.stepIndex ASC`
- `preview_length`: `-1` (tam içerik gerekli — sadece bu sorguda kullan, summary'de KULLANMA)
- `limit`: 100

### Step 3 — Filter messages (CONTEXT GUARD — critical)

Her step span'ının `input.messages` dizisinde her bir mesaj için:

| Role | Action |
|---|---|
| `system` | **TAMAMEN ATLA.** Okuma, özetleme, render etme. |
| `user` | İçeriği koru |
| `assistant` | `content` + `tool_calls[*].function.name` + `tool_calls[*].function.arguments` koru |
| `tool` | `tool_call_id` + `content` koru (tool result'u) |

`output` alanından koru: `text`, `finishReason`, `toolCalls`, `toolResults`.

DOM snapshot'ları gibi büyük tool result'ları **500 char ile truncate** et. Kullanıcı tam içerik isterse ayrıca sorgula.

### Step 4 — Collect human review (iki kaynak)

**Kaynak A — `metadata.eval` (BİRİNCİL — nihai kullanıcı değerlendirmesi)**

Projede Braintrust "Human Review" ekranı `eval` adlı serbest metin alanıyla konfigüre edilmiştir. Kullanıcı bir trace üzerine yorum yazdığında bu, root span'ın `metadata.eval` string alanına düşer.

- Step 1 sorgusunda `metadata` kolonunu zaten çektin → `row.metadata?.eval` kontrolü yap
- **Bu alan varsa ve doluysa:** kullanıcının o trace için yazdığı **nihai değerlendirme**dir. Diğer tüm sinyallerden (metrik, success score, kendi analizin) **daha yüksek güvenle** ele al.
- **Nasıl değerlendir:**
  - Analiz raporunun **başına** "📝 Human Review notu" başlığı altında tam metnini alıntıla
  - Yorumdaki her iddiayı somut failure mode / aksiyon maddesine dönüştür
  - Kendi analiz çıkarımın yorumla çelişiyorsa, yorumu doğru kabul et ve kendi çıkarımını revize et (kullanıcı ekranı görmüş, sen görmedin)
  - "Patterns & Improvement Hypotheses" bölümündeki aksiyon maddeleri yorumla hizalı olmalı; değilse neden olmadığını belirt

**Kaynak B — Span-level `comments` alanı (İKİNCİL)**

Step 2 sorgusundaki `comments` field'ı — Braintrust UI'nin "Comment" butonuyla span'a eklenen yorumlar. Bu yolun kullanılma ihtimali düşük (proje `metadata.eval` workflow'unu tercih ediyor) ama doluysa:
- `comments[*].comment.text`, `user_id`, `created` çıkar
- Output'a ilgili step'in altında `💬 "yorum metni"` formatında ekle

`null` olanları atla.

### Step 5 — Report format

Her trace için aşağıdaki şablonu üret:

```
## Trace {idx}: {created} — {task[:80]}
- Model: {model} | Steps: {llm_calls}/{maxSteps} | Tokens: {total_tokens} | Cost: ${estimated_cost}
- Duration: {duration}s | Result: {success ? '✅' : '❌'}
- Final: {output.message}
- URL: {finalPageUrl}

### 📝 Human Review (metadata.eval)   ← sadece doluysa
> "{metadata.eval tam metni}"

### Steps
1. [tool: {toolName}] {assistant.text[:200]}
   → {toolResult[:200]}
   💬 "span-level comment varsa burada"
2. ...
```

Tüm trace'lerin sonunda kısa bir analiz bölümü:

```
## Patterns & Improvement Hypotheses
- {tekrarlayan failure mode'lar}
- {tool kullanım anomalileri}
- {prompt iyileştirme önerileri}
- {comments üzerinden çıkarılan aksiyon maddeleri}
```

## Failure modes & guards

- **`BRAINTRUST_API_KEY` yok:** MCP 401 döner. Kullanıcıya `.env` kontrolünü söyle.
- **Çok fazla span (>100):** `OFFSET` ile paginate et veya kullanıcıya `limit` belirt.
- **Büyük DOM tool results:** 500 char truncate; full içerik için kullanıcı açıkça istesin.
- **`preview_length: -1` token-pahalı:** Step 2 (spans) sorgusunda ve Step 1'de `metadata` kolonunu çekerken kullan — aksi halde `metadata.eval` truncate olabilir. Metrik-only sorgularda default'ta bırak.
- **System prompt sızıntısı:** Step span'larından çekilen `input.messages[0]` system rolü analiz çıktısına asla düşmemeli — filtre (Step 3) bunu garanti eder. `elciSystemPrompt.ts`'yi kasıtlı Read etmek farklı: bu okuma context'e gelir, sızıntı sayılmaz ama sadece gerçekten gerektiğinde yap.
- **`metadata.eval` atlanması:** Human review notu varsa ve rapora dahil edilmemişse skill hatalı çalışıyor demektir — analiz öncesi her trace'in `metadata.eval` alanını kontrol ettiğinden emin ol.
