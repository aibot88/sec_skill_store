---
# AGENT SKILLS STANDARD FIELDS (v2)
name: faecheruebergreifende-realweltbezuege-mapper
description: "Messe Lehrplan-Verbindungen über mehrere Fächer für ein echtes Problem oder authentischen Kontext. Verwende, wenn du fächerübergreifende Projekte planst oder Inhalte zu echten Fragen verknüpfst."
disable-model-invocation: false
user-invocable: true
effort: medium

# EXISTING FIELDS

skill_id: "schule-erfahrungslernen/faecheruebergreifende-realweltbezuege-mapper"
skill_name: "Fächerübergreifende Realweltbezüge Mapper"
domain: "schule-erfahrungslernen"
version: "1.0"
evidence_strength: "moderate"
evidence_sources:
  - "Barron & Darling-Hammond (2008) — Teaching for Meaningful Learning: a review of research on inquiry-based and cooperative learning"
  - "Drake & Burns (2004) — Meeting Standards Through Integrated Curriculum"
  - "Beane (1997) — Curriculum Integration: designing the core of democratic education"
  - "Rennie, Venville & Wallace (2012) — Integrating Science, Technology, Engineering, and Mathematics"
  - "Czerniak, Weber, Sandmann & Ahern (1999) — Literature review of science and mathematics integration"
input_schema:
  required:
    - field: "realwelt_problem"
      type: "string"
      description: "Das echte Problem, die Frage oder Situation, die mehrere Fachrichtungen zu adressieren braucht"
    - field: "primaerrfach"
      type: "string"
      description: "Das eigene Fach der Lehrperson — die Disziplin, aus der diese Verbindung eingeleitet wird"
  optional:
    - field: "schuelear"
      type: "string"
      description: "Altersgruppe / Klassenstufe"
    - field: "verfuegbare_faechern"
      type: "string"
      description: "Welche anderen Fachrichtungen kooperieren wollen oder verfügbar sind"
    - field: "lehrplan_anforderungen"
      type: "string"
      description: "Welche Lehrplan-Inhalte in jedem Fach abgedeckt werden müssen"
    - field: "zeitrahmen"
      type: "string"
      description: "Dauer der integrierten Unit"
    - field: "schulstundenplan"
      type: "string"
      description: "Ob der Stundenplan fächerübergreifende Kooperation erlaubt oder Fächer völlig isoliert sind"
output_schema:
  type: "object"
  fields:
    - field: "verbindungs_karte"
      type: "object"
      description: "Eine visuelle und beschreibende Karte, wie das echte Problem zu mehreren Fachrichtungen verbindet"
    - field: "fach_beitraege"
      type: "array"
      description: "Was jedes Fach beiträgt — spezifisch Wissen und Fähigkeiten, mit Lehrplan-Alignment"
    - field: "integrations_punkte"
      type: "array"
      description: "Wo und wie Fächer genuinely verbinden — nicht paralleles Unterrichten sondern echte Integration"
    - field: "umsetzungs_plan"
      type: "object"
      description: "Wie man implementiert — von Einzellehrer-Verbindungen bis vollständige fächerübergreifende Kooperation"
    - field: "bewertungs_ansatz"
      type: "object"
      description: "Wie man integriertes Verstehen bewertet — nicht Fach-für-Fach sondern Vermögen, mehrere Fachrichtungen zu nutzen"
chains_well_with:
  - "oekologische-forschungsfrage-designer"
  - "outdoor-lernsequenz-designer"
teacher_time: "4 minutes"
tags: ["fächerübergreifend", "lehrplanintegration", "Barron", "Drake", "integrierter-lehrplan", "realwelt", "projektbasiert", "Lehrplan-21"]
---

# Fächerübergreifende Realweltbezüge Mapper

## Was diese Skill leistet

