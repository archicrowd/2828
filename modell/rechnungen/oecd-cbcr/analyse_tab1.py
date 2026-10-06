# -*- coding: utf-8 -*-
"""
OECD CbCR Tabelle I (DSD_CBCR@DF_CBCRI, Fassung 1.1) — Auswertung für Position 05
Anonymisierte und aggregierte länderbezogene Berichte, Jahr 2023.

AUFBAU DER DATEN
  REF_AREA          Sitzstaat des Konzerns (63 Jurisdiktionen, einschliesslich USA)
  COUNTERPART_AREA  Jurisdiktion der Tätigkeit (244)
  Jede Konzerngruppe wird genau einmal gemeldet, nämlich von ihrem Sitzstaat.
  Summieren über alle Sitzstaaten ist deshalb keine Doppelzählung.

RECHNUNG
  Je Sitzstaat wird der gesamte Gewinn seiner Konzerne im Verhältnis des
  Umsatzes mit fremden Dritten auf die Tätigkeitsländer verteilt und mit dem
  dort tatsächlich gebuchten Gewinn verglichen. Das bildet eine Besteuerung
  am Ort der Kundschaft nach einem Umsatzschlüssel nach.

GRENZEN
  - Drittumsatz wird dort gebucht, wo die verkaufende Einheit sitzt, nicht
    zwingend dort, wo die Kundschaft sitzt.
  - Einfaktor-Schlüssel. Übliche Vorschläge gewichten Umsatz, Beschäftigte
    und Sachanlagen gemeinsam.
  - Die OECD weist darauf hin, dass konzerninterne Beteiligungserträge den
    gemeldeten Gewinn aufblähen können. PROFIT_ADJ liegt nur für 2021 vor.
  - Verluste sind in den Summen enthalten.
  - Nicht alle Sitzstaaten melden; die Erfassung wächst von Jahr zu Jahr.
"""
import sys, pandas as pd, numpy as np

F = sys.argv[1] if len(sys.argv) > 1 else \
    '/mnt/user-data/uploads/OECD_CTP_TPS_DSD_CBCR_DF_CBCRI_1_1_complete_2026-10-01_07-07-01.csv'
JAHR = 2023
MRD = 1e9

KLUB = {'DEU':'Deutschland','FRA':'Frankreich','ESP':'Spanien','NLD':'Niederlande',
        'IRL':'Irland','BEL':'Belgien','AUT':'Österreich','DNK':'Dänemark',
        'SVN':'Slowenien','EST':'Estland'}
OASEN = {'LUX':'Luxemburg','MLT':'Malta','CHE':'Schweiz','SGP':'Singapur','HKG':'Hongkong',
         'BMU':'Bermuda','CYM':'Kaimaninseln','JEY':'Jersey','BHS':'Bahamas','PAN':'Panama',
         'ARE':'Ver.Arab.Emirate','CYP':'Zypern','IMN':'Isle of Man','GGY':'Guernsey',
         'VGB':'Brit. Jungferninseln','BRB':'Barbados','MUS':'Mauritius','LIE':'Liechtenstein',
         'MAC':'Macau','CUW':'Curaçao','AIA':'Anguilla','TCA':'Turks- und Caicosinseln'}
# Sammelposten und Sonderkategorien der OECD
SAMMEL = {'A','E','F','S','W','A_O','E_O','F_O','S_O','W_O','WXD','ANT_F','_T','_Z'}
STATELESS = 'STLS'
NAME = lambda c: KLUB.get(c) or OASEN.get(c) or ('staatenlos' if c == STATELESS else c)

d = pd.read_csv(F, usecols=['REF_AREA','COUNTERPART_AREA','MEASURE','STATISTICAL_OPERATION',
                            'AGGREGATION_TYPE','PROFIT_GROUPING','TIME_PERIOD','OBS_VALUE'],
                low_memory=False)
d = d[(d.TIME_PERIOD == JAHR) & (d.AGGREGATION_TYPE == 'TOTAL') &
      (d.PROFIT_GROUPING == '_T') & (d.STATISTICAL_OPERATION == '_Z')]

