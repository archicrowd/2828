# Verhaltenswirkungen des Goldenen Drittels – qualitative Voruntersuchung

Initiative 28:28 · 24. Oktober 2026 · Logbuch v4.48, ergänzt v4.49 (Abschnitt 8) · Stand C, Fassung 4.49 · Status: **Voruntersuchung, keine Rechnung**

## 0 | Zweck, Grenzen, Vorgehen

**Frage der Initiative:** Was gelingt durch die neuen Anreize, was nicht? Welche Verhaltenswirkungen sind zu erwarten, und was sagen Studien
und verhaltensökonomische Befunde dazu?

**Was die Rechnung heute enthält:** Die Rechenkette (65 Stufen) ist im Kern statisch. Verhalten steckt nur an vier Stellen in Form von
Annahmen oder Bändern: Weitergabe der Arbeitgeberbeiträge (80 %, Rückfallregel, `weitergabe_rueckfall.json`), Überwälzung der
Mehrwertsteuer (`preisniveau33.json`), Ausweichen bei Erbschaft und Vermögen (`ausweichen33.json`) und Inanspruchnahme (voll; Variante
69 %, `mikro_de.json → inanspruchnahme`). **Arbeitsangebot, Sparen, Wanderung und Steuerehrlichkeit reagieren in der Rechnung nicht.**

**Was diese Untersuchung leistet:** Sie ordnet je Baustein die erwartete Richtung der Wirkung, die Stärke der Belege und die Übertragbarkeit
auf die fünf gerechneten Staaten (DE, FR, IT, ES, PL). Sie beziffert keine Wirkung auf Aufkommen oder Dividende; das ist Stufe 2 (Abschnitt 5).

**Belegstufen**

| Stufe | Bedeutung |
|---|---|
| **A** | mehrere kausale Studien (Feldexperiment, Quasi-Experiment mit Verwaltungsdaten) mit gleichgerichtetem Ergebnis, in ähnlichem Umfeld |
| **B** | eine kausale Studie oder mehrere aus deutlich anderem Umfeld (USA, Einzelbranche, kleine Stichprobe) |
| **C** | Theorie, Laborbefund oder Plausibilität; keine Studie zur konkreten Regel |

**Quellenprüfung:** Alle Zahlen aus Studien wurden am 24.10.2026 an der Zusammenfassung (Abstract) oder am Volltext der angegebenen Fundstelle
abgelesen (Liste in Abschnitt 7). Werte, die nur maschinell aus einem PDF gelesen sind, tragen den Vermerk „maschinell gelesen, an der Quelle zu
prüfen“. Die Zuordnung der Befunde zu den Bausteinen ist Urteil der Initiative, kein Ergebnis der Studien.

## 1 | Übersicht

| Baustein | Erwartete Verhaltenswirkung | Richtung für das Ziel | Beleg | In der Rechnung? |
|---|---|---|---|---|
| Transformationsdividende ohne Antrag (354 € je Erwachsenem, 2028) | Einkommenseffekt: geringfügig weniger Arbeitsstunden, kaum weniger Beschäftigung; mehr Sicherheitsgefühl und Vertrauen | leicht negativ (Arbeit), positiv (Wohlbefinden) | A/B | nein |
| Halbanrechnung bei der Aufstockung | höhere Erwerbsbeteiligung im unteren Bereich; mehr Haushalte im Abschmelzbereich | positiv an der Beteiligungsgrenze, unklar bei den Stunden | B | nein |
| Grundauskommen und Dividende ohne Antrag | höhere Inanspruchnahme, weniger verdeckte Armut | positiv für das Ziel, Kosten bereits voll gerechnet | A | ja (voll) |
| Pflichtvorsorge 10 % auf eigenem Konto | höhere Gesamtersparnis bei passiven Sparern; Verdrängung freiwilligen Sparens bei aktiven | positiv | A | ja (als Pflicht) |
| Stufentarif, Brutto ohne Abzüge, kein Splitting | weniger Gestaltung, mehr Steuerehrlichkeit; mehr Arbeitsstunden von Zweitverdienern | positiv | B | nein |
| Weitergabe der Arbeitgeberbeiträge | ohne Pflicht: Weitergabe unsicher, teils an alle Beschäftigten verteilt; mit Pflicht und Rückfallregel gesichert | Risiko, durch Regel begrenzt | B | ja (80 %, Band) |
| Mehrwertsteuer-Label | Senkungen kommen schwächer bei Verbrauchern an als Erhöhungen; sichtbare Kennzeichnung kann Lenkung verstärken | gemischt | A (Überwälzung) / B (Lenkung) | teilweise (Preisniveau) |
| CO₂-Preis mit Rückgabe über die Dividende | Rückgabe wird unterschätzt; Zustimmung folgt eher Parteibindung als eigenem Vorteil | Akzeptanzrisiko | B | nein |
| Erbschaft 33 %, Vermögen 1,5 % | Ausweichen, an der Spitze stark; Wegzug hoch Mobiler | negativ für das Aufkommen | A/B | ja (Band) |
| Rentenregel E (Kürzung über dem Grundbedarf) | Verlustaversion; Widerstand der größten Wählergruppe; Vorzieheffekte vor dem Stichtag | Akzeptanzrisiko | C (für die Regel), A (für Verlustaversion) | nein |

## 2 | Befunde je Baustein

### 2.1 Transformationsdividende ohne Antrag

**Belege**

- **Alaska Permanent Fund Dividend** (jährlich, an alle Einwohner): keine Wirkung auf die Beschäftigung; Teilzeit +1,8 Prozentpunkte (rund
  +17 %). Methode: synthetische Kontrollgruppe, CPS-Daten (Jones/Marinescu, NBER w24312; AEJ: Economic Policy 2022).
- **OpenResearch-Studie, USA 2020–2023** (1.000 $ im Monat über drei Jahre an rund 1.000 Personen mit niedrigem Einkommen, Kontrollgruppe
  rund 2.000 mit 50 $): Erwerbsbeteiligung −4,2 Prozentpunkte, Arbeitszeit −1 bis −2 Stunden je Woche, Einkommen ohne Transfer rund
  −1.900 $ im Jahr; mehr Freizeit, keine bessere Beschäftigungsqualität, kein messbarer Anstieg von Gründungen (Vivalt u. a., NBER w32719, 2024).