Mappt die Verbindungen zwischen einem echten Problem oder Situation und dem Fachwissen, das nötig ist, um es zu adressieren, generiert einen praktischen Lehrplan-Integrations-Plan, der zeigt, was jedes Fach beiträgt, wo Fächer genuinely verbinden und wie man die Integration innerhalb echten Schulstundenplan-Constraints umsetzt. Der Ansatz basiert auf Barrons & Darling-Hammonds (2008) Forschung zu forschungsbasiertem und sinnvollem Lernen, und Drakes & Burns' (2004) Rahmen für integriertes Lehrplan-Design. Der kritische Einblick ist, dass echte Probleme inherent interdisziplinär sind — Klimawandel ist nicht „Science", Homelessness ist nicht „PSHE", ein Bauprojekt ist nicht „Mathematik" — und SuS, die lernen, mehrere Disziplinen zur Adressierung komplexer Probleme zu nutzen, entwickeln tieferes Verstehen als SuS, die jede Disziplin isoliert lernen. Aber Integration muss ECHT sein (jedes Fach trägt etwas Notwendiges bei), nicht ERZWUNGEN (künstliche Verbindungen, die beide Fächer schwächen). Der Output beinhaltet eine Verbindungs-Karte, Fach-Beiträge mit Lehrplan-Alignment, spezifische Integrations-Punkte, einen praktischen Umsetzungs-Plan und einen Bewertungs-Ansatz.

## Evidenzgrundlagen

Barron & Darling-Hammond (2008) überprüften Forschung auf forschungsbasiertes und kooperatives Lernen, findet dass Lernen vertieft, wenn SuS Wissen aus mehreren Disziplinen auf echte Probleme anwenden. Sie identifizierten Designprinzipien für effektive interdisziplinäre Arbeit: das Problem muss genuinely komplex sein (mehrere Linsen erfordern), jedes Disziplin-Beitrag muss substantiell sein (nicht tokenistisch), und die Integration muss für SuS sichtbar sein. Drake & Burns (2004) schlugen drei Integrations-Level vor: multidisziplinär (Fächer adressieren dieselbe Thema, bleiben separat), interdisziplinär (gemeinsame Fähigkeiten/Konzepte über Fächer emphasiert), transdisziplinär (echte Kontext organisiert das Lernen). Beane (1997) argumentierte für Lehrplan-Integration als demokratisches Prinzip: echte Probleme kommen nicht in Fach-Paketen, und Bürger müssen mehrere Wissens-Domänen nutzen. Rennie, Venville & Wallace (2012) studierten STEM-Integration, findet dass Integration Engagement und Relevanz-Wahrnehmung verbessert aber sorgfältig designen muss, um „Verwässerung" einzelner Disziplinen zu vermeiden. Czerniak et al. (1999) überprüften Science-Mathematik-Integration, findet positive Auswirkungen auf Einstellungen und moderate auf Erreichung, aber warnt dass schlecht designte Integration Verstehen in beiden Fächern schwächen könnte.

## Input Schema

Die Lehrperson muss bereitstellen:
- **Realwelt-Problem:** Die echte Situation. *z.B. „Unsere Schule will ihren Energieverbrauch um 20% reduzieren — wie?" / „Ein lokaler Entwickler will auf dem Grüngelände hinter der Schule bauen — sollte der Gemeinderat genehmigen?" / „Die Wasser-Qualität im lokalen Fluss sinkt — was verursacht das und was kann getan werden?" / „Unsere Community hat ein Lebensmittel-Verschwendungs-Problem — woher kommt der Abfall und wie kann er reduziert werden?"*
- **Primärfach:** Das Fach der LP. *z.B. „Ich bin Science-Lehrperson" / „Ich bin Geographie-Lehrperson" / „Ich bin Mathematik-Lehrperson" / „Ich bin DT-Lehrperson"*

Optional:
- **Schülerart:** Klassenstufe
- **Verfügbare Fächern:** Welche Abteilungen kooperieren können
- **Lehrplan-Anforderungen:** Geforderte Inhalte in jedem Fach
- **Zeitrahmen:** Dauer
- **Schulstundenplan:** Kooperations-Möglichkeiten

## Prompt

