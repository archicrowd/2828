# -*- coding: utf-8 -*-
"""
R14 — Lösung 2: einmalig erhöhter Freibetrag beim Ausstieg

ENTSCHEIDUNGSSTAND
  04b besteuert den BODENgewinn, nicht den ganzen Verkaufsgewinn (R13).
  Regelfreibetrag 100.000 EUR je Erwerb.
  Umzugsaufschub, wenn wieder in selbstgenutztes Eigentum investiert wird.
  NEU, Lösung 2: wer das Eigentum endgültig verlässt — Heim, Miete,
  Nachlass —, hat EINMAL IM LEBEN einen erhöhten Freibetrag.
  Vorbild: USA bis 1997, einmalige Freistellung von 125.000 USD ab 55.

DATENGRUNDLAGE, JETZT AMTLICH
  Destatis GENESIS 61262-0001, Häuserpreisindex Deutschland, Jahreswerte
  2000 bis 2025, Basis 2025 = 100. Alle Werte mit Kennzeichen "e"
  (geschätzt bzw. revidiert). Die Reihe bestätigt die Annahme aus R13:
  2000 -> 2010 nominal -0,7 %, 2010 -> 2025 +82,1 %.
  Vor 2000 liegt keine Reihe vor; Käufe davor werden mit dem Wert von
  2000 gerechnet. Das unterschätzt deren Gewinn und ist insofern
  vorsichtig.
  BBSR Deutschlandatlas 2018: Baulandpreise 15 bis 2.000 EUR je m²,
  Bundesschnitt 135.
"""
import json, numpy as np, textwrap

def de(v, nk=0):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=0): return ('+' if v >= 0 else '') + de(v, nk)

HPI = {int(k): v for k, v in json.load(open('hpi.json')).items()}
J0, J1 = min(HPI), max(HPI)
def idx(j): return HPI[min(max(j, J0), J1)]

BODEN_ANT = {'Land': 0.20, 'Mittelstadt': 0.35, 'Großstadt': 0.55, 'München': 0.70}
REGIO_DYN = {'Land': 0.75, 'Mittelstadt': 1.00, 'Großstadt': 1.35, 'München': 1.60}
FREI, SATZ = 100_000, 0.28
VERKAUF_J = 2026
def faktor(kauf, reg):
    # 2026 ist nicht in der Reihe; 2025 + 3,2 % Fortschreibung des Vorjahres
    i1 = idx(J1) * 1.032
    return 1 + (i1 / idx(kauf) - 1) * REGIO_DYN[reg]

# (Name, Kaufjahr, Region, Kaufpreis, Ausstieg?)  Ausstieg = kein Ersatzkauf
FAELLE = [
 ('Reihenhaus Landkreis Sachsen',     2005, 'Land',        110_000, True),
 ('Einfamilienhaus Kleinstadt NRW',   2000, 'Mittelstadt', 185_000, True),
 ('Eigentumswohnung Leipzig',         2015, 'Großstadt',   145_000, False),
 ('Einfamilienhaus Münchner Umland',  2010, 'München',     420_000, True),
 ('Altbauwohnung München',            2000, 'München',     180_000, True),
 ('Eigentumswohnung Berlin',          2018, 'Großstadt',   310_000, False),
 ('Vermietetes Haus Hamburg',         2012, 'Großstadt',   890_000, None),
 ('Neubau Brandenburg, Kauf im Hoch', 2022, 'Land',        395_000, True),
]
print('=' * 100)
print('R14 — LÖSUNG 2: EINMALIG ERHÖHTER FREIBETRAG BEIM AUSSTIEG')
print('=' * 100)

