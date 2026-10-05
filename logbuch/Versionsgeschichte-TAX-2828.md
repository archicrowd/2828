# TAX 28:28 — Logbuch, Datenbestand und Rechenplan

**Dieses Dokument ist die Rückseite der Webseite.** Die Seite zeigt das Modell,
dieses Logbuch zeigt, woher jede Zahl kommt, wann sie sich geändert hat und was
sich als falsch erwiesen hat. Es wird bei jeder Rechnung fortgeschrieben, nicht
bei jeder Textänderung.

Stand: 1. Oktober 2026 · Modellstand **v1.0**

---

## 1 | Wozu

Drei Zwecke, in dieser Reihenfolge.

**Nachvollziehbarkeit.** Jede Zahl auf der Webseite muss auf eine Quelle und ein
Skript zurückführbar sein. Wo das nicht geht, steht „Annahme".

**Fehlergedächtnis.** Abschnitt 4 führt die Korrekturen mit. Ein Entwurf, dessen
Irrtümer offen liegen, ist überprüfbar; einer, der immer schon richtig war, ist
es nicht. Für Fachgespräche ist dieser Abschnitt der wertvollste.

**Arbeitsstand.** Abschnitt 6 sagt, was als Nächstes gerechnet wird und was
ohne Datenvertrag nicht geht.

---

## 2 | Versionsschema

`MAJOR.MINOR.PATCH`

| | wann | Beispiel |
|---|---|---|
| **MAJOR** | eine der zehn Positionen ändert sich inhaltlich | Satz, Bemessungsgrundlage oder Mechanik einer Position |
| **MINOR** | eine Annahme wird durch eine Quelle ersetzt, oder eine neue Rechnung kommt hinzu | Position 05 erhält eine Größenordnung aus OECD-Daten |
| **PATCH** | Korrektur ohne inhaltliche Änderung | Rechenfehler, falsche Quelle, Textwiderspruch |

Jede Version nennt: Datum · was sich geändert hat · welche Datenquelle ·
welche Zahl sich bewegt hat · wodurch es auffiel.

Der Modellstand gehört sichtbar auf die Webseite. Vorschlag: im Fußbereich
`Modellstand v0.4 · 1. Oktober 2026` mit Verweis auf dieses Logbuch.

---

## 3 | Versionen

### v0.1 — Grundentwurf Deutschland
Zehn Positionen, Rechner für den Rechtsstand 2026, Aufkommen und Haushalt über
die Einkommensverteilung in drei Rechenwegen (optimistisch, vorsichtig,
Rezession). Dividende 515 € als 50 % des Existenzminimums.
*Charakter der Zahlen: Modellschätzung, keine Mikrosimulation.*

### v0.2 — Länderdateien, zehn Staaten
Übertragung der Regel auf Deutschland, Frankreich, Spanien, die Niederlande,
Irland, Belgien, Österreich, Dänemark, Slowenien und Estland.
Anker: Dividende als 21,4 % des nationalen Median-Äquivalenzeinkommens.
Quellen: IWF WEO April 2026 · EZB-Durchschnittskurs 2026 (0,8611 EUR/USD) ·
Median-Äquivalenzeinkommen über eine WKO-Zusammenstellung der EU-SILC-Daten
(Sekundärquelle, als solche gekennzeichnet) · Tax Foundation 2026 ·
Eurostat-Euroindikatoren 22. April 2026.
Für Irland ist **GNI\*** die Bezugsgröße (334,0 gegen 602,4 Mrd. € BIP, CSO
Ireland), nicht das BIP.
*Ergebnis: 257,2 Mio. Einwohner, 13.271 Mrd. €, rund 70 % der
EU-Wirtschaftsleistung. Dividenden 306 € (EE) bis 651 € (AT).*

### v0.3 — Position 05, erste Datenprüfung (Taxplorer)
Firmengenaue öffentliche Länderberichte, EU Tax Observatory.
**Belastbar:** Gewinn je beschäftigter Person und effektiver Satz — Luxemburg
1,30 Mio. € je Kopf bei 5,0 %, Deutschland 57.000 € bei 22,8 %.
**Nicht belastbar:** die Aufkommenswirkung. Für die Umsatzzerlegung liefern nur
rund 70 Konzern-Jahre lückenlose Angaben, und in jedem Land tragen drei
Konzerne mehr als die Gesamtsumme (Österreich 353 %, Spanien 276 %).
Frankreichs +18,6 Mrd. € sind im Kern ein einziger Konzern.
*Folge: Position 05 blieb unbelegt. Neu aufgenommen wurde der unbequeme
Einzelbefund, dass Sitzländer exportstarker Konzerne bei Besteuerung am
Kundenort verlieren (Dänemark).*

### v0.4 — Position 05, Größenordnung mit Quelle (OECD)
OECD *Corporate Tax Statistics*, Datensatz `DSD_CBCR@DF_CBCRI` (1.1), Jahr
2023, 63 Sitzstaaten, 244 Tätigkeitsländer, 1.367.305 Beobachtungen.

**Erstens**, die Fehlstellung ist amtlich belegt: Britische Jungferninseln
30,2 Mio. USD Gewinn je beschäftigter Person bei 2,1 % — Deutschland
44.345 USD bei 22,5 %. Staatenlose Einheiten weisen 267 Mrd. USD Gewinn aus,
mehr als Deutschland, besteuert mit 0,8 %.

**Zweitens**, der Klub gewinnt netto fast nichts: +15,5 Mrd. USD, weil Irland
(−94,9), Belgien (−24,2) und Dänemark (−17,2) gegen Deutschland (+54,4),
Frankreich (+44,7) und die Niederlande (+38,0) stehen. Größter Gewinner wären
die USA mit +553 Mrd. USD.

**Drittens**, und das ist die Änderung am Entwurf: **Position 05 finanziert den
Satz von 28 %, nicht umgekehrt.** Im deutschen Konzernsegment bringt die
Zerlegung +13,1 Mrd. €, während der Satz von 28 % gegenüber heute 3,1 bis
8,4 Mrd. € kostet — Deutschland ist unter den zehn das einzige Land, dessen
Unternehmensteuersatz **sinkt**. Netto +4,7 bis +10,0 Mrd. €.

**Viertens**, der österreichische Effektivsatz ist unabhängig bestätigt:
Taxplorer 12,5 %, OECD 12,0 %. Zwei Quellen, zwei Methoden.

*Skripte: `analyse_tab1.py`, `wirkung_28.py`. Ergebnisse: `t1-laender.csv`,
`t1-zerlegung.csv`, `t1-panelAI.csv`, `t1-wirkung-28.csv`, `t1-saetze-welt.csv`.*

### v0.5 — R6: Position 05 geprüft, Belegstand auf der Seite
Zwei Teile.

**Rechnung (R6).** Dieselbe Zerlegung unter vier Schlüsseln und über acht Jahre,
normiert auf den festen Kreis der **26 Sitzstaaten, die durchgängig melden**.
Drei Ergebnisse:

*Die Zahl aus v0.4 war zu hoch.* Die Mengenwirkung für Deutschland beträgt im
Median von acht Jahren **+8 Mrd. €, Spanne +5 bis +14** — 2023 lag am oberen
Rand. Zusammen mit der Satzwirkung (−3,1 bis −8,4) ergibt sich für die deutsche
Unternehmensseite ein mittlerer Fall von **+2 bis +3 Mrd. €**, im ungünstigsten
Fall **−5**, im günstigsten **+11**. Ein Verlust ist also nicht ausgeschlossen.

*Der Schlüssel ist fast gleichgültig, das Jahr nicht.* Einfaktor gegen
Dreifaktor ändert Deutschlands Ergebnis um rund 2 Mrd. €; die Streuung über die
Jahre ist dreimal so groß. In keinem Jahr und unter keinem Schlüssel ist das
Vorzeichen negativ.

*Der reine Zielort-Schlüssel ist der schwächere und der unfairere.* Er nimmt den
Niedrigsteuerplätzen nur etwa halb so viel ab wie der Dreifaktor-Schlüssel
(−31 gegen −58 Mrd. € im Median) und verschiebt Aufkommen von den
Produktionsländern zu den Absatzmärkten: Indonesien (−37 → +45), Mexiko
(−41 → +17), Indien (−36 → +22) und Vietnam (−2 → +36) wechseln das Vorzeichen,
die USA verlieren +193 Mrd. € ihres Zuflusses. Dafür ist der Zielort-Schlüssel
**einseitig durchsetzbar** — wo die eigene Kundschaft sitzt, kann ein Staat
selbst feststellen, Beschäftigte und Anlagen in Vietnam nicht. Ein vertretbarer
Tausch, der aber benannt werden muss.

Der Klub der zehn bleibt bei null: Median +0,5 (Einfaktor) bzw. −7,3
(Dreifaktor), Spanne −11 bis +18. **Der Klub ist kein Aufkommensargument,
sondern ein Rechtsdurchsetzungsargument.**

