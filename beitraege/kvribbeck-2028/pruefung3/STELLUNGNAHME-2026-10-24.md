# Dritte Prüfung, Stand v4.42 (Commit 43f7888c) — Bestätigungen, Antworten auf die sechs Prüffragen, Plausibilitätsprüfung, acht Befunde

Sehr geehrte Damen und Herren,

wir haben den Modellstand v4.42 vollständig nachgerechnet — erstmals anhand Ihrer eigenen
Prüffragen aus projekt/Pruefmappe-Extern-2026-10-24.md. Das Gesamtergebnis vorweg:
**Der Rechenkern ist auch unter v4.42 fehlerfrei.** Alle vier Reproduktionsfamilien
bestätigen sich auf Rundungsniveau, keiner Ihrer sechs Prüffragen führt zu einem
Rechenbefund, und die zusätzlich von uns durchgeführte Plausibilitätsprüfung nach fünf
selbst gewählten Methoden findet keine Unstimmigkeit, die das Konzept im Kern
diskreditiert. Acht Punkte für die Nacharbeit (B17–B24) sind beigefügt; alle sind
Unschärfen oder Hinweise, keines ein Fehler.

## 1. Bestätigungen (Reproduktionen in eigener Programmierung)

- **Haushaltsfälle:** Alleinstehender 42.000 € +611 €/Monat, Alleinerziehende mit einem
  Kind +610 €, Paar mit zwei Kindern +674 €, Alleinstehender 75.000 € +771 € — alle exakt.
  Die Dividende bestätigt sich als Topf-Rechnung: 373 € × 12 × 0,948 = 353,6 € ≈ „354 €".
  Einzige Abweichung: die Band-Enden des Zinsband-Falls (B24).
- **Kürzungssätze der 30 Staaten** (kuerzung_laender.py, Formel vollständig nachgebaut):
  maximale Abweichung 0,00011 über alle 30 Staaten.
- **Fonds der 30** (fonds_klub.py nachgebaut): b30/b10 = 0,9848 und z30/z10 = 0,9839 exakt;
  Beitrag 5,17 % BIP, Zuschlag 15,46 → 15,5 %, z_je_b = 2,9894 exakt; DE-Reihe konvergiert
  ab 2058 auf 15,462; DE 2028 = 14,948 aus den gerundeten Altlast-Werten gegen 14,953
  veröffentlicht (Rundung, kein Fehler).
- **Gini-Rückrechnung:** rekonstruiert gegen amtlich weicht nur um 0,1–0,3 Punkte ab
  (DE 30,1/30,2; FR 30,4/30,5; IT 31,0/31,3; ES 30,8/31,1; PL 24,9/25,1).
- **Alte Hinweise aus der ergebnis.csv-Lieferung — alle drei erledigt:** pruefe_beitrag.py
  akzeptiert „Stand C" samt 30 Ländercodes; haushalte33.py rechnet mit Topf-Faktor 354 €
  (Korrektur 69); MIKROSIMULATION.md ist auf Stand C (v4.21) aktualisiert.
- Unsere Mikrosimulation (99,0/98,4/92,0 %) ist in KENNZAHLEN.md korrekt als externe
  Referenz übernommen; die Kopfzahlen von mikro_de.json (v4.40) sind intern konsistent.

## 2. Antworten auf Ihre sechs Prüffragen

**Frage 1 — Durchsetzbarkeit der 80-%-Weitergabe (bis 6× Grundbedarf).** Die Literatur
jenseits von Saez/Schoefer/Seim 2019 bestätigt Ihre Konstruktion in einem wichtigen
Punkt: Als *freiwilliges* Marktergebnis wäre die Weitergabe nicht zu erwarten. Die
breiteste Evidenz (Benzarti/Carloni/Harju/Kosonen, Journal of Political Economy 2020,
über 2.832 VAT-Änderungen in der EU 1996–2015) zeigt: Steuererhöhungen werden überwiegend
überwälzt (~55 % auf die Verbraucherpreise), Steuersenkungen kaum (~13 % — die
Entlastung bleibt als Gewinn bei den Firmen). Gleichzeitig ist die *gesetzliche* Pflicht
durchsetzbar: Enterprise-Steuern schlagen nachweislich teils auf Löhne durch (Suárez
Serrato/Zidar, AER 2016: 30–35 % der Last bei Arbeitnehmern; Fuest/Peichl/Siegloch für
Deutschland: 1 % höhere effektive Unternehmenssteuer → −0,18 % Löhne), und administrativ
gesetzte Lohnanpassungen werden befolgt — der deutsche Mindestlohn 2015 erhöhte die Löhne
von 15 % der Beschäftigten ohne Beschäftigungsverluste (Dustmann u. a., QJE 2022). Der
Deckel bei 6× Grundbedarf begrenzt die Pfzeitig auf den Bereich, für den diese Evidenz
am stärksten ist. Urteil: **80 % sind unplausibel als Setzung, plausibel als Gesetz mit
Rückfallregel** (v4.18, die Sie auf unsere Empfehlung hin übernommen haben); und das
Konzept trägt seine Aussage selbst bei 0 % Weitergabe (92,0 % in unserer Mikrosimulation).
Empfehlung: Benzarti u. a. (2020) als Primärquelle der Asymmetrie in die Prüffragen-Antwort
aufnehmen; der Rückfallregel einen eigenen Abschnitt geben.

