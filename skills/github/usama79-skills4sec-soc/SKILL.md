# Skill: Wazuh Indexer SOC Investigations

## Purpose

Use this skill to investigate security alerts and vulnerabilities stored in Wazuh Indexer (OpenSearch-compatible API).

Primary use cases:
- Alert triage by rule, host, user, IP, or MITRE mapping
- Threat hunting over recent windows
- Cluster and index health checks
- Vulnerability context for affected agents

## Security Guardrails

- Never expose real indexer credentials in docs, screenshots, or logs.
- Use read-only users for hunting workflows when possible.
- Avoid `-k` unless your environment explicitly requires skipping TLS validation.
- Keep local configuration in untracked files with restricted permissions.

## Quick Start (Standalone)

### 1. Create Local Environment File (Untracked)

```bash
cat > wazuh_indexer_config.env <<'EOF'
WAZUH_INDEXER_HOST="https://<INDEXER_HOSTNAME_OR_IP>"
WAZUH_INDEXER_PORT="9200"
WAZUH_INDEXER_USERNAME="<READONLY_USER>"
WAZUH_INDEXER_PASSWORD="<PASSWORD>"
WAZUH_INDEXER_SKIP_SSL_VERIFY="false"
EOF

chmod 600 wazuh_indexer_config.env
```

### 2. Load Configuration and Build Helpers

```bash
source wazuh_indexer_config.env

BASE_URL="${WAZUH_INDEXER_HOST}:${WAZUH_INDEXER_PORT}"

if [ "${WAZUH_INDEXER_SKIP_SSL_VERIFY}" = "true" ]; then
  SSL_FLAG="-k"
else
  SSL_FLAG=""
fi

wazuh_get() {
  local path="$1"
  curl -sS ${SSL_FLAG} -u "${WAZUH_INDEXER_USERNAME}:${WAZUH_INDEXER_PASSWORD}" \
    -H "Content-Type: application/json" \
    "${BASE_URL}${path}"
}

wazuh_search() {
  local index="$1"
  local body="$2"
  curl -sS ${SSL_FLAG} -u "${WAZUH_INDEXER_USERNAME}:${WAZUH_INDEXER_PASSWORD}" \
    -H "Content-Type: application/json" \
    -X POST "${BASE_URL}/${index}/_search" \
    -d "${body}"
}
```

### 3. Connectivity Check

```bash
wazuh_get "/"
```

## Core Platform Checks

### 1. Cluster Health

```bash
wazuh_get "/_cluster/health?pretty"
```

### 2. Index Inventory

```bash
wazuh_get "/_cat/indices?v&format=json"
```

### 3. Node Stats

```bash
wazuh_get "/_nodes/stats?pretty"
```

## Alert Investigation Queries

### 4. Alert by Document ID

```bash
wazuh_search "wazuh-alerts-*" '{
  "query": {"term": {"_id": "<ALERT_ID>"}}
}'
```

### 5. Alerts by Rule ID (Last 24h)

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 50,
  "query": {
    "bool": {
      "must": [{"term": {"rule.id": "<RULE_ID>"}}],
      "filter": [{"range": {"@timestamp": {"gte": "now-24h", "lte": "now"}}}]
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

### 6. High-Severity Alerts (Level >= 10)

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 50,
  "query": {
    "bool": {
      "must": [{"range": {"rule.level": {"gte": 10}}}],
      "filter": [{"range": {"@timestamp": {"gte": "now-24h", "lte": "now"}}}]
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

### 7. Alerts by Agent Name

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 50,
  "query": {
    "bool": {
      "must": [{"term": {"agent.name": "<AGENT_NAME>"}}],
      "filter": [{"range": {"@timestamp": {"gte": "now-7d", "lte": "now"}}}]
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

### 8. Alerts by Source IP

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 50,
  "query": {
    "bool": {
      "must": [{"term": {"data.srcip": "<SOURCE_IP>"}}],
      "filter": [{"range": {"@timestamp": {"gte": "now-7d", "lte": "now"}}}]
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

### 9. Alerts by Username

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 50,
  "query": {
    "bool": {
      "should": [
        {"term": {"data.srcuser": "<USERNAME>"}},
        {"term": {"data.dstuser": "<USERNAME>"}}
      ],
      "minimum_should_match": 1,
      "filter": [{"range": {"@timestamp": {"gte": "now-7d", "lte": "now"}}}]
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

### 10. Alerts by MITRE Technique

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 50,
  "query": {
    "bool": {
      "must": [{"term": {"rule.mitre.id": "<TECHNIQUE_ID>"}}],
      "filter": [{"range": {"@timestamp": {"gte": "now-30d", "lte": "now"}}}]
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}'
```

## Analytics Queries

### 11. Top Rule IDs (24h)

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 0,
  "query": {"range": {"@timestamp": {"gte": "now-24h"}}},
  "aggs": {
    "top_rules": {"terms": {"field": "rule.id", "size": 10}}
  }
}'
```

### 12. Top Source IPs (24h)

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 0,
  "query": {"range": {"@timestamp": {"gte": "now-24h"}}},
  "aggs": {
    "top_src_ips": {"terms": {"field": "data.srcip", "size": 10}}
  }
}'
```

### 13. Alert Volume Timeline (1h buckets)

```bash
wazuh_search "wazuh-alerts-*" '{
  "size": 0,
  "query": {"range": {"@timestamp": {"gte": "now-24h"}}},
  "aggs": {
    "alerts_over_time": {
      "date_histogram": {"field": "@timestamp", "fixed_interval": "1h"}
    }
  }
}'
```

## Vulnerability Queries

### 14. Search by CVE

```bash
wazuh_search "wazuh-states-vulnerabilities*" '{
  "query": {"term": {"vulnerability.id": "<CVE_ID>"}}
}'
```

### 15. Critical/High Vulnerabilities by Agent

```bash
wazuh_search "wazuh-states-vulnerabilities*" '{
  "size": 0,
  "query": {"terms": {"vulnerability.severity": ["Critical", "High"]}},
  "aggs": {
    "by_agent": {
      "terms": {"field": "agent.name", "size": 20},
      "aggs": {"by_severity": {"terms": {"field": "vulnerability.severity"}}}
    }
  }
}'
```

## Investigation Workflow

1. Validate indexer health and index visibility.
2. Retrieve target alert and extract key IOCs (host, user, src/dst IP, rule, MITRE).
3. Expand context:
- same rule on same host (7d)
- same source IP across all agents (7d)
- same user across alerts (7d)
- same MITRE technique (30d)
4. Add vulnerability exposure for the affected host.
5. Report findings with confidence and recommended containment/monitoring actions.

## Common Errors and Fixes

- `401` or `403`: invalid credentials or insufficient permissions.
- TLS failures: verify certificates; only use `WAZUH_INDEXER_SKIP_SSL_VERIFY=true` when unavoidable.
- Empty results: incorrect index pattern, field name mismatch, or wrong time window.
- Parsing issues: check keyword vs text mapping (`term` for exact, `match` for analyzed).

## Output Template

```text
Wazuh Investigation Summary
Alert/Entity: <identifier>
Time Range: <start> to <end>

Findings:
- <finding 1>
- <finding 2>

Exposure Context:
- Host vulnerabilities: <summary>
- Related alerts: <summary>

Recommended Actions:
- <action 1>
- <action 2>
```
