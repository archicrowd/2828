# -*- coding: utf-8 -*-
"""
R1b — Wie wirkt die Höhe des Freibetrags in Position 03?

Quelle wie R1: Statistisches Bundesamt, Erbschaft- und Schenkungsteuerstatistik
2024, Statistischer Bericht 73611, Tabelle 73611-05 (Erwerbe nach dem Wert VOR
Abzug) und 73611-07 (Ableitungskette).

GÜNSTIGER UMSTAND
  Die amtlichen Größenklassen liegen bei 5, 10, 50, 100, 200, 300, 500 Tsd,
  2,5 / 5 / 10 / 20 Mio EUR. Freibeträge auf diesen Grenzen lassen sich daher
  OHNE jede Interpolation rechnen — das Ergebnis ist exakt und in der Tabelle
  so gekennzeichnet.

INNERHALB EINER KLASSE
  Liegt der Freibetrag mitten in einer Klasse, wird eine abgeschnittene
  Pareto-Verteilung auf [u, o) angepasst, deren Mittelwert den beobachteten
  Klassenmittelwert trifft. Gleichverteilung wäre falsch: in der Klasse
  500 Tsd bis 2,5 Mio liegt der beobachtete Mittelwert bei 899 Tsd, die
  Gleichverteilung ergäbe 1.500 Tsd. Ein erster Entwurf dieses Skripts hat
  diesen Fehler gemacht und dadurch bei hohen Freibeträgen ein STEIGENDES
  Aufkommen ausgewiesen — unmöglich, und genau daran fiel der Fehler auf.
"""
import pandas as pd, numpy as np

XLS = '/home/claude/erbschaft/erbst.xlsx'
MRD, SATZ = 1e6, 0.28
GRUNDFREIBETRAG = 12.348      # Tsd EUR, § 32a EStG 2026

def lies(blatt, um):
    d = pd.read_excel(XLS, sheet_name=blatt)
    d.columns = [str(c).strip() for c in d.columns]
    d = d.rename(columns=um)
    for c in d.columns:
        if pd.api.types.is_string_dtype(d[c]) or d[c].dtype == object:
            d[c] = d[c].astype('string').str.strip()
    d['n'] = pd.to_numeric(d['Wert'], errors='coerce')
    return d

def de(v, nk=1):
    return '.' if pd.isna(v) else format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# ------------------------------------------------------------------ Daten
k = lies('csv-73611-07', {'Gegenstand_der_Nachweisung': 'pos',
                          'Steuerpflichtige_Erwerbe': 'art', 'Masseinheit': 'e',
                          'Steuerpflichtiger_Erwerb_groesser_Null_groesser_gleich_Null': 'abgr'})
k = k[k.abgr == 'Steuerpflichtiger Erwerb größer/gleich Null']
hol = lambda p, e='1 000 EUR': k[(k.pos == p) & (k.art == 'Erwerbe insgesamt') & (k.e == e)].n.iloc[0]
VOR, NACH, STEU = hol('Gesamtwert der Erwerbe vor Abzug'), \
                  hol('Gesamtwert der Erwerbe nach Abzug'), hol('Tatsächlich festgesetzte Steuer')
P13A, P16 = hol('Steuerbegünstigungen nach § 13a ErbStG'), hol('Freibetrag nach § 16 ErbStG')
GRUND = hol('Grundvermögen')
REST = (VOR - NACH) - hol('Steuerbefreiungen nach § 13 ErbStG') - P13A \
       - hol('Freibetrag nach § 13d ErbStG') - hol('DBA-Vermögen')
KOSTEN_ANTEIL = REST / VOR        # echte Abzüge, die auch 28:28 zulassen müsste

g = lies('csv-73611-05', {'Groessenklasse_Wert_Erwerbe_vor_Abzug': 'kl',
                          'Merkmal_Name': 'm', 'Masseinheit': 'e',
                          'Steuerpflichtige_Erwerbe': 'art'})
g = g[g.art == 'Erwerbe Insgesamt']
w = g.pivot_table(index='kl', columns=['m', 'e'], values='n', aggfunc='first')
V, N = ('Wert der Erwerbe vor Abzug', '1 000 EUR'), ('Wert der Erwerbe vor Abzug', 'Fälle')
ST = ('Tatsächlich festgesetzte Steuer', '1 000 EUR')