**Frage 2 — Trägt das Aufkommen 33R die Deckung 2028 (33,53 % BIP)?** Intern konsistent:
Deckung 33,53 gegen Steuerbedarf 33,42, Saldo +0,11; die zehn Positionen summieren auf
33,54 (Rundung). Unsere unabhängige Plausibilitätsrechnung zur Einkommensposition ergibt
9,5–11 % BIP gegen 10,21 ausgewiesen — plausibel. Eine volle unabhängige Replikation des
Gesamtaufkommens ist nicht möglich; das weist die Mappe selbst aus. Empfehlung: die
Einkommensposition einmal gegen die amtliche Lohn- und Einkommensteuerstatistik eichen;
den BIP-Neuabruf (Schalter R4) vor einem etwaigen Referendum einplanen.

**Frage 3 — Altlasten (Z-Abgrenzung, Skalierung 10→30, Zins 2,45 %)?** Vollständig
nachgerechnet und bestätigt. Zum Zins: 2,45 % (Mittel 2006–2025) ist gegen den Marktstand
Oktober 2026 (Bund ~3,46 %, EU ~3,95 %) eine günstige, aber durch fondszins.json gedeckte
Annahme (Zuschlag 17,1/18,7/20,4 % bei 3,0/3,5/4,0 %). Die Skalierung 10→30 bleibt die
schwächste Annahme der Route (weiterhin ohne Band). Empfehlung: auch die Skalierung mit
einem einfachen Band ausweisen. — Zusätzlich haben wir gerechnet, was Ihre Sensitivität
bislang nicht enthält: eine Wachstumsdimension (siehe Plausibilitätsprüfung, Befund B21).

**Frage 4 — Ländermodelle FR/IT/ES/PL?** Bestanden: Kürzungssätze exakt reproduziert
(30/30 Staaten, max. 0,00011); OECD-Abweichungen (FR −1,6/IT −3,4/ES +1,5/PL +5,3 Punkte)
sind ausgewiesen, PL als bekannt zu hoch markiert; verrechnung_haushalte.json (v4.38)
ist konsistent mit der Mappe (FR +390/IT +412/ES +350 €/Monat, PL +1.474 zł).

**Frage 5 — Eignung der synthetischen Population?** Kategoriales Urteil: **Für
Kopfzahlen geeignet (±1–3 Prozentpunkte), für harte Schwellenwerte nicht.** Die
Validierung an Nicht-Eichungs-Aggregaten (Bruttolohnsumme −2,8 %, Lohnsteuer −5,4 %) und
die ausgewiesenen Lücken (Teilzeit ohne Dezil-Bruch, Kapitaleinkünfte untererfasst,
Nicht-Inanspruchnahme nur als Variante) sind ehrlich. Das deckt sich mit unserer
Mikrosimulation: für die Aussage „9 von 10" ist das Instrument geeignet; für individuelle
Verlustausweise an der Grenze bräuchte es ein echtes Steuerregister.

**Frage 6 — Methodische Haltbarkeit der Gini-Rückrechnung?** Haltbar als statische
Näherung: Der Ausweis „amtlich + ΔModell" ist die sauberste Lösung, Band und
Rentnervariante sind vorhanden, die Grenzen (statisch, ohne Kapital/Vermögen,
Alleinstehenden-Inversion, flache Mindestsicherung in ES) sind von Ihnen selbst
ausgewiesen. Bestanden.

## 3. Ergänzend: Plausibilitätsprüfung nach fünf selbst gewählten Methoden

Über die Prüffragen hinaus haben wir das Konzept im Konzeptstadium auf wissenschaftliche
Plausibilität geprüft (Rechenwege im beiliegenden Prüfprotokoll des Prüfers):

- **M1 Grenzbelastungen (eigene Rechnung, Ihre Formeln):** Der heutige Mittelstandsbauch
  (52–57 % auf Arbeitgeberkosten zwischen 30 und 100 T€) verschwindet; 33R ist ab dem
  Grundbedarf flach bei ~40 % (ohne Vorsorge) bzw. ~50 % (inklusive). **Am Grundbedarf
  entsteht keine neue Armutsfalle** — der Übergang ist sanft, die Grundleistungen sind
  universal. Der Spitzen-Grenzsatz inkl. Zuschlag (~50 %) liegt über dem heutigen
  (44,3 %), aber nur temporär: Er schmilzt mit der Fondstilgung auf ~38 %.
