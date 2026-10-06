# -*- coding: utf-8 -*-
"""
R1 — Position 03 (Erbschaft) auf der amtlichen Statistik gerechnet

QUELLE
  Statistisches Bundesamt, Erbschaft- und Schenkungsteuerstatistik 2024,
  Statistischer Bericht 73611, Festsetzungsjahr 2024, Erstfestsetzungen.
  Verwendete Tabellen:
    73611-07  Ermittlung des steuerpflichtigen Erwerbs und der Steuer
    73611-05  Erwerbe nach dem Wert der Erwerbe VOR Abzug (Größenklassen)
    73611-01  Zeitreihe 2007 bis 2024
  Abgrenzung durchgehend: "Steuerpflichtiger Erwerb größer/gleich Null",
  also alle festgesetzten Erwerbe, nicht nur die mit Steuerschuld.

FRAGE
  1. Was kostet die Verschonung des Betriebsvermögens heute an Aufkommen?
  2. Was brächte Position 03: ein Satz von 28 % auf alles oberhalb von
     400.000 EUR je Erwerb, ohne Verschonungsausnahmen?

METHODE
  Die Größenklassen von 73611-05 sind nach dem Wert der Erwerbe VOR Abzug
  gebildet. Der Freibetrag wird je Fall abgezogen, dann 28 % auf den Rest.
  Nur eine Klasse (300.000 bis 500.000) wird vom Freibetrag geschnitten;
  innerhalb dieser Klasse wird Gleichverteilung unterstellt. Das ist hier
  vertretbar: der beobachtete Klassenmittelwert liegt bei 396.746 EUR,
  die Gleichverteilung ergäbe 400.000 EUR.

GRENZEN
  - Ein Jahr, 2024. Die Statistik schwankt stark, weil wenige sehr grosse
    Übertragungen das Bild bestimmen. Die Zeitreihe steht unten.
  - Erfasst sind nur steuerlich festgesetzte Erwerbe. Übertragungen
    unterhalb der Freibeträge erscheinen nicht; das tatsächliche
    Erbvolumen ist um ein Vielfaches grösser.
  - Der Freibetrag von 400.000 EUR wird hier auf JEDEN Erwerb angewendet.
    Heute gilt er für Kinder; Ehegatten haben 500.000, entferntere
    Verwandte 20.000. Die Rechnung ist also für Steuerklasse II und III
    grosszügiger als geltendes Recht und für Ehegatten knapper.
  - Verhaltensreaktionen sind nicht gerechnet. Bei Erbschaften sind sie
    kleiner als bei laufenden Steuern, aber nicht null: Wegzug,
    vorgezogene Schenkungen, Umschichtung in begünstigtes Vermögen.
"""
import pandas as pd, numpy as np

XLS = '/home/claude/erbschaft/erbst.xlsx'
MIO, MRD = 1e3, 1e6          # Werte stehen in 1000 EUR
FREI = 400.0                 # 400.000 EUR = 400 Tsd EUR je Erwerb
SATZ = 0.28

def lies(blatt, umbenennen):
    d = pd.read_excel(XLS, sheet_name=blatt)
    d.columns = [str(c).strip() for c in d.columns]
    d = d.rename(columns=umbenennen)
    d['n'] = pd.to_numeric(d['Wert'], errors='coerce')
    for c in d.columns:                      # die Quelle hat nachgestellte Leerzeichen
        if pd.api.types.is_string_dtype(d[c]) or d[c].dtype == object:
            d[c] = d[c].astype('string').str.strip()
    return d

def de(v, nk=1):
    if pd.isna(v): return '.'
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

print('=' * 100)
print('R1 — ERBSCHAFT- UND SCHENKUNGSTEUER 2024, POSITION 03')
print('=' * 100)

# ------------------------------------------------- [1] Ableitungskette 73611-07
k = lies('csv-73611-07', {
    'Gegenstand_der_Nachweisung': 'pos', 'Steuerpflichtige_Erwerbe': 'art',
    'Masseinheit': 'e',
    'Steuerpflichtiger_Erwerb_groesser_Null_groesser_gleich_Null': 'abgr'})
k = k[(k.abgr == 'Steuerpflichtiger Erwerb größer/gleich Null')]

