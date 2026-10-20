# Stellungnahme zum zusammengefassten Prüfbericht (zwei Prüfungen und Mikrosimulation, 20.10.2026)

Initiative 28:28 · 20. Oktober 2026 · Logbuch v4.17 und v4.18

Der Bericht fasst beide Prüfungen zusammen (v4.11 und v4.13). Neu gegenüber dem Bericht, auf den die Stellungnahme vom 20.10.2026
(`Stellungnahme-Pruefung2-2026-10-20.md`) antwortet, ist Abschnitt 6, eine eigene Mikrosimulation zur Aussage „9 von 10 Beschäftigte“. Die
Befunde B11 bis B16 sind dort bewertet und in v4.14 umgesetzt. Hier folgen der Stand nach den Nacharbeiten und die neuen Rechnungen.

## 1 | Stand der Befunde

| Befund | Stand |
|---|---|
| B11 Fondszahlen der Seiten | **Entschieden (v4.17): gemeinsamer Fonds auf allen Seiten** (5,28 % BIP, Zuschlag 15,8 %, Spitze 149,6 % 2056). Die Seiten FR, IT, ES und PL nennen den eigenen Fonds nur noch zum Vergleich („allein trüge …“). Vorbehalt: Italien und Polen gehören nicht zu den zehn gerechneten Staaten; ihr Beitritt änderte den gemeinsamen Satz (nicht gerechnet). |
| B12 Dividendenpfade | umgesetzt v4.14 (`KENNZAHLEN.md`: geltend netz33, projektion33 archiviert). Messerschneide: siehe Abschnitt 3 (Ausweichreaktionen). |
| B13 Rentenkürzung | umgesetzt v4.14 (Seite, sechs Sprachen) |
| B14 Spitzenverdiener | v4.14: Beide Zahlen stammen nach unserer Rechnung aus der Beschlussvariante, die Basis war der OECD-Durchschnittslohn (63.288 €). Ihre Werte mit 50.000 € als Basis bestätigen wir (3× +10 %, 8× −1,3 %). **Neu v4.18:** Monitoring und Rückfallregel übernommen. |
| B15 Gesamtlast | umgesetzt v4.14 (`gesamtlast33`: mit Fonds 38,81 %, mit Pflichtvorsorge 42,91 % gegen 40,76 % heute; ohne Fonds 45,46 / 49,56 %) |
| B16 Z-Größen | umgesetzt v4.14 (Glossar) |
| B10 „9 von 10“ | Ihre Mikrosimulation stützt die Aussage für Vollzeitbeschäftigte deutlich, mit Grenzen (Abschnitt 2). |

## 2 | Zur Mikrosimulation (Abschnitt 6 des Berichts)

Die Rechnung ist eine unabhängige Stütze: Die Lohnverteilung ist auf die Verdiensterhebung 2024 geeicht, die Ankerquantile sind innerhalb von 0,3 % getroffen. Selbst ohne jede Weitergabe haben 91,6 % mehr.
Sie deckt sich mit unserer Gruppenrechnung: ohne Weitergabe 84 / 98 / 91 % je Haushaltstyp. Dass unsere Gruppenrechnung vorsichtiger ist,
erklären Sie überzeugend mit den Gewichten von `VERT`.

**Grenzen, die wir bei der Übernahme nennen würden:**
1. **Dividende:** Gerechnet sind 373 € je Erwachsenem und Kinder zur Hälfte. Geltend ist seit v4.5 der Kinderanteil 0,8 bei gleichem Topf, also 354 € je Erwachsenem und 283 € je Kind. Für Alleinstehende sind das 19 € im Monat weniger.
2. **Erfasste Personen:** Die Rechnung umfasst nur Vollzeitbeschäftigte. Teilzeit, Minijobs, Rentner und Selbständige fehlen. Die Aussage auf der Seite lautet „Beschäftigte“, deckt Teilzeit also mit ab.
3. **Untere Einkommen:** „Heute“ ist ohne bedarfsgeprüfte Leistungen (Wohngeld, Kinderzuschlag) gerechnet, „neu“ ohne Grundauskommen. Beides wirkt bei kleinen Einkommen gegenläufig. Unsere Rechnung `regel_boden` enthält beides und kommt auf 98 % je Haushaltstyp.
4. **Haushaltsstruktur und Partnerkorrelation** beruhen auf Annahmen (von Ihnen benannt).

