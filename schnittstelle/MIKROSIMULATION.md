# Schnittstelle für Mikrosimulationen

Stand: 21. Oktober 2026 (Modellstand v4.21) · bezieht sich auf **Stand C „Das Goldene Drittel“** (geltend). Die frühere Fassung vom
6. Oktober 2026 beschrieb Stand B (Quote 30,6 %, Dividende 550 €, Tarif bis 28 %); sie ist überholt (Hinweis der Prüfung vom 21.10.2026).

Ohne Mikrosimulation bleibt das Konzept auf der Ebene von Beispielhaushalten und Verteilungsannahmen. Diese Seite beschreibt, was Dritte
erhalten, was sie zurückgeben und wie ein Beitrag geprüft wird. Ein erster Beitrag liegt vor: `beitraege/kvribbeck-2028/`.

## Was das Projekt bereitstellt

| Datei | Inhalt |
|---|---|
| `README.md`, Abschnitt „Aktueller Stand“ | Karte der geltenden Skripte |
| `KENNZAHLEN.md` | welche Zahl gilt und wie sie abgegrenzt ist |
| `modell/haushalte33.py` (+ `.toml`) | Haushaltsformeln heute (Recht 2026) und neu (33R) |
| `modell/regel_boden.py` (+ `.toml`) | Grundauskommen (Grundbedarf × Skala, eigenes Einkommen zur Hälfte) |
| `daten/aggregate/haushalte33.json`, `regel_boden.json` | Ergebnisse der Beispielhaushalte |
| `schnittstelle/ergebnis-schema.csv` | Format der Rückgabedatei |
| `schnittstelle/pruefe_beitrag.py` | Formprüfung der Rückgabedatei |

## Was zu simulieren ist (Stand C, System 33R, 2028, Euro in Kaufkraft 2026)

| Baustein | Regel | Quelle im Repository |
|---|---|---|
| Einkommensteuer | 0 / 11 / 19 / 25 / 33 % ab 12.348 / 18.522 / 24.696 / 37.044 € (Grundbedarf × 1 / 1,5 / 2 / 3), Brutto ohne Abzüge, kein Splitting; die Dividende der Erwachsenen ist steuerpflichtig | `haushalte33.py` |
| Sozialbeiträge | entfallen; Arbeitgeberbeiträge mindestens zu 80 % im Bruttolohn (Gesetz zur Vertragsanpassung, Rückfallregel) | `haushalte33.toml`, `weitergabe_rueckfall.py` |
| Pflichtvorsorge | 10 % des Bruttolohns auf ein eigenes Konto ab dem ersten Euro | `heute_laender.toml`, `regel_boden.toml` |
| Dividende | 354 € je Erwachsenem, 283 € je Kind im Monat (Kinderanteil 0,8 bei gleichem Topf); Kinderdividende steuerfrei | `netz33.json` × `regel_boden.json: topf` |
| Grundauskommen | Grundbedarf × (1; 0,5 je weiterem Erwachsenen; 0,55 je Kind); eigenes Einkommen zur Hälfte angerechnet; DE 1.029 € allein, 2.675 € Paar mit zwei Kindern | `regel_boden.py` |
| Mehrwertsteuer | effektiver Satz 18,84 % (2028) statt 15,97 % auf den Konsum | `projektion33.json` |
| Altlastenzuschlag | 15,4 % auf Einkommen- und Mehrwertsteuer (gemeinsamer Fonds der 30 Staaten, Zins 2,45 %) | `fonds_geltend.json` |
| Bestandsrenten | Kürzung 7,5 %, Grundauskommen im Bestand | `rentnerausgleich.py` |

Für Vergleiche „heute“: Recht 2026 einschließlich Kindergeld; bedarfsgeprüfte Leistungen (Wohngeld, Kinderzuschlag, Bürgergeld) sind in
`sozial_laender.py` abgebildet. Wer sie weglässt, sollte zugleich das Grundauskommen weglassen und das im Beitrag nennen.

## Was Dritte zurückgeben

Ein Verzeichnis `beitraege/<kuerzel>-<jahr>/` mit `ergebnis.csv` im Format von `schnittstelle/ergebnis-schema.csv` (`stand` = „Stand C“,
`modellstand` = geprüfte Version), `LIESMICH.md` (Gruppendefinition, Datenquelle und Datenjahr, Methode, Annahmen, Fallzahlen, Grenzen,
Lizenz) und, wenn möglich, dem Rechenweg. Personennamen und E-Mail-Adressen gehören nicht in den Beitrag; Urheber ist die einreichende
Organisation.

Vorschlag der Auswertungen: Anteil mit mehr verfügbarem Einkommen je Weitergabe-Szenario, Gewinner und Verlierer je Dezil, Nettoeinkommen
je Haushaltstyp, Haushalte mit Kindern, Teilzeit und Bezieher bedarfsgeprüfter Leistungen.

## Daten

Mikrodaten (SOEP, EU-SILC) bleiben bei den Dritten, nach deren Datenvertrag. In dieses Repository kommen nur Aggregate; Mindestfallzahl je
Zelle n ≥ 30 (Annahme, mit dem Datengeber abzustimmen). Synthetische Populationen, die auf veröffentlichte Verteilungen geeicht sind, sind
zulässig; die Eichung ist im Beitrag zu nennen.

## Prüfung und Rückkopplung

`python3 schnittstelle/pruefe_beitrag.py beitraege/<kuerzel>-<jahr>/ergebnis.csv` prüft die Form. Inhaltlich wird der Beitrag im Logbuch
bewertet. Widerlegt ein Ergebnis eine Annahme, gilt: Parameter ändern, `python3 modell/alles.py` ausführen, Logbuch fortschreiben. Die
Entscheidung über Änderungen am Konzept trifft die Initiative.
