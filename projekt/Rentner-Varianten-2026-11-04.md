# Rentner: Varianten zur Regel E (Entwicklungsmodus)

Initiative 28:28 · 4. November 2026 · Modellstand v4.71 · vorläufig, kein Beschluss · Rechnung: `modell/rentner_varianten.py`, `modell/rentner_beitragsjahre.py`

## Auftrag

Hohe Erwartungen aus ungedeckten Zusagen sollen im Sinne der Generationengerechtigkeit eher zurücktreten; Rentner mit langen Beitragszeiten
und niedrigen Erwartungen sollen sicher ins Plus kommen. Keine neuen Abgaben, keine Sonderregeln; die Regel soll international übertragbar sein.

## Ausgangslage (Deutschland, 2028, Kaufkraft 2026)

- **Regel E:** 15 % Kürzung auf den Teil der Zusage über dem Grundbedarf G (1.029 € im Monat); Boden = heutige Grundsicherung.
  32 % der Rentnerhaushalte haben mehr, im Mittel −121 € im Monat; Entlastung des Fonds 25,1 Mrd. € (Kürzung minus Boden).
- **Ohne jede Kürzung** wären 67 % im Plus, im Mittel −3 €. Die Verluste des oberen Fünftels (−124 €) kommen dann aus Steuer, Label und
  Zuschlag. Wer verliert, verliert also vor allem durch die Kürzung.
- **Wo E trifft:** Zusagen zwischen 1 und 2 G (49 % der Personen) – darunter die typische Rente nach langer Erwerbszeit mit
  Durchschnittsverdienst (rund 1,75 G; Standardrente 2025 rund 1.800 € brutto, eigene Kenntnis, zu prüfen). Bei 1,5–2 G hat unter E niemand mehr.

## Grundgedanke

Die Kürzung folgt derselben Logik wie der Tarif: **Stufen in Vielfachen des Grundbedarfs des jeweiligen Staates.** Das ist keine neue Regel,
sondern die vorhandene, auf die Zusage angewandt, und es gilt in jedem Staat ohne nationale Beträge. Untere Stufen bleiben frei, obere
tragen mehr.

## Varianten, gerechnet (gleiche Entlastung des Fonds wie E, wo „neutral“)

| Variante | Kürzungsstufen | Anteil mit mehr | 1–1,5 G | 1,5–2 G | 2–3 G | über 3 G | Fonds gegen E |
|---|---|---|---|---|---|---|---|
| E (geltend) | 15 % ab 1 G | 32 % | +11 € (57 % im Plus) | −89 € (0 %) | −254 € | −649 € | 0 |
| T – wie der Tarif | 0 / 15 / 25 / 33 % ab 1,5 / 2 / 3 G | 52 % | +51 € (100 %) | −12 € (37 %) | −222 € | −856 € | −1,1 Mrd. € |
| N1,5/3 – neutral | 0 % bis 1,5 G, 19,4 % bis 3 G, 38,7 % darüber | 51 % | +51 € (100 %) | −22 € (32 %) | −221 € | −883 € | 0 |
| **N2/3 – neutral** | 0 % bis 2 G, 27,7 % bis 3 G, 55,4 % darüber | **65 %** | +51 € (100 %) | **+24 € (100 %)** | −162 € | −1.042 € | 0 |

Werte: Änderung des Haushaltsnettos je Monat im Mittel der Gruppe nach Zusage je Person; in Klammern Anteil im Plus. Personenanteile:
bis 1 G 21 %, 1–1,5 G 30 %, 1,5–2 G 19 %, 2–3 G 19 %, über 3 G 11 %. Bis 1 G sind 71 % im Plus, unabhängig von der Variante (Kürzung greift dort
nicht; kleine Verluste aus dem Label).

