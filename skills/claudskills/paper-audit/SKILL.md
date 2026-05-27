---
name: paper-audit
description: Audit paper drafts for logical consistency, compliance, and academic integrity (Triangulation Matrix).
allowed-tools:
  - Read
  - Write
  - Glob
---

# Paper Audit Skill

**Goal**: Simulate a ruthless reviewer to check Intent-Implementation consistency and logical triangulation.

## Workflow

1.  **Read Input**: Read the user's paper draft (or specific sections).
2.  **Load Standards**: Read `paper-audit/CHECKLIST.md`.

3.  **Execute Audit Layers**:

    *   **Layer 1: Compliance Check**:
        *   Check against `CHECKLIST.md`.
        *   Output Pass/Fail/Warn table.

    *   **Layer 2: The Triangulation Matrix (Strict Verification)**:
        *   Compare **Claims** (Abstract/Intro) vs. **Evidence** (Experiments/Results).
        *   **Output Table**:
            *   Column 1: The Promise (Specific claims).
            *   Column 2: The Proof (Figure/Table #).
            *   Column 3: The Gap (Exact match or weak proxy?).
            *   Verdict: ✅ Validated / ⚠️ Weak Support / 🔴 Hallucination.

    *   **Layer 3: Defensive Audit (Logic Stress Test)**:
        *   **Baseline Manipulation**: Are weak baselines used?
        *   **Ablation Amnesia**: Are modules justified by ablations?
        *   **Figure-Text Consistency**: Do numbers match?
        *   **Variable Continuity**: Are symbols consistent?
        *   **Recency Check**: Are >50% citations from last 1-3 years?

    *   **Layer 4: The Decision**:
        *   List top 3 Fatal Flaws.
        *   Mock Decision: Accept / Weak Accept / Major Revision / Reject.

4.  **Output**:
    *   Save full report to `psmfiles/paper_audit_report.md`.
