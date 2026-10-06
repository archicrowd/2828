# -*- coding: utf-8 -*-
"""
R4b — Position 07, zweiter Teil: "keine klimaschädlichen Subventionen"

QUELLE
  Umweltbundesamt (2021): Umweltschädliche Subventionen in Deutschland.
  Tabelle "Umweltschädliche Subventionen nach Sektor", Datenjahr 2018.
  Summe 65.425 Mio. EUR.

DIE FRAGE, DIE DIE SUMME NICHT BEANTWORTET
  65,4 Mrd. EUR klingt nach Gegenfinanzierung. Aber nur ein Teil davon
  ist Steuer, die bei Abschaffung in den Haushalt fliesst. Ein anderer
  Teil sind Umlagen im Strompreis, die gar nicht beim Staat ankommen,
  und ein dritter sind Ausgaben, deren Wegfall den Haushalt entlastet,
  aber kein Aufkommen erzeugt. Dieses Skript trennt das.

DIE ZUORDNUNG IST EINE SETZUNG
  Sie steht unten offen, Posten für Posten, und ist bestreitbar. Wer
  anders zuordnet, bekommt eine andere Zahl — aber er sieht, wo.
"""
import numpy as np

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# (Posten, Mio EUR 2018, Art)
#   STEUER  Steuervergünstigung: Abbau = Mehreinnahme
#   ZERTI   kostenfreie Zuteilung: Abbau = Versteigerungserlös
#   UMLAGE  Entlastung im Strompreis: Abbau entlastet andere Zahler, nicht den Haushalt
#   AUSGABE Zuschuss oder Programm: Abbau = Minderausgabe, kein Aufkommen
#   UNKLAR  aus der Tabelle nicht eindeutig zuzuordnen
POSTEN = [
 ('Strom- und Energiesteuer-Ermäßigungen produzierendes Gewerbe', 1144, 'STEUER'),
 ('Spitzenausgleich bei der Ökosteuer', 1720, 'STEUER'),
 ('Steuerentlastung für energieintensive Prozesse', 1290, 'STEUER'),
 ('Energiesteuervergünstigung für die Stromerzeugung', 2003, 'STEUER'),
 ('Steinkohlesubventionen', 1263, 'AUSGABE'),
 ('Begünstigungen für die Braunkohlewirtschaft (min.)', 287, 'AUSGABE'),
 ('Energiesteuervergünstigungen für Kohle', 85, 'STEUER'),
 ('Herstellerprivileg', 342, 'STEUER'),
 ('Energiesteuerbefreiung nicht-energetische Nutzung (min.)', 1299, 'STEUER'),
 ('Kostenfreie Zuteilung der CO2-Emissionsberechtigungen', 2134, 'ZERTI'),
 ('Zuschüsse an stromintensive Unternehmen', 219, 'AUSGABE'),
 ('Besondere Ausgleichsregelung des EEG', 5400, 'UMLAGE'),
 ('Eigenstromprivileg des EEG (Industrie)', 3660, 'UMLAGE'),
 ('Begünstigungen der energieintensiven Industrie', 611, 'UNKLAR'),
 ('Privilegierung von Sondervertragskunden bei Netzentgelten', 3600, 'UMLAGE'),
 ('Ermäßigte Sätze für Gewerbe und energieintensive Betriebe', 316, 'UNKLAR'),
 ('Exportkreditgarantien (Hermesdeckungen)', 1, 'AUSGABE'),
 ('Energiesteuervergünstigung für Dieselkraftstoff', 8202, 'STEUER'),
 ('Entfernungspauschale', 6000, 'STEUER'),
 ('Pauschale Besteuerung privat genutzter Dienstwagen (min.)', 3100, 'STEUER'),
 ('Biokraftstoffe', 960, 'STEUER'),
 ('Energiesteuerbefreiung der Binnenschifffahrt (min.)', 141, 'STEUER'),
 ('Energiesteuerbegünstigung von Arbeitsmaschinen', 25, 'STEUER'),
 ('Energiesteuerbefreiung des Kerosins', 8357, 'STEUER'),
 ('Mehrwertsteuerbefreiung für internationale Flüge', 3997, 'STEUER'),
 ('Förderung von Regionalflughäfen (min.)', 40, 'AUSGABE'),
 ('Wohnungsbauprämie', 81, 'AUSGABE'),
 ('Eigenheimrente', 46, 'STEUER'),
 ('Soziale Wohnraumförderung', 1191, 'AUSGABE'),
 ('Baukindergeld', 6, 'AUSGABE'),
 ('KfW-Wohneigentumsprogramm', 1726, 'AUSGABE'),
 ('Steuervergütung für Agrardiesel', 467, 'STEUER'),
 ('Kfz-Steuer-Befreiung landwirtschaftlicher Fahrzeuge', 470, 'STEUER'),
 ('Mehrwertsteuerermäßigung für tierische Produkte (min.)', 5242, 'STEUER'),
]
SUMME_UBA = 65425

