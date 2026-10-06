# -*- coding: utf-8 -*-
"""
ZEHN LÄNDERDATEIEN  —  Überschlagsrechnung zur Übertragbarkeit von TAX 28:28
Deutschland, Frankreich, Spanien, Niederlande, Irland, Belgien, Österreich,
Dänemark, Slowenien, Estland

Die verstärkte Zusammenarbeit nach dem EU-Vertrag verlangt mindestens neun
Mitgliedstaaten. Zehn Dateien lassen also Spielraum: Es müssen nicht alle
mitmachen, damit der Verbund zustande kommt.

METHODE UND GRENZEN (bitte mitlesen)
  Dies ist KEIN Mehrländermodell. Gerechnet wird ausschliesslich die Bruttokostenseite
  der Digitaldividende bei landesspezifischen Einkommensniveaus. Alle übrigen Bausteine
  (Tarifaufkommen, Unternehmen, Konsum, Boden, CO2, Abgabenumbau) sind NICHT je Land
  modelliert; der "rechnerische Satz" ist eine lineare Skalierung des deutschen Modells
  und ersetzt keine nationale Rechnung.

  IRLAND: Das irische BIP ist durch die Bilanzierung multinationaler Konzerne stark
  überhöht. Das irische Statistikamt weist deshalb das modifizierte Bruttonationaleinkommen
  GNI* aus: 334,0 Mrd. EUR gegenüber 602,4 Mrd. EUR BIP im Jahr 2025, also 55,5 %.
  Für Irland werden beide Bezugsgrössen gerechnet. Massgeblich ist GNI*.

QUELLEN (alle Abrufe September 2026)
  BIP nominal und BIP/Kopf 2026 (Projektion)   IWF, World Economic Outlook April 2026,
                                               abgerufen über Worldometer
  Umrechnung USD/EUR                           EZB-Durchschnittskurs 2026: 0,8611 EUR je USD
  Median-Äquivalenzeinkommen, Stand 2025       WKO, "Einkommen & Armutsgefährdung",
                                               Zusammenstellung aus EU-SILC
                                               -> KEINE Primärquelle, Werte vorläufig
  Spitzensatz Einkommensteuer 2026             Tax Foundation; Estland: estnische
                                               Handelskammer (24 % ab 01.01.2026)
  Unternehmensteuer 2026                       Tax Foundation; Estland auf ausgeschüttete
                                               Gewinne; Irland 12,5 %, für grosse Konzerne
                                               faktisch 15 % (globale Mindeststeuer)
  Mehrwertsteuer-Normalsatz                    allgemein bekannt; Estland 24 % ab 07/2025
  Defizit 2025, Schulden Ende 2025             Eurostat, Euroindikatoren 22.04.2026
  Irland GNI* und BIP 2025                     Central Statistics Office Ireland
  Verlagerte Gewinne, Einstufung als Oase       Tørsløv, Wier und Zucman,
                                               aktualisierte Zahlen 2019 (Daten 2016)
  Anteil 0-14 Jahre                            Weltbank; Estland, Irland und Slowenien
                                               geschätzt
  EU-Bevölkerung 2025                          Eurostat
  EU-BIP je Einwohner 2025 (41.570 EUR)        Eurostat
"""

# ---------------------------------------------------------------- Rahmengrössen
EUR_JE_USD = 0.8611          # EZB-Durchschnitt 2026
EU_BEV     = 452.0           # Mio., 2025
EU_BIP_PK  = 41570.0         # EUR je Einwohner, 2025
EU_BIP     = EU_BEV * EU_BIP_PK / 1000   # Mrd. EUR, 2025
L_DE       = 28              # Einheitssatz des deutschen Referenzmodells
PP_ERTRAG  = 0.55            # % BIP je Prozentpunkt Einheitssatz (deutsches Modell)