**Bitte:** Liefern Sie die Ergebnisse im Format `schnittstelle/ergebnis-schema.csv` als `ergebnis.csv`. Wir prüfen sie mit
`schnittstelle/pruefe_beitrag.py` und nehmen die Mikrosimulation dann mit Quellenangabe als zweite, externe Stütze der Aussage auf. Bis dahin
bleibt sie eine einzelne, externe Rechnung außerhalb des Repositorys.

## 3 | Neue Rechnungen zu den offenen Punkten (v4.18)

**Rückfallregel der Weitergabe** (`modell/weitergabe_rueckfall.py`):
- Regel: Wer die Vertragsanpassung unterlässt, zahlt die Differenz zur 80-%-Pflicht an den Altlastenfonds.
- Größenordnung: Die Arbeitgeberbeiträge betragen in Deutschland 7,9 bis 9,4 % des BIP (Eurostat 2024, D12 als obere Grenze).
- Kämen tatsächlich nur 50 % im Lohn an, flössen 2,4 bis 2,8 % des BIP an den Fonds, das sind 45 bis 53 % des Fondsbeitrags.
- Folge: Das Einbehalten lohnt sich für den Betrieb nicht mehr.
- Grenze der Regel: Den einzelnen Beschäftigten schützt sie nicht. Sein Anspruch folgt aus dem Gesetz zur Vertragsanpassung.

**Preisniveauschub** (`modell/preisniveau33.py`, statisch):
- **Mehrwertsteuer:** Der effektive Satz steigt 2028 von 15,97 auf 18,84 %, mechanisch sind das +2,47 %.
- **Annahmen:** Überwälzung 73 % (Carare und Danninger 2008, Erhöhung 2007) bis 100 % (Benzarti u. a. 2020: Erhöhungen wirken stärker als Senkungen). Anteil des Konsums mit Mehrwertsteuer 0,67 bis 0,84.
- **Ergebnis:** Die Verbraucherpreise steigen einmalig um **1,2 bis 2,1 %**.
- **Gegenrichtung:** Die Betriebe behalten 20 % der Arbeitgeberbeiträge, die Arbeitskosten sinken um 1,6 bis 1,9 % des BIP. Geben sie die Hälfte davon weiter, bleiben netto **+0,3 bis +1,3 %**.
- **Einordnung:** Das ist eine einmalige Niveauverschiebung. Mit dem sinkenden effektiven Satz geht sie bis 2060 auf +0,8 bis +1,3 % zurück. Zweitrundeneffekte und der CO₂-Preispfad sind nicht gerechnet.
- **Haushaltsrechnungen:** Sie setzen die volle Differenz auf den gesamten Konsum an und liegen damit auf der vorsichtigen Seite.
- **Wer trägt die Überwälzung:** die Haushalte über den Konsum, im Ausmaß der Konsumquote. Das ist in den Haushaltszahlen bereits enthalten.

**Ausweichreaktionen** (`modell/ausweichen33.py`):
- **Positionen:** Erbschaften 1,16 % des BIP (statisch gerechnet), große Vermögen 0,97 % (mit 50 % Ausweichen).
- **Ungünstiger Fall:** Bei der Erbschaft geht die Hälfte verloren, bei großen Vermögen drei Viertel. Dann fehlen 1,06 % des BIP, und die Dividende sinkt um 55 € (2028: 318 statt 373 €) bzw. um 75 € (2060: 164 statt 239 €).
- **Mittlerer Fall** (Erbschaft 25 %, Vermögen 50 %): −15 € (2028).
- **Messerschneide:** Die Dividende 2060 hängt damit spürbar an diesen beiden Positionen.

  Die Literatur zeigt große Reaktionen bei Vermögensteuern (Brülhart u. a. 2022, Schweiz: 1 Prozentpunkt weniger Satz bedeutet mindestens 43 % mehr deklariertes Vermögen nach sechs Jahren) und kleine bei der Erbschaftsteuer (Goupille-Lebret und Infante 2018, Frankreich). Die Varianten sind Annahmen.

**Handelsrecht:** Für die Besteuerung am Kundenort bleibt die DBCFT-Literatur (Auerbach, Devereux u. a.) der Prüfrahmen, eingearbeitet ist sie
noch nicht.

## 4 | Dritte Prüfung

Wir nehmen das Angebot gern an. Vorgeschlagener Gegenstand:
- Stand v4.18, insbesondere die neuen Rechnungen `preisniveau33`, `ausweichen33`, `weitergabe_rueckfall` und `regionen_de`;
- die Umstellung der Länderseiten auf den gemeinsamen Fonds (v4.17).
