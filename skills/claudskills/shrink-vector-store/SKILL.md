---
name: shrink-vector-store
description: "Shrink an embedding/RAG vector store 4–32× via int8 or binary quantization with a float rescore pass, preserving recall and provenance metadata. Use when a vector store is too large to be laptop-resident, query cost/latency is too high, or embeddings need to be quantized for FAISS/Qdrant/usearch. Do NOT use for embed-time ingestion failures (e.g. a provider 'too many tokens' 400 — that is an upstream chunking bug, not a storage-size problem) and do NOT enable the dark TurboQuant 4-bit path without the gate below."
---

# Shrink Vector Store

Reduce a stored embedding index's footprint with **scalar (int8)** or
**binary** quantization plus an **asymmetric float rescore**, so recall
stays high while the store shrinks 4–32×. Vectors change; provenance
metadata does not.

## Prerequisites

- `numpy` (only hard dependency). Python 3.
- The original float32 vectors (or a representative sample ≥10k) **and** a
  query set — required to measure recall; this skill cannot validate blind.

## Decision (commit to one)

| Goal | Choice | Shrink | Recall |
|------|--------|--------|--------|
| Safe default | **int8 + float rescore** | ~4× | ≈ float (rescore recovers it) |
| Maximum shrink | **binary + int8 rescore** | up to ~32× | ~96–99% with rescore |
| Extra trim (optional) | + Matryoshka dim-trim | stacks | depends on model support |

Pick **int8+rescore** unless the user explicitly needs maximum shrink.
Do not offer both and ask — choose, state which, proceed.

## Workflow

1. **Confirm scope.** Verify it is a storage-size problem, not an
   ingestion failure (see above). If ingestion, stop and explain.
2. **Locate the float baseline.** You need the original float32 vectors
   (or a sample ≥10k) and a query set to measure recall against.
3. **Quantize + build index.** Run the reference script:
   ```
   python scripts/quantize_embeddings.py --vectors vecs.npy --queries q.npy \
       --precision int8 --rescore --out store/
   ```
   `--precision {int8,binary}`; `--rescore` keeps a small float/int8 copy
   for the second-pass reorder; `--matryoshka N` optionally truncates dims.
4. **Validate recall (mandatory feedback loop).** The script reports
   `recall@10` of the quantized+rescore store vs the exact float baseline.
   **Gate: if recall@10 drops more than the user's tolerance (default 2%),
   do not ship** — fall back to a higher-precision setting and re-run.
5. **Preserve provenance.** Only the vector column is replaced. Any id /
   source / timestamp / provenance fields MUST be carried through
   unchanged. The script asserts row-count and id alignment; if it fails,
   stop — never silently drop provenance.
6. **Report.** State: precision used, achieved shrink ×, recall@10 vs
   float, and whether the recall gate passed.

## Rules

- **R0 — Storage problem only.** This skill addresses store *size*. An
  *embed-time* failure (provider rejects input as "too many tokens") is an
  upstream ingestion-chunking bug — quantization changes nothing about it.
  If that is the situation, say so and stop.
- **R1 — Asymmetric distance.** The query stays full precision; only the
  stored DB vectors are quantized. Never quantize the query.
- **R2 — Rescore is not optional for binary.** Binary without a rescore
  pass loses too much recall; the script enforces `--rescore` when
  `--precision binary`.
- **R3 — Provenance is immutable.** Quantization replaces vectors only.
  Row count, ordering, and all non-vector columns are preserved and
  asserted. A mismatch is a hard stop.
- **R4 — Measure, don't assume.** Always report measured recall@10 vs the
  exact float baseline on the user's own data. The "~96–99%" figures are
  priors, not guarantees for a given corpus.

## TurboQuant 4-bit path — DARK, gated (do not enable)

A 4-bit TurboQuant-style path (training-free random rotation +
per-coordinate scalar quant) can beat int8 on the footprint/recall
frontier. It is **deliberately not implemented here.** It is gated on an
external decision (port vetting + a measured benchmark beating the
int8-rescore baseline + an IP/patent review). Until that gate explicitly
passes:

- Do **not** add a 4-bit path to the script.
- Do **not** vendor a TurboQuant port into this skill.
- If asked for it, explain it is gated and that int8-rescore is the
  sanctioned baseline it must first be measured against.

## Output

A quantized store directory plus a stdout report. Concrete example
(int8 + rescore, 2000×128 sample):

```
precision=int8 rescore=True matryoshka=off
vectors=2000 dim=128 float_MB=1.0 quant_MB=0.3 shrink=4.0x
recall@10=0.9800 (gate: >= 0.9800)
written to <out>/
recall gate PASSED
```

Exit codes: 0 pass · 2 bad args/precondition · 3 provenance misalignment ·
4 recall gate failed. A non-zero exit means do not ship the quantized store.

## Limitations

- Needs the original float vectors (or a representative sample) to measure
  recall — cannot validate blind.
- Matryoshka dim-trim only works if the embedding model was trained for
  it; the script errors clearly if truncation collapses recall.
- Cross-environment determinism: if any rotation/projection is used,
  build-time and query-time must use the same seeded transform.

## Reference

- `scripts/quantize_embeddings.py` — run it (don't read it): quantizes,
  builds the index, runs the asymmetric rescore, and prints the recall@10
  vs float gate result. Handles its own errors and exits non-zero on a
  failed provenance or recall assertion.