# ------------------------------------------------------------------ Länderdaten
#  bip_usd  BIP nominal 2026, Mrd. USD        pk_usd  BIP/Kopf 2026, USD
#  median   Median-Äquivalenzeinkommen, EUR/Jahr, Stand 2025
#  k014     Anteil 0-14 Jahre, %              est     Spitzensatz Einkommensteuer, %
#  kst      Unternehmensteuer, %              mwst    Mehrwertsteuer-Normalsatz, %
#  defizit  Finanzierungssaldo 2025, % BIP    schuld  Schuldenstand Ende 2025, % BIP
#  bezug    Korrekturfaktor der Bezugsgrösse (nur Irland: GNI* statt BIP)
LAND = {
 'Deutschland': dict(bip_usd=5450.00, pk_usd=65303,  median=28891, k014=14,
                     est=47.5, kst=30.1, mwst=19, defizit=-2.7, schuld=63.5,
                     bezug=1.0, verlag='verliert'),
 'Frankreich':  dict(bip_usd=3600.00, pk_usd=52083,  median=26459, k014=17,
                     est=55.4, kst=25.8, mwst=20, defizit=-5.1, schuld=115.6,
                     bezug=1.0, verlag='verliert'),
 'Spanien':     dict(bip_usd=2090.00, pk_usd=41563,  median=20367, k014=14,
                     est=54.0, kst=25.0, mwst=21, defizit=-2.4, schuld=100.7,
                     bezug=1.0, verlag='verliert'),
 'Niederlande': dict(bip_usd=1450.00, pk_usd=79918,  median=34466, k014=15,
                     est=49.5, kst=25.8, mwst=21, defizit=-1.6, schuld=44.4,
                     bezug=1.0, verlag='OASE, 90 Mrd. USD zugeflossen (2016)'),
 'Irland':      dict(bip_usd=779.38,  pk_usd=140186, median=35138, k014=19,
                     est=48.0, kst=12.5, mwst=23, defizit=+1.8, schuld=32.9,
                     bezug=334.0/602.4, verlag='OASE, 117 Mrd. USD zugeflossen (2016)'),
 'Belgien':     dict(bip_usd=776.73,  pk_usd=65112,  median=31299, k014=17,
                     est=53.5, kst=25.0, mwst=21, defizit=-5.2, schuld=107.9,
                     bezug=1.0, verlag='OASE, 15 Mrd. USD zugeflossen (2016)'),
 'Österreich':  dict(bip_usd=623.72,  pk_usd=67761,  median=36546, k014=14,
                     est=55.0, kst=23.0, mwst=20, defizit=-4.2, schuld=81.5,
                     bezug=1.0, verlag='verliert'),
 'Dänemark':    dict(bip_usd=503.77,  pk_usd=83445,  median=36192, k014=16,
                     est=60.5, kst=22.0, mwst=25, defizit=+2.9, schuld=27.9,
                     bezug=1.0, verlag='verliert'),
 'Slowenien':   dict(bip_usd=86.73,   pk_usd=40630,  median=20416, k014=15,
                     est=50.0, kst=22.0, mwst=22, defizit=-2.5, schuld=65.7,
                     bezug=1.0, verlag='verliert'),
 'Estland':     dict(bip_usd=51.63,   pk_usd=37718,  median=17146, k014=15,
                     est=24.0, kst=22.0, mwst=24, defizit=-2.0, schuld=24.1,
                     bezug=1.0, verlag='verliert'),
}
REIHE = ['Deutschland', 'Frankreich', 'Spanien', 'Niederlande', 'Irland',
         'Belgien', 'Österreich', 'Dänemark', 'Slowenien', 'Estland']

# ------------------------------------------------- Die eine Regel: der Dividendenanker
# Deutschland: 515 EUR/Monat = 50 % des amtlichen Existenzminimums 2026 (12.348 EUR/Jahr).
# Als übertragbare Regel: ein fester Anteil des nationalen Median-Äquivalenzeinkommens.
DD_DE_MONAT = 515.0
ANKER = DD_DE_MONAT * 12 / LAND['Deutschland']['median']
KIND_ANTEIL = 0.5


def rechne(d):
    bip_eur = d['bip_usd'] * EUR_JE_USD                      # Mrd. EUR
    bev     = d['bip_usd'] * 1000 / d['pk_usd']              # Mio. Einwohner
    kinder  = bev * d['k014'] / 100
    erw     = bev - kinder
    dd_m    = d['median'] * ANKER / 12                       # EUR/Monat, Erwachsene
    kosten  = (erw * dd_m + kinder * dd_m * KIND_ANTEIL) * 12 / 1000   # Mrd. EUR/Jahr
    return dict(bip_eur=bip_eur, bezug_eur=bip_eur * d['bezug'], bev=bev,
                kinder=kinder, erw=erw, dd_m=dd_m, dd_k=dd_m * KIND_ANTEIL,
                kosten=kosten,
                quote=kosten / bip_eur * 100,
                quote_bezug=kosten / (bip_eur * d['bezug']) * 100)


