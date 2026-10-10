# Belgien: Eingangsdaten für die Länderrechnung (Standard Fassung 1.3, Modellstand v3.27)

Stand: 10. Oktober 2026. Rechnung: `modell/laender/rechne.py`; Parameter: `modell/laender/be.toml`; Ergebnis: `daten/aggregate/laender/be.json`.

Recherche durch einen Rechercheagenten (WebFetch/WebSearch, 10.10.2026). Von mir selbst geprüft sind nur die Einträge mit „geprüft“. Alle übrigen sind **Agent, nicht selbst geprüft**.

## 1. Stand 2025

| Größe | Wert | Quelle | Status | Prüfung |
|---|---|---|---|---|
| Schuldenquote 2025 | 107,9 % BIP | Eurostat `gov_10dd_edpt1`, GD, S13 | amtlich, maschinell | **geprüft** (WebFetch); gleich Repository, EU-Kommission |
| Saldo 2025 | −5,2 % BIP | Eurostat-Mitteilung 22.04.2026; Repository | amtlich | Repository-Wert; FPB und NBB vorläufig −5,3 % (Agent) |
| Schuldenquote 2024 | 103,9 % BIP | Eurostat | amtlich, maschinell | **geprüft** |

## 2. Prognosen

| Quelle | Größe | 2026 | 2027 | 2028 | 2029 | Status | Prüfung |
|---|---|---|---|---|---|---|---|
| Rechnungshof, Doc 56 1469/002 (22.05.2026), Regierungspfad mit geplanten Maßnahmen | Saldo Gesamtstaat | −4,9 | −5,0 | −5,1 | −5,5 | amtlich, Prognose | **geprüft** (WebFetch lachambre.be). Der Agent hatte für 2029 −5,0 gemeldet (Lesefehler). |
| dto. | Schuld Gesamtstaat | 110,3 | — | — | — | amtlich | **geprüft** |
| dto., Schneeballtabelle | Nominales Wachstum | 3,32 % | 2,92 % | 3,22 % | — | amtlich | **geprüft** |
| Planbureau (FPB), Februar 2026, unveränderte Politik | Saldo | −4,9 | −5,1 | −5,2 | −5,7 | amtlich (2026), sonst Sekundärquelle | Agent |
| dto. | Schuld | 109,4 | 111,9 | 114,0 | 116,6 | Sekundärquelle (Blog) | Agent |
| FPB, Juni 2026 | Saldo / Schuld | −5,1 / 109,9 | — | — | — | Sekundärquelle (Belga); plan.be nicht erreichbar | Agent |
| Nationalbank (NBB), Juni 2026 | Saldo | −5,3 | −5,5 | −5,7 | — | Sekundärquelle | Agent |
| dto. | Schuld | 111,3 | 112,9 | 114,8 | — | Sekundärquelle | Agent |
| EU-Kommission, Frühjahr 2026 | Saldo / Schuld | −5,2 / 110,5 | −5,4 / 112,8 | — | — | amtlich, Prognose | Agent |

In der Rechnung verwendet: Saldo aus dem Regierungspfad laut Rechnungshof. **Pfad C entfällt:** Für 2027 und 2028 gibt es keine amtliche Schuldenquote der Regierung. Zum Vergleich ergibt Pfad B 113,3 % (2028), FPB Februar 114,0 %, NBB 114,8 % (Sekundärquellen).

Hinweis: Der Haushalt 2027 wird bis 13.10.2026 vorgelegt. Der Regierungspfad kann sich dann ändern.

Befund: Das nominale Wachstum der Regierung (2,9 bis 3,3 %) liegt nahe an der Standardannahme von 3,0 %. Die einheitliche Annahme verzerrt hier, anders als bei Polen, kaum.

## 3. Steuern 2026 (Agent, nicht selbst geprüft)

| Größe | Wert | Quelle | Status |
|---|---|---|---|
| Einkommensteuer | 25 % bis 16.720 €; 40 % bis 29.510 €; 45 % bis 51.070 €; 50 % darüber | pv.be, Dexxter | Sekundärquelle; FOD Financiën nicht erreichbar |
| Steuerfreier Betrag | 11.550 € (nach Reformgesetz 15.07.2026); Angaben widersprüchlich (10.910 / 11.180 / 11.550 €) | Baker Tilly u. a. | Sekundärquelle |
| Gemeindezuschlag (Durchschnitt) | nicht gefunden | — | Lücke |
| Umsatzsteuer | 21 % / 12 % / 6 %; Hotels seit 01.03.2026 12 % | vatcalc | Sekundärquelle |

Vergleichspunkt für 28:28: Der Spitzensatz der Einkommensteuer liegt bei 50 %, zuzüglich Gemeindezuschlag. Das Konzept setzt 28 %.

## 4. Gemeinden

565 Gemeinden am 01.01.2026: Flandern 285 (nach den Fusionen 2025), Wallonien 261, Brüssel 19. Die Gesamtzahl ist aus den regionalen Angaben summiert (Agent, amtliche Regionalseiten). belgium.be nennt noch 581 (veraltet).

## 5. Wohnort (Ergebnis nach Standard 2.6, Euro 2028, nominal)

Preisniveau 118,7 (Repository, Eurostat). Dividendenboden 582,39 € je Erwachsenem und Monat, ausgezahlt (V3a) 642,79 €. Tarifstufen 13.977 / 27.955 / 41.932 / 55.909 €.

## 6. Lücken

1. Schuldenquote der Regierung 2027/2028 nicht gefunden; Pfad C entfällt.
2. Planbureau, Hoher Finanzrat, FOD Financiën: Seiten nicht erreichbar.
3. Steuerparameter nur aus Sekundärquellen; Gemeindezuschlag fehlt.