- **Finnisches Grundeinkommensexperiment 2017–2018** (560 € steuerfrei an 2.000 Arbeitslose): +6 Beschäftigungstage im zweiten Jahr (nicht
  trennbar vom gleichzeitigen „Aktivierungsmodell“), im ersten Jahr keine Wirkung; höhere Lebenszufriedenheit, weniger psychische Belastung,
  mehr Vertrauen in Mitmenschen und Institutionen (STM, Abschlussbericht 2020; Befragung mit Rücklauf 23 %, Kausalität der Befragungswerte
  von den Autoren selbst offen gelassen).

**Einordnung**

- Die Belege stützen keinen starken Rückzug aus der Arbeit. Die Wirkung wächst mit der Höhe der Zahlung im Verhältnis zum Einkommen. Die
  OpenResearch-Zahlung (1.000 $) lag bei einer Gruppe mit niedrigem Einkommen; die Dividende (354 €, 2028, sinkend auf 239 € 2060) ist
  kleiner und steuerpflichtig. Annahme: Die Arbeitsangebotswirkung liegt zwischen Alaska (null) und OpenResearch (negativ, klein).
- Wer arbeitet und die Dividende erhält, verliert sie nicht bei mehr Arbeit: Die Dividende hat keine Entzugsrate. Ein Ausstiegsanreiz entsteht
  nur über den Einkommenseffekt.
- Wohlbefinden und Vertrauen: positive Befunde aus Finnland, aber an Arbeitslosen und mit schwacher Befragungsbasis (Belegstufe B).

**Übertragbarkeit:** Alle drei Studien messen eine zusätzliche Zahlung bei sonst unverändertem System. Im Goldenen Drittel ersetzt die
Dividende Teile anderer Leistungen; der Einkommenseffekt netto ist für viele Haushalte kleiner als der Bruttobetrag. Für Staaten mit
niedrigerem Lohnniveau (PL, teils ES und IT) ist die Dividende im Verhältnis zum Lohn höher (Kaufkraftbasis des Landes); der Einkommenseffekt
dürfte dort größer sein (Annahme, nicht beziffert).

### 2.2 Halbanrechnung bei der Aufstockung (Transferentzug 50 %)

**Heute (DE):** Im Bürgergeld bleiben vom Hinzuverdienst nach § 11b SGB II die ersten 100 € frei, danach 20 % (bis 520 €), 30 % (bis 1.000 €)
und 10 % (bis 1.200 €, mit Kind 1.500 €) – Entzug also 70 bis 90 %; dazu kommt das Zusammenspiel mit Wohngeld und Kinderzuschlag
(Rechtsstand 2025, an der Quelle zu prüfen; eine 2026 beschlossene Neuordnung der Grundsicherung ist hier nicht berücksichtigt). Das ifo
Institut beschreibt „sehr hohe und ungleichmäßige Grenzbelastungen“ und schlägt die Integration des Wohngelds in das Bürgergeld vor
(Blömer/Hansen/Peichl, ifo Forschungsbericht 145, 2024; Zahlen zur Beschäftigungswirkung aus dem Abstract nicht ablesbar).

**Neu:** eine Regel für alle – Aufstockung = Grundauskommen + Härtefall − Dividenden − ½ × eigenes Einkommen. Entzug 50 %, gleichmäßig.

**Erwartung**

- **Beteiligungsgrenze (aufnehmen oder nicht):** Die Literatur findet die stärkeren Reaktionen bei der Entscheidung, überhaupt zu arbeiten,
  schwächere bei der Stundenzahl (Saez, QJE 2002, theoretisch; empirisch für den EITC). Ein Entzug von 50 % statt 70–90 % in den ersten
  Hunderten Euro macht den Einstieg und den Schritt aus dem Minijob deutlich attraktiver. Richtung: positiv (Belegstufe B).
- **Abschmelzbereich:** Mit niedrigerer Entzugsrate reicht die Aufstockung höher in die Einkommen hinein; mehr Haushalte stehen in einem
  Bereich mit 50 % Entzug (plus Pflichtvorsorge 10 % auf eigenes Konto). Für diese Haushalte kann die Stundenwirkung negativ sein. Das ist der
  bekannte Zielkonflikt jeder Entzugsrate; wo der Saldo liegt, entscheidet die Verteilung um die Grenze. **Nicht gerechnet.**
- **Wissen entscheidet:** Beim EITC reagieren Haushalte dort stärker, wo die Regel bekannt ist (Chetty/Friedman/Saez, AER 2013). Eine einfache,
  einheitliche Regel ist leichter zu kennen als das heutige Zusammenspiel dreier Leistungen (Annahme, plausibel; Belegstufe B/C).

**Lücke:** Die Grenzbelastung im Bereich der Aufstockung ist in `grenzbelastung33.json` nicht ausgewiesen (Rechnung beginnt bei 42.000 €).
Nächster Rechenschritt: Grenzbelastung heute und neu von 0 bis 30.000 € für die Haushaltstypen der Mikrosimulation.

### 2.3 Inanspruchnahme: Leistung ohne Antrag

**Belege**

- **Grundsicherung im Alter (DE):** rund 60 % der Berechtigten beziehen sie nicht (Basismodell 62 %; SOEP v33, 2010–2015); bei Ansprüchen unter
  200 € rund 80 %, über 600 € rund 20 %. Gründe nach den Autoren: Unkenntnis, Scham, Aufwand, Angst um Wohneigentum (DIW Wochenbericht 49/2019).
- **RSA (FR):** 34 % der berechtigten Haushalte beziehen ihn im Quartalsmittel nicht, 20 % drei Quartale lang nicht (DREES, Dossier 92,
  2022, Daten 2018).
- **EITC-Feldexperiment (USA, 35.050 Steuerpflichtige):** Ein Brief, eine vereinfachte Darstellung und ein sichtbarer Betrag erhöhten die
  Inanspruchnahme deutlich; Versuche, Scham oder Aufwand zu senken, wirkten nicht (Bhargava/Manoli, AER 2015).