def hol(pos, art='Erwerbe insgesamt', e='1 000 EUR'):
    s = k[(k.pos == pos) & (k.art == art) & (k.e == e)].n
    return s.iloc[0] if len(s) else np.nan

VOR   = hol('Gesamtwert der Erwerbe vor Abzug')
NACH  = hol('Gesamtwert der Erwerbe nach Abzug')
P13   = hol('Steuerbefreiungen nach § 13 ErbStG')
P13A  = hol('Steuerbegünstigungen nach § 13a ErbStG')
P13D  = hol('Freibetrag nach § 13d ErbStG')
DBA   = hol('DBA-Vermögen')
P16   = hol('Freibetrag nach § 16 ErbStG')
STPFL = hol('Steuerpflichtiger Erwerb (abgerundet)')
STEU  = hol('Tatsächlich festgesetzte Steuer')
BV    = hol('Betriebsvermögen (Wert > 0)')
FAELLE = hol('Gesamtwert der Erwerbe vor Abzug', e='Fälle')

ABZUG = VOR - NACH
REST  = ABZUG - P13 - P13A - P13D - DBA   # §5, §17, Auflagen, Nebenkosten

print(f'\n[1] VOM ERWERB ZUR STEUER, 2024, alle festgesetzten Erwerbe')
print(f'    {"Fälle insgesamt":<54}{de(FAELLE,0):>14}')
print(f'    {"Wert der Erwerbe vor Abzug":<54}{de(VOR/MRD,3):>14} Mrd EUR')
print(f'    {"  abzüglich Steuerbefreiungen § 13 (u.a. Familienheim)":<54}{de(-P13/MRD,3):>14}')
print(f'    {"  abzüglich Betriebsvermögen § 13a":<54}{de(-P13A/MRD,3):>14}  <<<')
print(f'    {"  abzüglich Mietwohngrundstücke § 13d":<54}{de(-P13D/MRD,3):>14}')
print(f'    {"  abzüglich DBA-Vermögen":<54}{de(-DBA/MRD,3):>14}')
print(f'    {"  abzüglich Zugewinnausgleich, Versorgungsfreibetrag,":<54}')
print(f'    {"    Auflagen und Erwerbsnebenkosten":<54}{de(-REST/MRD,3):>14}')
print(f'    {"Wert der Erwerbe nach Abzug":<54}{de(NACH/MRD,3):>14} Mrd EUR')
print(f'    {"  abzüglich persönliche Freibeträge § 16":<54}{de(-P16/MRD,3):>14}')
print(f'    {"  zuzüglich Vorerwerbe und übernommene Steuer":<54}'
      f'{de((STPFL-(NACH-P16))/MRD,3):>14}')
print(f'    {"Steuerpflichtiger Erwerb":<54}{de(STPFL/MRD,3):>14} Mrd EUR')
print(f'    {"Tatsächlich festgesetzte Steuer":<54}{de(STEU/MRD,3):>14} Mrd EUR')
print(f'\n    Abzüge insgesamt {de(ABZUG/MRD,3)} Mrd = {de(ABZUG/VOR*100)} % des Erwerbswerts,')
print(f'    bevor überhaupt ein persönlicher Freibetrag greift.')
print(f'    Davon allein Betriebsvermögen: {de(P13A/MRD,3)} Mrd = {de(P13A/ABZUG*100)} % aller Abzüge.')
print(f'    Zum Vergleich: übertragenes Betriebsvermögen (Wert > 0) {de(BV/MRD,3)} Mrd —')
print(f'    die Verschonung erfasst {de(P13A/BV*100)} % davon.')
print(f'    Effektiver Satz heute: {de(STEU/VOR*100)} % des Erwerbswerts, '
      f'{de(STEU/STPFL*100)} % des steuerpflichtigen Erwerbs.')

# ------------------------------------------- [2] Größenklassen 73611-05
g = lies('csv-73611-05', {'Groessenklasse_Wert_Erwerbe_vor_Abzug': 'kl',
                          'Merkmal_Name': 'm', 'Masseinheit': 'e',
                          'Steuerpflichtige_Erwerbe': 'art'})
g = g[g.art == 'Erwerbe Insgesamt']
w = g.pivot_table(index='kl', columns=['m', 'e'], values='n', aggfunc='first')

