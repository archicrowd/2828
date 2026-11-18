# Strukturanalyse: Einnahmen nach Quelle, Ausgaben nach Zweck – heute und im Goldenen Drittel

Initiative 28:28 · 18. November 2026 · Modellstand v4.99 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/struktur_vergleich.py` (+ `.toml`) → `daten/aggregate/struktur_vergleich.json`. Alle Werte in % des BIP des jeweiligen Jahres.

**Die drei Spalten:**
- **EU-27 heute**: Durchschnittsland nach Kommission und Eurostat (Einnahmen 2024, Ausgaben 2023).
- **Deutschland 2024**: Eurostat, Zuordnung eigene.
- **Modellland Goldenes Drittel**: Stand C (Variante 33R).

Das Modellland ist ein Mischland. Die Ausgaben sind der Schnitt der zehn Staaten, die Einnahmen stehen auf deutscher Basis (Abschnitt 5, Punkt 6).

## 1 Ergebnis in Kürze

Die Lücken haben eine gemeinsame Ursache: **Das System gleicht nicht in jedem Jahr aus, sondern nur über die Zeit, und die Dividende ist die einzige Größe, die nachgibt.**

1. **Einnahmen:** Das Gewicht verschiebt sich von Arbeit zu Konsum und Kapital.
   - Konsum wird die größte Quelle. Rund 2,8 % BIP davon sind Lenkungsabgaben (CO₂, Sonderstufen), die mit ihrem Erfolg wegfallen.
   - Kapital ist als fester Anteil am BIP gerechnet. Gewinne aus Automatisierung oder wachsenden Erbschaften stecken nicht in den Zahlen.
2. **Ausgaben:**
   - Gemeinwesen und Gesundheit bleiben nahe am heutigen Niveau und steigen mit Verteidigung und Alterung.
   - Die laufenden Geldleistungen sinken deutlich.
   - Die Verwaltung der staatlichen Ebene ist nicht eigens abgebildet.
3. **Gleichgewicht:**
   - 2028 stehen Ausgaben von 43,6 % BIP Einnahmen von 36,5 % gegenüber (Steuern und Fondsbeitrag). Die Differenz von 7,2 % BIP nimmt der Fonds als Kredit auf; seine Schuld steigt bis 2055 auf 151 % BIP.
   - Was im laufenden Haushalt fehlt, geht zulasten der Dividende: Sie sinkt von 3,33 % BIP (2028) auf 0,67 % (2060).

## 2 Einnahmen nach Quelle

| % BIP | EU-27 2024 | DE 2024 | Modellland 2028: Steuern | + Fondsbeitrag | + Pflichtvorsorge |
|---|---|---|---|---|---|
| Arbeit | 20,3 | 24,0 | 9,0 | 10,6 | 14,7 |
| Kapital, Vermietung, Boden, Erbschaft | 8,5 | 6,1 | 8,5 | 10,0 | 10,0 |
| Konsum | 10,6 | 9,5 | 12,8 | 15,0 | 15,0 |
| nicht zugeordnet / Subventionsabbau | – | 0,7 | 0,4 / 0,5 | 0,4 / 0,5 | 0,4 / 0,5 |
| **Summe** | **39,4** | **40,2** | **31,2** | **36,5** | **40,6** |
| Anteile Arbeit / Kapital / Konsum | 52 / 22 / 27 % | 60 / 15 / 24 % | 29 / 28 / 42 % | – | 37 / 25 / 37 % |

**Zuordnung (Annahmen, `struktur_vergleich.toml`):**
- Arbeit umfasst Lohn- und Einkommensteuer auf Arbeit und Renten sowie alle Sozialbeiträge (heute). Neu gehören dazu die Position Einkommen ohne Gewinn- und Mieteinkünfte, der anteilige Fondszuschlag und die Pflichtvorsorge.
- Kapital umfasst Gewinnsteuern, Kapitalerträge, Erbschaft, große Vermögen, Grundsteuer bzw. Grundstücksabgabe und Grunderwerbsteuer.
  - Dazu kommen die Einkommensteuer auf Personengesellschaften (0,98 % BIP) und auf Vermietung (0,40 %, Annahme nach EU-SILC). Sie ist heute und neu mit demselben Anteil von 13,3 % der Einkommensteuer angesetzt.
- Konsum umfasst Mehrwertsteuer bzw. Label, Verbrauchsteuern, Versicherungsteuer, Emissionshandel bzw. CO₂-Preis und die Kfz-Steuer der Haushalte.
- Die Kommission zählt das Einkommen der Selbständigen zum Kapital. In der deutschen Spalte steht nur der Gewinn der Personengesellschaften dort. Die Spalten EU-27 und DE sind deshalb nicht ganz gleich abgegrenzt.

**Lesart:**
- Arbeit trägt im Modellland noch gut ein Drittel der Pflichtzahlungen, heute sechs von zehn Euro. Mit 14,7 % BIP liegt sie 9,3 Punkte unter dem heutigen Wert in Deutschland. Davon sind 4,1 Punkte eigenes Vorsorgevermögen.
- Kapital steigt gegenüber Deutschland um 4,0 Punkte auf 10,0 % BIP. Es liegt damit über dem EU-Schnitt (8,5 %), aber nur durch Sätze und Breite der Basis, nicht durch Wachstum der Basis.
- Konsum steigt um 5,5 Punkte auf 15,0 % BIP. Das ist der größte Zuwachs und liegt deutlich über dem EU-Schnitt (10,6 %).

**Zeitpfad der Steuern im Modellland (ohne Fonds):**

| % BIP | 2028 | 2040 | 2050 | 2060 |
|---|---|---|---|---|
| Arbeit (mit kalter Progression) | 9,1 | 9,6 | 10,0 | 10,3 |
| Kapital | 8,5 | 8,5 | 8,5 | 8,5 |
| Konsum | 12,8 | 11,8 | 11,0 | 10,8 |
| davon Lenkungsabgaben | 2,8 | 1,9 | 1,1 | 1,0 |
| **Steuern** | **31,2** | **30,7** | **30,3** | **30,5** |

- Konsum verliert bis 2060 zwei Punkte, weil CO₂, Kraftstoffe, Alkohol und Tabak zurückgehen.
- Arbeit gewinnt 1,25 Punkte. Grund: Die Tarifstufen folgen den Löhnen nur zu 30 %, der Rest ist eine verdeckte Steuererhöhung auf Arbeit.
- Kapital bleibt fest, weil die Rechnung keinen Trend für Kapitaleinkommen oder Erbschaften enthält.

## 3 Ausgaben nach Zweck

| % BIP | EU-27 2023 | DE 2024 | Modellland 2028 | 2040 | 2050 |
|---|---|---|---|---|---|
| **Gemeinwesen** (Bildung, Ordnung, Verteidigung, Wirtschaft und Verkehr, Umwelt, Wohnen, Kultur) | 16,7 | 14,8 | 13,6 | 14,7 | 14,7 |
| **Unterstützung** | 26,5 | 27,6 | 25,3 | 23,1 | 20,7 |
| davon Gesundheit, Pflege | 7,3 | 7,5 | 7,8 | 8,1 | 8,4 |
| davon Alter (heute) bzw. Altrenten im Fonds (neu) | 10,4 | 9,7 | 10,8 | 10,3 | 8,2 |
| davon übrige Geldleistungen (heute) bzw. Seil und Härtefall (neu) | 8,8 | 10,4 | 3,4 | 3,4 | 3,4 |
| davon Dividende | – | – | 3,3 | 1,4 | 0,7 |
| **Verwaltung** (allgemeine öffentliche Dienste ohne Zinsen) | 4,2 | 5,2 | 3,0 | 3,0 | 3,0 |
| **Zinsen** (Altschulden) | 1,7 | 1,1 | 1,8 | 1,4 | 1,1 |
| **Summe** | **49,1** | **48,8** | **43,6** | **42,2** | **39,4** |
| Anteile Gemeinwesen / Unterstützung / Verwaltung | 35 / 56 / 9 % | 31 / 58 / 11 % | 32 / 60 / 7 % | 36 / 57 / 7 % | 38 / 54 / 8 % |

- Unterstützung bleibt der größte Block, ändert aber ihren Charakter.
  - Die heutigen Altersrenten laufen als Altlast im Fonds aus.
  - Die übrigen Geldleistungen (Familie, Grundsicherung, Wohngeld, Lohnersatz, Hinterbliebene) fallen in Deutschland von 10,4 auf 6,7 % BIP (Seil, Härtefall und Dividende zusammen).
- Neue Renten kommen aus der Pflichtvorsorge (eigenes Konto, 4,1 % BIP) und der Dividende. Beide sind keine Staatsausgaben.

**Abdeckung je Aufgabenbereich, Deutschland 2024 gegen Modellland 2028 (% BIP):**

| Bereich | DE 2024 | Modell 2028 | Differenz | Stand |
|---|---|---|---|---|
| Verteidigung | 1,34 | 1,40 | +0,06 | Pfad auf 2,50 % bis 2035 (Entscheidung) |
| Öffentliche Ordnung, Justiz | 1,61 | 1,34 | −0,27 | Gerichte und Strafvollzug nicht eigens abgebildet (**offen**) |
| Wirtschaft und Verkehr | 5,35 | 3,58 | −1,77 | Kürzung um 1,65 Punkte beschlossen (P8); Fernverkehrswege nicht eigens genannt (**offen**) |
| Umwelt | 0,56 | 0,86 | +0,30 | abgebildet |
| Wohnen, Gemeinwesen | 0,47 | 0,71 | +0,24 | abgebildet |
| Kultur, Sport | 1,05 | 1,22 | +0,17 | abgebildet |
| Bildung | 4,44 | 4,44 | 0,00 | abgebildet (Kitas zu prüfen) |
| **Allgemeine Verwaltung ohne Zinsen** | **5,21** | **2,99** | **−2,22** | Staatliche Ebene (Parlamente, Ministerien, Steuer- und Finanzverwaltung, Statistik) und Beiträge an die EU nicht eigens abgebildet (**offen**) |
| Gesundheit, Pflege | 7,51 | 7,75 | +0,24 | Netz; steigt mit der Alterung |
| Alter | 9,74 | 10,83 | +1,09 | Altrenten im Fonds (Schnitt der zehn), laufen bis 2092 aus |
| übrige Geldleistungen | 10,39 | 6,70 | −3,69 | Seil, Härtefall, Dividende |
| Zinsen | 1,12 | 1,80 | +0,68 | Fonds; Schnitt der zehn liegt über Deutschland |

Die Werte sind nicht ganz vergleichbar: Das Modell nimmt den Schnitt der zehn Staaten, Deutschland weicht davon ab.

## 4 Gleichgewicht: wo die Lücke liegt

| 2028, % BIP | |
|---|---|
| Ausgaben (Gemeinwesen, Unterstützung, Verwaltung, Altlasten) | 43,6 |
| Steuern | 31,2 |
| Fondsbeitrag (Zuschlag 17,3 % auf alle Steuern) | 5,3 |
| **Kreditaufnahme des Fonds** | **7,2** |
| Schuld des Fonds: höchster Stand | 151 % BIP im Jahr 2055, getilgt bis 2098 |

- Im laufenden Teil (Steuern gegen Gemeinwesen, Netz, Verwaltung, Dividende) ist der Haushalt jedes Jahr ausgeglichen. Möglich ist das nur, weil die Dividende als Rest gerechnet wird.
- Sie verliert bis 2060 2,65 Punkte des BIP:

| Ursache | Wirkung auf die Dividende 2028 → 2060 |
|---|---|
| Verteidigung auf 2,5 % | −1,10 |
| Wegfall der Lenkungsabgaben | −1,96 |
| Gesundheit und Pflege (Alterung) | −0,84 |
| kalte Progression | +1,25 |
| **zusammen** | **−2,65** (3,33 → 0,67 % BIP) |

Jede neue Lücke landet in der Dividende: die belegten Einnahmen (B-1), die Rentner, CO₂ (B-3) und künftig die Verwaltung. Der Grund ist der Bau der Rechnung, nicht ein einzelner Fehler.

## 5 Strukturprobleme und Empfehlungen

| Nr. | Befund | Empfehlung |
|---|---|---|
| 1 | Die **Dividende ist Restgröße** und trägt alle Abweichungen. | Die Dividende an eine stabile Basis binden (z. B. fester Anteil an Kapital- und Konsumaufkommen) und eine Ausgleichsrücklage einführen. Abweichungen gehen dann zuerst in die Rücklage, danach in eine Satzregel, nicht in die Dividende. |
| 2 | **Lenkungsabgaben** (2,8 % BIP 2028) finanzieren Daueraufgaben, obwohl sie wegfallen sollen. | Lenkungsabgaben dem Fonds (Altlasten) zuweisen, der selbst ausläuft. Daueraufgaben aus Arbeit, Kapital und Label ohne Sonderstufen tragen. |
| 3 | **Kapital ist statisch** gerechnet. Die Gewinne aus Automatisierung und Erbe, die das Projekt erwartet, fehlen. | Einen Trend für die Kapitalquote am Volkseinkommen und für das Erbvolumen rechnen (Varianten aus AMECO und der Bundesbank-Vermögensbilanz). Erst dann trägt die Annahme „Automatisierung finanziert die Dividende“. |
| 4 | **Kalte Progression** erhöht die Last auf Arbeit verdeckt (+1,25 % BIP bis 2060). | Offen ausweisen und entscheiden: Stufen voll an die Löhne binden (dann sinkt die Dividende stärker) oder die Progression ausdrücklich als Finanzierungsquelle beschließen. |
| 5 | **Verwaltung der staatlichen Ebene** fehlt (−2,2 % BIP gegen Deutschland, −1,2 gegen EU-27); dazu Justiz (−0,27) und Fernverkehrswege. | Eine Zeile „Staatsebene“ einführen und belegen, bevor sie als nächste Lücke auftaucht. Dabei die EU-Beiträge abgrenzen, die heute in der allgemeinen Verwaltung stehen (Annahme, zu prüfen). |
| 6 | **Mischland**: Ausgaben als Schnitt der zehn, Einnahmen auf deutscher Basis. | Einnahmen für den Schnitt der zehn rechnen oder Ausgaben für Deutschland. Die Länderseiten zeigen für den Schnitt der 30 Staaten 0,9 % BIP weniger Deckung. |
| 7 | **Ausgleich nur über die Zeit**: Fondskredit 7,2 % BIP im ersten Jahr, Schuld bis 151 % BIP. | Zinsrisiko offen zeigen (Fondszins 2,45 %, Empfindlichkeit `fondszins.json`). Die Lenkungsabgaben nach Punkt 2 senken den Kreditbedarf in der Anfangszeit. |

**Vorgeschlagene Reihenfolge:** zuerst Punkt 5 (prüfbar, schließt die nächste Lücke), dann Punkt 2 und 1 (Regeln), dann Punkt 3 (Trend). Punkt 6 ist eine Aufgabe der Rechnung und läuft nebenher.

## Quellen

- Europäische Kommission, GD TAXUD: Annual Report on Taxation 2026, Pressemitteilung vom 10.07.2026 (Steuerquote 39,4 %; Arbeit 51,5 %, Konsum 26,8 %, Kapital 21,6 % des Aufkommens 2024): https://taxation-customs.ec.europa.eu/news/european-commissions-annual-tax-report-art-provides-latest-insights-revenue-mix-2026-07-10_en
- Eurostat, Statistics Explained „Government expenditure by function – COFOG“ (EU-27 2023; PDF maschinell gelesen, an der Quelle zu prüfen): https://ec.europa.eu/eurostat/statistics-explained/SEPDF/cache/10912.pdf
- Eurostat gov_10a_taxag, gov_10a_exp, gov_10a_main, Deutschland 2024, vorläufig (`modell/haushaltsplan_de.toml`).
- BMF 2025 (Kapitalertragsteuern, `unternehmensbasis.toml`, Sekundärquelle); EU-SILC 2025 (Mieteinkünfte, `mikro_de.toml`).
- Rechnungen des Projekts: `systemvarianten.json` (33R), `projektion33.json`, `gesamtrechnung.json` (Dach und Gemeinden), `gesamtlast33.json`, `fonds_geltend.json`.
