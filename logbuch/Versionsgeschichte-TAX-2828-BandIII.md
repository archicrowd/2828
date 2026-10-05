# TAX 28:28 — Logbuch, Band III: ab v3.5.1

**Fortsetzung von `Versionsgeschichte-TAX-2828-BandII.md`.** Band II endet mit
v3.5 und Korrektur 46. Dieser Band führt ab v3.5.1 weiter und ist der erste, der
direkt in diesem Repository entsteht und nicht aus dem Projektraum übernommen
wurde.

Stand: 5. Oktober 2026 · Modellstand **v3.7**

---

## 3 | Versionen, Fortsetzung

### v3.5.1 — Parameterstand aus Logbuch und Gesamtkonzept, Prüfregeln

**Art der Änderung: PATCH.** Keine Zahl des Modells ändert sich, keine Position
ändert sich inhaltlich, es gibt keine neue Rechnung. Neu ist, dass die
Strukturgrößen erstmals in einer maschinenlesbaren Datei mit Pflichtfeldern
stehen, und dass Unstimmigkeiten sichtbar wurden, die im Fließtext nicht
auffielen.

**Anlass.** Aufbau des Repositorys `archicrowd/2828`. Die Regel „Zahlen
tragen Einheit, Bezugsjahr und Preisbasis" (Korrekturen 42 bis 46) wurde als
Prüfregel im Lauf-Skript umgesetzt, und die vorhandenen Größen wurden dagegen
gehalten.

**Was neu ist**
- `modell/parameter.toml`: 25 Parameter. Status: 20 × „modellrechnung", 5 × „annahme",
  0 × „belegt". Jeder Eintrag nennt Quelle und, wo nötig, einen Hinweis zur Prüfbarkeit.
- `modell/lauf.py`: lehnt ab (a) Geldbeträge ohne Preisbasis, (b) reale Werte ohne
  Preisjahr, (c) „belegt" mit der Quelle „eigene Setzung", (d) fehlende Pflichtfelder,
  (e) doppelte Namen. Getestet mit fünf absichtlich eingebauten Fehlern; alle fünf
  wurden gemeldet.
- `daten/aggregate/ergebnis.json`: maschinenlesbare Ergebnisdatei mit Modellstand und
  Prüfsumme des Parameterfiles. Die Ergebnisliste ist noch leer.
- `daten/aggregate/nicht-eingetragen.md`: Größen, die nicht eingetragen wurden, und
  die Unstimmigkeiten B1 bis B4 (unten).

**Quellen der Parameter.** Logbuch Band I (bis v3.1) und Band II (v3.2 bis v3.5)
sowie das Gesamtkonzept im Chat „Steuerkonzept von 2525 auf 3030 umstellen"
(Zeitpfad-Tabelle und Seitentext vom 4. Oktober 2026). **Keiner der Werte ist gegen
Rohdaten oder ein Rechenskript geprüft.** Die Skripte `modell/basis.py`, `pfad.py`,
`final.py`, `tilgung.py` und `aufschlag.py`, die Band II nennt, liegen nicht vor.

**Was die Nachrechnung ergab**
- Bestätigt: 12.157 × 1,13535 = 13.802 (Logbuch 13.803, Rundung). 14.227 ÷ 12.157 =
  1,17027 (Logbuch 1,17024, Rundung). 6.072 € je Kopf und Jahr entsprechen 11,21 % des
  BIP bei 255,1 Mio Personen (6.066 €) und 506 € je Monat.
- Die Dividendenreihe 550 → 512 → 707 € gilt für **Deutschland** (je Kopf und Monat,
  Preise 2028). Der Klubschnitt ist 506 → 472 → 651 €. Das Verhältnis beträgt in allen
  drei Stützjahren 1,087 (506 × 1,087 = 550; 472 × 1,087 = 513; 651 × 1,087 = 707,6).
  Auch die „49 € je BIP-Punkt und Monat" gelten für Deutschland.

**Wodurch es auffiel.** Beim Nachrechnen der Dividende gegen die Basis von 255,1 Mio
Personen. Die Auflösung stand im Gesamtkonzept, nicht im Logbuch.

