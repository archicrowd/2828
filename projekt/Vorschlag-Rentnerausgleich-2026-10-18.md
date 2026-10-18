# Rentnerausgleich, Altansprüche und Lebensarbeitszeit (Vorschlag, Logbuch v4.10)

Initiative 28:28 · 18. Oktober 2026 · Prüfrechnung `modell/rentnerausgleich.py` → `daten/aggregate/rentnerausgleich.json` (Deutschland, 2028,
Kaufkraft 2026)

**Frage der Initiative:** Welche Lösungen gibt es für den Rentnerausgleich? Vorschlag der Initiative: Lebensarbeitszeit mit einer Formel neu
definieren. Sind die Altansprüche ausreichend bedacht?

---

## 1 | Warum Rentner verlieren

Bestandsrenten werden weitergezahlt, gekürzt um die entfallenden Kranken- und Pflegebeiträge (12,35 %, Beschluss v3.48). Die Dividende ist
in der Rente enthalten: Der Altlastenfonds zahlt nur den Anspruch über der Dividende. Rentner bekommen also **keine Dividende zusätzlich**.
Netto verlieren sie aus drei Gründen:
- Die ganze Rente ist steuerpflichtig (heute zu 83 %).
- Die Mehrwertsteuer ist höher.
- Sie zahlen den Altlastenzuschlag von 13,7 % mit, also auf die Finanzierung ihrer eigenen Renten.

| Bruttorente heute | 900 € | 1.200 € | 1.600 € | 2.200 € |
|---|---|---|---|---|
| Netto heute | 789 € | 1.052 € | 1.389 € | 1.828 € |
| Differenz neu (Beschluss) | −35 € | −49 € | −92 € | −123 € |

**Korrektur 65:** In v4.8 und v4.9 stand, der Kinderanteil 0,8 (R1) vergrößere das Minus der Rentner auf −54 bis −142 €. Das war falsch. Weil die
Dividende Teil der Bestandsrente ist, ändert eine kleinere Erwachsenendividende das Rentnernetto nicht. Sie verschiebt nur Kosten in den
Altlastenfonds (der Anspruch über der Dividende wird größer). Es gelten wieder −35 bis −123 €.

## 2 | Ausgleichsvarianten (Differenz zu heute je Monat; Mehrkosten 2028)

| Variante | 900 € | 1.200 € | 1.600 € | 2.200 € | Mehrkosten |
|---|---|---|---|---|---|
| Beschluss | −35 | −49 | −92 | −123 | – |
| Kürzung 10 % statt 12,35 % | −15 | −26 | −61 | −84 | 6,2 Mrd. € (0,13 % BIP) |
| **Kürzung 7,5 %** | **+7** | **0** | **−27** | **−43** | **12,7 Mrd. € (0,26 %)** |
| Besteuerungsanteil 83 % wie heute | −35 | −46 | −64 | −55 | 5,4 Mrd. € (0,11 %) |
| Befreiung vom Altlastenzuschlag (als Erstattung) | −19 | −27 | −59 | −70 | 6,7 Mrd. € (0,14 %) |
| Pauschale 50 € steuerfrei | +13 | −1 | −44 | −75 | 10,4 Mrd. € (0,21 %) |
| Kürzung 7,5 % + Besteuerungsanteil 83 % | +7 | +9 | +3 | +29 | 18,8 Mrd. € (0,38 %) |

Die Mehrkosten sind grob gerechnet: Mittel der vier Beispielrenten mal 18 Mio. Rentner, ohne Rentenverteilung. Sie sinken mit dem Bestand.
Ab 2030 tritt nur noch ein Teil der Ansprüche aus der Zeit vor dem Stichtag in den Bestand ein.

**Empfehlung A:** Kürzung 7,5 % statt 12,35 %, über den Altlastenfonds (wie die Altansprüche selbst).
- Kleine und mittlere Renten (bis 1.200 €) stehen dann wie heute da.
- Höhere Renten tragen ein maßvolles Minus von 27 bis 43 €.
- Das passt zur Logik des Konzepts: Ausgeglichen wird, wo der Bedarf ist, und der Ausgleich steckt nicht in einer neuen Leistung, sondern in
  einem Parameter.

