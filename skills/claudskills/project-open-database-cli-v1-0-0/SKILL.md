---
name: project-open-database-cli
description: Skill multi-SGBD para operar bancos de dados (SQL Server, MySQL, SQLite, PostgreSQL, Firebird) via CLI. Cobre conexão, cache de sessão por pasta de SGBD, varredura automática pós-conexão, inspeção de colunas com PK (fields por database > schema > table), renovação de cache a cada 15 min e política de limpeza (7 dias). Usar quando o usuário pedir para conectar, explorar, consultar, exportar dados ou executar scripts SQL.
model: sonnet
thinking: extended
category: project
license: MIT
copyright: "Copyright (c) 2026 CSL Tech Solutions"
company: "CSL Tech Solutions"
author: "Claiton de Souza Linhares"
---

# project-open-database-cli

## Versão interna (ficheiro)

| Campo | Valor |
|-------|-------|
| **FileVersion** | 1.0.0 |
| **Política** | `.cursor/VERSION.md` |

## Responsabilidade única

Esta skill cobre a operação de bancos de dados via CLI para 5 SGBDs: **SQL Server**, **MySQL/MariaDB**, **SQLite**, **PostgreSQL** e **Firebird**. Cobre conexão interativa, varredura automática pós-conexão, cache de sessão persistente por SGBD, inspeção de colunas com PK usando as queries canónicas de [Providers.Common.SQLBuilder.pas](../../../projects/modules/ProvidersORM/src/Modulos/Providers.v161/Commons/Providers.Common.SQLBuilder.pas), execução de consultas e exportação de resultados. **Não cobre** compilação do projeto, configuração de engines no código-fonte, nem operações via código Delphi/FPC — apenas operação direta via terminal.

## When to use

- "conectar no banco" / "abrir banco"
- "listar bancos / tabelas / colunas"
- "executar query / rodar script SQL"
- "exportar resultado para arquivo"
- "inspecionar estrutura de tabela"
- "gerar relatório markdown de uma tabela"

## When NOT to use

- Compilar o projeto → usar `developer-delphi-build-toolchain`.
- Configurar engines no código (`USE_FIREDAC`, `USE_SQLDB`, `USE_ZEOS`) → usar `developer-delphi-programming-conditional-defines`.
- Implementar acesso via código Delphi/FPC → usar `developer-delphi-to-fpc-architecture-and-design`.
- Configurar connection strings no código → referenciar `config/database.ini` diretamente.
- Operações destrutivas em produção sem confirmação prévia.

## Dependências (skills prévias)

| Skill | Quando executar antes |
|-------|-----------------------|
| `developer-delphi-build-toolchain` | Para verificar paths dos executáveis CLI e parâmetros de conexão |

---

## Dados de conexão — obrigatório antes de qualquer operação

**REGRA:** antes de executar qualquer comando, **perguntar SEMPRE o tipo de banco primeiro**, depois os demais dados.

### Passo 0 — Tipo de banco (obrigatório)

```text
Qual tipo de banco?
  [1] SQL Server
  [2] MySQL / MariaDB
  [3] SQLite
  [4] PostgreSQL
  [5] Firebird
```

### Passo A — Verificar cache existente

Procurar arquivos `ss_<sgbd>_*.md` em todas as pastas de cache:

```bash
ls MSSqlcmd/ss_*.md MySQL/ss_*.md SQLite/ss_*.md PostgreSQL/ss_*.md Firebird/ss_*.md 2>/dev/null
```

#### Limpeza automática de caches antigos (TTL 7 dias)

Se houver caches com mais de 7 dias, apresentar opção de limpeza **antes** de listar os caches válidos:

```text
Encontrei N cache(s) com mais de 7 dias (candidatos a limpeza):
  [a] ss_sqlserver_10100210_1770000000.md — 18 dias
  [b] ss_mysql_localhost_1769500000.md    — 23 dias

  [c] Deletar todos (recomendado)
  [d] Manter todos
  [e] Escolher um a um
```

Padrão: recomendar deletar. Nunca deletar caches ≤ 7 dias. Sempre confirmar.

#### Caches válidos

Com caches ≤ 7 dias:

```text
Encontrei arquivos de cache de sessão anteriores:

  [1] ss_sqlserver_10100210_1776000000.md — SQL Server | Host: 192.168.1.100 | Usuário: sa | 2h atrás
  [2] ss_postgresql_localhost_1775999000.md — PostgreSQL | Host: localhost | Usuário: postgres | 5h atrás

  [3] Conectar a um servidor diferente (ignorar cache)
  [4] Informar novos dados do zero
```