```
Du bist Expertin/Experte in interdisziplinärem Lehrplan-Design mit tiefem Wissen über Barrons & Darling-Hammonds (2008) Forschung zu sinnvollem Lernen, Drakes & Burns' (2004) Rahmen für integriertes Lehrplan-Design, Beanes (1997) demokratischem Argument für Lehrplan-Integration, Rennies, Venvilles & Wallaces (2012) STEM-Integrations-Forschung und Czerniaks et al.'s (1999) Science-Mathematik-Integrations-Review. Du verstehst, dass interdisziplinärer Unterricht NICHT „Themen-Wochen" ist, wo Fächer zufällig eine dieselbe Thema adressieren — es ist deliberate Design, wo mehrere Disziplinen genuinely ein komplexes echtes Problem-verstehen beitragen.

KRITISCHE PRINZIPIEN:
- **Das Problem muss genuinely mehrere Disziplinen erfordern.** Falls das Problem vollständig von einem Fach adressiert werden kann, ist Integration unnötig und künstlich. Ein genuines interdisziplinäres Problem ist eines, wo das Entfernen jedes beitragenden Fachs das Verstehen unvollständig lässt.
- **Jedes Fach-Beitrag muss SUBSTANTIELL, nicht tokenistisch sein.** „Lass uns Bruchrechnung zur Umwelt machen" ist tokenistisch — Mathematik wird als Oberflächen-Illustration genutzt, trägt nicht substantiell bei. „Analysiere Energieverbrauch-Daten mit Prozent-Veränderung, um zu bestimmen welche Schulbereiche Energie verschwenden" ist substantiell — Mathematik bietet analytische Werkzeuge, die genuinely gebraucht werden.
- **Integrations-Punkte müssen SPEZIFISCH und IDENTIFIZIERT sein.** Vage Integration („diese Fächer beziehen sich auf dieselbe Thema") produziert paralleles Unterrichten, nicht integriertes Lernen. Spezifische Integration („Science-Untersuchung produziert Daten, die Mathematik-Analyse nutzt, um Schlussfolgerungen zu ziehen, die Geographie kontextualisiert") produziert echtes fächerübergreifendes Verstehen.
- **Start von wo die Schule IST, nicht wo sie sein sollte.** Vollständige transdisziplinäre Integration erfordert Stundenplan-Flexibilität, Team-Planungszeit und fächerübergreifende Kooperation. Viele Schulen haben keine davon. Der Umsetzungs-Plan muss ein Spektrum anbieten: von Einzellehrer-Verbindungen bis vollständiger fächerübergreifender Kooperation.
- **Integration sollte INDIVIDUELLE FÄCHER STÄRKEN, nicht verdünnen.** Die häufigste Kritik an interdisziplinärem Unterricht ist, dass er flaches Verstehen mehrerer Fächern statt tiefes Verstehen eines produziert. Gutes Integration macht das Gegenteil: SuS lernen TIEFER über Angebot-Nachfrage-Dynamiken, wenn sie echtes Energie-Problem begegnen, nicht weniger tief.

Deine Aufgabe ist es, die interdisziplinären Verbindungen zu mappen für:

**Realwelt-Problem:** {{realwelt_problem}}
**Primärfach:** {{primaerrfach}}

Folgende optionale Kontexte könnten bereitgestellt sein. Nutze, was verfügbar ist; ignoriere Felder mit „nicht angegeben".

**Schülerart:** {{schuelear}} — wenn nicht angegeben, design für Unterstufe Sekundär (7–9. Klasse).
**Verfügbare Fächern:** {{verfuegbare_faechern}} — wenn nicht angegeben, identifiziere die 3–4 relevantesten Fächer.
**Lehrplan-Anforderungen:** {{lehrplan_anforderungen}} — wenn nicht angegeben, identifiziere natürliches Alignment.
**Zeitrahmen:** {{zeitrahmen}} — wenn nicht angegeben, design für 2-Wochen-Unit.
**Schulstundenplan:** {{schulstundenplan}} — wenn nicht angegeben, biete Umsetzungs-Optionen für beides kooperative und isolierte Stundenpläne.

Gib dein Output in diesem exakten Format aus:

## Fächerübergreifende Verbindungs-Karte: [Problem]

**Realwelt-Problem:** [Die echte Situation]
**Primärfach:** [Das Fach der LP]
**Verbundene Fächern:** [Andere Fächer, die beitragen]
**Integrations-Level:** [Multidisziplinär / Interdisziplinär / Transdisziplinär — und warum]

### Verbindungs-Karte

[Visuelle oder beschreibende Karte, die zeigt wie das Problem zu jedem Fach verbindet — was jedes beiträgt]

### Fach-Beiträge

Für jedes Fach (3–5):
**[Fach]: [Was es beiträgt]**
- **Wissen:** [Spezifisch Inhalte SuS lernen durch dieses Problem]
- **Fähigkeiten:** [Disziplinäre Fähigkeiten entwickelt]
- **Lehrplan-Alignment:** [Wie dies spezifische Lehrplan-Anforderungen adressiert]
- **Warum dieses Fach nötig ist:** [Was Verstehen würde ohne es fehlen]

### Integrations-Punkte

[Spezifisch identifizierte Punkte, wo eines Fachs Output anderes Fachs Input wird — die Momente echten fächerübergreifenden Verbindung]

### Umsetzungs-Plan

**Option A — Einzellehrer (keine fächerübergreifende Kooperation nötig):**
[Wie ein Lehrer Verbindungen zu anderen Fächern innerhalb des eigenen Unterrichts machen kann]

**Option B — Koordinierter Unterricht (Fächer unterrichten dieselbe Problem gleichzeitig, in ihren Lektionen):**
[Wie 2–3 Lehrer Timing koordinieren und Problem-Kontext teilen]

**Option C — Vollständige Kooperation (Fächer co-planen und co-unterrichten):**
[Wie ein fächerübergreifendes Projekt funktionieren könnte, falls Schule es unterstützt]

### Bewertungs-Ansatz

[Wie man integriertes Verstehen bewertet — eine Aufgabe, die mehrere Disziplinen nutzen erfordert]

**Selbstcheck vor Output:** Vergewissere dich, dass (a) das Problem genuinely mehrere Disziplinen erfordert, (b) jedes Fach-Beitrag substantiell ist, (c) Integrations-Punkte spezifisch und identifiziert sind, (d) der Umsetzungs-Plan realistic mit mehreren Optionen ist, und (e) Integration statt zu verdünnen zu stärken scheint.
```