ART = {'STEUER': 'Steuervergünstigung — Abbau bringt Aufkommen',
       'ZERTI': 'kostenfreie Zuteilung — Abbau bringt Versteigerungserlös',
       'UMLAGE': 'Entlastung im Strompreis — erreicht den Haushalt nicht',
       'AUSGABE': 'Zuschuss oder Programm — Abbau mindert Ausgaben',
       'UNKLAR': 'aus der Tabelle nicht eindeutig zuzuordnen'}

print('=' * 96)
print('R4b — WAS VON DEN 65,4 MRD EUR KLIMASCHÄDLICHER SUBVENTIONEN AUFKOMMEN WÄRE')
print('=' * 96)

summe = sum(v for _, v, _ in POSTEN)
print(f'\n    Erfasste Posten: {len(POSTEN)}, Summe {de(summe/1000,1)} Mrd EUR.')
print(f'    Das trifft die UBA-Summe von {de(SUMME_UBA/1000,1)} Mrd EUR auf den Euro genau — die')
print(f'    Liste ist also vollständig. Nicht enthalten sind die Posten, die das')
print(f'    Umweltbundesamt als nicht quantifizierbar ausweist und deshalb auch')
print(f'    selbst nicht summiert: EU-Agrar- und Fischereiförderung, Kernenergie,')
print(f'    Kreuzfahrtfinanzierung, Flugsicherheitsgebühren, Arbeitnehmer-Spar-')
print(f'    zulage und die Gemeinschaftsaufgabe regionale Wirtschaftsstruktur.')

print('\n[1] NACH ART DES POSTENS')
print(f'{"Art":>10}{"Mio EUR":>12}{"Anteil":>9}   Bedeutung')
for a in ['STEUER', 'ZERTI', 'UMLAGE', 'AUSGABE', 'UNKLAR']:
    s = sum(v for _, v, k in POSTEN if k == a)
    print(f'{a:>10}{de(s,0):>12}{de(s/summe*100):>8} %   {ART[a]}')

steuer = sum(v for _, v, k in POSTEN if k in ('STEUER', 'ZERTI'))
umlage = sum(v for _, v, k in POSTEN if k == 'UMLAGE')
ausgabe = sum(v for _, v, k in POSTEN if k == 'AUSGABE')
print(f'''
    AUFKOMMENSWIRKSAM wäre der Abbau von {de(steuer/1000,1)} Mrd EUR, nicht {de(SUMME_UBA/1000,1)}.
    {de(umlage/1000,1)} Mrd EUR sind Entlastungen im Strompreis — ihr Abbau verteilt
    zwischen Stromkunden um, er füllt keinen Haushalt. {de(ausgabe/1000,1)} Mrd EUR sind
    Ausgaben; ihr Wegfall entlastet den Haushalt, erzeugt aber kein Aufkommen
    und gehört deshalb nicht in die Gegenfinanzierung einer Steuerreform.''')

print('\n[2] DIE GRÖSSTEN AUFKOMMENSWIRKSAMEN POSTEN')
print(f'{"Posten":<58}{"Mio EUR":>10}')
for name, v, k in sorted([p for p in POSTEN if p[2] in ('STEUER', 'ZERTI')],
                         key=lambda p: -p[1])[:10]:
    print(f'{name[:56]:<58}{de(v,0):>10}')

print('''
[3] WARUM DIE ZAHL TROTZDEM NICHT VERWENDBAR IST

    Datenjahr 2018, veröffentlicht 2021. Seither ist mehreres entfallen
    oder grundlegend geändert worden:
      - Die EEG-Umlage wurde 2022 abgeschafft. Die Besondere Ausgleichs-
        regelung und das Eigenstromprivileg (zusammen 9,1 Mrd EUR) gibt
        es in dieser Form nicht mehr.
      - Der Spitzenausgleich bei der Ökosteuer (1,7 Mrd EUR) ist Ende
        2023 ausgelaufen.
      - Die Steinkohlesubventionen (1,3 Mrd EUR) endeten 2018.
      - Die kostenfreie Zuteilung von CO2-Berechtigungen (2,1 Mrd EUR)
        läuft nach der Reform des EU-Emissionshandels bis 2034 aus; der
        Posten verschwindet also ohnehin.
    Mehrere Posten sind zudem als "min." ausgewiesen, also Untergrenzen.

    Und grundsätzlich: der statische Wert einer Steuervergünstigung ist
    nicht das, was ihr Abbau einbringt. Wer den Dieselsteuersatz anhebt,
    bekommt nicht 8,2 Mrd EUR, weil weniger Diesel getankt wird — was
    hier ja gerade der Zweck ist.

[4] WAS AUF DIE SEITE GEHÖRT
    Nicht "65 Mrd EUR klimaschädliche Subventionen abbauen". Sondern:
    die vier grössten steuerlichen Posten mit Namen und Jahr, als
    Grössenordnung, mit dem Hinweis auf das Datenjahr 2018 — und die
    Feststellung, dass eine aktuelle Fassung fehlt.''')
