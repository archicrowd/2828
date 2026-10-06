# -*- coding: utf-8 -*-
"""
A3 — Ersetzen die zehn Positionen die heutigen Regeln sauber?

DREI PRÜFUNGEN
  1. Welche heutige Steuer wird von welcher Position ersetzt — und welche
     bleibt stehen, ohne dass es jemand gesagt hat?
  2. Wo greifen zwei Positionen auf denselben Vorgang zu?
  3. Wer bekommt das Geld? Diese Frage haben wir nie gestellt, und sie ist
     die härteste von allen.
"""
def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# (heutige Steuer, Mrd 2025, ersetzt durch, Status)
ZUORDNUNG = [
 ('Lohnsteuer',                262.7, '01 Einkommen',        'ersetzt'),
 ('veranlagte Einkommensteuer', 78.4, '01 Einkommen',        'ersetzt'),
 ('Abgeltungsteuer',            24.8, '02 Kapital',          'ersetzt'),
 ('nicht veranlagte St. v. Ertrag', 31.1, '02 Kapital',      'ersetzt'),
 ('Steuern vom Umsatz',        310.2, '06 Konsum',           'ersetzt'),
 ('Körperschaftsteuer',         39.2, '05 Konzerne',         'ersetzt'),
 ('Gewerbesteuer',              75.3, '05 Konzerne',         'ersetzt'),
 ('Erbschaft/Schenkung',        15.4, '03 Erbschaft',        'ersetzt'),
 ('Grundsteuer A+B',            16.0, '04a Boden',           'umgebaut'),
 ('Solidaritätszuschlag',       12.9, '—',                   'OFFEN'),
 ('Grunderwerbsteuer',          15.1, '—',                   'OFFEN'),
 ('Kirchensteuer (rund)',       13.0, '—',                   'NICHT ERWÄHNT'),
 ('Energiesteuer',              37.6, '07 Klima (teilweise)','teilweise'),
 ('Stromsteuer',                 5.9, '07 Klima (teilweise)','teilweise'),
 ('Kraftfahrzeugsteuer',         9.6, '—',                   'OFFEN'),
 ('Tabaksteuer',                17.6, '—',                   'bleibt'),
 ('Versicherungsteuer',         19.6, '—',                   'bleibt'),
 ('Luftverkehrsteuer',           2.1, '07 Klima (teilweise)','teilweise'),
 ('Rennwett-/Lotteriesteuer',    2.5, '—',                   'bleibt'),
 ('Alkohol- und Biersteuer',     2.6, '—',                   'bleibt'),
 ('Zölle (EU-Eigenmittel)',      5.9, '—',                   'bleibt'),
]
print('=' * 98)
print('A3 — ERSETZEN DIE ZEHN POSITIONEN DIE HEUTIGEN REGELN SAUBER?')
print('=' * 98)
print(f'\n[1] ZUORDNUNG JEDER HEUTIGEN STEUER\n')
print(f'{"heutige Steuer":<32}{"Mrd":>7}  {"Position":<24}{"Status":<14}')
for nm, v, pos, st in ZUORDNUNG:
    print(f'{nm:<32}{de(v):>7}  {pos:<24}{st:<14}')
offen = [z for z in ZUORDNUNG if z[3] in ('OFFEN', 'NICHT ERWÄHNT')]
print(f'''
    UNGEKLÄRT: {de(sum(z[1] for z in offen))} Mrd EUR in {len(offen)} Steuern.''')
for nm, v, pos, st in offen:
    print(f'      {nm:<32}{de(v):>7}  {st}')
print(f'''
    Jede einzelne ist eine Entscheidung, die das Konzept treffen muss:
      Solidaritätszuschlag — ein Zuschlag auf die Einkommensteuer. Bei
        EINEM Satz von 28 % ist er logisch nicht haltbar. Er entfällt also,
        und das kostet 12,9 Mrd, die bisher in "Sonstige" mitlaufen.
      Grunderwerbsteuer — eine Steuer auf den Vorgang, nicht auf den
        Gewinn. Sie widerspricht direkt dem Umzugsaufschub aus 04b: der
        soll Umzüge erleichtern, die Grunderwerbsteuer verteuert sie mit
        3,5 bis 6,5 %. Entweder sie geht, oder 04b verliert seinen Zweck.
      Kirchensteuer — wird über die Einkommensteuer erhoben. Ohne
        Veranlagung und bei einem Satz ohne Zuschläge braucht sie eine
        eigene Lösung. Im Konzept kommt sie nicht vor.
      Kraftfahrzeugsteuer — überschneidet sich mit dem CO2-Preis.''')