print(f'\n[1] KALIBRIERUNG — wie hoch muss der einmalige Freibetrag sein?')
print(f'    Zweck: der gewöhnliche Ausstieg darf nicht belastet werden, der')
print(f'    aussergewöhnliche Lagegewinn schon. Bodengewinne der Fälle:\n')
print(f'{"Fall":<34}{"Kauf":>6}{"Verkauf":>11}{"Bodengewinn":>14}')
bg = {}
for name, kj, reg, preis, aus in FAELLE:
    v = preis * faktor(kj, reg)
    g = (v - preis) * BODEN_ANT[reg]
    bg[name] = (g, aus, reg, kj, preis, v)
    print(f'{name[:33]:<34}{kj:>6}{de(v):>11}{pm(g):>14}')

print(f'\n[2] WIRKUNG JE HÖHE DES EINMALIGEN FREIBETRAGS, nur Ausstiegsfälle\n')
STUFEN = [100_000, 200_000, 300_000, 400_000, 500_000]
print(f'{"Fall":<34}' + ''.join(f'{de(s/1000)+" Tsd":>13}' for s in STUFEN))
for name, (g, aus, reg, kj, preis, v) in bg.items():
    if aus is not True: continue
    row = f'{name[:33]:<34}'
    for s in STUFEN:
        row += f'{de(max(g - s, 0) * SATZ):>13}'
    print(row)
print(f'''
    Bei 300.000 EUR zahlt von den gewöhnlichen Ausstiegen keiner mehr —
    nur das Münchner Umland-Haus mit {de(bg["Einfamilienhaus Münchner Umland"][0])} EUR Bodengewinn
    bleibt drin, und das ist der Fall, den der Grundsatz treffen WILL.
    Gesetzt wird deshalb 300.000 EUR, einmal im Leben.''')

EINMAL = 300_000
print(f'\n[3] DIE REGEL IM ZUSAMMENSPIEL, Verkauf {VERKAUF_J}\n')
print(f'{"Fall":<34}{"Bodengewinn":>13}  {"greift":<24}{"Steuer":>9}')
ges = 0.0
for name, (g, aus, reg, kj, preis, v) in bg.items():
    if aus is None:
        st, wie = max(g, 0) * SATZ, 'vermietet: kein Schutz'
    elif aus is False:
        st, wie = 0.0, 'Umzugsaufschub'
    elif g <= 0:
        st, wie = 0.0, 'Verlust, vortragsfähig'
    elif g <= EINMAL:
        st, wie = 0.0, 'Ausstieg einmalig 300T'
    else:
        st, wie = (g - EINMAL) * SATZ, 'Ausstieg, Rest steuerpfl.'
    ges += st
    print(f'{name[:33]:<34}{pm(g):>13}  {wie:<24}{de(st):>9}')
print(f'{"":<34}{"":>13}  {"zusammen":<24}{de(ges):>9}')

print(f'''
[4] AUFKOMMEN — UND HIER KIPPT MEINE EMPFEHLUNG VON GESTERN

    Ich hatte in R13 empfohlen, nur den BODENanteil zu besteuern: prinzipien-
    treu, besser gezielt, keine Zusatzverwaltung. Das Aufkommen hatte ich
    dabei nicht nachgerechnet. Hier ist es, und es widerlegt mich.''')
UMSATZ, SELBST, KURZ, GEWINN_ANT, SATZ_HEUTE = 247.0, 0.50, 0.35, 0.25, 0.42
BODEN_MITTEL, AUSSTIEG = 0.40, 0.40
# heutiges Recht: steuerpflichtig nur binnen zehn Jahren UND nicht selbstgenutzt,
# dann aber der GANZE Gewinn zum persönlichen Satz
basis_heute = UMSATZ * KURZ * (1 - SELBST) * GEWINN_ANT
heute = basis_heute * SATZ_HEUTE
print(f'''
    Heutiges Recht: Basis {de(basis_heute,1)} Mrd (ganzer Gewinn, nur {de(KURZ*(1-SELBST)*100,1)} % der
    Fälle), Satz {de(SATZ_HEUTE*100)} % -> Aufkommen {de(heute,1)} Mrd EUR.

    Unter 04b entfällt die Zehnjahresfrist, der Satz fällt aber auf 28 %.
    Entscheidend ist, wie weit die Basis dafür wächst:''')
