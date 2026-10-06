# -*- coding: utf-8 -*-
"""
R13 — Wen der Freibetrag begünstigt und wen er belastet

DIE FRAGE
  100.000 EUR Freibetrag je Erwerb auf den Verkaufsgewinn selbstgenutzten
  Wohnens. Wer wird damit freigestellt, wer zahlt — und sind das die
  Richtigen nach dem Grundsatz "was der Boden wert ist, hat die
  Allgemeinheit gebaut"?

WARUM FÄLLE UND KEINE VERTEILUNG
  In R12 habe ich die Gewinne als Lognormal mit sigma 0,9 gesetzt. Das war
  eine Annahme, und sie trägt die Antwort auf diese Frage nicht: wer
  getroffen wird, hängt an WANN und WO gekauft wurde, nicht an einer
  Streuungsziffer. Deshalb hier gerechnete Konstellationen.

AMTLICHE GRUNDLAGEN
  Destatis: Preise für Häuser und Eigentumswohnungen +82 % von 2010 bis
    2025. Häuserpreisindex (2025 = 100): 2020 90,8 · 2021 101,4 ·
    2022 107,5 · 2023 98,4 · 2024 96,9 · 2025 100,0.
  BBSR Deutschlandatlas (Datenjahr 2018): Baulandpreise 15 bis 2.000 EUR
    je m², Bundesschnitt 135. Ostdeutsche Landkreise 15 bis 25, Alpenrand
    350 bis 900, die fünf teuersten Kreise 1.000 bis 2.000. Zwischen 2013
    und 2018 bundesweit +6 % im Jahr, Großstädte +12 %.

GESETZT UND NICHT ERHOBEN
  Der Verlauf VOR 2010. Nominal waren die Preise in Deutschland von Mitte
  der 1990er bis 2009 etwa flach — die Korrektur nach dem Wiedervereini-
  gungsboom. Ich rechne deshalb 1990 bis 2009 mit 0 % nominal und lasse
  den gesamten Zuwachs ab 2010 entstehen. Das ist vorsichtig in der
  Richtung, die hier zählt: es macht alte Käufe ÄRMER an Gewinn, als sie
  in Ballungsräumen tatsächlich sind.
  Der Bodenanteil am Objektwert. Gesetzt nach Lage: Land 20 %, Mittel-
  stadt 35 %, Großstadt 55 %, München 70 %.
"""
import numpy as np, textwrap

def de(v, nk=0):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=0): return ('+' if v >= 0 else '') + de(v, nk)

IDX = {1990: 55, 1995: 55, 2000: 55, 2005: 55, 2009: 55,
       2010: 55, 2015: 70, 2018: 82, 2020: 90.8, 2021: 101.4,
       2022: 107.5, 2023: 98.4, 2024: 96.9, 2025: 100.0, 2026: 103.0}
# 2010 = 55 folgt aus +82 % bis 2025 (100/1,82 = 54,9). Dazwischen linear
# zwischen den Stützjahren; 2015 und 2018 aus dem Verlauf interpoliert.
REGIO = {'Land': 0.20, 'Mittelstadt': 0.35, 'Großstadt': 0.55, 'München': 0.70}
# Regionaler Aufschlag auf die Bundesentwicklung, aus der BBSR-Spreizung
REGIO_DYN = {'Land': 0.75, 'Mittelstadt': 1.00, 'Großstadt': 1.35, 'München': 1.60}
FREI, SATZ = 100_000, 0.28

FAELLE = [
 # (Name, Kaufjahr, Region, Kaufpreis, selbstgenutzt, Umzug in neues Eigenheim)
 ('Reihenhaus Landkreis Sachsen',       2005, 'Land',        110_000, True,  True),
 ('Einfamilienhaus Kleinstadt NRW',     1995, 'Mittelstadt', 185_000, True,  False),
 ('Eigentumswohnung Leipzig',           2015, 'Großstadt',   145_000, True,  True),
 ('Einfamilienhaus Münchner Umland',    2010, 'München',     420_000, True,  False),
 ('Altbauwohnung München',              1990, 'München',     180_000, True,  False),
 ('Eigentumswohnung Berlin',            2018, 'Großstadt',   310_000, True,  True),
 ('Vermietetes Haus Hamburg',           2012, 'Großstadt',   890_000, False, False),
 ('Neubau Brandenburg, Kauf im Hoch',   2022, 'Land',        395_000, True,  False),
]