print(f'''
[2] WO ZWEI POSITIONEN DENSELBEN VORGANG TREFFEN

    geklärt:
      03 Erbschaft x 04b Verkaufsgewinn — Schritt auf den Verkehrswert
        zum Todestag. Jeder Vorgang einmal.
      04a Boden x 04b Verkaufsgewinn — kein Abzug der Grundsteuer, weil
        Bestand und Zuwachs verschiedene Grundlagen sind (A16). Aber die
        laufende Abgabe senkt das Preisniveau und damit die Gewinne:
        04a und 04b sind NICHT addierbar, rund 4,7 % Abschlag auf 04b.
      06 Konsum x 08 Dividende — die Mehrwertsteuer ist regressiv, die
        Dividende als Festbetrag progressiv. Offen ausgewiesen.

    ungeklärt:
      02 Kapital x 04b Verkaufsgewinn — ein Immobiliengewinn IST ein
        Kapitalgewinn. Die Abgrenzung ist nirgends definiert. Solange
        "Kapitalerträge 28 %" auf der heutigen Abgeltungsteuer kalibriert
        ist, enthält es die Immobiliengewinne nicht — aber das steht nur
        in meinem Prüfskript, nicht im Modell.
      05 Konzerne x 01 Einkommen — ein Personenunternehmen zahlt heute
        Einkommensteuer, eine Kapitalgesellschaft Körperschaft- und
        Gewerbesteuer. Bei einem Satz von 28 % für beide ist die
        Rechtsformneutralität erreicht — das ist ein starkes Argument des
        Konzepts, aber die Zuordnung der 152 Mrd zu den beiden Zeilen ist
        nicht hergeleitet.
      07 Klima x "Sonstige Steuern" — der Abbau klimaschädlicher
        Subventionen von 20 Mrd besteht überwiegend aus Vergünstigungen
        INNERHALB der Energiesteuer. Die Energiesteuer steckt in
        "Sonstige". Kein Doppelzählung, aber die 20 Mrd müssten dort
        aufschlagen, nicht als eigener Baustein daneben stehen.''')

print(f'''
[3] WER BEKOMMT DAS GELD? — DIE FRAGE, DIE WIR NIE GESTELLT HABEN

    Steuerverteilung 2025, amtlich (Destatis):
      Bund       388,7 Mrd
      Länder     415,3 Mrd
      Gemeinden  150,9 Mrd
      EU          34,9 Mrd''')
GEM_EIGEN = 75.3 + 16.0
print(f'''
    Davon sind {de(GEM_EIGEN)} Mrd eigene Gemeindesteuern: Gewerbesteuer 75,3
    und Grundsteuer 16,0. Das ist die Finanzautonomie der Kommunen.

    DAS PROBLEM: Position 05 ersetzt die Gewerbesteuer durch eine nach
    Umsatz verteilte Abgabe von 28 %. Damit verliert jede Gemeinde ihre
    wichtigste eigene Einnahme und den Anreiz, Gewerbe anzusiedeln. Das
    ist keine Nebenwirkung, sondern der Kernkritikpunkt an jeder
    formelhaften Aufteilung. Position 04a trifft die zweite Gemeindesteuer.
    Zusammen stehen {de(GEM_EIGEN)} Mrd kommunale Eigenfinanzierung zur Debatte,
    und das Konzept sagt dazu nichts.

    DIE RECHTSLAGE, belegt: Artikel 28 Abs. 2 Satz 3 GG verlangt eine
    Steuerquelle der Gemeinden mit Hebesatzrecht, die an der Wirtschafts-
    kraft anknüpft. Nach dem Gutachten des Wissenschaftlichen Dienstes des
    Bundestages (WD 4-049/19) ist "der Bestand der Gewerbesteuer durch
    diese Vorschrift nicht verfassungsrechtlich gesichert. Sie könnte
    vielmehr durch eine andere, vergleichbare Steuer ersetzt werden."
    Position 05 ist damit verfassungsrechtlich MÖGLICH — aber nur, wenn
    ein Ersatz mit Hebesatzrecht bereitsteht. Den gibt es im Konzept nicht.

    MÖGLICHE ANTWORT, die zum Konzept passt: 04a wird die kommunale
    Steuer mit Hebesatzrecht, so wie Estland es macht, wo die Gemeinde
    den Satz zwischen 0,1 und 1 % selbst setzt. Dann braucht 04a aber
    mehr Volumen als die heutigen 16 Mrd — und genau das wäre der von
    mir am 2.10. gerechnete Weg b) mit 1 % Satz und rund 35 Mrd.
    Die Entscheidung über 04a ist damit keine Steuerfrage, sondern eine
    Frage der Finanzverfassung.''')
