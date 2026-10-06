# -*- coding: utf-8 -*-
"""
R12 — Entwurf: Erträge aus Immobilien erfassen, Nutzung und Verkauf

DER GRUNDSATZ, DEN DER ENTWURF UMSETZT
  Lage und Wertzuwachs sind im Kaufpreis eingepreist — aber nur, soweit sie
  im Kaufzeitpunkt bekannt waren. Was danach hinzukommt, entsteht durch
  öffentliche Investition: U-Bahn, Schule, Bebauungsplan. Dieser Zuwachs
  ist unverdient und gehört erfasst.

DIE FOLGE, DIE DEM GRUNDSATZ WIDERSPRICHT
  Aus genau diesem Grundsatz folgt, dass die FRANZÖSISCHE Lösung falsch
  herum läuft. Frankreich senkt die Steuer mit der Haltedauer (voller
  Abschlag nach 22 bzw. 30 Jahren) — also gerade dann, wenn sich am meisten
  öffentliche Investition im Bodenwert niedergeschlagen hat. Dasselbe gilt
  für den Schweizer Besitzesdauerrabatt (−50 % nach 20 Jahren).
  Wer "unverdienter Zuwachs durch Infrastruktur" begründet, muss LÄNGERE
  Haltedauern voll erfassen, nicht entlasten.

WAS VON DEN VORBILDERN BLEIBT
  Dänemark  laufende Erfassung auf regelmässig neu bewerteten Werten
            (Neubewertung alle zwei Jahre, Ansatz 20 % unter dem
            Bewertungswert, Vorsichtsprinzip), progressiv mit Schwelle,
            und ein Übergangsrabatt für Alteigentümer
  Schweiz   Zuschlag für kurze Haltedauer (+50 % unter einem Jahr) und
            Steueraufschub bei Ersatzbeschaffung
  Frankreich Zuschlag auf grosse Gewinne (2 bis 6 % über 50.000 EUR)
  Österreich kein Behaltefristprivileg, ein Satz
  Deutschland § 154 BauGB: das Prinzip gilt hier schon
"""
import numpy as np

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1): return ('+' if v >= 0 else '') + de(v, nk)

UMSATZ, FAELLE = 247.0, 805_000
SATZ, SATZ_HEUTE = 0.28, 0.42
GEWINN_ANT = 0.25          # Gewinnanteil am Verkaufspreis, mittlere Annahme
SELBST = 0.50              # Anteil selbstgenutzt
KURZ = 0.35                # Anteil binnen zehn Jahren verkauft

print('=' * 98)
print('R12 — ENTWURF: NUTZUNG UND VERKAUF ERFASSEN, EIGENNUTZUNG MIT FREIBETRAG')
print('=' * 98)

print(f'''
[1] DIE BEIDEN HEBEL, UND WARUM ES ZWEI BRAUCHT

    Laufend (Position 04): die Bodenwertabgabe erfasst den Zuwachs, WÄHREND
      er entsteht, bei dem, der das Grundstück dann hält. Kein Verkauf nötig,
      keine Sperrwirkung, kein Streit über den Einstandspreis von 1974.
    Bei Verkauf (neu): der Veräußerungsgewinn erfasst, was die laufende
      Abgabe nicht getroffen hat — und verhindert das Ausweichen durch
      Halten und Vererben.

    Beide zusammen überschneiden sich. Wer den Zuwachs jährlich besteuert
    UND beim Verkauf noch einmal den vollen Gewinn, besteuert zweimal.
    Das ist die offene Konstruktionsfrage dieses Entwurfs, und sie hat
    zwei saubere Antworten:
      a) gezahlte Bodenwertabgabe vom Veräußerungsgewinn abziehen
      b) Einstandspreis um die gezahlte Abgabe erhöhen (Indexierung)
    Beide laufen wirtschaftlich auf dasselbe hinaus. Keines der geprüften
    Länder macht das — weil keines beide Hebel ernsthaft benutzt.
''')

print('[2] EIGENNUTZUNG: FREIBETRAG STATT FREISTELLUNG')
print(f'''    Der Zweck ist benannt: ein Umzug darf nicht zum Armutsrisiko werden.
    Dafür gibt es zwei Instrumente, und sie wirken verschieden.

    FREIBETRAG deckelt die Entlastung. Die USA machen das seit 1997 mit
      250.000 USD für Alleinstehende und 500.000 für Verheiratete; die OECD
      empfiehlt in "Housing Taxation in OECD Countries" ausdrücklich, die
      Freistellung des Hauptwohnsitzes zu DECKELN, damit die höchsten
      Gewinne erfasst werden. 29 von 38 Staaten stellen bisher ganz frei.
    ERSATZBESCHAFFUNG löst das Umzugsproblem direkter. Zürich schiebt die
      Steuer auf, wenn der Erlös binnen zwei Jahren in ein neues
      selbstgenutztes Objekt geht — voll bei vollständiger Reinvestition,
      anteilig sonst, kein Aufschub, wenn das Ersatzobjekt weniger kostet
      als der Einstandspreis des alten. Beim späteren Verkauf ohne Ersatz
      wird der GESAMTE aufgelaufene Gewinn versteuert.

    Der Unterschied ist entscheidend: der Freibetrag verschenkt den Zuwachs,
    die Ersatzbeschaffung verschiebt ihn nur. Wer umzieht, zahlt nichts; wer
    aussteigt und das Geld mitnimmt, zahlt. Das trifft genau Ihr Ziel und
    kostet den Staat nichts — dieselbe Logik wie die Stundung in Position 03.
''')

