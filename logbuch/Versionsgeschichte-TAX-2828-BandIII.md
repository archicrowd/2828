# TAX 28:28 — Logbuch, Band III: ab v3.5.1

**Fortsetzung von `Versionsgeschichte-TAX-2828-BandII.md`.** Band II endet mit
v3.5 und Korrektur 46. Dieser Band führt ab v3.5.1 weiter und ist der erste, der
direkt in diesem Repository entsteht und nicht aus dem Projektraum übernommen
wurde.

Stand: 7. Oktober 2026 · Modellstand **v3.22.1**

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

## 4 | Korrekturen, Fortsetzung

Neu ab v3.8: die Nummern 47 bis 53. **Nächste freie Nummer: 54.** Die Nummern 31 bis 41 sind
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

## 7 | Offene Punkte, Stand v3.22

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
