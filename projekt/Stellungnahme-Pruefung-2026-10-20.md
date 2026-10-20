# Stellungnahme zur externen Prüfung vom 19.10.2026

Initiative 28:28 · 20. Oktober 2026 · Logbuch v4.12

Eine dritte Instanz hat Webseite und Repository geprüft. Ihr Bericht umfasst eine volkswirtschaftliche, soziale und politische Analyse, ein
Audit des Repositorys und den Gegenentwurf „Regelwerk statt Dach“. Hier steht, was davon trifft, was auf einem Missverständnis beruht und was
daraus folgt.

## 1 | Wo die Prüfung irrt – und warum (unser Fehler)

| Aussage der Prüfung | Befund |
|---|---|
| Die Homepage-Fassung (33 %) sei im Repository nicht enthalten | **Falsch, aber von uns verursacht.** Stand C liegt seit v3.43 vollständig im Repository (systemvarianten, projektion33, netz33, altlasten, moeglichkeitsraum33, laenderseiten, regel_boden, gini …; Seite `seite/stand-c/`). README, INDEX, AGENTS und CLAUDE.md nannten aber die 28:28-Gesamtrechnung als „geltend“. Die Prüfung folgte diesem Wegweiser und prüfte den Vorläufer. **Korrektur 66**, Einstiegsdokumente berichtigt. |
| Offene Deckungslücke 0,24 BIP-Punkte; Klub-BIP +3,1 %; Verteidigungshebel; 30,6 % hält nur bei 3 % Nominalwachstum | Betrifft Stand B (28:28). Für Stand C nicht übertragbar; die Rechnungen sind dort andere (Steuerquote 33,5 % nach eigener Steuerbasis je Staat). Die Hinweise sind für Stand B richtig und stehen im Logbuch. |
| Der Altlastenfonds decke die Rentenversprechen „wohl nur teilweise“ | **Trifft nicht zu.** Der Fonds enthält ausdrücklich die Altrenten über der Dividende (Z, 2028 rund 8,8 % BIP im Klubschnitt, Eurostat-Tabelle 29), dazu den Schuldendienst. Der Beitrag beträgt nach v4.11 5,28 % BIP, der Zuschlag 15,8 %. Die Prüfung rechnete mit 13,7 % und nur mit der Schuld. |
| „Top-Verdiener gewinnen massiv“ | **Für Deutschland so nicht.** Beim 3-fachen Durchschnittslohn +6 %, beim 5-fachen −0,4 %, beim 8-fachen −2,1 % verfügbares Einkommen (v4.12; Durchschnittslohn nach OECD Taxing Wages 63.288 €, Pflichtvorsorge 10 %; mit 50.000 € als Basis: 150.000 € +10 %, 400.000 € −1,3 %, Prüfbericht B14). Gründe: Die Beiträge sind heute gedeckelt, die Pflichtvorsorge von 10 % gilt ungedeckelt, dazu kommt die höhere Mehrwertsteuer. **Für Frankreich trifft es zu** (+23 bis +39 % beim 2- bis 8-fachen Durchschnittslohn, Korrektur 64). |
| Polen: 33 % wären gegenüber der Flat Tax „massive Steuererhöhungen“ | **Zu kurz.** Heutige Belastung in Polen: Sozialbeiträge rund 13,7 % + Gesundheitsbeitrag 9 % + PIT. Im Modell gewinnen alle Lohnstufen (+3 bis +106 %). Vorbehalt: Die Sozialhilfe in Polen fehlt im heutigen Modell. |
| Splitting-Wegfall belastet Einverdiener-Ehen | Im Modell gewinnen Paare mit einem Einkommen, weil jeder Erwachsene eine eigene Dividende erhält (DE, 42.000 €: +667 €). |
| Dividende „Kinder halb“, 373 € | Die Prüfung las die veröffentlichte Seite (Fassung 4.0). Nach R1 gelten 354 € je Erwachsenem und 283 € je Kind (Fassung 4.8 und später, noch nicht hochgeladen). |

## 2 | Wo die Prüfung trifft

