---
name: agentic-security-review
description: Run the OWASP-aligned agentic security review path — covers goal hijacking, tool misuse, excessive agency, memory poisoning, secrets exposure, handoff failures, and observability. Opt-in from Stage 9 (Review) or the QA track. Not a new track — no state file or slash command namespace. Triggers "agentic security review", "agent security", "security review for agents", "/agentic-security-review".
argument-hint: "[feature-slug]"
---

# Agentic Security Review

An opt-in review path for identifying and mitigating risks unique to autonomous, tool-using agents. Invoke from Stage 9 (Review) or the Quality Assurance Track.

**Scope:** internal risk reduction. Not a certification or complete security guarantee.

## When to use

- Feature adds or changes agent tool use.
- Stage 9 (Review) for agent-facing workflows.
- QA track scope includes agentic automation.
- Post-incident or near-miss involving autonomous agent behavior.

## Procedure

1. **Locate the review doc.** Read [`docs/agentic-security-review.md`](../../../docs/agentic-security-review.md) — it contains the 7 risk categories and checklists.

2. **Set up a finding record.** Copy [`templates/agentic-security-findings.md`](../../../templates/agentic-security-findings.md) to `quality/<review-slug>/agentic-security-findings.md`. If no QA review is active, create a minimal `quality/<feature-slug>/` folder.

3. **Work through each risk category.** For every checklist item in `docs/agentic-security-review.md` (read-only reference — do not edit the canonical doc):
   - Mark `[x]` in the findings record if satisfied with evidence.
   - Mark open finding in the findings record if not satisfied.
   - Skip with `not-applicable` + rationale in the findings record if the category doesn't apply.

4. **Assess severity.** For each open finding:
   - **critical** — exploitable, high-impact, blocks release.
   - **high** — exploitable or likely, requires mitigation before release.
   - **medium** — possible exposure, mitigate in next sprint.
   - **low** — theoretical, accepted or deferred with rationale.

5. **Record mitigations and residual risk.** Fill in the finding-record fields: evidence, mitigation, residual risk, follow-up.

6. **Write verdict.** Complete the Summary and Verdict sections of the finding record.

7. **Link from the review artifact.** In Stage 9's `review.md` or the QA `quality-review.md`, add a section:
   ```markdown
   ## Agentic security review
   - Finding record: `quality/<slug>/agentic-security-findings.md`
   - Verdict: <complete / incomplete>
   - Blocker findings: <list or "none">
   ```

## Reporting

On completion, report:
```
Agentic security review complete.
  Finding record: quality/<slug>/agentic-security-findings.md
  Categories reviewed: 7
  Open findings: N (critical: X, high: Y, medium: Z, low: W)
  Blocker findings: <list or "none">
  Verdict: <complete / incomplete>
```

## Do not

- Do not claim the system is "secure" or "certified" — use "risk-reduced" or "reviewed for known categories."
- Do not skip the finding record — undocumented risks have no mitigation trail.
- Do not create a new track namespace, state file, or slash command — this is an opt-in skill, not a track.
- Do not modify `docs/agentic-security-review.md` during a review — findings go in the finding record, not the review doc.

## References

- [`docs/agentic-security-review.md`](../../../docs/agentic-security-review.md) — full risk categories and checklists
- [`templates/agentic-security-findings.md`](../../../templates/agentic-security-findings.md) — finding record template
- [`docs/quality-assurance-track.md`](../../../docs/quality-assurance-track.md) — ISO 9001-aligned QA workflow
- [`memory/constitution.md`](../../../memory/constitution.md) — Article IX (Reversibility)