- **Eurofound (2015):** Nicht-Inanspruchnahme ist in allen untersuchten Staaten verbreitet; Vereinfachung der Verfahren senkt sie und die
  Verwaltungskosten (Zahlen im Abstract nicht ablesbar).
- **Eigene Rechnung (v4.40):** Abstand zwischen Anspruch (4,7 Mio. Haushalte) und Bezug (rund 4,0 Mio.) = Quote 69 % bei Haushalten mit Erwerb.

**Einordnung:** Die Dividende ohne Antrag beseitigt die Nicht-Inanspruchnahme für ihren Teil vollständig. Für die Aufstockung hängt das von
der Ausgestaltung ab, die das Konzept noch offen lässt: Zahlt die Kommune auf Antrag oder von Amts wegen aus Steuer- und Lohndaten? Die
Belege sprechen für die Auszahlung von Amts wegen (vorausgefüllt, mit Widerspruchsrecht). **Kostenwirkung:** Die Rechnung setzt bereits volle
Inanspruchnahme an; eine höhere Inanspruchnahme kostet daher nichts über das Gerechnete hinaus. Gegen heute verschiebt sie aber den Vergleich:
Wer heute keinen Antrag stellt, gewinnt mehr (Variante v4.40: unterstes Zehntel +63 € statt +21 €).

**Übertragbarkeit:** hoch. Nicht-Inanspruchnahme ist in DE und FR belegt; für IT (ADI), ES (IMV) und PL fehlen hier Quoten. Für ES gibt es
Hinweise auf eine hohe Nicht-Inanspruchnahme des IMV (nicht geprüft; Aufgabe für R5).

### 2.4 Pflichtvorsorge 10 % auf eigenem Konto

**Belege**

- **Dänemark, 41 Mio. Beobachtungen:** Rund 85 % sind passive Sparer, die auf Steueranreize nicht reagieren, aber automatische Beiträge
  vollständig mitnehmen; rund 15 % aktive Sparer verschieben bei Anreizen nur Geld zwischen Konten. Je 1 $ staatlicher Förderung steigt die
  Ersparnis um 1 Cent (Chetty u. a., QJE 2014; NBER w18565).
- **Automatische Einbeziehung (USA):** deutlich höhere Teilnahme; viele bleiben beim voreingestellten Satz und der voreingestellten Anlage
  (Madrian/Shea, QJE 2001).

**Einordnung:** Eine Pflicht wirkt stärker als eine Voreinstellung. Für passive Sparer erhöht sie die Ersparnis nahezu im vollen Umfang; aktive
Sparer werden freiwilliges Sparen teilweise verringern. Für das Ziel (Mindestrente mit Pflichtvorsorge) ist die Richtung positiv (Belegstufe A).
Das Risiko liegt woanders: Wird das Konto nicht als eigenes erlebt, wirkt der Beitrag wie eine Steuer, und die Grenzbelastung wird als rund
50 % statt 40 % empfunden (`grenzbelastung33.json`). Sichtbarkeit des Kontos, Eigentum und Vererbbarkeit sind daher Teil der Anreizwirkung.

**Übertragbarkeit:** Vertrauen in die Unantastbarkeit ist die Voraussetzung. **Polen** ist das Gegenbeispiel: Am 3. Februar 2014 wurden die
Staatsanleihen der offenen Pensionsfonds (OFE), 153,15 Mrd. zł oder 51,5 % ihres Vermögens, an die ZUS übertragen und gelöscht; die Zahl der
OFE-Mitglieder fiel danach von 16,6 auf 2,5 Mio.; das Verfassungsgericht stufte die Mittel 2015 als öffentlich ein (Sekundärquelle: SII,
polnischer Anlegerverband; an amtlicher Quelle zu prüfen). Für PL ist daher mit Misstrauen gegenüber einer Pflichtvorsorge zu rechnen; die
Konstruktion braucht dort einen stärkeren Eigentumsschutz (verfassungsrechtlich, Verwahrung außerhalb des Staatshaushalts). Positive Vorbilder
mit langer Laufzeit: Australien (Superannuation), Schweden (Prämienpension) – beide auf der Webseite als Länderbeispiele geführt.

### 2.5 Stufentarif, Brutto ohne Abzüge, kein Splitting

**Belege**

- **Steuerehrlichkeit hängt an Meldewegen:** Bei Einkommen mit Drittmeldung (Lohn, Bankerträge) lag die Hinterziehungsquote in Dänemark bei
  0,3 %, bei selbst erklärtem Einkommen bei 37 %; Prüfungsankündigungen erhöhten das erklärte Einkommen (Kleven u. a., Econometrica 2011).
- **Russland, Einheitssatz 13 % (2001):** starke Zunahme der freiwilligen Steuerehrlichkeit, schwache Reaktion der Produktivität; der
  Effizienzgewinn ist mindestens 30 % kleiner als mit herkömmlichen Ansätzen berechnet (Gorodnichenko u. a., JPE 2009; NBER w13719).
- **Zweitverdiener:** In einem Modell für 17 Staaten würde der Übergang von gemeinsamer zu getrennter Besteuerung bei gleicher Steuerlast die
  Arbeitszeit verheirateter Frauen in Deutschland um rund 270 Stunden im Jahr (+33 %) erhöhen, in Frankreich und Dänemark um 50 bis 70 Stunden
  (Bick/Fuchs-Schündeln, Review of Economic Studies 2018; CEPR DP9115; maschinell aus dem PDF gelesen, an der Quelle zu prüfen; Modellrechnung,
  kein Experiment).

**Einordnung**

- „Brutto ohne Abzüge“ verkleinert den Anteil selbst erklärter Abzüge; mehr Einkommen wird über Drittmeldung erfasst. Richtung: weniger
  Hinterziehung und Gestaltung (Belegstufe B; Dänemark ist ein Land mit hoher Steuermoral).
- Die russische Reform betraf ein Land mit hoher Hinterziehung; der Befund stützt, dass niedrigere und einfachere Sätze vor allem über die
  Ehrlichkeit wirken. Für DE ist der Effekt kleiner zu erwarten (Annahme).