**Lesart.** N2/3 erfüllt den Auftrag am deutlichsten: Alle Zusagen bis zum doppelten Grundbedarf – also auch die Rente nach langer Erwerbszeit
mit Durchschnittsverdienst – kommen ins Plus, ohne dass der Fonds weniger erhält. Der Preis: Zusagen über 3 G (11 % der Rentner, vor allem hohe
Versorgungszusagen) verlieren im Mittel gut 1.000 € im Monat; der Grenzsatz der Kürzung liegt dort bei 55 %. T ist die einfachste, weil mit dem
Tarif gleichlaufende Fassung; sie belässt die Grenze bei 1,5 G und kostet den Fonds 1,1 Mrd. € (≈ 0,02 % des BIP).

## Weitere Varianten, noch nicht gerechnet

1. **Nominalschutz statt Kürzung:** Zusagen über der Schwelle werden nicht gekürzt, aber nicht mehr an die Preise angepasst, bis ihr realer Wert
   um den Kürzungssatz gesunken ist (bei 2 % Teuerung: 15 % nach rund 8 Jahren, 25 % nach rund 14 Jahren). Verlustaversion fällt geringer aus,
   weil kein Betrag sinkt. Nachteil: Die Entlastung kommt später; in den ersten Jahren trägt der Fonds mehr, also alle über den Zuschlag – das
   schwächt die Generationengerechtigkeit.
2. **Kürzung nach Zusage je Beitragsjahr:** gerechnet in v4.69, siehe Abschnitt „Vertiefung“.
3. **Boden nach der allgemeinen Regel:** Der Boden der Rentner ist heute die deutsche Grundsicherung (1.083 / 1.632 €). Universal wäre das
   Grundauskommen aller (G × Äquivalenzskala, Wohnkosten über den Härtefall H1). Das ändert für Deutschland wenig, macht die Regel aber ohne
   nationale Beträge anwendbar.
4. **Aufschlüsselung des Rentenbescheids:** Jede Rente in drei Teilen ausweisen – Gemeinsames (Dividende), Eigenes (ungekürzt), Zugesagtes (Teil
   des Fonds). Kein Geldfluss, aber nachvollziehbar, wofür gekürzt wird.

## Vertiefung: Kürzung nach Zusage je Versicherungsjahr (v4.69)

### Die Regel in einem Satz

**Jedes Versicherungsjahr schützt einen festen Teil der Zusage; geschützt ist höchstens, was ein volles Arbeitsleben einbringt – der doppelte
Grundbedarf.** Gekürzt wird nur, was darüber hinaus zugesagt ist, gestuft wie im Tarif.

Formel (Regel B): Freibetrag F = min(Jahre, V)/V × 2 G; Kürzung s auf den Teil der Zusage von F bis F + 1 G, 2 s darüber; s so, dass der Fonds
so viel entlastet wird wie unter E. V = Jahre bis zum vollen Schutz (45, 40 oder 35 gerechnet). In Deutschland (G = 1.029 € im Monat) schützt
jedes Jahr bei V = 45 rund 46 € Monatsrente. Die Regel braucht nur zwei Größen, die jedes Rentensystem führt: Zusage und Versicherungsjahre
(einschließlich angerechneter Erziehungs- und Pflegezeiten).

### Daten

EU-SILC und ASID enthalten keine Versicherungsjahre. Sie sind **zugeschätzt (Annahme)**: latente Jahre = a + b · ln(Zusage/Mittel) + Streuung,
kalibriert an den Bestandszahlen der Rentenversicherung (Rentenversicherungsbericht 2025, BT-Drs. 21/3080, Übersichten A 3.1 und A 3.2,
Renten wegen Alters ohne Vertragsrenten, 31.12.2024; maschinell aus dem PDF gelesen, an der Quelle zu prüfen):

| Versicherungsjahre | Anteil der Altersrenten | Ø Zahlbetrag (abgeleitet) | im Modell: Anteil | im Modell: Zusage gegen Mittel |
|---|---|---|---|---|
| unter 40 | 41,2 % | 686 € (0,57 × Mittel) | 42,0 % | 0,68 |
| 40 bis unter 45 | 19,2 % | 1.358 € (1,13 × Mittel) | 20,4 % | 0,94 |
| 45 und mehr | 39,6 % | 1.668 € (1,39 × Mittel) | 37,6 % | 1,40 |