**Webseite.** Neue Sektion `#evidence` („Belegstand"), zehn Zeilen, je Position
Behauptung, Stufe und Grundlage. Vier Stufen, **doppelt kodiert** als
Blockanzeige und als Wort, damit sie nicht allein von der Farbe abhängen. Unter
720 px wird die Tabelle zu Blöcken, weil die Begründungsspalte sonst aus dem
Bild scrollt. Modellstand im Fußbereich. Alle acht Sprachfassungen, neu
gebaut und bei 390 und 1280 px geprüft: kein Seitenüberlauf, kein
abgeschnittener Text.

Belegstand heute: **1× belegt** (Position 08), **1× Größenordnung**
(Position 05), **4× Modellrechnung** (01, 02, 06, 10), **4× offen**
(03, 04, 07, 09).

*Skripte: `r6_faktoren.py`, `r6_normiert.py`, `patch_beleg.py`. Ergebnisse:
`r6-varianten-2023.csv`, `r6-zeitreihe-einfaktor.csv`,
`r6-zeitreihe-dreifaktor.csv`, `r6-fester-kreis.csv`,
`r6-produktionslaender.csv`. Bericht: `Befund-R6.md`.*

### v0.6 — R1: Position 03 belegt
Erste Rechnung auf amtlichen Primärdaten: Erbschaft- und Schenkungsteuerstatistik
2024 (Statistischer Bericht 73611), 245.540 festgesetzte Erwerbe, 113,2 Mrd. €
Erwerbswert. Drei Ergebnisse.

**Der effektive Satz fällt, wo er steigen müsste.** Wer 100.000 bis 200.000 €
erbt, zahlt effektiv **13,5 %**; wer 10 bis 20 Mio. € erbt, **9,6 %**. Der
Verschonungsanteil steigt monoton von 6,4 % bei kleinen Erwerben auf **61,9 %**
in der Klasse 10 bis 20 Mio. Oberhalb von 20 Mio. springt der Satz auf 25,3 %,
weil die Regelverschonung bei 26 Mio. je Erwerber gedeckelt ist (§ 13a Abs. 1,
darüber § 28a). Die Daten bilden die gesetzliche Schwelle sichtbar ab.

**Was die Verschonung kostet.** § 13a nimmt **17,1 Mrd. €** aus der Bemessung —
**79,4 % des gesamten übertragenen Betriebsvermögens** und 51,9 % aller Abzüge.
Entgangene Steuer je nach unterstelltem Satz **3,9 bis 5,1 Mrd. € im Jahr**,
also **30 bis 39 % des gesamten Aufkommens** von 13,3 Mrd.

**Position 03 brächte +3,3 bis +4,8 Mrd. € (+24 bis +36 %)** — weniger als
erwartet. Grund: die Bemessungsgrundlage ist mit 64,6 Mrd. € fast genauso gross
wie heute (64,7), nur anders zusammengesetzt. Der Mehrertrag kommt allein aus
dem Satz. **Die eigentliche Stellschraube ist der Freibetrag:** ein
einheitlicher Betrag von 400.000 € je Erwerb kostet gegenüber der heutigen
Staffelung rund **3,8 Mrd. € im Jahr** — mehr, als die Abschaffung der
Betriebsvermögensverschonung einbringt. Steuerklasse II und III (Geschwister,
Nichten, Neffen, Nichtverwandte) sind 76,7 % der Erbfälle und haben heute
20.000 € Freibetrag. Das ist eine Entwurfsentscheidung, keine Rechengrösse, und
sie gehört benannt.

**Verteilungswirkung:** 159.057 Erwerbe unter 300.000 € zahlen heute zusammen
1,82 Mrd. € und wären vollständig frei. Zwischen 500.000 € und 20 Mio.
verdoppelt sich die Last etwa. Über 20 Mio. ändert sich fast nichts.

**Zeitreihe:** Das Aufkommen hat sich seit 2007 verdreifacht (4,22 → 13,30 Mrd.),
der effektive Satz stieg von 15,0 auf 20,5 %. 2024 ist kein Ausreisser. Anders
als bei Position 05 muss hier nicht über Jahre geglättet werden.

**Webseite:** Position 03 wechselt in der Belegstand-Tabelle von „offen" auf
„belegt", Stufe 3. Belegstand jetzt: **2× belegt** (03, 08), 1× Größenordnung
(05), 4× Modellrechnung (01, 02, 06, 10), **3× offen** (04, 07, 09).

**Nachtrag R1b, Freibetragskurve.** Exakt auf den amtlichen Klassengrenzen:
100 Tsd → 24,16 Mrd · 200 Tsd → 20,98 · 300 Tsd → 18,51 · 500 Tsd → 14,98.
Die Entwurfsfassung mit 400 Tsd liegt bei 16,54. Die Halbierung auf 200.000 €
brächte **+4,4 Mrd. €** und zöge 39.456 Erwerbe zusätzlich in die Steuer.
Geprüft wurde auch eine Formelbindung an das Existenzminimum nach dem Muster
von Position 08: **28 × 12.348 € = 345.744 €** ergäbe 17,57 Mrd. Der Gewinn
läge nicht in der Höhe, sondern darin, dass der Freibetrag eine abgeleitete
statt einer gesetzten Grösse wäre.

**Nachtrag R1c, Stundung.** Siehe offene Punkte.

*Skripte: `r1_erbschaft.py`, `r1b_freibetrag.py`, `r1c_stundung.py`.
Ergebnisse: `r1-groessenklassen.csv`, `r1-kette.csv`, `r1b-freibetragskurve.csv`,
`r1c-stundung-barwerte.csv`.
Bericht: `Befund-R1.md`. Quelle: Statistisches Bundesamt, Statistischer Bericht
73611, Erbschaft- und Schenkungsteuer 2024.*

### v0.7 — Verschonung durch Stundung ersetzt (Position 03)
**Entwurfsentscheidung.** Die Verschonungsausnahmen entfallen vollständig. An
ihre Stelle tritt eine Stundung für **Betriebe und Immobilien** mit einer
Zinsleiter:

> Zins im Jahr t = Refinanzierungssatz des Staates + (t−1)/9 × Marge,
> ab Jahr 10 voller marktüblicher Kreditzins. Kein Erlass; der offene Rest
> bleibt als Last auf dem Gegenstand und wird bei Verkauf fällig.

**Warum die Untergrenze der Refinanzierungssatz ist.** Dort verliert der Staat
nichts. Der Verzicht beschränkt sich auf die **Bankmarge** der ersten Jahre —
und die ist sachlich entbehrlich, weil die Forderung dinglich gesichert und das
Ausfallrisiko des Staates gering ist. Eine Bank verlangt die Marge für ein
Risiko, das hier nicht besteht.

**Was es kostet.** Mittleres Szenario (Basis 3,0 %, Marge 2,0 %), Tilgung in
zehn Raten: der Staat erhält im Barwert **103,1 je 100** — er gewinnt, weil der
Zins ab der Mitte über seiner Refinanzierung liegt. Der Verzicht gegenüber
vollem Marktzins ab Jahr 1 beträgt 6,7 je 100, auf 10 Mrd. € stundungsfähiger
Steuer also **rund 0,7 Mrd. € im Jahr** — gegen 3,9 bis 5,1 Mrd., die die heutige
Verschonung kostet. **Die Stundung ist damit keine Verschonung unter anderem
Namen.** Zum Vergleich die zinslose Variante aus R1c: dort 15 % (10 J) bis 26 %
(20 J) Erlass.

**Was die Erbin zahlt.** Geerbtes Haus 500.000 €, Freibetrag 400.000 €,
Steuer 28.000 €, zehn Raten: **280 € im Monat**. Bei 800.000 € sind es 1.122 €.
Tragbar ohne Verkauf, und kein Geschenk.

**Was offen bleibt.** Die Übergangslücke von rund 4,5 Mrd. € im Jahr über zehn
Jahre (kumuliert 45 Mrd.) ist eine reine Zeitverschiebung, muss aber im
Haushalt der ersten Jahre stehen. Und § 234 AO setzt für Stundungszinsen einen
festen Satz; eine an einen Referenzzins gebundene Leiter ist vermutlich
robuster — nach dem Urteil des Bundesverfassungsgerichts von 2021 zu § 233a AO —,
das ist aber an der Rechtsquelle zu prüfen.

**Webseite.** Position 03 neu formuliert in allen acht Sprachen, Belegstand
ergänzt, Anhang um die Stundungsparameter erweitert. Nebenbei behoben: die
Mehrwertsteuer-Leiter in Position 06 schnitt „A+ · 5 %" ab (60 px Text in einem
52-px-Kasten); die Leiter ist um 8 px verbreitert, der Abstand von 12 px je
Stufe bleibt.

*Skript: `r1d_zinsleiter.py`. Ergebnisse: `r1d-zinsleiter.csv`, `r1d-beispiele.csv`.*

### v0.8 — Stundungsrechner zu Position 03
Kein zweiter Rechner neben dem Einkommensrechner, sondern ein kleiner Block am
Fuss der Positionen: ein Schieber „Wert des Erbes", vier Ergebniszeilen und die
zehn Jahresraten als Balken. Überschrift: **„Position 03 ausprobiert: Muss das
Haus verkauft werden?"**

**Begründung der Grösse.** Der Hauptrechner beantwortet eine Frage, die fast
jeden betrifft. Erwerbe über 400.000 € gibt es 69.518 im Jahr — von 245.540
überhaupt festgesetzten. Ein gleichgewichtiger zweiter Rechner hätte um
Aufmerksamkeit konkurriert, ohne eine vergleichbare Zielgruppe zu haben. Der
kleine Block sitzt dafür genau dort, wo der Einwand entsteht.

**Rechenweg** identisch mit `r1d_zinsleiter.py`; die Ausgabe wurde gegen die
Python-Fassung geprüft und stimmt auf den Euro: bei 500.000 € Erbe 28.000 €
Steuer, erste Rate 3.640 €, letzte 2.940 €, Zinsen 5.647 €, **280 € im Monat**.

**Zwei Fehler nebenbei behoben.** Erstens gaben `es-ES` und `et-EE` vierstellige
Beträge ohne Tausendertrennung aus („3640 €" neben „29.120 €" in derselben
Spalte). Das ist korrektes Gebietsschema für Fliesstext, in einer Zahlenspalte
aber irreführend; `eur()` erzwingt jetzt `useGrouping:'always'`, was alle
Sprachfassungen betrifft. Zweitens war die linke Spalte des Rechners halb leer —
dort stehen jetzt die zehn Jahresraten als Balken, die zeigen, dass die Rate
sinkt, obwohl der Zinssatz steigt.

Geprüft: acht Sprachen, 390 und 1280 px, null Beanstandungen; zehn Balken,
monoton fallend, keine Skriptfehler.

*Patch: `patch_erbrechner.py`.*

### v0.9 — Freibetrag halbiert, Bezug geändert (Position 03)
**Zwei Entscheidungen.**

*Höhe:* 400.000 → **200.000 € je Erwerb**. Aufkommen **16,54 → 20,98 Mrd. €**,
also **+7,7 Mrd. € gegenüber heute** statt +3,3. Besteuert werden 108.974 statt
69.518 Erwerbe, 44,4 % statt 28,3 % aller festgesetzten. 200.000 € ist eine
exakte Klassengrenze der amtlichen Statistik — der Wert braucht keine
Interpolation.

*Bezug:* „je Kind" → **„je Erwerb"**. Alle Rechnungen seit R1 unterstellen einen
einheitlichen Betrag für jede erbende Person; die Seite sagte bisher etwas
anderes. Heute sind die Freibeträge gestaffelt (500.000 Ehegatten, 400.000
Kinder, 200.000 Enkel, 20.000 übrige). Steuerklasse II und III — Geschwister,
Nichten, Neffen, Nichtverwandte — sind 76,7 % der Erbfälle; für sie ist auch der
halbierte Betrag noch das Zehnfache des heutigen.

**Der Anlass war eine Rückfrage, nicht eine Rechnung.** Die Logik, die die
Halbierung trägt, stammt aus v0.7: die Stundung hat das stärkste Argument für
einen hohen Freibetrag entwertet. Er war da, damit niemand das Elternhaus
verkaufen muss — das leistet jetzt die Stundung, und zwar gezielter, weil sie
streckt statt pauschal zu entlasten.

**Die Grössenordnung, die das sichtbar macht:** der Freibetrag von 400.000 €
kostete 12,4 Mrd. € im Jahr — fast das gesamte heutige Aufkommen und rund
dreimal so viel wie die Betriebsvermögensverschonung. Die Halbierung holt
4,4 Mrd. € davon zurück.

**Was das für Erbende heisst.** Geerbtes Haus 500.000 €: Steuer 84.000 € statt
28.000 €, **841 € im Monat** über zehn Jahre statt 280 €. Bei 400.000 €:
56.000 € Steuer, 561 € im Monat. Unter 200.000 € bleibt alles frei.

**Webseite.** Position 03, Rechner, Belegstand und Anhang in allen acht Sprachen
umgestellt; der Schieber beginnt jetzt bei 50.000 € und startet bei 400.000 €,
damit die Freigrenze sichtbar wird. Geprüft: Rechnerausgabe gegen die
Python-Fassung, 390 und 1280 px, null Beanstandungen.

**Offen bleibt die Verwaltungsfrage.** Die Statistik erfasst nur die 245.540
Erwerbe, die das Finanzamt erreichen. Wie viele Erbfälle bei 200.000 € neu zu
veranlagen wären, geht aus ihr nicht hervor.

*Patch: `patch_frei200.py`. Kurve: `r1b-freibetragskurve.csv`.*

### v0.10 — Stundung nach Modell B, Rechner entfernt
**Die Stundung ist festgelegt:** laufend zu zahlen ist **nur der Zins**. Wer auch
den nicht tragen kann, dem wird er dem offenen Betrag zugeschlagen. Der offene
Betrag bleibt als Last auf dem geerbten Gegenstand und wird fällig bei Verkauf
oder Weitergabe. Die Zinsleiter bleibt unverändert.

**Anlass war ein Widerspruch, den der Verfasser gefunden hat.** Der Rechner
tilgte in zehn Jahren (Modell A), der Seitentext sagte „der offene Rest bleibt
als Last auf dem Gegenstand" (Modell B). Beides stand auf derselben Seite. Für
ein Erbe von 1 Mio. € ergab A 2.243 € im Monat, B 747 € — beide Rechnungen
richtig, die Entwürfe verschieden. Siehe Korrektur 15.

**Barwert für den Staat unter Modell B**, je 100 € gestundeter Steuer, abgezinst
mit dem Refinanzierungssatz: **102 nach fünf, 108 nach zehn, 121 nach zwanzig
Jahren.** Kein Verlust, und je länger gestundet wird, desto mehr — anders als
bei einer zinslosen Stundung, die mit jedem Jahr Geld kostet. Die Zahl im
Anhang stammte aus Modell A und ist ersetzt.

**Der Rechner ist entfernt.** Er setzte die lesende Person in den Stuhl des
Zahlenden; jede Zahl war eine Belastung für sie. Das ist der Rahmen, in dem
Erbschaftsteuerreformen verlieren. Nach der Halbierung des Freibetrags in v0.9
lieferte er zudem Belege gegen die Position, für die er gebaut war: aus „280 €
im Monat" wurden 841 €. An seine Stelle tritt ein Regeltext ohne jeden
Beispielbetrag — drei Absätze, die sagen, was gilt und warum es fair ist.

