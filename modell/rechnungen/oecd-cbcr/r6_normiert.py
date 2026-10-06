# -*- coding: utf-8 -*-
"""
R6b — Ist die Schwankung über die Jahre echt?

Die Zahl der meldenden Sitzstaaten wächst von 26 (2016) auf 58 (2023). Absolute
Beträge sind deshalb nicht vergleichbar. Zwei Gegenproben:

  [1] Differenz als Anteil des im Land gebuchten Gewinns — maßstabsfrei.
  [2] Fester Kreis: nur Sitzstaaten, die in ALLEN acht Jahren melden.
      Damit ist die Grundgesamtheit konstant.
"""
import pandas as pd, numpy as np

F = '/mnt/user-data/uploads/OECD_CTP_TPS_DSD_CBCR_DF_CBCRI_1_1_complete_2026-10-01_07-07-01.csv'
MRD, USD_EUR, SATZ = 1e9, 0.8611, 0.28
SAMMEL = {'A','E','F','S','W','A_O','E_O','F_O','S_O','W_O','WXD','ANT_F','_T','_Z'}
KLUB = {'DEU':'Deutschland','FRA':'Frankreich','ESP':'Spanien','NLD':'Niederlande',
        'IRL':'Irland','BEL':'Belgien','AUT':'Österreich','DNK':'Dänemark',
        'SVN':'Slowenien','EST':'Estland'}
OASEN = ['LUX','MLT','CHE','SGP','HKG','BMU','CYM','JEY','BHS','PAN','ARE','CYP',
         'IMN','GGY','VGB','BRB','MUS','LIE','MAC','CUW','AIA','TCA']

d = pd.read_csv(F, usecols=['REF_AREA','COUNTERPART_AREA','MEASURE','STATISTICAL_OPERATION',
                            'AGGREGATION_TYPE','PROFIT_GROUPING','TIME_PERIOD','OBS_VALUE'],
                low_memory=False)
d = d[(d.AGGREGATION_TYPE == 'TOTAL') & (d.PROFIT_GROUPING == '_T') &
      (d.STATISTICAL_OPERATION == '_Z') &
      (d.MEASURE.isin(['PROFIT','UPR','EMPLOYEES','ASSETS']))]
w = d.pivot_table(index=['TIME_PERIOD','REF_AREA','COUNTERPART_AREA'], columns='MEASURE',
                  values='OBS_VALUE', aggfunc='first').reset_index()
w = w[~w.COUNTERPART_AREA.isin(SAMMEL)]
jahre = sorted(w.TIME_PERIOD.unique())

# fester Kreis der Sitzstaaten
je_jahr = w.groupby('TIME_PERIOD').REF_AREA.unique()
fest = set(je_jahr.iloc[0])
for s in je_jahr:
    fest &= set(s)
print('=' * 92)
print('R6b — NORMIERTE GEGENPROBE')
print('=' * 92)
print(f'\nSitzstaaten, die in allen {len(jahre)} Jahren melden: {len(fest)}')
print('  ' + ', '.join(sorted(fest)))

def zerlege(t, gw):
    t = t.copy()
    t['u'] = t.UPR.clip(lower=0); t['e'] = t.EMPLOYEES.clip(lower=0); t['a'] = t.ASSETS.clip(lower=0)
    an = pd.Series(0.0, index=t.index); gg = pd.Series(0.0, index=t.index)
    for sp, g in [('u', gw.get('umsatz',0)), ('e', gw.get('besch',0)), ('a', gw.get('sach',0))]:
        if g == 0: continue
        s = t.groupby('REF_AREA')[sp].transform('sum')
        v = np.where(s > 0, t[sp].fillna(0) / s, np.nan)
        ok = pd.notna(v)
        an = an.add(pd.Series(np.where(ok, v * g, 0), index=t.index))
        gg = gg.add(pd.Series(np.where(ok, g, 0), index=t.index))
    t['zerlegt'] = np.where(gg > 0, an / gg, np.nan) * t.groupby('REF_AREA').PROFIT.transform('sum')
    return t.groupby('COUNTERPART_AREA').agg(gebucht=('PROFIT','sum'), zerlegt=('zerlegt','sum'))

EIN = dict(umsatz=1)
DREI = dict(umsatz=1/3, besch=1/3, sach=1/3)

