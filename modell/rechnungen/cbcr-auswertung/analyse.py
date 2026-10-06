# -*- coding: utf-8 -*-
"""
POSITION 05 — Besteuerung am Ort der Kunden, erste Datenprüfung
Quelle: Aliprandi, G., Borders, K., Gabriel, F., von Zedlitz, G. (2022):
Public Country-by-Country Reports: a new database. EU Tax Observatory.
Datenstand 2026-09-19. Lizenz CC BY-NC-ND 4.0, nicht kommerzielle Nutzung.
Die Datenbank selbst wird nicht weitergegeben, nur diese Auswertung.

FRAGE
  Wie weit fällt auseinander, wo Konzerngewinn gebucht wird und wo die
  Umsätze mit fremden Dritten entstehen? Letzteres ist der beste verfügbare
  Näherungswert für den Ort der Kundschaft.

METHODE
  Einfaktor-Zerlegung nach Umsatz mit Dritten (unrelated revenues).
  Je Konzern und Jahr wird der weltweite Gewinn im Verhältnis der
  Drittumsätze auf die Jurisdiktionen verteilt und mit dem tatsächlich
  gebuchten Gewinn verglichen.

GRENZEN — bitte mitlesen
  - Nur Konzerne, die länderbezogen berichten und dabei Drittumsätze UND
    Gewinn für JEDE Jurisdiktion ausweisen. Das ist eine Auswahl, keine
    Zufallsstichprobe, und sie umfasst keine Digitalkonzerne mit Sitz in
    den USA, soweit diese nicht veröffentlichen.
  - Drittumsatz wird dort gebucht, wo die verkaufende Einheit sitzt. Das
    ist nicht zwingend das Land der Kundschaft.
  - Einfaktor-Zerlegung nach Umsatz ist eine Entwurfsentscheidung. Übliche
    Vorschläge gewichten Umsatz, Beschäftigte und Sachanlagen gemeinsam.
  - Verluste werden bei der Verteilung nicht gesondert behandelt.
"""
import pandas as pd, numpy as np

KLUB = {'DEU': 'Deutschland', 'FRA': 'Frankreich', 'ESP': 'Spanien',
        'NLD': 'Niederlande', 'IRL': 'Irland', 'BEL': 'Belgien',
        'AUT': 'Österreich', 'DNK': 'Dänemark', 'SVN': 'Slowenien',
        'EST': 'Estland'}
OASEN = {'LUX': 'Luxemburg', 'MLT': 'Malta', 'CHE': 'Schweiz',
         'SGP': 'Singapur', 'HKG': 'Hongkong', 'BMU': 'Bermuda',
         'CYM': 'Kaimaninseln', 'JEY': 'Jersey', 'BHS': 'Bahamas',
         'PAN': 'Panama', 'ARE': 'Ver. Arab. Emirate', 'CYP': 'Zypern'}

d = pd.read_csv('/home/claude/cbcr/taxplorer.csv')

# Drittumsatz rekonstruieren, wo er sich aus Gesamt minus verbunden ergibt
d['unrel'] = d.unrelated_revenues
m = d.unrel.isna() & d.total_revenues.notna() & d.related_revenues.notna()
d.loc[m, 'unrel'] = d.loc[m, 'total_revenues'] - d.loc[m, 'related_revenues']

print('=' * 92)
print('POSITION 05 — gebuchter Gewinn gegen Umsatz mit Dritten')
print('=' * 92)

# ---------------------------------------------------------------- [1] Stichprobe
JAHRE = [2023, 2024]
s = d[d.year.isin(JAHRE)].copy()
voll = s.groupby(['company', 'year']).apply(
    lambda g: g.unrel.notna().all() and g.profit_before_tax.notna().all(),
    include_groups=False)
paare = voll[voll].index
s = s.set_index(['company', 'year']).loc[s.set_index(['company', 'year']).index.isin(paare)].reset_index()

print(f'\n[1] STICHPROBE  Jahre {JAHRE[0]} und {JAHRE[1]}')
print(f'  Konzern-Jahre mit lückenloser Angabe: {len(paare)}')
print(f'  Einzelne Konzerne: {s.company.nunique()} | Zeilen: {len(s)}')
print(f'  Drittumsatz insgesamt: {s.unrel.sum()/1e9:,.0f} Mrd | '
      f'Gewinn vor Steuern: {s.profit_before_tax.sum()/1e9:,.0f} Mrd')
print('\n  Sitzländer der Konzerne in der Stichprobe:')
for k, v in s.drop_duplicates(['company', 'year']).hq_country.value_counts().head(12).items():
    print(f'    {k:<22}{v:>4}')

# ---------------------------------------------- [2] Zerlegung nach Drittumsatz
g = s.groupby(['company', 'year'])
s['anteil_umsatz'] = s.unrel / g.unrel.transform('sum')
s['gewinn_welt'] = g.profit_before_tax.transform('sum')
s['gewinn_zerlegt'] = s.anteil_umsatz * s.gewinn_welt

agg = s.groupby('jur_code').agg(
    gebucht=('profit_before_tax', 'sum'),
    zerlegt=('gewinn_zerlegt', 'sum'),
    umsatz=('unrel', 'sum'),
    steuer=('tax_accrued', 'sum'),
    beschaeftigte=('employees', 'sum'),
    konzerne=('company', 'nunique'))