## 3 | Sind die Altansprüche ausreichend bedacht? Nicht vollständig.

| Punkt | Befund | Vorschlag |
|---|---|---|
| **Kleine Bestandsrenten** | Die Mindestrente gilt nur für Ansprüche nach dem Stichtag. Ein Boden für Bestandsrentner ist nicht geregelt. 900 € brutto ergeben neu 754 € netto; heute stünden mit Grundsicherung im Alter rund 1.083 € zu (764.065 Empfänger ab Altersgrenze, Dezember 2025). | **B1:** Boden auch für Bestandsrentner: Grundbedarf, Bestandsrente **voll** angerechnet (Freibetrag wie heute). Die Halbanrechnung gilt nur für die neue Vorsorge, sonst würde fast jede Rente bis 1.700 € aufgestockt. Kosten etwa wie die heutige Grundsicherung im Alter, rund 7 Mrd. € (0,14 % BIP), aus dem Härtefall- bzw. Netzbudget. |
| **Übergangsjahrgänge** | Anwartschaften gelten im Aggregat anteilig nach den Erwerbsjahren vor 2028. Eine Einzelregel fehlt. Heute wird der Teilanspruch voll mit der Dividende verrechnet: Wer 2045 mit 83 % Altanteil in Rente geht, bekommt seinen Altanspruch oder die Dividende, nicht beides. | **T1:** Verrechnung nur im Verhältnis der Altjahre: Dividende + Altanteil × (Anspruch − Dividende) + eigene Vorsorge. Macht den Übergang gleitend; Mehrkosten im Fonds in den 2040er Jahren in der Größenordnung von 0,3 % BIP (Überschlag, nicht gerechnet). |
| **Rentenalter uneinheitlich** | Das Kohortenschema der Altansprüche rechnet mit 65 Jahren, die Mindestrente mit 67. | Ein Rentenbeginn für beide, nach der Formel in Abschnitt 4. |
| **Hinterbliebene** | Bestehende Hinterbliebenenrenten laufen als Altanspruch weiter; im neuen System gibt es eigene Dividende und eigenes Konto (vererbbar). | Für Paare in der Übergangszeit klären, ob die Witwenrente aus Altanteilen anteilig fortbesteht. |
| **Beamtenpensionen** | Erworbene Ansprüche: nach Tabelle 29 (Eurostat nasa_10_pens1) in den staatlichen Systemen enthalten, an der Quelle zu prüfen. Nach dem Stichtag entstehen keine neuen (Setzung G3/G4). | Bestätigen; dieselbe Kürzungs- und Ausgleichsregel wie für Renten. |
| **Eigentumsschutz** | Kürzung und späterer Rentenbeginn greifen in Anwartschaften ein (DE: Art. 14 GG). Zulässig nur mit Übergang und Verhältnismäßigkeit (Vorbild: Rente mit 67, lange Vorlaufzeit). | Juristische Prüfung (offen seit v3.47). |

## 4 | Lebensarbeitszeit mit Formel

Vorbilder:
- **Dänemark:** Das Rentenalter folgt der Lebenserwartung, mit dem Ziel von rund 14,5 Jahren Rentenbezug. Erhöhungen werden alle 5 Jahre
  beschlossen, 15 Jahre im Voraus. Die Stufen: 67 seit 2022, 68 ab 2030, 69 ab 2035; 70 ab 2040, beschlossen im Mai 2025.
- **Niederlande:** Seit 2025 gelten zwei Drittel des Gewinns an Lebenserwartung als längere Arbeitszeit, ein Drittel als längerer
  Rentenbezug (Gesetz in Kraft seit 10.12.2020).

Vorschlag **L1**, eine Formel mit Schutz für frühe Berufsstarter:

> Rentenbeginn (Altansprüche und Mindestrente) = früherer der beiden Zeitpunkte:
> (a) Regelalter A(t) = 67 + ⅔ × (Lebenserwartung mit 65 im Jahr t − Lebenserwartung mit 65 im Jahr 2026), in Monaten gerundet,
> 15 Jahre im Voraus festgestellt;
> (b) Erreichen von L(t) Lebensarbeitsjahren (Erwerb, Kindererziehung, Pflege), L(2028) = 45, gleich gekoppelt; frühestens mit 63.
> Die eigene Vorsorge ist ab 63 frei verfügbar (eigenes Konto).

