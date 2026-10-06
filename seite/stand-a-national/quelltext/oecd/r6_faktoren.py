# -*- coding: utf-8 -*-
"""
R6 — Robustheitsprüfung von Position 05
OECD CbCR Tabelle I (DSD_CBCR@DF_CBCRI 1.1), Panel '_T', Jahre 2016-2023.

ZWEI VERSCHIEDENE FRAGEN, NICHT EINE BESSERE ANTWORT

  Einfaktor (Drittumsatz)   = Besteuerung am Ort der Kundschaft.
                              Das ist Position 05.
  Dreifaktor (Umsatz,       = Formelhafte Aufteilung nach dem Muster der
  Beschäftigte, Sachanlagen)  EU-Richtlinienentwürfe (CCCTB/BEFIT).
                              Das ist eine ANDERE Reform.

  Der Vergleich sagt deshalb nicht, welche Zahl stimmt, sondern wie viel
  des Ergebnisses an der Wahl des Schlüssels hängt. Bleibt die Richtung
  gleich, ist der Befund robust. Dreht sie, ist Position 05 eine
  Entwurfsentscheidung mit Verteilungsfolgen - und das muss auf die Seite.

METHODE
  Je Sitzstaat (REF_AREA) wird der Gewinn aller dort ansässigen Konzerne
  auf die Tätigkeitsländer verteilt:
      Anteil_j = w1*UPR_j/SUM(UPR) + w2*EMP_j/SUM(EMP) + w3*AST_j/SUM(AST)
  Summiert wird je Sitzstaat getrennt, dann über alle Sitzstaaten addiert.
  Doppelzählung entsteht nicht, weil jeder Konzern genau einmal von seinem
  Sitzstaat gemeldet wird.

GRENZEN
  - Die Zusammenfassung aller Konzerne eines Sitzstaats zu einer Einheit
    ist eine Näherung. Firmengenau wäre besser, dafür reicht die
    öffentliche Datenlage nicht (siehe v0.3).
  - Fehlt ein Faktor für eine Zelle, wird er für diese Zelle nicht
    gewichtet; die Abdeckung je Sitzstaat wird ausgewiesen.
  - Sachanlagen sind ohne Zahlungsmittel definiert, Beschäftigte sind
    Köpfe, nicht Lohnsumme. Die Richtlinienentwürfe nehmen für den
    Arbeitsfaktor halb Köpfe, halb Lohnsumme; Lohnsummen gibt es hier nicht.
  - Werte in USD. Verluste sind in den Summen enthalten.
"""
import pandas as pd, numpy as np

F = '/mnt/user-data/uploads/OECD_CTP_TPS_DSD_CBCR_DF_CBCRI_1_1_complete_2026-10-01_07-07-01.csv'
MRD, USD_EUR, SATZ = 1e9, 0.8611, 0.28
SAMMEL = {'A','E','F','S','W','A_O','E_O','F_O','S_O','W_O','WXD','ANT_F','_T','_Z'}
KLUB = {'DEU':'Deutschland','FRA':'Frankreich','ESP':'Spanien','NLD':'Niederlande',
        'IRL':'Irland','BEL':'Belgien','AUT':'Österreich','DNK':'Dänemark',
        'SVN':'Slowenien','EST':'Estland'}
OASEN = {'LUX':'Luxemburg','MLT':'Malta','CHE':'Schweiz','SGP':'Singapur','HKG':'Hongkong',
         'BMU':'Bermuda','CYM':'Kaimaninseln','JEY':'Jersey','BHS':'Bahamas','PAN':'Panama',
         'ARE':'Ver.Arab.Emirate','CYP':'Zypern','IMN':'Isle of Man','GGY':'Guernsey',
         'VGB':'Brit. Jungferninseln','BRB':'Barbados','MUS':'Mauritius','LIE':'Liechtenstein',
         'MAC':'Macau','CUW':'Curaçao','AIA':'Anguilla','TCA':'Turks- und Caicosinseln'}
STLS = 'STLS'
NAME = lambda c: KLUB.get(c) or OASEN.get(c) or ('staatenlos' if c == STLS else c)

print('=' * 100)
print('R6 — EINFAKTOR GEGEN DREIFAKTOR, UND DIE ZEITREIHE')
print('=' * 100)

d = pd.read_csv(F, usecols=['REF_AREA','COUNTERPART_AREA','MEASURE','STATISTICAL_OPERATION',
                            'AGGREGATION_TYPE','PROFIT_GROUPING','TIME_PERIOD','OBS_VALUE'],
                low_memory=False)