w = d.pivot_table(index=['REF_AREA','COUNTERPART_AREA'], columns='MEASURE',
                  values='OBS_VALUE', aggfunc='first').reset_index()
w = w[~w.COUNTERPART_AREA.isin(SAMMEL)]
for c in ['PROFIT','UPR','TOT_REV','TAX_ACCRUED','TAX_PAID','EMPLOYEES','ENTITIES_COUNT']:
    if c not in w:
        w[c] = np.nan

print('=' * 104)
print(f'OECD CbCR, Tabelle I — Jahr {JAHR}')
print('=' * 104)
print(f'Sitzstaaten: {w.REF_AREA.nunique()} | Tätigkeitsländer: {w.COUNTERPART_AREA.nunique()}'
      f' | Beobachtungen: {len(w):,}'.replace(',', '.'))
print(f'Gewinn weltweit {w.PROFIT.sum()/MRD:,.0f} Mrd USD | '
      f'Drittumsatz {w.UPR.sum()/MRD:,.0f} Mrd | '
      f'Steuer {w.TAX_ACCRUED.sum()/MRD:,.0f} Mrd | '
      f'Beschäftigte {w.EMPLOYEES.sum()/1e6:,.0f} Mio')

# --------------------------------------------- [1] Weltbild je Tätigkeitsland
g = w.groupby('COUNTERPART_AREA').agg(
    profit=('PROFIT','sum'), upr=('UPR','sum'), rev=('TOT_REV','sum'),
    tax=('TAX_ACCRUED','sum'), emp=('EMPLOYEES','sum'), ent=('ENTITIES_COUNT','sum'),
    sitze=('REF_AREA','nunique'))
g['satz'] = g.tax / g.profit.where(g.profit > 0) * 100
g['je_kopf'] = g.profit / g.emp.replace(0, np.nan)
g['name'] = [NAME(i) for i in g.index]

print(f'\n[1] GEWINN JE BESCHÄFTIGTER PERSON UND EFFEKTIVER SATZ')
print('    Tätigkeitsländer mit mindestens 20 Mrd USD Gewinn, nach Gewinn je Kopf')
print(f'{"Tätigkeitsland":<24}{"Gewinn Mrd":>12}{"je Kopf USD":>14}{"eff. Satz %":>13}'
      f'{"Beschäftigte Mio":>18}{"Sitzstaaten":>12}')
t = g[g.profit > 20 * MRD].sort_values('je_kopf', ascending=False)
for i, r in t.head(20).iterrows():
    jk = f'{r.je_kopf:,.0f}' if pd.notna(r.je_kopf) else '–'
    sz = f'{r.satz:.1f}' if pd.notna(r.satz) else '–'
    print(f'{r["name"]:<24}{r.profit/MRD:>12,.0f}{jk:>14}{sz:>13}'
          f'{r.emp/1e6:>18,.2f}{int(r.sitze):>12}')
print('    …')
for i, r in t.tail(6).iterrows():
    jk = f'{r.je_kopf:,.0f}' if pd.notna(r.je_kopf) else '–'
    sz = f'{r.satz:.1f}' if pd.notna(r.satz) else '–'
    print(f'{r["name"]:<24}{r.profit/MRD:>12,.0f}{jk:>14}{sz:>13}'
          f'{r.emp/1e6:>18,.2f}{int(r.sitze):>12}')

# ------------------------------------- [2] Zerlegung nach Drittumsatz je Sitzstaat
w['upr_pos'] = w.UPR.clip(lower=0)
sum_upr = w.groupby('REF_AREA').upr_pos.transform('sum')
sum_pro = w.groupby('REF_AREA').PROFIT.transform('sum')
w['zerlegt'] = np.where(sum_upr > 0, w.upr_pos / sum_upr * sum_pro, np.nan)

z = w.groupby('COUNTERPART_AREA').agg(gebucht=('PROFIT','sum'),
                                      zerlegt=('zerlegt','sum'),
                                      upr=('UPR','sum'))
z['diff'] = z.zerlegt - z.gebucht
z['name'] = [NAME(i) for i in z.index]
z['steuer28'] = z['diff'] * 0.28

