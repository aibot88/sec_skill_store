---
name: policy-layer
description: Especificação completa da camada de política de agentes — spend controls, rate limiting, tool access matrix e compliance checklist
version: 1.0.0
owner: platform-governance
tier: full
source: .enterprise/governance/agent-skills/policy-layer/SKILL.md
quick: .enterprise/governance/agent-skills/policy-layer/SKILL-QUICK.md
portable: true
license: Apache-2.0
---

# Policy Layer — Guia Completo

## Quando usar

Carregue esta skill quando SABLE ou qualquer agente precisar:
- Auditar governance de agentes AI
- Configurar spend controls ou rate limiting
- Revisar ou atualizar a Tool Access Matrix
- Investigar acesso não autorizado a ferramenta
- Implementar HITL gates para operações destrutivas
- Validar configuração de `settings.json` para conformidade

---

## PASSO 1 — Identificar o escopo da auditoria

Determinar o que está sendo auditado:

| Escopo | Ação |
|--------|------|
| Projeto específico | Ler `.claude/settings.json` do projeto |
| Configuração global | Ler `~/.claude/settings.json` |
| Agente específico | Ler `.hseos/agents/<agente>.agent.yaml` |
| Toda a plataforma | Ler ambos + AGENT-MANIFEST.md |

---

## PASSO 2 — Spend Controls

**Verificações obrigatórias:**

- [ ] Existe daily spend cap por agente ou por projeto?
- [ ] Sessões têm limite de tempo? (ex: max 60 min por sessão autônoma)
- [ ] Custo é rastreado por role (ORBIT, KUBE, FORGE, etc.)?

**Configuração de referência:**

```json
{
  "spend": {
    "daily_cap_usd": 5.00,
    "session_max_minutes": 60,
    "alert_threshold_usd": 3.00
  }
}
```

---

## PASSO 3 — Rate Limiting

**Verificações obrigatórias:**

- [ ] APIs externas têm rate cap? (GitHub, Azure DevOps, Kubernetes)
- [ ] Há backoff logic para respostas 429?
- [ ] Operações bulk são batchadas para evitar burst?

**Padrão HSEOS:**

```yaml
rate_limits:
  github_api: 30/min
  k8s_api: 20/min
  argocd_api: 10/min
  external_llm: 10/min
```

---

## PASSO 4 — Tool Access (Least Privilege)

**Verificações obrigatórias:**

- [ ] Cada agente acessa apenas as ferramentas que precisa?
- [ ] Ferramentas destrutivas restritas a roles específicos?
- [ ] Acesso documentado em `.claude/settings.json` ou equivalente?

**Tool Access Matrix (HSEOS canonical):**

| Tool category | ORBIT | KUBE | FORGE | RAZOR | SABLE | CIPHER | GHOST |
|---|---|---|---|---|---|---|---|
| Read files/code | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Write files | ✓ (workflow state) | ✓ (manifests) | ✓ (pipeline configs) | ✗ | ✗ | ✗ | ✓ (code) |
| kubectl / K8s MCP | ✗ (→ KUBE) | ✓ | ✗ | ✗ | ✓ (read-only) | ✗ | ✗ |
| GitHub MCP (write) | ✗ | ✓ (GitOps PRs) | ✓ (pipeline PRs) | ✓ (review only) | ✗ | ✗ | ✓ (PRs) |
| Delete / destructive | ✗ | HITL required | HITL required | ✗ | ✗ | ✗ | ✗ |
| ArgoCD (sync) | ✗ | ✓ | ✗ | ✗ | ✓ (read-only) | ✗ | ✗ |
| Secrets / pass | ✗ | ✗ | ✗ | ✗ | ✓ (read-only) | ✓ | ✗ |

---

## PASSO 5 — HITL Gates

Operações que **obrigatoriamente requerem Human-In-The-Loop gate**:

```
- kubectl delete (qualquer recurso)
- kubectl scale to 0
- git push --force
- git reset --hard
- docker rm / rmi (produção)
- DROP TABLE / truncate (banco)
- Modificar RBAC / permissões
- Deploy em prod sem aprovação explícita
```

**Padrão de implementação do gate:**

```
1. Agente descreve a operação destrutiva e o impacto
2. Agente aguarda confirmação explícita do usuário
3. Usuário confirma com "confirmar" ou "yes" (case-insensitive)
4. Agente executa e loga a ação com timestamp
```

---

## PASSO 6 — Audit Trail

**Verificações obrigatórias:**

- [ ] Ações de agentes logadas com: timestamp, agent ID, tool chamado, resultado
- [ ] Tool calls rejeitados também logados (com motivo)
- [ ] Política de retenção definida para logs

**Localização padrão HSEOS:** `.logs/agent-audit/YYYY-MM-DD.log`

**Formato de entrada:**

```
[2026-04-25T05:49:00Z] KUBE kubectl apply -f manifests/prod/ → SUCCESS
[2026-04-25T05:49:01Z] FORGE gh pr create → SUCCESS (PR #42)
[2026-04-25T05:49:05Z] ORBIT kubectl delete → REJECTED (HITL gate — awaiting user)
```

---

## PASSO 7 — Relatório de Compliance

Ao final da auditoria, gerar:

```markdown
## Policy Layer Audit — [data]

**Agente/Projeto auditado:** [nome]
**Auditado por:** SABLE

### Spend Controls
- Status: [PASS / WARN / FAIL]
- [notas]

### Rate Limiting
- Status: [PASS / WARN / FAIL]
- [notas]

### Tool Access (Least Privilege)
- Status: [PASS / WARN / FAIL]
- Violações: [lista ou "nenhuma"]

### HITL Gates
- Status: [PASS / WARN / FAIL]
- [notas]

### Audit Trail
- Status: [PASS / WARN / FAIL]
- [notas]

### Ações Recomendadas
1. [ação prioritária]
2. [ação secundária]
```

---

## Escalação

Escalar para SABLE (ou notificar o usuário) quando:

- Agente solicita acesso fora da sua coluna na Tool Access Matrix
- Spend cap atingido ou próximo (>80%)
- Operação destrutiva proposta sem HITL gate
- Audit logs ausentes para workflow concluído
- Tentativa de bypass de política detectada

---

## Anti-patterns (NUNCA fazer)

| Anti-pattern | Consequência |
|-------------|-------------|
| Conceder acesso temporário fora da matrix | Cria precedente e buracos de auditoria |
| Pular HITL gate "por eficiência" | Operação irreversível sem aprovação humana |
| Logar apenas sucessos, ignorar rejeições | Audit trail incompleto — não rastreável |
| Não revogar acesso temporário | Escalação de privilégio permanente |


## Quick Mode

For low-context activation, load `.enterprise/governance/agent-skills/policy-layer/SKILL-QUICK.md` or `QUICK.md` first. Load this full skill for deep analysis, violation fixing, or formal review gates.

