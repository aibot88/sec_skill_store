---
name: databricks-sdk-foundation
description: Foundation patterns for all Databricks SDK skills -- auth, client init, retry, error handling. Referenced by other skills, not used standalone.
---

# Databricks SDK Foundation

Shared patterns for authentication, retry logic, error handling, cluster lifecycle, and output formatting using the `databricks-sdk` Python package. Other Databricks skills reference this foundation.

## Prerequisites

Before using any Databricks skill, verify that the required packages are installed:

```bash
python3 -c "import databricks.sdk; import tenacity; print('OK')"
```

If this prints `OK`, you're ready. If it fails with `ModuleNotFoundError`, **stop and tell the user**:

> The required Python packages `databricks-sdk` and `tenacity` are not installed.
> Please set up a virtual environment and install them:
>
> **Using uv (recommended):**
> ```
> uv venv && source .venv/bin/activate && uv pip install databricks-sdk tenacity
> ```
>
> **Using venv:**
> ```
> python3 -m venv .venv && source .venv/bin/activate && pip install databricks-sdk tenacity
> ```

Do NOT run pip install on behalf of the user. Wait for them to confirm the environment is ready.

## dbx.py CLI Wrapper

This skill includes `dbx.py`, a thin CLI wrapper around the Python SDK. It provides CLI-level token efficiency with SDK-level robustness (retries, connection pooling, typed errors). All output is JSON. Errors go to stderr.

```bash
python3 dbx.py clusters list              # List all clusters
python3 dbx.py clusters get <ID>          # Get cluster details
python3 dbx.py clusters start <ID> --wait # Start and wait until RUNNING
python3 dbx.py clusters ensure <ID>       # Idempotent start
python3 dbx.py clusters find <PATTERN>    # Find by name

python3 dbx.py jobs list [--name PAT]     # List jobs
python3 dbx.py jobs submit --cluster <ID> --notebook <PATH> --wait
python3 dbx.py jobs run <JOB_ID> --wait   # Trigger existing job
python3 dbx.py jobs status <RUN_ID>       # Check run state
python3 dbx.py jobs output <RUN_ID>       # Get run output
python3 dbx.py jobs cancel <RUN_ID>

python3 dbx.py repl create <CLUSTER_ID>   # Create execution context
python3 dbx.py repl exec <CID> <CTX> <CODE>  # Execute and wait
python3 dbx.py repl destroy <CID> <CTX>   # Destroy context

python3 dbx.py workspace import <FILE> <PATH> --overwrite
python3 dbx.py workspace list <PATH>
python3 dbx.py workspace export <PATH> <FILE>

python3 dbx.py catalog list-catalogs
python3 dbx.py catalog list-schemas <CATALOG>
python3 dbx.py catalog list-tables <CATALOG> <SCHEMA>
python3 dbx.py catalog describe <FULL_NAME>
python3 dbx.py catalog search <CATALOG> --pattern <PATTERN>
```

## Client Initialization

### Auto-Detect Auth (Recommended)

