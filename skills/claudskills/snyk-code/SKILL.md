---
name: snyk-code
description: >
  Execute Snyk Code SAST (Static Application Security Testing) scans on source code files or projects,
  interpret vulnerability findings, generate structured security reports, and suggest remediations.
  Use this skill whenever the user mentions: "snyk", "snyk code", "SAST scan", "scan de segurança",
  "verificar vulnerabilidades no código", "análise estática de segurança", "snyk scan", "rodar snyk",
  "vulnerabilidade no código-fonte", or wants to audit code for security issues with Snyk.
  Also trigger when the user uploads code and asks for a security scan or wants a Snyk-style report.
---

# Snyk Code Skill

Realiza análise estática de segurança (SAST) usando o Snyk Code CLI, interpreta os resultados e
gera relatórios detalhados com remediações contextualizadas.

Suporta: **Linux**, **macOS** e **Windows** (PowerShell e CMD).

---

## Workflow principal

### 1. Detectar o sistema operacional e validar pré-requisitos

Antes de qualquer comando, identifique o SO do usuário e use a seção correta abaixo.

---

#### Linux / macOS

```bash
# Verificar Node.js (requer v14+)
node --version
npm --version

# Verificar se o Snyk já está instalado
snyk --version

# Instalar via npm
npm install -g snyk

# Alternativa via brew (macOS)
brew install snyk-cli

# Autenticar
snyk auth

# Configurar token manualmente
export SNYK_TOKEN="seu-token-aqui"
# Para persistir:
echo 'export SNYK_TOKEN="seu-token-aqui"' >> ~/.bashrc
```

---

#### Windows — PowerShell

```powershell
# Verificar instalação
node --version
snyk --version

# Instalar via npm
npm install -g snyk

# Alternativa via Chocolatey
choco install snyk

# Alternativa via Scoop
scoop install snyk

# Autenticar
snyk auth

# Configurar token (sessão atual)
$env:SNYK_TOKEN = "seu-token-aqui"

# Persistir para o usuário
[System.Environment]::SetEnvironmentVariable("SNYK_TOKEN", "seu-token-aqui", "User")
```

> AVISO: Se receber erro "File cannot be loaded", rode como Administrador:
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

---

#### Windows — CMD

```cmd
node --version
snyk --version
npm install -g snyk
snyk auth
set SNYK_TOKEN=seu-token-aqui
```

---

### 2. Executar o scan

#### Linux / macOS

```bash
snyk code test --json > snyk-report.json
snyk code test /caminho/para/projeto --json > snyk-report.json
snyk code test --severity-threshold=high --json > snyk-report.json
snyk code test --sarif > snyk-report.sarif
```

#### Windows — PowerShell

```powershell
# IMPORTANTE: use Out-File para evitar encoding UTF-16 que corrompe o JSON
snyk code test --json | Out-File -Encoding utf8 snyk-report.json
snyk code test C:\projetos\meu-app --json | Out-File -Encoding utf8 snyk-report.json
snyk code test --severity-threshold=high --json | Out-File -Encoding utf8 snyk-report.json
snyk code test --sarif | Out-File -Encoding utf8 snyk-report.sarif
```

#### Windows — CMD

```cmd
snyk code test --json > snyk-report.json
snyk code test --severity-threshold=high --json > snyk-report.json
```

---

### 3. Interpretar o JSON de saída

O JSON segue o formato SARIF 2.1.0:

```json
{
  "runs": [{
    "results": [
      {
        "ruleId": "python/SqlInjection",
        "message": { "text": "Unsanitized input flows into SQL query" },
        "level": "error",
        "locations": [{
          "physicalLocation": {
            "artifactLocation": { "uri": "app/db.py" },
            "region": { "startLine": 42, "startColumn": 8 }
          }
        }],
        "properties": {
          "priorityScore": 850,
          "isAutofixable": false,
          "cwe": ["CWE-89"]
        }
      }
    ]
  }]
}
```

| Campo | Significado |
|---|---|
| `ruleId` | Categoria da vulnerabilidade |
| `level` | error=alto, warning=médio, note=baixo |
| `priorityScore` | Score 0–1000 (maior = mais crítico) |
| `cwe` | CWE associado |
| `isAutofixable` | Snyk DeepCode AI pode gerar fix |

---

### 4. Rodar o parser Python

#### Linux / macOS

```bash
python3 scripts/parse_snyk_report.py snyk-report.json
python3 scripts/parse_snyk_report.py snyk-report.json --output relatorio.md
python3 scripts/parse_snyk_report.py snyk-report.json --min-severity high
```

#### Windows — PowerShell / CMD

```powershell
python scripts\parse_snyk_report.py snyk-report.json
python scripts\parse_snyk_report.py snyk-report.json --output relatorio.md
python scripts\parse_snyk_report.py snyk-report.json --min-severity high
```

---

### 5. Gerar relatório estruturado

```
## Relatorio Snyk Code — [projeto]
Data: [data] | Total: X | Criticos/Altos: Y

### CRITICO / ALTO
[1] python/SqlInjection — app/db.py:42
- CWE: CWE-89
- Priority Score: 850/1000
- Descricao: Input nao sanitizado flui para query SQL.
- Autofixavel: Nao

### Resumo por categoria
| Categoria        | Qtd |
| SqlInjection     |  2  |
| HardcodedSecret  |  3  |
```

---

### 6. Mapeamento OWASP

Para projetos com LLMs: consultar `references/cwe-owasp-llm-mapping.md`
Para projetos web/backend: usar OWASP Top 10 padrão.

---

### 7. Integração CI/CD

**GitHub Actions:**
```yaml
name: Snyk Code SAST
on: [push, pull_request]
jobs:
  snyk-code:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: code test
          args: --severity-threshold=high --sarif-file-output=snyk-code.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: snyk-code.sarif
```

**GitLab CI:**
```yaml
snyk-code:
  image: snyk/snyk:node
  script:
    - snyk auth $SNYK_TOKEN
    - snyk code test --severity-threshold=high --json > snyk-report.json
  artifacts:
    paths: [snyk-report.json]
  allow_failure: true
```

**Azure DevOps:**
```yaml
- task: CmdLine@2
  displayName: Snyk Code SAST
  env:
    SNYK_TOKEN: $(SNYK_TOKEN)
  inputs:
    script: |
      npm install -g snyk
      snyk code test --severity-threshold=high --json > snyk-report.json
```

---

### 8. Modo offline / sem CLI

Se o Snyk CLI não estiver disponível, Claude realiza análise semântica cobrindo:
Injection flaws, Broken Access Control, Insecure Deserialization, Hardcoded Secrets,
Path Traversal, SSRF, Cryptographic weaknesses, Prototype Pollution, XSS.

Sempre informar ao usuário quando a análise é semântica (sem CLI real).

---

## Referências

- `references/snyk-cli-reference.md` — todos os comandos e flags
- `references/cwe-owasp-llm-mapping.md` — mapeamento CWE para OWASP LLM Top 10
- `scripts/parse_snyk_report.py` — parser do JSON do Snyk
