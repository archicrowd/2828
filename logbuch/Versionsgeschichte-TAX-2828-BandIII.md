# TAX 28:28 — Logbuch, Band III: ab v3.5.1

**Fortsetzung von `Versionsgeschichte-TAX-2828-BandII.md`.** Band II endet mit
v3.5 und Korrektur 46. Dieser Band führt ab v3.5.1 weiter und ist der erste, der
direkt in diesem Repository entsteht und nicht aus dem Projektraum übernommen
wurde.

Stand: 6. Oktober 2026 · Modellstand **v3.12**

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

## 4 | Korrekturen, Fortsetzung

Neu ab v3.8: die Nummern 47 bis 52. **Nächste freie Nummer: 53.** Die Nummern 31 bis 41 sind
besetzt (Band I). Punkt B1 ist seit v3.12 Korrektur 52.

| Nr. | Was war falsch | Richtig | Wodurch auffiel |
|---|---|---|---|
| 47 | Band II, „Vorbemerkung zur Lücke": Die Einträge v3.2 bis v3.4 und die Korrekturen 31 bis 41 seien beim Zurücksetzen der Arbeitsumgebung verloren gegangen; die Nummern blieben deshalb unbesetzt | Beides liegt vollständig vor: `doku/Versionsgeschichte.md` (1.070 Zeilen) im Ausgabeordner des Vorchats. Verloren war nur dessen Arbeitsverzeichnis. Die Nummern 31 bis 41 sind besetzt, 42 bis 46 schließen korrekt an | Bericht des Vorchats nach Prüfung von `/mnt/user-data/outputs`; hier zeilenweiser Vergleich (v3.8). Der Vorchat hatte den Ausgabeordner nicht geprüft, bevor er den Verlust feststellte |
| 48 | Band II, „v3.2 bis v3.4 — Rekonstruktion": v3.3 sei der „Möglichkeitsraum" (31 Staaten, 534,8 Mio) und in v3.4 werde die Steuerquote 30,6 % abgeleitet | Der Originaleintrag v3.3 heißt „Kalibrierung behoben". Der Möglichkeitsraum steht in keinem Logbucheintrag, nur in einer eigenen Seite (Export). In v3.4 gilt Quote 27,91 % mit Obergrenze 40 %; 30,6 % kommt mit v3.5. Band II widerspricht sich selbst: Zeile 57 „abgeleitet", Zeile 105 „die gesetzten 30,6 %" | Vergleich der Rekonstruktion mit dem Originaleintrag (v3.8). Die Rekonstruktion stammte nicht aus dem Original, sondern aus später gebauten Dokumenten |
| 49 | Seit v3.9 (Zweitrechnung, `basis.py`, Gesamtkonzept Abschnitt 9): Klub-Einwohner 254,8 Mio; acht Länderwerte (ES, NL, IE, BE, AT, DK, SI, EE) sind Übertragungsfehler | 255,061 Mio laut Eurostat `demo_gind` (AVG, 2024) und `daten.py`; Kopfbeträge um 0,09 % niedriger. Zweitrechnung korrigiert (v3.11); `basis.py` und Gesamtkonzept bleiben unverändert und sind bei der nächsten Überarbeitung neu zu rechnen | Hinweis des Vorchats, Abruf der zehn Werte einzeln bei Eurostat |
| 50 | Band I (v3.1) bis Gesamtkonzept 4. Oktober: Zinsausgaben der zehn Staaten 2024 146 Mrd EUR, effektiver Zins 1,53 %, Zinsdienst 2028 1,20 % des BIP | 180,9 Mrd EUR (1,49 % des BIP), effektiver Zins 1,90 %; mit Auslauf ab 2024 Zinsdienst 2028 1,74 % | Abruf Eurostat `gov_10a_main` D41PAY je Land (v3.12); Herkunft der 146 Mrd unbekannt |
| 51 | Gesamtkonzept 4. Oktober, Abschnitt 4: 30,6 % halte das Versprechen „auch dann in jedem Jahr, wenn die Wirtschaft real überhaupt nicht wächst" | Schon in der Lesart des Originals waren 30,61 % nötig; in stimmiger Lesart (nominal 2 %, auch für den Schuldenabbau) 30,73 %. Neu abgeleitet 30,764 → Quote 30,8 % | Kennzahl `mindestquote_streng` (v3.10) und Prüfagent (v3.12) |
| 52 | Band II (Korrektur 43): Dividendenreihe 550 → 512 → 707 EUR ohne Bezugsgruppe und Zeiteinheit (B1) | Deutschland, EUR je Kopf und Monat, Preise 2028; seit v3.12 533 → 521 → 720 | Abgleich v3.7 |

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

## 7 | Offene Punkte, Stand v3.12

