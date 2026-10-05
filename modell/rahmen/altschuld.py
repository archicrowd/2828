# -*- coding: utf-8 -*-
"""Territorialer Aufschlag auf A's Anteil — und die Gegenprobe zur Quote 27,91 %."""
from basis import GDP, POP, SCHULD, BIP28_KLUB, KOPF_DE, KOPF_KLUB, D_START, de
A_OHNE_V,B_AUFG,V_ZIEL,QUOTE=6.44,10.35,2.50,30.60
V_START,V_JAHR,I_ALT,I_ZIEL,REST=1.40,2035,1.53,2.50,7.5
G_NOM,PREIS=0.030,0.020; G_REAL=(1+G_NOM)/(1+PREIS)-1
F=1.13535   # Fortschreibung 2024 -> 2028

print('='*94); print('TERRITORIALER AUFSCHLAG — WER TRÄGT WELCHE ALTLAST'); print('='*94)
# Zinsdienst, den A für jedes Gebiet übernimmt, zum einheitlichen Klubzins
zins_klub_pkt = D_START*I_ALT/100                       # % des Klub-BIP, Jahr 2028
print(f'  A übernimmt im Startjahr einen Zinsdienst von {de(zins_klub_pkt,2)} % des Klub-BIP')
print(f'  = {de(zins_klub_pkt/100*BIP28_KLUB,0)} Mrd EUR\n')
print(f'{"":>4}{"Schuld % BIP":>14}{"Zinsdienst":>12}{"je Kopf":>11}'
      f'{"Klubschnitt":>13}{"Aufschlag":>12}')
rows=[]
for k in sorted(GDP, key=lambda x:-SCHULD[x]):
    bip28 = GDP[k]/1000*F
    zins  = SCHULD[k]/100*bip28*I_ALT/100          # Mrd EUR
    jek   = zins*1e9/POP[k]
    schn  = zins_klub_pkt/100*BIP28_KLUB*1e9/sum(POP.values())
    rows.append((k, SCHULD[k], zins, jek, jek-schn))
    print(f'  {k:>2}{de(SCHULD[k],1)+" %":>14}{de(zins,1)+" Mrd":>12}{de(jek,0):>11}'
          f'{de(schn,0):>13}{("+" if jek-schn>0 else "")+de(jek-schn,0):>12}')
print(f'\n  Spanne des Aufschlags: {("+" if rows[0][4]>0 else "")}{de(rows[0][4],0)} EUR'
      f' ({rows[0][0]}) bis {de(rows[-1][4],0)} EUR ({rows[-1][0]}) je Kopf und Jahr')
print(f'  Summe über alle Gebiete (muss null sein): '
      f'{de(sum(r[4]*POP[r[0]] for r in rows)/1e9,3)} Mrd EUR')
print(f'  Das Dokument nennt +364 (FR) bis -1.045 (IE) — hier neu gerechnet.')

print(f'\n{"="*94}\nGEGENPROBE: WAS DIE QUOTE 27,91 % BEDEUTET\n{"="*94}')
def pfad(quote, jahre=33):
    d=D_START; out=[]
    for j in range(2028,2028+jahre):
        t=j-2028
        v = V_ZIEL if j>=V_JAHR else V_START+(V_ZIEL-V_START)*t/(V_JAHR-2028)
        zd= d*(I_ALT+(I_ZIEL-I_ALT)*min(t/REST,1.0))/100
        div=quote-(A_OHNE_V+v+zd)-B_AUFG
        out.append(dict(jahr=j,div=div,dde=div/100*KOPF_DE*(1+G_REAL)**t/12,
                        fix=div/100*KOPF_DE/12))
        d/=1+G_NOM
    return out
for q in (27.91, 30.60, 33.00):
    Q=pfad(q)
    u_real=[r['jahr'] for r in Q if r['dde']<479]
    u_fix =[r['jahr'] for r in Q if r['fix']<479]
    print(f'  Quote {de(q,2)} %   Dividende 2028 {de(Q[0]["div"],2)} % = {de(Q[0]["dde"],0)} EUR')
    print(f'    Jahre unter 479 EUR, in Preisen von 2028      : '
          f'{len(u_real)}' + (f'  ({u_real[0]}–{u_real[-1]})' if u_real else ''))
    print(f'    Jahre unter 479 EUR, ohne reales Wachstum      : '
          f'{len(u_fix)}' + (f'  ({u_fix[0]}–{u_fix[-1]})' if u_fix else ''))
    print(f'    Gesamtlast {de(q+7.75,2)} % des BIP\n')

print(f'{"="*94}\nPROBE DER FORMEL\n{"="*94}')
KIND_ANT,SCHULE=0.1586,3.70
je_e=(B_AUFG-SCHULE)/100*KOPF_KLUB; je_k=SCHULE/100*KOPF_KLUB/KIND_ANT
for name,ant in (('Gemeinde mit 12 % Kindern',0.12),('Klubschnitt',KIND_ANT),
                 ('Gemeinde mit 20 % Kindern',0.20)):
    print(f'  {name:<28}{de(je_e+je_k*ant,0):>8} EUR je Kopf Fachbudget'
          f'   {de((je_e+je_k*ant)/(je_e+je_k*KIND_ANT)*100-100,1):>6} % gegen Schnitt')
print(f'  Spreizung zwischen 12 % und 20 % Kinderanteil: '
      f'{de((je_e+je_k*0.20)/(je_e+je_k*0.12),3)}-fach')
