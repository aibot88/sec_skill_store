---
name: wise-scraper
description: "Structured web scraping for AI coders: explore, then exploit with shipped templates, runner, and hooks."
metadata:
  author: kundeng
  version: "2.0.0"
---

# WISE Scraper

WISE teaches an AI coding agent **structured, repeatable web scraping** for JS-rendered sites. The goal is a **working scraping project** built from shipped WISE assets.

> **Rule 0 — Orient before acting.** Before opening a browser or writing any code, read `references/guide.md § Big Picture` to understand what you're building and what decisions you need to make. Only then start exploration.

```
Orient → Explore → Evidence → Choose tier → Exploit → TreeRecord → Assemble
```

1. **Orient** — read the schema, templates, and runner options; understand what's shipped
2. **Explore** — inspect the live site with `agent-browser`, test selectors, map navigation
3. **Evidence** — record selector proof and DOM observations before designing the exploit
4. **Choose tier** — prefer shipped plumbing, escalate only when justified; ask about runtime preference if unclear
5. **Exploit** — assemble a profile from template fragments, run it, extend with hooks or task-local code
6. **Process** — TreeRecord is internal truth; flatten for flat output. Assemble markdown/CSV from artifacts.

Use when: JS-rendered sites, pagination, UI state, filter combos, structured repeatable output.
Not when: a stable API/export exists, or static `curl` is clearly enough.

## Core Model: NER (Navigation/Extraction Rules)

WISE profiles define a **graph of NER nodes**. Each node is a deterministic **(state, action) → observation** triple:

| Part | Schema field | What it answers |
|---|---|---|
| **State** | `state` | "Am I where I expect to be?" — precondition check |
| **Action** | `action` | "What deterministic thing do I do?" — browser primitives |
| **Observation** | `extract` | "What do I read/emit from this state?" — extraction rules |
| **Successors** | `expand` | "How many successor states?" — elements, pages, or combinations |
| **Retry** | `retry` | "Re-execute parent actions if state check fails" — `{ max, delay_ms }` |

Nodes form a DAG via `parents[]`. The engine walks top-down: check state, execute actions, extract, expand, recurse into children. The root node (named in `entry.root`) **must have `parents: []`** — it is the entry point and has no parent. All other nodes must reference at least one parent that exists in the same resource's `nodes` list.

### Extraction types

`text`, `attr`, `link`, `table`, `ai`, `html`, `image`, `grouped`. See `references/field-guide.md § Extraction` for details.

### Action types

`click`, `select`, `scroll`, `wait`, `reveal`, `navigate`, `input`. See `references/field-guide.md § Actions` for details.

### Expansion (unified)

Instead of separate `type: pagination` / `type: matrix` / `multiple: true`, all successor-state generation goes through `expand`:

| `expand.over` | What it does | Old equivalent |
|---|---|---|
| `elements` | One successor per CSS match | `multiple: true` |
| `pages` | One successor per page (next/numeric/infinite) | `type: pagination` |
| `combinations` | Cartesian product of filter axes | `type: matrix` |

Each `expand` block supports `order: dfs | bfs` (default: dfs).

**Stop conditions on page expansion:** `sentinel` (CSS appears), `sentinel_gone` (CSS disappears), `stable` (element count stops changing), `limit` (hard cap). See `references/field-guide.md § Stop Conditions`.

**Emit + expand interaction:** When a node has both `emit` and `expand`, node-level extraction is skipped; extraction happens per-element inside the expansion. See `references/guide.md § Data Flow`.

### Artifact Schemas (exploration output contract)

After exploration, the agent declares **what data it expects to produce** in the `artifacts` block. This serves as:
- **Runtime validation** — each extracted record is checked against the schema
- **Resource chaining** — `consumes` / `produces` wire resources into a DAG
- **Self-documentation** — the profile declares its output shape without running it

```yaml
artifacts:
  page_urls:
    fields:
      url:   { type: string, required: true }
      title: { type: string, required: true }
    dedupe: url                # deduplicate by this field
  page_content:
    fields:
      title: { type: string, required: true }
      body:  { type: string, required: true }
    consumes: page_urls        # DAG edge: depends on page_urls
    output: true               # final deliverable (written to disk)
    format: jsonl              # output format: jsonl | csv | json | markdown
    structure: nested          # nested (tree JSON, default) or flat (denormalized)
```

Full artifact fields: `fields`, `consumes`, `output`, `format`, `dedupe`, `structure`, `query`, `description`. See schema.ts `ArtifactSchema`.

Resources declare `produces` and `consumes` to link into the artifact DAG. The runner resolves execution order automatically. The runner prevents double-writes automatically — when nodes emit directly, the resource-level store write is skipped.

### Data Flow: TreeRecord, emit, and consumes

