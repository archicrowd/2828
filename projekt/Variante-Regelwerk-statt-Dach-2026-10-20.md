# Architekturvariante „Regelwerk statt Dach“ (zur Entscheidung, Logbuch v4.13)

Initiative 28:28 · 20. Oktober 2026 · Grundlage: Gegenentwurf der externen Prüfung vom 19.10.2026, auf das Konzept „Das Goldene Drittel“
übertragen. Ausgearbeitet als Text; eine neue Rechnung ist nicht nötig, weil die Formeln gleich bleiben.

---

## 1 | Was gleich bleibt

Die Variante ändert keine Regel, nur die Stellen, die sie anwenden. Gleich bleiben:
- Tarif 0/11/19/25/33 % am Grundbedarf und Mehrwertsteuer-Label;
- Transformationsdividende ohne Antrag, Kinder 80 %;
- Grundauskommen mit Halbanrechnung, Härtefall bei der Gemeinde;
- Gemeindeformel je Einwohner und je Kind;
- Altlasten als Sache der Staaten, gemeinsamer Fonds mit Verrechnung je Staat und Auslaufen in 30 Jahren, Neustartverfahren;
- Rentnerregeln (Kürzung 7,5 %, anteilige Verrechnung, Grundauskommen im Bestand, gekoppelter Rentenbeginn);
- Weitergabe der Arbeitgeberbeiträge per Gesetz bis zum Stichtag.

## 2 | Was sich ändert

| Funktion | Konzept heute („Dach“) | Variante „Regelwerk“ |
|---|---|---|
| Regeln setzen (Formeln, Tarif, Ankerwert) | Dach, Mehrheitsentscheid | **Regelbuch als Staatsvertrag.** Kernformeln nur einstimmig mit Ratifikation; Parameter in festen Korridoren mit ⅘-Mehrheit oder durch ein unabhängiges Organ mit engem Mandat |
| Steuern einziehen | Dach zieht ein und behält höchstens 32 % | **Jeder Staat zieht nach dem Regelbuch ein** (Quellenabzug, Drittmeldung) |
| Gemeinsame Aufgaben (Verteidigung, Binnenmarkt, digitale Souveränität) | aus dem Dachhaushalt | **Beitrag je Staat nach Formel** (% des BIP) an eine gemeinsame Stelle mit Zweckbindung; kein frei verhandelbarer Haushalt |
| Auszahlen (Dividende, Gemeindeformel, Fondsbeiträge) | Dach | **Ausgleichsstelle** mit eigener Rechtspersönlichkeit: Staaten zahlen ihre Anteile ein, die Stelle zahlt formelgebunden aus. Sie hat kein Ermessen |
| Prüfen und Streit | – | **Prüfhof** (jährlicher öffentlicher Bericht je Staat) und **Schiedsgericht**; Feststellung und Sanktion nie durch ein politisches Organ |
| Durchsetzen | Verfügungsgewalt des Dachs | **Fünf Schichten:** Quellenabzug; automatische Verrechnung mit Zahlungen der Ausgleichsstelle; Dividende und Grundauskommen als einklagbare Ansprüche vor nationalen Gerichten; Aussetzen von Vorteilen (Registerzugang, gegenseitige Anerkennung) ohne Abstimmung; Vollstreckbarkeit von Schiedssprüchen |
| Austritt | nicht vorgesehen | möglich, mit Abwicklungsregel für den Fonds |

## 3 | Bewertung

**Für die Variante:**
- Die Variante ist mit nationalem Verfassungsrecht und den EU-Verträgen deutlich leichter vereinbar: keine eigene Steuerhoheit einer neuen
  Ebene, kein eigener Haushalt.
- Die Legitimation bleibt bei den Staaten.
- Bei Bürgern und Ländern weckt sie weniger Widerstand.
- Die Bürgerinnen und Bürger erhalten mit dem einklagbaren Anspruch selbst ein Werkzeug gegen säumige Staaten.

**Gegen die Variante:**
- Der Vollzug ist schwächer gegen einen großen Nettozahler, der sich verweigert: Die Verrechnung trifft nur Empfänger. Dann bleiben nur
  Marktzugang, Vollstreckung und Reputation.
- Die Gleichheit der Regeln hängt an der Qualität der nationalen Verwaltung; Registerunion und Prüfhof sind deshalb Beitrittsbedingung.
- Gemeinsame Aufgaben (Verteidigung) werden über Beiträge finanziert, nicht über eine eigene Einnahme. Das macht sie anfälliger für
  Verhandlungen.

