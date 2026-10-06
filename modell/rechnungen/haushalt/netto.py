# -*- coding: utf-8 -*-
"""
R10c — Korrektur: die Nettoposition konsistent gegen das heutige Recht

DER FEHLER
  In tarif_wahl.py [4] stand die Spalte "netto mit DD" als
      Dividende − (ESt_neu − ESt_2025) − MwSt_mehr
  Die Einkommensteuer war damit gegen den Rechtsstand 2025 gerechnet, die
  Mehrwertsteuer aber gegen den ALTEN 28:28-Effektivsatz von 20,0 %. Der
  Schritt von heute 16,5 % auf 20,0 % fehlte also in der Nettoposition.
  Aufgefallen beim Abgleich mit dem Rechner der Seite, der korrekt gegen
  16,5 % rechnet.

WAS HIER STEHT
  Beide Bezugspunkte getrennt: der Schritt dieser Änderung (20,0 -> 21,5 %)
  und die Gesamtwirkung gegenüber dem heutigen Recht (16,5 -> 21,5 %).
  Die zweite Zahl ist die, die für den Leser zählt.
"""
import json
exec(open('tarif.py').read().split("print('=' * 100)")[0])
T = json.load(open('tarif_neu.json'))
S, ST = T['est'], T['mwst']
R_HEUTE, R_ALT, R_NEU = 0.165, r_eff(MWST_IST), r_eff(ST)

def vat(ein, kq, r_von, r_bis):
    return ein * kq * (r_bis/(1+r_bis) - r_von/(1+r_von))

print('=' * 104)
print('R10c — NETTOPOSITION, KORRIGIERT')
print('=' * 104)
print(f'''
    Mehrwertsteuer-Effektivsatz: heute {de(R_HEUTE*100,1)} % · 28:28 bisher {de(R_ALT*100,1)} % · '''
      f'''jetzt {de(R_NEU*100,1)} %
    Konsumquoten (Setzung nach Muster der EVS): '''
      f'''{" / ".join(de(k*100,0)+" %" for k in KONSUM)}
''')
print(f'{"Markt":>9}{"Dividende":>11}{"ESt heute":>11}{"ESt neu":>10}'
      f'{"ESt mehr":>10}{"MwSt mehr":>11}{"NETTO":>10}{"in % Markt":>12}')
ges = []
for (mio, b), kq in zip(VERT, KONSUM):
    ein = b + DD
    e25, e_neu = est(b, S25, G25), est(ein, S)
    d_vat = vat(ein, kq, R_HEUTE, R_NEU)
    netto = DD - (e_neu - e25) - d_vat
    ges.append((mio, b, netto))
    print(f'{de(b,0):>9}{de(DD,0):>11}{de(e25,0):>11}{de(e_neu,0):>10}'
          f'{pm(e_neu-e25,0):>10}{pm(d_vat,0):>11}{pm(netto,0):>10}'
          f'{pm(netto/b*100,1)+" %":>12}')

sw = sum(m*n for m, b, n in ges)/sum(m for m, b, n in ges)
print(f'''
    Gewichteter Durchschnitt {pm(sw,0)} EUR. Die Nettoposition bleibt stark
    progressiv und kippt zwischen 69.000 und 105.000 EUR Markteinkommen ins
    Minus — bei der früheren, fehlerhaften Rechnung lag der Kipppunkt
    oberhalb von 105.000 EUR. Die Richtung des Befundes ändert sich nicht,
    seine Lage schon.

    ZUM VERGLEICH der Schritt, den NUR diese Tarifänderung ausmacht
    (Mehrwertsteuer {de(R_ALT*100,1)} -> {de(R_NEU*100,1)} %):''')
print(f'\n{"Markt":>9}{"ESt mehr":>11}{"MwSt mehr":>12}{"zusammen":>11}{"in % Markt":>12}')
for (mio, b), kq in zip(VERT, KONSUM):
    ein = b + DD
    d_e = est(ein, S) - est(ein, EST_IST)
    d_v = vat(ein, kq, R_ALT, R_NEU)
    print(f'{de(b,0):>9}{pm(d_e,0):>11}{pm(d_v,0):>12}{pm(d_e+d_v,0):>11}'
          f'{de((d_e+d_v)/ein*100,2)+" %":>12}')
print(f'''
    Das ist die Zusatzlast der Anhebung selbst: {de(min((est(b+DD,S)-est(b+DD,EST_IST)+vat(b+DD,k,R_ALT,R_NEU))/(b+DD)*100 for (m,b),k in zip(VERT,KONSUM)),2)} % bis '''
      f'''{de(max((est(b+DD,S)-est(b+DD,EST_IST)+vat(b+DD,k,R_ALT,R_NEU))/(b+DD)*100 for (m,b),k in zip(VERT,KONSUM)),2)} %
    des Einkommens. Beide Tabellen sind nötig: die erste sagt, was die
    Reform insgesamt bringt, die zweite, was dieser Schritt kostet.''')