The internal representation is **TreeRecord** (schema.ts):

```typescript
interface TreeRecord {
  node: string;       // which NER node
  url: string;        // page URL at extraction time
  data: Record<string, unknown>;  // extracted payload
  children: Record<string, TreeRecord[]>;  // nested subtrees
  extracted_at: string;
}
```

Children without `emit` nest inside their parent's `children`. Children with `emit` snip off into their own artifact bucket. `emit` copies/flattens subtrees into artifacts.

**emit modes:**
- **`emit: "artifact_name"`** — shorthand: snapshot nested subtree to this artifact
- **`emit: [{ to: "artifact", flatten: ... }]`** — full form with per-target shaping
  - `flatten: true` — denormalize entire subtree (leaves only; interior nodes contribute context)
  - `flatten: "child_name"` — flatten only a named child node's records or data field

**ArtifactSchema.structure** controls output shape:
- `"nested"` (default) — tree JSON preserved
- `"flat"` — denormalized via `flattenTree` (records at leaves only)

**ArtifactSchema.query** — optional JMESPath expression applied to tree records before output. The tree is converted to a clean document (data fields promoted to top-level, children keyed by node name) then queried. Enables both downward denormalization (`[].pages[].books[].{title: title}`) and upward aggregation (`[].pages[].{titles: books[].title}`). When `query` is set, it takes precedence over `structure`.

**Template references** — three scopes for `{...}` placeholders in URLs, navigate targets, and field refs:
- `{field}` — local context (consumed record data, parent extraction)
- `{artifacts.name.field}` — cross-artifact reference (latest record from named artifact)
- `{config.key}` — input config reference (from CLI/YAML config)

**Entry URL cross-resource reference** — `entry.url` can be `{ from: "resource.node.field" }` instead of a string. This resolves to multiple visit targets by walking the named resource's tree records and extracting the field from matching nodes.

**consumes — two levels:**
- **Resource-level** `consumes` — drives entry URL iteration (the resource runs once per record in the consumed artifact)
- **Node-level** `consumes` — iterates within a walk (the node runs once per record, with fields available as `{field_ref}`)
- `consumes` accepts a string or string[] (multiple artifacts merged)

**BFS is required for discovery + emit.** When a node discovers URLs and emits them, use `order: bfs` so all URLs are collected before any child navigates away.

See `references/field-guide.md § Emit and Consumes` and `references/guide.md § Data Flow` for full details.

## Agent Contract

1. **Orient first.** Read `references/guide.md § Big Picture` and scan `templates/*.yaml` before touching `agent-browser` or writing code.
2. **Explore before exploiting.** Use `agent-browser` to inspect DOM, interactions, and state.
3. **Show evidence.** Record selectors, DOM snippets, or snapshots before writing profiles.
4. **Assemble from fragments.** Templates in `templates/*.yaml` are composable — combine them. They are not alternatives.
5. **Infer runtime preference.** If the user mentions Crawlee, Scrapy, or a Python pipeline, use Tier 4. If unclear, ask.
6. **DOM eval for live extraction.** HTML parsing libraries are for post-processing only.

### Exploit Tiers

| Tier | When | What |
|---|---|---|
| 1 | Target fits declarative flow | Assemble template fragments + shipped runner |
| 2 | Target needs adaptation | Copy/adapt runner modules, hooks, AI adapter |
| 3 | Target exceeds reference boundary | Bespoke project, carrying WISE discipline |
| 4 | User prefers alternative runtime | Same YAML profile, different backend (profile format is runtime-agnostic by design; no multi-backend runner is shipped today) |

### Architecture

```
YAML profile → Zod validation → Engine → BrowserDriver → TreeRecord → Assembly
                                   ↕            ↕
                              AIAdapter    agent-browser
```

- **Schema** — Zod is the single source of truth (`schema.ts`): runtime validation, TypeScript types, JSON Schema export
- **BrowserDriver** — abstract interface; `AgentBrowserDriver` (CLI) is shipped. The interface is abstract and additional drivers can be implemented.
- **AIAdapter** — abstract interface for exploitation-phase NLP. Default is `NullAIAdapter` (no-op); `AIChatAdapter` wraps `aichat` CLI and is opt-in via `--ai-model` flag
- **Engine** — walks the NER graph with unified `expand` (elements/pages/combinations)
- **Hooks** — 5 lifecycle hooks are invoked at runtime: `post_discover`, `pre_extract`, `post_extract`, `pre_assemble`, and `post_assemble`. `pre_extract` and `post_extract` can run at both resource and node scope; node hooks are selected by name from the module registry.
- **StateSetup** — auth/login flow executed before resource walk. Declares `skip_when` (CSS check if already logged in) and a sequence of setup actions (`open`, `click`, `input`, `password`). See schema.ts `StateSetup`.
- **InterruptHandler** — auto-dismisses cookie banners, modals, and other overlays during navigation
- **URL dedup** — visited Set per resource prevents re-visiting the same URL

