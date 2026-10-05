# TAX 28:28 — Logbuch, Band III: ab v3.5.1

**Fortsetzung von `Versionsgeschichte-TAX-2828-BandII.md`.** Band II endet mit
v3.5 und Korrektur 46. Dieser Band führt ab v3.5.1 weiter und ist der erste, der
direkt in diesem Repository entsteht und nicht aus dem Projektraum übernommen
wurde.

Stand: 5. Oktober 2026 · Modellstand **v3.6**

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
| Commit-Nachricht von `23b7050` nennt „26 gesamt" | Es sind 25 Parameter | Zählung im Lauf-Skript. Die Nachricht wurde nicht per Force-Push geändert |

**Ablaufnotiz, kein Fehler.** Der Push des Tags `v3.5` wurde von der Verbindung dieser
Sitzung mit HTTP 403 abgelehnt, der Push des Branches nicht. Der Tag wurde danach
über ein GitHub-Release am Commit `a5808b1` gesetzt. Die Ursache der Ablehnung ist
nicht geklärt.

---

## 7 | Offene Punkte, Stand v3.6

| Punkt | Status |
|---|---|
| **B1: Dokumentationslücke Dividendenreihe** | **neu, 5. Oktober 2026.** Band II (Korrektur 43) nennt 550 → 512 → 707 € ohne Bezugsgruppe („Deutschland") und ohne Zeiteinheit („je Monat"). Inhaltlich aufgelöst, im Logbuch nicht vermerkt. Ob Korrektur 47, entscheidet der Verfasser |
| **B2: 707 gegen 712 €** | **erklärt in v3.6 (Hypothese), nicht entschieden.** 707 und 512 gehören zu 0,980 % realem Wachstum je Kopf, 712 und 513 zu 1,0 %. Welche Zahl im Gesamtkonzept stehen bleibt, ist eine Entscheidung des Verfassers. Prüfung am Original nicht möglich |
| **B3: BIP Deutschland 2028** | **neu.** 4.914,9 Mrd € (Band II) gegen „amtlich fortgeschrieben 4.884 Mrd €" (Audit v3.0, ohne Jahr). Ob beide dasselbe Jahr meinen, ist nicht erkennbar |
| **B4: Irland, BIP oder GNI\*** | **neu.** Logbuch v0.2 nennt GNI\* als Bezugsgröße; das Klub-BIP 2024 stammt aus `nama_10_gdp` (BIP). Ob Irland dort nach BIP oder GNI\* eingeht, steht nicht im Logbuch. Unterschied nach den Zahlen aus v0.2 rund 268 Mrd € (etwa 2 % des Klub-BIP) |
| **B5: Ebene A 8,94 % gegen 9,04 %** | **neu in v3.6.** Band II v3.2 gegen Zeitpfad-Tabelle 2028; 0,10 Punkte ungeklärt |
| **B6: Ausgangslage 2024 als 2028** | **neu in v3.6.** Schuldenquote, effektiver Zins und Verteidigung stammen aus 2024. Entscheidung des Verfassers nötig (siehe v3.6) |
| **Rechenskripte** | `pfad.py` ist seit v3.6 als **Rekonstruktion** vorhanden (23 von 23 Referenzwerten), nicht als Original. Es fehlen weiterhin `basis.py`, `final.py`, `tilgung.py`, `aufschlag.py` (Band II) und alle Skripte bis v3.4. Aus diesem Repository reproduzierbar ist der Zeitpfad ab den Parametern, nicht die Herleitung der Parameter (Kalibrierung, COFOG-Anteile, 6,44 und 10,35) |
| **Herleitung von 6,44 und 10,35** | `a_ohne_verteidigung_zins_bip_2028` ist eine Restgröße der Dividende 2028, `b_fachaufgaben_bip_2028` stammt aus Band II (v3.2, COFOG). Die COFOG-Abrufe liegen nicht vor, die Shell erreicht `ec.europa.eu` nicht |
| **Nicht eingetragene Größen** | Mindestquote, Obergrenze von A, Höchstbedarf, territorialer Aufschlag: Bezugsjahr oder Bezugsgröße fehlt. Siehe `daten/aggregate/nicht-eingetragen.md`, Abschnitt A |
| **Rohdaten und Abrufe nicht reproduzierbar** | Die Eurostat-Abrufe (zehn Einzelabrufe COFOG GF02, `gov_10a_exp`, `gov_10a_taxag`, `nama_10_gdp`, `demo_gind`) sind im Logbuch nur benannt, die Abrufergebnisse liegen nicht vor. Die Shell erreicht `ec.europa.eu` nicht (Logbuch v3.1) |
| **Prüfstand der Logbuch-Abschrift** | Band I ab v0.10 und Band II sind Abschriften ohne Vergleichsquelle, siehe `HERKUNFT.md` |
| Alle offenen Punkte aus Band I (Abschnitt 7) und Band II (Zusatz zu v3.5) | unverändert, soweit hier nicht genannt |