- Escolher cache: carrega mapa, pede só a senha, prossegue sem nova varredura.
- Escolher [3]/[4]: executa varredura completa após coleta de dados.

### Passo B — Coleta de dados (sem cache ou dados novos)

Campos por SGBD:

| SGBD | Campos solicitados |
|------|---------------------|
| **SQL Server** | host, porta (1433), usuário, senha, database (opcional) |
| **MySQL** | host, porta (3306), usuário, senha, database (opcional) |
| **SQLite** | arquivo `.db` (caminho completo) |
| **PostgreSQL** | host, porta (5432), usuário, senha, database |
| **Firebird** | host, porta (3050), usuário, senha, caminho `.fdb` |

> A skill **nunca armazena senhas** em nenhum arquivo de cache.

---

## Executáveis CLI por SGBD

| SGBD | Executável | Workspace (embarcado) | Sistema |
|------|------------|------------------------|---------|
| SQL Server | `sqlcmd.exe` | `./MSSqlcmd/sqlcmd.exe` | — |
| MySQL | `mysql.exe` / `mysqlsh.exe` | `./MySQL/bin/` | `C:\Program Files\MySQL\...` |
| SQLite | `sqlite3.exe` | `./SQLite/sqlite3.exe` | — |
| PostgreSQL | `psql.exe` | — | `C:\Program Files\PostgreSQL\18\bin\psql.exe` |
| Firebird | `isql.exe` | — | `C:\Program Files\Firebird\Firebird_2_5\bin\isql.exe` |

Sempre usar caminho relativo à raiz do workspace (para executáveis embarcados) ou caminho absoluto do sistema (PostgreSQL / Firebird).

---

## Varredura automática após primeira conexão

**REGRA:** imediatamente após confirmar os dados de conexão, executar varredura automática antes de qualquer outra operação. Queries-fonte: `GetSQLTables*` de [Providers.Common.SQLBuilder.pas](../../../projects/modules/ProvidersORM/src/Modulos/Providers.v161/Commons/Providers.Common.SQLBuilder.pas).

Ver comandos detalhados por SGBD em [consultas_rapidas/](consultas_rapidas/).

Ao final, apresentar resumo e gravar cache em `<PastaSGBD>/ss_<sgbd>_<host_safe>_<unix_ts>.md`.

---

## Inspeção de colunas com PK (sob demanda)

Usar quando o usuário pedir "colunas de X", "estrutura de X", "campos de X", "desc X". Queries por SGBD extraídas de `GetSQLFields*` em [Providers.Common.SQLBuilder.pas](../../../projects/modules/ProvidersORM/src/Modulos/Providers.v161/Commons/Providers.Common.SQLBuilder.pas):

