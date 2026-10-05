# -*- coding: utf-8 -*-
"""SVG-Datenreihe für die Webseite: Dividende je Kopf und Monat, Preise 2028."""
from basis import KOPF_KLUB, D_START, de
A_OHNE_V,B_AUFG,V_ZIEL,QUOTE=6.44,10.35,2.50,30.60
V_START,V_JAHR,I_ALT,I_ZIEL,REST=1.40,2035,1.53,2.50,7.5
G_NOM,PREIS=0.030,0.020; G_REAL=(1+G_NOM)/(1+PREIS)-1
d=D_START; S=[]
for j in range(2028,2061):
    t=j-2028
    v=V_ZIEL if j>=V_JAHR else V_START+(V_ZIEL-V_START)*t/(V_JAHR-2028)
    zd=d*(I_ALT+(I_ZIEL-I_ALT)*min(t/REST,1.0))/100
    div=QUOTE-(A_OHNE_V+v+zd)-B_AUFG
    S.append((j, div/100*KOPF_KLUB*(1+G_REAL)**t/12)); d/=1+G_NOM

X0,X1,Y0,Y1 = 62.0,730.0,268.0,46.0
LO,HI = 400.0, 700.0
def px(j): return X0+(X1-X0)*(j-2028)/32
def py(e): return Y0-(Y0-Y1)*(e-LO)/(HI-LO)
pts=' '.join(f'{px(j):.1f},{py(e):.1f}' for j,e in S)
print('POLY:', pts)
print('AREA:', f'{X0:.1f},{Y0:.1f} ' + pts + f' {X1:.1f},{Y0:.1f}')
print('\nGITTER:')
for g in (400,450,500,550,600,650,700):
    print(f'  <line x1="62" y1="{py(g):.1f}" x2="730" y2="{py(g):.1f}" class="pg"/>'
          f'<text x="52" y="{py(g)+4:.1f}" text-anchor="end" class="pa">{g}</text>')
print('\nMARKEN:')
for j in (2028,2035,2060):
    e=dict(S)[j]
    print(f'  {j}: x={px(j):.1f} y={py(e):.1f} e={de(e,0)}')
print('\nJAHRESACHSE:')
for j in (2028,2035,2040,2050,2060):
    print(f'  <text x="{px(j):.1f}" y="290" text-anchor="middle" class="pa">{j}</text>')
print('\nTITEL-KREISE:')
print(' '.join(f'<circle cx="{px(j):.1f}" cy="{py(e):.1f}" r="9" fill="transparent">'
               f'<title>{j}: {de(e,0)} € je Monat</title></circle>' for j,e in S))
mn=min(S,key=lambda r:r[1])
print(f'\n  Start {de(S[0][1],0)} · Tiefpunkt {de(mn[1],0)} ({mn[0]}) · Ende {de(S[-1][1],0)}')