**Für die Rechnung:** keine Änderung. Dividende, Netz, Gemeindeformel und Fonds entstehen nach denselben Formeln; der Weg des Geldes ändert
sich. Die Obergrenze des Dachs (32 %) wird zur Obergrenze des gemeinsamen Beitrags.

## 4 | Was sich an Seite und Konzept ändern würde

- **Ebenen-Grafik:** „Das gemeinsame Dach“ wird zu „Gemeinsames Regelwerk und Ausgleichsstelle“; der Pfeil „Steuerbeitrag“ geht an den Staat.
- **„Fünf Regeln“ des Dachs:**
  - Obergrenze → gemeinsamer Beitrag;
  - „Formel statt Verhandlung“ bleibt;
  - „Entscheiden mit Mehrheit“ wird zu „Kern einstimmig, Parameter mit Mehrheit im Korridor, Vollzug durch Gericht“.
- **Konzept:** Abschnitt 3.6 neu fassen und Abschnitt „Vollzug“ ergänzen.

## 5 | Zur Entscheidung

1. Bei der Dach-Architektur bleiben, die Variante übernehmen oder sie als zweite Option auf der Seite nennen?
2. Wenn die Variante übernommen wird: Die Vollzugsschichten (insbesondere den einklagbaren Anspruch) auch dann aufnehmen, wenn das Dach bleibt?

## 6 | Gemeinsame Aufgaben ohne eigene Steuer: eine Pflichtquote, zwei Wege (v4.15)

Auftrag vom 20.10.2026: Aufteilung rechnen; der Verteidigungspfad bleibt 1,4 → 2,5 % BIP bis 2035. Rechnung: `modell/dach_beitrag.py`
→ `daten/aggregate/dach_beitrag.json`.

**Regel:**
1. **Pflichtquote.** Jeder Staat wendet denselben Anteil seines BIP für die abschließende Liste gemeinsamer Aufgaben auf:
   2028 6,19 %, ab 2035 7,29 %. Nur die Verteidigung wächst. Höchstens 32 % des Steueraufkommens (bisherige Dach-Regel); das sind
   2028 10,7 % BIP, die Quote liegt deutlich darunter.
2. **Zwei Wege.** Ein Teil geht in die gemeinsame Kasse, der Rest ist eigene Ausgabe des Staates nach gemeinsamem Mindeststandard.
   Der Prüfhof stellt jährlich fest, was anrechenbar ist.
3. **Rückfallregel.** Wer weniger anrechenbar ausgibt als die Quote, zahlt die Differenz in die Kasse. Die Ausgleichsstelle verrechnet
   sie mit ihren Zahlungen an den Staat. Mehrausgaben sind freiwillig und werden nicht gutgeschrieben.

**Ergebnis** (% BIP, Klub der zehn; Kassenanteile sind **Annahmen** zur Größenordnung, `dach_beitrag.toml`):

| Aufgabe | Ziel 2035 | Anteil Kasse | Kasse | eigene Ausgabe |
|---|---|---|---|---|
| Wirtschaftsraum, Agrar, Energie, Netze | 2,10 | 25 % | 0,53 | 1,58 |
| Verteidigung und digitale Souveränität | 2,50 | 40 % | 1,00 | 1,50 |
| Grundlagenforschung | 0,77 | 50 % | 0,39 | 0,39 |
| Hochschulen | 0,74 | 0 % | – | 0,74 |
| Außenbeziehungen, Standards, übergeordnete Polizei, Umwelt grenzüberschreitend | 1,18 | 100 % | 1,18 | – |
| **Summe** | **7,29** | **42 %** | **3,09** | **4,20** |

2028 (Verteidigung 1,4 %) sind es 2,65 % Kasse und 3,54 % eigene Ausgabe. Für Deutschland entspricht die Kasse 2028 rund 130 Mrd € (nominal 2028), 130 € je Einwohner und Monat.

**Einordnung:**
- **Größe der Kasse.** 2,65 bis 3,09 % BIP sind das 1,9- bis 2,2-Fache der heutigen EU-Eigenmittelobergrenze für Zahlungen (1,40 % BNE,
  Europäische Kommission). Das ist nicht in einem Schritt erreichbar. Die Kasse kann schrittweise wachsen, ohne dass sich die Pflichtquote
  oder die Rechnung ändert.
- **Bemessung.** Die Rechnung nutzt das BIP. Für Irland ergäbe das 261 € je Einwohner und Monat (Deutschland 130 €), weil das irische BIP
  durch Gewinne internationaler Konzerne überhöht ist. Vorschlag: den Kassenbeitrag wie in der EU am BNE bemessen. Gerechnet ist das nicht.