sig = 0.9
rng = np.random.default_rng(28)
def anteil_ueber(frei, schnitt):
    st = rng.lognormal(np.log(schnitt) - sig**2/2, sig, 300_000)
    return np.maximum(st - frei, 0).sum() / st.sum()
FALL_N = 805_000
print(f'\n{"Variante 04b":<46}{"Basis":>10}{"Faktor":>9}{"Aufkommen":>12}{"gegen heute":>13}')
for nm, bod, fr_reg, fr_ein in (
        ('ganzer Gewinn, Freibetrag 100/300 Tsd', 1.00, 100_000, 300_000),
        ('ganzer Gewinn, Freibetrag 200/300 Tsd', 1.00, 200_000, 300_000),
        ('nur Bodenanteil, Freibetrag 100/300',   BODEN_MITTEL, 100_000, 300_000),
        ('nur Bodenanteil, ohne Freibetrag',      BODEN_MITTEL, 0, 0)):
    schnitt = UMSATZ * 1e9 / FALL_N * GEWINN_ANT * bod
    f_aus = anteil_ueber(fr_ein, schnitt) if fr_ein else 1.0
    b_verm = UMSATZ * (1 - SELBST) * GEWINN_ANT * bod
    b_selbst = UMSATZ * SELBST * GEWINN_ANT * bod * AUSSTIEG * f_aus
    basis = b_verm + b_selbst
    auf = basis * SATZ
    print(f'{nm:<46}{de(basis,1):>10}{de(basis/basis_heute,2):>9}'
          f'{de(auf,1):>12}{pm(auf-heute,1):>13}')
print(f'''
    DER BEFUND: der Bodenanteil von {de(BODEN_MITTEL*100)} % frisst die Basisverbreiterung
    auf. Die Fallabdeckung wächst von {de(KURZ*(1-SELBST)*100,1)} auf gut 50 % der Umsätze,
    also fast dreifach — aber nur {de(BODEN_MITTEL*100)} % des Gewinns zählen, und der Satz
    fällt von {de(SATZ_HEUTE*100)} auf {de(SATZ*100)} %. Unter dem Strich VERLIERT die Bodenvariante
    gegenüber heute. Sie ist eine Gerechtigkeitsmassnahme, keine Finanzierung.

    DIE ALTERNATIVE, die beides schafft: ganzer Gewinn, aber ein höherer
    Regelfreibetrag von 200.000 EUR. Dann fällt das Kleinstadthaus aus NRW
    trotzdem heraus — sein ganzer Gewinn liegt bei {de(345_244-185_000)} EUR —, und
    das Aufkommen bleibt deutlich positiv.''')
print(f'''
[5] GEGENPROBE AN DEN FÄLLEN: ganzer Gewinn mit 200.000/300.000
''')
print(f'{"Fall":<34}{"ganzer Gewinn":>15}  {"greift":<26}{"Steuer":>9}')
ges2 = 0.0
for name, (g, aus, reg, kj, preis, v) in bg.items():
    gg = v - preis
    if aus is None:
        st, wie = max(gg, 0) * SATZ, 'vermietet: kein Schutz'
    elif aus is False:
        st, wie = 0.0, 'Umzugsaufschub'
    elif gg <= 0:
        st, wie = 0.0, 'Verlust, vortragsfähig'
    elif gg <= 300_000:
        st, wie = 0.0, 'Ausstieg einmalig 300 Tsd'
    else:
        st, wie = (gg - 300_000) * SATZ, 'Ausstieg, Rest steuerpfl.'
    ges2 += st
    print(f'{name[:33]:<34}{pm(gg):>15}  {wie:<26}{de(st):>9}')
print(f'{"":<34}{"":>15}  {"zusammen":<26}{de(ges2):>9}')
print(f'''
    Dieselbe Schutzwirkung wie die Bodenvariante — Sachsen, NRW, München
    zahlen nichts —, aber ein positives Aufkommen. Das Münchner Umland-Haus
    zahlt mehr, und das ist der Fall, den der Grundsatz treffen will.''')
