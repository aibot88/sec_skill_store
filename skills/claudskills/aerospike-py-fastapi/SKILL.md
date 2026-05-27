---
name: aerospike-py-fastapi
description: "MUST USE for building FastAPI/REST API applications with Aerospike database (aerospike-py Rust/PyO3 async client). Covers AsyncClient lifespan management, FastAPI Depends injection, aerospike_py exception-to-HTTP-status mapping (RecordNotFound→404, RecordExistsError→409, BackpressureError→503, AerospikeTimeoutError→504), POLICY_EXISTS_CREATE_ONLY/UPDATE_ONLY for CRUD semantics, NamedTuple attribute access (record.bins not tuple unpacking), client.ping() readiness probe, batch_read returning dict, batch_write with in_doubt retry signal, and global AerospikeError handler. Triggers on: FastAPI + Aerospike, REST API + aerospike-py, CRUD API with Aerospike, client.ping() health probe, batch_read/batch_write endpoint, web server/HTTP service backed by Aerospike NoSQL, uvicorn + Aerospike."
---

## 1. App Structure (Lifespan + DI)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from aerospike_py import AsyncClient
import aerospike_py

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncClient({
        "hosts": [("127.0.0.1", 3000)],
        "max_concurrent_operations": 64,      # backpressure
        "operation_queue_timeout_ms": 5000,
    })
    aerospike_py.init_tracing()                # OpenTelemetry (optional)
    # aerospike_py.start_metrics_server(port=9464)  # built-in /metrics; pick this OR §6 endpoint, not both
    await client.connect()
    app.state.aerospike = client
    yield
    await client.close()
    # aerospike_py.stop_metrics_server()
    aerospike_py.shutdown_tracing()

app = FastAPI(lifespan=lifespan)

def get_client(request: Request) -> AsyncClient:
    return request.app.state.aerospike
```

## 2. CRUD Endpoints

```python
from fastapi.responses import JSONResponse

NS, SET = "app", "records"

@app.post("/records/{pk}", status_code=201)
async def create(pk: str, body: dict, client: AsyncClient = Depends(get_client)):
    try:
        await client.put((NS, SET, pk), body,
                         policy={"exists": aerospike_py.POLICY_EXISTS_CREATE_ONLY})
        return {"key": pk}
    except aerospike_py.RecordExistsError:
        return JSONResponse(status_code=409, content={"error": "already exists"})

@app.get("/records/{pk}")
async def read(pk: str, client: AsyncClient = Depends(get_client)):
    try:
        record = await client.get((NS, SET, pk))
        return record.bins                     # NamedTuple attribute access
    except aerospike_py.RecordNotFound:
        return JSONResponse(status_code=404, content={"error": "not found"})

@app.put("/records/{pk}")
async def update(pk: str, body: dict, client: AsyncClient = Depends(get_client)):
    try:
        await client.put((NS, SET, pk), body,
                         policy={"exists": aerospike_py.POLICY_EXISTS_UPDATE_ONLY})
        return {"key": pk}
    except aerospike_py.RecordNotFound:
        return JSONResponse(status_code=404, content={"error": "not found"})

@app.delete("/records/{pk}", status_code=204)
async def delete(pk: str, client: AsyncClient = Depends(get_client)):
    try:
        await client.remove((NS, SET, pk))
    except aerospike_py.RecordNotFound:
        return JSONResponse(status_code=404, content={"error": "not found"})
```

## 2b. Batch Endpoints

`batch_read` returns `dict[UserKey, AerospikeRecord]` -- iterate with `.items()`. Missing keys are absent from the dict.

```python
from pydantic import BaseModel

class BatchReadReq(BaseModel):
    keys: list[str]

@app.post("/records:batchRead")
async def batch_read(req: BatchReadReq, client: AsyncClient = Depends(get_client)):
    keys = [(NS, SET, k) for k in req.keys]
    records = await client.batch_read(keys)            # dict[str, dict[str, Any]]
    return {"found": records, "missing": [k for k in req.keys if k not in records]}