**Befund-Kachel 2** behält die Überschrift „~40 % der Konzerngewinne in
Steueroasen", bekommt darunter aber eine eigene, aktuelle Zahl statt einer
Erläuterung: 30,2 Mio. USD Gewinn je beschäftigter Person auf den Britischen
Jungferninseln bei 2,1 %, in Deutschland 44.345 USD. Quelle im Kleingedruckten.

**Der Anhang** war veraltet und widersprach der Belegstand-Tabelle auf
derselben Seite: Position 05 stand dort noch unter „noch nicht belegt", die
Erbschaftsrechnung fehlte ganz. Abschnitt 4 heißt jetzt „Belegstand", ist nach
denselben vier Stufen gegliedert und nennt die Quellen mit Tabellennummern.

Geprüft: acht Sprachen, 390 und 1280 px, null Beanstandungen; keine
verwaisten Stile, keine Skriptfehler, keine Beträge im Regeltext.

*Patches: `patch_modellB.py`, Kachel in `patch`-Form im Logbuch.*

### v1.0 — Position 07 europäisch gefasst
**Erste Hauptversion.** Nach dem Versionsschema ändert sich eine der zehn
Positionen inhaltlich: der CO₂-Preis ist keine nationale Setzung mehr.

**Der Anlass steht im Gesetz.** Das Dritte BEHG-Änderungsgesetz sieht in
§ 10 Abs. 3 S. 2 Nr. 4 ab 2028 einen marktbasierten Preis nach dem Durchschnitt
der EU-ETS-1-Versteigerungen vor; der nationale Brennstoffemissionshandel geht
in den ETS 2 über, dessen Start die Verordnung (EU) 2026/667 vom 11. März 2026
um ein Jahr verschoben hat. **Ein nationaler Preis von 100 oder 150 € ab 2028
ist mit geltendem Recht unvereinbar.** Position 07 fordert deshalb einen
gemeinsamen Pfad entlang der vereinbarten Klimaziele — eine Aufgabe des Klubs.

**Was jetzt belegt ist.** § 44 Abs. 2 BEHG legt die Emissionsmengen bis 2030
fest: 301,0 → 180,6 Mio. t, −40 %. § 10 Abs. 2 S. 4 setzt für 2026 und 2027
einen Preiskorridor von 55 bis 65 €; das Gesetz **friert den Preis für 2027 ein**
statt ihn zu erhöhen (Koalitionsausschuss vom 12. Mai 2026). Aufkommen im
nationalen Brennstoffemissionshandel 2026: **13,9 bis 16,4 Mrd. €**, bei 100 €
wären es 25,2, bei 150 € 37,9.

**Die Schere:** bei festem Preis von 150 € fällt das Aufkommen von 2026 bis 2030
um **28,4 %**, weil die gesetzliche Menge sinkt. Wer die Dividende daraus speist,
finanziert sie aus einer schrumpfenden Quelle. Das gehört in die Haushaltsrechnung.

**Die Subventionen sind nicht, wofür sie gehalten werden.** Vom UBA-Betrag von
65,4 Mrd. € (Datenjahr 2018) wären nach eigener Zuordnung rund **47 Mrd.**
aufkommenswirksam; **12,7 Mrd. sind Entlastungen im Strompreis, die den Haushalt
nie erreichen**, 4,8 Mrd. sind Ausgaben. Mehrere Posten sind seither entfallen:
die EEG-Umlage 2022 (Besondere Ausgleichsregelung und Eigenstromprivileg,
zusammen 9,1 Mrd.), der Spitzenausgleich 2023, die Steinkohlesubventionen 2018.
Die Zahl bleibt deshalb offen, bis eine aktuelle Fassung vorliegt.

**Zum EU-ETS 1** liegen jetzt Kennzahlen vor (DEHSt): 1,01 Mrd. t EU-weit 2025,
−51 % seit 2005; Deutschland 1.794 Anlagen mit 264 Mio. t, −49 %. Die deutschen
Versteigerungserlöse daraus sind nicht enthalten und fehlen weiter.

**Belegstand:** 2× belegt (03, 08), **2× Größenordnung (05, 07)**, 4× Modellrechnung
(01, 02, 06, 10), **2× offen (04, 09)**.

*Skripte: `r4_co2.py`, `r4b_subventionen.py`, `patch_pos07.py`.
Quellen: Drittes BEHG-Änderungsgesetz; Umweltbundesamt 2021, Umweltschädliche
Subventionen in Deutschland, Datenjahr 2018; DEHSt, Kennzahlen zum
Emissionshandel 2025.*

### v2.0 — Haushaltsabgleich, Tarif aus dem Pfad begründet

**Zweite Hauptversion.** Drei Positionen ändern sich inhaltlich: 01 und 06
bekommen höhere mittlere Stufen, 04 verliert die ihr zugeschriebene
Mehreinnahme. Die Sätze stehen jetzt nicht mehr als Setzung da, sondern als
Ergebnis einer Haushaltsrechnung.

**Die Korrekturen aus R1 bis R6, zusammengeführt.** Sechs Posten des
Gesamtmodells wurden auf die geprüften Werte zurückgesetzt, alle nach unten:
Erbschaft 35,9 → 21,0 (Freibetrag 200.000 €); CO₂ 70,0 → 33,0 (Preiskorridor
des BEHG statt 100–150 €); Bodenwertabgabe 20,0 → 0,0; Unternehmen
157,6 → 152,0; Vermögen 32,7 → 30,0. Zusammen **−80,2 Mrd. €.** Der Saldo des
ersten Jahres fällt damit von +67,3 auf **−12,9 Mrd. €.**

**Der Pfad trägt das trotzdem — und das war der entscheidende Befund.** Ich
hatte zunächst gegen einen Zielsaldo von +42 Mrd. € im ersten Jahr gerechnet
und daraus eine Lücke von 54,9 Mrd. abgeleitet. Das Kriterium war falsch
gewählt: +42 Mrd. ist das Investitionsziel *eines* Jahres (1 % des BIP), nicht
die Bedingung, unter der die Regel funktioniert. Investiert wird nach Regel 1
aus dem Fonds, der mit 100 Mrd. € startet, nicht aus dem Jahressaldo. Geprüft
wurde deshalb der Pfad über 20 Jahre im Modell selbst. Ohne Gegenmaßnahme:
**kein Lückenjahr** in den ersten beiden Szenarien, **fünf im Stress-Szenario**,
Investitionsquote 91,1 % (vorsichtig) bzw. 42,4 % (Stress).

**Der echte Bedarf ist 36,1 Mrd. €,** nicht 54,9 — bisektiert gegen zwei
Kriterien: kein Lückenjahr in allen drei Szenarien (24,0 Mrd.) und
Investitionsquote 99 % im vorsichtigen Szenario (36,1 Mrd.).

**Die Entscheidung: +3 Punkte auf die bewegten Stufen.**

| | bisher | neu |
|---|---|---|
| Einkommensteuer | 0 / 9 / 16 / 21 / 26 / 28 % | **0 / 9 / 19 / 24 / 27 / 28 %** |
| Mehrwertsteuer | 5 / 11 / 17 / 22 / 28 % | **5 / 11 / 20 / 25 / 28 %** |
| Effektivsatz MwSt | 20,0 % | **21,5 %** |

Das bringt **38,9 Mrd. €** bei einem Bedarf von 36,1. Danach hat **kein
Szenario ein Lückenjahr**, das vorsichtige erreicht 99,5 % des
Investitionsziels, die Stufe 55 % trägt sich dort ab 2032. Unverändert: 0 %
bis 12.348 €, Eingangsstufe 9 %, MwSt-Grundstufe 5 %, Stufe A 11 % —
und der Spitzensatz 28 %.

**Ein gleichmäßiger Aufschlag, nicht das Optimum.** Eine Rastersuche findet
Kombinationen, die 36,1 genauer treffen, erzeugt aber schiefe Tarife: Stufen,
die fast zusammenfallen (25 und 26 % nebeneinander), oder eine einzelne
Mehrwertsteuerstufe mit fünf Punkten Sprung. Für ein Modell, dessen Anspruch
Erklärbarkeit ist, ist der gleichmäßige Aufschlag die bessere Wahl; der
Überschuss von 2,8 Mrd. geht in den Fonds. Die beiden Flanken sind gerechnet
und stehen in `tarif_wahl.py`: **ESt +4 / MwSt +2** belastet unten am wenigsten
(0,86 %), hat aber einen Sprung von 9 auf 20 % bei 25.000 €; **ESt +2 / MwSt +4**
ist der glatteste Tarif, belastet unten aber am stärksten. Gesetzt ist die Mitte.

**Der harte Befund: die Zusatzlast ist nicht progressiv, und kann es nicht sein.**
Von 335 Kombinationen, die das ursprüngliche Ziel erreichten, trug **keine
einzige** die Zusatzlast progressiv — auch nicht unter dem schwächeren
Kriterium „unten nicht mehr als oben". Der Grund ist strukturell: die oberste
Gruppe zahlt den Spitzensatz, und der bleibt bei 28 %. Eine Anhebung der Stufen
*darunter* trifft sie nur mit einem festen Betrag — die zweite Stufe um drei
Punkte anzuheben kostet jeden oberhalb von 25.000 € dieselben 380 €, für ein
Einkommen von 26.180 € sind das 1,45 %, für 306.180 € noch 0,12 %. **Wenn der
Spitzensatz feststeht, kann zusätzliches Aufkommen aus der Einkommensteuer nur
aus der Mitte kommen,** und das ist relativ zur Spitze zwangsläufig regressiv.
Die Mehrwertsteuer verstärkt es über die mit dem Einkommen fallende Konsumquote.
Die Zusatzlast dieses Schritts liegt zwischen **0,86 %** oben und **2,45 %** in
der Mitte.

**Netto bleibt die Reform progressiv.** Gegen das heutige Recht gerechnet
(Mehrwertsteuer 16,5 → 21,5 %): +5.514 € bei 8.000 € Markteinkommen (+68,9 %),
+4.579 € bei 20.000, +283 € bei 69.000, **−1.470 € bei 105.000** und −10.057 €
bei 300.000. Der Kipppunkt liegt zwischen 69.000 und 105.000 € Markteinkommen.

**Die Alternative, die diesen Preis vermeidet, ist gerechnet, aber nicht
gesetzt.** 20 der 36,1 Mrd. gehen auf eine einzige Korrektur zurück: die
Bodenwertabgabe. Würde Position 04 als Abgabe *über* dem heutigen
Grundsteuerniveau gefasst — 1 % auf 3.529 Mrd. € Bodenwert ergäbe rund
35 Mrd., also +20 —, sänke der Bedarf auf 16,1 Mrd., und die mittleren Stufen
müssten **gar nicht** steigen; die Mehrwertsteuer bliebe unberührt und die Last
unten bei 0,00 %. Träger wäre der Boden, der nicht ausweichen kann, und nach
R5b liegen 87 % des Bodenwerts auf 17 % der Fläche. **Das verlangt aber eine
Änderung an Position 04 und ist eine Entscheidung, die nicht beim Rechnen
anfällt.** Sie liegt vor.

**Beamte und Selbständige: Gleichbehandlung, nicht Gegenfinanzierung.** Die
Belege sprechen hier gegen die naheliegende Erwartung. Nach **IW Köln** kostet
die Einbeziehung der rund 1,9 Mio. Beamten den Staat **10 bis 20 Mrd. € im
Jahr** — er zahlt als Arbeitgeber, und langfristig steigen die Ausgaben mit,
bei ungünstigerer Altersstruktur. Nach **DIW** kosten die Pensionen schon heute
**über 63 Mrd. €** (≈1,5 % des BIP, Durchschnittspension 3.240 € gegen 1.599 €
Durchschnittsrente); der Vorschlag lautet deshalb, nur *neu* Eingestellte nicht
mehr zu verbeamten. Die Beiträge der rund 3,5 Mio. noch nicht
pflichtversicherten Selbständigen bringen überschlägig **29 Mrd. €** — aber als
Einführungsgewinn, dem Ansprüche folgen. Saldo überschlägig +19 Mrd.
**Dieser Betrag ist im Abgleich nicht angerechnet.** Wer ihn als dauerhafte
Gegenfinanzierung buchte, rechnete sich reich; das ist ein Fehler, den die
Debatte regelmäßig macht.

