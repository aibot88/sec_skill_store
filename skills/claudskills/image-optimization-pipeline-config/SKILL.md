---
# yaml-language-server: $schema=https://skillgraph.dev/schemas/skill.v4.schema.json
schema_version: 4
name: image-optimization-pipeline-config
description: "Use when authoring or reviewing the build-time image pipeline config — defining responsive srcset breakpoints, picking output formats (AVIF / WebP / JPEG fallback), tuning compression quality per format, and ensuring the pipeline never produces a lossy artifact for source PNGs with transparency. Activate this skill whenever the task touches `lib/images/pipeline.config.ts`, `scripts/build-images.ts`, or any code path that resizes or recompresses content images. Do NOT use for runtime image rendering choices (use a frontend skill) or for chasing a specific build failure (use debugging)."
version: 0.1.0
type: capability
category: content
domain: content/build/images
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
  notes: "sharp ^0.33 or equivalent; output formats AVIF / WebP / JPEG."
allowed-tools: Read Grep Bash
keywords:
  - image optimization
  - image pipeline
  - srcset breakpoints
  - responsive images
  - AVIF WebP fallback
  - sharp config
  - PNG transparency
  - compression quality
  - image build pipeline
  - format negotiation
  - image resize
triggers:
  - image-optimization-pipeline-config
paths:
  - "lib/images/pipeline.config.ts"
  - "scripts/build-images.ts"
  - "lib/images/format-negotiation.ts"
  - "!**/*.test.ts"
examples:
  - "configure srcset breakpoints for hero images and thumbnails differently"
  - "review the image pipeline — does it preserve transparency on PNG sources?"
  - "add AVIF output to the pipeline alongside WebP and JPEG"
  - "tune JPEG quality without breaking the AVIF pass"
anti_examples:
  - "pick the right <picture> element markup at runtime"
  - "the build is OOM-killed on the 10MB hero image"
  - "rewrite the pipeline in a different image library"
relations:
  boundary:
    - skill: documentation
      reason: "documentation writes prose about the image pipeline; this skill enforces the config contract in code"
    - skill: debugging
      reason: "debugging chases a specific build-time pipeline failure; this skill is the authoring/review primitive applied before failure"
    - skill: refactor
      reason: "refactor changes pipeline code shape; this skill enforces a specific config contract that must survive any refactor"
  verify_with:
    - testing-strategy
grounding:
  domain_object: "Build-time image pipeline configuration — the resize/compress/format-negotiation rules that turn source images in `content/` into the responsive variants under `public/images/`"
  grounding_mode: repo_specific
  truth_sources:
    - lib/images/pipeline.config.ts
    - scripts/build-images.ts
    - lib/images/format-negotiation.ts
  failure_modes:
    - lossy_compression_on_png_with_transparency
    - missing_avif_fallback_for_unsupported_clients
    - srcset_breakpoints_dont_match_layout_breakpoints
    - quality_setting_too_aggressive_visible_artifacts
    - pipeline_doesnt_skip_already_optimized_outputs
  evidence_priority: repo_code_first
portability:
  readiness: scripted
  targets:
    - skill-md
workspace_tags:
  - content
  - static-site
  - build-pipeline
lifecycle:
  stale_after_days: 90
  review_cadence: quarterly
---

# Image Optimization Pipeline Config

## Coverage

- The format-negotiation table — which output formats the pipeline produces (AVIF + WebP + JPEG fallback is the canonical shape) and the priority order browsers should request
- Srcset breakpoints — the widths the pipeline emits per image role (hero, content, thumbnail) and how those align with the site's CSS layout breakpoints
- Per-format compression quality — JPEG at 80, WebP at 75, AVIF at 65 is a defensible default; anything more aggressive needs visual A/B verification
- Transparency preservation — the pipeline must detect alpha channels in source PNGs and disable lossy formats (or fall back to lossless WebP / AVIF) for those specific images
- Idempotency — the pipeline must not reprocess already-optimized outputs on every build (cache invalidation by source-file hash, not timestamp)
- Source-format coverage — what the pipeline accepts as input (PNG, JPEG, WebP source) and what it explicitly rejects (HEIC, RAW, video formats)

## Philosophy

A build-time image pipeline is a config-defined contract between the source-of-truth images in `content/` and the bandwidth-optimized variants the browser receives. Bugs here are silent: a misconfigured srcset doesn't crash the build, it just sends a 4MB hero image to a phone. The discipline is to encode every choice — breakpoints, formats, quality, transparency rules — explicitly in the config, with a comment naming the constraint that drove each choice. Pipeline behavior should be derivable from the config without reading the build script.

## Key Files

| File | Purpose |
|---|---|
| `lib/images/pipeline.config.ts` | The canonical config: breakpoints, formats, quality settings, source-format allowlist |
| `scripts/build-images.ts` | The build entrypoint that reads the config and walks `content/` — should be a thin runner with no embedded policy |
| `lib/images/format-negotiation.ts` | The runtime helper that maps a request's `Accept:` header to the right pre-built variant |

## Verification

Before merging any change to the pipeline config:

- [ ] Every output format has an explicit quality setting; no relying on library defaults
- [ ] Srcset breakpoints match (or are a documented superset of) the site's CSS layout breakpoints
- [ ] PNG sources with an alpha channel route to lossless or alpha-preserving lossy formats (WebP-lossless, AVIF) — never to JPEG
- [ ] The pipeline skips already-optimized outputs by source-hash comparison; running the build twice in a row is a no-op on the second run
- [ ] An end-to-end test under `__tests__/images/` exercises a fixture image of each accepted format and asserts the expected variant set is produced
- [ ] The format-negotiation helper has a fallback path for clients that send no `Accept:` header (or one that lists no supported format)

## Do NOT Use When

| Use instead | When |
|---|---|
| (a frontend image-rendering skill) | The task is choosing the right `<picture>` / `<img srcset=...>` markup at the component level |
| `debugging` | A specific image is failing to optimize and you need to reproduce from build logs |
| `documentation` | The task is writing a contributor doc explaining how the pipeline works |
| `refactor` | The task is restructuring the pipeline code without changing the config contract |
