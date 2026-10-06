# -*- coding: utf-8 -*-
"""
R5b — Position 04, zweiter Teil: "Grundsteuer nur auf den Boden"

WAS POSITION 04 WIRKLICH SAGT
  Nicht "eine zusätzliche Abgabe auf Boden", sondern: die Grundsteuer
  richtet sich nur noch nach dem Wert des Grundstücks, nicht nach dem
  Gebäude darauf. Das ist ein UMBAU bei gleichem Aufkommen, kein neuer
  Steuerposten. Die interessante Größe ist deshalb nicht das Aufkommen,
  sondern der Satz, der es trägt — und die Verschiebung zwischen den
  Zahlenden.

QUELLEN
  Bodenwert: Statistisches Bundesamt, WISTA 6/2015, "Grund und Boden als
    Bestandteil der volkswirtschaftlichen Vermögensbilanzen".
    Projektrechnung auf Basis der Bodenrichtwerte der Gutachterausschüsse,
    verknüpft mit der Flächenstatistik über den Gemeindeschlüssel.
  Grundsteueraufkommen: Statistisches Bundesamt, Pressemitteilung
    PD25_N006_73 vom Februar 2025.

DIE GRENZE DIESER RECHNUNG
  Der Bodenwert ist für 2014 belegt. Für 2026 brauchte es einen
  Preisindex für Bauland, den ich hier nicht habe. Deshalb steht unten
  kein Punktwert, sondern der Satz als Funktion des Bodenwerts.
"""
import numpy as np

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# Destatis WISTA 6/2015, Mrd EUR
BODEN = {2011: 3104.3, 2012: 3198.6, 2014: 3529.0}
SIEDL = {2011: 2713.4, 2012: 2791.5, 2014: 3021.0}
STRUKTUR_2012 = [('Siedlungs- und Verkehrsfläche zu Wohnbauten', 2096.4),
                 ('Siedlungs- und Verkehrsfläche zu Nichtwohnbauten', 695.1),
                 ('Landwirtschafts- und Waldfläche', 395.1),
                 ('Flächen anderer Nutzung', 11.9)]
GRUNDSTEUER_2023 = 15.5      # Mrd EUR, Destatis

print('=' * 90)
print('R5b — "GRUNDSTEUER NUR AUF DEN BODEN"')
print('=' * 90)

print('\n[1] DER WERT DES BODENS, amtlich gerechnet')
print(f'{"Jahr":>6}{"Grund und Boden":>20}{"davon bebaut":>16}{"Anteil":>9}')
for j in sorted(BODEN):
    print(f'{j:>6}{de(BODEN[j],1)+" Mrd":>20}{de(SIEDL[j],1)+" Mrd":>16}'
          f'{de(SIEDL[j]/BODEN[j]*100):>8} %')
print(f'\n    Struktur 2012:')
ges = sum(v for _, v in STRUKTUR_2012)
for name, v in STRUKTUR_2012:
    print(f'      {name:<48}{de(v,1):>9} Mrd{de(v/ges*100):>8} %')
print(f'\n    Das Entscheidende steht in der Gegenüberstellung von Fläche und Wert:')
print(f'    Landwirtschaft und Wald sind 83 % der FLÄCHE, aber rund 12 % des WERTS.')
print(f'    Siedlungs- und Verkehrsfläche ist 17 % der Fläche und 87 % des Werts.')
print(f'    Eine Bodenwertsteuer trifft deshalb die Städte, nicht die Felder.')

print('\n[2] WELCHER SATZ TRÄGT DAS HEUTIGE AUFKOMMEN?')
print(f'    Grundsteuer 2023: {de(GRUNDSTEUER_2023,1)} Mrd EUR (Destatis).')
print(f'    Der Satz, der dieses Aufkommen allein aus dem Bodenwert holt:')
print(f'{"Bodenwert":>16}{"Satz":>10}{"entspricht":>28}')
for faktor, etikett in [(1.0, 'Stand 2014, unverändert'),
                        (1.3, 'Bodenwert +30 % seit 2014'),
                        (1.6, 'Bodenwert +60 % seit 2014'),
                        (2.0, 'Bodenwert verdoppelt')]:
    bw = BODEN[2014] * faktor
    satz = GRUNDSTEUER_2023 / bw * 100
    print(f'{de(bw,0)+" Mrd":>16}{de(satz,3)+" %":>10}{etikett:>28}')
