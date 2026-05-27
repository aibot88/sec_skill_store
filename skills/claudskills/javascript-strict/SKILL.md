---
name: javascript-strict
description: >
  JavaScript (Node.js) strictness, clean code, and security rules. Use when writing,
  reviewing, or refactoring plain JavaScript (non-TypeScript) Node.js code. Covers
  const-first variable declarations, async/await patterns, class vs function patterns,
  JSDoc documentation, error handling, hot-path performance, CommonJS module patterns,
  and vulnerability prevention. Derived from production Node.js services.
---

# JavaScript Strict Standard

Rules extracted from production Node.js services (non-TypeScript).

## CRITICAL: Variable Declarations

### JS-01: const by default, let when necessary, never var

```javascript
// BAD
var count = 0;
var items = [];

// GOOD
const VALID_MODES = ['bypass', 'browser', 'capsolver'];  // Never changes
let activeCount = 0;  // Reassigned in loop
let currentDelay = baseDelay;  // Mutated by logic
```

No `var` anywhere.

### JS-02: Destructure at declaration

```javascript
// BAD
const name = config.name;
const port = config.port;
const mode = config.mode;

// GOOD
const { name, port, mode } = config;

// GOOD: with defaults
const { mode = 'both', delay = 1000 } = options;
```

## CRITICAL: Error Handling

### JS-03: Never catch and swallow errors

```javascript
// BAD
try { await save(); } catch (e) {}

// BAD: logs but no recovery
try { await save(); } catch (e) { console.log(e); }

// GOOD: context + action
try {
  await save();
} catch (err) {
  console.error(`[Monitor] ${this.monitorId} Save failed:`, err.message);
  await this.notifyError('save_failure', err.message);
  // Decide: retry, skip, or throw
}
```

### JS-04: Prefix error logs with context

```javascript
// BAD
console.error(err.message);

// GOOD
console.error(`[Monitor] ${this.monitorId} Error:`, err.message);
console.error(`[TokenBank] ${this.baseHost} Persist failed:`, err.message);
console.warn(`[DEPRECATED] MONITOR_BYPASS is deprecated, use TMPT_MODE`);
```

Format: `[Module] ${identifier} Action: message`

### JS-05: Avoid recursive retry without limits

```javascript
// BAD: infinite recursion on persistent failure
async getTmpt() {
  try {
    const token = await this.tmptBank.getTmpt();
    if (!token) { await sleep(1000); return this.getTmpt(); }
    return token;
  } catch {
    await sleep(1000);
    return this.getTmpt(); // STACK OVERFLOW on persistent failure
  }
}

// GOOD: bounded retries
async getTmpt(retries = 10) {
  for (let i = 0; i < retries; i++) {
    try {
      const token = await this.tmptBank.getTmpt();
      if (token) return token;
    } catch (err) {
      console.error(`[Monitor] getTmpt attempt ${i + 1}/${retries}:`, err.message);
    }
    await sleep(1000 * Math.min(i + 1, 5)); // Backoff
  }
  throw new Error(`Failed to get TMPT after ${retries} attempts`);
}
```

## CRITICAL: Async Patterns

### JS-06: async/await over raw Promises

```javascript
// BAD
function fetchData() {
  return fetch(url).then(r => r.json()).then(data => process(data)).catch(handleError);
}

// GOOD
async function fetchData() {
  const response = await fetch(url);
  const data = await response.json();
  return process(data);
}
```

### JS-07: Promise.race for timeouts

```javascript
function withTimeout(promise, ms, message = 'Timeout') {
  let timeoutId;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutId = setTimeout(() => reject(new Error(message)), ms);
  });
  return Promise.race([promise, timeoutPromise])
    .finally(() => clearTimeout(timeoutId)); // ALWAYS clean up
}

// Usage
const data = await withTimeout(fetch(url), 5000, 'Request timed out');
```

Always `.finally()` to clear the timeout: prevents dangling timers.

### JS-08: Async file I/O only

```javascript
// BAD: blocks event loop 5-50ms
fs.writeFileSync(path, JSON.stringify(data, null, 2));

// GOOD
await fs.promises.writeFile(path, JSON.stringify(data, null, 2));

// BETTER: skip if unchanged
const json = JSON.stringify(data, null, 2);
const hash = crypto.createHash('md5').update(json).digest('hex');
if (hash !== this._lastHash) {
  await fs.promises.writeFile(path, json);
  this._lastHash = hash;
}
```

