# Option C: Unternehmensbasis verbreitern – Befund und Entscheidungen E1 bis E5

Initiative 28:28 · 15. November 2026 · Modellstand v4.89 (Stand der Entscheidungen: E4 beschlossen, E3 zur Entscheidung) · Rechnung: `modell/unternehmensbasis.py` (+ `.toml`) → `daten/aggregate/unternehmensbasis.json`
Status: **interne Prüfrechnung.** Beschluss der Initiative vom 15.11.2026: Weg C verfolgen, Rechnungen bis zur Entscheidung nicht auf Webseite,
Forschungsseite oder im Working Paper. Hinweis: Das Repository ist öffentlich; Logbuch und diese Vorlage sind dort einsehbar.

## 1 Befund

**Die Unternehmensposition des Modells (4,42 % BIP) setzt eine Gewinnbasis von 13,4 % des BIP voraus (rund 607 Mrd. € im Jahr 2025).**
- Die heute besteuerte Basis der Kapitalgesellschaften beträgt 6,0 % des BIP (260 bis 283 Mrd. €), aus Körperschaft- und Gewerbesteuer
  2025 zurückgerechnet.
- Die Modellbasis ist damit gut doppelt so groß.
- Mit allen Hebeln, die sich belegen lassen (Kundenort, Plattformen, Gewinnverlagerung, strengere Verlustverrechnung), erreicht die Position
  2,4 % des BIP (Spanne 2,1 bis 2,8). Es bleiben rund **2 Punkte des BIP** offen.
- Größenordnungen wie 13 % des BIP zeigt nur die Volkswirtschaftliche Gesamtrechnung:
  - Unternehmensgewinn der Kapitalgesellschaften 2024: 15,4 % des BIP.
  - Betriebsüberschuss 2024: 11,0 % des BIP.
  - Beide enthalten Personengesellschaften, öffentliche Unternehmen und Dividenden zwischen Unternehmen. Eine Steuerbasis sind sie nicht.

**Korrektur 89 (eigener Fehler in v4.87).**
- **Fehler:** v4.87 hatte das Aufkommen der Kapitalgesellschaften in der VGR (125,1 Mrd. €) durch 30 % geteilt (Basis 417 Mrd. €). Diese
  Größe enthält aber die ganze Gewerbesteuer, auch die der Personengesellschaften.
- **Grund:** Personengesellschaften zählen in der VGR als Quasi-Kapitalgesellschaften. Das ist eigene Kenntnis und an der Quelle zu prüfen;
  die Summen stützen es: 2023 KSt 45,9 + Soli darauf rund 2,5 + Gewerbesteuer 75,7 Mrd. € gegen 128,4 Mrd. € in der VGR.
- **Wirkung:** Die Lücke der Unternehmensposition steigt von −1,01 auf −2,05 Punkte. Die Lücke aller vier Positionen steigt von −2,06 auf
  **−3,10 % BIP** (Spanne −2,45 bis −3,59).
- **Folge für die Dividende:** Die Dividende 2028 läge rechnerisch bei rund 211 € statt 364 € (mit Kinderanteil).

## 2 Zahlen (Basis 2025, Mrd. €; % BIP 2025 = 4.531,7 Mrd. €)

| Größe | vorsichtig | mittel | hoch | Quelle |
|---|---|---|---|---|
| Kapitalgesellschaften heute | 260 (aus KSt) | 272 | 283 (aus Gewerbesteuer) | Kasse 2025; Messbetragsanteil 57 % (2018) |
| H1 Kundenort und Plattformen | +21 | +37 | +70 | R6 (OECD-Länderberichte), `plattformen33.json` |
| H2 Gewinnverlagerung (ohne Überschneidung mit H1) | 0 | +10 | +19 | ifo 2021: 5,7 Mrd. € Steuerausfall je Jahr |
| H3 dauerhaft strengere Verlustverrechnung (seit v4.89 0: nicht beschlossen) | 0 | 0 | 0 | bis v4.88: +4 / +8 / +12 |
| **Basis zusammen** | **281** | **318** | **372** | |
| **Unternehmen bei 33 %** | **2,05 %** | **2,32 %** | **2,71 %** | Modell 4,42 % |
| H4 Personengesellschaften (Umbuchung aus Einkommen) | +0,98 | +0,98 | +0,98 | Gewerbeertrag rund 134 Mrd. €; Summe unverändert |
| H5 Einmalbesteuerung der Dividenden (Kapitalerträge) | −0,78 | −0,58 | −0,39 | Dividendenanteil 57 % der Kapitalertragsteuern |