d = d[(d.AGGREGATION_TYPE == 'TOTAL') & (d.PROFIT_GROUPING == '_T') &
      (d.STATISTICAL_OPERATION == '_Z') &
      (d.MEASURE.isin(['PROFIT','UPR','EMPLOYEES','ASSETS','TAX_ACCRUED']))]
w = d.pivot_table(index=['TIME_PERIOD','REF_AREA','COUNTERPART_AREA'], columns='MEASURE',
                  values='OBS_VALUE', aggfunc='first').reset_index()
w = w[~w.COUNTERPART_AREA.isin(SAMMEL)]
for c in ['PROFIT','UPR','EMPLOYEES','ASSETS','TAX_ACCRUED']:
    if c not in w:
        w[c] = np.nan

# ------------------------------------------------------ Abdeckung der Faktoren
print('\n[0] ABDECKUNG DER DREI FAKTOREN, Jahr 2023')
j = w[w.TIME_PERIOD == 2023]
for f in ['UPR','EMPLOYEES','ASSETS']:
    mask = j[f].notna() & (j[f] != 0)
    print(f'  {f:<11} belegt in {mask.sum():>6,} von {len(j):>6,} Zellen '
          f'= {mask.mean()*100:>4.1f} %   '
          f'Summe {j.loc[mask, f].sum()/ (MRD if f!="EMPLOYEES" else 1e6):>12,.0f} '
          f'{"Mrd USD" if f!="EMPLOYEES" else "Mio Köpfe"}')

def zerlege(t, gewichte):
    """gewichte: dict Faktor -> Gewicht. Summiert je Sitzstaat."""
    t = t.copy()
    t['upr_p'] = t.UPR.clip(lower=0)
    t['emp_p'] = t.EMPLOYEES.clip(lower=0)
    t['ast_p'] = t.ASSETS.clip(lower=0)
    anteil = pd.Series(0.0, index=t.index)
    gew_ges = pd.Series(0.0, index=t.index)
    for sp, gw in [('upr_p', gewichte.get('umsatz', 0)),
                   ('emp_p', gewichte.get('beschaeftigte', 0)),
                   ('ast_p', gewichte.get('sachanlagen', 0))]:
        if gw == 0:
            continue
        s = t.groupby('REF_AREA')[sp].transform('sum')
        a = np.where(s > 0, t[sp].fillna(0) / s, np.nan)
        # nur mitwägen, wo der Faktor im Sitzstaat überhaupt vorkommt
        gueltig = pd.notna(a)
        anteil = anteil.add(pd.Series(np.where(gueltig, a * gw, 0), index=t.index))
        gew_ges = gew_ges.add(pd.Series(np.where(gueltig, gw, 0), index=t.index))
    anteil = np.where(gew_ges > 0, anteil / gew_ges, np.nan)   # auf 1 normieren
    t['zerlegt'] = anteil * t.groupby('REF_AREA').PROFIT.transform('sum')
    return t.groupby('COUNTERPART_AREA').agg(gebucht=('PROFIT','sum'),
                                             zerlegt=('zerlegt','sum'))

VARIANTEN = {
    'Einfaktor Umsatz':       dict(umsatz=1),
    'Dreifaktor zu je 1/3':   dict(umsatz=1/3, beschaeftigte=1/3, sachanlagen=1/3),
    'Zweifaktor Umsatz+Besch':dict(umsatz=.5, beschaeftigte=.5),
    'Halb Umsatz, Rest je 1/4':dict(umsatz=.5, beschaeftigte=.25, sachanlagen=.25),
}

# ------------------------------------------------- [1] Varianten für 2023
print('\n[1] DIE ZEHN LÄNDERDATEIEN JE SCHLÜSSEL — Differenz in Mrd EUR, Jahr 2023')
erg = {}
for nm, gw in VARIANTEN.items():
    z = zerlege(j, gw)
    z['diff'] = (z.zerlegt - z.gebucht) * USD_EUR / MRD
    erg[nm] = z['diff']
tab = pd.DataFrame(erg)
kopf = f'{"Land":<16}' + ''.join(f'{n[:17]:>19}' for n in VARIANTEN)
print(kopf)
for c, n in KLUB.items():
    if c in tab.index:
        print(f'{n:<16}' + ''.join(f'{tab.loc[c, k]:>+19,.1f}' for k in VARIANTEN))
kl = tab.loc[[c for c in KLUB if c in tab.index]]
print(f'{"SUMME ZEHN":<16}' + ''.join(f'{kl[k].sum():>+19,.1f}' for k in VARIANTEN))
print(f'{"  bei 28 % Steuer":<16}' + ''.join(f'{kl[k].sum()*SATZ:>+19,.1f}' for k in VARIANTEN))
print('-' * (16 + 19 * len(VARIANTEN)))
for grp, codes in [('Niedrigsteuerplätze', OASEN), ('staatenlos', {STLS: ''})]:
    t = tab.loc[[c for c in codes if c in tab.index]]
    print(f'{grp:<16}' + ''.join(f'{t[k].sum():>+19,.1f}' for k in VARIANTEN))
