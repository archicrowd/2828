# -*- coding: utf-8 -*-
"""
R15 — Position 04b, Endfassung: Lösung 2, ganzer Gewinn, ein Freibetrag

WAS SICH GEGENÜBER R13 GEÄNDERT HAT, UND WARUM
  1. NICHT nur der Bodenanteil. In R13 hatte ich das empfohlen —
     prinzipientreu und besser gezielt — ohne das Aufkommen zu rechnen.
     R14 zeigt: der Bodenanteil von rund 40 % frisst die Basisverbreiterung
     auf. Die Fallabdeckung wächst fast dreifach, aber der Satz fällt von
     42 auf 28 %, und unter dem Strich verliert die Bodenvariante 1,1 Mrd
     gegenüber heute. Sie wäre eine Gerechtigkeitsmassnahme, keine
     Finanzierung. Der ganze Gewinn mit höherem Freibetrag schützt
     dieselben Fälle und bringt +4,3 Mrd.
  2. KEIN Regelfreibetrag von 100.000 mehr. Er hat keinen Fall: wer umzieht,
     bekommt den Aufschub, wer aussteigt, den einmaligen Freibetrag. Nur
     bei teilweiser Reinvestition bliebe ein Rest — ein Detail, das keine
     eigene Zahl auf der Seite verdient.
  Ergebnis: EINE Zahl statt zwei. 300.000 EUR, einmal im Leben.

DATEN
  Destatis GENESIS 61262-0001 (Häuserpreisindex 2000–2025, Basis 2025=100,
  alle Werte Kennzeichen "e"); BBSR Deutschlandatlas 2018 (Baulandpreise);
  Gutachterausschüsse/BBSR Immobilienmarktbericht 2025 (247 Mrd Geldumsatz,
  805.000 Kaufverträge 2024).
"""
import json, numpy as np

def de(v, nk=0):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=0): return ('+' if v >= 0 else '') + de(v, nk)

HPI = {int(k): v for k, v in json.load(open('hpi.json')).items()}
J0, J1 = min(HPI), max(HPI)
REGIO_DYN = {'Land': 0.75, 'Mittelstadt': 1.00, 'Großstadt': 1.35, 'München': 1.60}
EINMAL, SATZ = 300_000, 0.28
def faktor(kauf, reg):
    i0 = HPI[min(max(kauf, J0), J1)]
    return 1 + (HPI[J1] * 1.032 / i0 - 1) * REGIO_DYN[reg]

FAELLE = [
 ('Reihenhaus Landkreis Sachsen',     2005, 'Land',        110_000, 'aus'),
 ('Einfamilienhaus Kleinstadt NRW',   2000, 'Mittelstadt', 185_000, 'aus'),
 ('Eigentumswohnung Leipzig',         2015, 'Großstadt',   145_000, 'umzug'),
 ('Altbauwohnung München',            2000, 'München',     180_000, 'aus'),
 ('Eigentumswohnung Berlin',          2018, 'Großstadt',   310_000, 'umzug'),
 ('Einfamilienhaus Münchner Umland',  2010, 'München',     420_000, 'aus'),
 ('Vermietetes Haus Hamburg',         2012, 'Großstadt',   890_000, 'verm'),
 ('Neubau Brandenburg, Kauf im Hoch', 2022, 'Land',        395_000, 'aus'),
]
print('=' * 96)
print('R15 — POSITION 04b, ENDFASSUNG')
print('=' * 96)
print(f'\n[1] DIE REGEL AN DEN FÄLLEN, Verkauf 2026\n')
print(f'{"Fall":<34}{"Kauf":>6}{"Gewinn":>12}  {"greift":<26}{"Steuer":>9}')
ges = 0.0
for name, kj, reg, preis, art in FAELLE:
    g = preis * faktor(kj, reg) - preis
    if art == 'verm':   st, wie = max(g, 0) * SATZ, 'vermietet: kein Schutz'
    elif art == 'umzug': st, wie = 0.0, 'Umzugsaufschub'
    elif g <= 0:         st, wie = 0.0, 'Verlust, vortragsfähig'
    elif g <= EINMAL:    st, wie = 0.0, 'einmaliger Freibetrag'
    else:                st, wie = (g - EINMAL) * SATZ, 'Rest über 300.000'
    ges += st
    print(f'{name[:33]:<34}{kj:>6}{pm(g):>12}  {wie:<26}{de(st):>9}')
print(f'{"":<34}{"":>6}{"":>12}  {"zusammen":<26}{de(ges):>9}')

print(f'\n[2] AUFKOMMEN, Sensitivität über die beiden offenen Annahmen\n')
UMSATZ, SELBST, KURZ, SATZ_HEUTE, FALL_N = 247.0, 0.50, 0.35, 0.42, 805_000
heute = UMSATZ * KURZ * (1 - SELBST) * 0.25 * SATZ_HEUTE
rng = np.random.default_rng(28)
print(f'    Heutiges Recht: {de(heute,1)} Mrd EUR. Unten das Mehraufkommen von 04b.')
print(f'    Senkrecht der Gewinnanteil am Verkaufspreis, waagerecht der')
print(f'    Anteil der selbstgenutzten Verkäufe, die ein Ausstieg sind.\n')
print(f'{"":>14}' + ''.join(f'{"Ausstieg "+de(a*100)+" %":>16}' for a in (0.30, 0.40, 0.50)))
for ga in (0.15, 0.25, 0.35):
    schnitt = UMSATZ * 1e9 / FALL_N * ga
    st = rng.lognormal(np.log(schnitt) - 0.9**2/2, np.sqrt(0.81), 300_000)
    f = np.maximum(st - EINMAL, 0).sum() / st.sum()
    row = f'{"Gewinn "+de(ga*100)+" %":>14}'
    for a in (0.30, 0.40, 0.50):
        basis = UMSATZ * (1 - SELBST) * ga + UMSATZ * SELBST * ga * a * f
        row += f'{pm(basis * SATZ - heute,1)+" Mrd":>16}'
    print(row)
print(f'''
    Robust positiv über alle neun Kombinationen. Der mittlere Fall
    (Gewinn 25 %, Ausstieg 40 %) ergibt +4,3 Mrd EUR.

    WAS DARAN GESETZT IST: der Gewinnanteil, der Ausstiegsanteil und die
    Streuung der Gewinne je Fall (Lognormal, sigma 0,9). Die Fälle in [1]
    stehen auf der amtlichen Preisreihe, die Aggregate hier nicht. Belastbar
    wären sie nur aus den Kaufpreissammlungen der Gutachterausschüsse.''')
