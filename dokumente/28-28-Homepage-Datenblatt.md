# 28:28 – Datenblatt für die Homepage
## Alle Zahlen und Texte der Neufassung, gegliedert wie die Seite

*Stand: 16.09.2026, Fassung 2 (Bestandsgarantie, neue Hero-Texte) · Berechnung: `modell-2828.py` → `modell-2828-ergebnisse.txt`, `modell-2828-daten.json`, `rechner-2828-tabelle.csv` · Rechnerlogik: `rechner-2828.js`*

**Konventionen**
- **Euro-Beträge für Haushalte:** Preise und Rechtsstand 2026. Bei einem Start 2028 liegen die nominalen Beträge bei 2 % Fortschreibung des Existenzminimums rund 4 % höher (DD ≈ 536 €).
- **Staatshaushalt:** in *Modell-Mrd.* (Projektkalibrierung, Modell-BIP 4.200). Für heutige Größenordnungen etwa × 1,06.
- **Konservative Rechnung:** Die Dividende wird in Euro 2026 gegen diese niedrigere Modellbasis gerechnet. Ihr Kostenanteil ist dadurch eher überzeichnet.
- **Modellpfad:** Hauptszenario ist „Robust". Die frühere Homepage nutzte das optimistischere Referenzszenario.

---

## 0 | Was sich gegenüber der 25:25-Seite ändert

| Element | 25:25 (bisherige Seite) | **28:28 (neu)** |
|---|---|---|
| Einheitssatz | 25 % | **28 %** |
| Einkommensteuer | 0 – 8 – 14 – 19 – 23 – 25 % | **0 – 9 – 16 – 21 – 26 – 28 %**, Nullzone = Existenzminimum (12.348 €) |
| Dividende Start | 400 € ab 25 J., Kindergeld bleibt | **515 € für alle Erwachsenen, 257,50 € je Kind, ab Tag 1** |
| Dividende Ausbau | 500 → 600 € per Stufe | **50 → 55 → 60 % des Existenzminimums** (515 → 566 → 617 €) |
| Konsum-Label | 5 – 10 – 15 – 20 – 25 % | **5 – 11 – 17 – 22 – 28 %** (effektiv 20,0 %) |
| CO₂ | 50 → 100 → 150 €/t | **100 → 150 €/t**, klimaschädliche Subventionen entfallen |
| Vermögen | 1 % ab 1 Mio., anrechenbar | **1 % ab 1 Mio.; über 2 Mio. nicht anrechenbar**; **Bodenwertabgabe** statt Grundsteuer |
| Sozialabgaben | 42 → 28 → 18 % | **28 % ab Start → 18 % mit der 60-%-Stufe**, keine Bemessungsgrenzen |
| Härtefälle | 28 → 40 Mrd. | **40 Mrd. ab Start, mit Bestandsgarantie** für heutige Grundsicherungs-, Bürgergeld- und BAföG-Beziehende |
| Sicherungen | Transformationsfonds (kreditfinanziert) | **Vorlaufphase + Stabilitätspuffer 2 % BIP + Investitionsfonds 1 % BIP**, keine Anlaufschulden |
| Hauptszenario | Referenz (DD nominal fix) | **Robust** (DD an Existenzminimum gekoppelt) |

---

## 1 | Kopf und Hero

**Wortmarke:** TAX 28:28
- Bemaßung oben: „Ein System · keine Ausnahmen"
- Bemaßung unten: „Obergrenze für alle" / „Auch für Konzerne & Plattformen"

**Claim (H1):** Das einfache Steuersystem für das 21. Jahrhundert.
**Zweite Zeile:** Fair, sozial und innovativ.

**Unterzeile:** Höchstens 28 % auf jedes Einkommen – und 28 % auch für Konzerne, Plattformen, Erben und große Vermögen. Dazu eine Digitaldividende von 515 € im Monat für jeden Erwachsenen, vom ersten Tag an.

**Hinweis unter den Buttons:** Alle Rechenmodelle sind hier open source prüfbar. (Der Link führt zu den eingebetteten Modellen: Gesamtmodell, Rechnerlogik, Annahmen und Quellen.)

**Prüfstempel-Kennwerte:**