R = {k: rechne(v) for k, v in LAND.items()}
Q_DE = R['Deutschland']['quote']
for k in REIHE:
    # Einordnung: das deutsche Modell um die Mehr- oder Minderkosten verschoben
    R[k]['l_impl'] = L_DE + (R[k]['quote_bezug'] - Q_DE) / PP_ERTRAG

# --------------------------------------------------------------------- Ausgabe
def de(x, n=0):
    return f'{x:,.{n}f}'.replace(',', '§').replace('.', ',').replace('§', '.')

print('=' * 104)
print('ZEHN LÄNDERDATEIEN  —  TAX 28:28, Übertragbarkeit (Überschlag, kein Mehrländermodell)')
print('=' * 104)
print(f'Anker der Dividendenregel: {ANKER*100:.2f} % des nationalen Median-Äquivalenzeinkommens')
print(f'  abgeleitet aus Deutschland: {DD_DE_MONAT:.0f} EUR/Monat bei Median {de(LAND["Deutschland"]["median"])} EUR')
print(f'  Kinder: {KIND_ANTEIL*100:.0f} % des Erwachsenenbetrags')
print(f'  Umrechnung: {EUR_JE_USD} EUR je USD (EZB-Durchschnitt 2026)')
print()

print('[1] GRÖSSE DES KLUBS')
b_sum = sum(R[k]['bev'] for k in REIHE)
g_sum = sum(R[k]['bip_eur'] for k in REIHE)
z_sum = sum(R[k]['bezug_eur'] for k in REIHE)
k_sum = sum(R[k]['kosten'] for k in REIHE)
print(f'{"Land":<14}{"Einw. Mio":>11}{"BIP Mrd EUR":>13}{"Bezug Mrd":>12}{"BIP/Kopf EUR":>14}')
for k in REIHE:
    r = R[k]
    print(f'{k:<14}{r["bev"]:>11.2f}{de(r["bip_eur"]):>13}{de(r["bezug_eur"]):>12}'
          f'{de(LAND[k]["pk_usd"]*EUR_JE_USD):>14}')
print(f'{"KLUB":<14}{b_sum:>11.2f}{de(g_sum):>13}{de(z_sum):>12}')
print(f'  Anteil an der EU: Bevölkerung {b_sum/EU_BEV*100:.1f} %, '
      f'Wirtschaftsleistung rund {g_sum/EU_BIP*100:.0f} %')
print(f'  (EU-Summe {de(EU_BIP)} Mrd. EUR, Stand 2025; Länderwerte sind Projektionen für 2026,')
print(f'   die Wirtschaftsquote ist daher eher die Obergrenze)')
print()

print('[2] DIVIDENDE NACH DER EINEN REGEL UND IHRE BRUTTOKOSTEN')
print(f'{"Land":<14}{"Median EUR":>11}{"DD EUR/M":>10}{"Kind EUR/M":>12}'
      f'{"Kosten Mrd":>12}{"% BIP":>8}{"% Bezug":>9}{"rechn. Satz":>13}')
for k in REIHE:
    r = R[k]
    print(f'{k:<14}{de(LAND[k]["median"]):>11}{r["dd_m"]:>10.0f}{r["dd_k"]:>12.0f}'
          f'{de(r["kosten"]):>12}{r["quote"]:>8.1f}{r["quote_bezug"]:>9.1f}{r["l_impl"]:>13.1f}')
print(f'{"KLUB":<14}{"":>11}{"":>10}{"":>12}{de(k_sum):>12}'
      f'{k_sum/g_sum*100:>8.1f}{k_sum/z_sum*100:>9.1f}')
print('  Bei Irland weicht "% Bezug" vom BIP ab: Bezugsgrösse ist GNI* (55,5 % des BIP).')
print()

