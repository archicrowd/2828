# Schnittstelle für Mikrosimulationen (Entwurf)

Stand: 6. Oktober 2026 · bezieht sich auf **Stand B** (Klub A / Gemeinden B, Quote 30,6 %).
Das Gesamtkonzept nennt die Haushaltsmikrosimulation „die wichtigste offene Rechnung": Ohne sie bleibt
das Konzept auf der Ebene der Aggregate, und niemand weiß, wie es einer Alleinerziehenden mit zwei
Kindern ergeht (Gesamtkonzept, Abschnitt 8). Dieser Entwurf beschreibt, was Dritte erhalten und was
sie zurückgeben sollen. Er ist nicht mit einer Mikrosimulationsgruppe abgestimmt.

## Was das Projekt bereitstellt

| Datei | Inhalt |
|---|---|
| `dokumente/TAX-2828-Gesamtkonzept.pdf` | die Reform in Worten (maßgeblich) |
| `modell/parameter.toml` | Parameter mit Einheit, Bezugsjahr, Preisbasis, Quelle, Status |
| `daten/aggregate/kennzahlen.csv` | benannte Ergebnisgrößen des Rahmenmodells |
| `dokumente/aussagen.csv` | 130 Zahlen des Konzepts mit Sollwert und Toleranz |
| `schnittstelle/ergebnis-schema.csv` | Format der Rückgabedatei |
| `schnittstelle/pruefe_beitrag.py` | Formprüfung der Rückgabedatei |

## Was zu simulieren ist (Reformbausteine, Stand B)

| Baustein | Inhalt laut Gesamtkonzept | Festgelegt? |
|---|---|---|
| Einkommensteuer (01) | Stufentarif 0 bis 28 %, Schwellen 12.348 / 25.000 / 40.000 / 55.000 / 70.000 EUR, Brutto ohne Abzüge, kein Splitting | Schwellen ja; **Sätze der mittleren Stufen nein** (siehe unten) |
| Kapital (02) | 28 % auf alle Erträge, Veräußerungsgewinne eingeschlossen | ja |
| Erbschaft (03) | 28 % über 200.000 EUR je Erwerb, Stundung statt Verschonung | ja |
| Mehrwertsteuer (06) | Label A+ bis D, Effektivsatz im Standardkorb rund 21,5 % | Stufen nicht einheitlich dokumentiert |
| Sozialabgaben | entfallen vollständig | ja |
| Dividende | je Kopf gleich, Kinder zur Hälfte; Klubschnitt 506 EUR je Monat (Preise 2028), Deutschland 550 EUR | Höhe ist Restgröße, Mindestquote 30,61 % |
| Bestandsgarantie (09) | Bezieher von Bürgergeld, Grundsicherung, BAföG erhalten mindestens das bisherige Niveau | Härtefallfonds ohne Zahl |

**Offene Festlegung, die vor einer Simulation zu treffen ist:** Das Gesamtkonzept nennt nur die
Schwellen des Tarifs. Die Sätze der mittleren Stufen unterscheiden sich zwischen den zwei Fassungen
der Webseite im Repository: 9 / 16 / 21 / 26 % (veröffentlichte Seite, `seite/stand-a-national/`) gegen
9 / 19 / 24 / 27 % (`seite/stand-a-neuerer-build/`). Die Entscheidung liegt beim Autor; die
Rechnung dazu steht in `modell/rechnungen/haushalt/` (R10, Stand A, nicht neu gerechnet).

## Was Dritte zurückgeben

Eine Datei `ergebnis.csv` im Format von `schnittstelle/ergebnis-schema.csv`, dazu `LIESMICH.md` mit:
Gruppendefinition, Datenquelle und Datenjahr, Methode (Modell, Version), Annahmen zu Verhalten,
Fallzahlen, bekannten Grenzen, Autorinnen und Autoren, Lizenz des Beitrags.

Vorschlag der Auswertungen (nicht abgestimmt): Nettoeinkommen je Haushaltstyp vor und nach der Reform;
Gewinner und Verlierer je Einkommensdezil; Wirkung der Dividende auf Haushalte mit Kindern; Wirkung für
die Bezieher von Bestandsleistungen; Aufkommen je Position als Gegenprobe zu den Aggregaten des Modells.

## Daten

Mikrodaten (SOEP, EU-SILC) liegen bei den Dritten und bleiben dort, nach deren Datenvertrag. In dieses
Repository kommen nur Aggregate. Mindestfallzahl je Zelle: Annahme des Bearbeiters n ≥ 30, mit dem
Datengeber abzustimmen. Das Projekt stellt keine Mikrodaten bereit.

## Rückkopplung

Ein Ergebnis kann eine Annahme des Modells widerlegen (z. B. die Höhe der Dividende, die
Bestandsgarantie). Dann gilt: Parameter in `modell/parameter.toml` ändern, `python3 modell/alles.py`
ausführen, betroffene Aussagen in `daten/aggregate/aussagen_pruefung.csv` benennen, Logbuch fortschreiben.
Die Entscheidung über Änderungen am Konzept trifft der Projektverantwortliche.

## Grenzen dieses Entwurfs

Das Rahmenmodell rechnet in Aggregaten (zehn Staaten, ein BIP je Kopf, ein Wachstumspfad). Eine
Mikrosimulation je Land braucht Ländermodelle (z. B. nationale Steuer-Transfer-Modelle); eine
Zusammenstellung geeigneter Institute liegt im Vorchat vor, ist aber nicht eingecheckt (enthält
persönliche Adressen). Der Abgleich der Seite (Stand A) mit dem Rahmen (Stand B) steht aus.
