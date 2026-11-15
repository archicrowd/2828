# Option C: Unternehmensbasis – Befund, Beschlüsse E2 bis E4, offen E1 und E5

Initiative 28:28 · 15. November 2026 · Modellstand v4.90 · Rechnung: `modell/unternehmensbasis.py` (+ `.toml`) → `daten/aggregate/unternehmensbasis.json`
Status: **interne Prüfrechnung.** Die Rechnungen erscheinen bis zum Abschluss von Weg C nicht auf Webseite, Forschungsseite oder im
Working Paper (Beschluss 15.11.2026). Die beschlossenen **Regeln** stehen seit v4.90 in Konzept, Forschungsseite und Working Paper; Zahlen
dazu nicht. Das Repository ist öffentlich.

## 1 Befund

- **Modellbasis:** Die Unternehmensposition des Modells (4,42 % BIP) setzt eine Gewinnbasis von 13,4 % des BIP voraus (rund 607 Mrd. €, 2025).
- **Heutige Basis:** Die heute besteuerte Basis der Kapitalgesellschaften beträgt 6,0 % des BIP (260 bis 283 Mrd. €).
- **Mit den Hebeln:** Mit Kundenort, Plattformen, Gewinnverlagerung und der beschlossenen Verlustverrechnung erreicht die Position
  **2,37 % des BIP** (2,08 bis 2,80). Es fehlen rund **2 Punkte**.
- **Gewinn aus dem Abschluss (E1 b):**
  - Er verbreitert die Basis nicht. Bundesbank 2023: Gewinn der Kapitalgesellschaften vor Steuern ohne Erträge aus Beteiligungen,
    mit Banken, rund 270 Mrd. €; die steuerliche Basis lag bei rund 306 Mrd. € (Verhältnis 0,88; Versicherer fehlen).
  - Konzerne mit Sitz in Deutschland weisen 2023 weltweit 271 Mrd. € Gewinn aus, davon 103 Mrd. € im Inland (Steuer dort 31 %).
- **Größenordnung des Modellwerts:** 13 % des BIP gibt es nur als volkswirtschaftlicher Unternehmensgewinn (15,4 % des BIP, mit
  Personengesellschaften, öffentlichen Unternehmen und Beteiligungserträgen). Weg C kann die Lücke daher nicht schließen.
- **Alle vier Positionen zusammen (B-1):** −3,10 % BIP (−2,45 bis −3,59). Die Dividende 2028 läge rechnerisch bei rund 211 € statt 364 €
  (mit Kinderanteil).

Korrektur 89 (v4.88): Die Belegrechnung v4.87 hatte die ganze Gewerbesteuer den Kapitalgesellschaften zugerechnet. Die Lücke der
Unternehmensposition steigt dadurch von −1,01 auf −2,05 Punkte.

## 2 Zahlen (Basis 2025, Mrd. €; % BIP 2025 = 4.531,7 Mrd. €)

| Größe | vorsichtig | mittel | hoch | Quelle |
|---|---|---|---|---|
| Kapitalgesellschaften heute | 260 (aus KSt) | 272 | 283 (aus Gewerbesteuer) | Kasse 2025; Messbetragsanteil 57 % (2018) |
| H1 Kundenort und Plattformen | +21 | +37 | +70 | R6 (OECD-Länderberichte), `plattformen33.json` |
| H2 Gewinnverlagerung (ohne Überschneidung mit H1) | 0 | +10 | +19 | ifo 2021: 5,7 Mrd. € Steuerausfall je Jahr |
| H3 Verlustverrechnung 50 % über 1 Mio. € (beschlossen) | +4 | +8 | +12 | 10/20/30 % weniger genutzter Verlustvortrag (Annahme) |
| **Basis zusammen** | **285** | **326** | **385** | |
| **Unternehmen bei 33 %** | **2,08 %** | **2,37 %** | **2,80 %** | Modell 4,42 % |
| E4 Befristung der Altverluste, 2033 (einmalig, % BIP) | 0 | +0,08 | +0,10 | Summe 2028–2045 rund 0 |

## 3 Beschlüsse vom 15.11.2026

**E3 Einmalbesteuerung: höchstens ein Drittel je Einkommensart.**
- Unternehmensgewinne, Kapitalerträge, Arbeitseinkommen und Erbschaften werden je für sich mit höchstens einem Drittel besteuert.
- Die Kapitalerträge bleiben in der Deckung.
- Regeltext (umgesetzt in v4.90): „Kein Satz liegt über einem Drittel: Einkommen, Kapitalerträge, Unternehmensgewinne und Erbschaften
  werden je für sich mit höchstens einem Drittel besteuert.“
- Kursgewinne: Klärung zurückgestellt; das Konzept führt sie als Kapitalertrag mit höchstens 33 %.

**E2 Rechtsformen: Personengesellschaften bleiben in der Position Einkommen.**
- Der Gewinn wird bei den Inhabern besteuert, höchstens mit 33 %, wie bei Kapitalgesellschaften.
- Keine Umbuchung, die Summe bleibt unverändert.

**E4 Verluste.**
- Verlustvorträge, die Ende 2027 bestehen, sind fünf Jahre nutzbar (2028–2032) und verfallen danach.
- Neue Verluste sind unbefristet vortragbar.
- Verrechnung: bis 1 Mio. € voll, darüber höchstens mit der Hälfte des Gewinns (heute 70 %, ab 2028 60 %).
- Vorbilder:
  - Frist fünf Jahre: neun EU-Staaten.
  - Verrechnung mit 50 %: Frankreich, Niederlande, Vereinigtes Königreich (Tax Foundation 2024).