## HIGH: Module Patterns

### JS-09: CommonJS with clear exports

```javascript
// Single class export
class Monitor { ... }
module.exports = Monitor;

// Named function exports
module.exports = {
  addMonitor: async (data) => { ... },
  getMonitor: async (id) => { ... },
  updateMonitor: async (id, updates) => { ... },
};

// Utility exports
const { sleep, withTimeout, shouldRun } = require('./utils');
module.exports = { sleep, withTimeout, shouldRun };
```

### JS-10: No circular dependencies

If A requires B and B requires A, extract shared logic into C.

## HIGH: Class Patterns

### JS-11: Classes for stateful objects, functions for utilities

```javascript
// GOOD: class for stateful service
class Monitor {
  constructor(monitorData, tmptBank, mode = 'both') {
    this.monitorId = monitorData.id;
    this.tmptBank = tmptBank;
    this.mode = mode;
    this.stopped = false;
    this.delay = 100;
    this.notifiedListings = new Set(); // Use Set, not Array
  }

  async start() { ... }
  async stop() { this.stopped = true; }
}

// GOOD: plain functions for stateless utilities
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function formatProxy(line) {
  const [host, port, user, pass] = line.split(':');
  return `http://${user}:${pass}@${host}:${port}`;
}
```

## HIGH: Documentation (JSDoc)

### JS-12: JSDoc for all public methods

```javascript
/**
 * Makes an HTTP request with TMPT error handling and retry logic.
 * @param {Object} config - Request configuration
 * @param {string} config.url - Target URL
 * @param {string} [config.method='GET'] - HTTP method
 * @param {Object} [config.headers] - Additional headers
 * @param {number} [config.timeout=5000] - Timeout in milliseconds
 * @returns {Promise<Object>} Response object with data and status
 * @throws {Error} If request fails after retries
 */
async makeRequest(config) { ... }
```

Essential for non-TypeScript codebases: provides IDE autocomplete and documentation.

## MEDIUM: Performance Rules

### JS-13: Set for membership, Map for lookups

```javascript
// BAD: O(n) per check
const newIds = currentIds.filter(x => !savedIds.includes(x));

// GOOD: O(1) per check
const savedSet = new Set(savedIds);
const newIds = currentIds.filter(x => !savedSet.has(x));
```

### JS-14: Single-pass algorithms in hot paths

```javascript
// BAD: 3 passes, 3 arrays
const available = tokens.filter(t => !t.expired);
available.sort((a, b) => a.lastUsed - b.lastUsed);
const best = available[0];

// GOOD: 1 pass, 0 arrays
let best = null;
for (const t of tokens) {
  if (t.expired) continue;
  if (!best || t.lastUsed < best.lastUsed) best = t;
}
```

### JS-15: Cache expensive computations

```javascript
// BAD: regex + split every call
function getProxy() {
  const proxies = source.split(/\r?\n/);
  return proxies[Math.floor(Math.random() * proxies.length)].split(':');
}

// GOOD: parse once
class ProxyPool {
  constructor(source) {
    this.urls = source.split(/\r?\n/).filter(Boolean).map(formatProxy);
  }
  random() { return this.urls[Math.floor(Math.random() * this.urls.length)]; }
}
```

### JS-16: Index Maps for frequent lookups

```javascript
// BAD: O(n) find per lookup
function findToken(value) {
  return this.tokens.find(t => t.value === value);
}

// GOOD: O(1) Map lookup
this.tokenIndex = new Map(tokens.map(t => [t.value, t]));
function findToken(value) {
  return this.tokenIndex.get(value);
}
```

## Security Rules

### JS-17: Never eval() or Function()

```javascript
// BAD: code injection
eval(userInput);
new Function(userInput)();

// GOOD: use safe alternatives
JSON.parse(jsonString);
```

### JS-18: Never innerHTML with user data

```javascript
// BAD: XSS
element.innerHTML = `<p>${userInput}</p>`;

// GOOD
element.textContent = userInput;
```

### JS-19: Environment variables for secrets

```javascript
// BAD: in source code
const API_KEY = 'sk-abc123...';