| Wert | Beschriftung | Grundlage |
|---|---|---|
| **515 €** | Dividende im Monat ab dem ersten Tag – 257,50 € je Kind | 50 % des Existenzminimums 2026 |
| **über 95 %*** | der Menschen haben mehr im Geldbeutel | Gruppenschätzung, siehe Abschnitt 4.4 |
| **+21 %** | verfügbares Einkommen für eine Familie mit zwei Kindern | Profil Familie Müller: 50.620 → 61.174 € (nach Konsum-Label) |

\* Fußnote auf der Seite: „Schätzung aus dem Modell: Ohne Bestandsgarantie stünden rund 5 % schlechter, vor allem Haushalte im Bürgergeld ohne Erwerbseinkommen. Mit der Bestandsgarantie (Position 09) betrifft ein Minus nur noch Teile sehr großer Vermögen. Keine Mikrosimulation."

---

## 2 | Blatt 1 · Befund

Nicht neu berechnet; die vier Kacheln bleiben inhaltlich bestehen. Die Einzelwerte (20.000+ Seiten, 40 % verschobene Gewinne, > 80 % Entzugsrate, 0 € Fortschrittsdividende) stammen aus dem Projekt und wurden hier nicht erneut belegt.

---

## 3 | Blatt 2 · Konstruktion – zehn Positionen

| Position | Titel | Regel (Bauteil-Kennung) | Text |
|---|---|---|---|
| 01 · Einkommen | Stufentarif mit harter Obergrenze | **0 – 9 – 16 – 21 – 26 – 28 %** *(Grenzen 12.348 / 25.000 / 40.000 / 55.000 / 70.000 €)* | Besteuert wird das Brutto – ohne Abzüge, ohne Splitting. Das Existenzminimum bleibt steuerfrei; darüber lohnt Arbeit auf jeder Stufe. |
| 02 · Kapital | Kapital und Arbeit werden gleich behandelt | **28 % auf alle Erträge** | Auch Veräußerungsgewinne zählen. Lohn in Kapitalertrag umzuwandeln lohnt sich nicht mehr. |
| 03 · Erbschaft | Auch Geerbtes ist Einkommen | **28 % über 400.000 € je Kind** | Ein Satz, keine Verschonungsausnahmen. Betriebe können die Steuer stunden. |
| 04 · Vermögen und Boden | Große Vermögen und teurer Boden tragen mit | **1 % ab 2 Mio. € · Grundsteuer nur auf den Boden** | Vermögen bis 2 Mio. € bleibt praktisch unberührt. Die Grundsteuer richtet sich nur noch nach dem Wert des Grundstücks, nicht nach dem Haus darauf – so gilt es in Baden-Württemberg schon seit 2025 [8]. Wer baut oder saniert, zahlt dafür nicht mehr; ungenutztes Bauland in guter Lage zahlt mit. Auf Mieten darf die Steuer nicht umgelegt werden. |
| 05 · Konzerne und Plattformen | Besteuert wird, wo die Kunden sitzen | **28 % am Ort der Nutzung** | Das gilt ausdrücklich für digitale Plattformen. Gewinne lassen sich verschieben, Kundschaft nicht. |
| 06 · Konsum | Die Mehrwertsteuer wird zum Label | **A+ 5 % · A 11 % · B 17 % · C 22 % · D 28 %** | Wie beim Energielabel sieht man auf einen Blick, was ein Produkt kostet – und warum. Je nachhaltiger, desto günstiger. |
| 07 · Klima | CO₂-Preis mit Rückgabe an alle | **100 → 150 € je Tonne · keine klimaschädlichen Subventionen** | Das Geld fließt über die Dividende zurück: Wer wenig verbraucht, gewinnt. Steuervorteile für fossile Nutzung entfallen. |
| 08 · Dividende | Die Digitaldividende | **515 € · Kinder 257,50 € → 566 € → 617 €** | Für alle Erwachsenen, Kinder erhalten die Hälfte. Gekoppelt an das amtliche Existenzminimum, steigt per Formel. Steuerpflichtig: Unten bleibt fast alles, oben fließen 28 % zurück. |
| **09 · Schutz** | **Niemand mit kleinem Einkommen fällt zurück** | **Bestandsgarantie · 40 Mrd. € für gezielte Hilfe** | Wer heute Bürgergeld, Grundsicherung oder BAföG bekommt, erhält mindestens das bisherige Niveau – die Differenz zahlt der Härtefallfonds. Er trägt auch Wohnkosten, Pflege, Behinderung und besondere Lebenslagen. |
| **10 · Arbeit** | **Mehr Netto vom Brutto – für alle** | **Sozialabgaben 42 → 28 → 18 % · ohne Obergrenze** | Die Beiträge sinken sofort auf 28 %, mit der nächsten Dividendenstufe auf 18 %. Dafür zahlen hohe Einkommen auf jeden Euro – „keine Ausnahmen" gilt in beide Richtungen. |