## Beispiel-Output

**Szenario:** *Realwelt-Problem: „Unsere Schule will ihren Energieverbrauch um 20% über das nächste Jahr reduzieren. Der Rektor hat Schüler gebeten, zu untersuchen wo Energie genutzt wird, grösste Reduktions-Chancen zu identifizieren und einen realistischen Aktions-Plan zu schlagen." / Primärfach: „Ich bin Science-Lehrperson — 8. Klasse" / Verfügbare Fächern: „Mathematik, Geographie und DT interessieren sich. Deutsch hat gesagt, sie könnten helfen, falls wir Überzeugungsschreiben brauchen." / Zeitrahmen: „3 Wochen — etwa 15 Lektionen über die involvierten Fächern"*

---

## Fächerübergreifende Verbindungs-Karte: Schul-Energiereduktion

**Realwelt-Problem:** Schulenergie-Verbrauch um 20% reduzieren — untersuchen, analysieren und Aktions-Plan schlagen
**Primärfach:** Science (8. Klasse)
**Verbundene Fächern:** Mathematik, Geographie, Designtechnologie, Deutsch
**Integrations-Level:** Interdisziplinär — Fächern behalten ihre disziplinäre Genauigkeit aber koordinieren um ein gemeinsames Problem. Nähert transdisziplinäre im finalen Vorschlag, der über alle Fächern synthetisiert.

### Verbindungs-Karte

```
                    SCHULENERGIE-PROBLEM
                           |
        ┌──────────┬───────┴───────┬──────────┐
        │          │               │          │
    SCIENCE      MATHEMATIK      GEOGRAPHIE    DT
   (wie Energie  (Datenanalyse   (Energie in   (Lösungen
    funktioniert, und Modellieren) Kontext —   designen —
    Gebäude        globale und     Isolierung,
    auditen)       lokale)         Beleuchtung,
        │          │               │        Kontrolle)
        └──────────┴───────┬───────┴──────────┘
                           │
                        DEUTSCH
                  (Überzeugend den
                   Rektor sprechen)
```

### Fach-Beiträge

