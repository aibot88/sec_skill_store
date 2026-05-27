---
name: fastapi-async
description: FastAPI com endpoints async, Pydantic v2 e dependency injection
roles: [dev]
---
- Endpoints sempre `async def`.
- Pydantic v2 (`model_config`, não `Config` antiga).
- DB via `Depends(get_session)`; nunca abrir session global.
- HTTP externo: `httpx.AsyncClient` injetado, nunca `requests`.
- `response_model` explícito em todo endpoint.
- Erros via `HTTPException` ou exception handler global.
- Background tasks pra trabalho assíncrono curto; queue real (Celery/RQ) pra trabalho longo.
