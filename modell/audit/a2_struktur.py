# -*- coding: utf-8 -*-
"""
A2 — Zeilenweiser Abgleich und die Struktur des Modells

FRAGE
  Ersetzt jede Modellzeile eine heutige Steuer sinnvoll, und ist die Summe
  plausibel? Und: was ist auf der Ausgabenseite eigentlich drin?
"""
def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1): return ('+' if v >= 0 else '') + de(v, nk)

# Modellzeilen nach allen Korrekturen R1-R16, Szenario Robust, DD-Stufe 50 %
MODELL = [
 ('Einkommensteuer (inkl. steuerpfl. DD)', 313.3, 341.1,
  'Lohnsteuer 262,7 + veranlagte ESt 78,4'),
 ('Kapitalerträge 28 %',                    48.8,  55.9,
  'Abgeltungsteuer 24,8 + nicht veranl. 31,1'),
 ('Mehrwertsteuer (Label)',                375.9, 310.2, 'Steuern vom Umsatz'),
 ('Unternehmen & Plattformen 28 %',        152.0, 114.5,
  'Körperschaftsteuer 39,2 + Gewerbesteuer 75,3'),
 ('Erbschaft 28 %',                         21.0,  15.4, 'Erbschaft/Schenkung'),
 ('Vermögen-Mindeststeuer',                 30.0,   0.0, 'existiert heute nicht'),
 ('CO2 (BEHG-Korridor)',                    33.0,   0.0,
  'BEHG-Erlöse sind keine Steuer, fliessen in den KTF'),
 ('Position 04b Verkaufsgewinn',             4.1,   0.0,
  '§ 23 EStG wird amtlich nicht ausgewiesen'),
 ('Sonstige Steuern',                      165.0, 140.4,
  'Energie 37,6 · Versicherung 19,6 · Tabak 17,6 · Grunderwerb 15,1 · Soli 12,9 · KFZ 9,6 · Rest 27,9'),
]
BAUSTEINE = [('Vermögensteuer 1 % ab 2 Mio.', 9.3), ('Bodenwertabgabe', 0.0),
             ('Abbau klimaschädlicher Subventionen', 20.0), ('CO2-Pfad', 0.0)]
AUSGABEN = [('Basisausgaben nach Transferersatz', 596.0),
            ('SV-Zuschuss', 60.0), ('Härtefallfonds', 40.0),
            ('Digitaldividende', 475.9)]
STEUER_IST = 989.8
print('=' * 104)
print('A2 — ZEILENWEISER ABGLEICH GEGEN DIE AMTLICHE STEUERSTATISTIK 2025')
print('=' * 104)
print(f'\n{"Modellzeile":<38}{"Modell":>9}{"heute":>9}{"Delta":>9}  entspricht heute')
m_s = h_s = 0.0
for nm, m, h, q in MODELL:
    m_s += m; h_s += h
    print(f'{nm:<38}{de(m):>9}{de(h):>9}{pm(m-h):>9}  {q[:46]}')
print(f'{"-"*104}')
print(f'{"Steuern zusammen":<38}{de(m_s):>9}{de(h_s):>9}{pm(m_s-h_s):>9}')
b_s = sum(v for _, v in BAUSTEINE)
print(f'{"Bausteine":<38}{de(b_s):>9}{de(0):>9}{pm(b_s):>9}')
print(f'{"EINNAHMEN":<38}{de(m_s+b_s):>9}{de(STEUER_IST):>9}{pm(m_s+b_s-STEUER_IST):>9}')
print(f'''
    Das Modell erhebt {de((m_s+b_s)/STEUER_IST*100-100,1)} % mehr Steuern als heute, also
    {pm(m_s+b_s-STEUER_IST)} Mrd EUR. Bei einem BIP von 4.884 Mrd (2028, 3 % nominal)
    sind das {de((m_s+b_s-STEUER_IST)/4884*100,1)} Prozentpunkte zusätzliche Steuerquote.
    Das ist eine sehr grosse Zahl und sie gehört auf die Seite — bisher
    steht sie nirgends.''')

