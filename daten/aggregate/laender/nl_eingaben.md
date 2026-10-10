# Niederlande: Eingangsdaten für die Länderrechnung (Standard Fassung 1.3, Modellstand v3.27)

Stand: 10. Oktober 2026. Rechnung: `modell/laender/rechne.py`; Parameter: `modell/laender/nl.toml`; Ergebnis: `daten/aggregate/laender/nl.json`.

Recherche durch einen Rechercheagenten (WebFetch/WebSearch, 10.10.2026). Von mir selbst geprüft sind nur die Einträge mit „geprüft“. Alle übrigen sind **Agent, nicht selbst geprüft**. WebFetch liest maschinell.

## 1. Stand 2025

| Größe | Wert | Quelle | Status | Prüfung |
|---|---|---|---|---|
| Schuldenquote 2025 | 44,4 % BIP | Eurostat `gov_10dd_edpt1`, GD, S13 | amtlich, maschinell | **geprüft** (WebFetch); gleich Repository, CBS 26.03.2026, EU-Kommission |
| Schuldenquote 2025, revidiert | 44,7 % BIP (524 Mrd. €) | CBS 01.09.2026, vorläufig | amtlich, maschinell | Agent. Gleicher Schuldenstand, BIP nach unten revidiert. Nicht verwendet (Standard 1.3: Eurostat). |
| Saldo 2025 | −1,6 % BIP | CBS 26.03.2026 und 01.09.2026; Repository (Eurostat) | amtlich | Repository-Wert; CBS Agent |

## 2. Prognosen

| Quelle | Größe | 2026 | 2027 | 2028 | 2029 | Status | Prüfung |
|---|---|---|---|---|---|---|---|
| Miljoenennota 2027, Bijlage, Tabel 1.1 (15.09.2026), „gebaseerd op … MEV van het CPB“ | Saldo | −2,3 | −2,9 | −2,5 | −2,5 | amtlich, Prognose | **geprüft** (WebFetch rijksfinancien.nl) |
| dto. | Schuld | 45,6 | 46,9 | 47,4 | 48,3 | amtlich, Prognose | **geprüft** |
| dto. | BIP, Mrd. € nominal | 1.224 | 1.278 | 1.332 | 1.382 | amtlich | **geprüft** |
| dto., Tabel 3.1.2 | Nominales Wachstum | 4,6 % | 4,4 % | 4,2 % | 3,8 % | amtlich | Agent; Zuordnung zu Jahren teils erschlossen, 2027 im Text bestätigt. Gegenprobe: BIP 1.278 / 1.224 = +4,4 %, 1.332 / 1.278 = +4,2 % (passt). |
| CPB, MEV 2027 (September 2026), Tabel 2.1 | Saldo | −2,7 | −2,2 | — | — | amtlich, Prognose | Agent; CPB-Seite nicht erreichbar, PDF von einer Drittseite (Arbeitgeberverband) |
| dto. | Schuld | 46,1 | 46,7 | — | — | amtlich, Prognose | Agent |
| dto. | Wachstum real / Deflator | 1,4 / 3,1 | 1,2 / 3,1 | — | — | amtlich | Agent |
| Mittelfristiger Plan 2026–2030 (14.04.2026), Ratsempfehlung 03.07.2026 | Saldo | −2,4 | −1,5 | −1,3 | −1,2 | amtlich, Plan | Agent |
| dto. | Schuld | 46,8 | 46,5 | 46,1 | 45,6 | amtlich, Plan | Agent |
| EU-Kommission, Frühjahr 2026 | Saldo / Schuld | −2,5 / 46,9 | −1,9 / 47,0 | — | — | amtlich, Prognose | Agent |

In der Rechnung verwendet: Miljoenennota 2027. Sie ist das jüngste Regierungsdokument und deckt 2026–2028 vollständig ab.

**Widerspruch:** Für 2026 und 2027 nennt die Miljoenennota −2,3 / −2,9 %, das CPB −2,7 / −2,2 %. Beide geben an, die Haushaltspolitik der Miljoenennota einzuschließen. Die Miljoenennota beruft sich auf das CPB. Ursache nicht geklärt, am Original des CPB zu prüfen. Der Plan vom April (−1,5 / −1,3 % für 2027 / 2028) ist durch den Haushalt vom September überholt: Die Defizite liegen dort um 1,0 bis 1,4 Punkte höher.

## 3. Steuern 2026 (Agent, nicht selbst geprüft)

| Größe | Wert | Quelle | Status |
|---|---|---|---|
| Box 1 unter AOW-Alter | 35,75 % bis 38.883 €; 37,56 % bis 78.426 €; 49,50 % darüber (Stufe 1 einschließlich Volksversicherungsbeiträge) | Belastingdienst (Vorläufige Veranlagung 2026) | amtlich, maschinell |
| Box 1 ab AOW-Alter | Stufe 1: 17,85 % | dto. | amtlich, maschinell |
| Box 3 | Pauschalsystem mit Gegenbeweis; Freibetrag 59.357 €; Satz 36 %; fiktive Renditen Bank 1,28 %, übrige 6,00 %, Schulden 2,70 % (vorläufig) | Belastingdienst | amtlich, maschinell |
| Box 3, Reform | Gesetz zur tatsächlichen Rendite (36.748): Zweite Kammer 12.02.2026; Erste Kammer ohne Schlussabstimmung (Stand 05.10.2026); geplant 01.01.2028 | Erste Kammer | amtlich, offen |
| Umsatzsteuer | 21 % / 9 %; Beherbergung seit 01.01.2026 21 % | Grant Thornton (Sekundärquelle); Belastingdienst nicht erreichbar | Sekundärquelle |

Vergleichspunkt für 28:28: Der Spitzensatz in Box 1 liegt bei 49,50 %, in Box 3 bei 36 %. Das Konzept setzt 28 %.

## 4. Gemeinden

342 Gemeinden am 01.01.2026 (CBS, „Gemeentelijke indeling op 1 januari 2026“). Status: amtlich, maschinell, Agent.

## 5. Wohnort (Ergebnis nach Standard 2.6, Euro 2028, nominal)

Preisniveau 121,0 (Repository, Eurostat). Dividendenboden 593,67 € je Erwachsenem und Monat, ausgezahlt (V3a) 655,25 €. Tarifstufen 14.248 / 28.496 / 42.744 / 56.992 €.

## 6. Lücken

1. Widerspruch Miljoenennota gegen CPB beim Saldo 2026/2027.
2. CPB-Projektion für 2028 nicht gefunden (MEV reicht bis 2027).
3. Steuerparameter nicht selbst am Original geprüft.