### Resource globals

Resources support a `globals` block for timing and retry defaults: `timeout_ms`, `retries`, `user_agent`, `request_interval_ms`, `page_load_delay_ms`. See schema.ts `Resource.globals`.

## Read Next — by step

Do **not** read all references upfront. Read only what the current step needs:

| Step | Read |
|---|---|
| Orient | `references/guide.md § Big Picture` |
| Explore | `agent-browser` CLI help (`agent-browser --help`) |
| Choose tier / runtime | SKILL.md § Exploit Tiers, `references/comparisons.md` (if Tier 4) |
| Write profile | `references/field-guide.md`, `references/schema.ts`, scan `templates/*.yaml` |
| Add hooks | `references/guide.md § Hook System` |
| Add AI extraction | `references/ai-adapter.md` |
| Config / CLI | `references/guide.md § Config Composition`, `§ Runner CLI Reference` |
| Worked examples | `examples/overview.md` |

## Working Rules

- **Assemble from template fragments** — combine pieces, don't pick one template
- **Header-based table mapping** — not positional
- **Sort verification required** — verify state changed via child's `state` check
- **Avoid ambiguous clicks** — scope by CSS/role/context
- **TreeRecord is internal truth** — flatten for flat output; assemble final formats (markdown/CSV) from artifacts
- **BFS for URL discovery** — use `order: bfs` when you need to collect all URLs before visiting

## Common Patterns

These patterns recur across real scraping targets. Internalize them before writing profiles.

### Attribute vs text extraction

`textContent` on an element is often truncated or includes child-element noise. When the full value lives in an HTML attribute (e.g., `title`, `aria-label`, `data-name`), use `attr` extraction instead of `text`:

```yaml
# Prefer this when <a> text is truncated but title has the full name
- attr: { name: company, css: "a.company-link", attr: "title" }
# Instead of
- text: { name: company, css: "a.company-link" }
```

**Tip:** During exploration, compare `element.textContent` with `element.getAttribute('title')` (or other attrs) to decide which source is authoritative.

### Sort verification via navigation

When sorting is triggered by clicking a column header that changes the URL (e.g., `?sort=price`), the sort is navigation-based, not JS-based. The child node's `state.url_pattern` check implicitly verifies the sort applied:

```yaml
- name: sort
  action:
    - click: { css: "a.sort-by-price" }
    - wait: { idle: true }

- name: rows
  parents: [sort]
  state:
    url_pattern: "sort=price"    # proves sort navigation succeeded
  expand: { over: elements, scope: "table tbody tr" }
```

No separate sort-verification node is needed when the URL itself encodes the sort state.

### Relative URL templates

`link` extraction returns raw `href` attribute values, which are often relative paths (`/docs/page`). When a consuming resource or node navigates to these URLs, prepend the base URL in the entry template or navigate action:

```yaml
# In the consuming resource's entry
entry:
  url: "https://example.com{url}"    # {url} = "/docs/page" from artifact
  root: page_node

# Or in a navigate action
action:
  - navigate: { to: "https://example.com{url}" }
```

### Expand over wrappers, not leaves

When expanding over elements for extraction, expand over the **parent wrapper**, not the leaf element you want to extract from. Expanding over `<a>` tags directly and then extracting `link: { css: "a" }` fails because the extractor looks for `<a>` children of `<a>`:

```yaml
# Correct: expand over wrapper, extract from child
expand: { over: elements, scope: ".link-wrapper:has(a)" }
extract:
  - link: { name: url, css: "a" }

# Wrong: expand over <a> directly, then extract <a> finds nothing
expand: { over: elements, scope: "a.doc-link" }
extract:
  - link: { name: url, css: "a" }     # looks for <a> inside <a> — fails
```

## Common Failure Modes

- Jumping to `agent-browser` or code before reading the framework
- Designing the exploit before collecting exploration evidence
- Jumping to bespoke code when template fragments would work
- Using HTML parsing on the live page instead of DOM eval
- Reaching for AI when selectors and plumbing are sufficient
- Ignoring user runtime preference (Crawlee/Scrapy) and defaulting to shipped runner
- **Root node with wrong parents**: The root node (named in `entry.root`) must have `parents: []`. A common mistake is setting `parents: [root]` on the entry root node itself, or on a pagination node that IS the root — this causes "unknown node" validation errors.
- **Missing root node**: If `entry.root: root` but no node named `root` exists in `nodes[]`, validation fails. Either add a `root` node or set `entry.root` to the actual first node name.