**Position 04 erstmals gerechnet, Stufe 0 → 2.** Bodenwert 3.529 Mrd. €, davon
87 % auf 17 % der Fläche; ein Satz von 0,22 bis 0,44 % trägt die heutigen
15,5 Mrd. € Grundsteuer. Position 04 ist damit ein Umbau bei gleichem
Aufkommen — die im Modell gebuchten 20 Mrd. € waren eine Doppelzählung.

**Belegstand:** 2× belegt (03, 08), **3× Größenordnung (04, 05, 07)**,
4× Modellrechnung (01, 02, 06, 10), **1× offen (09)**. Vorher `1130212301`,
jetzt `1132212301`.

*Skripte: `haushalt/abgleich.py`, `haushalt/pfad.py` (R9), `haushalt/tarif.py`
und `tarif_wahl.py` (R10, R10b), `haushalt/netto.py` (R10c),
`site/patch_tarif.py`, `patch_ev.py`, `patch_anhang.py`.
Quellen: IW Köln 2025 zur Einbeziehung der Beamten; DIW 2025 zu Pensionslasten
und Selbständigen; im Übrigen die Quellen aus v0.5 bis v1.0.*

---

### v3.0 — Position 04 zweiteilig, und das Audit der Gesamtlogik

**Dritte Hauptversion.** Position 04 wird zweiteilig und erfasst erstmals
Verkaufsgewinne. Dazu das erste Audit, das nicht einzelne Positionen prüft,
sondern den Gesamtrahmen — mit Befunden, die grösser sind als alle bisher
gefundenen Fehler zusammen.

**Position 04a** Grundsteuer nur auf den Boden, alle zwei Jahre neu bewertet,
Ansatz unter dem Bewertungswert (dänisches Vorsichtsprinzip), aufkommensneutral.
**Position 04b** Verkaufsgewinn 28 %, **ohne Behaltefrist**, ganzer Gewinn,
**kein Abzug der Grundsteuer**, Umzugsaufschub bei Ersatzbeschaffung binnen zwei
Jahren, **einmalig 300.000 € beim endgültigen Ausstieg**, Verlustverrechnung,
Schritt auf den Verkehrswert im Erbfall. Mehraufkommen **4,1 Mrd €**.

**Die Begründung, die der Nutzer geliefert hat,** und sie entkräftet meinen
eigenen Einwand vom 2. Oktober: Lage und Wertzuwachs sind im Kaufpreis
eingepreist, aber nur soweit sie im Kaufzeitpunkt bekannt waren. Was danach
hinzukommt, entsteht durch öffentliche Investition. Daraus folgt, dass die
**französische Abschmelzung und der Schweizer Besitzesdauerrabatt falsch herum
laufen** — sie entlasten gerade den Zuwachs, der erfasst werden soll.
Übernommen wurden deshalb nur der Schweizer Zuschlag für kurze Haltedauer und
die Ersatzbeschaffung, dazu der dänische Bewertungsrhythmus.

**§ 154 BauGB zeigt: das Prinzip gilt in Deutschland schon.** Der Eigentümer im
Sanierungsgebiet hat „einen Ausgleichsbetrag in Geld zu entrichten, der der
durch die Sanierung bedingten Erhöhung des Bodenwerts seines Grundstücks
entspricht"; Absatz 5 erlaubt die Umwandlung in ein Darlehen, wenn ihm die
Zahlung bei Fälligkeit nicht zuzumuten ist. Das ist die Stundung aus Position 03,
seit Jahrzehnten geltendes Recht.

**Zielgenauigkeit, an acht Fällen auf der amtlichen Preisreihe gerechnet.**
Der einmalige Freibetrag von 300.000 € stellt Sachsen, die NRW-Kleinstadt und
die Münchner Altbauwohnung frei; es zahlen das Münchner Umland-Haus (81.540 €
auf 591.213 € Gewinn) und das vermietete Hamburger Objekt (254.031 €). Der
Freibetrag wirkt als regionaler und zeitlicher Filter, ohne eine Region zu
nennen — bei einer Baulandspreizung von 15 bis 2.000 € je m² (Faktor 133)
entsteht ein Gewinn über 300.000 € ländlich kaum, in München beim Normalfall.

**DAS AUDIT — fünf Befunde auf dem Gesamtrahmen**

1. **Die Verhältnisse stimmen, die Euro-Beträge nicht.** BIP0 = 4.200 Mrd gegen
   amtlich fortgeschrieben 4.884; Einkommensteuer auf 284 kalibriert gegen
   amtlich 341,1 Mrd. Beides etwa gleich stark zu niedrig — das Modell rechnet
   auf dem Niveau 2021/22 und ist als 2028 etikettiert. Gegenprobe: mit dem
   amtlichen BIP fällt die Investitionsquote nur von 99,4 auf 98,1 %, kein
   Szenario bekommt ein Lückenjahr. **Der Pfad ist robust, die Beträge sind es
   nicht.**
2. **Zwei unbelegte Blöcke tragen die Bilanz:** „Sonstige Steuern" 165 Mrd und
   „Basisausgaben + Zuschuss + Härtefall" 696 Mrd, zusammen **861 Mrd** = 73 %
   der Einnahmen und 59 % der Ausgaben. Alles in R1 bis R16 Geprüfte summiert
   sich auf 240 Mrd. **Die Belegstand-Tabelle bewertet zehn Positionen, aber
   die zwei grössten Zahlen des Modells sind keine Position.**
3. **Die Sozialversicherung fehlt ganz** — 707,7 Mrd Beiträge, und Position 10
   senkt den Satz von 41,3 auf 28 bzw. 18 %. Ungedeckt wären 168 bzw. 339 Mrd;
   im Modell steht ein Zuschuss von 60. Das tragende Gegenargument — die
   Dividende ersetzt Leistungen — steckt vermutlich in den 596 Mrd, steht aber
   nirgends.
4. **Vier heutige Steuern über 50,6 Mrd sind nicht zugeordnet:** Soli 12,9,
   Grunderwerbsteuer 15,1, Kirchensteuer ~13, KFZ-Steuer 9,6. Die
   Grunderwerbsteuer ist der dringendste Fall, weil sie dem Umzugsaufschub aus
   04b direkt widerspricht.
5. **Wer das Geld bekommt, wurde nie gefragt.** Position 05 ersetzt die
   Gewerbesteuer (75,3), 04a die Grundsteuer (16,0) — die gesamte kommunale
   Steuerautonomie. Nach WD 4-049/19 ist die Gewerbesteuer verfassungsrechtlich
   nicht gesichert und darf ersetzt werden, aber Art. 28 Abs. 2 S. 3 GG verlangt
   eine Quelle mit Hebesatzrecht. Das Konzept stellt keine bereit. Die Antwort
   wäre 04a nach estnischem Muster — und damit genau die Variante b) mit 1 %
   Satz und rund 35 Mrd.

**Was das Audit NICHT gefunden hat:** einen Konstruktionsfehler im Prinzip. Der
eine Satz hält über alle geprüften Interaktionen, die Positionen widersprechen
sich nicht, die Haushaltsregel ist robust. Die Lücken liegen in der
Dokumentation und in der Vollständigkeit der Bilanz, nicht in der Logik.

**Belegstand:** unverändert `1132212301`. Das Audit ändert keine Positionsstufe
— es zeigt, dass die Tabelle den Rahmen nicht abdeckt.

*Skripte: `immo/r11`–`r16`, `audit/a1`–`a4`. Dokument: „TAX 28:28 — Audit der
Gesamtlogik". Quellen: BMF-Monatsbericht Dezember 2025; BMF-Steuerschätzung
Oktober 2025; Destatis Steuereinnahmen und PM 309/2025; VGRdL BIP Februar 2026;
Destatis GENESIS 61262-0001; BBSR Deutschlandatlas; BAS, BMG, BA; § 23 EStG;
§ 154 BauGB; WD 4-049/19; OECD Housing Taxation; Kanton Zürich StB 216.3.*

---

### v3.1 — Der Rahmen wird europäisch: zwei Ebenen, A und B

**Richtungsentscheidung des Nutzers, nicht Ergebnis einer Rechnung.** Das Konzept
war zu nah am deutschen Steuerrecht. Es wird neu gefasst als Rahmen für eine
idealisierte europäische Kernzone — gedanklich der Mittelwert des Klubs — mit nur
zwei Verwaltungsebenen: **A** für den Klub (Wirtschaftsraum, Verteidigung,
Anerkennung von Bildung), **B** für die Kommunen (Aufgaben des täglichen Umfelds
in eigener Verantwortung). Kreis, Bundesland und Nation entfallen als
Steuerebenen. **Die Sozialabgaben werden aus dem Konzept gestrichen** und auf
Einzelnen, lokale Strukturen und Tarifautonomie verwiesen.

**Erstmals eigene Daten zur Ausgabenseite des Klubs.** Sechs Prüfungen lang ging
es nur um Steuern; jetzt die COFOG-Funktionsrechnung und die Ebenengliederung
aller zehn Staaten aus Eurostat 2024. Klub: **12,157 Bio. € BIP, 255,1 Mio
Menschen, 49,5 % Staatsquote**.

**Die Zuordnung, aus dem Jetzt erzeugt.** Regel: der kommunale Teil einer Funktion
ist das, was die Kommunen heute dafür ausgeben, der Rest geht an A.
- **Ebene A: 7,12 % des BIP** = 866 Mrd € = 3.394 €/Kopf. Größter Posten der
  Wirtschaftsraum mit 3,75, dann Verteidigung 1,40.
- **Ebene B: 11,37 % des BIP** = 1.382 Mrd € = 5.419 €/Kopf. Größter Posten die
  Schulen mit 4,44. **B ist die größere Ebene**, nicht A.
- **Außerhalb des Rahmens: Sozialschutz 20,09 %** = 2.443 Mrd €.
- **Offen: Gesundheit 7,75 %** und der Altschuldendienst 1,20 %.

**Dänemark ist der Präzedenzfall für drei der vier Strukturentscheidungen.**
Sozialbeiträge 0,7 % des BIP gegen 17,5 in Deutschland, bei gleich großem
Sozialschutz — finanziert aus Einkommensteuern von 31,0 % des BIP. Kommunalebene
31,2 % des BIP, die größte im Klub. Und die Strukturreform zum 1.1.2007: **271 auf
98 Gemeinden**, **14 Kreise abgeschafft**, Nachfolgeregionen **ohne Steuerhoheit**,
Mindestgröße 20.000 Einwohner. Finanziert werden die Gemeinden über eine
kommunale Einkommensteuer mit eigenem Satz (89 % ihres Steueraufkommens, Schnitt
25 %) und die Bodensteuer (11 %), ausgeglichen über Bedarf gegen Aufkommen bei
Durchschnittssatz.

**Der Schlüssel, und was ihn bestimmt.** Nicht die Aufgabenverteilung, sondern die
Digitaldividende: ohne sie A:B = 39:61, mit ihr bei A 62:38. Sie ist mit 11,51 %
des BIP größer als alle A-Aufgaben zusammen. Empfehlung in drei Teilen:
Bodenwertabgabe mit Hebesatz (trägt 7 % von B), **fester Vertragsanteil von 34 %**
am gemeinsamen Aufkommen, dänischer Bedarfsausgleich zwischen den Gemeinden.
Der Übergang ist eine Buchung: jede Aufgabe nimmt ihr heutiges Budget mit — B
wächst um **4,03 Punkte oder 490 Mrd €**, genau das, was Land und Zentrale heute
für Schule, Polizei und Gericht ausgeben.

**Die Rechnung geht knapp auf.** Hauptvariante (Gesundheit privat, Dividende bei A)
braucht 31,20 % des BIP, das Modell erhebt 27,91 % — Lücke **3,29 Punkte**. Die
beiden Einsparpfade (wegfallende Verwaltung 1,96 Punkte, estnisches
Verwaltungsniveau 0,94) bringen höchstens 2,90. Restlücke **0,4 bis 3,3 Punkte**.
Zum ersten Mal eine Lücke in tragbarer Größenordnung.