*Skripte: `modell/lauf.py`. Dateien: `modell/parameter.toml`,
`daten/aggregate/ergebnis.json`, `daten/aggregate/nicht-eingetragen.md`.
Commits: `cf189a2`, `262e984`, `23b7050`.*

---

### v3.6 — Zeitpfad rekonstruiert und gegen die Tabelle des Gesamtkonzepts geprüft

**Art der Änderung: MINOR** (neue Rechnung). Keine bestehende Zahl des Modells
ändert sich. 5. Oktober 2026.

**Anlass.** Auftrag, die Rechnung wieder in sich stimmig zu stellen. Das Skript
`pfad.py` (und `dyn.py`) liegt nicht vor. Es wurde aus den Parametern und aus
Fragmenten des Originals rekonstruiert, die im Chat zu sehen waren
(Konstanten `A_OHNE_V`, `B_AUFG`, `V_START`, `D_START`, `I_ALT`, `REST`, Aufbau von
`verteidigung()` und `zins_eff()`).

**Was neu ist**
- `modell/pfad.py`: Rekonstruktion des Zeitpfads 2028 bis 2060. Aufbau im Kopf der
  Datei. Kern: nominaler Schuldenstand konstant (Quote fällt mit 3,0 % nominalem
  Wachstum), Altbestand läuft linear über 7,5 Jahre auf den Zielzins 2,5 % aus,
  Verteidigung steigt linear bis 2035 auf 2,5 %, Dividende ist Restgröße.
- 4 Parameter ergänzt (jetzt 29): `b_fachaufgaben_bip_2028`,
  `a_ohne_verteidigung_zins_bip_2028`, `zins_effektiv_altbestand`,
  `restlaufzeit_schulden`.
- `daten/aggregate/referenz_gesamtkonzept.csv`: 23 Referenzwerte, aus dem Chat
  abgeschrieben (Zeitpfad-Tabelle, Mindestquote).
- Ausgaben: `pfad.csv` (Jahre 2028–2060), `pfad_abgleich.csv`,
  `pfad_sensitivitaet.csv`.

**Ergebnis des Abgleichs.** 23 von 23 Werten innerhalb der Toleranz (0,01 Punkte
des BIP; 1,5 EUR je Kopf und Monat). Größte Abweichung bei den Anteilen: 0,0053
Punkte (2040). Dividende je Kopf und Monat (Klub, real, Preise 2028): 505,4 gegen
506 (2028), 471,1 gegen 472 (2035), 649,9 gegen 651 (2060). Mindestquote: 30,616
gegen 30,61 (ohne Wachstum), 29,971 gegen 29,97 (Zentralfall). Die Tabelle ist
in sich rechenbar: in allen sechs Spalten gilt Dividendenanteil = 30,6 − A gesamt − 10,35.

**Beweiskraft, offen gesagt**
1. Eine Rekonstruktion, die die Tabelle trifft, zeigt Übereinstimmung, nicht, dass
   das Original so gerechnet hat. Andere Strukturen könnten dieselben Werte liefern.
2. Die Spalte 2028 ist nicht unabhängig: `a_ohne_verteidigung_zins_bip_2028` ist
   die Restgröße aus der Dividende 2028 (6,439).
3. Zinsdienst, A gesamt und Dividendenanteil hängen über zwei Gleichungen
   zusammen. Unabhängig sind etwa neun Werte (Zinsdienst 2030 bis 2060, Dividende
   je Kopf 2035 und 2060, die zwei Mindestquoten).
4. Die Toleranzen wurden festgelegt, nachdem ein Prototyp gelaufen war. Sie
   entsprechen der Rundung der Referenz, aber die Wahl ist kein unabhängiger Test.
5. Die Referenzwerte sind Sekundärquelle (Chat), nicht das Ergebnis des Originalskripts.