1. **Weitergabe der Arbeitgeberbeiträge** – der schwächste Baustein. Das neue Rechenergebnis (`modell/weitergabe_sensitivitaet.py`):
   - In Deutschland bleibt der Vorteil auch ohne jede Weitergabe positiv (+149 bis +433 € im Monat), weil die eigenen Beiträge entfallen.
     Bei 80 % Weitergabe sind es +362 bis +763 €.
   - In Frankreich (38 % mit mehr) und Spanien (53 %) trägt das Ergebnis ohne Weitergabe nicht.
   - **Folge:** Die Pflicht braucht eine Durchsetzungsregel. Denkbar sind ein gesetzlicher Umrechnungsschlüssel im Arbeitsvertrag zum
     Stichtag, ein Nachweis in der Lohnabrechnung und Tarifbindung als Normalfall.
2. **Niveau des starken Netzes** – auf der Seite nicht beziffert. Es ist gerechnet (Netz 9,6 % BIP 2028; Grundauskommen 1.029 € im Monat
   für Alleinstehende in DE; Gesundheitskatalog −5 %, Annahme), aber nicht sichtbar. Die Seite sollte es nennen.
3. **Ausweichreaktionen** bei Vermögens- und Erbschaftsteuer – im Modell nur pauschal (Annahme 50 % bei der Vermögensteuer).
4. **Preisniveauschub** durch die höhere Mehrwertsteuer und die Lohnrunde – nicht modelliert (statische Rechnung).
5. **Besteuerung am Kundenort** – handelsrechtlich (WTO, Doppelbesteuerungsabkommen) im Repository nicht geprüft.
6. **Label-Mehrwertsteuer** – Zuordnung und Lobbydruck. Die Konsumgewichte sind eine Annahme (Logbuch).
7. **Verfassungs- und Vertragsrecht, demokratische Legitimation des Dachs** – juristische Prüfung offen seit v3.47.
8. **Pflichtvorsorge 10 %** – das Risiko, Kosten der Vermögensverwaltung zu verschieben. Ein günstiger öffentlicher Standardfonds wäre zu
   prüfen.
9. **Kommunaler Wettbewerb um Einwohner und Kinder; strukturschwache Regionen** – nicht modelliert.

## 3 | Zum Gegenentwurf „Regelwerk statt Dach“

Der Gegenentwurf trennt die vier Funktionen des Dachs:
- Regelsetzung,
- Einzug,
- Altschulden,
- Verteilung.

An die Stelle des Dachs treten ein Regelbuch, ein Prüfhof und ein Schiedsgericht. Die Staaten setzen die Regeln um, eine Ausgleichsstelle
zahlt nach Formel aus. Einiges davon hat das Konzept bereits:
- Altlasten sind Sache der Staaten (v3.47).
- Der gemeinsame Fonds verrechnet je Staat und schmilzt in 30 Jahren ab; das entspricht dem opt-in-Zinsausgleich mit Auslaufklausel.
- Es gibt ein Neustartverfahren, das der vorgeschlagenen Staateninsolvenzordnung entspricht.
- Bezugsgröße ist der Grundbedarf als Ankerwert.

Der eigentliche Unterschied: **Einzug und Haushalt beim Dach** (Original) oder **bei den Staaten mit formelgebundener Ausgleichsstelle**
(Gegenentwurf). Rechnerisch ändert das an Dividende, Netz und Gemeindeformel wenig, wenn dieselben Formeln gelten. Politisch und rechtlich
(Art. 106/107 GG, EU-Eigenmittel) ist der Gegenentwurf deutlich leichter umsetzbar. Seine Vollzugsschichten sind ein brauchbarer Baustein für
beide Architekturen:
- Quellenabzug;
- automatische Verrechnung;
- Dividende als einklagbarer Anspruch;
- Marktzugang als Pfand;
- Vollstreckung.

**Empfehlung:** als Architekturvariante zur Entscheidung vorlegen. Die Rechnung bleibt dieselbe; die Seite müsste die Rolle des Dachs neu
beschreiben.

## 4 | Zur Entscheidung

1. Durchsetzungsregel für die Weitergabe festlegen. Alternativ die Seite um die Empfindlichkeit ergänzen (Ergebnis mit 0 / 50 / 80 %).
2. Niveau des starken Netzes auf der Seite beziffern.
3. Gegenentwurf „Regelwerk statt Dach“ als Variante ausarbeiten (Text, keine neue Rechnung)?
4. Rückmeldung an die prüfende Instanz mit Hinweis auf Stand C und Korrektur 66, Bitte um erneute Prüfung des geltenden Modells.
