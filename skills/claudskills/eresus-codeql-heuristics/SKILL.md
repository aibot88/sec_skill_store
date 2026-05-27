---
name: eresus-codeql-heuristics
description: >
  Language-specific vulnerability hotspot reference for manual code audit.
  Trigger when the user asks to: "what sinks should I look for in Java?", "Python security hotspots",
  "dangerous functions in Go", "JavaScript injection patterns",
  or when starting a manual audit of a specific language and needing a sink/source checklist.
metadata:
  version: "1.0"
  domain: application-security
  mode: reference
  persona: security-researcher
---

# CodeQL-Informed Audit Heuristics

## Purpose

Provide a language-specific reference of dangerous sinks, sources, and patterns that
security auditors should prioritize during manual code review. These heuristics are derived
from the CodeQL Community Packs — the same query suites used by GitHub Advanced Security
to find real vulnerabilities at scale.

Use this skill as a **checklist companion** during manual audit. It tells you **what to look for**
in each language. The actual manual reasoning is done by `eresus-manual-security-audit`.

---

## Java / Kotlin

### Command Injection
- `Runtime.exec()`, `ProcessBuilder.command()`
- `Runtime.getRuntime().exec(userInput)`

### JNDI Injection
- `InitialContext.lookup(userInput)`
- `Context.lookup()` with attacker-controlled LDAP/RMI URLs

### Expression Language Injection
- `SpELExpressionParser.parseExpression(userInput)`
- `OGNL.getValue(userInput)`
- `MVEL.eval(userInput)`

### SQL Injection
- `Statement.execute(query)` with string concatenation
- `Statement.executeQuery("SELECT ... " + userInput)`
- JPA `createNativeQuery()` with interpolated strings
- MyBatis `${}` (raw) vs `#{}` (parameterized)

### Deserialization
- `ObjectInputStream.readObject()`
- `XStream.fromXML()`
- `Kryo.readObject()`
- Jackson `@JsonTypeInfo` with `MINIMAL_CLASS` / `CLASS`

### XXE
- `DocumentBuilderFactory` without `setFeature(XMLConstants.FEATURE_SECURE_PROCESSING)`
- `SAXParserFactory` without disabling external entities
- `XMLInputFactory` without disabling DTDs

### Unsafe Reflection
- `Class.forName(userInput).newInstance()`
- `Method.invoke()` with user-controlled method names

### Path Traversal
- `new File(basePath + userInput)` without canonicalization
- `Paths.get(userInput)` without restricting to base directory

---

## Python

### Command Injection
- `os.system(userInput)`
- `subprocess.Popen(userInput, shell=True)`
- `subprocess.call(userInput, shell=True)`
- `os.popen(userInput)`

### Code Injection
- `eval(userInput)`
- `exec(userInput)`
- `compile(userInput, ...)`

### Deserialization
- `pickle.loads(userInput)`
- `pickle.load(untrustedFile)`
- `yaml.load(userInput)` — safe: `yaml.safe_load()`
- `shelve.open(userInput)`
- `marshal.loads(userInput)`

### Template Injection (SSTI)
- `jinja2.Template(userInput).render()`
- `jinja2.Environment(autoescape=False)`
- `mako.template.Template(userInput)`

### SQL Injection
- `cursor.execute("SELECT ... " + userInput)`
- Django `extra()`, `raw()`, `RawSQL()` with user input
- SQLAlchemy `text(userInput)`

### Path Traversal
- `open(basePath + userInput)`
- Flask `send_file(userInput)`
- FastAPI `FileResponse(userInput)`
- `os.path.join(base, userInput)` without `os.path.realpath()` check

### SSRF
- `requests.get(userInput)`
- `urllib.request.urlopen(userInput)`

---

## JavaScript / TypeScript

### Code Injection
- `eval(userInput)`
- `Function(userInput)()`
- `setTimeout(userInput, ms)` (string form)
- `setInterval(userInput, ms)` (string form)
- `vm.runInNewContext(userInput)`
- `vm.runInThisContext(userInput)`

### Command Injection
- `child_process.exec(userInput)`
- `child_process.execSync(userInput)`
- `` child_process.exec(`cmd ${userInput}`) ``

### XSS / DOM Injection
- `element.innerHTML = userInput`
- `element.outerHTML = userInput`
- `document.write(userInput)`
- `insertAdjacentHTML('beforeend', userInput)`
- React: `dangerouslySetInnerHTML={{ __html: userInput }}`
- Vue: `v-html="userInput"`
- Angular: `bypassSecurityTrustHtml(userInput)`

### Prototype Pollution
- `lodash.merge({}, userInput)`
- `lodash.set(obj, userInput.key, userInput.value)`
- `Object.assign(target, JSON.parse(userInput))`
- Deep clone/merge with `__proto__`, `constructor.prototype` keys

### NoSQL Injection
- MongoDB `$where: userInput`
- `collection.find({ field: userInput })` when userInput is `{ $gt: "" }`
- `collection.find(JSON.parse(userInput))`