Ausgangszahlen: Männer 6,13 Mio. Renten, Ø 1.490 €; Frauen 7,82 Mio., Ø 980 €; ab 45 Jahren Männer 1.778 €, Frauen 1.449 €; ab 40 Jahren
Männer 1.718 €, Frauen 1.356 € (€ je Monat, nominal 2024). Die Klassenmittel unter 40 und 40–45 sind daraus abgeleitet (eigene Rechnung). Die
Anpassung ist mäßig (Mittel der Klasse 40–45 im Modell zu niedrig). Weitere Grenzen: Die Zusage ist im Modell ein fester Anteil (70 %) des
Bruttoeinkommens je Person (`rentner_kombi.py`), nicht der einzelne Anspruch; Beamte sind nicht getrennt.

### Ergebnis (Deutschland 2028, Kaufkraft 2026; alle Varianten mit gleicher Entlastung des Fonds, 25,1 Mrd. €)

| Variante | Sätze | Anteil mit mehr | lange Laufbahn (≥ 40 J.) bis 2 G: im Plus | kurze Laufbahn (< 35 J.) über 2 G: Mittel | 1,5–2 G im Plus | über 3 G Mittel |
|---|---|---|---|---|---|---|
| E (geltend) | 15 % ab 1 G | 32 % | 34 % | −261 € | 0 % | −649 € |
| **N2/3 (nur Höhe)** | 27,7 / 55,4 % ab 2 / 3 G | **65 %** | **98 %** | −178 € | 100 % | −1.042 € |
| B1,5 (V = 45, ein Satz) | 21,8 % | 44 % | 66 % | −338 € | 15 % | −747 € |
| B2 (V = 45, ein Satz) | 35,6 % | 59 % | 96 % | −395 € | 77 % | −918 € |
| B2/1 (V = 45) | 25,8 / 51,6 % | 60 % | 96 % | −340 € | 80 % | −997 € |
| B2/1 (V = 40) | 27,1 / 54,2 % | 63 % | 98 % | −292 € | 93 % | −1.026 € |
| B2/1 (V = 35) | 27,5 / 55,0 % | 64 % | 98 % | −224 € | 98 % | −1.037 € |
| B2,5 (V = 45, ein Satz) | 57,8 % | 66 % | 98 % | −409 € | 97 % | −1.092 € |

Lange Laufbahn bis 2 G: 31 % der Rentner; kurze Laufbahn über 2 G: 1 %. Werte: Änderung des Haushaltsnettos je Monat.

**Einzelfälle – Kürzung im Monat** (Bruttorente 2025/26 nominal, gegen G 2026 gelesen; Rentenwert 40,79 €, eigene Kenntnis, zu prüfen;
Ruhegehalt 1,79375 % je Dienstjahr nach § 14 BeamtVG, eigene Kenntnis, zu prüfen; Bezüge 5.000 € angenommen):

| Fall | Zusage | E | N2/3 | B2/1 (V = 45) | B2/1 (V = 35) |
|---|---|---|---|---|---|
| 45 J. Durchschnittsverdienst (45 EP) | 1.836 € | 121 € | 0 | 0 | 0 |
| 40 J. niedriger Verdienst (32 EP) | 1.305 € | 41 € | 0 | 0 | 0 |
| 30 J. höherer Verdienst (45 EP, gleiche Beiträge wie Fall 1) | 1.836 € | 121 € | 0 | 120 € | 20 € |
| 45 J. an der Beitragsbemessungsgrenze (≈ 90 EP) | 3.671 € | 396 € | 609 € | 567 € | 605 € |
| Ruhegehalt nach 40 Dienstjahren | 3.588 € | 384 € | 562 € | 642 € | 559 € |
| 20 J. Durchschnittsverdienst (20 EP) | 816 € | 0 | 0 | 0 | 0 |