**Befunde**
- **„1,0 % reales Wachstum je Kopf" ist (1,03 / 1,02) − 1 = 0,980 %.** Mit 0,980 %
  trifft die Rekonstruktion die Mindestquote 29,97 (29,971) und Klub 2060 mit
  649,9 gegen 651. Mit exakt 1,0 % ergeben sich 29,958 und 654,0. Der Parameter
  `wachstum_real_je_kopf = 1.0` ist damit eine gerundete Bezeichnung, nicht der
  gerechnete Wert. **Auflösung von B2 (Hypothese):** 707 (2060) und 512 (2035) passen
  zu 0,980 % (Klubwert mal 1,087: 706,5 und 512,0); 712 und 513 passen zu 1,0 % (710,9
  und 512,7; Rest −0,1 %, wie bei den Klubwerten). Die beiden Werte gehören zu zwei
  Wachstumsraten, nicht zu zwei Rechenfehlern. Am Original nicht geprüft.
- **B5: Ebene A.** Band II (v3.2) nennt 8,94 % des BIP, die Zeitpfad-Tabelle für
  2028 „A gesamt" 9,04 %. Die Differenz von 0,10 Punkten ist nicht erklärt. Der
  Pfad rechnet mit 9,04.
- **B6: Die Ausgangslage von 2024 steht im Modell als 2028.** Schuldenquote 78,4 %
  (9.537 Mrd EUR geteilt durch 12.157 Mrd EUR, Stand 2024), effektiver Zins 1,53 %
  (2024) und Verteidigung 1,401 % (COFOG 2024) werden als Werte für 2028 geführt.
  Das Auslaufen des Altbestands beginnt dadurch im Modell 2028, im Bestand aber
  schon 2024. Gleichzeitig unterstellt das Modell, dass die Schuldenquote von 2024
  bis 2028 bei 78,4 % bleibt; das ist eine Annahme (Defizite gleichen das Wachstum
  aus), keine Rechnung.
  Sensitivität (`zinsauslaufen_ab_2024_statt_2028`, `a_ohne_verteidigung_zins_bip_2028`
  unverändert): Zinsdienst 2028 1,61 % statt 1,20 %; Dividende 2028 487 statt 505
  EUR (−18 EUR, −3,6 %); 2030 478 statt 495; 2035 469 statt 471; ab 2040 gleich.
  Mindestquote 30,01 statt 29,97. Der Tiefpunkt ändert sich kaum, die ersten Jahre schon.
- **Zielzins.** Der Pfad setzt für den gesamten Altbestand 2,5 %. Der Klubdurchschnitt
  mit Garantie liegt nach der Rechnung vom 4. Oktober bei etwa 2,45 % (2,78 % Markt
  minus 31,5 Mrd EUR Ersparnis auf 9.537 Mrd EUR). 2,5 % ist also ein Mittelwert,
  nicht der Zins, den jeder Staat zahlt.

**Annahmen ohne Datengrundlage, durchgerechnet** (`pfad_sensitivitaet.csv`)

| Annahme | Wert | Mindestquote | Dividende Klub 2035 (EUR/Monat, real 2028) |
|---|---|---|---|
| Restlaufzeit | 5,0 Jahre | 30,01 % | 469 |
| Restlaufzeit | 7,5 Jahre (Zentralfall) | 29,97 % | 471 |
| Restlaufzeit | 10,0 Jahre | 29,83 % | 478 |
| Zielzins | 2,30 % | 29,85 % | 477 |
| Zielzins | 2,50 % (Zentralfall) | 29,97 % | 471 |
| Zielzins | 2,78 % (Marktzins 2024, keine Garantie) | 30,14 % | 463 |

Die Steuerquote von 30,6 % deckt alle getesteten Fälle. Der kleinste Abstand beträgt
0,46 Punkte (Zielzins 2,78 %). Das gilt für die Annahmen der Rekonstruktion, nicht
für ein Fälligkeitsprofil der zehn Staaten, das nicht vorliegt.

**Wodurch es auffiel.** Beim Gegenrechnen der Tabelle: die Mindestquote 29,97
stimmte nur mit 0,980 % statt mit 1,0 % überein, und die Zinsdienst-Reihe stimmte nur,
wenn die Ausgangslage 2024 als 2028 geführt wird.

*Skripte: `modell/pfad.py`. Dateien: `modell/parameter.toml`,
`daten/aggregate/referenz_gesamtkonzept.csv`, `pfad.csv`, `pfad_abgleich.csv`,
`pfad_sensitivitaet.csv`. Quellen der Eingaben unverändert Sekundärquellen, siehe v3.5.1.*

---