### Path Traversal
- `path.join(base, userInput)` without `path.resolve()` + prefix check
- `fs.readFile(userInput)`
- Express `res.sendFile(userInput)`

### postMessage
- `window.addEventListener('message', handler)` without `event.origin` check

### SSRF
- `fetch(userInput)`, `axios.get(userInput)`, `got(userInput)`
- URL construction: `fetch(\`/api/${userInput}\`)`

---

## Go

### Command Injection
- `exec.Command(userInput)`
- `exec.CommandContext(ctx, userInput)`
- `os.StartProcess(userInput, ...)`

### SQL Injection
- `db.Query("SELECT ... " + userInput)`
- `db.Exec("INSERT INTO ... " + userInput)`
- `fmt.Sprintf("SELECT ... %s", userInput)` passed to `db.Query()`

### Template Injection
- `text/template` (NO auto-escaping) vs `html/template` (auto-escapes)
- `template.HTML(userInput)` explicitly marking user input as safe

### Path Traversal
- `filepath.Join(base, userInput)` — does NOT prevent `../`
- `os.Open(userInput)` without validation
- Need: `filepath.Rel()` or prefix check after `filepath.Clean()`

### TLS Misconfiguration
- `InsecureSkipVerify: true`
- `MinVersion: tls.VersionTLS10`

### SSRF
- `http.Get(userInput)`
- `http.NewRequest("GET", userInput, nil)`

---

## Ruby

### Command Injection
- `system(userInput)`
- `` `#{userInput}` `` (backticks)
- `IO.popen(userInput)`
- `Open3.capture3(userInput)`
- `Kernel.exec(userInput)`

### Deserialization
- `Marshal.load(userInput)` — RCE via universal gadget chain
- `YAML.load(userInput)` — RCE via Psych → safe: `YAML.safe_load()`
- `Oj.load(userInput, mode: :object)` — safe: `mode: :strict`
- `Ox.load(userInput, mode: :object)` — safe: `mode: :generic`

### SQL Injection
- `ActiveRecord: .where("column = '#{userInput}'")`
- `ActiveRecord: .order(userInput)`
- `ActiveRecord: .pluck(userInput)`
- `ActiveRecord: .select(userInput)`

### Dynamic Dispatch
- `object.send(userInput)` — calls any method
- `object.public_send(userInput)` — calls any public method

### Template Injection
- `ERB.new(userInput).result(binding)`
- `Slim::Template.new { userInput }`

### Path Traversal
- `File.read(params[:file])`
- `send_file(params[:path])`

---

## C# / .NET

### Deserialization
- `BinaryFormatter.Deserialize(stream)` — **banned in .NET 9+**
- `SoapFormatter.Deserialize(stream)`
- `NetDataContractSerializer.ReadObject(reader)`
- `ObjectStateFormatter.Deserialize(input)`
- `LosFormatter.Deserialize(input)`
- `XmlSerializer` with polymorphic `[XmlInclude]` types

### Command Injection
- `Process.Start(userInput)`
- `Process.Start("cmd.exe", "/c " + userInput)`

### SQL Injection
- `new SqlCommand("SELECT ... " + userInput)`
- `cmd.CommandText = "SELECT ... " + userInput`
- EF Core `FromSqlRaw("SELECT ... " + userInput)`

### XSS
- `HtmlString(userInput)` — bypasses Razor encoding
- `Html.Raw(userInput)`

### Unsafe Reflection
- `Type.GetType(userInput)`
- `Activator.CreateInstance(Type.GetType(userInput))`

### Path Traversal
- `Path.Combine(basePath, userInput)` without canonicalization
- `File.ReadAllText(userInput)`

---

## C / C++

### Buffer Overflow
- `strcpy(dst, src)` — safe: `strncpy()`, `strlcpy()`
- `strcat(dst, src)` — safe: `strncat()`
- `sprintf(buf, fmt, ...)` — safe: `snprintf()`
- `gets(buf)` — **never safe**, removed in C11

### Format String
- `printf(userInput)` — safe: `printf("%s", userInput)`
- `fprintf(fp, userInput)`
- `syslog(priority, userInput)`

### Integer Overflow
- `malloc(count * size)` without overflow check
- `size_t` arithmetic wrapping to zero
- Signed/unsigned comparison mismatches

### Memory Safety
- Use-after-free: accessing memory after `free()`
- Double-free: calling `free()` twice on same pointer
- Null dereference: missing NULL checks after `malloc()`

### Command Injection
- `system(userInput)`
- `popen(userInput, "r")`
- `execvp(userInput, args)`

---

## Audit Priority Rules

When performing depth-first manual review, prioritize:

1. **Security-sensitive sinks** over style issues
2. **Exploitable paths** over theoretical vulnerabilities
3. **Business logic flaws** over pattern-match findings
4. **Trust boundary violations** over defense-in-depth gaps

---

## Tooling Constraints

Use ONLY these tools for code inspection:
- `view_file` — read source code
- `grep_search` — find pattern matches

Do NOT use terminal commands like `grep`, `rg`, `cat`, `sed`, or any shell-based tools.
