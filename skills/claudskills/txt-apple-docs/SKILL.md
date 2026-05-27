---
name: txt-apple-docs
description: Look up authoritative Apple-authored documentation for any text-system or Swift API via Sosumi (sosumi.ai URL swap and MCP server) and Xcode 26.3+ xcrun mcpbridge. Use when an Apple Text skill needs grounding against the actual Apple docs, an exact API signature is required, a Swift compiler diagnostic needs the official explanation, or a recently-shipped framework update has to be verified against the source. This is the entry point for documentation grounding — invoke it before reciting any specific API signature from memory.
license: MIT
---

# Apple Documentation Lookup

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

This skill is the documentation pipe for the Apple Text skill set. Apple's `developer.apple.com` pages are JS-rendered and return a "needs JavaScript" stub to non-browser fetches, so the practical access paths are Sosumi (a clean Markdown mirror at `sosumi.ai` plus an MCP server at `https://sosumi.ai/mcp`) and Apple's own `xcrun mcpbridge` (Xcode 26.3+, on-machine Xcode-bundled docs and indexed WWDC transcripts). Before claiming any specific API signature, behavior, deprecation status, or available-since version, fetch the current Apple docs through one of these tools — Apple ships fast and training cutoffs lag, so a memorized signature is the most common source of confidently-wrong code in this domain.

## Contents

- [Sosumi: URL swap and MCP](#sosumi-url-swap-and-mcp)
- [xcrun mcpbridge](#xcrun-mcpbridge)
- [When to use which](#when-to-use-which)
- [Local sidecar references](#local-sidecar-references)
- [Configuration](#configuration)
- [References](#references)

## Sosumi: URL swap and MCP

`sosumi.ai` mirrors Apple's developer documentation under the same path structure as `developer.apple.com`. The URL swap is one-to-one — every Apple docs URL has a Sosumi equivalent.

```
developer.apple.com/documentation/uikit/uitextview
        ↓
sosumi.ai/documentation/uikit/uitextview
```

The Sosumi page returns clean Markdown that any agent can read directly. This is the format used in every cross-reference link inside Apple Text skill content; the markdown stays portable to any client that can read URLs.

The Sosumi MCP server lives at `https://sosumi.ai/mcp` (Streamable HTTP + SSE) and exposes two tools:

- `search_documentation` — keyword search across Apple's documentation index, returns ranked candidate URLs.
- `fetch_documentation` — pull the Markdown body of a specific page given its URL or symbol path.

When connected via MCP, prefer `search_documentation` for "what's the right API for X" questions and `fetch_documentation` for "give me the current signature of Y" questions. Both are stateless and cheap — call them freely rather than guessing from memory.

Verifying a URL before publishing it in skill content:

```sh
curl -s -o /dev/null -w "%{http_code}\n" "https://sosumi.ai/documentation/uikit/uitextview"
# 200 = good. 404 = path doesn't resolve, find a working alternative or omit the link.
```

Apple sometimes reorganizes documentation paths between Xcode releases. A 404 doesn't mean the API is gone; it means the path moved. Search via `sosumi.ai` or via the MCP `search_documentation` tool to find the new location.

## xcrun mcpbridge

Xcode 26.3 (Feb 2026) shipped `xcrun mcpbridge`, an MCP server that exposes Xcode's bundled documentation and indexed WWDC transcripts to external agents. It's an Apple-controlled fallback for cases where Sosumi 404s, the network is unavailable, or you need WWDC-session content that Sosumi doesn't index.

The bridge launches as a subprocess and speaks MCP over stdio:

```sh
xcrun mcpbridge
```

Among its 20-tool catalog, the relevant ones for documentation are:

- `DocumentationSearch` — keyword search against the docs bundled with the local Xcode install.
- `WWDCTranscriptSearch` — keyword search against indexed WWDC session transcripts.

These return on-machine content that matches the Xcode version installed. If the local Xcode is 26.3, `DocumentationSearch` returns the docs Apple shipped with 26.3 — which may differ from `sosumi.ai`'s mirror if the mirror is a release behind. For verification work, the bridge is the closer-to-source channel; for portable skill content, Sosumi URLs are the right link target.

Skill content should always link to `sosumi.ai` URLs (so the markdown is portable to clients without `xcrun mcpbridge` available). Use the bridge as a runtime verification tool, not as a link target in committed content.

## When to use which

Three practical cases:

- **You're writing or editing a skill and need to add a documentation link.** Use Sosumi via URL swap. Verify with `curl` that the URL returns 200 before committing.
- **You're answering a live question and need to confirm an exact API signature.** Use the Sosumi MCP server (`fetch_documentation` on the symbol page) if connected, or `xcrun mcpbridge`'s `DocumentationSearch` if the agent runs locally with Xcode 26.3+ available.
- **You need WWDC-session content for a "what changed" question.** `xcrun mcpbridge`'s `WWDCTranscriptSearch` is the right path — Sosumi indexes the documentation but not the session transcripts.

Neither path is a substitute for opening the actual project source. Documentation tells you what the API does; the project source tells you what's already calling it. Skills that diagnose code (`txt-textkit-debug`, `txt-fallback-triggers`) ground their patterns in source code first, then verify API claims against docs second.

## Local sidecar references

This skill carries a small set of pre-fetched Apple-text-relevant doc summaries as repo sidecars, useful as an offline fallback and as quick context when no MCP server is connected:

- [references/xcode-docs-index.md](references/xcode-docs-index.md) — index of the Apple-text subset and the bundled Swift diagnostics catalog.
- [references/xcode-attributedstring-updates.md](references/xcode-attributedstring-updates.md) — Foundation `AttributedString` surface changes.
- [references/xcode-styled-text-editing.md](references/xcode-styled-text-editing.md) — SwiftUI styled `TextEditor` editing behavior.
- [references/xcode-toolbar-features.md](references/xcode-toolbar-features.md) — toolbar features near editing and text-centric UI.

These sidecars are time-stamped against the Xcode version that produced them. Treat them as snapshots: useful for context when MCP is unavailable, but recheck against Sosumi or `xcrun mcpbridge` before quoting a signature into production code.

## Configuration

Two environment variables control the runtime Apple-doc reading behavior used by other Apple Text skills:

| Variable | Default | Purpose |
|---|---|---|
| `APPLE_TEXT_XCODE_PATH` | `/Applications/Xcode.app` | Custom Xcode path (e.g., `/Applications/Xcode-beta.app`) |
| `APPLE_TEXT_APPLE_DOCS` | `false` | When `true`, enables runtime loading of Apple-authored Markdown docs from the local Xcode install |

When `APPLE_TEXT_APPLE_DOCS=true` and a local Xcode contains the for-LLM Markdown bundle, prefer it for verification. The repo sidecars in `references/` are the offline fallback when the runtime channel is unavailable.

## References

- `/skill txt-attributed-string` — `AttributedString` decisions and conversions
- `/skill txt-swiftui-texteditor` — SwiftUI rich-text editing on iOS 26+
- `/skill txt-writing-tools` — Writing Tools integration (time-sensitive surface)
- `/skill txt-detectors-tagger` — Foundation/NaturalLanguage utilities
- [Sosumi.ai](https://sosumi.ai/) — Markdown mirror of Apple developer docs
- [Giving external agents access to Xcode](https://sosumi.ai/documentation/xcode/giving-external-agents-access-to-xcode) — `xcrun mcpbridge` overview