- SQL Server: [referencia_sqlserver.md](consultas_rapidas/referencia_sqlserver.md#colunas-com-pk)
- MySQL: [referencia_mysql.md](consultas_rapidas/referencia_mysql.md#colunas-com-pk)
- SQLite: [referencia_sqlite.md](consultas_rapidas/referencia_sqlite.md#colunas-com-pk)
- PostgreSQL: [referencia_postgresql.md](consultas_rapidas/referencia_postgresql.md#colunas-com-pk)
- Firebird: [referencia_firebird.md](consultas_rapidas/referencia_firebird.md#colunas-com-pk)

Ao inspecionar colunas, acrescentar na seção `## Colunas inspecionadas` do cache hierarquizada em `database > schema > table > fields` (ver formato abaixo).

---

## Cache de sessão persistente (`ss_*.md`)

### Nome do arquivo

```text
<PastaSGBD>/ss_<sgbd>_<host_safe>_<unix_ts>.md
```

Exemplos:

- `MSSqlcmd/ss_sqlserver_10100210_1776373731.md`
- `PostgreSQL/ss_postgresql_localhost_1776400000.md`
- `SQLite/ss_sqlite_mybase_1776400500.md`

### Estrutura hierárquica

```markdown
# Cache <SGBD> — <HOST>

> **Gerado em:** YYYY-MM-DD HH:MM
> **SGBD:** <SGBD> | **Host:** <HOST>:<PORTA> | **Usuário:** <USUARIO> | **Database:** <DATABASE>

## Mapa de bancos e tabelas

### Database: <DATABASE_1>

#### Schema: <SCHEMA_1>

Tabelas (N): T1, T2, T3 ...

#### Schema: <SCHEMA_2>

Tabelas (N): T1, T2 ...

### Database: <DATABASE_2>
...

## Colunas inspecionadas

### Database: <DATABASE>

#### Schema: <SCHEMA>

##### Tabela: <TABELA>

| Posição | Coluna | Tipo | Tamanho | Nullable | Default | PK | Constraint |
| ------- | ------ | ---- | ------- | -------- | ------- | -- | ---------- |
| 1 | Id | INT | - | NO | - | ✓ | PK_<tabela> |
| 2 | Nome | VARCHAR | 100 | NO | - |  |  |

> Inspecionado em: YYYY-MM-DD HH:MM
```

### Regras de hierarquia por SGBD

| SGBD | Database | Schema | Fallback quando ausente |
|------|----------|--------|--------------------------|
| SQL Server | ✓ (`table_catalog`) | ✓ (ex. `dbo`) | — |
| PostgreSQL | ✓ (`table_catalog`) | ✓ (ex. `public`) | — |
| MySQL | ✓ (`TABLE_SCHEMA`) | — | Schema: `default` |
| SQLite | — | — | Database: nome do `.db`; Schema: `main` |
| Firebird | — | — | Database: nome do `.fdb`; Schema: `default` |

### Regra de atualização

Ao inspecionar colunas de tabela já presente no cache, **substituir** a sub-seção `##### Tabela: <TABELA>` inteira pelo resultado mais recente (preservar timestamp).

---

## Renovação automática do cache (a cada 15 minutos)

**REGRA:** durante a sessão ativa, renovar o cache a cada 15 min sem interromper o fluxo.

Lógica:

1. Após cada solicitação do usuário, calcular `tempo_atual - timestamp_cache`.
2. Se > 900 s: informar de forma não-bloqueante (`[Cache expirado — renovando...]`).
3. Re-executar varredura do SGBD.
4. **Sobrescrever** o arquivo de cache existente com o mesmo nome (timestamp atualizado no cabeçalho).
5. Preservar a seção `## Colunas inspecionadas` (não apagar inspeções já feitas).
6. Confirmar: `[Mapa atualizado — HH:MM — N databases, M tabelas]`.

Ao carregar cache de arquivo já expirado (sessão nova), oferecer renovação imediata:

```text
Cache encontrado, mas tem X minutos (limite: 15 min).
  [1] Renovar agora (recomendado)
  [2] Usar cache desatualizado
```

---

## Limpeza periódica de caches antigos

- **TTL de retenção:** 7 dias.
- **Gatilho:** ao iniciar a skill (antes do Passo A).
- **Ação:** apresentar lista de caches > 7 dias com opção `[c] Deletar todos (recomendado) / [d] Manter todos / [e] Escolher um a um`.
- **Nunca deletar sem confirmar.**
- **Comando manual:** `limpar [--older-than <dias>]` no loop interativo do `database_session_manager.py`.

---

## Script auxiliar

O script Python [`.cursor/scripts/database_session_manager.py`](../../scripts/database_session_manager.py) automatiza o fluxo desta skill:

- Detecta caches existentes em todas as pastas de SGBD.
- Propõe limpeza de caches > 7 dias.
- Apresenta prompt de tipo de banco + credenciais.
- Executa varredura automática usando o CLI apropriado.
- Loop interativo: `bancos`, `tabelas <db>`, `colunas <tabela>`, `mapa`, `limpar`, `ajuda`, `sair`.

Execução (a partir da raiz do workspace):

```powershell
python .cursor/scripts/database_session_manager.py
python .cursor/scripts/database_session_manager.py --sgbd sqlserver
python .cursor/scripts/database_session_manager.py --limpar --older-than 7
```

---

## Conexão / Exploração / Consultas / Exportação

Ver comandos prontos por SGBD em:

- [consultas_rapidas/referencia_sqlserver.md](consultas_rapidas/referencia_sqlserver.md)
- [consultas_rapidas/referencia_mysql.md](consultas_rapidas/referencia_mysql.md)
- [consultas_rapidas/referencia_sqlite.md](consultas_rapidas/referencia_sqlite.md)
- [consultas_rapidas/referencia_postgresql.md](consultas_rapidas/referencia_postgresql.md)
- [consultas_rapidas/referencia_firebird.md](consultas_rapidas/referencia_firebird.md)

Fluxo completo em [exemplos/explorar_banco.md](exemplos/explorar_banco.md).

---

## Automação com tratamento de erro

Flags específicas por SGBD para automação (retorno de exit code em falha):

| SGBD | Flag | Exemplo |
|------|------|---------|
| SQL Server | `-b` | `sqlcmd ... -i script.sql -b` |
| PostgreSQL | `-v ON_ERROR_STOP=1` | `psql ... -v ON_ERROR_STOP=1 -f script.sql` |
| MySQL | `--force` (negativo) / verificar errorlevel | `mysql ... < script.sql && echo ok` |
| SQLite | `-bail` | `sqlite3 -bail banco.db < script.sql` |
| Firebird | `-b` (bail out on first error) | `isql ... -b -i script.sql` |

---

## Checklist de operação

- [ ] Tipo de banco confirmado ANTES de qualquer comando.
- [ ] Executável localizado (embarcado ou no sistema).
- [ ] Conexão validada antes de executar scripts destrutivos.
- [ ] Queries de exportação prefixadas com `SET NOCOUNT ON;` (SQL Server) ou equivalente.
- [ ] Flag de erro presente em scripts de automação.
- [ ] Saídas salvas em `Data/` com nome descritivo.
- [ ] Senhas não expostas em histórico de terminal quando possível.
- [ ] Backup confirmado antes de DDL/DML destrutivo em produção.

---

## Anti-padrões

| Anti-padrão | Por que é errado | Como corrigir |
|-------------|------------------|---------------|
| Executar comando sem perguntar tipo de banco primeiro | Sintaxe muda por SGBD; assumir errado leva a erros de parse | Passo 0 sempre — perguntar tipo antes de tudo |
| Gravar senha no cache | Risco de vazamento | Skill **nunca** grava senhas |
| Carregar cache > 7 dias como válido | Estrutura pode ter mudado | Aplicar política de retenção + limpeza proposta |
| Usar path absoluto do exe embarcado (MSSqlcmd) | Quebra em outra máquina | Usar `./MSSqlcmd/sqlcmd.exe` relativo |
| Omitir `SET NOCOUNT ON` em exportações SQL Server | Insere `"N rows affected"` no arquivo | Prefixar a query |
| Paths com espaços sem aspas | Comando falha no shell | Envolver paths com aspas duplas |

---

## Troubleshooting rápido

| Problema | Causa provável | Ação |
|----------|----------------|------|
| `sqlcmd: command not found` | PATH não configurado | Usar caminho completo `./MSSqlcmd/sqlcmd.exe` |
| `Login failed for user` | Credenciais incorretas | Verificar `-U`/`-P` ou usar `-E` (Windows Auth) |
| `Cannot open database` | Nome do banco incorreto ou sem permissão | Verificar mapa do cache |
| Timeout / não conecta | Firewall bloqueando porta | Liberar porta TCP e verificar protocolo |
| Erro de certificado TLS | Servidor sem certificado válido | `-N -C` (dev) ou certificado válido (produção) |
| Firebird connection string | Formato `host/porta:caminho.fdb` | `isql -u SYSDBA -p masterkey -d localhost/3050:C:\dados\base.fdb` |
| PostgreSQL senha | `.pgpass` ou env `PGPASSWORD` | Configurar env antes do comando |

---

## Referências

- `MSSqlcmd/COMO_USAR_MSSQL_CLI.md` — guia completo sqlcmd
- `MySQL/COMO_USAR_MYSQL_CLI.md` — guia completo mysql/mysqlsh
- `SQLite/COMO_USAR_SQLITE_CLI.md` — guia completo sqlite3
- `PostgreSQL/COMO_USAR_POSTGRESQL_CLI.md` — guia completo psql
- `Firebird/COMO_USAR_FIREBIRD_CLI.md` — guia completo isql
- [Providers.Common.SQLBuilder.pas](../../../projects/modules/ProvidersORM/src/Modulos/Providers.v161/Commons/Providers.Common.SQLBuilder.pas) — fonte canónica das queries de exploração por SGBD
- [.cursor/scripts/database_session_manager.py](../../scripts/database_session_manager.py) — script Python auxiliar

---

## Changelog (este arquivo)

- 1.0.0 (16/04/2026): criação — skill renomeada de `project-abrir-bancos-cli_V1.1.0` (português) para `project-open-database-cli_V1.0.0` (inglês), alinhada ao padrão das demais skills. Expandida de 3 para 5 SGBDs (+ PostgreSQL + Firebird); adicionado checklist com tipo de banco obrigatório, cache de sessão `ss_*.md` com fields por `database > schema > table`, varredura automática pós-conexão, inspeção de colunas com PK via queries do `Providers.Common.SQLBuilder`, renovação de cache a cada 15 min, política de retenção/limpeza de 7 dias. Exemplos totalmente genéricos (sem servidores concretos).
