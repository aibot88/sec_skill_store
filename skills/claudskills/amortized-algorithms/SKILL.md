---
name: amortized-algorithms
description: Use when analyzing sequences of data-structure operations with aggregate analysis, accounting credits, potential functions, binary counters, multipop stacks, dynamic tables, resizing policies, or amortized versus average-case reasoning
license: MIT
---

# Amortized Analysis

## Overview

Amortized analysis is not average-case analysis and does not use probability. It proves that every worst-case operation sequence has small average cost per operation, even when individual operations in that sequence can be expensive.

**Core principle:** bound the total actual cost of every prefix of the operation sequence by either an aggregate counting argument, nonnegative stored credit, or a nonnegative potential function.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style. Keep costs, thresholds, sums, inequalities, and asymptotic bounds in display LaTeX blocks rather than inline prose or table cells.

When an answer needs a threshold such as one half or one quarter, introduce it in prose and then display the exact expression separately.

Operation names may appear in code spans, but mathematical content may not. If a pressure-test answer puts an asymptotic bound, threshold, ratio, variable expression, or inequality in an inline code span or prose sentence, treat the formatting part of the test as failed even when the amortized reasoning is substantively correct.

## When to Use

Use this skill for:

- Data-structure operations where an expensive operation consumes work created by earlier cheap operations.
- Stack operations with `PUSH`, `POP`, `MULTIPOP`, or batched deletion from a structure whose items must have been inserted first.
- Binary counters, bit flips, resettable counters, Gray-code-style flip accounting, or carry-chain arguments.
- Dynamic arrays, dynamic tables, resizing policies, load factors, expansion, contraction, and resize thrashing.
- Proofs that ask for aggregate analysis, the accounting method, the potential method, amortized cost, stored credit, or potential functions.
- Production reviews where a textbook amortized guarantee must be tied to handles, resize thresholds, memory movement, latency spikes, or adversarial operation sequences.

Do **not** use this skill for ordinary average-case analysis, randomized algorithms, expected running time, or probability distributions over inputs. Use `probabilistic-analysis-and-randomized-algorithms` when randomness is essential.

## First Decision: Which Amortized Method Fits?

| Situation | Prefer | Proof obligation |
| --- | --- | --- |
| A single global counting argument bounds all work | Aggregate analysis | Count the expensive events over the whole sequence, not per operation. |
| Future expensive work can be prepaid by specific inserted objects or bits | Accounting method | Show stored credit never becomes negative on every prefix. |
| The data structure has a global measure of saved work | Potential method | Define potential before analyzing operations, then prove it is initially normalized and never below the initial level. |
| A production structure resizes, rebuilds, or batches work | Potential method or accounting method | Tie the proof to exact thresholds, copy cost, and hysteresis. |

Amortized bounds are worst-case sequence bounds. They do not say each individual operation is cheap, and they do not remove latency spikes unless the implementation deamortizes or spreads the work physically.

## The Three Proof Patterns

### Aggregate analysis

Use aggregate analysis when all operations can share one average charge. Prove a total-cost bound for every length of sequence, then divide by the number of operations.

Proof skeleton:

1. Define the actual unit cost, such as one pop, one bit flip, or one elementary insertion.
2. Count how many expensive unit events can occur in any sequence prefix.
3. Bound the total actual cost of every prefix.
4. Divide by the number of operations and state the amortized cost.

For a binary counter starting at zero, bit position i flips at most the count below in a sequence of increments.

$$
\left\lfloor \frac{n}{2^i} \right\rfloor
$$

The total flips are bounded by the geometric sum below.

$$
\sum_{i=0}^{k-1}\left\lfloor \frac{n}{2^i}\right\rfloor < 2n
$$

Therefore the total cost is linear in the number of increments, independent of a single increment's carry-chain length.

### Accounting method

Use accounting when an operation can deposit credit on concrete objects. The total amortized charge must dominate total actual cost for every prefix.

The required prefix condition is below.

$$
\sum_{i=1}^{n}\widehat{c_i}\ge \sum_{i=1}^{n}c_i
$$

Equivalently, the stored credit below must never be negative.

$$
\sum_{i=1}^{n}\widehat{c_i}-\sum_{i=1}^{n}c_i\ge 0
$$

Useful accounting placements:

- For a multipop stack, charge each push enough to pay for inserting the item and for its later removal. Store the prepaid unit on the pushed item.
- For a binary counter, charge setting a zero bit to one enough to pay for the set now and the later reset to zero. Store the prepaid unit on each one bit.
- For table expansion with doubling, charge each insertion enough to insert the new item and help pay for the next copying phase.

Do not undercharge early operations with a promise to repay later. That fails the prefix condition and is not a valid amortized upper bound.

### Potential method

Use potential when stored work is easier to model as a property of the whole structure. The amortized cost of one operation is actual cost plus the change in potential.