### Befund

1. **Das Kriterium Jahre ändert in Deutschland wenig.** Lange Versicherungszeiten und hohe Renten gehen in der gesetzlichen Rente zusammen
   (ab 45 Jahren Ø 1.668 €, unter 40 Jahren Ø 686 €). Wer eine hohe Zusage hat, hat meist auch lange Jahre; Zusagen über 2 G mit kurzer Laufbahn
   betreffen im Modell 1 % der Rentner. Nur B2,5 liegt beim Anteil knapp über N2/3 (66 % gegen 65 %), mit einem Satz von 58 % ab
   dem Freibetrag; B2/1 mit V = 35 erreicht N2/3 nahezu.
2. **Je Beitragsjahr ist nicht dasselbe wie ungedeckt.** In der gesetzlichen Rente kauft jeder Beitragseuro denselben Anspruch (Entgeltpunkte).
   Die Höhe je Jahr misst dort die Lohnhöhe, nicht eine fehlende Deckung. Fall 3 zeigt die Folge: gleiche Beiträge, gleiche Rente wie Fall 1,
   aber gekürzt, weil in weniger Jahren gezahlt. Das widerspricht dem Grundsatz „gleicher Beitrag, gleiches Recht“ und wäre beim Eigentumsschutz
   der Anwartschaften (P1) schwerer zu begründen als eine Kürzung nach der Höhe.
3. **Die Versorgungszusage wird nicht besser getroffen.** Beamte haben lange Dienstzeiten; ihr Merkmal ist der hohe Satz je Jahr (1,79 % der
   letzten Bezüge) ohne eigene Beiträge, nicht die kurze Laufbahn. Das erfassen Höhe-Stufen ebenso (562 € unter N2/3).
4. **Wo das Kriterium trägt:** in Systemen, in denen Zusagen je Jahr weit über dem liegen, was Beiträge erwerben – Endgehaltsformeln,
   Sonderregime, frühe Ruhestandsrechte. Dort trennt es Erworbenes von Gewährtem. Für Deutschland ist das nicht gerechnet; für andere Staaten
   fehlen die Daten.

### Narrativ (Vorschlag)

**„Ein Arbeitsleben schützt den doppelten Grundbedarf.“** Wer ein volles Erwerbsleben lang mit durchschnittlichem Verdienst eingezahlt hat,
erreicht in Deutschland rund 1,8 G – und bleibt ungekürzt. Was darüber hinaus zugesagt ist, wurde mit Beiträgen erworben, die die damaligen
Rentner bezahlt haben, nicht angespart; es trägt gestuft zum Altlastenfonds bei, wie hohe Einkommen im Tarif. Die Rechnung für diese Aussage
ist **N2/3** (Höhe allein). Die Versicherungsjahre begründen die Schwelle von 2 G, sie müssen nicht in die Formel.

Wenn die Jahre in die Formel sollen, dann als **Jahresschutz ab 35 Jahren (B2/1, V = 35):** voller Schutz ab 35 Versicherungsjahren, darunter
anteilig. Ergebnis fast gleich N2/3 (64 % gegen 65 %), Fall 3 verliert 20 € statt 0. Nutzen in Deutschland klein, international größer
(Punkt 4); Kosten: eine zweite Größe je Person und der Konflikt mit gleichem Recht je Beitrag.

**Weiterführend (nicht gerechnet):** Für „ungedeckt“ im engen Sinn wäre der Maßstab die Zusage je Beitragseuro (Deckungsgrad), nicht je Jahr.
Er setzt Beitragsdaten je Person voraus; für Beamte ist umstritten, ob niedrigere Bruttobezüge als impliziter Beitrag gelten.

### Nachtrag v4.71: Option ab 35 mit Sockel (BS35), international gedacht

