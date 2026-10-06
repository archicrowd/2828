# -*- coding: utf-8 -*-
"""
Was die OECD-Daten für die zehn Positionen und für den Satz von 28 % bedeuten.

FRAGE
  Position 05 verändert die Bemessungsgrundlage, der Satz von 28 % verändert
  den Tarif. Beides wirkt gegenläufig. Welcher Teil trägt wie viel?

PANELS — bitte beachten
  '_T'      alle Teilgruppen, Verluste gegengerechnet. Volle Länderabdeckung.
            Hier steht die tatsächlich zurückgestellte Steuer. Nur dieses
            Panel wird für die Aufkommensrechnung verwendet.
  'PANELAI' nur Teilgruppen mit positivem Gewinn. Richtig für den
            internationalen Satzvergleich, aber LÜCKENHAFT: für Dänemark
            weist es 4,9 Mrd. USD Gewinn aus, das Gesamtpanel 44,0. Für
            Aufkommensrechnungen deshalb unbrauchbar.

ZWEI VERGLEICHSMASSSTÄBE FÜR DIE SATZWIRKUNG
  a) gegen den gesetzlichen Satz  — was der Entwurf formal ändert
  b) gegen den effektiven Satz    — was tatsächlich gezahlt wird; liegt in
     Deutschland ÜBER dem gesetzlichen, weil Verlustgesellschaften trotzdem
     zahlen (Mindestbesteuerung). Beide Werte spannen das Band auf.

ABGRENZUNG
  Erfasst sind nur Konzerne über 750 Mio. EUR Umsatz. Der Mittelstand fehlt.
  Alle Zahlen gelten für das Konzernsegment, nicht für die gesamte deutsche
  Unternehmensbesteuerung.
"""
import pandas as pd, numpy as np

F = '/mnt/user-data/uploads/OECD_CTP_TPS_DSD_CBCR_DF_CBCRI_1_1_complete_2026-10-01_07-07-01.csv'
JAHR, MRD, USD_EUR, SATZ = 2023, 1e9, 0.8611, 0.28
SAMMEL = {'A','E','F','S','W','A_O','E_O','F_O','S_O','W_O','WXD','ANT_F','_T','_Z'}

# gesetzlicher Satz 2026, Tax Foundation; Deutschland einschliesslich Gewerbesteuer
GESETZ = {'DEU':30.1,'FRA':25.8,'ESP':25.0,'NLD':25.8,'IRL':12.5,
          'BEL':25.0,'AUT':23.0,'DNK':22.0,'SVN':22.0,'EST':22.0}
KLUB = {'DEU':'Deutschland','FRA':'Frankreich','ESP':'Spanien','NLD':'Niederlande',
        'IRL':'Irland','BEL':'Belgien','AUT':'Österreich','DNK':'Dänemark',
        'SVN':'Slowenien','EST':'Estland'}

cols = ['REF_AREA','COUNTERPART_AREA','MEASURE','STATISTICAL_OPERATION',
        'AGGREGATION_TYPE','PROFIT_GROUPING','TIME_PERIOD','OBS_VALUE']
raw = pd.read_csv(F, usecols=cols, low_memory=False)
raw = raw[(raw.TIME_PERIOD == JAHR) & (raw.AGGREGATION_TYPE == 'TOTAL') &
          (raw.STATISTICAL_OPERATION == '_Z')]

def tafel(grp):
    w = (raw[raw.PROFIT_GROUPING == grp]
         .pivot_table(index=['REF_AREA','COUNTERPART_AREA'], columns='MEASURE',
                      values='OBS_VALUE', aggfunc='first').reset_index())
    return w[~w.COUNTERPART_AREA.isin(SAMMEL)]

alle, pos = tafel('_T'), tafel('PANELAI')

print('=' * 100)
print(f'WIRKUNG AUF DIE ZEHN POSITIONEN UND AUF DEN SATZ 28 % — OECD CbCR Tabelle I, {JAHR}')
print('=' * 100)

