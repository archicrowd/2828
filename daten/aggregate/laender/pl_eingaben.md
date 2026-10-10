# Polen: Eingangsdaten für die Länderrechnung (Standard Fassung 1.2, Modellstand v3.26)

Stand: 10. Oktober 2026. Rechnung: `modell/laender/rechne.py`; Parameter: `modell/laender/pl.toml`; Ergebnis: `daten/aggregate/laender/pl.json`.

„WebFetch“ heißt: Die Seite wurde abgerufen und der Wert maschinell aus Text oder Datenbankausgabe gelesen. Der Wert ist nicht von Hand am Original geprüft. Polen steht nicht im Gewichtsbestand der Gesamtrechnung. Die Gewichtungsrechnung (Standard 2.4) und die ausgezahlte Dividende V3a (Standard 2.6) entfallen deshalb.

## 1. Staatsschuld und Saldo, Stand 2025 und Verlauf

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| Schuldenquote, Gesamtstaat (EU-Definition) | 59,7 % BIP | 2025 | Eurostat `gov_10dd_edpt1`, GD, S13 | amtlich, maschinell | WebFetch 10.10.2026. Gleich bei GUS (01.04.2026), im Fortschrittsbericht (28.04.2026) und bei der EU-Kommission (21.05.2026). |
| Finanzierungssaldo | −7,3 % BIP | 2025 | Eurostat `gov_10dd_edpt1`, B9, S13 | amtlich, maschinell | WebFetch. Gleich im Fortschrittsbericht und bei der EU-Kommission. GUS vorläufig: −7,2 %. |
| Verlauf der Schuldenquote | 2010: 53,7 · 2011: 54,8 · 2012: 54,5 · 2013: 56,9 · 2014: 51,1 · 2015: 51,1 · 2016: 54,1 · 2017: 50,4 · 2018: 48,2 · 2019: 45,2 · 2020: 56,6 · 2021: 53,0 · 2022: 48,8 · 2023: 49,5 · 2024: 54,8 · 2025: 59,7 | 2010–2025 | Eurostat `gov_10dd_edpt1`, GD, S13 | amtlich, maschinell | WebFetch. 2023 und 2024 gleich im Fortschrittsbericht (Tabelle 8). |
| Saldo 2023, 2024 | −5,2 % / −6,4 % BIP | 2023, 2024 | Fortschrittsbericht 28.04.2026, Tabelle 8 | amtlich | WebFetch des PDF (gov.pl) |
| Schuldenquote, 1. Quartal 2026 | 61,6 % BIP | Q1 2026 | Finanzministerium, über Notes from Poland, 12.06.2026 | Sekundärquelle, Quartalswert | Kontrollwert, geht nicht in die Rechnung ein |

Die Abweichung beim Saldo 2025 ist geklärt. Eurostat, der Fortschrittsbericht und die EU-Kommission nennen alle −7,3 %. Die −7,2 % von GUS waren die vorläufige Meldung vom 1. April.

## 2. Prognosen 2026–2030

| Größe | 2026 | 2027 | 2028 | 2030 | Quelle | Status |
|---|---|---|---|---|---|---|
| Saldo Gesamtstaat, Haushaltsentwurf 2027 | −7,1 | −7,1 | — | — | Ministerrat 28.08.2026; 2027: PAP Biznes (Überschrift), Notes from Poland; 2026: rp.pl („tyle ile rok wcześniej“), Notes from Poland | Prognose, Sekundärquelle (je zwei Quellen) |
| Defizit des Staatshaushalts (nicht Gesamtstaat) | — | 282,6 Mrd. Zł | — | — | Forsal/PAP 28.08.2026 | Sekundärquelle; nicht in der Rechnung. In v3.24 irrtümlich in der Zeile zum Gesamtstaat geführt (Korrektur 56) |
| Saldo, Fortschrittsbericht | −6,8 | — | — | — | Fortschrittsbericht 28.04.2026, Tabelle 7 (gov.pl) | amtlich, Prognose (älter) |
| Saldo, EU-Kommission | −6,5 | −6,3 | — | — | Frühjahrsprognose 21.05.2026 (Länderseite der Kommission) | amtlich, Prognose |
| Schuld (EU-Def.), Schuldenstrategie 2027–2030 | 67,6 | 69,3 | — | 76,6 | Ministerrat Ende September 2026; rp.pl 29.09.2026, Parkiet 29.09.2026, Interia | Prognose, **Sekundärquelle** (vier übereinstimmende Quellen: zusätzlich Forsal/PAP 29.09.2026); Original (Sejm-Drucksache 3150) nicht abrufbar |
| Schuld (EU-Def.), Fortschrittsbericht | 65,1 | — | — | — | Fortschrittsbericht 28.04.2026 | amtlich, Prognose (älter) |
| Schuld (EU-Def.), EU-Kommission | 64,5 | 68,3 | — | — | Frühjahrsprognose 21.05.2026 | amtlich, Prognose |
| Schuld, nationale Definition (PDP) | 55,3 | 55,9 | 58,6 | 58,3 | Schuldenstrategie 2027–2030, über Parkiet und Interia | Sekundärquelle; Strefa Biznesu nennt 55,09 für 2027 (Widerspruch, vermutlich Schreibfehler) |
| Nominales BIP-Wachstum | 6,2 % | — | — | — | Fortschrittsbericht 28.04.2026, Tabelle 3 | amtlich, Annahme der Regierung |