- Der Wegfall des Splittings ist die verhaltensökonomisch am besten begründete Arbeitsangebotswirkung des Tarifs, mit Ausnahme der Aufstockung,
  die haushaltsbezogen rechnet: Im Abschmelzbereich gilt für Zweitverdiener wieder ein Entzug von 50 % (Abschnitt 2.2).
- Spitzensatz: Die Grenzbelastung sinkt 2028 bei 60.000 € von 48,8 % auf 40,0 % (v4.47). Die Wirkung auf die Stunden von Hauptverdienern gilt
  in der Literatur als klein; die Wirkung auf das gemeldete Einkommen (Gestaltung) als größer.

**Übertragbarkeit:** IT, ES und PL haben größere Bereiche selbst erklärter und nicht erklärter Arbeit. Laut Eurobarometer 498 (2019) war in
Spanien 36 %, in Italien 35 % der nicht angemeldeten Arbeit abhängige Beschäftigung; in Dänemark gaben 8 %, in Schweden 7 % der Befragten
nicht angemeldete Arbeit an (Europäische Kommission/ELA, Williams/Horodnic 2020; Befragung, Untergrenze nach den Autoren). Werte für FR und PL
waren aus dem Bericht nicht sicher ablesbar. Schätzungen der Schattenwirtschaft in % des BIP (Medina/Schneider, IMF WP 18/17) sind
methodisch umstritten („Obergrenze“ nach den Autoren selbst) und werden hier nicht verwendet. Folgerung: Der Ehrlichkeitsgewinn eines
einfachen Tarifs kann in IT, ES und PL größer sein als in DE; zugleich ist dort das Aufkommensrisiko aus selbst erklärtem Einkommen höher.
Beides ist nicht beziffert.

### 2.6 Weitergabe der Arbeitgeberbeiträge

**Belege**

- **Schweden, Senkung der Arbeitgeberbeiträge für junge Beschäftigte (31 % → 15 %):** keine Wirkung auf die Nettolöhne der Begünstigten
  gegenüber etwas Älteren, auch nach sechs Jahren; Beschäftigung der Jungen +2 bis 3 Prozentpunkte (weniger Trennungen); begünstigte Betriebe
  wuchsen und erhöhten die Löhne aller Beschäftigten (Saez/Schoefer/Seim, AER 2019; NBER w23976).

**Einordnung:** Ohne Pflicht kommt eine Senkung der Arbeitgeberbeiträge nicht zwingend bei den Beschäftigten an, für die sie gesenkt wird;
sie verteilt sich über Gewinne, Investitionen und Löhne im ganzen Betrieb. Die Konstruktion des Goldenen Drittels (gesetzliche Anpassung aller
Verträge zum Stichtag, mindestens 80 %, Monitoring, Rückfallregel) setzt genau hier an. Der schwedische Befund stützt die Rückfallregel als
notwendig (Belegstufe B; Einzelland, Altersgruppe). Zugleich zeigt er eine mögliche positive Nebenwirkung: Wo Betriebe Mittel behalten,
steigt die Beschäftigung.

### 2.7 Mehrwertsteuer-Label

**Belege**

- **Asymmetrische Überwälzung:** Erhöhungen der Mehrwertsteuer wurden in der EU (1996–2015, über 2.800 Güter) drei- bis viermal stärker in
  Preise weitergegeben als Senkungen; finnische Friseure gaben eine Senkung um 14 Punkte zu 60 % gar nicht weiter, die Rücknahme dagegen fast
  vollständig (Benzarti u. a., JPE 2020; VATT-Zusammenfassung).
- **Sichtbarkeit:** Ausgewiesene Bruttopreise senkten in einem US-Supermarkt die Nachfrage nach den betroffenen Gütern um rund 8 %; in den Preis
  eingerechnete Verbrauchsteuern wirkten stärker als an der Kasse aufgeschlagene (Chetty/Looney/Kroft, AER 2009; NBER w13330).

**Einordnung**

- Für das Label heißt das: Die Senkungen (A+ 5 %, A 11 %) kommen vermutlich nur teilweise bei den Verbrauchern an, die Erhöhungen (C 25 %,
  S 33 %) weitgehend. Das spricht für einen höheren Preisniveauschub als mechanisch symmetrisch gerechnet. `preisniveau33.json` rechnet mit
  einem Band +1,2 bis +2,1 % (mechanisch +2,47 %); ob das Band die Asymmetrie abdeckt, ist zu prüfen (Aufgabe für Stufe 2).
- In der EU sind Preise schon heute Bruttopreise; der US-Befund zur Sichtbarkeit überträgt sich nur auf die zusätzliche Kennzeichnung (Label
  am Regal). Dass ein sichtbares Label die Lenkung verstärkt, ist plausibel, aber nicht belegt (Belegstufe C).

### 2.8 CO₂-Preis und Rückgabe über die Dividende

**Belege**

- **Kanada und Schweiz:** geringe Kenntnis der Rückgabe und deutliche Unterschätzung der Beträge; persönliche Information wirkte in der Schweiz
  leicht positiv, in Kanada bei konservativen Wählern eher negativ; Wahrnehmung folgt stärker der Parteibindung als dem eigenen Vorteil
  (Mildenberger u. a., Nature Climate Change 2022).
- **Frankreich (Gelbwesten):** Befragte überschätzen ihre Nettoverluste, halten die Steuer mit Rückgabe für regressiv und für ökologisch
  unwirksam; Informationen ändern die Überzeugungen nur wenig, geänderte Überzeugungen erhöhen die Zustimmung aber deutlich (Douenne/Fabre,
  AEJ: Economic Policy 2022).

**Einordnung:** Eine Rückgabe allein sichert keine Zustimmung. Das Goldene Drittel verbindet die Rückgabe mit einer sichtbaren, monatlichen
Zahlung unter eigenem Namen; das ist sichtbarer als die Schweizer Rückgabe über die Krankenkassenprämie. Ob das reicht, ist offen (Belegstufe
B). Für **Frankreich** ist das Akzeptanzrisiko belegt und hoch.