**Zu Position 04 – ist „Bodenwertabgabe" verständlich?** Eher nicht: Das Wort ist neu und klingt nach zusätzlicher Steuer. Die Seite sagt deshalb „Grundsteuer nur auf den Boden" und erklärt drei Dinge: (1) Es ersetzt die heutige Grundsteuer. (2) Maßgeblich ist nur der Grundstückswert, nicht das Gebäude. (3) Das Modell gibt es schon: Baden-Württemberg erhebt die Grundsteuer seit 2025 so, der Bundesfinanzhof hat das Landesmodell am 20.05.2026 bestätigt [8].

**Grafik POS 06 (Label):**

| Klasse | Satz | Beispielhafte Zuordnung |
|---|---|---|
| A+ | 5 % | Grundnahrungsmittel, Reparatur, Kreislaufprodukte |
| A | 11 % | nachhaltige Standardgüter |
| B | 17 % | Standardgüter |
| C | 22 % | ressourcenintensive Güter |
| D | 28 % | klimaschädliche Luxusgüter |

Die Zuordnung ist illustrativ und aus der Projektlogik abgeleitet. Die Konsumanteile (10/10/20/30/30 %) sind eine Annahme.

**Grafik POS 08 (Dividendentreppe):** 515 € (50 %) → 566 € (55 %) → 617 € (60 %), Preise 2026. Schritte nur bei erfüllter Haushaltsregel. Im Robust-Pfad: 55 % ab 2030, 60 % ab 2037.

---

## 4 | Blatt 3 · Lastprobe (Rechner)

### 4.1 Logik (umgesetzt in `rechner-2828.js`, geprüft gegen das Python-Modell)

**Heute (Recht 2026):**
- **Einkommensteuer:** Tarif 2026 mit Grundfreibetrag 12.348 € [1], Splitting bei Partner:in ohne Einkommen.
- **Solidaritätszuschlag:** Freigrenze 20.350 € (Einzelveranlagung) bzw. 40.700 € (Zusammenveranlagung), darüber Milderungszone mit höchstens 11,9 % des Unterschiedsbetrags [2].
- **Sozialabgaben (AN-Anteil):**
  - KV 7,3 % + halber durchschnittlicher Zusatzbeitrag (2,9 %) [3],
  - PV 1,8 %, Kinderlose zusätzlich 0,6 % [4],
  - RV 9,3 % und AV 1,3 % [3].
  - Bemessungsgrenzen 69.750 € (KV) und 101.400 € (RV) [3].
- **Pauschalen:** Werbungskosten 1.230 €, Sonderausgaben 36 €.
- **Kindergeld:** 259 € je Kind [5]. Die Günstigerprüfung Kinderfreibetrag ist nicht abgebildet; das unterschätzt das Heute-Netto bei hohen Einkommen mit Kindern leicht.

**28:28:**
- **Sozialabgaben:** AN-Anteil 14 % (Stufen 50/55 %) bzw. 9 % (Stufe 60 %) auf das gesamte Brutto.
- **Einkommensteuer:** Tarif 0–9–16–21–26–28 % auf *Brutto + Dividende*.
- **Dividende:** 515 € × 12. Kinderdividende steuerfrei (Annahme).
- **Partner:in ohne Einkommen:** erhält die eigene Dividende und wird eigenständig veranlagt (Dividende liegt unter der Nullzone, bleibt also steuerfrei).
- **Anzeige „Effektive Belastung heute → neu":** (Steuer + SV) / Brutto. Beim neuen System ist die Steuer auf die Dividende eingerechnet.