print(f'\n[2] DIE AUSGABENSEITE — HIER IST DIE GRÖSSERE LÜCKE\n')
for nm, v in AUSGABEN:
    print(f'      {nm:<40}{de(v):>8}')
a_s = sum(v for _, v in AUSGABEN)
print(f'      {"-"*48}\n      {"zusammen":<40}{de(a_s):>8}')
print(f'''
    Von diesen {de(a_s)} Mrd sind {de(AUSGABEN[0][1]+AUSGABEN[1][1]+AUSGABEN[2][1])} Mrd — die drei ersten Zeilen —
    im Modell NICHT hergeleitet. Der Kommentar nennt sie "Basisausgaben
    nach Transferersatz/RV/Verwaltung", es gibt aber keine Quelle und keine
    Rechnung dazu. Die Digitaldividende ist die einzige Ausgabenzeile, die
    aus einer Formel folgt.''')

print(f'''
[3] DER EIGENTLICHE BEFUND DIESES AUDITS

    Zwei Blöcke tragen das Modell, und beide sind unbelegt:
      Einnahmen  "Sonstige Steuern"        {de(165.0):>8} Mrd
      Ausgaben   "Basis + Zuschuss + Härte" {de(696.0):>8} Mrd
      zusammen                             {de(861.0):>8} Mrd

    Das sind {de(861/(m_s+b_s)*100,1)} % der Einnahmen und {de(696/a_s*100,1)} % der Ausgaben.
    Alles, was wir in R1 bis R16 geprüft haben — Erbschaft 21,0, CO2 33,0,
    Vermögen 30,0, Verkaufsgewinn 4,1, Aufteilung 152,0 — summiert sich auf
    {de(21+33+30+4.1+152)} Mrd. Die beiden unbelegten Blöcke sind dreimal so gross.

    Anders gesagt: die Belegstand-Tabelle bewertet zehn Positionen, aber
    die zwei grössten Zahlen des Modells sind gar keine Position. Das ist
    die wichtigste Lücke, und sie ist grösser als alle bisher gefundenen
    zusammen.''')

print(f'''
[4] DIE SOZIALVERSICHERUNG — SIE FEHLT GANZ, OBWOHL ZWEI POSITIONEN SIE UMBAUEN
    Beitragseinnahmen 2024: rund 707,7 Mrd EUR (Renten- 304,8, Kranken-
    298,1, Pflege- 65,4, Arbeitslosenversicherung 39,4).
    Heutiger Gesamtbeitragssatz: Rente 18,6 + Kranken rund 16,5 + Pflege 3,6
    + Arbeitslos 2,6 = rund 41,3 %.
    Position 10 verspricht 28 %, später 18 %.''')
BEITRAEGE, SATZ_IST = 707.7, 0.413
for ziel in (0.28, 0.18):
    neu = BEITRAEGE * ziel / SATZ_IST
    print(f'''
      Beitragssatz {de(ziel*100,0)} %: Einnahmen {de(neu)} statt {de(BEITRAEGE)} Mrd
        Rückgang {de(neu-BEITRAEGE)} Mrd — im Modell steht ein Zuschuss von 60 Mrd.
        Ungedeckt bleiben damit {de(abs(neu-BEITRAEGE)-60)} Mrd.''')
print(f'''
    GEGENARGUMENT, und es ist das tragende: die Digitaldividende von
    {de(475.9)} Mrd soll die Grundsicherungs- und Teile der Rentenfunktion
    ersetzen. Dann entfallen auf der Ausgabenseite der Sozialversicherung
    entsprechende Leistungen. Genau diese Verrechnung steckt vermutlich in
    den {de(596.0)} Mrd "Basisausgaben nach Transferersatz" — nur steht sie
    nirgends offen.

    SOLANGE DAS NICHT AUFGESCHRIEBEN IST, ist das Modell für Dritte nicht
    nachrechenbar. Nicht weil die Zahlen falsch wären, sondern weil der
    grösste Umbau des ganzen Konzepts — ein Transfersystem von über
    700 Mrd — in einer einzigen unerklärten Zeile verschwindet.''')
