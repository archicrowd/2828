# -*- coding: utf-8 -*-
"""Der Zeitpfad in Anteilen, in Preisen von 2028 und nominal — und was daraus folgt."""
from basis import POP, BIP28_DE, BIP28_KLUB, KOPF_DE, KOPF_KLUB, D_START, de

A_SUM, B_AUFG, V_ZIEL = 8.94, 10.35, 2.50
A_OHNE_V = round(A_SUM - V_ZIEL, 2)
QUOTE, BODEN, KIND_ANT, SCHULE = 30.60, 0.82, 0.1586, 3.70
G_NOM, PREIS = 0.030, 0.020          # nominales Wachstum, Preissteigerung
G_REAL = (1+G_NOM)/(1+PREIS)-1       # reales Wachstum je Kopf, Bevölkerung konstant
V_START, V_JAHR, I_ALT, I_ZIEL, REST = 1.40, 2035, 1.53, 2.50, 7.5
VERSPRECHEN = 479.0

def pfad(quote=QUOTE, g_nom=G_NOM, preis=PREIS, v_ziel=V_ZIEL, jahre=33):
    g_real=(1+g_nom)/(1+preis)-1; d=D_START; out=[]
    for j in range(2028, 2028+jahre):
        t = j-2028
        v  = v_ziel if j>=V_JAHR else V_START+(v_ziel-V_START)*t/(V_JAHR-2028)
        zd = d*(I_ALT+(I_ZIEL-I_ALT)*min(t/REST,1.0))/100
        a  = A_OHNE_V+v+zd; div = quote-a-B_AUFG
        out.append(dict(jahr=j, v=v, d=d, zd=zd, a=a, div=div,
            de_fix =div/100*KOPF_DE/12,                      # ohne reales Wachstum
            de_real=div/100*KOPF_DE*(1+g_real)**t/12,        # Preise 2028
            de_nom =div/100*KOPF_DE*(1+g_nom)**t/12,         # laufende Preise
            kl_real=div/100*KOPF_KLUB*(1+g_real)**t/12))
        d /= 1+g_nom
    return out

P = pfad()
print('='*98); print('ZEITPFAD — DREI LESARTEN DESSELBEN ANTEILS'); print('='*98)
print(f'  nominal {de(G_NOM*100,1)} %, Preise {de(PREIS*100,1)} %, real je Kopf '
      f'{de(G_REAL*100,2)} %, Bevölkerung konstant\n')
print(f'{"Jahr":>6}{"Verteid.":>10}{"Schuld":>9}{"Zins":>8}{"A":>8}{"Dividende":>11}'
      f'{"DE ohne Wachst.":>17}{"DE Preise 2028":>16}{"DE nominal":>12}')
for r in P:
    if r['jahr'] in (2028,2030,2035,2040,2050,2060):
        print(f'{r["jahr"]:>6}{de(r["v"],2)+" %":>10}{de(r["d"],1)+" %":>9}'
              f'{de(r["zd"],2)+" %":>8}{de(r["a"],2)+" %":>8}{de(r["div"],2)+" %":>11}'
              f'{de(r["de_fix"],0):>17}{de(r["de_real"],0):>16}{de(r["de_nom"],0):>12}')
print(f'\n  Das Dokument nennt in dieser Spalte 550 / 561 / 589 / 695 / 967 / 1.333 —')
print(f'  das ist die nominale Reihe, ohne sie als nominal zu kennzeichnen.')

for et, key in (('ohne reales Wachstum','de_fix'), ('in Preisen von 2028','de_real')):
    mn = min(P, key=lambda r:r[key]); en = P[-1]
    print(f'\n  {et}:')
    print(f'    Tiefpunkt {de(mn[key],0)} EUR im Jahr {mn["jahr"]}'
          f'  ({de((mn[key]/P[0][key]-1)*100,1)} % gegen 2028)')
    print(f'    2060      {de(en[key],0)} EUR'
          f'  ({de((en[key]/P[0][key]-1)*100,1)} % gegen 2028)')

# ---- Die Quote neu abgeleitet -------------------------------------------
print(f'\n{"="*98}\nABLEITUNG DER QUOTE\n{"="*98}')
for et, key in (('ohne reales Wachstum (streng)','de_fix'),
                ('in Preisen von 2028 (zentral)','de_real')):
    lo, hi = 25.0, 40.0
    for _ in range(90):
        m=(lo+hi)/2
        if min(r[key] for r in pfad(m)) < VERSPRECHEN: lo=m
        else: hi=m
    print(f'  Versprechen {de(VERSPRECHEN,0)} EUR hält jedes Jahr, {et:<32}'
          f'ab Quote {de((lo+hi)/2,2)} %')
print(f'\n  Gewählt: {de(QUOTE,2)} %. Das ist die strenge Ableitung — das Versprechen')
print(f'  hält auch dann, wenn die Wirtschaft real nicht wächst. Bei {de(G_REAL*100,1)} %')
print(f'  realem Wachstum liegt der Tiefpunkt {de((min(r["de_real"] for r in P)/VERSPRECHEN-1)*100,0)} % über dem Versprechen.')

# ---- Empfindlichkeiten ---------------------------------------------------
print(f'\n{"="*98}\nEMPFINDLICHKEIT\n{"="*98}')
print(f'{"Fall":<46}{"Div. 2028":>11}{"Tiefpunkt":>11}{"Jahr":>7}{"2060":>9}')
faelle = [('Zentralfall', dict()),
          ('nominales Wachstum nur 1,5 %', dict(g_nom=0.015)),
          ('Preise 3 % statt 2 %', dict(preis=0.030)),
          ('Verteidigung 3,5 % statt 2,5 %', dict(v_ziel=3.50)),
          ('Verteidigung 2,0 % (COFOG-vergleichbar)', dict(v_ziel=2.00))]
for et, kw in faelle:
    Q = pfad(**kw); mn = min(Q, key=lambda r:r['de_real'])
    print(f'  {et:<44}{de(Q[0]["de_real"],0):>11}{de(mn["de_real"],0):>11}'
          f'{mn["jahr"]:>7}{de(Q[-1]["de_real"],0):>9}')
print(f'\n  Der Zielwert der Verteidigung ist der empfindlichste Parameter:')
print(f'  ein Punkt des BIP sind {de(1.0/100*KOPF_DE/12,0)} EUR Dividende im Monat.')