**Drei Auditbefunde lösen sich auf.** Die vier ungeklärten Steuern (50,6 Mrd)
entfallen mit der Ebene, der sie gehören. Die Frage nach Art. 28 Abs. 2 S. 3 GG ist
beantwortet und zugleich gegenstandslos. Die fehlende Sozialversicherung fehlt
nicht mehr, sie ist gestrichen. **Ein Befund wird schärfer:** der unbelegte
696-Mrd-Block hat jetzt einen Maßstab — A+B kosten für Deutschland zu Klubsätzen
**800 Mrd €**, das Modell liegt 104 Mrd darunter.

**Neu und ungelöst: die Altschulden.** Löst man die nationale Steuerebene auf, muss
die Schuld irgendwohin. Die Streuung im Klub reicht von 24,1 bis 115,6 % des BIP,
Faktor 4,8. Vergemeinschaftung wäre ein Transfer mehrerer A-Jahresbudgets;
territoriale Zuordnung hält die nationale Ebene fiskalisch am Leben.

**Und ein Zielkonflikt, den das Konzept bisher umgeht:** ein einheitlicher Satz von
28 % und kommunale Hebesatzautonomie sind nicht gleichzeitig möglich. Dänemark hat
sich für die Autonomie entschieden, der Name dieses Konzepts für die
Einheitlichkeit.

**Belegstand:** Position 10 entfällt. Die Tabelle braucht eine neue Zeile für die
Ebenenzuordnung, die bisher in keiner Position vorkommt.

*Skripte: `rahmen/daten.py`. Dokument: „TAX 28:28 — Rahmenstruktur A und B".
Quellen: Eurostat gov_10a_exp, gov_10a_taxag, nama_10_gdp, demo_gind (alle 2024);
NATO Hague Summit Declaration 25.6.2025; EU-Kommission MFF 2028–2034 vom
16.7.2025; Local Government Denmark; UCLG/OECD Länderprofil Dänemark; Oates,
Fiscal Federalism 1972.*

*Datenweg: `ec.europa.eu` ist für die Shell dieser Sitzung gesperrt (403 auf
CONNECT); die Eurostat-API war nur über die Web-Werkzeuge erreichbar. Kontrolle
über Summenidentitäten je Land — alle zwanzig Prüfungen gingen mit höchstens
0,2 Punkten Rundungsrest auf.*

---

### v3.2 — Parität, und der Umbau wird freiwillig

**Zweite Richtungsentscheidung des Nutzers.** Der Entwurf aus v3.1 wird in drei
Punkten geschärft, und alle drei sind Konstruktionsentscheidungen, keine
Rechenergebnisse:

1. **A zieht alle Steuern ein** und gibt den Teil an B weiter, der außerhalb der
   A-Aufgaben liegt. Keine getrennten Steuerhoheiten, keine Zerlegung, kein
   jährlicher Verteilungsstreit.
2. **Die Mittelebenen werden nicht abgeschafft, sondern freiwillig.** B kann aus
   seinem Anteil Abgaben an Pflichtverbände, Kreise, Länder und Nationen leisten
   — wenn es deren Leistung will. Damit wird aus einer Verfassungsrevolution eine
   Haushaltsentscheidung, und das „Abholen" kann in der heutigen Struktur
   geschehen. Der Anreiz trägt den Umbau, nicht der Zwang.
3. **Pflichtverband bei kleiner Größe, aber Wahlfreiheit des Partners** —
   regional benachbart oder **strukturverwandt**. Zwei Hafenstädte dürfen
   zusammengehen statt zweier Nachbarn ohne Gemeinsamkeit.

**Parität stellt sich von selbst ein.** Der Nutzer fragte, ob eine „gewisse
Parität" zwischen A und B möglich sei — auch in den Aufgaben. Sie fällt aus
seinen eigenen drei Begründungen heraus:

| Schritt | A | B | A:B |
| --- | --- | --- | --- |
| Ausgangslage v3.1 | 7,12 | 11,37 | 39:61 |
| Verteidigung auf Haager 3,5 % | 9,22 | 11,37 | 45:55 |
| Übergeordnete Polizei (1/3 von GF0301) | 9,51 | 11,08 | 46:54 |
| Hochschulen (GF0904) an A | **9,94** | **10,35** | **49:51** |

Verteidigungsfähigkeit, einheitliche Durchsetzung und bedingungslose Mobilität
sind zusammen 4,53 Punkte des BIP — genau die Größenordnung, die A fehlte.
Abstand am Ende: **0,41 Punkte oder 50 Mrd €**, weniger als die Unsicherheit der
vier geschätzten A-Posten.

**Die Digitaldividende wird dadurch zum freien Parameter.** Feste Last: A 9,94 +
B 10,35 + Altschuldendienst 1,20 = **21,49 % des BIP**. Alles darüber ist
Dividende:

| Steuerquote | Dividende | € je Monat |
| --- | --- | --- |
| 27,9 % (bisheriges Modellniveau) | 6,42 % | 255 |
| 31,2 % | 9,71 % | 386 |
| **33,0 %** | **11,51 %** | **457 (heutige Projekthöhe)** |
| 35,0 % | 13,51 % | 537 |

**Der ehrlichste Befund des Tages: die Gesamtlast bleibt gleich.** Heute erheben
die zehn 40,76 % des BIP (25,95 Steuern + 14,88 Beiträge). Der Entwurf braucht
33,00 % Steuern plus 7,75 Punkte kommunal organisierte Gesundheit außerhalb des
Steuertopfs = **40,75 %**. Der Umbau verschiebt nicht die Höhe der Abgaben,
sondern ihre Verfassung. Das ist belastbarer als jedes Entlastungsversprechen —
und es ist die Aussage, mit der das Konzept öffentlich bestehen muss.

**Der Anreiz, quantifiziert.** Die Verwaltung der Mittelebenen kostet 1,96 % des
BIP oder 934 € je Kopf — **19 % des B-Budgets**. Eine Gemeinde mit 20.000
Einwohnern verhandelt damit jährlich über **18,7 Mio €**, die heute ohne ihr Zutun
bei Kreis und Land verbleiben.

**Artikel 113 AEUV ist die Eintrittsschwelle, nicht eine Nebenbedingung.** Der
Vertragstext verlangt für Steuerharmonisierung ausdrücklich, dass der Rat
„acting unanimously in accordance with a special legislative procedure"
beschließt. Die Forderung des Nutzers nach Handlungsfähigkeit statt
Einstimmigkeit ist im geltenden EU-Rahmen also nicht darstellbar. Entweder
Vertragsänderung — die wiederum Einstimmigkeit aller 27 braucht — oder der Klub
konstituiert sich außerhalb. Verstärkte Zusammenarbeit (mindestens neun Staaten,
der Klub hat zehn) als Zwischenweg ist **ungeprüft** und gehört vor einen
Europarechtler.

**Klub ohne die Neutralen gerechnet.** Ohne Irland und Österreich: 11,10 statt
12,16 Bio € BIP, 240,5 statt 255,1 Mio Menschen. Die Staatsquote steigt sogar auf
50,6 %, weil mit Irland die Konzernbuchungsverzerrung verschwindet. Der Klub
verliert 8,7 % Wirtschaftsleistung und gewinnt Handlungsfähigkeit.

**Belegstand:** unverändert. Die Parität ist eine Setzung mit Begründung, keine
Messung — vier A-Posten von zusammen 1,18 Punkten (17 % der Ebene A) sind
Schätzungen.

*Neue Daten: GF0301 Polizei (0,87 % BIP) und GF0904 Hochschulen (0,74 %) für alle
zehn. Skripte: `rahmen/daten.py`. Lieferung: `Rahmenstruktur-A-und-B.docx`,
vier Seiten, zur Korrektur. Quellen zusätzlich: Artikel 113 AEUV, konsolidierte
Fassung.*

---

### v3.3 — Kalibrierung behoben, und was dabei auffiel

**Drei übertragene Aufgaben.** Der Nutzer stellt die EU-Verträge und die Zuordnung
der Altschulden zurück (Sache der Communities beim Umstieg), überträgt die weitere
Berechnung und verweist die Mikrosimulation an Dritte. Vorrang hat ein sauberes,
nachvollziehbar kommunizierbares Konzept.

**Die Kalibrierung ist behoben — der älteste Auditbefund.** Neue Basis aus
geprüften Werten: Eurostat-Ist 2024 (4.329,0 Mrd) fortgeschrieben mit den
nominalen Raten der Frühjahrsprojektion vom 22.4.2026 (+3,3 / +2,8 / +3,8 %),
2028 vorsichtig mit +3,0 % → **BIP0 = 4.914,9 statt 4.200 Mrd, Faktor 1,1702**.
Da alle Positionen mit demselben Faktor skalieren, ändert sich keine Quote: die
Einnahmen bleiben 27,91 % des BIP, Pfad und Investitionsquote bleiben unberührt.
Der Fehler saß in der Basis, nicht in der Mechanik — wie vermutet.

**Der 696-Mrd-Block ist geklärt, aber anders als gedacht.** Umbasiert sind es
814,5 Mrd. Der Aufgabenkatalog der Rahmenstruktur kostet **1.056,2 Mrd** —
Lücke **+241,7 Mrd oder 4,92 Punkte des BIP**. Davon erklärt die Haager Zusage
103,2 Mrd (Verteidigung 3,5 statt 1,4 %), die übrigen 138,5 Mrd sind **die Ebene
A, die das Modell nie enthielt**, weil es ein nationales Modell war. Der Block war
nicht zu niedrig gegriffen, sondern zu eng gefasst.

**Neuer Befund, den niemand gesucht hatte: die Refinanzierungswelle.** Der Klub
schuldet 9,537 Bio € (78,4 % BIP) und zahlt dafür 146 Mrd Zinsen — ein effektiver
Satz von **1,53 %** gegen einen Marktzins von **2,78 %**. Die 125 Basispunkte
Differenz sind kein Vorteil, sondern eine Verzögerung: bei rund 7,5 Jahren
Restlaufzeit steigt der Zinsdienst auf **265 Mrd oder 2,18 % des BIP**, ein
Anstieg von 119 Mrd. Das frisst **39 € Dividende je Kopf und Monat**.

**Die Zinsgarantie, gerechnet.** Renditespreizung der zehn 2024: 2,30 % (DK) bis
3,55 % (EE), 125 Basispunkte. Eine Garantie bei 2,50 % spart **31,5 Mrd im Jahr**
und fängt 27 % des Zinsanstiegs ab. Das tragende Argument ist neu: **A verfügt
über 1.354 Mrd Eigeneinnahmen = 14,2 % des Schuldenstands**, gegen 1,6 % beim
heutigen EU-Haushalt — das 8,8-Fache der Deckung. Die unbequeme Seite:
Deutschland und Dänemark gewinnen nichts und haften mit, Frankreich und Spanien
nehmen 83 % des Vorteils. **Die Garantie vermeidet die Vergemeinschaftung nicht,
sie kleidet sie anders ein** — senkt aber die Gesamtkosten, statt nur umzuverteilen.

**Und daraus folgt die Entscheidung, die das Konzept bisher nicht treffen musste.**
Feste Last mit Zinsanstieg und Garantie: 22,21 % des BIP. Drei Wege:

| Weg | Steuerquote | Dividende (DE) |
| --- | --- | --- |
| A Satz halten, Dividende senken | 27,91 % | 280 € |
| **B Dividende halten, Quote heben** | **33,72 %** | **565 €** |
| C Verteidigung auf heutigem Stand | 27,91 % | 383 € |

Empfehlung: **Weg B.** 33,7 % stehen gegen eine heutige Gesamtlast von 40,8 % aus
Steuern und Beiträgen. Die Aussage „andere Abgaben statt weniger, dafür eine
Dividende" hält jeder Prüfung stand. Die Aussage „28 % und 457 €" hält ihr nicht
stand.

**Belegstand:** Kalibrierung von „offen" auf „belegt". Der unbelegte Ausgabenblock
von „offen" auf „erklärt". Neu offen: die Restlaufzeit der Schulden (mit 7,5 Jahren
als Erfahrungswert angesetzt, nicht erhoben).

