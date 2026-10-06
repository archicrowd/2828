# -*- coding: utf-8 -*-
"""Der vollständige korrigierte Zahlensatz für das Gesamtdokument."""
from basis import GDP, POP, BIP28_DE, BIP28_KLUB, KOPF_DE, KOPF_KLUB, D_START, de
import json

A_POSTEN=[('Wirtschaftsraum, Agrar, Energie, Netze',3.75),
          ('Verteidigung und digitale Souveränität',2.50),('Grundlagenforschung',0.77),
          ('Hochschulen',0.74),('Außenbeziehungen',0.30),
          ('Bildungs-, Markt- und Produktstandards',0.30),('Übergeordnete Polizei',0.29),
          ('Umwelt, grenzüberschreitend',0.29)]
B_POSTEN=[('Schulen',3.70),('Kommunalverwaltung',1.62),('Nahverkehr, Ortsstraßen',1.48),
          ('Kultur, Sport, Gemeinschaft',1.22),('Ordnung, Feuerwehr, Rettung',1.05),
          ('Wohnen, Gemeinwesen',0.71),('Wasser, Abwasser, Abfall',0.57)]
A_SUM, B_AUFG = round(sum(v for _,v in A_POSTEN),2), round(sum(v for _,v in B_POSTEN),2)
V_ZIEL, A_OHNE_V = 2.50, round(A_SUM-2.50,2)
QUOTE, BODEN, KIND_ANT, SCHULE = 30.60, 0.82, 0.1586, 3.70
V_START, V_JAHR, I_ALT, I_ZIEL, REST = 1.40, 2035, 1.53, 2.50, 7.5
G_NOM, PREIS = 0.030, 0.020; G_REAL=(1+G_NOM)/(1+PREIS)-1

def pfad(quote=QUOTE, jahre=33):
    d=D_START; out=[]
    for j in range(2028,2028+jahre):
        t=j-2028
        v = V_ZIEL if j>=V_JAHR else V_START+(V_ZIEL-V_START)*t/(V_JAHR-2028)
        zd= d*(I_ALT+(I_ZIEL-I_ALT)*min(t/REST,1.0))/100
        a = A_OHNE_V+v+zd; div=quote-a-B_AUFG
        out.append(dict(jahr=j,v=v,d=d,zd=zd,a=a,div=div,
            kl=div/100*KOPF_KLUB*(1+G_REAL)**t/12, dde=div/100*KOPF_DE*(1+G_REAL)**t/12))
        d/=1+G_NOM
    return out
P=pfad(); r0=P[0]; mx=max(P,key=lambda r:r['a'])
Z=dict(
 bip24=sum(GDP.values())/1000, bip28_klub=BIP28_KLUB, bip28_de=BIP28_DE,
 pop=sum(POP.values()), kopf_klub=KOPF_KLUB, kopf_de=KOPF_DE,
 a_sum=A_SUM, b_aufg=B_AUFG, quote=QUOTE, boden=BODEN,
 a_2028=r0['a'], b_2028=QUOTE-r0['a'], div_2028=r0['div'],
 a_max=mx['a'], a_max_jahr=mx['jahr'], deckel=mx['a']/(QUOTE-BODEN)*100,
 je_einw=(B_AUFG-SCHULE)/100*KOPF_KLUB, je_kind=SCHULE/100*KOPF_KLUB/KIND_ANT,
 schuld_abs=D_START/100*BIP28_KLUB,
 a_anteil_schuld=r0['a']/D_START*100, deckel_anteil=0.36*(QUOTE-BODEN)/D_START*100,
 entlastung_pkt=40.76-38.35, entlastung_mrd=(40.76-38.35)/100*BIP28_KLUB,
 verw_ersparnis=(1.62-B_AUFG*0.058)/100*KOPF_KLUB/12,
)
def e(pct): return pct/100*KOPF_KLUB
print('='*96); print('KORRIGIERTER ZAHLENSATZ — GESAMTKONZEPT'); print('='*96)
print(f'\n  Klub 2028 {de(BIP28_KLUB,0)} Mrd EUR · {de(sum(POP.values())/1e6,1)} Mio Menschen'
      f' · {de(KOPF_KLUB,0)} EUR je Kopf')