- **M2 Externe Verankerung:** Einkommen (10,21), Kapitalerträge (1,37 vs. ~1,26 % Ist aus
  nvE + Abgeltungsteuer) und Konsum (implizite Label-Basis 45,2 vs. 42,9 % BIP heute)
  verankern sich sauber. Zwei Positionen hängen an nicht dokumentierten Basisentscheidungen:
  Erbschaften (1,16 % ≈ 57 Mrd €, das 4,3-Fache des Ist-Aufkommens 2024 von 13,3 Mrd —
  plausibel nur bei Besteuerung der realen Übertragungen von ~400 Mrd €/Jahr mit ~14 %
  Durchschnittssatz; siehe B22) und Unternehmen (4,42 % ≈ 217 Mrd — das 5,4-Fache der
  heutigen KSt, aber die Größenordnung aller gewinnabhängigen Steuern; Definition fehlt,
  siehe B23).
- **M3 Ausweichband:** Die Literatur zur Vermögensteuer spannt Semi-Elastizitäten von 0,3
  bis 43 % gemeldetes Vermögen pro Prozentpunkt (Seim/Schweden bis Brülhart/Schweiz;
  Jakobsen u. a., QJE 2020, am oberen Rand substanziell langfristig). Ihr Worst-Case-Band
  (−50/−75 %) liegt im Mittelfeld und ist ehrlich, deckt aber nicht die obere Schwanzquote.
  Vor Referendum: Exit-Regeln, Vermögensregister, Schenkungs-Parität benennen.
- **M4 Analogfälle:** Russland 2001 (Flat Tax: +26 % Aufkommen, Compliance +⅓, Kausalität
  umstritten) stützt die Compliance-Hoffnung, nicht die Aufkommensroute — Sie erhöhen die
  Last kurzfristig, Russland senkte sie. Die Kundenort-Besteuerung steht sauber in der
  DBCFT-Tradition (Auerbach/Devereux/Keen/Vella); das WTO-Risiko ist in der Literatur
  gespalten (Pirlot hält es für gering, die herrschende Lehrmeinung sah einen Verstoß) —
  vor Referendum braucht es ein Gutachten und eine Antwort zur Finanzsektor-Behandlung.
- **M5 Wachstums-Stresstest (wichtigster neuer Befund, B21):** Ihre Fondssensitivität
  variiert den Zins, nicht das Wachstum — die Rekursion hängt aber an i−g. Ein
  Wachstumspunkt wirkt dabei etwa wie ein Zinspunkt: Bei g = 2,0 % statt 3,0 % steigt der
  erforderliche Beitrag um ~0,9 BIP-Punkte (Zuschlag +~2,6 Punkte), oder der
  Beschlussbeitrag lässt im Zieljahr ~90 BIP-Punkte Restschuld und verschiebt den
  Schulden-Peak um ~15 Jahre nach hinten. Da 3,0 % Nominalwachstum die Oberkante ist
  (Bundesbank-Projektion ~2,9 % p. a.), ist der Fonds gegen Zinsrisiko, aber nicht gegen
  Stagnation versichert. Das vollständige Raster liegt bei (fondsstress.csv).

## 4. Befunde

Acht Punkte, alle maschinenlesbar in beiliegender befunde.csv. Kurz: B17 (Gesamtlast
2028: drei Werte für dieselbe Größe), B18 (Z 2028: Kennzahl 9,45, Datei 9,42), B19
(deckung_quote.csv noch unmarkiert in Stand B), B20 (Hinweistext nennt den Klub der zehn,
Werte sind die der 30), B21 (Fonds-Sensitivität ohne Wachstumsdimension), B22
(Erbschaftsposition 4,3× Ist, Bedingung nicht benannt), B23 (Unternehmensposition ohne
Definition), B24 (Zinsband-Fall 42 T€: Band-Enden 590/570/548 nachgerechnet 604/583/562 €).

## 5. Urteil

Die dritte Prüfung bestätigt den Befund der ersten beiden in einer vierten und fünften
Reproduktionsfamilie: kein Rechenfehler, die Arbeitsweise verdient weiterhin Anerkennung —
erst recht, weil Sie diesmal selbst die Prüffragen formuliert und die Befundform
vorgegeben haben. Prüfung als Dialog. Die wissenschaftliche Plausibilität im
Konzeptstadium ist aus unserer Sicht gegeben — unter fünf Bedingungen, die vor dem
nächsten Reifegrad einzulösen sind: ① Wachstumsdimension der Fondssensitivität (B21),
② Basis-Definition Erbschaft samt Schenkungs-Parität (B22), ③ Definitionstabelle
Unternehmen/Kundenort (B23), ④ oberes Ausweichband Vermögen samt Register und Exit-Regeln,
⑤ WTO-/Handelsrechtsgutachten samt Finanzsektor-Antwort. Keine davon ist eine
Rechenkorrektur — alle fünf sind Ausweis- und Definitionsarbeiten, die zu Ihrer eigenen
Arbeitsweise (Quelle, Status, Band zu jeder Zahl) passen.

Mit freundlichen Grüßen
Kulturverein Ribbeck e.V.