// GOOD
require('dotenv').config();
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error('API_KEY required');
```

### JS-20: Mask secrets in logs

```javascript
// BAD
console.log(`Token: ${token}`);

// GOOD
console.log(`Token: ${token.slice(0, 8)}...`);
```

### JS-21: Be cautious with NODE_TLS_REJECT_UNAUTHORIZED

```javascript
// DANGER: disables SSL verification globally
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// BETTER: per-request agent with custom CA
const agent = new https.Agent({ rejectUnauthorized: false });
// Only use for proxy connections, never for production APIs
```

### JS-22: AbortController for cancellable fetch and timeouts

```javascript
// BAD: no way to cancel; the fetch leaks if the caller goes away
const data = await fetch(url).then(r => r.json());

// GOOD: timeout + caller-driven cancellation
async function fetchJSON(url, { signal, timeoutMs = 5000 } = {}) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(new Error('timeout')), timeoutMs);
  signal?.addEventListener('abort', () => ctrl.abort(signal.reason));
  try {
    const res = await fetch(url, { signal: ctrl.signal });
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}
```

Replaces the `Promise.race` timeout pattern in modern Node.

### JS-23: `crypto.randomBytes` for tokens, never `Math.random`

```javascript
// BAD: predictable, seedable, not for security
const token = Math.random().toString(36).slice(2);

// GOOD: cryptographically random
const { randomBytes } = require('node:crypto');
const token = randomBytes(32).toString('hex');
```

Same rule for session IDs, password reset tokens, nonces, and salts.

## Runtime Targets

- **Node.js 24 LTS "Krypton"** is the current Active LTS, supported through April 2028. Latest patch line is 24.15.x. New projects target Node 24.
- **Release schedule change** (announced Oct 2026 cycle): one major release per year (April), every release becomes LTS after the October promotion. Plan upgrades around April + October windows.
- **Native TypeScript stripping** is unflagged default since Node 23.6, available throughout 24.x. `--experimental-transform-types` still required for enums/namespaces (which `erasableSyntaxOnly` in TS bans anyway).

### JS-24a: Use stdlib over third-party where Node has shipped equivalents

| Replace | With (Node 22+) |
|---|---|
| `dotenv` | `node --env-file=.env`, or `process.loadEnvFile()` |
| `node-fetch`, `axios` (for simple cases) | global `fetch`, `Request`, `Response`, `Headers` |
| `ws` (server) | global `WebSocket` (client) / `node:ws` patterns |
| `mocha`, `jest` (for libs without React) | `node:test` + `node --test` |
| `glob` | `fs.glob` / `fs.globSync` |
| `better-sqlite3` (for simple use) | `node:sqlite` |

Smaller `node_modules`, less supply-chain surface, fewer compatibility bugs across runtimes.

### JS-24b: `--permission` for sandboxed processes

```bash
node --permission \
     --allow-fs-read=/app \
     --allow-fs-write=/app/tmp \
     --allow-net=api.example.com \
     server.js
```

Restricts what filesystem paths and network targets the process can touch. Useful for plugin runners, untrusted code, or hardening prod entrypoints. Still flagged experimental in Node 24, treat as defense-in-depth.

### JS-25: Stream large I/O, do not buffer

```javascript
// BAD: loads entire file into memory
const data = await fs.promises.readFile('huge.csv');
process(data);

// GOOD: stream + pipeline (handles backpressure and errors)
const { pipeline } = require('node:stream/promises');
const { createReadStream, createWriteStream } = require('node:fs');

await pipeline(
  createReadStream('huge.csv'),
  parseCsv(),
  transform(),
  createWriteStream('out.json'),
);
```

Anything over a few MB or coming from the network should stream.

## Vulnerability Checklist

- [ ] No `var` declarations (const/let only)
- [ ] No `eval()` or `new Function()`
- [ ] No `innerHTML` with user-controlled data
- [ ] No `writeFileSync` in event loop (use async)
- [ ] No recursive retries without bounds
- [ ] No unbounded arrays for membership checks (use Set)
- [ ] All errors caught and logged with context
- [ ] Secrets in .env, not source code
- [ ] Tokens/credentials masked in logs
- [ ] JSDoc on all public methods
- [ ] `NODE_TLS_REJECT_UNAUTHORIZED` only for proxy, never production
