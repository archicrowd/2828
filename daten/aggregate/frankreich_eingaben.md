# Frankreich: Eingangsdaten für die länderspezifische Fassung

Stand: 10. Oktober 2026 · Modellstand v3.23 · Bausteinen: `modell/frankreich.py` (Rechnung), `daten/aggregate/frankreich.json` (Ergebnis)

Die Angaben stammen aus einer Recherche über Abrufe (WebFetch) am 10.10.2026. Die Einträge mit „Agent“ sind von einem
Rechercheagenten abgerufen und **nicht von mir selbst gegen die Originale geprüft**. Die Einträge mit „geprüft“ habe ich
über Eurostat selbst abgerufen (Abrufe unten). Status: amtlich (Originalquelle), Sekundärquelle, Prognose, Annahme.

## 1. Staatsverschuldung und Defizit

| Größe | Wert | Bezugsjahr | Preisbasis | Quelle | Status | Prüfung |
|---|---|---|---|---|---|---|
| Schuldenstand (Maastricht, brutto) | 3.460,5 Mrd. €; 115,6 % BIP | 2025 | laufend | INSEE, IR78 (27.03.2026), https://www.insee.fr/fr/statistiques/8956575 | amtlich | Agent |
| Defizit | 152,5 Mrd. €; 5,1 % BIP | 2025 | laufend | wie oben | amtlich | Agent; Repository-Wert gleich |
| Defizit (revidiert) | 169,1 Mrd. €; 5,8 % BIP | 2024 | laufend | wie oben | amtlich | Agent |
| Ausgaben / Einnahmen | 57,2 % / 52,1 % BIP | 2025 | laufend | wie oben | amtlich | Agent |
| Schuldenquote (Regierungsprognose) | 2026: 119,3 %; 2027: 121,7 %; 2028: 122,4 % | 2026–2028 | laufend | Rapport sur la dette 2027 (PLF 2027), https://www.budget.gouv.fr/documentation/file-download/34336 | amtlich, Prognose | Agent |
| Saldo Gesamtstaat (Regierungsprognose) | 2026: −5,4 %; 2027: −5,0 %; 2028: −3,9 % | 2026–2028 | laufend | PLF-Anhang und RESF 2027 (06.10.2026), https://www.tresor.economie.gouv.fr/Articles/2026/10/06/le-rapport-economique-social-et-financier-resf-2027-est-publie | amtlich, Prognose | Agent |
| Wachstum real (Regierungsannahme) | 0,5 % (2026), 1,0 % (2027) | 2026–2027 | real | RESF 2027 | amtlich, Annahme | Agent |
| Zinsausgaben 2026 | 77 Mrd. € (+12 Mrd.) | 2026 | laufend | Cour des comptes, über Public Sénat (25.06.2026) | **Sekundärquelle** | Agent |
| Einschätzung Hoher Finanzrat (HCFP) | Prognosen „optimistisch“; 2026 Defizit wahrscheinlich 5,4 %; 2027 Wachstum 0,7–0,9 % statt 1 % | 2026–2027 | — | Public Sénat (07.10.2026) | **Sekundärquelle** | Agent |

Widersprüche: Schuldenquote 2025 115,6 % (INSEE) gegen 115,7 % (PLF, Tabelle 3.460,5 Mrd. €, Text 3.460,1 Mrd. €), Ursache ungeklärt.
Ein Presseartikel nennt für den Cour-Bericht einen Rückgang „von 5,4 % auf 5,0 %“ für 2025; das passt nicht zu INSEE (5,1 %).

## 2. Sozialbeiträge und Gesundheit

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| Sozialbeiträge, netto (D61), Gesamtstaat | 16,5 % BIP | 2024 | Eurostat gov_10a_taxag, FR, S13 | amtlich | **geprüft** |
| Sozialbeiträge, netto (D61), Sozialversicherung S1314 | 14,5 % BIP | 2024 | wie oben | amtlich | **geprüft** |
| Sozialbeiträge (cotisations sociales effectives) | 446,3 Mrd. € | 2025 | INSEE, Compléments IR78 | amtlich | Agent |
| Sozialbeiträge, Eurostat D61 Deutschland (Vergleich) | 17,5 % BIP (vorläufig) | 2024 | Eurostat gov_10a_taxag, DE, S13 | amtlich, vorläufig | **geprüft** |
| Prélèvements obligatoires | 43,6 % BIP | 2025 | INSEE | amtlich | Agent |
| Gesundheitsausgaben gesamt | 11,4 % BIP | 2024 | DREES, Comptes de la santé 2025 | amtlich | Agent |
| Leistungen Krankheit | 9,5 % BIP | 2024 | DREES, CPS 2025 | amtlich | Agent |

