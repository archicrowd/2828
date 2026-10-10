# Arbeitsanweisung für Länderrechnungen und Ländervergleich (für nachfolgende Agenten)

Stand: 10. Oktober 2026, Modellstand v3.29. Sicherung der Arbeitsweise aus den Sitzungen v3.23 bis v3.28. Maßgeblich bleiben `CLAUDE.md`, `modell/laender/STANDARD.md` und das Logbuch (Band III). Diese Anweisung beschreibt, **wie** gearbeitet wurde und welche Fehler vermieden werden müssen.

## 1. Was es gibt

| Datei | Zweck |
|---|---|
| `modell/laender/STANDARD.md` | Regeln für jede Länderrechnung (Eingaben, Pfade A/B/C, Klubwirkung, Wohnort) |
| `modell/laender/rechne.py` | ein Skript für alle Länder; liest `modell/laender/<cc>.toml` |
| `modell/laender/<cc>.toml` | Eingaben je Land mit Quelle und Status (fr, es, nl, be, pl) |
| `daten/aggregate/laender/<cc>_eingaben.md` | Eingabedatei je Land: jede Größe mit Wert, Bezugsjahr, Quelle, Status, Prüfung |
| `daten/aggregate/laender/<cc>.json`, `laender_vergleich.csv`, `laender_klub.json` | Ergebnisse der Länderrechnung |
| `modell/laendervergleich.py` + `modell/laender/vergleich.toml` | Ländervergleich nach den Kriterien der Webseite (seit v3.28) |
| `daten/aggregate/laendervergleich.json`, `.csv` | Ergebnis des Ländervergleichs |
| `modell/uebergang.py` + `modell/uebergang.toml` | Übergangsrechnung 2028–2060: Dividende je Land nach V3a und V2B, Angleichung als Szenario (seit v3.29) |

## 2. Ablauf für ein neues Land

1. **Eingangslage im Repository prüfen:** `daten/aggregate/schulden_2010_2025.csv`, `preisniveau_2024.csv`, `laender_2024.csv`, `laendervarianten.json`. Klubländer haben dort schon Schuld 2025, Saldo 2025, Preisniveau, Einwohner, Dividende und Gemeindebeträge.
2. **Recherche:** Ein Rechercheagent je Land ist sinnvoll; Länder parallel. Der Auftrag an den Agenten nennt: Regierungspfad Saldo und Schuld 2026–2028, nominales Wachstum, EU-Kommission (Frühjahrsprognose), Ist-Werte 2025, Steuerparameter, Zahl der Gemeinden; Status je Zeile; keine Umgehung gesperrter Seiten; keine Personennamen oder E-Mail-Adressen.
3. **Selbst prüfen, bevor etwas in die Rechnung geht:** Eurostat-Werte (Schuld, Saldo, Preisniveau) und die tragenden Regierungszahlen am Original abrufen. Agentenwerte, die nicht geprüft sind, werden in der Eingabedatei als „Agent, nicht selbst geprüft“ markiert. Beispiel v3.27: Der Agent las beim belgischen Defizit 2029 −5,0 statt −5,5 %.
4. **Parameterdatei** `modell/laender/<cc>.toml` anlegen (Pflichtfelder siehe `rechne.py`, `PFLICHT`). Fehlt eine amtliche Schuldenquote der Regierung, bleibt `quote_regierung = []`; Pfad C entfällt. Ein fehlendes Einzeljahr darf linear interpoliert werden, als Annahme gekennzeichnet (`quote_regierung_hinweis`).
5. **Eingabedatei** `daten/aggregate/laender/<cc>_eingaben.md` schreiben, mit Widersprüchen und Lücken.
6. `python3 modell/laender/rechne.py` und `python3 modell/laendervergleich.py`; Prüfungen in den Skripten müssen bestehen.
7. Version abschließen (Abschnitt 5).

## 3. Datenzugang: was funktioniert, was nicht

