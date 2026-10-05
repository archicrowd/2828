# -*- coding: utf-8 -*-
"""Lohnt aktive Tilgung? Und: wie hängt die Dividende am Wachstum?"""
from basis import KOPF_DE, D_START, de
A_OHNE_V, B_AUFG, V_ZIEL, QUOTE = 6.44, 10.35, 2.50, 30.60
V_START, V_JAHR, I_ALT, I_ZIEL, REST = 1.40, 2035, 1.53, 2.50, 7.5

def pfad(tilg=0.0, g_nom=0.030, preis=0.020, jahre=43):
    g_real=(1+g_nom)/(1+preis)-1; d=D_START; out=[]
    for j in range(2028, 2028+jahre):
        t=j-2028
        v  = V_ZIEL if j>=V_JAHR else V_START+(V_ZIEL-V_START)*t/(V_JAHR-2028)
        zd = d*(I_ALT+(I_ZIEL-I_ALT)*min(t/REST,1.0))/100
        tl = tilg if d>tilg else max(d,0.0)
        div= QUOTE-(A_OHNE_V+v+zd)-B_AUFG-tl
        out.append(dict(jahr=j,d=d,div=div,eur=div/100*KOPF_DE*(1+g_real)**t/12))
        d = (d-tl)/(1+g_nom)
    return out

O, M = pfad(0.0), pfad(0.50)
print('='*92); print('AKTIVE TILGUNG VON 0,50 % DES BIP GEGEN NULLTILGUNG'); print('='*92)
print(f'{"Jahr":>6}{"Schuld ohne":>14}{"Schuld mit":>13}{"Div. ohne":>12}{"Div. mit":>11}{"Differenz":>12}')
kum = 0.0; break_even = None
for a,b in zip(O,M):
    kum += b['eur']-a['eur']
    if break_even is None and kum >= 0 and a['jahr']>2029: break_even = a['jahr']
    if a['jahr'] in (2028,2035,2040,2050,2060,2070):
        print(f'{a["jahr"]:>6}{de(a["d"],1)+" %":>14}{de(b["d"],1)+" %":>13}'
              f'{de(a["eur"],0):>12}{de(b["eur"],0):>11}{de(b["eur"]-a["eur"],0):>12}')
print(f'\n  Kumulierte Differenz je Kopf bis 2050   '
      f'{de(sum(b["eur"]-a["eur"] for a,b in zip(O,M) if a["jahr"]<=2050)*12,0)} EUR')
print(f'  bis 2070                               '
      f'{de(sum(b["eur"]-a["eur"] for a,b in zip(O,M))*12,0)} EUR')
print(f'  Break-even der Tilgung                 {break_even if break_even else "nach 2070"}')
print(f'  Dividendenverzicht im Startjahr        {de(O[0]["eur"]-M[0]["eur"],0)} EUR im Monat')

print(f'\n{"="*92}\nWORAN DIE DIVIDENDE HÄNGT\n{"="*92}')
print(f'  Der Anteil fällt von {de(O[0]["div"],2)} % auf {de(O[32]["div"],2)} % des BIP,')
print(f'  also um {de((O[32]["div"]/O[0]["div"]-1)*100,1)} % in 32 Jahren. Alles Weitere ist Wachstum:')
print(f'\n{"reales Wachstum je Kopf":<28}{"2035":>10}{"2060":>10}{"gegen 2028":>13}')
for g in (0.000, 0.005, 0.010, 0.015, 0.020):
    Q = pfad(0.0, g_nom=(1+g)*1.02-1, preis=0.020)
    print(f'  {de(g*100,1)+" %":<26}{de(Q[7]["eur"],0):>10}{de(Q[32]["eur"],0):>10}'
          f'{de((Q[32]["eur"]/Q[0]["eur"]-1)*100,0)+" %":>13}')
print(f'\n  Die Kaufkraft der Dividende folgt dem realen Wachstum je Kopf,')
print(f'  vermindert um {de(-(O[32]["div"]/O[0]["div"]-1)*100,1)} % Anteilsverlust. Das ist die ganze Aussage —')
print(f'  jede Eurozahl darüber hinaus ist eine Wachstumsannahme, keine Rechnung.')