for titel, filt in [('ALLE MELDENDEN SITZSTAATEN', None), ('FESTER KREIS', fest)]:
    print(f'\n[{titel}]')
    print('  Differenz als Anteil des im Land gebuchten Gewinns, in %  (Einfaktor)')
    print(f'{"Land":<15}' + ''.join(f'{y:>8}' for y in jahre) + f'{"Median":>9}')
    quoten, absolut = {}, {}
    for y in jahre:
        t = w[w.TIME_PERIOD == y]
        if filt:
            t = t[t.REF_AREA.isin(filt)]
        z = zerlege(t, EIN)
        quoten[y] = (z.zerlegt - z.gebucht) / z.gebucht.abs().replace(0, np.nan) * 100
        absolut[y] = (z.zerlegt - z.gebucht) * USD_EUR / MRD
    q, ab = pd.DataFrame(quoten), pd.DataFrame(absolut)
    for c, n in KLUB.items():
        if c in q.index:
            print(f'{n:<15}' + ''.join(
                f'{q.loc[c,y]:>+8,.0f}' if pd.notna(q.loc[c,y]) else f'{"–":>8}' for y in jahre)
                + f'{q.loc[c].median():>+9,.0f}')
    print(f'\n  Mengenwirkung bei 28 %, Mrd EUR  (Einfaktor | Dreifaktor)')
    print(f'{"Jahr":<8}{"DEU ein":>10}{"DEU drei":>10}{"Zehn ein":>11}{"Zehn drei":>11}'
          f'{"Oasen ein":>12}{"Oasen drei":>12}')
    zeilen = []
    for y in jahre:
        t = w[w.TIME_PERIOD == y]
        if filt:
            t = t[t.REF_AREA.isin(filt)]
        z1, z3 = zerlege(t, EIN), zerlege(t, DREI)
        f1 = (z1.zerlegt - z1.gebucht) * USD_EUR / MRD * SATZ
        f3 = (z3.zerlegt - z3.gebucht) * USD_EUR / MRD * SATZ
        kl = [c for c in KLUB if c in f1.index]
        oa = [c for c in OASEN if c in f1.index]
        row = dict(jahr=y, de_ein=f1.get('DEU', np.nan), de_drei=f3.get('DEU', np.nan),
                   zehn_ein=f1[kl].sum(), zehn_drei=f3[kl].sum(),
                   oasen_ein=f1[oa].sum(), oasen_drei=f3[oa].sum())
        zeilen.append(row)
        print(f'{y:<8}{row["de_ein"]:>+10,.1f}{row["de_drei"]:>+10,.1f}'
              f'{row["zehn_ein"]:>+11,.1f}{row["zehn_drei"]:>+11,.1f}'
              f'{row["oasen_ein"]:>+12,.1f}{row["oasen_drei"]:>+12,.1f}')
    r = pd.DataFrame(zeilen)
    print(f'{"Median":<8}{r.de_ein.median():>+10,.1f}{r.de_drei.median():>+10,.1f}'
          f'{r.zehn_ein.median():>+11,.1f}{r.zehn_drei.median():>+11,.1f}'
          f'{r.oasen_ein.median():>+12,.1f}{r.oasen_drei.median():>+12,.1f}')
    print(f'{"Spanne":<8}{r.de_ein.min():>+10,.1f}{r.de_drei.min():>+10,.1f}'
          f'{r.zehn_ein.min():>+11,.1f}{r.zehn_drei.min():>+11,.1f}'
          f'{r.oasen_ein.min():>+12,.1f}{r.oasen_drei.min():>+12,.1f}')
    print(f'{"":<8}{r.de_ein.max():>+10,.1f}{r.de_drei.max():>+10,.1f}'
          f'{r.zehn_ein.max():>+11,.1f}{r.zehn_drei.max():>+11,.1f}'
          f'{r.oasen_ein.max():>+12,.1f}{r.oasen_drei.max():>+12,.1f}')
    if filt:
        r.to_csv('/home/claude/oecd/r6-fester-kreis.csv', index=False)

# ------------------------- Produktionsländer: wer verliert bei reiner Zielortsteuer
print('\n[PRODUKTIONSLÄNDER] 2023, Mrd EUR Differenz')
t = w[w.TIME_PERIOD == 2023]
z1, z3 = zerlege(t, EIN), zerlege(t, DREI)
v = pd.DataFrame({'einfaktor': (z1.zerlegt - z1.gebucht) * USD_EUR / MRD,
                  'dreifaktor': (z3.zerlegt - z3.gebucht) * USD_EUR / MRD})
v['wandel'] = v.dreifaktor - v.einfaktor
print('  Grösste Gewinner durch Hinzunahme von Beschäftigten und Sachanlagen:')
for i, r in v.nlargest(12, 'wandel').iterrows():
    print(f'    {i:<6}{r.einfaktor:>+10,.1f} -> {r.dreifaktor:>+10,.1f}   Wandel {r.wandel:>+9,.1f}')
print('  Grösste Verlierer:')
for i, r in v.nsmallest(8, 'wandel').iterrows():
    print(f'    {i:<6}{r.einfaktor:>+10,.1f} -> {r.dreifaktor:>+10,.1f}   Wandel {r.wandel:>+9,.1f}')
v.to_csv('/home/claude/oecd/r6-produktionslaender.csv')
print('\n-> r6-fester-kreis.csv, r6-produktionslaender.csv')