The SDK follows the [Databricks Unified Auth](https://docs.databricks.com/en/dev-tools/auth/unified-auth.html) chain automatically -- picks up `~/.databrickscfg`, environment variables, or managed identity:

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
```

### Explicit Profile

Use a named profile from `~/.databrickscfg`:

```python
w = WorkspaceClient(profile="<PROFILE_NAME>")
```

### Environment Variables

**Never hardcode real tokens in code or notebooks.** Prefer `~/.databrickscfg` or set environment variables in your shell profile. This example is for local-only development:

```python
import os

os.environ["DATABRICKS_HOST"] = "https://<WORKSPACE>.cloud.databricks.com"
os.environ["DATABRICKS_TOKEN"] = "<YOUR_PAT>"

w = WorkspaceClient()
```

| Variable | Purpose |
|----------|---------|
| `DATABRICKS_HOST` | Workspace URL |
| `DATABRICKS_TOKEN` | Personal access token |
| `DATABRICKS_CLIENT_ID` | OAuth client ID (service principal) |
| `DATABRICKS_CLIENT_SECRET` | OAuth client secret (service principal) |

## Retry Pattern

Use `tenacity` for transient errors. The SDK raises specific exceptions for retryable conditions.

### Decorator Usage

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from databricks.sdk.errors import ResourceConflict, TemporarilyUnavailable, TooManyRequests

@retry(
    retry=retry_if_exception_type((
        ResourceConflict,
        TemporarilyUnavailable,
        TooManyRequests,
        ConnectionError,
        TimeoutError,
    )),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    reraise=True,
)
def create_cluster(w, config):
    return w.clusters.create_and_wait(**config)
```

### Inline Usage

```python
from tenacity import Retrying, stop_after_attempt, wait_exponential, retry_if_exception_type
from databricks.sdk.errors import ResourceConflict, TemporarilyUnavailable, TooManyRequests

for attempt in Retrying(
    retry=retry_if_exception_type((
        ResourceConflict,
        TemporarilyUnavailable,
        TooManyRequests,
        ConnectionError,
        TimeoutError,
    )),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    reraise=True,
):
    with attempt:
        result = w.jobs.run_now(job_id=123)
```

## Error Handling

The SDK raises typed exceptions from `databricks.sdk.errors`. Always handle specific errors before generic ones:

```python
from databricks.sdk.errors import NotFound, PermissionDenied, BadRequest

try:
    cluster = w.clusters.get(cluster_id="<CLUSTER_ID>")
except NotFound:
    print(f"Cluster not found -- check the cluster ID")
except PermissionDenied:
    print(f"No access to this cluster -- verify permissions")
except BadRequest as e:
    print(f"Invalid request: {e}")
```

### Common Exceptions

| Exception | HTTP Code | Typical Cause |
|-----------|-----------|---------------|
| `NotFound` | 404 | Resource doesn't exist or was deleted |
| `PermissionDenied` | 403 | Insufficient ACLs or token scope |
| `BadRequest` | 400 | Malformed input or invalid parameters |
| `ResourceConflict` | 409 | Concurrent modification (retryable) |
| `TemporarilyUnavailable` | 503 | Service overloaded (retryable) |
| `TooManyRequests` | 429 | Rate limited (retryable) |
| `Unauthenticated` | 401 | Invalid or expired credentials |

## Cluster State Machine

Cluster states follow this lifecycle:

```
PENDING → RUNNING → RESIZING → RUNNING
                  ↘ RESTARTING → RUNNING
                  ↘ TERMINATING → TERMINATED
```

### Start and Wait (Recommended)

The SDK provides a blocking helper that handles polling:

```python
from databricks.sdk.errors import NotFound, ResourceConflict

cluster = w.clusters.get(cluster_id="<CLUSTER_ID>")

if cluster.state.value == "TERMINATED":
    w.clusters.start_and_wait(cluster_id="<CLUSTER_ID>")
```

### Manual Polling (When You Need Progress Updates)

```python
import time

def wait_for_cluster(w, cluster_id, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        info = w.clusters.get(cluster_id=cluster_id)
        state = info.state.value
        print(f"Cluster state: {state}")
        if state == "RUNNING":
            return info
        if state in ("TERMINATING", "TERMINATED", "ERROR"):
            raise RuntimeError(f"Cluster entered {state}: {info.state_message}")
        time.sleep(15)
    raise TimeoutError(f"Cluster did not reach RUNNING within {timeout}s")
```

### Valid States

| State | Meaning |
|-------|---------|
| `PENDING` | Starting up (provisioning VMs) |
| `RUNNING` | Ready for workloads |
| `RESIZING` | Adding/removing workers (still usable) |
| `RESTARTING` | Restarting (temporarily unavailable) |
| `TERMINATING` | Shutting down |
| `TERMINATED` | Fully stopped, can be restarted |
| `ERROR` | Failed to start, check `state_message` |

## Output Formatting

### SDK Objects to Dicts

Most SDK response objects support `as_dict()` for serialization:

```python
cluster = w.clusters.get(cluster_id="<CLUSTER_ID>")
cluster_dict = cluster.as_dict()
```

### JSON Formatting for Agent Output

```python
import json

# Single object
cluster = w.clusters.get(cluster_id="<CLUSTER_ID>")
print(json.dumps(cluster.as_dict(), indent=2))

# List of objects
jobs = w.jobs.list()
print(json.dumps([j.as_dict() for j in jobs], indent=2))
```

### Filtered Output

Extract only relevant fields to keep agent context concise:

```python
cluster = w.clusters.get(cluster_id="<CLUSTER_ID>")
summary = {
    "cluster_id": cluster.cluster_id,
    "name": cluster.cluster_name,
    "state": cluster.state.value,
    "spark_version": cluster.spark_version,
    "num_workers": cluster.num_workers,
}
print(json.dumps(summary, indent=2))
```