In der Rechnung verwendet: Saldo −7,1 % (2026, 2027) aus dem jüngsten Regierungsdokument, 2028 Annahme gleich 2027. Schuldenquote 67,6 / 69,3 % aus der Schuldenstrategie. 2028: **Annahme** 71,7 %, linear interpoliert zwischen 2027 und 2030 (Standard 2.3).

Befund: Nach der Strategie steigt die Quote 2026 um 7,9 Punkte. Mit Saldo −7,1 % und nominalem Wachstum 6,2 % erklärt die Fortschreibung nur einen Anstieg auf 63,3 %. Die Differenz von 4,3 Punkten ist eine Bestandsanpassung. Die Ursache ist nicht geprüft. Denkbar wären Vorfinanzierung oder Schulden außerhalb des Haushalts, das ist aber eine Vermutung. Das implizite Wachstum von −1,3 % im Pfad C ist deshalb keine Wachstumsprognose (Standard 2.3).

Befund zur Wachstumsannahme: Der Standard setzt für alle Länder 3,0 % nominales Wachstum. Die polnische Regierung erwartet 2026 6,2 %. Die Pfade A und B überzeichnen den Schuldenanstieg Polens deshalb. Ob das Wachstum je Land gesetzt wird, entscheidet die Initiative.

## 3. Bruttoinlandsprodukt, Bevölkerung, Preisniveau

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| BIP, nominal | 852.229,8 Mio. € | 2024 | Eurostat `nama_10_gdp`, B1GQ, CP_MEUR | amtlich, maschinell | WebFetch 10.10.2026 |
| Bevölkerung, Jahresdurchschnitt | 36.559.233 | 2024 | Eurostat `demo_gind`, AVG | amtlich, maschinell | WebFetch 10.10.2026. Stimmt mit der Vorchat-Quelle überein. |
| Preisniveau, Individualverbrauch (EU27 = 100) | 70,2 | 2024 | Eurostat `prc_ppp_ind`, `na_item` PLI_EU27_2020, `ppp_cat` A01 | amtlich, maschinell | WebFetch 10.10.2026. Gegenprobe Deutschland mit derselben Abfrage: 109,1 = Repository-Wert. Gleiche Abgrenzung. |

Ursache der früheren Fehlabrufe: Die Abfrage setzte A01 als `na_item`. A01 gehört zur Dimension `ppp_cat` (Arbeitsfehler, v3.25 behoben).

## 4. Wohnort (Ergebnis nach Standard 2.6, Euro 2028, nominal)

| Größe | Polen | Deutschland (Vergleich) |
|---|---|---|
| Dividendenboden je Erwachsenem und Monat | 344,43 € | 535,29 € |
| je Kind und Monat | 172,22 € | 267,64 € |
| Tarifstufen (Beginn 9 / 16 / 21 / 28 %) | 8.266 / 16.533 / 24.799 / 33.065 € | 12.847 / 25.694 / 38.541 / 51.387 € |

Die Beträge sind kaufkraftgleich. 344,43 € in Polen entsprechen nach Preisniveau 535,29 € in Deutschland.

## 5. Verfassung

Nicht im Wortlaut geprüft. Der Abruf des englischen Verfassungstexts beim Sejm (Art. 15, 16, 163, 167, 216 Abs. 5) wartete auf eine Freigabe und wurde zurückgezogen. Allgemein bekannt, aber hier nicht belegt: Art. 216 Abs. 5 begrenzt die Staatsschuld (nationale Definition) auf drei Fünftel des BIP. Darauf beziehen sich die Aussagen des Ministers zur 60-%-Grenze. Status: **Annahme**, an der Quelle zu prüfen.

## 6. Lücken

1. Schuldenquote 2028 der Regierung nicht gefunden (interpoliert).
2. Saldo 2028 nicht gefunden (Annahme gleich 2027).
3. Nominales Wachstum der Regierung nur für 2026.
4. Schuldenstrategie 2027–2030 und Haushaltsentwurf 2027 nicht am Original geprüft.
5. Verfassungswortlaut.
6. Anzahl der Gemeinden (gminy) nicht belegt; die Übersicht des Geoportals (Stand 01.01.2026) nennt keine Zahl im Text.

## 7. Abrufe am 10.10.2026 (WebFetch)

- Eurostat `gov_10dd_edpt1`, PL, GD, S13, 2010–2025; B9, 2025.
- Eurostat `nama_10_gdp`, PL, B1GQ, CP_MEUR, 2024.
- Eurostat `demo_gind`, PL, AVG, 2024.
- Eurostat `prc_ppp_ind`, PL und DE, `ppp_cat` A01, `na_item` PLI_EU27_2020, 2024.
- GUS, 01.04.2026. Fortschrittsbericht, gov.pl, 28.04.2026. EU-Kommission, Länderseite Polen, Frühjahr 2026.
- rp.pl 29.09.2026; Parkiet 29.09.2026; Interia (Schuldenstrategie); Strefa Biznesu 05.10.2026; Notes from Poland 12.06.2026 und 28.08.2026.
- Nicht erreichbar: Sejm-Drucksache 3150 (Zugangsprüfung), PAP Biznes (Bot-Schutz), Scope Ratings (JavaScript), ING Think (robots), Sejm-Verfassungstext (Freigabe nicht beantwortet).
