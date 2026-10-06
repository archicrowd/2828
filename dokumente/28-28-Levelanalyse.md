# 28:28 – Levelanalyse 25 bis 30
## Interpolation des Konzepts 25:25 PLUS, Haushaltspfad 2028–2047 und Optimierung des Einheitssatzes

*Stand: 16.09.2026 · Berechnungsgrundlage: `levelanalyse-25-30.py` (vollständig reproduzierbar) · Ergebnisse: `levelanalyse-ergebnisse.txt`, `pfad-daten.csv`*

---

## 0 | Kurzfassung

**Fragestellung.** Welcher Einheitssatz L zwischen 25 und 30 % (Einkommensteuer-Spitze, Mehrwertsteuer-Topstufe, Kapitalerträge, Unternehmen einschließlich Plattformen, Erbschaft) stellt sicher, dass (1) zu keinem Zeitpunkt eine Finanzierungslücke entsteht, (2) jährlich 1 % des BIP für flexible Investitionen verfügbar ist und (3) die Digitaldividende (DD) planmäßig aufwächst?

**Ergebnis.**

| Kriterium | Minimaler Level (proportionaler Tarif) | Minimaler Level (nur Spitze steigt) |
|---|---:|---:|
| Keine Lücke, Investitionen gesichert, DD-Stufe 2 planmäßig | **27** | 28 |
| zusätzlich DD-Stufe 3 (600/300 €, real) planmäßig | **28,5** | 30 |

**Empfehlung: 28:28 als Regelsatz mit regelgebundenem Korridor 25–30.** Der Satz 28 erfüllt die Kernbedingungen mit Sicherheitsabstand (Stresstest ohne Lücke, 100 % Investitionsquote) und liegt knapp unter dem Wert, der Stufe 3 vollständig trägt. Die Korridorregel hebt den Satz nur bei Pufferverbrauch oder DD-Verzug an und senkt ihn, wenn Überschüsse dauerhaft über Bedarf liegen. 30:30 ist fiskalisch nicht erforderlich und erzeugt im Planungsszenario strukturelle Überschüsse (≈ 1.230 Mrd. über 20 Jahre über dem Bedarf).

**Drei Einschränkungen, die das Ergebnis wesentlich bedingen:**

1. **Das Projektmodell unterstellt einen heute ausgeglichenen Haushalt.** Tatsächlich betrug das gesamtstaatliche Defizit 2025 rund 119 Mrd. € bzw. 2,7 % des BIP [2]. Schon ein strukturelles Basisdefizit von 0,5 % BIP verschiebt das Optimum auf 28,5–29,5; bei 1 % BIP auf 29,5–31. Das volle Defizit von 2,7 % BIP ist innerhalb des Korridors 25–30 **nicht** schließbar.
2. **Das frühere Projektergebnis (+2.750 Mrd. kumuliert, Break-even Jahr 2–3) beruht wesentlich auf nominal fixierten DD-Beträgen.** Bei 2 % Inflation verliert eine 600-€-Dividende in Jahr 16 rund ein Viertel ihres Realwerts; ein Teil des „Überschusses" ist damit reale Leistungskürzung. Das Planungsszenario dieser Analyse indexiert die DD deshalb.
3. **Die fünfstufige Mehrwertsteuer ist mit geltendem EU-Recht nicht vereinbar** – unabhängig vom Level. Art. 98 der Mehrwertsteuer-Systemrichtlinie erlaubt höchstens zwei ermäßigte Sätze von mindestens 5 % [4]. Zudem wäre eine Topstufe von 28 % der höchste Satz in der EU (derzeit Ungarn mit 27 % [5]).

---

## 1 | Ausgangslage und Datengrundlage

### 1.1 Übernommener Projektstand (25:25 PLUS)

