---
name: security-fix
description: Security remediation en vulnerability fix skill. Past fixes toe voor kwetsbaarheden uit security check-rapporten. Automatische dependency updates, configuratie-patches, code fixes via Edit tool, en PR-creatie. Gebruik na een security audit/scan om kritieke en hoge severity issues op te lossen.
---

# Security Fix

Je bent een security engineer die kwetsbaarheden fixt. Gebruik deze instructies om audit-bevindingen systematisch op te lossen.

## Wanneer activeren

Activeer deze skill wanneer de gebruiker:
- Vraagt om "security fixes toe te passen" of "kwetsbaarheden te fixen"
- Verwijst naar een audit rapport en vraagt om remediatie
- Vraagt om "dependencies te updaten" vanwege security issues
- Een PR wil maken met security patches
- `/security-fix` gebruikt als commando

## Stap 1: Audit rapport inlezen

### Van JSON bestand
Als er een audit rapport beschikbaar is (v2.0 schema, zie `security-check/references/tool-output-schemas.md`):
```bash
cat security_reports/security_audit_*.json
```

Lees het rapport en categoriseer findings per `fix_type`:
- **`dependency`**: Automatisch fixbaar met package manager
- **`auto`**: Configuratie-fix, automatiseerbaar
- **`manual`**: Code-wijziging vereist, menselijke review nodig

### Van inline bevindingen
Als de gebruiker bevindingen beschrijft zonder JSON, stel zelf de categorisering op.

## Stap 2: Fix strategie bepalen

### Veilig voor automatisering (geen bevestiging nodig):
- Dependency version updates (na dry-run)
- Configuratie flags: debug=false, https=true, secure cookies
- Security headers toevoegen
- Ingebouwde security features activeren

### Menselijke review vereist (altijd bevestiging vragen):
- Code logica wijzigingen
- Database schema wijzigingen
- Authenticatie/autorisatie wijzigingen
- Breaking API changes
- Secret rotatie (informeer, niet automatisch uitvoeren)

## Stap 3: Dependency fixes

### Ecosysteem detecteren
```bash
ls package.json pnpm-lock.yaml yarn.lock requirements.txt Pipfile pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
```

### Per package manager

| Ecosysteem | Audit commando | Fix commando |
|-----------|---------------|-------------|
| npm | `npm audit --json` | `npm audit fix` |
| pnpm | `pnpm audit --json` | `pnpm audit --fix` |
| yarn | `yarn audit --json` | `yarn upgrade` |
| pip | `pip-audit --format json` | `pip-audit --fix` |
| pipenv | `pipenv check` | `pipenv update` |
| poetry | - | `poetry update` |
| cargo | `cargo audit --json` | `cargo update` |
| go | `govulncheck ./...` | `go get -u ./... && go mod tidy` |
| maven | - | `mvn versions:use-latest-versions` |

### Script (alternatief):
```bash
python <skill_path>/scripts/apply_dependency_fixes.py <project_path> --dry-run
python <skill_path>/scripts/apply_dependency_fixes.py <project_path>
```

Draai altijd eerst `--dry-run` en toon de output aan de gebruiker voordat je de echte fix toepast.

## Stap 4: Configuratie fixes

### Met script:
```bash
python <skill_path>/scripts/apply_config_fix.py <config_pad> --preset disable_debug
python <skill_path>/scripts/apply_config_fix.py <config_pad> --preset secure_cookies
python <skill_path>/scripts/apply_config_fix.py <config_pad> --preset enable_https
python <skill_path>/scripts/apply_config_fix.py <config_pad> --preset enable_csrf
python <skill_path>/scripts/apply_config_fix.py <config_pad> --preset disable_cors_wildcard
```

### Met Claude's Edit tool (voorkeur voor kleine wijzigingen):
Gebruik de Edit tool direct voor configuratiebestanden. Voorbeelden:

**Debug mode uitzetten** (Django settings.py):
```
Edit: DEBUG = True -> DEBUG = False
```

**Secure cookies** (Express):
```
Edit: cookie: { secure: false } -> cookie: { secure: true, httpOnly: true, sameSite: 'strict' }
```

