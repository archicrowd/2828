# Wirtschaftliche Dynamik des Goldenen Drittels: Thesen und Werte

Initiative 28:28 · 14. November 2026 · Modellstand v4.83 · Rechnung: `modell/wirtschaftsdynamik.py` (+ `.toml`) → `daten/aggregate/wirtschaftsdynamik.json`
Status: **Prüfrechnung, Vorschlag zur Entscheidung.** Nicht in der geltenden Rechnung; der Grundpfad bleibt statisch.

## 0 Frage und Vorgehen

**Frage der Initiative:** Welche wirtschaftliche Dynamik entsteht aus dem höheren verfügbaren Einkommen, aus Deregulierung, Markterleichterung,
Entbürokratisierung und der größeren Zuversicht breiter Schichten?

**Vorgehen:**
- Sechs Kanäle, je ein Wert in drei Fällen (vorsichtig, mittel, hoch), mit Belegstufe und Aufbauzeit.
- Gemessen wird das Niveau des BIP gegen den Grundpfad in %. Die Wirkung auf die Dividende ist wie in `dynamik33.py` gerechnet: Steuern als
  Anteil am BIP, dazu die Progression.
- Die Fälle werden kanalweise addiert. Alle Unsicherheiten zeigen dabei in dieselbe Richtung, deshalb ist die Spanne eher zu weit.

**Belegstufen:** wie in der Voruntersuchung zu den Verhaltenswirkungen (24.10.2026).

| Stufe | Bedeutung |
|---|---|
| A | mehrere kausale Studien |
| B | eine kausale Studie oder mehrere aus anderem Umfeld |
| C | Theorie, Plausibilität oder eine einzelne, nicht kausale Schätzung |

**Was das Konzept regelt und was nicht:** Es regelt das Steuer- und Sozialsystem und die Regeln der Gemeinschaft der Staaten. Eine allgemeine
Deregulierung von Produkt- oder Arbeitsmärkten enthält es nicht; dafür wird hier keine Wirkung angesetzt.

## 1 Thesen

### T1 Mehr Kaufkraft gibt einen kurzen Schub, keinen dauerhaften Wohlstand (Belegstufe B)

- Die Haushalte haben 2028 zusammen rund 218 Mrd. € mehr. Das entspricht etwa 5,1 % des BIP. Grundlage ist die Mikrosimulation: im Mittel
  442 € je Haushalt und Monat, 80 % Weitergabe, Kaufkraft 2026.
- Das liegt in der Größenordnung dessen, was der Fonds 2028 neu aufnimmt (6,9 % des BIP). Der Schub ist also zu einem großen Teil über die
  Streckung der Altlasten finanziert.
- **Wert:** BIP +0,8 / +1,8 / +3,0 % in den Jahren 2028 bis 2030, danach bis 2033 auslaufend.
  - Multiplikator 0,15 / 0,35 / 0,6. Die Studien finden für Steuer- und Transferimpulse im Mittel etwa 0,6 bis 0,7 (Gechert 2015). Die
    Abschläge stehen für Vollauslastung, die Reaktion der Europäischen Zentralbank und Importe (Annahme).
- **Grenze:** Nachfrage schafft dauerhaft nur dann mehr, wenn Arbeit und Kapazität mitwachsen (T2 bis T4). Sonst wird ein Teil zu
  Preissteigerung. Das kommt zum einmaligen Preisschub der Mehrwertsteuer (+1,2 bis +2,1 %) hinzu. In der Tilgungsphase des Fonds (nach 2055)
  wirkt der Kanal umgekehrt; das ist nicht gerechnet.

### T2 Arbeit lohnt sich mehr und wird billiger (Belegstufe B)

**Wert:** BIP +0,4 / +1,7 / +2,8 % dauerhaft, aufgebaut bis 2035.

- **Arbeitsvolumen:** +0,9 / +2,8 / +4,6 % (`dynamik33`, v3.49). Der vorsichtige Fall rechnet nur mit der billigeren Arbeit, also der Nachfrage
  der Betriebe.
- **Abzug für die Dividende:** −0,3 % Arbeitsvolumen wegen des Einkommenseffekts. Der Wert liegt zwischen den Befunden aus Alaska (keine
  Wirkung) und der OpenResearch-Studie (−1 bis −2 Stunden je Woche bei Geringverdienern).
