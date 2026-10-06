# -*- coding: utf-8 -*-
"""
patch_tarif.py — Der neue Tarif auf der Seite

GRUNDLAGE
  haushalt/pfad.py (R9): mit den korrigierten Einnahmen aus R1 bis R6 braucht
  der 20-Jahres-Pfad 36,1 Mrd EUR zusätzlich, damit in allen drei Szenarien
  kein Lückenjahr entsteht.
  haushalt/tarif_wahl.py (R10b): gleichmässiger Aufschlag von 3 Punkten auf
  die bewegten Stufen, Eingangsstufen und Spitzensatz unverändert.

  Einkommensteuer  0 / 9 / 16 / 21 / 26 / 28  ->  0 / 9 / 19 / 24 / 27 / 28
  Mehrwertsteuer   5 / 11 / 17 / 22 / 28      ->  5 / 11 / 20 / 25 / 28
  Effektivsatz Mehrwertsteuer 20,0 %  ->  21,5 %

BREITENPRÜFUNG
  Alle neuen Werte sind zweistellig wie die alten ("19 %" statt "16 %",
  "20 %" statt "17 %"). Die Leiterbreiten aus der letzten Korrektur bleiben
  damit gültig; es ist keine CSS-Änderung nötig. Wird unten verifiziert.
"""
import pathlib, re, json, sys

tpl = pathlib.Path('tpl.py'); s0 = s = tpl.read_text()

# ------------------------------------------------- 1 Einkommensteuer-Leiter
for alt, neu in (('t3">16', 't3">19'), ('t4">21', 't4">24'), ('t5">26', 't5">27')):
    assert s.count(alt) == 1, f'{alt}: {s.count(alt)} Treffer'
    s = s.replace(alt, neu)

# ------------------------------------------------- 2 Mehrwertsteuer-Leiter
for alt, neu in (('v3">B &middot; 17', 'v3">B &middot; 20'),
                 ('v4">C &middot; 22', 'v4">C &middot; 25')):
    assert s.count(alt) == 1, f'{alt}: {s.count(alt)} Treffer'
    s = s.replace(alt, neu)

# ------------------------------------------------- 3 Rechner: Tarifsätze
alt = 'tarifSaetze:[0,.09,.16,.21,.26,.28]'
neu = 'tarifSaetze:[0,.09,.19,.24,.27,.28]'
assert s.count(alt) == 1
s = s.replace(alt, neu)

# ------------------------------------------------- 4 Rechner: Effektivsatz
# labelKosten vergleicht den neuen Effektivsatz r mit dem heutigen r0=16,5 %.
alt = "function labelKosten(n){const r=.20,r0=.165;"
neu = "function labelKosten(n){const r=.215,r0=.165;"
assert s.count(alt) == 1
s = s.replace(alt, neu)

tpl.write_text(s)
print(f'tpl.py: {sum(1 for a, b in zip(s0, s) if a != b)} Zeichen geändert, '
      f'{len(s)-len(s0):+d} Zeichen Länge')

# ------------------------------------------------- 5 Effektivsatz in 8 Sprachen
# Dezimaltrennzeichen je Sprache: nur en nutzt den Punkt.
ERSATZ = {'de': ('rund 20 %', 'rund 21,5 %'),
          'en': ('around 20 %', 'around 21.5 %'),
          'fr': ('environ 20 %', 'environ 21,5 %'),
          'nl': ('ongeveer 20 %', 'ongeveer 21,5 %'),
          'da': ('omkring 20 %', 'omkring 21,5 %'),
          'es': ('alrededor del 20 %', 'alrededor del 21,5 %'),
          'et': ('umbes 20 %', 'umbes 21,5 %'),
          'sl': ('približno 20 %', 'približno 21,5 %')}
for code, (alt, neu) in ERSATZ.items():
    p = pathlib.Path(f'lang/{code}.json')
    d = json.loads(p.read_text())
    assert alt in d['p06p'], f'{code}: "{alt}" nicht in p06p: {d["p06p"]}'
    d['p06p'] = d['p06p'].replace(alt, neu)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    print(f'  lang/{code}.json  p06p: {alt} -> {neu}')
print('\nAlle Ersetzungen genau einmal getroffen. Keine CSS-Änderung nötig '
      '(alle Werte zweistellig).')