KLASSEN = [
    ('unter 5 000 EUR', 0, 5), ('von 5 000 bis unter 10 000 EUR', 5, 10),
    ('von 10 000 bis unter 50 000 EUR', 10, 50), ('von 50 000 bis unter 100 000 EUR', 50, 100),
    ('von 100 000 bis unter 200 000 EUR', 100, 200), ('von 200 000 bis unter 300 000 EUR', 200, 300),
    ('von 300 000 bis unter 500 000 EUR', 300, 500), ('von 500 000 bis unter 2,5 Mill. EUR', 500, 2500),
    ('von 2,5 Mill. bis unter 5 Mill. EUR', 2500, 5000), ('von 5 Mill. bis unter 10 Mill. EUR', 5000, 10000),
    ('von 10 Mill. bis unter 20 Mill. EUR', 10000, 20000), ('von 20 Mill. und mehr', 20000, None),
]
GRENZEN = {0, 5, 10, 50, 100, 200, 300, 500, 2500, 5000, 10000, 20000}

def pareto_alpha(u, o, m):
    """Formparameter der auf [u,o) abgeschnittenen Pareto-Verteilung,
       deren Mittelwert m trifft. None, wenn m ausserhalb von (u,o)."""
    if not (u < m < o):
        return None
    q = u / o
    def mittel(a):
        if abs(a - 1.0) < 1e-9:
            a = 1.0 + 1e-9
        return (a / (a - 1.0)) * u * (1 - q ** (a - 1.0)) / (1 - q ** a)
    lo, hi = 1e-6, 60.0
    if mittel(lo) < m or mittel(hi) > m:       # m ausserhalb des erreichbaren Bereichs
        return None
    for _ in range(200):                       # Bisektion, mittel() faellt monoton in a
        mid = (lo + hi) / 2
        if mittel(mid) > m:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def teil_ueber(u, o, n, summe, t):
    """Fälle und Wertsumme oberhalb von t innerhalb der Klasse [u,o)."""
    if t <= u:
        return n, summe
    if o is not None and t >= o:
        return 0.0, 0.0
    m = summe / n
    if o is None:                              # offene Spitzenklasse: Pareto ohne Obergrenze
        a = m / (m - u) if m > u else None      # E[X]=a*u/(a-1)  ->  a = m/(m-u)
        if a is None or a <= 1:
            return n, summe
        anteil = (u / t) ** a
        return n * anteil, n * anteil * a * t / (a - 1)
    a = pareto_alpha(u, o, m)
    if a is None:                              # Mittelwert am Rand: linear behelfen
        anteil = (o - t) / (o - u)
        return n * anteil, n * anteil * (t + o) / 2
    q = u / o
    F = lambda x: (1 - (u / x) ** a) / (1 - q ** a)
    anteil = 1 - F(t)
    # Teilmittelwert oberhalb t, abgeschnittene Pareto auf [t,o)
    qt = t / o
    teilm = (a / (a - 1)) * t * (1 - qt ** (a - 1)) / (1 - qt ** a) if abs(a - 1) > 1e-9 else t
    return n * anteil, n * anteil * teilm

def rechne(frei):
    """Gibt Basis, Fälle über dem Freibetrag und exakt/genähert zurück."""
    basis = faelle = 0.0
    exakt = frei in GRENZEN
    for name, u, o in KLASSEN:
        if name not in w.index:
            continue
        r = w.loc[name]
        wert, n = r[V], r[N]
        if wert <= 0 or n <= 0:
            continue
        if o is not None and o <= frei:
            continue
        nn, ss = teil_ueber(u, o, n, wert, frei)
        faelle += nn
        basis += max(0.0, ss - nn * frei)
    return basis, faelle, exakt

print('=' * 98)
print('R1b — DIE HÖHE DES FREIBETRAGS IN POSITION 03')
print('=' * 98)
print(f'\nAusgangslage 2024: {de(VOR/MRD,1)} Mrd EUR Erwerbswert, '
      f'{de(STEU/MRD,2)} Mrd EUR Steuer.')
