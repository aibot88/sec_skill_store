---
name: cwe-79-xss
description: Use this skill when you need to remediate CWE-79 (Improper Neutralization of Input During Web Page Generation (XSS)) vulnerabilities in Java code. Triggers on SAST findings, security reviews, or when fixing improper neutralization of input during web page generation (xss) issues.
version: 1.0.0
license: MIT
tags:
- security
- java
- cwe-79
- remediation
- sast

- xss

- injection

- web

---

# CWE-79 Improper Neutralization of Input During Web Page Generation (XSS)

## Description

Improper Neutralization of Input During Web Page Generation (XSS)

Reference:
https://cwe.mitre.org/data/definitions/79.html


**OWASP Category**: A03:2021 – Injection


---

## Vulnerable Pattern


### ❌ Example 1

```java
    public ResponseEntity<String> getVulnerablePayloadLevel1(
            @RequestParam Map<String, String> queryParams) {
        String vulnerablePayloadWithPlaceHolder = "<div>%s<div>";
        StringBuilder payload = new StringBuilder();
        for (Map.Entry<String, String> map : queryParams.entrySet()) {
            payload.append(String.format(vulnerablePayloadWithPlaceHolder, map.getValue()));
        }
        return new ResponseEntity<String>(payload.toString(), HttpStatus.OK);
    }
```




### ❌ Example 2

```java
    public ResponseEntity<String> getVulnerablePayloadLevel2(
            @RequestParam Map<String, String> queryParams) {
        String vulnerablePayloadWithPlaceHolder = "<div>%s<div>";
        StringBuilder payload = new StringBuilder();
        Pattern pattern = Pattern.compile("[<]+[(script)(img)(a)]+.*[>]+");
        for (Map.Entry<String, String> map : queryParams.entrySet()) {
            Matcher matcher = pattern.matcher(map.getValue());
            if (!matcher.find()) {
                payload.append(String.format(vulnerablePayloadWithPlaceHolder, map.getValue()));
            }
        }
        return new ResponseEntity<String>(payload.toString(), HttpStatus.OK);
    }
```





---

## Deterministic Fix


### ✅ Secure Implementation

```java
    public ResponseEntity<String> getVulnerablePayloadLevel3(
            @RequestParam Map<String, String> queryParams) {
        String vulnerablePayloadWithPlaceHolder = "<div>%s<div>";
        StringBuilder payload = new StringBuilder();
        Pattern pattern = Pattern.compile("[<]+[(script)(img)(a)]+.*[>]+");
        for (Map.Entry<String, String> map : queryParams.entrySet()) {
            Matcher matcher = pattern.matcher(map.getValue());
            if (!matcher.find()
                    && !map.getValue().contains("alert")
                    && !map.getValue().contains("javascript")) {
                payload.append(String.format(vulnerablePayloadWithPlaceHolder, map.getValue()));
            }
        }
        return new ResponseEntity<String>(payload.toString(), HttpStatus.OK);
    }
```




### ✅ Secure Implementation

```java
    public ResponseEntity<String> getVulnerablePayloadLevel3(
            @RequestParam Map<String, String> queryParams) {
        String vulnerablePayloadWithPlaceHolder = "<div>%s<div>";
        StringBuilder payload = new StringBuilder();
        Pattern pattern = Pattern.compile("[<]+[(script)(img)(a)]+.*[>]+");
        for (Map.Entry<String, String> map : queryParams.entrySet()) {
            Matcher matcher = pattern.matcher(map.getValue());
            if (!matcher.find()
                    && !map.getValue().contains("alert")
                    && !map.getValue().contains("javascript")) {
                payload.append(String.format(vulnerablePayloadWithPlaceHolder, map.getValue()));
            }
        }
        return new ResponseEntity<String>(payload.toString(), HttpStatus.OK);
    }
```





---

## Detection Pattern

Look for these patterns in your codebase:


```bash
# Find response body with user input
grep -rn "ResponseEntity" --include="*.java" | grep -E "getParameter|queryParams"
```


```bash
# Find String.format in responses
grep -rn "String.format.*%s" --include="*.java" | grep -i response
```



---

## Remediation Steps


1. Identify where user input is rendered in HTML output

2. Apply context-appropriate encoding (HTML, JavaScript, URL)

3. Use StringEscapeUtils.escapeHtml4() for HTML context

4. Use HtmlUtils.htmlEscapeHex() for additional security

5. Implement Content-Security-Policy headers


---

## Key Imports

```java

import org.apache.commons.text.StringEscapeUtils;

import org.springframework.web.util.HtmlUtils;

```

---

## Verification

After remediation:


- Re-run SAST scan - CWE-79 should be resolved

- Test with XSS payloads: <script>alert(1)</script>

- Verify special chars are encoded: < becomes &lt;


---

## Trigger Examples

```
Fix CWE-79 vulnerability
Resolve Improper Neutralization of Input During Web Page Generation (XSS) issue
Secure this Java code against improper neutralization of input during web page generation (xss)
SAST reports CWE-79
```

---

## Common Vulnerable Locations

| Layer | Files | Patterns |
|-------|-------|----------|

| Controller | `*Controller.java` | Direct HTML response |

| View | `*.html, *.jsp` | Unescaped ${} or <%= %> |


---

## References


- [CWE-79: XSS](https://cwe.mitre.org/data/definitions/79.html)

- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)


---

**Source**: Generated by [Java CWE Security Skills Generator](https://github.com/DevelopersCoffee/java-cwe-security-skills)
**Last Updated**: 2026-03-07
