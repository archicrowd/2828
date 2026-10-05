# -*- coding: utf-8 -*-
"""Territorialer Aufschlag, saubere Herleitung.

A übernimmt den Zinsdienst des Altbestands. Finanziert wird er aus A's Anteil,
also mit einem EINHEITLICHEN Satz auf das jeweilige BIP. Was ein Gebiet
einzahlt, folgt deshalb seinem BIP; was A für es auszahlt, folgt seiner Schuld.
Die Differenz ist der Transfer, und der Aufschlag hebt ihn auf.
"""
from basis import GDP, POP, SCHULD, BIP28_KLUB, de
I_ALT, D_START, F = 1.53, 78.4, 1.13535
satz = D_START*I_ALT/100                     # % des BIP, den A für Zinsen braucht

print('='*98); print('TERRITORIALER AUFSCHLAG'); print('='*98)
print(f'  Einheitlicher Finanzierungssatz: {de(satz,4)} % des BIP'
      f'  = {de(satz/100*BIP28_KLUB,0)} Mrd EUR klubweit\n')
print(f'{"":>4}{"BIP je Kopf":>13}{"Schuld":>9}{"Zins für":>11}{"zahlt ein":>11}'
      f'{"Aufschlag":>12}{"in % von A":>12}')
R=[]
for k in GDP:
    bip28 = GDP[k]/1000*F
    kopf  = bip28*1e9/POP[k]
    aus   = SCHULD[k]/100*bip28*I_ALT/100*1e9/POP[k]   # EUR je Kopf, Zinsdienst
    ein   = satz/100*kopf                              # EUR je Kopf, Beitrag
    R.append((k, kopf, SCHULD[k], aus, ein, aus-ein))
R.sort(key=lambda r:-r[5])
A_KOPF = 9.04/100*BIP28_KLUB*1e9/sum(POP.values())
for k,kopf,s,aus,ein,auf in R:
    print(f'  {k:>2}{de(kopf,0):>13}{de(s,1)+" %":>9}{de(aus,0):>11}{de(ein,0):>11}'
          f'{("+" if auf>0 else "")+de(auf,0):>12}{de(auf/A_KOPF*100,1)+" %":>12}')
print(f'\n  Spanne  {("+" if R[0][5]>0 else "")}{de(R[0][5],0)} EUR ({R[0][0]})'
      f' bis {de(R[-1][5],0)} EUR ({R[-1][0]}) je Kopf und Jahr')
print(f'  Probe, Summe über alle Gebiete: '
      f'{de(sum(r[5]*POP[r[0]] for r in R)/1e9,4)} Mrd EUR — null, wie gefordert')
print(f'  A behält je Kopf {de(A_KOPF,0)} EUR; der größte Aufschlag sind'
      f' {de(max(abs(r[5]) for r in R)/A_KOPF*100,1)} % davon')
print(f'''
  Warum Irland am stärksten entlastet wird, obwohl seine Schuldenquote niedrig
  ist: Sein BIP je Kopf liegt beim {de(max(r[1] for r in R)/(BIP28_KLUB*1e9/sum(POP.values())),2)}-Fachen des Klubschnitts, weil
  Konzerne dort buchen. Es zahlt deshalb in den gemeinsamen Zinstopf weit mehr
  ein als sein eigener Altbestand kostet. Der Aufschlag gibt das zurück. Das
  ist kein Entgegenkommen, sondern die Folge der Bemessung am BIP.

  Über dreißig Jahre schmilzt der Aufschlag linear ab: im ersten Jahr voll,
  im fünfzehnten zur Hälfte, im einunddreißigsten null.''')