**CORS restrictie**:
```
Edit: origin: '*' -> origin: 'https://yourdomain.com'
```

## Stap 5: Code fixes (manual fix_type)

Voor code-level kwetsbaarheden, gebruik Claude's Edit tool. Raadpleeg het referentiebestand voor specifieke fix-patronen:

```
Read: <skill_path>/references/fix-patterns.md
```

### Beschikbare fix-patronen

| Categorie | Kwetsbaarheden |
|-----------|---------------|
| Injection | SQL Injection, Command Injection, NoSQL Injection, SSTI |
| XSS | XSS Prevention, React Unsafe HTML, Target _blank |
| Crypto | Weak Crypto, Insecure Random, Password Hashing, Unsafe YAML |
| Auth/Access | Hardcoded Secrets, NEXT_PUBLIC_ secrets, Mass Assignment, JWT Fixes |
| Network | SSRF, Open Redirect, Insecure TLS, Insecure Cookies, Security Headers |
| Data | Path Traversal, XXE, Insecure Deserialization, Prototype Pollution |
| Upload | File Upload Validatie |
| Supabase | service_role misuse, RLS ontbreekt |

**Belangrijk**: Lees altijd de omringende code voor context. Toon de voorgestelde wijziging aan de gebruiker voor bevestiging bij niet-triviale changes.

## Stap 6: Verificatie en rapportage

Na het toepassen van fixes:

1. **Tests draaien**:
```bash
# Detecteer en draai test suite
npm test || pytest || cargo test || go test ./... || mvn test
```

2. **Opnieuw scannen** (als tools beschikbaar zijn):
```bash
semgrep --config=auto --json --severity=ERROR <target_path>
trivy fs --format json --scanners vuln <target_path>
```

3. **Fix-resultaten JSON schrijven**:
Schrijf de resultaten naar `./security_reports/security_fix_<datum>.json` met dit schema:
```json
{
  "version": "1.0",
  "fix_date": "ISO8601",
  "target": "/pad",
  "source_audit": "pad/naar/audit.json",
  "results": [
    {
      "id": "finding-001",
      "status": "fixed|skipped|manual_review",
      "severity": "HIGH",
      "type": "check_id",
      "file": "pad",
      "line": 45,
      "message": "originele beschrijving",
      "fix_type": "auto|manual|dependency",
      "action_taken": "wat er gedaan is"
    }
  ],
  "summary": {
    "total_processed": 10,
    "fixed": 7,
    "skipped": 1,
    "manual_review": 2
  }
}
```

4. **HTML rapport genereren en openen**:
```bash
python <skill_path>/scripts/generate_fix_report.py ./security_reports/security_fix_<datum>.json ./security_reports/security_fix.html
open ./security_reports/security_fix.html
```

5. **Terminal samenvatting**:
Toon een beknopte samenvatting:
```
## Security Fix Samenvatting

- Gefixt: X bevindingen
- Resterend: Y bevindingen
- Handmatige review: Z bevindingen

Volledig rapport: `./security_reports/security_fix.html`
```

## Stap 7: PR creatie (optioneel)

Als de gebruiker een PR wil:

### Met script:
```bash
python <skill_path>/scripts/create_remediation_pr.py <project_path> \
  --title "fix: security remediation" \
  --severity high \
  --audit-ref "Audit rapport datum"
```

### Met Claude's Bash tool:
```bash
git checkout -b security-remediation-$(date +%Y%m%d)
git add -u  # Alleen tracked files, voorkomt het stagen van secrets
git commit -m "fix: security remediation - severity issues"
git push -u origin HEAD
gh pr create --title "Security Remediation" --body "..."
```

**Let op**: Gebruik `git add -u` (niet `git add -A`) om te voorkomen dat onbedoelde bestanden (secrets, credentials) meegenomen worden.

## Prioriteitsvolgorde

Pas fixes altijd toe in deze volgorde:
1. **CRITICAL** findings eerst
2. **HIGH** severity
3. **dependency** fixes (laag risico, hoge impact)
4. **auto** configuratie fixes
5. **manual** code fixes (hoogste risico, per stuk bevestigen)
6. **MEDIUM/LOW** als tijd toelaat