print(f'  Deutschland 2028 {de(BIP28_DE,1)} Mrd EUR · {de(KOPF_DE,0)} EUR je Kopf'
      f' · Verhältnis {de(KOPF_DE/KOPF_KLUB,4)}')
print(f'\n  EINZUG UND TEILUNG 2028        % BIP     EUR je Kopf')
for n,p in (('Gesamtaufkommen',QUOTE),('   davon zieht A ein',QUOTE-BODEN),
            ('   davon erhebt B selbst',BODEN),('A behält',r0['a']),
            ('B verfügt',QUOTE-r0['a']),('   B Fachaufgaben',B_AUFG),
            ('   B Dividende',r0['div'])):
    print(f'  {n:<30}{de(p,2):>6}  {de(e(p),0):>12}')
print(f'\n  Obergrenze A: Höchstbedarf {de(mx["a"],2)} % im Jahr {mx["jahr"]}'
      f' = {de(Z["deckel"],1)} % des Einzugs -> vertraglich 36 %')
print(f'  Formel: {de(Z["je_einw"],0)} EUR je Einwohner · {de(Z["je_kind"],0)} EUR je Kind (5-19)')
print(f'  Bodenabgabe {de(e(BODEN),0)} EUR je Kopf = {de(BODEN/(QUOTE-r0["a"])*100,1)} %'
      f' des kommunalen Haushalts')
print(f'  Verwaltungsersparnis auf estnischem Niveau: {de(Z["verw_ersparnis"],0)} EUR im Monat')
print(f'\n  AUFGABEN IN MRD EUR')
for t,ps,s in (('A',A_POSTEN,A_SUM),('B',B_POSTEN,B_AUFG)):
    print(f'    Ebene {t}: ' + ' · '.join(f'{de(v/100*BIP28_KLUB,0)}' for _,v in ps)
          + f'  Summe {de(s/100*BIP28_KLUB,0)} Mrd')
print(f'\n  ZEITPFAD (EUR in Preisen von 2028, reales Wachstum je Kopf {de(G_REAL*100,1)} %)')
print(f'{"Jahr":>8}{"Verteid.":>10}{"Schuld":>9}{"Zins":>8}{"A":>8}{"Div. %":>9}'
      f'{"Klub EUR":>10}{"DE EUR":>9}')
for r in P:
    if r['jahr'] in (2028,2030,2035,2040,2050,2060):
        print(f'{r["jahr"]:>8}{de(r["v"],2):>10}{de(r["d"],1):>9}{de(r["zd"],2):>8}'
              f'{de(r["a"],2):>8}{de(r["div"],2):>9}{de(r["kl"],0):>10}{de(r["dde"],0):>9}')
print(f'\n  SCHULDEN  Stand {de(D_START,1)} % = {de(Z["schuld_abs"],0)} Mrd EUR')
print(f'  A-Einnahmen deckungsfähig: {de(Z["a_anteil_schuld"],1)} % des Bestands,'
      f' an der Obergrenze {de(Z["deckel_anteil"],1)} %')
print(f'\n  LAST  Entlastung {de(Z["entlastung_pkt"],2)} Punkte = {de(Z["entlastung_mrd"],0)} Mrd EUR')
json.dump({k:(round(v,4) if isinstance(v,float) else v) for k,v in Z.items()},
          open('/home/claude/modell/zahlen.json','w'), indent=1, ensure_ascii=False)
json.dump([{k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items()} for r in P],
          open('/home/claude/modell/pfad.json','w'), indent=1)
print('\n  -> zahlen.json, pfad.json geschrieben')