$$
\widehat{c_i}=c_i+\Phi(D_i)-\Phi(D_{i-1})
$$

The total amortized cost telescopes as shown below.

$$
\sum_{i=1}^{n}\widehat{c_i}=\sum_{i=1}^{n}c_i+\Phi(D_n)-\Phi(D_0)
$$

To use this as an upper bound on actual cost, prove the condition below for every prefix.

$$
\Phi(D_i)\ge \Phi(D_0)
$$

Most answers normalize the initial potential to zero and then prove nonnegativity.

$$
\Phi(D_0)=0
$$

$$
\Phi(D_i)\ge 0
$$

If the initial potential is not zero, subtract the initial value from the potential function. The amortized costs stay the same because only potential differences matter.

## Stack and Counter Patterns

### Multipop stack

A `MULTIPOP` can be expensive once, but it cannot pop an object that was not previously pushed. Across any sequence starting from an empty stack, the number of successful pops, including pops inside `MULTIPOP`, is at most the number of pushes.

For potential analysis, use stack size as potential.

$$
\Phi(S)=\text{number of objects in }S
$$

Then `PUSH` has constant amortized cost because it pays for the push and increases potential by one. `POP` and `MULTIPOP` have zero amortized removal cost because their actual pop work is exactly offset by the potential drop.

If the stack starts with objects already present, include them in the initial potential or state their contribution separately. Do not silently assume an empty initial state when the prompt gives one.

### Binary counter

For a binary counter, the actual cost is the number of bit flips. A single increment can flip many bits, but bit flips become rarer at higher positions.

For potential analysis, use the number of one bits.

$$
\Phi(A)=\text{number of one bits in }A
$$

If an increment resets t one bits before setting at most one zero bit, its actual cost is at most the quantity below.

$$
t+1
$$

The potential change is at most the quantity below.

$$
1-t
$$

Thus the amortized cost is bounded by a constant.

$$
\widehat{c}\le (t+1)+(1-t)=2
$$

If the counter does not start at zero, account for the initial one bits. The initial potential can pay for early resets, so the total actual cost includes the difference between initial and final potential.

## Dynamic Table Pattern

Dynamic tables teach the main production lesson of amortized analysis: resizing can be cheap on average only when the policy creates enough cheap operations between expensive copies.

### Expansion-only tables

For a table that only inserts, doubles when full, and copies live items into the new table, the insertion that triggers expansion costs the old live count plus the new insertion. Aggregate analysis works because expansions happen at powers of two.

The total cost for a sequence of insertions is bounded by a linear term plus a geometric series.

$$
\sum_{i=1}^{n}c_i < n+\sum_{j=0}^{\lfloor \lg n\rfloor}2^j < 3n
$$

For potential analysis after the initial allocation, use the expansion potential below when the table is at least half full.

$$
\Phi(T)=2\left(T.\mathrm{num}-\frac{T.\mathrm{size}}{2}\right)
$$

This potential is zero immediately after expansion, grows as the table fills, and reaches the amount needed to pay for copying when the table becomes full.

### Expansion and contraction

Never shrink immediately when deletion makes the table less than half full if expansion still occurs when full. That policy can resize repeatedly after only a few operations.

Replayable bad pattern:

1. Start with capacity twice k and size just above k.
2. Repeat two deletes followed by two inserts.
3. The second delete shrinks and copies almost k items.
4. The second insert grows and copies k items.
5. A constant-size operation cycle pays a copy cost proportional to k.

The safe policy is hysteresis: grow when full, but shrink only when deletion takes the table below the quarter-full threshold. After shrinking by half, the load returns near one half, leaving room before the next resize.

Display the exact thresholds when answering:

$$
\alpha(T)=\frac{T.\mathrm{num}}{T.\mathrm{size}}
$$

$$
\text{grow when }\alpha(T)=1
$$

$$
\text{shrink when }\alpha(T)<\frac{1}{4}
$$

Use the piecewise potential below for insertion and deletion.

$$
\Phi(T)=
\begin{cases}
2\left(T.\mathrm{num}-\frac{T.\mathrm{size}}{2}\right), & \alpha(T)\ge \frac{1}{2},\\
\frac{T.\mathrm{size}}{2}-T.\mathrm{num}, & \alpha(T)<\frac{1}{2}.
\end{cases}
$$

This potential is nonnegative under the policy, zero near half full, and accumulates enough value near full or near quarter full to pay for copying live items.

Be careful: the common absolute-value shortcut is not the same potential for the quarter-shrink policy unless the shrink threshold and constants are rederived. Do not assert nonnegativity or sufficiency without checking both branches and every resize case.

## Production Translation

Amortized analysis explains total work, not necessarily tail latency. In production answers, separate the theorem from the engineering contract:

- State whether the operation can still have a large single-call cost.
- Name the unit cost: pointer pop, bit flip, copied element, allocated slot, rebuild work, or hash-table reinsertion.
- Confirm the operation sequence is the one the proof covers. Adding `DECREMENT`, `MULTIPUSH`, arbitrary bulk operations, resets, or adversarial resize rules can break a bound.
- State any representation assumption, such as contiguous storage, copy cost proportional to live items, stable handles, minimum capacity, or high-order-bit pointer.
- If latency spikes matter, recommend deamortization, incremental migration, reserve capacity, bounded batch sizes, or a data structure with worst-case guarantees.

## Answer Template

Use this structure for exercise and review answers:

1. **Cost model.** State what one unit of actual cost counts.
2. **Sequence model.** State the allowed operations and initial state.
3. **Expensive-event explanation.** Identify why one operation can be expensive and why not every operation can be expensive.
4. **Method.** Choose aggregate, accounting, or potential analysis.
5. **Invariant.** For accounting, prove credit never goes negative. For potential, prove potential is normalized and nonnegative for every prefix.
6. **Bound.** Sum the amortized costs and then relate them back to total actual cost.
7. **Caveats.** State whether single-operation latency, extra operations, or production constraints change the conclusion.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Treating amortized analysis as average-case analysis because most increments are cheap | State that no probability is involved and the bound is for every operation sequence. |
| Saying a binary counter increment has worst-case cost based on the number of performed increments rather than counter width | Separate the counter width, sequence length, and number of flipped bits. |
| Charging every table insertion one unit because expansions are rare | Use aggregate geometric counting, charge enough credit, or define a potential that pays for copying. |
| Choosing a potential such as item count for table expansion without checking whether the potential drop pays for copying | Compute actual cost plus potential change for expansion and verify a constant amortized bound. |
| Claiming the dynamic-table contraction potential is always nonnegative without checking the low-load branch | Prove the piecewise potential is nonnegative under the exact load-factor policy. |
| Shrinking at the half-full threshold | Give the resize-thrashing operation pattern and switch to a quarter-full contraction threshold. |
| Reporting only the amortized result | Include the prefix upper-bound condition and the initial-state assumption. |
| Giving the right bound while writing the bound or threshold inline | Move the mathematical expression into a display block and refer to it in prose. |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| "Amortized" means random average behavior. | It is a deterministic worst-case sequence guarantee. |
| Worst-case per operation multiplied by sequence length is the final answer. | That bound may be loose; count how often expensive work can actually occur. |
| Credit may go negative early if later operations repay it. | Invalid: every prefix must have nonnegative total stored credit. |
| Any potential function that feels like stored work is acceptable. | It must telescope and remain at least the initial potential for every prefix. |
| Dynamic-array shrink and grow thresholds should be symmetric. | Use hysteresis: grow at full and shrink near quarter full to prevent thrashing. |
| A constant amortized bound removes resize latency spikes. | It bounds total work; deamortization is needed for worst-case per-operation latency. |
| Bulk operations are automatically cheap if simple operations are cheap. | A bulk operation needs its own accounting source, such as prior inserted items. |

## Red Flags

Stop and repair the answer if it contains any of these:

- It says "average case" or "expected" when no distribution or randomness is part of the proof.
- It ignores the initial state even though the structure may start nonempty.
- It states a potential function but never proves nonnegativity or the prefix upper-bound condition.
- It says expansions are rare but does not count them or pay for copying.
- It recommends shrinking at the half-full threshold with no thrashing counterexample.
- It puts load-factor thresholds, inequalities, sums, or asymptotic bounds inline instead of display blocks.
- It excuses inline mathematical notation because the reasoning is otherwise correct.

## Verification Pressure Tests

Use these prompts to check whether this skill is working:

1. "A teammate says `MULTIPOP` makes stack operations linear and binary-counter increments are average-case cheap. Correct them with an amortized proof and state whether probability is involved."
2. "Review this proof: charge every doubling-table insertion one unit because expansions are rare. Fix it using aggregate, accounting, and potential reasoning."
3. "A dynamic array doubles when full and halves as soon as deletion makes it less than half full. Give a concrete bad operation pattern and a safe shrink policy."
4. "Use the potential method for a binary counter that starts with some one bits, and explain how initial potential changes the total actual-cost bound."
5. "For a production vector-like container, explain what amortized insertion does and does not guarantee for latency, allocation, copying, and handle stability."

Static checks for this skill:

- `SKILL.md` lives at `clrs/amortized-algorithms/SKILL.md`.
- Frontmatter name is `amortized-algorithms` and description starts with `Use when`.
- The parent `clrs` skill lists this chapter skill.
- Formal costs, thresholds, sums, and bounds are displayed in LaTeX blocks.
- GREEN pressure-test answers are rejected if they leak mathematical notation inline, even when their amortized-analysis substance is correct.
- The text distinguishes amortized total-work guarantees from production worst-case latency and resize-policy design.