_J = sorted(IDX)
def idx(jahr):
    """Index mit linearer Interpolation zwischen den Stützjahren."""
    if jahr in IDX: return IDX[jahr]
    return float(np.interp(jahr, _J, [IDX[j] for j in _J]))

def wert(kauf, jahr, region):
    """Wertentwicklung mit regionalem Faktor auf die Bundesdynamik."""
    bund = idx(jahr) / idx(kauf) - 1
    return 1 + bund * REGIO_DYN[region]

print('=' * 104)
print('R13 — ZIELGENAUIGKEIT DES FREIBETRAGS VON 100.000 EUR')
print('=' * 104)
print(f'\n[1] DIE FÄLLE, Verkauf 2026\n')
print(f'{"Fall":<34}{"Kauf":>6}{"Preis":>10}{"Verkauf":>10}'
      f'{"Gewinn":>10}{"davon Boden":>13}{"steuerpfl.":>12}{"Steuer":>9}')
erg = []
for name, kj, reg, preis, selbst, umzug in FAELLE:
    f = wert(kj, 2026, reg)
    verkauf = preis * f
    gewinn = verkauf - preis
    boden_ant = REGIO[reg]
    gewinn_boden = gewinn * boden_ant
    if not selbst:
        stpf = gewinn                      # kein Freibetrag, kein Aufschub
    elif umzug:
        stpf = 0.0                         # Umzugsaufschub greift
    else:
        stpf = max(gewinn - FREI, 0)
    steuer = stpf * SATZ
    erg.append((name, kj, reg, preis, verkauf, gewinn, gewinn_boden, stpf, steuer,
                selbst, umzug))
    print(f'{name[:33]:<34}{kj:>6}{de(preis):>10}{de(verkauf):>10}'
          f'{pm(gewinn):>10}{de(gewinn_boden):>13}{de(stpf):>12}{de(steuer):>9}')

print(f'''
[2] WER WIRD FREIGESTELLT, UND WARUM

    Frei durch UMZUGSAUFSCHUB (zahlt nichts, egal wie hoch der Gewinn):''')
for e in erg:
    if e[9] and e[10]:
        print(f'      {e[0][:40]:<42} Gewinn {pm(e[5]):>9} EUR')
print('\n    Frei durch FREIBETRAG (Gewinn positiv, aber unter 100.000):')
keiner = True
for e in erg:
    if e[9] and not e[10] and e[7] == 0 and e[5] > 0:
        print(f'      {e[0][:40]:<42} Gewinn {pm(e[5]):>9} EUR'); keiner = False
if keiner:
    print('      keiner in dieser Auswahl — die kurzen Haltedauern liegen')
    print('      alle schon im Umzugsaufschub')
print('\n    VERLUST, eigene Frage:')
for e in erg:
    if e[5] < 0:
        print(f'      {e[0][:40]:<42} Verlust {de(e[5]):>8} EUR')
        print('      Kauf im Hoch 2022, Verkauf 2026 nach der Korrektur. Unter')
        print('      "alles ist Einkommen" muss ein Verlust abziehbar sein —')
        print('      sonst ist die Regel einseitig. Das ist bisher nicht geklärt.')
print('\n    ZAHLT:')
for e in erg:
    if e[8] > 0:
        print(f'      {e[0][:40]:<42} Steuer {de(e[8]):>9} EUR '
              f'({de(e[8]/e[5]*100,1)} % des Gewinns)')

print(f'''
[3] DAS MUSTER — UND ES IST DAS GEWOLLTE

    Der Freibetrag von 100.000 EUR wirkt als REGIONALER UND ZEITLICHER
    FILTER, ohne eine Region zu nennen. Getroffen wird, wer lange in einem
    Ballungsraum gehalten hat — also genau dort, wo die öffentliche
    Investition am meisten in den Bodenwert gewandert ist. Nicht getroffen
    wird, wer auf dem Land oder kurz gehalten hat.

    Das ist kein Zufall, sondern folgt aus der Spreizung der Baulandpreise:
    15 bis 2.000 EUR je m², Faktor 133 (BBSR). Ein Gewinn über 100.000 EUR
    entsteht in ländlichen Kreisen nur bei sehr grossen Objekten, in München
    schon beim Durchschnittsfall.

[4] WAS DER UMZUGSAUFSCHUB NICHT FÄNGT — DIE ECHTEN HÄRTEN
    Der Aufschub setzt voraus, dass wieder in selbstgenutztes Wohneigentum
    investiert wird. Drei Gruppen tun das nicht:''')