**Anlass.** Ohne Sockel kürzt die Option ab 35 auch niedrige Renten nach kurzer Laufbahn: Bei 10 Jahren und einer Rente in Höhe von G liegt der
Freibetrag bei 0,57 G, gekürzt würden 121 € im Monat. Kurze Laufbahnen sind häufig die von Zugewanderten, von Frauen mit Erziehungszeiten und,
in vielen Staaten, von Menschen mit langer informeller Arbeit. Das widerspräche SDG 1 und dem Auftrag.

**Regel BS35.** Freibetrag F = max(1 G; min(Jahre, 35)/35 × 2 G); Kürzung 27,5 % von F bis F + 1 G, 55,1 % darüber (neutral zu E).
Kernsatz: **„Ein Arbeitsleben schützt den doppelten Grundbedarf, und niemandem wird der Grundbedarf genommen.“**

**Ergebnis Deutschland 2028.** Gleich B2/1 (V = 35): 64 % der Rentnerhaushalte mit mehr, Satz unverändert 27,5 / 55,1 %, lange Laufbahn bis 2 G
zu 98 % im Plus, kurze Laufbahn über 2 G im Mittel −224 €. Der Sockel ändert die Summen nicht, weil im Modell kurze Laufbahnen mit Zusagen über
ihrem Freibetrag, aber unter 1 G kaum vorkommen. Das liegt auch an der Zuschätzung der Jahre aus der Höhe der Zusage (Annahme), die solche Fälle
selten erzeugt. Im Einzelfall wirkt er: 10 Jahre, Rente 1.029 €: Kürzung 0 statt 121 €. In Staaten mit vielen kurzen Laufbahnen ist die Wirkung
größer; nicht gerechnet, Daten fehlen.

**Einordnung.** BS35 ist die Fassung für die internationale Regel: Sie trifft, was N2/3 nicht sieht (hohe Zusagen nach kurzer Laufbahn,
Sonderregime, Endgehaltsformeln), und schützt den Grundbedarf ohne Ansehen der Jahre. Kosten gegenüber N2/3: eine zweite Größe je Person
(Versicherungsjahre, auch aus anderen Staaten anzurechnen) und die ungleiche Behandlung gleicher Beiträge oberhalb von 1 G (Fall 3: 20 €).
In Systemen mit Beitragskonten (Schweden, Italien nach 1996, Polen; eigene Kenntnis, zu prüfen) bleibt N2/3 die genauere Regel.

## Folgen für andere Bausteine (zu prüfen)

- Armutsquote SDG 1.2: Mit N2/3 gewinnen die unteren und mittleren Rentnerhaushalte; die Quote dürfte sinken (neu zu rechnen, v4.67 rechnet
  Rentner unverändert).
- Kürzungssatz je Staat (`kuerzung_laender`): leitet sich bisher aus 15 % über G ab; bei Stufen ändert sich die Verteilung zwischen den Staaten.
- Verfassungsrecht (Eigentumsschutz von Anwartschaften, P1): hohe Grenzsätze der Kürzung sind rechtlich angreifbarer als ein einheitlicher Satz.

## Zu entscheiden

Grenze der freien Stufe (1,5 G oder 2 G), Höhe der oberen Sätze (Obergrenze z. B. 33 % wie im Tarif; N2/3 erreicht 55 %), Nominalschutz als
Übergang; Versicherungsjahre in der Formel (Jahresschutz ab 35 Jahren) oder nur in der Begründung der Schwelle.

**Quellen:** Deutscher Bundestag, Drucksache 21/3080, Rentenversicherungsbericht 2025 (28.11.2025), Übersichten A 3.1/A 3.2; Wissenschaftliche
Dienste, WD 6 - 3000 - 045/26 (Durchschnittswerte langjährig Versicherter, 31.12.2024); Bundesregierung, Antwort auf eine Schriftliche Frage,
Juni 2026, Arbeitsnummer 240 (Fundort: Veröffentlichung einer Landtagsfraktion, Sekundärfundort; Altersrenten ab 45 Jahren, Bestand 31.12.2025: Ø 1.712 €, 34 % unter 1.450 €).