Entlastung von Altlastenfonds und Mindestrente durch den späteren Rentenbeginn. Annahmen: Kopplung ab 2030, Lebenserwartung mit 65 heute
19,6 Jahre (Destatis 2023/2025), Zuwachs 0,07 Jahre je Jahr. Ohne zusätzliche Steuern aus längerer Arbeit, also vorsichtig gerechnet:

| Jahr | 2035 | 2040 | 2045 | 2050 | 2060 | 2070 |
|---|---|---|---|---|---|---|
| ⅔-Kopplung: Rentenbeginn + Jahre | 0,23 | 0,47 | 0,70 | 0,93 | 1,40 | 1,87 |
| Entlastung % BIP | 0,09 | 0,18 | 0,24 | 0,27 | 0,25 | 0,10 |
| entspricht Dividende je Erwachsenem | +5 € | +10 € | +14 € | +17 € | +17 € | +7 € |
| 1:1-Kopplung (DK): Entlastung % BIP | 0,14 | 0,27 | 0,36 | 0,41 | 0,38 | 0,15 |

**Finanzierung des Ausgleichs (Summe 2028–2098, % BIP × Jahre, Diskont Zins 2,5 % gegen Wachstum 3 %):**

| Entlastung | Summe | Kosten | Summe |
|---|---|---|---|
| ⅔-Kopplung | 8,6 | Kürzung 7,5 % (A) | 7,9 |
| 1:1-Kopplung | 12,9 | Boden für kleine Bestandsrenten (B1) | 4,4 |
| | | A + B1 | 12,3 |
| | | Pauschale 50 € | 6,4 |

**Lesart:** Der Ausgleich wird sofort fällig, die Entlastung durch die Lebensarbeitszeit kommt erst nach 2035. Der Altlastenfonds kann die
Lücke überbrücken, weil er ohnehin über Jahrzehnte streckt. Die ⅔-Kopplung trägt den Ausgleich A allein. Die 1:1-Kopplung trägt A und B1
zusammen. Die Kostenpfade sind vereinfacht: Sie sinken mit dem Anteil der Altansprüche, ohne Alterungszuwachs. Sie sind daher eher zu
niedrig.

## 5 | Zur Entscheidung

1. **A:** Kürzung 7,5 % statt 12,35 % (oder Pauschale 50 € oder Besteuerungsanteil 83 %)?
2. **B1:** Boden für kleine Bestandsrenten mit voller Anrechnung?
3. **T1:** anteilige Verrechnung für Übergangsjahrgänge?
4. **L1:** Rentenbeginn nach Formel, ⅔-Kopplung mit Lebensarbeitsjahren als Alternative (oder 1:1 wie Dänemark)?

## Quellen

- Destatis (Juli 2026): Sterbetafel 2023/2025, fernere Lebenserwartung mit 65: Männer 18,0, Frauen 21,1 Jahre: https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/sterbetafel.html
- Destatis/BMAS über Münster Aktuell (21.08.2026), Grundsicherung im Alter und bei Erwerbsminderung 2025 (Sekundärquelle): https://ms-aktuell.de/welt/sozialhilfeausgaben-2025-21-08-2026/
- Lex.dk, Folkepension og pensionsalder (70 ab 2040, beschlossen Mai 2025): https://lex.dk/folkepension_og_pensionsalder
- CEPOS, Notat Folkepensionsalder og levetidsindeksering (Sekundärquelle, um 2020): https://cepos.dk/wp-content/uploads/2024/08/notat_folkepensionsalder-og-levetidsindeksering.pdf
- Taxlive, Wet verandering koppeling AOW-leeftijd (Sekundärquelle): https://www.taxlive.nl/nl/documenten/vn-vandaag/wet-verandering-koppeling-aow-leeftijd-in-werking-getreden/
- Eigene Rechnungen: haushalte33 (Rentner), sozialschutz (Kohortenschema), netz33 (Mindestrente), z_pfad.csv (Altlastenfonds).
