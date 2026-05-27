---
name: sast-semgrep
description: Semantic Static Analysis with Taint Support. Used to prove Hypotheses by finding Data Flows from Source to Sink.
tools: Read, Grep, Glob, Bash, Edit, Write
---

# SAST with Semgrep (Hypothesis Engine)

> "Don't just grep. Trace the data."

## 1. Taint Mode (The "Proof" Engine)

Use Taint Mode to prove a hypothesis: "User input flows to this sink without sanitization."

```yaml
rules:
  - id: hypothesis-user-input-to-exec
    mode: taint
    pattern-sources:
      - pattern: req.query.$KEY
      - pattern: process.argv[...]
    pattern-sinks:
      - pattern: exec(...)
      - pattern: eval(...)
    pattern-sanitizers:
      - pattern: escapeShell(...)
    message: "Hypothesis Confirmed: User input reaches exec() without escaping."
    severity: ERROR
```

## 2. Abstraction Patterns

When `cve-researcher` asks "Find all controllers that use this unsafe pattern", use structural matching.

- **Hypothesis**: "All controllers taking a `redirect` param are vulnerable."
- **Rule**:
  ```yaml
  patterns:
    - pattern-inside: |
        class Controller { ... }
    - pattern: return redirect($URL)
    - pattern-not: return redirect("Safe Constant")
  ```

## 3. Workflow Integration

1. **Hypothesize**: `cve-researcher` suspects a logic bug type.
2. **Draft Rule**: Create a temporary rule file `rules/temp-hypothesis.yml`.
3. **Scan**: `semgrep scan --config=rules/temp-hypothesis.yml .`
4. **Verify**: If results > 0, the hypothesis is plausible.

## 4. Writing Tips

- **Metavariables**: `$X` matches anything. `$F(...)` matches any function call.
- **Ellipsis**: `...` matches "any logic in between".
- **Focus**: Don't try to find *everything*. Write a rule to find *one specific logic flaw*.
