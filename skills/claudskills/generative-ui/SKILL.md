---
name: generative-ui
description: "Use when reasoning about the pattern where a language model emits, as structured output, a description of UI components or a UI sub-tree that an application then renders for the user: the typed-schema component palette, the structured-output mechanism (JSON Schema, function-calling) that constrains emission to renderable specs, the application-side render pipeline that turns the spec into pixels, the interaction loop by which user actions on the rendered UI flow back into the next turn, the security boundary between model-author and application-renderer, and the difference between this and adjacent patterns (chat with markdown, prebuilt-widget routing, RSC streaming, model-emits-code). Do NOT use for the page-level rendering taxonomy (use rendering-models), the protocol cycle of tool calls (use tool-call-flow), the trust boundary against untrusted content (use prompt-injection-defense), or general component-library architecture (use design-system-architecture)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"agent\",\"domain\":\"agent/ui\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-16\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-16\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"generative UI\\\\\\\",\\\\\\\"generative interface\\\\\\\",\\\\\\\"structured output\\\\\\\",\\\\\\\"component schema\\\\\\\",\\\\\\\"typed UI spec\\\\\\\",\\\\\\\"JSON Schema\\\\\\\",\\\\\\\"function calling UI\\\\\\\",\\\\\\\"RSC streaming UI\\\\\\\",\\\\\\\"model-rendered components\\\\\\\",\\\\\\\"assistant UI\\\\\\\",\\\\\\\"chat UI components\\\\\\\"]\",\"triggers\":\"[\\\\\\\"the assistant should show a chart not a paragraph\\\\\\\",\\\\\\\"how does the model render a card\\\\\\\",\\\\\\\"structured output for UI\\\\\\\",\\\\\\\"is it safe to render what the model returned\\\\\\\",\\\\\\\"should this be a tool call or a UI emission\\\\\\\"]\",\"examples\":\"[\\\\\\\"design the component schema for an assistant that can render a date picker, a chart, or a confirmation card depending on the question\\\\\\\",\\\\\\\"decide whether the model should emit a UI spec or call a tool that returns prerendered HTML\\\\\\\",\\\\\\\"explain why the model's output must be schema-validated before rendering\\\\\\\",\\\\\\\"design the interaction loop so a user clicking a button in a model-rendered card produces a follow-up turn the model can reason about\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"design the JSON shape of an HTTP API endpoint (use api-design)\\\\\\\",\\\\\\\"decide the page-level rendering model (CSR vs SSR vs RSC) (use rendering-models)\\\\\\\",\\\\\\\"design the design-system component library itself (use design-system-architecture)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"tool-call-flow\\\\\\\",\\\\\\\"rendering-models\\\\\\\",\\\\\\\"client-server-boundary\\\\\\\",\\\\\\\"prompt-injection-defense\\\\\\\",\\\\\\\"api-design\\\\\\\",\\\\\\\"type-safety\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"tool-call-flow\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"tool-call-flow owns the protocol cycle by which a model invokes external capabilities and receives results; this skill owns the pattern where the model's output is itself a UI specification rendered by the application. The two compose — a UI spec may be emitted via a tool-call-flow-shaped mechanism — but the conceptual surfaces differ.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"rendering-models\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"rendering-models owns the page-level rendering taxonomy (CSR/SSR/SSG/RSC/streaming); this skill owns the model→spec→component pipeline that operates inside any of those rendering models. They compose.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"prompt-injection-defense\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"prompt-injection-defense owns the security property that a system must preserve against attacker-controlled directives in model input; this skill owns the rendering pattern whose threat surface includes rendering attacker-influenced output. The two skills are read together for security analysis.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"api-design\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"api-design owns the external HTTP request/response surface; this skill owns the model-to-renderer schema surface. Both are typed contracts, but between different actors.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"design-system-architecture\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"design-system-architecture owns the component library and its tokens; this skill consumes a design system as the component palette the model can draw from.\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"api-design\\\\\\\",\\\\\\\"type-safety\\\\\\\",\\\\\\\"prompt-injection-defense\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"Generative UI is to a model-rendered interface what a building's framework is to a tenant's customization — the architect (application) lays the structural floor plan, frames the walls, and provides a catalog of approved fixtures (component palette); the tenant (model) picks which fixtures to install where for this particular layout, but cannot punch new holes in load-bearing walls or wire fixtures that don't exist in the catalog. The freedom is in the composition; the safety is in the structure.\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"Generative UI is the pattern in which a language model emits, as structured output constrained by a typed schema, a specification of a UI component or sub-tree that an application then renders for the user. The model's output is not a chat response, not a tool call asking for execution, and not raw code — it is a typed instance of a component-vocabulary schema. The application owns the rendering, the interaction layer, and the visual design; the model owns the choice of which components to compose and with what data. The pattern depends on three contracts holding simultaneously: the schema (the typed component vocabulary the model and application share), the generation constraint (the model's emission is restricted to valid instances of the schema), and the render policy (the application renders only what the schema describes, with no escape to model-authored markup or code).\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/generative-ui/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/generative-ui/SKILL.md
---

# Generative UI

## Coverage

The pattern where a language model emits, as structured output constrained by a typed schema, a specification of a UI component or sub-tree that an application then renders for the user. Covers the three load-bearing contracts (component schema, generation constraint, render pipeline), the interaction loop that closes the cycle from user action back into the model's next turn, the trust boundary that makes the rendering safe under adversarial input, the taxonomy by palette openness / generation mechanism / rendering location / interactivity / trust posture, and the distinction from adjacent patterns (chat with markdown, prebuilt-widget routing, RSC streaming as a transport, model-emits-code which is something else).

## Philosophy

The conventional model-to-user pipeline is: model emits text; user reads text. Generative UI inverts this: model emits a typed component specification; application renders the specification; user sees a UI surface authored by the application's design system but composed by the model.

This indirection is what makes the pattern simultaneously safe and expressive. Safe, because the application owns the rendering — the model can only ask the application to render components the application has chosen to expose, with data the schema permits. Expressive, because the model can compose components, choose presentations per response, and adapt to the question at hand without the developer pre-building every variant.

The discipline is in the three contracts. The schema must be small enough to be a coherent design vocabulary but expressive enough to cover the assistant's responses. The generation constraint must be reliable enough that the model's emission is always renderable. The render pipeline must enforce schema validation, design-system compliance, and security policies independently of what the model intended. When all three hold, generative UI lets a language model author the choice of what to show without ever touching the rendering surface.

## The Three Load-Bearing Contracts

| Contract | Owner | Defines | Failure mode if absent |
|---|---|---|---|
| Component schema | Application developer | The typed vocabulary the model may emit and the application will render | Model emits unrenderable specs; design inconsistency |
| Generation constraint | Model + API | The mechanism that forces the model's output to be a valid schema instance | Specs fail validation; retry loops; production flake |
| Render pipeline | Application | The code that turns a validated spec into pixels with design-system and security policies enforced | Model output reaches the DOM unchecked; security and design break |

## Generation Mechanisms Compared

| Mechanism | How it works | Reliability | Cost |
|---|---|---|---|
| Grammar-constrained decoding | Logits are masked at decode time so only schema-valid tokens emit | Highest — schema-valid by construction | Higher decode cost; requires vendor support |
| Function calling | Each component is a function in the tool list; props are arguments | High — schema-valid in most cases; occasional mis-typed argument | Standard tool-use latency |
| Free-form + post-validation | Model emits JSON unconstrained; validator retries on failure | Lowest — retries are common | Cheapest to implement, most variance in production |

Production-grade generative UI uses grammar-constrained decoding (OpenAI Structured Outputs, Anthropic tool-use with strict schemas, Gemini response schema) or function calling. Free-form with post-validation should be considered a prototype mechanism.

## The Render Pipeline

A schema-validated spec is the *input* to the render pipeline, not the output of it. The pipeline performs:

1. **Schema validation.** Confirm the spec matches the published JSON Schema or TypeScript type for the component vocabulary. Reject (and either retry or fall back) anything that doesn't.
2. **Component lookup.** Map the spec's `type` discriminator to the application's registered component implementation. A spec asking for a component the application doesn't ship is a routing error, not a permission to render arbitrary content.
3. **Props validation.** Validate the spec's props against the component's TypeScript type independently of the schema — defense in depth against schema drift.
4. **Safety policy.** For every prop that could be a security boundary — image URLs, link targets, embedded content, HTML strings — apply per-component policy (origin allowlist, URL sanitization, length cap, recursion-depth limit). The schema describes structure; the safety policy describes acceptable content.
5. **Recursive render.** Render the component with the validated props; for nested components in props, recurse through the same pipeline.
6. **Interaction wiring.** Wire interactive elements (buttons, inputs) to the application's event-routing layer, which encodes user actions as structured events the model can read in its next turn.

This pipeline is the entire load-bearing surface of generative UI's safety. The model's "intent" does not authorize rendering; the pipeline does.

## The Interaction Loop

For interactive generative UI, every interactive component needs three definitions:

| Definition | Example for a Confirm button | Why it matters |
|---|---|---|
| Action shape | `{ kind: 'confirm', component_id: string, accepted: boolean }` | The model needs a typed event in the next turn |
| Encoding in history | A user-role message with `content: [{ type: 'ui_event', event: <action shape> }]` (Anthropic) or equivalent | The model reads it the same way it reads any other turn |
| Side-effect policy | Confirming requires an additional tool call gated by user identity, never auto-executed from the click | The click is a user signal, not authorization for the destructive operation |

A generative UI with interactive components but no interaction-loop definition is one-way: the user clicks and nothing happens. A generative UI that auto-executes destructive actions on click is a prompt-injection-defense failure waiting to happen. The middle path — click produces a structured event the model reasons about, the model emits a tool call that goes through normal authorization — is the discipline.

## Vendor And Framework Examples

| Implementation | Provided by | Mechanism |
|---|---|---|
| OpenAI Structured Outputs | OpenAI | Grammar-constrained decoding against a JSON Schema |
| OpenAI Assistants tools | OpenAI | Function calling where each function returns a UI fragment |
| Anthropic tool use with strict schemas | Anthropic | Function-calling-style tool list with schema-constrained inputs |
| Gemini response schema | Google | Response constrained to a typed schema |
| Vercel AI SDK `streamUI` | Vercel | RSC streaming of components selected by function calling |
| LangChain structured chat | LangChain | Pydantic-typed structured output |
| OpenRouter / generic JSON mode | Multiple | Free-form JSON with post-validation, falling back to retry |

Citing one vendor's API as the canonical pattern is a category error; the pattern predates and outlives any single implementation. Use whichever mechanism the chosen model supports most reliably.

## Verification

After applying this skill, verify:
- [ ] The component palette is a published, typed schema (JSON Schema, TypeScript discriminated union, or equivalent) — not an informal convention.
- [ ] The generation mechanism is grammar-constrained decoding or function calling — not free-form-with-retry in production.
- [ ] Every spec the model emits is validated against the schema by the render pipeline before any component is invoked — the model's emission alone does not authorize rendering.
- [ ] Per-component safety policies are enforced: image URLs pass an origin allowlist; link targets are sanitized; content-length is bounded; nested specs terminate in finite depth.
- [ ] Every interactive component has a defined action shape, history encoding, and side-effect policy. Auto-executing destructive actions on rendered-component clicks is forbidden.
- [ ] The render pipeline never executes model-authored markup, HTML, or code. The only thing the model authors is a typed selection from the palette.
- [ ] The pattern is used for open-ended assistant responses, not for known repeated workflows where traditional UI design is the better fit.
- [ ] Accessibility (keyboard navigation, ARIA roles, focus management) is the responsibility of the application's component implementations — generative UI does not produce accessible UI for free, only delegates it to the design system.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Designing the page-level rendering model (CSR vs SSR vs RSC vs streaming) | `rendering-models` | rendering-models owns the page-rendering taxonomy; this skill operates inside any of those models |
| Designing the protocol cycle of a tool call | `tool-call-flow` | tool-call-flow owns the model↔runtime cycle; this skill owns the model→render-pipeline pattern |
| Defending against attacker-controlled directives in model input | `prompt-injection-defense` | prompt-injection-defense owns the security property; this skill owns the rendering pattern that must preserve it |
| Designing the component library itself (tokens, primitives, composition) | `design-system-architecture` | design-system-architecture owns the library; this skill consumes it as the palette |
| Designing the JSON shape of an HTTP API endpoint | `api-design` | api-design owns the request/response surface; this skill owns the model-to-renderer schema |
| Evaluating model accuracy on a specific task | `eval-driven-development` | eval-driven-development owns measurement; this skill owns the pattern being evaluated |

## Key Sources

- React Team. [Server Components RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md). The architectural basis for streaming UI from server to client used by several generative-UI implementations.
- OpenAI. [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs). Canonical reference for grammar-constrained decoding against JSON Schema — one of the primary mechanisms for the generation-constraint contract.
- Anthropic. [Tool use overview](https://docs.anthropic.com/en/docs/build-with-claude/tool-use). Tool-use with input schemas as a function-calling-style mechanism for emitting typed UI specs.
- JSON Schema. [Draft 2020-12 specification](https://json-schema.org/draft/2020-12/json-schema-core). The schema language commonly used to type the component palette.
- Google. [Gemini structured output / response schema documentation](https://ai.google.dev/gemini-api/docs/structured-output). Third-vendor implementation of the same generation-constraint contract.
- Vercel. [AI SDK `streamUI` documentation](https://sdk.vercel.ai/docs/ai-sdk-rsc/streaming-react-components). One implementation example of the pattern delivered over React Server Components streaming — cited as a worked implementation, not as the pattern itself.
- Nielsen Norman Group. [Generative UI and Outcome-Oriented Design](https://www.nngroup.com/articles/generative-ui/). Practitioner framing of where generative UI fits in the broader UX landscape.
- Schick, T., et al. (2023). ["Toolformer: Language Models Can Teach Themselves to Use Tools"](https://arxiv.org/abs/2302.04761). Background on the structured-emission research thread that enabled reliable typed model outputs.
- Karpathy, A. [LLM OS framing](https://twitter.com/karpathy/status/1723140519554105733). Conceptual framing in which generative UI is one of the rendering surfaces of an LLM-as-OS — useful for situating the pattern in a broader architecture.