- Recht: Das BVerfG hat die Mindestbesteuerung auch mit Definitiveffekt bestätigt (2 BvL 19/14, 23.7.2025) und dem Gesetzgeber beim
  Systemwechsel Spielraum zuerkannt (Rn. 79). Ein rein fiskalischer Zweck trägt nicht (Rn. 81); die Regel ist mit dem Systemwechsel zu
  begründen. Den Teil zum Vertrauensschutz habe ich nicht gelesen; eine rechtliche Prüfung steht aus.
- Wirkung: dauerhaft +0,06 bis +0,09 % BIP. Die Befristung bringt einmalig wenig (2033 bis +0,10) und zieht einen klaren Schnitt.
- Beschrieben in Konzept (Regel „Verluste“) und Working Paper (v4.90).

## 4 Offen

**E1 Bemessungsgrundlage.** Empfehlung: der konsolidierte Konzerngewinn aus dem Abschluss, nach Kundenumsatz verteilt.
- Das entspricht dem Wortlaut der Konzeptregel.
- Ausschüttungen innerhalb des Konzerns (heute § 8b KStG) und Verluste im Konzern gleichen sich darin von selbst aus.
- Aufkommen: rund wie heute (Abschnitt 1). Die Entscheidung ist eine Frage der Einfachheit, nicht der Deckung.

**E5 Was die Lücke trägt – jetzt die eigentliche Entscheidung.** Rund 2 Punkte der Unternehmensposition und gut 1 Punkt der übrigen drei
Positionen lassen sich nicht belegen.

| Option | Wirkung |
|---|---|
| A Belegte Werte in die Deckung | Dividende 2028 rund 211 € statt 364 € (mittel; 186 bis 243 €). Im Stand C ist die Dividende der Rest; die übrigen Bausteine bleiben |
| B Unternehmenssatz über 33 % | widerspricht E3 |
| C Weitere Einnahmen (Bausteine aus dem Kernmodell, z. B. Bodenwertabgabe, Abbau klimaschädlicher Subventionen) | jeweils eigene Prüfung |
| D Ausgaben senken (Netz, Gemeinden, Fonds) | berührt beschlossene Bausteine |

Empfehlung: A. Wer weitere Einnahmen will (C), rechnet sie einzeln und belegt.

## 5 Quellen (abgerufen 15.11.2026)

- Destatis, Körperschaftsteuerstatistik 2017, Fachserie 14 Reihe 7.2. [PDF](https://www.statistischebibliothek.de/mir/servlets/MCRFileNodeServlet/DEHeft_derivate_00072070/2140720177004.pdf)
- Destatis, Gewerbesteuerstatistik 2018, Fachserie 14 Reihe 10.2. [PDF](https://www.statistischebibliothek.de/mir/servlets/MCRFileNodeServlet/DEHeft_derivate_00073476/2141020187004.pdf)
- Destatis, VGR Fachserie 18 Reihe 1.4 (August 2024). [PDF](https://www.statistischebibliothek.de/mir/servlets/MCRFileNodeServlet/DEHeft_derivate_00098412/5812105239004_August2024.pdf)
- Destatis, Wirtschaftliche Tätigkeit deutscher multinationaler Unternehmen 2023 (länderbezogene Berichte). [Destatis](https://destatis.de/EN/Themes/Government/Taxes/Business-Tax/maps-multinat-enterprises.html)
- Deutsche Bundesbank, Ertragslage und Finanzierungsverhältnisse deutscher Unternehmen 2024, Monatsbericht Dezember 2025. [Bundesbank](https://publikationen.bundesbank.de/content/972382)
- Deutsche Bundesbank, Jahresabschlussstatistik, hochgerechnete Angaben (Tab. III/2; maschinell aus dem PDF gelesen, an der Quelle zu prüfen). [PDF](https://bundesbank.de/resource/blob/827826/5339ba185ff3e7ba37087b692a65ef74/472B63F073F071307366337C94F8C870/1-0-jahresabschlussstatistik-hochgerechnete-angaben-data.pdf)
- Deutsche Bundesbank, Ertragslage der deutschen Kreditinstitute 2024, Monatsbericht September 2025. [Bundesbank](https://publikationen.bundesbank.de/content/965140)
- Eurostat, nasa_10_nf_tr, DE 2024. [API](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nasa_10_nf_tr?format=JSON&geo=DE&time=2024&unit=CP_MEUR&na_item=B4N)
- sozialpolitik-aktuell, Tab. II.8, nach BMF-Datensammlung 2026 (Sekundärquelle). [PDF](https://www.sozialpolitik-aktuell.de/files/sozialpolitik-aktuell/_Politikfelder/Finanzierung/Datensammlung/PDF-Dateien/tabII8.pdf)
- ifo Institut (2021), ifo Schnelldienst 74(1). [ifo](https://ifo.de/en/node/61139)
- Tax Foundation (2024, aktualisiert 13.11.2025): Net Operating Loss Provisions in Europe. [Tax Foundation](https://taxfoundation.org/data/all/eu/net-operating-loss-tax-europe-2024/)
- BVerfG, Beschluss vom 23.7.2025, 2 BvL 19/14. [BVerfG](https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/DE/2025/07/ls20250723_2bvl001914.html)
- EuGH, C-319/02 (Manninen), 7.9.2004. [Urteil](https://lexetius.com/2004,1970)
- Wissenschaftliche Dienste des Bundestags, WD 4 - 3000 - 085/24. [PDF](https://bundestag.de/resource/blob/1038786/7028aaf9b974b2904f52d4de729c04d0/WD-4-085-24-pdf.pdf)