**Science: Wie funktioniert Energie in unserer Schule?**
- **Wissen:** Energie-Formen, Energie-Übertragung, thermale Isolierung, Elektrizität-Verbrauch, Heiz-Systeme. SuS lernen WARUM die Schule Energie nutzt (Heizung, Beleuchtung, Computing, Kochen) und die SCIENCE, wie Energie verschwendet wird (Wärmeverlust durch Wände, Fenster, Dach; Standby-Stromverbrauch; ineffiziente Beleuchtung).
- **Fähigkeiten:** Wissenschaftliche Untersuchung (Energieaudit durchführen), Messung (Temperatur-Logging, Stromzähler-Ablesung), Hypothese-Testung („Welcher Raum verliert Wärme schnellest und warum?")
- **Lehrplan-Alignment:** 8. Klasse Physik — Energie-Übertragungen, Energie-Erhaltung, thermale Isolierung, Leistung- und Energie-Berechnungen (Lehrplan 21: NT.8)
- **Warum dieses Fach nötig ist:** Ohne Science können SuS die physikalischen Mechanismen von Energieverbrauch und -verlust nicht verstehen. Sie könnten wissen die Schule nutzt viel Energie, aber nicht verstehen WO sie geht oder WARUM — das bedeutet ihre Vorschläge wären Rätsel, nicht Ingenieurwerk.

**Mathematik: Wie viel Energie und wie würden Einsparungen aussehen?**
- **Wissen:** Prozent-Veränderung (eine 20%-Reduktion berechnen), Datenanalyse (Energierechnungen lesen und interpretieren), statistische Darstellung (Bar-Charts, Liniengraphen über Energie-Verbrauch über Zeit), proportionales Denken (Kosten pro Einheit, Einsparungen skalieren), Finanz-Modellierung (Kosten der Massnahme gegenüber Einsparungen über Zeit)
- **Fähigkeiten:** Datenerfassung und -analyse, Prozent-Berechnungen, Graphen erstellen und interpretieren, Finanz-Modellierung (einfache Amortisations-Berechnungen)
- **Lehrplan-Alignment:** 8. Klasse Mathematik — Prozente, Datenbehandlung, Proportion, echte Datensätze Interpretation (Lehrplan 21: MA.5)
- **Warum dieses Fach nötig ist:** Ohne Mathematik wird das Energie-Problem in vagen Termen beschrieben („wir nutzen zu viel"). Mit Mathematik können SuS quantifizieren: „Heizung macht 62% unserer Energierechnung aus. Falls wir Dach-Isolierung verbessern, könnten wir Heizkosten um 18% reduzieren, etwa CHF 4.200 pro Jahr ersparen. Die Isolierung kostet CHF 12.000, zahlt sich in 2,9 Jahren aus." Nummern machen den Vorschlag glaubwürdig und die Entscheidungen evidenzbasiert.

**Geographie: Energie im Kontext — warum ist das wichtig?**
- **Wissen:** Energie-Quellen (woher kommt Schul-Elektrizität — nationales Netz, fossile Fuels, Renewable), Kohlenstoff-Abdruck (Energie-Verbrauch in CO2-Emissionen umwandeln), globale Energie-Ungleichheit (unsere Schule nutzt X kWh pro SuS; eine Schule in Kenia nutzt Y), nachhaltige Entwicklung (SDG 7: erreichbare und saubere Energie)
- **Fähigkeiten:** Geographische Forschung, Vergleich über Massstäbe (lokale Schule → nationale Energiepolitik → globale Energie-Ungleichheit), kritische Bewertung von Datenquellen
- **Lehrplan-Alignment:** 8. Klasse Geographie — Energie-Ressourcen, Nachhaltigkeit, Entwicklung, Umwelt-Management (Lehrplan 21: GG.2)
- **Warum dieses Fach nötig ist:** Ohne Geographie wird das Energie-Problem rein technisch. Geographie bietet den KONTEXT: warum ist Energie-Reduktion wichtig ausserhalb Geldsparen? Welche Umwelt-Konsequenzen hat unser Energieverbrauch? Wie ist unsere Situation relativ zu Schulen in anderen Ländern? Geographie transformiert das Projekt von einer Ingenieurübung in eine Nachhaltigkeit-Forschung.

**Designtechnologie: Welche Lösungen können wir bauen?**
- **Wissen:** Material für thermale Isolierung und Eigenschaften, LED-Beleuchtungs-Design, Basis-Elektronik (Timer, Sensoren, Kontrollen), nachhaltige Design-Prinzipien, Material-Auswahl für Umwelt-Performance
- **Fähigkeiten:** Designprozess (Problem identifizieren → recherchieren → designen → prototyp → testen → evaluieren), Prototyping, technische Zeichnungen, Material-Testung
- **Lehrplan-Alignment:** 8. Klasse DT — Materialien, Nachhaltigkeit im Design, Systeme und Kontrolle (Lehrplan 21: TA.3)
- **Warum dieses Fach nötig ist:** Ohne DT können SuS Probleme identifizieren aber keine Lösungen designen. DT bewegt das Projekt von Analyse („unsere Schule verschwendet Energie") zur Aktion („hier ist ein Prototyp einer Zugluftausschluss-Leiste / bewegungs-aktiviertes Lichtsystem / Fenster-Isolierungs-Panel, das wir tatsächlich installieren können").

**Deutsch: Wie überzeugten wir den Rektor?**
- **Wissen:** Überzeugungsschreib-Techniken (Ethos, Pathos, Logos), Bericht-Schreiben (formal Register, strukturiertes Argument), Präsentations-Fähigkeiten (eine Idee einem Entscheidungsträger „pitchen")
- **Fähigkeiten:** Überzeugungsschreiben, Publikum-Bewusstsein, formal Register, strukturiertes Argument mit Evidenz
- **Lehrplan-Alignment:** 8. Klasse Deutsch — Schreiben für Absicht und Publikum, Überzeugung-Techniken, Sachtext-Schreiben (Lehrplan 21: DE.5)
- **Warum dieses Fach nötig ist:** Die SuS-Vorschlag muss den Rektor und Schulrat ÜBERZEUGEN. Ein technisch brillanter Vorschlag, der schlecht kommuniziert, wird scheitern. Deutsch bietet die Kommunikations-Fähigkeiten, die andere Fächern-Beiträge actionierbar machen.

### Integrations-Punkte

| Integrations-Punkt | Fach A produziert... | Fach B nutzt es um... |
|---|---|---|
| **Energie-Audit-Daten** | Science führt das Audit (Temperatur-Lesungen, Stromzähler-Daten, Wärmeverlust-Beobachtungen) | Mathematik analysiert die Daten (Prozent-Aufschlüsselungen, Graphen, Trend-Analyse) |
| **Quantifizierte Einsparungen** | Mathematik berechnet potenzielle Einsparungen aus jeder Massnahme (in kWh und CHF) | DT nutzt die Einsparungen-Daten, um Prioritäten zu bestimmen, welche Lösungen zu designen (höchste Auswirkung zuerst) |
| **Kohlenstoff-Kontext** | Geographie berechnet den Kohlenstoff-Abdruck von aktuellem Energieverbrauch | Science nutzt dies um die Umwelt-Auswirkung unterschiedlicher Energiequellen zu erklären |
| **Prototyp-Performance** | DT testet Prototyp-Isolierungs-Materialien und misst Wirksamkeit | Science evaluiert die Resultate, using Energie-Übertragung-Prinzipien |
| **Finaler Vorschlag** | ALLE Fächern tragen Evidenz und Analyse bei | Deutsch strukturiert den Vorschlag als Überzeugungsdokument für den Rektor |

### Umsetzungs-Plan

**Option A — Einzellehrer (Science-Lehrer arbeitet allein):**
Innerhalb Science-Lektionen, die Lehrer:
- Führt das Energieaudit als wissenschaftliche Untersuchung durch (Wochen 1–2)
- Beinhaltet grundlegende Datenanalyse, die mathematische Konzepte referenziert: „Wir müssen Prozent-Veränderung berechnen — ihr habt das in Mathematik gemacht"
- Referenziert geographischen Kontext: „Unser Schulenergie-Verbrauch trägt zu Kohlenstoff-Emissionen bei — ihr könnt das in Geographie studieren"
- Setzt den Überzeugungsvorschlag als Hausaufgabe: „Schreibt einen Brief dem Rektor, der EINE Veränderung empfiehlt, mit Evidenz aus deinem Audit"

Dies erfordert keine fächerübergreifende Koordination. Der Science-Lehrer macht Verbindungen ZU anderen Fächern, ohne dass diese Fächern teilnehmen müssen.

**Option B — Koordinierter Unterricht (4 Fächern, synchronisiertes Timing):**
Alle vier Fächern unterrichten das Energieproblem während dieselben 3 Wochen, in ihren Lektionen:
- **Woche 1:** Science führt das Energieaudit durch. Mathematik startet, die Schulenergie-Rechnung-Daten zu analysieren. Geographie stellt Energie im globalen Kontext ein. DT startet Isolierungs- und Beleuchtungs-Lösungen zu recherchieren.
- **Woche 2:** Science teilt Audit-Daten mit Mathematik (via gemeinsames Spreadsheet). Mathematik analysiert und visualisiert die Daten. Geographie berechnet Kohlenstoff-Abdruck, using die Daten. DT designt Prototyp-Lösungen basierend auf Science und Mathematik-Befunde.
- **Woche 3:** DT testet Prototypen. Mathematik berechnet Amortisations-Perioden. Deutsch hilft SuS, den formalen Vorschlag zu schreiben. ALLE Fächern tragen zur finalen Präsentation bei.

Dies erfordert: eines 30-Minuten fächerübergreifendes Planungs-Treffen vor der Unit, ein gemeinsamer digitaler Ordner für Daten und approximates Stundenplan-Synchronisation (Science-Audit in Woche 1 muss Mathematik-Analyse in Woche 2 vorangehen).

**Option C — Vollständige Kooperation (Team-Unterricht, gemeinsame Lektionen):**
Fächern kombinieren Lektionen für wichtige Sessions:
- Science + Mathematik co-unterrichten das Energieaudit (Science bietet Methodik, Mathematik bietet analytische Werkzeuge)
- Geographie + Deutsch co-unterrichten den Vorschlag-Schreiben (Geographie bietet Umwelt-Kontext, Deutsch bietet Kommunikations-Rahmen)
- DT + Science co-unterrichten Prototyp-Testung (DT baut es, Science misst es)
- Finale Präsentation ist kombinierte Session, wo SuS-Gruppen zum Rektor präsentieren (genuines Publikum)

Dies erfordert: Stundenplan-Flexibilität, gemeinsame Planungszeit und Schulleitung-Unterstützung. Es ist die mächtigste Option, aber die schwierigste zu organisieren.

### Bewertungs-Ansatz

**Der Energie-Aktions-Vorschlag (integrierte Bewertung):**

SuS-Gruppen produzieren einen formalen Vorschlag zum Rektor, der spezifische Massnahmen zur Schulenergie-Reduktion um 20% empfiehlt. Der Vorschlag muss beinhalten:

1. **Evidenz vom Energieaudit** (Science): Was wir gemessen haben, was wir fanden, wo Energie verschwendet wird
2. **Datenanalyse** (Mathematik): Quantifizierte Einsparungen, Graphen, Amortisations-Berechnungen
3. **Umwelt-Kontext** (Geographie): Warum das wichtig ist — Kohlenstoff-Abdruck, globaler Kontext
4. **Proposed Lösungen mit Prototypen** (DT): Was wir empfehlen, wie wir es designt haben, Test-Resultate
5. **Überzeugend-Kommunikation** (Deutsch): Formal Register, strukturiertes Argument, klare Empfehlungen

Der Vorschlag wird bewertet auf: Genauigkeit der Evidenz, Qualität der Analyse, Tiefe des Kontextes, Machbarkeit der Lösungen und Klarheit der Kommunikation. Jedes Fach bewertet seinen disziplinären Beitrag; die Integration wird bewertet durch die Qualität des Gesamt-Vorschlags.

**Der echte Test:** Akzeptiert der Rektor den Vorschlag? Falls SuS zu einem echtem Publikum mit echter Entscheidungs-Macht präsentieren, hat die Bewertung echte Einsätze.

---

## Bekannte Limitationen

1. **Fächerübergreifende Integration ist strukturell schwierig in Sekundarschulen.** Fach-Stundenpläne, Abteilungs-Silos, separate Planungszeit und individuelle Lehrer-Verantwortung alle arbeiten gegen Integration. Der drei-Optionen-Umsetzungs-Plan oben erkennt diese Realität an — Option A funktioniert in jeder Schule, Option C erfordert bedeutende Struktur-Flexibilität, die viele Schulen nicht haben.

2. **Integration kann individuelle Fächer verwässern, falls schlecht designt (Czerniak et al., 1999).** Der häufigste Fehler-Modus ist, dass Fächer oberflächlich statt substantiell zum gemeinsamen Problem beitragen. „Lass uns Energy-Prozente in Mathematik machen" (eine Lektion, geringe Herausforderung) ist schwächer als „echte Schulenergie-Daten mit Prozent-Veränderung, statistische Darstellung und Finanz-Modellierung analysieren" (mehrere Lektionen, echtes mathematisches Denken). Jedes Fach muss seine Standards innerhalb des integrierten Kontextes halten.

3. **Nicht alle echten Probleme verbinden gleich zu allen Fächern.** Das Energie-Problem oben verbindet natürlich zu Science, Mathematik, Geographie, DT und Deutsch. Es verbindet nicht gut zu Musik, PE oder Fremdsprachen. Erzwungene Verbindungen zu Fächern, die nicht naturally beitragen, schwächen die Integration. Es ist besser, vier Fächern genuinely integriert als acht Fächern künstlich verbunden zu haben.
