# Debugging & Code Review Skill — Production Grade

## When to Use
Trigger this skill for any request involving:
- Broken, erroring, or misbehaving code in any language
- Stack traces, error messages, or unexpected output
- "Why doesn't this work?" or "What's wrong with my code?"
- Code review, quality audit, or refactor requests
- Performance problems, memory leaks, or slow execution
- Tests that fail unexpectedly
- Security review or vulnerability assessment
- "Make this code better / cleaner / more maintainable"

---

## The Debugging Mindset

Debugging is not guessing. It is a **systematic process of eliminating hypotheses** until one remains.

The single biggest mistake is jumping to solutions before understanding the problem. Every minute spent understanding saves five minutes of wrong fixes.

Three rules that govern everything else:

1. **Read the error before doing anything else.** The error message almost always contains the answer or a direct pointer to it. Most bugs are solved by reading carefully, not by intuition.
2. **Change one thing at a time.** Changing multiple things simultaneously makes it impossible to know what fixed (or broke) what.
3. **Reproduce before fixing.** If you can't reliably reproduce the bug, you can't know when you've fixed it.

---

## Phase 1: Triage — Understand Before Touching Anything

When presented with broken code, resist the urge to immediately start editing. Spend the first pass purely understanding.

### Read the Full Error Message

```
Error structure (most languages):
  [Error Type]: [Message]
    at [File]:[Line]:[Column]
    at [call stack frame 2]
    at [call stack frame 3]
```

Extract these four things from every error:
- **Error type** — what category of failure is this? (`TypeError`, `NullPointerException`, `SyntaxError`, `SIGSEGV`)
- **Error message** — what exactly went wrong? Read it literally.
- **File + line number** — where did it fail? This is the starting point, not necessarily the root cause.
- **Call stack** — how did execution get there? The root cause is often several frames up from where it crashed.

> **Critical rule:** The line that throws is not always the line that's wrong. A null reference on line 87 was probably caused by a missing assignment on line 23. Always trace the stack upward.

### The Five Questions Before Writing Any Fix

1. **What was the code supposed to do?** Understand the intent.
2. **What is it actually doing?** Observe the real behavior, not what you expect.
3. **What changed recently?** Bugs rarely appear in code that has been stable for months. Check git log.
4. **What are the assumptions?** Which assumption is being violated — about data shape, types, order of operations, or environment?
5. **Is this the only place this happens?** Is it consistent or intermittent? Intermittent bugs are almost always concurrency, timing, or state issues.

### Reproduce the Bug First

Before writing a single fix:
```
Minimal reproduction checklist:
  ✓ Can I trigger the bug reliably?
  ✓ Can I reduce it to the smallest possible case?
  ✓ Does it happen in a clean environment (not just my machine)?
  ✓ Does it depend on specific data, state, or timing?
```

A bug you cannot reproduce is a bug you cannot fix. If it's intermittent, add logging first — then wait for it to reproduce with evidence.

---

## Phase 2: Error Taxonomy — Know What You're Fighting

Understanding the type of bug determines the debugging strategy.

### By Error Category

**Syntax Errors**
- Caught at parse/compile time. The program never runs.
- Root cause: typo, missing bracket, unclosed string, wrong indentation (Python)
- Fix: read the error line number precisely. Syntax errors are often one line above where reported.
```python
# Error points to line 5, but the real problem is line 3
def calculate(x, y   # ← missing closing paren
    return x + y     # ← reported here
```

**Type Errors**
- Caused by operating on the wrong type: calling a method that doesn't exist, passing a string where a number is expected, treating `null`/`undefined`/`None` as an object.
- Most common bug class in dynamically typed languages (Python, JavaScript).
- Fix: add type assertions or logging to find where the wrong type entered the system.
```javascript
// Common pattern: API response shape changed
const name = user.profile.name;  // TypeError if user.profile is undefined
// Fix: always validate external data shapes at the boundary
const name = user?.profile?.name ?? 'Unknown';
```

**Logic Errors**
- The code runs without errors but produces wrong output.
- The hardest class of bugs because no tooling catches them — only correct understanding does.
- Root causes: off-by-one errors, wrong operator (`>` vs `>=`), incorrect algorithm, wrong formula, inverted condition.
```python
# Off-by-one — extremely common
for i in range(len(items)):      # correct
for i in range(len(items) - 1): # BUG: misses last item
for i in range(len(items) + 1): # BUG: index out of bounds
```

