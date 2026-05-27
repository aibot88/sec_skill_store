---
name: nomos-mcp
description: >
  Manage Nomos artifacts via MCP Server. Use when creating, updating, or deleting
  products, rules, requirements, blueprints, or instances in a Nomos catalog.
  Also use to validate the catalog after changes, manage workspaces (Git branches),
  or check the compliance status of product instances.
---

# Nomos MCP Server Skill

## Überblick

Der Nomos MCP Server gibt KI-Agenten Zugriff auf Nomos-Artefakte über das
Model Context Protocol (MCP). Alle Änderungen erfolgen scope-kontrolliert
und immer auf isolierten Git-Branches — niemals direkt auf `main`.

## Voraussetzungen

- Nomos Backend läuft unter `NOMOS_API_BASE` (Standard: `http://localhost:8080`)
- `NOMOS_AGENT_SCOPE` ist gesetzt (`read`, `draft` oder `write`)
- Für Workspace-Tools: Git-Repository unter `NOMOS_REPO_PATH`

## Scope-Matrix

| Tool                        | read | draft | write |
|-----------------------------|------|-------|-------|
| list_products               | ✓    | ✓     | ✓     |
| get_product                 | ✓    | ✓     | ✓     |
| create_product              | ✗    | ✓     | ✓     |
| update_product              | ✗    | ✓     | ✓     |
| delete_product              | ✗    | ✓     | ✓     |
| add/remove_product_rule     | ✗    | ✓     | ✓     |
| add/remove_product_req      | ✗    | ✓     | ✓     |
| get_product_variants        | ✓    | ✓     | ✓     |
| list_rules / get_rule       | ✓    | ✓     | ✓     |
| create_rule / update_rule   | ✗    | ✓     | ✓     |
| list/get_requirements       | ✓    | ✓     | ✓     |
| update_requirement          | ✗    | ✓     | ✓     |
| list/get_blueprints         | ✓    | ✓     | ✓     |
| list/get_instances          | ✓    | ✓     | ✓     |
| get_instance_compliance     | ✓    | ✓     | ✓     |
| create_workspace            | ✗    | ✓     | ✓     |
| get/list_workspaces         | ✓    | ✓     | ✓     |
| validate_catalog            | ✓    | ✓     | ✓     |
| get_health                  | ✓    | ✓     | ✓     |

**Merge in `main` ist kein Tool — das bleibt Menschen vorbehalten.**

## Typischer Agent-Workflow (DRAFT-Scope)

```
1. get_current_workspace        → aktuellen Branch prüfen
2. create_workspace             → neuen Branch anlegen (z.B. 'agent/add-gdpr-rules')
3. list_products / get_product  → Kontext verstehen
4. create_product / update_rule → Änderungen vornehmen
5. validate_catalog             → Validierung prüfen (keine Errors = OK)
6. [Mensch reviewt und mergt via PR]
```

## Sicherheitshinweise

- Schreiben direkt auf `main` ist nicht möglich (wirft PermissionError)
- Jeder schreibende Aufruf prüft den Scope via `@require_scope` Decorator
- Der MCP Server hat keinen direkten Dateisystemzugriff — er nutzt die REST API
- Workspace-Tools nutzen `subprocess`/`git` lokal im `NOMOS_REPO_PATH`

## Konfiguration (Claude Desktop)

```json
{
  "mcpServers": {
    "nomos": {
      "command": "python",
      "args": ["-m", "nomos_mcp.server"],
      "cwd": "/path/to/nomos/mcp",
      "env": {
        "NOMOS_API_BASE": "http://localhost:8080",
        "NOMOS_AGENT_SCOPE": "draft",
        "NOMOS_REPO_PATH": "/path/to/nomos"
      }
    }
  }
}
```

## Fehlerbehandlung

Alle Tools geben bei API-Fehlern den HTTP-Status-Code und Response-Body zurück:
```
HTTP 404: {"detail": "Produkt nicht gefunden"}
HTTP 400: {"detail": "Missing required field: version"}
```

Bei Scope-Fehlern:
```
Zugriff verweigert: Scope 'read' reicht nicht aus. Dieses Tool erfordert mindestens scope 'draft'.
```