print(f'\n[2] ZERLEGUNG DES GEWINNS NACH UMSATZ MIT DRITTEN')
print(f'{"Tätigkeitsland":<24}{"gebucht Mrd":>13}{"zerlegt Mrd":>13}{"Differenz":>12}'
      f'{"bei 28 % Mrd":>14}{"Drittums. Mrd":>15}')
print('  Grösste Zuflüsse:')
for i, r in z.nlargest(12, 'diff').iterrows():
    print(f'  {r["name"]:<22}{r.gebucht/MRD:>13,.0f}{r.zerlegt/MRD:>13,.0f}'
          f'{r["diff"]/MRD:>+12,.0f}{r.steuer28/MRD:>+14,.0f}{r.upr/MRD:>15,.0f}')
print('  Grösste Abflüsse:')
for i, r in z.nsmallest(12, 'diff').iterrows():
    print(f'  {r["name"]:<22}{r.gebucht/MRD:>13,.0f}{r.zerlegt/MRD:>13,.0f}'
          f'{r["diff"]/MRD:>+12,.0f}{r.steuer28/MRD:>+14,.0f}{r.upr/MRD:>15,.0f}')

print('\n[3] DIE ZEHN LÄNDERDATEIEN')
print(f'{"Land":<22}{"gebucht Mrd":>13}{"zerlegt Mrd":>13}{"Differenz":>12}'
      f'{"bei 28 % Mrd":>14}{"eff. Satz %":>13}')
for c, nm in KLUB.items():
    if c in z.index:
        r, q = z.loc[c], g.loc[c] if c in g.index else None
        sz = f'{q.satz:.1f}' if q is not None and pd.notna(q.satz) else '–'
        print(f'{nm:<22}{r.gebucht/MRD:>13,.1f}{r.zerlegt/MRD:>13,.1f}'
              f'{r["diff"]/MRD:>+12,.1f}{r.steuer28/MRD:>+14,.1f}{sz:>13}')
kl = z.loc[[c for c in KLUB if c in z.index]]
print(f'{"Summe der zehn":<22}{kl.gebucht.sum()/MRD:>13,.1f}{kl.zerlegt.sum()/MRD:>13,.1f}'
      f'{kl["diff"].sum()/MRD:>+12,.1f}{kl.steuer28.sum()/MRD:>+14,.1f}')
oa = z.loc[[c for c in OASEN if c in z.index]]
print(f'{"Summe Niedrigsteuerpl.":<22}{oa.gebucht.sum()/MRD:>13,.1f}{oa.zerlegt.sum()/MRD:>13,.1f}'
      f'{oa["diff"].sum()/MRD:>+12,.1f}{oa.steuer28.sum()/MRD:>+14,.1f}')
if STATELESS in z.index:
    r = z.loc[STATELESS]
    print(f'{"staatenlose Einheiten":<22}{r.gebucht/MRD:>13,.1f}{r.zerlegt/MRD:>13,.1f}'
          f'{r["diff"]/MRD:>+12,.1f}{r.steuer28/MRD:>+14,.1f}')

# ------------------------------------------------------ [4] Robustheit
print('\n[4] ROBUSTHEIT — wie viele Sitzstaaten tragen das Ergebnis?')
print(f'{"Tätigkeitsland":<22}{"Differenz Mrd":>15}{"Sitzstaaten":>13}{"3 grösste in %":>17}')
for c in list(KLUB) + ['LUX','IRL','CHE','SGP','BMU','HKG','NLD']:
    if c not in z.index:
        continue
    t = w[w.COUNTERPART_AREA == c].copy()
    t['dz'] = t.zerlegt - t.PROFIT
    t = t.dropna(subset=['dz'])
    if len(t) == 0 or abs(t.dz.sum()) < 1e6:
        continue
    top3 = t.dz.abs().nlargest(3).sum() / abs(t.dz.sum()) * 100
    print(f'{NAME(c):<22}{t.dz.sum()/MRD:>+15,.1f}{len(t):>13}{top3:>16,.0f} %')

g.to_csv('/home/claude/oecd/t1-laender.csv')
z.to_csv('/home/claude/oecd/t1-zerlegung.csv')
print('\n-> t1-laender.csv, t1-zerlegung.csv')