# Klassengrenzen in Tsd EUR; None = offen
GRENZEN = [
    ('unter 5 000 EUR',                     0,      5),
    ('von 5 000 bis unter 10 000 EUR',      5,     10),
    ('von 10 000 bis unter 50 000 EUR',    10,     50),
    ('von 50 000 bis unter 100 000 EUR',   50,    100),
    ('von 100 000 bis unter 200 000 EUR', 100,    200),
    ('von 200 000 bis unter 300 000 EUR', 200,    300),
    ('von 300 000 bis unter 500 000 EUR', 300,    500),
    ('von 500 000 bis unter 2,5 Mill. EUR', 500,  2500),
    ('von 2,5 Mill. bis unter 5 Mill. EUR', 2500, 5000),
    ('von 5 Mill. bis unter 10 Mill. EUR', 5000, 10000),
    ('von 10 Mill. bis unter 20 Mill. EUR', 10000, 20000),
    ('von 20 Mill. und mehr',              20000,  None),
]
V = ('Wert der Erwerbe vor Abzug', '1 000 EUR')
N = ('Wert der Erwerbe vor Abzug', 'Fälle')
A = ('Wert der Erwerbe nach Abzug', '1 000 EUR')
S = ('Tatsächlich festgesetzte Steuer', '1 000 EUR')

print(f'\n[2] EFFEKTIVER STEUERSATZ NACH DER HÖHE DES ERWERBS')
print(f'    Steuer geteilt durch den Wert des Erwerbs VOR Abzug.')
print(f'{"Größenklasse":<34}{"Fälle":>9}{"Erwerbswert":>14}{"Verschont":>11}'
      f'{"Steuer":>11}{"eff. Satz":>11}')
zeilen = []
for name, u, o in GRENZEN:
    if name not in w.index: continue
    r = w.loc[name]
    v, n, a, s = r[V], r[N], r[A], r[S]
    versch = (v - a) / v * 100 if v > 0 else np.nan
    eff = s / v * 100 if v > 0 else np.nan
    zeilen.append(dict(klasse=name, u=u, o=o, faelle=n, wert=v, nach=a, steuer=s,
                       verschont_pct=versch, eff_pct=eff))
    kurz = name.replace('von ', '').replace(' EUR', '').replace('Mill.', 'Mio')
    print(f'{kurz:<34}{de(n,0):>9}{de(v/MRD,2):>12} Mrd{de(versch):>10} %'
          f'{de(s/MRD,2):>9} Mrd{de(eff):>10} %')
z = pd.DataFrame(zeilen)
ins = w.loc['Insgesamt']
print(f'{"Insgesamt":<34}{de(ins[N],0):>9}{de(ins[V]/MRD,2):>12} Mrd'
      f'{de((ins[V]-ins[A])/ins[V]*100):>10} %{de(ins[S]/MRD,2):>9} Mrd'
      f'{de(ins[S]/ins[V]*100):>10} %')

tief = z.loc[z[(z.u >= 2500)].eff_pct.idxmin()]
print(f'\n    Auffällig: der niedrigste effektive Satz oberhalb von 2,5 Mio EUR liegt')
print(f'    in der Klasse "{tief.klasse}" bei {de(tief.eff_pct)} %, obwohl dort')
print(f'    {de(tief.verschont_pct)} % des Erwerbswerts verschont werden. Oberhalb von 20 Mio')
print(f'    steigt der Satz auf {de(z.iloc[-1].eff_pct)} %, weil die Verschonung des')
print(f'    Betriebsvermögens bei 26 Mio EUR je Erwerber gedeckelt ist (§ 13a Abs. 1 ErbStG).')

