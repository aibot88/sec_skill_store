---
name: vllm-reasoning-parsers
description: |-
  vLLM reasoning-parser operator + developer reference. `--reasoning-parser` CLI wiring, `ReasoningParser` contract (non-streaming `extract_reasoning` + per-delta `extract_reasoning_streaming`), `is_reasoning_end` xgrammar gating, `--structured-outputs-config.enable_in_reasoning` bypass, 22 built-in parsers with per-model quirks, 15 production pitfalls, authoring custom parsers via `@ReasoningParserManager.register_module` or plugin.
when_to_use: |-
  Trigger on `--reasoning-parser`, `reasoning_content`, `reasoning_parser_plugin`, `<think>`/`</think>` handling, `extract_reasoning`, `extract_reasoning_streaming`, `is_reasoning_end`, `ReasoningParser`, `ReasoningParserManager`, harmony channels (`<|channel|>analysis`/`final`), Qwen3 prompt-side `<think>`, DeepSeek-R1 missing start tag, Kimi K2 tool-section implicit end, Hunyuan state machine, Granite phrase markers, `enable_thinking=False`, `chat_template_kwargs={enable_thinking,thinking}`, reasoning-vs-content split, reasoning leaked into content, content empty while reasoning filled, structured output breaking with thinking disabled, tool calls not parsed when reasoning is on, adding support for a new reasoning model. Symptoms — "why is `reasoning_content` null on DeepSeek-R1", "Qwen3 JSON gibberish with `enable_thinking=False`". Applies even without "parser" in prompt. Also implicit — "audit reasoning config", "deploy-memo reasoning", "thinking split wrong". NOT for prompt-side Jinja (→ `vllm-chat-templates`) or tool-call JSON extraction (→ `vllm-tool-parsers`).
---

# vLLM reasoning parsers

Target: operators wiring up `--reasoning-parser NAME` on a chat-completion endpoint, or developers authoring a parser for a new thinking model. Source of truth: `vllm/reasoning/` on `main`.

## What a reasoning parser actually does

When a reasoning-trained model emits a single token stream like

```
<think>user asked X, let me check Y...</think>The answer is 42.
```

vLLM splits this into two fields on the chat-completion response: `reasoning` (the CoT) and `content` (the final answer). `--reasoning-parser NAME` selects the class that does the split. Without it, the whole stream lands in `content`.

> **Field-name note.** On current `main` the field is `reasoning` (see `ChatCompletionResponseMessage.reasoning` / `DeltaMessage.reasoning` in `vllm/entrypoints/openai/chat_completion/protocol.py`). Pre-v0.19 code and many third-party docs / clients call it `reasoning_content`. If a client is reading `reasoning_content` against a current-main server it will see `null` every time even when the parser ran correctly.

The parser is also the gating authority for **xgrammar / structured output**: by default, grammar enforcement is held off until `is_reasoning_end(input_ids)` flips true, so the model thinks freely before being constrained to JSON. Flip that default with `--structured-outputs-config.enable_in_reasoning=true` — then the grammar applies from token 0 regardless of reasoning state (useful for structured CoT).

## The contract (`ReasoningParser` ABC)

`vllm/reasoning/abs_reasoning_parsers.py`. Every parser implements:

| Method | Called by | Purpose |
|---|---|---|
| `is_reasoning_end(input_ids)` | xgrammar, non-streaming serving, tool-call gate | Has `</think>`-equivalent been emitted yet? |
| `is_reasoning_end_streaming(input_ids, delta_ids)` | xgrammar per decode step | Same, but cheap — checks only the delta |
| `extract_content_ids(input_ids) -> list[int]` | structured output | Token IDs of post-reasoning content |
| `extract_reasoning(model_output, request) -> (reasoning, content)` | non-streaming chat completion | Full-string split; either field may be `None` |
| `extract_reasoning_streaming(previous_text, current_text, delta_text, previous_token_ids, current_token_ids, delta_token_ids) -> DeltaMessage \| None` | streaming chat completion | Per-delta split; returns `DeltaMessage(reasoning=..., content=...)` or `None` to swallow |