- **Was für den hohen Fall spricht:** der Wegfall des Splittings. Für Zweitverdienerinnen in Deutschland errechnet ein Modell +270 Stunden im
  Jahr (Bick/Fuchs-Schündeln 2018, Modellrechnung).

### T3 Ein einfaches System baut Bürokratie ab (Belegstufe C)

**Wert:** BIP +0,3 / +0,7 / +1,0 % dauerhaft, aufgebaut bis 2035.

- **Bezugsgröße:** Nach einer ifo-Studie kostet Bürokratie „bis zu“ 146 Mrd. € Wirtschaftsleistung im Jahr, rund 3,4 % des BIP 2024
  (Simulation: Deutschland auf dem Niveau Schwedens).
- **Anteil, den das Goldene Drittel abbaut:** 10 / 20 / 30 % (Annahme). Gemeint sind Steuer, Sozialbeiträge, Lohnabrechnung und Leistungen aus
  einer Hand.
- **Kritisch:**
  - Es ist eine einzelne Studie, Auftraggeber war eine Interessenvertretung (IHK München und Oberbayern), und „bis zu“ bezeichnet eine Obergrenze.
  - Die direkten Kosten nach dem Normenkontrollrat sind mit 65 Mrd. € weniger als halb so hoch.
  - Mögliche Doppelzählung mit Einsparungen der Verwaltung, die im Netzbudget schon stecken.

### T4 Ein Markt ohne Grenzen wirkt langsam, aber groß (Belegstufe C)

**Wert:** BIP 0 / +0,7 / +1,75 % dauerhaft, aufgebaut bis 2045.

- **Bezugsgröße:** Nach dem IWF wirken die Hemmnisse im EU-Binnenmarkt wie ein Zoll von 44 % auf Waren und 110 % auf Dienstleistungen. 10 %
  weniger Hemmnisse ergäben +7 % BIP (Kammer, F&D Juni 2025; Zeitraum und Methode dort nicht genannt, Sekundärquelle).
- **Was die Gemeinschaft abbaut:** 0 / 1 / 2,5 % der Hemmnisse, über gleiche Steuerregeln, ein Label, Register und Gericht (Annahme, lineare
  Übertragung).
- **Kritisch:** Für die EU-Staaten ist der Binnenmarkt zum großen Teil schon da. Der Zugewinn liegt vor allem bei den Dienstleistungen und bei den
  Partnern außerhalb der EU.

### T5 Gegenrichtung: Kapital und Gewinne tragen mehr (Belegstufe C)

**Wert:** BIP −1,0 / −0,5 / 0 % dauerhaft, aufgebaut bis 2040.

- **Rangfolge der Wachstumsschädlichkeit (OECD, Heady u. a. 2009):** Unternehmensteuern vor Einkommensteuern, dann Verbrauchsteuern, zuletzt
  Grundsteuern.
- **Was das Drittel verschiebt:**
  - von der Arbeit zum Konsum und zum Boden; das ist günstig;
  - zu Kapitalerträgen (33 % statt 26,4 %) und Gewinnen (33 % statt rund 30 %); das ist ungünstig.
- Die Rangfolge ist gut belegt, die Größe der Wirkung ist eine Annahme.
- **Gegenläufig:** Die Pflichtvorsorge erhöht die Ersparnis. In einem offenen Kapitalmarkt bestimmt aber vor allem der Kapitalkostensatz die
  Investitionen im Inland.

### T6 Zuversicht ist Folge, nicht eigene Ursache (Befund Belegstufe B, Wirkung C)

**Wert:** 0 / 0 / +0,3 %.

- **Befund:** Vertrauensschübe spiegeln vor allem Nachrichten über die künftige Produktivität (Barsky/Sims 2012). Zuversicht entsteht also, wenn
  T2 bis T4 eintreten, und darf nicht zusätzlich gezählt werden.
- **Höchstens:** weniger Vorsichtssparen bei unteren Einkommen durch Boden und Dividende (Annahme).

## 2 Werte zusammen

Niveau des BIP gegen den Grundpfad; Dividende je Erwachsenem und Monat, Kaufkraft 2026.