print(f'\n    Die Grössenordnung ist stabil: ein halbes Promille bis gut vier')
print(f'    Promille des Bodenwerts. Zum Vergleich: die heutige Grundsteuer')
print(f'    entspricht rund {de(GRUNDSTEUER_2023/BODEN[2014]*100,3)} % des Bodenwerts von 2014.')

print('\n[3] WAS SICH VERSCHIEBT')
print('''    Bei gleichem Aufkommen gibt es Gewinner und Verlierer, und sie sind
    vorhersagbar:
      mehr zahlen   teures Grundstück, wenig darauf — Baulücken, Parkplätze,
                    flache Bebauung in guter Lage, gehortete Grundstücke
      weniger zahlen teures Gebäude auf billigem Boden — Neubau im Umland,
                    hochwertig saniertes Objekt in mittlerer Lage
    Das ist der eigentliche Zweck: wer Boden in guter Lage hält, ohne ihn
    zu nutzen, zahlt künftig dafür. Die Höhe dieser Verschiebung lässt sich
    aus aggregierten Daten NICHT beziffern — dafür bräuchte es die
    Einzeldaten der Grundsteuerwertestatistik.''')

print('\n[4] WARUM DIE GRUNDSTEUERWERTE DIE RECHNUNG NICHT TRAGEN')
print('''    Naheliegend wäre, die 35,4 Millionen wirtschaftlichen Einheiten der
    neuen Grundsteuerwertestatistik aufzusummieren. Das geht nicht:

      - Die Statistik ist "durch die Öffnungsklausel KEINE einheitliche
        Bundesstatistik des Grundvermögens" (Destatis, WISTA 5/2025).
        Die Länder rechnen nach verschiedenen Modellen; Bayern, Hamburg,
        Niedersachsen und Hessen nach Flächenmodellen, die überhaupt
        keinen Wert erzeugen. Baden-Württemberg nutzt ein reines
        Bodenwertmodell und meldet deshalb ALLE Grundstücke als unbebaut.
      - Die veröffentlichten Ergebnisse beruhen ausdrücklich auf
        "nicht plausibilisierten Daten".
      - Aggregierte Grundsteuerwerte werden in dem Aufsatz gar nicht
        ausgewiesen, nur Fallzahlen und Anteile.

    Das ist kein Mangel des Entwurfs, sondern der Datenlage. Es ändert
    sich: mit dem Jahressteuergesetz 2024 wurde der Erhebungskreis
    erweitert, und Grundsteuerwerte lassen sich künftig mit der Lohn- und
    Einkommensteuer sowie der Erbschaftsteuer auf Personenebene
    verknüpfen. Dann wäre die Verschiebung aus Abschnitt 3 rechenbar.''')

print('\n[5] EIN BELEG, DER AUF DER SEITE SCHON STEHT')
print('''    Position 04 verweist darauf, dass Baden-Württemberg die Grundsteuer
    bereits nach dem Bodenwert erhebt. Die Grundsteuerwertestatistik
    bestätigt das aus der Verwaltungspraxis: Baden-Württemberg meldet
    86 % unbebaute Grundstücke, weil das Bodenwertmodell nicht zwischen
    bebaut und unbebaut unterscheidet. Das Modell ist also kein Entwurf,
    sondern geltendes Landesrecht in einem Flächenland mit 11 Millionen
    Einwohnern.''')

print(f'''
[6] WAS NOCH FEHLT
    - Ein Preisindex für Bauland, um den Bodenwert von 2014 auf 2026
      fortzuschreiben. Erst dann wird aus der Satzformel eine Zahl.
    - Die sektorale Aufteilung des Bodenwerts: wie viel entfällt auf
      private Haushalte, Unternehmen, den Staat. Der Aufsatz beschreibt
      das Verfahren, die Tabelle liegt mir nicht vor.
    - Die Entscheidung, ob land- und forstwirtschaftlicher Boden
      ({de(STRUKTUR_2012[2][1],1)} Mrd EUR, {de(STRUKTUR_2012[2][1]/ges*100)} % des Werts)
      einbezogen wird. Das ist eine Entwurfsfrage, keine Rechenfrage.''')
