---
name: vaf-termsheet-mapping
description: "Mappt Term-Sheet-Daten auf Vertragsfelder, erkennt fehlende Punkte, Widersprüche und rechtlich relevante Abweichungen."
---

# Term-Sheet-Mapping

## Aufgabe

Der Skill überführt wirtschaftliche Eckdaten in Vertragsklauseln. Er arbeitet freistehend innerhalb des Vertragsausfüller-Plugins und setzt keine anderen Plugins voraus.

## Startet bei

- hochgeladener Word-Vorlage oder altem Vertrag
- Term Sheet, E-Mail, Tabelle oder Freitext mit Eckdaten
- Wunsch nach neuem Vertragsentwurf
- Wunsch nach Redline oder Track Changes

## Workflow

1. Parteien, Objekt, Preis, Laufzeit, Optionen, Kaution, Nebenpflichten, Versicherung und Sonderbedingungen auslesen.
2. Jeden Term-Sheet-Punkt einem Feld, einer Klausel oder einer Anlage zuordnen.
3. Punkte ohne Vertragsklausel als Ergänzungsbedarf markieren.
4. Konflikte wie abweichende Laufzeit, Miete, Umsatzsteuer oder Rückbaupflicht sichtbar machen.

## Ausgabe

- Vertragsdatenmatrix
- Rückfragenliste
- Ausfüllprotokoll
- Entwurfs- oder Prüfvermerk
- klare Stopper vor Track Changes, falls noch keine ausdrückliche Bestätigung vorliegt

## Leitplanken

- Originaldateien werden nie überschrieben.
- Track Changes, Redline oder Vergleichsfassung nur nach ausdrücklicher Rückfrage und Bestätigung.
- Offene Werte bleiben sichtbar; sie werden nicht erfunden.
- Juristische Wahlentscheidungen werden erklärt und protokolliert.