*Skripte: `neu/`, `zins/schuld.py`. Lieferung: `Rechenstand-Oktober.docx`, drei
Seiten. Quellen zusätzlich: Eurostat gov_10dd_edpt1 und irt_lt_mcby_a (2024);
Frühjahrsprojektion der Bundesregierung vom 22.4.2026; US Census Bureau
NST-EST2025-POP.*

---

### v3.4 — Verteidigungsziel 2,5 %, Altschuld geloest, und die 28 traegt

**Zwei Nutzerentscheidungen, beide verbessern die Rechnung.**

**1. Das Verteidigungsziel sinkt von 3,5 auf 2,5 % und schliesst digitale Souveraenitaet
ein.** Der Nutzer stellt die 3,5 % als politisch diktierte Zahl in Frage. Die Pruefung
gibt ihm teilweise recht, und zwar aus dem Haager Text selbst: Die Erklaerung teilt ihre
5 % in **mindestens 3,5 % Kernverteidigung und bis zu 1,5 %** fuer, woertlich, „defend our
networks, ensure our civil preparedness and resilience, unleash innovation, and strengthen
our defence industrial base". Netzverteidigung und Innovation stehen dort also schon
ausserhalb der Kernverteidigung — dass digitale Souveraenitaet zur Verteidigung zaehlt, ist
die Systematik des Dokuments, nicht eine Umdeutung.

Zusammensetzung der 2,50 %: Kernverteidigung heute 1,40 + Aufwuchs 0,50 + Netze/Cloud/
Chips 0,35 + eigene autonome Intelligenz 0,25. **Digitalprogramm 0,60 % = 85 Mrd im Jahr**,
mit der Grundlagenforschung zusammen 195 Mrd.

**Folge: A faellt von 9,94 auf 8,94 % des BIP, das Verhaeltnis von 49:51 auf 46:54.** Die
Paritaet war eine Beobachtung, kein Konstruktionsziel — sie geht mit dem niedrigeren Ziel
verloren, und das ist der Preis.

**2. Die Deckelung wird zur Schranke statt zur Zuteilung.** A's Bedarf ist nicht konstant:
9,04 % des BIP in 2028, Hoechststand 10,49 % in 2035 (= 38,7 % des Einzugs), danach
fallend. Deshalb **Obergrenze 40 %, nicht fester Schluessel**. A nimmt nur, was die Aufgaben
kosten; der Rest fliesst durch an B und die Dividende. Eine Obergrenze, die nicht
ausgeschoepft werden muss, kann nicht zum Anspruch werden.

**DER ENTSCHEIDENDE BEFUND: ueber die Zeit gerechnet traegt der Satz von 28 %.** Die
statische Rechnung war zu streng, weil sie die Haager Zusage sofort verbuchte — sie gilt
aber fuer 2035.

| Jahr | Verteidigung | Schuld | Zinsdienst | Dividende Klub | Deutschland |
| --- | --- | --- | --- | --- | --- |
| 2028 | 1,40 % | 78,4 % | 1,20 % | **396 €** | 418 € |
| 2035 | 2,50 % | 63,7 % | 1,55 % | 404 € | 426 € |
| 2040 | 2,50 % | 55,0 % | 1,37 % | 480 € | 507 € |
| 2060 | 2,50 % | 30,4 % | 0,76 % | **941 €** | 993 € |

**Kein Einbruch, in keinem Jahr negativ — auch nicht bei 1,5 % Wachstum.** Beim Ziel von
3,5 % faellt die Dividende bis 2035 auf 347 € und erreicht den Startwert erst 2039 wieder;
der Unterschied betraegt dauerhaft 66 € im Monat.

**Und die Gesamtlast sinkt tatsaechlich:** 27,91 % Steuern + 7,75 % Gesundheit ausserhalb
= **35,66 % gegen heute 40,76 %**, eine Entlastung von 5,10 Punkten oder 726 Mrd im Jahr.
Der Tausch gegen die hoehere Quote ist bezifferbar: 5,09 Punkte weniger Last kosten 237 €
Dividende im Monat (33 % ergaebe 633 € statt 396).

**Die Altschulden sind geloest, ohne die Communities zu beruehren.** A uebernimmt den
Zinsdienst — Praezedenzfall ist Hamiltons Schuldenuebernahme von 1790, Besteuerungsrecht
gegen Schuldenuebernahme. Ohne Ausgleich waere das ein Dauertransfer von +364 EUR je Kopf
(Frankreich) bis −1.045 EUR (Irland). Deshalb ein **territorialer Aufschlag auf A's Anteil,
der sich klubweit auf null summiert** und ueber 30 Jahre abschmilzt. **Er erreicht die
Gemeinden nicht:** jede bekommt ueberall dieselben Betraege je Einwohner und je Kind.

**Nebenbefund, der die Erzaehlung aendert: die Schulden arbeiten sich von selbst ab.** Bei
ausgeglichenem Haushalt bleibt der Bestand in Euro konstant, das BIP waechst, die Quote
faellt von 78,4 auf 30,4 % — ohne einen Tilgungseuro. **Aktive Tilgung ist kontraproduktiv:**
0,50 % des BIP kosten 24 € Dividende im Monat und haben sich bis 2050 nicht zurueckverdient.
Das gilt, solange der Zins unter dem Wachstum liegt — und genau das sicherzustellen ist der
eigentliche Wert der Garantie, nicht die 10 € Dividende.

**Zum Namen:** „Europaeische Gemeinschaften" im Plural ist der amtliche Name der EGKS, EWG
und EURATOM vor Maastricht, auf Englisch ebenso. Vorschlag: **Freie Gemeinschaften Europas**
— dieselbe Aussage ohne die Kollision.

**Belegstand:** Verteidigungsannahme von „gesetzt" auf „aus dem Haager Text begruendet".
Altschulden von „ungeloest" auf „Mechanismus benannt, Frist offen". Neu offen: die
Zusammensetzung der 2,5 % ist eine Setzung und fachlich zu pruefen.

*Skripte: `pfad/dyn.py`. Lieferung: `Rahmenstruktur-A-und-B-v3.docx` und die Webseite in
zweiter Fassung mit Zeitdiagramm.*

---

---

## 4 | Korrekturen

Chronologisch, mit Ursache. Alle bisher von mir (dem KI-System) gemacht und
bemerkt; das ist kein Qualitätsnachweis, sondern ein Hinweis darauf, dass eine
externe Prüfung fehlt.

| # | Was war falsch | Richtig | Wodurch auffiel |
|---|---|---|---|
| 1 | Belgien „verliert durch Gewinnverlagerung" | Tørsløv, Wier und Zucman führen Belgien als eine von fünf EU-Steueroasen (−15 Mrd. USD, 2016) | Gegenlesen der Primärquelle |
| 2 | Ohne Irland sei Position 05 „nur halb wirksam" | Besteuerung am Kundenort wirkt einseitig; Irlands Beitritt bringt Rechtsfrieden, nicht Wirksamkeit | innerer Widerspruch im Seitentext |
| 3 | Estlands BIP aus einem neueren IWF-Jahrgang als die übrigen neun | alle zehn auf WEO April 2026 vereinheitlicht | Quervergleich der Jahrgänge; Deutschlands Dividendenquote 10,7 → 10,2 % des BIP |
| 4 | GETTSIM scheitere, weil es nicht auf PyPI liege | pip erreicht hier **keinen** Index, auch `numpy` nicht | Gegentest mit einem Standardpaket |
| 5 | „Die USA fehlen in den OECD-Daten" | gilt für Tabelle II (50 Sitzstaaten), nicht für Tabelle I (63, mit USA) | Abgleich beider Tabellen |
| 6 | Effektivsatz-Perzentile als Prozent gelesen | die Quelle liefert Anteile; Median 0,1 statt 14,3 % | Plausibilitätsprüfung gegen den Aggregatsatz |
| 7 | Effektive Sätze von 78 % (LU) und −235 % (UK) | Verlust-Teilgruppen im Nenner; Neurechnung auf Panel A(i) wie bei der OECD | Unplausibilität der Werte |
| 8 | „Deutschland gewinnt +15 Mrd. USD durch Position 05" | Steuer aus Panel A(i) mit Basis aus Panel `_T` multipliziert. Konsistent: +4,7 bis +10,0 Mrd. € | Rückfrage nach der Wirkung auf den 28er-Satz |
| 9 | Estlands „24:24:24" als Entwurfsentscheidung dargestellt | verteidigungsfinanziert und befristet bis 2028 | Recherche zur Entstehung |
| 10 | „Position 05 bringt Deutschland +13,1 Mrd. €" | das war 2023, ein Spitzenjahr. Median über acht Jahre: **+8**, Spanne +5 bis +14 | Zeitreihe im festen Kreis (R6) |
| 11 | Im vollen Panel erschien 2022 für Deutschland ein Minus von 3,7 Mrd. € | Abdeckungsartefakt: im festen Kreis ist es ein Plus von 4,7. Kein Jahr ist negativ | Normierung auf durchgängig meldende Sitzstaaten |
| 12 | Freibetragskurve mit Gleichverteilung innerhalb der Größenklassen gerechnet | ergab bei hohen Freibeträgen ein **steigendes** Aufkommen — unmöglich. Ersetzt durch eine Pareto-Anpassung, die den beobachteten Klassenmittelwert trifft. In der Klasse 500 Tsd bis 2,5 Mio liegt der Mittelwert bei 899 Tsd, die Gleichverteilung unterstellt 1.500 | Monotonieprüfung der eigenen Ergebnisreihe |
| 16 | Anhang nannte Position 05 unter „noch nicht belegt" | widersprach der Belegstand-Tabelle auf derselben Seite; Abschnitt 4 neu gefasst | Durchgang durch die deutsche Fassung |
| 15 | Rechner tilgte in zehn Jahren, Seitentext sagte „Last auf dem Gegenstand" | zwei verschiedene Entwürfe, beide von mir geschrieben. Entschieden: Modell B | der Verfasser rechnete nach und kam auf andere Werte |
| 14 | Freibetragskurve: `es-ES` und `et-EE` zeigten vierstellige Beträge ungetrennt | korrektes Gebietsschema für Fliesstext, in einer Zahlenspalte aber irreführend. `eur()` erzwingt jetzt die Gruppierung | Sichtprüfung des Rechners in allen acht Sprachen |
| 13 | „Festgesetzte Steuer 13,285 Mrd. €" als das verwendet, was der Staat erhält | Bruttowert. Das Bundesamt hält fest, dass die Erlasse nach der Verschonungsbedarfsprüfung (§ 28a ErbStG) **nicht enthalten** sind. Das Mehraufkommen aus Position 03 ist eher zu niedrig angesetzt | Erläuterungen zur Statistik gelesen |

| 15 | Zielsaldo von +42 Mrd. € im ersten Jahr als Kriterium verwendet und daraus eine Lücke von 54,9 Mrd. abgeleitet | Falsches Kriterium. +42 Mrd. ist das Investitionsziel *eines* Jahres; investiert wird nach Regel 1 aus dem Fonds (Start 100 Mrd.), nicht aus dem Jahressaldo. Der echte Bedarf ist **36,1 Mrd.** — ein Drittel weniger | Den Modellkern (`simuliere`) gelesen, bevor ich den Tarif festlegte |
| 16 | Bodenwertabgabe mit +20 Mrd. € als Mehreinnahme gebucht | Doppelzählung. Position 04 beschreibt einen Umbau der Grundsteuer **bei gleichem Aufkommen**; dann sind es null. Die 20 Mrd. wären nur bei einem höheren Satz zu holen — das wäre eine andere Position | R5b gegen den Wortlaut von Position 04 gelesen |
| 17 | Nettoposition inkonsistent gerechnet: Einkommensteuer gegen den Rechtsstand 2025, Mehrwertsteuer aber gegen den alten 28:28-Satz von 20,0 % | Der Schritt von heute 16,5 % auf 20,0 % fehlte. Korrekt gegen 16,5 % gerechnet liegt der Kipppunkt zwischen 69.000 und 105.000 € statt darüber; die Richtung des Befundes bleibt, seine Lage nicht | Abgleich mit dem Rechner-JS der Seite, das korrekt gegen 16,5 % rechnet |
| 18 | Gleichmäßiger Tarifaufschlag auf alle mittleren Stufen angewandt | Lief in den Spitzensatz hinein: 26 + 3 = 29 > 28. Die fünfte Stufe ist jetzt bei 27 % gedeckelt, die MwSt-Stufe C bei 26 % | Eigene Ausgabe gelesen |
| 19 | Erste Mehrkriteriensuche ließ doppelte Sätze zu und wählte `0/9/18/27/28/28` | Das verkürzt die sechsstufige Leiter faktisch auf fünf und ändert damit die Tarifstruktur. Strikte Monotonie wird jetzt verlangt | Eigene Ausgabe gelesen |
| 20 | Skripte als R7/R8 bezeichnet | Kollidierte mit dem Rechenplan, in dem R7 die Monte-Carlo-Rechnung und R8 die Dezilverteilung ist. Umbenannt in R9 (Pfad) und R10 (Tarif) | Rechenplan beim Schreiben dieses Eintrags gegengelesen |