### 2.9 Erbschaft und große Vermögen

**Belege**

- **Dänemark (Vermögensteuer 1989–1997 gesenkt und abgeschafft):** Das steuerpflichtige Vermögen der sehr Vermögenden stieg nach acht Jahren
  um rund 30 % stärker, das der mäßig Vermögenden um rund 10 % (Senkung des Satzes 1,2 bzw. 1,84 Punkte); bei den sehr Vermögenden vermuten die
  Autoren einen Teil als Ausweichen, ohne ihn zu beziffern (Jakobsen u. a., QJE 2020; NBER w24371; maschinell aus dem PDF gelesen, an der Quelle
  zu prüfen).
- **Wanderung hoch Bezahlter:** Ein Vorzugstarif für zugewanderte Spitzenverdiener verdoppelte in Dänemark ihre Zahl; Elastizität der Wanderung
  bezogen auf den Nettosatz rund 1,5 bis 2 (Kleven u. a., QJE 2014; NBER w18885). Der Befund gilt für Zuwanderer mit Vorzugstarif, nicht für
  Einheimische.

**Einordnung:** Die Ausweichbänder in `ausweichen33.json` (Erbschaft 50 %, Vermögen 75 % im ungünstigen Fall) liegen in der Größenordnung, die
der dänische Befund für die Spitze nahelegt; eine direkte Umrechnung steht aus (Stufe 2). Weil das Goldene Drittel die Vermögensteuer auf die
Einkommensteuer anrechnet und in 30 Staaten zugleich gilt, ist der Ausweichweg über Wegzug innerhalb der EU kleiner als bei einem Einzelstaat
(Annahme, Belegstufe C). Wegzug in Drittstaaten bleibt (Exit-Regeln, offener Punkt P1/R4).

### 2.10 Rentenregel E und Verlustaversion

**Belege (allgemein, nicht zur Regel):** Verluste wiegen in Entscheidungen schwerer als gleich große Gewinne (Kahneman/Tversky, Econometrica
1979; in der Folgearbeit 1992 ein Faktor um 2); Menschen bevorzugen den bestehenden Zustand (Samuelson/Zeckhauser, Journal of Risk and
Uncertainty 1988). Belegstufe A für den Befund, C für die Übertragung.

**Einordnung**

- Nach Regel E haben 30,7 % der Rentnerhaushalte mehr, im Mittel −124 € im Monat (`rentner_kombi.json`). Die Verluste konzentrieren sich im
  oberen Fünftel (−479 €). Mit Verlustaversion ist die wahrgenommene Bilanz der Rentner deutlich schlechter als die gerechnete.
- Mögliche Verhaltenswirkungen: früherer Rentenbeginn vor dem Stichtag, um unter alte Regeln zu fallen (Vorzieheffekt); politischer
  Widerstand. Regel E nimmt Teile davon auf (Kürzung nur über dem Grundbedarf, Wegfall der KV- und PV-Beiträge). Ob ein Stichtag Vorzieheffekte
  auslöst, hängt davon ab, ob früher beginnende Renten ebenfalls gekürzt werden – zu klären in der Ausgestaltung.
- Framing: Die Wirkung der Darstellung („Kürzung“ gegen „neuer Boden plus Beitragsfreiheit“) ist in Experimenten gut belegt; die Initiative
  sollte die Verluste trotzdem offen nennen (Haltung der Initiative; sonst Vertrauensschaden).

## 3 | Übertragbarkeit in die Länder

| Gesichtspunkt | DE | FR | IT | ES | PL |
|---|---|---|---|---|---|
| Nicht-Inanspruchnahme der Mindestsicherung heute | hoch (Grundsicherung im Alter ~60 %; eigene Rechnung 69 %) | RSA 34 % (2018) | ADI: keine Quote geprüft | IMV: Hinweise auf hohe Quote, nicht geprüft | keine Quote geprüft |
| Wirkung „ohne Antrag“ | groß | groß | vermutlich groß | vermutlich groß | offen |
| Vertrauen in Pflichtvorsorge | mittel (Riester-Erfahrung, Annahme) | mittel | mittel | mittel | **gering** (OFE 2014) |
| Nicht angemeldete Arbeit, selbst erklärtes Einkommen | gering bis mittel | mittel | höher (Annahme gestützt auf Eurobarometer 498) | höher (ebenso) | höher (Annahme) |
| Akzeptanz CO₂-Preis mit Rückgabe | mittel | **gering** (Gelbwesten, Douenne/Fabre) | offen | offen | gering (Kohle, Annahme) |
| Splitting heute | ja (Ehegatten) | ja (quotient familial) | nein (individuell) | wahlweise gemeinsam | wahlweise gemeinsam |
| Zweitverdienerwirkung des Wegfalls | groß | mittel | klein | mittel | mittel |

Die Spalten IT, ES und PL beruhen überwiegend auf Annahmen. Die Angaben zur Ehegattenbesteuerung sind Sekundärwissen der Initiative und an den
OECD-Länderberichten (Taxing Wages) zu prüfen. Folgerung für R5 (Übertragbarkeit): Neben Löhnen, Mehrwertsteuer nach Einkommen, Rentenformen und
Mieten sind je Staat drei Verhaltensgrößen zu erheben: (1) Nicht-Inanspruchnahme der heutigen Mindestsicherung, (2) Anteil selbst erklärter
und nicht erklärter Einkommen, (3) Vertrauen in staatliche Zusagen (z. B. Eurobarometer, Vertrauen in Regierung und Parlament).

## 4 | Was gelingt durch die neuen Anreize – vorläufiges Urteil

**Gut belegt und gleichgerichtet**

1. **Leistung ohne Antrag** erreicht Berechtigte, die heute leer ausgehen (DE, FR belegt). Die Kosten sind in der Rechnung bereits voll angesetzt.
2. **Pflichtvorsorge** erhöht die Ersparnis der passiven Mehrheit; Voraussetzung ist Vertrauen in das Eigentum am Konto.
3. **Dividende** führt nach den vorliegenden Studien nicht zu einem nennenswerten Rückzug aus der Arbeit; leichte Verschiebung zu Teilzeit möglich.

