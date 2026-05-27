---
name: secure-code-write
description: 'Proactive secure-coding coach scoped to the file or topic you are working on — surfaces relevant SAST rule IDs, CWE patterns, language-specific PASS/FAIL code snippets. Use when about to write auth, crypto, SQL, deserialization, file-handling, or template code; coaching juniors; pair-programming a security-sensitive change.'
argument-hint: "[<file-path>] | [<topic: auth|crypto|sql|xss|deser>]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
model: sonnet
triggers:
  - "secure coding"
  - "auth code"
  - "crypto code"
  - "sql injection"
  - "secure write"
chain:
  - sast-scan
outputBudget: medium
cooldown: per-session
---

# Vulnetix Secure Code Write Skill

## Use when

- About to write authentication, crypto, SQL, deserialization, file-handling, or template code.
- Coaching a junior on a new security-sensitive feature.
- Pair-programming a security-sensitive change with a reviewer who wants to surface rules upfront.
- Reviewing a PR and want the rule digest the author should have seen.
- Cross-referencing the SAST rules that would fail BEFORE writing the code that triggers them.

## Don't use for

- Actually scanning code — use `/vulnetix:sast-scan`.
- Generic security advice — this skill is rule-grounded, not narrative.
- Educating non-developer audiences — the rule digest is engineer-targeted.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

A coach, not a scanner. Use this when about to author auth, crypto, SQL, deserialization, file-handling, or templating code — surfaces the rules a reviewer would check, before you write the buggy version.

## Step 1: Load capabilities + decide topic

Read `.vulnetix/capabilities.yaml`. Determine language from `derived.primary_package_manager` or the file extension of `$ARGUMENTS`.

If `$ARGUMENTS` is a topic keyword (auth, crypto, sql, xss, deser, file, template), use it directly. Else infer from file content (Read the file, look for keywords).

## Step 2: Pull rule digest

```bash
vulnetix scan --list-default-rules -o json | jq '[.rules[] | select(.tags | contains([$topic]))]' --arg topic "$TOPIC"
```

Plus CWE intel:

```bash
vulnetix vdb cwe list --keyword "$TOPIC" -V v2 -o json | jq -f "${CLAUDE_PLUGIN_ROOT}/skills/_lib/jq/cwe.jq"
```

## Step 3: Render coach

```
Secure-code coach: <topic> in <language>

Top rules to honor:
1. <rule-id>: <one-line summary>  (CWE-XXX)
2. ...

Common pitfalls:
- ...

Snippets that pass / fail:
PASS:
<code>

FAIL:
<code>
```

Tailor snippets to the detected language.

## Step 4: Optional inline check

If the user is editing a file, offer:

```
Run `/vulnetix:sast-scan --paths <file>` after I finish to confirm.
```

## No memory writes

Coaching only.

## Edge cases & gotchas

- Topic detection from file content uses keyword heuristics — be explicit (`--topic crypto`) if working with mixed-concern code.
- Rule digest is `vulnetix scan --list-default-rules` filtered by tag; the rule set updates with the CLI release, not per-org policy.
- PASS/FAIL snippets are language-tailored from `derived.primary_package_manager`. JVM-stack repos with both Java and Kotlin may get snippets in only one.
- `vdb cwe <id> -V v2` returns CWE-specific defensive guidance — use it for educational follow-up, not as the rule source.
- No memory writes — this is read-only coaching.
- For green-field projects without a lockfile, the language detection falls back to `--topic`; pass explicitly.