Optional:

- `count_reasoning_tokens(token_ids)` — for usage accounting. Default returns `0`. `BaseThinkingReasoningParser` implements it via depth counter so nested `<think>…<think>…</think>…</think>` are handled.
- `adjust_request(request)` — mutate request (rare).
- `prepare_structured_tag(original, tool_server)` — emit a `structural_tag` JSON (GPT-OSS uses this for harmony).
- `reasoning_start_str` / `reasoning_end_str` — expose delimiter strings so `ReasoningConfig.initialize_token_ids` can derive the multi-token ID sequences automatically.

**Streaming vs. non-streaming are two independent code paths.** A parser that's correct on `extract_reasoning` can be buggy on `extract_reasoning_streaming` and vice versa. Every parser must be tested on both.

## The CLI path (what `--reasoning-parser qwen3` actually triggers)

`vllm/engine/arg_utils.py:552` declares `reasoning_parser: str = StructuredOutputsConfig.reasoning_parser`. `api_server.py` validates it against `ReasoningParserManager.list_registered()` at startup (invalid name = fast-fail with the list of registered names).

On request, `OpenAIServingChat` instantiates a **fresh parser per request** via `self.reasoning_parser_cls(tokenizer, chat_template_kwargs=chat_template_kwargs)` (`vllm/entrypoints/openai/chat_completion/serving.py:240`). "Fresh per request" is load-bearing for stateful parsers — see Hunyuan in the matrix.

Registry: `vllm/reasoning/__init__.py` has a `_REASONING_PARSERS_TO_REGISTER` dict of `name → (filename, ClassName)` that feeds `ReasoningParserManager.register_lazy_module`. Lazy import means a broken parser file won't crash vLLM startup until somebody selects it.

Plugin path: `--reasoning-parser-plugin /path/to/my_parser.py` calls `ReasoningParserManager.import_reasoning_parser(path)`, which `importlib`-loads the file. The file registers itself via `@ReasoningParserManager.register_module(["my-name"])` at import time. Then `--reasoning-parser my-name` selects it.

## The 15 things that go wrong

See `references/pitfalls.md` for each with repros and fixes. Quick index:

1. **`reasoning_content` is `null` on DeepSeek-R1** — chat template injected `<think>` into the prompt, so the model never emitted a start token. Parser must tolerate missing start (base `BaseThinkingReasoningParser` does, via the `.partition(start_token)` pattern).

2. **`content` is empty, CoT in `reasoning_content` with `enable_thinking=False`** — parser didn't branch on `chat_template_kwargs`. Qwen3 / DeepSeek-V3 / Kimi K2 route to `IdentityReasoningParser` (or internal flag) when thinking is off. DeepSeek-V3 has *two* names: `deepseek_v3` (thinking-default-off) and `glm45`/`holo2` = `DeepSeekV3ReasoningWithThinkingParser` (thinking-default-on).

3. **Gibberish JSON when `guided_json` + `enable_thinking=False`** — the reasoning parser's `is_reasoning_end` on the *prompt* must return True so xgrammar enforces from token 0. Serving layer caches this result as `prompt_is_reasoning_end_arr[i]`. If the parser only checks for `</think>` in input_ids and the thinking-disabled chat template emits `<think>\n\n</think>\n\n` in the prompt, this works; if it does something else, xgrammar silently stays gated.

4. **Truncated output = wrong field** — when the model hits `max_tokens` mid-reasoning, is the whole output "reasoning" or "content"? Qwen3 with `enable_thinking=True` (default) → `(model_output, None)` = all reasoning. Qwen3 with `enable_thinking=False` → `(None, model_output)` = all content. DeepSeek-R1 base → `(model_output, None)`. Know the parser's policy before shipping.

5. **Nested `<think>` tags** — base parser's `partition` stops at the first `</think>`; if a CoT contains a literal `</think>` substring (sometimes seen in distillation artifacts), content gets split wrong. `count_reasoning_tokens` uses a depth counter so counts are right, but the split is not.