**Plausibel, schwächer belegt**

4. **Niedrigerer, einheitlicher Entzug (50 %)** erleichtert den Einstieg in Arbeit; die Stundenwirkung im Abschmelzbereich ist offen.
5. **Einfacher Tarif ohne Abzüge und ohne Splitting** stärkt Steuerehrlichkeit und Arbeit von Zweitverdienern.

**Risiken, die die Konstruktion begrenzen muss**

6. **Weitergabe** kommt ohne Pflicht nicht sicher an (Schweden) – die Rückfallregel ist notwendig, nicht nur vorsichtig.
7. **Mehrwertsteuer-Senkungen** kommen schwächer an als Erhöhungen (EU-Befund) – Preisniveau eher am oberen Rand des Bandes.
8. **CO₂-Rückgabe** wird unterschätzt; Zustimmung ist vor allem in FR gefährdet.
9. **Spitzenvermögen** weichen aus; das Band in `ausweichen33.json` ist gegen den dänischen Befund zu prüfen.
10. **Rentner** erleben Verluste stärker als gerechnet; Akzeptanzrisiko in der größten Wählergruppe.

Keiner dieser Befunde stellt die Rechnung grundsätzlich in Frage; mehrere zeigen, dass Teile der Wirkung von der Ausgestaltung abhängen, die
das Konzept noch offen lässt (Auszahlung von Amts wegen, Eigentumsschutz der Vorsorge, Stichtag der Rentenregel, Sichtbarkeit der Dividende). Antworten der Initiative und Einordnung: Abschnitt 8.

## 5 | Nächste Schritte (Stufe 2, quantitativ)

| Nr. | Schritt | Grundlage | Wirkung auf |
|---|---|---|---|
| V1 | Grenzbelastung 0–30.000 € heute/neu je Haushaltstyp | Mikrosimulation, § 11b SGB II | Abschnitt 2.2 |
| V2 | Arbeitsangebot als Band: Beteiligungs- und Stundenelastizitäten aus der Literatur auf die Mikrosimulation | Mikrosimulation; Elastizitäten mit Quelle | Aufkommen, Dividende |
| V3 | Asymmetrische Überwälzung im Preisniveau (Senkung 40 %, Erhöhung 100 % als Variante) | Benzarti u. a. 2020 | `preisniveau33` |
| V4 | Ausweichband Vermögen gegen Jakobsen u. a. 2020 umrechnen | Volltext QJE | `ausweichen33` |
| V5 | Länderwerte zu Nicht-Inanspruchnahme, nicht erklärter Arbeit und Vertrauen | Eurostat, Eurobarometer, nationale Studien | R5 |
| V6 | Akzeptanzbefragung (Conjoint, mit und ohne Information über den eigenen Betrag) | eigene Erhebung, Kooperationspartner | Darstellung |

## 6 | Grenzen dieser Voruntersuchung

- Die Literaturauswahl ist nicht systematisch (keine Metaanalyse, keine Suchstrategie mit Ein- und Ausschlusskriterien). Sie erfasst Studien, die
  in der Fachdiskussion häufig zitiert werden; das bevorzugt veröffentlichte, eher deutliche Befunde.
- Die meisten Belege stammen aus Einzelreformen in einem Staat. Das Goldene Drittel ändert viele Regeln gleichzeitig; Wechselwirkungen
  (z. B. Dividende und Halbanrechnung zusammen) sind nicht untersucht.
- Mehrere Zahlen sind nur aus Abstracts gelesen; die Volltexte enthalten Einschränkungen, die hier fehlen können.
- Die psychologischen Befunde (Verlustaversion, Status quo) sind gut belegt, ihre Übertragung auf die konkrete Reform ist Urteil.

## 8 | Antworten der Initiative zu den Gestaltungsfragen (24.10.2026) und Einordnung