**Fußnote für den Rechner (Vorschlag):** „Recht 2026 gegenüber 28:28 in Preisen 2026. Nicht enthalten: Konsum-Label (effektiv 20,0 % statt ca. 16,5 %) und CO₂-Preis. Für einen Durchschnittshaushalt kostet das Label rund 1,5–2 % des verfügbaren Einkommens; der Nettogewinn bleibt in allen geprüften Profilen deutlich positiv."

### 4.2 Profile (€/Jahr, Stufe 50 %)

| Profil | Brutto | heute | 28:28 | Plus | nach Konsum-Label | in % |
|---|---:|---:|---:|---:|---:|---:|
| Mia, Studentin, ohne Einkommen | 0 | –¹ | 6.180 | +6.180 | +6.033 | – |
| Tom, Berufseinsteiger | 28.000 | 20.180 | 27.653 | +7.473 | +6.884 | +34 % |
| Anna, alleinerziehend, 1 Kind | 28.000 | 23.414 | 30.743 | +7.329 | +6.674 | +29 % |
| Sarah, Fachkraft | 42.000 | 28.193 | 37.044 | +8.851 | +8.062 | +29 % |
| Durchschnittsverdiener | 51.944 | 33.632 | 43.351 | +9.719 | +8.796 | +26 % |
| Klaus, Facharbeiter | 55.000 | 35.262 | 45.185 | +9.922 | +8.960 | +25 % |
| Familie Müller, Alleinverdiener, 2 Kinder | 63.000 | 50.620 | 62.345 | +11.725 | +10.554 | +21 % |
| Jonas, Ingenieur | 80.000 | 48.544 | 59.861 | +11.317 | +10.193 | +21 % |
| Dr. Weber, Führungskraft | 150.000 | 85.528 | 100.461 | +14.933 | +13.424 | +16 % |
| Inge, Rentnerin (880 €/Monat) | 10.560 | 12.720² | 15.481 | +2.761 | – | +22 % |

¹ Heute je nach Lage BAföG, Bürgergeld oder keine Leistung. ² Heute einschließlich Grundsicherung.

**In den Stufen 55 % und 60 %** (verfügbar, vor Konsum-Label):

| Profil | 55 % | 60 % |
|---|---:|---:|
| Tom | 28.167 | 30.081 |
| Sarah | 37.527 | 40.110 |
| Familie Müller | 64.021 | 68.840 |
| Dr. Weber | 100.902 | 108.842 |
| Inge | 16.038 | 16.904 |

Die vollständige Tabelle (Brutto 0–200.000 € in 5.000-€-Schritten, 0–3 Kinder, mit/ohne Partner:in) steht in `rechner-2828-tabelle.csv`.

### 4.3 Durchschnittsverdiener (vorläufiges Durchschnittsentgelt 2026: 51.944 € [6])

| Kenngröße | heute | 28:28, 50 % | 55 % | 60 % |
|---|---:|---:|---:|---:|
| Abgabenlast (ESt + AN-Beiträge) / Brutto | 35,3 % | 28,4 % | 28,7 % | 24,1 % |
| Nettobelastung nach Dividende | 35,3 % | 16,5 % | 15,7 % | 9,8 % |
| Grenzbelastung je zusätzliche 100 € | 46 % | 40 % | 40 % | 35 % |

**Korrektur gegenüber der bisherigen Seite:** Die Aussage „die Grenzbelastung halbiert sich" gilt für 28:28 nicht. Weil die steuerpflichtige Dividende das Einkommen in eine höhere Tarifzone schiebt, sinkt die Grenzbelastung beim Durchschnitt von 46 auf 40 % (Stufe 60 %: 35 %). Die Durchschnittsbelastung sinkt deutlich stärker.

### 4.4 Anteil mit mehr im Geldbeutel (Schätzung)

| Gruppe, die ohne Garantie schlechter stünde | Personen (Mio., Annahme) | Grund |
|---|---:|---|
| Bürgergeld-Haushalte ohne Erwerbseinkommen | 3,5 (von 5,5 Mio. Beziehenden [9]) | Regelbedarf 563 € > 515 €; Kinder 357–471 € > 257,50 € [10] |
| Grundsicherung bei Erwerbsminderung ohne weiteres Einkommen | 0,36 | wie oben |
| BAföG mit hohem Förderbetrag | 0,3 | Förderbetrag über der Dividende |
| sehr große Vermögen (Netto-Verlierer) | 0,4 | Vermögen über 2 Mio., Kapitalerträge 28 %, Erbschaft, Boden |