agg['diff'] = agg.zerlegt - agg.gebucht
agg['name'] = [KLUB.get(i) or OASEN.get(i) or i for i in agg.index]

def block(titel, codes):
    print(f'\n{titel}')
    print(f'{"Land":<20}{"gebucht Mrd":>13}{"zerlegt Mrd":>13}{"Differenz":>12}'
          f'{"Drittums. Mrd":>15}{"Konzerne":>10}')
    t = agg.loc[[c for c in codes if c in agg.index]].sort_values('umsatz', ascending=False)
    for i, r in t.iterrows():
        print(f'{r["name"]:<20}{r.gebucht/1e9:>13,.1f}{r.zerlegt/1e9:>13,.1f}'
              f'{r["diff"]/1e9:>+12,.1f}{r.umsatz/1e9:>15,.1f}{int(r.konzerne):>10}')
    print(f'{"Summe":<20}{t.gebucht.sum()/1e9:>13,.1f}{t.zerlegt.sum()/1e9:>13,.1f}'
          f'{t["diff"].sum()/1e9:>+12,.1f}{t.umsatz.sum()/1e9:>15,.1f}')
    return t

print('\n[2] ZEHN LÄNDERDATEIEN')
k = block('', list(KLUB))
print('\n[3] BEKANNTE NIEDRIGSTEUERPLÄTZE')
o = block('', list(OASEN))

# ----------------------------------------------------- [4] Aufkommenswirkung
print('\n[4] ÜBERSCHLAG DER AUFKOMMENSWIRKUNG BEI 28 %')
for code in ['DEU'] + [c for c in KLUB if c != 'DEU']:
    if code in agg.index:
        r = agg.loc[code]
        print(f'  {r["name"]:<16} Differenz {r["diff"]/1e9:>+8,.1f} Mrd '
              f'-> bei 28 %: {r["diff"]*0.28/1e9:>+7,.2f} Mrd Steuer '
              f'(Stichprobe, {int(r.konzerne)} Konzerne)')

# --------------------------------- [5] Effektive Sätze, breitere Stichprobe
print('\n[5] EFFEKTIVE STEUERSÄTZE — breitere Stichprobe')
print('    (alle Zeilen mit Gewinn > 0 und ausgewiesener Steuer, Jahre 2023-2025)')
b = d[(d.year.between(2023, 2025)) & (d.profit_before_tax > 0) & d.tax_accrued.notna()]
eff = b.groupby('jur_code').agg(gewinn=('profit_before_tax', 'sum'),
                                steuer=('tax_accrued', 'sum'),
                                besch=('employees', 'sum'),
                                n=('company', 'nunique'))
eff = eff[eff.n >= 5]
eff['satz'] = eff.steuer / eff.gewinn * 100
eff['gewinn_je_kopf'] = eff.gewinn / eff.besch.replace(0, np.nan) / 1000
eff['name'] = [KLUB.get(i) or OASEN.get(i) or i for i in eff.index]

print(f'\n{"Land":<20}{"Gewinn Mrd":>12}{"eff. Satz %":>13}{"Gewinn je Kopf Tsd":>21}{"Konzerne":>10}')
for code in list(KLUB) + list(OASEN):
    if code in eff.index:
        r = eff.loc[code]
        gk = f'{r.gewinn_je_kopf:,.0f}' if pd.notna(r.gewinn_je_kopf) else '–'
        print(f'{r["name"]:<20}{r.gewinn/1e9:>12,.1f}{r.satz:>13.1f}{gk:>21}{int(r.n):>10}')

print('\n  Niedrigste effektive Sätze aller Jurisdiktionen mit mind. 5 Konzernen:')
for i, r in eff.nsmallest(12, 'satz').iterrows():
    print(f'    {r["name"]:<22}{r.satz:>6.1f} %   Gewinn {r.gewinn/1e9:>8,.1f} Mrd   '
          f'{int(r.n):>3} Konzerne')

# --------------------------------------------- [6] Robustheit: Konzentration
print('\n[6] ROBUSTHEIT — wie viele Konzerne tragen das Ergebnis?')
s['diff_zeile'] = s.gewinn_zerlegt - s.profit_before_tax
print(f'{"Land":<16}{"Differenz Mrd":>15}{"Konzerne":>10}{"3 groesste in % der Summe":>28}')
for code in KLUB:
    t = s[s.jur_code == code].groupby('company')['diff_zeile'].sum()
    if len(t) == 0 or abs(t.sum()) < 1e6:
        continue
    anteil = t.abs().sort_values(ascending=False).head(3).sum() / abs(t.sum()) * 100
    print(f'{KLUB[code]:<16}{t.sum()/1e9:>+15,.1f}{len(t):>10}{anteil:>27,.0f} %')
print('  Werte ueber 100 % heissen: einzelne Konzerne bewegen mehr als die Summe,')
print('  positive und negative Betraege heben sich auf. Die Laenderwerte sind')
print('  damit NICHT als Schaetzung verwendbar, nur als Richtung.')

agg.to_csv('/home/claude/cbcr/ergebnis-zerlegung.csv')
eff.to_csv('/home/claude/cbcr/ergebnis-effektivsaetze.csv')
print('\n-> ergebnis-zerlegung.csv, ergebnis-effektivsaetze.csv')