- **Rückfallregel in der Verteidigung.** Ließe ein Staat seine Verteidigungsausgaben auf dem Stand 2024 (COFOG GF02, nicht
  NATO-Abgrenzung), zahlte er 2035 die Differenz in die Kasse:
  - Irland 2,4 % BIP;
  - Österreich 1,8 %;
  - Spanien 1,6 %;
  - Belgien 1,2 %;
  - Deutschland und Slowenien 1,1 %;
  - Niederlande 0,9 %;
  - Dänemark 0,7 %;
  - Frankreich 0,6 %;
  - Estland 0 (es liegt mit 3,7 % darüber).

  Für die neutralen Staaten (Irland, Österreich) braucht es eine Regel, was anrechenbar ist, etwa Zivilschutz und Cybersicherheit. **Offen.**
- **Wirkung auf die Rechnung:** keine. Dividende, Netz und Gemeindeformel bleiben, solange die Pflichtquote erfüllt ist.

**Kernsatz:** „Jedes Land gibt denselben Anteil seiner Wirtschaftskraft für die gemeinsamen Aufgaben. Einen Teil zahlt es in die gemeinsame
Kasse, den Rest gibt es nach gemeinsamen Regeln selbst aus. Wer weniger tut, zahlt die Differenz.“

## 7 | Sicherheit als echte Gemeinschaftsaufgabe (Vorschlag v4.16, zur Entscheidung)

Einwand der Initiative (20.10.2026): Ohne gemeinsame Verteidigung und Souveränität bliebe Europa im Wettbewerb der Großmächte strukturell
im Nachteil. Ein Beitragsmodell überzeugt dafür nicht voll.

Der Einwand trifft. Für die Sicherheit hat die Variante drei Schwächen:
- **Geld:** Beiträge werden verhandelt; das macht die Finanzierung unsicher (Abschnitt 3).
- **Zersplitterung:** Gemeinsame Beschaffung gibt es nur, wenn Staaten sie wollen.
- **Entscheidung:** In der Außen- und Sicherheitspolitik gilt Einstimmigkeit (Art. 31 EUV).

**Vorschlag: Regelwerk für Steuern, Sozialstaat und Gemeinden – Sicherheitsunion mit eigener Einnahme für das, was nur gemeinsam geht.**
1. **Eigene Einnahme nach Vertrag statt Beitrag.**
   - Ein fester Anteil der Mehrwertsteuer fließt per Quellenabzug in die Sicherheitskasse.
   - Der Anteil wird einmal im Vertrag festgelegt, ratifiziert und gedeckelt. Es gibt keine jährliche Verhandlung, und die Steuerhoheit
     bleibt bei den Staaten.
   - Das Muster ist der Eigenmittelbeschluss der EU. Er ist auch mit den Anforderungen des Bundesverfassungsgerichts vereinbar:
     begrenzt, vom Parlament gebilligt, kein Automatismus über die Grenze hinaus.

   | gemeinsamer Teil der Verteidigung (2035) | % BIP | Anteil der Mehrwertsteuer |
   |---|---|---|
   | 40 % (Rechnung v4.15) | 1,00 | 12,1 % |
   | 50 % | 1,25 | 15,1 % |
   | 60 % | 1,50 | 18,1 % |
   | 100 % (alles gemeinsam) | 2,50 | 30,2 % |

   Rechnung `modell/dach_beitrag.py`, Mehrwertsteuer nach projektion33 (8,28 % BIP 2035). Die Gesamtlast ändert sich nicht: Der Anteil
   ersetzt den Kassenbeitrag.
2. **Gemeinsame Fähigkeiten im gemeinsamen Eigentum:**
   - Luft- und Raketenabwehr;
   - Satelliten und Raumfahrt;
   - Cyberabwehr;
   - strategischer Lufttransport;
   - Munitions- und Materialreserven;
   - eine gemeinsame Beschaffungsagentur mit Vorrang europäischer Fertigung.

   Anknüpfungspunkt ist SAFE (bis 150 Mrd. € Darlehen für gemeinsame Beschaffung, in Kraft seit 29.05.2025, Rat der EU).
3. **Entscheiden:**
   - Für Betrieb und Beschaffung der gemeinsamen Fähigkeiten gilt die qualifizierte Mehrheit.
   - Über den Einsatz nationaler Streitkräfte entscheiden weiter die nationalen Parlamente (in Deutschland Parlamentsvorbehalt).
   - Ob die gemeinsamen Fähigkeiten ein eigenes Einsatzmandat brauchen, ist eine offene Rechtsfrage (Art. 24 Abs. 2 GG, Art. 42 EUV).
