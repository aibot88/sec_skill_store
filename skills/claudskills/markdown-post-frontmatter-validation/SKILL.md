---
# yaml-language-server: $schema=https://skillgraph.dev/schemas/skill.v4.schema.json
schema_version: 4
name: markdown-post-frontmatter-validation
description: "Use when authoring or reviewing the frontmatter of a markdown post — checking required fields (title, date, slug, tags), validating against the content schema in `lib/content/schema.ts`, catching ambiguous date formats or tags not in the controlled vocabulary, and ensuring the slug matches the file path. Activate this skill whenever the task touches files under `content/posts/**/*.md`, the `parsePostFrontmatter()` helper, or any code path that reads YAML frontmatter from a content file. Do NOT use for general YAML schema design (use a generic schema-design skill) or for chasing a specific build-time validation failure (use debugging)."
version: 0.1.0
type: capability
category: content
domain: content/markdown/frontmatter
scope: codebase
owner: markdown-static-site-maintainer
freshness: "2026-05-06"
drift_check:
  last_verified: "2026-05-06"
eval_artifacts: none
eval_state: unverified
routing_eval: absent
stability: experimental
license: MIT
compatibility:
  runtimes:
    - node
  node: ">=20"
  notes: "Astro / Next / Eleventy / Hugo all read YAML frontmatter; the validation pattern is portable across them."
allowed-tools: Read Grep
keywords:
  - markdown frontmatter
  - post frontmatter
  - frontmatter validation
  - content schema
  - parsePostFrontmatter
  - YAML frontmatter
  - title required
  - tag vocabulary
  - slug mismatch
  - date format
  - controlled vocabulary
  - markdown post metadata
triggers:
  - markdown-post-frontmatter-validation
paths:
  - "content/posts/**/*.md"
  - "lib/content/schema.ts"
  - "lib/content/parse-frontmatter.ts"
  - "!**/*.test.md"
examples:
  - "validate the frontmatter of a new post against our content schema"
  - "why does the build fail when I add a tag like `Politics` (capital P)?"
  - "review this post's frontmatter — is the date format correct?"
  - "explain how the slug is derived from the file path"
anti_examples:
  - "design a YAML schema for a different domain"
  - "the build is failing — what's the actual error?"
  - "rewrite parsePostFrontmatter for performance"
relations:
  boundary:
    - skill: documentation
      reason: "documentation writes prose explaining the frontmatter format; this skill enforces the validation contract in code"
    - skill: debugging
      reason: "debugging chases a specific build-time validation failure from logs; this skill is the authoring discipline applied before failure"
    - skill: refactor
      reason: "refactor changes code shape; this skill enforces a specific validation contract that must survive any refactor"
  verify_with:
    - testing-strategy
grounding:
  domain_object: "Markdown post frontmatter — the YAML block at the top of every content file that drives the site's index, routing, and rendering"
  grounding_mode: repo_specific
  truth_sources:
    - content/posts/_template.md
    - lib/content/schema.ts
    - lib/content/parse-frontmatter.ts
  failure_modes:
    - missing_required_title_field
    - ambiguous_date_format_no_timezone
    - tag_not_in_controlled_vocabulary
    - slug_mismatch_with_file_path
    - frontmatter_block_not_terminated
  evidence_priority: repo_code_first
portability:
  readiness: scripted
  targets:
    - skill-md
workspace_tags:
  - content
  - static-site
  - markdown
lifecycle:
  stale_after_days: 90
  review_cadence: quarterly
---

# Markdown Post Frontmatter Validation

## Coverage

- Required-field enforcement — every post must declare `title`, `date`, `slug`, and `tags`; missing fields fail the build at parse time
- Date format discipline — ISO 8601 with explicit timezone (`2026-05-06T12:00:00Z`); ambiguous formats like `2026-05-06` or `5/6/26` are rejected
- Slug-to-path consistency — the `slug` field must match the post's directory name; out-of-sync slugs cause silent route conflicts
- Controlled-vocabulary tagging — every tag in the post's `tags` array must appear in `lib/content/tag-vocabulary.ts`; lowercase, hyphen-separated, no synonyms
- Schema evolution — when `lib/content/schema.ts` changes, every post's frontmatter is re-validated; existing posts that violate the new schema are flagged before the next build runs
- Reserved-field protection — fields like `_id`, `_internal`, or any underscore-prefixed key are reserved for the build pipeline and rejected in author-facing frontmatter

## Philosophy

The frontmatter block is the contract every post makes with the site's index, the router, and the renderer. If that contract is loose — if posts can omit fields, use ambiguous dates, or invent ad-hoc tags — the index drifts, routes silently overlap, and the search surface degrades. The cost of catching frontmatter bugs at build time is one re-run; the cost of catching them in production is a broken page or a missing entry in the archive. The rule is: validate at parse time, fail loud, and keep the schema small enough that authors can hold it in their head.

## Key Files

| File | Purpose |
|---|---|
| `content/posts/_template.md` | The canonical template every new post copies — its frontmatter is the worked example of every required field |
| `lib/content/schema.ts` | The TypeScript schema (Zod or equivalent) that runtime validation calls |
| `lib/content/parse-frontmatter.ts` | The thin wrapper that reads the YAML block and runs `schema.parse()` — the failure surface for build-time errors |

## Verification

Before merging any change to a post's frontmatter or to the schema:

- [ ] Every post has the four required fields: `title`, `date`, `slug`, `tags`
- [ ] `date` is ISO 8601 with timezone (no naked `YYYY-MM-DD`, no locale-formatted dates)
- [ ] `slug` matches the post's directory name exactly — not derived from `title` at runtime
- [ ] Every tag in `tags` is present in `lib/content/tag-vocabulary.ts` (run `npm run check:tags` to confirm)
- [ ] No underscore-prefixed fields (`_id`, `_internal`, etc.) — those are reserved for the pipeline
- [ ] Schema changes (`lib/content/schema.ts`) are paired with a `npm run validate:posts` pass against the entire `content/posts/**/*.md` set

## Do NOT Use When

| Use instead | When |
|---|---|
| (a generic schema-design skill) | The task is designing a new YAML schema for an unrelated domain |
| `debugging` | A specific build is failing and you need to reproduce the validation error from logs |
| `documentation` | The task is writing a runbook or contributor doc about the frontmatter format |
| `refactor` | The task is restructuring `parse-frontmatter.ts` without changing the validation contract |
