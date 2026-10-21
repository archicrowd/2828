# TAX 28:28 — Logbuch, Band III: ab v3.5.1

**Fortsetzung von `Versionsgeschichte-TAX-2828-BandII.md`.** Band II endet mit
v3.5 und Korrektur 46. Dieser Band führt ab v3.5.1 weiter und ist der erste, der
direkt in diesem Repository entsteht und nicht aus dem Projektraum übernommen
wurde.

Stand: 21. Oktober 2026 · Modellstand **v4.23**

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

### v3.8 — Vollständiges Logbuch und Originalskripte aus dem Export, Lückenaussage berichtigt

**Art der Änderung: MINOR** (Rekonstruktionen werden an Originalen geprüft, ein vollständiger
Logbuchband ersetzt eine unvollständige Abschrift). Keine Zahl des Modells ändert sich.
5. Oktober 2026.

**Datenquelle.** Paket `6001ff54-2828-export.zip`, vom Vorchat „Steuerkonzept von 2525 auf
3030 umstellen" aus dessen Ausgabeordner zusammengestellt (171 Dateien) und hier
hochgeladen. **Sekundärquelle** im Sinne von `CLAUDE.md`: Es ist das Material des Verfassers,
aber nicht amtlich. Die Eurostat-Werte darin sind feste Zahlen in `basis.py`, an Eurostat
nicht geprüft (die Shell erreicht `ec.europa.eu` nicht).

**Was neu im Repository liegt**
- `logbuch/Versionsgeschichte-TAX-2828.md` (Band I) ist jetzt die **Originaldatei**: 1.070 Zeilen,
  v0.1 bis v3.4, Korrekturen 1 bis 41. Vorher lag eine Abschrift bis v3.1 vor.
- `modell/rahmen/`: sieben Originalskripte des Rahmenmodells (`basis.py`, `pfad.py`, `final.py`,
  `tilgung.py`, `aufschlag.py`, `altschuld.py`, `kurve.py`), unverändert kopiert.
- `modell/vergleich_original.py` und `daten/aggregate/vergleich_original.csv`: Zweitrechnung
  (`modell/pfad.py`, `modell/aufschlag.py`) gegen die Originale.

**Prüfung der Logbuch-Abschrift.** Band II im Repository ist zeilengleich mit dem Original
(`diff`: 0 Zeilen Unterschied, SHA-256 `438a4cd8…`). Band I im Repository war bis v3.1 bis auf
einen Zeilenumbruch (Zeilen 664/665) gleich dem Original; es fehlten v3.2 bis v3.4 und die
Korrekturen 31 bis 41. Damit ist der in `HERKUNFT.md` genannte „ungeprüfte" Teil geprüft.

**Berichtigung der Lückenaussage.** Band II behauptet, die Einträge v3.2 bis v3.4 und die
Korrekturen 31 bis 41 seien verloren. Das ist falsch (Korrektur 47). Ich habe die Aussage in
`README.md`, `CLAUDE.md`, `HERKUNFT.md` und in Band III (v3.5.1 bis v3.7) übernommen, ohne den
Ausgabeordner des Vorchats prüfen zu können; das ist ein eigener Fehler (siehe Arbeitsfehler).

**Befunde aus dem Vergleich mit den Originalskripten**
1. **Zeitpfad bestätigt.** `final.py` liefert im Zentralfall für Deutschland 550 € (2028), 512 €
   (2035, Tiefpunkt) und 707 € (2060) bei 0,980 % realem Wachstum je Kopf (= 1,03/1,02 − 1);
   die Zweitrechnung trifft alle 33 Jahreswerte des Dividendenanteils innerhalb 0,01 Punkten.
2. **B2 gegen das Original bestätigt.** `tilgung.py` rechnet die Sensitivität mit
   g_nom = (1+g)·1,02 − 1; die Zeile „1,0 %" liefert 513 € (2035) und 712 € (2060). Die
   Abweichung 707/712 ist die Kopplung des nominalen an das reale Wachstum, wie in v3.7 vermutet.
3. **Mindestquote.** Original: 30,611 % ohne reales Wachstum (Bisektion auf `KOPF_DE`), 29,97 %
   in Preisen von 2028. Die Zweitrechnung nennt 30,616 %: sie skaliert 479 € mit 506/550 statt
   direkt mit `KOPF_DE`. Differenz 0,005 Punkte, Näherungsfehler der Zweitrechnung.
4. **Obergrenze von A.** `pfad.py`: Höchstbedarf 10,49 % (2035) geteilt durch 29,78 %
   (Einzug) = 35,2 %; „vertraglich" wird `round(35,2 + 0,8)` = 36 %. Die 36 % sind also eine
   **Setzung mit Aufschlag von 0,8 Punkten**, nicht abgeleitet. In v3.4 (Original) stand noch 40 %.
5. **Territorialer Aufschlag.** `aufschlag.py` liefert +254 (FR) bis −728 (IE) EUR je Kopf und
   Jahr, die Zweitrechnung +253 bis −726; die Differenz stammt wahrscheinlich aus den Einwohnerzahlen (Befund 6; nicht getrennt nachgerechnet).
   Das Skript druckt „null, wie gefordert", rechnet aber 0,0955 Mrd EUR, weil `D_START` dort
   auf den gerundeten Wert 78,4 gesetzt ist (berechnet: 78,445). Rundungsartefakt, kein Fehler im Verfahren.
6. **Einwohnerzahlen weichen ab.** Für acht Länder (ES, NL, IE, BE, AT, DK, SI, EE) liegen die
   Werte in `daten/aggregate/laender_2024.csv` um 0,004 bis 0,076 Mio (bis 0,16 %) über denen
   in `basis.py`; DE und FR sind gleich. Welche stimmen, ist ohne Eurostat-Zugriff nicht zu
   entscheiden. Für die Gesamtkonzept-Zahlen maßgeblich ist `basis.py`. Die Datei `laender_2024.csv`
   wird **nicht geändert**, solange die Quelle nicht geprüft ist.
7. **`altschuld.py` ist eine andere Methode als `aufschlag.py`.** `altschuld.py` bemisst den
   Beitrag je Kopf am Klubschnitt (+185 FR bis −531 EE), `aufschlag.py` am BIP des Gebiets
   (+254 FR bis −728 IE). Beide stehen in `modell/rahmen/`; der Gesamtkonzept-Wert stammt aus
   `aufschlag.py`. Dass die Spanne vom Bemessungsprinzip abhängt, steht bisher nirgends im Text.
   Die in `altschuld.py` gedruckte Zahl „Dokument nennt +364 bis −1.045" ist der Wert aus v3.4.
8. **Gegenprobe zur alten Quote.** Bei 27,91 % liegt die Dividende 2028 bei 418 € (DE, Preise
   2028) und unterschreitet 479 € in 25 Jahren (2028 bis 2052); ohne reales Wachstum in allen 33.
9. **Aktive Tilgung** (0,50 % des BIP, `tilgung.py`): Dividendenverzicht 25 € je Monat im
   Startjahr, kumuliert −5.859 € je Kopf bis 2050; Break-even nach 2070.
10. **Basis-Probe.** `basis.py` meldet selbst: Klub-BIP 2028 aus der Fortschreibung des Istwerts
    13.802,7 Mrd €, im Dokument 14.227 (Faktor 1,17024 der alten Kalibrierung, 3,07 % höher).
    Welche Beträge in `TAX-2828-Gesamtkonzept.docx` auf welcher Basis stehen, ist **noch nicht
    geprüft**; die Datei liegt im Export, aber noch nicht im Repository.
11. **v3.4 im Original.** Dort gilt Quote 27,91 %, Obergrenze 40 %, Dividende Klub 396 € (2028)
    und 941 € (2060), Gesamtlast 35,66 %. Die Quote 30,6 % gehört erst zu v3.5
    (Korrekturen 42 bis 46). Die „Rekonstruktion" in Band II schreibt sie v3.4 zu (Korrektur 48).

**Nicht gelesen.** `zahlen.py`, `pfad.json`, `zahlen.json`, `gesamtkonzept-bau.js`, das Gesamtkonzept
selbst und alle übrigen Pakete (Kern, Webseite, Dokumente, Einzelrechnungen, Uploads).

**Noch nicht ins Repository übernommen.** Eine Sammelkopie des restlichen Exports wurde in
dieser Sitzung vom Berechtigungsfilter abgelehnt und nicht umgangen. Offen ist deshalb, ob und
wie `modell/kern/`, `seite/`, `dokumente/`, `modell/rechnungen/` und das Manifest der Drittdateien
(SHA-256, ohne die Dateien) eingecheckt werden. Die Drittdateien (PDF, xlsx) gehören nicht hinein.

*Skripte: `modell/rahmen/*.py` (Original), `modell/vergleich_original.py`. Quelle: Export des Vorchats.*

---

### v3.9 — Übernahme des Exports, Einwohnerzahl berichtigt, Wegweiser

**Art der Änderung: MINOR** (Quelle ersetzt Annahme: Einwohnerzahl; neue Dateien kommen hinzu).
6. Oktober 2026. Auftrag des Verfassers: Dateien lesen und danach einchecken (Frage 1), Band II im
Projektraum berichtigen (Frage 2), übrige Entscheidungen nach meinem Ermessen (Frage 3).

**Bewegte Zahl.** Klub-Einwohner 2024: **255,1 → 254,8 Mio** (Parameter `klub_einwohner_2024`).
Folge: Mindestquote der Zweitrechnung 29,960 → 29,965 % (zentral) und 30,604 → 30,610 % (streng),
Original 29,966 und 30,611. Dividende Klub 2028: 505,4 → 506,0 € je Monat, wie im Gesamtkonzept.
Neuer Parameter `de_einwohner_2024` (83,516593 Mio). Keine Zahl des Gesamtkonzepts ändert sich.

**Wodurch es auffiel.** Das Gesamtkonzept (Abschnitt 9) nennt 254,8 Mio; die Summe der Einwohner in
`basis.py` ist 254.823.736. Logbuch Band I (v3.1) und mein Parameter nannten 255,1 Mio. Ursache der
Differenz im Logbuch nicht geklärt; ob sie Korrektur 49 wird, entscheidet der Verfasser (zusammen
mit B1). `daten/aggregate/laender_2024.csv` übernimmt seitdem die Einwohnerzahlen aus `basis.py`.

**Zweitrechnung angeglichen.** Die Mindestquote der Zweitrechnung rechnet wie das Original auf das BIP
je Kopf Deutschlands (`final.py`) statt über das Verhältnis 506/550. `vergleich_original.py` prüft jetzt
56 Größen (Einwohner, 33 Jahreswerte, Mindestquote zweifach, zehn Aufschläge), alle innerhalb der
Toleranz (Mindestquote 0,0009 Punkte, Aufschlag höchstens 1,5 €).

**Was neu im Repository liegt** (Quelle: Export des Vorchats; Sekundärquelle)
`modell/rahmen/zahlen.py`; `modell/kern/` (nationales Gesamtmodell); `modell/rechnungen/` (R1 bis R16,
ohne die Rechercheliste); `modell/audit/`; `seite/` (acht Sprachfassungen, zwei Builds, Seite zum Stand B);
`dokumente/` (Gesamtkonzept als PDF und Word, ältere Dokumente, Bauskript); `archiv/uploads-eigen/`;
`daten/herkunft/uploads-manifest.csv` (sieben Drittdateien mit Größe und SHA-256, ohne die Dateien);
`daten/aggregate/rahmen_original/` (zwei JSON-Ausgaben des Originals); `INDEX.md` und je Bereich eine
`LIESMICH.md`. Nicht eingecheckt: Drittdateien, OECD-Rohdaten, Rechercheliste (persönliche E-Mail-Adressen
von sechs externen Forschenden). Die Datei `.gitignore` bleibt unverändert.

**Gelesen und nicht gelesen.** Vollständig gelesen: Gesamtkonzept (PDF), `basis.py`, `pfad.py`, `final.py`,
`tilgung.py`, `aufschlag.py`, `altschuld.py`, `kurve.py`, `zahlen.py`, beide JSON-Dateien; vom Logbuch
Band II und III vollständig, von Band I der Eintrag v3.4, der Beginn von v3.2, die Korrekturen 31 bis 41 und
Abschnitt 7. Nur im Kopf gelesen: alle übrigen Python-Dateien (Docstring), `modell-2828.py` (Kopf), die
Seiten (Titel, externe Verweise), die ersten Zeilen der Word- und Markdown-Dokumente. Nicht gelesen:
Rechnungsergebnisse, Befunddateien, Quelltext der Seite im Einzelnen, `gesamtkonzept-bau.js`. Der
Hinweis in den `LIESMICH.md` gilt entsprechend. Durchsuchung nach Zugangsdaten und Adressen: nur
die Adresse `2828@archicrowd.de` der Seite und die Forscher-Adressen (ausgeschlossen) gefunden.

**Befunde beim Lesen des Gesamtkonzepts**
1. **B10 geschlossen.** Das Gesamtkonzept steht auf der korrigierten Basis (Klub-BIP 13.803 Mrd €,
   Aufkommen 16.575 € je Kopf, Dividende 6.072 €, Formel 3.602/12.636 €). Die Spalte „Dokument" in
   `pfad.py` bezeichnet die Vorfassung, nicht diese Datei.
2. **Wortlaut der Obergrenze.** Die Einleitung sagt, der Klub dürfe „höchstens 36 % des Aufkommens
   behalten", Abschnitt 1.2 „36 % dessen, was A einzieht". Das sind verschiedene Bezugsgrößen (30,60 gegen
   29,78 % des BIP; 11,0 gegen 10,72 % des BIP). Gerechnet ist die zweite (B13).
3. **B12: Deckung der Quote.** Das Gesamtkonzept nennt als Gegenfinanzierung „Verbrauch, CO₂, Boden und
   Unternehmen", rechnet sie aber nicht. Die Quote 30,6 % ist aus dem Versprechen von 479 € abgeleitet, nicht
   aus den Steuerpositionen aufgebaut. Das nationale Modell (Stand A) lieferte 27,91 % (Band I, v3.4).
4. **Dividendenversprechen.** Die Tabelle im Gesamtkonzept nennt 1,0 % realen Wachstum, die Rechnung
   0,980 % (3,0 % nominal, 2,0 % Preise). Bekannt aus B2; das Dokument sagt „1,0 %" und nennt
   daneben 707/512 € (Text) und 712/513 € (Tabelle).
5. **Veröffentlichte Seite.** `archicrowd.de` zeigt nach einem Abruf in dieser Sitzung den älteren
   Build (Tarif 0/9/16/21/26/28, Mehrwertsteuer 5/11/17/22/28), mit `noindex`. Kurzauszug des Abrufwerkzeugs,
   nicht Zeile für Zeile verglichen. Das Impressum der Seite nennt eine Person mit Namen.

**Projektraum.** Band I (vollständig), Band II (mit Berichtigungshinweis) und Band III sind im Projekt
„2525" unter `claude/` aktualisiert beziehungsweise neu angelegt; die Änderung erfolgte auf Weisung
des Verfassers. Der Projektraum wird nicht automatisch nachgeführt: nach jeder Version ist er neu
zu schreiben (Abweichung vom Wortlaut von `CLAUDE.md`, die das Repository als maßgeblich führt).

*Skripte: `modell/vergleich_original.py`, `modell/pfad.py`. Quellen: Export des Vorchats, Gesamtkonzept
vom 4. Oktober 2026.*

---

### v3.10 — Projektverwaltung: Bausteinregister, Aussagenregister, Schnittstelle für Dritte

**Art der Änderung: MINOR** (neue Rechnungen und Prüfungen, eine Annahme durch das Original ersetzt).
6. Oktober 2026. Auftrag des Verfassers: Überblick über alle Teile behalten, das Ineinandergreifen der
Bausteine sichern, Rechenwege prüfen und zusammenfassen, Datenverlust vermeiden.

**Bewegte Zahl.** `verteidigung_basis_cofog_2024`: **1,401 → 1,40 % des BIP**. Alle acht Originalskripte
und das Gesamtkonzept rechnen mit 1,40; die 1,401 stand nur im Logbuch. Wirkung rund 0,001 Punkte des BIP;
die Abgleiche bleiben innerhalb der Toleranz. Aufgefallen durch den neuen Konstantenvergleich.

**Neu**
- `modell/kennzahlen.py`: rund 160 benannte Größen aus den Originalskripten (`daten/aggregate/kennzahlen.csv`).
- `dokumente/aussagen.csv`, `modell/pruefe_aussagen.py`: 131 Zahlen des Gesamtkonzepts und der Seite zum
  Stand B mit Sollwert, Einheit, Toleranz und Kennzahl. Ergebnis: alle innerhalb der Toleranz, eine bekannt
  abweichend (A113, siehe B14). Die Sollwerte wurden von Hand aus der PDF übertragen: ein Tippfehler dort fiele
  auf, ein im Dokument und im Skript gleich falscher Wert nicht.
- `modell/pruefe_konstanten.py`: vergleicht die im Skript fest stehenden Konstanten der Originale mit
  `parameter.toml` (ast, ohne Ausführung). Die Originale führen dieselben Konstanten bis zu achtmal doppelt.
  `modell/rechnungen/pfad/dyn.py` (Verteidigungsziel 3,5 %) wird als veraltet gemeldet.
- `projekt/bausteine.csv` (19 Bausteine), `projekt/nahtstellen.csv` (11 Nähte), `projekt/pruefsummen.sha256`
  (Originale), `projekt/pruefe_projekt.py` (Register gegen Dateisystem, einheitlicher Modellstand, lückenlose
  Korrekturnummern, keine fremden E-Mail-Adressen, keine Rohdatenformate, Prüfsummen).
- `modell/alles.py`: ein Befehl für alle acht Stufen (letzter Lauf 8 von 8 ohne Fehler).
- `schnittstelle/` (Entwurf Mikrosimulation, Ergebnisformat, Formprüfung), `beitraege/`, `CONTRIBUTING.md`,
  `CITATION.cff` (Autor und Projektverantwortlicher: Arndt Hermann), `LIZENZ-VORSCHLAG.md` (keine Lizenz
  festgelegt, keine Rechtsberatung).

**Befunde aus dem Vorchat** (nur Suche in den Textstellen; Sekundärquelle, der Chat wurde nicht befragt)
1. **B12 bestätigt.** Der Chat nennt 30,6 % ausdrücklich abgeleitet (Quote, bei der die Dividende 479 EUR hält).
   In v3.1 steht 31,20 % Bedarf gegen 27,91 % Erhebung (Lücke 3,29 Punkte). Eine Aufstellung, wie die
   Steuerpositionen 30,6 % aufbringen, wurde nicht gefunden.
2. **B9 teilweise geklärt.** Chat-Code: Höchstbedarf 2035 = 35,2 % des Einzugs, „Deckelung 36 %". Der Abstand
   von 0,8 Punkten ist die Aufrundung auf volle Prozent; eine Begründung als Sicherheitsabstand steht nicht dabei.
3. **B7 Quelle gefunden.** 255,1 Mio stammen aus `modell/rechnungen/rahmen/daten.py` (v3.1), 254,8 Mio aus
   `basis.py` (v3.5) und dem Gesamtkonzept. Warum acht Länder abweichen, sagt der Chat nicht.
4. **B14 neu.** Gesamtkonzept und Chat: Steuern 25,95 + Sozialbeiträge 14,88 = 40,83, genannt wird 40,76.
   Differenz 0,07 Punkte (rund 10 Mrd EUR), ungeklärt. Die Entlastung von 2,41 Punkten bezieht sich auf 40,76.

**Soll der Vorchat nochmals befragt werden?** Ja, gezielt und mit Verlangen nach Fundstelle (Datei, Zeile):
B9 (Begründung des Aufschlags), B7 (Abrufdatum), B12 (gibt es eine Aufbaurechnung der Quote?), B14 (Herkunft
von 40,76), B8 (Wahl der BIP-Bemessung). Der Vorchat hat sich schon einmal geirrt (Korrektur 47) und bleibt
Sekundärquelle, bis eine Datei die Antwort belegt. Entscheidungen des Autors (B4, B6, mittlere Tarifstufen)
kann er nicht treffen.

*Skripte: siehe oben. Quellen: Gesamtkonzept vom 4. Oktober 2026; Vorchat (Sekundärquelle).*

---

### v3.11 — Korrektur 49 (Einwohnerzahlen), B14 geschlossen, B8 geklärt

**Art der Änderung: PATCH** (Eingangsdaten der Zweitrechnung korrigiert; Originalskripte und Gesamtkonzept unverändert).
6. Oktober 2026. Auftrag des Verfassers: notwendige Korrekturen ausführen, kleine Fehler begradigen und runden.

**Bewegte Zahl.** `klub_einwohner_2024`: **254,8 → 255,061 Mio**; acht Länderwerte in `laender_2024.csv` ersetzt
(ES, NL, IE, BE, AT, DK, SI, EE). Datenquelle: Eurostat `demo_gind`, Indikator AVG, 2024, zehn Staaten einzeln am
6. Oktober 2026 abgerufen (Web-Abruf, Antwort maschinell gelesen, an der Quelle zu prüfen). Aufgefallen durch den Hinweis des
Vorchats (Sekundärquelle) und anschließenden Abruf. Alle zehn Werte stimmen mit `daten.py` überein; `basis.py` weicht bei acht ab
(DE und FR gleich). Die Summe steigt um 0,24 Mio; die Kopfbeträge sinken um 0,09 %.
`alles.py`: 8 von 8 Stufen ohne Fehler; die Einwohnerzeilen in `vergleich_original.csv` weichen gegen `basis.py` ab (gemeldet, informativ).

**Bewusst nicht geändert.** `modell/rahmen/basis.py` (Prüfsumme) und das Gesamtkonzept rechnen weiter mit 254,8 Mio.
Gemäß Rundungsvorgabe des Verfassers gelten die Abweichungen des Konzepts (Formel 3.602/12.636 statt etwa 3.599/12.625; Dividende
505,5 gegen 506 EUR je Monat) als kleine Fehler; sie sind hier offen benannt und werden bei der nächsten Überarbeitung des Konzepts
neu gerechnet. Die Aussage A121 prüft das Konzept und bleibt bei 254,8.

**Weitere Einträge.**
- **B14 geschlossen (keine Korrektur).** 40,76 % ist das Eurostat-Aggregat `D2_D5_D91_D61_M_D995`; die Posten summieren sich
  BIP-gewichtet auf 40,82 (eigene Nachrechnung: 25,947 + 14,877 = 40,823 gegen 40,760, Differenz 0,063). Dänemark meldet
  D995 = 0,3 % des BIP (Eurostat `gov_10a_taxag`); für die übrigen Länder nicht abgerufen, ein Rest ist Rundung der Posten auf eine
  Nachkommastelle. Es fehlt im Gesamtkonzept eine Fußnote; Aussage A113 bleibt „bekannt".
- **B8 geklärt.** `altschuld.py` ist laut Vorchat ein verworfener erster Versuch; die BIP-Bemessung folgt aus der Finanzierung nach
  BIP-Anteil (Gesamtkonzept Abschnitt 5). In `modell/LIESMICH.md` als überholt gekennzeichnet. Sekundärquelle, aus dem Konzepttext
  nachvollziehbar.
- **B9.** Die Obergrenze 36 % ist eine Aufrundung (35,2 + 0,8, `pfad.py`). Nach Angabe des Vorchats (Tabelle nicht nachgerechnet)
  trägt sie Einzelabweichungen und deren Häufung (36,0 %), nicht aber 3,5 % Verteidigung (38,6 %). Entscheidung des Autors.
- **B12.** Nach Angabe des Vorchats gab es nie eine Aufbaurechnung der Quote; sie entsteht über das Dividendenversprechen. Lücke zum
  nationalen Modell 2,69 Punkte (rund 371 Mrd EUR, nicht nachgerechnet). Wichtigste offene Rechnung.
- **Berichtigung zu Band III.** Die wiederholte Aussage „die Shell erreicht ec.europa.eu nicht" gilt für die Shell, nicht für das Web-Abrufwerkzeug.
  Eurostat-Abrufe sind je Land und Dimension einzeln möglich (Sammelabrufe lieferten heute erneut nur ein Land).

*Skripte: `modell/alles.py`. Quellen: Eurostat `demo_gind`, `gov_10a_taxag`; Vorchat (Sekundärquelle), Dokument `Antworten-B7-B8-B9-B12-B14.md` im Projektraum.*

---

### v3.12 — Gesamtrechnung, Entscheidungen, neue Fassung des Gesamtkonzepts, Lizenz

**Art der Änderung: MAJOR** (Quote, Dividende und Text des Gesamtkonzepts ändern sich).
6. Oktober 2026. Auftrag des Verfassers: Lizenzvorschlag angenommen; offene Entscheidungen im Sinne des
Konzepts treffen; Gesamtrechnung ausführen; Gesamtkonzept mit den rechnerischen Erkenntnissen aktualisieren.

**Bewegte Zahlen** (Fassung 4. Oktober → Fassung 6. Oktober 2026; Klub, Preise 2028)

| Größe | vorher | jetzt | Ursache |
|---|---|---|---|
| Steuerquote | 30,6 % | **30,8 %** | Auslauf ab 2024 (B6) und strenge Lesart des Kriteriums (Korrektur 51) |
| effektiver Zins 2024 | 1,53 % (146 Mrd EUR) | **1,90 %** (180,9 Mrd EUR) | Korrektur 50 |
| Zinsdienst 2028 | 1,20 % des BIP | **1,74 %** (240 Mrd EUR) | Korrektur 50 und B6 |
| A 2028 | 9,04 % | **9,58 %** | ebenso |
| Dividende Klub 2028 / 2035 / 2060 | 506 / 472 / 651 EUR | **490 / 479 / 662 EUR** | ebenso |
| Dividende Deutschland 2028 / Tiefpunkt / 2060 | 550 / 512 / 707 EUR | **533 / 521 / 720 EUR** | ebenso |
| Formel je Einwohner / je Kind | 3.602 / 12.636 EUR | **3.599 / 12.625 EUR** | Korrektur 49 |
| Obergrenze von A | 36 % (Setzung) | **36 %** (abgeleitet, berechnet 35,1 %) | B9 |
| Entlastung | 2,41 Punkte | **2,21 Punkte** (305 Mrd EUR) | höhere Quote |
| größter Aufschlag / größte Entlastung | +254 FR / −728 IE | **+367 FR / −1.053 IE** EUR je Kopf und Jahr | Zinssatz 2028 2,22 statt 1,53 % |

Datenquellen: Eurostat `gov_10a_main` (D41PAY, S13, 2024, neun Staaten einzeln am 6. Oktober 2026 abgerufen, Antworten
maschinell gelesen, an der Quelle zu prüfen; Belgien vorläufig; **Estland geschätzt 0,2 Mrd EUR**, Abruf an Ratenbegrenzung
gescheitert); `demo_gind` (v3.11); übrige Eingänge aus `basis.py` (Abrufe 2. bis 4. Oktober, nicht erneut geprüft).

**Neu**
- `modell/gesamtrechnung.py` mit `modell/gesamtrechnung.toml`: eine Rechnung für alle Zahlen des Konzepts. Formeln der
  Originale; **Selbstprüfung**: mit den alten Eingängen trifft sie `final.pfad()` in allen 33 Jahren exakt. Ergebnis
  `daten/aggregate/gesamtrechnung.json`, `gesamtrechnung_pfad.csv`, `gesamtrechnung_obergrenze.csv`, `deckung_quote.csv`.
- `daten/aggregate/zinsausgaben_2024.csv` (Aggregat, Quelle je Zeile).
- `dokumente/werkzeuge/gesamtkonzept-bau.js` liest die Zahlen aus der JSON-Datei; im Text steht keine Zahl mehr von Hand.
  Doppelter Titelblock der alten Fassung entfernt. Neue Fassung `dokumente/TAX-2828-Gesamtkonzept.{docx,pdf}` (12 Seiten);
  alte Fassung nach `dokumente/archiv/TAX-2828-Gesamtkonzept-2026-10-04.{docx,pdf}` verschoben, Prüfsummen deshalb
  bewusst mit `--aktualisieren` auf die neuen Pfade gesetzt (Inhalt unverändert).
- `modell/pruefe_konzept.py`: sucht 27 Kernzahlen in der Schreibweise des Dokuments im PDF-Text und meldet veraltete
  Werte. Negativtest: die alte PDF schlägt 29-fach an.
- `LICENSE` (MIT, Skripte), `LICENSE-DOKUMENTE.md` (CC BY 4.0), `LIZENZ.md` (vorher `LIZENZ-VORSCHLAG.md`), `CITATION.cff`.
- `parameter.toml` bleibt die Basis der Fassung vom 4. Oktober (Regression); Aussagenregister ebenso.

**Entscheidungen des Bearbeiters im Auftrag des Verfassers** (im Sinne des Konzepts; jede ist ein Parameter oder ein Satz
im Bauskript und kann zurückgenommen werden)

| Punkt | Entscheidung | Begründung |
|---|---|---|
| B1 Dividendenreihe ohne Bezug | als Korrektur 52 geführt | Fehler offen führen |
| B2 zwei Zentralfälle | ein Zentralfall: 3,0 % nominal = 0,98 % real; Tabelle mit Zeile 0,98 % | eine Rechnung, eine Zahl |
| B4 Irland BIP oder GNI* | BIP, im Text begründet; Größenordnung GNI* (−2 %) genannt | A's Einnahmen sind ein Anteil am BIP; Steuern knüpfen am Ort der Wertschöpfung an |
| B6 Ausgangslage | Auslaufen des Altbestands ab 2024; Schuldenquote 2028 = 78,4 % als Annahme, Sensitivität 82 % | der Zins von 2024 ist ein Stand von 2024; Vorsicht (Abschnitt 8 des Konzepts) |
| B9 Obergrenze | Regel: höchster Bedarf im Zentralfall und in jedem einzelnen Finanzierungsrisiko (Zielzins 2,78 %, Wachstum 1,5 %, Schuld 82 %), auf volle Prozent aufgerundet → 36 % | trägt alle Einzelrisiken (bis 35,7 %), nicht deren Häufung (36,7 %) und nicht 3,5 % Verteidigung (38,5 %); das verlangt eine Vertragsänderung |
| B13 Bezugsgröße | überall „dessen, was A einzieht" | einheitlich |
| Tarifstufen | 0/9/16/21/26/28 % | einzige durchgerechnete Fassung (nationales Modell); 9/19/24/27 nie gerechnet; vorläufig bis zur Mikrosimulation |
| Quotenregel | strenge Mindestquote, auf 0,1 aufgerundet | Abrunden bräche das Versprechen |
| Reihenfolge | Mikrosimulation erst nach Prüfung der Aggregate (Vorgabe des Verfassers) | |

**B12: Deckung der Quote.** Erstmals gerechnet, auf deutscher Basis: das nationale Modell (Kern, Stufe 50 %) ergibt
27,91 % der Modellbasis, mit den gesondert ausgewiesenen Bausteinen (Vermögensteuer, Subventionsabbau, CO₂-Pfad) 29,03 %,
mit der Bodenwertabgabe dieses Entwurfs (0,82 statt 0,48) 29,85 %. **Lücke zur Quote 30,8 %: 0,95 Punkte**, auf den Klub
übertragen rund 131 Mrd EUR (2028, nominal). Annahmen: Dividende einkommensteuerpflichtig wie im Kern; deutsche
Steuerstruktur stellvertretend für den Klub (nicht zutreffend, Dänemark etwa hat kaum Sozialbeiträge und 31 % D5); Basis 4.200
Modell-Mrd mit den bekannten Kalibrierfragen (Korrekturen 26, 42). Der Vorchat nannte 2,69 Punkte (Kern ohne Bausteine);
die Bausteine standen im Kern gesondert und sind hier mitgezählt. Im Konzept als Abschnitt 7.1 und als wichtigste offene
Rechnung geführt.

**Unabhängige Prüfung.** Ein getrennter Prüfagent hat die Kernzahlen ohne Import der Gesamtrechnung nachgerechnet
(alle bestätigt) und den Text gelesen. Befunde und Umgang:
1. *Fehler:* Die strenge Ableitung des Originals hält den Kopfbetrag fest, lässt die Schuld aber mit 3 % nominal
   schrumpfen; „real kein Wachstum" heißt nominal 2 %. In stimmiger Lesart 30,764 % statt 30,651 %. **Übernommen**
   (Korrektur 51), Quote 30,8 %; die Tabellenzeile 0,0 % liegt jetzt über 479 EUR (481 EUR 2035).
2. „für jeden gleich" gegen „Kinder zur Hälfte": Text präzisiert, Beträge als Schnitt je Einwohner bezeichnet.
3. „größter Aufschlag 20,3 %" war die Entlastung Irlands: getrennt ausgewiesen (Frankreich +7,1 %, Irland 20,3 %).
4. Die Quote hängt am Auslauf, nicht am Zinsniveau (Höchstjahr 2035 hat ohnehin 2,5 %); Änderungsabsatz präzisiert, der
   aussagelose Risikofall „Restlaufzeit 5 Jahre" entfernt.
5. „jeder Wert einzeln abgerufen" zu pauschal: Herkunft je Datengruppe benannt.
6. und 7. Deutschland-Werte und Preisbasis gekennzeichnet (25 EUR, 49 EUR; 240 und 131 Mrd EUR 2028 nominal).
8. „86 % der kommunalen Aufgaben" nicht herleitbar: Zahl gestrichen.
9. und 10. Verteidigungsbasis belassen (DE-COFOG 1,4 % steht in `daten.py`); „Wie viel", „Gemeinschaften" statt „Communities".
Einschätzung des Prüfers zur Plausibilität der Zinsausgaben (aus eigenem Wissen, nicht an der Quelle): plausibel; 146 Mrd
waren eher zu niedrig.

**Nicht neu gebaut:** Seite zum Stand B (`seite/rahmenstruktur-seiten/`, zeigt 506/472/651), Webseite Stand A.

*Skripte: `modell/gesamtrechnung.py`, `modell/pruefe_konzept.py`, `dokumente/werkzeuge/gesamtkonzept-bau.js`, `modell/alles.py`.
Quellen: Eurostat `gov_10a_main`, `demo_gind`; nationales Modell `modell/kern/modell-2828-ergebnisse.txt`.*

---

### v3.13 — Kurzfassung des Gesamtkonzepts (zwei Seiten)

**Art der Änderung: MINOR** (neues Dokument, keine Rechnung geändert). 6. Oktober 2026.
Auftrag des Verfassers: Kurzform auf zwei Seiten mit klarer Erzählung für Laien, anknüpfend an die alte Webseite
(Komplexität, blockierte Verwaltung, Arbeit höher belastet als Kapital und Maschinen, neues Grundsystem mit gemeinsamem
Dach, „95 % haben mehr"), danach die neuen Regeln und eine Erklärung zur offenen Entwicklungsarbeit.

**Bewegte Zahl:** keine. Neu in `gesamtrechnung.toml` (nur durchgereicht, mit Quelle): Abgabenkeil Deutschland 47,9 %
und OECD-Schnitt 34,9 % (OECD, Taxing Wages 2025, Tabelle 3.1, 2024, Alleinstehende ohne Kinder, Durchschnittslohn;
über die OECD-Seite gelesen, maschinell zusammengefasst, an der Quelle zu prüfen), Abgeltungsteuer 26,375 %
(§ 32d EStG mit Solidaritätszuschlag), Anteil mit mehr Geld 95 % (Gruppenschätzung Stand A, `modell/kern`, Abschnitt F).

**Neu:** `dokumente/werkzeuge/kurzfassung-bau.js`, `dokumente/TAX-2828-Kurzfassung.{docx,pdf}` (zwei Seiten, alle Zahlen
aus `gesamtrechnung.json`); `pruefe_konzept.py` prüft zehn Kernzahlen und die Seitenzahl der Kurzfassung.

**Wo die Kurzfassung bewusst vorsichtiger ist als der Auftrag**
- „95 % haben später mehr in der Tasche": als **Gruppenschätzung des nationalen Modells** ausgewiesen. Sie stammt aus
  Stand A (Quote 27,91 %, Dividende 515 EUR je Erwachsenem), ist ohne Mikrosimulation entstanden und für Stand B nicht neu
  gerechnet. Als Tatsache stünde sie nicht im Text, solange sie sich nicht prüfen lässt.
- „Einkommen aus Arbeit höher besteuert als Kapitalerträge und maschinelle Gewinne": belegt mit dem Abgabenkeil (47,9 %)
  gegen die Abgeltungsteuer (26,4 %) und dem Umstand, dass Sozialbeiträge nur auf Arbeit anfallen. Nicht behauptet: dass
  Unternehmensgewinne insgesamt niedriger belastet seien; bei ausgeschütteten Gewinnen kommt die Unternehmensbesteuerung hinzu.
- „urwaldartig": als Bild in der Erzählung, ohne Zahl; keine unbelegten Superlative.
- „parteilos": als Selbstbeschreibung des Projekts und als Einladung formuliert.
- Das Repository ist privat; „öffentliches Logbuch" ist deshalb ersetzt durch „mit der Veröffentlichung zugänglich".
- Dividende: der Klubschnitt (490 EUR je Einwohner, Preise 2028), nicht der deutsche Wert (siehe B17).

*Skripte: `dokumente/werkzeuge/kurzfassung-bau.js`, `modell/pruefe_konzept.py`. Quellen: OECD Taxing Wages 2025; § 32d EStG;
nationales Modell (Stand A).*

---

### v3.14 — Datenzugang für Dritte (Menschen und KI-Agenten)

**Art der Änderung: MINOR** (neue Zugangsdateien und Prüfungen; Ergebnis der Rechnung unverändert). 7. Oktober 2026.
Auftrag des Verfassers: eine Sammlung von Informationen, mit denen Dritte, Menschen oder KI-Agenten, Zugriff auf die
nötigen Daten bekommen, um alle Bestandteile des Konzepts zu prüfen und weiterzubearbeiten.

**Bewegte Zahl:** keine. `gesamtrechnung.json` ist vor und nach der Umstellung schlüsselgleich und wertgleich (geprüft).

**Neu**
- `DATENZUGANG.md` (für Menschen): Zugang, Weg von der Quelle zum Dokument, Prüfen in vier Schritten, gesperrte Daten,
  Weiterbearbeiten, Begriffe. `AGENTS.md` (für KI-Agenten): Lesereihenfolge, Befehle, Invarianten, Abrufregeln,
  Kennzeichnung, Rückgabeformat.
- `daten/quellen.csv`: 21 Quellen mit Herausgeber, Datensatz, Verwendung, Datei, Status, Zugang und Weitergaberecht.
- `modell/eingangswerte.py` → `daten/aggregate/eingangswerte.csv`: 125 Eingangswerte, je amtlichem Wert eine Eurostat-URL
  (ein Land, eine Größe); `--abrufen` gleicht mit Netzzugang alle Werte ab (in der Projektumgebung nicht ausführbar, Shell ohne Netz).
- `projekt/manifest.py` → `projekt/manifest.json`: maschinenlesbare Projektkarte; prüft Quellen-IDs und alle in den
  Zugangsdateien genannten Dateien.
- `dokumente/werkzeuge/package.json` (docx 9.7.1) für reproduzierbares Bauen der Dokumente.
- `alles.py` um zwei Stufen erweitert (Eingangswerte, Projektkarte).
- Feste Rechengrößen aus `gesamtrechnung.py` nach `gesamtrechnung.toml` verlegt (Verteidigung 1,40 und 2035, Wachstum 3,0,
  Preise 2,0, Last heute 40,76, Steuern 25,95, Sozialbeiträge 14,88, Gesundheit 7,75), je mit Quelle und Status.
- **Gesundheit 7,75 % nachgerechnet:** BIP-gewichteter COFOG-Wert GF07 (S13, 2024) der zehn Staaten = 7,750. Die Herkunft
  galt in Band I als offen. Ebenso Verteidigung 1,40 = GF02 gewichtet (1,4006).

**Externer Test.** Ein getrennter Prüfagent hat nur mit `AGENTS.md` begonnen. Ergebnis: Einstieg gelingt, `alles.py`
läuft, Zins und Einwohner lassen sich lückenlos bis zur Quelle verfolgen, die Dividende nur teilweise (Posten der
Ebenen A und B, Bodenwertabgabe, Kinderanteil, Fortschreibungsfaktor ohne Abrufadresse, siehe B19). Zwölf Befunde,
eingearbeitet: Stufenzahl, Lizenzverweis, Hinweis „alles.py schreibt", feste Größen ins Parameterfile, fehlerhafte
Spalte in `laender_2024.csv` entfernt, Status „gelesen" statt „belegt" für die OECD-Werte, Abschnitt 7 nachgeführt,
irreführende Schlusszeilen zweier Stufen, `package.json`, nicht gemeldeter Wert (Estland D91) ausdrücklich geführt.
Drei Abrufformen getestet (nama_10_gdp, gov_10dd_edpt1, gov_10a_exp für DE): alle eindeutig.

**Befund für B15: Revision des deutschen BIP.** Eurostat meldet seit dem 6. Oktober 2026 für Deutschland ein BIP 2024 von
4.386.940 Mio EUR (vorläufig; maschinell gelesen am 7. Oktober 2026), das Modell rechnet mit 4.328.970 (+1,34 %).
Schuldenquote (62,2) und Verteidigung (1,4) stimmen. Grobe Wirkung (nicht gerechnet): Klub-BIP 2024 +0,5 %. Nicht übernommen,
weil die übrigen neun Länder nicht neu abgerufen sind und ein gemischter Datenstand schlechter wäre als ein einheitlich
älterer. Vorgehen: alle zehn BIP-Werte, Schuldenquoten und Zinsausgaben in einem Durchgang neu abrufen, dann neu rechnen;
bestätigt sich die Abweichung, als Korrektur 53 führen (Ursache: Revision, kein Übertragungsfehler).

*Skripte: `modell/eingangswerte.py`, `projekt/manifest.py`, `modell/alles.py`. Quellen: Eurostat (Abrufformen), Register.*

---

### v3.15 — Neue deutsche Webseite zum Stand B

**Art der Änderung: MINOR** (neue Seite; Rechnung um Reihen für die Seite ergänzt, keine bisherige Zahl bewegt). 7. Oktober 2026.
Auftrag des Verfassers: die Webseite aktualisieren, zunächst deutsch, unter strenger Beachtung der vorhandenen Gestaltung;
kompakt und einfach; neue Elemente gut darstellen, bisherige aktualisieren oder zur Disposition stellen; anschauliche,
spielerisch bedienbare Elemente; keine technischen Details und keine Klarstellungen zu Ungenauigkeiten; Hinweise auf
erfolgreiche Erfahrungen in anderen Ländern.

**Neu:** `seite/stand-b/de.html` (gebaut mit `seite/werkzeuge/seite_bau.py`, alle Zahlen aus `gesamtrechnung.json`; das
Stylesheet wird beim Bau wörtlich aus der veröffentlichten Seite übernommen und nur ergänzt), `seite/stand-b/QUELLEN.md`.
In `gesamtrechnung.py`: Dividende je Erwachsenem und je Kind (Klubschnitt je Einwohner / (1 − k/2), k = Anteil
Minderjähriger 16,67 %, Annahme aus dem nationalen Modell) → **535 EUR je Erwachsenem, 267 EUR je Kind** (2028, Preise 2028);
Reihen 2028–2060 je Wachstumsfall und die Anteile von Dach und Dividende für die Grafiken. `pruefe_konzept.py` prüft sechs
Kernzahlen im Quelltext der Seite.

**Aufbau der Seite:** Kopf mit drei Kennzahlen; „Zu komplex …" mit belegten Werten (Abgabenkeil, Abgeltungsteuer, fünf
Ebenen, keine Beiträge auf Maschinen); „Zwei Ebenen, ein Dach" mit Schaubild und Regler „Wohin fließen 100 € Steuern"
(2028–2060, mit Obergrenze); elf Bausteine; Rechner (Einkommensteuer nach Tarif, Dividende des Haushalts); Gemeinderechner
(Einwohner, Kinderanteil, Verwaltungsanteil → Budget und Dividendenplus); Zeitpfad der Dividende mit drei Wachstumsfällen;
fünf Sicherungen des Dachs; sechs Länderbeispiele (Estland, Dänemark, Schweiz, Alaska, Baden-Württemberg, Neuseeland);
Klub mit Einwohnern der zehn Staaten und Zeitleiste; „Offen entwickelt" mit Kurzfassung und Gesamtkonzept.

**Zur Disposition gestellt und entfallen:** Vergleich „heute gegen 28:28" je Haushalt und die zehn Musterhaushalte (Stand A;
für Stand B nicht gerechnet, weil die Finanzierung der Gesundheit außerhalb des Steuertopfs je Haushalt nicht festgelegt
ist), „Zwei Zukünfte" (Pfade des nationalen Modells), Haushaltsregeln des nationalen Modells, Länderdividenden je Land
(Stand A; im Stand B gilt eine Dividende), Kasten Irland, Belegstand-Tabelle, Anhang mit Quelltexten (ersetzt durch
„Offen entwickelt"). Die Einschränkungen stehen weiter im Gesamtkonzept und im Logbuch, nicht auf der Seite.

**Bewusst beibehalten:** der Hinweis „* Schätzung des Projekts" bei „über 95 %" (eine Zeile). Ohne ihn stünde eine
ungeprüfte Zahl als Tatsache auf der Seite.

**Geprüft:** Darstellung bei 1280 und 390 Pixel Breite; Bedienelemente automatisch getestet (Regler, Schaltflächen,
Rechenwerte: Steuer bei 80.000 EUR 13.389 EUR; Dividende 2060 für zwei Erwachsene und zwei Kinder 2.168 EUR je Monat;
Verwaltung auf 5,8 % → +46 EUR); keine Skriptfehler; fehlende Ressourcen nur die Schriftdateien (`fonts/`, liegen auf dem Server).

**Korrektur 53** (siehe Abschnitt 4): Die veröffentlichte Seite nennt für Estland ab 2026 einen Satz von 24 %; es bleiben 22 %.

*Skripte: `seite/werkzeuge/seite_bau.py`, `modell/gesamtrechnung.py`, `modell/pruefe_konzept.py`. Quellen: `seite/stand-b/QUELLEN.md`.*

---

### v3.16 — Webseite: Überarbeitung nach Durchsicht des Verfassers, Möglichkeitsraum

**Art der Änderung: PATCH** (Text und Bedienelemente der Seite; keine Zahl der Rechnung bewegt). 7. Oktober 2026.

**Umgesetzt nach Vorgabe des Verfassers:** „keine Sozialabgaben" aus Kopf und Kennzahl entfernt; „sichert die gemeinsamen
Interessen"; Leitzeilen „Das heutige System:" und „Das Konzept:" in großer Schrift; „frustriert"; Abgabenkeil als
Durchschnitt in Deutschland ausgewiesen (der OECD-Schnitt bleibt als Vergleich, damit die Aussage stimmt); „Gelder und
Aufgaben werden hin und her verwaltet, Ziele nicht erreicht"; im Schaubild „Steuerbeitrag" und „mindestens 64 % gehen weiter
an die Gemeinde" (64 = 100 − Obergrenze 36; „mindestens", weil das Dach meist weniger braucht, 2028 rund 32 %); neuer Kasten
„Warum eine Dividende?" (Rückfluss aus gemeinsam geerbtem Fortschritt und Automatisierung, Ausgleich der Umbauaufgaben);
Texte zu Einzelnem, Gemeinde (Mitgliedschaften in Kreisen und Verbünden) und Dach (Mehrheit der Mitglieder); Regler startet
2033; Zeitpfad-Text „bis 2035 müssen alte Fehler gekittet werden …" (im Auftrag stand „bis 2025"; gemeint ist der Tiefpunkt
2035, so umgesetzt); Beispiele Baden-Württemberg und Neuseeland entfernt; Abschnitt „Ein Klub mit Raum zum Wachsen" mit
wählbaren Staaten (31 europäische und Kanada), Schwelle Vereinigte Staaten, Vorwahlen und Kästen zu Großbritannien,
Kanada und „Sechs genügen".

**Neu:** `daten/aggregate/moeglichkeitsraum.csv` (33 Zeilen: zehn Klubstaaten aus `laender_2024.csv`, 21 Staaten aus der
Möglichkeitsraum-Seite des Vorchats als Sekundärquelle, Kanada nach Statistics Canada 2025, Schwelle USA). Quellen in
`seite/stand-b/QUELLEN.md`.

**B17 präzisiert (Frage des Verfassers: gleiche Dividende überall oder das halbe Existenzminimum am Wohnort?).**
Drei Lesarten, Dividende je Erwachsenem 2028 (Preise 2028), eigene Rechnung:
1. *Gleicher Eurobetrag im ganzen Klub* (jetziger Text): 535 EUR überall. Einfach, aber ungleiche Kaufkraft (in Estland viel
   mehr wert als in Dänemark) und Anreiz, von der Dividende in günstige Regionen zu ziehen.
2. *Gleicher Anteil am örtlichen BIP je Kopf* (so rechnet `final.py` für Deutschland): DE 582, FR 479, ES 366, NL 695, BE 587,
   AT 604, DK 751, SI 356, EE 326, **IE 1.168 EUR**. Das irische BIP (Konzernbuchungen) verzerrt diese Lesart; ungeeignet.
3. *Halbes Existenzminimum am Wohnort* (Vorschlag des Verfassers): gleiche Kaufkraft statt gleicher Eurobetrag. Für einen
   Klub braucht es ein einheitliches Maß; nationale gesetzliche Existenzminima sind politisch gesetzt und schwer vergleichbar.
   Neutraler wäre ein Klubwert, der mit dem Preisniveau des Wohnlandes gewichtet wird (Eurostat, Preisniveauindizes
   für den Konsum). Umzugsregel: Anspruch auf den neuen Satz erst nach einer Wartezeit mit Wohnsitz und Steuerpflicht
   (Vorbild Alaska: ein volles Kalenderjahr Wohnsitz). Rechnerisch nicht umgesetzt; braucht die Preisniveaus der zehn
   Staaten (Abruf) und eine Entscheidung, ob auch die Formel der Gemeinden nach Preisniveau gewichtet wird.
Entscheidung des Verfassers. Bis dahin nennt die Seite die Dividende im Klubschnitt und behauptet keine Gleichheit mehr
(„dieselbe Dividende" im Klubabschnitt entfernt).

*Skript: `seite/werkzeuge/seite_bau.py`. Quellen: `seite/stand-b/QUELLEN.md`, Statistics Canada, EAD.*

---

### v3.17 — Autorschaft Initiative 28:28, Preisniveaus und Ländervarianten (B17), Grafiken der Webseite

**Art der Änderung: MINOR** (neue Rechnung ohne Wirkung auf die geltende Quote; Texte und Seite). 7. Oktober 2026.

**Autorschaft.** Auf Wunsch der Initiative steht als Autorin durchgängig „Initiative 28:28": `CITATION.cff`, `LICENSE`,
`LICENSE-DOKUMENTE.md`, `LIZENZ.md`, `CONTRIBUTING.md`, `DATENZUGANG.md`, `CLAUDE.md`, Projektkarte, Gesamtkonzept,
Kurzfassung, Fußzeile der neuen Seite. Der Name des Verantwortlichen steht nur noch im Impressum der Webseite. Nicht geändert:
frühere Logbucheinträge (Geschichte) und die archivierten Seiten des Stands A. Hinweis: Eine Initiative ohne Rechtsform ist
keine Rechtsperson; Urheber im Rechtssinn bleiben die beteiligten Personen (Einschätzung, keine Rechtsberatung).

**Preisniveaus (neu, Quelle Q22).** Eurostat `prc_ppp_ind`, Preisniveauindex des Individualverbrauchs 2024 (EU27 = 100), je Land
einzeln abgerufen, maschinell gelesen: DE 109,1 · FR 107,9 · ES 90,7 · NL 121,0 · IE 141,2 · BE 118,7 · AT 119,7 · DK 142,8 ·
SI 91,0 · EE 96,5; einwohnergewichtet 108,2. → `daten/aggregate/preisniveau_2024.csv`.

**Ländervarianten (neu, `modell/laendervarianten.py`).** Dividende je Erwachsenem 2028 (Preise 2028):

| | DE | FR | ES | NL | IE | BE | AT | DK | SI | EE |
|---|---|---|---|---|---|---|---|---|---|---|
| V1 gleicher Betrag | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 |
| V2 Anteil am örtlichen BIP | 582 | 479 | 366 | 695 | 1.168 | 587 | 604 | 751 | 356 | 326 |
| V3a Preisniveau, budgetneutral | 539 | 533 | 448 | 598 | 698 | 587 | 592 | 706 | 450 | 477 |
| V3b halbes Existenzminimum, verankert | 514 | 509 | 428 | 571 | 666 | 560 | 564 | 673 | 429 | 455 |

V3b setzt in Deutschland die Hälfte des Grundfreibetrags 2026 an (12.348 / 24 = 514,50 EUR) und überträgt mit dem Preisniveau;
der Dividendentopf 2028 deckt das zu **104,8 %**. Die Lesart ist also mit der geltenden Quote finanzierbar, mit kleiner Reserve.
Gemeinden als Pro-Kopf-Variante des Länderbeitrags (10,35 % des BIP je Kopf des eigenen Landes): DE 6.091, FR 5.015, ES 3.833,
NL 7.283, IE 12.237, BE 6.147, AT 6.326, DK 7.869, SI 3.724, EE 3.415 EUR je Einwohner und Jahr (Klubschnitt 5.601). Keine
Umverteilung zwischen den Ländern über die Gemeindebudgets; die Irland-Anomalie wird nach Entscheidung der Initiative
hingenommen (Begründung der Initiative: Mit der Besteuerung am Ort der Nutzung entfällt die Gewinnverlagerung, das irische BIP
normalisiert sich).

**Offen (Entscheidung der Initiative):** V3a oder V3b; Wartezeit der Umzugsregel; ob das Quotenkriterium künftig am halben
Existenzminimum (514,50 EUR je Erwachsenem in Deutschland) statt an 479 EUR je Kopf gemessen wird. Erst dann Neurechnung von
Quote, Gesamtkonzept und Seite.

**Webseite.** Grafik „Wohin die Reise geht" hinter „Sechs genügen" wiederhergestellt, mit zwei Reitern: Staatsschulden
(Euroraum 2010–2025 nach Eurostat, Klub ab 2028 aus der Gesamtrechnung) und CO₂-Emissionen Deutschlands (2010–2025, Klimaziele
2030, 2040, 2045 nach Umweltbundesamt und Klimaschutzgesetz). Nicht wiederhergestellt: „Einkommensungleichheit" und „Belastung
Durchschnittsverdienst" der früheren Seite; beide stammen aus dem nationalen Modell und gelten für Stand B nicht ohne
Haushaltsmikrosimulation und ohne geklärte Finanzierung der Gesundheit.

*Skripte: `modell/laendervarianten.py`, `seite/werkzeuge/seite_bau.py`. Quellen: Eurostat prc_ppp_ind, gov_10dd_edpt1;
Umweltbundesamt; § 32a EStG.*

---

### v3.18 — Sprachfassungen der Webseite, Prognoselinie Staatsschulden

**Art der Änderung: MINOR** (Seite in sechs Sprachen; keine Zahl der Rechnung bewegt). 7. Oktober 2026.
Auftrag der Initiative: Staatsschulden-Grafik um eine gestrichelte Prognose für den fehlenden Zeitraum ergänzen; Länderversionen
zunächst als Übersetzungen mit Referenzland Deutschland; Frage nach einer international tragfähigen Rechtsform.

**Seite.** Die Vorlage ist von den Texten getrennt: `seite/werkzeuge/vorlage.html` (Aufbau, Grafiken, Rechner),
`seite/werkzeuge/sprachen/<sprache>.json` (alle Texte, 250 Schlüssel), `seite_bau.py` prüft, dass jede Sprache genau die Schlüssel der
deutschen Fassung hat, und formatiert Zahlen, Euro und Prozent je Sprache. Sprachen: Deutsch (Referenz), Englisch, Französisch,
Italienisch, Spanisch, Polnisch – die Sprachen der „Sechs genügen", Englisch zugleich für Großbritannien, Irland und Kanada.
Ländernamen im Möglichkeitsraum kommen aus dem Browser (`Intl.DisplayNames`). Alle Zahlen und Länderangaben beziehen sich auf
Deutschland; das steht in jeder Übersetzung im Abschnitt „Das heutige System" und in der Fußzeile. Gesamtkonzept und Kurzfassung
bleiben deutsch (Hinweis an den Links). Übersetzungen durch das KI-System, **nicht muttersprachlich gegengelesen**.

**Staatsschulden-Grafik.** Gestrichelte Linie 2024–2028 für den Klub: von der BIP-gewichteten Schuldenquote 2024 (78,45 %) zur
Startannahme 2028 (78,4 %), beschriftet „Klub bis zum Start (Schätzung)". Sie füllt die Lücke zwischen Euroraum-Reihe und Klubpfad.

**Geprüft:** alle sechs Seiten gebaut und automatisch bedient (Regler, Rechner, Gemeinde, Möglichkeitsraum, Grafiken); Rechenwerte in
allen Sprachen gleich (Steuer bei 80.000 EUR 13.389 EUR, Dividende 2060 zwei Erwachsene und zwei Kinder 2.168 EUR, Verwaltung 5,8 % →
+46 EUR); keine Skriptfehler. `pruefe_konzept.py` prüft je Sprachfassung Modellstand und Formelbetrag.

**Rechtsform (Antwort an die Initiative, keine Rechtsberatung).** Siehe Antwort im Gespräch; kurz: Einstieg als eingetragener Verein
in Deutschland oder als Verein nach Schweizer ZGB; europäisches Dach später als belgische AISBL; die geplante EU-Richtlinie über
europäische grenzüberschreitende Vereine (Parlament März 2024) ist noch nicht verabschiedet.

*Skripte: `seite/werkzeuge/seite_bau.py`, `seite/werkzeuge/vorlage.html`, `seite/werkzeuge/sprachen/*.json`, `modell/pruefe_konzept.py`.*

---

### v3.19 — Staatsschulden: Fortschreibung des Status quo bis zum Systemwechsel

**Art der Änderung: MINOR, bewegt Zahlen der Rechnung.** 7. Oktober 2026.
Auftrag der Initiative: „Die Strichlinie in der Grafik soll sich aus einer Prognose der Weiterentwicklung des Status quo darstellen
bis zum Systemwechsel und folgt erst dann dem neuen Pfad."

**Daten.** Bruttoschuldenstand (GD) 2010–2025 und Finanzierungssaldo (B9) 2025 der zehn Klubstaaten, Eurostat `gov_10dd_edpt1`
(Sektor S13, % des BIP), abgerufen 7. Oktober 2026 über das Web-Abrufwerkzeug, je Land und Größe ein Abruf. Ablage als Aggregat
`daten/aggregate/schulden_2010_2025.csv` (eine Zeile je Land, keine Rohantwort). Prüfung: die Werte 2024 stimmen mit `basis.py`
überein. Werte 2025 sind die Meldung vom Oktober 2026 und können noch revidiert werden (**vorläufig**).

**Rechnung (`modell/schuldenpfad.py`).** Klubquote je Jahr BIP-gewichtet (Gewichte BIP 2024 aus `basis.py`; Annahme: feste Gewichte
über den ganzen Zeitraum, vereinfachend). Fortschreibung 2026–2028 mit `d(t) = d(t−1)/(1+g) − saldo_2025`, g = 3,0 % nominal
(`gesamtrechnung.toml`), Saldo 2025 gewichtet −2,93 % des BIP, als gleich bleibend angenommen (**Annahme „Status quo"**: keine
Konsolidierung, keine Verteidigungsaufwüchse über 2025 hinaus). Ergebnis: Klub 2025 79,5 %, 2026 80,1 %, 2027 80,7 %, **2028 81,3 %**.
Ausgabe `daten/aggregate/schuldenpfad.json`.

**Folge für das Modell.** Damit der neue Pfad an die Strichlinie anschließt, startet die Gesamtrechnung 2028 mit 81,3 % statt der
Annahme 78,4 % (Stand 2024). Der Risikofall „Schuldenquote 2028 höher" ist jetzt +3,5 Punkte (84,8 %), vorher 82 %.

**Bewegte Zahlen** (alle Preise 2028, Klub):

| Größe | v3.18 | v3.19 |
|---|---:|---:|
| Schuldenquote 2028 | 78,4 % (Annahme) | 81,3 % (Fortschreibung) |
| strenge Mindestquote | 30,76 % | 30,83 % |
| **Quote (aufgerundet)** | **30,8 %** | **30,9 %** |
| Ebene A 2028 | 9,58 % BIP | 9,64 % BIP |
| Zinsdienst 2028 | 1,74 % BIP | 1,80 % BIP |
| Dividende 2028 je Einwohner/Monat | 490,2 € | 491,8 € |
| Tiefpunkt 2035 | 478,8 € | 480,8 € |
| Dividende 2060 | 662,4 € | 666,8 € |
| Erwachsene 2028 / Kinder 2028 | 534,8 / 267,4 € | 536,6 / 268,3 € |
| Obergrenze berechnet / festgesetzt | 35,14 % / 36 % | 35,21 % / 36 % |
| Entlastung (deutsche Basis) | 2,21 Punkte = 305 Mrd € | 2,11 Punkte = 291 Mrd € |
| Deckungslücke zur Quote | 0,95 Punkte = 131 Mrd € | 1,05 Punkte = 145 Mrd € |

Die Dividende steigt trotz höherer Schuld leicht, weil die Quote auf 30,9 % aufgerundet wird und der Rundungsüberschuss in die Dividende
fließt. Eine Quote von 30,83 % (streng) ergäbe etwa die alte Dividende. **Kritisch:** die Fortschreibung hängt an einer einzigen
Saldo-Annahme; bei einem Defizit von −2 % statt −2,93 % läge die Quote 2028 bei 78,6 % (2,7 Punkte tiefer), die strenge Mindestquote
bei rund 30,77 %, also aufgerundet wieder 30,8 % (nachgerechnet mit `pfad(d0=…)`). Die Quote steht damit genau an einer Rundungsschwelle.

**Grafik der Seite.** Linie „Klub der zehn bis heute" 2010–2025 (ersetzt die Euroraum-Reihe), gestrichelt „Fortschreibung bis zum
Systemwechsel" 2025–2028, durchgezogen „mit 28:28 ab 2028" von 81,3 % auf 32 % 2060. Beschriftungen in allen sechs Sprachen.
Gesamtkonzept §8 und Kurzfassung neu gebaut.

**Wodurch aufgefallen:** Auftrag der Initiative; bei der Umsetzung zeigte sich, dass eine Strichlinie aus dem Status quo nicht an die
Startannahme 78,4 % anschließt (Bruch von knapp 3 Punkten), daher die Änderung des Startwerts.

**Geprüft:** `python3 modell/alles.py` (14 Stufen); Selbstprüfung der Gesamtrechnung gegen `final.pfad()` (mit dessen Startwert, unverändert 33 Jahre gleich);
Grafik auf `de.html` als Bildschirmfoto gesichtet (Anschluss 2028 ohne Sprung).

*Skripte: `modell/schuldenpfad.py` (neu), `modell/gesamtrechnung.py`, `modell/gesamtrechnung.toml`, `seite/werkzeuge/seite_bau.py`,
`seite/werkzeuge/sprachen/*.json`, `dokumente/werkzeuge/gesamtkonzept-bau.js`, `modell/alles.py`.*

---

### v3.20 — Dividende nach Preisniveau, Umzugsregel, Quotenkriterium halbes Existenzminimum (B17)

**Art der Änderung: MINOR, bewegt die Quote.** 7. Oktober 2026.
Entscheidungen der Initiative: „Länderbezogene Anpassung der Dividende (mein Vorschlag). Umzugswartedauer 3 Jahre mit Nachweis
einer Steuerzahlung. Deine Entscheidung zur Quote."

**1. Dividende je Land (entschieden).** Lesart V3a aus v3.17: Der Dividendentopf des Klubs wird nach Einwohnern × Preisniveau
verteilt (Eurostat `prc_ppp_ind`, Individualverbrauch 2024, EU27 = 100; Klub einwohnergewichtet 108,17), Kinder zur Hälfte.
Deutschland erhält das Klubmittel × 1,0086. Der ganze Topf wird ausgezahlt. **Vereinfachung (Annahme):** gleicher
Minderjährigenanteil in allen Ländern; sonst ist die Verteilung nicht exakt budgetneutral.

**2. Umzugsregel (entschieden).** Bei Umzug innerhalb des Klubs gilt die Dividende des bisherigen Landes, bis drei Jahre Wohnsitz und
eine nachgewiesene Steuerzahlung im neuen Land vorliegen (`umzug_wartezeit_jahre = 3`). Ohne Wirkung auf die Rechnung. **Offen**
(Gesamtkonzept Abschnitt 8): was als Steuerzahlung gilt (Rentner, Studierende, Personen ohne Einkommensteuer), Kinder, und die
Vereinbarkeit mit Freizügigkeit und Gleichbehandlung (Art. 45 AEUV, VO 883/2004) beim Umzug in ein teureres Land. Keine Rechtsprüfung.

**3. Quotenkriterium (Entscheidung des KI-Systems im Auftrag der Initiative).** Neu: Die Quote ist die kleinste, bei der der
Klubtopf in jedem Jahr 2028–2060 das halbe Existenzminimum am Wohnort deckt, bei null realem Wachstum (strenge Lesart, Korrektur 51).
Maß: halber Grundfreibetrag Deutschland 2026 (12.348 EUR, § 32a EStG), mit 2 % je Jahr in Preise 2028 fortgeschrieben = **535,29 EUR
je Erwachsenem und Monat**, mit dem Preisniveau übertragen. Das ergibt 486,48 EUR je Klub-Einwohner und Monat.

Begründung: (a) Mit der Dividende nach Preisniveau zählt der Topf des Klubs, nicht mehr das deutsche BIP je Kopf; das alte
Kriterium (479 EUR je Kopf, nach örtlichem BIP, Lesart von `final.py`) passt nicht mehr zur Auszahlungsregel. (b) 479 EUR war eine
Setzung aus dem Projektstand ohne Herleitung; das halbe Existenzminimum ist amtlich verankert und ist der Vorschlag der Initiative.
(c) Die strenge Lesart bleibt, weil ein Boden, der nur bei Wachstum hält, kein Boden ist.

| Kriterium (alle mit Dividende nach Preisniveau, außer erster Zeile) | Mindestquote | Quote |
|---|---:|---:|
| bisher: 479 EUR je Kopf DE nach örtlichem BIP, streng (v3.19) | 30,827 | 30,9 |
| 479 EUR je Kopf DE, streng | 31,590 | 31,6 |
| halbes Existenzminimum ohne Fortschreibung (514,50 EUR), streng | 31,428 | 31,5 |
| halbes Existenzminimum, Preise 2028, nur Zentralfall (3,0 % nominal) | 31,018 | 31,1 |
| **halbes Existenzminimum, Preise 2028, streng (gewählt)** | **31,847** | **31,9** |

**Kritisch.** Das gewählte Kriterium hebt die Quote um einen vollen Punkt. Folgen: Deckungslücke 1,05 → **2,05 Punkte
(283 Mrd EUR Klub 2028)**, Entlastung 2,11 → **1,11 Punkte (153 Mrd EUR)**.
Im Zentralfall liegt die Dividende dafür deutlich über dem Boden (2028: 10,4 %). Wer die Quote niedriger halten
will, wählt den Zentralfall (31,1 %); dann fällt die Dividende bei null Wachstum unter den Boden. Die Entscheidung ist ein
Parameter und kann von der Initiative revidiert werden. Das Existenzminimum ist mit der Preissteigerung fortgeschrieben (Annahme);
der Grundfreibetrag folgt tatsächlich dem Existenzminimumbericht und stieg zuletzt schneller als die Preise.

**Dividende je Erwachsenem und Monat, Preise 2028 (`tabelle_laender_div`):**

| Land | Preisniveau | Boden | 2028 | 2035 | 2060 | Tiefpunkt bei null Wachstum |
|---|---:|---:|---:|---:|---:|---:|
| Dänemark | 142,8 | 701 | 773 | 762 | 1.049 | 704 |
| Irland | 141,2 | 693 | 765 | 753 | 1.037 | 696 |
| Niederlande | 121,0 | 594 | 655 | 646 | 889 | 597 |
| Österreich | 119,7 | 587 | 648 | 639 | 879 | 590 |
| Belgien | 118,7 | 582 | 643 | 633 | 872 | 585 |
| Deutschland | 109,1 | 535 | 591 | 582 | 801 | 538 |
| Frankreich | 107,9 | 529 | 584 | 576 | 793 | 532 |
| Estland | 96,5 | 473 | 523 | 515 | 709 | 476 |
| Slowenien | 91,0 | 446 | 493 | 486 | 669 | 449 |
| Spanien | 90,7 | 445 | 491 | 484 | 666 | 447 |

**Bewegte Zahlen** (gegen v3.19): Quote 30,9 → **31,9 %**; Obergrenze von A 36 → **35 %** (Regel aus Zentralfall und Einzelrisiken,
berechnet 34,08 %, Einzelrisiken bis 34,67 %; Häufung der Risiken 35,59 %
weiterhin nicht gedeckt); Klubschnitt je Einwohner 2028 491,8 → 536,9 EUR, Tiefpunkt 480,8 (2035) → 528,7 EUR
(2032), 2060 666,8 → 728,4 EUR; Deutschland je Erwachsenem 2028 536,6 (Klubmittel, bisher auf der Seite) →
**590,8 EUR**, je Kind 295,4 EUR, 2060 801,5 EUR. Der Tiefpunkt verschiebt sich auf 2032, weil
der höhere Dividendenanteil das Wachstum stärker zur Geltung bringt. Höchstbedarf von A unverändert (10,59 % BIP, 2035).

**Geändert:** `modell/gesamtrechnung.py` (Preisniveaus, Feld `de_land`, Kriterium, Ländertabelle; Selbstprüfung gegen `final.pfad()`
unverändert 33 Jahre exakt, weil die Originalfelder erhalten bleiben), `gesamtrechnung.toml` (`versprechen_de_monat` nur Vergleich,
`umzug_wartezeit_jahre`), `laendervarianten.py` (Korrektur 54), Gesamtkonzept (1.4 neu mit Ländertabelle und Umzugsregel, Abschnitt 4
Kriterium und „Was das Kriterium kostet", Abschnitt 8 zwei neue offene Punkte, Abschnitt 9 Änderungsabsatz; die Zahlen im
Änderungsabsatz zum 4. Oktober sind jetzt fest geschrieben statt aus der laufenden Rechnung), Kurzfassung, Seite in sechs Sprachen
(Dividende Deutschland statt Klubmittel, ein Satz zur gleichen Kaufkraft; Übersetzung nicht muttersprachlich geprüft),
`pruefe_konzept.py`.

**Wodurch aufgefallen:** Entscheidung der Initiative; bei der Umsetzung zeigte sich, dass das alte Kriterium auf dem deutschen BIP
je Kopf ruhte und mit der Dividende nach Preisniveau nicht mehr gilt, und dass der Anker 514,50 EUR nicht in Preisen 2028 stand
(Korrektur 54).

**Geprüft:** `python3 modell/alles.py`; `pruefe_konzept.py` (57 Prüfungen); Seite in drei Sprachen automatisch bedient (Rechner 2060,
zwei Erwachsene und zwei Kinder: 2.404 EUR im Monat = 2 × 801 + 2 × 401); Gesamtkonzept zwölf, Kurzfassung zwei Seiten.

*Skripte: `modell/gesamtrechnung.py`, `modell/laendervarianten.py`, `dokumente/werkzeuge/gesamtkonzept-bau.js`,
`dokumente/werkzeuge/kurzfassung-bau.js`, `seite/werkzeuge/seite_bau.py`, `seite/werkzeuge/sprachen/*.json`, `modell/pruefe_konzept.py`.*

---

### v3.21 — Tarifstufen am Grundbedarf, Umzugsregel präzisiert

**Art der Änderung: MINOR, bewegt die Deckung, nicht die Quote.** 7. Oktober 2026.
Vorgaben der Initiative: „Für Studenten, Kinder entfällt der Steuernachweis, Rentner sind doch eigentlich nicht steuerbefreit? Was
den Grundbedarf (Existenzminimum) angeht, ist das ein wesentliches Kriterium als dynamische Stellschraube. Es hat Orts- und
Zeitbezug. Ggf. sollte daher auch die Steuerdynamik 0–28 in der Form reagieren, dass die Stufen vom 1-, 2-, 3-, 4-fachen
Grundbedarf ausgehen, bis sie die 28 % erreichen."

**1. Umzugsregel.** Kinder und Studierende: kein Steuernachweis, die drei Jahre Wohnsitz gelten weiter. Rentner: Renten sind in
Deutschland einkommensteuerpflichtig (Besteuerungsanteil bei Rentenbeginn 2026: 84 %, § 22 EStG; Zahl aus Sekundärquellen, amtlich
zu prüfen); im Entwurf wird ohnehin das Brutto besteuert. Wer mit allen Einkünften unter dem Grundbedarf bleibt, zahlt aber keine
Einkommensteuer und kann keine Zahlung nachweisen. **Vorschlag, nicht entschieden:** Als Nachweis genügt die Veranlagung im neuen
Land (unbeschränkte Steuerpflicht), ohne Mindestzahlung. Offen auch: wer als Studierender gilt.

**2. Tarifstufen am Grundbedarf (umgesetzt).** Lesart: Die sechs Sätze 0 / 9 / 16 / 21 / 26 / 28 % beginnen beim 1-, 2-, 3-, 4- und
5-fachen Grundbedarf; 28 % gilt ab dem Fünffachen. Grundbedarf = Grundfreibetrag 2026 (12.348 EUR), mit 2 % je Jahr fortgeschrieben
(Annahme), am Wohnort mit dem Preisniveau übertragen. Deutschland 2028: **12.847 / 25.694 / 38.541 / 51.387 / 64.234 EUR** (Preise 2028). Länder 2028 (1- bis 5-fach):
DK 16.815–84.076; IE 16.627–83.134; NL 14.248–71.241; AT 14.095–70.475; BE 13.977–69.886; DE 12.847–64.234; FR 12.706–63.528; EE 11.363–56.816; SI 10.716–53.578; ES 10.680–53.401 EUR. Damit hängen Dividende (½ Grundbedarf) und Tarif an einer Größe; steigt sie, wandern die Stufen mit (keine kalte
Progression). Alternative Lesart „28 % ab dem Vierfachen" (Satz 26 % entfällt) mitgerechnet.

**Aufkommen (`modell/tarif_grundbedarf.py`).** Aufkommensfunktion des nationalen Modells (`modell/kern/modell-2828.py`,
`est_aufkommen`, Szenario Robust, Elastizität 0,35, Dividendenstufe 50 %), deutsche Basis, Modellbasis 4.200 Mrd, Euro 2026:

| Variante | Stufen (EUR 2026) | Einkommensteuer | Änderung | Steuer bei 80.000 EUR |
|---|---|---:|---:|---:|
| bisher | 12.348 / 25.000 / 40.000 / 55.000 / 70.000 | 313,3 Mrd | – | 13.389 |
| **1- bis 5-facher Grundbedarf (gewählt)** | 12348 / 24696 / 37044 / 49392 / 61740 | 324,3 Mrd | +0,26 Pkt. BIP | 14.003 |
| 1- bis 4-fach, 28 % ab 4-fach | 12348 / 24696 / 37044 / 49392 | 326,7 Mrd | +0,32 Pkt. BIP | 14.250 |

**Kritisch.** Die Funktion rechnet mit sieben Einkommensgruppen und einer Kalibrierung des Stands A; sie ist eine Größenordnung,
keine Mikrosimulation. Die Stufen liegen ab der zweiten etwas tiefer als bisher, daher das Mehraufkommen. Für die übrigen neun
Länder gibt es keine Aufkommensrechnung; die Folge der ortsbezogenen Stufen für den Klub ist offen (Mikrosimulation, nach
Entscheidung der Initiative erst, wenn alles andere geprüft ist).

**Bewegte Zahlen:** Einkommensteuer (deutsche Basis) 7,46 → 7,72 % BIP; nachgewiesene Deckung
29,85 → **30,11 %**; Deckungslücke 2,05 → **1,79 Punkte (247 Mrd EUR Klub 2028)**. Quote (31,9 %),
Dividende, Obergrenze unverändert. Rechner der Seite: Steuer bei 80.000 EUR 13.389 → **13.664 EUR** (jetzt Stufen in Preisen 2028,
Korrektur 55).

**Wodurch aufgefallen:** Vorschlag der Initiative; Korrektur 55 beim Umstellen des Rechners.

**Geprüft:** `python3 modell/alles.py` (15 Stufen, neue Stufe „Tarif nach Grundbedarf"); `pruefe_konzept.py`; Rechner nachgerechnet
(13.664 EUR von Hand mit den Stufen 2028).

*Skripte: `modell/tarif_grundbedarf.py` (neu), `modell/gesamtrechnung.py`, `gesamtrechnung.toml` (`tarif_stufenabstand_grundbedarf`),
`seite/werkzeuge/seite_bau.py`, `seite/werkzeuge/sprachen/*.json`, Bauskripte Gesamtkonzept und Kurzfassung, `modell/alles.py`.*

---

### v3.22 — Tarif 0 / 9 / 16 / 21 / 28 % mit vier Stufen am Grundbedarf; Umzugsregel: Zweck des Nachweises

**Art der Änderung: MINOR, bewegt die Deckung, nicht die Quote.** 7. Oktober 2026.
Entscheidung der Initiative: „Die alternative Lesart ist einfacher und zukunftssicherer. Der Steuernachweis trägt die Idee, dass
Umzüge nur dann belohnt werden, wenn ein neues Einkommen vor Ort gesichert ist. Man kann das zunächst ausklammern."

**1. Tarif.** Sätze 0 / 9 / 16 / 21 / 28 %, Stufen beim 1-, 2-, 3- und 4-fachen Grundbedarf; 28 % ab dem Vierfachen. Der Satz 26 %
des nationalen Modells entfällt. Deutschland 2028: **12.847 / 25.694 / 38.541 / 51.387 EUR** (Preise 2028). Länder 2028 (1- bis 4-fach): DK 16.815–67.261; IE 16.627–66.507; NL 14.248–56.992; AT 14.095–56.380; BE 13.977–55.909; DE 12.847–51.387; FR 12.706–50.822; EE 11.363–45.453; SI 10.716–42.862; ES 10.680–42.721 EUR.

**2. Umzugsregel.** Zweck des Steuernachweises im Konzept festgehalten: Ein Umzug wird nur belohnt, wenn vor Ort ein neues
Einkommen gesichert ist. Kinder und Studierende ohne Nachweis (v3.21). Personen ohne steuerpflichtiges Einkommen über dem
Grundbedarf (etwa Rentner mit kleiner Rente): **vorerst ausgeklammert**; der Vorschlag aus v3.21 (Veranlagung statt Zahlung) ist
zurückgezogen.

**Bewegte Zahlen** (grobe Aufkommensfunktion des nationalen Modells, deutsche Basis, siehe v3.21): Einkommensteuer 7,72 → **7,78 % BIP**
(gegen die festen Stufen bis v3.20: +0,32 Punkte); nachgewiesene Deckung 30,11 → **30,17 %**; Deckungslücke 1,79 →
**1,73 Punkte (239 Mrd EUR Klub 2028)**. Rechner der Seite: Steuer bei 80.000 EUR 13.664 → **13.921 EUR**
(Preise 2028, von Hand nachgerechnet). Quote 31,9 %, Dividende und Obergrenze unverändert. Dieselbe Einschränkung wie in
v3.21: Größenordnung, keine Mikrosimulation; für die übrigen neun Länder nicht gerechnet.

**Wodurch aufgefallen:** Entscheidung der Initiative.

**Geprüft:** `python3 modell/alles.py`; `pruefe_konzept.py`; Seite bedient (Rechner 13.921 EUR, keine Skriptfehler).

*Skripte: `modell/tarif_grundbedarf.py`, `modell/gesamtrechnung.py`, `gesamtrechnung.toml`, Bauskripte, `seite/werkzeuge/sprachen/*.json`.*

---

### v3.22.1 — Upload-Paket der Webseite

**Art der Änderung: PATCH** (Werkzeug, keine Zahl bewegt). 9. Oktober 2026. Auftrag der Initiative: die Dateien zusammenstellen, die
auf der Homepage ersetzt werden müssen; die Schriften liegen dort.

Neu `seite/werkzeuge/paket_bau.py`: kopiert die sechs Sprachfassungen und die beiden PDF nach `seite/paket/` (nicht im
Repository, `.gitignore`) und packt sie als Zip. Neu erzeugt: `index.html` (bisher die englische Seite; jetzt Weiterleitung nach
Browsersprache, sonst Englisch, ohne Cookies) und Weiterleitungen `da.html`, `nl.html`, `sl.html`, `et.html` auf `en.html`, weil diese
Sprachen entfallen und alte Links sonst den Stand A mit überholten Zahlen zeigen würden. `fonts/` bleibt auf dem Server; das Skript
bricht ab, wenn eine neue Seite eine Schriftdatei verlangt, die die alte Seite nicht verlangt (geprüft: sieben Dateien, alle
vorhanden in der alten Seite). Anleitung in `seite/LIESMICH.md`.

**Geprüft:** Weiterleitung im Browser mit Sprache de-DE → `de.html`, pl-PL → `pl.html`, nl-NL → `en.html`, `da.html` → `en.html`.
Nicht geprüft: ob auf dem Server weitere Dateien der alten Seite liegen (nicht einsehbar); sie bleiben unberührt.

---

### v3.23 — Frankreich: Eingangsdaten und Schuldenfortschreibung (erste länderspezifische Rechnung)

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.
Auftrag der Initiative: länderspezifische Betrachtung für die französische Seite; Freigabe der Eurostat-Abrufe.

**Recherche (Agent, geprüft in Teilen).** Eingangsdaten zu Schulden, Sozialbeiträgen, Rente, Einkommensteuer, Kapitalsteuer,
Mehrwertsteuer, Kommunen, Verfassung, mit Status je Zeile: `daten/aggregate/frankreich_eingaben.md`. Amtlich: INSEE (Schuldenquote
2025 115,6 %, Defizit 5,1 %), Regierungsprognose (Saldo −5,4 / −5,0 / −3,9 % für 2026–2028, PLF-Anhang und RESF 2027), DGCL
(34.875 Gemeinden), DGFiP (PFU 31,4 % ab 2026, Quotient familial 1.807 € je Halbanteil). Sekundärquellen gekennzeichnet (Zinsausgaben
Cour des comptes, HCFP-Einschätzung). **Vom Agenten abgerufen, nicht von mir gegen die Originale geprüft:** alle Einträge mit
„Agent“ in der Datei.

**Eurostat, selbst abgerufen (10.10.2026):** Sozialbeiträge netto (D61) 2024: Frankreich 16,5 % BIP (Sozialversicherung 14,5 %),
Deutschland 17,5 % (vorläufig). Alterssicherung (COFOG 10.2) 2024: Frankreich 13,4 %, Deutschland 9,9 % (vorläufig). Die COR-Zahl
für Rente (14,1 %) hat eine andere Abgrenzung und ist nicht vergleichbar.

**Rechnung (`modell/frankreich.py`, neu).** Schuldenquote Frankreichs mit d(t) = d(t−1)/(1+g) − Saldo (wie `schuldenpfad.py`).
Drei Pfade: A Klubannahme (Defizit −5,1 %, g 3,0 %) 120,6 % 2028; B Regierungsdefizit, g 3,0 % 119,6 %; C Regierungsdefizit mit
implizitem Wachstum (1,49 / 2,23 / 2,70 %) 122,4 % = Regierungsprognose. Ergebnis `daten/aggregate/frankreich.json`.

**Wirkung auf den Klub (Sensitivität, kein Ersatz).** Frankreich hat 24,1 % des Klub-BIP. Klubquote 2028: 81,29 % (Konzept
unverändert), mit Frankreich auf Pfad B 81,29 %, auf Pfad C 81,96 %. Ein französisches Regierungsdefizit wirkt also neutral; das
Wachstum entscheidet. C liegt innerhalb des Risikofalls im Konzept (+3,5 Punkte, 84,8 %). **Entscheidung der Initiative:** ob die
Klubquote 2028 auf 82,0 % gesetzt wird.

**Korrigiert (Arbeitsfehler, nicht veröffentlicht):** In der Zwischenrechnung zur Klubwirkung stand 81,04 % für Pfad B. Ursache:
der Rest-Saldo wurde konstant gehalten, obwohl er sich mit dem Saldo Frankreichs jährlich ändert. Korrekt: 81,29 %. Die Ausgabe des
Skripts ist die korrekte Fassung.

**Offen:** Mehrwertsteuer-Aufkommen Frankreich (D211), Verwaltungsanteil der Gemeinden (COFOG S1313), Zuständigkeiten der
Départements und Régions, Verfassungstext (Art. 1 und 72, Abruf fehlgeschlagen), Schuldenstand 2028 in Mrd. €. Vorläufige Werte
(Eurostat „p“) sind als solche zu führen.

**Früher falsche Angabe, jetzt belegt:** Die Zahl der französischen Gemeinden lag in meiner Antwort bei „rund 35.000“. Amtlich
sind es 34.875 (1.1.2026).

**Wodurch aufgefallen:** Auftrag der Initiative; die Zwischenrechnung zur Klubwirkung ergab zunächst eine Wirkung, die sich bei
Prüfung als Rechenfehler erwies.

**Geprüft:** `python3 modell/alles.py` (16 Stufen, neue Stufe „Frankreich Schuldenpfad“); Ausgabe des Skripts gegen die Regierungs-
prognose (Pfad C reproduziert sie).

*Skripte: `modell/frankreich.py` (neu). Quellen: INSEE IR78; PLF 2027 (Rapport sur la dette); RESF 2027; DGCL Bulletin BIS 206;
DGFiP Brochure „Calcul de l'impôt“; Eurostat gov_10a_taxag, gov_10a_exp (Abruf 10.10.2026).*

---

### v3.24 — Standard für Länderrechnungen, Polen, Umstellung Frankreich

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.
Auftrag der Initiative: Die Vergleichsrechnungen sollen einen gemeinsamen Standard haben. Der Standard soll das Rechenmodell
insgesamt festigen und 28:28 länderspezifisch kommunizieren. Danach Polen. Eine Unterscheidung der Länder nach Klub und
Möglichkeitsraum ist nicht gewünscht und kommt im Standard nicht vor.

**Standard (`modell/laender/STANDARD.md`, Fassung 1).** Jede Eingabe mit Quellenstatus (amtlich, Original geprüft / amtlich,
maschinell / Sekundärquelle / Prognose / Annahme / Lücke). Staatsschuld und Saldo aus einer gemeinsamen Quelle (Eurostat
`gov_10dd_edpt1`, S13). Drei Pfade: A Status quo, B Regierungsdefizit, C Regierungsschuldenquote (nur mit Prognose). Der
Gewichtungsschritt (Wirkung auf die Klubquote 2028) läuft nur für Länder im Gewichtsbestand der Gesamtrechnung und hat eine
Begründung, wenn er entfällt. Ein gemeinsames Skript `modell/laender/rechne.py` rechnet alle Länder gleich. Je Land eine
Parameterdatei `modell/laender/<cc>.toml` und eine Eingabedatei `daten/aggregate/laender/<cc>_eingaben.md`.

**Umstellung Frankreich.** `modell/frankreich.py` ist durch `rechne.py` ersetzt. Die neue Ausgabe reproduziert die v3.23-Werte
auf zwei Stellen: Pfad A 120,65 %, Pfad B 119,63 %, Pfad C 122,4 % (2028). Klubwirkung 81,29 % (Pfad B) und 81,96 % (Pfad C).
Die Ausgabe ist jetzt `daten/aggregate/laender/fr.json`. Keine Zahl des Konzepts ändert sich.

**Polen (erste Rechnung nach dem Standard).** Schuldenquote 2025: 59,7 % BIP (Eurostat, und GUS: gleiche Zahl). Saldo 2025:
−7,3 % BIP (Eurostat; GUS vorläufig −7,2 %). Ergebnis 2028: Pfad A (Status quo) 75,9 %; Pfad B (Haushaltsentwurf 2027 mit
−7,1 % für 2026 und 2027, 2028 gleich 2027 als Annahme) 75,3 %. Pfad C entfällt: keine Schuldenquoten-Prognose der Regierung
gefunden. Die Gewichtungsrechnung entfällt: Polen steht nicht im Gewichtsbestand der Gesamtrechnung.
- Bevölkerung 2024 (36.559.233) und BIP 2024 (852.229,8 Mio. €) aus Eurostat abgerufen. Vorher war die Bevölkerung nur
  aus einer Sekundärquelle bekannt.
- Quartalswert Schuldenquote 1. Quartal 2026: 61,6 % (Finanzministerium, Sekundärquelle, Kontrollwert, geht nicht in die Rechnung).
- Der Mittelfristplan 2024 (Ziel: Defizit unter 3 % 2028) ist überholt und nicht eingerechnet.
- **Offen:** Preisniveau Polen (PLI, EU27 = 100) nicht abrufbar, zweimal fehlgeschlagen. Ohne diesen Wert ist die
  Dividendenrechnung für Polen nicht möglich. Erneuter Abruf nötig.

**Spanien.** Die Eingaben stehen jetzt unter `daten/aggregate/laender/es_eingaben.md`. Die Rechnung ist noch nicht nach dem
Standard gerechnet (Entscheidung der Initiative ausstehend). Die Eurostat-Werte aus dem Agentenbericht vom 10.10.2026 sind
jetzt per WebFetch bestätigt: Schuld 2025 100,7 %; Saldo 2025 −2,4 %; Sozialbeiträge D61 2024 13,2 %; Umsatzsteuer D211 2024
6,4 %; Gesundheit GF07 2024 6,5 % (vorläufig); Alterssicherung GF1002 2024 10,4 % (vorläufig). Die Abrufe per Shell-Befehl
waren zuvor nicht möglich (HTTP 403). Der Status „vorläufig“ fehlt bei D61 und D211.

**Korrigiert (Arbeitsfehler, nicht veröffentlicht):** Die Datei `es_eingaben.md` hatte den Abschnitt „Abrufe (Eurostat, 10.10.2026)“
mit Werten, die ich nicht selbst abgerufen hatte; sie stammten aus dem Agentenbericht. Die Datei ist korrigiert. Die Werte sind jetzt
per WebFetch bestätigt.

**Geprüft:** `python3 modell/alles.py` (16 Stufen, Stufe „Länderpfade nach Standard“ ersetzt „Frankreich Schuldenpfad“).
Pfad C reproduziert die Regierungsquote (Prüfung in `rechne.py`). Frankreich gegen v3.23: Abweichung 0,00.

**Wodurch aufgefallen:** Auftrag der Initiative. Die Frankreich-Rechnung war nur eine Einzelrechnung; die Vergleichbarkeit
mit weiteren Ländern war nicht festgelegt.

**Offen:** Preisniveau Polen; Schuldenquoten-Prognose Polens; Spanien nach dem Standard rechnen; Umsetzung des Standards in
Webseite und Konzepttexten (Standard 6); Verfassungswortlaut Polens (Art. 15 und 16) nicht geprüft.

*Skripte: `modell/laender/rechne.py` (neu), `modell/frankreich.py` (ersetzt, entfernt). Quellen: Eurostat `gov_10dd_edpt1`,
`nama_10_gdp`, `demo_gind`, `gov_10a_taxag`, `gov_10a_exp` (WebFetch, 10.10.2026); GUS, 01.04.2026; Notes from Poland,
12.06.2026 und 28.08.2026 (Sekundärquellen); gov.pl, Mittelfristplan, 08.10.2024.*

---

### v3.25 — Polen: fehlende Werte nachrecherchiert; Standard Fassung 1.1 (Wohnort, Bestandsanpassung)

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.
Auftrag der Initiative: intensiver nach den fehlenden Werten suchen, notfalls in seriöser Sekundärliteratur.

**Gefunden (Polen).**
- Preisniveau 2024 (Individualverbrauch, EU27 = 100): **70,2** (Eurostat `prc_ppp_ind`, WebFetch). Gegenprobe Deutschland mit derselben
  Abfrage: 109,1 = Repository-Wert, also gleiche Abgrenzung.
- Verlauf der Schuldenquote 2010–2025 (Eurostat): 53,7 … 49,5 (2023), 54,8 (2024), 59,7 (2025).
- Fortschrittsbericht der Regierung zum Mittelfristplan (Ministerrat 28.04.2026, amtlich): Saldo 2026 −6,8 %, Schuld 2026 65,1 %,
  nominales Wachstum 2026 6,2 %. Saldo 2025 −7,3 % bestätigt; die −7,2 % von GUS waren vorläufig.
- EU-Kommission, Frühjahrsprognose 21.05.2026 (amtlich): Saldo −6,5 / −6,3 %, Schuld 64,5 / 68,3 % (2026 / 2027).
- Schuldenstrategie 2027–2030 (Ministerrat Ende September 2026): Schuld nach EU-Definition 67,6 % (2026), 69,3 % (2027), 76,6 % (2030).
  **Sekundärquelle:** rp.pl, Parkiet und Interia nennen übereinstimmend dieselben Werte; das Original (Sejm-Drucksache 3150) war nicht
  abrufbar (Zugangsprüfung).

**Nicht gefunden:** Schuldenquote und Saldo 2028. In der Rechnung: Schuld 2028 **Annahme** 71,7 % (linear zwischen 2027 und 2030),
Saldo 2028 **Annahme** −7,1 % (gleich 2027). Verfassungswortlaut: Abruf wartete auf Freigabe und wurde zurückgezogen.

**Rechnung Polen (nach Standard).** Pfad A 2028: 75,9 %; Pfad B: 75,3 %; Pfad C (Regierung): 67,6 / 69,3 / 71,7 %. Pfad C liegt 2028
3,6 Punkte unter B. Grund: Der Standard setzt 3,0 % nominales Wachstum, Polen erwartet 6,2 %. **Befund:** Die einheitliche
Wachstumsannahme überzeichnet den Schuldenanstieg in Ländern mit hohem nominalem Wachstum. Entscheidung der Initiative, ob das
Wachstum je Land gesetzt wird.
**Bestandsanpassung 2026:** 4,3 Punkte. Die Strategie lässt die Quote um 7,9 Punkte steigen, Saldo und Wachstum erklären 63,3 %. Ursache
nicht geprüft. Das implizite Wachstum im Pfad C (−1,3 % für 2026) ist deshalb keine Wachstumsprognose.

**Wohnort Polen (Euro 2028, nominal).** Dividendenboden 344,43 € je Erwachsenem und Monat (Kind 172,22 €); Tarifstufen 8.266 /
16.533 / 24.799 / 33.065 €. Kaufkraftgleich zu 535,29 € und 12.847 / 25.694 / 38.541 / 51.387 € in Deutschland.

**Standard Fassung 1.1 (`modell/laender/STANDARD.md`).** Neu: lineare Interpolation einzelner Prognosejahre als Annahme (2.3);
Ausweis der Bestandsanpassung, wenn das Regierungswachstum vorliegt (2.3); Abschnitt Wohnort mit Dividendenboden und Tarifstufen
(2.6). Das Preisniveau weiterer Länder steht nur in der Länderdatei, nicht in `preisniveau_2024.csv`, weil diese Tabelle die
Gesamtrechnung speist. Prüfung: Für Frankreich reproduziert der Wohnort-Abschnitt `laendervarianten.json` (Boden 529,40 €, V3a
584,31 €) und `tarif_grundbedarf.json` (12.706 / 25.411 / 38.117 / 50.822 €). Die Stufe „Länderpfade nach Standard“ läuft jetzt
nach den Ländervarianten, weil sie deren Ergebnis liest.

**Korrigiert (Arbeitsfehler).** In v3.24 stand, das Preisniveau Polens sei „nicht abrufbar“. Ursache war meine Abfrage: A01 wurde als
`na_item` gesetzt, gehört aber zur Dimension `ppp_cat`. Mit richtiger Abfrage war der Wert sofort abrufbar. Der in v3.24 genannte
Grund war damit falsch; eine Zahl war nicht betroffen.

**Geprüft:** `python3 modell/alles.py`; Frankreich unverändert gegen v3.23/v3.24 (Pfade, Klubwirkung, Boden, Stufen).

**Wodurch aufgefallen:** Auftrag der Initiative; die Gegenprobe Deutschland machte die frühere Fehlabfrage sichtbar.

**Offen:** Schuld und Saldo Polens 2028 aus dem Original; Schuldenstrategie im Original; Verfassungswortlaut Polens; Wachstum je Land
(Entscheidung); Spanien nach dem Standard rechnen.

*Skripte: `modell/laender/rechne.py` (Wohnort, Bestandsanpassung). Quellen: Eurostat `gov_10dd_edpt1`, `prc_ppp_ind`, `nama_10_gdp`,
`demo_gind` (WebFetch 10.10.2026); Fortschrittsbericht zum Mittelfristplan, gov.pl, 28.04.2026; EU-Kommission, Frühjahrsprognose
2026; rp.pl, Parkiet (29.09.2026), Interia, Strefa Biznesu (05.10.2026), Notes from Poland (Sekundärquellen).*

---

### v3.26 — Spanien nach dem Standard, Polen nachrecherchiert, gemeinsame Klubwirkung; Korrektur 56

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026. Auftrag der Initiative: „wühl dich weiter“.

**Spanien (Rechnung nach Standard, `modell/laender/es.toml`).** Neu gefunden: Stabilitätsziele 2027–2029 (Ministerrat 07.07.2026,
Pressemitteilung des Finanzministeriums, amtlich): Defizit −1,8 / −1,6 / −1,5 %, Schuld 97,6 / 96,4 / 95,3 %. Schuld 2026 99,1 %
daraus abgeleitet. Saldo 2026 −2,1 % und Wachstum real 2,2 % / Deflator 3,1 % aus dem Informe de Progreso Anual (30.04.2026) über
El Debate (Sekundärquelle; Original für den Abruf gesperrt). EU-Kommission Frühjahr 2026 (amtlich): −2,4 / −2,0 %, 99,6 / 98,9 %.
Ergebnis 2028: Pfad A 99,2 %, B 97,5 %, C (Regierung) 96,4 %. Wohnort: Dividendenboden 445,01 €, ausgezahlt (V3a) 491,17 € je
Erwachsenem und Monat; Tarifstufen 10.680 / 21.360 / 32.041 / 42.721 € (Euro 2028, nominal). Prüfungen gegen `laendervarianten.json`
und `tarif_grundbedarf.json` bestanden. Eurostat-Werte aus dem Agentenbericht schon in v3.24 per WebFetch bestätigt.

**Gemeinsame Klubwirkung (Standard Fassung 1.2, 2.4).** Frankreich und Spanien zugleich auf ihrem Regierungspfad (37,3 % des Klub-BIP):
Klubquote 2028 **81,82 %** statt 81,29 %. Einzeln: Frankreich 81,96 %, Spanien 81,15 %; die Summe der Einzelabweichungen (+0,53) ergibt
den gemeinsamen Wert. Ausgabe `daten/aggregate/laender_klub.json`. Die Entscheidung 81,3 oder 82,0 % bleibt bei der Initiative; der
gemeinsame Wert liegt näher an 82,0 %, beruht aber auf zwei von zehn Ländern.

**Polen, nachrecherchiert.** Schuldenstrategie 2027–2030: vierte übereinstimmende Quelle (Forsal/PAP 29.09.2026); nationale Schuld
(PDP) 55,3 % (2026), 58,3 % (2030). Saldo 2027 −7,1 % für den Gesamtstaat bestätigt (PAP Biznes, Überschrift), 2026 ebenso (rp.pl,
Überschrift „tyle ile rok wcześniej“). Weiter **nicht gefunden:** Schuld und Saldo 2028; die Zahlen des mehrjährigen Finanzplans (WPFP)
sind in den erreichbaren Quellen nicht genannt. Annahmen aus v3.25 bleiben.

**Korrektur 56.** In v3.24 stand in `pl_eingaben.md` „282,6 Mrd. Zł (2027)“ in der Zeile zum Gesamtstaatsdefizit. Das ist das
Defizit des Staatshaushalts. Keine Rechnung betroffen.

**Nicht gefunden:** Zahl der Gemeinden in Spanien und Polen (keine Zahl in den erreichbaren amtlichen Seiten); Verfassungswortlaut Polens.
Gesperrt für den Abruf: Informe de Progreso Anual (Ministerium, robots), AIReF-Bericht (robots), Sejm-Drucksache 3150.

**Geprüft:** `python3 modell/alles.py`; Frankreich unverändert; gemeinsame Wirkung gegen die Summe der Einzelwirkungen.

**Wodurch aufgefallen:** Nachrecherche; die Korrektur 56 beim Abgleich der Haushaltsangaben (Forsal/PAP: „deficyt państwa“).

*Skripte: `modell/laender/rechne.py` (gemeinsame Wirkung), `modell/laender/es.toml` (neu). Quellen: Hacienda, Pressemitteilung
07.07.2026; EU-Kommission, Frühjahrsprognose 2026 (Spanien); El Debate 01.05.2026; Forsal/PAP 28.08. und 29.09.2026;
PAP Biznes und rp.pl (Überschriften, 28.08.2026).*

---

### v3.27 — Niederlande und Belgien nach dem Standard; Klubwirkung berichtigt (Korrektur 57)

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026. Auftrag der Initiative: Niederlande und Belgien, je Land
ein Rechercheagent. Die Agenten haben recherchiert; Rechnung, Eurostat-Prüfung und Gegenprüfung der tragenden Werte am Original habe
ich selbst gemacht.

**Niederlande (`modell/laender/nl.toml`).** Schuld 2025 44,4 %, Saldo −1,6 % (Eurostat, geprüft). Regierungspfad aus der Miljoenennota
2027 (15.09.2026, Tabel 1.1, am Original geprüft): Saldo −2,3 / −2,9 / −2,5 %, Schuld 45,6 / 46,9 / 47,4 %; nominales Wachstum
4,6 / 4,4 / 4,2 %. **Widerspruch:** Das CPB (MEV 2027) nennt −2,7 / −2,2 % für 2026 / 2027 (Agent, Drittseite); ungeklärt.
Ergebnis 2028: A 45,3 %, B 48,1 %, C 47,4 %. Wohnort: Boden 593,67 €, V3a 655,25 €; Stufen ab 14.248 € (Euro 2028, nominal).

**Belgien (`modell/laender/be.toml`).** Schuld 2025 107,9 %, Saldo −5,2 % (Eurostat, geprüft). Regierungspfad laut Rechnungshof
(22.05.2026, am Original geprüft): −4,9 / −5,0 / −5,1 %; Schuld nur 2026 (110,3 %), daher **kein Pfad C**. Ergebnis 2028: A 113,9 %,
B 113,3 % (FPB Februar 114,0 %, NBB 114,8 %, Sekundärquellen). Nominales Wachstum der Regierung 2,9 bis 3,3 %, nahe an 3,0 %.
Wohnort: Boden 582,39 €, V3a 642,79 €; Stufen ab 13.977 €. Haushalt 2027 wird bis 13.10.2026 vorgelegt.

**Korrektur 57 (Klubwirkung).** Bis v3.26 hielt die Klubwirkung den Klub-Gesamtsaldo bei −2,93 %: Wich ein Land vom Status quo ab,
trugen die übrigen Länder rechnerisch die Gegenbewegung. Darum ergab „Regierungsdefizit“ für jedes Land 81,29 %, und die Aussage aus
v3.23, das französische Defizit wirke neutral, war ein Artefakt. Jetzt behalten die übrigen Länder ihren eigenen Saldo 2025. Neue Werte
(Klubquote 2028, Referenz 81,29 %): Frankreich C 81,72 % (bisher 81,96 %), Spanien C 80,93 % (81,15 %), Niederlande C 81,49 %;
Frankreich, Spanien und Niederlande gemeinsam (46,4 % des Klub-BIP) **81,55 %**. Frankreich und Spanien allein, aus den Einzelwirkungen
summiert: rund 81,36 % (bisher 81,82 %). Kontrollen: Status quo ergibt die Referenz; die Einzelwirkungen addieren sich zur gemeinsamen.
**Folge für die offene Entscheidung (81,3 oder 82,0 %):** Der bisherige Hinweis „näher an 82,0 %“ trägt nicht mehr; die drei Länder
zusammen bewegen die Klubquote um +0,26 Punkte.

**Polen, Verfassung.** Freigabe der Initiative für sejm.gov.pl erteilt. Die Seite lehnte den Abruf ab („Request Rejected“); der Abruf
über isap.sejm.gov.pl wartete auf eine neue Freigabe und wurde zurückgezogen. Offen.

**Geprüft:** `python3 modell/alles.py`; Wohnort NL und BE gegen `laendervarianten.json` und `tarif_grundbedarf.json`; Frankreich-Pfade unverändert.

**Wodurch aufgefallen:** Die Ausgabe zeigte für vier Länder denselben Klubwert beim Regierungsdefizit.

*Skripte: `modell/laender/rechne.py` (Klubwirkung mit Status quo), `nl.toml`, `be.toml` (neu). Quellen: Eurostat `gov_10dd_edpt1` (WebFetch);
Miljoenennota 2027 (rijksfinancien.nl); Rekenhof Doc 56 1469/002 (lachambre.be); Rechercheagenten (CPB, CBS, Belastingdienst, FPB, NBB,
EU-Kommission, Sekundärquellen, je Zeile gekennzeichnet).*

---

### v3.28 — Ländervergleich nach den Kriterien der Webseite; Arbeitsanweisung für nachfolgende Agenten

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026. Auftrag der Initiative: Arbeitsanweisungen im
Projektraum sichern; neue Rechnung auf Basis der verfügbaren Daten; Ländervergleich nach den Kriterien der Kommunikation auf der Webseite.

**Kriterien (aus `seite/werkzeuge/sprachen/de.json`).** Dividende je Erwachsenem und je Kind 2028; höchstens 28 % mit Stufen am
Grundbedarf; Rechner (Einkommensteuer, Durchschnittssatz, Haushaltsdividende, Sozialabgaben 0); Gemeindebudget je Einwohner und je Kind;
heutige Last (Abgabenkeil, Kapitalertragsteuer, Sozialabgaben); Staatsschulden.

**Rechnung (`modell/laendervergleich.py`, neu; Eingaben `modell/laender/vergleich.toml`).** Elf Länder (zehn Klubländer und Polen).
Rechenregel des Rechners der Seite (Funktion `steuer` in `vorlage.html`). Euro 2028, nominal. Gegenproben: Deutschland 590,81 € je
Erwachsenem = `gesamtrechnung.json`; Tarifstufen und Dividendenboden gegen `tarif_grundbedarf.json` und `laendervarianten.json`.
Ergebnisse (`daten/aggregate/laendervergleich.json`, `.csv`):
- Dividende je Erwachsenem und Monat: von 344,43 € (Polen, nur Boden) und 491,17 € (Spanien) bis 773,30 € (Dänemark). In den
  Klubländern kaufkraftgleich (V3a proportional zum Preisniveau). Polen erhält nur den Boden (V3b) und liegt kaufkraftbereinigt rund
  10 % unter den Klubländern.
- Kaufkraftgleiche Musterhaushalte haben überall denselben Durchschnittssatz: 4,5 % beim 2-fachen, 11,5 % beim 4-fachen Grundbedarf.
- Gleicher Eurobetrag (40.000 € brutto): Durchschnittssatz 6,3 % (Dänemark) bis 14,4 % (Polen); Dividende minus Steuer von +6.747 €
  (Dänemark) bis −1.611 € (Polen) im Jahr.
- Familie (zwei Erwachsene, zwei Kinder, ein Einkommen beim 3-fachen Grundbedarf): Dividende minus Steuer +10.333 € (Polen) bis +23.635 €
  (Dänemark), Deutschland +18.057 €.
- Gemeinde je Einwohner (Pro-Kopf-Variante je Land, v3.17): 2.194 € (Estland) bis 7.863 € (Irland); Polen nicht gerechnet.
- Schulden 2028 im Status quo für alle elf Länder; Regierungspfad für Frankreich, Spanien, Niederlande, Polen.

**Befunde für die Kommunikation.** (1) Die Webseite zeigt die klubweite Gemeindeformel (3.599 € je Einwohner, 12.625 € je Kind),
die Entscheidung v3.17 nennt die Pro-Kopf-Variante je Land; für eine länderspezifische Seite ist das zu klären (Nahtstelle N16).
(2) Die heutige Last ist nur lückenhaft belegt: Abgabenkeil nur Deutschland (47,9 %) und OECD-Schnitt (34,9 %); Kapitalertragsteuer
für DE, FR, ES, NL; Spitzensatz für FR, NL, BE; Sozialbeiträge für DE, FR, ES. Für einen Vergleich „heute gegen 28:28“ fehlen die
Abgabenkeile je Land (OECD Taxing Wages 2025).

**Arbeitsanweisung (`modell/laender/ARBEITSANWEISUNG.md`, neu; Kopie im Projektraum `claude/Arbeitsanweisung-Laender.md`).** Ablauf je
Land, Datenzugang (Eurostat nur über WebFetch, Dimension `ppp_cat`), gesperrte Seiten, Regeln aus den Korrekturen 56 und 57,
Reihenfolge beim Abschluss einer Version, Projektraum.

**Nebenbei behoben:** `rechne.py` las jede `.toml`-Datei im Ordner als Länderdatei; jetzt nur `<cc>.toml` (zweistellig).

**Geprüft:** `python3 modell/alles.py` (17 Stufen, neu „Ländervergleich (Webseite)“); Gegenproben im Skript.

**Wodurch aufgefallen:** Auftrag der Initiative.

*Skripte: `modell/laendervergleich.py` (neu). Quellen: Ergebnisse der Gesamtrechnung, Ländervarianten, Tarif am Grundbedarf und
Länderrechnung; heutige Last je Zeile in `vergleich.toml` belegt (OECD Taxing Wages 2025, Eurostat, nationale Steuerverwaltungen,
Sekundärquellen gekennzeichnet).*

---

### v3.29 — Leitlinie „nationaler Ausgangspunkt, Angleichung durch gleiche Regeln“; Übergangsrechnung der Dividende

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.

**Leitlinie der Initiative (10.10.2026, sinngemäß):** Mindestens für eine Übergangszeit sind unterschiedliche Preise, Dividenden usw. zu
berücksichtigen, weil die Nationalstaaten der Ausgangspunkt sind und nicht generell in Frage gestellt werden. Das spiegelt sich auch in den
Wachstumsannahmen, die auf das Modell und seine Anreize bezogen zu setzen sind. Die Angleichung soll durch die gleichen Regeln und Chancen
über die Zeit selbstständig entstehen; Wettbewerbsanreize für Gemeinden und Regionen bleiben bei allen Solidarmechanismen bestehen.

**Prüfung des geltenden Modells gegen die Leitlinie.**
- Dividende V3a (v3.20, Klubtopf nach Einwohnern × Preisniveau): Die Kaufkraft je Kopf ist vom ersten Jahr an in allen Ländern gleich; die
  Euro-Beträge unterscheiden sich nur nach Preisniveau. Rückfluss eines zusätzlichen Euro BIP je Kopf in die eigene Dividende (Anteil am
  Topf): DE 33,0 %, FR 26,9 %, ES 16,1 %, NL 7,9 %, BE 5,1 %, AT 4,0 %, DK 3,1 %, IE 2,8 %, SI 0,7 %, EE 0,5 %. Für kleine Länder
  fast kein eigener Anreiz. V3a entspricht der Leitlinie damit nicht: Angleichung ist sofort verordnet, nicht durch Regeln erwachsen.
- Gemeinden (Pro-Kopf-Variante je Land, v3.17: 10,35 % des eigenen BIP je Kopf): gleiche Regel, nationaler Ausgangspunkt, voller
  eigener Anreiz; entspricht der Leitlinie. Einen Boden für Gemeinden gibt es nicht.
- Altschulden (Aufschlag je Land über dreißig Jahre): Jedes Land trägt seine eigene Last; entspricht der Leitlinie.
- Wachstum: im ganzen Modell einheitlich (real 0,98 %, nominal 3,0 %); entspricht der Leitlinie nicht.

**Rechnung (`modell/uebergang.py`, `modell/uebergang.toml`, neu).** Derselbe Klubtopf je Jahr (Dividendenanteil am Klub-BIP aus der
Gesamtrechnung) nach zwei Regeln: V3a (geltend) und **V2B** (jedes Land erhält denselben Anteil am eigenen BIP je Kopf; Boden V3b,
halbes Existenzminimum am Wohnort, als Solidarmechanismus, budgetneutral von den übrigen Ländern getragen). Angleichung als Szenario:
beta-Konvergenz des realen Einkommens je Kopf, beta = 0 und beta = 2 % je Jahr (Literaturwert, Barro und Sala-i-Martin 1992; nicht am
Original geprüft, **Annahme**); Preisniveau folgt dem relativen Einkommen mit epsilon = 0,681 (**eigene Schätzung**, Querschnitt der neun
Klubländer ohne Irland 2028, kleine Stichprobe). Anreizzuschlag delta je Land: vorgesehen, Vorgabe 0 (keine Quelle). Selbstprüfung:
V3a ohne Angleichung reproduziert die Länderdividende der Gesamtrechnung 2028, 2035, 2060; V2B ist in jedem Jahr budgetneutral.

**Ergebnisse (Euro je Erwachsenem und Monat, Preise 2028).**
- 2028, V2B gegen V3a: DE 618 / 591, FR 529 / 584, ES 445 / 491, NL 739 / 655, IE 1.241 / 765, BE 624 / 643, AT 642 / 648,
  DK 798 / 773, SI 446 / 493, EE 473 / 523. Auf dem Boden: FR, ES, SI, EE (Aufstockung 1,9 % des Topfes). Unter V2B erhalten
  einkommensstarke Länder mehr, Länder auf dem Boden weniger als unter V3a.
- Kaufkraftspreizung unter V2B (höchste zu niedrigster, ohne Irland): 2028 1,25. Ohne Angleichung steigt sie bis 2060 auf 1,70, weil der
  Boden real konstant bleibt und die Einkommen wachsen; mit beta = 2 % sinkt sie auf 1,32 (2060), die Aufstockung endet um 2045.
- Irland: unter V2B 1.241 € (2028), Folge des verzerrten BIP (2,18-facher Klubschnitt). Unter V3a 765 €.
- Anreiz unter V2B: 100 % Rückfluss oberhalb des Bodens; **0 % für Länder auf dem Boden**, solange sie dort liegen (volle Entzugsrate).

**Entscheidungen der Initiative, die aus der Leitlinie folgen (offen).** (1) V2B als Regel statt V3a, oder ein Pfad von V2B zu V3a.
(2) Irland: BIP-Verzerrung hinnehmen (wie bei den Gemeinden) oder ein bereinigtes Maß. (3) Entzugsrate am Boden: Bei voller Aufstockung
haben Länder auf dem Boden keinen eigenen Anreiz; eine Entzugsrate unter 100 % hielte ihn, kostet aber mehr Topf. (4) Anreizzuschlag
delta je Land und nationale Wachstumsannahmen (eine Quelle fehlt). (5) Boden der Gemeinden. Bis dahin gilt V3a; die Gesamtrechnung ist
unverändert.

**Geprüft:** `python3 modell/alles.py` (18 Stufen, neu „Übergangsrechnung 2028–2060“); Selbstprüfung und Budgetneutralität im Skript.

**Wodurch aufgefallen:** Leitlinie der Initiative; Prüfung der geltenden Regeln auf eigenen Anreiz.

*Skripte: `modell/uebergang.py` (neu). Quellen: Ergebnisse der Gesamtrechnung und der Ländervarianten (Eurostat-Eingänge dort);
Barro, R. J., Sala-i-Martin, X. (1992): Convergence, Journal of Political Economy 100(2) (Literaturwert, nicht am Original geprüft).*

---

### v3.30 — Klarstellung der Leitlinie: gleiches Recht; Anreizbewertung je Land aus dem Abgabenkeil

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.

**Klarstellung der Initiative (10.10.2026, sinngemäß).** Ausgangspunkt sind aus statistischen und politischen Gründen die
Nationalstaaten; Preise und Dividenden unterscheiden sich zwangsläufig. Die Angleichung wird nicht verordnet, sie entsteht aus
gleichen Regeln über die Zeit. Wachstumsannahmen für Prognosen werden je Land angesetzt, aus der Bewertung des Modells und seiner
Anreize (Bereitschaft, Arbeit aufzunehmen, zu investieren, Dynamisierung des Binnenmarkts), möglichst ohne neue Regeln. Gemeinden und
Regionen haben bei Nachteilen die Förderkulissen der EU; Selbstregulierung im Konzept über niedrigere Produktionskosten. Der
Irland-Effekt erfordert keine Sonderbehandlung; gleiches Recht ist zwingend; Streuung kann vorübergehend geduldet werden.

**Begriff.** In v3.29 stand „Boden“ für die Mindestdividende (halbes Existenzminimum am Wohnort, Entscheidung v3.20). „Boden“ bezeichnet
im Konzept aber die Bodenwertabgabe. Ab v3.30 heißt es „Mindestdividende“.

**Übergangsrechnung angepasst (`modell/uebergang.py`).** Hauptvariante jetzt **V2** (gleicher Anteil am eigenen BIP je Kopf, ohne
Aufstockung, ohne Sonderbehandlung Irlands). V2B (mit Aufstockung) bleibt nur als Vergleich. Ausgewiesen wird, wo V2 die Mindestdividende
unterschreitet: 2028 Frankreich 524 statt 529 €, Spanien 401 statt 445 €, Slowenien 389 statt 446 €, Estland 357 statt 473 €
(je Erwachsenem und Monat, Preise 2028). Ohne Angleichung bleiben Slowenien und Estland bis nach 2045 darunter; mit Angleichung (beta 2 %)
Estland bis etwa 2045. **Konflikt mit v3.20:** Dort sichert die Quote die Mindestdividende in jedem Jahr. Unter V2 gilt das nur im
Klubschnitt, nicht in jedem Land. Entscheidung der Initiative: Mindestdividende als Rechenkriterium der Quote im Klubschnitt (ohne
Garantie je Land) oder als Zusage je Land (verlangt eine Aufstockung, also eine Sonderregel).

**Anreizbewertung (`modell/anreize.py`, `modell/anreize.toml`, neu; Daten `daten/aggregate/abgabenkeil_2024.csv`).** Abgabenkeil heute
laut OECD Taxing Wages 2025 (Daten 2024, Alleinstehende, Durchschnittslohn; Rechercheagent, Stichprobe von sechs Werten selbst am Original
geprüft; DE 47,9 % und OECD 34,9 % gleich Repository). Keil unter 28:28: Arbeitskosten 2028 gleich, Arbeitgeberbeiträge gehen in den
Bruttolohn über (Inzidenz voll, **Annahme**; Literatur: zwei Drittel bis 90 %), Einkommensteuer nach den Stufen am Grundbedarf des Landes.
Abbau des Keils: BE 35,2, SI 34,8, EE 31,6, FR 31,3, DE 29,8, AT 29,5, ES 27,7, PL 24,4, DK 22,5, IE 20,9, NL 18,4 Punkte
(Klubschnitt, BIP-gewichtet, 28,5). Wirkung je Punkt auf das BIP-Niveau: 0,28 % (Attinasi u. a. 2019, IJCB 15(4), DSGE-Modell;
Agent las das Original) und 0,14 % (halbe Wirkung wegen Wechselwirkungen, Bassanini und Duval 2006, **Annahme**). **Eingerechnet wird nur
der Unterschied zum Klubschnitt**, aufgebaut über 10 Jahre (**Annahme**): Wachstumszuschlag von +0,19 Punkten je Jahr (Belgien) bis
−0,28 Punkte je Jahr (Niederlande). Der klubweite Niveaueffekt (zentral 8,0 %) wird nicht eingerechnet: Die Literaturwerte gelten für
Änderungen um wenige Punkte, nicht für einen Abbau um 20 bis 35 Punkte. **Einschränkung:** Der OECD-Keil enthält keine Konsumsteuern;
28:28 verlagert Last auf Kapital, Boden, Konsum und Konzerne. Der Vergleich überzeichnet deshalb die Entlastung der Arbeit.

**Ergebnis.** Die Anreize wirken in Richtung Angleichung (stärkster Zuschlag für Länder mit hohem Keil und niedrigerem Einkommen). Die
Kaufkraftspreizung unter V2 (ohne Irland) sinkt 2060 von 1,70 auf 1,64 ohne und von 1,32 auf 1,30 mit beta-Konvergenz.

**Nicht quantifiziert (Literatur widersprüchlich oder ohne passende Größe):** Investitionen und Unternehmenssteuer (Gechert und Heimberger
2021: kein Effekt nach Korrektur des Publikationsbias, gegen die OECD-Rangfolge); Dividende und Arbeitsangebot (von null, Alaska, bis
−4,2 Punkte Erwerbsbeteiligung, US-Experiment 2024); Vertiefung des Binnenmarkts (nur klubweite Szenarien, IWF 2025: +3 % in 10 Jahren);
Bodenwertabgabe (OECD: Verlagerung zur Grundsteuer am wenigsten schädlich; Größe 0,25 bis 1 % je Prozent des Aufkommens, unsicher).
Quellenliste mit Status: Agentenbericht vom 10.10.2026 (im Logbuch zusammengefasst, nicht als Datei).

**Ländervergleich ergänzt.** Abgabenkeil heute und unter 28:28 für alle elf Länder (`laendervergleich.json`).

**Geprüft:** `python3 modell/alles.py` (19 Stufen, neu „Anreize je Land (Abgabenkeil)“); Stufen gegen `tarif_grundbedarf.json`.

**Wodurch aufgefallen:** Klarstellung der Initiative; Prüfung der Variante V2 gegen die Entscheidung v3.20.

*Skripte: `modell/anreize.py` (neu), `modell/uebergang.py`, `modell/laendervergleich.py`. Quellen: OECD, Taxing Wages 2025, Tab. 1.2,
1.4, 1.7; Eurostat `ert_bil_eur_a` (Wechselkurse 2024: 7,4589 DKK, 4,3058 PLN je Euro); Attinasi u. a. (2019); Bassanini und Duval
(2006); González-Páramo und Melguizo (2013); weitere im Text.*

---

### v3.31 — Nachfrageprüfung: Umverteilung, Produktgruppen, Mehrwertsteuer-Label; Prüfbefund Konsumaufkommen

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt; ein Prüfbefund zur Deckung.** 10. Oktober 2026.
Auftrag der Initiative: Den Zusammenhang zwischen höherem verfügbaren Einkommen für rund 95 % der Bevölkerung und Nachfrage/Wachstum erneut
und nach Produkten prüfen; ob die gestaffelten Mehrwertsteuersätze regionales Wachstum vor internationalen Ressourcenkonsum setzen.

**Klarstellung zu v3.30.** Der klubweite Angebotseffekt (Abbau des Abgabenkeils, zentral 8,0 % BIP-Niveau) war dort bewusst nicht
eingerechnet, nur die Unterschiede zwischen den Ländern. Ein Nachfragekanal fehlte im Modell ganz. Der geringe Effekt in v3.30 war eine
Folge dieser Methode, kein Befund über die Wirkung.

**Rechnung (`modell/nachfrage.py`, `modell/nachfrage.toml`, neu).** Grundlagen: zwei Rechercheagenten (Konsumneigung und Multiplikatoren;
Produktgruppen, Importanteile, Elastizitäten, Erfahrungen mit ermäßigten Sätzen), je Zeile mit Status in `nachfrage.toml`.
1. **Umverteilung und Nettoentlastung.** Die Nettoentlastung insgesamt beträgt nur 1.11 % des BIP; der größere
   Teil ist Umverteilung (das Konsum-Label hebt den effektiven Satz im Kernmodell von 16,5 auf 20 % und nimmt einen Teil des Nettogewinns
   über die Preise zurück). Mehrkonsum = Umverteilung (Szenarien 2, 4, 6 % des BIP, **Annahme**, kein Verteilungsmodell für den Klub) ×
   Abstand der Konsumneigung unten gegen oben (0,1 HFCS bis 0,3 Italien) + Entlastung × Konsumneigung (0,2 bis 0,5), abzüglich
   Importanteil 20 % und Abschlag für Geldpolitik und Angebotsgrenzen (0 bis 50 %, **Annahme**). Ergebnis: BIP-Niveau
   **+0.17 bis +1.88 %**, zentral +0.71 %. Ein Niveaueffekt, dauerhaft nur, weil die Dividende dauerhaft ist; kein
   zusätzliches jährliches Wachstum. Kein Modell einer steuerfinanzierten Bürgerdividende mit Nachfragewirkung für Europa gefunden.
2. **Angebot.** Klubweiter Niveaueffekt aus dem Abbau des Abgabenkeils: Obergrenze 4,0 bis 8,0 % (lineare Übertragung, nicht gedeckt).
3. **Mehrwertsteuer-Label nach Produktgruppen** (Budgetanteile Eurostat hbs_str_t223 2020; Importanteile Insee 2019; Elastizitäten
   Labandeira u. a. 2017, Andreyeva u. a. 2010, Dybczak u. a. 2010; Weitergabe Senkung 30 %, Erhöhung 80 %; Referenz deutsche Sätze).
   Zuordnung der Gruppen ist eine **Annahme dieser Prüfung**. Ergebnis: Der Inlandsanteil am Konsum ändert sich praktisch nicht
   (+0.004 Punkte bei Zuordnung nach Datenblatt; -0.069 Punkte bei steuernder Zuordnung). Gründe: geringe Satzabstände gegenüber heute
   (17/22/5 gegen 19/19/7 %), unvollständige Weitergabe von Senkungen (Literatur 13 bis 50 %), unelastische Nachfrage. Bei unelastischer
   Nachfrage steigen die Ausgaben für teurer besteuerte Güter, obwohl die Mengen sinken (Kraftstoffe, Fahrzeuge etwa −4 bis −6 %);
   das Geld fließt nicht in regionale Dienste. Das Label senkt den Ressourcenverbrauch, lenkt aber kaum Kaufkraft in die Region.
   Erfahrungen: Reparatur-Ermäßigung Schweden 2017 ohne messbaren Effekt; Restaurants Finnland 2010 ohne, Schweden 2012 mit
   Beschäftigungseffekt (+5 Punkte je Jahr); Lebensmittel haben hohe Importanteile (Frankreich 40 bis 52 %).

**Prüfbefund Konsumaufkommen (Entscheidung offen, keine Zahl geändert).** Das Kernmodell setzt den effektiven Labelsatz mit 20 % an
(Gewichte 10/10/20/30/30 % für A+ bis D, als Annahme gekennzeichnet): 60 % des Konsums in C und D. Bei einer Zuordnung nach den
Produktgruppen des Datenblatts ergeben sich 14.94 % (Konsumaufkommen 6.98 statt 8.95 % des BIP, -1.97), bei einer
steuernden Zuordnung mit 58.9 % in C/D 16.88 % (7.76 % des BIP, -1.19). Die Deckungslücke (1,73 Punkte) würde damit
um 1,2 bis 2,0 Punkte größer. Zu entscheiden: Zuordnung der Produkte zu den Labelstufen und die Sätze; danach Neurechnung der Deckung.
Mögliche Korrektur, sobald die Zuordnung feststeht.

**Was die Prüfung für die Kommunikation bedeutet.** Die Aussage „mehr Geld für 95 %“ ist eine Verteilungsaussage. Gesamtwirtschaftlich
ist die Nachfragewirkung ein moderater Niveaueffekt; der größere mögliche Effekt liegt auf der Angebotsseite (Arbeit), ist aber nicht
belegt. Die These „Label setzt regionales Wachstum vor Ressourcenkonsum“ trägt für die Mengen (Ressourcen), nicht für die Wertschöpfung.

**Geprüft:** `python3 modell/alles.py` (20 Stufen, neu „Nachfrageprüfung“).

**Wodurch aufgefallen:** Nachfrage der Initiative; beim Abgleich der Produktgruppen mit den Labelgewichten des Kernmodells.

*Skripte: `modell/nachfrage.py` (neu). Quellen: Jappelli und Pistaferri (2014); Albacete, Fessler, Pekanov (SUERF, HFCS); Christelis u. a.
(2020); Roeger und in 't Veld (2010); Eurostat hbs_str_t223 (2020), icw_sr_10; Insee Première 1756 (2019); EZB Wirtschaftsbericht 3/2024;
Labandeira u. a. (2017); Andreyeva u. a. (2010); Dybczak u. a. (2010); Benzarti u. a. (2017); Kosonen (2015); Harju, Kosonen, Nordström
Skans (2018); Tillväxtanalys (Schweden, Restaurants); Benedek u. a. (2015, IWF). Status je Zeile in `nachfrage.toml`.*

---

### v3.32 — Nachfrageprüfung: Sichtbarkeit (Salienz) des Mehrwertsteuer-Labels

**Art der Änderung: PATCH, keine Zahl des Konzepts bewegt.** 10. Oktober 2026. Hinweis der Initiative: Ungeprüft ist, wie das Label
psychologisch wirkt; es gibt Kunden eine leichte Handhabe, umwelt- und regionalbewusster zu kaufen; vermutlich keine ausreichende Evidenz.

**Evidenz (selbst abgerufen, Kurzfassungen).** Richtung belegt, Größe nicht: Chetty, Looney, Kroft (2009, AER 99(4); FEDS 2009-11):
Ausweis des Steueranteils am Regal senkte die Nachfrage der betroffenen Produkte um 8 %; Kunden reagieren auf verdeckte Steuern zu
schwach. Potter u. a. (2021, Environment and Behavior), systematische Übersicht, 56 Studien: Umweltlabels erhöhen die Wahl nachhaltiger
Lebensmittel überwiegend (60 von 76 Vergleichen), 41 Studien hypothetisch, 39 mit unklarem oder hohem Verzerrungsrisiko, keine gepoolte
Effektgröße. Für ein Label, das Steuersatz und Umweltstufe verbindet, keine Studie gefunden. Die Vermutung der Initiative trifft zu.

**Rechnung.** Faktor auf die Preiselastizitäten bei steuernder Zuordnung (1,0 / 1,5 / 2,0 / 3,0; **Annahme**). Veränderung des
inländischen Wertschöpfungsanteils am Konsum, in % des BIP: −0,04 / +0,03 / +0,10 / +0,24 (volle Weitergabe: −0,05 / +0,04 / +0,13
/ +0,32). Die Umlenkung in die Region beginnt erst ab etwa der 1,3-fachen Preisreaktion der Literatur; selbst bei dreifacher Reaktion
bleibt sie unter 0,35 % des BIP. Der Ressourceneffekt (Mengen) wird mit der Salienz größer.

**Folge.** Für die Kommunikation tragfähig: Das Label macht den Umweltgehalt sichtbar und senkt den Ressourcenverbrauch; die Richtung der
Verhaltenswirkung ist belegt. Nicht belegt: eine nennenswerte Verlagerung von Wertschöpfung in die Region. Ein Feldversuch wäre der Weg,
die Größe zu bestimmen.

**Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Hinweis der Initiative.

*Skript: `modell/nachfrage.py`. Quellen: Chetty, Looney, Kroft (2009); Potter u. a. (2021).*

---

### v3.33 — Entscheidungen der Initiative zur nächsten Fassung; Tragfähigkeitsprüfung

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.

**Entscheidungen der Initiative (10.10.2026): „Wir folgen allen Empfehlungen“** der Entscheidungsvorlage
(`projekt/Entscheidungsvorlage-2026-10-10.md`): E1 Mehrwertsteuer-Label Option C (steuernde Zuordnung, verbindliche Produktliste nach
Ressourcen- oder CO₂-Fußabdruck je Euro); zusätzliche Lücke über die Dividende (Lesart: Vorschlag „E1 C mit Dividende“ aus der Antwort vom
10.10.2026); E2 Dividende V2 (gleicher Anteil am eigenen BIP je Kopf), Mindestdividende als Rechenkriterium im Klubschnitt; E3 Gemeindeformel
je Land (Pro-Kopf-Variante, v3.17); E4 Schuldenquote 2028 81,3 % beibehalten. Umsetzung in der Gesamtrechnung erst mit dem Textentwurf.

**Tragfähigkeitsprüfung (`modell/tragfaehigkeit.py`, neu).**
- Deckung: Die modellierten Steuerbasen tragen bisher 30.17 % des BIP gegen eine Quote von 31.9 % (Lücke 1.73, seit v3.12 offen, B12).
  Nach E1 C 28.98 % (Lücke **2.92**).
- **Widerspruch in den Empfehlungen:** Die zusätzliche Lücke (1.19 Punkte) über die Dividende zu schließen (−10.0 %), unterschreitet die
  Mindestdividende im Klubschnitt in 10 Jahren (2028 99.3 %, Tiefpunkt 96.9 % 2035). Das verletzt das Kriterium v3.20, das nach E2 im
  Klubschnitt weiter gilt. Die ganze Lücke über die Dividende (−24.5 %) läge 23 Jahre darunter. Die Empfehlung war nicht mit dem Kriterium
  abgestimmt (Fehler der Vorlage, offen geführt).
- Tarif (grob, deutsche Basis): höhere Spitzensätze bringen wenig (32 % +0.39, 35 % +0.64 Punkte). Die Lage der Stufen wirkt stärker:
  bei 28 % Obergrenze Stufen beim 1-, 1,5-, 2- und 3-fachen Grundbedarf +1.14; Sätze 0/12/20/24/28 +0.83; 0/10/20/26/35 +1.32.
  Die Obergrenze 28 % ist nicht der Engpass; der Hebel liegt in der Progression der mittleren Einkommen.
- Wachstum: Die Quote ist nach der strengen Lesart gesetzt (real 0 % = nominal 2 %, Korrektur 51). Ohne reales Wachstum liegt die Dividende
  2060 bei 524 € statt 735 € (Deutschland, Preise 2028); die Mindestdividende hält. Das Konzept braucht kein Wachstum, um zu tragen.
- Lenkung: CO₂ trägt 1.67 % des BIP zur Deckung bei; diese Grundlage schrumpft mit Zielerreichung. Steuernde Abgaben sind keine
  dauerhafte Finanzierungsquelle.
- Wachstum und Kreislaufwirtschaft: Haberl u. a. (2020, Environmental Research Letters, doi 10.1088/1748-9326/ab842a): relative Entkopplung
  häufig, absolute langfristige Entkopplung selten; beobachtete Raten reichen für rasche absolute Minderungen nicht; Suffizienz und absolute
  Reduktionsziele nötig (Kurzfassung selbst gelesen).

**Offen (Entscheidung der Initiative):** wie die zusätzliche Lücke geschlossen wird, ohne die Mindestdividende zu verletzen: Stufen bei 28 %
tiefer legen (z. B. 1/1,5/2/3-facher Grundbedarf) oder weitere Bausteine; die alte Lücke (1,73) bleibt Aufgabe B12.

**Geprüft:** `python3 modell/alles.py` (21 Stufen, neu „Tragfähigkeit (Entscheidungen)“). **Wodurch aufgefallen:** Frage der Initiative.

*Skript: `modell/tragfaehigkeit.py` (neu). Quellen: Gesamtrechnung, Nachfrageprüfung, Kernmodell (Tarif); Haberl u. a. (2020).*

---

### v3.34 — Justierungspakete (29:29, Erbschaft, Vermögen, Mehrwertsteuer) und Stabilitätsprüfung

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026. Vorschlag der Initiative: mehrere kleine Justierungen
(29:29 in allen Konzeptteilen; Erbschaftsfreibetrag 100.000 € je Erwerb; Vermögensteuer etwas höher; Mehrwertsteuer über Produktgruppen
oder Sätze leicht anheben). Ziel: Stabilität auf allen Ebenen, keine Belastung durch kleine Ausreißer.

**Rechnung (`modell/justierung.py`, neu).** Hebel in Punkten des BIP (grob; Einkommensteuer über das Kernmodell, deutsche Basis; übrige
proportional): Einkommensteuer 29 % +0.10; mit Stufen beim 1-/1,5-/2-/3-fachen Grundbedarf +1.29; Kapital 29 % +0.04;
Konzerne 29 % +0.13; Erbschaftssatz 29 % +0.03; Erbschaftsfreibetrag 100.000 € +0.09 bis +0.18 (**Annahme**: 100.000 bis
200.000 Erwerbe über 200.000 € je Jahr in Deutschland; die Landesstatistik Rheinland-Pfalz 2024 zeigt die Konzentration, aber nur nach
heutigen Freibeträgen); Vermögensteuer 1,25 % +0.10, 1,5 % +0.19 (**Annahme**: die Hälfte der Mehreinnahme geht durch Ausweichen
verloren); Mehrwertsteuer-Label (steuernd) alle Sätze +1 +0.38 (effektiv 17.88 %), +2 +0.77 (effektiv 18.88 %).
Pakete gegen die Lücke nach E1 C (2.92):
  - P1 moderat (29:29, Erbe 100k, Vermögen 1,25 %, Label +1): +0.92 Punkte; Lücke danach 2.0; Reserve -1.12
  - P2 kräftig (29:29, Erbe 100k, Vermögen 1,5 %, Label +2): +1.4 Punkte; Lücke danach 1.52; Reserve -0.64
  - P3 wie P2, Stufen 1/1,5/2/3 bei 29 %: +2.59 Punkte; Lücke danach 0.33; Reserve 0.55

**Stabilität.** Reserve heute: Der Dividendenanteil darf um 0.88 Punkte des BIP sinken, bevor die Mindestdividende im Klubschnitt
in einem Jahr bricht (Tiefpunkt 108,7 %, 2032). Jede Deckungslücke zehrt diese Reserve auf. Schon die alte Lücke (1,73) übersteigt sie;
das geltende Konzept ist also nur stabil, wenn die Lücke tatsächlich geschlossen wird. Vorgeschlagenes Kriterium: Lücke geschlossen und
Reserve mindestens 1,0 Punkte. **Kein Paket erfüllt es**; P3 kommt am nächsten (Restlücke 0,33, Reserve 0,55). Dach: Abstand zur Obergrenze
35 % im Zentralfall 0,92 Punkte; alle drei Finanzierungsrisiken zugleich −0,59; Verteidigung 3,5 % (Haager Zusage) −2,30.

**Einordnung.** 29:29 bringt zusammen nur +0,30 Punkte; der größte Hebel ist die Lage der Tarifstufen, danach die Mehrwertsteuer. Das
Schließen der Lücke erhöht die Abgabenlast nicht über die Quote von 31,9 % hinaus; es sorgt dafür, dass die Instrumente die Quote
tatsächlich erbringen. Die Umbenennung (TAX 28:28, Initiative 28:28) wäre eine eigene Entscheidung.

**Offen (Entscheidung der Initiative):** Paket; zusätzlicher Hebel für die Reserve (etwa 0,8 Punkte, z. B. Label +3 oder Bausteine);
Stabilitätsmechanismus ohne neue Steuer (Ausgleichsrücklage, Dividende über einen gleitenden Mehrjahresdurchschnitt wie beim Alaska-Fonds);
Name 28:28 oder 29:29; Obergrenze des Dachs gegen kombinierte Risiken und Verteidigungszusage.

**Geprüft:** `python3 modell/alles.py` (22 Stufen, neu „Justierung und Stabilität“). **Wodurch aufgefallen:** Vorschlag der Initiative;
Reserve gegen Lücke gestellt.

*Skript: `modell/justierung.py` (neu). Quellen: Gesamtrechnung, Tragfähigkeit, Nachfrageprüfung, Kernmodell; Statistisches Landesamt
Rheinland-Pfalz, Erbschaft- und Schenkungsteuerstatistik 2024 (Bericht L4093, Tabelle T 5).*

---

### v3.35 — Entscheidungen: 28:28 bleibt, Verteidigung außen vor, Strategie Verwaltung; Belege zur Digitalisierung; Korrektur 58

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.

**Entscheidungen der Initiative.** (1) Verteidigung wird weiter nicht gesondert gerechnet: Der Wert von 3,5 % ist politisch gesetzt und
sagt nichts über die Verteidigungsfähigkeit. (2) Die Obergrenze des Dachs (35 %) kann notfalls angepasst werden. (3) Statt neuer Steuern
eine Strategie und Verpflichtung zu Entbürokratisierung, Digitalisierung und Aufgabenstreichung, damit die Budgets besser wirken. (4) 28:28
bleibt; die übrigen Potenziale werden ausgeschöpft (kein 29:29).

**Belege zur Digitalisierung der Verwaltung (Rechercheagent, Kernzahlen selbst nicht am Original geprüft).** Keine Ex-post-Messung gefunden,
die einen Rückgang der Verwaltungsausgaben am BIP durch Digitalisierung zeigt. Ex-ante für Deutschland: NKR/Fraunhofer FOKUS 2015, Verwaltung
−0,7 Mrd. € je Jahr (60 Leistungen); NKR/McKinsey 2017, Verwaltung −3,9 Mrd. € je Jahr, einmalige Investition 2,5 Mrd. €; zusammen etwa
0,02 bis 0,12 % des BIP. Eurostat COFOG 2024: Verwaltungskern (GF0101) DE 2,1, DK 1,7, EE 1,8, EU 1,9 % des BIP; Estlands GF01 ist seit 2014
nicht gesunken. Kausale Belege nur für einzelne Prozesse (z. B. elektronische Steuererklärung Tadschikistan −40 % Aufwand; elektronische
Zahlungen Indien −19 bis −24 % Programmausgaben durch weniger Abfluss). Umsetzungsrisiken: OZG Ende 2022 19 % der Leistungen online
(Bundesrechnungshof); IT-Projekte im Mittel +27 % Kosten (Flyvbjerg/Budzier 2013). Als Werbung, nicht als Beleg: „2 % des BIP“ (e-Estonia,
Erwartung von 2002), „1.407 Jahre Arbeitszeit“ (Hersteller), „5 Mrd. €“ (EU, hochgerechnet aus einem dänischen Programm), „146 Mrd. €“ (ifo,
BIP-Verlust, keine Verwaltungskosten). **Annahme für das Modell:** Verwaltung netto 0,1 bis 0,3 % des BIP nach 8 bis 12 Jahren; mehr als
0,4 Punkte spekulativ. Aufgabenstreichung ist davon getrennt und nur mit benannten Aufgaben bezifferbar.

**Rechnung (`modell/justierung.py`, erweitert).** Pakete nach den Entscheidungen (28 % bleibt; Stufen beim 1-/1,5-/2-/3-fachen Grundbedarf;
Erbschaftsfreibetrag 100.000 €; Vermögensteuer 1,5 %; Mehrwertsteuer +2 oder +3; Verwaltung 0,1 oder 0,3):
  - P4 Entscheidung v3.35 (28 % bleibt, Stufen 1/1,5/2/3, Erbe 100k, Vermögen 1,5 %, Label +2, Verwaltung 0,1): +2.34; Lücke 0.58; Reserve 0.3
  - P4 wie oben, Verwaltung 0,3: +2.54; Lücke 0.38; Reserve 0.5
  - P5 wie P4, Label +3, Verwaltung 0,1: +2.71; Lücke 0.21; Reserve 0.67
  - P5 wie P4, Label +3, Verwaltung 0,3: +2.91; Lücke 0.01; Reserve 0.87
Nur mit allen Hebeln am oberen Rand (Mehrwertsteuer +3, effektiv 19.88 %, Preise etwa +2,9 % gegen heute; Verwaltung 0,3)
ist die Lücke geschlossen; die Reserve der Mindestdividende bleibt mit 0,87 Punkten unter dem Vorschlag von 1,0.

**Korrektur 58** (Abschnitt 4): Aussage im Gesamtkonzept zur Verwaltung in Estland und zu 1,02 Punkten des BIP nicht belegt.

**Offen:** Stabilitätsmechanismus ohne neue Steuer (Ausgleichsrücklage, Dividende über gleitenden Mehrjahresdurchschnitt); Liste der Aufgaben,
die gestrichen werden können; Wahl zwischen P4 und P5.

**Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Frage der Initiative nach Belegen; Abgleich mit dem Konzepttext.

*Skript: `modell/justierung.py`. Quellen: NKR/Fraunhofer FOKUS (2015); NKR/McKinsey (2017); NKR-Jahresbericht 2025 (BT-Drs. 21/3050); Eurostat
gov_10a_exp (COFOG GF01, GF0101); Okunogbe und Pouliquen (2022); Banerjee u. a. (2020); Bundesrechnungshof (2023); Flyvbjerg und Budzier (2013);
e-Estonia; Falck, Guo, Pfaffl (ifo Schnelldienst 11/2024).*

---

### v3.36 — Ablösung statt Umbau der Verwaltung; Dach auf Kernaufgaben; stabile Pakete

**Art der Änderung: MINOR, keine Zahl des Konzepts bewegt.** 10. Oktober 2026.

**Leitlinie der Initiative (10.10.2026, sinngemäß).** Größere Digitalisierungsgewinne entstehen, wenn neue Regeln von Beginn an digital
umgesetzt werden; die bisherigen Belege betreffen überwiegend nachträglich umgebaute Strukturen. 28:28 strebt eine Ablösung an, die alte
Regeln und Verfahrenswege vollständig ersetzt; 1 % des BIP erscheint dann eher vorsichtig (Vergleich: Onlinehandel gegen Ladengeschäft bei
Raum- und Personalkosten). Das Dach beschränkt sich auf die benannten Kernaufgaben; Steuerungs- und Subventionsmechanismen werden weitreichend
auf die Gemeindeebene verlagert (Beispiel Agrarförderung: Schutz über die Mehrwertsteuer und ihre Regionalität, notfalls handelt das Dach
protektionistisch, ohne einzelnen Ländern Subventionen zuzuweisen). Eine gewisse Freiheit gegenüber Studien, die im heutigen Regelwerk
verhaftet sind, ist angebracht.

**Umsetzung als prüfbare Setzung.** Statt Umbau-Studien die Verwaltungskosten der Verfahren, die 28:28 abschafft:
- Verwaltung der Sozialschutzsysteme in Deutschland: 1,12 % des BIP (Eurostat tps00098: Sozialschutzausgaben 31,28 % des BIP; tps00101:
  davon Verwaltung 3,59 %; 2024 vorläufig). Entfällt durch Steuerfinanzierung ohne Beiträge und automatische Dividende zu 40 bis 70 %
  (**Setzung**; Gesundheit und Rentenübergang bleiben zu verwalten): 0,45 bis 0,78 % des BIP. Übertragung auf den Klub: **Annahme**.
- Dach: Der Posten „Wirtschaftsraum, Agrar, Energie, Netze“ (3,75 %) entspricht den Wirtschaftsausgaben (COFOG GF04, EU27 2024: 5,3 %)
  ohne örtlichen Verkehr (1,48 bei den Gemeinden). Zerlegung EU27 2024: Verkehr 2,5; allgemeine Wirtschafts- und Arbeitsmarktangelegenheiten
  1,0; Energie 0,6; Landwirtschaft 0,3; Industrie und Bau 0,2; Rest 0,7 (`daten/aggregate/dach_verwaltung_2024.csv`). Abgabe an die
  Gemeindeebene ohne zusätzliches Gemeindebudget: S1 Landwirtschaft, Industrie, halbe Energie = 0,8; S2 dazu halbe allgemeine Wirtschafts-
  und Arbeitsmarktangelegenheiten und halber Rest = 1,65 (**Setzung**; EU27-Anteile als Annahme für den Klub; Energie 2024 noch erhöht).

**Pakete (`modell/justierung.py`, erweitert; Grundlage: 28 % bleibt, Stufen 1/1,5/2/3, Erbschaftsfreibetrag 100.000 €, Vermögensteuer 1,5 %):**
  - P6 ohne Mehrwertsteuer-Erhöhung, Ablösung 0,45, Dach S1: +2.72; Lücke 0.2; Reserve 0.68; stabil nein
  - P7 Mehrwertsteuer +1, Ablösung 0,45, Dach S1: +3.1; Lücke -0.18; Reserve 1.06; stabil ja
  - P8 ohne Mehrwertsteuer-Erhöhung, Ablösung 0,45, Dach S2: +3.57; Lücke -0.65; Reserve 1.53; stabil ja
  - P6 ohne Mehrwertsteuer-Erhöhung, Ablösung 0,78, Dach S1: +3.05; Lücke -0.13; Reserve 1.01; stabil ja
  - P7 Mehrwertsteuer +1, Ablösung 0,78, Dach S1: +3.43; Lücke -0.51; Reserve 1.39; stabil ja
  - P8 ohne Mehrwertsteuer-Erhöhung, Ablösung 0,78, Dach S2: +3.9; Lücke -0.98; Reserve 1.86; stabil ja
Ohne Mehrwertsteuererhöhung ist das Konzept stabil, wenn die Ablösung am oberen Rand gelingt (P6) oder das Dach weitreichend entlastet wird (P8).

**Rechtliche Vorbehalte (nach Kenntnis, in dieser Sitzung nicht geprüft):** Eine Mehrwertsteuer, die nach Herkunft unterscheidet, wäre mit dem
Diskriminierungsverbot (Art. 110 AEUV) und der Mehrwertsteuer-Systemrichtlinie nicht vereinbar; zulässig erscheint eine Staffelung nach
Fußabdruck, die Transportwege einschließt und so regionale Ware indirekt begünstigt. Außenzölle und Handelspolitik sind ausschließliche
Zuständigkeit der EU (Art. 3 Abs. 1 AEUV); ein Klub von EU-Staaten kann nicht selbst protektionistisch handeln.

**Offen:** Wahl des Pakets; Aufgabenliste des Dachs im Einzelnen; Stabilitätsmechanismus (Ausgleichsrücklage) als zusätzliche Sicherung.

**Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Leitlinie der Initiative.

*Skript: `modell/justierung.py`. Quellen: Eurostat gov_10a_exp (COFOG GF04 und Teilposten, EU27 2024), tps00098, tps00101 (WebFetch 10.10.2026).*

### v3.37 — Entscheidungen eingerechnet: Quote 30,2 %, Deckung ohne Lücke; Korrektur 59

**Art der Änderung: MAJOR in der Rechnung (Quote, Obergrenze, Deckung bewegt); die veröffentlichten Texte bleiben bis zur Freigabe auf
v3.36 (Fassung 7. Oktober 2026).** 10. Oktober 2026.

**Entscheidungen der Initiative (10.10.2026).** „Wir folgen allen Empfehlungen“ (E1 C, E2 V2 im Klubschnitt, E3 je Land, E4 81,3 %); Paket
P8; 28:28 bleibt; Verteidigung bleibt außer Betracht; die Obergrenze des Dachs darf sich anpassen. Zum Rechtsrahmen: „Auf den aktuellen
Rechtsrahmen der EU nehmen wir nicht zwingend Rücksicht. Eine starke Gruppe kann neue Forderungen durchsetzen.“ Die Vorbehalte aus v3.36
(Art. 110 AEUV, Art. 3 Abs. 1 AEUV) bleiben als Sachinformation im Logbuch; sie sind keine Bedingung der Rechnung mehr.

**Umsetzung in `modell/gesamtrechnung.py` (neue Parameter in `gesamtrechnung.toml`, Originale in `modell/rahmen/` unverändert):**
- `dach_kuerzung_wirtschaftsraum` 1,65: Posten „Wirtschaftsraum, Agrar, Energie, Netze“ 3,75 → 2,10 % des BIP; Summe A 8,94 → 7,29.
  Die Selbstprüfung gegen `final.pfad()` rechnet weiter mit dem Original (33 Jahre exakt).
- `label_effektiv_pct` 16,88 (E1 C): Konsum 8,95 → 7,76 % des BIP (deutsche Basis). `tragfaehigkeit.py` bricht ab, wenn der Parameter von
  `nachfrage.json` abweicht.
- `tarif_stufen_vielfache` 1/1,5/2/3: Einkommen 7,78 → 8,92 % (Kernmodell, grob); Stufen DE 2028: 12.847 / 19.270 / 25.694 / 38.541 €.
  Länderrechnungen, Anreize und Ländervergleich lesen die Vielfachen jetzt aus `tarif_grundbedarf.json`.
- Erbschaftsfreibetrag 100.000 €: +0,13 % (150.000 Erwerbe über 200.000 € je Jahr, **Annahme**; Satz 28 % statt 29 % in v3.36).
- Vermögensteuer 1,5 %: +0,19 % (Hälfte Ausweichen, **Annahme**).
- E2/E3: `tabelle_laender_div` führt V2 (gleicher Anteil am eigenen BIP je Kopf) und die Gemeindeformel je Land; V3a zum Vergleich.
  2028 unter der Mindestdividende (halbes Existenzminimum am Wohnort): FR 522/529, ES 399/445, SI 388/446, EE 356/473 €
  je Erwachsenem und Monat (Euro 2028, nominal). Das Kriterium der Quote gilt für den Klubschnitt.

**Bewegte Zahlen:**

| Größe | v3.36 | v3.37 |
|---|---|---|
| strenge Mindestquote | 31,85 | 30,20 |
| Quote (% des BIP) | 31,9 | **30,2** |
| Obergrenze (% dessen, was A einzieht) | 35 | **32** |
| Ebene A 2028 / Höchstbedarf (2035) | 9,64 / 10,59 | 7,99 / 8,94 |
| Deckung nachgewiesen (deutsche Basis) | 30,17 | **30,44** |
| Lücke (Quote minus Deckung) | 1,73 (nach E1 C 2,92) | **−0,24** (Überschuss, 33 Mrd € Klub 2028) |
| Reserve bis zur Mindestdividende / mit Überschuss | 0,88 / – | 0,84 / **1,08** (Kriterium 1,0: stabil) |
| Entlastung gegen heute | 1,11 | 2,81 Punkte (388 Mrd € Klub 2028) |
| Klubdividende 2028 je Einwohner (€ im Monat, Euro 2028) | 537 | 535 (durch das Kriterium bestimmt; Unterschied aus der Rundung der Quote) |

Die Dividende bleibt nahezu gleich, weil die Quote aus der Mindestdividende abgeleitet wird: Die Kürzung des Dachs senkt die Quote, nicht die
Dividende. Eine höhere Dividende statt einer niedrigeren Quote wäre eine eigene Entscheidung (Quote 31,9 hielte die Dividende um 1,65 Punkte
des BIP höher, die Deckung reichte dann nicht).

**Nebenwirkung der steileren Stufen (`modell/anreize.py`):** Der Abgabenkeil unter 28:28 steigt bei den Modellhaushalten um 2,3 bis 3,5
Punkte (z. B. 18,10 → 20,42 %); der Abbau des Keils gegen heute sinkt im Klubschnitt von 28,5 auf 25,8 Punkte, der nicht eingerechnete
Niveaueffekt des Angebots (Obergrenze, zentral) von 8,0 auf 7,2 %. Die Übergangsrechnung (V2B) braucht 2,03 statt 1,86 % des Topfes.

**Obergrenze 32 %:** nicht gedeckt sind die Häufung der drei Finanzierungsrisiken (32,04 %) und Verteidigung 3,5 % (33,84 %; außer Betracht).

**Korrektur 59** (Abschnitt 4): Ablösung der Sozialverwaltung in v3.36 gegen die Lücke der Quote gerechnet.

**Folgen außerhalb der Rechnung:** `modell/pruefe_konzept.py` meldet 21 von 22 Stufen; die Stufe „Gesamtkonzept gegen Rechnung“ schlägt
**bewusst** fehl, weil Gesamtkonzept, Kurzfassung und Webseite bis zur Freigabe des Textentwurfs auf v3.36 stehen. `justierung.py` rechnet
seit v3.37 auf eingefrorenen Eingängen (Stand v3.36, `daten/aggregate/justierung_basis_v336.json`) und dokumentiert die Entscheidungsgrundlage.

**Grenzen:** Deckung auf deutscher Basis (B12 auf Klubebene offen); Einkommensteuer aus dem Kernmodell mit sieben Gruppen; Erbschaft,
Vermögen, Dach S2 und die Übertragung der EU27-Anteile auf den Klub sind Annahmen oder Setzungen. Der Überschuss von 0,24 Punkten liegt
innerhalb dieser Unsicherheit.

**Geprüft:** `python3 modell/alles.py` (21 von 22, siehe oben). **Wodurch aufgefallen:** Auftrag der Initiative („P8 … Go on“).

*Skripte: `modell/gesamtrechnung.py`, `modell/tarif_grundbedarf.py`, `modell/tragfaehigkeit.py`, `modell/justierung.py`, `modell/nachfrage.py`,
`modell/laender/rechne.py`, `modell/anreize.py`, `modell/laendervergleich.py`. Quellen wie v3.33 bis v3.36.*

### v3.38 — Deutscher Textentwurf zur Freigabe; Deutschland nach V2

**Art der Änderung: MINOR (Text und Darstellung); in der Rechnung bewegt sich nur die Reihe Deutschland (V2 statt V3a).** 10. Oktober 2026.

**Entscheidung der Initiative (10.10.2026):** „Wie vorgeschlagen“: Die Ersparnis am Dach senkt die Quote (30,2 %), sie erhöht nicht die
Dividende.

**Rechnung.** `gesamtrechnung.py`: Die Reihe Deutschland (`de_land`, `erw_de_*`, `punkt_bip_eur_de`, Sensitivität, Webseite) folgt jetzt
der Entscheidung E2 (V2: BIP je Kopf Deutschland gegen Klub, Faktor `f_de` 1,0875) statt dem Preisniveau (`r_de` 1,0086, V3a).
Bewegte Zahlen (Euro je Monat, Preise 2028): Deutschland je Einwohner 2028 539 → 581, Tiefpunkt 531 → 572 (2032), 2060 732 → 789;
je Erwachsenem 2028 588 → 634, 2060 798 → 860; ein Punkt des BIP 45 → 49 € (Deutschland). Klubwerte, Quote und Deckung unverändert.
Neu ausgegeben: `gemeinde_einw_de` 3.913 €, `gemeinde_kind_de` 13.729 € (Jahr, 2028, nominal), `verw_zehntel_eur` 7 €, `laender_unter_boden_v2`.
`laendervergleich.py`: Dividende der zehn Staaten nach V2 (übrige Länder weiter Boden, als Lücke gekennzeichnet).

**Text (Entwurf, `ENTWURF=1`):** Gesamtkonzept (15 Seiten) und Kurzfassung (2 Seiten) in `dokumente/entwurf/`, Webseite Deutsch in
`seite/entwurf/de.html` mit rotem Hinweis „Entwurf zur Freigabe“. Die veröffentlichte Fassung (7. Oktober 2026) bleibt unberührt.
Inhalt der Änderungen: Dividende und Gemeindeformel nach V2/E3 mit Ländertabellen; Boden als Kriterium im Klubschnitt, vier Länder
darunter offen genannt; Dach auf Kernaufgaben (Posten 3,75 → 2,10, Herleitung COFOG GF04); Label nach Fußabdruck, effektiv 16,9 %, regionale
Wirkung nicht belegt (−0,04 % des BIP), Salienz empirisch offen; Tarifstufen 1/1,5/2/3; Erbschaft 100.000 €; Vermögen 1,5 %; Deckung mit
Überschuss 0,24 innerhalb der Unsicherheit; Stabilität (Reserve 1,08); Ablösung der Sozialverwaltung außerhalb der Quote (Korrektur 59);
Länderstandard und Klubquote 81,55 % bei Regierungspfaden FR/ES/NL; Rechtsrahmen nach Entscheidung nicht bindend, Kollisionen benannt
(Art. 113, 110, 3 AEUV); Estland-Aussage zurückgezogen (Korrektur 58); Webseite: Verwaltungsvergleich mit Estland ersetzt.

**Geprüft:** Behauptung „über 95 % haben mehr“ gegen die engeren Stufen: Im Kernmodell (`modell/kern/modell-2828.py`, Stand A, Euro 2026,
Alleinstehende ohne Kinder, Dividendenstufe 50 %, nach Mehrwertsteuer-Mehrbelastung) bleibt der Nettovorteil für alle Bruttoeinkommen von
15.000 bis 150.000 € positiv (+6.362 bis +12.157 € im Jahr statt +6.548 bis +14.071 €). Die 95 % beruhen dort auf Risikogruppen
(Transferbezieher, sehr große Vermögen), nicht auf Erwerbseinkommen; die Aussage bleibt mit Kennzeichnung „Schätzung“ stehen. **Grenze:**
Stand A (Quote 27,91 %, Label 20 %), keine Mikrosimulation.

**Prüfung:** `modell/pruefe_konzept.py --entwurf` (neu, 54 Prüfungen, 0 Fehler), neue Stufe „Textentwurf gegen Rechnung“ in `alles.py`
(23 Stufen). Die Stufe „Gesamtkonzept gegen Rechnung“ bleibt bis zur Übernahme des Entwurfs bewusst rot (v3.37).

**Wodurch aufgefallen:** Auftrag der Initiative; V2-Reihe Deutschland beim Lesen des Entwurfs (Abschnitt 4 nannte noch das Preisniveau).

*Skripte: `dokumente/werkzeuge/gesamtkonzept-bau.js`, `kurzfassung-bau.js`, `seite/werkzeuge/seite_bau.py`, `modell/pruefe_konzept.py`,
`modell/gesamtrechnung.py`, `modell/laendervergleich.py`. Quellen wie v3.33 bis v3.37.*

### v3.39 — Freigabe: Fassung 10. Oktober 2026 übernommen, sechs Sprachfassungen

**Art der Änderung: MINOR (Veröffentlichung), keine Zahl der Rechnung bewegt.** 10. Oktober 2026.

**Freigabe der Initiative (10.10.2026)** mit Korrekturen an der Webseite: Hinweis unter den Kennzahlen nur „* Schätzung des Projekts.“
(„Beträge in Preisen von 2028“ gestrichen); Zwischentitel „Das heutige System:“ und „Das Konzept:“ dunkelblau wie der übrige Text (vorher
Rot bzw. Grün); Untertitel „Starke Gemeinden, starke Bürger, ein starkes europäisches Dach“; Text „… entscheidet selbst über Finanzen und
die Weitergabe an andere Verwaltungen“; Dreiecksgrafik neu gesetzt (Dreiecksfläche, gerade Pfeile mit Beschriftung entlang der Seiten,
Dividende als Grundlinie); „Du“ statt „Sie“ mit Untertitel „klar geregelte Abgaben“, dazu „Deine Gemeinde“ (Angleichung an das Du).
Nebenbefund: In der mobilen Grafik fehlten seit v3.15 die Pfeilspitzen (Marker lagen in der ausgeblendeten breiten Grafik); behoben.

**Übernahme:** Gesamtkonzept und Kurzfassung in `dokumente/` (Fassung 10. Oktober 2026, Quote 30,2 %, Obergrenze 32 %), Webseite in sechs
Sprachen in `seite/stand-b/`. Entwurfsordner entfernt (Inhalt in v3.38). Die geänderten Textschlüssel (17) sind für EN, FR, IT, ES, PL vom
KI-System übersetzt; **muttersprachlich zu prüfen** (B16), mindestens Französisch und Polnisch. Informelle Anrede in der Grafik:
Toi / Tu / Tú / Ty.

**Geprüft:** `python3 modell/alles.py`; `pruefe_konzept.py` 59 Prüfungen ohne Fehler (die bewusst rote Stufe aus v3.37 ist damit grün);
Grafik in allen sechs Sprachen bei 1.200 und 390 Pixel Breite angesehen. **Wodurch aufgefallen:** Durchsicht des Entwurfs durch die Initiative.

### v3.40 — Webseite: Ansprache vom Kleinen zum Großen

**Art der Änderung: PATCH (Aufbau der Webseite), keine Zahl bewegt.** 12. Oktober 2026.

**Wunsch der Initiative (12.10.2026):** Nach „Das Konzept:“ folgen zuerst die Regeln für den Einzelnen („Wenige Regeln, ein Prinzip“), dann
der Rechner; der Teil zu Gemeinde und Dach („Starke Gemeinden, starke Bürger, ein starkes europäisches Dach“ mit Dreiecksgrafik, Dividende,
drei Ebenen und Verteilung von 100 €) steht danach, vor „Ihre Gemeinde rechnet selbst“.

**Umsetzung:** `seite/werkzeuge/vorlage.html`, Abschnitte umgestellt: `#konzept` (Kicker und Bausteine), `#rechner`, `#ebenen` (neu benannt,
vorher Teil von `#konzept`), `#gemeinde`. Texte und Zahlen unverändert; alle sechs Sprachfassungen neu gebaut. Navigation „Konstruktion“
und Schaltfläche „Konzept ansehen“ führen weiter auf `#konzept`, jetzt auf die Bausteine.

**Geprüft:** `python3 modell/alles.py`; `pruefe_konzept.py` 59 ohne Fehler; Seite ganz angesehen (1.200 Pixel), keine Skriptfehler.
**Wodurch aufgefallen:** Wunsch der Initiative.

### v3.41 — Gesamtkonzept als Einführung (RTF), Quellenverzeichnis

**Art der Änderung: MINOR (Text), keine Zahl der Rechnung bewegt.** 12. Oktober 2026.

**Auftrag der Initiative (12.10.2026):** Gesamtkonzept wie die Webseite vom Kleinen zum Großen umbauen; die missverständlichen Begriffe
„Boden“ und „Klub“ ersetzen; die Kooperation im Möglichkeitsraum als Möglichkeit, nicht als Bedingung, nach dem Menschen an seinem Ort
beschreiben; RTF mit kurzem Inhaltsverzeichnis und vollständigem externem Quellenverzeichnis (Titel, Autor, Jahr, Link mit Abruftag);
Begriffe und Rechnungen am Anfang des Gedankengangs herleiten; keine Bezüge auf frühere Fassungen; Einführung statt Differenzierung.

**Umsetzung:** `dokumente/werkzeuge/gesamtkonzept_rtf.py` → `dokumente/TAX-2828-Gesamtkonzept.rtf` (17 Seiten, davon 5 Quellen).
Alle Zahlen aus `gesamtrechnung.json`, `tragfaehigkeit.json`, `tarif_grundbedarf.json`, `nachfrage.json`, `moeglichkeitsraum.csv`.
Aufbau: 1 Worum es geht; 2 Der einzelne Mensch an seinem Ort (Grundbedarf als Maß, Tarif, Kapital/Erbschaft/Vermögen, Label, CO₂,
keine Sozialbeiträge und Bestandsgarantie, Dividende, Rechenbeispiel); 3 Die Gemeinde (Aufgaben, Herleitung der Formel, Grundstücksabgabe,
Selbstentscheidung); 4 Das gemeinsame Dach (Einzug und Obergrenze, Aufgaben, Unternehmen am Ort der Kunden, Mehrheit); 5 Kooperation im
Möglichkeitsraum (Nutzen, gleiche Regeln und nationaler Ausgangspunkt, Altschulden, Möglichkeitsraum); 6 Rechnung (Abgabenquote abgeleitet,
Zeitpfad, Deckung und Stabilität, Gesamtlast); 7 Offen; 8 Zahlengrundlage; Quellenverzeichnis.
Begriffe: „Staatengemeinschaft“/„teilnehmende Staaten“ statt „Klub“; „gemeinsames Dach“ statt „Ebene A“; „Mindestniveau der Dividende“
statt „Boden“; „Grundstücksabgabe (Bodenwert)“ statt „Bodenwertabgabe“; „Abgabenquote“ und „BIP“ beim ersten Gebrauch erklärt.

**Quellenverzeichnis:** `daten/quellen_verzeichnis.json`, 154 Einträge in sechs Gruppen, von einem Rechercheagenten aus den Dateien des
Repositorys zusammengestellt (DOIs teils am 12.10.2026 aufgelöst). 80 Einträge ohne Link, 28 ohne Abruftag (vor allem Gesetze und
Länderquellen, deren Fundstelle das Repository nicht verzeichnet); Vermerke „Sekundärquelle“, „Original nicht eingesehen“, „Link nicht
geprüft“, „maschinell gelesen“ im Verzeichnis. Autorennamen der zitierten Werke sind auf ausdrücklichen Wunsch aufgenommen (die Regel
„keine Personennamen aus Quellen“ betrifft Texte, nicht Literaturangaben).

**Befunde des Agenten (offen):** Tabellenangabe OECD Taxing Wages uneinheitlich (Tabelle 3.1 gegen Tab. 1.2/1.4/1.7); QUELLEN.md nennt
365,9 statt 365,8 Mio für „Sechs genügen“; Abrufdatum der deutschen Schuldenquote 2024 widersprüchlich (quellen.csv gegen eingangswerte.csv);
Jahresangaben einzelner Literatur (Melguizo/González-Páramo, Gechert/Heimberger 2022, Benzarti u. a. 2020 als Zeitschriftenfassung);
Frankreich nimmt die Schuldenquote 2025 von INSEE statt Eurostat (Standard 1.3, im toml vermerkt).
**Widerspruch Rechner der Webseite:** Der Rechner besteuert nur den Bruttolohn; Deckungsrechnung und Gesamtkonzept behandeln die
Dividende der Erwachsenen als steuerpflichtig. Zu entscheiden und anzugleichen.

**Geprüft:** RTF in PDF gewandelt und vollständig gelesen; `python3 modell/alles.py`. **Wodurch aufgefallen:** Auftrag der Initiative.

### v3.42 — Sozialschutz und Übergang: zwei Vorschläge geprüft und zusammengeführt; Korrektur 60

**Art der Änderung: MINOR (neue Prüfrechnung), keine Zahl der Gesamtrechnung bewegt.** 16. Oktober 2026.

**Auftrag der Initiative (16.10.2026):** Die Vorschläge „Generationenbaustein“ und „Hütte · Route · Seil“ (Projektraum) auf Anwendbarkeit und Sinn
prüfen, die drei Stränge zusammenführen, Recherchen ergänzen, eine Modellrechnung vorbereiten; Bedeutung für die Finanzierungsregel 28:28.

**Daten (Rechercheagent, WebFetch 16.10.2026, maschinell aus dem Abruf gelesen, an der Quelle zu prüfen):** Eurostat `gov_10a_exp` 2024, COFOG GF07,
GF10 und GF1001–GF1009 je Land (SDMX-TSV; Stichproben per JSON bestätigt); `nasa_10_pens1` (Tabelle 29, erworbene Rentenansprüche, 2021);
`demo_pjanind` (Anteil 65+, 2024); Ageing Report 2024, amtliche Länderberichte (2022, 2030–2070; 2028 nicht veröffentlicht). Ablage
`daten/aggregate/sozialschutz_2024.json`. Offen: Hauptbericht-Tabelle je Land nicht lesbar; Abweichung AT zwischen Länderbericht und Tabelle 5.
**Faktencheck** der Sekundärangaben (zweiter Agent): `projekt/faktencheck_vorschlaege_2026-10-16.json`; 8 bestätigt, 4 abweichend (Frankreich,
RAND-Quellen, Nichtinanspruchnahme, Kostenkonzentration nur bifg), Sozialbudget 2024 nur Sekundärquelle.

**Rechnung `modell/sozialschutz.py` (Schätzung, Setzungen in `sozialschutz.toml`):** Sozialschutz 2024 20,07 % BIP (zehn Staaten); Zuordnung nach dem
Hütte-Vorschlag: Hütte 13,26 · Route 4,10 · Seil 2,72 gegen Dividende 11,86. Zugesagtes Z (Ansprüche über der Dividende, vor dem Stichtag 2028
erworben, Kohortenschema, skaliert auf Tabelle 29): **2028 8,86 %, 2040 8,31 %, 2050 6,16 %, 2060 3,46 %, unter 0,1 ab 2074**; je Land 2028
von 0 (DK) bis 14,0 % (AT). Gegenprobe Barwert gegen Tabelle 29: DE 329/320, FR 413/397, AT 438/450 %. Dauerzustand nach Auslauf: 19,33 % gegen
20,07 % heute. Z über Steuern: Quote 2028 39,7 %, Lücke 9,3; über Schuld: +223 Punkte Schuldenquote bis 2069. Mit Z, Pflicht-Route, Seil und
Härtefall (Mitte 0,65) Gesamtlast 2028 rund 54 % gegen 40,76 % heute.

**Befunde:** (1) Bestandsgarantie und Härtefallfonds sind in keinem Rechenskript finanziert. (2) Die Hütte-Zuordnung für Ältere (7,0 % BIP)
übersteigt die Dividende der über 65-Jährigen (2,7 %) deutlich. (3) H2 (50 % Anrechnung) widerspricht der Aussage „mindestens 72 Cent je Euro“.
(4) Gesundheit über Steuern (65 %) hebt die Quote um 5,0 Punkte und ist mit 28:28 nicht zu decken. (5) Projektsteuerung „Geltende Fassung“
stand auf dem 7. Oktober (nachgeführt). (6) Der Hütte-Vorschlag nimmt Korrektur 59 als nächste Nummer an; richtig ist 60.

**Korrektur 60** (Abschnitt 4): Gesamtlast-Aussage ohne die Altansprüche.

**Ergebnis für 28:28:** Die Regel bleibt als Regel der Steuern haltbar, wenn Z über einen eigenen, sinkenden Übergangsbeitrag beim Ausgangsstaat
und Gesundheit und Seil über Prämien laufen; „keine Sozialabgaben“ gilt erst im Dauerzustand. Zusammenführung und Antwortbogen S1–S13:
`projekt/Zusammenfuehrung-Sozialschutz-2026-10-16.md`.

**Geprüft:** `python3 modell/alles.py` (neue Stufe „Sozialschutz und Übergang (Vorbereitung)“). **Wodurch aufgefallen:** Vorschläge zweier Agenten.

*Quellen: Eurostat gov_10a_exp, nasa_10_pens1, demo_pjanind (16.10.2026); European Commission/EPC, 2024 Ageing Report, Länderberichte und
Institutional Paper 279; Faktencheck-Datei (BMAS, DRV/WD 6, Destatis PM 455/2025, Pensionsmyndigheten, Folketing, Légifrance-Sekundärquellen,
bifg, Lohr u. a. 1986, Brook u. a. 1983, IZA DP 18420, JAMA Netw Open 2021, DIW, Diamond 2016, BVerfGE 53, 257).*

### v3.43 — Systemvarianten 25:25 (Viertellösung) und 33:33 (Drittellösung)

**Art der Änderung: MINOR (Prüfrechnung), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Auftrag der Initiative (17.10.2026, sinngemäß):** Das System soll klar, einfach und kommunizierbar bleiben, möglichst ohne Sonderfälle. Zwei
Wege prüfen, die die Finanzierung erleichtern: (1) 25:25 mit einer Dividende, die nur 25 % des höheren Existenzminimums einschließlich
Sozialabdeckung deckt, alle Steuerwerte auf 25 %; (2) 33:33, die Sozialabgaben eingeschlossen, Dividende wie gehabt, Einkommen, Kapital und
Mehrwertsteuer bis 33 %.

**Rechnung `modell/systemvarianten.py`** (Mindestquote mit den Funktionen der Gesamtrechnung; Deckung der Positionen auf deutscher Basis mit
skalierten Sätzen; Z mit der Dividende der Variante neu, `sozialschutz.py` dafür in Funktionen zerlegt, Ergebnis unverändert). Setzungen in
`systemvarianten.toml`; Sozialabdeckung = Gesundheit + Seil je Kopf (476 € im Monat, DE).

**Bewegte Zahlen (Prüfrechnung):** 25:25: Mindestniveau 387 €, Dividende DE 479 € (Erw., Monat, Preise 2028), Quote 27,3 (+ Härtefall 27,95),
Deckung 28,30, Saldo +0,35; Z 2028 9,54. 33:33: Quote mit Gesundheit, Seil und Z 2028 50,18, Deckung 33,96, Saldo −16,22, Dauerzustand −7,36;
nur mit Seil +0,39; Gesundheit und Seil dauerhaft aus Steuern erst bei Spitzensätzen um 45 %. 28:28 zum Vergleich mit Härtefall: −0,41.

**Hinweis:** Der Härtefall (0,65, Annahme) fehlt bisher in der Gesamtrechnung; mit ihm hat auch 28:28 einen Fehlbetrag von 0,41 (Befund v3.42).

**Geprüft:** `python3 modell/alles.py` (neue Stufe). **Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen wie v3.42 (Eurostat gov_10a_exp, nasa_10_pens1, demo_pjanind, Ageing Report 2024); Kernmodell für die Einkommensteuer.*

### v3.44 — Drittellösung mit Dividende von einem Drittel; Altlasten außerhalb

**Art der Änderung: MINOR (Prüfrechnung), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Frage und Vorgabe der Initiative (17.10.2026):** Wurde 33:33 mit einer Dividende von einem Drittel des Existenzminimums gerechnet? (Nein: in v3.43
„wie gehabt“, Mindestniveau ½ Grundbedarf.) Altlasten aus Staatsschulden und Rentenansprüchen werden außerhalb finanziert; die Unterscheidung zwischen
echten Anlagen und Versprechen zulasten späterer Generationen ist diskutabel und muss nicht voll einkalkuliert sein. Lösung und Erzählung suchen.

**Rechnung `modell/systemvarianten.py`, erweitert:** Zinsdienst wahlweise außerhalb der Quote (Mindestquote mit Zins null; Zinsen aus dem Pfad der
Gesamtrechnung in den Altlastenbeitrag); Anteil der Gesundheit in den Steuern als Parameter; Prämien je Einwohner und Dividende nach Prämien;
Altlastenbeitrag mit Z voll und halb. Neue Systeme 28A, 25A, 33A, 33G, 33L in `systemvarianten.toml`.

**Bewegte Zahlen (Prüfrechnung, 2028):** 28:28 Altlasten außerhalb: Quote 28,5, Saldo +1,29, Dividende nach Prämien 67 € je Einwohner. 33:33 mit
Dividende ⅓ von Grundbedarf + Sozialabdeckung, Gesundheit und Seil in den Steuern: Saldo −5,26; mit ⅓ des Grundbedarfs: −2,06. **Lösung 33L:** Seil und
30 % der Gesundheit in den Steuern: Steuerbedarf 33,80, Deckung 33,96, Saldo +0,16; Dividende DE 618 € (Erw.); Gesundheitsprämie 245 € je Einwohner;
Altlastenbeitrag 10,73 (Z halb 6,27); Gesamtlast Dauerzustand 40,01. Ohne Prämie gleich teuer bei Dividende ¼ des Grundbedarfs (DE 351 €, Saldo −0,26).

**Grenzen:** wie v3.43; Hochkostenpool 30 % Setzung; Überschuss 0,16 klein. **Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Frage der Initiative.

*Quellen wie v3.42/v3.43; Kostenkonzentration: Wende/Schmitt, bifg 2021 (Faktencheck 16.10.2026).*

### v3.45 — Mehrwertsteuer-Sonderstufe, prämienfreie Drittellösung, Altlastenfonds mit Streckung

**Art der Änderung: MINOR (Prüfrechnungen), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Vorgaben der Initiative (17.10.2026):** Altlastenbeitrag nicht einseitig und nicht länderbezogen auf die Löhne; maximale Streckung, Tilgung bei
Einnahmenspitzen; prämienfreie Lösung prüfen; 33 % Mehrwertsteuer nur für die ganz schädlichen Produkte, kein Regelfall.

**Rechnungen:** `systemvarianten.py` erweitert (Sonderstufe je Produktgruppe; Lösen des Mindestniveaus auf einen Ziel-Saldo), neue Systeme 33M, 33N, 33P.
Neu `modell/altlasten.py` (+ `.toml`): Fonds mit Schuld 2028 (81,3 %) und Altrenten Z; gleichbleibender Beitrag; d(t+1) = d(t)(1+i)/(1+g) + Z − c;
Varianten Zieljahr/Zielquote, Zins 2,5/3,0, Z voll/halb, Deckel 100/120 %; Verteilung bei gemeinsamem Fonds je Staat.

**Bewegte Zahlen (Prüfrechnung):** Label 5–28 mit 33 nur für Alkohol/Tabak: effektiv 17,06 %, Deckung 32,85 (statt 33,96). 33M (Dividende ⅓, 618 €):
Saldo −0,95. **33N** (mit Prämie, ausgeglichen): Mindestniveau 30 % von Grundbedarf + Sozialabdeckung, Dividende DE 560 €, nach Prämien 227 € je Einwohner,
Saldo +0,15. **33P** (prämienfrei): Mindestniveau 18 % des Grundbedarfs, Dividende DE 265 €, nach Prämien 224 €, Saldo +0,23, Z 2028 10,46.
Fonds bis 2125 auf 60 %: Beitrag 1,06 bis 2,85 % BIP (3,2 bis 8,7 % Zuschlag auf alle Steuern), Schuldenspitze 149 bis 249 % um 2060–2065;
Deckel 120 % mit Z halb: 2,08 (33N) bzw. 2,75 (33P). Gemeinsamer Fonds: Altlast 2028 gegen Schnitt 12,2 %: AT +5,2 … DK −11,5 Punkte.

**Grenzen:** wie v3.43/v3.44; keine Rückwirkung der Schuldenquote auf den Zins; Tilgungsregel nicht beziffert. **Geprüft:** `python3 modell/alles.py`
(neue Stufe). **Wodurch aufgefallen:** Vorgaben der Initiative.

*Quellen wie v3.42–v3.44.*

### v3.46 — Beschlüsse: prämienfreies Drittel, Sonderstufe für Schädliches, Altlastenfonds bis 2098

**Art der Änderung: MINOR (Prüfrechnung der Beschlüsse), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Beschlüsse der Initiative (17.10.2026):** prämienfrei; 33 % Mehrwertsteuer für umwelt- und gesundheitsschädliche Produkte; Altrenten: anlagegedeckte voll,
der Rest zur Hälfte, die andere Hälfte der Verhandlung der Generationen unterworfen; Streckung höchstens 70 Jahre; gemeinsamer Fonds mit abschmelzender
Verrechnung je Staat; Quelle des Beitrags nach Empfehlung.

**Umsetzung:** System 33F in `systemvarianten.toml` (Sonderstufe 33 % für Alkohol/Tabak und Kraftstoffe, 32 % Mischsatz Fahrzeuge, Annahme 80 % Verbrenner;
Mindestniveau gelöst auf Saldo +0,2). `altlasten.py`/`.toml`: Abschnitt „beschluss“ (Z 50 %, da staatliche Systeme laut Tabelle 29 praktisch ungedeckt;
Zins 2,5 %; Tilgung bis 2098 auf 0 %); Verrechnung: Beitrag je Staat = c × (Anteil nach eigener Altlast 2028, linear in 30 Jahren auf 1).

**Bewegte Zahlen (Prüfrechnung):** 33F: Label effektiv 17,55 %, Deckung 33,04, Steuerbedarf 32,92, Dividende DE 281 € (Erw., Monat, Preise 2028),
Mindestniveau 201 €, Gesamtlast Dauerzustand 33,7 %. Fonds: Beitrag 3,15 % BIP (Zuschlag 9,6 % auf alle Steuern, 142 € je Einwohner), Schuldenspitze
109,4 % (2052), 2098 0 %; Zins 3 %: 3,53 %; Z 75 %: 4,24 %; Z 100 %: 5,33 %. Zuschlag 2028 je Staat von 0,9 (DK) bis 13,2 % (AT), ab 2058 einheitlich 9,6 %.

**Empfehlung:** Zuschlag auf alle Steuern statt Abzug von der Dividende (Tragfähigkeit, Leistungsfähigkeit, Breite, Sichtbarkeit).

**Offen gekennzeichnet:** Halbe Einrechnung der Altrenten bedeutet ohne weitere Verhandlung eine starke Kürzung bestehender Renten über der Dividende
(Beispiel 1.200 € → 741 €, Untergrenze Grundbedarf); Vertrauens- und Eigentumsschutz juristisch zu prüfen. Härtefall wird mit kleiner Dividende größer als
die Annahme 0,65 % BIP. **Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Beschlüsse der Initiative.

*Quellen wie v3.42–v3.45; Tabelle 29 (Eurostat nasa_10_pens1, 2021) für die Deckung der staatlichen Rentensysteme.*

### v3.47 — Drittel-System: Trends bis 2060, Haushalte gegen heute, Webseitenentwurf

**Art der Änderung: MINOR (Prüfrechnungen und Entwurf), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Auftrag der Initiative:** keine Halbierung der Altrenten, Altlasten Sache der Staaten; Allgemeingültigkeit des Bauplans; mit Prognosen belegbarer Trends rechnen;
Erzählung finden; Webseite zuerst auf Deutsch entwerfen.

**Neu:** `modell/projektion33.py` (+ `.toml`): Zeitpfad 33F 2028–2060 auf dem Grundpfad der Gesamtrechnung (Quote 21,8, Zinsen außerhalb), mit Trends für
Verbrenneranteil, Kraftstoffe (Projektionsbericht 2026, Verkehrsemissionen als Näherung), CO₂, Energie- und Tabaksteuer, Gesundheit und Pflege (Ageing Report 2024);
Variante Bürgerfonds. `modell/haushalte33.py` (+ `.toml`): Haushalte heute (Kernmodell, Recht 2026; 2035 mit IGES-Beitragssätzen) gegen 33F, Varianten Weitergabe
der Arbeitgeberbeiträge, Altlastenzuschlag, eigene Vorsorge; Rentnerfall; Raster für den Rechner. `seite/werkzeuge/entwurf33_bau.py`: deutscher Entwurf
`seite/entwurf/konzept33/de.html`, Quellen `seite/entwurf/QUELLEN-33.md`. Bericht `projekt/Drittel-Erzaehlung-Trends-2026-10-17.md`.

**Bewegte Zahlen (Prüfrechnung, Kaufkraft 2026):** Lenkungsanteil der Dividende 2028 59 % (3,09 % BIP). Dividende je Erwachsenem 270 € (2028), 175 € (2035),
98 € (2045), 48 € (2060); Mindestniveau 193 € ab 2034 unterschritten. Bürgerfonds (Hälfte angelegt): 191 € (2028), 69–79 € (2060). Haushalt alleinstehend
42.000 €: +588 €/Monat (Weitergabe, Vorsorge wie heute), +369 € mit Zuschlag 16,2 %, +96 € ohne Weitergabe; 2035 +567 €. Rentner 1.200 €: +114 €.
Grenzbelastung bei 55.000 €: 56 % → 34 %. Anteil mit mehr Geld: 100 % mit Weitergabe, 82 % ohne (67 % mit Zuschlag).

**Offen gekennzeichnet:** Die Dividende des Drittel-Systems ist unter den Trends nicht dauerhaft (Entscheidung F2). Die Weitergabe der Arbeitgeberbeiträge
entscheidet über das Ergebnis (Annahme). Kinderdividende (135 €) unter dem Kindergeld. Konsumquote des Kernmodells für die Haushaltsrechnung linear geglättet
(Sprünge der Grenzbelastung an den Stufengrenzen). Energiesteueranteil Kraftstoffe 85 % und Tabak/Alkoholsteuer 17,8 Mrd € Annahmen.
**Geprüft:** `python3 modell/alles.py` (32 Stufen); Seite im Browser (Desktop und 390 px, keine Skriptfehler). **Wodurch aufgefallen:** Auftrag der Initiative;
der Rückgang der Dividende zeigte sich erst mit den Trendpfaden.

*Quellen: Umweltbundesamt (Umweltbezogene Steuern 2024; Projektionsbericht 2026, Tabelle 2); Europäische Kommission, 2024 Ageing Report (IP 279, Tabellen 4 und 5,
maschinell gelesen); VO (EU) 2019/631 i. d. F. 2023/851, Ratsdokument ST 10065/1/26; ACEA (27.1.2026); Rat der EU (9.10.2026, ETS2); IGES für DAK (über Deutsches
Ärzteblatt 25.6.2024, eine Studie); Destatis (Zigaretten 2024). Abruf 16./17.10.2026.*

### v3.48 — Beschlüsse: Weitergabe ≥ 80 %, Rentenkürzung um eingesparte Beiträge, Mehrwertsteuer 25 %; Einwanderung

**Art der Änderung: MINOR (Prüfrechnungen und Entwurf), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Beschlüsse der Initiative (17.10.2026):** (1) Betriebe müssen mindestens 80 % der gesparten Arbeitgeberbeiträge in den Lohn geben. (2) Renten werden um die
eingesparten Sozialbeiträge gekürzt. (3) Die Mehrwertsteuerstufen 22 und 28 % werden zu 25 % zusammengefasst. **Frage:** Was bedeuten Einwanderungsziele?

**Umsetzung:** System 33R in `systemvarianten.toml` (Label 5/11/17/25, Sonderstufe 33 %, Fahrzeug-Mischsatz 31 %, Saldo +0,2). `sozialschutz.py`: Parameter
`KUERZUNG` (Anspruch × (1 − Satz)); `altlasten.toml`: Kürzung 12,35 % (Kranken- und Pflegebeitrag der Rentner in Deutschland 2026; **Annahme für alle zehn
Staaten**), Beschluss auf 33R mit vollen Altrenten (v3.47). `haushalte33.toml`: Weitergabe 0,8 (Pflicht) und 1,0; Zuschlag 13,7 %; Rente gekürzt.
`projektion33.toml`: System 33R. Neu `modell/einwanderung33.py` (+ `.toml`): zusätzliche Nettoeinwanderung 0,2 und 0,4 % der Bevölkerung je Jahr,
Erwerbsalter, Erwerbstätigkeit und Produktivität als Annahmen (kontrolliert / schwierige Integration). Webseitenentwurf auf 33R umgestellt.

**Bewegte Zahlen (Prüfrechnung, Kaufkraft 2026):** Label effektiv 18,82 % (33F: 17,55); Deckung 33,53; Dividende 2028 DE 308 € (Preise 2028) = 296 €,
2035 202 €, 2060 83 €; Mindestniveau 217 € ab 2034 unterschritten. Altrenten Z 2028 10,28 → 8,84 % BIP mit Kürzung. Fonds (Z voll, gekürzt): 4,59 % BIP =
Zuschlag 13,7 %, Spitze 153,6 % (2056). Haushalt alleinstehend 42.000 €, Weitergabe 80 %, Vorsorge wie heute: +474 € (mit Zuschlag +295 €); Paar mit einem
Einkommen, zwei Kinder, mit Zuschlag ab rund 55.000 € im Minus. Rentner: −18 € (900 €) bis −70 € (2.200 €), mit Zuschlag −35 bis −123 €. Grenzbelastung bei
55.000 €: 56,4 → 36,3 %. Einwanderung +0,4 %/Jahr (kontrolliert): Altenquotient 2060 0,52 → 0,42, BIP +20 %, je Kopf +4 %, Fondsbeitrag 4,59 → 3,95 % BIP,
Dividende 2060 83 → 148 €; schwierige Integration: BIP je Kopf −1,6 %, Dividende 2060 109 €.

**Offen gekennzeichnet:** Rentner verlieren leicht (Kürzung und höhere Mehrwertsteuer, volle Besteuerung). Kürzungssatz je Staat verschieden. Durchsetzung der
80-%-Pflicht offen. Demografische Ausgangswerte der Einwanderungsrechnung aus einer Aussage des Rats (ST 9160/24: heute drei, 2070 weniger als zwei Personen
im Erwerbsalter je Person über 65) interpoliert, keine Bevölkerungsprojektion gerechnet; keine Geburten, keine Rentner unter den Eingewanderten bis 2060.
**Geprüft:** `python3 modell/alles.py`; Seite im Browser. **Wodurch aufgefallen:** Beschlüsse und Frage der Initiative.

*Quellen: wie v3.47; Rat der EU ST 9160/24 (Altenquotient, Aussage); CaixaBank Research (Ageing Report 2024, Spanien: +33 % Zuwanderung senkt Rentenausgaben
um 1,4 Punkte; Sekundärquelle); Eurostat Erwerbstätigenquote 2024 (75,8 %, nicht eigens abgerufen).*

### v3.49 — Progression an den Stufen (Korrektur 61), Beschäftigung und Automatisierung, Leistungspaket und Namen

**Art der Änderung: MINOR (Korrektur einer Prüfrechnung, Szenarien, Entwurf), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Anlass:** Frage der Initiative, warum Automatisierung und billigere Arbeit keine stärkeren Gewinne bringen; Bitte, die Modellrechnung zu prüfen; Vorschlag,
das Leistungspaket gesamthaft sichtbar zu machen und Namen zu prüfen (Goldenes Drittel, Goldenes Netz, Zukunftsschatz, Transformationsdividende/TrafoDi).

**Prüfung:** (1) Beschäftigung, Automatisierung und Verschiebung zum Kapital waren in v3.47/v3.48 nicht enthalten (statische Anteile, Wachstum je Kopf 0,98 %).
(2) **Fehler (Korrektur 61):** `projektion33.py` hielt den Anteil der Einkommensteuer am BIP fest, obwohl die Stufen am Grundbedarf hängen, der nur zu 30 % den Löhnen
folgt (Mischindex § 28a SGB XII, an der Quelle zu prüfen). Mit realem Wachstum steigt der Anteil (Kernmodell: Einkommen × 1,366 bis 2060 → Anteil × 1,17 bei voller
Preisbindung). (3) Der Rückgang der Konsumquote mit dem Einkommen (Kernmodell) wird nicht auf die Zeit übertragen (Sparquoten ohne Trend; Annahme).

**Neu:** `projektion33.py`: Funktion `progression`, Parameter `stufen_lohnanteil = 0,3`, Mindestniveau mit 30 % Lohnbindung, Leistungspaket (Netz in € je Kopf).
`modell/dynamik33.py` (+ `.toml`): Szenarien Beschäftigung +2,8/+4,6 % (Nachfrage −0,25 auf −3,5 % Arbeitskosten; Angebot Elastizität 0,05/0,10), KI +0,07/0,3/0,6 Pp
Produktivität (Acemoglu 2024; OECD 2024), Verschiebung zum Kapital 3 Punkte (effektive Belastung 21 % Arbeit / 32 % Kapital im Drittel-System, Annahmen).
Webseitenentwurf: Abschnitt „Was Du vom System bekommst“, Namen als Vorschlag, Automatisierung und Arbeit im Zeitpfad.

**Bewegte Zahlen (Prüfrechnung, Kaufkraft 2026):** Progression 2060 +1,24 Punkte BIP. Dividende 296 € (2028), 217 € (2035), 170 € (2045), 170 € (2060) statt 83 €;
Mindestniveau ab 2035 knapp unterschritten. Bürgerfonds (Hälfte): 2060 191–201 €. Szenarien 2060: KI 176–233 €, Beschäftigung +4,6 %: 183 €, alles zusammen
(KI 0,3/0,6, Verschiebung 3 Punkte): 242–273 €. Heutiges System bei Verschiebung um 3 Punkte: −0,64 Punkte BIP. Leistungspaket: Netz 524 € je Einwohner und Monat
(2028) → 770 € (2060); mit Dividende 820 → 940 €.

**Offen gekennzeichnet:** Wachstum wirkt vor allem über Löhne; die Dividende ist ein kleiner Rest des BIP. Die Progression ist eine Wahl (Stufen an Löhnen gebunden: kein
Zuwachs). Beschäftigungs- und KI-Wirkungen unsicher; KI-Annahmen können sich mit den Produktivitätsannahmen des Ageing Report überschneiden.
**Geprüft:** `python3 modell/alles.py`; Seite im Browser. **Wodurch aufgefallen:** Nachfrage der Initiative zur Automatisierung.

*Quellen: Acemoglu (2024), NBER WP 32487; Filippucci, Gal, Schief (OECD AI Papers 29, VoxEU 8.12.2024); Keane (2011); Chetty u. a. (2011); Lichter, Peichl, Siegloch
(2015, Meta-Studie Arbeitsnachfrage, nicht am Abruftag geprüft); OECD Taxing Wages 2025.*

### v3.50 — Das starke Netz als Grundversorgung; Finanzierung und Begriffe

**Art der Änderung: MINOR (Prüfrechnung, Entwurf), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Vorgabe der Initiative:** Kranken-, Pflege- und Rentenversicherung bieten nur eine brauchbare Grundversorgung ohne Extras, stets Raum und Anreiz für eigenes
Engagement; Name „Das starke Netz“; Finanzierung darstellen und Begriffe zuordnen.

**Befund vorab:** In v3.46–v3.49 waren Teile des Netzes nicht finanziert: Absicherung im Alter über der Dividende für Menschen ohne Altansprüche (Härtefall 0,65 %
als Annahme reicht nicht), Pflege außerhalb von GF07, Invalidität über dem Seil-Anteil. Das „Seil“ (2,72 %) finanzierte dagegen Lohnersatz (Extras im Sinne der Vorgabe).

**Neu:** `modell/netz33.py` (+ `.toml`): Netz als Grundversorgung: Gesundheit GF07 mit Kürzung des Katalogs 0/5/10 % (Annahme), Pflege Teilkasko 1,7 % BIP (Ageing Report
2024), davon 50 % schon in GF07 (Annahme), Grundbedarf bei Invalidität (2,2 % der Bevölkerung) und Arbeitslosigkeit (2,9 %), Waisen 0,05, Härtefall 0,65; Grundrente
ab 67 in drei Varianten: Volksrente für alle (Niederlande), Volksrente 2/3, Mindestrente mit Pflichtvorsorge (Faktor 0,125, Annahme). Dividende als Rest.
Webseitenentwurf: „Das starke Netz“, „Deine eigene Route“, Paket mit Vorschlagswerten.

**Bewegte Zahlen (Prüfrechnung, Kaufkraft 2026, Katalog −5 %):** Netz 2028 9,62 % BIP (bisher finanziert 11,12). Dividende 2028 373 € (bisher 296 €). Volksrente:
2060 148 €, Dauerzustand −51 € (nicht tragfähig; Netz 15,1 %). Zwei Drittel: Dauerzustand 95 €. Mindestrente mit Pflichtvorsorge: 2060 264 €, Dauerzustand 248 €
(Netz 10,9 %). Netz je Einwohner 454 € (2028) → 684 € (2060).

**Offen gekennzeichnet:** Kürzung des Leistungskatalogs, Mengen (Erwerbsminderung, Arbeitslose) und Faktor der Mindestrente sind Annahmen ohne Mikrodaten.
Mindestrente mit Anrechnung der eigenen Rente zur Hälfte wirkt als Grenzbelastung von 50 % auf kleine eigene Renten. Pflichtvorsorge ist eine Pflicht auf den Lohn
(Eigentum, kein Beitrag) und mit „0 € Sozialbeiträge“ zu erklären. Lohnersatz bei Arbeitslosigkeit entfällt als Pflichtleistung. Rechner und Zeitpfad des Entwurfs
noch ohne die Grundversorgung. **Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Vorgabe der Initiative; Prüfung, welche Leistungen das Netz trägt.

*Quellen: Ageing Report 2024 (Langzeitpflege EU27 1,7 % BIP, maschinell gelesen); Sozialschutz COFOG GF10 (sozialschutz_2024.json); Vorbilder AOW Niederlande,
Superannuation Australien, Arbeitslosenkassen Dänemark (allgemein bekannt, nicht eigens geprüft).*

### v3.51 — Beschluss: Netz als Grundversorgung mit Mindestrente und Pflichtvorsorge 10 %; fehlende Werte recherchiert; Konzept als Word-Datei

**Art der Änderung: MINOR (Prüfrechnung, Entwurf, Dokument), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Beschluss der Initiative:** Allen Empfehlungen aus v3.47–v3.50 wird gefolgt: Namen (Goldenes Drittel, starkes Netz, Transformationsdividende, eigene Route,
Zukunftsschatz), Grundversorgung ohne Extras, Mindestrente mit Pflichtvorsorge, Katalog −5 %. Fehlende Werte recherchieren, rechnen, Konzept als Word-Datei.

**Recherchiert:** 1,8 Mio. Erwerbsminderungsrenten Ende 2024 (DRV über sozialpolitik-aktuell.de; Anteil 2,15 % statt 2,2 % angenommen); Arbeitslosenquote Euroraum
6,2 % (Eurostat, Dezember 2025; Anteil 3,0 %); GKV-Leistungsausgaben 2024 311,7 Mrd € mit Fahrkosten 9,6, Reha 4,7, Zahnersatz 4,2, Krankengeld 20,5 Mrd € (BMG;
Größenordnung für den schlankeren Katalog; Krankengeld ist Geldleistung und liegt nicht in GF07); Grundsicherung im Alter 739.000 Personen Ende 2024 (Destatis über
Deutsches Ärzteblatt). **Nicht gefunden mit vertretbarem Aufwand:** Verteilung der künftigen eigenen Renten (Mikrodaten); Anteil der Pflege in GF07.

**Änderung der Rechnung:** `netz33.py`: Faktor der Mindestrente nicht mehr gesetzt (0,125), sondern aus der Verteilung VERT des Kernmodells berechnet (Pflichtvorsorge
10 %, 40 Sparjahre, 2,5 % real, Lohnwachstum 1 %, Bezugsdauer 20 Jahre, eigene Rente zur Hälfte angerechnet, 10 % mit langen Lücken; Annahmen) → Faktor 0,37–0,42
statt 0,125 (die frühere Setzung war zu günstig). Jahresreihe des Beschlusses (`beschluss`) für Haushalte, Rechner und Zeitpfad. `haushalte33.py`: Dividende nach
Beschluss, Pflichtvorsorge 10 % (Vergleich 18,6 %). Webseitenentwurf auf den Beschluss umgestellt. Neu `dokumente/werkzeuge/konzept33-bau.js` →
`dokumente/entwurf/TAX-Drittel-Konzept.docx` (+ PDF), alle Zahlen aus den Ergebnisdateien.

**Bewegte Zahlen (Prüfrechnung, Kaufkraft 2026):** Netz 9,63 % BIP (2028), 11,05 (2060), 11,91 (Dauerzustand). Dividende 373 € (2028), 294 € (2035), 246 € (2045),
234 € (2060), 174 € (Dauerzustand; mit Faktor 0,125 waren es 247 €). Pflicht 12 %: Dauerzustand 193 €. Haushalt alleinstehend 42.000 €, Weitergabe 80 %, Pflichtvorsorge
10 %: +826 € im Monat, mit Altlastenzuschlag 13,7 % +642 €; Paar mit einem Einkommen und zwei Kindern +540 € (mit Zuschlag).

**Offen gekennzeichnet:** Das Mehr der Haushalte beruht auch auf der Streckung der Altlasten im Fonds (Schuldenspitze 154 %); Rentner leicht im Minus; Kinderdividende
(187 € 2028) unter dem Kindergeld; Einwanderungs- und Automatisierungsrechnung noch mit der Dividende ohne Netz-Beschluss (Differenzen gültig, Niveaus nicht).
Inhaltsverzeichnis der Word-Datei wird beim Öffnen in Word aktualisiert (in der PDF-Fassung leer). **Geprüft:** `python3 modell/alles.py`; Dokument als PDF gerendert
und gesichtet. **Wodurch aufgefallen:** Beschluss der Initiative; Nachrechnung des Faktors der Mindestrente.

*Quellen: BMG, Finanzentwicklung der GKV 1.–4. Quartal 2024; DRV über sozialpolitik-aktuell.de (Abb. VIII.22); Eurostat Euro-Indikatoren (Arbeitslosigkeit); Destatis über
Deutsches Ärzteblatt (28.3.2025); weitere wie v3.47–v3.50.*

### v3.52 — Das Drittel-System im Möglichkeitsraum (30 Staaten)

**Art der Änderung: MINOR (Prüfrechnung, Dokument), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Auftrag:** Rechnung auch für den Möglichkeitsraum.

**Daten (neu abgerufen, Eurostat SDMX-TSV über Web-Abruf, 17.10.2026):** gov_10a_exp (GF07, GF10, GF1001, GF1002, GF1003, GF1005; 2023, S13), demo_pjanind
(Anteil 65+, 2024), une_rt_a (Arbeitslosenquote 2024), nama_10_gdp (BIP 2024), gov_10a_taxag (Steuern und Sozialbeiträge 2024), prc_ppp_ind (BIP je Kopf in KKS 2024),
gov_10dd_edpt1 (Schuldenquote 2024, EU27). Norwegen, Island, Schweiz: Schuldenquote **Annahme** (44 / 61 / 37 %, Größenordnung IMF, nicht geprüft). Abgelegt als
Aggregat `daten/aggregate/moeglichkeitsraum_2024.json`. Vereinigtes Königreich und Kanada nicht gerechnet (keine harmonisierten Daten).

**Neu:** `modell/moeglichkeitsraum33.py` (+ `.toml`): je Staat Netz aus Landesdaten, Grundbedarf nach Preisniveau, Dividende als Rest, eigener Altlastenfonds
(Schuld 2024 + Altrenten über der Dividende, gekürzt um 12,35 %, Tilgung bis 2098). Kernannahme: gleicher BIP-Anteil des Aufkommens wie auf deutscher Basis.
Konzept (Word) um Abschnitt 6.4 ergänzt.

**Bewegte Zahlen (Prüfrechnung):** 30 Staaten, 465,6 Mio. Menschen, BIP 19.515 Mrd € (2024). Abgabenquote heute im Mittel 39,8 %. Netz 2028 im Mittel 9,1 % BIP.
Dividende je Erwachsenem in deutscher Kaufkraft: 2028 im Mittel 357 €, Dauerzustand 205 € (Spanne Dauer: Frankreich 71 €, Tschechien 91 € bis Norwegen 442 €,
Luxemburg 1.001 €). Altlasten: Zuschlag im Mittel 12,1 % (Irland 2,2 %, Niederlande 4,9 % bis Italien 18,3 %, Frankreich 17,5 %, Griechenland 17,4 %).
Last neu 2028 (Drittel + eigener Fonds) 34,2 bis 39,7 %; höher als heute in Irland, Schweiz, Rumänien, Bulgarien, Malta.

**Offen gekennzeichnet:** Aufkommen je Staat nicht nach eigener Steuerbasis gerechnet; Irland (BIP überzeichnet); Schweiz (Gesundheit privat, Annahme 7 %);
nordische Staaten (Pflegedienste in GF1002, Altlast überzeichnet); Altrenten ohne Altersprofil und ohne Tabelle 29; Mindestrentenfaktor aus deutscher Verteilung.
**Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: Eurostat (Datensätze wie oben), abgerufen 17.10.2026.*

### v3.53 — Möglichkeitsraum: Aufkommen nach eigener Steuerbasis, Altrenten auf Tabelle 29 begrenzt

**Art der Änderung: MINOR (Prüfrechnung, Dokument), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Anlass:** Fortsetzung v3.52 (offene Punkte: Aufkommen je Staat, Altrenten je Staat).

**Daten (neu abgerufen, Eurostat, 17.10.2026):** nama_10_gdp PC_GDP 2023: Arbeitnehmerentgelt (D1), Bruttobetriebsüberschuss und Selbständigeneinkommen
(B2A3G), Konsum der privaten Haushalte (P31_S14); nasa_10_pens1 PC_GDP S13PU F63_LE 2021 (Tabelle 29) für alle 30 Staaten. Ergänzt in `moeglichkeitsraum_2024.json`.

**Änderung:** `moeglichkeitsraum33.py`: Aufkommen je Staat = deutsche Positionen × (Lohn-, Gewinn-, Konsumanteil relativ zu Deutschland), übrige Positionen wie DE
(Parameter `aufkommen = "eigen"`, Vergleich `"gleich"` = v3.52). Altrenten je Staat auf die ungedeckten Ansprüche der Tabelle 29 skaliert (wie sozialschutz.z_laender).
Konzept (Word) Abschnitt 6.4 mit Spalte „Steuern neu“.

**Bewegte Zahlen (Prüfrechnung, Dividende in deutscher Kaufkraft):** Steuern neu 2028 28,6 % (Irland) bis 34,4 % (Griechenland), Mittel 32,8 %. Dividende 2028 im Mittel
326 € (v3.52: 357 €), Dauerzustand 161 € (v3.52: 205 €). Dauerzustand niedrig oder negativ: Schweden −42 €, Dänemark 2 €, Tschechien 15 €, Frankreich 22 €. Altlasten:
Dänemark 1,2 % Zuschlag (Tabelle 29: kaum ungedeckte Ansprüche), Italien und Frankreich 18 %; Mittel 12,2 %.

**Offen gekennzeichnet:** Wo die Dividende im Dauerzustand verschwindet, trägt das Drittel das Netz nur knapp; diese Staaten brauchen eigene Lösungen. Irland:
Gewinne multinationaler Konzerne werden im Bauplan am Ort der Kunden besteuert, die irische Basis ist überzeichnet. Vereinigtes Königreich und Kanada weiter offen.
**Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** offene Punkte aus v3.52.

*Quellen: Eurostat nama_10_gdp, nasa_10_pens1 (abgerufen 17.10.2026).*

### v3.54 — Neustartverfahren für überschuldete Staaten (Vorschlag), Griechenland als Fall

**Art der Änderung: MINOR (Vorschlag, Prüfrechnung, Dokument), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Frage der Initiative:** Quasi-Insolvenzverfahren für überschuldete Staaten; wie wurde Griechenland saniert; verzichten Gläubiger und Bürger auf garantierte Leistungen?

**Recherchiert:** ESM (Hilfen 288,7 Mrd €; PSI 2012: 197 Mrd €, Schnitt 53,5 %, Beteiligung 97 %, −107 Mrd €; Erleichterungen 2017/2018); griechischer Staatsrat
2015 und 2019 (Rentenkürzungen verfassungswidrig; Sekundärquellen To Vima, European Pensions); Lastenausgleich 1952 (WD 4-176/08); Detroit 2014 (−4,5 %,
Inflationsausgleich gestrichen; Fox News/AP, Sekundärquelle); Sachverständigenrat 2015.

**Neu:** `projekt/Neustartverfahren-2026-10-17.md`; `modell/neustart33.py` (+ `.toml`): Zuschlag des eigenen Fonds bei Schuldenschnitt 0/20/33 % und zusätzlicher
Kürzung der Altrenten 0/10 %. Konzept (Word) Abschnitt 3.8.

**Bewegte Zahlen (Prüfrechnung):** Zuschlag Griechenland 16,5 % → 14,7 % (Schnitt 33 %), 14,9 % (Altrenten −10 %), 13,2 % (beides); Italien 18,0 → 14,6 %;
Frankreich 18,0 → 15,0 %; Spanien 14,2 → 11,6 %.

**Offen gekennzeichnet:** Bei Zins unter Wachstum bringt ein Schnitt wenig; Rentenzusagen wiegen schwerer. Rechtsfragen (Eigentumsschutz, Art. 125 AEUV)
nicht geprüft. Angaben zu Rentenkürzungen in Griechenland aus Sekundärquellen. **Geprüft:** `python3 modell/alles.py`. **Wodurch aufgefallen:** Frage der Initiative.

*Quellen: ESM; WD 4-176/08; Sachverständigenrat 2015; To Vima 11.6.2015; European Pensions 15.7.2020; Euronews 6.5.2016; Fox News 16.4.2014.*

---

### v3.55 — Webseitenentwurf nach Vorbild der veröffentlichten Seite (Drittel-System), Neuseeland gestrichen

**Art der Änderung: MINOR (Darstellung), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Auftrag der Initiative:** Die Ergebnisse in den deutschen Webseitenentwurf übertragen, eng am Vorbild, nur geänderte Inhalte, Zahlen und Begriffe tauschen;
den Vergleich mit Neuseeland streichen (die Label sind eine Neuerung, die nicht dazu passt).

**Neu:** `seite/werkzeuge/entwurf_drittel_bau.py` → `seite/entwurf/drittel/de.html`. Baut auf `seite_bau.py` (Vorlage der veröffentlichten Seite) und ersetzt
nur Daten und Texte: Tarif 0/11/19/25/33 an 1/1,5/2/3 × Grundbedarf (12.348 €, 2026); Label 5/11/17/25 mit Sonderstufe S 33; Transformationsdividende
373 € (2028) → 234 € (2060) je Erwachsenem und Monat, Kaufkraft 2026; viertes Segment „Das starke Netz" im Geldfluss; Zeitpfad mit Grundpfad und zwei
Trendvarianten aus `dynamik33`; Sicherung 4 „Altlasten: Sache der Staaten" mit Fonds und Neustartverfahren; Schuldenkurve des Altlastenfonds
(Spitze 154 % im Jahr 2056 als Stützpunkt mitgeführt, sonst glättet die Interpolation sie auf 151 %); Klub-Text mit 30 Staaten (EU, Norwegen, Island,
Schweiz; 465,6 Mio Menschen). Kopfzeile vorläufig „TAX 33:33" (Namensentscheidung F1 offen). Roter Hinweis „Entwurf zur Prüfung – nicht veröffentlichen".
Stufe in `modell/alles.py`; Register B31 ergänzt.

**Gestrichen:** Neuseeland in `seite/werkzeuge/entwurf33_bau.py` (alter Entwurf, eigene Gliederung) und in Abschnitt 7 des Konzepts (Word, neu gebaut).

**Geprüft:** Desktop- und Mobilansicht ohne Skriptfehler; Bildschirmabzüge aller Abschnitte durchgesehen; `python3 modell/alles.py` (35 Stufen).
**Offen:** Vorbild-Karte Estland nennt weiter „22 % Einheitssatz" aus der veröffentlichten Seite (nicht neu geprüft); Kaufkraftbezug der Netzwerte im Rechner;
Obergrenze des Dachs (32 %) aus der veröffentlichten Seite übernommen, für das Drittel-System nicht neu gerechnet. **Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: wie v3.47–v3.54 (Eurostat, eigene Rechnungen `projektion33`, `netz33`, `dynamik33`, `altlasten`, `moeglichkeitsraum33`).*

---

### v3.56 — Webseitenentwurf: Wortmarke „Das Goldene Drittel", Einleitungssatz, Rechner „mehr im Geldbeutel" mit Zeitstrahl

**Art der Änderung: MINOR (Darstellung, Rechner), keine Zahl der Gesamtrechnung bewegt.** 17. Oktober 2026.

**Auftrag der Initiative:** „TAX 33:33" wird in gleich großen Buchstaben „Das Goldene Drittel" in drei Zeilen; nach „innovativ" der Satz „Alle Steuern
und Abgaben werden gerecht auf Arbeit, Kapital und Automation verteilt. Arbeiten lohnt sich. Ein starkes Netz und die Transformationsdividende
sorgen für sozialen Frieden."; im Rechner ein Zeitstrahl als Regler, statt der Einkommensteuer das Mehr im Geldbeutel (nach Steuern und
Sozialabgaben, mit Arbeitgeberanteil im Lohn).

**Geändert:** Wortmarke und Kopfzeile „Das Goldene Drittel" (drei Zeilen, Schriftgröße 116 in allen Zeilen). Rechner: Jahr als Regler 2028–2060;
angezeigt werden verfügbares Einkommen heute und im Goldenen Drittel (Monat), darin die Transformationsdividende, Mehr im Jahr und im Monat.
`modell/haushalte33.py` schreibt dafür einen Rechnerblock in `haushalte33_raster.json` (Netto heute je Beitragsregime 2028/2035, 1–3 Erwachsene,
0–3 Kinder; Dividende und effektiver Labelsatz je Jahr). Die Seite rechnet das Neue mit denselben Formeln wie `neu()`; Annahmen: Weitergabe 80 %,
Pflichtvorsorge 10 %, Altlastenzuschlag 13,7 % (Beispiel), weitere Erwachsene ohne eigenes Einkommen, heute ab 2035 IGES-Sätze und danach gleich gehalten.
Bruttoregler beginnt bei 10.000 € (Raster).

**Geprüft:** Seite gegen Modell: 42.000 € alleinstehend 2028 +642 €, alleinerziehend 1 Kind +549 €, Paar mit 2 Kindern 55.000 € 2035 +550 € –
identisch mit `haushalte33_raster.json`. Keine Skriptfehler, Desktop und Mobil. `python3 modell/alles.py`.
**Offen gekennzeichnet:** „Automation" ist im Modell keine eigene Steuerbasis; sie wird über Gewinne und Kapitalerträge (33 %) erfasst. Das Mehr steigt
mit dem Einkommen in Euro (100.000 € 2045: +1.136 € im Monat), weil Spitzensatz und Weitergabe hoch wirken; Verteilungswirkung zur Entscheidung.
Bürgergeld/Wohngeld nicht gerechnet. **Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: Kernmodell (Recht 2026), IGES für DAK-Gesundheit 2024 (Sekundärquelle), eigene Rechnungen `haushalte33`, `netz33`, `projektion33`.*

---

### v3.57 — Webseitenentwurf: Textänderungen der Initiative, neue Kontaktadresse, „Mio." in den Einwohnerzahlen

**Art der Änderung: PATCH (Texte), keine Zahl bewegt.** 18. Oktober 2026.

**Auftrag der Initiative (Anlage, 31 Stellen):** u. a. Hinweis zur Hero-Zahl („Prognose nach den Regeln des Projekts", Jahreseinkommen); Problemteil
(„Sozialbeiträge auf Maschinenarbeit"); Erbschaft („33 % Einkommensteuer auf Erbschaften über 100.000 €"); Konzepttext (weniger Verwaltungsebenen,
Anteil direkt vom Dach, Delegation an Verwaltungszusammenschlüsse); Mehrheit der Abgesandten der Gemeindezusammenschlüsse; Sicherungen
(„Warum das Dach Stabilität gibt", „Die Obergrenze"); Vorbilder („Viele Bausteine …", Estland ohne Satzangabe); Klub („Mio." durchgängig, „neues
Bündnis … zukunftsfähiger aufgestellt"); Altlastentext; Zeitleiste („In kleinen Verbünden beginnen", „Stetig erweitern"); „mach mit"; Methodik
(KI-Werkzeuge); Kontaktadresse tax.better@archicrowd.de in Links und Impressum (Betreff „Das Goldene Drittel"); als zweite Projektadresse in `projekt/pruefe_projekt.py` zugelassen.

**Wörtlich übernommen, Rechtschreibung angeglichen:** „ihren Anteil", „Das europäische Dach", „in dem Einzelne mit Veto", Komma vor „ihr Wissen
einzubringen". Klub-Kacheln zweizeilig (Name, Zahl mit „Mio."), damit die Einheit nicht umbricht.

**Offen gekennzeichnet (Wertungen der Initiative, im Modell nicht belegt):** „zukunftsfähiger aufgestellt" (kein Vergleich gerechnet); „viel günstiger
finanziert" (Zinsvorteil des gemeinsamen Fonds nicht beziffert); „moderater Zuschlag" (Beispiel 13,7 % auf alle Steuern, Schuldenquote des Fonds bis
154 % im Jahr 2056 – beide Zahlen stehen nicht mehr im Text, die Kurve zeigt den Anstieg); „Prognose" für eine Modellrechnung unter Annahmen.
Anrede uneinheitlich („mach mit" gegen „Rechnen Sie selbst nach", „Wählen Sie selbst"). **Geprüft:** Seite ohne Skriptfehler; `python3 modell/alles.py`.
**Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: keine neuen; Zahlen wie v3.55/v3.56.*

---

### v3.58 — Webseitenentwurf: durchgängig „Sie", Einleitung in drei Sätzen, „9 von 10 Beschäftigten haben mehr im Geldbeutel"

**Art der Änderung: PATCH (Texte) mit Gegenprobe, keine Zahl der Gesamtrechnung bewegt.** 18. Oktober 2026.

**Auftrag der Initiative:** durchgängig siezen; Einleitung auf drei klare Sätze; statt „+642 €" wieder eine Mehrheitsaussage („9 von 10 haben mehr
im Geldbeutel"?) – die frühere Aussage „über 95 %" war mit dem Systemwechsel entfallen.

**Gegenprobe (`modell/haushalte33.py`, neu: Anteile je Haushaltstyp unter den geltenden Regeln):** Beschäftigte mit mehr verfügbarem Einkommen
2028 und 2035: alleinstehend 100 %, alleinerziehend mit 1 Kind 100 %, Paar mit einem Einkommen und 2 Kindern 97,8 % (Verlust erst bei sehr hohen
Einkommen mit Splitting). **Für alle Erwachsenen gilt „9 von 10" nicht:** Rentnerinnen und Rentner haben nach den Regeln (Kürzung um 12,35 %,
höhere Mehrwertsteuer, Zuschlag) 35 bis 123 € im Monat weniger (Renten 900–2.200 €). Bei rund 46,0 Mio. Erwerbstätigen (Destatis, Jahresdurchschnitt
2025, Sekundärquelle Börsen-Zeitung) und rund 21 Mio. Rentenbeziehenden (Annahme; DRV meldet 19,1 Mio. gezahlte Renten Ende 2025, Renten ≠ Personen)
wären es unter den Erwachsenen eher zwei von drei. Deshalb auf der Seite: „9 von 10 **Beschäftigten**" (gerundet nach unten, Modell 97,8–100 %),
im Kleingedruckten das Beispiel +642 € und das Minus der Rentner. Der Baustein prüft die Aussage bei jedem Bau (≥ 90 %, sonst Abbruch).

**Grenzen:** Lohnverteilung des Kernmodells mit nur 7 Stützstellen; Beamte und Selbständige nicht gerechnet; Fälle ohne Einkommen nicht gerechnet.

**Weitere Änderungen:** „Du"/„Deine Gemeinde" in der Grafik → „Sie"/„Ihre Gemeinde"; „Offen entwickelt – machen Sie mit". Einleitung: „Alle Steuern
und Abgaben werden gerecht auf Arbeit, Kapital und Automation verteilt – höchstens ein Drittel auf jedes Einkommen. Arbeit lohnt sich, und das starke
Netz und die Transformationsdividende sorgen für sozialen Frieden. Die Gemeinden entscheiden selbst, ein gemeinsames europäisches Dach sichert die
gemeinsamen Interessen." **Geprüft:** `python3 modell/alles.py`; Seite ohne Skriptfehler. **Wodurch aufgefallen:** Frage der Initiative.

*Quellen: Destatis (über Börsen-Zeitung, Erwerbstätige 2025); DRV (über Joyn/newstime, 19,1 Mio. Renten Ende 2025); eigene Rechnung `haushalte33`.*

---

### v4.0 — Fassung 4.0 „Das Goldene Drittel": Webseite in sechs Sprachen, Konzept und Kurzfassung, Upload-Paket

**Art der Änderung: MAJOR (neue Fassung der Webseite und der Dokumente: Drittel-System statt 28:28).** 18. Oktober 2026. Benennung „4.0" durch die
Initiative. Keine Zahl der Rechnung bewegt; die Seite zeigt die Ergebnisse von v3.47–v3.58.

**Auftrag der Initiative:** zwei Texte kürzen (Fußnote zur Hero-Zahl ohne Rentnerangabe; Einleitung „… das starke soziale Netz … Die Gemeinden
entscheiden eigenständiger, ein europäisches Dach sichert die gemeinsamen Interessen mit Mehrheitsentscheid."); Länderseiten anpassen; ZIP für die
Aktualisierung der Webseite.

**Neu/geändert:**
- `seite/werkzeuge/drittel_bau.py` (vorher `entwurf_drittel_bau.py`) baut `seite/stand-c/{de,en,fr,it,es,pl}.html` ohne Entwurfsbanner; die
  geänderten Texte liegen in `seite/werkzeuge/drittel_texte.py` (sechs Sprachen, Zahlen sprachgerecht formatiert). Wortmarke je Sprache: The Golden
  Third, Le Tiers d'or, Il Terzo d'oro, El Tercio de Oro, Złota Trzecia (zweizeilig); Netz: The Strong Net, Le Filet solide, La Rete forte, La Red
  fuerte, Mocna Sieć. `seite/entwurf/drittel/` entfällt.
- Anrede: Deutsch „Sie", Französisch „vous" (Grafik „Toi/Ta commune" angeglichen); Italienisch, Spanisch, Polnisch duzen wie die bestehenden Fassungen.
- Dokumente: Konzept als Fassung 4.0 (Sie-Form, „Ihre eigene Route", Kennzahlen „Beschäftigte mit mehr" und Rentner), neu Kurzfassung (zwei Seiten,
  `konzept33-bau.js --kurz`). Die Seite verlinkt `dokumente/TAX-Drittel-Konzept.pdf` und `TAX-Drittel-Kurzfassung.pdf` (nur deutsch).
- `seite/werkzeuge/paket_bau.py` packt Fassung 4.0: sechs Seiten, zwei PDF, `index.html` (Sprachwahl), Weiterleitungen da/nl/sl/et; Schriftenprüfung
  bestanden (7 Dateien in `fonts/`, alle schon auf dem Server). Paket `Webseite-v4.0.zip` neben dem Zielordner, außerhalb des Repositorys bauen (Projektprüfung verbietet .zip).

**Geprüft:** alle sechs Seiten ohne Skriptfehler, mobil ohne Querscrollen (390 px); Rechner in allen Sprachen +642 € (42.000 €, 2028, allein);
Text auf deutsche Reste in den Übersetzungen durchsucht (keine); Kurzfassung zwei Seiten, Konzept elf Seiten; `python3 modell/alles.py`.

**Offen gekennzeichnet:** Übersetzungen maschinell, muttersprachlich gegenzulesen (B16), auch die Namen der Wortmarke (insbesondere Polnisch);
PDF nur deutsch; die Fußnote nennt das Minus der Rentner nicht mehr (steht im Konzept, Kurzfassung Tabelle 1); Wertungen aus v3.57 unverändert offen.
Alte PDF (TAX-2828-*.pdf) bleiben auf dem Server, werden aber nicht mehr verlinkt. **Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: keine neuen; Zahlen wie v3.55–v3.58.*

---

### v4.1 — Länderbezug der Sprachversionen: Referenzland Frankreich, Italien, Spanien, Polen; Englisch als Durchschnitt der 30 Staaten

**Art der Änderung: MINOR (neue Prüfrechnungen, Webseite), keine Zahl der Gesamtrechnung bewegt; Korrektur 62.** 18. Oktober 2026.

**Auftrag der Initiative:** Länderseiten auf die Werte der Länder beziehen, Bezug zu den Spezifika, Begriffen und Instrumenten der Länder; unten
„Referenzland dieser Sprachversion ist …“. Entscheidungen (18.10.2026): Englisch ohne Referenzland (Durchschnitt der 30 Staaten); Rechner „heute
gegen neu“ je Land.

**Neu:**
- `modell/laenderseiten.py` (+ `.toml`) → `laenderseiten.json`: je Staat Dividende 2028–2060 (deutscher Beschlusspfad × Verhältnis Land/DE aus
  dem Möglichkeitsraum-Modell, jahrweise; Mindestrente mit deutschem Anlaufgewicht, Annahme), Geldfluss (Netz und Dividende des Landes),
  Gemeindeformel nach BIP je Kopf, Grundbedarf und Tarifstufen, eigener Altlastenfonds ab der Schuldenquote 2028 (Fortschreibung: FR PLF/RESF 2027,
  IT DPFP 2026 über redigo.info – Sekundärquelle, ES Hacienda, PL Schuldenstrategie, Interpolation).
  Ergebnis 2028/2060 je Erwachsenem und Monat: DE 373/234 €, FR 200/52 €, IT 276/174 €, ES 226/136 €, PL 191/131 € (808/555 zł), EU30 267/147 €.
  Zuschlag des eigenen Fonds: FR 18,4 %, IT 18,1 %, ES 14,0 %, PL 10,5 %; Schuldenspitze FR 200 %, IT 214 %, ES 164 %, PL 128 %.
- `modell/heute_laender.py` (+ `.toml`, alle Parameter mit Quelle und Status) → `heute_laender.json`: vereinfachte Modelle „heute“ nach Recht 2026
  (FR: cotisations, CSG/CRDS, IR mit quotient familial und décote, prime d'activité, allocations familiales; IT: INPS, IRPEF mit detrazioni,
  cuneo fiscale, trattamento integrativo, addizionali, assegno unico; ES: Seguridad Social mit MEI, IRPF mit reducción, mínimos, conjunta; PL: ZUS,
  zdrowotna, PIT mit kwota wolna, wspólne rozliczenie, ulga na dzieci, 800+), Arbeitgeberbeiträge (FR mit RGDU 2026) und „neu“ wie haushalte33.
  **OECD-Abgleich** (Alleinstehend, Durchschnittslohn; Modell 2026 gegen OECD 2024, Abgabenkeil): FR 45,6/47,2, IT 43,7/47,1, ES 42,1/40,6,
  PL 40,0/34,7. PL weicht ab, weil die OECD den Gesundheitsbeitrag offenbar anders abgrenzt; das Modell entspricht polnischen Lohnrechnern (Netto
  rund 72 % des Bruttos); IT: Entlastungen 2025/2026 (cuneo) senken die Steuer gegenüber 2024.
  **Anteil der Beschäftigten mit mehr Geld** (deutsche Lohnverteilung auf den Durchschnittslohn des Landes skaliert, Annahme): IT 100 %, ES 100 %,
  PL 97,8 %, **FR 20–36 %**. Frankreich verliert bei Geringverdienern und Familien: prime d'activité, allocations familiales und quotient familial
  entfallen, Arbeitgeberbeiträge am SMIC wegen RGDU fast null, Dividende niedriger, Zuschlag höher. Sensitivität: Pflichtvorsorge nicht als Abzug
  → Alleinstehende 87 %; Zuschlag 13,7 % → Alleinstehende 62 %. Der Initiative mitgeteilt; Entscheidung offen (N24).
- `daten/aggregate/laender_zeitreihen.json`: Schuldenquoten 2010–2025 (Eurostat gov_10dd_edpt1, amtlich), Treibhausgase 2010–2024 und 1990
  (Eurostat env_air_gge, gesamt ohne LULUCF, amtlich, maschinell übernommen), Klimaziele (FR Code de l'énergie L100-4: −40 % 2030; ES Ley 7/2021
  art. 3: −23 % 2030; IT, PL nur EU-Ziel 2050; EU −55 % netto, hier auf die Bruttoreihe angewandt, Annahme).
- `seite/werkzeuge/laender_texte.py`: Ländertexte (Abgabenkeil und OECD-Rang, Kapitalertragsteuer: FR PFU 31,4 % seit 2026, IT 26 %, ES 19–30 %,
  PL 19 %; Verwaltungsebenen: FR sechs, „millefeuille territorial“; Begriffe cotisations/CSG, INPS, Seguridad Social, ZUS; Rechner-Erläuterung;
  Schulden- und Klimagrafik des Landes; Fußzeile „Referenzland dieser Sprachversion ist …“). Polen in Złoty (4,2397 zł/€, Eurostat 2025).
  Englisch: Durchschnitt der 30 Staaten, Klimagrafik EU-27, Schuldengrafik Klub der zehn, im Rechner Wahl des Landes.
- Hero-Aussage je Land: „9 von 10“ nur, wenn die Rechnung sie deckt (≥ 90 %); Frankreich zeigt stattdessen das Mehr beim Durchschnittslohn
  (+441 €) und im Kleingedruckten den gerechneten Anteil (2 bis 4 von 10).
- Skalen der Schulden- und Klimagrafik aus den Daten (vorher fest).

**Korrektur 62:** siehe Abschnitt 4.

**Geprüft:** alle sechs Seiten ohne Skriptfehler; Rechner gleich Modell (FR 30.000 € +190 €, IT 24.000 € +390 €, ES 21.000 € +355 €,
PL 64.000 zł +1.594 zł, EN-Wahl je Land identisch); `python3 modell/alles.py`.
**Offen:** Übersetzungen und Länderbegriffe muttersprachlich prüfen; feinere Lohnverteilungen je Land (z. B. Eurostat SES); Mindestsicherung
(RSA, ADI, IMV) und Wohnhilfen nicht modelliert; italienische Assegno-unico-Werte 2025; Polen OECD-Abgrenzung; Entscheidung zu Frankreich.
**Wodurch aufgefallen:** Auftrag der Initiative; Korrektur 62 bei der Übertragung auf Länder mit anderem Dividendenanteil.

*Quellen: OECD Taxing Wages 2025; Eurostat gov_10dd_edpt1, env_air_gge, ert_bil_eur_a; Parameterquellen in modell/heute_laender.toml und
modell/laenderseiten.toml (amtlich, Sekundärquellen und Annahmen gekennzeichnet).*

---

### v4.2 — Frankreich: Zerlegung „neu gegen heute“, Zinsempfindlichkeit, Neustartverfahren; Lücke Mindestsicherung und Wohnhilfen

**Art der Änderung: PATCH (Prüfrechnung), keine Zahl der Gesamtrechnung und der Seiten bewegt.** 18. Oktober 2026.

**Fragen der Initiative:** Fehlende Mindestsicherung und Wohnhilfen als Problem des Modells? Was ist aus dem Härtefallfonds geworden? Neustartverfahren
für Frankreich? Liegt das Ergebnis an Schulden und Rentenzusagen oder an allocations familiales und quotient familial?

**Neu:** `modell/zerlegung_laender.py` → `daten/aggregate/zerlegung_laender.json`. Monatsunterschied je Haushalt (Euro 2026), Einzeleffekte gegen den Gesamtfall:

| Frankreich | gesamt | Zuschlag (Altlasten) | Pflichtvorsorge | Dividende unter DE-Niveau | prime d'activité | Rest (Beiträge, Tarif, Weitergabe, MwSt.) |
|---|---|---|---|---|---|---|
| 20.000 €, allein | −131 | −70 | −167 | −107 | −276 | +489 |
| 20.000 €, allein + 1 Kind | −354 | −73 | −167 | −180 | −595 | +661 |
| 30.000 €, Paar + 2 Kinder | −192 | −159 | −250 | −382 | −657 | +1.256 |
| 45.000 €, allein | +441 | −286 | −375 | −89 | 0 | +1.191 |

allocations familiales und quotient familial wirken in diesen Fällen kaum einzeln (die prime d'activité gleicht den Wegfall der allocations
familiales aus; der quotient familial wirkt erst bei steuerpflichtigem Einkommen). Dividende Frankreich 200 € gegen 352 € bei deutschem Niveau
(kaufkraftgleich): Gesundheit 8,4 % BIP (DE 7,0 %), schwächere Steuerbasis. Italien zum Vergleich: alle Fälle positiv.

**Zins:** Zuschlag des eigenen Fonds bei 2,5 / 3,5 / 4,5 % Zins: FR 18,4 / 22,7 / 27,4 %, IT 18,1 / 22,6 / 27,6 %, DE 11,7 / 14,6 / 17,8 %.
Marktzins Frankreich 10 Jahre am 16.10.2026: 4,79 %, Abstand zu Deutschland 137 Basispunkte (ideal-investisseur.fr, Sekundärquelle); Fitch A+
stabil (28.08.2026, refrance.fr, Sekundärquelle). Das Modell rechnet mit 2,5 %, also unter dem heutigen Marktzins (r < g); für Frankreich
ist das optimistisch.

**Neustartverfahren (neustart33, Schnitt 33 %, Altrenten −10 %):** Zuschlag 18,4 → 15,3 %. Anteil mit mehr Geld unverändert (36 / 36 / 36 %,
grobe Verteilung); ohne Zuschlag 62 / 36 / 36 %; Pflichtvorsorge als Vermögen 87 / 36 / 36 %.

**Methodische Lücke (offen, gilt für alle Länder einschließlich Deutschland):** „Heute“ enthält keine bedarfsgeprüften Leistungen außer der
prime d'activité (FR): in Deutschland fehlen Wohngeld, Kinderzuschlag und aufstockendes Bürgergeld, in Frankreich APL und RSA, in Italien
assegno di inclusione, in Spanien ingreso mínimo vital, in Polen dodatek mieszkaniowy. Das überzeichnet den Vorteil des neuen Systems bei
Geringverdienern mit Kindern. Umgekehrt ist der Härtefallfonds (0,65 % BIP je Staat, Wohnkosten über dem Grundbedarf, besondere Lagen;
netz33.toml, Annahme) im neuen System finanziert, aber im Rechner keinem Haushalt zugeordnet. Eine Leistung für Erwerbstätige mit niedrigem
Lohn (wie prime d'activité, Kinderzuschlag) hat das Drittel-System nicht; die Dividende ersetzt sie nur teilweise. Die Aussage „9 von 10“
(DE, IT, ES, PL) ist bis zur Nachrechnung unter diesem Vorbehalt zu lesen. **Wodurch aufgefallen:** Frage der Initiative.

*Quellen: eigene Rechnungen heute_laender, laenderseiten, neustart33; Marktdaten Sekundärquellen wie oben.*

---

### v4.3 — Bedarfsgeprüfte Leistungen heute, Härtefall-Boden neu, Kinderanteil der Dividende, Mindestlohn je Land; Korrektur 63

**Art der Änderung: MINOR (Prüfrechnung), Korrektur 63; Seiten unverändert.** 18. Oktober 2026.

**Auftrag der Initiative:** (1) Lücke aus v4.2 schließen; (2) halbe Kinderdividende am Bedarf prüfen, Vorschläge machen – keine neuen Programme,
sondern Parameter und Regeln, die sich selbst justieren; (3) Wirkung eines Mindestlohns je Land und Erfahrungen.

**Neu:** `modell/sozial_laender.py` (+ `.toml`) → `daten/aggregate/sozial_laender.json`. Heute zusätzlich: DE Bürgergeld-Aufstockung (Regelbedarf
2026, KdU nach Haushaltsgröße – Annahme, Erwerbstätigenfreibetrag § 11b SGB II; Näherung auch für Wohngeld und Kinderzuschlag), FR APL (grob,
Annahme), ES CAPI (Annahme); IT (ADI) und PL greifen bei Vollzeitlöhnen nicht. Neu: Härtefall-Boden = Grundbedarf × (1 + 0,5 je weitere/n
Erwachsene/n + 0,45 je Kind), Skala aus dem deutschen Bürgergeld mit Unterkunft abgeleitet; Kinderanteil s der Dividende aus demselben Topf
(Erwachsenendividende × (1−K/2)/(1−K+sK), K = 16,67 %).

**Kinderbedarf (Verhältnis Kind zu Erwachsenem):** steuerliches Existenzminimum sächlich 0,55, mit BEA 0,79; Regelbedarf 0,63 / 0,69 / 0,84
(0–5 / 6–13 / 14–17 Jahre), Mittel 0,71; OECD-Skala gegen den Erwachsenenmittelwert 0,40 / 0,67; heutiges Kindergeld 259 € gegen
Dividende 373 € = 0,69. Die halbe Kinderdividende (186 €) liegt unter dem heutigen Kindergeld. Varianten 2028 je Erwachsenem / Kind:
s = 0,6: 366 / 220 €; **s = 0,7: 360 / 252 €**; s = 1,0: 342 / 342 € (DE; andere Länder in der Datei).

**Anteil der Beschäftigten mit mehr Geld** (Alleinstehend / Alleinerziehend 1 Kind / Paar mit einem Einkommen, 2 Kinder; grobe Verteilung):

| Stand | DE | FR | IT | ES | PL |
|---|---|---|---|---|---|
| v4.1 (ohne Bedarfsleistungen) | 100/100/98 | 36/36/20 | 100/100/100 | 100/100/100 | 100/98/100 |
| heute mit Bedarfsleistungen, neu mit Boden | 87/87/60 | 36/36/58 | 100 | 100 | 100/98/100 |
| + Kinderanteil 0,7 | 87/87/60 | 36/36/73 | 100 | 100 | 100/98/100 |
| + Pflichtvorsorge erst über dem Grundbedarf | 87/87/60 | 62/36/73 | 100 | 100 | 100 |

Paar mit 2 Kindern bei einem Drittel des Durchschnittslohns, Monat: DE −423 € (s 0,5) → −215 € (Paket); FR +83 €; IT +640 €; ES +944 €.

**Mindestlohn** (Eurostat earn_mw_cur, amtlich; Anteil am Durchschnittslohn 2026 mit Lohnwachstum als Annahme): DE 41,9 %, FR 45,9 %,
ES 50,9 %, PL 52,9 %, IT kein gesetzlicher Mindestlohn. Regel „mindestens 50 % des Durchschnitts“ (Referenzwert der Richtlinie (EU) 2022/2041):
DE +19 % – im neuen System sinken die Lohnkosten dennoch um 1,5 %, weil 21 % Arbeitgeberbeiträge entfallen; Vollzeit allein 2.511 € statt
2.284 € (neu) und 1.687 € (heute) je Monat. FR +9 % – Lohnkosten +8,9 %, weil am SMIC wegen RGDU kaum Beiträge entfallen; Vollzeit allein
1.648 € gegen 1.702 € heute. ES und PL erfüllen die Regel bereits.
**Erfahrungen:** DE 2015: Löhne gestiegen, keine Beschäftigungsverluste, Wechsel zu produktiveren Betrieben (Dustmann u. a. 2022, QJE,
amtlich veröffentlicht, Abstract über RePEc). ES 2019 (+22 %): Beschäftigung der Betroffenen 6–11 Punkte geringer, vor allem Junge, Befristete,
Landwirtschaft (Banco de España, berichtet von elderecho.com 08.06.2021, Sekundärquelle). FR: rund 75 Mrd. € Beitragsentlastungen mit begrenzter
Beschäftigungswirkung und Lohnstauchung am SMIC (Bericht Bozio/Wasmer 2024, Lesart der CFDT, Sekundärquelle).

**Korrektur 63:** siehe Abschnitt 4.
**Offen:** Kosten des Härtefall-Bodens gegen 0,65 % BIP; Inanspruchnahme heutiger Leistungen (volle Inanspruchnahme überzeichnet „heute“);
feinere Lohnverteilung; KdU und APL als Annahmen; Polen ohne Wohngeld.
**Wodurch aufgefallen:** Auftrag der Initiative; die Korrektur 63 folgt aus der Nachrechnung mit Bedarfsleistungen.

*Quellen: Eurostat earn_mw_cur; biallo.de (Familienleistungen 2026, Sekundärquelle); Dustmann u. a. (2022); Banco de España über elderecho.com;
Bozio/Wasmer (2024) über CFDT; Richtlinie (EU) 2022/2041.*

---

### v4.4 — Regeln R1–R4 in der Modellrechnung (Kinderanteil 0,8 geprüft; Pflichtvorsorge über dem Grundbedarf; Härtefall-Boden; Mindestlohn)

**Art der Änderung: MINOR (Prüfrechnung), keine Zahl der Gesamtrechnung und der Seiten bewegt.** 18. Oktober 2026.

**Beschluss der Initiative (18.10.2026):** R2–R4 nach Vorschlag; R1 mit Kinderanteil 0,8 prüfen.

**Neu:** `modell/regeln_r1_r4.py` → `daten/aggregate/regeln_r1_r4.json`.

**R1 Kinderanteil (Topf unverändert), 2028 je Monat Erwachsene / Kind:** DE 0,5: 373 / 186 €; 0,7: 360 / 252 €; **0,8: 354 / 283 €**;
FR 0,8: 190 / 152 €; IT 262 / 210 €; ES 214 / 171 €; PL 767 / 613 zł. 0,8 entspricht dem Verhältnis des steuerlichen Existenzminimums eines
Kindes mit Betreuungsbedarf zu dem eines Erwachsenen (9.756 / 12.348 = 0,79) und liegt über dem heutigen Kindergeld (259 €). Rückwirkung
über die Lücke Grundbedarf − Erwachsenendividende (Mindestrente, Invalidität, Arbeitslosigkeit): +0,02 % BIP 2060, Dividende −1 €.

**Anteil der Beschäftigten mit mehr Geld (Paket R1 0,8 + R2 + R3; heute mit Bedarfsleistungen):** DE 87 / 87 / 60 %, FR 62 / 36 / 73 %,
IT, ES, PL 100 %. Gegen 0,7 unverändert (grobe Verteilung). Beispielhaushalte (Monat): DE Paar + 2 Kinder bei 1/3 Durchschnittslohn −165 €
(0,5 ohne Regeln: −423 €), bei 2/3 +800 €; FR Alleinerziehend bei 1/2 −229 €.

**R2 Pflichtvorsorge erst über dem Grundbedarf:** Geringverdiener sparen weniger, die Mindestrente muss mehr aufstocken. DE: Faktor der
mittleren Aufstockung 0,433 → 0,585; Mindestrente 2060 0,60 → 0,81 % BIP, Dauerzustand 1,07 → 1,45 % BIP; Dividende 2060 −15 €,
Dauerzustand −26 € je Erwachsenem und Monat.

**R3 Härtefall-Boden:** wirkt bei Familien mit sehr niedrigem Lohn (FR Paar + 2 Kinder 58 → 73 %). Er zieht jeden zusätzlichen Euro voll an,
solange der Haushalt unter dem Boden liegt (kein Erwerbstätigenfreibetrag wie heute im Bürgergeld). Größenordnung DE: Fonds 31,9 Mrd. €
(0,65 % BIP); 809.815 erwerbstätige Leistungsberechtigte 2025 (BT-Drs. 21/6855, amtlich) kosteten bei 500 bzw. 1.000 € Aufstockung
4,9 bzw. 9,7 Mrd. € – im Rahmen, Wohnkosten über dem Grundbedarf kommen hinzu (nicht beziffert).

**R4 Mindestlohn ≥ 50 % des Durchschnitts (Vollzeit, Paket 0,8), Monat heute → neu:** DE (+19,3 %) allein 1.687 → 2.610 €, Paar + 2 Kinder
3.012 → 3.500 €; FR (+8,9 %) allein 1.702 → 1.742 €, Alleinerziehend 2.036 → 1.888 €, Paar + 2 Kinder 2.530 → 2.330 €; ES, PL ohne Änderung
der Regel, Haushalte deutlich im Plus. Lohnkosten DE −1,5 %, FR +8,9 % (v4.3).

**Offen:** feinere Lohnverteilung (die Anteile springen in groben Stufen); Erwerbsanreiz im Bodenbereich (Freibetrag wie § 11b SGB II als Regel
prüfen); R2 gegen höhere Mindestrente abwägen (z. B. Freibetrag halber Grundbedarf); Frankreich bleibt bei Alleinerziehenden und Geringverdienern
im Minus. **Wodurch aufgefallen:** Beschluss der Initiative.

*Quellen: eigene Rechnungen sozial_laender, netz33, moeglichkeitsraum33; BT-Drs. 21/6855 (02.07.2026).*

---

### v4.5 — Eine Regel für Boden, Erwerb und Vorsorge: „Der Grundbedarf ist der Boden, das eigene Einkommen zählt zur Hälfte“

**Art der Änderung: MINOR (Prüfrechnung), keine Zahl der Gesamtrechnung und der Seiten bewegt.** 18. Oktober 2026.

**Beschluss und Auftrag der Initiative:** R1 Kinderanteil 0,8 beschlossen. R2/R3 seien zu „gebastelt“; gesucht ist eine klare Regel nahe an der
Konzeptphilosophie: Das Netz trägt, wird aber keine Hängematte; enges Existenzminimum als Bezugspunkt, das schon ein Engagement zur eigenen
Vorsorge verlangt.

**Regel (ersetzt R2 und R3):** Boden = Grundbedarf des Landes × OECD-modifizierte Skala (1 / 0,5 / 0,3) – enges Existenzminimum, internationaler
Standard der Armutsmessung. Die Dividende zählt voll, das eigene Einkommen nach Steuern zur Hälfte (dieselbe Halbanrechnung wie bei der
Mindestrente). Pflichtvorsorge 10 % ab dem ersten Euro, auch am Boden nicht aufgestockt. Damit gibt es eine Zahl (½) für Erwerb und Alter und
einen Maßstab (Grundbedarf) für Steuerfreiheit, Boden und Mindestrente. R2 entfällt; die Rückwirkung auf die Mindestrente (v4.4: −26 € im
Dauerzustand) entfällt mit ihr.

**Neu:** `modell/regel_boden.py` (+ `.toml`) → `daten/aggregate/regel_boden.json`.

**Ergebnisse (2028, Monat; heute mit Bedarfsleistungen):**
- Boden allein / allein + 1 Kind / Paar + 2 Kinder: DE 1.029 / 1.338 / 2.161 €; FR 971 / 1.262 / 2.039 €; IT 862 / 1.121 / 1.810 €;
  ES 801 / 1.041 / 1.682 €; PL 2.819 / 3.665 / 5.921 zł. Zum Vergleich DE Bürgergeld mit Unterkunft (Annahmen sozial_laender.toml):
  1.083 / – / 2.634 €.
- Anteil der Beschäftigten mit mehr Geld: DE 100 / 87 / 60 %, FR 73 / 36 / 100 %, IT, ES, PL 100 %.
- Belastung eines zusätzlichen Euros bei halbem Vollzeit-Mindestlohn: neu 56–69 % in allen Ländern; heute DE 90–98 % (Bürgergeld), FR 52 %
  (prime d'activité), IT 4 %, ES 7 %, PL 21 % (keine Leistung in diesem Bereich).
- DE Paar + 2 Kinder ohne Erwerb: Boden 2.105 € gegen Bürgergeld 2.634 € (eng gewollt); bei ¼ Mindestlohn 2.403 € gegen 2.838 €, bei vollem
  Mindestlohn 3.169 € gegen 3.012 €. Alleinstehend Vollzeit-Mindestlohn 2.280 € gegen 1.687 €.
- IT, ES, PL: Der Boden liegt über der heutigen Absicherung von Geringverdienern (dort heute keine allgemeine Leistung für Beschäftigte).

**Kosten (DE, grob, offen):** Aufstockung für Beschäftigte, wenn alle 45 Mio. Beschäftigten den jeweiligen Haushaltstyp hätten: 22,8 / 25,1 /
52,0 Mrd. € gegen 31,9 Mrd. € Härtefallfonds. Die Schätzung überzeichnet stark, weil Teilzeit- und Minijob-Beschäftigte meist mit einem weiteren
Einkommen im Haushalt leben (Anrechnung je Haushalt). Belastbar nur mit Haushaltsdaten (EU-SILC, Datenvertrag nötig). Umrechnung: 1 Mrd. €
über dem Fonds kostet rund 1 € Dividende je Erwachsenem und Monat (0,1 % BIP ≈ 5,1 €).

**Offen:** Kosten mit Haushaltsverteilung; Grundbedarf je Land gegen nationale Armutsschwellen prüfen; feinere Lohnverteilung.
**Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: eigene Rechnungen sozial_laender, regeln_r1_r4, netz33; OECD-modifizierte Skala (Eurostat-Standard).*

---

### v4.6 — Regel Boden beschlossen; Kosten aus der Dezilverteilung (EU-SILC) je Land

**Art der Änderung: MINOR (Beschluss, Prüfrechnung), keine Zahl der Gesamtrechnung und der Seiten bewegt.** 18. Oktober 2026.

**Beschluss der Initiative (18.10.2026):** „Rechne das so“ – Regel aus v4.5 (Boden = Grundbedarf × OECD-Skala, eigenes Einkommen zur Hälfte,
Pflichtvorsorge 10 % ab dem ersten Euro) und Kinderanteil 0,8 gelten; Kosten aus veröffentlichten Verteilungstabellen schätzen.

**Neu:** `modell/boden_kosten.py` (+ `.toml`) → `daten/aggregate/boden_kosten.json`. Weil der Boden mit der OECD-Skala gebildet wird, ist er je
Äquivalenzerwachsenem der Grundbedarf; die Aufstockung lässt sich daher aus den Dezilen des äquivalenzgewichteten verfügbaren Einkommens schätzen
(Eurostat ilc_di01, EU-SILC 2025, amtlich). Band: heutiges Einkommen in D1–D2 voll bzw. zur Hälfte eigenes Einkommen (Rest Transfers).
Annahmen: 75 % der Bevölkerung in Haushalten im Erwerbsalter, 1,4 Personen je Äquivalenzerwachsenem, Fortschreibung 2024→2026.

| Land | Grundbedarf / Median | Kosten der Aufstockung, % BIP | Mrd. € | Netzbudget im Erwerbsalter (Härtefall + Arbeitslosigkeit + Invalidität), % BIP |
|---|---|---|---|---|
| DE | 40 % | 0,13–0,59 | 6,0–27,3 | 1,17 |
| FR | 42 % | 0,48–1,25 | 15,0–39,0 | 1,74 |
| IT | 44 % | 0,33–0,96 | 7,7–22,5 | 1,37 |
| ES | 45 % | 0,50–1,20 | 8,5–20,3 | 2,05 |
| PL | 48 % | 0,44–1,29 | 3,9–11,7 Mrd. € | 1,23 |

Die Regel ist in allen fünf Ländern im vorhandenen Netzbudget finanziert; nur Polen überschreitet es in der oberen Schätzung knapp (0,06 Punkte,
Dividende rund −6 zł). Der Grundbedarf liegt bei 40–48 % des Medianeinkommens – unter der Armutsgefährdungsschwelle (60 %), nahe der Schwelle
für strenge Armut (40 %): ein enges Existenzminimum, wie beschlossen.

**Offen:** Einbau in Rechner und Texte der Seiten; Aussage zu den Gewinnern je Land neu fassen (DE 100/87/60 %, FR 73/36/100 %); Annahmen zu
Haushaltsstruktur und Transfers durch Haushaltsdaten ersetzen, sobald verfügbar. **Wodurch aufgefallen:** Beschluss der Initiative.

*Quellen: Eurostat ilc_di01 (EU-SILC 2025); eigene Rechnungen regel_boden, moeglichkeitsraum33.*

---

### v4.7 — Vergleich mit Dänemark und Schweden; Vorschlag Härtefall (H1–H3) und Rolle der Gemeinden (G1–G5)

**Art der Änderung: MINOR (Prüfrechnung, Vorschlag), keine Zahl der Gesamtrechnung und der Seiten bewegt.** 18. Oktober 2026.

**Auftrag der Initiative (18.10.2026):** Konzept mit den Regeln in Dänemark und Schweden vergleichen; benachteiligte Gruppen; Reaktion der
Härtefallregel; Ausgabe durch die Gemeinden und deren Gestaltungsrecht.

**Neu:** `modell/vergleich_dk_se.py` (+ `.toml`) → `daten/aggregate/vergleich_dk_se.json`; `projekt/Vorschlag-Haertefall-Gemeinden-2026-10-18.md`.
Datenquellen: borger.dk (kontanthjælp 2026, amtlich), STAR (Reform L 13, amtlich), Socialstyrelsen (Riksnorm 2026, Meddelandeblad 4/2026,
amtlich), Prop. 2025/26:201 (amtlich), SCB (Kommunalsteuer 2026, amtlich), Eurostat ilc_di01 D5 DK 269.953 kr., SE 326.669 kr. (EU-SILC 2025,
amtlich); themis.dk (Steuersätze DK, Sekundärquelle); kommunale Richtlinie Falköping (jobbstimulans, an der Quelle zu prüfen).

| Kennzahl | DE Boden | DE heute | DK | SE |
|---|---|---|---|---|
| Niveau mit Wohnen, % des Medians | 40,3 | 42,4 | 44,5 (netto, Wohngeld zusätzlich) | Norm + tatsächliche Miete |
| Niveau ohne Wohnen, % des Medians | 22,5 | – | – | 18,1 / 26,4 (Paar + 2 Kinder) |
| Gewicht eines Kindes | 0,30 | 0,63–0,84 | Zuschlag je Versorger | 0,57–1,0 |
| Belastung eines Zusatzeuros im Bezug | 66 % | 98 % | 42 % / 80 % | 100 % / 80 % |

**Befund:** Das Niveau des Bodens entspricht DK und dem Bürgergeld. Unterschiede: Wohnkosten werden in DK/SE getrennt behandelt (Boden pauschal,
Wohnanteil DE ≈ 454 €), Kinder deutlich höher gewichtet. Benachteiligt im Konzept: Familien mit geringem Erwerb (DE Paar + 2 Kinder ohne Erwerb
−473 € gegen Bürgergeld), Haushalte mit hohen Mieten (700 € → Lücke 246 €), Mehrbedarfe, einmalige Notlagen; Rentner und französische
Geringverdiener aus anderen Gründen (Rentnerausgleich, N24).

**Vorschlag (nicht beschlossen):** Härtefall als Zuschlag zum Boden mit derselben Halbanrechnung – H1 Wohnkosten über dem Wohnanteil bis zur
örtlichen Angemessenheitsgrenze (Gemeinde im Korridor des Landes), H2 Mehrbedarfe landeseinheitlich, H3 Einmalbedarfe nach Ermessen der Gemeinde
aus einem Pauschalbudget. Kindergewicht als Parameter K1 (0,3 / 0,45 / 0,5 → DE Paar + 2 Kinder 2.161 / 2.470 / 2.572 €). Gemeinde zahlt
Aufstockung und Härtefall aus, Land setzt Höhe und erstattet den Rechtsanspruch voll (G1–G5); dänische Erstattungstreppe nicht empfohlen
(VIVE 2020: Bevorzugung arbeitsmarktnaher Fälle; eine Studie, erstes Reformjahr).

**Offen:** Entscheidung H1–H3, K1, G1–G5 (N27); Kosten von H1–H3 und K1 mit Mietdaten nach Haushaltstyp. **Wodurch aufgefallen:** Auftrag der
Initiative.

*Quellen: siehe `projekt/Vorschlag-Haertefall-Gemeinden-2026-10-18.md`, Abschnitt Quellen; eigene Rechnungen regel_boden, vergleich_dk_se.*

---

### v4.8 — Kindergewicht 0,55 (Vorschlag), Härtefall und Gemeinderolle eingerechnet, Gini je Land; Webseite und Konzept Fassung 4.8 zur Freigabe

**Art der Änderung: MINOR (Regelvorschlag, Prüfrechnungen, Webseite, Konzept).** 18. Oktober 2026. Bewegte Zahlen: Dividende auf der Seite
373 → 354 € je Erwachsenem, je Kind 186 → 283 € (R1 eingebaut, Topf 0,948); Beispiel 42.000 € +642 → +630 €; Rentner −35…−123 → −54…−142 €
im Monat; Paar + 2 Kinder ohne Erwerb (Boden) 2.105 → 2.620 €; DE Beschäftigte mit mehr 100/87/60 → 100/100/98 %.

**Auftrag der Initiative (18.10.2026):** Kindergewicht fair anpassen (auch 0,7–0,8), sonst den Empfehlungen v4.7 folgen, alles rechnen und
freigeben lassen; Webseite: Bildung/Gemeinden, Anreize, Sicherheit mit Freiheit, Gini-Grafik, Dividenden- und Schuldengrafik zurücknehmen,
andere Kontinente mit Vorbehalt.

**Neu:** `modell/kindergewicht.py` (Varianten 0,3–0,8), `modell/haertefall.py` (+ `.toml`, H1–H3 gegen Netzbudget), `modell/gini.py` (+ `.toml`,
Gini heute und neu je Land und Jahr); `boden_kosten.py` mit Kindergewicht (`kinder_je_aequivalent` 0,31, Annahme); `regel_boden.py` gibt Topf und
deutsche Beispiele aus; Seite: `seite/werkzeuge/v48_bau.py`, `v48_texte.py`, `drittel_bau.py` (VERSION v4.8); Konzept `konzept33-bau.js` Fassung 4.8;
Vorlage `projekt/Freigabe-v4.8-2026-10-18.md`.
Datenquellen: Eurostat ilc_di12 (Gini 2025: DE 30,1, FR 30,4, IT 31,0, ES 30,8, PL 24,9, DK 28,2, SE 28,6) und ilc_di01 (Anteile D1/D10),
amtlich, Abruf 18.10.2026; Kinderfreibetrag 2026 (Sekundärquelle); Destatis 10.500 € je Schüler 2024 (über Münster Aktuell, Sekundärquelle).

| Kindergewicht | DE Paar + 2 ohne Erwerb | Kosten DE / FR / IT / ES / PL (% BIP, obere Schätzung) |
|---|---|---|
| 0,3 | 2.105 € | 0,59 / 1,25 / 0,96 / 1,20 / 1,29 |
| **0,55 (Vorschlag)** | **2.620 €** | **0,77 / 1,47 / 1,18 / 1,43 / 1,56** |
| 0,8 | 3.134 € | 0,96 / 1,73 / 1,40 / 1,72 / 1,87 |

Begründung 0,55: sächliches Existenzminimum Kind / Grundbedarf; BEA als Sachleistung der Gemeinde. Mit H1–H3 (Annahmen) Reserve obere Schätzung:
DE +0,17, FR −0,01, IT −0,07, ES +0,32, PL −0,65 % BIP (PL Dividende −63 zł). Gini 2028: DE 30,1 → 26,5, FR 30,4 → 32,4, IT 31,0 → 28,8,
ES 30,8 → 25,3, PL 24,9 → 19,3 (statisch; Rekonstruktion trifft amtlich auf 0,1–0,3 Punkte). Rechner der Seite gegen Modell: 20 Stichproben,
Abweichung ≤ 1 €.

**Befunde, die offen geführt werden:** Frankreich – Gini steigt (N24). IT/ES/PL – Belastung des Zusatzeuros bei kleinem Lohn höher als heute
(Boden neu), heutige Bedarfsleistungen dort nicht gerechnet (Anteil mit mehr überzeichnet). R1 senkt die Erwachsenendividende auch für Rentner.
Korrektur 63 („9 von 10“ in DE nicht gedeckt) galt für Kindergewicht 0,3; mit 0,55 ist die Aussage gedeckt (98 %), vorbehaltlich Freigabe.

**Offen:** Freigabe (Kindergewicht, H1–H3/G1–G5, Upload Fassung 4.8); Übersetzungen gegenlesen; Mietdaten für H1; Rentnerausgleich.
**Wodurch aufgefallen:** Auftrag der Initiative.

*Quellen: siehe `projekt/Freigabe-v4.8-2026-10-18.md`.*

---

### v4.9 — Frankreich und Polen im Gini: Zerlegung und Gegenproben; Korrektur 64

**Art der Änderung: PATCH (Prüfrechnung, Korrektur der Erklärung), keine Zahl der Gesamtrechnung bewegt; Seite und Konzept: Erklärung und
Spannweite für Frankreich ergänzt.** 18. Oktober 2026.

**Frage der Initiative (18.10.2026):** Warum hat Frankreich eine solche Anomalie, gibt es Denk- oder Rechenfehler; warum wächst dort die
Ungleichheit über die Zeit und nähert sich wenig an; warum ist der Effekt in Polen so gut?

**Neu:** `modell/gini_frankreich.py` → `daten/aggregate/gini_frankreich.json`. Gegenproben zu `gini.py` (2028, untere Schätzung):

| | DE | FR | IT | ES | PL |
|---|---|---|---|---|---|
| amtlich 2025 | 30,1 | 30,4 | 31,0 | 30,8 | 24,9 |
| Rechnung v4.8 | 26,3 | 32,2 | 28,8 | 25,3 | 19,3 |
| Weitergabe gedeckelt beim Beitrag zum 1-fachen Durchschnittslohn | 25,7 | 27,6 | 25,8 | 23,5 | 17,8 |
| dito 1,5-fach | 26,2 | 29,8 | 26,8 | 24,6 | 18,5 |
| Abbildung über Familienhaushalt statt Einzelperson | 24,2 | 29,5 | 29,6 | 24,2 | 19,0 |
| Dividende je Erwachsenem / Median (%) | 13,9 | 8,1 | 13,4 | 11,9 | 13,1 |
| Boden / Median (%) | 40,3 | 41,5 | 44,2 | 44,5 | 48,3 |

Änderung des verfügbaren Einkommens je Dezil FR: +58 / +12 / +3 / +7 / +18 / +18 / +19 / +23 / +25 / +29 %; PL: +92 / +50 / +43 / +38 / +33 /
+29 / +26 / +22 / +20 / +19 %. Arbeitgeberbeiträge FR (Modell, Recht 2026): 0 % beim 0,3-fachen, 0,7 % beim 0,5-fachen, 33 % beim
1-fachen, 46 % beim 2-fachen Durchschnittslohn, ohne Deckel; DE höchstens 18.107 € (BBG).

**Befund Frankreich:** Kein Rechenfehler gefunden. Die Anomalie hat drei Ursachen.
1. **Weitergabe ungedeckelter Arbeitgeberbeiträge:** Hohe Löhne steigen um 24–41 %. Das ist die Folge der Regel „80 % Weitergabe“
   und keine Rechenpanne.
2. **Delle beim SMIC:** Dort fallen wegen der Beitragsentlastung (RGDU) kaum Beiträge an, die weitergegeben werden könnten, und die prime
   d'activité entfällt. Das trifft die Dezile 3–4 (+3 / +7 %).
3. **Kleinste Dividende:** Das Netz ist in Frankreich am teuersten (11,0 % BIP, Gesundheit 8,4). Die Dividende beträgt deshalb nur
   5,15 % BIP, 8 % des Medians gegenüber 12–14 % in den anderen Ländern.

**Denkfehler 1 (Abbildung):** Die Rechnung bildet jeden Punkt der Verteilung als alleinstehende Person ab. Damit landet die SMIC-Delle in den
mittleren Dezilen. Mit Familienhaushalten ergibt sich 29,5 statt 32,2. Die wahre Haushaltsmischung liegt dazwischen.

**Denkfehler 2 (Bewertung):** Weitergegebene Beiträge zählen als verfügbares Einkommen. Heute finanzieren sie in Frankreich Renten nach
Lohnhöhe (AGIRC-ARRCO) und Arbeitslosengeld. Der Gewinn hoher Löhne ist als Einkommen richtig, als Wohlfahrtsgewinn aber überzeichnet. Das
gilt für alle Länder ohne Bemessungsgrenze stärker (FR, IT).

**Über die Zeit:** Der Gini in Frankreich ist 2028–2060 praktisch konstant (32,4 → 32,3). Er springt beim Systemwechsel und wächst danach
nicht weiter. In DE, IT und PL steigt er leicht, weil die Dividende sinkt.

**Befund Polen:**
- Die Dividende ist der größte Anteil am BIP (8,96 %), weil das Netz am billigsten ist (7,54 %).
- Der Boden liegt am höchsten über dem Median (48 %): Der Grundbedarf folgt dem Preisniveau (65 % von DE), die Einkommen liegen
  relativ dazu niedriger.
- Abgaben heute sind fast proportional (ZUS und 9 % Gesundheitsbeitrag).

Vorbehalte:
- Heutige Sozialhilfe in Polen ist nicht gerechnet; der Gewinn unten ist dadurch zu hoch.
- Die Bodenkosten überschreiten in der oberen Schätzung das Budget (1,56 gegen 1,23 % BIP); der Effekt ist dort teilweise nicht finanziert.

**Korrektur 64:** Die Erklärung des französischen Gini-Anstiegs in v4.8 (Seite, Konzept, Freigabevorlage: „Lohnzuschüsse fallen weg und
hohe Einkommen zahlen weniger als heute“) war unvollständig und gewichtete falsch. Hauptursache ist die Weitergabe ungedeckelter
Arbeitgeberbeiträge, dazu kommt die Abbildung über Einzelpersonen. Die Texte sind in sechs Sprachen und im Konzept berichtigt, mit Spannweite
(Deckel 27,6–29,8; Familie 29,5). **Wodurch aufgefallen:** Nachfrage der Initiative.

**Offen:** Entscheidung über einen Deckel der Weitergabe. Ohne Bemessungsgrenze verbliebe der Rest beim Arbeitgeber; eine Alternative ist die
Zuführung an Netz und Dividende des Landes. Weitere offene Punkte:
- Haushaltsmischung aus EU-SILC statt zweier Grenzfälle;
- Abgleich FR mit OECD Taxing Wages auch beim 1,67-fachen Lohn;
- heutige Bedarfsleistungen PL, IT, ES;
- Gini mit dem Wert der Rentenansprüche.

*Quellen: Eurostat ilc_di01, ilc_di12; eigene Rechnungen gini, gini_frankreich, heute_laender (OECD-Abgleich beim Durchschnittslohn).*

---

### v4.10 — Rentnerausgleich, Altansprüche, Lebensarbeitszeit (Vorschlag); Korrektur 65

**Art der Änderung: MINOR (Prüfrechnung, Vorschlag, Korrektur).** 18. Oktober 2026. Bewegte Zahl: Rentner im Konzept −54…−142 € → wieder
−35…−123 € im Monat (Korrektur 65); sonst keine Zahl der Gesamtrechnung oder der Seiten.

**Frage der Initiative (18.10.2026):** Lösungen für den Rentnerausgleich; Lebensarbeitszeit mit Formel; Altansprüche ausreichend bedacht?

**Neu:** `modell/rentnerausgleich.py` (+ `.toml`) → `daten/aggregate/rentnerausgleich.json`; `projekt/Vorschlag-Rentnerausgleich-2026-10-18.md`.
Datenquellen: Destatis Sterbetafel 2023/2025 (Lebenserwartung mit 65: 18,0 / 21,1 Jahre, amtlich); Grundsicherung im Alter Dezember 2025
764.065 Empfänger, Ausgaben 2025 11,8 Mrd. € (Destatis/BMAS über Sekundärquelle); Dänemark 70 ab 2040 (lex.dk), Niederlande ⅔-Kopplung
(Sekundärquelle).

| Variante (DE 2028) | 900 € | 1.200 € | 1.600 € | 2.200 € | Mehrkosten |
|---|---|---|---|---|---|
| Beschluss | −35 | −49 | −92 | −123 | – |
| Kürzung 7,5 % statt 12,35 % | +7 | 0 | −27 | −43 | 0,26 % BIP |
| Pauschale 50 € | +13 | −1 | −44 | −75 | 0,21 % BIP |
| Besteuerungsanteil 83 % | −35 | −46 | −64 | −55 | 0,11 % BIP |

Lebensarbeitszeit (Rentenbeginn an Lebenserwartung gekoppelt, ab 2030): ⅔-Kopplung entlastet Fonds und Mindestrente um 0,18 (2040) bis 0,27 %
BIP (2050), Summe 2028–2098 8,6 % BIP-Jahre; 1:1-Kopplung 12,9. Kosten Kürzung 7,5 %: 7,9; Boden für kleine Bestandsrenten: 4,4.

**Befunde zu den Altansprüchen:** kein Boden für kleine Bestandsrenten (Mindestrente nur nach Stichtag; heute Grundsicherung im Alter);
Einzelregel für Übergangsjahrgänge fehlt (Teilanspruch wird voll mit der Dividende verrechnet); Rentenalter uneinheitlich (65 im
Kohortenschema, 67 bei der Mindestrente); Hinterbliebene und Beamtenpensionen zu bestätigen; Eigentumsschutz juristisch offen.

**Korrektur 65:** v4.8/v4.9 (Konzept, Freigabevorlage, Logbuch, Projektsteuerung) gaben das Rentnerminus mit −54 bis −142 € an, weil der
kleinere Erwachsenenanteil der Dividende (R1) vom Rentnernetto abgezogen wurde. Die Dividende ist aber Teil der Bestandsrente (Fonds zahlt den
Anspruch über der Dividende, sozialschutz.z_pfad); R1 verschiebt nur Kosten in den Fonds. Richtig: −35 bis −123 €. **Wodurch aufgefallen:**
Nachrechnung der Rentnerfälle für den Ausgleich.

**Offen:** Entscheidung A, B1, T1, L1; Rentenverteilung (DRV, Rentenbestand nach Zahlbetrag) statt vier Beispielrenten; Kosten von T1 rechnen;
Rentenalter im Kohortenschema vereinheitlichen; juristische Prüfung.

*Quellen: siehe `projekt/Vorschlag-Rentnerausgleich-2026-10-18.md`.*

---

### v4.11 — Rentnerpaket beschlossen und gerechnet (A, T1, B1, L1); „Boden“ heißt Grundauskommen

**Art der Änderung: MINOR (Beschluss, Rechnung), Zahlen der Seiten und des Konzepts bewegt.** 18. Oktober 2026.

**Beschluss der Initiative (18.10.2026):** „Folge deinen Empfehlungen und rechne ohne komplexe Sonderregeln. Vermeide den Begriff Boden, finde
einen besseren.“

**Umgesetzt:**
- **A:** Bestandsrenten werden um 7,5 % statt um 12,35 % gekürzt (`altlasten.toml`, `haushalte33.toml`).
- **T1:** Der Altanspruch verrechnet die Dividende nur im Verhältnis der Altjahre (`sozialschutz.toml [rentner]`).
- **B1:** Das Grundauskommen gilt auch für kleine Bestandsrenten, mit voller Anrechnung der Rente. Angesetzt sind 0,143 % BIP × Altanteil, so
  viel wie die heutige Grundsicherung im Alter (Sekundärquelle). Die Kosten trägt der Fonds.
- **L1:** Rentenbeginn 67 + ⅔ des Zuwachses der Lebenserwartung mit 65 ab 2030. Er wirkt auf den Fonds und auf die Mindestrente. Im
  Kohortenschema gilt jetzt einheitlich das Rentenalter 67 (vorher 65).
- **Nicht übernommen:** die Lebensarbeitsjahre als zweiter Weg zum Rentenbeginn (Sonderregel).
- **Weitere Anpassungen:**
  - Der Altlastenzuschlag wird jetzt in haushalte33, sozial_laender und rentnerausgleich aus `altlasten.json` gelesen; vorher stand der Wert
    13,7 % fest im Parameterfile.
  - Rentnerfälle: Heute wird mit Grundsicherung im Alter gerechnet (1.083 €), neu mit dem Grundauskommen (1.029 €).
- **Begriff:** „Boden“ heißt in allen Texten jetzt **Grundauskommen**:
  - Webseite in sechs Sprachen: Grundauskommen / basic livelihood / minimum vital / minimo vitale und die übrigen Entsprechungen;
  - Konzept, Freigabevorlage.

  Dateinamen der Skripte (`regel_boden.py`, `boden_kosten.py`) bleiben unverändert, damit die Versionsgeschichte lesbar bleibt.

Datenquellen: wie v4.10 (Destatis Sterbetafel 2023/2025; Grundsicherung im Alter 2025, Sekundärquelle); eigene Rechnungen.

**Bewegte Zahlen:**

| Größe | vorher (v4.10) | v4.11 |
|---|---|---|
| Beitrag gemeinsamer Altlastenfonds (% BIP) | 4,59 | 5,28 |
| Altlastenzuschlag auf alle Steuern | 13,7 % | 15,8 % |
| Schuldenquote des Fonds, Spitze | 153,6 % | 149,6 % (2056) |
| Zuschlag je Land DE / FR / IT / ES / PL | 11,7 / 18,4 / 18,1 / 14,0 / 10,5 % | 14,2 / 20,3 / 20,7 / 16,5 / 12,7 % |
| Dividende DE 2060 (Kaufkraft 2026) | 234 € | 239 € |
| Rentner 900 / 1.200 / 1.600 / 2.200 € (heute mit Grundsicherung) | −35 / −49 / −92 / −123 € | −54 / −35 / −33 / −52 € |
| Alleinstehend 42.000 €: mehr im Monat | +630 € | +602 € |
| DE Beschäftigte mit mehr (Haushaltstypen) | 100 / 100 / 98 % | 98 / 98 / 98 % |
| Gini 2028 DE / FR / IT / ES / PL | 26,5 / 32,4 / 28,8 / 25,3 / 19,3 | 26,4 / 32,2 / 28,5 / 25,1 / 19,1 |

**Zerlegung des Fondsbeitrags (% BIP):**
- Basis mit einheitlichem Rentenalter 67: 4,64;
- A: +0,26;
- **T1: +0,50**;
- B1: +0,07;
- L1: −0,18;
- Ergebnis 5,28.

T1 ist teurer als der Überschlag in v4.10 (0,3). Die Rentner 900 € verlieren gegenüber heute mit Grundsicherung 54 €, weil das Grundauskommen
(Grundbedarf 12.348 € im Jahr) unter dem heutigen Bedarf aus Regelbedarf und Unterkunft liegt (Annahme 1.083 €).

**Offen:**
- Entscheidung, ob T1 seinen Preis wert ist (ohne T1: Fonds ≈ 4,78 % BIP, Zuschlag ≈ 14,3 %, Überschlag);
- Rentenverteilung DRV statt Beispielrenten;
- Eigentumsschutz;
- Übersetzungen des neuen Begriffs gegenlesen.

**Wodurch aufgefallen:** Beschluss der Initiative.

*Quellen: `projekt/Vorschlag-Rentnerausgleich-2026-10-18.md`; eigene Rechnungen altlasten, sozialschutz, netz33, haushalte33, rentnerausgleich.*

---

### v4.12 — Externe Prüfung vom 19.10.2026: Stellungnahme, Empfindlichkeit der Weitergabe; Korrektur 66 (Einstiegsdokumente)

**Art der Änderung: PATCH (Dokumentation, Prüfrechnung), keine Zahl der Rechnung bewegt.** 20. Oktober 2026.

**Anlass:** Eine dritte Instanz prüfte Webseite und Repository am 19.10.2026 und reichte eine Analyse ein (volkswirtschaftlich, sozial,
politisch; Repo-Audit; Gegenentwurf „Regelwerk statt Dach“). Stellungnahme: `projekt/Stellungnahme-Pruefung-2026-10-20.md`.

**Neu:** `modell/weitergabe_sensitivitaet.py` (+ `.toml`) → `daten/aggregate/weitergabe_sensitivitaet.json`. DE 2028, mehr im Monat, alleinstehend
20.000 / 42.000 / 75.000 €:

| Weitergabe | 0 % | 50 % | 80 % (Beschluss) | 100 % |
|---|---|---|---|---|
| alleinstehend | +167/+250/+149 | +290/+470/+532 | +362/+602/+763 | +410/+691/+917 |
| DE Beschäftigte mit mehr (min. über Haushaltstypen) | 84 % | 84 % | 98 % | 98 % |
| FR / ES mit mehr (min.) | 38 / 53 % | 58 / 98 % | 73 / 100 % | 73 / 100 % |

Befund: In Deutschland hängt die Größe des Vorteils an der Weitergabe, nicht sein Vorzeichen (auch ohne Weitergabe +149 bis +433 €, weil die
eigenen Beiträge entfallen). In Frankreich und Spanien trägt das Ergebnis ohne Weitergabe nicht. Nicht gegengerechnet: höhere Gewinne bei
geringer Weitergabe erhöhen das Aufkommen (33 %).

**Korrektur 66:** README, INDEX, AGENTS, DATENZUGANG und CLAUDE.md nannten bis v4.11 die 28:28-Gesamtrechnung (Stand B, `gesamtrechnung.py`)
als geltend; das Drittel-System (Stand C, seit v3.43) war in den Einstiegsdokumenten nicht verzeichnet. Die externe Prüfung schloss daraus,
die Webseitenfassung sei im Repository nicht enthalten, und prüfte den Vorläufer. Einstiegsdokumente berichtigt: Abschnitt „Aktueller Stand“
im README mit Skriptkarte. **Wodurch aufgefallen:** externe Prüfung.

**Offen (aus der Prüfung übernommen):** Durchsetzung der Weitergabe (Tarifbindung, Übergangsregel, Nachweis); Niveau des starken Netzes auf
der Seite beziffern; Ausweichreaktionen bei Vermögen und Erbschaft; Preisniveauschub der Mehrwertsteuer; Handelsrecht der Besteuerung am
Kundenort (WTO, Doppelbesteuerungsabkommen); Label-Zuordnung gegen Lobbydruck; Verfassungs- und Vertragsrecht; Gegenentwurf
„Regelwerk statt Dach“ als Architekturvariante prüfen.

*Quellen: Prüfbericht vom 19.10.2026 (nicht im Repository; Literaturangaben dort, an der Quelle zu prüfen); eigene Rechnungen.*

---

### v4.13 — Beschlüsse zur Prüfung: Weitergabe per Gesetz bis zum Stichtag, Netzniveau auf der Seite, Variante „Regelwerk statt Dach“, Rückmeldung

**Art der Änderung: PATCH (Beschluss, Texte), keine Zahl der Rechnung bewegt.** 20. Oktober 2026.

**Beschluss der Initiative (20.10.2026):**
1. Die Weitergabe wird so durchgesetzt, dass eine gesetzliche Vorgabe die Anpassung der Arbeitsverträge bis zum Stichtag der Einführung
   festlegt.
2. Das Netzniveau kommt auf die Seite.
3. Der Gegenentwurf wird als Variante ausgearbeitet.
4. Rückmeldung an die prüfende Instanz.

**Umgesetzt:**
- **Seite (sechs Sprachen):**
  - Die Karte „Arbeit“ nennt die gesetzliche Vertragsanpassung bis zum Stichtag.
  - Die Karte „Das starke Netz“ nennt das Grundauskommen je Land, Alleinstehende / Paar mit zwei Kindern, und die Netzkosten in % BIP 2028:
    DE 1.029 / 2.675 €, 9,6 %; FR 971 / 2.525 €, 11,5 %; PL 2.819 / 7.330 zł, 8,1 %.
  - Englische Fassung: Beispiel Deutschland.
- **Konzept:** Die Weitergaberegel ist mit Durchsetzung und Empfindlichkeit beschrieben; in „Was noch offen ist“ stehen Nachweis, Sanktion,
  neue Verträge nach dem Stichtag und die Architekturvariante.
- **Neu:** `projekt/Variante-Regelwerk-statt-Dach-2026-10-20.md` (Text, keine Rechnung) und `projekt/Rueckmeldung-Pruefung-2026-10-20.md`
  (Entwurf, keine Personennamen).

**Hinweis zur Weitergabe:** Das Gesetz sichert die Weitergabe zum Stichtag (neuer Bruttolohn = bisheriger Bruttolohn + mindestens 80 % des
bisherigen Arbeitgeberbeitrags). Wie sich die Löhne danach entwickeln, entscheidet der Arbeitsmarkt. Die Inzidenzforschung ist uneinheitlich;
die Empfindlichkeitsrechnung (v4.12) bleibt deshalb maßgeblich für die Spannweite.

**Offen:** Nachweis und Sanktion, Behandlung neuer Verträge nach dem Stichtag; Entscheidung zur Architekturvariante; Versand der Rückmeldung
(durch die Initiative). **Wodurch aufgefallen:** Beschluss der Initiative zur externen Prüfung.

---

### v4.14 — Zweite externe Prüfung (Stand C): Glossar der Kennzahlen, vergleichbare Gesamtlast, Rentenkürzung auf der Seite; Korrektur 67

**Art der Änderung: PATCH (Dokumentation, Prüfrechnung, Texte), keine Zahl der geltenden Rechnung bewegt.** 20. Oktober 2026.

**Anlass:** Zweite Prüfung des Repositorys (Stand C, v4.13, Commit e3a7db8). Der Rechenkern ist unabhängig bestätigt: Haushaltsformeln auf
±14 € im Jahr, Fonds-Rekursion, Weitergabe-Empfindlichkeit, Grundauskommen, Netz, Polen. Der frühere Vorbehalt zum Altlastenfonds ist
zurückgenommen. Sechs neue Befunde B11–B16; Bewertung in `projekt/Stellungnahme-Pruefung2-2026-10-20.md`.

**Neu:**
- `KENNZAHLEN.md`: welche Zahl gilt (Dividendenpfade, Altlasten je Abgrenzung, Gesamtlast, Lohnbasis); im README verlinkt.
- `modell/gesamtlast33.py` (+ `.toml`) → `daten/aggregate/gesamtlast33.json`:

  | % BIP | 2028 | 2060 |
  |---|---|---|
  | Steuern + Fonds | 38,81 | 37,41 |
  | mit Pflichtvorsorge | 42,91 | 41,51 |
  | heute | 40,76 | |
  | ohne Fonds (Altlasten im selben Jahr) | 45,46 / 49,56 | |

- `projektion33.json` trägt einen Statusvermerk: Vorstufe, das Mindestniveau ist keine Zusage.
- Seite (sechs Sprachen), Abschnitt „Altlasten“: Rentenkürzung 7,5 % und Grundauskommen für kleine Renten benannt (B13).
- Konzept: Zeile „Pflichtzahlungen 2028“ in der Kurzfassung.
- Stellungnahme und Rückmeldung: Lohnbasis 63.288 € (OECD) ergänzt (B14).

**Korrektur 67:** Das Repository enthielt zwei Dividendenpfade (netz33: 373 €, projektion33: 296 € für 2028) und zwei Gesamtlasten
(systemvarianten: 45,46 % ohne Fonds), ohne zu kennzeichnen, welche gilt. Unsere Stellungnahme vom 20.10.2026 nannte Prozentwerte für
Vielfache des Durchschnittslohns ohne die Lohnbasis. Behoben durch `KENNZAHLEN.md`, den Statusvermerk und die ergänzten Texte.
**Wodurch aufgefallen:** zweite externe Prüfung (B12, B14, B15, B16).

**Bewertung B11:** Die Fondszahlen 6,65 / 20,3 / 196 % sind der eigene Fonds Frankreichs, auf der französischen Seite so benannt, also nicht
veraltet. Uneinheitlich ist aber, dass die deutsche Seite den gemeinsamen Fonds und die übrigen Länderseiten den eigenen Fonds zeigen.
Entscheidung offen.

**Offen:**
- B11-Entscheidung (eigener oder gemeinsamer Fonds auf allen Seiten);
- Rückfallregel und Monitoring der Weitergabe (Vorschlag der Prüfung);
- Rechnung zum Preisniveauschub (Überschlag 2,5 % auf mehrwertsteuerpflichtigen Konsum) und zu den Ausweichreaktionen;
- DBCFT-Literatur als Prüfrahmen;
- dritte Prüfung.

*Quellen: Prüfbericht vom 20.10.2026 (nicht im Repository); eigene Rechnungen gesamtlast33, regel_boden, netz33, altlasten.*

---

### v4.15 — Gemeinsame Aufgaben ohne eigene Steuer: Pflichtquote mit Kasse, Anrechnung und Rückfallregel

**Art der Änderung: MINOR (neue Prüfrechnung zur Architekturvariante), keine Zahl der geltenden Rechnung bewegt.** 20. Oktober 2026.

**Anlass:** Frage der Initiative, was in der Variante „Regelwerk statt Dach“ mit den übrigen gemeinsamen Aufgaben geschieht; Auftrag,
die Aufteilung zu rechnen. Beschluss: Der Verteidigungspfad bleibt bei 1,4 → 2,5 % BIP bis 2035.

**Neu:** `modell/dach_beitrag.py` (+ `.toml`) → `daten/aggregate/dach_beitrag.json`. Regel:
- Pflichtquote = Dach-Pfad (projektion33): 2028 6,19 %, ab 2035 7,29 % BIP;
- zwei Wege: gemeinsame Kasse oder angerechnete eigene Ausgabe;
- Rückfallregel: Wer weniger anrechenbar ausgibt, zahlt die Differenz in die Kasse;
- Obergrenze 32 % des Steueraufkommens.

| % BIP, Klub | 2028 | 2035 |
|---|---|---|
| Pflichtquote | 6,19 | 7,29 |
| gemeinsame Kasse | 2,65 | 3,09 |
| angerechnete eigene Ausgabe | 3,54 | 4,20 |
| Obergrenze (32 % der Steuern) | 10,73 | 10,57 |

**Datenquelle:**
- Aufgabenliste: `gesamtrechnung.json`, `tabelle_a`;
- Pfad: `projektion33.json`;
- BIP, Einwohner, COFOG GF02 2024: Eurostat über `modell/rechnungen/rahmen/daten.py`;
- EU-Eigenmittelobergrenze 1,40 % BNE: Europäische Kommission, Seite „Eigenmittelobergrenzen 2021–2027“, abgerufen am 20.10.2026.

**Kassenanteile je Aufgabe:** Annahmen der Initiative zur Größenordnung, keine abgeleiteten Werte.

**Bewegte Zahl:** keine der geltenden Rechnung. Neu ist die Kasse mit 2,65 % BIP 2028; für Deutschland sind das 130,2 Mrd € (nominal 2028), 130 € je Einwohner und Monat.

**Befunde:**
- **Größe der Kasse:** Sie ist 1,9- bis 2,2-mal so groß wie die EU-Obergrenze.
- **Irland:** Bei Bemessung am BIP zahlt Irland 261 € je Einwohner und Monat; Vorschlag ist die Bemessung am BNE.
- **Rückfallregel:** Bliebe die Verteidigung auf dem Stand von 2024, zahlten 2035 Irland 2,4 %, Österreich 1,8 % und Spanien 1,6 % BIP in die Kasse.

**Wodurch aufgefallen:** Rechnung zur Frage der Initiative.

**Offen:**
- Kassenanteile (Verhandlungsfrage);
- Bemessung am BNE;
- Anrechnung für neutrale Staaten;
- Entscheidung zur Architektur;
- Finanzverteilung innerhalb der Staaten (Länder, Regionen, Gemeinden; Art. 28 Abs. 2 und Art. 79 Abs. 3 GG), siehe N33.

*Quellen: eigene Rechnung dach_beitrag; Europäische Kommission (Eigenmittelobergrenzen); Eurostat gov_10a_exp 2024.*

---

### v4.16 — Kreisdaten Deutschland: Gemeindeformel je Kreis und Strukturzuschlag; Sicherheitskasse über einen Anteil der Mehrwertsteuer

**Art der Änderung: MINOR (neue Prüfrechnung, neue Daten), keine Zahl der geltenden Rechnung bewegt.** 20. Oktober 2026.

**Anlass:** Auftrag der Initiative, die Daten je Kreis einzusammeln. Dazu ihr Einwand, ein Beitragsmodell für Verteidigung und Souveränität
lasse Europa im Wettbewerb der Großmächte strukturell im Nachteil.

**Daten:** Eurostat, 400 Kreise (NUTS 2024):
- Einwohner, Menschen ab 65 und Kinder von 5 bis 19 Jahren (1.1.2024);
- Fläche (2023; Thüringen mit dem neuesten Jahr und den Codes nach NUTS 2024);
- BIP (2022, Mio. €).

Abgerufen am 20.10.2026 über das Web-Abrufwerkzeug (die Shell ist gesperrt) und maschinell aus der Abfrage gelesen; an der Quelle zu prüfen.
**Prüfung:** Die Summen je Bundesland stimmen bei allen sieben Dateien mit einem getrennten NUTS-1-Abruf überein (BIP auf ±0,6 Mio. €).
Rohdaten liegen in `daten/roh/kreise/` (nicht im Repository), die Abrufadressen in `modell/regionen_de.toml`.

**Nicht erreichbar:** heutige Gemeindeeinnahmen je Kreis. Regionalstatistik und INKAR verbieten den automatischen Abruf (robots.txt).

**Neu:**
- `modell/regionen_de.py` (+ `.toml`) → `daten/aggregate/regionen_de.json`:
  - Gemeindeformel (3.913 € je Einwohner, 13.729 € je Kind, Kaufkraft 2026) im Mittel 5.853 € je Einwohner und Jahr;
  - Spanne P90/P10 1,05 gegen 2,43 beim BIP je Einwohner;
  - Strukturzuschlag 10 % (Fläche, Menschen ab 65): dünn besiedelt 99,0 → 111,0; Ost 99,0 → 105,3; kreisfreie Städte 99,1 → 94,3 (Index).
- `modell/dach_beitrag.py` (v4.16): Wie viel der Mehrwertsteuer der gemeinsame Teil der Verteidigung braucht. 2035 sind das bei 40 / 50 / 60 / 100 % gemeinsam
  12,1 / 15,1 / 18,1 / 30,2 % der Mehrwertsteuer (8,28 % BIP).
- Architekturvariante, Abschnitt 7 (Sicherheitsunion mit eigener Einnahme, Vorschlag) und Abschnitt 8 (Regionen).

**Bewegte Zahl:** keine der geltenden Rechnung.

**Wodurch aufgefallen:** Einwand der Initiative (Verteidigung) und offener Punkt N33 (Regionen).

**Offen:**
- Gemeindeeinnahmen je Kreis heute (CSV-Datei der Initiative);
- Strukturzuschlag entscheiden;
- Anteil der Sicherheitskasse entscheiden;
- Rechtsprüfung (Art. 23, 24, 28, 79 GG; Art. 42 EUV);
- nukleare Abschreckung.

*Quellen: Eurostat demo_r_pjanaggr3, demo_r_pjangrp3, reg_area3, nama_10r_3gdp; Rat der EU, Seite zu SAFE (abgerufen 20.10.2026); Art. 28 GG (gesetze-im-internet.de).*

---

### v4.17 — B11 entschieden: gemeinsamer Altlastenfonds auf allen Länderseiten, eigener Fonds als Vergleich

**Art der Änderung: MINOR (Beschluss, geltende Länderrechnungen bewegt).** 20. Oktober 2026.

**Anlass:** Prüfbericht B11 (zusammengefasster Bericht vom 20.10.2026). Bis v4.16 zeigte die deutsche Seite den gemeinsamen Fonds, die Seiten
FR, IT, ES und PL den eigenen Fonds je Staat. **Beschluss der Initiative (20.10.2026): gemeinsamer Fonds überall.**

**Änderung:**
- `modell/laenderseiten.py`: `staaten.*.fonds` ist jetzt der gemeinsame Fonds (Beschluss: 5,28 % BIP, Zuschlag 15,8 %, Spitze 149,6 % 2056,
  getilgt 2098), dazu die Verrechnung 2028, wo der Staat zu den zehn gerechneten gehört.
- Der eigene Fonds je Staat steht als Vergleich unter `fonds_eigen`.
- Alle Haushaltsrechnungen der Länder nutzen damit den Zuschlag 15,8 %.
- `zerlegung_laender.py` rechnet die Zinsempfindlichkeit weiter am eigenen Fonds.
- Seite (FR, IT, ES, PL): Der Abschnitt zu den Altlasten nennt den gemeinsamen Fonds und „allein trüge …“. Italien und Polen tragen den Hinweis, dass sie nicht zu den zehn gerechneten Staaten gehören.

**Datenquelle:** `altlasten.json` (Beschluss v3.46/v4.11), `laenderseiten.json`.

**Bewegte Zahlen** (Zuschlag eigener Fonds → gemeinsamer Fonds; Beispiel brutto im Monat; Gini 2028, Mitte):

| | Zuschlag | Beispiel | zweites Beispiel | Gini |
|---|---|---|---|---|
| FR | 20,3 → 15,8 % | 30.000 €: +174 → +211 € | 45.000 €: +412 → +482 € | 32,2 → 32,6 |
| IT | 20,7 → 15,8 % | 24.000 €: +371 → +407 € | +447 → +508 € | 28,5 → 29,0 |
| ES | 16,5 → 15,8 % | 21.000 €: +340 → +344 € | +376 → +384 € | 25,1 (unverändert) |
| PL | 12,7 → 15,8 % | 64.000 zł: +1.557 → +1.506 zł | +1.525 → +1.437 zł | 19,1 → 18,9 |

- Die Anteile mit mehr bleiben nahezu gleich (FR 20–36 %). Mit dem Grundauskommen hat in Frankreich der Fall „alleinerziehend, 1 Kind“ jetzt 100 statt 73 %, in Polen der Fall „Paar, 2 Kinder“ 98 statt 100 %.
- Der Gini steigt in FR und IT leicht, weil der Zuschlag auf die Steuerschuld progressiv wirkt und kleiner wird.
- Deutschland ist unverändert.

**Vorbehalt:** Italien und Polen sind nicht unter den zehn Staaten, für die der gemeinsame Fonds gerechnet ist. Mit ihrem Beitritt änderte sich
der gemeinsame Satz; das ist nicht gerechnet, Italien würde ihn eher erhöhen (eigener Fonds 20,7 %).

**Wodurch aufgefallen:** Prüfbericht B11; Nahtstelle N31.

*Quellen: eigene Rechnung; Prüfbericht Kulturverein Ribbeck e.V., 20.10.2026 (nicht im Repository).*

---

### v4.18 — Prüfbericht (zusammengefasst): Rückfallregel der Weitergabe, Preisniveauschub, Ausweichreaktionen; Mikrosimulation bewertet

**Art der Änderung: MINOR (drei neue Prüfrechnungen, Texte), keine Zahl der geltenden Rechnung bewegt.** 20. Oktober 2026.

**Anlass:** Zusammengefasster Prüfbericht des Kulturvereins Ribbeck e.V. (zwei Prüfungen und Mikrosimulation, 20.10.2026). Bewertung in
`projekt/Stellungnahme-Pruefung3-2026-10-20.md`. Abgearbeitet wurde nach den Vorschlägen der Stellungnahme vom 20.10.2026.

**Neu:**
- `modell/weitergabe_rueckfall.py` (+ `.toml`): Arbeitgeberbeiträge DE 7,9 bis 9,4 % BIP (Eurostat nama_10_gdp D12 und D11, 2024). Bei
  tatsächlicher Weitergabe von 50 % fließen 2,4 bis 2,8 % BIP an den Fonds (45 bis 53 % des Fondsbeitrags).
- `modell/preisniveau33.py` (+ `.toml`): Preisniveauschub 2028 +1,2 bis +2,1 %, mechanisch +2,47 % bei einem effektiven Satz von 15,97 → 18,84 %.
  Annahmen: Überwälzung 0,73 bis 1,0; Anteil des Konsums mit Mehrwertsteuer 0,67 bis 0,84 (D211 / 15,97 % / P31_S14).
  Mit halber Weitergabe der Arbeitskostensenkung netto +0,3 bis +1,3 %; bis 2060 sinkt der Schub auf +0,8 bis +1,3 %.
- `modell/ausweichen33.py` (+ `.toml`): Erbschaft (1,16 % BIP) und große Vermögen (0,97 %). Im ungünstigen Fall fehlen 1,06 % BIP, die
  Dividende sinkt um 55 € (2028) und um 75 € (2060: 164 statt 239 €).
- Texte:
  - Seite (sechs Sprachen) und Konzept nennen Monitoring und Rückfallregel.
  - Das Konzept (Fassung 4.18, Abschnitt 8) nennt Preisniveauschub und Ausweichreaktionen.
  - `KENNZAHLEN.md` ist ergänzt.
- Mikrosimulation des Prüfers: Sie stützt die Aussage „9 von 10“ für Vollzeitbeschäftigte (99,7 %, ohne Weitergabe 91,6 %).
  - Grenzen: 373 € statt 354/283 €; nur Vollzeit; heute ohne Bedarfsleistungen und neu ohne Grundauskommen.
  - Die Ergebnisdatei im Schnittstellenformat ist erbeten.

**Datenquelle:**
- Eurostat nama_10_gdp (D11, D12, B1GQ, P31_S14) und gov_10a_taxag (D211), DE 2024, abgerufen am 20.10.2026 über das Web-Abrufwerkzeug;
- Carare und Danninger (2008, IMF WP 08/175);
- Benzarti, Carloni, Harju, Kosonen (2020, JPE);
- Fuest, Neumeier, Stöhlker (ifo 2020);
- Brülhart, Gruber, Krapf, Schmidheiny (2022, AEJ: Policy);
- Jakobsen, Jakobsen, Kleven, Zucman (2020, QJE);
- Goupille-Lebret und Infante (2018, JPubE).

Alle Literaturangaben sind nur aus den Abstracts gelesen.

**Bewegte Zahl:** keine der geltenden Rechnung.

**Wodurch aufgefallen:** Prüfbericht (dringendste offene Punkte: Preisniveau, Ausweichen), Befund B14 (Rückfallregel).

**Korrektur 68:** In v4.15 bis v4.17 blieb der Modellstand in `parameter.toml`, README, INDEX und Band III auf v4.14 stehen; das Upload-Paket trug deshalb den Namen v4.14. Behoben: alle auf v4.18, README-Karte um die neuen Skripte ergänzt. **Wodurch aufgefallen:** Paketname beim Bau, danach Projektprüfung (Modellstand uneinheitlich).

**Offen:**
- Zweitrundeneffekte und CO₂-Preispfad im Preisniveau;
- Ausweichen mit Verteilungsdaten statt Annahmen;
- DBCFT-Prüfrahmen;
- Ergebnisdatei der Mikrosimulation;
- dritte Prüfung.

---

### v4.19 — Prüfung offener Punkte: Fondszins gegen Marktrenditen, gemeinsamer Fonds mit Italien und Polen, Wertungen der Seite

**Art der Änderung: MINOR (zwei neue Prüfrechnungen, Texte), keine Zahl der geltenden Rechnung bewegt.** 21. Oktober 2026.

**Anlass:** Auftrag der Initiative, die offenen Punkte weiter zu prüfen (21.10.2026).

**1. Fondszins** (`modell/fondszins.py` + `.toml`):
- Der Beschluss rechnet mit 2,5 % („Setzung“, Garantiezins der Gesamtrechnung) bei 3 % nominalem Wachstum.
- Marktrenditen 10 Jahre im Oktober 2026: Bundesanleihen 3,46 % (Trading Economics), EU-Anleihen 3,95 % (bondScovery, geschätzte Kurve). Beides sind Sekundärquellen, an Bundesbank- oder EZB-Daten zu prüfen.
- Der Zins liegt damit über dem Wachstum, die Schuld schmilzt nicht von selbst.

| Fondszins | Beitrag % BIP | Zuschlag | Spitze | DE, alleinstehend, 42.000 € |
|---|---|---|---|---|
| 2,5 % (Beschluss) | 5,28 | 15,8 % | 149,6 % (2056) | +602 € |
| 3,0 % | 5,80 | 17,4 % | 151,9 % | +581 € |
| 3,5 % | 6,34 | 19,0 % | 153,8 % | +560 € |
| 4,0 % | 6,90 | 20,7 % | 155,3 % | +537 € |
| Übergang 2,22 → 3,5 % (7,5 Jahre) | 6,27 | 18,8 % | 151,0 % | +562 € |

- Der Anteil mit mehr bleibt bei 98 %.
- Gemeinsame Anleihen rentieren derzeit über Bundesanleihen. Billiger als heute ist der Fonds für Frankreich (4,79 %) und Italien, nicht für Deutschland.

**2. Gemeinsamer Fonds mit Italien und Polen** (`modell/fonds_klub.py`):
- Methode: Bei gleichem Zins und Wachstum ist die Rekursion linear; der gemeinsame Beitrag ist das BIP-gewichtete Mittel der eigenen Beiträge (Abgrenzung Möglichkeitsraum). Das Ergebnis ist auf den Beschluss skaliert (Annahme).
- Gemeinsamer Satz: mit Italien 16,8 %, mit Polen 15,6 %, mit beiden 16,6 %, mit allen 30 Staaten 15,5 % (Beschluss mit zehn Staaten: 15,8 %).
- Der auf den Seiten IT und PL genutzte Satz liegt damit innerhalb von einem Punkt.

**3. Wertungen der Seite** (sechs Sprachen):
- „kann viel günstiger finanziert werden … moderater Zuschlag“ ist ersetzt durch den Zuschlag mit Zinsannahme und den Wert bei Marktzinsen. Grund: Die eigenen Fonds sind schon mit 2,5 % gerechnet, und gemeinsame Anleihen sind derzeit nicht günstiger als Bundesanleihen.
- Gestrichen sind „zukunftsfähiger aufgestellt“ (unbelegt) und „macht den Klub stärker“ (jetzt: „vergrößert den Klub“; mit Italien steigt der gemeinsame Satz).
- Konzept (Fassung 4.19), Abschnitt 8: Zins und Abgrenzung ergänzt.

**Datenquelle:**
- Trading Economics und bondScovery (abgerufen 21.10.2026, Sekundärquellen);
- `altlasten.py` (gleiche Rekursion, Abgleich 5,28 % exakt);
- `moeglichkeitsraum33.json`.

**Bewegte Zahl:** keine der geltenden Rechnung.

**Wodurch aufgefallen:** Prüfung der Setzung „Garantiezins 2,5 %“ und der Wertungen (offen seit v3.57).

**Offen:**
- Zinsannahme entscheiden (N35);
- Abgrenzung des gemeinsamen Fonds (zehn, zwölf oder 30 Staaten);
- Marktzinsen an amtlicher Quelle prüfen.

---

### v4.20 — Beschlüsse: Fondszins = Mittel der vergangenen 20 Jahre (2,45 %), gemeinsamer Fonds der 30 Staaten

**Art der Änderung: MINOR (Beschluss, geltende Zahlen bewegt).** 21. Oktober 2026.

**Anlass:** Entscheidungen der Initiative zu den offenen Punkten aus v4.19 (N35 und Abgrenzung des Fonds):
1. Fondszins = Durchschnitt der vergangenen 20 Jahre;
2. der gemeinsame Fonds umfasst alle 30 Staaten.

**Umsetzung:**
- **Zins:** Mittel der Renditen zehnjähriger Staatsanleihen im Euroraum 2006–2025 nach dem Konvergenzkriterium (Eurostat irt_lt_mcby_a, geo EA) = **2,45 %**; Deutschland zum Vergleich 1,87 %.
  - Reihe in `altlasten.toml` (`zins_reihe_ea`, `zins_reihe_de`), maschinell aus der Abfrage gelesen.
  - `altlasten.py` prüft, dass der Beschlusszins dem Mittel entspricht.
  - `moeglichkeitsraum33.toml` hat denselben Zins.
- **30 Staaten:** `modell/fonds_klub.py` schreibt `daten/aggregate/fonds_geltend.json`. Methode: Beschluss der zehn (Rentnerpaket, Startschuld 2028) × Verhältnis 30/10 aus dem Möglichkeitsraum (lineare Rekursion, Annahme: Abgrenzung wirkt gleich).
  - Schuldenpfad der 30: Niveau skaliert.
  - Haushalte (DE und Länder), Rentner, Gesamtlast, Rückfallregel, Länderseiten, Seite und Konzept lesen jetzt `fonds_geltend.json`.
  - Die Verrechnung je Staat und die Einwanderungs- und Dynamikrechnungen bleiben bei den zehn.
  - Stufenfolge in `alles.py`: `fonds_klub` direkt nach dem Möglichkeitsraum, `haushalte33` danach.
- **Texte:**
  - Seite (sechs Sprachen) nennt den Fonds der 30 Staaten und den Zins „Mittel der vergangenen 20 Jahre“; die Hinweise „Italien/Polen nicht unter den zehn“ sind gestrichen.
  - Konzept Fassung 4.20 (Tabelle, Anmerkungen, Abschnitt 8); der Wert 42.000 € in der Weitergabe-Zeile wird jetzt aus der Rechnung gelesen.

**Bewegte Zahlen:**

| | vorher (zehn, 2,5 %) | jetzt (30, 2,45 %) |
|---|---|---|
| Fondsbeitrag | 5,28 % BIP | **5,14 % BIP** |
| Zuschlag auf alle Steuern | 15,8 % | **15,4 %** |
| Schuldenspitze | 149,6 % (2056) | **147,3 % (2055)** |
| Gesamtlast 2028 (mit Pflichtvorsorge) | 38,81 % (42,91 %) | **38,67 % (42,77 %)** |
| DE alleinstehend, 42.000 € | +602 € | **+608 €** |
| DE ohne Weitergabe, 42.000 € | +250 € | +254 € |
| Beispiele FR / IT / ES / PL | +211 € / +407 € / +344 € / +1.506 zł | +214 € / +410 € / +346 € / +1.513 zł |
| Bestandsrenten | −33 bis −54 € | −32 bis −54 € |
| Gini 2028 | FR 32,6, ES 25,1 | FR 32,7, ES 25,2 |

- Bei Marktzins 3,5 / 4 % (Risiko): Zuschlag 18,6 / 20,3 %, DE 42.000 € +565 / +542 €.
- Nur zehn Staaten bei 2,45 %: 5,23 % BIP / 15,7 %.
- Eigene Fonds je Land (Vergleich): DE 14,0 %, FR 20,1 %, IT 20,5 %, ES 16,3 %, PL 12,5 %.
- Anteile mit mehr unverändert.

**Datenquelle:** Eurostat irt_lt_mcby_a (EA, DE), 2006–2025, abgerufen 21.10.2026; `moeglichkeitsraum33.json`; `altlasten.py`.

**Wodurch aufgefallen:** Prüfung der Setzung 2,5 % (v4.19), Beschluss der Initiative.

**Offen:**
- Verrechnung je Staat für die 30 rechnen;
- Einwanderung und Dynamik auf den Fonds der 30 umstellen;
- 30-Staaten-Fonds direkt statt über das Verhältnis rechnen (Altrenten aller 30 im Sozialschutzmodell).

---

### v4.21 — Mikrosimulation des Prüfers übernommen (beitraege/kvribbeck-2028); Schnittstelle auf Stand C; Korrektur 69

**Art der Änderung: MINOR (externer Beitrag, Schnittstelle), Beispielhaushalte in haushalte33 bewegt.** 21. Oktober 2026.

**Anlass:** Der Kulturverein Ribbeck e.V. hat die erbetene Ergebnisdatei der Mikrosimulation geliefert, als Issue-Text, weil der Zugang nur Leserechte hat. Dazu kamen drei Hinweise zum Repository.

**Neu:**
- `beitraege/kvribbeck-2028/ergebnis.csv` (245 Zeilen, übernommen aus dem Issue-Text) und `LIESMICH.md` (Entwurf des Prüfers).
  - Formprüfung: in Ordnung.
  - Ergebnis, Anteil der Vollzeitbeschäftigten mit mehr: Beschluss 99,0 % (Monte-Carlo-Band 98,9–99,0), Vergleichsvorsorge 97,7 %, halbe Weitergabe 98,4 %, ohne Weitergabe 92,0 %.
  - Oberstes Dezil ohne Weitergabe: 47,1 % mit mehr, Median −0,2 %.
  - Haushalte mit Kindern: 98,4 %.
  - Gerechnet mit 354/283 €, Zuschlag 15,8 % (v4.18) und effektivem Satz 18,84 %.
  - Grenzen: nur Vollzeit; heute ohne Bedarfsleistungen, neu ohne Grundauskommen; Haushaltsstruktur angenommen.
  - Einordnung: externe Rechnung, eine Quelle; als zweite Stütze der Aussage „9 von 10“ im Konzept (Abschnitt 8) und in `KENNZAHLEN.md` genannt.
- Hinweis 1: `schnittstelle/pruefe_beitrag.py` akzeptiert „Stand C“ und die Ländercodes der 30 Staaten; das Schema ist angepasst.
- Hinweis 3: `schnittstelle/MIKROSIMULATION.md` ist neu gefasst für Stand C (Bausteine mit Quelle im Repository).

**Korrektur 69 (Hinweis 2):** `modell/haushalte33.py` rechnete seit v4.5 weiter mit 373 € je Erwachsenem und Kindern zur Hälfte statt mit
dem Kinderanteil 0,8 bei gleichem Topf (354 / 283 €).
- Betroffen waren die Beispielhaushalte in `haushalte33.json` und die Prüfung der Aussage „9 von 10“ auf der Seite.
- Nicht betroffen waren der Rechner der Seite (nutzt den Topf-Faktor) und die Haushaltszahlen aus `regel_boden`.

Bewegte Zahlen (DE, 2028, Weitergabe 80 %, Pflichtvorsorge, Zuschlag 15,4 %, im Monat):

| Haushalt | 42.000 € brutto |
|---|---|
| alleinstehend | +619 → +608 € |
| alleinerziehend, 1 Kind | +526 → +607 € |
| Paar, ein Einkommen, 2 Kinder | +516 → +673 € |

- Beim Paar mit 150.000 €: −192 → −35 €.
- Anteile mit mehr: alleinerziehend 97,8 → 100 %.
- `haushalte33` und `regel_boden` stimmen bei 42.000 € jetzt überein (608 €).

**Wodurch aufgefallen:** Prüfer (Hinweis 2 im Issue-Text vom 21.10.2026).

**Datenquelle:** Beitrag kvribbeck-2028 (Verdiensterhebung 2024 und Mikrozensus 2024 des Statistischen Bundesamts als Eichung, nach Angabe des Prüfers).

**Offen:**
- Rechenweg-Skript des Prüfers (angekündigt);
- Schreibrechte für den Prüfer (Entscheidung der Initiative);
- Mikrosimulation mit Teilzeit, Bedarfsleistungen und Grundauskommen.

### v4.22 — Eigene synthetische Mikrosimulation Deutschland, Stufe 1 (modell/mikro_de.py)

**Art der Änderung: MINOR (neue Prüfrechnung), keine geltende Zahl bewegt.** 21. Oktober 2026.

**Anlass:** Beschluss der Initiative vom 21.10.2026, dem Vorgehen des Prüfers zu folgen und eine eigene, auf veröffentlichte Eckwerte
geeichte Population zu rechnen, die über die Vollzeitbeschäftigten hinaus Teilzeit, Minijobs, Bürgergeld, Familien und Rentner umfasst.

**Methode:**
- 40.000 Haushalte erwerbsfähigen Alters und 8.000 Rentnerhaushalte je Ziehung, fünf Ziehungen mit festen Startwerten.
- Eichung (exponentielles Raking) auf: Haushalte je Typ, Bedarfsgemeinschaften ohne Erwerb, 24,02 Mio. Vollzeit- und 10,97 Mio.
  Teilzeitbeschäftigte (Destatis, 31.12.2025), 2,71 Mio. ausschließlich geringfügig Beschäftigte unter 65 (BA, 31.12.2025),
  14,02 Mio. minderjährige und 3,55 Mio. volljährige Kindergeldkinder (BA Familienkasse, Dez. 2025). Restfehler < 10⁻⁹.
- Löhne: Vollzeit nach den Perzentilen der PM 134 (Destatis, 2024), P90–P99 Pareto-Interpolation, Spitze über P99 auf das Mittel 62.235 €
  geeicht (Alpha 2,83); Teilzeit lognormal um 2.517 €/Monat (Verdiensterhebung April 2025; Streuung 0,55 Annahme); Minijob gleichverteilt (Annahme).
- Partnerlöhne mit Rangkorrelation 0 / 0,3 / 0,5 (Gauß-Copula); Renten lognormal auf Zahlbetrag 1.154 € und Anteil unter 1.000 € von 42 %
  (Sekundärquelle) geeicht.
- heute: Recht 2026 mit Splitting beider Partnereinkommen, Midijob-Bereich genähert, Bürgergeld nach `sozial_laender` (volle
  Inanspruchnahme); neu: `regel_boden` (33R, Dividende 354/283 €, Grundauskommen mit Halbanrechnung, Pflichtvorsorge), Rentner nach
  `rentnerausgleich`. Gegenprobe gegen `regel_boden.neu` und `sozial_laender.heute` für Einverdienerhaushalte: Abweichung 0,0 €.

**Validierung an nicht geeichten Aggregaten 2025:**

| Größe | Modell | amtlich | Abweichung |
|---|---|---|---|
| Bruttolöhne und -gehälter (mit Beamten und Nebenjob-Minijobs als Annahme) | 1.961 Mrd. € | 2.026,5 Mrd. € (Eurostat D11, vorläufig) | −3,2 % |
| Lohnsteuer (mit Beamten als Annahme) gegen kassenmäßige Lohnsteuer + Kindergeld | 302,6 Mrd. € | 262,7 + 55,3 = 318,0 Mrd. € | −4,8 % |
| Grundsicherung im Alter, Fälle | 10,5 Mio. | 0,76 Mio. (Sekundärquelle) | **nicht bestanden** |
| Bürgergeld-Anspruch, Haushalte (Näherung einschließlich Wohngeld/Kinderzuschlag) | 4,65 Mio. | rund 3,1 Mio. Bedarfsgemeinschaften (abgeleitet, Annahme) | zu hoch (volle Inanspruchnahme) |

- Die Lohnsteuer liegt unter dem Ziel, obwohl Pensionen und Betriebsrenten fehlen; Tarif 2026 statt 2025 erklärt einen Teil.
- Die Buchung des Kindergeldes als Abzug von der kassenmäßigen Lohnsteuer ist eine Annahme, an der Quelle zu prüfen.
- Rentner: Die Verteilung gilt je Rente, nicht je Haushalt; Partnereinkommen, Hinterbliebenen- und Betriebsrenten fehlen. Die Kosten der
  Böden für Rentner (heute 59,8 Mrd. €, neu 52,7 Mrd. €) sind deshalb nicht belastbar. Das Vorzeichen für Rentner hängt daran nicht:
  Über dem Boden wirkt die Kürzung um 7,5 %, unter dem Boden liegt das Grundauskommen (1.029 €) unter der Grundsicherung (1.083 €).

**Ergebnis (DE, 2028, Kaufkraft 2026, Weitergabe 80 %, Ziehung 1; Spanne der fünf Ziehungen in Klammern):**

| Gruppe | Haushalte mit mehr | Mittel im Monat |
|---|---|---|
| Hauptperson Vollzeit (16,5 Mio. Haushalte) | 99,3 % (99,3–99,4) | +1.018 € |
| Hauptperson Teilzeit (5,0 Mio.) | 99,8 % (99,8) | +744 € |
| Hauptperson Minijob (1,0 Mio.) | 47,6 % | +225 € (Median −5 €) |
| Bürgergeld ohne Erwerb (2,4 Mio.) | 14,7 % | −45 € |
| Rentnerhaushalte (12,2 Mio.) | 0 % | −96 € (allein −64 €, Paar −130 €) |
| alle Haushalte erwerbsfähigen Alters | 89,2 % | |
| alle Haushalte (37,1 Mio.) / Personen | 59,9 % / 70,7 % | +530 € |

- Weitergabe 0 / 50 / 100 %: Vollzeit 93,8 / 98,8 / 99,7 %; erwerbsfähige Haushalte 83,8 / 88,4 / 89,8 %.
- Vergleich mit dem Beitrag kvribbeck-2028 (nur Vollzeit, Personen): 92,0 / 98,4 / 99,0 % – die Rechnungen stützen sich gegenseitig, sind aber
  nicht unabhängig (gleiche Formeln des Repositorys, ähnliche Eichquellen).
- Dezile (Personen, heutiges Äquivalenzeinkommen): D1 0 %, D2 57 %, D3 48 %, D4 68 %, D5 79 %, D6–D10 86–94 %.
- Partnerkorrelation 0 / 0,3 / 0,5 und Haushaltsanteile ±15 %: Gesamtanteil 59,6–60,0 %, praktisch ohne Wirkung.
- Grundauskommen erwerbsfähige Haushalte: 32,3 Mrd. € (ohne Erwerb 24,2, mit Erwerb 8,1); liegt im oberen Bereich der Schätzung aus
  `boden_kosten` (9,7–35,8 Mrd. €). Rentner siehe oben.

**Bewertung:** Die Aussage „9 von 10 Beschäftigten haben mehr“ hält auch mit Teilzeit, Paaren mit zwei Einkommen und Bedarfsleistungen.
Für die Gesamtbevölkerung gilt sie nicht: Rentnerhaushalte und Bürgergeldhaushalte ohne Erwerb verlieren im Mittel 45 bis 130 € im Monat.
Die Seite spricht von Beschäftigten; eine Aussage über „die Haushalte“ wäre nicht gedeckt. Die Spanne der Ziehungen (unter 0,5 Punkten)
misst nur das Rauschen der Ziehung, nicht die Unsicherheit der Annahmen.

**Datenquellen:** Destatis PM 134 (08.04.2025), Verdiensterhebung April 2025, Strukturdaten Beschäftigte 31.12.2025, Haushalte und Familien
(Mikrozensus); BA Familienkasse Jahreszahlen 2025 (PDF, maschinell gelesen, an der Quelle zu prüfen) und Pressemitteilung 21.01.2026; BA
Geringfügige Beschäftigung 31.12.2025; BA Strukturen der Grundsicherung 2025 über sozialpolitik-aktuell.de (Sekundärquelle); DRV
Jahresbericht 2025; Eurostat nama_10_gdp (D11 2024/2025); BMF-Monatsbericht Dezember 2025 (Werte aus `modell/audit/a1_kalibrierung.py`).

**Wodurch aufgefallen:** Vorschlag des Prüfers (synthetische Population mit kleiner Fehlervarianz), Beschluss der Initiative.

**Offen (Stufe 2):** Haushaltseinkommen der Rentner (Alterssicherungsbericht/ASID oder EU-SILC-Aggregate) statt Rentenverteilung; Teilzeit-
Dezile; Selbständige und Beamte; Nicht-Inanspruchnahme; Rentner mit Minijob; amtliche Haushaltszahlen nach Erwerbsstatus (Mikrozensus).

### v4.23 — Mikrosimulation Stufe 2: Rentnerhaushalte mit Haushaltseinkommen (modell/mikro_rentner_de.py)

**Art der Änderung: MINOR (Prüfrechnung verbessert), keine geltende Zahl bewegt; Aussage zu Rentnern im Konzept präzisiert.** 21. Oktober 2026.

**Anlass:** v4.22 bestand die Prüfung an der Grundsicherung im Alter nicht (10,5 Mio. Fälle statt 0,76 Mio.), weil Renten je Rente gezogen
wurden. Auftrag der Initiative vom 21.10.2026: Rentner mit Haushaltseinkommen rechnen.

**Methode:**
- Äquivalenzgewichtetes Nettoeinkommen der Personen ab 65 aus EU-SILC 2025 (Einkommen 2024, Eurostat, amtlich):
  - Median 24.940 €, Mittel 28.780 € (ilc_di03);
  - Anteile unter 40 / 50 / 60 / 70 % des Gesamtmedians 28.891 €: 4,4 / 10,9 / 19,5 / 31,1 % (ilc_li02).
  - Zwischen den Stützstellen linear, über dem Median lognormal (Streuung 0,51, so dass das Mittel getroffen wird).
  - Allein Lebende und Paare verschoben auf die Armutsgefährdungsquoten 30,0 / 14,3 % (ilc_li03).
- Einkommensarten nach dem Alterssicherungsbericht 2024 (ASID 2023, Sekundärquelle sozialpolitik-aktuell):
  GRV 53 %, andere Systeme 17 %, Betriebsrente 7 %, privat 9 %, Erwerb 13 %.
  - Annahme: gleiche Anteile über alle Einkommen; Variante „nur GRV“ als Schranke.
  - Das Brutto wird aus dem Netto nach Recht 2026 zurückgerechnet (Krankenversicherung je Art als Annahme).
- neu: Renten aus GRV und anderen Systemen um 7,5 % gekürzt (Annahme: Beamtenversorgung gleich), keine Kassenbeiträge, alles nach 33R
  steuerpflichtig, Mehrwertsteuer und Zuschlag, keine zusätzliche Dividende, Grundauskommen je Haushalt (1 / 1,5) mit voller Anrechnung.
- heute: Variante „voll“ (Grundsicherung für alle Berechtigten) und „beobachtet“ (Einkommen wie in EU-SILC).

**Prüfwerte ohne Eichung:**

| Größe | Modell | Vergleich | Befund |
|---|---|---|---|
| Netto je Rentnerhaushalt 2023 | 2.888 € | ASID 2023: 2.769 € | +4 % (Abgrenzung abweichend) |
| GRV brutto je Person ab 65 | 1.311 € | DRV: Zahlbetrag 1.154 € / (1 − 12,35 %) ≈ 1.317 € (2024) | passt; der DRV-Wert ist eine Rente, nicht eine Person (Annahme) |
| Paare, Äquivalenzeinkommen Mittel / Median | 32.135 / 28.194 € | ilc_di04: 31.053 / 26.606 € | +3 / +6 % |
| Personen unter dem Grundsicherungsbedarf | 1,13 Mio. | 0,76 Mio. Empfänger (Sekundärquelle) | plausibel bei Nicht-Inanspruchnahme; **bestanden** in der Größenordnung |

**Ergebnis (2028, Kaufkraft 2026, Weitergabe 80 %):**

| Variante | Rentnerhaushalte mit mehr | Mittel je Haushalt im Monat | allein / Paar |
|---|---|---|---|
| ASID, Grundsicherung voll (Basis) | 5,4 % (Ziehungen 5,4–6,1) | −145 € (Median −88 €) | −114 / −179 € |
| ASID, Einkommen beobachtet | 12,6 % | −124 € | −89 / −162 € |
| nur GRV | 2,7 % | −147 € | −115 / −181 € |

- Alle Haushalte: 61,7 % mit mehr (v4.22: 59,9 %), Personen 72,3 %; erwerbsfähige Haushalte unverändert 89,2 %.
- Grundauskommen der Rentner 2,3 Mrd. € im Jahr (v4.22: 52,7 Mrd. €, nicht belastbar); Grundauskommen insgesamt 34,5 Mrd. €.
- Grundsicherung heute im Modell 3,1 Mrd. €: nur die Lücke der Nichtbezieher, weil das EU-SILC-Einkommen der Bezieher die Leistung schon enthält;
  mit den amtlichen Ausgaben nicht vergleichbar.

**Bewertung:**
- Die Beispielrenten des Konzepts (900–2.200 €, −33 bis −54 € je Person) sind richtig gerechnet, liegen aber unter dem Durchschnitt.
- Ein durchschnittlicher Rentnerhaushalt verliert mehr: 114 € (allein) bis 179 € (Paar) im Monat. Hauptursache ist die volle Besteuerung
  nach 33R gegenüber dem Besteuerungsanteil und den Freibeträgen heute; die Kürzung um 7,5 % ersetzt die entfallenden Kassenbeiträge annähernd.
- Das Konzept nennt seit Fassung 4.23 beide Zahlen. Die Frage eines weiteren Ausgleichs für Rentner bleibt der Initiative vorgelegt
  (Vorschlag Rentnerausgleich, Logbuch v4.10/v4.11).
- Keine Korrektur: Keine veröffentlichte Zahl war falsch. Die Aussage galt nur für den genannten Bereich.

**Datenquellen:** Eurostat ilc_di03, ilc_di04, ilc_li02, ilc_li03 (EU-SILC 2025, Abruf 21.10.2026); BMAS Alterssicherungsbericht 2024 über
sozialpolitik-aktuell.de (abbVIII69, Sekundärquelle); DRV Jahresbericht 2025; Rentenanpassung 2024 (4,57 %, Annahme ohne Abruf).

**Wodurch aufgefallen:** nicht bestandene Prüfung in v4.22.

**Offen:** Zusammensetzung der Alterseinkommen nach Einkommenshöhe (ASID-Tabellen); Rentner unter 65; Hinterbliebene in Erwerbshaushalten;
Ausgleich für durchschnittliche Rentnerhaushalte (Entscheidung).

---

## 4 | Korrekturen, Fortsetzung

Neu ab v3.8: die Nummern 47 bis 61. **Nächste freie Nummer: 62.** Die Nummern 31 bis 41 sind
besetzt (Band I). Punkt B1 ist seit v3.12 Korrektur 52.

| Nr. | Was war falsch | Richtig | Wodurch auffiel |
|---|---|---|---|
| 47 | Band II, „Vorbemerkung zur Lücke": Die Einträge v3.2 bis v3.4 und die Korrekturen 31 bis 41 seien beim Zurücksetzen der Arbeitsumgebung verloren gegangen; die Nummern blieben deshalb unbesetzt | Beides liegt vollständig vor: `doku/Versionsgeschichte.md` (1.070 Zeilen) im Ausgabeordner des Vorchats. Verloren war nur dessen Arbeitsverzeichnis. Die Nummern 31 bis 41 sind besetzt, 42 bis 46 schließen korrekt an | Bericht des Vorchats nach Prüfung von `/mnt/user-data/outputs`; hier zeilenweiser Vergleich (v3.8). Der Vorchat hatte den Ausgabeordner nicht geprüft, bevor er den Verlust feststellte |
| 48 | Band II, „v3.2 bis v3.4 — Rekonstruktion": v3.3 sei der „Möglichkeitsraum" (31 Staaten, 534,8 Mio) und in v3.4 werde die Steuerquote 30,6 % abgeleitet | Der Originaleintrag v3.3 heißt „Kalibrierung behoben". Der Möglichkeitsraum steht in keinem Logbucheintrag, nur in einer eigenen Seite (Export). In v3.4 gilt Quote 27,91 % mit Obergrenze 40 %; 30,6 % kommt mit v3.5. Band II widerspricht sich selbst: Zeile 57 „abgeleitet", Zeile 105 „die gesetzten 30,6 %" | Vergleich der Rekonstruktion mit dem Originaleintrag (v3.8). Die Rekonstruktion stammte nicht aus dem Original, sondern aus später gebauten Dokumenten |
| 49 | Seit v3.9 (Zweitrechnung, `basis.py`, Gesamtkonzept Abschnitt 9): Klub-Einwohner 254,8 Mio; acht Länderwerte (ES, NL, IE, BE, AT, DK, SI, EE) sind Übertragungsfehler | 255,061 Mio laut Eurostat `demo_gind` (AVG, 2024) und `daten.py`; Kopfbeträge um 0,09 % niedriger. Zweitrechnung korrigiert (v3.11); `basis.py` und Gesamtkonzept bleiben unverändert und sind bei der nächsten Überarbeitung neu zu rechnen | Hinweis des Vorchats, Abruf der zehn Werte einzeln bei Eurostat |
| 50 | Band I (v3.1) bis Gesamtkonzept 4. Oktober: Zinsausgaben der zehn Staaten 2024 146 Mrd EUR, effektiver Zins 1,53 %, Zinsdienst 2028 1,20 % des BIP | 180,9 Mrd EUR (1,49 % des BIP), effektiver Zins 1,90 %; mit Auslauf ab 2024 Zinsdienst 2028 1,74 % | Abruf Eurostat `gov_10a_main` D41PAY je Land (v3.12); Herkunft der 146 Mrd unbekannt |
| 51 | Gesamtkonzept 4. Oktober, Abschnitt 4: 30,6 % halte das Versprechen „auch dann in jedem Jahr, wenn die Wirtschaft real überhaupt nicht wächst" | Schon in der Lesart des Originals waren 30,61 % nötig; in stimmiger Lesart (nominal 2 %, auch für den Schuldenabbau) 30,73 %. Neu abgeleitet 30,764 → Quote 30,8 % | Kennzahl `mindestquote_streng` (v3.10) und Prüfagent (v3.12) |
| 52 | Band II (Korrektur 43): Dividendenreihe 550 → 512 → 707 EUR ohne Bezugsgruppe und Zeiteinheit (B1) | Deutschland, EUR je Kopf und Monat, Preise 2028; seit v3.12 533 → 521 → 720 | Abgleich v3.7 |
| 53 | Veröffentlichte Webseite (Stand A, Kasten „Warum Estland im Klub ist"): „Ab Januar 2026 gilt ein Satz von 24 %" | Estland bleibt 2026 bei 22 %; die geplante Anhebung wurde 2025 aufgegeben (Sekundärquellen, amtlich zu prüfen) | Recherche für die Länderbeispiele der neuen Seite (v3.15) |
| 54 | v3.17, Lesart V3b (`laendervarianten.py`, Logbuch v3.17): halbes Existenzminimum 514,50 EUR je Erwachsenem „in Preisen 2028", Deckungsgrad 104,8 % | 514,50 EUR ist der Grundfreibetrag 2026 nominal; in Preisen 2028 (2 % je Jahr, Annahme) 535,29 EUR. Deckungsgrad 2028 bei Quote 30,9 % damit rund 101 %, nicht 105 % | Umsetzung der Entscheidung B17 (v3.20): Preisbasis des Ankers gegen die der Rechnung geprüft |
| 55 | Rechner der Seite zum Stand B: Tarifstufen 12.348 / 25.000 / … EUR (Euro 2026) zusammen mit der Dividende in Preisen 2028 | Beide in Preisen 2028; seit v3.21 Stufen beim 1- bis 5-fachen Grundbedarf 2028 | Umstellung des Tarifs auf den Grundbedarf (v3.21) |
| 56 | v3.24, `daten/aggregate/laender/pl_eingaben.md`, Zeile „Defizit, Regierungsprognose“: „7,1 % BIP (2026 und 2027); 282,6 Mrd. Zł (2027)“ | 7,1 % ist das Defizit des Gesamtstaats; 282,6 Mrd. Zł ist das Defizit des Staatshaushalts (zentraler Haushalt), eine andere Abgrenzung. Seit v3.25 nicht mehr in der Zeile; seit v3.26 als eigene Zeile gekennzeichnet. Keine Rechnung betroffen | Forsal/PAP 28.08.2026 nennt die 282,6 Mrd. Zł ausdrücklich als „deficyt państwa“ (Nachrecherche v3.26) |
| 57 | v3.23 (Frankreich), v3.24 bis v3.26 (Standard 2.4): Klubwirkung mit einem Rest-Saldo der übrigen Länder, der den Klub-Gesamtsaldo bei −2,93 % festhielt. Daraus: „Ein französisches Regierungsdefizit wirkt also neutral; das Wachstum entscheidet“ (v3.23); Frankreich B 81,29 %, C 81,96 %; Spanien C 81,15 %; Frankreich und Spanien gemeinsam 81,82 % (v3.26) | Die übrigen Länder behalten ihren eigenen Saldo 2025 (Status quo). Frankreich B 81,05 %, C 81,72 %; Spanien B 81,07 %, C 80,93 %; Niederlande C 81,49 %; Frankreich, Spanien und Niederlande gemeinsam 81,55 %. Die Neutralität des Defizits war ein Artefakt der Methode. Gesamtrechnung und Konzept nicht betroffen (Sensitivität) | v3.27: Die Spalte „Regierungsdefizit“ ergab für jedes Land genau den Referenzwert 81,29 %; das ließ sich nur aus der Bauart erklären |
| 58 | Gesamtkonzept (seit v3.12), Abschnitt Gemeinden: „Estlands Gemeinden geben 5,8 % aus, Deutschlands 16,8 % … bei vergleichbarem Aufgabenvolumen. Der Weg auf estnisches Niveau setzt 1,02 Punkte des BIP frei.“ | Das vergleichbare Aufgabenvolumen ist nicht belegt; die Aufgaben der Gemeinden unterscheiden sich je Land. Belegt ist eine Einsparung der Verwaltung von netto etwa 0,1 bis 0,3 % des BIP nach 8 bis 12 Jahren (deutsche Ex-ante-Studien); der Verwaltungskern (COFOG GF0101) liegt in Estland mit 1,8 % auf EU-Niveau (1,9 %). Die 1,02 Punkte sind eine rechnerische Obergrenze, keine erreichbare Einsparung. Keine Rechnung betroffen (nicht in der Deckung); Text in der nächsten Fassung zu ändern | Recherche zur Wirkung der Verwaltungsdigitalisierung (v3.35) |
| 59 | v3.36, `modell/justierung.py`, Pakete P6 bis P8: Die Ablösung der Verwaltung der Sozialschutzsysteme (0,45 bis 0,78 % des BIP) schließe die Lücke der Quote; P8 mit Lücke −0,65 bzw. −0,98 und Reserve 1,53 bzw. 1,86 | Diese Verwaltungskosten trägt heute der Beitragshaushalt; die Posten der Quote (Ebenen A und B) enthalten sie nicht. Ihr Wegfall gehört zur Entlastung gegen heute und ist Voraussetzung dafür, dass der Wegfall der Beiträge trägt; er schließt keine Lücke der Quote. P8 ohne Ablösung: +3,12, Lücke −0,20, Reserve 1,08, stabil; P6 und P7 nicht stabil | Durchsicht der Pakete vor dem Einrechnen in die Gesamtrechnung (v3.37) |
| 60 | Gesamtkonzept, Kurzfassung und Webseite (seit v3.11, zuletzt Fassung 12. Oktober 2026): „Die Gesamtlast sinkt um 2,81 Punkte des BIP“ (40,76 gegen 37,95 %) | Der Vergleich enthält heute die Finanzierung des gesamten Sozialschutzes (20,07 % BIP), der Entwurf nur die Dividende (11,86 %) und die Gesundheit. Die Altansprüche über der Dividende (Z, 2028 rund 8,9 % BIP, Schätzung v3.42), eine Pflicht-Vorsorge und Pflichtversicherungen fehlen. Mit ihnen liegt die Last 2028 bei rund 54 %; im Dauerzustand nach dem Auslauf von Z ist der Sozialschutz etwa so groß wie heute. Aussage bis zur Entscheidung über den Übergang zurückzuziehen | Vorschläge Generationenbaustein und Hütte/Route/Seil (16.10.2026), Rechnung v3.42 |
| 61 | v3.47 und v3.48, `modell/projektion33.py`: Anteil der Einkommensteuer am BIP bis 2060 fest; Dividende 2060 48 € (33F) bzw. 83 € (33R), Kaufkraft 2026 | Die Stufen hängen am Grundbedarf, der nur zu 30 % den Löhnen folgt; mit realem Wachstum steigt der Anteil (2060 +1,24 Punkte). Dividende 33R 2060 170 €. Haushalts- und Einwanderungsrechnung damit neu | Nachfrage der Initiative zu Automatisierungsgewinnen; Prüfung, welche Wirkungen des Wachstums fehlen (v3.49) |
| 62 | Webseite v4.0 (alle Sprachen), `drittel_texte.py`, div_p1: „Jedes Land zahlt denselben Anteil seiner Wirtschaftsleistung aus.“ | Im Drittel-System ist die Dividende der Rest nach Dach, Gemeinden und Netz; ihr Anteil am BIP unterscheidet sich je Land (2028: Frankreich 4,6 %, Deutschland 7,3 %, Polen 8,4 %). Der Satz stammt aus 28:28. Ersetzt durch „Ihre Höhe folgt aus der Wirtschaftsleistung und den Aufgaben jedes Landes.“ (v4.1) | Länderrechnung für die Sprachversionen (v4.1) |
| 63 | Webseite DE seit v3.58, Konzept 4.0: „9 von 10 Beschäftigten haben mehr im Geldbeutel“ (haushalte33, heute ohne bedarfsgeprüfte Leistungen) | Mit Bürgergeld-Aufstockung heute (volle Inanspruchnahme angenommen; Näherung auch für Wohngeld und Kinderzuschlag) haben in Deutschland 87 % der Alleinstehenden und Alleinerziehenden, aber nur 60 % der Paare mit einem Einkommen und zwei Kindern mehr (grobe Verteilung, sozial_laender.py). Die Aussage ist für Deutschland so nicht gedeckt; Italien, Spanien, Polen bleiben bei 98–100 %. Die Seite wird beim nächsten Bau angepasst (Entscheidung zu R1–R4 abwarten); das Paket v4.1 nicht hochladen | Frage der Initiative zu Mindestsicherung und Härtefallfonds (v4.2/v4.3) |
| 64 | Seite, Konzept und Freigabevorlage v4.8: Frankreichs Gini steige, „weil Lohnzuschüsse wegfallen und hohe Einkommen weniger zahlen als heute“ | Hauptursache ist die 80-%-Weitergabe der in Frankreich ungedeckelten Arbeitgeberbeiträge (hohe Löhne +24–41 %), dazu die SMIC-Delle und die kleinste Dividende (8 % des Medians); rund die Hälfte des Anstiegs hängt an der Abbildung über Einzelpersonen (Familienabbildung 29,5 statt 32,2). Mit Deckel der Weitergabe sinkt der Gini auch in Frankreich (27,6–29,8). Texte in sechs Sprachen und im Konzept berichtigt (v4.9) | Nachfrage der Initiative zur Anomalie |
| 65 | Konzept 4.8/4.9, Freigabevorlage, Logbuch v4.8, Projektsteuerung: Rentner verlieren durch R1 zusätzlich 19 €, Minus −54 bis −142 € | Die Dividende ist Teil der Bestandsrente (Fonds zahlt nur den Anspruch darüber); R1 ändert das Rentnernetto nicht, sondern die Kosten des Fonds. Richtig −35 bis −123 €. Konzept berichtigt (v4.10) | Nachrechnung für den Rentnerausgleich |
| 66 | README, INDEX, AGENTS, DATENZUGANG, CLAUDE.md bis v4.11: „geltende Rechnung `modell/gesamtrechnung.py`“ (28:28, Stand B) | Geltend ist seit v3.43 das Drittel-System (Stand C); die Einstiegsdokumente verzeichneten es nicht, eine externe Prüfung prüfte deshalb den Vorläufer. Abschnitt „Aktueller Stand“ mit Skriptkarte ergänzt (v4.12) | externe Prüfung vom 19.10.2026 |
| 67 | Repository bis v4.13: zwei Dividendenpfade (netz33 373 €, projektion33 296 € für 2028) und Gesamtlast 45,46 % (systemvarianten, ohne Fonds) ohne Kennzeichnung des geltenden Werts; Stellungnahme 20.10.2026: Vielfache des Durchschnittslohns ohne Lohnbasis | geltend netz33 (mit R1 354 €), Gesamtlast mit Fonds 38,81 % (mit Pflichtvorsorge 42,91 %), Lohnbasis OECD 63.288 €; `KENNZAHLEN.md`, Statusvermerk in projektion33 (v4.14) | zweite externe Prüfung 20.10.2026 |
| 68 | Modellstand in parameter.toml, README, INDEX und Band III nach v4.15–v4.17 nicht fortgeschrieben (blieb v4.14) | alle auf v4.18; README-Skriptkarte ergänzt (v4.18) | Bau des Upload-Pakets, Projektprüfung |
| 69 | haushalte33.py seit v4.5 mit 373 € und Kindern zur Hälfte statt Kinderanteil 0,8 bei gleichem Topf (354/283 €) | Topf-Faktor und Kinderanteil aus regel_boden.toml in neu() (v4.21); Beispiele 42.000 €: allein +608, alleinerziehend +607, Paar mit 2 Kindern +673 € | Hinweis des Prüfers (Kulturverein Ribbeck e.V.), 21.10.2026 |

Der Originaltext in Band II bleibt stehen, damit der Fehler prüfbar ist; an der Vorbemerkung
steht seit v3.8 ein Verweis auf diese Korrekturen. Maßgeblich für v3.2 bis v3.4 ist Band I.

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
| v3.5.1 bis v3.7, `README.md`, `CLAUDE.md`, `HERKUNFT.md`: Die Skripte und Logbucheinträge bis v3.4 seien verloren und nicht reproduzierbar; `pfad.py`, `aufschlag.py` seien mangels Original Rekonstruktionen ohne Vergleichsmöglichkeit | Die Originale lagen im Ausgabeordner des Vorchats. Ich habe die Verlustaussage aus Band II übernommen, ohne nach einem erhaltenen Ausgabeordner zu fragen | Hochgeladener Export, v3.8 |
| v3.7: `daten/aggregate/nicht-eingetragen.md` und Hinweise in `parameter.toml` nennen `altschuld.py` als Quelle des Aufschlag-Verfahrens | Das Original von `altschuld.py` nutzt eine andere Bemessung (Klubschnitt je Kopf) als `aufschlag.py` (BIP); die Zahlen +254/−728 stammen aus `aufschlag.py` | Vergleich mit den Originalen, v3.8 |
| Commit-Nachricht von `23b7050` nennt „26 gesamt" | Es sind 25 Parameter | Zählung im Lauf-Skript. Die Nachricht wurde nicht per Force-Push geändert |

**Ablaufnotiz, kein Fehler.** Der Push des Tags `v3.5` wurde von der Verbindung dieser
Sitzung mit HTTP 403 abgelehnt, der Push des Branches nicht. Der Tag wurde danach
über ein GitHub-Release am Commit `a5808b1` gesetzt. Die Ursache der Ablehnung ist
nicht geklärt.

---

## 7 | Offene Punkte, Stand v4.23

Neu seit v3.23 (Stand v4.23): **Rentner: Ausgleich für durchschnittliche Rentnerhaushalte (−114 / −179 €) entscheiden, Zusammensetzung der Alterseinkommen nach Einkommenshöhe;** **Mikrosimulation Stufe 2 (weiter): Teilzeit-Dezile, Selbständige und Beamte, Nicht-Inanspruchnahme; Aussage zu Rentnern und Bürgergeldhaushalten ohne Erwerb auf der Seite prüfen;** **Mikrosimulation: Rechenweg des Prüfers, Teilzeit und Bedarfsleistungen; Fonds der 30: Verrechnung je Staat, direkte Rechnung statt Verhältnis, Einwanderung/Dynamik umstellen; Preisniveau: Zweitrundeneffekte und CO₂-Pfad; Ausweichen mit Verteilungsdaten; Gemeindeeinnahmen je Kreis heute (Datei der Initiative); Strukturzuschlag (Vorschlag 10 %); Sicherheitsunion mit Anteil der Mehrwertsteuer (Vorschlag 50 % = 15 %), Rechtsprüfung (N34); Gemeinsame Aufgaben: Kassenanteile, Bemessung am BNE, Anrechnung für neutrale Staaten (N32); Finanzverteilung im Staat und Stärkung der Regionen (N33); Fonds auf den Länderseiten vereinheitlichen (B11); dritte Prüfung; Weitergabe: Nachweis, Sanktion, neue Verträge; Architekturvariante „Regelwerk statt Dach“ entscheiden; Punkte der externen Prüfung ( Ausweichreaktionen, Preisniveau, WTO, Labels, Recht, Gegenentwurf); Rentnerpaket gerechnet (A, T1, B1, L1); T1 kostet 0,50 % BIP – prüfen; Rentenverteilung DRV; Deckel der Weitergabe (Frankreich, Korrektur 64); Haushaltsmischung im Gini; Freigabe Fassung 4.8 (Kindergewicht 0,55, H1–H3/G1–G5, Upload); Übersetzungen der neuen Texte gegenlesen; Mietdaten für H1; Bedarfsleistungen IT/ES/PL heute; Rentnerausgleich; Härtefall H1–H3, Kindergewicht K1, Rolle der Gemeinden G1–G5 entscheiden und Kosten mit Mietdaten rechnen (N27); Regel Boden und Kinderanteil 0,8 in Seiten einbauen; Gewinneraussage je Land neu fassen; Kosten mit Haushaltsdaten verfeinern; Grundbedarf gegen Armutsschwellen je Land; Entscheidung R1–R4 (Kinderanteil, Pflichtvorsorge über dem Grundbedarf, Härtefall-Boden, Mindestlohnregel); Kosten des Bodens; Aussage „9 von 10“ in DE nach Korrektur 63 neu fassen;** **Bedarfsgeprüfte Leistungen heute (Wohngeld, Kinderzuschlag, APL, RSA, ADI, IMV) in allen Haushaltsrechnungen nachtragen und Härtefallfonds zuordnen; Erwerbstätigenleistung im Netz entscheiden; Zins des Fonds je Land;** **Länderseiten: Entscheidung Frankreich (N24), feinere Lohnverteilungen, Mindestsicherung je Land, Übersetzungen und Begriffe prüfen;** **Fassung 4.0: Übersetzungen und Wortmarken muttersprachlich prüfen; Konzept in weiteren Sprachen; Server aktualisieren (ZIP);** **Mehrheitsaussage: feinere Lohnverteilung, Beamte, Selbständige, Fälle ohne Einkommen; Ausgleich für Rentner;** **Webseite: Wertungen umgesetzt in v4.19; Zinsvorteil des gemeinsamen Fonds beziffern;** **Rechner: Verteilungswirkung bei hohen Einkommen, Fälle ohne Einkommen;** **Webseitenentwurf Drittel: Obergrenze des Dachs neu rechnen, Estland-Satz prüfen, Freigabe;** **Neustartverfahren: Entscheidung, Rechtsprüfung (Eigentumsschutz, Art. 125 AEUV), Ratifizierungsstand der ESM-Reform;** **Möglichkeitsraum: UK und Kanada (OECD-Daten); Altersprofil je Staat (Ageing Report); eigene Lösungen für Staaten mit Lücke im Dauerzustand (SE, DK, CZ, FR);** **Konzept (Word) prüfen; Rentnerausgleich; Durchsetzung der Weitergabepflicht; Einwanderung und Automatisierung auf den Netz-Beschluss umrechnen; Gesamtrechnung auf das Drittel-System umstellen;** **Namen (Goldenes Drittel, Goldenes Netz, Transformationsdividende, Zukunftsschatz) beschließen und markenrechtlich prüfen; Stufenbindung (Preise/Löhne) als Wahl festlegen;** **Rentner im Drittel-System leicht im Minus (Ausgleich prüfen); Kürzungssatz je Staat; Durchsetzung der 80-%-Pflicht; Tag v3.47 lokal, Push abgelehnt (nachholen);** **Drittel-System F1–F4 (Name, Dauer der Dividende unter Trends, Verteilung, Webseitenentwurf);** **Beschlüsse 17.10.2026 in die Gesamtrechnung übernehmen; Härtefall rechnen; Verhandlung der zweiten Hälfte der Altrenten; juristische Prüfung;** **E1–E6 (Prämie oder prämienfrei, Sonderstufe, Anteil der Altrenten, Streckung und Deckel, Quelle des Beitrags, Verrechnung je Staat);** **Drittellösung D1–D5 (Marke, Altlastenbeitrag, Anteil der Zusagen, Gesundheitsanteil, Übernahme);** **Wahl der Marke (V1–V4: 28:28 / 25:25 / 33:33 / 33:33 nur mit Seil);** **Sozialschutz und Übergang: Antwortbogen S1–S13 (Zusammenführung 16.10.2026); Gesamtlast-Aussage zurückziehen (Korrektur 60); Härtefall finanzieren;** **Steuerpflicht der Dividende im Rechner der Webseite angleichen; Durchsicht der RTF-Einführung;** **Fassung 10. Oktober 2026 freigegeben und veröffentlicht (v3.39); muttersprachliches Gegenlesen der geänderten Texte (B16); Aufgabenliste des Dachs im Einzelnen; Ausgleichsrücklage; Deckung auf Klubebene (B12) für den Überschuss von 0,24 Punkten**; Text Verwaltung (Korrektur 58) umgesetzt in v3.39; Paket P8 entschieden und eingerechnet (v3.37); EU-Rechtsrahmen nach Entscheidung nicht bindend; **Entscheidungen E1 C, E2 V2, E3 je Land, E4 81,3 % gefallen (v3.33); offen: zusätzliche Lücke ohne Verletzung der Mindestdividende schließen (Stufen oder Bausteine)**; **Konsumaufkommen: Zuordnung der Produkte zu den Labelstufen und Sätze (effektiv 14,9 bis 16,9 % statt 20 %, Deckungslücke +1,2 bis +2,0 Punkte)**; Verteilungsmodell für den Klub (Umfang der Umverteilung); Leitlinie v3.29/v3.30: Regel der Dividende (V3a geltend, V2 nach Leitlinie); Mindestdividende im Klubschnitt oder je Land (Konflikt mit v3.20); Anreize für Investition, Binnenmarkt, Dividende und Arbeitsangebot nicht quantifiziert; Ländervergleich: Abgabenkeil je Land fehlt (OECD Taxing Wages); Gemeindeformel auf der Seite (Klub) gegen Entscheidung v3.17 (je Land); Klubquote 2028, gemeinsame Wirkung FR+ES+NL 81,55 % nach Korrektur 57 (Entscheidung 81,3 / 82,0 %); Niederlande: Widerspruch Miljoenennota/CPB; Belgien: Haushalt 2027 ab 13.10.2026; Polen, Schuld und Saldo 2028 nicht gefunden (Annahmen); Schuldenstrategie und Verfassung nicht im Original; Wachstum je Land (Entscheidung); Spanien nach dem Standard rechnen; Umsetzung des Standards in Webseite und Konzepttexten (Standard, Abschnitt 6). Die übrigen Punkte von v3.23 gelten weiter.

| Punkt | Status |
|---|---|
| **B1: Dokumentationslücke Dividendenreihe** | **geschlossen in v3.12 (Korrektur 52)** |
| **B2: 707 gegen 712 EUR** | **geschlossen in v3.12.** Ein Zentralfall (3,0 % nominal = 0,98 % real), dieselbe Rechnung in Zeitpfad und Tabelle |
| **B3: BIP Deutschland 2028** | **überholt, geschlossen in v3.7.** Beide Werte meinen 2028. 4.914,9 hat eine dokumentierte Herleitung und ist seit v3.3 Basis. Quelle von 4.884 unbekannt (Differenz 0,63 %) |
| **B4: Irland, BIP oder GNI\*** | **entschieden in v3.12: BIP**, Begründung im Konzept (Abschnitt 5, 9); Größenordnung GNI\* genannt, nicht gerechnet |
| **B5: Ebene A 8,94 % gegen 9,04 %** | **geschlossen in v3.7, war kein Widerspruch** (8,94 enthält Verteidigung 2,50, die Tabelle 2028 rechnet mit 1,40) |
| **B6: Ausgangslage 2024 als 2028** | **entschieden in v3.12, geändert in v3.19:** Schuldenquote 2028 = 81,3 % als Fortschreibung des Status quo (`modell/schuldenpfad.py`, gleich bleibende Defizite 2025, 3,0 % nominales Wachstum); Risikofall +3,5 Punkte (84,8 %). Vorher Annahme 78,4 % (= Stand 2024) |
| **Rechenskripte** | Originale in `modell/rahmen/` (unverändert, Prüfsummen); geltende Rechnung `modell/gesamtrechnung.py` (v3.12); Zweitrechnung als Regression. Das Bauskript `gesamtkonzept-bau.js` ist seit v3.12 gelesen und neu geschrieben. Skripte bis v3.4 liegen in `modell/kern/`, `rechnungen/`, `audit/` (Stand A, nicht erneut ausgeführt) |
| **B7: Einwohnerzahl** | **geschlossen in v3.12.** Gesamtkonzept rechnet mit 255,061 Mio; `basis.py` bleibt als Original |
| **B8: Bemessung des Aufschlags** | **geklärt in v3.11.** BIP-Bemessung folgt aus der Finanzierung nach BIP-Anteil; `altschuld.py` überholt (Sekundärquelle) |
| **B9: Obergrenze** | **entschieden in v3.12:** abgeleitete Regel (36 % bis v3.19). **Seit v3.20: 35 %** (größerer Einzug bei Quote 31,9 %); nicht gedeckt: Häufung der Risiken (35,6 %) und 3,5 % Verteidigung (37,3 %) |
| **B10: Basis des Gesamtkonzepts** | **geschlossen in v3.9.** Das Gesamtkonzept steht auf der korrigierten Basis |
| **B12: Deckung der Quote** | **gerechnet in v3.12 (deutsche Basis):** 29,85 % nachgewiesen, Lücke 0,95 Punkte zu 30,8 % (v3.19: 1,05 Punkte zu 30,9 %; v3.20: 2,05 Punkte zu 31,9 %; v3.21: 1,79 Punkte; **seit v3.22: 1,73 Punkte, 239 Mrd EUR Klub**, Tarif 0/9/16/21/28 am Grundbedarf). Klubebene offen: Steuerbasen der zehn Staaten nach Position. **Nächste Rechnung** |
| **B13: Bezugsgröße der Obergrenze im Text** | **geschlossen in v3.12** (überall „dessen, was A einzieht") |
| **B14: Gesamtlast heute 40,76 gegen Summe 40,83** | **geschlossen in v3.11, keine Korrektur.** 40,76 ist das Eurostat-Aggregat abzüglich D995; Fußnote im Gesamtkonzept fehlt |
| **B15: Neu abrufen** | **offen, präzisiert in v3.14.** Deutsches BIP 2024 bei Eurostat revidiert (4.386.940 statt 4.328.970 Mio EUR, +1,34 %, vorläufig). Alle zehn BIP-Werte (Schuldenstände 2010–2025 und Defizite 2025 seit v3.19 neu abgerufen), Renditen, COFOG-Posten und Zinsausgaben (Estland) in einem Durchgang neu abrufen, dann neu rechnen. Ratenbegrenzung: Pausen einplanen |
| **B16: Seite zum Stand B** | **sechs Sprachen in v3.18.** Offen: muttersprachliches Gegenlesen, Länderanpassung (eigene Zahlen je Land statt Referenzland Deutschland), Veröffentlichung mit `fonts/` |
| **B17: Dividende gleich oder je Land?** | **entschieden in v3.20:** Dividende nach Preisniveau (V3a), Boden halbes Existenzminimum am Wohnort (Quotenkriterium, streng), Umzugsregel drei Jahre mit Steuernachweis. Umzugsregel v3.21: Kinder und Studierende ohne Steuernachweis; Fälle ohne Einkommen vorerst ausgeklammert (v3.22). Offen: Europarecht; jährliche Fortschreibung der Preisniveaus; Fortschreibung des Existenzminimums |
| **B18: 95 % für Stand B** | **neu, v3.13.** Die Gruppenschätzung stammt aus Stand A; für Stand B neu schätzen, spätestens mit der Mikrosimulation |
| **B19: Posten der Ebenen A und B** | **neu, v3.14.** Zuordnung COFOG-Gruppen und Sektoren (S13, S1313) zu den 15 Posten sowie die Bodenwertabgabe 0,82 sind nicht als Tabelle mit Abrufadresse dokumentiert. Nachholen: `daten/zuordnung_posten.csv` (Posten, GF-Codes, Sektor, Anteil, URL) |
| **Registerpflege** | **neu, v3.10.** Nach jeder Version `python3 modell/alles.py`, `projekt/bausteine.csv` und `nahtstellen.csv` anpassen, Projektraum nachführen. Der Abgleich mit dem Projektraum geschieht von Hand |
| **Stand A und Stand B** | **neu, v3.8.** Modell (`1-modell`) und achtsprachige Webseite im Export stehen auf dem nationalen Stand (Quote 27,91 % bzw. 33 %, Position 10 Sozialabgaben, Logbuch v2.0); das Gesamtkonzept auf dem europäischen (Quote 30,6 %, v3.5). Die Seite hat den Rahmenwechsel nie gesehen. Zwei Builds der Seite (Tarifstufen 0/9/16/21/26/28 gegen 0/9/19/24/27/28); der Quelltext passt nur zum älteren, die Patch-Skripte sind nicht ausgeführt. Nach Angabe des Exports; von mir nicht geprüft |
| **Herleitung von 6,44 und 10,35** | Summen der COFOG-abgeleiteten Posten (Band II, v3.2). Siehe B19. Eurostat ist über das Web-Abrufwerkzeug erreichbar (nicht über die Shell); die Posten lassen sich damit nachholen |
| **Nicht eingetragene Größen** | Mindestquote, Obergrenze von A, Höchstbedarf, territorialer Aufschlag: Bezugsjahr oder Bezugsgröße fehlt. Siehe `daten/aggregate/nicht-eingetragen.md`, Abschnitt A |
| **Rohdaten und Abrufe nicht reproduzierbar** | **teilweise behoben in v3.14:** jede amtliche Eingangsgröße hat eine Abrufadresse (`daten/aggregate/eingangswerte.csv`); Abrufergebnisse selbst liegen nicht als Rohdaten vor (Regel: keine Rohdaten im Repository) |
| **Prüfstand der Logbuch-Abschrift** | **geschlossen in v3.8**: Band I ist die Originaldatei, Band II zeilengleich, siehe `HERKUNFT.md` |
| Alle offenen Punkte aus Band I (Abschnitt 7) und Band II (Zusatz zu v3.5) | unverändert, soweit hier nicht genannt |
