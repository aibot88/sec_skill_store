---
name: diff-summary
description: One-call structured triage of a git diff. Returns per-file role classification (source/test/config/doc/generated/build/fixture/migration), risk tier (low/medium/high) with reasons, public-API touch detection, co-changed-test detection, secret-risk path flagging, and aggregate stats. Replaces the 5-20 Read calls an agent burns reading each modified file individually to figure out "what kind of change is this and how risky is it". Stateless, no network, stdlib Python only.
when_to_use: Trigger on "what changed in this branch", "triage this PR", "summarize the diff", "is this PR safe to merge", "what's risky about this change", "what did I touch", pre-commit / pre-PR sanity checks, code-review preparation. Use BEFORE reading individual modified files — the structural picture answers most "what kind of PR is this" questions without reading any file content.
allowed-tools: Bash(diff-summary:*) Bash(python3 *diff-summary*:*)
---

# diff-summary

Structured triage of a git diff. One call replaces the per-file Read sweep an agent normally does to figure out which files in a diff are tests, which touch the public API, which are migrations, which need careful review.

Lives at `${CLAUDE_SKILL_DIR}/../../bin/diff-summary`; the plugin auto-adds `bin/` to PATH, so just run `diff-summary ...`.

## When to reach for this

- User asks **"what changed in this branch / triage this PR / is this safe to merge"** → run `diff-summary --base main --pretty`. Read the `summary.highRiskFiles` and `summary.byRole` first; only Read individual files where risk is HIGH.
- User asks **"what am I about to commit"** → run `diff-summary --pretty` (default = working tree) or `diff-summary --staged --pretty` after a `git add`.
- Pre-PR sanity check → `diff-summary --base main --risk medium --pretty` shows only the files that need a second look.
- "Did I forget to update the tests?" → check `summary.sourceFilesWithoutTestChanges`.

## Headline command

```bash
diff-summary                              # working tree (default)
diff-summary --staged                     # staged index
diff-summary --base main                  # <base>...HEAD (3-dot merge-base)
diff-summary --range A..B                 # explicit range, passed verbatim

diff-summary --max-files 200              # cap files[] (default 200)
diff-summary --include-patches            # include raw unified diff per file (opt-in)
diff-summary --public-api-only            # filter files[] to publicApiTouched only
diff-summary --risk medium                # filter files[] to risk >= MIN
diff-summary --output /tmp/d.json --shape-depth 2  # offload large payload
diff-summary --pretty                     # indented JSON
```

The four diff-source flags (`--staged`, `--base`, `--range`, default) are mutually exclusive.

## Output shape (truncated)

```json
{
  "tool": {"name": "diff-summary", "version": "0.1.0"},
  "mode": "base",
  "base": "main",
  "head": "abc1234",
  "branch": "feature/foo",
  "summarizedAt": "2026-04-28T12:34:56Z",
  "stats": {"files": 12, "insertions": 234, "deletions": 67, "movedLinesEstimate": 18},
  "files": [
    {
      "path": "src/foo.ts",
      "status": "modified",
      "role": "source",
      "language": "typescript",
      "insertions": 42, "deletions": 5,
      "binary": false,
      "publicApiTouched": true,
      "risk": "high",
      "riskReasons": ["touches-public-api", "no-test-changes"]
    }
  ],
  "summary": {
    "byRole": {"source": 5, "test": 3, "config": 2, "doc": 1, "generated": 1},
    "highRiskFiles": ["src/foo.ts"],
    "testFilesTouched": 3,
    "sourceFilesWithoutTestChanges": ["src/bar.ts"],
    "publicApiTouches": ["src/foo.ts"],
    "migrationsTouched": [],
    "secretsRiskFiles": []
  }
}
```

## Stay in your lane

- **Reading file contents** → use the Read tool. `diff-summary` is the structural picture; for the actual changed code, Read the file.
- **Deeper logical / security review** → use a code-reviewer skill or sub-agent. This tool flags risk paths; it does not analyze whether the logic is correct.
- **Coverage analysis** → out of scope. We flag "no co-changed test in this diff", which is not the same as "this code has no test coverage anywhere."
- **Secret scanning** → out of scope. We flag SECRET-RISK PATHS (`.env*`, `*.pem`, `*.key`, `id_rsa*`, `secrets.*`) so you can prompt the user, but we do not read or scan file contents. Use git-secrets or detect-secrets for real secret scanning.
- **Symbol indexing / "where is `myFunction` defined"** → not this tool.

## Honest limits

- Public-API detection is heuristic — it looks for `+export `, `+pub fn`, `+func [A-Z]`, `+def <name>(`, plus well-known entrypoint paths (`index.{ts,tsx,js}`, `mod.rs`, `lib.rs`, `__init__.py`, `main.go`). It will miss public-API touches in unusual file layouts and over-flag in test fixtures named `index.ts`.
- Risk tiers are advisory, not deterministic. They guide where to look first.
- Co-changed-test detection is name-stem-based; refactors that move tests across directories will trip it. Prefer false-positive (no test detected when there is one) over false-negative.
- Moved-lines estimate is naive whitespace-trimmed line matching across files — useful for "is this a refactor?" but not authoritative.
- Without `--include-patches`, only stats + classification ship. With it, the raw unified diff per file is included — payload size grows quickly; offload with `--output` for large diffs.