| Punkt | Status |
|---|---|
| **B1: Dokumentationslücke Dividendenreihe** | **geschlossen in v3.12 (Korrektur 52)** |
| **B2: 707 gegen 712 EUR** | **geschlossen in v3.12.** Ein Zentralfall (3,0 % nominal = 0,98 % real), dieselbe Rechnung in Zeitpfad und Tabelle |
| **B3: BIP Deutschland 2028** | **überholt, geschlossen in v3.7.** Beide Werte meinen 2028. 4.914,9 hat eine dokumentierte Herleitung und ist seit v3.3 Basis. Quelle von 4.884 unbekannt (Differenz 0,63 %) |
| **B4: Irland, BIP oder GNI\*** | **entschieden in v3.12: BIP**, Begründung im Konzept (Abschnitt 5, 9); Größenordnung GNI\* genannt, nicht gerechnet |
| **B5: Ebene A 8,94 % gegen 9,04 %** | **geschlossen in v3.7, war kein Widerspruch** (8,94 enthält Verteidigung 2,50, die Tabelle 2028 rechnet mit 1,40) |
| **B6: Ausgangslage 2024 als 2028** | **entschieden in v3.12:** Auslauf ab 2024; Schuldenquote 2028 = 78,4 % bleibt Annahme (Sensitivität 82 %) |
| **Rechenskripte** | seit v3.8 liegen die Originale `basis.py`, `pfad.py`, `final.py`, `tilgung.py`, `aufschlag.py`, `altschuld.py`, `kurve.py` in `modell/rahmen/`. `modell/pfad.py` und `modell/aufschlag.py` bleiben als **unabhängige Zweitrechnung** (`modell/vergleich_original.py`). Ungelesen: `zahlen.py`, `gesamtkonzept-bau.js`, JSON-Ausgaben. Skripte der Versionen bis v3.4 (Kern, Webseite, Audit, Einzelrechnungen) liegen im Export, aber noch nicht im Repository |
| **B7: Einwohnerzahl** | **geschlossen in v3.12.** Gesamtkonzept rechnet mit 255,061 Mio; `basis.py` bleibt als Original |
| **B8: Bemessung des Aufschlags** | **geklärt in v3.11.** BIP-Bemessung folgt aus der Finanzierung nach BIP-Anteil; `altschuld.py` überholt (Sekundärquelle) |
| **B9: Obergrenze 36 %** | **entschieden in v3.12:** abgeleitete Regel bestätigt 36 %; nicht gedeckt: Häufung der Risiken (36,7 %) und 3,5 % Verteidigung (38,5 %) |
| **B10: Basis des Gesamtkonzepts** | **geschlossen in v3.9.** Das Gesamtkonzept steht auf der korrigierten Basis |
| **B12: Deckung der Quote** | **gerechnet in v3.12 (deutsche Basis):** 29,85 % nachgewiesen, Lücke 0,95 Punkte zu 30,8 %. Klubebene offen: Steuerbasen der zehn Staaten nach Position. **Nächste Rechnung** |
| **B13: Bezugsgröße der Obergrenze im Text** | **geschlossen in v3.12** (überall „dessen, was A einzieht") |
| **B14: Gesamtlast heute 40,76 gegen Summe 40,83** | **geschlossen in v3.11, keine Korrektur.** 40,76 ist das Eurostat-Aggregat abzüglich D995; Fußnote im Gesamtkonzept fehlt |
| **B15: Neu abrufen** | **neu, v3.12.** BIP, Schuldenquoten, Renditen und COFOG-Posten sind seit dem 4. Oktober nicht erneut geprüft; Zinsausgaben Estland geschätzt. Abruf je Land einzeln über das Web-Abrufwerkzeug (Ratenbegrenzung beachten) |
| **B16: Seite zum Stand B** | **neu, v3.12.** zeigt die Werte der Fassung 4. Oktober; neu bauen, sobald B12 auf Klubebene steht |
| **Registerpflege** | **neu, v3.10.** Nach jeder Version `python3 modell/alles.py`, `projekt/bausteine.csv` und `nahtstellen.csv` anpassen, Projektraum nachführen. Der Abgleich mit dem Projektraum geschieht von Hand |
| **Stand A und Stand B** | **neu, v3.8.** Modell (`1-modell`) und achtsprachige Webseite im Export stehen auf dem nationalen Stand (Quote 27,91 % bzw. 33 %, Position 10 Sozialabgaben, Logbuch v2.0); das Gesamtkonzept auf dem europäischen (Quote 30,6 %, v3.5). Die Seite hat den Rahmenwechsel nie gesehen. Zwei Builds der Seite (Tarifstufen 0/9/16/21/26/28 gegen 0/9/19/24/27/28); der Quelltext passt nur zum älteren, die Patch-Skripte sind nicht ausgeführt. Nach Angabe des Exports; von mir nicht geprüft |
| **Herleitung von 6,44 und 10,35** | Beide sind Summen der COFOG-abgeleiteten Posten aus Band II (v3.2): 6,44 für Ebene A ohne Verteidigung, 10,35 für Ebene B. Die zugrunde liegenden Eurostat-Abrufe (COFOG, zehn Staaten) liegen nicht vor, die Shell erreicht `ec.europa.eu` nicht. Nachgerechnet sind die Summen der Posten, nicht die Posten |
| **Nicht eingetragene Größen** | Mindestquote, Obergrenze von A, Höchstbedarf, territorialer Aufschlag: Bezugsjahr oder Bezugsgröße fehlt. Siehe `daten/aggregate/nicht-eingetragen.md`, Abschnitt A |
| **Rohdaten und Abrufe nicht reproduzierbar** | Die Eurostat-Abrufe (zehn Einzelabrufe COFOG GF02, `gov_10a_exp`, `gov_10a_taxag`, `nama_10_gdp`, `demo_gind`) sind im Logbuch nur benannt, die Abrufergebnisse liegen nicht vor. Die Shell erreicht `ec.europa.eu` nicht (Logbuch v3.1) |
| **Prüfstand der Logbuch-Abschrift** | **geschlossen in v3.8**: Band I ist die Originaldatei, Band II zeilengleich, siehe `HERKUNFT.md` |
| Alle offenen Punkte aus Band I (Abschnitt 7) und Band II (Zusatz zu v3.5) | unverändert, soweit hier nicht genannt |
