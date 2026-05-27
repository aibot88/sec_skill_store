---
name: authz-per-resource
description: Toda query checa que o user é dono do recurso
roles: [dev, qa, cto]
---
Endpoint que retorna ou modifica recurso: **sempre** filtre por `user_id` (ou `tenant_id` em multi-tenant), mesmo se já validou ID via rota.

IDOR (Insecure Direct Object Reference) é o bug #1 de aplicações web.

Padrão:
```python
# Errado — confia no ID da URL
job = Job.objects.get(id=job_id)

# Certo — restringe ao dono
job = Job.objects.get(id=job_id, user_id=current_user.id)
```

Teste cobre acesso cruzado: user A não vê recurso de user B. Em SQL: RLS Postgres com policy obrigatória.