- **Eurostat nur über WebFetch**, nicht über die Shell (Proxy: HTTP 403). Muster: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<TABELLE>?format=JSON&lang=EN&geo=<CC>&...`. Je Land und Reihe einzeln abfragen.
- **Preisniveau:** Tabelle `prc_ppp_ind`, Dimension `ppp_cat=A01` (Individualverbrauch) und `na_item=PLI_EU27_2020`. **A01 ist `ppp_cat`, nicht `na_item`.** Diese Verwechslung kostete in v3.24 den Wert für Polen. Gegenprobe immer mit Deutschland (109,1).
- **Schulden:** `gov_10dd_edpt1`, `unit=PC_GDP`, `na_item=GD` bzw. `B9`, `sector=S13`.
- **Steuern und Ausgaben:** `gov_10a_taxag` (D61, D211, `sector=S13`), `gov_10a_exp` (`cofog99=GF07` usw.).
- WebFetch liest maschinell (Modellzusammenfassung). Werte als „amtlich, maschinell“ führen.
- **Gesperrt oder nicht erreichbar** (Stand 10.10.2026, nicht umgehen): Légifrance; Sejm-Seiten (Verfassung, Drucksachen; „Request Rejected“ trotz Freigabe); isap.sejm.gov.pl (Freigabe nötig); PAP Biznes; Scope Ratings; ING Think; spanisches Wirtschaftsministerium (Informe de Progreso); AIReF; cpb.nl; plan.be; hogeraadvanfinancien.be; financien.belgium.be; Teile von belastingdienst.nl.
- **Gut erreichbar:** Länderseiten der EU-Kommission (Prognose), Haushaltsseiten (rijksfinancien.nl, hacienda.gob.es, gov.pl-Anhänge, lachambre.be), Fachpresse.
- Eine neue Domain kann eine Freigabe der Initiative erfordern. Ohne Antwort wird der Abruf zurückgezogen; dann die Adresse nennen und um Freigabe bitten.

## 4. Regeln, die aus Fehlern entstanden sind

- **Gesamtstaat und Staatshaushalt nicht vermischen** (Korrektur 56): Polens 282,6 Mrd. Zł sind das Defizit des Staatshaushalts, nicht des Gesamtstaats.
- **Klubwirkung:** Die übrigen Länder behalten ihren eigenen Saldo 2025 (Korrektur 57). Ein Rest-Saldo, der den Klub-Gesamtsaldo festhält, macht jede Defizitabweichung rechnerisch neutral. Kontrolle: Land im Status quo ergibt die Referenz 81,29 %; Einzelwirkungen addieren sich zur gemeinsamen.
- **Implizites Wachstum in Pfad C** enthält Bestandsanpassungen. Liegt das Regierungswachstum vor, die Bestandsanpassung ausweisen (Polen 2026: 4,3 Punkte).
- **Einheitliche Wachstumsannahme 3,0 %** überzeichnet die Schuld in Ländern mit hohem nominalem Wachstum (Polen 6,2 %). Entscheidung der Initiative offen.
- **Preisniveau weiterer Länder nur in der Länderdatei**, nie in `preisniveau_2024.csv`; diese Tabelle speist die Gesamtrechnung.
- **Kein Wert ungeprüft als eigener Abruf ausgeben.** Agentenwerte als solche kennzeichnen (Arbeitsfehler v3.24, Spanien).
- Eine Ursache, die nicht belegt ist, als Vermutung schreiben.

## 5. Eine Version abschließen (Reihenfolge einhalten)

1. Versionsnummer an fünf Stellen: `modell/parameter.toml`, `modell/gesamtrechnung.toml`, `CITATION.cff`, `README.md` („Modellstand: vX“), `INDEX.md`; Logbuch Band III Kopf („Modellstand **vX**“); `projekt/Projektsteuerung.md`.
2. Logbucheintrag vor `## 4 | Korrekturen, Fortsetzung`: Art der Änderung, Datum, Auftrag, Änderung, Quelle, bewegte Zahl, wodurch aufgefallen, geprüft, offen. Korrekturen in die Tabelle unter Abschnitt 4 (nächste freie Nummer in `CLAUDE.md`, dort und im Kopf der Tabelle mitführen). Abschnitt 7 (Offene Punkte) nachführen.
3. `projekt/bausteine.csv` (B22) und bei neuen Nahtstellen `projekt/nahtstellen.csv` anpassen.
4. `python3 modell/alles.py` **zuerst** (schreibt `gesamtrechnung.json` mit neuer Version), **dann** `NODE_PATH=/opt/npm-tools/node_modules node dokumente/werkzeuge/gesamtkonzept-bau.js`, `kurzfassung-bau.js`, `python3 seite/werkzeuge/seite_bau.py`, `soffice --headless --convert-to pdf --outdir dokumente dokumente/TAX-2828-*.docx`, PDFs nach `seite/stand-b/dokumente/` kopieren, **dann** erneut `python3 modell/alles.py` und `python3 modell/pruefe_konzept.py`. In falscher Reihenfolge trägt die Seite die alte Version, und die Stufe „Gesamtkonzept gegen Rechnung“ schlägt fehl.
5. Prüfen, dass sich in `gesamtrechnung.json` nur die Version geändert hat (`git diff -U0`), wenn keine Konzeptzahl bewegt werden soll.
6. Ein Commit (erste Zeile Version und Thema, dann bewegte Zahl und Quelle, Attributionszeilen laut Sitzung), Tag `vX.Y.Z` lokal, `git push origin HEAD:main`. **Tag-Push scheitert über den Sitzungsproxy;** Tags setzt der Verantwortliche.
7. Projektraum „2525“ nachführen: `claude/Versionsgeschichte-TAX-2828-BandIII.md` und `claude/Projektsteuerung.md` aus den Repository-Dateien überschreiben, diese Anweisung als `claude/Arbeitsanweisung-Laender.md`.