| Frage | Antwort der Initiative | Einordnung nach den Belegen | Status |
|---|---|---|---|
| Aufstockung von Amts wegen oder auf Antrag? | „Die Kommune zahlt die Aufstockung auf Antrag?“ (mit Fragezeichen) | Ein Antrag erhält einen Teil der heutigen Nicht-Inanspruchnahme (DE ~60 % bei der Grundsicherung im Alter, FR 34 % beim RSA). Was nach Bhargava/Manoli wirkt, ist mit einem Antrag vereinbar: ein Hinweisschreiben von Amts wegen an Haushalte, deren Steuer- und Lohndaten einen Anspruch nahelegen, mit vorausgefülltem Antrag und dem Betrag; Weiterbewilligung ohne neuen Antrag, solange die Daten passen. Vorschlag: **Antrag mit Hinweis und Vorausfüllung von Amts wegen.** Die Rechnung setzt auf beiden Seiten (heute, neu) volle Inanspruchnahme an; mit Antrag ist die Wirkung unten kleiner als ausgewiesen, die Kosten auch | **entschieden v4.50:** auf Antrag, mit Hinweis und Vorausfüllung von Amts wegen (E12) |
| Eigentum am Vorsorgekonto | Sperrkonto mit Altersgrenze, ggf. Wahloptionen für die Anlage | Die Sperre schützt gegen vorzeitiges Entnehmen durch den Sparer, nicht gegen den Zugriff des Gesetzgebers (Polen 2014: per Gesetz übertragen, 2015 vom Verfassungsgericht als öffentliche Mittel eingestuft; Sekundärquelle). Dafür braucht es zusätzlich Verwahrung außerhalb des Staatshaushalts bei getrennten Trägern, Pfändungs- und Insolvenzschutz und eine ausdrückliche Eigentumszuordnung (Rechtsprüfung P1). Zur Wahl der Anlage: In Schweden (Prämienpension, 2000 rund 460, 2004 rund 660 Fonds) trafen 2000 noch 67 % eine eigene Wahl, bei späteren Berufsanfängern nur noch rund 8 bis 18 %; der Standardfonds erhielt 2003 rund 90 % der Beiträge (SSA, Social Security Bulletin 65(4); Cronqvist/Thaler, AER 2004). Folgerung: **wenige Wahloptionen und ein sorgfältig gestalteter Standardfonds** für die passive Mehrheit (vgl. Abschnitt 2.4: 85 % passive Sparer) | entschieden (Sperrkonto, Anlagewahl; v4.50 wenige Optionen und Standardfonds) |
| Rentenkürzung und Stichtag | Die Kürzung bezieht sich pauschal auf Rentenzahlungen | Gilt die Kürzung für alle Zahlungen aus dem alten System ab dem Stichtag, gleich wann die Rente begann, entfällt der Anreiz, den Rentenbeginn vor den Stichtag zu ziehen. Das entspricht der Rechnung (Regel E auf alle Zusagen über dem Grundbedarf). Bleibt: Abschläge für frühen Rentenbeginn und anteilige Verrechnung (T1) für Übergangsjahrgänge wirken wie bisher | entschieden, Vorzieheffekt aus der Kürzung entfällt |
| Dividende als Rückgabe des CO₂-Preises? | Nicht ausschließlich; es geht auch um Digitalisierungsgewinne, z. B. aus der Plattformbesteuerung | Sachlich richtig: Die Dividende ist der Rest nach allen Aufgaben, nicht zweckgebunden. Bezifferbar ist bisher nur der Anteil der Lenkungseinnahmen; der Anteil der Plattformbesteuerung ist nicht ausgewiesen, weil die Basis der Unternehmensposition nicht belegt ist (B23, R4). Für die Akzeptanz (Abschnitt 2.8) spricht eine breitere Begründung nicht dagegen: Die Ablehnung in FR und Kanada hing an der wahrgenommenen Belastung durch den CO₂-Preis. Konzept angepasst (v4.49) | entschieden; Anteil Plattformen zu beziffern (R4) |
| Mehrwertsteuer-Label und Überwälzung | Wettbewerb um Nachhaltigkeit: Anbieter bemühen sich um günstigere Sätze durch Zertifizierung bei qualifizierten, zugelassenen, staatlich überwachten Stellen; das wirkt einer stummen Weitergabe von Mehrkosten entgegen | Plausibel als Mechanismus: Wo ein Anbieter durch Zertifizierung eine günstigere Stufe erreicht und Wettbewerber in derselben Gütergruppe nicht, kann er die Ersparnis im Preis zeigen oder als Marge behalten; Wettbewerb und das sichtbare Label sprechen für Weitergabe. Belegt ist das nicht (Belegstufe C); Benzarti u. a. fanden die Asymmetrie gerade bei allgemeinen Satzsenkungen ohne Wettbewerbsvorteil des Einzelnen. Zwei Risiken: (1) **Zertifizierer** – Unabhängigkeit, Interessenkonflikte und Gefälligkeitsprüfungen sind ein bekanntes Problem von Zertifizierungsmärkten (Dranove/Jin, JEL 2010, Übersichtsarbeit; Befunde im Volltext nicht geprüft); staatliche Zulassung, Rotation, Stichproben und Haftung begrenzen es. (2) **Europarecht** – Nach dem Neutralitätsgrundsatz dürfen gleichartige, miteinander im Wettbewerb stehende Waren nicht unterschiedlich besteuert werden; maßgeblich ist die Sicht des Durchschnittsverbrauchers (EuGH C-515/20 vom 3.2.2022; Sekundärquelle PwC-Blog, an der Quelle zu prüfen). Ein anbieterbezogener Satz für sonst gleiche Waren muss sich daran messen lassen: Die Zertifizierung müsste eine objektive, für Verbraucher erkennbare Eigenschaft begründen. Zur Rechtsprüfung P1 | entschieden (Mechanismus); Rechtsprüfung und Variante V3 offen |

Folgerung für Stufe 2: V3 (asymmetrische Überwälzung) bleibt als Variante sinnvoll, mit zwei Fällen: allgemeine Satzänderung (Benzarti) und
zertifizierungsgetriebene Senkung (Wettbewerb, Annahme höherer Weitergabe).

## 7 | Quellen (abgerufen am 24.10.2026)