| Fall | 2028 | 2030 | 2035 | 2045 und später | Dividende 2035 / 2045 |
|---|---|---|---|---|---|
| vorsichtig | +0,8 % | +0,8 % | +0,1 % | −0,3 % | +1 € / −1 € |
| **mittel** | **+1,8 %** | **+2,4 %** | **+2,3 %** | **+2,5 %** | **+12 € / +12 €** |
| hoch | +3,0 % | +4,5 % | +4,9 % | +5,9 % | +26 € / +29 € |

**Lesart:**
- **Für die Menschen** wirkt die Dynamik vor allem über mehr Beschäftigung und höhere Löhne.
- **Für die Dividende** ist die Wirkung klein: rund 5 € je Erwachsenem und Monat je Prozent BIP. Ein Grund ist, dass die Aufgaben als Anteil am
  BIP mitwachsen.
- **Für den Fonds:** Ein um 2,5 % höheres BIP senkt seinen Beitrag von 5,15 auf rund 5,0 % des BIP (Näherung wie `dynamik33`).

## 3 Vorschlag zur Entscheidung

1. Die geltende Rechnung bleibt statisch (vorsichtig). Dynamik wird nicht eingerechnet, um die Dividende zu erhöhen.
2. In Konzept und Working Paper steht der **mittlere Fall** als „erwartete Dynamik“, mit der Spanne und den Belegstufen.
3. Auf der Webseite höchstens ein Satz ohne Zahl, etwa: „Mehr Arbeit, weniger Bürokratie und ein Markt ohne Grenzen stärken die Wirtschaft.“
4. **Nächste Schritte:**
   - V2 aus der Voruntersuchung (Arbeitsangebot auf der Mikrosimulation);
   - eine zweite Quelle zur Bürokratie (Normenkontrollrat, Weltbank);
   - Beleg zum IWF-Wert an der Originalstudie;
   - eine Sektorrechnung Haushalte, Staat, Fonds und Unternehmen, die den Nachfrageschub mit der Fondsfinanzierung in einem Zusammenhang
     zeigt.

## 4 Quellen

- Barsky, R., Sims, E. (2012): Information, Animal Spirits, and the Meaning of Innovations in Consumer Confidence. AER 102(4). [NBER w15049](https://www.nber.org/papers/w15049) (Zusammenfassung)
- Bick, A., Fuchs-Schündeln, N. (2018): Review of Economic Studies 85(3) (aus der Voruntersuchung, maschinell gelesen, an der Quelle zu prüfen)
- Gechert, S. (2015): What fiscal policy is most effective? A meta-regression analysis. Oxford Economic Papers 67(3). [RePEc](https://econpapers.repec.org/RePEc:oup:oxecpp:v:67:y:2015:i:3:p:553-580.) (Zusammenfassung)
- Gechert, S., Rannenberg, A. (2018): Which Fiscal Multipliers Are Regime-Dependent? Journal of Economic Surveys 32(4). [RePEc](https://econpapers.repec.org/RePEc:bla:jecsur:v:32:y:2018:i:4:p:1160-1182) (Zusammenfassung)
- Heady, C., Johansson, Å., Arnold, J., Brys, B., Vartia, L. (2009): Tax Policy for Economic Recovery and Growth. Kent DP 0925. [PDF](https://www.kent.ac.uk/economics/repec/0925.pdf) (Abschnitt 2)
- ifo Institut (2024): Bürokratie in Deutschland kostet jährlich 146 Milliarden Euro an Wirtschaftsleistung. Pressemitteilung vom 14.11.2024 (Studie für die IHK München und Oberbayern). [ifo](https://www.ifo.de/pressemitteilung/2024-11-14/buerokratie-deutschland-kostet-jaehrlich-146-milliarden-euro)
- Kammer, A. (2025): Europe's Integration Imperative. Finance & Development, Juni 2025 (IWF). [IMF](https://www.imf.org/en/publications/fandd/issues/2025/06/europes-integration-imperative-alfred-kammer) (Sekundärquelle für die IWF-Forschung 2024)
- Eigene Dateien: `mikro_de.json`, `dynamik33.json`, `gesamtlast33.json`, `ausweichen33.json`, Voruntersuchung Verhaltenswirkungen (24.10.2026)

Hinweis zu Personennamen: Genannt sind nur Autorinnen und Autoren veröffentlichter Studien als bibliografische Angabe.