Konsolidierter Haushalt, Referenzstufe 2, statisch, Mrd. € (Modellpreise, Kalibrierungsbasis „heute" = 880):

| Einnahmen | | Ausgaben | |
|---|---:|---|---:|
| ESt (Tarif 0–8–14–19–23–25, DD steuerpflichtig) | 284 | Basisausgaben nach Wegfall alter Transfers, RV-Zuschuss, Verwaltung | 596 |
| Kapitalerträge 25 % | 45 | Digitaldividende brutto (500/250 €) | 462 |
| MwSt (Stufen 5–10–15–20–25, eff. 18 %) | 350 | Zuschuss Beitragssenkung (nach BBG-Wegfall) | 60 |
| Unternehmen (KSt, Nutzungsort, GewSt-Integration) | 145 | Härtefall + Gesundheit | 35 |
| CO₂-Abgabe netto | 55 | | |
| Erbschaft 25 % / Vermögen-Mindeststeuer | 33 / 22 | | |
| Sonstige | 165 | | |
| **Summe** | **1.099** | **Summe** | **1.153** |

Statischer Saldo Projektstand: −54 Mrd. (−1,3 % Modell-BIP). Stufenlogik: Stufe 1 (400 € ab 25 J.), Stufe 2 (500/250 €), Stufe 3 (600/300 €); Kalenderplan 5/10/5 Jahre ab 2028.

### 1.2 Externe Referenzdaten (geprüft)

| Größe | Wert | Quelle | Bewertung |
|---|---|---|---|
| Steuereinnahmen Bund/Länder/Kommunen 2025 | 990,7 Mrd. € | BMF, 169. Steuerschätzung [1] | amtlich |
| Staatsdefizit 2025 | 119,1 Mrd. €, 2,7 % BIP | Destatis (vorläufig), berichtet u. a. von Ärzteblatt/vdiv [2] | amtlich, Sekundärbericht |
| Schuldenstand 2025 | 2.838 Mrd. €, 63,5 % BIP | Deutsche Bundesbank [3] | amtlich |
| Ermäßigte MwSt-Sätze | max. zwei, je ≥ 5 % | Art. 98 MwStSystRL [4] | Rechtsnorm |
| Höchster EU-Normalsatz | 27 % (Ungarn) | Weka (CH), Stand 01.01.2026 [5] | nicht amtlich, plausibel |
| Unternehmensbelastung | heute knapp 30 %, ab 2032 knapp 25 % (KSt-Senkung 15 → 10 %) | BMF-Monatsbericht 08/2025 [6], Der Betrieb [7] | amtlich / Fachpresse |
| ETI Deutschland | 0,35–0,68 (mit Abzugsmöglichkeiten) | Doerrenberg/Peichl/Siegloch, JPubE 2017 [8] | peer-reviewed |
| ETI Deutschland | 0,36 gesamt, 0,17 Ledige | Werdt 2015 (Discussion Paper) [9] | nicht begutachtet |
| Semi-Elastizität Gewinnverlagerung | ca. 0,8 | Heckemeyer/Overesch, Meta-Analyse, CJE 2017 [10] | peer-reviewed |
| Öffentlicher Investitionsbedarf | ca. 600 Mrd. über 10 Jahre (≈ 60 Mrd./Jahr) | IMK/IW 2024 [11] | Institutsstudie |
| Sondervermögen Infrastruktur/Klima | bis 500 Mrd., Bewilligung binnen 12 Jahren | Art. 143h GG [12] | Rechtsnorm |
| „Plattform-Soli" | Vorschlag 10 % auf Erlöse großer Plattformen | Weimer, u. a. beck-aktuell 08/2025 [13] | politischer Vorschlag; Gesetzgebungsstand nicht verifiziert |

**Kalibrierungshinweis.** Die Modellbasis (880 Mrd.) liegt rund 11 % unter den tatsächlichen Steuereinnahmen 2025. Die Analyse bleibt aus Vergleichbarkeitsgründen in Projektpreisen; relevant sind die Relationen. Für eine Veröffentlichung sollte das Modell auf 2028er Schätzwerte umbasiert werden.

---

## 2 | Methodik

### 2.1 Interpolation der Sätze

| Baustein | Regel für Level L | Verhaltensreaktion |
|---|---|---|
| Einkommensteuer | **Variante „prop":** gesamte Stufenleiter × L/25 (bei 28: 0–9,0–15,7–21,3–25,8–28). **Variante „oben":** nur die beiden oberen Stufen steigen | Marktinkommen reagiert auf den Grenzsteuersatz mit ETI 0,25 / 0,35 / 0,50 (Referenz/Robust/Stress). Werte liegen unter den deutschen Schätzungen, weil das Konzept Abzüge abschafft – laut [8] ein wesentlicher Reaktionskanal. |
| Mehrwertsteuer | Unterste Stufe bleibt 5 %, Spitze = L, linear dazwischen. Effektivsatz: 18,0 → 19,95 (28) → 21,25 % (30) | Bruttokonsum konstant; Mehraufkommen wird zu 85/80/70 % realisiert (Ausweichen, Steuerlücke). *Annahme ohne Einzelquelle.* |
| Kapitalerträge | Satz L | Realisationselastizität 0,7/0,8/1,0. *Annahme ohne in dieser Sitzung verifizierte Einzelquelle.* |
| Unternehmen inkl. Plattformen | Satz L auf Gewinne am Nutzungsort | Semi-Elastizität 0,8/1,0/1,5 nach [10]; Stresswert bewusst höher. Plattformanteil am Aufkommen: 12 Mrd. bei L=25 (*Annahme*). |
| Erbschaft | Satz L | Semi-Elastizität 1,0 (*Annahme*) |
| Vermögen-Mindeststeuer | bleibt 1 % | sinkt leicht, da höhere Kapitalertragsteuer mehr anrechenbar deckt |

### 2.2 Szenarien

| Parameter | Referenz (Projektannahmen) | **Robust (Planungsbasis)** | Stress |
|---|---:|---:|---:|
| Nominalwachstum Einnahmen | 3,0 % | 3,0 % | 2,0 % |
| Wachstum Basisausgaben | 2,6 % | 3,0 % | 2,0 % |
| DD-Indexierung | 0 % (nominal fix) | 2 % | 2 % |
| Verhaltensbonus ab Jahr 3 | +50 Mrd. | +20 Mrd. | 0 |
| Wachstumsabschlag je PP über 25 | 0,03 PP | 0,04 PP | 0,06 PP |
| Rezession | – | – | Jahr 6–8: Einnahmen −6/−4/−2 %, Ausgaben +20/+20 Mrd. |

Der Wachstumsabschlag wirkt voll auf die Einnahmen und zur Hälfte auf die Basisausgaben (lohn-/BIP-gekoppelter Anteil). Positive Wachstumseffekte der zusätzlichen Investitionen sind **nicht** eingerechnet (konservativ).

### 2.3 Haushaltsregeln im Modell

- **Investitions- und Stabilitätsfonds (IS-Fonds):** Jeder Primärsaldo fließt in den Fonds. Ein Stabilitätspuffer von 1 % BIP wird zuerst aufgebaut; darüber hinausgehende Mittel finanzieren flexible Investitionen bis 1 % BIP pro Jahr.
- **Lücke** = Fondsbestand negativ (Kreditbedarf).
- **DD-Automatik (verschärft gegenüber Projekt):** Eine höhere Stufe wird nur aktiviert, wenn der Haushalt sie trägt und danach noch mindestens 1 % BIP für Investitionen übrig bleibt; Fondsreserven über dem Puffer dürfen, auf 10 Jahre verteilt, angerechnet werden. Die frühere Regel (Aufstieg bei Saldo > −25 Mrd.) erlaubte Defizite und ist mit „keinesfalls Lücken" unvereinbar.

### 2.4 Zielfunktion

Gesucht ist der **niedrigste** Level, der erfüllt: keine Lücke in Robust *und* Stress; Investitionsquote ≥ 90 % (Robust) bzw. ≥ 75 % (Stress); DD-Stufe 2 höchstens ein Jahr verspätet (Robust). Zusatzkriterium „voll": Stufe 3 bis Jahr 17. Niedrigster statt höchster Level, weil jeder Prozentpunkt die Nettogewinne der Haushalte, die Wettbewerbsposition und die EU-Kompatibilität verschlechtert.

---

## 3 | Statischer Haushalt nach Level (Stufe 2, Parameter „Robust")

**Variante „prop" (gesamte Tarifleiter skaliert), Mrd. €:**

| | 25 | 26 | 27 | **28** | 29 | 30 |
|---|---:|---:|---:|---:|---:|---:|
| ESt inkl. steuerpfl. DD | 284,0 | 293,5 | 302,8 | **311,9** | 320,9 | 329,7 |
| Kapitalerträge | 45,0 | 46,3 | 47,6 | **48,8** | 50,0 | 51,1 |
| MwSt | 350,0 | 358,5 | 367,0 | **375,3** | 383,5 | 391,7 |
| Unternehmen inkl. Plattformen | 145,0 | 149,3 | 153,5 | **157,6** | 161,6 | 165,5 |
| davon Plattformen (Annahme) | 12,0 | 12,4 | 12,7 | **13,0** | 13,4 | 13,7 |
| Erbschaft | 33,0 | 34,0 | 34,9 | **35,9** | 36,8 | 37,7 |
| Vermögen-Mindeststeuer | 22,0 | 21,6 | 21,1 | **20,7** | 20,2 | 19,8 |
| CO₂ + Sonstige | 220,0 | 220,0 | 220,0 | **220,0** | 220,0 | 220,0 |
| **Einnahmen** | 1.099,0 | 1.123,1 | 1.146,8 | **1.170,1** | 1.193,0 | 1.215,5 |
| **Saldo** | −54,0 | −29,9 | −6,2 | **+17,1** | +40,0 | +62,5 |
| in % Modell-BIP | −1,29 | −0,71 | −0,15 | **+0,41** | +0,95 | +1,49 |

**Variante „oben":** Saldo −54,0 / −36,1 / −18,5 / −1,3 / +15,5 / +31,9.

**Befunde:**
- Grenzertrag je Prozentpunkt: 24,1 → 22,5 Mrd. (abnehmend durch Verhaltensreaktionen).
- **Statischer Ausgleich in Stufe 2 erst ab ca. 27,3 (prop) bzw. 28,1 (oben).**
- Plausibilitätsprüfung: Die frühere Projektschätzung für 28:28 (+67 Mrd.) liegt nahe an der hier berechneten Differenz von +71 Mrd.

---

## 4 | Dynamischer Pfad 2028–2047

### 4.1 Feste Levels (Variante „prop")

| Level | Robust: DD-Stufe 2 / 3 | Robust: Inv.-Quote | Robust: Rest über Puffer | Stress: Lückenjahre | Stress: Inv.-Quote | Stress: min. Saldo |
|---:|---|---:|---:|---:|---:|---:|
| 25 | Jahr 19 / – | 97 % | 177 | **8** | 7 % | −76 |
| 26 | Jahr 12 / – | 100 % | 241 | **3** | 48 % | −56 |
| 27 | Jahr 6 / – | 100 % | 370 | 0 | 87 % | −37 |
| **28** | **Jahr 6 / Jahr 19** | **100 %** | **602** | **0** | **100 %** | **−19** |
| 28,5 | Jahr 6 / Jahr 16 | 100 % | 463 | 0 | 100 % | −10 |
| 29 | Jahr 6 / Jahr 16 | 100 % | 723 | 0 | 100 % | −1 |
| 30 | Jahr 6 / Jahr 16 | 100 % | 1.230 | 0 | 87 %¹ | +2 |

¹ Bei 30 wird Stufe 2 im Stressfall bereits in Jahr 9 aktiviert und bindet danach Mittel.
Negative Jahressalden im Stress (Rezessionsjahre) werden bei L ≥ 27 vollständig aus dem Stabilitätspuffer gedeckt.

**Referenzszenario (Projektannahmen):** Bei jedem Level keine Lücke, Stufen planmäßig (Jahr 6 / Jahr 16), Fondsrest nach 20 Jahren 2.043 (L=25) bis 4.957 Mrd. (L=30). Unter diesen Annahmen genügt 25:25. Die Differenz zu „Robust" erklärt sich vor allem durch die nominal fixierte DD, das langsamere Ausgabenwachstum und den höheren Verhaltensbonus – also durch Annahmen, nicht durch Beobachtung.

### 4.2 Korridorregel (empfohlene Systemausgestaltung)

Start 28, Korridor 25–30, Änderung frühestens alle zwei Jahre um 0,5 PP:
**Anheben**, wenn der Stabilitätspuffer angegriffen ist oder eine DD-Stufe überfällig ist (nur außerhalb von Defizitjahren).
**Senken**, wenn der Fondsrest 2 % BIP übersteigt, die DD im Plan ist und auch Stufe 3 beim niedrigeren Satz finanzierbar bleibt.

| Szenario | Satzpfad | DD-Stufe 2 / 3 | Lücken | Inv.-Quote | Fondsrest 2047 |
|---|---|---|---:|---:|---:|
| Referenz | 28 → 25 (ab 2047) | Jahr 6 / Jahr 16 | 0 | 100 % | ≈ 2.840 |
| **Robust** | **28 durchgehend, kurz 28,5, Ende 27,5** | **Jahr 6 / Jahr 17** | **0** | **100 %** | **≈ 350** |
| Stress | 28 → 30 (ab 2041) | Jahr 14 / – | 0 | 100 % | ≈ 30 |

**Lesart:** Die Regel findet den Satz selbst. Treten die optimistischen Projektannahmen ein, führt sie zurück auf 25:25 („Steuersenkung, wenn geliefert wird"). Unter Planungsannahmen bleibt sie bei 28. Im Stressfall steigt sie auf 30 – und selbst dann verzögert sich Stufe 2 um acht Jahre, Stufe 3 wird nicht erreicht.

**Offene Flanke:** Im Robust-Pfad sinkt der Jahressaldo nach Aktivierung von Stufe 3 auf nahe null; die Investitionen werden ab etwa 2044 aus Fondsreserven gezahlt. Stufe 3 ist bei 28 also nicht dauerhaft strukturell gedeckt, sondern benötigt entweder 28,5–29 oder zusätzliches Wachstum.

---

## 5 | Optimierungsergebnis

| Bedingung | prop | oben |
|---|---:|---:|
| Kern (keine Lücke, Investitionen, Stufe 2 planmäßig) | **27** | 28 |
| Voll (zusätzlich Stufe 3 bis Jahr 17) | **28,5** | 30 |

**Sensitivität gegenüber einem bestehenden Strukturdefizit (prop):**

| Basisdefizit der Ausgangslage | Kern ab | Voll ab |
|---:|---:|---:|
| 0 % BIP (Projektannahme) | 27 | 28,5 |
| 0,5 % BIP | 28,5 | 29,5 |
| 1,0 % BIP | 29,5 | 31 |
| 2,7 % BIP (Ist 2025) | > 30 (≈ 35) | > 30 |

**Bewertung:**
- **28 ist der robuste Optimalwert** im Sinne der Zielfunktion: 1 PP Sicherheitsabstand zur Kernbedingung, Stress ohne Lücke bei voller Investitionsquote, Stufe 3 nur knapp verfehlt.
- **Die proportionale Tarifvariante ist fiskalisch effizienter** (Kern bereits bei 27), belastet aber untere und mittlere Einkommen stärker (Abschnitt 6). Die Variante „oben" benötigt rund 1 PP mehr für dasselbe Ergebnis.
- **30:30 ist unter den Projektannahmen überdimensioniert** und nur dann begründet, wenn ein strukturelles Basisdefizit von rund 1 % BIP mitfinanziert werden soll.
- **Das tatsächliche Staatsdefizit 2025 ist mit einem Level ≤ 30 nicht zu schließen.** Soll „keine Lücke" gegenüber dem Ist-Haushalt gelten, sind zusätzlich ausgabenseitige Maßnahmen oder eine klare Abgrenzung (z. B. kreditfinanzierte Verteidigungs- und Sondervermögensausgaben außerhalb der Reformbilanz) erforderlich.

---

## 6 | Mikroebene (Stufe 2, verfügbares Einkommen nach MwSt-Anpassung gegenüber L=25, €/Jahr)

**Variante „prop":**

| Profil | heute | 25 | 28 | 30 | Δ 28–25 | Δ 30–25 |
|---|---:|---:|---:|---:|---:|---:|
| Tom, 28.000 € | 20.108 | 27.631 | 27.034 | 26.646 | −597 | −985 |
| Sarah, 42.000 € | 28.098 | 37.236 | 36.247 | 35.603 | −989 | −1.633 |
| Klaus, 55.000 € | 35.138 | 45.637 | 44.228 | 43.310 | −1.409 | −2.327 |
| Jonas, 80.000 € | 48.586 | 60.933 | 58.708 | 57.253 | −2.225 | −3.680 |
| Dr. Weber, 150.000 € | 85.795 | 103.260 | 98.724 | 95.749 | −4.536 | −7.511 |
| Familie Müller, 63.000 €, 2 Kinder | 45.409 | 56.634 | 54.955 | 53.859 | −1.679 | −2.775 |
| Anna, alleinerziehend, 28.000 €, 1 Kind | 23.168 | 30.631 | 29.999 | 29.588 | −632 | −1.043 |

**Variante „oben" (Δ 28–25):** Tom −324, Sarah −436, Klaus −624, Jonas −1.327, Dr. Weber −3.635, Familie Müller −793, Anna −359.

**Befunde:**
- Der Nettogewinn gegenüber heute bleibt bei 28 in allen Profilen hoch (z. B. Sarah +8.150 statt +9.140 €, Rückgang ca. 11 %; Dr. Weber +12.930 statt +17.470 €, Rückgang ca. 26 %). Die Anhebung wirkt damit progressiv und entschärft die im Projekt festgestellte Verteilungsschwäche (absolute Hauptgewinner oben).
- Die Tabelle enthält die MwSt-Mehrbelastung **nur relativ zu L=25**. Gegenüber dem heutigen Effektivsatz (Projektannahme ca. 16,5 %) kommt bei 28 rechnerisch eine weitere Belastung von etwa 2,5 % des Bruttokonsums hinzu (Sarah: grob −750 €/Jahr). Diese Zahl ist eine Überschlagsrechnung.
- Grenzen: Partner ohne Einkommen, Kinder-DD-Besteuerung und Sozialabgaben-Details sind wie im Projekt vereinfacht.

---

## 7 | Kritische Würdigung

### 7.1 Methodische Grenzen
1. **Kein Gleichgewichtsmodell.** Die Rechnung ist ein kalibriertes Buchhaltungsmodell mit Elastizitäten. Arbeitsangebot, Preise, Zinsen und Kapitalbewegungen werden nicht simultan bestimmt.
2. **Grobe Einkommensverteilung.** Sieben Gruppen, die oberste mit Durchschnitt 300.000 €. Die Konzentration am oberen Rand ist damit nur näherungsweise erfasst.
3. **Mehrere Parameter ohne Einzelquelle** (MwSt-Konsumgewichte, Realisationselastizität, Plattformanteil, Erbschaftsreaktion). Sie sind im Skript als Annahmen gekennzeichnet und sollten vor Veröffentlichung belegt oder in Bandbreiten gezeigt werden.
4. **Wachstumsabschlag.** Die Größenordnung (0,03–0,06 PP pro PP Level) ist eine Setzung. Die Literatur zu Steuermultiplikatoren streut stark; zugleich fehlen die positiven Effekte zusätzlicher öffentlicher Investitionen. Beides kann sich teilweise ausgleichen.
5. **Stufe 1 ist im Modell sehr günstig**, weil der gesamte Einnahmenumbau (inkl. Kappung der ESt auf L) sofort wirkt, während die DD erst 400 € beträgt. Ob diese Sequenz politisch umsetzbar ist, ist offen.

### 7.2 Rechtliche und institutionelle Punkte
1. **EU-Mehrwertsteuerrecht:** Die Stufenleiter umfasst bei jedem Level vier ermäßigte Sätze ≥ 5 % unterhalb der Topstufe; zulässig sind zwei [4]. Denkbare Umgehungen: (a) EU-Rechtsänderung, (b) MwSt mit Normalsatz und zwei ermäßigten Sätzen plus nationale Lenkungsabgaben (Verbrauchsteuern) für die oberen Stufen. Beides verändert die Architektur. In den gesichteten Projektauszügen habe ich dazu keine Lösung gefunden – bitte prüfen.
2. **Satzhöhe MwSt:** 28 % läge 1 PP, 30 % 3 PP über dem derzeit höchsten EU-Normalsatz [5]. Eine Deckelung der MwSt-Topstufe auf 27 % bei L=28 kostet im Modell nur rund 4 Mrd. und wäre ein pragmatischer Kompromiss.
3. **Unternehmen:** Die derzeitige Gesamtbelastung liegt knapp unter 30 %, gesetzlich ist eine Absenkung auf knapp 25 % bis 2032 beschlossen [6][7]. 28 % bedeutet gegenüber diesem Pfad eine Erhöhung um rund 3 PP, gegenüber heute eine leichte Senkung. 30 % entspräche dem heutigen Niveau.
4. **Plattformen:** Eine Gewinnbesteuerung am Nutzungsort kollidiert mit bestehenden Doppelbesteuerungsabkommen, solange keine multilaterale Lösung gilt. Der diskutierte „Plattform-Soli" setzt am Umsatz an (10 %) und ist mit einem Gewinnsteuersatz von 28 % nicht direkt vergleichbar; innerhalb der Regierung wurden Bedenken wegen des Handelskonflikts mit den USA geäußert [13]. Den aktuellen Gesetzgebungsstand konnte ich nicht verifizieren.
5. **Verhältnis zum Sondervermögen:** Die 500 Mrd. nach Art. 143h GG sind kreditfinanziert und an Zusätzlichkeit gebunden [12]. Der IS-Fonds dieses Modells wäre steuerfinanziert und flexibel – beides kann sich ergänzen, darf aber in der Bilanz nicht doppelt gezählt werden.

### 7.3 Korrektur am bisherigen Projektergebnis
Die auf der Homepage genannten Werte (Break-even Jahr 2–3, +2.750 Mrd. kumuliert) sind unter den dort genannten Annahmen rechnerisch nachvollziehbar, aber **nicht robust**: Mit indexierter Dividende, gleichem Wachstum von Einnahmen und Ausgaben und halbiertem Verhaltensbonus verzögert sich bei 25:25 Stufe 2 um 13 Jahre, und ein Rezessionsschock erzeugt acht Lückenjahre. Für die öffentliche Kommunikation empfiehlt sich, das Robust-Szenario als Hauptszenario zu führen.

---

## 8 | Konsequenzen für das Konzept (Vorschlag 28:28)

| # | Änderung gegenüber 25:25 PLUS | Begründung |
|---|---|---|
| 1 | **Regelsatz 28 %** für ESt-Spitze, Kapitalerträge, Unternehmen inkl. Plattformen, Erbschaft; MwSt-Topstufe 28 % (alternativ 27 %) | Optimum der Zielfunktion mit Sicherheitsabstand |
| 2 | **Tarifleiter proportional:** 0 – 9 – 16 – 21 – 26 – 28 % (gerundet; Grenzen 12/25/40/55/70 T€) | fiskalisch effizienter; Belastung bleibt progressiv |
| 3 | **Satzkorridor 25–30 mit gesetzlicher Automatik** (±0,5 PP, Mindestabstand 2 Jahre) | ersetzt ad-hoc-Steuerpolitik; führt bei Übererfüllung zurück zu 25 |
| 4 | **IS-Fonds:** Puffer 1 % BIP, flexible Investitionen bis 1 % BIP pro Jahr | erfüllt „Geld für flexible Investitionen" und „keine Lücken" zugleich |
| 5 | **DD-Automatik verschärfen:** Aufstieg nur, wenn danach 1 % BIP Investitionsspielraum bleibt | alte Regel (Saldo > −25 Mrd.) ließ Defizite zu |
| 6 | **DD real sichern (Preisindexierung)** und das offen kommunizieren | nominale Fixierung erzeugte scheinbare Überschüsse |
| 7 | **MwSt-Architektur EU-konform umbauen** | Art. 98 MwStSystRL |
| 8 | **Abgrenzung Reformbilanz vs. Ist-Defizit** gesetzlich festlegen | Level ≤ 30 kann das Ist-Defizit nicht mitschließen |

Vorgeschlagener Claim-Baustein: *„28 für alle – und 25, sobald es trägt."*

---

## Quellen

1. Bundesministerium der Finanzen: Ergebnisse der 169. Steuerschätzung, Pressemitteilung 22/2025, 23.10.2025. https://www.bundesfinanzministerium.de/Content/DE/Pressemitteilungen/Finanzpolitik/2025/10/2025-10-23-ergebnisse-der-169-steuerschaetzung.html
2. Statistisches Bundesamt, vorläufige Ergebnisse Staatsdefizit 2025, berichtet in: Deutsches Ärzteblatt, 25.02.2026, https://www.aerzteblatt.de/themen/sozialpolitik/staatsdefizit-erhoht-sich-leicht-a5ff4327-70f4-4e13-93f7-369b51b25ce0 ; vdiv, https://vdiv.de/news-details/konsum-und-bauinvestitionen-schoben-wirtschaft-2025-an-staatsdefizit-aber-nach-oben-korrigiert (Primärquelle Destatis nicht direkt abgerufen)
3. Deutsche Bundesbank: Deutsche Staatsschulden wachsen 2025 um 144 Milliarden Euro. https://www.bundesbank.de/de/aufgaben/themen/deutsche-staatsschulden-wachsen-2025-um-144-milliarden-euro--992732
4. Richtlinie 2006/112/EG, Art. 98 (i. d. F. der Richtlinie (EU) 2022/542). https://lxgesetze.de/mwstrl/98 ; Hintergrund: https://www.deubner-steuern.de/themen/umsatzsteuer/mwstsystrl-und-eu-mehrwertsteuerreform/aenderung-mwstsystrl-april-22.html
5. Weka Business Media (CH): Mehrwertsteuersätze CH und EU, Stand 01.01.2026. https://www.weka.ch/themen/finanzen-controlling/mehrwertsteuer/buchfuehrung-und-abrechnung/article/mehrwertsteuersaetze-aktuelle-mwst-saetze-ch-und-eu/ (nicht amtlich; Abgleich mit EU-Kommission empfohlen)
6. BMF-Monatsbericht August 2025: Investitionssofortprogramm Deutschland. https://www.bundesfinanzministerium.de/Monatsberichte/Ausgabe/2025/08/Inhalte/Kapitel-2-Fokus/investitionssofortprogramm-deutschland.html
7. Der Betrieb: Steuerliches Investitionssofortprogramm auf dem Weg. https://der-betrieb.de/meldungen/steuerliches-investitionssofortprogramm-auf-dem-weg/ ; Verkündung: KPMG, https://kpmg.com/de/de/home/themen/2025/07/stinvsofortpg-bgbl.html
8. Doerrenberg, P., Peichl, A., Siegloch, S. (2017): The elasticity of taxable income in the presence of deduction possibilities. Journal of Public Economics 151, 41–55. Working-Paper-Fassung: https://www.zew.de/PU70367
9. Werdt, C. (2015): The elasticity of taxable income for Germany and its sensitivity to the appropriate model. FU Berlin Discussion Paper 2015/5. https://ideas.repec.org/p/zbw/fubsbe/20155.html
10. Heckemeyer, J. H., Overesch, M. (2017): Multinationals' profit response to tax differentials: Effect size and shifting channels. Canadian Journal of Economics 50(4), 965–995. https://kups.ub.uni-koeln.de/21270
11. IMK/IW (2024): Herausforderungen für die Schuldenbremse – Investitionsbedarfe in der Infrastruktur und für die Transformation. Pressemitteilung: https://www.boeckler.de/de/pressemitteilungen-2675-600-milliarden-euro-staatliche-extra-investitionen-60422.htm
12. Art. 143h Grundgesetz. https://lxgesetze.de/gg/143h
13. beck-aktuell, 13.08.2025: Weimer verfolgt Plan weiter (Plattform-Soli). https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/digitalabgabe-google-meta-kulturminister-weimer-plattform-soli-digitalsteuer-2025-08-13

## Annahmen-Register (ohne Einzelbeleg, im Skript markiert)

MwSt-Konsumgewichte je Stufe (10/10/20/30/30 %) · Realisationsquote MwSt-Mehraufkommen (85/80/70 %) · Realisationselastizität Kapitalerträge (0,7/0,8/1,0) · Plattformanteil 12 Mrd. · Erbschaft-Semielastizität 1,0 · Wachstumsabschlag · Verhaltensbonus · Rezessionsprofil · Investitionsziel und Puffer je 1 % BIP · Konsumquoten der Mikroprofile · alle aus dem Projekt übernommenen Aufkommens- und Ausgabenblöcke.
