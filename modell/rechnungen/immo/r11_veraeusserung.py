# -*- coding: utf-8 -*-
"""
R11 — Die Lücke, die niemand gebucht hat: Gewinne aus Immobilienverkäufen

DER BEFUND, DER DIESE RECHNUNG AUSLÖST
  Eine Textsuche über das gesamte Gesamtmodell (modell-2828.py) findet die
  Begriffe Veräußerung, Verkauf, Spekulation, Immobilie, Grundstück und
  Wertzuwachs NICHT EIN EINZIGES MAL. Der Posten "Kapitalerträge 28 %"
  (45 Mrd) ist auf die heutige Abgeltungsteuer kalibriert, und die erfasst
  private Immobiliengewinne nach zehn Jahren gerade nicht.
  Das ist kein Fehlbetrag, sondern nicht gebuchtes Aufkommen.

DAS GELTENDE RECHT
  § 23 Abs. 1 Nr. 1 EStG: steuerpflichtig nur, wenn "der Zeitraum zwischen
  Anschaffung und Veräußerung nicht mehr als zehn Jahre beträgt". Danach
  steuerfrei. Ausgenommen sind Objekte, die "ausschliesslich zu eigenen
  Wohnzwecken genutzt wurden" — die sind immer frei. Freigrenze 600 EUR.
  Unter 28:28 ("alles ist Einkommen, einmal, 28 %") fiele die Zehnjahres-
  frist weg. Die Selbstnutzung ist eine Entscheidung, keine Rechenfrage,
  und wird deshalb unten als Variante geführt.

DATENGRUNDLAGE
  Geldumsatz am deutschen Immobilienmarkt 2024: 247 Mrd EUR bei 805.000
  Kaufverträgen (Gutachterausschüsse / BBSR, Immobilienmarktbericht
  Deutschland 2025). Davon 73 % der KAUFFÄLLE Wohnimmobilien — der
  Umsatzanteil wird dort nicht genannt und ist hier nicht unterstellt.
  Häuserpreisindex (Destatis, 2025 = 100): 2020 90,8 · 2021 101,4 ·
  2022 107,5 · 2023 98,4 · 2024 96,9 · 2025 100,0.

WAS HIER SCHÄTZUNG IST UND NICHT MEHR
  Der Gewinnanteil am Verkaufspreis ist die entscheidende Unbekannte und
  aus dem Geldumsatz allein nicht herzuleiten. Die amtliche Statistik weist
  keine realisierten Wertzuwächse aus. Die Spanne unten ist deshalb breit
  und als Spanne zu lesen, nicht als Zahl. Wer eine Zahl braucht, braucht
  die Kaufpreissammlungen der Gutachterausschüsse mit Vor- und
  Nachverkaufspreis desselben Objekts.
"""
import numpy as np

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1): return ('+' if v >= 0 else '') + de(v, nk)

UMSATZ, FAELLE = 247.0, 805_000
SATZ_2828 = 0.28
# Heutige Durchschnittsbelastung der STEUERPFLICHTIGEN Fälle: § 23 wirkt
# zum persönlichen Satz. Wer ein Objekt binnen zehn Jahren mit Gewinn
# verkauft, hat typisch ein hohes Einkommen -> oberer Tarifbereich.
SATZ_HEUTE = 0.42

print('=' * 96)
print('R11 — GEWINNE AUS IMMOBILIENVERKÄUFEN: DIE UNGEBUCHTE POSITION')
print('=' * 96)
print(f'''
[1] WAS HEUTE SCHON BESTEUERT WIRD, UND WAS NICHT
    Steuerpflichtig ist der schmale Rand: Verkauf binnen zehn Jahren UND
    nicht selbstgenutzt. Alles andere ist frei. Die Anteile sind nicht
    amtlich erhoben; unten drei Annahmen, die die Spanne aufspannen.
''')
# (Name, Anteil am Umsatz binnen 10 Jahren, Anteil selbstgenutzt)
SZEN = [('vorsichtig', 0.25, 0.60), ('mittel', 0.35, 0.50), ('weit', 0.45, 0.40)]
GEWINN = [0.15, 0.25, 0.35]      # Gewinnanteil am Verkaufspreis

print(f'{"Annahme":>12}{"<10 Jahre":>12}{"selbstgenutzt":>15}'
      f'{"heute steuerpfl.":>18}{"heute frei":>13}')
print(f'{"":>39}{"(Anteil am Geldumsatz)":>31}')
for name, kurz, selbst in SZEN:
    stpf = kurz * (1 - selbst)
    print(f'{name:>12}{de(kurz*100,0)+" %":>12}{de(selbst*100,0)+" %":>15}'
          f'{de(stpf*100,1)+" %":>18}{de((1-stpf)*100,1)+" %":>13}')

print(f'''
[2] AUFKOMMEN UNTER 28:28, VARIANTE A — ALLE GEWINNE, AUCH SELBSTGENUTZT
    Das ist die reine Logik des Konzepts. Gewinnanteil waagerecht.
''')
print(f'{"Annahme":>12}' + ''.join(f'{"Gewinn "+de(g*100,0)+" %":>16}' for g in GEWINN))
tab = {}
for name, kurz, selbst in SZEN:
    row = f'{name:>12}'
    for g in GEWINN:
        basis = UMSATZ * g
        brutto = basis * SATZ_2828
        heute = UMSATZ * kurz * (1 - selbst) * g * SATZ_HEUTE
        tab[(name, g)] = (basis, brutto, heute)
        row += f'{pm(brutto - heute, 1)+" Mrd":>16}'
    print(row)