# ------------------------------------------- [3] Position 03 rechnen
print(f'\n[3] POSITION 03 — 28 % AUF ALLES ÜBER {de(FREI,0)} TSD EUR JE ERWERB')
print(f'    Bemessungsgrundlage: Wert der Erwerbe vor Abzug, keine Verschonungen.')
print(f'{"Größenklasse":<34}{"Fälle über FB":>14}{"Basis":>14}{"Steuer 28 %":>14}')
basis_ges = 0.0
for _, r in z.iterrows():
    if r.o is not None and r.o <= FREI:
        n_ueber, basis = 0.0, 0.0
    elif r.u >= FREI:
        n_ueber, basis = r.faelle, max(0.0, r.wert - r.faelle * FREI)
    else:
        # Klasse wird vom Freibetrag geschnitten: Gleichverteilung in [u, o]
        anteil = (r.o - FREI) / (r.o - r.u)
        n_ueber = r.faelle * anteil
        mitte = (FREI + r.o) / 2
        basis = n_ueber * (mitte - FREI)
    basis_ges += basis
    if basis > 0:
        kurz = r.klasse.replace('von ', '').replace(' EUR', '').replace('Mill.', 'Mio')
        print(f'{kurz:<34}{de(n_ueber,0):>14}{de(basis/MRD,2):>11} Mrd'
              f'{de(basis*SATZ/MRD,2):>11} Mrd')
AUFK = basis_ges * SATZ
print(f'{"SUMME":<34}{"":>14}{de(basis_ges/MRD,2):>11} Mrd{de(AUFK/MRD,2):>11} Mrd')

# Abschlag fuer echte Kostenposten, die auch 28:28 abziehen muesste
anteil_kosten = REST / VOR
basis_eng = basis_ges * (1 - anteil_kosten)
AUFK_ENG = basis_eng * SATZ
print(f'\n    Gegenrechnung: Zugewinnausgleich, Versorgungsfreibetrag, Auflagen und')
print(f'    Erwerbsnebenkosten ({de(REST/MRD,2)} Mrd = {de(anteil_kosten*100)} % des Erwerbswerts)')
print(f'    sind keine Verschonungen, sondern echte Abzüge. Bleiben sie bestehen:')
print(f'    Basis {de(basis_eng/MRD,2)} Mrd, Steuer {de(AUFK_ENG/MRD,2)} Mrd.')
print(f'\n    ERGEBNIS  heute {de(STEU/MRD,2)} Mrd  ->  Position 03 '
      f'{de(AUFK_ENG/MRD,2)} bis {de(AUFK/MRD,2)} Mrd EUR')
print(f'              Mehraufkommen +{de((AUFK_ENG-STEU)/MRD,2)} bis '
      f'+{de((AUFK-STEU)/MRD,2)} Mrd  '
      f'(+{de((AUFK_ENG/STEU-1)*100,0)} bis +{de((AUFK/STEU-1)*100,0)} %)')


# ----------------------------- [3b] Wie teuer ist der einheitliche Freibetrag?
print(f'\n[3b] DER FREIBETRAG IST DIE ENTSCHEIDENDE STELLSCHRAUBE')
print(f'    Position 03 nennt "400.000 EUR je Kind". Oben ist der Betrag auf JEDEN')
print(f'    Erwerb angewendet. Heute sind die Freibeträge gestaffelt: 500.000 für')
print(f'    Ehegatten, 400.000 für Kinder, 200.000 für Enkel, 20.000 für alle')
print(f'    übrigen. Steuerklasse II und III — Geschwister, Nichten, Neffen,')
print(f'    Nichtverwandte — sind 76,7 % der Erbfälle und 42,3 % des')
print(f'    steuerpflichtigen Erwerbs (Tabelle 73611-06).')
basis_heutefb = VOR - P16
print(f'\n    {"Variante":<46}{"Basis":>12}{"Steuer 28 %":>14}')
print(f'    {"heute (gestaffelte FB, Verschonungen, Tarif)":<46}'
      f'{de(STPFL/MRD,1):>9} Mrd{de(STEU/MRD,2):>11} Mrd')
print(f'    {"400.000 EUR je Erwerb, keine Verschonungen":<46}'
      f'{de(basis_eng/MRD,1):>9} Mrd{de(AUFK_ENG/MRD,2):>11} Mrd')
print(f'    {"  dasselbe ohne Abzug echter Kosten":<46}'
      f'{de(basis_ges/MRD,1):>9} Mrd{de(AUFK/MRD,2):>11} Mrd')
print(f'    {"heutige Freibeträge, keine Verschonungen":<46}'
      f'{de(basis_heutefb*(1-anteil_kosten)/MRD,1):>9} Mrd'
      f'{de(basis_heutefb*(1-anteil_kosten)*SATZ/MRD,2):>11} Mrd')
