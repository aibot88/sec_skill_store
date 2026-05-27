---
name: chrome-ext-security
description: >
  This skill should be used when working on security aspects of a Chrome extension or when
  the user asks about Chrome extension security best practices. Trigger when: implementing
  Content Security Policy in extensions, "extension CSP", "eval in extension", "content script
  security", "extension XSS", "remote code in extension", "MV3 security", "unsafe-eval",
  "content script isolation", "DOM safety in extension", "Trusted Types", "extension sandbox",
  "chrome extension security audit", "innerHTML in extension", "message validation".
---

# Chrome Extension Security

MV3 enforces a strict security model. All executable code must be bundled locally. The Content Security Policy bans `eval()` and remote scripts. Content scripts operate in an isolated world but share a DOM with potentially hostile pages. The service worker is the trusted core — all messages from content scripts must be validated.

## Hard Security Rules

### Remote Code Ban
All executable JavaScript must be bundled locally within the extension package. No fetching scripts from CDNs, no dynamically loaded SDKs. Violating this triggers **Blue Argon** CWS rejection.

### eval() and String-to-Code Prohibition
These are banned in standard extension contexts:
- `eval()`
- `new Function(string)`
- `setTimeout(string)` / `setInterval(string)`

**Escape hatches for legitimate needs:**
- `userScripts` API (Chrome 120+) for user script managers
- Sandboxed iframes (no Chrome API access)
- `wasm-unsafe-eval` in CSP for WebAssembly

### Content Security Policy (MV3)
Declared as an object (not a string). No remote domains in `script-src`, `worker-src`, `object-src`, or `style-src`:

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'",
    "sandbox": "sandbox allow-scripts; script-src 'self' 'unsafe-eval'"
  }
}
```

### Code Obfuscation Ban
Standard minification (whitespace removal, variable shortening) is allowed. Base64 encoding logic, character encoding to hide functionality, or other obfuscation triggers **Red Titanium** rejection.

## Trust Boundaries

### Content Scripts Are Untrusted
Content scripts share an execution environment with potentially malicious web pages. The service worker must:
- Validate and sanitize ALL messages received from content scripts
- Never pass content script data to `eval()`, `innerHTML`, or other injection sinks
- Treat content script messages like untrusted user input at an API boundary

### DOM Injection Safety
When injecting UI into web pages:
- Use `textContent` or `innerText` instead of `innerHTML` for text
- Use `document.createElement()` for DOM construction
- Enforce Trusted Types API when handling HTML
- Mount injected UI inside Shadow DOM to isolate from host page

### Network Request Security
- Content script `fetch()` calls are subject to host page CSP
- Proxy sensitive network requests through the service worker
- Use HTTPS for all data transmission
- Never put sensitive data in URL query parameters or headers (leaks into server logs)

### Third-Party Library Risks
NPM packages may internally use `eval()` or `new Function()`. This violates MV3 CSP and causes CWS rejection. Audit dependencies for:
- Dynamic code execution
- Inline script injection
- Remote resource loading

Isolate unavoidable dynamic code in sandboxed iframes.

## Additional Resources

### Reference Files

- **`references/csp-rules.md`** — Complete CSP configuration guide for MV3 extensions
- **`references/dom-safety.md`** — Detailed DOM injection patterns, Trusted Types, and XSS prevention
