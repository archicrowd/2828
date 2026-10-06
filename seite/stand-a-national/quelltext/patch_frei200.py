# -*- coding: utf-8 -*-
"""Freibetrag in Position 03 von 400.000 auf 200.000 EUR je Erwerb.

ZWEI ÄNDERUNGEN AUF EINMAL, beide ausdrücklich:
  1. Höhe: 400.000 -> 200.000 EUR. Aufkommen 16,54 -> 20,98 Mrd EUR
     (exakte Klassengrenze der amtlichen Statistik, keine Interpolation).
  2. Bezug: "je Kind" -> "je Erwerb". Alle bisherigen Rechnungen unterstellen
     einen einheitlichen Betrag für jede erbende Person. Heute sind es
     500.000 für Ehegatten, 400.000 für Kinder, 200.000 für Enkel und
     20.000 für alle übrigen; Steuerklasse II und III sind 76,7 % der
     Erbfälle. Für sie bleibt auch der halbierte Betrag das Zehnfache
     des heutigen.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, 'lang')

P03R = {
 'de': '28 % über 200.000 € je Erwerb',
 'en': '28 % above 200,000 € per acquisition',
 'fr': '28 % au-delà de 200 000 € par transmission',
 'es': '28 % por encima de 200.000 € por adquisición',
 'nl': '28 % boven 200.000 € per verkrijging',
 'da': '28 % over 200.000 € pr. erhvervelse',
 'sl': '28 % nad 200.000 € na pridobitev',
 'et': '28 % üle 200 000 € omandamise kohta',
}
FREI = {
 'de': 'Unter dem Freibetrag von 200.000 € — keine Steuer.',
 'en': 'Below the allowance of 200,000 € — no tax.',
 'fr': 'En dessous de l’abattement de 200 000 € — pas d’impôt.',
 'es': 'Por debajo del mínimo exento de 200.000 € — sin impuesto.',
 'nl': 'Onder de vrijstelling van 200.000 € — geen belasting.',
 'da': 'Under bundfradraget på 200.000 € — ingen skat.',
 'sl': 'Pod olajšavo 200.000 € — brez davka.',
 'et': 'Alla 200 000 € maksuvaba summa — maksu ei ole.',
}
# Im Kleingedruckten unter dem Rechner nur die Zahl austauschen
FINE_ALT = ['400.000 €', '400,000 €', '400 000 €']
FINE_NEU = {'de': '200.000 €', 'en': '200,000 €', 'fr': '200 000 €', 'es': '200.000 €',
            'nl': '200.000 €', 'da': '200.000 €', 'sl': '200.000 €', 'et': '200 000 €'}

EV3 = {
 'de': 'Eigene Auswertung der amtlichen Erbschaft- und Schenkungsteuerstatistik 2024 '
   '(245.540 Erwerbe, 113,2 Mrd. €). Wer 150.000 € erbt, zahlt effektiv 13,5 %; wer 15 Mio. € '
   'erbt, 9,6 % — in dieser Klasse werden 61,9 % des Erwerbs verschont. Die Verschonung des '
   'Betriebsvermögens erfasst 79,4 % des übertragenen Betriebsvermögens und kostet 3,9 bis '
   '5,1 Mrd. € im Jahr. Position 03 brächte 20,98 Mrd. € statt 13,28, also +7,7 Mrd. € — '
   'gerechnet auf einer exakten Klassengrenze der amtlichen Statistik. Die Verschonung wird '
   'durch eine Stundung ersetzt: der Staat verliert dabei nichts, der Verzicht beschränkt sich '
   'auf die Bankmarge der ersten Jahre und beträgt rund 0,7 Mrd. €.',
 'en': 'Own analysis of the official German inheritance and gift tax statistics 2024 '
   '(245,540 acquisitions, 113.2 bn €). An inheritance of 150,000 € is taxed at an effective '
   '13.5 %; one of 15 m € at 9.6 % — in that bracket 61.9 % of the acquisition is exempt. The '
   'business-asset relief covers 79.4 % of all business assets transferred and costs 3.9 to '
   '5.1 bn € a year. Position 03 would raise 20.98 bn € instead of 13.28, that is +7.7 bn € — '
   'computed on an exact class boundary of the official statistics. The exemption is replaced '
   'by a deferral: the state loses nothing, the concession is limited to the bank margin of the '
   'early years and amounts to about 0.7 bn €.',
 'fr': 'Analyse propre de la statistique officielle allemande des droits de succession et de '
   'donation 2024 (245 540 transmissions, 113,2 Md€). Un héritage de 150 000 € est imposé à '
   '13,5 % en taux effectif ; un héritage de 15 M€ à 9,6 % — dans cette tranche, 61,9 % de la '
   'transmission est exonérée. L’exonération des biens d’entreprise couvre 79,4 % des biens '
   'transmis et coûte 3,9 à 5,1 Md€ par an. La position 03 rapporterait 20,98 Md€ au lieu de '
   '13,28, soit +7,7 Md€ — calculé sur une limite de classe exacte de la statistique '
   'officielle. L’exonération est remplacée par un report : l’État ne perd rien, la concession '
   'se limite à la marge bancaire des premières années et représente environ 0,7 Md€.',
 'es': 'Análisis propio de la estadística oficial alemana del impuesto sobre sucesiones y '
   'donaciones de 2024 (245.540 adquisiciones, 113,2 mil millones €). Quien hereda 150.000 € '
   'paga un tipo efectivo del 13,5 %; quien hereda 15 millones, el 9,6 % — en ese tramo se '
   'exonera el 61,9 % de la adquisición. La exención de activos empresariales cubre el 79,4 % '
   'de los transmitidos y cuesta de 3,9 a 5,1 mil millones € al año. La posición 03 recaudaría '
   '20,98 mil millones € en lugar de 13,28, es decir +7,7 — calculado sobre un límite de clase '
   'exacto de la estadística oficial. La exención se sustituye por un aplazamiento: el Estado '
   'no pierde nada, la concesión se limita al margen bancario de los primeros años y asciende '
   'a unos 0,7 mil millones €.',
 'nl': 'Eigen analyse van de officiële Duitse erf- en schenkbelastingstatistiek 2024 '
   '(245.540 verkrijgingen, 113,2 mld €). Wie 150.000 € erft betaalt effectief 13,5 %; wie '
   '15 mln € erft 9,6 % — in die klasse is 61,9 % van de verkrijging vrijgesteld. De '
   'vrijstelling voor ondernemingsvermogen dekt 79,4 % van het overgedragen '
   'ondernemingsvermogen en kost 3,9 tot 5,1 mld € per jaar. Positie 03 zou 20,98 mld € '
   'opbrengen in plaats van 13,28, dus +7,7 mld € — berekend op een exacte klassegrens van de '
   'officiële statistiek. De vrijstelling wordt vervangen door uitstel: de staat verliest '
   'niets, de tegemoetkoming beperkt zich tot de bankmarge van de eerste jaren en bedraagt '
   'ongeveer 0,7 mld €.',
 'da': 'Egen analyse af den officielle tyske arve- og gaveafgiftsstatistik 2024 '
   '(245.540 erhvervelser, 113,2 mia. €). Den der arver 150.000 € betaler effektivt 13,5 %; '
   'den der arver 15 mio. € betaler 9,6 % — i den klasse fritages 61,9 % af erhvervelsen. '
   'Virksomhedslempelsen dækker 79,4 % af den overførte virksomhedsformue og koster 3,9 til '
   '5,1 mia. € om året. Position 03 ville indbringe 20,98 mia. € i stedet for 13,28, altså '
   '+7,7 mia. € — beregnet på en eksakt klassegrænse i den officielle statistik. Lempelsen '
   'erstattes af henstand: staten taber intet, indrømmelsen begrænser sig til bankmarginen i '
   'de første år og udgør omkring 0,7 mia. €.',
 'sl': 'Lastna analiza uradne nemške statistike davka na dediščine in darila 2024 '
   '(245.540 pridobitev, 113,2 milijarde €). Kdor podeduje 150.000 €, plača efektivno 13,5 %; '
   'kdor podeduje 15 milijonov, 9,6 % — v tem razredu je oproščenih 61,9 % pridobitve. '
   'Oprostitev za poslovno premoženje zajema 79,4 % prenesenega poslovnega premoženja in stane '
   '3,9 do 5,1 milijarde € na leto. Postavka 03 bi prinesla 20,98 milijarde € namesto 13,28, '
   'torej +7,7 — izračunano na natančni meji razreda uradne statistike. Oprostitev nadomešča '
   'odlog: država pri tem ne izgubi ničesar, odpoved je omejena na bančno maržo prvih let in '
   'znaša približno 0,7 milijarde €.',
 'et': 'Oma analüüs Saksamaa ametlikust päranditi- ja kinkemaksustatistikast 2024 '
   '(245 540 omandamist, 113,2 miljardit €). Kes pärib 150 000 €, maksab tegelikult 13,5 %; '
   'kes pärib 15 miljonit, 9,6 % — selles klassis on 61,9 % omandamisest vabastatud. Ärivara '
   'soodustus hõlmab 79,4 % üleantud ärivarast ja maksab 3,9 kuni 5,1 miljardit € aastas. '
   'Positsioon 03 tooks 20,98 miljardit € 13,28 asemel, seega +7,7 — arvutatud ametliku '
   'statistika täpsel klassipiiril. Soodustuse asendab ajatamine: riik ei kaota midagi, '
   'loobumine piirdub esimeste aastate pangamarginaaliga ja on umbes 0,7 miljardit €.',
}

for code in P03R:
    p = os.path.join(L, code + '.json')
    d = json.load(open(p, encoding='utf-8'))
    d['p03r'] = P03R[code]
    d['erb_frei'] = FREI[code]
    d['ev_g3'] = EV3[code]
    for a in FINE_ALT:
        d['erb_fine'] = d['erb_fine'].replace(a, FINE_NEU[code])
    if 'src_text' in d:
        for a in FINE_ALT:
            d['src_text'] = d['src_text'].replace('Freibetrag ' + a, 'Freibetrag ' + FINE_NEU[code])
            d['src_text'] = d['src_text'].replace('allowance ' + a.replace('€', '').strip() + ' EUR',
                                                  'allowance 200,000 EUR')
            d['src_text'] = d['src_text'].replace('Freibetrag ' + a.replace('€', 'EUR'),
                                                  'Freibetrag ' + FINE_NEU[code].replace('€', 'EUR'))
        d['src_text'] = d['src_text'].replace('Freibetrag 400.000 EUR', 'Freibetrag 200.000 EUR')
        d['src_text'] = d['src_text'].replace('allowance 400,000 EUR', 'allowance 200,000 EUR')
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(f'  {code}.json: p03r, erb_frei, erb_fine, ev_g3'
          + (', src_text' if 'src_text' in d else ''))

# ------------------------------------------------------------------ tpl.py
tp = os.path.join(HERE, 'tpl.py')
t = open(tp, encoding='utf-8').read()
alt = 'const E={frei:400000,satz:.28,basis:.030,marge:.020,n:10};'
assert alt in t, 'Rechnerparameter nicht gefunden'
t = t.replace(alt, 'const E={frei:200000,satz:.28,basis:.030,marge:.020,n:10};', 1)
alt_r = 'min="100000" max="2000000" step="10000" value="500000"'
assert alt_r in t
t = t.replace(alt_r, 'min="50000" max="2000000" step="10000" value="400000"', 1)
open(tp, 'w', encoding='utf-8').write(t)
print('  tpl.py: Freibetrag 200.000, Schieber ab 50.000, Startwert 400.000')
