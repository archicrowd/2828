# -*- coding: utf-8 -*-
"""Zeitpfad und alle Eurobeträge auf der korrigierten Basis 2028."""
from basis import (GDP, POP, BIP28_DE, BIP28_KLUB, KOPF_DE, KOPF_KLUB,
                   D_START, de)

# ---- Aufgabenstruktur, % des BIP ---------------------------------------
A_POSTEN = [('Wirtschaftsraum, Agrar, Energie, Netze',3.75),
            ('Verteidigung und digitale Souveränität',2.50),
            ('Grundlagenforschung',0.77),('Hochschulen',0.74),
            ('Außenbeziehungen',0.30),('Bildungs-, Markt- und Produktstandards',0.30),
            ('Übergeordnete Polizei',0.29),('Umwelt, grenzüberschreitend',0.29)]
B_POSTEN = [('Schulen',3.70),('Kommunalverwaltung',1.62),
            ('Nahverkehr, Ortsstraßen',1.48),('Kultur, Sport, Gemeinschaft',1.22),
            ('Ordnung, Feuerwehr, Rettung',1.05),('Wohnen, Gemeinwesen',0.71),
            ('Wasser, Abwasser, Abfall',0.57)]
A_SUM   = round(sum(v for _,v in A_POSTEN),2)
B_AUFG  = round(sum(v for _,v in B_POSTEN),2)
V_ZIEL  = 2.50
A_OHNE_V= round(A_SUM - V_ZIEL,2)

QUOTE   = 30.60          # Steuerquote, % des BIP
BODEN   = 0.82           # davon erhebt B selbst
KIND_ANT= 0.1586         # Anteil der 5- bis 19-Jährigen
SCHULE  = 3.70
VERSPRECHEN = 479.0      # EUR/Monat je Kopf Deutschland, bisheriger Projektstand

# ---- Zeitpfad -----------------------------------------------------------
G_NOM, V_START, V_JAHR = 0.030, 1.40, 2035
I_ALT, I_ZIEL, REST    = 1.53, 2.50, 7.5

def verteidigung(j):
    return V_ZIEL if j >= V_JAHR else V_START+(V_ZIEL-V_START)*(j-2028)/(V_JAHR-2028)
def zins_eff(j):
    return I_ALT + (I_ZIEL-I_ALT)*min((j-2028)/REST, 1.0)
def pfad(quote=QUOTE, jahre=33):
    d, out = D_START, []
    for j in range(2028, 2028+jahre):
        v, zd = verteidigung(j), d*zins_eff(j)/100
        a   = A_OHNE_V + v + zd
        div = quote - a - B_AUFG
        out.append(dict(jahr=j, v=v, d=d, zd=zd, a=a, div=div,
                        klub=div/100*KOPF_KLUB/12, dde=div/100*KOPF_DE/12))
        d /= 1+G_NOM
    return out

P = pfad()
print('='*94); print('ZEITPFAD — KORRIGIERTE BASIS'); print('='*94)
print(f'  A ohne Verteidigung {de(A_OHNE_V,2)} %   B Fachaufgaben {de(B_AUFG,2)} %   '
      f'Quote {de(QUOTE,2)} %')
print(f'\n{"Jahr":>6}{"Verteidig.":>12}{"Schuld":>10}{"Zinsdienst":>12}'
      f'{"A gesamt":>11}{"Dividende":>12}{"Klub EUR/M":>13}{"DE EUR/M":>11}')
for r in P:
    if r['jahr'] in (2028,2030,2035,2040,2050,2060):
        print(f'{r["jahr"]:>6}{de(r["v"],2)+" %":>12}{de(r["d"],1)+" %":>10}'
              f'{de(r["zd"],2)+" %":>12}{de(r["a"],2)+" %":>11}{de(r["div"],2)+" %":>12}'
              f'{de(r["klub"],0):>13}{de(r["dde"],0):>11}')
mx = max(P, key=lambda r:r['a']); mn = min(P, key=lambda r:r['div'])
print(f'\n  Höchstbedarf A      {de(mx["a"],2)} % im Jahr {mx["jahr"]}')
print(f'  Obergrenze A        {de(mx["a"]/(QUOTE-BODEN)*100,1)} % des Einzugs  -> '
      f'vertraglich {de(round(mx["a"]/(QUOTE-BODEN)*100+0.8,0),0)} %')
print(f'  Tiefste Dividende   {de(mn["div"],2)} % im Jahr {mn["jahr"]}  = '
      f'{de(mn["dde"],0)} EUR/Monat Deutschland  (Versprechen {de(VERSPRECHEN,0)})')

# ---- Ableitung der Quote ------------------------------------------------
lo, hi = 25.0, 40.0
for _ in range(80):
    m = (lo+hi)/2
    if min(r['dde'] for r in pfad(m)) < VERSPRECHEN: lo = m
    else: hi = m