print(f'''
    Gelesen wird die Tabelle als Mehraufkommen gegenüber heute. Sie enthält
    schon die SATZWIRKUNG: die heute steuerpflichtigen Fälle werden von
    rund {de(SATZ_HEUTE*100,0)} % auf {de(SATZ_2828*100,0)} % entlastet, was gegenrechnet.

    DESHALB FÄLLT DIE SPALTE NACH UNTEN, NICHT NACH OBEN. Die "weite"
    Annahme unterstellt, dass heute schon mehr besteuert wird — und je mehr
    heute zum persönlichen Satz erfasst ist, desto mehr VERLIERT 28:28 durch
    den Satz von 28 %. Dieselbe Struktur wie bei Position 05: der eine Satz
    verbreitert die Basis und senkt gleichzeitig den Satz.''')

print(f'''
[3] ZERLEGUNG, am mittleren Fall (35 % binnen zehn Jahren, 50 % selbst-
    genutzt, 25 % Gewinnanteil) — wie bei Position 05''')
basis, brutto, heute = tab[('mittel', 0.25)]
stpf_heute = UMSATZ * 0.35 * 0.50 * 0.25
print(f'''
      Gewinnvolumen insgesamt                {de(basis,1):>8} Mrd EUR
      davon heute steuerpflichtig            {de(stpf_heute,1):>8} Mrd EUR  ({de(stpf_heute/basis*100,0)} %)
      davon heute frei                       {de(basis-stpf_heute,1):>8} Mrd EUR  ({de((basis-stpf_heute)/basis*100,0)} %)

      Mengenwirkung  bisher freie Basis x 28 %      {pm((basis-stpf_heute)*SATZ_2828,1):>7} Mrd
      Satzwirkung    steuerpflichtige Basis x (28−{de(SATZ_HEUTE*100,0)})  {pm(stpf_heute*(SATZ_2828-SATZ_HEUTE),1):>7} Mrd
      {"-"*56}
      netto                                         {pm(brutto-heute,1):>7} Mrd''')

print(f'''
[4] VARIANTE B — SELBSTGENUTZTES WOHNEN BLEIBT FREI
    Das tun 29 der 38 OECD-Staaten (20 ohne Bedingung, 9 mit). Die OECD
    empfiehlt in "Housing Taxation in OECD Countries" allerdings, die
    Freistellung zu DECKELN, damit die höchsten Gewinne erfasst werden.
''')
print(f'{"Annahme":>12}' + ''.join(f'{"Gewinn "+de(g*100,0)+" %":>16}' for g in GEWINN))
for name, kurz, selbst in SZEN:
    row = f'{name:>12}'
    for g in GEWINN:
        basis_b = UMSATZ * (1 - selbst) * g
        heute = UMSATZ * kurz * (1 - selbst) * g * SATZ_HEUTE
        row += f'{pm(basis_b * SATZ_2828 - heute, 1)+" Mrd":>16}'
    print(row)

print(f'''
[5] WAS DAVON ABZUZIEHEN IST: DIE SPERRWIRKUNG
    Eine Steuer auf den Verkaufsgewinn verteuert den Verkauf und hält
    Eigentümer im Objekt. Das ist der "lock-in", und er ist der am besten
    belegte Verhaltenseffekt in diesem ganzen Modell — Grund: er wirkt auf
    den Zeitpunkt, und den kann man frei wählen. Österreich hat die Frist
    2012 abgeschafft und wäre der Erfahrungsbeweis; eine Auswertung der
    dortigen Transaktionszahlen liegt mir nicht vor.
    Mit einem Abschlag von 20 bis 40 % auf das Mehraufkommen:
''')
mid = tab[('mittel', 0.25)]
netto_a = mid[1] - mid[2]
basis_b = UMSATZ * 0.50 * 0.25
netto_b = basis_b * SATZ_2828 - mid[2]
for nm, v in (('Variante A (alle Gewinne)', netto_a),
              ('Variante B (Selbstnutzung frei)', netto_b)):
    print(f'      {nm:<34}{de(v*0.6,1):>6} bis {de(v*0.8,1):<6} Mrd EUR')
print(f'''
[6] EINORDNUNG
    Zum Vergleich: Position 03 (Erbschaft) bringt nach R1b 21,0 Mrd EUR,
    Position 05 (Konzerne) nach R6 im Median 8 Mrd. Die Größenordnung hier
    ist also keine Randnotiz — und sie steht bisher in keiner Zeile des
    Haushalts. Sie würde die Anhebung der mittleren Tarifstufen, über die
    gestern entschieden wurde, ganz oder teilweise überflüssig machen.
    Das ist ein Grund, sie zu rechnen, und ein Grund, sie vorsichtig zu
    rechnen: eine Position, die den unangenehmen Teil der Reform wegnimmt,
    verdient mehr Misstrauen als eine, die ihn verursacht.''')
