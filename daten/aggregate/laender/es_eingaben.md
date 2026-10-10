# Spanien: Eingangsdaten für die länderspezifische Fassung

Stand: 10. Oktober 2026 · Modellstand v3.26 (Modellwerte unverändert); Rechnung nach Standard seit v3.26: `modell/laender/es.toml`, Ergebnis `daten/aggregate/laender/es.json` · Bausteine: B20 (Gesamtrechnung), dieser Datei. Keine Rechnung in diesem Schritt; die Modellwerte bleiben unverändert (Elastizität der Annahmen).

Abgerufen am 10.10.2026 durch Rechercheagenten (WebFetch/WebSearch). **Nicht von mir gegen die Originale geprüft.** Eurostat-Werte aus der Array-Position abgeleitet, an der Datenbank gegenzuprüfen. Status: amtlich, Sekundärquelle, Prognose, Annahme.

## 1. Staatsverschuldung und Defizit

| Größe | Wert | Bezugsjahr | Quelle | Status |
|---|---|---|---|---|
| Schuldenstand (Staat, PDE) | 100,7 % BIP (1.698 Mrd. €) | 2025 Q4 | Banco de España 31.03.2026; Eurostat gov_10dd_edpt1 GD (100,7) | amtlich, bestätigt |
| Schuldenstand, Vorabmeldung | 100,8 % | Dez. 2025 | Banco de España 17.02.2026 | amtlich, vorläufig |
| Schuldenstand | ca. 101,7 % (aus Differenz „1 pp weniger“) | 2024 | Banco de España | Annahme (abgeleitet) |
| Finanzierungssaldo | −2,4 % BIP (2025); −3,2 % (2024) | 2025 / 2024 | Eurostat gov_10dd_edpt1 B9 | amtlich |
| Schuldenstand, Prognose | 2026: 99,1 % (Hacienda), 99,9 % (AIReF); 2027: 97,6 % (Hacienda), 98,2 % (AIReF), 97,9 % (BdE) | 2026–2027 | El Independiente 08.07.2026; Bolsamania 18.06.2026 | Prognose, **Sekundärquelle** |
| Defizit, Prognose | 2026: 2,4 % (BdE), 2,1 % (Regierung, Nov. 2025); 2027: 2,3 % (BdE), 1,8 % (Regierung); 2028: 1,6 % (Regierung) | 2026–2028 | Bolsamania; Forbes 18.11.2025 | Prognose, **Sekundärquelle** |
| Schuldenstand 2028 | nicht gefunden | — | — | Lücke |

**Nachrecherche v3.26 (10.10.2026):**

| Größe | 2026 | 2027 | 2028 | 2029 | Quelle | Status |
|---|---|---|---|---|---|---|
| Defizit, Stabilitätsziele | — | −1,8 | −1,6 | −1,5 | Finanzministerium, Pressemitteilung 07.07.2026 (Ministerrat), WebFetch der Originalseite | amtlich, Ziel |
| Schuld, Stabilitätsziele | 99,1 (abgeleitet) | 97,6 | 96,4 | 95,3 | wie oben; 2026 aus „1,5 Punkte weniger“ abgeleitet | amtlich, Ziel |
| Defizit / Schuld, Informe de Progreso Anual | −2,1 / 99,3 | — | — | — | Informe 30.04.2026, über El Debate 01.05.2026 (Original für Abruf gesperrt) | Prognose, Sekundärquelle |
| Wachstum real / Deflator | 2,2 % / 3,1 % | — | — | — | wie oben; nominal 5,4 % daraus abgeleitet | Sekundärquelle, Ableitung = Annahme |
| Saldo / Schuld, EU-Kommission | −2,4 / 99,6 | −2,0 / 98,9 | — | — | Frühjahrsprognose 21.05.2026 | amtlich, Prognose |

Der Widerspruch Defizit 2026 Regierung 2,1 % gegen BdE 2,4 % bleibt: Die EU-Kommission sieht ebenfalls 2,4 %. Die Lücke „Schuldenstand 2028“ ist geschlossen (96,4 %, amtliches Ziel).