HAERTE = [
 ('Umzug ins Heim oder betreute Wohnen',
  'verkauft und mietet. Kein Ersatzobjekt, also kein Aufschub. Der Gewinn '
  'ist voll steuerpflichtig, obwohl das Geld die Pflege zahlt.'),
 ('Verkleinern in die Miete im Alter',
  'genau die Mobilität, die man wohnungspolitisch will — grosse Wohnung '
  'frei für eine Familie. Der Aufschub bestraft sie.'),
 ('Erbfall',
  'der Erbe tritt nach heutigem Recht in die Anschaffung des Erblassers '
  'ein und übernimmt den gesamten latenten Gewinn. Zusammen mit Position '
  '03 trifft denselben Vorgang zweimal.'),
]
for t, b in HAERTE:
    print(f'\n      {t}')
    for zeile in textwrap.wrap(b, 68):
        print(f'        {zeile}')

print(f'''

[5] DIE ERBFALL-KOLLISION, GERECHNET
    Beispiel: Erblasser kauft 1985 in Frankfurt für 150.000, Wert 2026''')
f_erb = wert(1990, 2026, 'Großstadt')
kauf_erb, wert_erb = 150_000, 150_000 * f_erb
gewinn_erb = wert_erb - kauf_erb
FREI_ERB = 200_000          # Position 03
erbst = max(wert_erb - FREI_ERB, 0) * SATZ
vst = max(gewinn_erb - FREI, 0) * SATZ
print(f'''      Wert bei Erbfall                      {de(wert_erb):>9} EUR
      Position 03, Freibetrag 200.000       {de(erbst):>9} EUR Erbschaftsteuer
      Position 04b, Freibetrag 100.000      {de(vst):>9} EUR auf den Verkaufsgewinn
      zusammen                              {de(erbst+vst):>9} EUR = {de((erbst+vst)/wert_erb*100,1)} % des Werts

    Das ist zu viel, und zwar nicht wegen der Höhe, sondern wegen der
    Begründung: derselbe Wertzuwachs wird zweimal als Einkommen erfasst,
    einmal beim Erben und einmal beim Verkaufen. Die saubere Lösung ist
    der SCHRITT AUF DEN VERKEHRSWERT: mit der Erbschaftsteuer wird der
    Wert zum Todestag neuer Einstandspreis. Was danach wächst, ist der
    Gewinn des Erben; was davor wuchs, hat die Erbschaftsteuer erfasst.
    Jeder Vorgang einmal — das ist Ihr Grundsatz, nicht mein Zusatz.''')
vst_neu = 0.0
print(f'''      mit Schritt auf den Verkehrswert      {de(erbst+vst_neu):>9} EUR = '''
      f'''{de((erbst+vst_neu)/wert_erb*100,1)} % des Werts''')

print(f'''
[6] DIE ZWEITE OFFENE FRAGE: GANZER GEWINN ODER NUR DER BODEN?
    Der Grundsatz begründet nur den BODENanteil — das Gebäude hat der
    Eigentümer bezahlt, und es verbraucht sich. Gerechnet macht das viel aus.
''')
print(f'{"Fall":<34}{"Steuer ganzer Gewinn":>22}{"nur Bodenanteil":>18}{"Differenz":>12}')
sum_g = sum_b = 0.0
for name, kj, reg, preis, verkauf, gewinn, g_boden, stpf, steuer, selbst, umzug in erg:
    if selbst and umzug:
        sg = sb = 0.0
    elif selbst:
        sg = max(gewinn - FREI, 0) * SATZ
        sb = max(g_boden - FREI, 0) * SATZ
    else:
        sg, sb = gewinn * SATZ, g_boden * SATZ
    sum_g += sg; sum_b += sb
    print(f'{name[:33]:<34}{de(sg):>22}{de(sb):>18}{de(sg-sb):>12}')
print(f'{"zusammen":<34}{de(sum_g):>22}{de(sum_b):>18}{de(sum_g-sum_b):>12}')
print(f'''
    Nur der Bodenanteil wäre {de((1-sum_b/sum_g)*100,0)} % weniger Aufkommen — aber genau
    das, was der Grundsatz hergibt. Der ganze Gewinn ist leichter zu
    erklären und zu prüfen (ein Kaufpreis, ein Verkaufspreis), erfasst
    aber auch Inflation auf dem Gebäude. Das ist eine Entscheidung
    zwischen Prinzipientreue und Vollziehbarkeit.''')