6. **Tool calls break with reasoning enabled** — tool parser only sees the `content` half of `extract_reasoning`'s return. If the reasoning parser returns `(everything, None)`, tool parser sees nothing. Kimi K2 handles this by treating `<|tool_calls_section_begin|>` as an implicit reasoning-end marker.

7. **Stateful parser reused across requests** — Hunyuan A13B's `extract_reasoning_streaming` is a token-ID state machine with `self.current_state` / `self.token_buffer`. Second concurrent request on the same instance = interleaved garbage. vLLM already instantiates per-request, but custom plugins must not hoist state to class-level.

8. **Multi-token delimiter** — `<think>` may encode as a single token (DeepSeek-R1 vocab) or as multiple (`<think`, `>` in some tokenizers). Single-token path: `vocab.get("<think>")`. Multi-token: `tokenizer.encode("<think>")` and do sequence match (see GPT-OSS `reasoning_end_token_ids_prefix`). `BaseThinkingReasoningParser` raises at init if `vocab.get` returns None — don't inherit from it unless the delimiter is a single vocab entry.

9. **Single-token delta spam** — if delta is exactly one token that *is* `<think>` or `</think>`, return `None` from streaming so the client doesn't see an empty delta. Almost every parser has this skip.

10. **Harmony / GPT-OSS is different** — no `<think>` tag. Reasoning ends at `<|channel|>final<|message|>` (optionally with up to 20 special tokens between prefix and suffix). `extract_reasoning` raises `NotImplementedError` — non-streaming goes through a separate harmony branch. Don't copy DeepSeek-R1 for a harmony model.

11. **Mistral's tokenizer requirement** — `MistralReasoningParser` raises unless `isinstance(tokenizer, MistralTokenizer)`. Uses `SpecialTokens.begin_think` / `end_think` (from `mistral_common`), not the string `<think>`.

12. **Granite is regex-on-text** — "Here is my thought process:" / "Here is my response:" are phrases, not special tokens. Streaming parser has to buffer partial matches across deltas (`Here is my thou…`) which makes it the most complex parser in the tree. Read `granite_reasoning_parser.py:140+` before modifying.

13. **Implicit reasoning-end** — Kimi K2 ends at `</think>` **or** `<|tool_calls_section_begin|>`. MiniMax M2 never emits `<think>`, only `</think>`. Custom `is_reasoning_end` must encode these facts or xgrammar gates at the wrong moment.

14. **`--enable-reasoning` is gone** — older docs / Stack Overflow answers still reference it. Since roughly v0.8 the only flag is `--reasoning-parser NAME`; the enable/disable is implicit in whether one is passed.

15. **`reasoning_content` is always null — but parser worked fine.** Current-main response field is `reasoning`, not `reasoning_content` (renamed in `protocol.py`). Client-side name mismatch that looks exactly like a parser failure. Before debugging parsers, `jq '.choices[0].message | keys'` to see what fields actually exist — if `reasoning` is there, it's just a client rename.

## The per-model matrix

`references/parser-matrix.md` — one row per registered name (`deepseek_r1`, `deepseek_v3`, `ernie45`, `gemma4`, `glm45`, `openai_gptoss`, `granite`, `holo2`, `hunyuan_a13b`, `hy_v3`, `kimi_k2`, `mimo`, `minimax_m2`, `minimax_m2_append_think`, `mistral`, `nemotron_v3`, `olmo3`, `qwen3`, `seed_oss`, `step3`, `step3p5`) with: delimiter style, start-token-in-prompt-or-output, thinking-disable mechanism, truncation policy, structured-output gating peculiarities.