print(f'    {"  dasselbe ohne Abzug echter Kosten":<46}'
      f'{de(basis_heutefb/MRD,1):>9} Mrd{de(basis_heutefb*SATZ/MRD,2):>11} Mrd')
print(f'\n    Der einheitliche Freibetrag von 400.000 EUR kostet gegenüber den heutigen')
print(f'    gestaffelten Freibeträgen rund '
      f'{de((basis_heutefb*(1-anteil_kosten)-basis_eng)*SATZ/MRD,1)} Mrd EUR im Jahr.')
print(f'    Das ist die grösste einzelne Entwurfsentscheidung in Position 03 —')
print(f'    grösser als die Abschaffung der Betriebsvermögensverschonung.')

# ------------------------------------------- [4] Was kostet die Verschonung
print(f'\n[4] WAS DIE VERSCHONUNG DES BETRIEBSVERMÖGENS KOSTET')
print(f'    Die Verschonung nach § 13a nimmt {de(P13A/MRD,3)} Mrd EUR aus der Bemessung.')
print(f'    Sie konzentriert sich auf grosse Erwerbe; der Satz, der ohne sie griffe,')
print(f'    liegt zwischen dem heutigen Spitzensatz der Steuerklasse I und 28 %.')
for satz, etikett in [(0.19, 'Steuerklasse I, 600 Tsd bis 6 Mio'),
                      (0.23, 'Steuerklasse I, 6 bis 13 Mio'),
                      (0.27, 'Steuerklasse I, 13 bis 26 Mio'),
                      (0.30, 'Steuerklasse I, über 26 Mio'),
                      (0.28, 'TAX 28:28')]:
    print(f'      bei {de(satz*100,0):>2} %  ({etikett:<34}) '
          f'{de(P13A*satz/MRD,2):>6} Mrd EUR entgangene Steuer')
print(f'\n    Bandbreite 23 bis 30 %: {de(P13A*0.23/MRD,2)} bis {de(P13A*0.30/MRD,2)} Mrd EUR im Jahr —')
print(f'    das sind {de(P13A*0.23/STEU*100,0)} bis {de(P13A*0.30/STEU*100,0)} % des gesamten heutigen Aufkommens von '
      f'{de(STEU/MRD,2)} Mrd.')

# ------------------------------------------- [5] Zeitreihe
t = lies('csv-73611-01', {'Merkmal_SteuerpflichtigerErwerb_FestgesetzteSteuer': 'm',
                          'Masseinheit': 'e', 'Steuerpflichtige_Erwerbe': 'art',
                          'Steuerpflichtige_Erwerbe_Untergliederung': 'unter',
                          'Festsetzungsjahr': 'jahr'})
t = t[(t.art == 'Insgesamt') & (t.e == '1 000 EUR')]
# beide Untergliederungen addieren, damit alle festgesetzten Erwerbe erfasst sind
r = t.groupby(['jahr', 'm']).n.sum().unstack()
print(f'\n[5] ZEITREIHE 2007 BIS 2024 — wie stark schwankt die Statistik?')
print(f'{"Jahr":<8}{"stpfl. Erwerb":>16}{"Steuer":>12}{"Satz":>10}{"Index Steuer":>14}')
basis = None
for j_ in sorted(r.index):
    sp, st = r.loc[j_].get('Steuerpflichtiger Erwerb'), r.loc[j_].get('Festgesetzte Steuer')
    if pd.isna(sp) or pd.isna(st) or sp == 0:
        continue
    if basis is None:
        basis = st
    print(f'{str(j_)[:4]:<8}{de(sp/MRD,2):>13} Mrd{de(st/MRD,2):>9} Mrd'
          f'{de(st/sp*100):>9} %{de(st/basis*100,0):>14}')
st_reihe = r['Festgesetzte Steuer'].dropna() / MRD
print(f'\n    Spanne {de(st_reihe.min(),2)} bis {de(st_reihe.max(),2)} Mrd EUR, '
      f'Median {de(st_reihe.median(),2)}, 2024: {de(STEU/MRD,2)}.')