## 6. Ländervergleich nach den Kriterien der Webseite (seit v3.28)

Die Webseite kommuniziert länderbezogen: Dividende je Erwachsenem und je Kind (2028), höchstens 28 % mit Stufen am Grundbedarf, den Rechner (Einkommensteuer, Durchschnittssatz, Haushaltsdividende, Sozialabgaben 0), das Gemeindebudget je Einwohner und je Kind, die heutige Last (Abgabenkeil, Kapitalertragsteuer, Sozialabgaben) und die Staatsschulden. `modell/laendervergleich.py` rechnet diese Größen je Land mit derselben Rechenregel wie der Rechner der Seite (`seite/werkzeuge/vorlage.html`, Funktion `steuer`). Musterhaushalte und Angaben zur heutigen Last stehen in `modell/laender/vergleich.toml`, jede Angabe mit Quelle. Fehlende Angaben bleiben leer und erscheinen als Lücke.

## 7. Leitlinie der Initiative (v3.29) und Übergangsrechnung

Leitlinie (10.10.2026): Nationalstaaten sind der Ausgangspunkt und werden nicht in Frage gestellt. Mindestens in einer Übergangszeit gelten unterschiedliche Preise und Dividenden. Die Angleichung entsteht durch gleiche Regeln und Chancen über die Zeit von selbst. Wachstumsannahmen sind je Land und mit Bezug auf die Anreize des Modells zu setzen. Wettbewerbsanreize für Gemeinden und Regionen bleiben bei allen Solidarmechanismen bestehen.
Umsetzung als Rechnung: `modell/uebergang.py` + `modell/uebergang.toml` (V3a gegen V2B, Angleichung als Szenario, Anreizmaß „Rückfluss“). Die Gesamtrechnung ist nicht verändert; eine Änderung der geltenden Regel ist eine Entscheidung der Initiative.

## 8. Offene Punkte (Stand v3.29)

Siehe Logbuch Band III, Abschnitt 7. Wichtigste: Regel der Dividende nach der Leitlinie v3.29 (V3a oder V2B, Irland, Entzugsrate am Boden, Anreizzuschlag delta); Entscheidung Klubquote 2028 (81,3 / 82,0 %; Länderwirkung bisher +0,26 Punkte); Wachstum je Land; Irland, Österreich, Dänemark, Slowenien, Estland nach dem Standard; Abgabenkeil je Land (OECD Taxing Wages); Polen 2028 und Verfassung; Widerspruch Miljoenennota/CPB; belgischer Haushalt 2027.