Konzeptunterschied: 11,4 % (Gesamtausgaben) und 9,5 % (Krankheitsleistungen) sind verschiedene Größen. Für die Webseite nur eine Größe mit Begriff verwenden.

## 3. Rente

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| Rentenausgaben (COR-Abgrenzung) | 14,1 % BIP | 2025 | COR, Rapport annuel (Juni 2026) | amtlich | Agent |
| Rentenausgaben, Prognose | 14,1 % (2030), 14,2 % (2045), 15,3 % (2070) | Prognose | wie oben | amtlich, Prognose | Agent |
| Alterssicherung, COFOG 10.2 (Eurostat) | **Frankreich 13,4 %**, Deutschland **9,9 %** BIP | 2024 | Eurostat gov_10a_exp, S13, GF1002 (vorläufig, „p“) | amtlich, vorläufig | **geprüft** |
| Umlagefinanzierung | 277 Mrd. € von 417 Mrd. € Ressourcen | 2025 | COR (wie oben) | amtlich | Agent |

Die beiden Rentenzahlen (14,1 % und 13,4 %) stammen aus verschiedenen Abgrenzungen (COR-Systemabgrenzung gegen COFOG 10.2) und sind nicht vergleichbar.

## 4. Einkommensteuer und Familie

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| Tarif je Anteil (Grenze / Satz) | bis 11.600 € 0 %; bis 29.579 € 11 %; bis 84.577 € 30 %; bis 181.917 € 41 %; darüber 45 % | 2026 (Einkommen 2025), nominal | service-public.gouv.fr, F1419 | amtlich | Agent |
| Quotient familial, Deckel je halbem Anteil | 1.807 € | 2026, nominal | DGFiP-Brochure „Calcul de l'impôt“, S. 370 | amtlich | Agent; Presse bestätigt (Sekundärquelle) |
| Quotient familial, weitere Deckel | 4.262 € (Alleinerziehende, erste Halbanteile); 2.011 € bzw. 3.614 € (Verwitwete); 1.079 € | 2026 | Brochure, S. 370–371 (Auszug) | amtlich (Auszug) | Agent |
| Anteile je Kind | 1. und 2. Kind je 0,5; ab 3. Kind je 1 | 2026 | toutsurmesfinances.com | **Sekundärquelle** | Agent |
| Deckel je Kind ab dem 3. Kind | 3.614 € (aus dem Halbanteil-Deckel abgeleitet) | 2026 | eigene Ableitung | **Annahme** | — |
| Kindergeld (2 Kinder) | 153,01 € monatlich | ab 01.04.2026 | solidarites.gouv.fr | amtlich | Agent |

## 5. Kapitaleinkünfte

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| Prélèvement forfaitaire unique (PFU) | 31,4 % (ab 2026); 30 % bis 2025 | 2026 | impots.gouv.fr, „Les revenus mobiliers“ (08.04.2026) | amtlich | Agent; Presse bestätigt |
| Zusammensetzung 2026 | Einkommensteuer 12,8 %, Sozialabgaben 18,6 % (CSG 10,6, CRDS 0,5, Solidaritätsabgabe 7,5) | 2026 | wie oben | amtlich | Agent |

## 6. Mehrwertsteuer

| Größe | Wert | Quelle | Status | Prüfung |
|---|---|---|---|---|
| Normalsatz / ermäßigt / Sondersatz | 20 % / 10 % und 5,5 % / 2,1 % | economie.gouv.fr (Seite 11.12.2025) | amtlich | Agent |
| Mehrwertsteuer-Aufkommen (D211, Eurostat) | nicht abgerufen | gov_10a_taxag | — | Lücke |

## 7. Kommunen