| 21 | Kachel versprach „die laufend gezahlte Grundsteuer wird abgezogen", und ich hatte das mit Doppelbesteuerung begründet | Falsch. Die Grundsteuer besteuert den Bestand, der Verkaufsgewinn den Zuwachs — zwei Grundlagen, wie Dividende und Kursgewinn. Bei Vermietung ist sie schon Werbungskosten, bei Eigennutzung greift sie auf einen sonst unbesteuerten Nutzungswert. Kein Abzug | Nutzerfrage: „Ist die volle Abzugsfähigkeit in der Sache richtig?" |
| 22 | Den Abzug in keiner Fallrechnung von R13 bis R15 eingepreist, obwohl er in der Kachel stand | Kumulierte Grundsteuer ist 2,8 bis 8,9 % des Gewinns, der Abzug hätte die Steuer der Fälle um 5,4 % gesenkt | Dieselbe Nutzerfrage: „Hast du das für deine Beispiele eingepreist?" |
| 23 | In R13 den Bodenanteil als Bemessungsgrundlage für 04b empfohlen, prinzipientreu und besser gezielt — ohne das Aufkommen zu rechnen | Der Bodenanteil von 40 % frisst die Basisverbreiterung auf: Fallabdeckung fast dreifach, aber Satz von 42 auf 28 %. Die Bodenvariante VERLIERT 1,1 Mrd gegenüber heute. Ganzer Gewinn mit höherem Freibetrag schützt dieselben Fälle und bringt +4,3 | Aufkommen in R14 nachgerechnet |
| 24 | Kapitalisierung der Bodenabgabe als zweite Belastung dargestellt | Der Preisrückgang IST der Barwert der künftigen Abgaben. Wer hält, zahlt die Zahlungen; wer verkauft, trägt den Preisverlust. Niemand beides. Der Befund daraus betrifft das Modell: 04a und 04b sind nicht addierbar, rund 4,7 % Abschlag | Beim Schreiben der Begründung selbst gemerkt |
| 25 | Vorhergesagt, der Pfad bricht mit dem amtlichen BIP | Er bricht nicht. Investitionsquote 99,4 auf 98,1 %, keine Lückenjahre. Investiert wird aus dem Überschuss über dem Puffer, nicht bis zum Ziel — ein höheres BIP hebt beide und hebt sich auf | Den Lauf gemacht statt die Behauptung stehen zu lassen |
| 26 | Den Gesamtrahmen des Modells in 16 Prüfungen nie gegen die amtliche Statistik gestellt | BIP 14 % zu niedrig, Einkommensteuer 16,7 %, zwei unbelegte Blöcke von 861 Mrd, Sozialversicherung fehlt ganz | Nutzerauftrag: „Haben wir Zahlen und Systeme die in ihrer Gänze logisch sind" |

| 27 | Die ungedeckten 168 bis 339 Mrd der Sozialversicherung als größtes Loch des Modells geführt | Kein Loch, sondern eine Grenze, die der Nutzer jetzt gezogen hat. Die Arithmetik des Audits stimmte, die Einordnung als Fehler nicht | Nutzerentscheidung: Sozialabgaben aus dem Konzept streichen |
| 28 | Sechs Prüfungen lang nur die Steuerseite des Klubs erhoben, nie die Ausgabenseite | Erst die COFOG-Daten zeigen, dass Ebene B mit 11,4 % des BIP größer ist als Ebene A mit 7,1 — die Grundstruktur des Konzepts war unbekannt, während über Freibeträge gestritten wurde | Nutzerauftrag, die Rahmenstruktur aus dem Jetzt zu entwickeln |
| 29 | 04a als offene Wahl zwischen aufkommensneutral und Hebesatzrecht dargestellt | In der Rahmenstruktur ist es keine Wahl: B hat keine andere eigene Steuer, also ist der hohe Satz Bedingung und nicht Variante | Beim Rechnen des Eigenfinanzierungsgrades (7 %) selbst gemerkt |
| 30 | Angenommen, eine saubere Zuordnung nach Mobilität würde den Schlüssel ersetzen | Sie erzeugt ihn: nach dem Mobilitätsprinzip fallen 25 der 26 Steuerpunkte an A. Die Zuordnungslehre ist die Ursache des Schlüsselproblems, nicht seine Alternative | Beim Schreiben der Steuerzuordnung |

| 31 | Erwartet, dass Parität zwischen A und B eine Setzung erzwingt | Sie fällt aus den drei Begründungen des Nutzers heraus: 49:51 bei einem Abstand von 0,41 Punkten. Nicht gelegt, sondern gerechnet | Nutzerfrage nach „einer gewissen Parität" |
| 32 | In v3.1 die Mittelebenen als abzuschaffen dargestellt und die Gebietsreform als unausweichlich bezeichnet | Der Nutzer löst es eleganter: die Ebenen werden freiwillig und müssen gekauft werden. Das Abholen geschieht in der heutigen Struktur, der Anreiz trägt den Umbau | Nutzerentscheidung |
| 33 | Die Verteilungsfrage zwischen Gemeinden nur geografisch gedacht (Gebietsreform, Nachbarverbände) | Strukturverwandtschaft ist das bessere Kriterium: zwei Hafenstädte teilen mehr als zwei Nachbarn. Stand in keiner meiner Varianten | Nutzervorgabe „regionale oder ggf. auch strukturverwandte Verbände" |
| 34 | Die Entlastungswirkung des Konzepts nie gegen die heutige Gesamtlast gestellt | Sie ist null: 40,75 gegen 40,76 % des BIP. Das Konzept verschiebt die Verfassung der Abgaben, nicht ihre Höhe — und das muss es auch so sagen | Beim Rechnen der Dividendenvarianten selbst gemerkt |

| 35 | Die Zinsgarantie als eleganten Ausweg um die Vergemeinschaftung herum eingeordnet | Sie ist Vergemeinschaftung, nur in Garantieform: DE und DK haften mit und gewinnen nichts, FR und ES nehmen 83 % des Vorteils. Ihr echter Wert liegt darin, die Gesamtkosten zu senken, nicht die Verteilungsfrage zu umgehen | Beim Rechnen der Laenderwirkung selbst gemerkt |
| 36 | Den Zinsdienst von 1,20 % des BIP als feste Groesse durch alle Rechnungen getragen | Er ist der effektive Satz eines auslaufenden Altbestands (1,53 %) und steigt bei Umschuldung auf 2,18 % des BIP. Elf Rechnungen lang stand eine Zahl in der festen Last, die sich fast verdoppelt | Beim Vergleich von GF0107 mit den Marktrenditen aufgefallen |
| 37 | Die Lücke zwischen Modellblock und Aufgabenkatalog als Kalibrierungsproblem erwartet | Sie ist inhaltlich: 138,5 Mrd sind die Ebene A, die im nationalen Modell nicht vorkam, 103,2 Mrd die Haager Zusage. Die Umbasierung allein erklärt nichts davon | Beim Abgleich nach der Umbasierung |

| 38 | Die Haager 3,5 % als Gesamtgroesse der Verteidigung behandelt | Die Erklaerung selbst trennt 3,5 % Kernverteidigung von bis zu 1,5 % fuer Netze, Resilienz und Innovation. Der Nutzer hatte recht, dass Digitales dazugehoert — es steht sogar im Text | Nutzereinwand, dann der Wortlaut nachgelesen |
| 39 | Den festen Schluessel als Zuteilung konstruiert | A's Bedarf schwankt zwischen 33,4 und 38,7 % des Einzugs. Als Zuteilung erzeugt der Schluessel Ueberschuss oder Luecke; als Obergrenze loest er beides und schuetzt staerker | Beim Rechnen des Zeitpfads |
| 40 | Die statische Momentaufnahme als Urteil ueber die 28 genommen und drei Wege zur Wahl gestellt | Die Momentaufnahme verbuchte die Haager Zusage sofort, obwohl sie fuer 2035 gilt. Ueber die Zeit traegt die 28 ohne jeden Einbruch. Die ganze Entscheidungstabelle der v3.3 war ein Artefakt der falschen Zeitachse | Nutzerhinweis auf die zeitliche Steigerung |
| 41 | Angenommen, der territoriale Schuldaufschlag schmelze mit der fallenden Schuldenquote von selbst | Er tut es nicht: Bestand und Zins bleiben in Euro konstant, also auch der Aufschlag. Er sinkt nur relativ zum Einkommen, und das genuegt politisch nicht — es braucht eine ausdrueckliche Frist | Mitten in der eigenen Rechnung widerlegt |

**Panel-Falle, zum Mitschreiben:** `PANELAI` (nur Teilgruppen mit Gewinn) ist
richtig für Effektivsätze, aber lückenhaft — für Dänemark 4,9 gegen 44,0 Mrd.
USD im Gesamtpanel. Für Aufkommensrechnungen nur `_T` verwenden.

---

## 5 | Datenbestand und Weitergabe

| Quelle | Inhalt | Lizenz / Auflage | Weitergabe |
|---|---|---|---|
| OECD CbCR Tab. I + II | anonymisierte Länderberichte | OECD-Nutzungsbedingungen | Rohdaten nicht exportiert (167 MB); Skripte und Aggregate ja |
| Taxplorer, EU Tax Observatory | firmengenaue Länderberichte | **CC BY-NC-ND 4.0, nur nicht kommerziell** | **Rohdatenbank wird nicht weitergegeben, nicht in den Projektraum, nicht in Ausgaben.** Nur Aggregate, mit Zitat |
| IWF WEO April 2026 | BIP, BIP pro Kopf | öffentlich | frei |
| Eurostat Euroindikatoren | Defizit, Schuldenstand | öffentlich | frei |
| WKO-Zusammenstellung EU-SILC | Median-Äquivalenzeinkommen | Sekundärquelle | als Sekundärquelle gekennzeichnet; Primärquelle nachzutragen |
| Tax Foundation 2026 | Steuersätze | öffentlich | frei |
| CSO Ireland | GNI\* | öffentlich | frei |
| SOEP, EU-SILC Mikrodaten | Haushaltsdaten | **Vertrag erforderlich** | dürfen hier nicht hochgeladen werden |

Zitat für Taxplorer: Aliprandi, G., Borders, K., Gabriel, F., von Zedlitz, G.
(2022): *Public Country-by-Country Reports: a new database.* EU Tax Observatory.

**Rechenumgebung:** Python 3.11 mit numpy, pandas, scipy, scikit-learn,
matplotlib, openpyxl. Kein Paketindex erreichbar, keine Statistikportale aus
der Shell. Daten kommen über Upload oder über freigegebene Links herein.
Nicht verfügbar: EUROMOD, GETTSIM, CORTAX (GAMS), statsmodels.

---

## 6 | Rechenplan

Geordnet nach Nutzen je Aufwand. Alle genannten Quellen sind frei und
veröffentlicht; keine erfordert einen Datenvertrag.