print(f'  Abgeleitete Mindestquote, damit das Versprechen jedes Jahr hält: '
      f'{de((lo+hi)/2,3)} %')

# ---- Eurobeträge 2028 ---------------------------------------------------
r0 = P[0]
print(f'\n{"="*94}\nEUROBETRÄGE 2028 — ALT GEGEN KORRIGIERT\n{"="*94}')
ALT_KOPF = 14227e9/sum(POP.values())
def zeile(name, pct, alt):
    neu = pct/100*KOPF_KLUB
    print(f'  {name:<40}{de(pct,2)+" %":>9}{de(alt,0):>11}{de(neu,0):>11}'
          f'{de(neu-alt,0):>9}')
print(f'  {"":<40}{"% BIP":>9}{"Dokument":>11}{"korrigiert":>11}{"Diff":>9}')
zeile('Gesamtaufkommen je Kopf', QUOTE, 17068)
zeile('   davon zieht A ein', QUOTE-BODEN, 16611)
zeile('   davon erhebt B selbst (Bodenabgabe)', BODEN, 457)
zeile('A behält 2028', r0['a'], 5042)
zeile('B verfügt 2028', QUOTE-r0['a'], 12026)
zeile('   B Fachaufgaben', B_AUFG, 5773)
zeile('   B Dividende', r0['div'], 6253)
print()
je_einw = (B_AUFG-SCHULE)/100*KOPF_KLUB
je_kind = SCHULE/100*KOPF_KLUB/KIND_ANT
print(f'  Formel je Einwohner   {de((B_AUFG-SCHULE),2)} %  Dokument 3.710 -> '
      f'korrigiert {de(je_einw,0)} EUR')
print(f'  Formel je Kind        {de(SCHULE,2)} % / {de(KIND_ANT*100,2)} %  '
      f'Dokument 13.011 -> korrigiert {de(je_kind,0)} EUR')
probe = je_einw + je_kind*KIND_ANT
print(f'  Probe: je Einwohner + {de(KIND_ANT*100,2)} % x je Kind = {de(probe,0)} EUR'
      f'  gegen Fachaufgaben {de(B_AUFG/100*KOPF_KLUB,0)} EUR')

# ---- Aufgabentabellen in Mrd EUR ---------------------------------------
print(f'\n{"="*94}\nAUFGABEN IN MRD EUR, KLUB 2028 ({de(BIP28_KLUB,0)} Mrd)\n{"="*94}')
for titel, posten, summe in (('Ebene A — der Klub', A_POSTEN, A_SUM),
                             ('Ebene B — die Kommunen', B_POSTEN, B_AUFG)):
    print(f'\n  {titel}')
    for n, v in posten:
        print(f'    {n:<44}{de(v,2)+" %":>9}{de(v/100*BIP28_KLUB,0):>9} Mrd')
    print(f'    {"Summe":<44}{de(summe,2)+" %":>9}{de(summe/100*BIP28_KLUB,0):>9} Mrd')

# ---- Verwaltungsersparnis ---------------------------------------------
VERW_B = dict(A_POSTEN+B_POSTEN)['Kommunalverwaltung']
anteil_de, anteil_ee = VERW_B/B_AUFG*100, 5.8
verw_ee = B_AUFG*anteil_ee/100
print(f'\n{"="*94}\nVERWALTUNGSERSPARNIS\n{"="*94}')
print(f'  Kommunalverwaltung im Klub            {de(VERW_B,2)} % des BIP '
      f'= {de(anteil_de,1)} % des B-Haushalts')
print(f'  estnisches Niveau {de(anteil_ee,1)} % des Haushalts   {de(verw_ee,2)} % des BIP')
print(f'  Ersparnis                             {de(VERW_B-verw_ee,2)} Punkte')
print(f'  je Kopf und Monat   Dokument 48 EUR -> korrigiert '
      f'{de((VERW_B-verw_ee)/100*KOPF_KLUB/12,0)} EUR')

# ---- Schuldendeckung ---------------------------------------------------
print(f'\n{"="*94}\nSCHULDEN UND KLUBGARANTIE\n{"="*94}')
print(f'  Schuldenstand 2028                    {de(D_START,1)} % des BIP = '
      f'{de(D_START/100*BIP28_KLUB,0)} Mrd EUR')
print(f'  A-Einnahmen 2028 {de(r0["a"],2)} % -> {de(r0["a"]/D_START*100,1)} % des Schuldenstands')
print(f'  an der Obergrenze 36 % des Einzugs    '
      f'{de(0.36*(QUOTE-BODEN),2)} % -> {de(0.36*(QUOTE-BODEN)/D_START*100,1)} %')
print(f'  Dokument nennt 14,2 % — das ist der Wert an der Obergrenze, nicht 2028.')