**Ergebnis nach Standard (v3.26):** Pfad A 2028 99,2 %, Pfad B 97,5 %, Pfad C (Regierung) 96,4 %. Bestandsanpassung 2026: 1,5 Punkte (mit abgeleitetem Wachstum, Annahme). Wohnort (Euro 2028, nominal): Dividendenboden 445,01 € je Erwachsenem und Monat, ausgezahlt (V3a) 491,17 €; Tarifstufen 10.680 / 21.360 / 32.041 / 42.721 €. Klubwirkung: mit Spanien auf dem Regierungspfad 81,15 % statt 81,29 %.

Haushalt 2026: Nach Presse (Forbes 26.04.2026) wurden die Presupuestos 2026 nicht vorgelegt; es gelten die verlängerten Haushalte von 2023 (prorrogados). **Sekundärquelle**, Congreso/BOE nicht geprüft.

Widersprüche: Defizit 2026 Regierung 2,1 % gegen BdE 2,4 % (nicht erklärt). Schuldenstand 2026 Hacienda 99,1 % gegen AIReF 99,9 %. Vorabwert 100,8 % gegen Endwert 100,7 %.

## 2. Sozialbeiträge und Gesundheit

| Größe | Wert | Bezugsjahr | Quelle | Status |
|---|---|---|---|---|
| Sozialbeiträge netto (D61), Gesamtstaat | 13,2 % BIP (davon Sozialversicherung S1314: 12,5 %) | 2024 | Eurostat gov_10a_taxag, D61 | amtlich, per WebFetch bestätigt |
| Gesundheitsausgaben (COFOG 07) | 6,5 % BIP | 2024 | Eurostat gov_10a_exp, GF07, S13 | amtlich, vorläufig |

Zum Vergleich mit den bisherigen Angaben: Frankreich 16,5 % (S1314 14,5 %), Deutschland 17,5 % (vorläufig). Die Rolle des Sistema Nacional de Salud (Comunidades Autónomas als Träger) ist nicht recherchiert.

## 3. Rente

| Größe | Wert | Bezugsjahr | Quelle | Status |
|---|---|---|---|---|
| Alterssicherung (COFOG 10.2) | 10,4 % BIP | 2024 | Eurostat gov_10a_exp, GF1002, S13 | amtlich, vorläufig |
| Fondo de Reserva | 15.267 Mio. € (höchster Stand seit 10 Jahren) | 31.03.2026 | Moncloa 13.04.2026 | amtlich (Regierung) |
| Alterssicherung, Projektion | 14 % BIP Durchschnitt bis 2050; Spitze 15,3 % | 2050 | Diario de León 10.04.2026 (INTegraSS) | **Sekundärquelle**, Regierungsposition |
| Vergleich Spitze | 17,3 % (EU Ageing Report 2024), 16,1 % (AIReF) | 2050 | wie oben | Sekundärquelle |

Der Informe de Envejecimiento (aktuelle Ausgabe) wurde nicht gefunden.

## 4. Einkommensteuer (IRPF)

| Größe | Wert | Bezugsjahr | Quelle | Status |
|---|---|---|---|---|
| Staatliche Skala (Art. 63.1 LIRPF), 6 Stufen | 9,5 % bis 12.450 €; 12 % bis 20.200 €; 15 % bis 35.200 €; 18,5 % bis 60.000 €; 22,5 % bis 300.000 €; 24,5 % darüber | 2026 | Guía Fiscal; Struktur bestätigt in Hacienda „Tributación Autonómica 2026“ | Sekundärquelle, Struktur amtlich |
| Mínimo del contribuyente | 5.550 € (ab 65: 6.700 €; ab 75: 8.100 €) | Renta 2025 | AEAT Manual Renta 2025 | amtlich (ab 65/75 nur Sekundär) |
| Mínimo por descendientes | 2.400 € (1. Kind), 2.700 € (2.), 4.000 € (3.), 4.500 € (ab 4.); unter 3 Jahren +2.800 € | Renta 2025 | AEAT | amtlich |
| Autonomes Tramo Madrid | 8,5 / 10,7 / 12,8 / 17,4 / 20,5 % | 2026 | taxdown (Grenzen aus Sekundärquelle abgeleitet; Höchstsatz durch Hacienda bestätigt) | Sekundärquelle |
| Autonomes Tramo Asturias | 8 Stufen, 9 % bis 26 % | 2026 | taxdown | Sekundärquelle |
| Gemeinsame Veranlagung | optional; Basisabzug 3.400 € (Ehe), 2.150 € (Alleinerziehende) | 2026 | taxdown | Sekundärquelle, Norm nicht geprüft |

