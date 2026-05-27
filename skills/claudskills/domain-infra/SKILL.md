---
name: domain-infra
description: Padrões de infraestrutura Kubernetes, secrets, clusters e operações GitOps no Yby CLI
---

# Padrões de Infraestrutura — Yby CLI

## Clusters

Dois modos suportados: `local` (k3d) e `remote` (VPS via SSH). A lógica de orquestração fica em `pkg/services/environment/` usando as interfaces `ClusterManager` e `MirrorService`.

Nunca acessar kubectl/k3d diretamente — sempre via `shared.Runner` para permitir mocks em testes.

## Secrets

Duas estratégias suportadas via flag `--strategy`:
- `sealed-secrets` (padrão) — usa Sealed Secrets do Kubernetes
- `sops` — integra com o binário `sops` para encriptação via age/KMS

Permissões de arquivos sensíveis (`.envrc`, YAMLs de secrets): sempre `0600`, nunca `0644`.

```go
if err := os.WriteFile(path, data, 0600); err != nil {
    return errors.Wrap(err, errors.ERR_IO, "falha ao escrever secret")
}
```

## Bootstrap Kubernetes

O pacote `pkg/services/bootstrap/` gerencia instalação de Argo CD, configuração de secrets e outros recursos de cluster. Usa `K8sClient` interface — nunca instanciar cliente K8s diretamente nos testes.

## Network

Port-forward e credenciais ficam em `pkg/services/network/`. Usa `ClusterNetworkManager` e `LocalContainerManager` — mockáveis via interfaces.

## Mirror

Git mirror server (`pkg/mirror/`) roda no cluster com túnel e sync loop. Não modificar sem entender o protocolo de sincronização bidirecional.

## Ambientes

Configurações em `.yby/environments.yaml`. Nunca hardcodar nomes de ambiente — usar `pkg/context` para resolver o ambiente ativo (`--context` flag ou `YBY_ENV`).

## Topologias de Scaffold

O engine em `pkg/scaffold/` filtra templates por `topology` (single/multi), `workflow` e `features`. O ambiente padrão para topologia `single` é `local` (não `prod`).

## Segurança

- Arquivos sensíveis sempre com permissão `0600`
- Nunca logar secrets ou tokens — usar `[REDACTED]` se necessário
- Validar shells antes de executar comandos SSH (`pkg/executor/`)
- Verificar dependências externas (sops, kubectl, k3d) antes de usá-las