print('[3] WEG ZUM EINHEITSSATZ 28 (Prozentpunkte, + = Erhöhung, - = Senkung)')
print(f'{"Land":<14}{"ESt heute":>10}{"-> 28":>8}{"KSt heute":>11}{"-> 28":>8}'
      f'{"MwSt":>7}{"Defizit":>9}{"Schulden":>10}')
for k in REIHE:
    d = LAND[k]
    print(f'{k:<14}{d["est"]:>10.1f}{28-d["est"]:>+8.1f}{d["kst"]:>11.1f}{28-d["kst"]:>+8.1f}'
          f'{d["mwst"]:>7.0f}{d["defizit"]:>+9.1f}{d["schuld"]:>10.1f}')
print()

print('[4] GEWINNVERLAGERUNG')
for k in REIHE:
    print(f'  {k:<14}{LAND[k]["verlag"]}')
print()

print('[5] PRÜFGRÖSSEN')
n_ab = sum(1 for k in REIHE if LAND[k]['est'] > 28)
n_auf = sum(1 for k in REIHE if LAND[k]['est'] < 28)
print(f'  Spitzensatz sinkt in {n_ab} von 10 Ländern, steigt in {n_auf}.')
print(f'  Unternehmensteuer sinkt in {sum(1 for k in REIHE if LAND[k]["kst"] > 28)} von 10, '
      f'steigt in {sum(1 for k in REIHE if LAND[k]["kst"] < 28)}.')
print(f'  Rechnerischer Satz im Korridor 25-30: '
      f'{sum(1 for k in REIHE if 25 <= R[k]["l_impl"] <= 30)} von 10.')
print(f'  Spanne der Dividende: {min(R[k]["dd_m"] for k in REIHE):.0f} bis '
      f'{max(R[k]["dd_m"] for k in REIHE):.0f} EUR/Monat.')
print('  Verstärkte Zusammenarbeit nach EU-Vertrag verlangt mindestens 9 Mitgliedstaaten:')
print('  zehn Dateien lassen einen Platz Spielraum.')
print('  Von den fünf EU-Steueroasen bei Tørsløv, Wier und Zucman (Belgien, Irland,')
print('  Luxemburg, Malta, Niederlande) sind drei dabei; Luxemburg und Malta fehlen.')
print()

print('[6] WAS DIESE RECHNUNG NICHT ZEIGT')
for s in ['Bestehende Sozialleistungen, Beitragssysteme und Steuerbasen je Land.',
          'Kaufkraftunterschiede: 306 EUR in Estland sind mehr wert als 306 EUR in Irland.',
          'Dänemark und Estland finanzieren ihren Sozialstaat überwiegend aus Steuern;',
          '  der Hebel "Beiträge senken" fehlt dort weitgehend.',
          'Belgien, Irland und die Niederlande verlieren bei der Besteuerung am Kundenort',
          '  Aufkommen; das ist hier nicht gegengerechnet.',
          'Irlands Körperschaftsteuer trägt einen aussergewöhnlich hohen Anteil des',
          '  Staatshaushalts; der Übergang wäre dort der härteste des Klubs.',
          'Der Median-Wert stammt aus einer Zusammenstellung, nicht aus der Primärstatistik.']:
    print('  - ' + s)

# ------------------------------------------------------- Zahlen für die Webseite
import json
web = {k: dict(dd=round(R[k]['dd_m']), dd_kind=round(R[k]['dd_k']),
               kosten=round(R[k]['kosten']), quote=round(R[k]['quote'], 1),
               quote_bezug=round(R[k]['quote_bezug'], 1),
               l=round(R[k]['l_impl'], 1), bev=round(R[k]['bev'], 2),
               bip=round(R[k]['bip_eur']),
               **{x: LAND[k][x] for x in ('median', 'est', 'kst', 'mwst',
                                          'defizit', 'schuld')})
       for k in REIHE}
web['_klub'] = dict(bev=round(b_sum, 1), bip=round(g_sum), kosten=round(k_sum),
                    quote=round(k_sum / g_sum * 100, 1),
                    eu_bev=round(b_sum / EU_BEV * 100, 1),
                    eu_bip=round(g_sum / EU_BIP * 100),
                    anker=round(ANKER * 100, 1))
json.dump(web, open('/home/claude/site/klub10-daten.json', 'w'), indent=1, ensure_ascii=False)
print('\n-> /home/claude/site/klub10-daten.json')