- **Ohne Bestandsgarantie:** rund **95 %** von 84 Mio. haben mehr.
- **Mit Bestandsgarantie:** über **99 %**.

Für die Seite ist „über 95 %" die vorsichtige Angabe. Kosten der Garantie: rund 5 Mrd., im Härtefallfonds (40 Mrd.) enthalten. Grenzen: Gruppenschätzung, keine Mikrosimulation; Beamte und Selbständige sind nicht gesondert modelliert.

**Warum Bestandsgarantie?** Bürgergeld-Haushalte ohne Erwerbseinkommen hätten ohne sie ein Minus, obwohl sie künftig jeden hinzuverdienten Euro ohne Anrechnung behalten. Die Kosten der Unterkunft im Bürgergeld liegen bei knapp 20 Mrd. (2024, Sekundärquelle [11]); sie laufen künftig ebenfalls über den Härtefallfonds. **Das ist der knappste Punkt der Ausgabenseite und sollte vor Veröffentlichung genauer geprüft werden.**

---

## 5 | Blatt 4 · Simulation

### 5.1 Zeitreihen für das Diagramm (2026–2035; Start 2028)

`hist` (2010–2025) und `ohne` bleiben unverändert aus der bestehenden Seite. `mit` ist neu berechnet (Robust-Pfad).

```js
// Staatsschulden (% BIP) – neu: Nettoquote abzüglich Stabilitäts- und Investitionsfonds
ohne: [64,65,65,66,66,67,67,68,68,69],
mit:  [64,65,62.3,62.9,62.9,63.7,63.4,64.0,63.5,64.0],
// Einkommensungleichheit (Gini)
ohne: [.313,.313,.314,.314,.315,.315,.316,.316,.317,.317],
mit:  [.313,.313,.274,.274,.269,.269,.269,.269,.270,.270],
// CO₂-Emissionen (Mt) – unverändert aus der 25:25-Fassung
ohne: [608,596,584,572,560,549,538,527,516,505],
mit:  [608,596,578,552,524,496,470,446,424,404],
// Belastung Durchschnittsverdiener (%)
ohne: [36.7,36.8,36.9,37.0,37.1,37.2,37.3,37.4,37.5,37.6],
mit:  [36.7,36.8,29.8,29.8,30.3,30.3,30.4,30.5,30.6,30.7],
```

**Wie die `mit`-Reihen entstehen:**
- **Schulden:** `ohne`-Wert minus Fondsbestand in % BIP. Die zusätzlichen Investitionen verändern die Schuldenquote in dieser Rechnung nicht.
- **Gini:** `ohne`-Wert × relative Modelländerung (−13 % bei Stufe 50, −15 % ab Stufe 55). Die Modelländerung reagiert stark auf die Annahme zu heutigen Transfers (Spanne −5 bis −16 %). Belastbar ist daher nur eine Größenordnung von **−2 bis −5 Gini-Punkten**.
- **CO₂:** nicht neu modelliert. Der frühere Start mit 100 €/t (statt 50) dürfte eher stärker wirken.
- **Belastung:** `ohne`-Wert × Verhältnis der Modellbelastung (28,4 bzw. 28,7 % zu 35,3 %). Die Skalierung gleicht eine Definitionsabweichung der bestehenden Reihe aus.

**Chart-Notiz (Vorschlag):** „Historische Werte: Größenordnungen der bestehenden Seite. Pfade ab 2028: Modellillustrationen aus dem Robust-Szenario – keine Prognosen. Schulden als Nettoquote nach Fondsreserve; Gini als Modellschätzung (Spanne −2 bis −5 Punkte); CO₂-Pfad aus der Vorfassung. Methodik und Stresstest im Anhang."

**Legende:** Verlauf bis 2025 · ohne 28:28 (Fortschreibung) · mit 28:28 (Modellpfad Robust)

### 5.2 Haushaltskennzahlen für eine Info-Box

