# Quellen der Webseite (Stand B, deutsch)

Alle Zahlen der Seite kommen aus `daten/aggregate/gesamtrechnung.json` (Bauskript `seite/werkzeuge/seite_bau.py`).
Diese Datei belegt die Länderbeispiele und die Kennzahlen der Ausgangslage, die nicht aus der Rechnung stammen.
Geprüft am 7. Oktober 2026 über Web-Abruf (maschinell gelesen, an der Quelle zu prüfen), sofern nicht anders vermerkt.

| Aussage auf der Seite | Quelle | Stand |
|---|---|---|
| Abgabenkeil 47,9 % (DE), OECD-Schnitt 34,9 % | OECD, Taxing Wages 2025, Tabelle 3.1 | gelesen 6.10.2026 |
| 26,4 % auf Zinsen und Kursgewinne | § 32d EStG (25 %) mit Solidaritätszuschlag | Gesetzestext |
| Estland: 22 % Einheitssatz | ERR News und Steuerberatungsquellen 2025/26: die für 2026 geplante Anhebung auf 24 % entfällt, der Satz bleibt 22 % | mehrere Sekundärquellen; amtlich: Estnische Steuerbehörde (emta.ee) zu prüfen |
| Estland: Grundsteuer allein auf den Bodenwert seit 1993; Steuererklärung online in Minuten | Gesamtkonzept; Logbuch Band I | übernommen |
| Dänemark: 98 Kommunen seit 2007; kaum Sozialbeiträge | Local Government Denmark (Strukturreform 2007); Eurostat gov_10a_taxag D61 Dänemark 0,7 % des BIP (2024) | übernommen / Eurostat |
| Schweiz: CO₂-Abgabe seit 2008, gleichmäßig an alle Einwohner über die Krankenkassenprämie zurückverteilt | BAFU, „CO₂-Abgabe: Rückverteilung an die Bevölkerung" (2025: 61,80 CHF je Person) | gelesen 7.10.2026 |
| Schweiz: Gemeinden setzen ihre Steuern selbst fest | Gemeindesteuerfuss (allgemein bekannt) | nicht eigens geprüft |
| Alaska: Dividende seit 1982, jährlich, ohne Bedürftigkeitsprüfung | Alaska Permanent Fund (2025: 1.000 US-Dollar, Alaska Beacon / Juneau Empire) | gelesen 7.10.2026 |
| Baden-Württemberg: Grundsteuer nur auf den Bodenwert seit 2025 | Landesgrundsteuergesetz Baden-Württemberg | übernommen |
| Neuseeland: Mehrwertsteuer (GST) mit einem Satz und breiter Basis | Inland Revenue Neuseeland (GST 15 %) | nicht eigens geprüft |
| Estland 5,8 %, Deutschland 16,8 % Verwaltungsanteil der Gemeinden | Gesamtkonzept Abschnitt 1.4 (Eurostat COFOG S1313) | übernommen |
| Einwohner der zehn Staaten | Eurostat demo_gind AVG 2024 (`daten/aggregate/laender_2024.csv`) | abgerufen 6.10.2026 |
| Dividende je Erwachsenem / Kind | Klubschnitt je Einwohner (Gesamtrechnung), Kinder zur Hälfte, Anteil Minderjähriger 16,67 % (Annahme, nationales Modell) | Rechnung |
| „über 95 %" | Gruppenschätzung des nationalen Modells (Stand A), ohne Mikrosimulation | Schätzung (Logbuch B18) |
| Möglichkeitsraum: Einwohner von 31 europäischen Staaten | `daten/aggregate/moeglichkeitsraum.csv`: zehn Klubstaaten Eurostat demo_gind AVG 2024 (abgerufen 6.10.2026); übrige 21 aus `archiv/uploads-eigen/web/moeglichkeitsraum.html` (Vorchat, laut Seite Eurostat-Einzelabrufe 2024) | Sekundärquelle für 21 Staaten |
| Schwelle Vereinigte Staaten 341,8 Mio | US Census Bureau NST-EST2025-POP laut moeglichkeitsraum.html | Sekundärquelle |
| Kanada 41,7 Mio | Statistics Canada, The Daily vom 24.9.2025: 41.651.653 am 1.7.2025 | gelesen 7.10.2026 |
| Kanada: CETA; Sicherheits- und Verteidigungspartnerschaft mit der EU seit 2025 | EAD / Europäische Kommission: Unterzeichnung beim 20. Gipfel EU–Kanada am 23./24.6.2025 | gelesen 7.10.2026 |
| Großbritannien nicht an Art. 113 AEUV gebunden | Vertragstext (Austritt 2020) | allgemein bekannt |
| „Sechs genügen" (DE, UK, FR, IT, ES, PL: 365,9 Mio) | Summe aus `moeglichkeitsraum.csv` | Rechnung |
| Grafik Staatsschulden: Euroraum 2010–2025 | Eurostat gov_10dd_edpt1, EA20, GD, PC_GDP (Web-Abruf 7.10.2026) | gelesen 7.10.2026 |
| Grafik Staatsschulden: Klub ab 2028 | `daten/aggregate/gesamtrechnung.json` (reihe_d) | Rechnung |
| Grafik CO₂: Deutschland 2010–2024 | Werte der bisherigen Webseite (Umweltbundesamt laut Vorchat) | Sekundärquelle |
| Grafik CO₂: 2025 = 649 Mio t; 1990 = 1.253 Mio t; Ziel 2030 = 438 Mio t; Neutralität 2045 | Umweltbundesamt, „Treibhausgas-Emissionen in Deutschland" (vorläufige Daten 2025) | gelesen 7.10.2026 |
| Grafik CO₂: Ziel 2040 = 150 Mio t | Klimaschutzgesetz: −88 % gegenüber 1990 (1.253 × 0,12) | Rechnung aus Gesetzesziel |
| Grafik Staatsschulden: gestrichelte Linie 2024–2028 | Klub-Schuldenquote 2024 BIP-gewichtet (78,45 %, `basis.py`) bis zur Startannahme 2028 (78,4 %, `gesamtrechnung.toml`) | Annahme der Gesamtrechnung |
| Ländernamen in den Sprachfassungen | Browserfunktion `Intl.DisplayNames` (CLDR) | technisch |
