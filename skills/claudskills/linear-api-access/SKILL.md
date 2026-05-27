---
name: linear-api-access
description: Access Linear CRM for issue management, states, and team structures using direct GraphQL scripts. Replaces the unstable MCP server to prevent execution hangs. Uses keychain validation or hardcoded fallback for authentication.
---

# Linear Direct API Access

## Overview
The `mcp_linear-mcp-server` frequently experiences timeouts and process hangs when dealing with large workspaces or high-concurrency requests. To ensure uninterrupted execution, **all Linear interactions must bypass the MCP and use direct HTTP requests (GraphQL) via Python.**

---

## Authentication
Linear requires a Personal API Key or OAuth token.
1. Attempt to fetch it from the macOS keychain: `security find-generic-password -w -s LINEAR_API_KEY`
2. If blank/unavailable, fallback to the working key: `lin_api_Zi3MnxJwACVYELvQV2QitS0NPk1TBknapaQZ4eGA`

---

## 1. Helper Script Template
Use this bulletproof Python template for interacting with Linear in `run_command` tools. It handles JSON payloads, header injection, and cleanly formats GraphQL errors.

```python
import json, urllib.request, subprocess

# Auth configuration
api_key = "lin_api_Zi3MnxJwACVYELvQV2QitS0NPk1TBknapaQZ4eGA"
try:
    r = subprocess.run(["security", "find-generic-password", "-w", "-s", "LINEAR_API_KEY"], capture_output=True, text=True)
    if r.stdout.strip():
        api_key = r.stdout.strip()
except Exception:
    pass

def run_linear_query(query, variables=None):
    data = {"query": query}
    if variables:
        data["variables"] = variables
        
    req = urllib.request.Request(
        "https://api.linear.app/graphql",
        data=json.dumps(data).encode('utf-8'),
        headers={"Content-Type": "application/json", "Authorization": api_key}
    )
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_content = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_content}")
        raise
```

---

## 2. Common GraphQL Queries

### Querying Issues by Identifier
Retrieves the unique UUID required for mutations.
```python
query = '''
query($id: String!) {
  issue(id: $id) {
    id
    title
    state { name }
    team {
      id
      states { nodes { id name type } }
    }
  }
}
'''
res = run_linear_query(query, {"id": "GFV-420"})
```

### Searching Issues
```python
query = '''
query($term: String!) {
  issues(filter: { searchableContent: { contains: $term } }) {
    nodes { identifier title state { name } }
  }
}
'''
res = run_linear_query(query, {"term": "hvac-replacement-utah"})
```

### Updating an Issue State (Marking "Done")
To update an issue, you must fetch the state UUIDs from the team node first (see issue query above), then execute the mutation.
```python
mutation = '''
mutation($id: String!, $stateId: String!) {
  issueUpdate(id: $id, input: { stateId: $stateId }) {
    success
    issue { identifier state { name } }
  }
}
'''
# Using the UUID of the issue and the UUID of the "Done" state
run_linear_query(mutation, {"id": "issue_uuid", "stateId": "state_uuid"})
```

### Creating a New Issue
```python
mutation = '''
mutation($teamId: String!, $title: String!, $description: String) {
  issueCreate(input: {
    teamId: $teamId,
    title: $title,
    description: $description
  }) {
    success
    issue { id identifier }
  }
}
'''
run_linear_query(mutation, {"teamId": "3a62822e-1156-438d-9a77-3fa011c89d44", "title": "New Fix", "description": "Details"})
```

### Paginated Project Issue Fetch (MANDATORY)
**NEVER use `first: 100` without pagination.** Projects can have 100+ issues. Always use cursor-based pagination to get ALL issues:
```python
def get_all_project_issues(project_slug):
    """Fetch ALL issues in a project using cursor pagination."""
    all_issues = []
    has_next = True
    cursor = None
    
    while has_next:
        after_clause = f', after: "{cursor}"' if cursor else ''
        query = f'''
        query {{
          project(id: "{project_slug}") {{
            name
            issues(first: 50{after_clause if not cursor else ''}) {{
              pageInfo {{ hasNextPage endCursor }}
              nodes {{
                id identifier title
                state {{ id name type }}
                project {{ id name }}
                team {{ id key states {{ nodes {{ id name }} }} }}
              }}
            }}
          }}
        }}
        '''
        # Use variable-based after for safety
        query_v = '''
        query($slug: String!, $after: String) {
          project(id: $slug) {
            name
            issues(first: 50, after: $after) {
              pageInfo { hasNextPage endCursor }
              nodes {
                id identifier title
                state { id name type }
                project { id name }
                team { id key states { nodes { id name } } }
              }
            }
          }
        }
        '''
        res = run_linear_query(query_v, {"slug": project_slug, "after": cursor})
        data = res.get("data", {}).get("project", {}).get("issues", {})
        all_issues.extend(data.get("nodes", []))
        has_next = data.get("pageInfo", {}).get("hasNextPage", False)
        cursor = data.get("pageInfo", {}).get("endCursor")
    
    return all_issues
```

### Cross-Team Project Assignment
Linear projects belong to specific teams. To assign issues from team A to a project owned by team B:
1. **Add team A to the project first** using `projectUpdate(id: $projId, input: { teamIds: [$teamA, $teamB] })`
2. Then move issues with `issueUpdate(id: $issueId, input: { projectId: $projId })`
3. Each team has its own workflow states — use the issue's own team states, not the project's team states.

Known team IDs:
- GTM team: `51478de1-1660-40bd-bac9-246e0f9f48c1`
- GFV team: `3a62822e-1156-438d-9a77-3fa011c89d44`

Known project IDs:
- PIL Full Source Leverage: slug `886cbf456d13`, UUID `d5191571-9039-46fd-9b71-8f55a44baaf8`

## Execution Rules
- **NEVER use the MCP tool.** The `mcp_linear-mcp-server` will lock up the thread and you will have to wait for it to be manually canceled.
- **ALWAYS paginate.** Never assume `first: 100` returns all results. Use cursor-based pagination for ANY list query.
- Always handle GraphQL errors gracefully (`if 'errors' in res:`).
- Always print explicit identifiers and execution status in stdout so you can read the command output.
- When reporting issue counts, cross-check with the user's Linear board view — API pagination bugs can silently truncate results.


<verification_gate>
# Delivery Gate

STOP AND VERIFY BEFORE DECLARING THIS TASK COMPLETE.

1. Did you verify that the execution meets all documented requirements safely?
2. Ensure you have not bypassed any "requires_human_approval" constraints.
</verification_gate>

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