print('[3] AUFKOMMEN JE FREIBETRAG, Eigennutzung mit Ersatzbeschaffung')
print(f'''    Annahmen: Gewinnanteil {de(GEWINN_ANT*100,0)} % des Verkaufspreises, {de(SELBST*100,0)} % der Fälle
    selbstgenutzt, {de(KURZ*100,0)} % binnen zehn Jahren verkauft (heute steuerpflichtig).
    Durchschnittlicher Verkaufspreis {de(UMSATZ*1e9/FAELLE,0)} EUR.
''')
schnitt = UMSATZ * 1e9 / FAELLE
gewinn_schnitt = schnitt * GEWINN_ANT
print(f'      Durchschnittlicher Gewinn je Fall {de(gewinn_schnitt,0)} EUR')
print(f'\n{"Freibetrag":>13}{"Anteil Fälle frei":>20}{"Basis selbstgen.":>19}'
      f'{"Aufkommen davon":>18}{"zusammen mit Rest":>20}')
rest_basis = UMSATZ * (1 - SELBST) * GEWINN_ANT        # nicht selbstgenutzt
heute = UMSATZ * KURZ * (1 - SELBST) * GEWINN_ANT * SATZ_HEUTE
# Gewinne je Fall als Lognormal um den Schnitt, sigma aus Marktstreuung gesetzt
sig = 0.9
mu = np.log(max(gewinn_schnitt, 1)) - sig**2/2
rng = np.random.default_rng(28)
stich = rng.lognormal(mu, sig, 400_000)
for fb in (0, 50_000, 100_000, 200_000, 500_000):
    ueber = np.maximum(stich - fb, 0)
    anteil_frei = (stich <= fb).mean()
    faktor = ueber.sum() / stich.sum()
    basis_s = UMSATZ * SELBST * GEWINN_ANT * faktor
    ges = (basis_s + rest_basis) * SATZ - heute
    print(f'{de(fb,0):>13}{de(anteil_frei*100,1)+" %":>20}{de(basis_s,1)+" Mrd":>19}'
          f'{de(basis_s*SATZ,1)+" Mrd":>18}{pm(ges,1)+" Mrd":>20}')
print(f'''
    Gegengerechnet ist überall die Satzwirkung: die heute schon
    steuerpflichtigen Fälle fallen von rund {de(SATZ_HEUTE*100,0)} auf {de(SATZ*100,0)} %, das sind
    −{de(heute - UMSATZ*KURZ*(1-SELBST)*GEWINN_ANT*SATZ,1)} Mrd EUR.

    Die Verteilung der Gewinne je Fall ist gesetzt (Lognormal, sigma {de(sig,1)}),
    nicht erhoben. Sie entscheidet, wie stark ein Freibetrag greift, und
    gehört zu den Dingen, die nur die Kaufpreissammlungen der
    Gutachterausschüsse hergeben. Die Spalte ist als Ordnung zu lesen.
''')
print('''[4] WAS DARAUS FOLGT — VORSCHLAG

    Position 04 wird zweiteilig, der Grundsatz bleibt einer:

    04a  Grundsteuer nur auf den Boden, auf regelmässig neu bewerteten
         Werten. Neubewertung alle zwei Jahre, Ansatz unter dem
         Bewertungswert (dänisches Vorsichtsprinzip), Satz aufkommens-
         neutral zur heutigen Grundsteuer. Der Zuwachs wird erfasst,
         während er entsteht.
    04b  Veräußerungsgewinne aus Immobilien sind Einkommen, 28 %, OHNE
         Behaltefrist. Die gezahlte Bodenabgabe wird angerechnet.
         Selbstgenutztes Wohnen: Steueraufschub bei Ersatzbeschaffung
         binnen zwei Jahren, dazu ein Freibetrag je Erwerb. Kein Erlass —
         wer aussteigt, zahlt den aufgelaufenen Gewinn.

    Übergang: ein Rabatt für Alteigentümer nach dänischem Muster, der mit
    dem Verkauf endet. Und für die Zahlungsschwachen dieselbe Stundung wie
    in Position 03 — § 154 Abs. 5 BauGB sieht genau das schon vor, wenn dem
    Eigentümer "nicht zugemutet werden kann, die Verpflichtung bei
    Fälligkeit mit eigenen oder fremden Mitteln zu erfüllen".

    Nicht übernommen: die französische Abschmelzung und der Schweizer
    Besitzesdauerrabatt. Beide widersprechen dem Grundsatz. Übernommen vom
    Schweizer Modell wird nur der ZUSCHLAG für kurze Haltedauer, der echte
    Spekulation trifft, und die Ersatzbeschaffung.''')