print(f'    Das ist kein Rauschen, sondern ein Trend: das Aufkommen hat sich seit 2007')
print(f'    verdreifacht, der effektive Satz auf den steuerpflichtigen Erwerb ist von')
print(f'    15,0 auf 20,5 % gestiegen. 2024 ist damit kein Ausreisser, sondern der')
print(f'    aktuelle Stand einer stetigen Entwicklung. Der Sprung 2016 fällt mit der')
print(f'    Neufassung der Verschonungsregeln nach dem Urteil des Bundesverfassungs-')
print(f'    gerichts von 2014 zusammen.')


# ------------------------------------------- [6] Wer zahlt mehr, wer weniger
print(f'\n[6] VERSCHIEBUNG JE GRÖSSENKLASSE — heute gegen Position 03')
print(f'    Die Bemessungsgrundlage ist unter Position 03 fast gleich gross wie heute')
print(f'    ({de(basis_ges/MRD,1)} gegen {de(STPFL/MRD,1)} Mrd EUR), aber anders zusammengesetzt.')
print(f'{"Größenklasse":<30}{"heute":>12}{"Position 03":>14}{"Veränderung":>14}{"je Fall heute":>16}')
kleine_h = kleine_n = 0.0
for _, r in z.iterrows():
    if r.o is not None and r.o <= FREI:
        n_ueber, basis = 0.0, 0.0
    elif r.u >= FREI:
        n_ueber, basis = r.faelle, max(0.0, r.wert - r.faelle * FREI)
    else:
        anteil = (r.o - FREI) / (r.o - r.u)
        n_ueber = r.faelle * anteil
        basis = n_ueber * ((FREI + r.o) / 2 - FREI)
    neu_st = basis * SATZ * (1 - anteil_kosten)
    kurz = r.klasse.replace('von ', '').replace(' EUR', '').replace('Mill.', 'Mio')
    if r.o is not None and r.o <= FREI:
        kleine_h += r.steuer; kleine_n += r.faelle
        continue
    jefall = r.steuer / r.faelle * 1000 if r.faelle else np.nan
    print(f'{kurz:<30}{de(r.steuer/MRD,2):>9} Mrd{de(neu_st/MRD,2):>11} Mrd'
          f'{("+" if neu_st>=r.steuer else "") + de((neu_st-r.steuer)/MRD,2):>14}'
          f'{de(jefall,0):>13} EUR')
print(f'{"alle unter 300 Tsd":<30}{de(kleine_h/MRD,2):>9} Mrd{de(0,2):>11} Mrd'
      f'{de(-kleine_h/MRD,2):>14}{de(kleine_h/kleine_n*1000,0):>13} EUR')
print(f'\n    {de(kleine_n,0)} Erwerbe unter 300.000 EUR zahlen heute zusammen '
      f'{de(kleine_h/MRD,2)} Mrd EUR')
print(f'    und wären unter Position 03 vollständig frei.')
print(f'    Die Klassen zwischen 500.000 und 20 Mio zahlten etwa das Doppelte.')
print(f'    Die Klasse über 20 Mio bliebe fast unverändert, weil dort schon heute')
print(f'    {de(z.iloc[-1].eff_pct)} % effektiv anfallen — die Verschonung ist bei 26 Mio gedeckelt.')

z.to_csv('/home/claude/erbschaft/r1-groessenklassen.csv', index=False)
pd.DataFrame([dict(groesse='Erwerbe vor Abzug', mrd=VOR/MRD),
              dict(groesse='§13 Steuerbefreiungen', mrd=P13/MRD),
              dict(groesse='§13a Betriebsvermögen', mrd=P13A/MRD),
              dict(groesse='§13d Mietwohngrundstücke', mrd=P13D/MRD),
              dict(groesse='übrige Abzüge', mrd=REST/MRD),
              dict(groesse='Erwerbe nach Abzug', mrd=NACH/MRD),
              dict(groesse='§16 persönliche Freibeträge', mrd=P16/MRD),
              dict(groesse='steuerpflichtiger Erwerb', mrd=STPFL/MRD),
              dict(groesse='festgesetzte Steuer', mrd=STEU/MRD),
              dict(groesse='Position 03, eng', mrd=AUFK_ENG/MRD),
              dict(groesse='Position 03, weit', mrd=AUFK/MRD),
              ]).to_csv('/home/claude/erbschaft/r1-kette.csv', index=False)
print('\n-> r1-groessenklassen.csv, r1-kette.csv')
