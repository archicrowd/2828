# -*- coding: utf-8 -*-
"""
OECD Country-by-Country Reporting, Tabelle I — Auswertung
Datensatz: OECD.CTP.TPS:DSD_CBCR@DF_CBCRI (1.1), anonymisiert und aggregiert.

Das Skript ist so geschrieben, dass es unverändert läuft, sobald die Datei
mehrere Sitzstaaten enthält (REF_AREA). Bei nur einem Sitzstaat wird dessen
Auswertung gezeigt, bei mehreren zusätzlich die Summe über alle.

MESSGRÖSSEN
  UPR            Umsatz mit fremden Dritten          -> Näherung für den Ort der Kundschaft
  RPR            Umsatz mit verbundenen Unternehmen
  TOT_REV        Gesamtumsatz
  PROFIT         Gewinn vor Steuern
  TAX_ACCRUED    zurückgestellte Ertragsteuer        -> effektiver Satz
  TAX_PAID       gezahlte Ertragsteuer (Kassenbasis)
  EMPLOYEES      Beschäftigte
  ENTITIES_COUNT Zahl der Einheiten
  ETR (P5..P95)  Verteilungspunkte des effektiven Satzes je Partnerland

ZUR VORSICHT
  - Werte in USD. Negative Gewinne einzelner Länder sind in den Summen enthalten.
  - Doppelzählung: Beteiligungserträge zwischen Konzerngesellschaften können den
    Gewinn aufblähen; die OECD weist ausdrücklich darauf hin.
  - Die Zerlegung nach Drittumsatz ist eine Einfaktor-Rechnung und unterstellt,
    dass der Drittumsatz dort gebucht wird, wo die Kundschaft sitzt.
"""
import sys, pandas as pd, numpy as np

PFAD = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/oecd/cbcr1.csv'

KLUB = {'DEU':'Deutschland','FRA':'Frankreich','ESP':'Spanien','NLD':'Niederlande',
        'IRL':'Irland','BEL':'Belgien','AUT':'Österreich','DNK':'Dänemark',
        'SVN':'Slowenien','EST':'Estland'}
OASEN = {'LUX':'Luxemburg','MLT':'Malta','CHE':'Schweiz','SGP':'Singapur',
         'HKG':'Hongkong','BMU':'Bermuda','CYM':'Kaimaninseln','JEY':'Jersey',
         'BHS':'Bahamas','PAN':'Panama','ARE':'Ver.Arab.Emirate','CYP':'Zypern',
         'IMN':'Isle of Man','GGY':'Guernsey','VGB':'Brit. Jungferninseln',
         'BRB':'Barbados','MUS':'Mauritius','LIE':'Liechtenstein'}
# Sammelposten der OECD (A_O = Afrika übrige usw.) aus Länderrechnungen heraushalten
SAMMEL = {'A_O','E_O','F_O','S_O','O_O','C_O','N_O','_T','W_O','STA','WXD','_X'}
NAME = lambda c: KLUB.get(c) or OASEN.get(c) or c

d = pd.read_csv(PFAD)
d = d.loc[:, [c for c in d.columns if not c.startswith('Unnamed')]]

breit = (d[d.STATISTICAL_OPERATION == '_Z']
         .pivot_table(index=['REF_AREA', 'COUNTERPART_AREA', 'TIME_PERIOD'],
                      columns='MEASURE', values='OBS_VALUE', aggfunc='sum')
         .reset_index())
etr = (d[d.MEASURE == 'ETR']
       .pivot_table(index=['REF_AREA', 'COUNTERPART_AREA', 'TIME_PERIOD'],
                    columns='STATISTICAL_OPERATION', values='OBS_VALUE', aggfunc='first')
       .reset_index())

sitz = sorted(breit.REF_AREA.unique())
jahre = sorted(breit.TIME_PERIOD.unique())
print('=' * 100)
print('OECD CbCR, Tabelle I — Auswertung')
print('=' * 100)
print(f'Sitzstaaten in der Datei: {len(sitz)}  {sitz if len(sitz) <= 12 else "(…)"}')
print(f'Jahre: {jahre} | Partnerländer: {breit.COUNTERPART_AREA.nunique()} | Zeilen: {len(breit)}')
if len(sitz) == 1:
    print(f'\n!! Die Datei enthält nur EINEN Sitzstaat ({sitz[0]}).')
    print('   Für die Frage nach Position 05 werden alle Sitzstaaten gebraucht,')
    print('   insbesondere USA, Deutschland, Frankreich, Niederlande, Irland.')

k = breit[~breit.COUNTERPART_AREA.isin(SAMMEL)].copy()
MRD = 1e9

# ---------------------------------------------------------------- [1] Überblick
print(f'\n[1] ÜBERBLICK  (Sitzstaat {", ".join(sitz)}, {jahre[0]})')
print(f'  Gesamtumsatz        {k.TOT_REV.sum()/MRD:>12,.1f} Mrd USD')
print(f'  davon mit Dritten   {k.UPR.sum()/MRD:>12,.1f} Mrd USD  ({k.UPR.sum()/k.TOT_REV.sum()*100:.0f} %)')
print(f'  Gewinn vor Steuern  {k.PROFIT.sum()/MRD:>12,.1f} Mrd USD')
print(f'  Steuer zurückgest.  {k.TAX_ACCRUED.sum()/MRD:>12,.1f} Mrd USD'
      f'   -> effektiv {k.TAX_ACCRUED.sum()/k.PROFIT.sum()*100:.1f} %')