### v3.7 — Offene Punkte aus dem Chat geklärt, zweite Rekonstruktion

**Art der Änderung: MINOR** (Annahmen und offene Punkte durch Quellen ersetzt, eine neue
Rechnung). Keine Zahl des Modells ändert sich. Berichtigt werden Aussagen aus v3.5.1
und v3.6, siehe „Arbeitsfehler" unten. 5. Oktober 2026.

**Datenquelle.** Suche im Chat „Steuerkonzept von 2525 auf 3030 umstellen": Fragmente
der Originalskripte (`altschuld.py`), der Auftrag für die unabhängige Nachrechnung,
Seitentext, Tabellen. **Sekundärquelle**: die Originalskripte selbst wurden nicht
eingesehen, nur Teile ihres Codes und ihrer Ausgabe im Chat.

**Was geklärt ist**
- **B5, kein Widerspruch.** 8,94 % ist die A-Summe der Rahmenstruktur *mit* Verteidigung
  bei 2,50 % (Ziel 2035). Im Startjahr steht Verteidigung bei 1,40 %: A-Aufgaben 2028 =
  8,94 − 2,50 + 1,40 = 7,84 %; mit Zinsdienst 1,20 % ergibt das 9,04 %. 2035:
  8,94 + 1,55 = 10,49 %. Eine frühere Tabelle im Chat nennt genau diese
  Aufteilung (A-Aufgaben 7,84 und 8,94, Zinsdienst 1,20 und 1,55).
- **6,44 ist abgeleitet, keine Restgröße.** 6,44 = 3,75 + 0,77 + 0,74 + 0,30 + 0,30 +
  0,29 + 0,29 (die sieben A-Posten ohne Verteidigung) = 8,94 − 2,50. Die Spalte 2028 der
  Zeitpfad-Tabelle ist damit ein **unabhängiger** Test, nicht nur eine Kalibrierung.
