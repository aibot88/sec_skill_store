---
name: eresus-serialization-review
description: >
  Serialization and deserialization security review skill for object mappers, parser pipelines, message formats,
  and state transfer mechanisms. Trigger when the user asks to: "review serialization security", "check deserialization",
  "audit Jackson/Fastjson/YAML/XML parsing", "look for gadget-chain risk", "review session or message deserialization",
  or wants a focused audit of parser-driven attack surface. Complements eresus-sast-scanner with a deep dive on serialization abuse paths.
metadata:
  version: "1.0"
  domain: application-security
  mode: targeted-review
---

# Serialization Security Review

## Purpose

Find vulnerabilities caused by unsafe serialization, deserialization, object mapping, parser configuration,
and cross-boundary state transfer. Focus on cases where untrusted bytes, JSON, YAML, XML, cookies, view state,
cache blobs, or queue messages are turned into executable, privileged, or overly dynamic objects.

## High-Risk Targets

Prioritize:

- Java native serialization and `ObjectInputStream`
- Jackson polymorphic typing and unsafe default typing
- Fastjson auto-type behavior
- .NET `BinaryFormatter`, `LosFormatter`, `NetDataContractSerializer`
- PHP `unserialize()` and POP-chain entry points
- Python `pickle`, `marshal`, and unsafe YAML loaders
- Node parsers that revive functions, prototypes, or constructors
- session cookies, view state, queue payloads, cache entries, and signed blobs crossing trust boundaries

---

## Workflow

### Step 1: Find Deserialization Boundaries

Locate where external or semi-trusted data is parsed, decoded, revived, or reconstructed:

- HTTP body parsers
- cookies and session stores
- file import handlers
- webhook processors
- message queue consumers
- cache/database blob readers
- mobile/app local state restores

### Step 2: Classify the Input Trust Level

For each boundary, decide whether the input is:

- fully attacker-controlled
- user-controlled but signed/encrypted
- partner-controlled
- internal-only but reachable through weaker upstream systems

Do not assume "internal" means safe without an integrity guarantee.

### Step 3: Identify Dangerous Parser Features

Look for:

- polymorphic type resolution
- class-name-based instantiation
- automatic object revival
- unsafe YAML/XML object construction
- magic methods, hooks, or callbacks triggered after deserialization
- prototype pollution or constructor abuse
- gadget-friendly libraries on the classpath or dependency tree

### Step 4: Judge Exploitability

Confirm:

- the data crosses a trust boundary
- attacker influence reaches the parser
- type restrictions or integrity checks are absent, weak, or bypassable
- the resulting object graph has dangerous side effects or privileged behavior

### Step 5: Recommend Safe Patterns

Prefer:

- explicit DTO binding
- strict schemas
- allowlisted concrete types
- data-only formats without executable behavior
- integrity validation before parsing
- safe parser defaults and feature disablement

### Step 6: Report by Boundary

For each issue, state:

- boundary
- parser/serializer in use
- attacker control level
- impact
- exact hardening action

---

## Guardrails

- Do not report plain serialization for output-only responses as a vulnerability by itself.
- Do not assume every JSON parser use is dangerous; focus on dynamic typing, unsafe features, and trust boundaries.
- Do not treat signed data as safe if the signing key is weak, leaked, or validation happens after parsing.
- Do not forget secondary entry points such as queues, caches, or admin import tools.
- Do not stop at `deserialize()`; inspect post-deserialization hooks and object behavior.

---

## Output Format

Use:

```markdown
[SEVERITY] <serialization issue title>
Boundary: <entry point or state-transfer path>
File: <path>:<line>
Why it matters: <trust boundary + parser behavior + impact>
Fix: <concrete hardening action>
```