# ------------------------------------------------- [A] Wo steht 28 % weltweit?
a = pos.groupby('COUNTERPART_AREA').agg(profit=('PROFIT','sum'), tax=('TAX_ACCRUED','sum'))
a = a[a.profit > 0]
a['satz'] = a.tax / a.profit * 100
print('\n[A] WO STEHT 28 % IM VERGLEICH ZU DEM, WAS WELTWEIT GEZAHLT WIRD')
print('    Panel A(i), gewinngewichtet. Nur Satzvergleich, keine Aufkommensrechnung.')
print(f'    Weltweiter effektiver Satz: {a.tax.sum()/a.profit.sum()*100:.1f} %')
for s in (10, 15, 20, 28):
    u = a[a.satz < s]
    print(f'    Gewinn unter {s:>2} %: {u.profit.sum()/MRD:>8,.0f} Mrd USD'
          f' = {u.profit.sum()/a.profit.sum()*100:>4.1f} %  ({len(u)} Jurisdiktionen)')

# ------------------------------------- [B] Zerlegung und Aufkommen, Panel '_T'
alle['upr_pos'] = alle.UPR.clip(lower=0)
su = alle.groupby('REF_AREA').upr_pos.transform('sum')
sp = alle.groupby('REF_AREA').PROFIT.transform('sum')
alle['zerlegt'] = np.where(su > 0, alle.upr_pos / su * sp, np.nan)
z = alle.groupby('COUNTERPART_AREA').agg(basis_alt=('PROFIT','sum'),
                                         basis_neu=('zerlegt','sum'),
                                         steuer_alt=('TAX_ACCRUED','sum'))

print('\n[B] AUFKOMMEN IM KONZERNSEGMENT, in Mrd EUR  (Panel _T, Kurs 0,8611)')
print('    Satzwirkung  = (28 % − Vergleichssatz) × heutige Basis')
print('    Mengenwirkung= 28 % × zusätzlich zugeordnete Basis')
print(f'{"Land":<14}{"Basis alt":>10}{"Basis neu":>10}{"Steuer alt":>11}'
      f'{"eff.":>7}{"gesetzl.":>9}{"Satzw. eff":>11}{"Satzw. ges":>11}'
      f'{"Mengenw.":>10}{"Band":>15}')
rows = []
for c, nm in KLUB.items():
    if c not in z.index:
        continue
    r = z.loc[c]
    b_alt, b_neu = r.basis_alt * USD_EUR / MRD, r.basis_neu * USD_EUR / MRD
    st_alt = r.steuer_alt * USD_EUR / MRD
    eff = r.steuer_alt / r.basis_alt * 100 if r.basis_alt > 0 else np.nan
    ges = GESETZ[c]
    sw_eff = b_alt * (SATZ - eff / 100) if pd.notna(eff) else np.nan
    sw_ges = b_alt * (SATZ - ges / 100)
    mw = (b_neu - b_alt) * SATZ
    lo, hi = sorted([sw_eff + mw, sw_ges + mw])
    print(f'{nm:<14}{b_alt:>10,.1f}{b_neu:>10,.1f}{st_alt:>11,.1f}'
          f'{eff:>6,.1f}%{ges:>8,.1f}%{sw_eff:>+11,.1f}{sw_ges:>+11,.1f}'
          f'{mw:>+10,.1f}{f"{lo:+,.1f} … {hi:+,.1f}":>15}')
    rows.append(dict(land=nm, basis_alt=b_alt, basis_neu=b_neu, steuer_alt=st_alt,
                     eff=eff, gesetzlich=ges, satzwirkung_eff=sw_eff,
                     satzwirkung_ges=sw_ges, mengenwirkung=mw, band_lo=lo, band_hi=hi))
