---
name: check-helm
description: "Prueft Helm Chart-Dateien eines Kamerplanter-Komponente auf NFR-002-Konformitaet: SecurityContext, NetworkPolicies, Resource Limits, Health Probes, StatefulSet/Deployment-Unterscheidung, PVC-Konfiguration. Nutze diesen Skill nach Aenderungen an Helm-Charts oder beim Hinzufuegen neuer Komponenten."
argument-hint: "[Komponenten-Name, z.B. backend, worker, arango, redis]"
disable-model-invocation: true
---

# Helm-Chart-Check (NFR-002): $ARGUMENTS

## Schritt 1: Chart-Dateien laden

Suche die Helm-Dateien fuer die Komponente `$ARGUMENTS`:

```
helm/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml / statefulset.yaml
    ├── service.yaml
    ├── networkpolicy.yaml
    ├── configmap.yaml
    └── (weitere)
```

Lies parallel: `spec/nfr/NFR-002_Kubernetes-Plattform.md` (erste 60 Zeilen) und `spec/style-guides/HELM.md` fuer Referenz.

## Schritt 2: Stateless vs. Stateful prufen

Klassifiziere die Komponente:

| Typ | Erwartetes Workload-Objekt | Besonderheiten |
|-----|--------------------------|----------------|
| **Stateless** (Backend, Worker, Frontend) | `Deployment` | Kann beliebig skaliert werden |
| **Stateful** (ArangoDB, Redis, TimescaleDB) | `StatefulSet` | Geordnete Identitaeten, PVC pro Pod |

- ❌ Fehler: Stateful-Komponente als Deployment deployt
- ❌ Fehler: Stateless-Komponente als StatefulSet deployt

## Schritt 3: Security-Checks (NFR-002 §4)

Prüfe in `deployment.yaml` / `statefulset.yaml`:

```yaml
# MUSS vorhanden sein:
securityContext:
  runAsNonRoot: true
  runAsUser: 1000          # Kein root (0)
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]

# Container-Level:
resources:
  requests:
    memory: "..."
    cpu: "..."
  limits:
    memory: "..."
    cpu: "..."
```

## Schritt 4: NetworkPolicy prüfen

Prüfe ob `networkpolicy.yaml` existiert und folgende Regeln enthält:

- **Ingress:** Nur erlaubte Sources (z.B. nur Traefik → Backend)
- **Egress:** Nur benoetigte Destinations (z.B. Backend → ArangoDB, Redis)
- **Default-Deny:** `podSelector: {}` mit leeren ingress/egress-Regeln als Basis

## Schritt 5: Health Probes prüfen

```yaml
# MUSS in jedem Deployment/StatefulSet vorhanden sein:
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Schritt 6: Sonstige NFR-002-Checks

- **ConfigMaps/Secrets:** Keine hardcodierten Secrets in values.yaml (Referenz auf Secret-Objekte)
- **Image-Tags:** Keine `latest`-Tags — spezifische Minor-Version (z.B. `python:3.14-slim`)
- **HPA:** Vorhanden fuer stateless Komponenten? `minReplicas` / `maxReplicas` definiert?
- **PodDisruptionBudget:** Fuer kritische Stateful-Komponenten vorhanden?
- **bjw-s/common Chart:** Wird der gemeinsame Helm-Chart-Typ korrekt genutzt?

## Schritt 7: Report ausgeben

```markdown
# Helm-Chart-Review: {Komponente}

## Workload-Typ
{Deployment/StatefulSet — korrekt/falsch}

## Security-Context
{Checkliste: runAsNonRoot, readOnlyRootFilesystem, capabilities.drop, resource limits}

## NetworkPolicy
{Existiert: ja/nein | Ingress-Regeln: {N} | Egress-Regeln: {N}}

## Health Probes
{liveness: ✅/❌ | readiness: ✅/❌}

## Sonstige Findings
{Nummerierte Liste mit Pfad:Zeile und Beschreibung}

## Bewertung
- ✅ NFR-002-konform / ❌ {N} Violations gefunden
```