print(f'Alle Rechnungen: keine Verschonungen, Satz 28 %, echte Abzüge '
      f'({de(KOSTEN_ANTEIL*100)} %) bleiben abziehbar.')

print(f'\n[1] AUFKOMMEN UND BETROFFENE NACH HÖHE DES FREIBETRAGS')
print(f'{"Freibetrag":>12}{"Basis":>12}{"Steuer":>12}{"gegen heute":>14}'
      f'{"Fälle besteuert":>18}{"Anteil aller Fälle":>20}{"":>4}')
FAELLE_GES = w.loc['Insgesamt'][N]
zeilen = []
for frei in [50, 100, 150, 200, 250, 300, 400, 500, 750, 1000]:
    b, f, ex = rechne(frei)
    b *= (1 - KOSTEN_ANTEIL)
    st = b * SATZ
    zeilen.append(dict(frei=frei, basis=b, steuer=st, faelle=f, exakt=ex,
                       diff=st - STEU, anteil=f / FAELLE_GES * 100))
    mark = '' if ex else '  genähert'
    print(f'{de(frei,0)+" Tsd":>12}{de(b/MRD,1):>9} Mrd{de(st/MRD,2):>9} Mrd'
          f'{("+" if st>=STEU else "")+de((st-STEU)/MRD,2):>14}'
          f'{de(f,0):>18}{de(f/FAELLE_GES*100):>19} %{mark}')
z = pd.DataFrame(zeilen)
print(f'\n    Zum Vergleich: heute zahlen {de(w.loc["Insgesamt"][("Tatsächlich festgesetzte Steuer","Fälle")],0)} '
      f'von {de(FAELLE_GES,0)} Erwerben Steuer.')

# ------------------------------------------------- [2] Was die Halbierung bringt
a400 = z[z.frei == 400].iloc[0]
a200 = z[z.frei == 200].iloc[0]
print(f'\n[2] DIE HALBIERUNG AUF 200.000 EUR IM EINZELNEN')
print(f'    Aufkommen    {de(a400.steuer/MRD,2)} -> {de(a200.steuer/MRD,2)} Mrd EUR  '
      f'(+{de((a200.steuer-a400.steuer)/MRD,2)} Mrd, +{de((a200.steuer/a400.steuer-1)*100,0)} %)')
print(f'    Besteuerte Fälle  {de(a400.faelle,0)} -> {de(a200.faelle,0)}  '
      f'(+{de(a200.faelle-a400.faelle,0)} Erwerbe)')
print(f'    Anteil aller Erwerbe  {de(a400.anteil)} % -> {de(a200.anteil)} %')
# Wer kommt neu hinzu
neu_wert = 0.0
print(f'\n    Neu belastet werden die Klassen:')
for name, u, o in KLASSEN:
    if name not in w.index or o is None or u >= 400:
        continue
    if o <= 200:
        continue
    r = w.loc[name]
    # bei 200 belastet, bei 400 nicht oder nur teilweise
    b200 = rechne(200)
    kurz = name.replace('von ', '').replace(' EUR', '').replace('Mill.', 'Mio')
    n400, _ = teil_ueber(u, o, r[N], r[V], 400)
    n200, _ = teil_ueber(u, o, r[N], r[V], 200)
    dn = n200 - n400
    if dn > 0:
        print(f'      {kurz:<30}{de(dn,0):>10} Erwerbe zusätzlich, '
              f'heutige Steuer je Fall {de(r[ST]/r[N]*1000,0)} EUR')

# --------------------------------------- [3] Konsistenz mit Position 01
print(f'\n[3] GEGENPROBE AN DER EIGENEN LOGIK')
print(f'    Position 03 sagt: "Auch Geerbtes ist Einkommen." Der Grundfreibetrag')
print(f'    für Einkommen beträgt 2026 {de(GRUNDFREIBETRAG,3)} Tsd EUR im Jahr.')
for frei in [200, 400]:
    print(f'      Ein Freibetrag von {de(frei,0)} Tsd EUR entspricht '
          f'{de(frei/GRUNDFREIBETRAG)} Jahren steuerfreien Einkommens.')