Die Comunidades Autónomas setzen eigene Tramos. Splitting im engeren Sinn ist im Quelltext nicht belegt. Eine ältere Tabelle (19 bis 47 %) widerspricht der amtlichen Skala und ist veraltet.

## 5. Kapitaleinkünfte (base del ahorro)

19 % (bis 6.000 €); 21 % (bis 50.000 €); 23 % (bis 200.000 €); 27 % (bis 300.000 €); 30 % (ab 300.000 €). Ley 7/2024, ab Veranlagung 2025. Quelle Guía Fiscal, **Sekundärquelle**.

**Befund für das Modell:** Der Spitzensatz für Kapitalerträge liegt in Spanien seit 2025 bei 30 %. Das Konzept setzt 28 % auf Kapitalerträge. Das ist eine Setzung, kein Fehler im Konzept, aber für die spanische Fassung ein Vergleichspunkt.

## 6. Mehrwertsteuer (IVA)

| Größe | Wert | Quelle | Status |
|---|---|---|---|
| Normalsatz / ermäßigt / superermäßigt | 21 % / 10 % / 4 % (Ley 37/1992) | SparkReceipt (kommerziell), AEAT nicht abrufbar | Sekundärquelle |
| Aufkommen (D211, S13) | 6,4 % BIP | Eurostat gov_10a_taxag, 2024, aus Array | amtlich, per WebFetch bestätigt |
| Befristete Senkungen 2026 | Kraftstoff, Strom, Gas auf 10 % bis 30.06.2026 (RDL 7/2026); Strom/Gas danach bedingt (RDL 18/2026) | Hacienda 20.03.2026; PwC-Newsletter Juli 2026 | amtlich (Mitteilung); Sekundärquelle für Folgeregel; BOE-Wortlaut nicht geprüft |

## 7. Gemeinden und Regionen

| Größe | Wert | Bezugsjahr | Quelle | Status |
|---|---|---|---|---|
| Ausgaben der Gemeinden (S1313), gesamt | 6,1 % BIP | 2024 | Eurostat gov_10a_exp, TOTAL | amtlich, vorläufig |
| Anzahl Municipios | nicht gefunden | 01.01.2026 | — | Lücke |
| Comunidades Autónomas (17), Provinzen (50) | allgemein bekannt | — | — | Annahme, nicht belegt |
| Aufgaben und Finanzierung der CCAA (Gesundheit, Bildung, Soziales) | nicht recherchiert | — | — | Lücke |

## 8. Verfassung (nur Fundstelle)

BOE-A-1978-31229 (BOE Nr. 311, 29.12.1978). Art. 137, 143 und 156 (Autonomie und Finanzautonomie) nicht im Wortlaut geprüft. Keine Rechtsbewertung.

## 9. Lücken

- Schuldenstand 2028: nicht gefunden.
- Informe de Envejecimiento: nicht gefunden.
- Anzahl Municipios: nicht gefunden.
- Rolle des SNS und Finanzierung der CCAA.
- Originaldokumente der Prognosen (BdE, Hacienda, AIReF) und der Haushaltsverlängerung: nicht abgerufen.
- Verfassungswortlaut.

## Eurostat-Werte: per WebFetch bestätigt (10.10.2026)

Die Shell erreicht Eurostat nicht (HTTP 403). Die Abrufe erfolgten über WebFetch (maschinell gelesen). Alle sechs Werte stimmen mit dem Agentenbericht überein.

| Reihe | Wert | Bezugsjahr | Status in der Datenbank |
|---|---|---|---|
| `gov_10dd_edpt1`, GD, S13 | 100,7 % BIP | 2025 | amtlich |
| `gov_10dd_edpt1`, B9, S13 | −2,4 % BIP | 2025 | amtlich |
| `gov_10a_taxag`, D61, S13 | 13,2 % BIP | 2024 | nicht angegeben |
| `gov_10a_taxag`, D211, S13 | 6,4 % BIP | 2024 | nicht angegeben |
| `gov_10a_exp`, GF07, S13 | 6,5 % BIP | 2024 | vorläufig (p) |
| `gov_10a_exp`, GF1002, S13 | 10,4 % BIP | 2024 | vorläufig (p) |
