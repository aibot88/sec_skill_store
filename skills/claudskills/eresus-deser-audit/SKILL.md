---
name: eresus-deser-audit
description: >
  Deserialization vulnerability audit skill with gadget chain knowledge for all major languages.
  Trigger when the user asks to: "audit deserialization", "check for insecure deserialization",
  "find pickle vulnerabilities", "Marshal.load audit", "gadget chain analysis",
  "check for unsafe YAML loading", or when reviewing code that processes serialized data
  (JSON with type info, YAML, XML, binary formats).
metadata:
  version: "1.0"
  domain: application-security
  mode: deserialization-audit
  persona: exploit-developer
---

# Deserialization Vulnerability Audit

## Purpose

Perform a targeted audit of deserialization attack surfaces across any language.
This skill provides structured knowledge of dangerous deserialization sinks, safe alternatives,
gadget chain indicators, and a step-by-step exploitation methodology.

This is a **depth-first specialist skill** — it goes deeper on deserialization than the
general `eresus-manual-security-audit` skill. Use it when the target application processes
serialized data from untrusted sources.

---

## Universal Attack Methodology

### Step 1: Identify the Deserialization Sink

Search the codebase for functions that convert serialized data back into objects.
Use `grep_search` with these patterns per language:

**Java:** `ObjectInputStream`, `readObject`, `XStream`, `fromXML`, `Kryo`, `readClassAndObject`
**Python:** `pickle.load`, `pickle.loads`, `yaml.load`, `marshal.loads`, `shelve.open`
**Ruby:** `Marshal.load`, `YAML.load`, `Oj.load`, `Ox.load`
**PHP:** `unserialize`, `simplexml_load_string`
**.NET:** `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer`, `LosFormatter`
**Node.js:** `node-serialize`, `funcster`, `cryo`

### Step 2: Trace the Input Source

For each sink found, trace backwards to determine:
- Does the serialized data come from an untrusted source? (HTTP request, file upload, message queue, database)
- Is there any validation or type filtering before deserialization?
- Can the attacker control the full serialized payload or only parts of it?

### Step 3: Check for Type Control

The key question: **can the attacker control which class/type gets instantiated?**

- If the format allows arbitrary type specification (YAML tags, Java serialization, .NET TypeNameHandling),
  it is almost certainly exploitable
- If the format is type-restricted (JSON without polymorphism, `yaml.safe_load`), it may be safe

### Step 4: Identify Available Gadgets

Look for classes on the classpath/load path that have dangerous side effects during deserialization:
- Classes with `__reduce__` / `readObject` / `marshal_load` methods
- Classes that perform I/O, execute commands, or make network requests during construction
- Classes that invoke callbacks or proxy methods during deserialization

### Step 5: Build and Test

1. **Detection PoC first** — construct a callback-based payload (DNS/HTTP) that proves the sink
   processes attacker-controlled types
2. **RCE PoC second** — only after confirming the sink is exploitable, construct a command execution payload
3. **Document the chain** — show the full gadget chain from deserialized object to code execution

---

## Per-Language Reference

### Java

| Sink | Risk | Safe Alternative |
|------|------|-----------------|
| `ObjectInputStream.readObject()` | Critical — arbitrary class instantiation | `ObjectInputFilter` (Java 9+), allowlist |
| `XStream.fromXML()` | Critical — without type allowlist | `XStream.allowTypes()` or `XStream.setupDefaultSecurity()` |
| `Kryo.readObject()` | High — without registration | `kryo.setRegistrationRequired(true)` |
| `Jackson @JsonTypeInfo(use=CLASS)` | Critical — arbitrary class | `@JsonTypeInfo(use=NAME)` with allowlist |
| `SnakeYAML.load()` | Critical — arbitrary class via `!!` tags | `new SafeConstructor()` |

**Gadget chain indicators in Java:**
- Classes implementing `Serializable` with `readObject()` or `readResolve()`
- Proxy classes: `InvocationHandler`, `DynamicProxy`
- Known gadget libraries: Commons Collections, Commons BeanUtils, Spring, ROME

### Python

| Sink | Risk | Safe Alternative |
|------|------|-----------------|
| `pickle.loads(data)` | Critical — arbitrary code execution | `json.loads()`, Pydantic models |
| `pickle.load(file)` | Critical — arbitrary code execution | `json.load()`, Protocol Buffers |
| `yaml.load(data)` | Critical — arbitrary object instantiation | `yaml.safe_load(data)` |
| `shelve.open(path)` | Critical — uses pickle internally | Custom JSON-based storage |
| `marshal.loads(data)` | High — code object creation | `json.loads()` |