k = pd.DataFrame(rows)
print(f'{"Summe zehn":<14}{k.basis_alt.sum():>10,.1f}{k.basis_neu.sum():>10,.1f}'
      f'{k.steuer_alt.sum():>11,.1f}{"":>16}{k.satzwirkung_eff.sum():>+11,.1f}'
      f'{k.satzwirkung_ges.sum():>+11,.1f}{k.mengenwirkung.sum():>+10,.1f}'
      f'{f"{k.band_lo.sum():+,.1f} … {k.band_hi.sum():+,.1f}":>15}')

de = k[k.land == 'Deutschland'].iloc[0]
print(f"""
    DEUTSCHLAND IM KLARTEXT
      Konzerngewinn heute in Deutschland gebucht        {de.basis_alt:>7,.1f} Mrd EUR
      tatsächlich zurückgestellte Steuer darauf         {de.steuer_alt:>7,.1f} Mrd EUR
        effektiv {de.eff:,.1f} % — über dem gesetzlichen Satz von {de.gesetzlich:,.1f} %,
        weil Verlustgesellschaften trotzdem zahlen.
      Basis nach Zerlegung nach Kundenumsatz            {de.basis_neu:>7,.1f} Mrd EUR
      Steuer bei 28 % auf diese Basis                   {de.basis_neu*SATZ:>7,.1f} Mrd EUR
      ------------------------------------------------------------------
      Mengenwirkung (Position 05)                       {de.mengenwirkung:>+7,.1f} Mrd EUR
      Satzwirkung (28 % statt {de.gesetzlich:,.1f} bzw. {de.eff:,.1f} %)    {de.satzwirkung_ges:>+7,.1f} bis {de.satzwirkung_eff:+,.1f} Mrd EUR
      Zusammen                                          {de.band_lo:>+7,.1f} bis {de.band_hi:+,.1f} Mrd EUR

      Der Satz von 28 % ist für Deutschland eine SENKUNG. Er kostet Aufkommen.
      Position 05 ist das, was diese Senkung bezahlt — und sie trägt mehr als
      das Doppelte dessen, was der Satz kostet.""")

# ------------------------------------------------ [C] Was ohne Position 05 bleibt
print('\n[C] GEGENPROBE — 28 % OHNE POSITION 05')
for _, r in k.iterrows():
    lo, hi = sorted([r.satzwirkung_eff, r.satzwirkung_ges])
    print(f'    {r.land:<14}{lo:>+8,.1f} bis {hi:+,.1f} Mrd EUR'
          + ('   <- Verlust' if hi < 0 else ''))
print(f'    {"Summe zehn":<14}{k.satzwirkung_eff.sum():>+8,.1f} bis '
      f'{k.satzwirkung_ges.sum():+,.1f} Mrd EUR')

# -------------------------------- [D] Elastizität: welcher Teil der Basis flieht?
print('\n[D] VERHALTENSREAKTION — ANHANG PUNKT 3')
print('    Die Semi-Elastizität der erklärten Gewinne (0,8 / 1,0 / 1,5) misst')
print('    Gewinnverlagerung als Reaktion auf den Satz. Position 05 schaltet')
print('    diesen Kanal ab: verlagern lässt sich der Gewinn, nicht die Kundschaft.')
print(f'    Deutschland: {de.basis_alt/de.basis_neu*100:,.0f} % der neuen Basis ist Altbestand,')
print(f'                 {(de.basis_neu-de.basis_alt)/de.basis_neu*100:,.0f} % ist neu zugeordnet.')
print('    Auf den neu zugeordneten Teil darf die Elastizität nicht angewendet')
print('    werden. Auf den Altbestand schon — dort sinkt der Satz aber, die')
print('    Elastizität wirkt also zugunsten der Rechnung, nicht gegen sie.')

k.to_csv('/home/claude/oecd/t1-wirkung-28.csv', index=False)
a.sort_values('profit', ascending=False).to_csv('/home/claude/oecd/t1-saetze-welt.csv')
print('\n-> t1-wirkung-28.csv, t1-saetze-welt.csv')
