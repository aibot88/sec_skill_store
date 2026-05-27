---
name: cowork.generiere_material
description: "Phase-3-Pipeline-Skill (T-31-3, ADR 0034) für Material-Generation zu existierender UE im Cowork-Mode. Trigger: 'Erzeuge AB für KW##', 'Generiere Material zur UE', 'AB / Lösungsblatt / PPP', 'Material-Set für Stunde', 'Plugin-Output'. Eingabe: TUV-Pfad (v2.1 mit erwartungshorizont) ODER Sequenz-Stand-Verweis + Material_Geruest (Track-AC-Output). Output: AB n1+n2+n3 + Lösungsblätter (= Erwartungshorizont-Visualisierung, ADR_0040 + ADR_0052) + PPP + Tafelbild + _manifest.md. Komposition: artefakte-generator (Phase-1-Orchestrator) + cowork.bd_hook_p23_material (R57 Track-C Phase-3) + cowork.audit_pre_commit. Persistierung erst nach Lehrkraft-Bestätigung. NICHT-Trigger: Kein reines AB-Single-Output (das ist artefakt-arbeitsblatt); kein UE-Authoring/Planning (das ist upstream Sequenz-/UE-Planungs-Skills)."
domain_scope: universal
schema_pin: tuv_v2.1
phase: phase_3
mode: cowork-first
skill_typ: pipeline
adr_refs: [ADR_0007, ADR_0008, ADR_0017, ADR_0019, ADR_0030, ADR_0032, ADR_0033, ADR_0034, ADR_0040, ADR_0052]
empirie_refs:
  - docs/architektur/track_delta_material_parser_compiler/00_design.md
  - docs/architektur/track_delta_material_parser_compiler/spike_notes/00_konsolidierung.md
  - decisions/0081-track-delta-material-parser-compiler-scope-lock.md
bd_hook_pre_run: cowork.bd_hook_p23_material
---

## BD-Hook P2.3 Trigger-Punkt (R57-Iteration Track-C Phase-3, ADR_0052)

**Pre-Material-Generation, post-TUV+Material_Geruest-Read:** Trigger `cowork.bd_hook_p23_material`-Skill als Validator. Hook prüft ob Material_Geruest.didaktische_orte[] + AB-Konzept addressieren TUV.phasen[].erwartungshorizont.kognitive_zielzustaende.

**Lösungsblatt-Generation = Erwartungshorizont-Visualisierung (ADR_0040 + ADR_0052):** Lösungsblatt visualisiert sicherbare_kernerkenntnisse pro Phase. Tafelbild-Generation analog.

**Hook-FAIL-Konsequenz:** Material-Konzept-Refactor pflichtig pre-AB-Render (Track-R-Cross-Reference).

# Pipeline-Skill `cowork.generiere_material`

## Trigger-Beispiele

- "Erzeuge AB für KW##"
- "Generiere Material zur UE"
- "AB / Lösungsblatt / PPP für Stunde"
- "Material-Set für Stunde"
- "Plugin-Output"

## Komposition

```
1. lehrkraft_project_instructions.md → Material-Konventionen + Niveau-Mix
2. TUV-File laden (geplant oder gehalten)
3. artefakte-generator-Orchestrator-Skill triggern (Phase-1-Pipeline):
   - artefakt-recherche → _recherche.yaml
   - artefakt-arbeitsblatt × {n1, n2, n3} → AB.docx + lsg.docx
   - PPP-Folien-Plan via pptx_writer
4. cowork.audit_pre_commit → DSGVO + 60a + Mager + Niveau-Trennschärfe
5. Lehrkraft-Preview im Chat
6. Persist + _manifest.md
```

## Pflicht-Kontext (ADR_0061 Dual-Pfad-Konvention — TUV ist primärer Anker)

**TUV-Layer (Pflicht):**
1. TUV-File (Vertragsfeld-Treue laut tuv_v2.1.json) — primärer Konsumptions-Anker für KE-Lernziel + Phasen-Verlauf

**Pfad-B (Verbatim-Lehrplan-Layer, Indirekt via TUV):**
2. `core/fach/<fach_id>/lp_lernbereiche/LP-<fach_id>-LB<n>.yaml` — Konsumiert via TUV-Lehrplan-Verbatim-Footer (Pfad-A NICHT konsumiert in Material-Render)

**Setup-Layer:**
3. `lehrkraft_project_instructions.md` (Material-Konventionen + AB-Layout-Präferenzen)

**Recherche-Layer:**
4. Recherche-Briefing falls vorhanden (`_recherche.yaml` mit Lizenz-Klassifikation)

**Konfig-Layer:**
5. `core/config/niveaustufen.json` (Antwortformat-Pool)
6. `core/config/methode_zu_antwortformat.yaml` (Format-Hint pro TUV-Phase-6-Methode)

## Reasoning-Schritte

1. **TUV identifizieren** (aus Trigger-Argument oder Sequenz-Stand)
2. **TUV-Schema-Validate** via `core/scripts/validate_tuv.py`
3. **Niveau-Mix bestimmen** via `waehle_niveaus(tuv)` aus AFB-Spektrum der Teilziele
4. **Recherche** ggf. aus Cache (`_recherche.yaml`) oder via `artefakt-recherche`-Skill
5. **Pro Niveau** (n1/n2/n3 falls in Mix):
   - `methode_mapping` → format-Hint + bewertungs_pattern
   - `aufgabe.formulieren` × Teilziel → LLM-Aufgabe (Cowork: Claude reasont)
   - `mager.konjugieren` → S-Perspektive
   - Layout-Render: `lib/layout.py:render_ab` → AB.docx
   - Lösungsblatt mit per-Aufgabe-Erwartungshorizont
