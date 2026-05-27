---
name: vps-security-scanner
description: "Realiza auditoria de segurança completa em VPS Linux: análise de portas expostas, configuração SSH, vulnerabilidades em containers Docker, usuários do sistema, permissões, logs de acesso e pacotes instalados. Use quando o usuário pedir para verificar segurança do servidor, auditar VPS, escanear vulnerabilidades, ou gerar relatório de segurança do sistema. Suporta scan com trivy (containers) e grype (packages). Gera relatório estruturado por severidade (Critical/High/Medium/Low)."
version: 1.0.0
category: security
framework: doe
---

# VPS Security Scanner

Auditoria de segurança completa para servidores Linux (VPS). Integra varredura de rede, análise de configuração, scan de vulnerabilidades em containers Docker e pacotes do sistema.

**Objetivo:** Detectar e relatar falhas de segurança ANTES que sejam exploradas.

---

## Quando usar

- Usuário pede "audite a segurança do VPS"
- Execução diária via systemd timer (automação)
- Após deploy de novos containers ou serviços
- Quando houver suspeita de comprometimento
- Compliance / checklist de hardening (CIS Benchmarks)

---

## Fluxo DOE Obrigatório

| Passo | Ação |
|---|---|
| 1. **Análise** | Verificar acesso SSH, tools necessários instalados (nmap, trivy/grype) |
| 2. **Plano** | Apresentar checklist de scans que serão executados + tempo estimado |
| 3. **Aprovação** | Aguardar "DE ACORDO" do usuário (ou auto-executar se via timer) |
| 4. **Execução** | Rodar todos os scans em paralelo (network, ssh, docker, packages, users, logs) |
| 5. **Review** | Gerar relatório Markdown estruturado por severidade → Enviar via Telegram |

---

## Scans Executados

### 1. Network Security Scan
- **Ferramenta:** `nmap -sV -sC <VPS_IP>`
- **Detecta:** Portas abertas desnecessárias, serviços desatualizados, banners expostos
- **Severidade:** High se HTTP/FTP sem TLS, Medium se SSH na porta padrão 22

### 2. SSH Configuration Audit
- **Arquivo:** `/etc/ssh/sshd_config`
- **Checklist:**
  - [ ] ✅ `PermitRootLogin no`
  - [ ] ✅ `PasswordAuthentication no`
  - [ ] ✅ `PubkeyAuthentication yes`
  - [ ] ✅ `Port` diferente de 22 (opcional but recommended)
  - [ ] ❌ `PermitEmptyPasswords no`
  - [ ] ✅ `Protocol 2` (nunca Protocol 1)
- **Severidade:** Critical se root login habilitado, High se senha habilitada

### 3. Docker Vulnerability Scan
- **Ferramenta:** `trivy image --severity HIGH,CRITICAL <image>`
- **Escopo:** Todas imagens Docker em uso (`docker ps --format '{{.Image}}'`)
- **Detecta:** CVEs conhecidas em packages dentro dos containers
- **Severidade:** Herdada do Trivy (Critical/High/Medium/Low)

### 4. System Package Vulnerabilities
- **Ferramenta:** `grype <OS>` ou `apt list --upgradable` (Ubuntu/Debian)
- **Detecta:** Pacotes do sistema desatualizados com CVEs conhecidas
- **Severidade:** Critical se kernel desatualizado, High se serviços de rede

### 5. User Account Audit
- **Comando:** `cat /etc/passwd | grep -v nologin`
- **Checklist:**
  - [ ] Usuários com UID 0 além de root → **Critical**
  - [ ] Usuários sem home directory ou shell inválida → **Medium**
  - [ ] Contas de serviço com shell de login → **Low**
- **Severidade:** Critical se múltiplos UID 0, Medium se contas órfãs

### 6. File Permission Audit
- **Comandos:**
  - `find / -perm -4000 -type f` (arquivos SUID)
  - `find /etc -type f -perm -002` (arquivos world-writable em /etc)
- **Severidade:** High se SUID em binários suspeitos, Critical se /etc writable