for c in ['USA','GBR','CHN','JPN']:
    if c in tab.index:
        print(f'{c:<16}' + ''.join(f'{tab.loc[c, k]:>+19,.1f}' for k in VARIANTEN))

print('\n  Vorzeichenwechsel zwischen Einfaktor und Dreifaktor:')
e, dr = tab['Einfaktor Umsatz'], tab['Dreifaktor zu je 1/3']
dreh = tab[(np.sign(e) != np.sign(dr)) & (e.abs() > 1) & (dr.abs() > 1)]
if len(dreh) == 0:
    print('    keiner bei Beträgen über 1 Mrd EUR')
for i, r in dreh.reindex(dreh['Einfaktor Umsatz'].abs().sort_values(ascending=False).index).head(12).iterrows():
    print(f'    {NAME(i):<24}{r["Einfaktor Umsatz"]:>+10,.1f}  ->  {r["Dreifaktor zu je 1/3"]:>+10,.1f}')

# ------------------------------------------------------ [2] Zeitreihe
print('\n[2] ZEITREIHE — Differenz in Mrd EUR, Einfaktor Umsatz')
jahre = sorted(w.TIME_PERIOD.unique())
reihe1, reihe3 = {}, {}
for y in jahre:
    ty = w[w.TIME_PERIOD == y]
    z1 = zerlege(ty, VARIANTEN['Einfaktor Umsatz'])
    z3 = zerlege(ty, VARIANTEN['Dreifaktor zu je 1/3'])
    reihe1[y] = (z1.zerlegt - z1.gebucht) * USD_EUR / MRD
    reihe3[y] = (z3.zerlegt - z3.gebucht) * USD_EUR / MRD
r1, r3 = pd.DataFrame(reihe1), pd.DataFrame(reihe3)

def zeitreihe(df, titel):
    print(f'\n  {titel}')
    print(f'{"Land":<16}' + ''.join(f'{y:>9}' for y in jahre) + f'{"Sitzstaaten":>13}')
    for c, n in KLUB.items():
        if c in df.index:
            print(f'{n:<16}' + ''.join(
                f'{df.loc[c, y]:>+9,.1f}' if pd.notna(df.loc[c, y]) else f'{"–":>9}'
                for y in jahre))
    kl = df.loc[[c for c in KLUB if c in df.index]]
    print(f'{"SUMME ZEHN":<16}' + ''.join(f'{kl[y].sum():>+9,.1f}' for y in jahre))
    for grp, codes in [('Oasen', OASEN), ('staatenlos', {STLS: ''}), ('USA', {'USA': ''})]:
        t = df.loc[[c for c in codes if c in df.index]]
        print(f'{grp:<16}' + ''.join(f'{t[y].sum():>+9,.1f}' for y in jahre))

zeitreihe(r1, 'Einfaktor Umsatz (= Position 05)')
zeitreihe(r3, 'Dreifaktor zu je 1/3 (= Richtlinienmuster)')

print(f'\n  Meldende Sitzstaaten je Jahr:')
for y in jahre:
    sub = w[w.TIME_PERIOD == y]
    print(f'    {y}  {sub.REF_AREA.nunique():>3} Sitzstaaten, '
          f'{sub.COUNTERPART_AREA.nunique():>4} Tätigkeitsländer, '
          f'Gewinn {sub.PROFIT.sum()/MRD:>8,.0f} Mrd USD')

# ----------------------------------------- [3] Deutschland im Zeitverlauf
print('\n[3] DEUTSCHLAND — Mengenwirkung über die Jahre, Mrd EUR bei 28 %')
print(f'{"Jahr":<8}{"Einfaktor":>12}{"Dreifaktor":>12}{"Spanne":>12}')
for y in jahre:
    a, b = r1.loc['DEU', y] * SATZ, r3.loc['DEU', y] * SATZ
    print(f'{y:<8}{a:>+12,.1f}{b:>+12,.1f}{abs(a-b):>12,.1f}')

tab.to_csv('/home/claude/oecd/r6-varianten-2023.csv')
r1.to_csv('/home/claude/oecd/r6-zeitreihe-einfaktor.csv')
r3.to_csv('/home/claude/oecd/r6-zeitreihe-dreifaktor.csv')
print('\n-> r6-varianten-2023.csv, r6-zeitreihe-einfaktor.csv, r6-zeitreihe-dreifaktor.csv')