6. **PPP** via `pptx_writer` (alle Folien-Phasen aus TUV)
7. **Tafelbild-Skizze** (ASCII oder Markdown — wenn `tafelbild` in Material-Auswahl)
8. **Audit**: `cowork.audit_pre_commit`-Skill (60a-Footer, Attribution, Mager-Schema, Niveau-Trennschärfe)
9. **Lehrkraft-Preview** im Chat → Bestätigung pro Niveau
10. **Persist** mit Naming-Convention `KW##_DDMMYY_<slug>_<typ>[_n<i>][_lsg].docx`
11. **`_manifest.md`** mit Provenance-Trail (TUV-SHA, Quellen, Audit-Status, Zeitstempel)

### Schritt 4a: K4a-Plan-Preview (Track-Δ NEU)

Nach Composer-Lauf, **vor Renderer**:

- `render_k4a_preview(plan)` → Markdown-Tabelle im Chat (1 Tabelle pro Niveau)
- Edit-Action-Vokabular für Lehrkraft:
  - `drop <chain_step_id>` — Schritt aus Plan entfernen
  - `swap <baustein_id> <new_baustein_id>` — Baustein austauschen
  - `reorder <chain_step_id> <new_position>` — Sequenz verschieben
- Lehrkraft-Approve → Schritt 5
- Reject → Re-Iterate (KEINE docx erzeugt — atomic-staging noch nicht aktiv)

### Schritt 5b: Renderer (Atomic-Output, Track-Δ)

`render_paper(model, output_root, kw, when, slug)`:
- Schreibt in `.staging/<run_id>/`-Folder
- Idempotenz-Hash auf File-Content basiert (Δ-3 Audit-Fix: mtime-aware)
- Bei Render-Exception: staging-folder cleanup, kein partial-Output

### Schritt 5c: K4b-Final-Approve (Track-Δ)

- Lehrkraft sieht 6 docx-Files (Pfade im Chat) sowie `_manifest.md`
- Approve → atomic-rename `staging/<run_id>/` → `output_root/run_<idempotenz>/`
- Reject → `staging/<run_id>/` löschen, keine bleibenden Files

**F1-Style Error-Handling (K4a/K4b zweistufig):**
- **K4a-Reject** mit Edit-Action (drop/swap/reorder): Re-Iterate, **max-Retry = 3**. Nach 3 Rejects: Eskalation zu Lehrkraft "Bitte UE-Planung in Phase-D revidieren."
- **K4a-Approve → Schritt 5b (Renderer)** mit Atomic-Output in staging
- **K4b-Reject** (Lehrkraft sieht 6 docx + manifest, ablehnt): `.staging/<run_id>/` löschen — keine bleibenden Files
- **K4b-Approve** → atomic-rename in Final-Output
- **Render-Crash** (Renderer-Exception): staging-cleanup automatisch (atomic_render-Pattern), keine partial-Files, Lehrkraft sieht Fehler-Report

(Track-Δ ADR_0081 proposed.)

## Output-Schema

```yaml
tuv_file: <pfad>
generierte_files:
  - AB_n1.docx, AB_n1_lsg.docx
  - AB_n2.docx, AB_n2_lsg.docx
  - AB_n3.docx, AB_n3_lsg.docx
  - PPP.pptx
  - Tafelbild.md
manifest_file: _manifest.md
audit_status: PASS | FAIL
audit_findings: [<liste>]
lehrkraft_bestaetigt: bool
total_attribution_lines: <n>
```

## Anti-Pattern

- Material ohne TUV-Schema-Validate (Drift-Risk → Generation auf falschem Schema)
- Material ohne KE-Pflicht-Anker (Track-β-2 + ADR_0064): jedes Material-Geruest hat ke_refs Pflicht (>=1 Kompetenzerwartung die operationalisiert wird). IK-Beispiel-Pool optional (Gegenstaende fuer KE-Bildung).
- AFB-Tags / Mager-Notation im AB-Schauseite (ADR 0008)
- Lösungsblatt mit konstantem Erwartungshorizont pro UE (RA3-HIGH-3 aus T-30-9-Audit)
- Differenzierungs-Marker fehlt obwohl Klassen-Kontext welche fordert
- 60a-Footer fehlt
- Attribution nur in separater `attribution.txt` statt im AB-Footer (RA4-HIGH-6)
- Persist ohne `cowork.audit_pre_commit`-Pass

## DSGVO-Reminder (ADR 0022 Pflicht)

Material (AB / Lösungsblatt / Folien / Tafelbild / Karten / Stationen) kann personenbezogene Beispiele enthalten:

- KEINE Klarnamen in Beispiel-Sätzen / Aufgabe-Vignetten / Differenzierungs-Hinweisen
- Pseudonyme Konvention: Initialen (A.B.) ODER fiktive Identifikationsfiguren (Mia/Johann/Anna/Peter)
- AVV-Marker prüfen vor LLM-Call für Material-Generierung
- Identifikationsfiguren bleiben fiktiv — keine echten SuS-Bezüge in AB-Vignetten

Verstoß = § 26 BayDSG-Risk + § 203 StGB-Risk.

## Cross-Refs

- ADR 0007 TUV-Schema-Treue
- ADR 0008 Schauseite-vs-Formalstruktur
- ADR 0022 Datenschutz (Pseudonymisierung in Material-Output)
- ADR 0034 Pipeline-Skill-Workflow
- ADR 0035 Multi-Layer-Evaluation (Layer-1 DSGVO-Compliance)
- T-30-9 BEFUND_PHASE_2_BUNDLE_AUDIT.md (RA3-HIGH-3/4/5/6 als Akzeptanz-Kriterien)