print(f'  Beschäftigte        {k.EMPLOYEES.sum()/1e6:>12,.2f} Mio')

# ------------------------------------------- [2] Gewinn je Kopf, effektiver Satz
k['satz'] = k.TAX_ACCRUED / k.PROFIT.where(k.PROFIT > 0) * 100
k['je_kopf'] = k.PROFIT / k.EMPLOYEES.replace(0, np.nan)
k['marge'] = k.PROFIT / k.TOT_REV.replace(0, np.nan) * 100
k['name'] = k.COUNTERPART_AREA.map(NAME)

gross = k[(k.PROFIT > 0.5 * MRD)].sort_values('je_kopf', ascending=False)
print('\n[2] GEWINN JE BESCHÄFTIGTER PERSON — Partnerländer mit über 0,5 Mrd USD Gewinn')
print(f'{"Partnerland":<24}{"Gewinn Mrd":>12}{"je Kopf USD":>14}{"eff. Satz %":>13}'
      f'{"Marge %":>10}{"Beschäftigte":>14}')
for _, r in gross.head(18).iterrows():
    jk = f'{r.je_kopf:,.0f}' if pd.notna(r.je_kopf) else '–'
    sz = f'{r.satz:.1f}' if pd.notna(r.satz) else '–'
    print(f'{r["name"]:<24}{r.PROFIT/MRD:>12,.1f}{jk:>14}{sz:>13}'
          f'{r.marge:>10,.1f}{r.EMPLOYEES:>14,.0f}')

# ----------------------------------------------- [3] Zerlegung nach Drittumsatz
tot_profit = k.PROFIT.sum()
k['anteil_upr'] = k.UPR / k.UPR.sum()
k['zerlegt'] = k.anteil_upr * tot_profit
k['diff'] = k.zerlegt - k.PROFIT

print('\n[3] ZERLEGUNG DES GEWINNS NACH UMSATZ MIT DRITTEN')
print('    (gesamter Gewinn der Konzerne im Verhältnis der Drittumsätze verteilt)')
print(f'{"Partnerland":<24}{"gebucht Mrd":>13}{"zerlegt Mrd":>13}{"Differenz":>12}{"Drittums. Mrd":>15}')
zeig = pd.concat([k.nlargest(10, 'diff'), k.nsmallest(10, 'diff')]).drop_duplicates('COUNTERPART_AREA')
for _, r in zeig.sort_values('diff', ascending=False).iterrows():
    print(f'{r["name"]:<24}{r.PROFIT/MRD:>13,.1f}{r.zerlegt/MRD:>13,.1f}'
          f'{r["diff"]/MRD:>+12,.1f}{r.UPR/MRD:>15,.1f}')

for titel, codes in [('    Summe der zehn Länderdateien', KLUB), ('    Summe der Niedrigsteuerplätze', OASEN)]:
    t = k[k.COUNTERPART_AREA.isin(codes)]
    if len(t):
        print(f'{titel:<24}{t.PROFIT.sum()/MRD:>13,.1f}{t.zerlegt.sum()/MRD:>13,.1f}'
              f'{t["diff"].sum()/MRD:>+12,.1f}{t.UPR.sum()/MRD:>15,.1f}')

# --------------------------------------------------- [4] Verteilung der Sätze
if len(etr):
    e = etr[~etr.COUNTERPART_AREA.isin(SAMMEL)].copy()
    e['name'] = e.COUNTERPART_AREA.map(NAME)
    e = e.merge(k[['COUNTERPART_AREA', 'PROFIT']], on='COUNTERPART_AREA', how='left')
    e = e[e.PROFIT > 0.5 * MRD].sort_values('P50')
    for c in ('P5','P25','P50','P75','P95'):
        if c in e.columns:
            e[c] = e[c] * 100   # Anteile in Prozent
    print('\n[4] VERTEILUNG DER EFFEKTIVEN SÄTZE JE PARTNERLAND, in %')
    print('    Perzentile über die Konzern-Teilgruppen — unempfindlich gegen einzelne Riesen.')
    print('    Die Quelle liefert Anteile; hier mit 100 multipliziert. Gegenprobe: der')
    print('    aggregierte Satz liegt über dem Median, weil er nach Gewinn gewichtet ist.')
    print(f'{"Partnerland":<24}{"P5":>8}{"P25":>8}{"Median":>9}{"P75":>8}{"P95":>8}')
    for _, r in e.head(16).iterrows():
        f = lambda v: f'{v:,.1f}' if pd.notna(v) else '–'
        print(f'{r["name"]:<24}{f(r.get("P5")):>8}{f(r.get("P25")):>8}'
              f'{f(r.get("P50")):>9}{f(r.get("P75")):>8}{f(r.get("P95")):>8}')

k.to_csv('/home/claude/oecd/oecd-auswertung.csv', index=False)
print('\n-> oecd-auswertung.csv')