print(f'    Erbschaften fallen einmal im Leben an, laufendes Einkommen jedes Jahr.')
print(f'    Ein Lebensfreibetrag ist also nicht per se inkonsistent — aber seine')
print(f'    Höhe ist eine Setzung, die begründet werden muss.')

# --------------------------------------- [4] Das Problem mit dem Wohnhaus
print(f'\n[4] WAS BEIM SENKEN ZU BEDENKEN IST — DAS SELBSTGENUTZTE HAUS')
print(f'    Grundvermögen macht {de(GRUND/MRD,1)} von {de(VOR/MRD,1)} Mrd EUR aus, '
      f'{de(GRUND/VOR*100,0)} % der Erwerbe.')
print(f'    Heute bleibt das Familienheim nach § 13 Abs. 1 Nr. 4b/4c ErbStG steuerfrei,')
print(f'    wenn die Erben zehn Jahre darin wohnen. Position 03 streicht diese Ausnahme.')
print(f'\n    Steuer auf ein geerbtes Haus, ein Kind, Satz 28 %:')
print(f'{"Hauswert":>12}{"bei FB 400":>14}{"bei FB 200":>14}{"heute (Familienheim)":>24}')
for hw in [300, 400, 500, 600, 800, 1200]:
    s4 = max(0, hw - 400) * SATZ
    s2 = max(0, hw - 200) * SATZ
    print(f'{de(hw,0)+" Tsd":>12}{de(s4,1)+" Tsd":>14}{de(s2,1)+" Tsd":>14}'
          f'{"0 (bei Eigennutzung)":>24}')
print(f'\n    Bei einem Freibetrag von 200.000 EUR zahlt das Kind für ein Haus von')
print(f'    500.000 EUR {de((500-200)*SATZ,0)} Tsd EUR — aus Vermögen, das keine Zahlungsmittel sind.')
print(f'    Position 03 sieht Stundung bisher nur für Betriebe vor. Ohne Ausweitung')
print(f'    auf selbstgenutztes Wohneigentum erzwingt die Senkung Verkäufe.')


# ------------------------------- [5] Der Freibetrag als Formel statt als Zahl
print(f'\n[5] EINE VARIANTE, DIE ZUR ARCHITEKTUR DES ENTWURFS PASST')
print(f'    Position 08 koppelt die Dividende an das amtliche Existenzminimum und')
print(f'    lässt sie per Formel steigen, nicht per Wahlversprechen. Derselbe Anker')
print(f'    liesse sich für den Erbschaftsfreibetrag verwenden: ein Vielfaches des')
print(f'    jährlichen Existenzminimums ({de(GRUNDFREIBETRAG,3)} Tsd EUR, 2026).')
print(f'\n{"Vielfaches":>12}{"Freibetrag":>14}{"Steuer":>12}{"gegen heute":>14}'
      f'{"besteuerte Fälle":>19}')
for mult in [12, 16, 20, 24, 28, 32, 40]:
    frei = GRUNDFREIBETRAG * mult
    b, f, _ = rechne(frei)
    st = b * (1 - KOSTEN_ANTEIL) * SATZ
    mark = '   <- "28 Jahre"' if mult == 28 else ('   <- heutiger Kinderfreibetrag' if mult == 32 else '')
    print(f'{mult:>10} x{de(frei,0)+" Tsd":>14}{de(st/MRD,2)+" Mrd":>12}'
          f'{("+" if st>=STEU else "")+de((st-STEU)/MRD,2):>14}{de(f,0):>19}{mark}')
print(f'\n    Der Vorteil liegt nicht in der Höhe, sondern darin, dass der Freibetrag')
print(f'    dann eine abgeleitete Grösse ist und nicht eine gesetzte. Er steigt mit')
print(f'    dem Existenzminimum, ohne dass ihn jemand neu beschliessen muss — genau')
print(f'    die Eigenschaft, die der Entwurf bei der Dividende hervorhebt.')

z.to_csv('/home/claude/erbschaft/r1b-freibetragskurve.csv', index=False)
print('\n-> r1b-freibetragskurve.csv')
