---
name: find-cwe
description: Find the right CWE ID for a vulnerability. Use when filing a CVE and the CWE is unknown or needs verification.
---

# CWE Finder

Find the most appropriate CWE ID for the vulnerability and return the entry ready to paste into the CVE record.

## If a CWE ID is already known — verify it

Use the WebFetch tool to look up the entry:
```
https://cwe-api.mitre.org/api/v1/cwe/weakness/<ID>
```

Confirm the name and description match the vulnerability. If not, search for a better fit.

## If searching by keyword — use web search

Use the WebSearch tool to search for the vulnerability type — e.g. `site:cwe.mitre.org path traversal`, `site:cwe.mitre.org resource exhaustion`. Look for the most specific CWE that accurately describes the root cause, not just the impact.

Prefer **Base** level CWEs over **Class** (too broad) or **Variant** (too specific) when in doubt.

## Output

Return the snippet ready to paste into `problemTypes`:

```json
{
  "descriptions": [
    {
      "cweId": "CWE-<ID>",
      "description": "CWE-<ID> <Name>",
      "lang": "en",
      "type": "CWE"
    }
  ]
}
```

Usually one CWE. Multiple are acceptable when the vulnerability genuinely has distinct root causes, but this is the exception not the rule.