4. **Teilnahme:**
   - Die Sicherheitsunion ist offen für alle Staaten des Regelwerks, aber nicht Pflicht.
   - Neutrale Staaten tragen über Zivilschutz und Cyberabwehr bei und zahlen denselben Anteil der Mehrwertsteuer.

**Kernsatz:** „Steuern, Sozialstaat und Gemeinden nach gemeinsamen Regeln in jedem Staat. Sicherheit gemeinsam: mit eigener Einnahme,
gemeinsamen Fähigkeiten und gemeinsamer Beschaffung.“

**Offen:**
- Anteil (Vorschlag: 50 %, rund 15 % der Mehrwertsteuer);
- Rechtsprüfung (Art. 23, 24, 79 Abs. 3 GG; Art. 42 EUV);
- nukleare Abschreckung, im Modell nicht behandelt.

## 8 | Geld innerhalb der Staaten und Stärkung der Regionen (Rechnung v4.16)

Rechnung `modell/regionen_de.py` mit Daten für alle 400 Kreise (Eurostat 2024). Die Daten wurden maschinell aus den Abfragen gelesen und sind an der Quelle zu prüfen; die Summen je Bundesland stimmen überein.

**Befund 1: Die Gemeindeformel verteilt fast gleich je Kopf, unabhängig von der Wirtschaftskraft.**
- Je Einwohner gibt es im Mittel 5.853 € im Jahr (Kaufkraft 2026).
- Die Spanne zwischen den Kreisen (90. zu 10. Perzentil) beträgt 1,05. Beim BIP je Einwohner beträgt sie 2,43.
- Das wirtschaftsstärkste Fünftel der Kreise erhält 99,3 % des Durchschnitts, das schwächste 99,8 %.

Gegenüber heute ist das ein starker Ausgleich, weil die Gewerbesteuer heute der Wirtschaftskraft folgt. Beziffert ist das nicht: Die
heutigen Gemeindeeinnahmen je Kreis (Regionalstatistik 71231, INKAR) waren über das Abrufwerkzeug nicht erreichbar.

**Befund 2: Ohne Zuschlag bekommen dünn besiedelte und alternde Kreise etwas weniger je Kopf**, weil sie weniger Kinder haben:
- Kreise unter 100 Einwohnern je km²: 99,0 % des Durchschnitts;
- ostdeutsche Flächenländer: 99,0 %.

Ihre Kosten je Kopf sind aber höher (Wege, Netze, Pflege).

**Strukturzuschlag** (Anteil des Topfs je zur Hälfte nach Fläche und nach Menschen ab 65; aufkommensneutral):

| Index (Deutschland = 100) | ohne | 5 % | 10 % | 15 % |
|---|---|---|---|---|
| dünn besiedelt (unter 100 Einw./km²) | 99,0 | 105,0 | 111,0 | 117,0 |
| ostdeutsche Flächenländer | 99,0 | 102,2 | 105,3 | 108,4 |
| Landkreise | 100,4 | 101,6 | 102,7 | 103,8 |
| kreisfreie Städte | 99,1 | 96,7 | 94,3 | 92,0 |
| wirtschaftsstärkstes Fünftel | 99,3 | 97,2 | 95,1 | 93,0 |
| Spanne P90/P10 | 1,05 | 1,09 | 1,15 | 1,22 |

Mit 10 % liegen die Kreise mit dem meisten Geld je Kopf bei 7.257 bis 7.504 € (Prignitz, Altmarkkreis Salzwedel), die mit dem wenigsten
bei 5.197 bis 5.357 € (Universitätsstädte, München).

**Vorschlag:**
- Strukturzuschlag 10 %;
- eigener Hebesatz auf den Bodenwert;
- kleiner Gemeindeanteil an der Gewinnsteuer am Betriebsort mit Hebesatz im engen Korridor (Art. 28 Abs. 2 GG, Rechtsprüfung offen);
- die Aufteilung zwischen Bund und Ländern regelt jeder Staat selbst.

**Nächster Schritt:** heutige Gemeindeeinnahmen je Kreis als Datei, um Gewinner und Verlierer gegenüber heute zu zeigen. Am einfachsten lädt
die Initiative die Tabelle 71231-01-03-4 (Realsteuervergleich) als CSV von regionalstatistik.de herunter und hängt sie an.