- **B2, nachgerechnet.** Die Sensitivitätstabelle koppelt das nominale Wachstum an das
  reale: g_nominal = (1 + r) × (1 + 2,0 %) − 1. Die Zeile „1,0 % Zentralfall" rechnet
  also mit 3,02 % nominal, der Seitentext mit 3,0 % nominal und damit 0,980 % real.
  `modell/pfad.py` trifft alle zehn Werte der Tabelle (2035 und 2060, fünf Zeilen) auf
  höchstens 0,8 EUR und die Textwerte 512 und 707 auf 0,03 bzw. 0,5 EUR. Ohne die
  Kopplung weicht die Zeile 2,0 % um bis zu 20 EUR ab. Der Chat gibt die Rechenvorgabe
  selbst an („das reale Wachstum je Kopf ist also (1.03/1.02 - 1)").
  **Folge:** Seitentext (707 EUR) und Tabelle (712 EUR) sind zwei verschiedene Läufe
  mit 0,02 Punkten Unterschied im nominalen Wachstum, nicht ein Rechenfehler. Dass beide
  als „Zentralfall" auf derselben Seite stehen, bleibt ein Darstellungsproblem.
- **Obergrenze von A: Bezugsgröße geklärt.** 36 % beziehen sich auf den **Einzug von A**
  = 30,60 − 0,82 = 29,78 % des BIP. Gegenrechnung: 36 % × 29,78 = 10,72 % des BIP;
  geteilt durch 78,4 % Schuldenquote 13,7 % (Seitentext: 13,7 %); A 2028 mit 9,04 %
  geteilt durch 78,4 % ergibt 11,5 % (Seitentext: 11,5 %). Der Höchstbedarf von 10,49 %
  des BIP (2035) entspricht 35,2 % des Einzugs. Die ältere Angabe 40 % bezog sich auf
  eine überholte Fassung mit Steuerquote 27,91 % (10,49 / 27,09 = 38,7 %).
- **Territorialer Aufschlag: Einheit geklärt, nachgerechnet.** Einheit EUR je Kopf und
  **Jahr** (Startjahr, schmilzt über dreißig Jahre ab), nominal 2028 (die Rechnung nutzt
  die nominale BIP-Fortschreibung; ausdrücklich dokumentiert ist die Preisbasis nicht).
  `modell/aufschlag.py` ergibt +253 EUR (Frankreich) bis −726 EUR (Irland) gegen +254
  und −728 in Korrektur 44; Summe über alle Gebiete null. Die Abweichung von 1 bis 2 EUR
  liegt vermutlich an gerundeten Schuldenquoten (Summe 78,45 % gegen 78,4 %).
- **B3, überholt, nicht entschieden.** Beide Werte meinen 2028. 4.884 Mrd EUR nennt der
  frühe Audit (Band I, v3.0) als „amtlich fortgeschrieben", ohne Quelle für den Pfad.
  4.914,9 Mrd EUR ergibt sich aus Eurostat-Ist 2024 (4.329,0) mal 1,13535 (= 1,033 ×
  1,028 × 1,038 × 1,03) und ist seit v3.3 die Basis. Differenz 30,9 Mrd EUR = 0,63 %.
  Woher 4.884 stammt, bleibt unbekannt; die Basis ändert sich dadurch nicht.
- **B4, Sachstand geklärt, Entscheidung offen.** Das Klubmodell rechnet mit dem
  **BIP** Irlands: 561.940 Mio EUR (Eurostat `nama_10_gdp`, 2024) in der Länderliste, und
  der Seitentext nennt Irlands BIP je Kopf das 2,19-Fache des Klubschnitts (Nachrechnung:
  118.240 EUR gegen 54.120 EUR = 2,185, 2028). Die ältere Seitenfassung „Klub der Neun"
  rechnete die Dividendenkosten für Irland dagegen mit GNI\* (334,0 gegen 602,4 Mrd EUR,
  2025). Beide Bezugsgrößen stehen also im Konzept. **Größenordnung** bei Ersatz durch
  GNI\* (Annahme: Verhältnis 0,5545 aus 2025 gilt auch 2024): Klub-BIP 2024 um etwa
  250 Mrd EUR (2,1 %) niedriger, Schuldenquote 80,1 % statt 78,4 %, Dividende im
  Klubschnitt etwa 2 % niedriger (rund 496 statt 506 EUR 2028). Einfache Skalierung,
  keine Neurechnung der Anteile.
- **B6, präzisiert.** Der Seitentext nennt „10,8 Billionen EUR = 78,4 %". Das ist 78,4 %
  des **BIP 2028** (0,784 × 13.803 = 10.822 Mrd EUR). Der Eurostat-Stand 2024 beträgt
  9.537 Mrd EUR. Das Modell unterstellt damit, dass der Schuldenstand von 2024 bis 2028
  um 13,5 % in Euro wächst (Quote konstant), ab 2028 aber konstant bleibt, und dass das
  Auslaufen des Altbestands erst 2028 beginnt. Der Seitentext nennt kein Bezugsjahr.
  Sensitivität unverändert (v3.6).
- **Zwei Fassungen im Chat.** Eine ältere Zeitpfad-Tabelle (Dividende 8,52 %, 396 EUR
  Klub, 418 EUR Deutschland, Steuerquote 27,91 %) steht im selben Chat und ist
  überholt. Maßgeblich sind 30,6 % und die Tabelle in v3.6.

**Was neu ist:** `modell/aufschlag.py`, `daten/aggregate/laender_2024.csv` (Länderliste,
Sekundärquelle, an der Quelle zu prüfen), `aufschlag.csv`; in `pfad.py` der Abgleich der
Sensitivitätstabelle (jetzt 35 Referenzwerte); Parameter `obergrenze_a_anteil_einzug`
(30 Parameter); berichtigte Hinweise zu `a_ohne_verteidigung_zins_bip_2028`,
`b_fachaufgaben_bip_2028`, `dividende_de_monat_2060`, `wachstum_real_je_kopf`.

**Wodurch es auffiel.** Suche nach 8,94 und 9,04 im Chat; dabei erschien die Tabelle
mit 7,84 + 1,20. Die Abweichung der 0,0-Zeile der Sensitivitätstabelle (−13 EUR in 2060)
legte die Kopplung nahe.

**Beweiskraft.** Wie in v3.6: Rekonstruktion, Übereinstimmung ist kein Beweis für das
Original. Neu ist, dass dieselbe Struktur nun drei voneinander getrennte Tabellen trifft
(Zeitpfad, Sensitivität, Aufschlag) und dass die Kopplungsannahme aus dem Chat selbst
stammt und nicht aus meiner Anpassung. Die Kopplung wurde aber nach Sicht der Abweichung
getestet; ihre Wahl ist deshalb nur durch die zehn Treffer gestützt, nicht vorab festgelegt.

*Skripte: `modell/pfad.py`, `modell/aufschlag.py`. Quellen wie v3.6, Sekundärquelle Chat.*

---

## 4 | Korrekturen, Fortsetzung

Keine neue nummerierte Korrektur. **Die Nummer 47 ist frei.** Ob Punkt B1 unten als
Korrektur geführt wird, entscheidet der Verfasser.

### Arbeitsfehler beim Aufbau des Repositorys

Fehler des KI-Systems bei der Arbeit an diesem Repository. Sie betreffen die
Übertragung, nicht das Modell, und sind deshalb nicht nummeriert.

| Was war falsch | Richtig | Wodurch auffiel |
|---|---|---|
| Behauptet, die Sitzung sei keinem Projekt zugeordnet | Sie war an das Projekt „2525" gebunden; die Suche lief auf dessen Chats | Treffer des Chats „Steuerkonzept von 2525 auf 3030 umstellen" |
| Die hochgeladene Datei als Band I behandelt | Sie war der Stand v0.9 (1. Oktober 2026), nicht der Projektstand v3.1. Nicht committet | Kopfzeile und Versionsüberschriften der Datei |
| Zwischenhypothese: die Dividendenreihe beruhe auf einer Bezugsgröße von rund 235 Mio Personen, mögliche Folge „Zahlen in verschiedenen Einheiten nebeneinander" | Die Reihe gilt für Deutschland; das Verhältnis zum Klubschnitt (1,087) erklärt alles. Die Hypothese stand kurz als Befund in `nicht-eingetragen.md` (Commit `262e984`) und ist in `23b7050` korrigiert | Suche im Chat des Gesamtkonzepts |
| v3.6: `a_ohne_verteidigung_zins_bip_2028` (6,44) als aus der Dividende 2028 zurückgerechnete Restgröße geführt; daraus gefolgert, die Spalte 2028 sei kein unabhängiger Test | 6,44 ist die Summe der sieben A-Posten ohne Verteidigung (= 8,94 − 2,50). Die Spalte 2028 ist ein unabhängiger Test. Die Übereinstimmung mit der Restgröße 6,439 ist keine Kalibrierung | Suche nach 8,94 und 9,04 im Chat (v3.7) |
| v3.6: Punkt B5 („0,10 Punkte ungeklärt") als Unstimmigkeit geführt | Kein Widerspruch: 8,94 enthält die Verteidigung mit 2,50, die Tabelle 2028 rechnet mit 1,40 (8,94 − 2,50 + 1,40 + 1,20 = 9,04). Ich hatte die Herkunft im Chat nicht gesucht, bevor ich den Punkt eintrug | wie oben |
| v3.6: Die Zahl „etwa neun unabhängige Werte" | Zu niedrig, weil die Spalte 2028 und die Konstante 6,44 als abhängig gezählt wurden | wie oben |
| Commit-Nachricht von `23b7050` nennt „26 gesamt" | Es sind 25 Parameter | Zählung im Lauf-Skript. Die Nachricht wurde nicht per Force-Push geändert |

**Ablaufnotiz, kein Fehler.** Der Push des Tags `v3.5` wurde von der Verbindung dieser
Sitzung mit HTTP 403 abgelehnt, der Push des Branches nicht. Der Tag wurde danach
über ein GitHub-Release am Commit `a5808b1` gesetzt. Die Ursache der Ablehnung ist
nicht geklärt.

---

## 7 | Offene Punkte, Stand v3.7

| Punkt | Status |
|---|---|
| **B1: Dokumentationslücke Dividendenreihe** | **neu, 5. Oktober 2026.** Band II (Korrektur 43) nennt 550 → 512 → 707 € ohne Bezugsgruppe („Deutschland") und ohne Zeiteinheit („je Monat"). Inhaltlich aufgelöst, im Logbuch nicht vermerkt. Ob Korrektur 47, entscheidet der Verfasser |
| **B2: 707 gegen 712 €** | **nachgerechnet in v3.7.** Seitentext: 3,0 % nominal (0,980 % real). Tabelle: nominales Wachstum an das reale gekoppelt, Zeile 1,0 % hat 3,02 % nominal. Alle zehn Tabellenwerte auf höchstens 0,8 EUR getroffen. Offen bleibt nur die Darstellung: zwei „Zentralfälle" auf einer Seite. Welche Zahl gilt, entscheidet der Verfasser |
| **B3: BIP Deutschland 2028** | **überholt, geschlossen in v3.7.** Beide Werte meinen 2028. 4.914,9 hat eine dokumentierte Herleitung und ist seit v3.3 Basis. Quelle von 4.884 unbekannt (Differenz 0,63 %) |
| **B4: Irland, BIP oder GNI\*** | **Sachstand geklärt in v3.7, Entscheidung offen.** Das Klubmodell rechnet mit BIP (Länderliste, Faktor 2,19 im Seitentext). Die ältere Seitenfassung „Klub der Neun" rechnete mit GNI\*. Ersatz durch GNI\* senkte das Klub-BIP um etwa 2,1 %, die Dividende um etwa 2 % (Größenordnung). Welche Bezugsgröße gilt und wie sie ausgewiesen wird, entscheidet der Verfasser |
| **B5: Ebene A 8,94 % gegen 9,04 %** | **geschlossen in v3.7, war kein Widerspruch** (8,94 enthält Verteidigung 2,50, die Tabelle 2028 rechnet mit 1,40) |
| **B6: Ausgangslage 2024 als 2028** | **offen, präzisiert in v3.7.** Schuldenquote 78,4 % gilt im Seitentext als Quote 2028 (10,8 Bio EUR), der Eurostat-Stand 2024 sind 9,537 Bio EUR. Effektiver Zins (1,53 %) und Verteidigung (1,401 %) stammen aus 2024. Entscheidung des Verfassers nötig, ob das Auslaufen des Altbestands 2024 oder 2028 beginnt (Sensitivität in v3.6) |
| **Rechenskripte** | `pfad.py` (seit v3.6, 35 von 35 Referenzwerten) und `aufschlag.py` (seit v3.7) sind **Rekonstruktionen**, nicht Originale. Es fehlen weiterhin `basis.py`, `final.py`, `tilgung.py` (Band II) und alle Skripte bis v3.4. Aus diesem Repository reproduzierbar ist der Zeitpfad ab den Parametern, nicht die Herleitung der Parameter (Kalibrierung, COFOG-Anteile, 6,44 und 10,35) |
| **Herleitung von 6,44 und 10,35** | Beide sind Summen der COFOG-abgeleiteten Posten aus Band II (v3.2): 6,44 für Ebene A ohne Verteidigung, 10,35 für Ebene B. Die zugrunde liegenden Eurostat-Abrufe (COFOG, zehn Staaten) liegen nicht vor, die Shell erreicht `ec.europa.eu` nicht. Nachgerechnet sind die Summen der Posten, nicht die Posten |
| **Nicht eingetragene Größen** | Mindestquote, Obergrenze von A, Höchstbedarf, territorialer Aufschlag: Bezugsjahr oder Bezugsgröße fehlt. Siehe `daten/aggregate/nicht-eingetragen.md`, Abschnitt A |
| **Rohdaten und Abrufe nicht reproduzierbar** | Die Eurostat-Abrufe (zehn Einzelabrufe COFOG GF02, `gov_10a_exp`, `gov_10a_taxag`, `nama_10_gdp`, `demo_gind`) sind im Logbuch nur benannt, die Abrufergebnisse liegen nicht vor. Die Shell erreicht `ec.europa.eu` nicht (Logbuch v3.1) |
| **Prüfstand der Logbuch-Abschrift** | Band I ab v0.10 und Band II sind Abschriften ohne Vergleichsquelle, siehe `HERKUNFT.md` |
| Alle offenen Punkte aus Band I (Abschnitt 7) und Band II (Zusatz zu v3.5) | unverändert, soweit hier nicht genannt |