**Runtime Errors / Exceptions**
- Code is syntactically valid but fails during execution due to bad state, bad input, or environmental failure.
- Classes: division by zero, index out of bounds, stack overflow (infinite recursion), file not found, network timeout, out of memory.

**Concurrency Errors**
- Race conditions, deadlocks, thread starvation.
- Almost always intermittent and timing-dependent — hardest to reproduce.
- Hallmarks: "works on my machine", "fails under load", "fails randomly".
- Fix strategy: add structured logging with timestamps; look for shared mutable state; suspect any code that reads then writes without atomicity.

**Environment / Configuration Errors**
- Code is correct but the environment is wrong: wrong dependency version, missing environment variable, wrong file path, wrong database schema, stale cache.
- Hallmark: "it worked yesterday" or "it works on dev but not prod".
- Fix strategy: compare environments systematically. Check versions, env vars, config files, and infrastructure differences.

**Integration / Boundary Errors**
- The code is correct but the data coming in from outside (API, database, user input, file) doesn't match expectations.
- Root cause: schema change, API version change, encoding issue, null from database where code assumes non-null.
- Fix strategy: validate and log all external inputs at the boundary. Never trust external data shape.

---

## Phase 3: The Debugging Process

### Step 1 — Localize: Find the Exact Failure Point

Binary search the codebase. Don't read everything — narrow down to where the behavior diverges from expectation.

```
Strategy:
  1. Find the last point where behavior was correct
  2. Find the first point where behavior was wrong
  3. The bug lives between those two points

Tools:
  - Add print/console.log at midpoints to bisect
  - Comment out blocks to isolate which section fails
  - Use breakpoints in a debugger to inspect state at each step
  - Check git blame/log — when did this line last change?
```

### Step 2 — Inspect State: What Do the Values Actually Contain?

The most common debugging error is assuming you know what a variable contains. You don't. Verify it.

```javascript
// Don't assume — verify
console.log('user object:', JSON.stringify(user, null, 2));
console.log('type:', typeof user.id, '| value:', user.id);
console.log('array length:', items.length, '| first item:', items[0]);
```

```python
# Python — inspect before assuming
print(f"Type: {type(data)}, Value: {repr(data)}")
print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
```

**What to inspect at every suspicious point:**
- The actual value (not what you think it is)
- The type (especially in dynamic languages)
- For collections: length, first item, last item
- For objects: which keys are present vs. missing
- For numbers: is it `NaN`, `Infinity`, `null`, or `undefined`?

### Step 3 — Form a Hypothesis

State your hypothesis explicitly before testing it. This prevents confirmation bias.

```
Hypothesis format:
  "I believe [X] is happening because [Y], which would mean [Z] is true.
   I will verify by [specific test]."

Example:
  "I believe the user ID is being passed as a string instead of an integer
   because the API is returning it quoted. I will verify by logging
   typeof userId before the database query."
```

### Step 4 — Test the Hypothesis (One Change at a Time)

Make exactly one change. Observe the result. If it fixes the bug, you understand the cause. If it doesn't, you've eliminated one hypothesis — which is still progress.