class BatchWriteItem(BaseModel):
    key: str
    bins: dict
    ttl: int | None = None

@app.post("/records:batchWrite")
async def batch_write(items: list[BatchWriteItem], client: AsyncClient = Depends(get_client)):
    records = [
        ((NS, SET, item.key), item.bins) if item.ttl is None
        else ((NS, SET, item.key), item.bins, {"ttl": item.ttl})
        for item in items
    ]
    result = await client.batch_write(records)         # BatchWriteResult
    # br.key may be None for some failure paths -- guard before dereferencing
    def _user_key(br):
        return str(br.key.user_key) if br.key is not None else None
    in_doubt = [_user_key(br) for br in result.batch_records if br.result != 0 and br.in_doubt]
    failed   = [_user_key(br) for br in result.batch_records if br.result != 0 and not br.in_doubt]
    if in_doubt:
        # Some writes may have applied -- caller should reconcile via batch_read, not blind retry
        return JSONResponse(status_code=503, content={"in_doubt": in_doubt, "failed": failed})
    return {"failed": failed}
```

## 3. Global Error Handler

```python
@app.exception_handler(aerospike_py.BackpressureError)
async def backpressure_handler(request, exc):
    return JSONResponse(status_code=503, content={"error": "server busy, retry later"})

@app.exception_handler(aerospike_py.AerospikeError)
async def aerospike_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})
```

## 4. Exception → HTTP Status Mapping

| Exception | HTTP Status | Meaning |
|-----------|-------------|---------|
| `RecordNotFound` | 404 | Record does not exist |
| `RecordExistsError` | 409 | Record already exists (CREATE_ONLY) |
| `RecordGenerationError` | 409 | Optimistic lock conflict |
| `BackpressureError` | 503 | Too many concurrent operations |
| `AerospikeTimeoutError` | 504 | Operation timed out (canonical name; `TimeoutError` alias removed) |
| `AerospikeIndexError` | 400/500 | Secondary index error (400 if user supplied bad query, else 500) |
| `AerospikeError` | 500 | Catch-all server error |

## 5. Health Check

```python
@app.get("/health/ready")
async def ready(client: AsyncClient = Depends(get_client)):
    # ping() does an info("build") round-trip; never raises -- returns False on failure.
    return {"status": "ok"} if await client.ping() else JSONResponse(503, {"status": "unhealthy"})

@app.get("/health/live")
async def live():
    return {"status": "ok"}  # liveness should NOT depend on Aerospike (avoids restart loops on transient blip)
```

## 6. Metrics Endpoint

```python
from fastapi import Response

@app.get("/metrics")
async def metrics():
    return Response(
        content=aerospike_py.get_metrics(),
        media_type="text/plain; version=0.0.4",
    )
```

Or use the built-in server: `aerospike_py.start_metrics_server(port=9464)` in lifespan.

## 7. Key Patterns

- **Lifespan**: Create `AsyncClient` in lifespan, store on `app.state`, close on shutdown
- **DI**: Use `Depends(get_client)` for every endpoint — never create client per-request
- **Exceptions on module**: `aerospike_py.RecordNotFound` (NOT `aerospike_py.exception.RecordNotFound`)
- **NamedTuple returns**: `record.bins`, `record.meta.gen` (NOT tuple unpacking)
- **batch_read**: returns `dict[UserKey, AerospikeRecord]` — iterate with `.items()`, missing keys are absent
- **batch_write**: inspect `BatchRecord.in_doubt` before retrying non-idempotent writes
- **Health probe**: `await client.ping()` for readiness; trivial 200 OK for liveness
- **Backpressure**: Set `max_concurrent_operations` to prevent connection pool exhaustion
- **Exception name**: `AerospikeTimeoutError` (legacy `TimeoutError` alias removed)

Detail: `../aerospike-py-api/reference/client-config.md` | `../aerospike-py-api/reference/admin.md` | `../aerospike-py-api/reference/health.md` | `../aerospike-py-api/reference/write.md`
