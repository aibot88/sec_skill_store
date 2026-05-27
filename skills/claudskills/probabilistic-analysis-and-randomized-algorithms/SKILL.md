---
name: probabilistic-analysis-and-randomized-algorithms
description: Use when analyzing randomized algorithms, probabilistic analysis, indicator random variables, hiring and secretary problems, random permutations, balls-and-bins, birthday paradox, streaks, or average-case versus expected-time reasoning.
license: MIT
---

# Probabilistic Analysis and Randomized Algorithms

## Overview

Use probability to analyze either a distribution on inputs or random choices made by an algorithm. The core move is to name the sample space first, then convert events into expectations with indicator random variables whenever direct counting becomes messy.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style.

## When to Use

- A problem asks for average-case cost under random input order.
- A randomized algorithm permutes, samples, searches, or makes random choices internally.
- Expected counts involve records, collisions, empty bins, inversions, fixed points, or repeated trials.
- A prompt asks whether a shuffle, sample, or randomized strategy is uniform.
- A problem asks for the birthday paradox, balls-and-bins, coupon collector, streaks, or online hiring.

Do **not** use this skill merely because an answer contains asymptotic notation. Use `characterizing-running-times` when probability is not part of the model.

## First Distinction

| Situation | Concept | Expectation is over | Required statement |
| --- | --- | --- | --- |
| Deterministic algorithm, random input model | Average-case analysis | Input distribution | State the assumed input distribution |
| Algorithm makes random choices | Expected running time or expected cost | Random-number generator outcomes | State the guarantee for each fixed input if applicable |

Do not conflate these. Randomizing the input inside the algorithm removes the need to assume a random input distribution, but it adds work for the randomization step.

## Indicator Random Variable Workflow

Use this whenever the quantity is a count of events.

1. Define one event per item, trial, pair, or position.
2. Define the indicator:

$$
X_i = I\{A_i\}.
$$

3. Use Lemma 5.1:

$$
E[X_i] = \Pr\{A_i\}.
$$

4. Express the total count as a sum:

$$
X = \sum_i X_i.
$$

5. Apply linearity of expectation:

$$
E[X] = \sum_i E[X_i].
$$

Independence is **not required** for linearity of expectation. Independence matters only when multiplying probabilities or using distribution facts that require it.

## Hiring Problem

For `HIRE-ASSISTANT`, a candidate in position:

$$
i
$$

is hired exactly when that candidate is the best among the first:

$$
i
$$

candidates.

Use:

$$
X_i = I\{\text{candidate } i \text{ is hired}\}.
$$

Under a uniform random arrival order:

$$
\Pr\{\text{candidate } i \text{ is hired}\} = \frac{1}{i}.
$$

Therefore:

$$
E[X] = \sum_{i=1}^{n}\frac{1}{i} = \ln n + O(1).
$$

The average-case hiring cost is:

$$
O(c_h\ln n),
$$

excluding the unavoidable interviewing cost:

$$
c_i n.
$$

Worst case still hires every candidate when ranks arrive in increasing order, giving hiring cost:

$$
O(c_h n).
$$

## Random Permutations

A uniform random permutation means every one of the possible permutations has probability:

$$
\frac{1}{n!}.
$$

It is **not enough** to prove that each element has probability:

$$
\frac{1}{n}
$$

of landing in each position. That condition is only marginal uniformity.

Use `PERMUTE-BY-CYCLE` as the counterexample: choose a random cyclic offset and rotate all elements by that offset. Each element lands in each position with probability:

$$
\frac{1}{n},
$$

but only the cyclic rotations can occur. Most of the possible permutations have probability zero, so the distribution is not uniform.

For `RANDOMLY-PERMUTE`, also called `RANDOMIZE-IN-PLACE` in some editions, which swaps the current array position with a random position from the current suffix, prove uniformity with this invariant: just before iteration:

$$
i,
$$

each possible prefix of length:

$$
i - 1
$$

occurs with probability:

$$
\frac{(n-i+1)!}{n!}.
$$

Maintenance: a fixed next element is selected from the remaining positions with probability:

$$
\frac{1}{n-i+1}.
$$

At termination, each full permutation has probability:

$$
\frac{1}{n!}.
$$

## Random Sampling

To show a sampling procedure returns a uniform subset, prove the subset distribution, not just per-element inclusion probabilities. `RANDOM-SAMPLE` makes only:

$$
m
$$