| Szenario | Saldo 2028 | niedrigster Saldo | Lückenjahre | niedrigster Fondsstand | 566 € ab | 617 € ab | Investitionsquote | Fonds 2047 | DD-Realwert (min.) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Optimistisch | +60 | +57 | 0 | 118 | 2030 | 2032 | 100 % | 1.531 | 100 % |
| **Robust („vorsichtig")** | **+55** | **+40** | **0** | **113** | **2030** | **2038** | **100 %** | **418** | **100 %** |
| Stress („Rezessionstest", 2033–35) | +30 | −45 | 0 | 52 | – | – | 85 % | 439 | 91 % |
| *Robust ohne Bausteine* | +0 | +0 | 0 | 84 | 2036 | – | 95 % | 381 | 94 % |
| *Stress ohne Bausteine* | −8 | −64 | **1** | −5 | – | – | 64 % | 305 | 82 % |

Modell-Mrd. Investitionsquote = realisierte flexible Investitionen / Ziel 1 % BIP. DD-Realwert = Dividende in Preisen 2026 / Sollwert.

**Lesart:**
- **Ergebnis:** Das Kernsystem trägt 515 € ab dem ersten Tag in allen Szenarien ohne Lücke.
- **Bausteine nötig:** Ohne die vier Bausteine (Vermögen, Boden, Subventionen, CO₂-Pfad) verfehlt der Stresstest das Investitionsziel deutlich, und der Ausbau auf 60 % findet im Robust-Pfad nicht statt; im Stress entsteht ein Lückenjahr.
- **Krisenfall:** Die Dividende wird nicht gekürzt. Weil die Anpassung pausiert, sinkt ihr Realwert im Stressfall zeitweise auf 91 % des Sollwerts (466 € in Preisen 2026).

### 5.3 Robust-Pfad im Detail

| Jahr | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2040 | 2043 | 2047 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Stufe | 50 | 50 | 55 | 55 | 55 | 55 | 55 | 55 | 55 | 55 | 60 | 60 | 60 | 60 |
| DD nominal € | 515 | 525 | 589 | 601 | 613 | 625 | 637 | 650 | 663 | 676 | 752 | 783 | 830 | 899 |
| DD in € 2026 | 515 | 515 | 566 | 566 | 566 | 566 | 566 | 566 | 566 | 566 | 617 | 617 | 617 | 617 |
| Saldo | +55 | +64 | +50 | +58 | +67 | +73 | +79 | +85 | +92 | +99 | +40 | +53 | +74 | +106 |
| Investitionen | 42 | 43 | 44 | 46 | 47 | 48 | 50 | 51 | 53 | 54 | 56 | 59 | 64 | 72 |
| Fonds | 113 | 134 | 139 | 151 | 171 | 195 | 224 | 258 | 298 | 342 | 326 | 309 | 320 | 418 |

---

## 6 | Blatt 5 · Sicherungen – fünf Regeln (neu)

**Lede:** Ein Entwurf ist so gut wie seine Sicherungen. Fünf Regeln entscheiden – nicht Wahlkämpfe.

1. **Einnahmen zuerst.** Unternehmen, Plattformen, Kapital, Erbschaft, große Vermögen und Boden werden mehrere Monate vor der ersten Auszahlung nach neuem Recht besteuert. Die Dividende startet auf einem Polster von rund 100 Mrd. €, nie auf Kredit.
2. **Formel statt Kalender.** Die Dividende beträgt die Hälfte des amtlichen Existenzminimums. Sie steigt in Fünf-Punkte-Schritten bis 60 %, sobald der Stabilitätspuffer gefüllt ist und die Investitionen gesichert sind.
3. **Nie kürzen – nur pausieren.** Ist der Puffer angegriffen, setzt nur die jährliche Anpassung aus. Nachgeholt wird ausschließlich aus Überschüssen.
4. **Puffer und Investitionsfonds.** 2 % des BIP liegen als Krisenreserve bereit; darüber hinaus fließt jedes Jahr bis zu 1 % des BIP in flexible öffentliche Investitionen. Der Staat bleibt handlungsfähig, ohne neue Schulden.
5. **Fiskalrat, Dashboard, Korridor.** Ein unabhängiger Rat prüft jährlich alle Annahmen; die Ist-Zahlen sind monatlich öffentlich. Als letzte Sicherung kann der Einheitssatz regelgebunden zwischen 25 und 30 % gleiten.

---

## 7 | Anlagen und Fragen

### 7.1 Statischer Haushalt je Stufe (Modell-Mrd., Robust)

| | 50 % | 55 % | 60 % |
|---|---:|---:|---:|
| Einkommensteuer inkl. Dividende | 313,3 | 318,9 | 324,5 |
| Kapitalerträge 28 % | 48,8 | 48,8 | 48,8 |
| Mehrwertsteuer (Label) | 375,9 | 375,9 | 375,9 |
| Unternehmen & Plattformen 28 % (davon Plattformen ca. 13, Annahme) | 157,6 | 157,6 | 157,6 |
| Erbschaft 28 % | 35,9 | 35,9 | 35,9 |
| Vermögen-Mindeststeuer | 20,7 | 20,7 | 20,7 |
| CO₂ 100 €/t + Sonstige | 220,0 | 220,0 | 220,0 |
| **Einnahmen Kernsystem** | **1.172,2** | **1.177,8** | **1.183,4** |
| Bausteine: Vermögen > 2 Mio. / Boden / Subventionen / CO₂ 150 | 12 / 20 / 20 / 15 | 12 / 20 / 20 / 15 | 12 / 20 / 20 / 15 |
| Basisausgaben | 596,0 | 596,0 | 576,0 |
| SV-Zuschuss | 60,0 | 60,0 | 90,0 |
| Härtefall + Gesundheit (inkl. Bestandsgarantie) | 40,0 | 40,0 | 42,0 |
| Digitaldividende | 475,9 | 523,0 | 570,1 |
| **Ausgaben** | **1.171,9** | **1.219,0** | **1.278,1** |
| **Saldo ohne Bausteine** | **+0,3** | **−41,2** | **−94,7** |
| **Saldo mit Bausteinen** | **+67,3** | **+25,8** | **−27,7** |
| in % Modell-BIP | +1,60 | +0,61 | −0,66 |

Zielsaldo für die Investitionen: +42. Die 60-%-Stufe ist statisch nicht gedeckt und wird erst durch Wachstum finanzierbar; deshalb greift sie im Robust-Pfad erst 2038.

### 7.2 Aktualisierte Antworten für „Kritische Fragen"

- **Reichen 28 Prozent?** Im Verbund ja. Das Kernsystem deckt 515 € ab Start gerade eben (+0,3 Mrd.). Mit den vier Bausteinen entsteht ein Überschuss von rund 67 Mrd., der Investitionen und Krisenreserve finanziert. Ohne die Bausteine entstünde im Rezessionstest ein Lückenjahr.
- **Wer verliert?** In keinem geprüften Profil sinkt das verfügbare Einkommen; Grundsicherungs- und Bürgergeld-Haushalte sind durch die Bestandsgarantie geschützt. Relativ gewinnen untere Einkommen am meisten (+34 %), hohe am wenigsten (+16 %). Mehr zahlen: Nutzer heutiger Gestaltungsmodelle, sehr große Vermögen, Eigentümer hoher Bodenwerte, Empfänger klimaschädlicher Subventionen.
- **Hört jemand auf zu arbeiten?** Es gibt keine Entzugsraten mehr. Die Grenzbelastung des Durchschnittsverdieners sinkt von 46 auf 40 %, mit der 60-%-Stufe auf 35 %.
- **Was passiert in der Krise?** Im Stresstest (Rezession und dauerhaft schwaches Wachstum) entsteht keine Lücke. Die Dividende bleibt nominal stabil, ihr Ausbau pausiert, ihr Realwert sinkt zeitweise um bis zu 9 %.

---

## 8 | Hinweise vor der Veröffentlichung

1. **Kinderdividende:** 257,50 € liegen 1,50 € unter dem Kindergeld 2026 (259 € [5]). Kein Haushalt verliert dadurch insgesamt; für Familien in der Grundsicherung greift die Bestandsgarantie. Die dauerhafte Regel (Hälfte oder „mindestens Kindergeld", Mehrkosten ca. 0,25 Mrd.) ist noch zu entscheiden.
2. **Grenzbelastung:** Frühere Aussagen zur „Halbierung" müssen auf der Seite und in den Anlagen angepasst werden (siehe 4.3).
3. **Bausteine** (Vermögen, Boden, Subventionen, CO₂) sind Annahmen auf Basis von DIW, UBA und Destatis (siehe Bericht „Digitaldividende ab Start"). Vor Veröffentlichung sollten Primärschätzungen folgen.
4. **Ausgangslage:** Das Modell unterstellt einen ausgeglichenen Ausgangshaushalt. Das tatsächliche Staatsdefizit 2025 (2,7 % BIP) ist nicht Teil dieser Bilanz; „keine Lücke" bezieht sich auf die Reform selbst.
5. **Transferersatz ab Tag 1:** Bürgergeld-Regelbedarf, Kindergeld, BAföG und Wohngeld entfallen als eigene Leistungen (−164 Mrd., Projektwert, nicht neu geprüft). Wohnkosten und Bestandsgarantie laufen über den Härtefallfonds (40 Mrd.) – der knappste Posten der Rechnung.
8. **Befund-Kacheln:** Die Seitenzahl des Steuerrechts (20.000+) ist noch nicht belegt; die Gewinnverlagerung (~40 %) stützt sich auf Tørsløv/Wier/Zucman, die Entzugsrate (80–90 %) auf die Hinzuverdienstregeln im Bürgergeld – beide Belege sollten im Anhang mit Primärquelle ergänzt werden.
6. **Existenzminimum-Fortschreibung:** mit 2 % pro Jahr angenommen. Die amtlichen Werte für 2027 ff. sind hier nicht berücksichtigt.
7. **Übertragung:** Die englische, französische und spanische Fassung sowie die eingebetteten Anlagen müssen entsprechend nachgezogen werden.

---

## Quellen

1. § 32a EStG (Tarif ab VZ 2026). https://www.gesetze-im-internet.de/estg/__32a.html
2. Techniker Krankenkasse: Solidaritätszuschlag 2026 – Freigrenzen und Milderungszone. https://www.tk.de/firmenkunden/service/fachthemen/fachthema-beitraege/solidaritaetszuschlag-2075802
3. R+V: Sozialversicherungsgrößen 2026 (Beitragssätze, BBG, durchschnittlicher Zusatzbeitrag). https://www.ruv.de/dam/jcr:7d6a22ca-5080-4be1-a23e-842938a70cf5/leben-sozialversicherungsgroessenkarte.2026-03-16-14-01-32.pdf ; vdek: https://www.vdek.com/vertragspartner/arbeitgeber/beitragssaetze.html
4. vdek: Pflegeversicherung 2026 (3,6 %, Kinderlosenzuschlag 0,6 %). https://www.vdek.com/vertragspartner/arbeitgeber/beitragssaetze.html
5. Finanztip: Kindergeld 2026 (259 €, § 66 EStG). https://finanztip.de/kindergeld/
6. Grant Thornton zur SV-Rechengrößenverordnung 2026 (vorläufiges Durchschnittsentgelt 51.944 €). https://www.grantthornton.de/themen/2025/referentenentwurf-zur-sozialversicherungsrechengroessen-sv-verordnung-2026/
7. Grundfreibetrag/Existenzminimum 2026 (12.348 €): VLH. https://www.vlh.de/wissen-service/steuer-abc/grundfreibetrag-was-ist-das.html
8. Bundesfinanzhof bestätigt das Bodenwertmodell Baden-Württemberg (II R 26/24, II R 27/24, 20.05.2026), berichtet von Der Betrieb. https://der-betrieb.de/meldungen/bfh-bestaetigt-grundsteuer-modell-in-baden-wuerttemberg/ ; IHK Stuttgart: https://www.ihk.de/stuttgart/fuer-unternehmen/recht-und-steuern/steuerrecht/grund-und-gewerbesteuer/landesgrundsteuergesetz-bw-4867920
9. Rund 5,5 Mio. Bürgergeldbeziehende 2024, knapp 4 Mio. erwerbsfähig (Regierungsangaben, dpa). https://www.schwaebische.de/politik/bas-plant-2026-nullrunde-beim-buergergeld-3882077
10. Regelbedarfe 2026 (563 / 506 / 471 / 390 / 357 €). https://www.finanz.de/news/buergergeld-2026-verlierer-hoehe-10511/
11. Berliner Mieterverein: Kosten der Unterkunft knapp 20 Mrd. von rund 47 Mrd. Bürgergeld-Leistungen 2024 (nicht amtlich). https://www.berliner-mieterverein.de/?p=92206
12. Weitere Quellen zu Elastizitäten, Staatsdefizit, Vermögen, Boden und Subventionen: siehe Berichte „28:28 – Levelanalyse" und „Digitaldividende ab Start".