Never:
- Make three changes and see if it works
- Delete code hoping the bug disappears
- Add a try/catch that swallows the error (this hides bugs — it doesn't fix them)

### Step 5 — Fix the Root Cause, Not the Symptom

This is the most important discipline in debugging.

```javascript
// Symptom fix — wrong
try {
  processUser(user);
} catch (e) {
  // silently swallow — BUG IS STILL THERE, just hidden
}

// Root cause fix — right
// Find WHY processUser fails and fix the upstream data or logic
if (!user || !user.id) {
  throw new Error(`processUser called with invalid user: ${JSON.stringify(user)}`);
}
processUser(user);
```

**Ask: "Why did this happen?" five times (The 5 Whys):**
```
Bug: Payment failed
Why 1: The charge API returned an error
Why 2: The amount was null
Why 3: The cart total returned undefined
Why 4: The cart was empty when total was calculated
Why 5: The cart state was cleared before checkout completed ← ROOT CAUSE
```

Fix Why 5. Not Why 1.

### Step 6 — Verify the Fix

After fixing:
1. Confirm the original bug is gone
2. Run the full test suite — did you break anything else?
3. Test edge cases: empty input, null, very large values, concurrent execution
4. If the bug was in production: deploy to staging first, monitor after production deploy

---

## Phase 4: Language-Specific Debugging Patterns

### JavaScript / TypeScript

**Most common bugs:**
- `undefined` is not an object (accessing property of undefined/null)
- Async/await not awaited — promise returned but not resolved
- `this` context lost in callbacks and event handlers
- Mutating state directly in React (object/array reference not changed)
- `==` vs `===` type coercion surprises

```javascript
// Async debugging — always check if await is missing
const data = fetchData();        // BUG: data is a Promise, not the value
const data = await fetchData();  // correct

// this context — always verify in callbacks
class Timer {
  start() {
    setTimeout(function() {
      this.stop(); // BUG: this is undefined or window
    }, 1000);
    setTimeout(() => {
      this.stop(); // correct: arrow function preserves this
    }, 1000);
  }
}

// React state mutation
// BUG: direct mutation doesn't trigger re-render
state.items.push(newItem);
setState(state);

// correct: new reference
setState(prev => ({ ...prev, items: [...prev.items, newItem] }));

// Defensive optional chaining for external data
const city = response?.data?.address?.city ?? 'Unknown';
```

**TypeScript-specific:**
```typescript
// Use strict null checks — catches entire classes of runtime errors at compile time
// tsconfig.json: "strict": true

// Never use 'any' — it defeats the purpose
function process(data: any) { ... }     // gives up type safety
function process(data: UserData) { ... } // correct

// Type narrowing before operations
function getName(user: User | null): string {
  if (!user) return 'Guest';  // narrowed — TypeScript knows user is User below
  return user.name;
}
```

### Python

**Most common bugs:**
- Mutable default argument (the classic Python trap)
- Modifying a list while iterating it
- Integer division vs float division (Python 2 vs 3 legacy)
- Scope issues with `global` and `nonlocal`
- Silent exception swallowing with bare `except:`

```python
# Mutable default argument — one of Python's most famous bugs
def add_item(item, items=[]):    # BUG: list is shared across ALL calls
    items.append(item)
    return items

def add_item(item, items=None):  # correct
    if items is None:
        items = []
    items.append(item)
    return items

# Never use bare except — it catches SystemExit and KeyboardInterrupt
try:
    process()
except:            # BUG: catches everything including ctrl+C
    pass

try:
    process()
except Exception as e:           # correct: catches only real exceptions
    logger.error(f"Failed: {e}")
    raise  # re-raise unless you're intentionally swallowing

# Modifying list during iteration
for item in items:           # BUG if items is modified inside
    if condition(item):
        items.remove(item)   # skips next item

for item in items[:]:        # correct: iterate a copy
    if condition(item):
        items.remove(item)
```

### SQL

**Most common bugs:**
- Missing `WHERE` clause on `UPDATE`/`DELETE` (catastrophic)
- `NULL` comparison with `=` instead of `IS NULL`
- Implicit type conversion in comparisons
- N+1 query problem (loop calling database per iteration)
- Off-by-one in `LIMIT`/`OFFSET` pagination

```sql
-- ALWAYS verify WHERE clause before UPDATE/DELETE
-- Run as SELECT first to see what you'll affect
SELECT * FROM users WHERE last_login < '2023-01-01';  -- verify rows first
UPDATE users SET status = 'inactive' WHERE last_login < '2023-01-01';  -- then update

-- NULL comparison
SELECT * FROM users WHERE deleted_at = NULL;    -- WRONG: always returns 0 rows
SELECT * FROM users WHERE deleted_at IS NULL;   -- correct

-- N+1 pattern — never query inside a loop
for user_id in user_ids:
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", user_id)  # N queries

-- Fix: one query with IN clause or JOIN
cursor.execute("SELECT * FROM orders WHERE user_id IN (?)", user_ids)
```

### General Async / Concurrency

```javascript
// Race condition pattern
let counter = 0;
async function increment() {
  const current = counter;       // read
  await someAsyncOperation();    // yield — another call can run here
  counter = current + 1;         // write — overwrites other increments: RACE CONDITION
}

// Fix: use atomic operations or locks
// In Node.js: use a queue or mutex library
// In databases: use transactions with appropriate isolation levels

// Promise.all vs sequential — know the difference
// Sequential (slow — waits for each)
const a = await fetchA();
const b = await fetchB();

// Parallel (fast — runs simultaneously)
const [a, b] = await Promise.all([fetchA(), fetchB()]);

// Error handling in Promise.all — if one rejects, all reject
// Use Promise.allSettled when you want all results regardless of failures
const results = await Promise.allSettled([fetchA(), fetchB()]);
```

---

## Phase 5: Code Review — What to Look For

Code review is not about style. It is about correctness, maintainability, and safety. Style is enforced by linters, not humans.

### Review in This Order (Most Critical First)

**1. Correctness — Does it actually do what it claims?**
- Does the logic match the stated intent?
- Are edge cases handled: empty array, null input, zero, negative numbers, very large input?
- Are error cases handled and communicated appropriately?
- Are all code paths reachable? Are there dead branches?
- Do tests exist and do they test the right things?

**2. Security — Could this be exploited?**
See Phase 6 for the full security checklist.

**3. Error Handling — What happens when things go wrong?**
- Are errors caught at the right level?
- Are error messages informative to developers without leaking internals to users?
- Are failures loud (logged, alerted) or silent (swallowed)?
- Is the system left in a consistent state after an error?

**4. State Management — Is state mutation safe?**
- Is shared mutable state clearly identified and protected?
- Can this code run concurrently? Is it safe if it does?
- Are side effects predictable and documented?

**5. Performance — Will this scale?**
- Are there N+1 queries hidden in loops?
- Are expensive operations (network calls, disk I/O) repeated unnecessarily?
- Is data loaded eagerly when lazy loading would suffice?
- Does memory grow unboundedly?

**6. Maintainability — Will someone understand this in 6 months?**
- Is the intent of non-obvious code explained in comments?
- Are names (variables, functions, classes) accurate and descriptive?
- Is the function doing one thing or many things?
- Is the code at a consistent level of abstraction?
- Is there duplication that should be extracted?

**7. Interface / API Design — Is this the right abstraction?**
- Is the function signature intuitive? Would a new developer know how to call it?
- Are parameters ordered logically? Are defaults sensible?
- Does it follow the principle of least surprise?
- Will this API be painful to change later?

### Code Review Comment Tiers

Use explicit severity labels so the author knows what's blocking vs. optional:

```
🚨 BLOCKER    — Must fix before merge. Correctness, security, or data integrity issue.
⚠️  IMPORTANT  — Should fix. Significant tech debt, error handling gap, or performance issue.
💡 SUGGESTION — Optional improvement. Readability, style, or minor refactor.
❓ QUESTION   — I don't understand this. Please explain or clarify.
✅ PRAISE     — This is good. Explicitly call out well-written code.
```

**Always explain why, not just what:**
```
❌ Bad review comment:
   "This is wrong."

✅ Good review comment:
   "⚠️ IMPORTANT: This will silently fail if `user` is null — the optional chaining
   (?.) prevents the TypeError but returns undefined, which then gets passed to
   formatName() and causes a different error downstream. Suggest adding a null
   guard here: if (!user) return null; and handling the null case at the call site."
```

### The Minimal-Diff Principle

When fixing bugs or reviewing code, make the **smallest possible change** that fixes the root cause.

```javascript
// Bad fix: rewrites the whole function "while I'm here"
// Now it's impossible to review what actually changed

// Good fix: surgical, targeted change
// Before:
const total = items.reduce((sum, item) => sum + item.price, 1); // BUG: starts at 1

// After:
const total = items.reduce((sum, item) => sum + item.price, 0); // fix: start at 0
```

Minimal diffs are:
- Easier to review
- Easier to revert if the fix introduced a regression
- Easier to understand in git history six months later

---

## Phase 6: Security Review Checklist

Security bugs are bugs with adversaries. Review these explicitly on every PR that touches authentication, data access, or external input.

### Input Validation (Every External Input is Hostile)

```javascript
// SQL Injection — never concatenate user input into queries
const query = `SELECT * FROM users WHERE email = '${email}'`; // CRITICAL: injectable

// Fix: parameterized queries — always
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [email]);

// XSS — never insert user content as raw HTML
element.innerHTML = userComment;  // CRITICAL: executes scripts

// Fix: use textContent or a sanitization library
element.textContent = userComment;  // safe: treats as text, not HTML
```

### Authentication & Authorization

```
Checklist:
  ✓ Is this endpoint/function protected by authentication?
  ✓ Is authorization checked per resource, not just per route?
    (User A shouldn't access User B's data even if both are authenticated)
  ✓ Are tokens validated on every request, not just at login?
  ✓ Are session tokens invalidated on logout?
  ✓ Is rate limiting applied to auth endpoints?
  ✓ Are passwords hashed with bcrypt/argon2, not MD5/SHA1?
  ✓ Are sensitive values (tokens, passwords) excluded from logs?
```

### Secrets & Credentials

```
Never in code:
  ✗ API keys hardcoded in source
  ✗ Passwords in config files committed to git
  ✗ Database credentials in .env files committed to repo
  ✗ Private keys in any file tracked by version control

Always:
  ✓ Use environment variables injected at runtime
  ✓ Use a secrets manager (AWS Secrets Manager, Vault, etc.) for production
  ✓ Add .env to .gitignore before first commit
  ✓ Rotate any credential that was ever committed — it's compromised

# Check for accidental commits
git log --all --full-history -- "**/.env"
git log -S "password" --source --all
```

### Dependency Vulnerabilities

```bash
# JavaScript
npm audit
npm audit fix

# Python
pip-audit
safety check

# Check for outdated packages with known CVEs before shipping
```

---

## Phase 7: Performance Debugging

### Finding the Bottleneck

Never optimize without measurement. Optimizing the wrong thing is wasted effort.

```
Performance debugging process:
  1. Measure — establish baseline with real data, not toy examples
  2. Profile — find where time is actually spent (not where you think it is)
  3. Identify — is it CPU, memory, I/O, or network?
  4. Fix — the actual bottleneck, not what looks suspicious
  5. Measure again — verify the improvement is real
```

### Common Performance Anti-Patterns

```javascript
// N+1 query — the most common backend performance killer
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findAll({ where: { userId: user.id } }); // N queries
}
// Fix: eager load with JOIN
const users = await User.findAll({ include: [Order] }); // 1 query

// Unnecessary re-computation in loops
const items = getItems();
for (let i = 0; i < items.length; i++) {
  const config = loadConfig();  // BUG: called N times, should be once
  process(items[i], config);
}
// Fix: hoist invariants out of loops
const config = loadConfig();
for (const item of items) {
  process(item, config);
}

// Memory leak — event listener never removed
window.addEventListener('resize', handler);  // added on component mount
// Fix: remove on unmount
useEffect(() => {
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler); // cleanup
}, []);
```

### Profiling Tools by Language

```
JavaScript (Browser):
  - Chrome DevTools → Performance tab → record → flame chart
  - Memory tab → heap snapshot → compare before/after suspected leak
  - Network tab → waterfall → find slow or blocking requests

JavaScript (Node.js):
  - node --prof app.js → generates v8 log
  - clinic.js (clinic doctor / clinic flame)
  - 0x for flame graphs

Python:
  - cProfile: python -m cProfile -o output.prof script.py
  - snakeviz output.prof  (visual flame graph)
  - memory_profiler: @profile decorator for line-by-line memory
  - py-spy: sampling profiler, attaches to running process

General:
  - Always profile with production-like data volume
  - Never trust micro-benchmarks for system-level decisions
```

---

## Phase 8: Debugging Difficult Scenarios

### Intermittent / Flaky Bugs

These are the hardest bugs and almost always fall into one category:

```
Intermittent bug causes (in order of frequency):
  1. Race condition — two async operations completing in unpredictable order
  2. Uninitialized state — code reads value before it's been set
  3. External dependency — API, database, or network behaving inconsistently
  4. Memory/resource exhaustion — only fails under load
  5. Floating point — calculations that are "almost right" most of the time
  6. Time-dependent — fails near midnight, on daylight saving change, on leap day

Investigation strategy:
  1. Add structured logging BEFORE the suspected failure point
  2. Include timestamp, process ID, thread ID, and full state snapshot
  3. Deploy to staging and run load test / wait for natural reproduction
  4. When it reproduces, the log tells the story
```

### "Works on My Machine" Bugs

```
Systematic comparison checklist:
  Runtime versions:   node --version / python --version
  Dependency versions: cat package-lock.json / pip freeze
  Environment vars:   printenv | sort (compare dev vs prod)
  OS differences:     file path separators, line endings (CRLF vs LF), timezone
  Database state:     schema version, seed data, migration state
  External services:  are dev and prod pointing to the same API endpoints?

Most common culprits:
  - Node/Python version mismatch (feature doesn't exist in older version)
  - package-lock.json not committed — different versions installed
  - Environment variable missing in production
  - Timezone set to local on dev, UTC on prod (date calculations differ)
  - Case-sensitive filesystem (Mac: case-insensitive, Linux: case-sensitive)
```

### Production-Only Bugs

When you can't reproduce locally and can't attach a debugger:

```
Strategy:
  1. Add structured logging at every decision point (not just errors)
     Log: input values, branch taken, output values, timing
  2. Use feature flags to isolate — disable one subsystem at a time
  3. Check monitoring: when did it start? what changed at that time?
     (Deploys, config changes, traffic spikes, dependency updates)
  4. Reproduce on staging with production data snapshot if possible
  5. If all else fails: add verbose logging, deploy, collect evidence,
     fix with evidence. Never blindly push fixes to production.
```

---

## Phase 9: Writing Good Error Messages

The quality of error messages determines how quickly future bugs are fixed. Good errors are self-diagnosing.

### Anatomy of a Good Error Message

```
✅ Good error:
   "Failed to process payment for order #4821: charge API returned
   'insufficient_funds' for card ending in 4242. User ID: 9983.
   Timestamp: 2024-01-15T14:32:11Z"

❌ Bad errors:
   "Something went wrong"
   "Error processing request"
   "Unexpected error occurred"
   "null"
   (silence — error swallowed entirely)
```

**A good error message contains:**
1. **What** failed (the operation)
2. **Why** it failed (the specific reason)
3. **Where** it failed (file, function, ID, timestamp)
4. **Context** that helps diagnose it (IDs, values, state)
5. **What to do** next (if actionable)

### Error Handling Patterns

```javascript
// Layered error handling — errors get context added as they bubble up
class PaymentError extends Error {
  constructor(message, { orderId, userId, code } = {}) {
    super(message);
    this.name = 'PaymentError';
    this.orderId = orderId;
    this.userId = userId;
    this.code = code;
  }
}

// Add context as error propagates upward
async function processPayment(orderId, userId) {
  try {
    return await chargeCard(getCardForUser(userId), getOrderTotal(orderId));
  } catch (err) {
    throw new PaymentError(
      `Payment failed for order ${orderId}: ${err.message}`,
      { orderId, userId, code: err.code }
    );
  }
}

// At the top level: log full context, send user a clean message
try {
  await processPayment(orderId, userId);
} catch (err) {
  logger.error('Payment processing failed', {
    error: err.message,
    orderId: err.orderId,
    userId: err.userId,
    stack: err.stack
  });
  return res.status(402).json({ error: 'Payment could not be processed.' });
  // User gets clean message. Developer gets full context in logs.
}
```

---

## Phase 10: Testing as a Debugging Tool

Every bug you fix should produce a test. This is not optional — it is how you prove the fix works and prevent regression.

### Write the Test Before the Fix

```javascript
// 1. Write a failing test that captures the bug
it('should return 0 for empty cart, not throw', () => {
  expect(calculateTotal([])).toBe(0);  // this fails — proves the bug exists
});

// 2. Fix the code
function calculateTotal(items) {
  if (!items || items.length === 0) return 0;  // handle empty case
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 3. Test passes — proves the fix works
// 4. Test stays in the suite — prevents future regression
```

### What to Test After Debugging

For every bug fixed, write tests covering:
- The exact scenario that caused the bug (regression test)
- The boundary condition that exposed it (empty, null, zero, max value)
- At least one "normal" path to confirm you didn't break the happy path

### Test Quality Rules

```javascript
// Tests should be DAMP (Descriptive and Meaningful Phrases), not DRY
// Readable test names tell the story of what's being tested

// Bad test name
it('test1', () => { ... })
it('handles error', () => { ... })

// Good test name
it('returns empty array when no items match the filter', () => { ... })
it('throws PaymentError when card is declined, preserving order ID', () => { ... })

// Each test: one assertion, one scenario
// If a test can fail for two different reasons, split it into two tests
```

---

## Anti-Patterns: The Debugging Hall of Shame

| ❌ Don't | ✅ Do Instead |
|---|---|
| Change multiple things at once | One change at a time, verify after each |
| Add try/catch to hide the error | Fix the root cause; log errors properly |
| `console.log` then forget to remove | Use a proper logger with log levels |
| Assume you know the variable's value | Verify with logging or debugger |
| Fix the symptom, not the root cause | Ask "why" 5 times before touching code |
| Optimize without profiling first | Measure, profile, then optimize the bottleneck |
| Delete code hoping the bug disappears | Understand why before removing anything |
| "It works, don't touch it" | All code must be understandable and testable |
| Write fix without a regression test | Always write the test that proves the fix |
| Hard-code credentials to "test quickly" | Never — rotate any secret that touched code |
| Review code for style only | Review for correctness, security, and errors first |
| Vague error messages ("error occurred") | Specific, contextual, actionable error messages |
| Suppress warnings as noise | Warnings are almost always future bugs — fix them |

---

## Pre-Ship Checklist

### Correctness
- [ ] The bug is reproducible and the fix targets the root cause, not the symptom
- [ ] A regression test exists that fails before the fix and passes after
- [ ] Edge cases tested: null/undefined/empty input, zero, negative, max values
- [ ] All existing tests still pass

### Code Quality
- [ ] Each function does one thing — no hidden side effects
- [ ] Names accurately describe what things are and do
- [ ] Non-obvious logic has a comment explaining *why*, not *what*
- [ ] No dead code, commented-out code blocks, or debug logging left in
- [ ] Error handling is explicit — no bare except/catch blocks

### Security
- [ ] No user input concatenated into SQL queries, shell commands, or HTML
- [ ] No credentials, tokens, or secrets in source code
- [ ] Authorization is checked, not just authentication
- [ ] Dependency vulnerability scan run (`npm audit` / `pip-audit`)

### Performance
- [ ] No N+1 queries introduced
- [ ] No expensive operations inside loops that could be hoisted
- [ ] No new memory leaks (event listeners, timers, closures with large captures)

### Observability
- [ ] Errors are logged with enough context to diagnose in production
- [ ] New code paths have logging at appropriate severity levels
- [ ] Sensitive data (passwords, tokens, PII) is excluded from logs

---

## Quick Reference: Debugging Decision Tree

```
Bug reported or error encountered
│
├── Is there an error message?
│   ├── Yes → Read it fully. Note type, message, file, line, stack.
│   │         Trace stack upward — root cause is often higher up.
│   └── No  → It's a logic error. Add logging to find where
│             behavior diverges from expectation.
│
├── Can you reproduce it?
│   ├── Yes → Reduce to minimal reproduction case. Proceed.
│   └── No  → Add logging at decision points. Wait for reproduction.
│             It's likely concurrency, timing, or environment.
│
├── Do you know where it fails?
│   ├── Yes → Inspect actual variable values at that point.
│   │         Verify — don't assume — what they contain.
│   └── No  → Binary search: add checkpoints at midpoints to bisect.
│
├── Do you know why it fails?
│   ├── Yes → Form explicit hypothesis. Test with one change.
│   └── No  → Check: what changed recently? (git log)
│             What are the assumptions? Which one is violated?
│
├── Fix applied — does it work?
│   ├── Yes → Write regression test. Code review. Ship.
│   └── No  → Revert. Hypothesis was wrong.
│             Eliminate it and form a new one.
│
└── Is the fix at the root cause?
    ├── Yes → Verify with 5 Whys. Add test. Done.
    └── No  → You fixed a symptom. The bug will return.
              Keep asking why until you reach the origin.
```

---

> **The best debuggers are not the ones who fix bugs the fastest. They are the ones who understand bugs the most deeply — because those fixes never come back.**