| Größe | Wert | Bezugsjahr | Quelle | Status | Prüfung |
|---|---|---|---|---|---|
| Gemeinden | 34.875 | 01.01.2026 | DGCL, Bulletin BIS 206 | amtlich | Agent |
| Intercommunalités mit eigener Steuerkraft | 1.252 | 01.01.2026 | wie oben | amtlich | Agent |
| Gemeindeverwaltung, Anteil am Fachbudget (COFOG S1313) | nicht abgerufen. Hinweis: Der Wert „S1313 = 0,0 %“ bei D61 betrifft Sozialbeiträge der Gemeinden, nicht die Verwaltung | 2024 | Eurostat gov_10a_exp (nicht erneut abgerufen) | — | Lücke |
| Départements und Régions, Zuständigkeiten 2026 | nicht belegt | — | Quelle von 2015 veraltet, nicht verwendet | Lücke | — |

## 8. Verfassung (nur Fundstelle)

Artikel 1 und 72 der Verfassung vom 4. Oktober 1958: Légifrance JORFTEXT000000571356 (Fassung 23.07.2017). Der Abruf ist
fehlgeschlagen; der Wortlaut ist nicht geprüft. Keine Bewertung der Zulässigkeit (keine Rechtsberatung).

## 9. Klub-Rechnung (Ergebnis `modell/frankreich.py`)

Schuldenquote Frankreich 2025: 115,6 %. Gewicht Frankreich am Klub-BIP: 24,1 % (Gewichte BIP 2024, basis.py).

| Jahr | A: Klub-Annahme (Defizit −5,1 %, g 3,0 %) | B: Regierungsdefizit, g 3,0 % | C: Regierungsdefizit und implizites Wachstum | Regierung |
|---|---|---|---|---|
| 2026 | 117,3 | 117,6 | 119,3 | 119,3 |
| 2027 | 119,0 | 119,2 | 121,7 | 121,7 |
| 2028 | 120,6 | 119,6 | 122,4 | 122,4 |

Das implizite nominale Wachstum des Regierungspfads beträgt 1,49 % (2026), 2,23 % (2027), 2,70 % (2028). Das liegt unter der Klubannahme von 3,0 %. Der Unterschied zwischen B und C entsteht also durch das Wachstum, nicht durch das Defizit.

Klubquote 2028 (BIP-gewichtet, Rest-Saldo so, dass der Klub-Gesamtsaldo −2,93 % bleibt):
- Klubmethode (Konzept, `schuldenpfad.py`): **81,29 %**
- Frankreich wie Klub (A): 81,29 %
- Frankreich mit Regierungsdefizit (B): 81,29 %
- Frankreich mit Regierungsdefizit und Regierungswachstum (C): **81,96 %**

Die Wirkung von C (+0,7 Punkte) liegt innerhalb des Risikofalls im Konzept („Schuldenquote 2028 +3,5 Punkte“, 84,8 %).

## 10. Lücken

- Schuldenstand 2028 in Mrd. €: nicht in den Dokumenten.
- Cour des comptes (Originalbericht), HCFP-Originalavis, PLF-Textfassung: nicht abgerufen.
- Sozialbeiträge des Gesamtstaates in % BIP aus Eurostat für S13 als Summe: nur über D61 (16,5 %), nicht über die Summe der Einzelposten geprüft.
- Vergleich DK D61 (0,7 %): aus dem Repository übernommen, nicht in dieser Sitzung abgerufen.
- Verfassung: Wortlaut.
- Zuständigkeiten Départements und Régions 2026.
- Mehrwertsteuer-Aufkommen Frankreich (D211) und Anteil der Ausnahmen.

## Abrufe (Eurostat, 10.10.2026, geprüft)

- `gov_10a_taxag`, FR, PC_GDP, D61, 2024: S13 16,5; S1314 14,5; S1311 1,9; S1313 0,0 (S1312 fehlt, Flag „m“)
- `gov_10a_taxag`, DE, PC_GDP, D61, 2024: S13 17,5 (p); S1314 16,4 (p)
- `gov_10a_exp`, FR, PC_GDP, GF1002, S13, 2024: Gesamt 13,4 (p)
- `gov_10a_exp`, DE, PC_GDP, GF1002, S13, 2024: Gesamt 9,9 (p)
