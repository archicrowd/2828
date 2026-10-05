# -*- coding: utf-8 -*-
"""Rekonstruktion der Zahlengrundlage und Probe gegen das Gesamtdokument."""

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# ---- Eurostat 2024, zehn Klubstaaten -------------------------------------
GDP = {'DE':4328970.0,'FR':2935236.2,'ES':1594330.0,'NL':1115252.0,'IE':561940.5,
       'BE':619914.3,'AT':494087.6,'DK':400267.4,'SI':67418.1,'EE':39883.0}  # Mio EUR
POP = {'DE':83516593,'FR':68775952,'ES':48797875,'NL':17942942,'IE':5380300,
       'BE':11796841,'AT':9158750,'DK':5961249,'SI':2123949,'EE':1369285}
# gov_10dd_edpt1: Schuldenquote % BIP; irt_lt_mcby_a: Rendite 10J %
SCHULD = {'DE':62.2,'FR':112.6,'ES':101.6,'NL':43.8,'IE':38.3,
          'BE':103.9,'AT':80.0,'DK':30.5,'SI':66.4,'EE':23.5}
RENDITE= {'DE':2.32,'FR':2.97,'ES':3.15,'NL':2.62,'IE':2.72,
          'BE':2.92,'AT':2.84,'DK':2.30,'SI':3.11,'EE':3.55}

BIP24_KLUB = sum(GDP.values())/1000.0          # Mrd EUR
POP_KLUB   = sum(POP.values())

# ---- Fortschreibung 2024 -> 2028 ----------------------------------------
# Frühjahrsprojektion der Bundesregierung, 22.04.2026: nominal +3,3 / +2,8 / +3,8 %
# 2028 vorsichtig +3,0 %
RATEN = (0.033, 0.028, 0.038, 0.030)
F2428 = 1.0
for r in RATEN: F2428 *= 1+r

BIP28_DE   = GDP['DE']/1000.0 * F2428
BIP28_KLUB = BIP24_KLUB * F2428

print('='*86)
print('BASIS — PROBE DER FORTSCHREIBUNG')
print('='*86)
print(f'  Klub-BIP 2024, Summe der zehn        {de(BIP24_KLUB,1):>12} Mrd EUR')
print(f'  Faktor 2024 -> 2028 ({" / ".join(de(r*100,1)+" %" for r in RATEN)})   {de(F2428,5):>12}')
print(f'  Deutschland 2028                     {de(BIP28_DE,1):>12} Mrd EUR   (Dokument: 4.914,9)')
print(f'  Klub 2028                            {de(BIP28_KLUB,1):>12} Mrd EUR   (Dokument: 14.227)')
print()
print(f'  Der im Dokument genannte Klubwert unterstellt den Faktor '
      f'{de(14227/BIP24_KLUB,5)} —')
print(f'  das ist der Kalibrierungsfaktor der alten Modellbasis (4.200 -> '
      f'{de(4200*14227/BIP24_KLUB/1000,1)}),')
print(f'  nicht die Fortschreibung des Istwerts. Abweichung '
      f'{de((14227/BIP28_KLUB-1)*100,2)} %.')

# ---- Kopfgrößen ---------------------------------------------------------
KOPF_KLUB = BIP28_KLUB*1e9/POP_KLUB
KOPF_DE   = BIP28_DE  *1e9/POP['DE']
print(f'\n  BIP je Kopf 2028, Klub               {de(KOPF_KLUB,0):>12} EUR')
print(f'  BIP je Kopf 2028, Deutschland        {de(KOPF_DE,0):>12} EUR')
print(f'  Verhältnis DE zu Klub                {de(KOPF_DE/KOPF_KLUB,4):>12}')

# ---- Schuldenstand, BIP-gewichtet --------------------------------------
d_abs = sum(GDP[k]*SCHULD[k]/100 for k in GDP)
D_START = d_abs/sum(GDP.values())*100
i_alt_mkt = sum(GDP[k]*SCHULD[k]/100*RENDITE[k] for k in GDP)/d_abs
print(f'\n  Schuldenquote Klub, BIP-gewichtet    {de(D_START,1):>12} %   (Dokument: 78,4)')
print(f'  Streuung                             {de(min(SCHULD.values()),1)} bis {de(max(SCHULD.values()),1)} %'
      f'  Faktor {de(max(SCHULD.values())/min(SCHULD.values()),1)}')
print(f'  Marktrendite, schuldengewichtet      {de(i_alt_mkt,2):>12} %')