### 7. Log Analysis (Auth Failures)
- **Arquivo:** `/var/log/auth.log` (Debian/Ubuntu) ou `/var/log/secure` (RHEL)
- **Detecta patterns:**
  - Tentativas de login SSH falhadas (brute force)
  - Sudo failures
  - Logins de IPs desconhecidos
- **Severidade:** High se > 100 tentativas falhadas na última hora

### 8. Firewall Check
- **Comandos:** `ufw status` ou `iptables -L -n`
- **Detecta:** Firewall desabilitado ou regras permissivas demais
- **Severidade:** High se firewall inexistente, Medium se política INPUT accept all

---

## Scripts Necessários

Os scripts ficam em `.agents/skills/vps-security-scanner/scripts/`:

### `run-all-scans.sh`
```bash
#!/bin/bash
# Executa todos os scans em paralelo e salva outputs

OUTPUT_DIR="/tmp/vps-security-scan-$(date +%s)"
mkdir -p "$OUTPUT_DIR"

# Network scan
nmap -sV -sC ${VPS_IP:-localhost} > "$OUTPUT_DIR/nmap.txt" 2>&1 &

# SSH config
cat /etc/ssh/sshd_config > "$OUTPUT_DIR/sshd_config.txt" &

# Docker scan (se Docker instalado)
if command -v docker &> /dev/null; then
  docker ps --format '{{.Image}}' | xargs -I {} trivy image --severity HIGH,CRITICAL {} > "$OUTPUT_DIR/trivy.txt" 2>&1 &
fi

# Package scan
apt list --upgradable 2>/dev/null > "$OUTPUT_DIR/upgradable.txt" &

# User audit
cat /etc/passwd | grep -v nologin > "$OUTPUT_DIR/users.txt" &

# SUID files
find / -perm -4000 -type f 2>/dev/null > "$OUTPUT_DIR/suid.txt" &

# Auth log
tail -n 500 /var/log/auth.log > "$OUTPUT_DIR/auth.txt" 2>&1 &

# Firewall
ufw status verbose > "$OUTPUT_DIR/firewall.txt" 2>&1 || iptables -L -n > "$OUTPUT_DIR/firewall.txt" 2>&1 &

wait # Aguarda todos os jobs
echo "$OUTPUT_DIR"
```

### `parse-results.py`
```python
#!/usr/bin/env python3
"""
Processa outputs dos scans e gera relatório estruturado
"""
import os
import sys
import json
import re
from datetime import datetime

def main():
    output_dir = sys.argv[1]
    findings = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': [],
        'info': []
    }
    
    # Parse nmap (portas abertas)
    # Parse ssh config (hardening)
    # Parse trivy (CVEs)
    # Parse users (UID 0)
    # Parse SUID (binários perigosos)
    # Parse auth.log (brute force)
    # Parse firewall (regras)
    
    # Gerar relatório Markdown
    report = generate_markdown_report(findings)
    print(report)

def generate_markdown_report(findings):
    report = f"""# 🔒 VPS SECURITY SCAN REPORT
**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Host:** {os.getenv('VPS_HOST', 'localhost')}

---

## 📊 RESUMO EXECUTIVO

| Severidade | Quantidade |
|---|---|
| 🔴 Critical | {len(findings['critical'])} |
| 🟠 High | {len(findings['high'])} |
| 🟡 Medium | {len(findings['medium'])} |
| 🔵 Low | {len(findings['low'])} |
| ⚪ Info | {len(findings['info'])} |

---

## 🔴 CRITICAL FINDINGS

"""
    # Continue formatando...
    return report

if __name__ == '__main__':
    main()
```

---

## Formato do Relatório