calls to `RANDOM` and maintains that the returned set is a uniform subset of the current prefix size after each loop iteration.

## Birthday Paradox

For exact collision probability, analyze the complement that all birthdays are distinct:

$$
\Pr\{\text{all distinct}\} = \prod_{i=1}^{k-1}\left(1-\frac{i}{n}\right).
$$

Use:

$$
1+x \le e^x
$$

to get the threshold where collision probability is at least one half:

$$
k(k-1) \ge 2n\ln 2.
$$

For the indicator approximation, define one indicator per pair of people. The expected number of matching pairs is:

$$
\binom{k}{2}\frac{1}{n} = \frac{k(k-1)}{2n}.
$$

Remember the two questions differ: probability of at least one collision and expected number of colliding pairs need not have the same threshold.

## Balls and Bins

For a fixed bin after tossing:

$$
n
$$

balls into:

$$
b
$$

bins, the expected load is:

$$
\frac{n}{b}.
$$

The expected tosses until a fixed bin receives a ball is:

$$
b.
$$

For the coupon collector question, partition the process into stages where a hit means landing in an empty bin. In stage:

$$
i,
$$

the hit probability is:

$$
\frac{b-i+1}{b}.
$$

The expected time to fill every bin is:

$$
\sum_{i=1}^{b}\frac{b}{b-i+1} = b(\ln b + O(1)).
$$

## Streaks of Heads

For a streak of at least:

$$
k
$$

heads beginning at a fixed position:

$$
\Pr\{A_{ik}\} = \frac{1}{2^k}.
$$

Use a union bound to show long streaks are unlikely. For length about twice the logarithm, the probability of a streak anywhere is at most:

$$
\frac{1}{n}.
$$

For the lower bound, partition flips into groups of length about half the logarithm and show a full-heads group occurs with high probability. The expected longest streak has length:

$$
\Theta(\lg n).
$$

For an approximate indicator analysis of streaks of length at least:

$$
k,
$$

use:

$$
E[X_k] = \frac{n-k+1}{2^k}.
$$

## Online Hiring Problem

For `ONLINE-MAXIMUM`, reject the first:

$$
k
$$

candidates, then hire the first later record. Assume a uniform random order and distinct scores.

Let:

$$
S_i
$$

be success when the best applicant appears in position:

$$
i.
$$

There is no success for the first:

$$
k
$$

positions. For later positions:

$$
\Pr\{S_i\} = \frac{1}{n}\cdot\frac{k}{i-1}.
$$

Therefore:

$$
\Pr\{S\} = \sum_{i=k+1}^{n}\frac{k}{n(i-1)} = \frac{k}{n}\sum_{i=k}^{n-1}\frac{1}{i}.
$$

Integral bounds give the useful approximation:

$$
\Pr\{S\} \approx \frac{k}{n}(\ln n - \ln k).
$$

Maximize the lower-bound expression by choosing:

$$
k \approx \frac{n}{e}.
$$

Then the success probability is at least about:

$$
\frac{1}{e}.
$$

## Common Patterns

| Problem shape | Indicator choice | Result to reach |
| --- | --- | --- |
| Expected hires or records | One indicator per position being a new maximum | Harmonic sum |
| Hat-check fixed points | One indicator per customer getting own hat | Expected value one |
| Random inversions | One indicator per pair out of order | Half of all pairs |
| Birthday matches | One indicator per pair sharing a day | Pair count divided by days |
| Empty bins | One indicator per bin empty | Multiply by probability a fixed bin is empty |
| Streak starts | One indicator per possible starting position | Count starts times single-start probability |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Using indicator variables but trying to prove independence before summing expectations | Linearity of expectation does not require independence |
| Saying average-case and expected running time are the same thing | Average-case is over input distribution; expected time is over algorithmic random choices |
| Proving each element is equally likely in each position and calling the shuffle uniform | Prove every full permutation has equal probability; use `PERMUTE-BY-CYCLE` as the marginal-uniform counterexample |
| Ignoring the cost model in the hiring problem | Separate unavoidable interview cost from random hiring cost |
| Treating expected number of birthday matches as the same as probability of at least one match | These are related but answer different questions |
| Multiplying probabilities without checking independence or conditional probability | Use conditional probability explicitly when events are not obviously independent |
| Claiming online hiring always finds the best with high probability | The classic threshold succeeds with probability only about the reciprocal of Euler's number |