**Nicht beziffert, weil keine Zahl vorliegt:**
- Steuerfreie Veräußerungsgewinne nach § 8b Abs. 2 KStG: Laut Wissenschaftlichem Dienst des Bundestags ist zur Höhe „keine Aussage" möglich.
- Abschreibungen und Rückstellungen: Unterschied zwischen steuerlicher und wirtschaftlicher Bewertung.
- Steuerbefreite und öffentliche Unternehmen.

## 3 Entscheidungen

**E1 Bemessungsgrundlage.**
- **(a) Heutiger steuerlicher Gewinn mit gezielter Verbreiterung (H1 bis H3):** belegbar, rund 2,4 % des BIP.
- **(b) Konsolidierter Konzerngewinn aus dem Abschluss, nach Kundenumsatz verteilt:**
  - Das ist der Wortlaut der Konzeptregel („der Gewinn des Konzerns wird nach diesem Umsatzanteil auf die Staaten verteilt").
  - Gewinnausschüttungen innerhalb des Konzerns und Verluste im Konzern gleichen sich dabei von selbst aus.
  - Wie groß diese Basis ist, ist noch nicht belegt. Nächster Schritt: Daten der globalen Mindeststeuer (Säule 2) und der EU-Vorschläge
    (BEFIT) suchen.
- **(c) Basis nahe der VGR (Unternehmensgewinn):** Nur damit wäre der Modellwert erreichbar. Diese Basis besteuert aber auch
  Personengesellschaften, öffentliche Unternehmen und Gewinne aus dem Ausland. Sie ist eher eine neue Steuer als eine Verbreiterung.

**E2 Rechtsformen.**
- Sollen Personengesellschaften in die Unternehmensposition, also eine Besteuerung unabhängig von der Rechtsform? Das bucht rund 1 Punkt aus
  der Position Einkommen um; die Summe bleibt gleich.
- Zu klären ist dann, wie Gewinne beim Inhaber behandelt werden (Freistellung oder Anrechnung) und wie Einzelunternehmen behandelt werden.
- Die Position Einkommen ist auf die gesamte Einkommensteuer geeicht (Kernmodell: 284 Mrd. €), enthält die Gewinne der Personengesellschaften
  also schon. Prüfpunkt offen.

**E3 Einmalbesteuerung – die Entscheidung mit der größten Tragweite (zur Entscheidung, Stand v4.89).**

| Option | Wirkung | Aufkommen (Kapitalerträge, % BIP; mittel) | Bewertung |
|---|---|---|---|
| (a) Dividende beim Empfänger frei, die Unternehmensteuer ist abgeltend | jeder ausgeschüttete Euro trägt genau 33 % | −0,58 (−0,39 bis −0,78) ≈ −30 € je Erwachsenem und Monat 2028 | hält die Regel wörtlich, einfach; Vorbild: Estland und Lettland besteuern Gewinne bei der Ausschüttung, nicht beim Empfänger (eigene Kenntnis, an der Quelle zu prüfen). Dividenden aus Staaten mit niedriger Steuer außerhalb der Gemeinschaft nur frei, wenn dort mindestens 15 % gezahlt wurden (globale Mindeststeuer), sonst 33 % mit Anrechnung |
| (b) Anrechnung der Unternehmensteuer auf die Steuer des Empfängers (wie 1977–2000) | ausgeschüttete Gewinne tragen den persönlichen Satz (0 bis 33 %) | mehr als −0,58: Empfänger unter 33 % erhalten Erstattungen | progressiv, aber aufwendig; muss nach EuGH (Manninen, C-319/02, 2004) auch für ausländische Körperschaftsteuer gelten – einer der Gründe für die Abschaffung 2001 |
| (c) Regeltext präzisieren: „ein Drittel je Steuer“ | ausgeschüttete Gewinne tragen 55 % (heute rund 48 %) | 0 | Aufkommen bleibt, das Versprechen wird schwächer und muss offen gesagt werden |

Folgefrage zu (a): Kursgewinne aus Aktien enthalten einbehaltene Gewinne, die schon mit 33 % belastet sind. Ob sie beim Empfänger
steuerpflichtig bleiben, ist offen (Anteil an der Abgeltungsteuer nicht belegt).

Vorher stand hier:
- **Was die Regel verspricht:** „Kein Euro wird mit mehr als einem Drittel besteuert – Einkommen, Kapitalerträge, Unternehmensgewinne".
- **Was die Deckung rechnet:** 33 % beim Unternehmen und noch einmal 33 % auf die Dividende. Ein ausgeschütteter Gewinn trägt damit
  1 − 0,67 × 0,67 = **55 %**. Heute sind es rund 48 %: 29,9 % + 26,375 % × 70,1 %.
- **Die Optionen:**
  - **(a) Dividende beim Empfänger frei:** Die Regel ist eingehalten. Die Kapitalerträge sinken um 0,4 bis 0,8 Punkte.
  - **(b) Anrechnung der Unternehmensteuer beim Empfänger:** Für Inländer wirkt das wie (a). Der Unterschied liegt bei Anteilseignern im
    Ausland.
  - **(c) Regel präzisieren** („je Steuer ein Drittel"): Das Aufkommen bleibt, das Versprechen wird schwächer und ist offen zu kommunizieren.
- Diese Frage betrifft den Kern der Erzählung und sollte vor E1 entschieden werden.

**E4 Verluste – beschlossen am 15.11.2026: beim Systemwechsel befristen.** Regel (Vorschlag zur Bestätigung):
- **Altverluste:** Verlustvorträge, die Ende 2027 bestehen, sind fünf Jahre nutzbar (2028–2032), unter der heutigen Mindestbesteuerung. Danach
  verfallen sie.
- **Neue Verluste:** unbefristet vortragbar, mit derselben Mindestbesteuerung.
- **Vorbild:** Die Frist von fünf Jahren gilt in neun EU-Staaten (Tax Foundation 2024).
- **Verfassung:** Das BVerfG hat die Mindestbesteuerung auch mit Definitiveffekt bestätigt (2 BvL 19/14, 23.7.2025) und dem Gesetzgeber beim
  Systemwechsel Spielraum zuerkannt (Rn. 79). Ein rein fiskalischer Zweck rechtfertigt aber keine Abweichung (Rn. 81). Die Befristung ist
  deshalb mit dem Systemwechsel zu begründen, nicht mit dem Aufkommen. Die Teile zum Vertrauensschutz sind nicht gelesen; eine rechtliche
  Prüfung steht aus.

Ergebnis der Rechnung (% BIP je Jahr, mittel):
- 2028–2032: −0,04, weil Altverluste vorgezogen genutzt werden.
- 2033: +0,10, 2035: +0,03, ab 2038: 0.
- Summe 2028–2045 rund 0 (Spanne −0,4 bis +0,5 Punkt-Jahre).

**Die Befristung schließt die Lücke nicht.** Sie zieht einen klaren Schnitt, statt die neue Basis über Jahrzehnte mit Altverlusten zu belasten.
- Der Bestand ist groß: 667 Mrd. € (2017).
- Davon liegen 400 Mrd. € bei Unternehmen ohne Gewinn und werden zum großen Teil nie genutzt.
- Dauerhaft mehr brächte nur eine strengere Verrechnung auch neuer Verluste. Die ist nicht beschlossen.

Vorher stand hier:
- Der Bestand an Verlustvorträgen betrug Ende 2017 rund 701 Mrd. €.
- Zu entscheiden ist, ob die Vorträge beim Systemwechsel übernommen, gekappt oder zeitlich begrenzt werden. Dabei sind Vertrauensschutz und
  Rechtsprechung zu beachten; eine rechtliche Prüfung steht aus.
- Für den laufenden Betrieb gilt die Mindestbesteuerung (H3).

**E5 Was eine verbleibende Lücke trägt.** Im Stand C ist die Dividende der Rest. Bleibt die Lücke, sinkt die Dividende. Andere Wege wären
eine andere Position oder ein anderer Satz; beides berührt das Drittel.

## 4 Vorschlag zum Vorgehen

1. E4 ist beschlossen (Befristung, Regel oben). Als Nächstes E3 entscheiden (Regeltext), dann E2.
2. Für E1 (b) Daten suchen: Säule 2, BEFIT, Konzernabschlüsse.
3. Erst danach die Deckung neu rechnen und Webseite, Konzept und Working Paper anpassen.

## 5 Quellen (abgerufen 15.11.2026)

- Destatis, Körperschaftsteuerstatistik 2017, Fachserie 14 Reihe 7.2. [PDF](https://www.statistischebibliothek.de/mir/servlets/MCRFileNodeServlet/DEHeft_derivate_00072070/2140720177004.pdf)
- Destatis, Gewerbesteuerstatistik 2018, Fachserie 14 Reihe 10.2. [PDF](https://www.statistischebibliothek.de/mir/servlets/MCRFileNodeServlet/DEHeft_derivate_00073476/2141020187004.pdf)
- Destatis, VGR Fachserie 18 Reihe 1.4 (August 2024), Einkommensteuern nach Sektoren 2023. [PDF](https://www.statistischebibliothek.de/mir/servlets/MCRFileNodeServlet/DEHeft_derivate_00098412/5812105239004_August2024.pdf)
- Eurostat, nasa_10_nf_tr, DE 2024 (B4N, B2A3N; vorläufig). [API](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nasa_10_nf_tr?format=JSON&geo=DE&time=2024&unit=CP_MEUR&na_item=B4N)
- sozialpolitik-aktuell, Tab. II.8, nach BMF-Datensammlung 2026 (Sekundärquelle; Spaltenköpfe im PDF verschoben, Jahreszuordnung aus der Reihenfolge erschlossen). [PDF](https://www.sozialpolitik-aktuell.de/files/sozialpolitik-aktuell/_Politikfelder/Finanzierung/Datensammlung/PDF-Dateien/tabII8.pdf)
- ifo Institut (2021): Gewinnverlagerung großer deutscher Unternehmen in Niedrigsteuerländer, ifo Schnelldienst 74(1), 38–42. [ifo](https://ifo.de/en/node/61139); dazu EU Tax Observatory (1,6 Mrd. € nur große deutsche Konzerne). [Observatory](https://taxobservatory.eu/?p=440)
- Tax Foundation (Mengden, 2024, aktualisiert 13.11.2025): Net Operating Loss Carryforward and Carryback Provisions in Europe. [Tax Foundation](https://taxfoundation.org/data/all/eu/net-operating-loss-tax-europe-2024/)
- BVerfG, Beschluss vom 23.7.2025, 2 BvL 19/14 (Mindestgewinnbesteuerung). [BVerfG](https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/DE/2025/07/ls20250723_2bvl001914.html)
- EuGH, Urteil vom 7.9.2004, C-319/02 (Manninen). [Urteil](https://lexetius.com/2004,1970)
- Wissenschaftliche Dienste des Bundestags, WD 4 - 3000 - 085/24 (Dezember 2024), § 8b Abs. 2 KStG. [PDF](https://bundestag.de/resource/blob/1038786/7028aaf9b974b2904f52d4de729c04d0/WD-4-085-24-pdf.pdf)