```markdown
# 🔒 VPS SECURITY SCAN REPORT
**Data:** 2026-04-09 18:30:15
**Host:** 147.93.69.211

---

## 📊 RESUMO EXECUTIVO

| Severidade | Quantidade |
|---|---|
| 🔴 Critical | 2 |
| 🟠 High | 5 |
| 🟡 Medium | 8 |
| 🔵 Low | 3 |
| ⚪ Info | 12 |

**CLASSIFICAÇÃO GERAL:** ⚠️ ATENÇÃO NECESSÁRIA

---

## 🔴 CRITICAL FINDINGS

### [C-001] Root Login Habilitado via SSH
- **Categoria:** Acesso Não Autorizado
- **Arquivo:** `/etc/ssh/sshd_config`
- **Evidence:** `PermitRootLogin yes`
- **Impacto:** Permite acesso direto como root se senha for comprometida
- **Recomendação:**
  ```bash
  sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
  systemctl restart sshd
  ```

### [C-002] CVE-2024-1234 em imagem Docker nginx:latest
- **Categoria:** Vulnerabilidades Conhecidas
- **Container:** nginx-proxy
- **CVE:** CVE-2024-1234 (CVSS 9.8)
- **Descrição:** Remote Code Execution via crafted HTTP header
- **Recomendação:**
  ```bash
  docker pull nginx:1.25.4-alpine
  docker-compose up -d nginx-proxy
  ```

---

## 🟠 HIGH FINDINGS

### [H-001] Porta 3306 (MySQL) exposta publicamente
- **Categoria:** Network Exposure
- **Evidence:** `nmap` mostra `3306/tcp open mysql`
- **Recomendação:** Configurar firewall para permitir apenas IPs autorizados
  ```bash
  ufw deny 3306/tcp
  ufw allow from 10.0.0.0/24 to any port 3306
  ```

... (continua para Medium, Low, Info)

---

## ✅ RECOMMENDED ACTIONS (Priority Order)

1. 🔴 **Desabilitar root login SSH** (Critical — 5 min)
2. 🔴 **Atualizar imagem nginx** (Critical — 2 min)
3. 🟠 **Fechar porta 3306** (High — 2 min)
4. 🟠 **Instalar fail2ban** (High — 10 min)
...

---

## 📈 COMPLIANCE STATUS

- [x] CIS Benchmark 1.1 - Ensure mounting of cramfs filesystems is disabled
- [ ] CIS Benchmark 2.2.6 - Ensure SSH root login is disabled ← **FALHOU**
- [x] CIS Benchmark 3.4.1 - Ensure firewall is enabled
- [ ] CIS Benchmark 5.2.3 - Ensure SSH LogLevel is INFO or higher

**Score:** 72/100 (Aceitável, mas precisa melhorias)

---

**Scan Duration:** 42 segundos
**Next Scan:** Agendado para 2026-04-10 06:00 (systemd timer)
```

---

## Integração com Telegram

O relatório deve ser enviado via Telegram com:
- **Título:** 🔒 Daily Security Scan Report
- **Badge:** Se Critical findings > 0 → 🚨 | Se High findings > 5 → ⚠️ | Senão → ✅
- **Resumo:** Top 3 findings mais críticos
- **Link:** Arquivo completo salvo em `/opt/gueclaw-data/files/security-reports/YYYY-MM-DD.md`

---

## Dependências

| Tool | Instalação | Usado para |
|---|---|---|
| `nmap` | `apt install nmap` | Network scanning |
| `trivy` | `curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh` | Docker CVE scan |
| `grype` | `curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh` | Package CVE scan |
| `fail2ban` | `apt install fail2ban` | Log analysis (opcional) |

---

## Automação (Systemd Timer)

Ver: `.agents/skills/vps-security-scanner/systemd/` para configuração completa.

**Resumo:**
- Timer: `/etc/systemd/system/vps-security-scan.timer`
- Service: `/etc/systemd/system/vps-security-scan.service`
- Script: `/opt/gueclaw/automation/daily-security-scan.sh`
- Horário: 06:00 (America/Sao_Paulo) todos os dias
- Notificação: Telegram (sempre, independente de findings)

---

## Notas de Segurança

- Este scan **não substitui** um pentest profissional
- Falsos positivos podem ocorrer (ex: porta aberta intencionalmente)  
- Sempre confirme findings críticos manualmente antes de corrigir
- Logs de scan são armazenados em `/var/log/vps-security-scanner/`

---

**Autor:** GueClaw Security Guardian
**Versão:** 1.0.0
**Última atualização:** 2026-04-09
