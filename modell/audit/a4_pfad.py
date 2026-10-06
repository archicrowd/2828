# -*- coding: utf-8 -*-
"""
A4 — 04b im Pfad, und was die Kalibrierungsfrage daraus macht

ZWEI ÄNDERUNGEN
  1. Neue Einnahmezeile "Verkaufsgewinn Immobilien 28 %" mit 4,1 Mrd
     (R15 ergab 4,3; abzüglich 4,7 % Kapitalisierungseffekt aus R16).
  2. Das BIP. Das Modell setzt 4.200 Mrd für 2028, amtlich sind es nach
     Fortschreibung rund 4.884. Beide werden gerechnet.
"""
import importlib.util, io, contextlib, math, json
def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1): return ('+' if v >= 0 else '') + de(v, nk)

spec = importlib.util.spec_from_file_location(
    'm2828', '/mnt/user-data/outputs/horizon25-broschure/modell-2828.py')
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)

NEU = dict(co2=33.0, erb=19.32, unt=139.85, verm_b=9.32, pos04b=4.1)
def einnahmen_korr(anteil, sc, detail=False):
    t = m.L / 100
    d = {
     'Einkommensteuer (inkl. steuerpfl. DD)': m.est_aufkommen(anteil, sc['eti']),
     'Kapitalerträge 28 %':                   45*(t/.25)*((1-t)/.75)**sc['eps'],
     'Mehrwertsteuer (Label 5–28 %)':         m.mwst_aufkommen(sc['leak']),
     'Unternehmen & Plattformen 28 %':        NEU['unt']*(t/.25)*math.exp(-sc['semi']*(m.L-25)/100),
     'Erbschaft 28 %':                        NEU['erb']*(t/.25)*math.exp(-(m.L-25)/100),
     'Vermögen-Mindeststeuer (anrechenbar)':  22*(1-0.02*(m.L-25)),
     'CO₂-Abgabe (BEHG-Korridor, netto)':     NEU['co2'],
     'Verkaufsgewinn Immobilien 28 % (04b)':  NEU['pos04b'],
     'Sonstige Steuern':                      165,
    }
    return (sum(d.values()), d) if detail else sum(d.values())
m.einnahmen = einnahmen_korr
m.BAUSTEINE = {'Vermögensteuer 1 % ab 2 Mio.': NEU['verm_b'],
               'Bodenwertabgabe (aufkommensneutral)': 0.0,
               'Abbau klimaschädlicher Subventionen': 20.0}
m.bausteine = lambda t: sum(m.BAUSTEINE.values())

print('=' * 100)
print('A4 — 04b IM PFAD, UND DIE KALIBRIERUNGSFRAGE')
print('=' * 100)
d = m.einnahmen(50, m.SZ['Robust'], detail=True)[1]
print(f'\n[1] EINNAHMEN NACH ALLEN KORREKTUREN, Jahr 1, Robust, DD-Stufe 50 %\n')
for k, v in d.items(): print(f'      {k:<42}{de(v):>9}')
print(f'      {"Bausteine":<42}{de(m.bausteine(0)):>9}')
print(f'      {"-"*51}\n      {"zusammen":<42}{de(sum(d.values())+m.bausteine(0)):>9}')
print(f'      {"Ausgaben":<42}{de(m.ausgaben(50)):>9}')
print(f'      {"SALDO":<42}{pm(sum(d.values())+m.bausteine(0)-m.ausgaben(50)):>9}')

T = json.load(open('/home/claude/haushalt/tarif_neu.json'))
def lauf(bip, tarif, mwst):
    m.BIP0 = bip
    m.TARIF_SAETZE[:] = tarif; m.MWST_STUFEN[:] = mwst
    return {n: m.kennzahlen(m.simuliere(m.SZ[n]))
            for n in ('Optimistisch', 'Robust', 'Stress')}
ALT = ([0,.09,.16,.21,.26,.28], [5,11,17,22,28])
NEUT = (T['est'], T['mwst'])
print(f'''
[2] DER PFAD, VIER KOMBINATIONEN
    "BIP 4.200" ist die Modellannahme, "BIP 4.884" die Fortschreibung der
    amtlichen Zahl (4.469,9 für 2025, 3 % nominal bis 2028).
''')
print(f'{"BIP":>7}{"Tarif":>20}{"Szenario":<14}{"Saldo J1":>10}'
      f'{"Lücken":>8}{"Investquote":>13}{"Fonds Ende":>12}{"60 %":>7}')
for bip in (4200, 4884):
    for nm, (ts, ms) in (('alt 16/21/26', ALT), ('neu 19/24/27', NEUT)):
        k = lauf(bip, ts, ms)
        for szen in ('Robust', 'Stress'):
            kk = k[szen]
            print(f'{de(bip,0):>7}{nm:>20}{szen:<14}{pm(kk["saldo1"]):>10}'
                  f'{kk["luecken"]:>8}{de(kk["invquote"]*100):>12} %'
                  f'{de(kk["fonds_ende"],0):>12}{str(kk["j60"] or "–"):>7}')
print(f'''
[3] WAS DAS BEDEUTET — UND EINE KORREKTUR AN MIR SELBST

    Ich hatte erwartet, dass der Pfad mit dem amtlichen BIP bricht. Er
    bricht nicht. Die Investitionsquote fällt im Robust-Szenario nur von
    99,4 auf 98,1 %, im Stress von 78,2 auf 75,0 %, und die Zahl der
    Lückenjahre bleibt bei null. Der Grund: investiert wird nach Regel 1
    aus dem ÜBERSCHUSS über dem Puffer, nicht bis zum Ziel. Der Überschuss
    ist die bindende Grösse, nicht das Ziel — ein höheres BIP hebt beide
    und hebt sich dabei weitgehend auf.

    DAS IST EIN ERGEBNIS ZUGUNSTEN DES MODELLS. Seine Aussagen hängen
    nicht am Kalibrierungsniveau. Was weiter gilt:
      - die VERHÄLTNISSE sind belastbar: Investitionsquote, Lückenjahre,
        Verteilungswirkung, die Rangfolge der Positionen
      - die ABSOLUTEN EURO-BETRÄGE sind es nicht. Sie liegen auf dem
        Niveau etwa 2021/2022 und dürfen nicht als 2028er Werte gelesen
        werden. Auf der Seite steht das nirgends.
      - 04b bringt 4,1 Mrd und verbessert den Saldo des ersten Jahres von
        −12,8 auf −8,7 Mrd.

    Der nächste Arbeitsschritt bleibt die Kalibrierung auf ein Basisjahr —
    nicht weil der Pfad sonst kippt, sondern weil ein Modell, dessen
    Euro-Beträge um ein Sechstel neben der amtlichen Statistik liegen, von
    Dritten zu Recht nicht verwendet wird.''')