**Gadget chain indicators in Python:**
- Classes with `__reduce__()` or `__reduce_ex__()` methods
- The `os.system`, `subprocess.Popen` classes are directly invokable via `__reduce__`
- `pickle` can execute arbitrary code with just `__reduce__` returning `(os.system, ('cmd',))`

### Ruby

| Sink | Risk | Safe Alternative |
|------|------|-----------------|
| `Marshal.load(data)` | Critical — RCE via universal gadget chain | `JSON.parse(data)` |
| `YAML.load(data)` | Critical — RCE via Psych engine | `YAML.safe_load(data)` |
| `Oj.load(data, mode: :object)` | Critical — arbitrary object instantiation | `Oj.load(data, mode: :strict)` |
| `Ox.load(data, mode: :object)` | Critical — arbitrary object instantiation | `Ox.load(data, mode: :generic)` |

**Ruby universal gadget chain (works up to Ruby 3.3.x):**
- Based on William Bowling's research (vakzz)
- Detection: callback payload that hits an URL when processed by vulnerable sink
- RCE: uses `zip` command via GTFOBins technique
- Affects ALL four serialization libraries (Marshal, YAML/Psych, Oj, Ox)

### PHP

| Sink | Risk | Safe Alternative |
|------|------|-----------------|
| `unserialize($data)` | Critical — POP chain exploitation | `json_decode($data)` |
| `simplexml_load_string($data)` | High — XXE | `libxml_disable_entity_loader(true)` |

**Gadget chain indicators in PHP:**
- Classes with `__wakeup()`, `__destruct()`, `__toString()`, `__call()` magic methods
- POP (Property-Oriented Programming) chains via autoloaded classes
- Frameworks like Laravel, Symfony have known gadget chains

### .NET

| Sink | Risk | Safe Alternative |
|------|------|-----------------|
| `BinaryFormatter.Deserialize()` | Critical — **banned in .NET 9+** | `System.Text.Json` |
| `SoapFormatter.Deserialize()` | Critical | `System.Text.Json` |
| `NetDataContractSerializer` | Critical | `DataContractSerializer` with known types |
| `ObjectStateFormatter` | Critical — ViewState attacks | Encrypted/signed ViewState |
| `LosFormatter` | Critical | `System.Text.Json` |
| `JsonSerializer` with `TypeNameHandling.All` | Critical | `TypeNameHandling.None` |

**Gadget chain indicators in .NET:**
- Classes implementing `ISerializable`
- `OnDeserializing` / `OnDeserialized` attributes
- Known chains: `System.Windows.Data.ObjectDataProvider`, `System.Activities.*`

### Node.js

| Sink | Risk | Safe Alternative |
|------|------|-----------------|
| `node-serialize.unserialize()` | Critical — direct `eval()` | `JSON.parse()` |
| `funcster.deepDeserialize()` | Critical — function reconstruction | `JSON.parse()` |
| `cryo.parse()` | High — object reconstruction | `JSON.parse()`, `superjson` |

---

## Red Flags Checklist

When reviewing any deserialization code, check for these red flags:

- [ ] Serialized data comes from HTTP request body, headers, cookies, or query parameters
- [ ] Serialized data comes from message queues, webhooks, or external APIs
- [ ] Serialized data is stored in a database that may be compromised
- [ ] No type filtering or allowlisting before deserialization
- [ ] Using a serialization format that supports arbitrary type instantiation
- [ ] Using `pickle`, `Marshal`, `BinaryFormatter`, or `ObjectInputStream` with user data
- [ ] YAML loaded with `yaml.load()` instead of `yaml.safe_load()`
- [ ] JSON deserialization with type handling enabled (`@JsonTypeInfo`, `TypeNameHandling`)
- [ ] Session data stored in cookies using serialization (not encrypted/signed)
- [ ] ViewState without encryption and MAC validation

---

## Tooling Constraints

Use ONLY these tools:
- `view_file` — read source code to trace deserialization flows
- `grep_search` — find deserialization sinks across the codebase

Do NOT use terminal commands like `grep`, `rg`, `cat`, `sed`, or any shell tools.

---

## Integration

Use this skill when `eresus-manual-security-audit` or `eresus-sast-scanner` identifies
a deserialization entry point that needs deeper analysis.

This skill complements `eresus-serialization-review` which focuses on the broader
serialization attack surface (format confusion, schema validation, etc.).