- Benzarti, Y., Carloni, D., Harju, J., Kosonen, T. (2020): What Goes Up May Not Come Down: Asymmetric Incidence of Value-Added Taxes. JPE 128(12). Zusammenfassung: [VATT](https://vatt.fi/en/-/vat-cuts-do-not-increase-consumer-purchasing-power)
- Bhargava, S., Manoli, D. (2015): Psychological Frictions and the Incomplete Take-Up of Social Benefits. AER 105(11). [IDEAS](https://ideas.repec.org/a/aea/aecrev/v105y2015i11p3489-3529.html)
- Bick, A., Fuchs-Schündeln, N. (2018): Taxation and Labour Supply of Married Couples across Countries. Review of Economic Studies 85(3). [CEPR DP9115](https://repec.cepr.org/repec/cpr/ceprdp/DP9115.pdf)
- Blömer, M., Hansen, E., Peichl, A. (2024): Die Ausgestaltung des Transferentzugs. ifo Forschungsbericht 145. [ifo](https://www.ifo.de/publikationen/2024/monographie-autorenschaft/die-ausgestaltung-des-transferentzugs)
- Cronqvist, H., Thaler, R. (2004): Design Choices in Privatized Social-Security Systems: Learning from the Swedish Experience. AER 94(2). [IDEAS](https://ideas.repec.org/a/aea/aecrev/v94y2004i2p424-428.html)
- Chetty, R., Friedman, J., Leth-Petersen, S., Nielsen, T., Olsen, T. (2014): Active vs. Passive Decisions and Crowd-Out in Retirement Savings Accounts. QJE 129(3). [NBER w18565](https://www.nber.org/papers/18565)
- Chetty, R., Friedman, J., Saez, E. (2013): Using Differences in Knowledge across Neighborhoods to Uncover the Impacts of the EITC on Earnings. AER 103(7). [NBER w18232](https://nber.org/papers/w18232)
- Chetty, R., Looney, A., Kroft, K. (2009): Salience and Taxation. AER 99(4). [NBER w13330](https://www.nber.org/papers/w13330)
- DIW (2019): Starke Nichtinanspruchnahme von Grundsicherung deutet auf hohe verdeckte Altersarmut. Wochenbericht 49/2019. [DIW](https://www.diw.de/de/diw_01.c.699957.de/publikationen/wochenberichte/2019_49/starke_nichtinanspruchnahme_von_grundsicherung_deutet_auf_hohe_verdeckte_altersarmut.html)
- DREES (2022): Mesurer régulièrement le non-recours au RSA et à la prime d'activité. Les Dossiers de la DREES 92. [DREES](https://drees.solidarites-sante.gouv.fr/publications-communique-de-presse/les-dossiers-de-la-drees/mesurer-regulierement-le-non-recours-au)
- Dranove, D., Jin, G. Z. (2010): Quality Disclosure and Certification: Theory and Practice. Journal of Economic Literature 48(4). [NBER w15644](https://www.nber.org/papers/w15644)
- Douenne, T., Fabre, A. (2022): Yellow Vests, Pessimistic Beliefs, and Carbon Tax Aversion. AEJ: Economic Policy 14(1). [IDEAS](https://ideas.repec.org/a/aea/aejpol/v14y2022i1p81-110.html)
- Eurofound (2015): Access to social benefits: Reducing non-take-up. [Eurofound](https://www.eurofound.europa.eu/en/publications/all/access-social-benefits-reducing-non-take)
- EuGH, Urteil vom 3.2.2022, C-515/20 (Neutralitätsgrundsatz bei ermäßigten Sätzen), nach PwC-Blog [Update: Bedeutung des Neutralitätsgrundsatzes](https://blogs.pwc.de/de/steuern-und-recht/article/233341/update-bedeutung-des-neutralitaetsgrundsatzes-fuer-steuersatzermaessigungen/) (Sekundärquelle)
- Europäische Kommission / ELA, Williams, C., Horodnic, I. (2020): Undeclared work in the European Union (Special Eurobarometer 498). [ELA](https://www.ela.europa.eu/sites/default/files/2022-06/KE-02-20-972-EN-N_0.pdf)
- Gorodnichenko, Y., Martinez-Vazquez, J., Sabirianova Peter, K. (2009): Myth and Reality of Flat Tax Reform. JPE 117(3). [NBER w13719](https://www.nber.org/papers/w13719)
- Jakobsen, K., Jakobsen, K., Kleven, H., Zucman, G. (2020): Wealth Taxation and Wealth Accumulation: Theory and Evidence from Denmark. QJE 135(1). [NBER w24371](https://www.nber.org/papers/w24371)
- Jones, D., Marinescu, I. (2022): The Labor Market Impacts of Universal and Permanent Cash Transfers: Evidence from the Alaska Permanent Fund. AEJ: Economic Policy 14(2). [NBER w24312](https://www.nber.org/papers/w24312)
- Kahneman, D., Tversky, A. (1979): Prospect Theory. Econometrica 47(2). Tversky, A., Kahneman, D. (1992): Advances in Prospect Theory. Journal of Risk and Uncertainty 5. (Standardliteratur, nicht erneut abgerufen)
- Kleven, H., Knudsen, M., Kreiner, C., Pedersen, S., Saez, E. (2011): Unwilling or Unable to Cheat? Econometrica 79(3). [NBER w15769](https://nber.org/papers/w15769)
- Kleven, H., Landais, C., Saez, E., Schultz, E. (2014): Migration and Wage Effects of Taxing Top Earners. QJE 129(1). [NBER w18885](https://www.nber.org/papers/w18885)
- Madrian, B., Shea, D. (2001): The Power of Suggestion. QJE 116(4). [NBER w7682](https://www.nber.org/papers/w7682)
- Medina, L., Schneider, F. (2018): Shadow Economies Around the World. IMF WP 18/17. [IMF](https://www.imf.org/en/Publications/WP/Issues/2018/01/25/Shadow-Economies-Around-the-World-What-Did-We-Learn-Over-the-Last-20-Years-45583) (nur zur Abgrenzung genannt, Werte nicht verwendet)
- Mildenberger, M., Lachapelle, E., Harrison, K., Stadelmann-Steffen, I. (2022): Limited impacts of carbon tax rebate programmes on public support for carbon pricing. Nature Climate Change 12(2). [BORIS Bern](https://boris.unibe.ch/169899)
- Saez, E. (2002): Optimal Income Transfer Programs: Intensive versus Extensive Labor Supply Responses. QJE 117(3). (Standardliteratur, nicht erneut abgerufen)
- Saez, E., Schoefer, B., Seim, D. (2019): Payroll Taxes, Firm Behavior, and Rent Sharing: Evidence from a Young Workers' Tax Cut in Sweden. AER 109(5). [NBER w23976](https://www.nber.org/papers/w23976)
- Samuelson, W., Zeckhauser, R. (1988): Status Quo Bias in Decision Making. Journal of Risk and Uncertainty 1. (Standardliteratur, nicht erneut abgerufen)
- SII (Stowarzyszenie Inwestorów Indywidualnych): 8 lat od pierwszego skoku na OFE. [SII](https://www.sii.org.pl/15073/analizy/newsroom/8-lat-od-pierwszego-skoku-na-ofe-na-drugi-gieldowy-wciaz-czekamy.html) (Sekundärquelle)
- SSA (2004): Design and Implementation Issues in Swedish Individual Pension Accounts. Social Security Bulletin 65(4). [SSA](https://www.ssa.gov/policy/docs/ssb/v65n4/v65n4p38.html)
- STM, Sozial- und Gesundheitsministerium Finnland (2020): Ergebnisse des Grundeinkommensexperiments. [STM](https://stm.fi/en/-/perustulokokeilun-tulokset-tyollisyysvaikutukset-vahaisia-toimeentulo-ja-psyykkinen-terveys-koettiin-paremmaksi)
- Vivalt, E., Rhodes, E., Bartik, A., Broockman, D., Miller, S. (2024): The Employment Effects of a Guaranteed Income. NBER w32719. [NBER](https://www.nber.org/system/files/working_papers/w32719/w32719.pdf)

Hinweis zu Personennamen: Genannt sind nur Autorinnen und Autoren veröffentlichter Studien als bibliografische Angabe.