Router:
- `deepseek_r1`, `qwen3`, `mimo`, `ernie45`, `minimax_m2`, `olmo3`, `seed_oss`, `step3`, `step3p5`, `gemma4` → `<think>`/`</think>` family, inherit `BaseThinkingReasoningParser`.
- `deepseek_v3`, `glm45`, `holo2` → delegating wrapper; picks R1 or Identity by `chat_template_kwargs`.
- `kimi_k2` → `<think>`/`</think>` + implicit end at tool-section.
- `hunyuan_a13b` → `<think>\n` … `\n</think>\n<answer>\n` … `\n</answer>`, token-ID state machine.
- `hy_v3` → `<think>`/`</think>` (BaseThinking) + `_identity_parser` delegate when `chat_template_kwargs.reasoning_effort == "no_think"` (the default when unset). Hunyuan V3; distinct from `hunyuan_a13b`.
- `granite` → "Here is my thought process:" / "Here is my response:" regex on text.
- `openai_gptoss` → harmony channels; `extract_reasoning` is a `raise NotImplementedError`.
- `mistral` → `[THINK]`/`[/THINK]` via `SpecialTokens`, requires `MistralTokenizer`.
- `nemotron_v3` → R1 base + swap fields on `enable_thinking=False` or `force_nonempty_content=True`.
- `minimax_m2_append_think` → identity-ish; always prepends `<think>` to content, never treats anything as reasoning.

## Writing a custom parser

`references/writing-custom-parser.md` for the step-by-step. Shape:

```python
from vllm.reasoning import ReasoningParser, ReasoningParserManager
from vllm.entrypoints.openai.engine.protocol import DeltaMessage

@ReasoningParserManager.register_module(["my_model"])
class MyReasoningParser(ReasoningParser):
    def __init__(self, tokenizer, *args, **kwargs):
        super().__init__(tokenizer, *args, **kwargs)
        # resolve delimiter token IDs via self.vocab or tokenizer.encode(...)

    def is_reasoning_end(self, input_ids): ...
    def extract_content_ids(self, input_ids): ...
    def extract_reasoning(self, model_output, request): ...
    def extract_reasoning_streaming(self, prev_text, cur_text, delta_text,
                                    prev_ids, cur_ids, delta_ids): ...
```

Register decorator → lazy entry in `ReasoningParserManager.lazy_parsers`. Pass the file to `vllm serve ... --reasoning-parser-plugin /path/to/my_parser.py --reasoning-parser my_model`.

Shortcuts when delimiter is a single vocab token: inherit `BaseThinkingReasoningParser` (`vllm/reasoning/basic_parsers.py`), override `start_token` / `end_token` properties only. That covers 90% of the surface — see `deepseek_r1_reasoning_parser.py` (32 lines) for the minimal concrete subclass.

## Testing a parser

Unit tests live in `tests/reasoning/` (DeepSeek R1, Qwen3, Granite, Hunyuan, GPT-OSS, Kimi K2 all have coverage). Run a single file with:

```bash
.venv/bin/python -m pytest tests/reasoning/test_qwen3_reasoning_parser.py -v
```

Every new parser needs tests for:
- Non-streaming: start-in-prompt, start-in-output, truncated (no end), nested, empty.
- Streaming: delta that is only the start token, only the end token, end token spanning two deltas, content-before-end-token in same delta, content-after-end-token in same delta.
- `is_reasoning_end` on both pre-reasoning, mid-reasoning, and post-reasoning token ID sequences.
- Thinking-disabled path if applicable.

## Companion skills

- `vllm-chat-templates` — how the chat template injects `<think>` into the prompt (or not); why `enable_thinking=False` can change what the parser sees.
- `vllm-tool-parsers` — tool-call extraction runs on the post-reasoning `content` only. A wrong reasoning split silently breaks tool calling.
- `vllm-configuration` — `chat_template_kwargs` flows through `ChatCompletionRequest.chat_template_kwargs` into the parser `__init__`.
- `vllm-performance-tuning` — structured output tuning; reasoning parser choice affects xgrammar gating latency.
- `vllm-input-modalities` — reasoning parsers don't apply to embedding / rerank / ASR endpoints.

Upstream issue/PR anchors for each pitfall → `references/sources.md`.