| | Position | Rechnung | Quelle | ersetzt |
|---|---|---|---|---|
| ~~R1~~ | 03 Erbschaft | ~~Aufkommen bei 28 % und Kosten der Verschonungen~~ | | **erledigt in v0.6** |
| **R2** | 01, 10 | Tarifaufkommen des Stufentarifs und des Abgabenumbaus, direkt auf der amtlichen Verteilung gerechnet | Destatis Lohn- und Einkommensteuerstatistik, Größenklassen des Gesamtbetrags der Einkünfte | „Modellschätzung" |
| **R3** | 06 Konsum | Effektivsatz des Mehrwertsteuer-Labels aus den tatsächlichen Konsumausgaben | Destatis VGR, Konsum nach Verwendungszweck (COICOP) | Annahme 10/10/20/30/30 |
| ~~R4~~ | 07 Klima | Aufkommen auf dem Preispfad 100 → 150 €/t mit Minderungspfad | Drittes BEHG-Änderungsgesetz; UBA 2021 | **erledigt in v1.0** |
| ~~R5~~ | 04 Boden | Bemessungsgrundlage der Bodenwertabgabe | Destatis WISTA 6/2015; Grundsteuerwerte 2025 | **erledigt in v2.0** |
| ~~R6~~ | 05 Konzerne | ~~Dreifaktor-Zerlegung und Zeitreihe~~ | | **erledigt in v0.5** |
| **R7** | alle | **Monte-Carlo über alle unsicheren Parameter** statt drei Rechenwegen: Elastizitäten, Label-Gewichte, Bodensatz, CO₂-Pfad als Verteilungen; Ausgabe ist die Verteilung des Haushaltssaldos | eigene Rechnung, setzt R1–R5 voraus | „optimistisch / vorsichtig / Rezession" |
| **R9** | alle | **erledigt in v2.0:** Haushaltsabgleich und Tarifentscheidung aus dem 20-Jahres-Pfad | eigene Rechnung auf `modell-2828.py` | Zielsaldo-Kriterium |
| **R8** | 09 Schutz | Gewinner- und Verlierer-Anteile je Dezil | aus R2 ableitbar auf Klassenebene; echte Haushaltsebene braucht SOEP oder EU-SILC | „Modellschätzung" |

**Technische Grundlage, parallel zu R1:** ein Verzeichnis mit einem Parameterfile,
einem Lauf-Skript und einer maschinenlesbaren Ergebnisdatei, aus der die
Webseite ihre Zahlen zieht. Heute stehen die Zahlen von Hand in den
Sprachdateien; damit können Seite und Rechnung auseinanderlaufen. Nach dem
Umbau ist das ausgeschlossen, und jede Zahl trägt ihre Version.

**Was nicht geht, und was es bräuchte**

| Ziel | Hindernis | Weg |
|---|---|---|
| echte Mikrosimulation Haushalte | SOEP-Core v41 braucht Vertrag; GETTSIM hier nicht installierbar | Vertrag mit dem FDZ des DIW; Rechnung außerhalb dieser Umgebung |
| EU-weiter Vergleich der zehn | EUROMOD braucht Zugang und nationale Teams | Kontakt über die EUROMOD-Länderteams (Liste liegt vor) |
| Unternehmensseite im Gleichgewicht | CORTAX ist in GAMS geschrieben, JRC-intern | Kooperationsanfrage JRC Sevilla |
| Verhaltensreaktionen | kein Verhaltensmodul | Elastizitäten aus der Literatur, offen ausgewiesen (Anhang Punkt 3) |

**Hinweis zur Elastizität im Anhang:** die Semi-Elastizität der erklärten
Gewinne (0,8 / 1,0 / 1,5) darf auf den neu zugeordneten Teil der
Bemessungsgrundlage nicht angewendet werden — Position 05 schaltet genau diesen
Kanal ab. Von der neuen deutschen Basis sind 24 % neu zugeordnet, 76 %
Altbestand, und dort sinkt der Satz. Der Anhang rechnet derzeit zu vorsichtig.

---

## 7 | Offene Punkte, Stand v3.4

| Punkt | Status |
|---|---|
| Bodenwertabgabe | **neu gefasst, 2. Oktober 2026:** Position 04 ist ein Umbau der Grundsteuer bei gleichem Aufkommen, nicht eine neue Abgabe. Satz, der 15,5 Mrd. € trägt: 0,22 bis 0,44 % des Bodenwerts (Bodenwert 2014 = 3.529 Mrd. €, Destatis WISTA 6/2015). Für eine Zahl statt einer Formel fehlt ein Baulandpreisindex 2014→2026 |
| **Position 04: Weggabelung, Entscheidung offen** | **neu, 2. Oktober 2026:** aufkommensneutral (so wie formuliert) oder als Abgabe über dem heutigen Niveau? Die zweite Fassung brächte +20 Mrd. € und machte die Anhebung der mittleren Stufen überflüssig — die Mehrwertsteuer bliebe unberührt, die Zusatzlast unten bei 0,00 %. Gerechnet in `tarif_wahl.py` [4]. Keine Rechenfrage mehr, sondern eine Entscheidung |
| **Regressivität des Finanzierungszuschlags** | **strukturell, nicht behebbar:** solange der Spitzensatz bei 28 % feststeht, kann zusätzliches Aufkommen aus der Einkommensteuer nur aus der Mitte kommen. Keine von 335 geprüften Kombinationen vermeidet das. Entweder man nimmt es hin, verlagert auf den Boden (Position 04), oder man gibt den einen Satz auf — und damit die Identität des Konzepts |
| **Konsumquoten** | Setzung nach dem Muster der EVS (100/95/88/82/76/68/50 %), keine Daten. Sie bestimmen, wie regressiv die Mehrwertsteuerstufen wirken. Nächster Schritt: EVS-Konsumquoten nach Einkommensklassen; sie würden R3 mit abdecken |
| **Verteilungsgruppen** | Die Rechnung läuft auf sieben Gruppen (`VERT`) mit je einem Durchschnittseinkommen. Innerhalb einer Gruppe gibt es keine Streuung, Dezilaussagen sind damit nicht möglich. Das ist die Grenze zu R8 und braucht SOEP oder EU-SILC |
| **Wachstumsabschlag greift zu kurz** | Im Modell hängt `drag` nur am Spitzensatz (`L−25`), nicht an der Gesamtlastquote. Die Anhebung der mittleren Stufen erzeugt deshalb rechnerisch **keinen** Wachstumsabschlag, obwohl sie die Durchschnittsbelastung um gut einen Punkt des BIP hebt. Der Pfad ist an dieser Stelle zu freundlich; die Größenordnung des fehlenden Effekts ist rund 1 % BIP nach 20 Jahren |
| **Deutsche ETS-1-Versteigerungserlöse** | weiter offen, seit v1.0 unverändert. Die DEHSt-Kennzahlen nennen Mengen, nicht Erlöse |
| Verschiebung durch die Bodenwertsteuer | offen — aus aggregierten Daten nicht beziffernbar. Die Grundsteuerwertestatistik trägt es nicht: keine einheitliche Bundesstatistik, vier Länder nutzen Flächenmodelle ohne Wert, Daten nicht plausibilisiert. Nach dem Jahressteuergesetz 2024 künftig möglich |
| Vermögensteuer 1 % ab 2 Mio. € | **Größenordnung, Stand 2. Oktober 2026:** 17 bis 42 Mrd. €, mittlerer Fall um 30. Zwischenrechnung aus DIW Politikberatung kompakt 211 (2026); die DIW-Zahlen sind maschinell aus dem PDF gelesen und an der Quelle zu prüfen |
| „je Person" oder „je Haushalt" bei Position 04 | **neu** — nicht bestimmt; das DIW rechnet je Person, bei Haushalten läge die Basis niedriger |
| Höhe der abzubauenden klimaschädlichen Subventionen | offen |
| CO₂-Aufkommen | **gerechnet, 2. Oktober 2026, auf Rechtsgrundlage.** Drittes BEHG-Änderungsgesetz: § 44 Abs. 2 legt die Emissionsmengen 2021–2030 fest (301,0 → 180,6 Mio t, −40 %), § 10 Abs. 2 S. 4 den Preiskorridor 55–65 € für 2026 und 2027. Aufkommen auf dem Rechtspfad 2026: 13,9–16,4 Mrd. €; bei 100 € 25,2; bei 150 € 37,9 |
| **Position 07 ist ab 2028 nicht national setzbar** | **neu und hart.** § 10 Abs. 3 S. 2 Nr. 4 BEHG neu: ab 2028 marktbasierter Preis nach dem EU-ETS-1-Durchschnitt; der nationale Handel geht in den ETS 2 über (Kapitel IVa der Emissionshandelsrichtlinie), dessen Start die Verordnung (EU) 2026/667 um ein Jahr verschoben hat. Ein nationaler Preis von 100 oder 150 € ab 2028 ist mit geltendem Recht unvereinbar. Zu entscheiden: europäische Forderung, nationale Zusatzabgabe, oder Pfad absenken |
| Schrumpfende Quelle | **neu.** Bei festem Preis von 150 € fällt das Aufkommen von 2026 bis 2030 um 28,4 %, weil die gesetzliche Menge sinkt. Gehört in die Haushaltsrechnung der Dividende |
| Anteil der Plattformbesteuerung am Nutzungsort | **teilweise geschlossen**, v0.5: +5 bis +14 Mrd. €, Median +8, über acht Jahre und vier Schlüssel geprüft |
| Gemischter Schlüssel (½ Umsatz, je ¼ Beschäftigte und Sachanlagen) | **neu** — sieht nach dem besseren Tausch aus: −249 gegen −161 (Einfaktor) und −279 Mrd. € (Dreifaktor) bei den Oasen, für Deutschland fast unverändert. Zu prüfen |
| Verteilungswirkung zulasten der Produktionsländer | **neu** — unter dem Zielort-Schlüssel verlieren Indonesien, Mexiko, Indien und Vietnam; gehört auf die Seite |
| Gewichte der Mehrwertsteuerstufen | offen, R3 |
| ~~Stundung statt Verschonung~~ | **entschieden in v0.7.** Ursprünglicher Befund: allgemeine Stundungsoption für Betriebe **und** Immobilien. 61 % des geerbten Vermögens sind illiquide (Grund 40 %, Betrieb 19 %, Land- und Forstwirtschaft 1 %), rund 10 von 16,5 Mrd. € Steuer wären stundungsfähig. **Entscheidend ist der Zins:** zinslos über 20 Jahre in Raten ist ein Erlass von 26 %, über 10 Jahre von 15 % — das wäre die Verschonung unter anderem Namen. Verzinst ist es reine Zahlungsstreckung, kostet dauerhaft nichts, reisst aber eine einmalige Übergangslücke von 45 Mrd. € über zehn Jahre. Gewählt: objektgebunden mit Zinsleiter, Untergrenze Refinanzierungssatz |
| Verwaltungsaufwand bei 200.000 € Freibetrag | **neu, v0.9** — wie viele Erbfälle zusätzlich zu veranlagen wären, sagt die Statistik nicht; sie erfasst nur, was das Finanzamt heute erreicht |
| Übergangslücke der Stundung | **neu, v0.7** — 4,5 Mrd. € im Jahr über zehn Jahre, kumuliert 45 Mrd. Reine Zeitverschiebung, gehört aber in den Haushalt der ersten Jahre |
| Vereinbarkeit der Zinsleiter mit § 234 AO | **neu, v0.7** — Rechtsquelle nicht prüfbar aus dieser Umgebung |
| Höhe der Erlasse nach § 28a ErbStG | **neu, v0.6** — nicht in der Statistik enthalten, Quelle zu finden |
| ~~Höhe und Staffelung des Erbschaftsfreibetrags~~ | **entschieden in v0.9:** 200.000 € je Erwerb, einheitlich. Ursprünglich: **neu, v0.6** — 400.000 € einheitlich kostet 3,8 Mrd. € gegenüber der heutigen Staffelung; Steuerklasse II und III sind 76,7 % der Erbfälle. Entwurfsentscheidung, zu benennen |
| Seitenzahl des Steuerrechts | offen, Kennzahl |
| Gewinneranteil ist Modellschätzung | offen, R8 |
| Übergangsausgleich im Klub | **neu und ungelöst** — nach v0.4 keine Nebenbedingung, sondern Voraussetzung |
| 28 % ist für neun der zehn eine Erhöhung | **neu** — verändert die politische Ökonomie des Klubs |
| Primärquelle für die Median-Äquivalenzeinkommen | offen |
