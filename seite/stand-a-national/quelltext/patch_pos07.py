# -*- coding: utf-8 -*-
"""Position 07: Preispfad als europäische Forderung, nicht als nationale Setzung.

GRUND
  § 10 Abs. 3 Satz 2 Nr. 4 BEHG in der Fassung des Dritten Änderungsgesetzes:
  ab 2028 marktbasierter Preis nach dem Durchschnitt der EU-ETS-1-Ver-
  steigerungen. Der nationale Brennstoffemissionshandel geht in den ETS 2
  über. Ein national gesetzter Preis von 100 oder 150 EUR ist dann nicht
  mehr möglich.

BELEGSTAND
  Position 07 wechselt von Stufe 0 (offen) auf Stufe 2 (Größenordnung):
  Menge und Preis bis 2027 stehen im Gesetz, der Pfad danach ist ein
  europäischer Marktpreis, und der Subventionsteil bleibt offen.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, 'lang')

T = {
'de': dict(
 p07r='Europäischer Preispfad · Rückgabe über die Dividende',
 p07p='Ab 2028 bildet den CO₂-Preis der europäische Emissionshandel, nicht der Bundestag. '
   '28:28 setzt deshalb keinen nationalen Preis, sondern fordert einen gemeinsamen Pfad '
   'entlang der vereinbarten Klimaziele – das ist eine Aufgabe des Klubs. Die Erlöse fließen '
   'über die Dividende zurück: Wer wenig verbraucht, gewinnt. Steuervorteile für fossile '
   'Nutzung entfallen.',
 ev_g7='Eigene Rechnung auf dem Dritten BEHG-Änderungsgesetz. § 44 Abs. 2 legt die '
   'Emissionsmengen bis 2030 fest: 301,0 → 180,6 Mio. Tonnen, −40 %. § 10 Abs. 2 Satz 4 setzt '
   'für 2026 und 2027 einen Preiskorridor von 55 bis 65 €. Aufkommen im nationalen '
   'Brennstoffemissionshandel 2026 damit 13,9 bis 16,4 Mrd. €. Ab 2028 bildet den Preis der '
   'europäische Emissionshandel — ein national gesetzter Pfad ist dann nicht mehr möglich, '
   'daher die europäische Fassung. Offen bleibt der Subventionsabbau: von den 65,4 Mrd. € des '
   'Umweltbundesamts (Datenjahr 2018) wären rund 47 aufkommenswirksam, 12,7 sind Entlastungen '
   'im Strompreis, die den Haushalt nie erreichen — und mehrere Posten sind seither entfallen.',
 ev_lede='Welche Zahl worauf beruht, Position für Position. Vier Stufen: aus amtlicher '
   'Quelle gerechnet; eigene Rechnung mit Näherung; aus Verteilungsannahmen gerechnet; '
   'nicht gerechnet. Heute sind zwei Zeilen belegt, zwei offen. Jede neue '
   'Rechnung verschiebt eine Zeile.'),
'en': dict(
 p07r='European price path · returned through the dividend',
 p07p='From 2028 the carbon price is set by European emissions trading, not by the German '
   'parliament. 28:28 therefore sets no national price but calls for a common path along the '
   'agreed climate targets – a task for the club. The proceeds come back through the dividend: '
   'those who consume little gain. Tax breaks for fossil use end.',
 ev_g7='Own calculation on the Third Act amending the German Fuel Emissions Trading Act. § 44(2) '
   'fixes the emission volumes to 2030: 301.0 → 180.6 m tonnes, −40 %. § 10(2) sentence 4 sets a '
   'price corridor of 55 to 65 € for 2026 and 2027. Revenue from national fuel emissions trading '
   'in 2026 is therefore 13.9 to 16.4 bn €. From 2028 the price is set by European emissions '
   'trading — a nationally set path is then no longer possible, hence the European wording. The '
   'removal of subsidies stays open: of the 65.4 bn € reported by the Federal Environment Agency '
   '(data year 2018) about 47 would raise revenue, 12.7 are electricity-price reliefs that never '
   'reach the budget — and several items have since lapsed.',
 ev_lede='What each figure rests on, position by position. Four levels: computed from an '
   'official source; own calculation with an approximation; computed from distributional '
   'assumptions; not computed. Today two rows are substantiated and two are open. '
   'Every new calculation moves a row.'),
'fr': dict(
 p07r='Trajectoire de prix européenne · restituée par le dividende',
 p07p='À partir de 2028, le prix du carbone est fixé par le marché européen des quotas, non par '
   'le parlement allemand. 28:28 ne fixe donc aucun prix national mais demande une trajectoire '
   'commune alignée sur les objectifs climatiques convenus – une tâche pour le club. Les recettes '
   'reviennent par le dividende : qui consomme peu y gagne. Les avantages fiscaux pour les '
   'énergies fossiles disparaissent.',
 ev_g7='Calcul propre sur la troisième loi modifiant la loi allemande sur l’échange de quotas '
   'pour les combustibles. L’article 44(2) fixe les volumes d’émissions jusqu’en 2030 : '
   '301,0 → 180,6 Mt, −40 %. L’article 10(2) phrase 4 fixe un corridor de prix de 55 à 65 € pour '
   '2026 et 2027. Les recettes du système national s’élèvent donc à 13,9 à 16,4 Md€ en 2026. À '
   'partir de 2028, le prix est fixé par le marché européen — une trajectoire nationale n’est '
   'alors plus possible, d’où la formulation européenne. La suppression des subventions reste '
   'ouverte : sur les 65,4 Md€ recensés par l’Agence fédérale de l’environnement (année 2018), '
   'environ 47 produiraient des recettes, 12,7 sont des allègements du prix de l’électricité qui '
   'n’atteignent jamais le budget — et plusieurs postes ont depuis disparu.',
 ev_lede='Sur quoi repose chaque chiffre, position par position. Quatre niveaux : calculé à '
   'partir d\'une source officielle ; calcul propre avec approximation ; calculé à partir '
   'd\'hypothèses de répartition ; non calculé. Aujourd\'hui deux lignes sont étayées '
   'et deux sont ouvertes. Chaque nouveau calcul déplace une ligne.'),
'es': dict(
 p07r='Senda de precios europea · devuelta por el dividendo',
 p07p='Desde 2028 el precio del CO₂ lo fija el comercio europeo de derechos, no el parlamento '
   'alemán. Por eso 28:28 no establece un precio nacional, sino que reclama una senda común '
   'alineada con los objetivos climáticos acordados: una tarea del club. Los ingresos vuelven a '
   'través del dividendo: quien consume poco, gana. Las ventajas fiscales para el uso fósil '
   'desaparecen.',
 ev_g7='Cálculo propio sobre la tercera ley de modificación de la ley alemana de comercio de '
   'emisiones de combustibles. El § 44(2) fija los volúmenes de emisión hasta 2030: '
   '301,0 → 180,6 millones de toneladas, −40 %. El § 10(2) frase 4 establece un corredor de '
   'precios de 55 a 65 € para 2026 y 2027. La recaudación del sistema nacional en 2026 es por '
   'tanto de 13,9 a 16,4 mil millones €. Desde 2028 el precio lo fija el mercado europeo: una '
   'senda nacional ya no es posible, de ahí la formulación europea. La supresión de subvenciones '
   'queda abierta: de los 65,4 mil millones € de la Agencia Federal de Medio Ambiente (año 2018) '
   'unos 47 generarían ingresos, 12,7 son alivios en el precio de la electricidad que nunca '
   'llegan al presupuesto, y varias partidas han decaído desde entonces.',
 ev_lede='En qué se basa cada cifra, posición por posición. Cuatro niveles: calculado a '
   'partir de una fuente oficial; cálculo propio con aproximación; calculado a partir de '
   'supuestos de distribución; no calculado. Hoy dos filas están acreditadas y '
   'dos están abiertas. Cada nuevo cálculo mueve una fila.'),
'nl': dict(
 p07r='Europees prijspad · teruggave via het dividend',
 p07p='Vanaf 2028 bepaalt de Europese emissiehandel de CO₂-prijs, niet de Duitse Bondsdag. '
   '28:28 stelt daarom geen nationale prijs vast, maar vraagt om een gemeenschappelijk pad langs '
   'de afgesproken klimaatdoelen – een taak van de club. De opbrengsten komen terug via het '
   'dividend: wie weinig verbruikt, wint. Belastingvoordelen voor fossiel gebruik vervallen.',
 ev_g7='Eigen berekening op de derde wijzigingswet van de Duitse wet op de emissiehandel voor '
   'brandstoffen. § 44(2) legt de emissiehoeveelheden tot 2030 vast: 301,0 → 180,6 mln ton, '
   '−40 %. § 10(2) zin 4 stelt voor 2026 en 2027 een prijscorridor van 55 tot 65 € vast. De '
   'opbrengst van het nationale systeem bedraagt in 2026 dus 13,9 tot 16,4 mld €. Vanaf 2028 '
   'bepaalt de Europese emissiehandel de prijs — een nationaal pad is dan niet meer mogelijk, '
   'vandaar de Europese formulering. De afbouw van subsidies blijft open: van de 65,4 mld € van '
   'het Duitse Milieuagentschap (datajaar 2018) zou ongeveer 47 opbrengst geven, 12,7 zijn '
   'verlichtingen in de elektriciteitsprijs die de begroting nooit bereiken — en meerdere posten '
   'zijn sindsdien vervallen.',
 ev_lede='Waarop elk cijfer rust, positie voor positie. Vier niveaus: berekend uit een '
   'officiële bron; eigen berekening met benadering; berekend uit verdelingsaannames; niet '
   'berekend. Vandaag zijn twee regels onderbouwd en twee open. Elke nieuwe '
   'berekening verschuift een regel.'),
'da': dict(
 p07r='Europæisk prisspor · tilbageført gennem udbyttet',
 p07p='Fra 2028 fastsættes CO₂-prisen af den europæiske kvotehandel, ikke af den tyske forbundsdag. '
   '28:28 fastsætter derfor ingen national pris, men kræver et fælles spor langs de aftalte '
   'klimamål – en opgave for klubben. Indtægterne vender tilbage gennem udbyttet: den der '
   'forbruger lidt, vinder. Skattefordele for fossil anvendelse bortfalder.',
 ev_g7='Egen beregning på den tredje ændringslov til den tyske lov om kvotehandel med brændstoffer. '
   '§ 44(2) fastlægger emissionsmængderne frem til 2030: 301,0 → 180,6 mio. ton, −40 %. '
   '§ 10(2) punktum 4 fastsætter et priskorridor på 55 til 65 € for 2026 og 2027. Provenuet i det '
   'nationale system udgør dermed 13,9 til 16,4 mia. € i 2026. Fra 2028 fastsættes prisen af den '
   'europæiske kvotehandel — et nationalt spor er da ikke længere muligt, deraf den europæiske '
   'formulering. Afviklingen af subsidier er fortsat åben: af de 65,4 mia. € fra det tyske '
   'miljøagentur (dataår 2018) ville omkring 47 give provenu, 12,7 er lettelser i elprisen, der '
   'aldrig når budgettet — og flere poster er siden bortfaldet.',
 ev_lede='Hvad hvert tal hviler på, position for position. Fire niveauer: beregnet ud fra en '
   'officiel kilde; egen beregning med tilnærmelse; beregnet ud fra fordelingsantagelser; '
   'ikke beregnet. I dag er to rækker dokumenteret, og to er åbne. Hver ny beregning '
   'flytter en række.'),
'sl': dict(
 p07r='Evropska cenovna pot · vračilo prek dividende',
 p07p='Od leta 2028 ceno CO₂ določa evropska trgovina z emisijami, ne nemški parlament. 28:28 zato '
   'ne določa nacionalne cene, ampak zahteva skupno pot ob dogovorjenih podnebnih ciljih – to je '
   'naloga kluba. Prihodki se vrnejo prek dividende: kdor malo porabi, pridobi. Davčne ugodnosti '
   'za fosilno rabo odpadejo.',
 ev_g7='Lastni izračun na tretjem zakonu o spremembi nemškega zakona o trgovanju z emisijami goriv. '
   '§ 44(2) določa količine emisij do leta 2030: 301,0 → 180,6 milijona ton, −40 %. § 10(2) '
   'četrti stavek določa cenovni koridor 55 do 65 € za leti 2026 in 2027. Prihodek nacionalnega '
   'sistema v letu 2026 tako znaša 13,9 do 16,4 milijarde €. Od leta 2028 ceno določa evropska '
   'trgovina z emisijami — nacionalna pot takrat ni več mogoča, od tod evropska formulacija. '
   'Odprava subvencij ostaja odprta: od 65,4 milijarde € nemške agencije za okolje (podatki 2018) '
   'bi jih približno 47 prineslo prihodek, 12,7 so olajšave pri ceni elektrike, ki proračuna '
   'nikoli ne dosežejo — in več postavk je od tedaj odpadlo.',
 ev_lede='Na čem temelji posamezna številka, postavka za postavko. Štiri ravni: izračunano iz '
   'uradnega vira; lastni izračun z približkom; izračunano iz predpostavk o porazdelitvi; ni '
   'izračunano. Danes sta dokazani dve vrstici, dve sta odprti. Vsak nov izračun '
   'premakne eno vrstico.'),
'et': dict(
 p07r='Euroopa hinnarada · tagastus dividendi kaudu',
 p07p='Alates 2028. aastast kujundab CO₂ hinna Euroopa heitkogustega kauplemine, mitte Saksamaa '
   'parlament. 28:28 ei sea seetõttu riiklikku hinda, vaid nõuab ühist rada kokkulepitud '
   'kliimaeesmärkide järgi – see on klubi ülesanne. Tulud tulevad tagasi dividendi kaudu: kes '
   'vähe tarbib, võidab. Maksusoodustused fossiilsele kasutusele kaovad.',
 ev_g7='Oma arvutus Saksamaa kütuse heitkogustega kauplemise seaduse kolmanda muutmisseaduse alusel. '
   '§ 44 lg 2 määrab heitkogused aastani 2030: 301,0 → 180,6 miljonit tonni, −40 %. § 10 lg 2 '
   'neljas lause sätestab aastateks 2026 ja 2027 hinnakoridori 55 kuni 65 €. Riikliku süsteemi '
   'tulu 2026. aastal on seega 13,9 kuni 16,4 miljardit €. Alates 2028 kujundab hinna Euroopa '
   'heitkogustega kauplemine — riiklik rada ei ole siis enam võimalik, sellest ka euroopalik '
   'sõnastus. Toetuste kaotamine jääb lahtiseks: Saksamaa keskkonnaameti 65,4 miljardist eurost '
   '(andmeaasta 2018) annaks tulu umbes 47, 12,7 on elektrihinna soodustused, mis eelarveni kunagi '
   'ei jõua — ja mitu kirjet on vahepeal kadunud.',
 ev_lede='Millele iga arv tugineb, positsioon positsiooni haaval. Neli taset: arvutatud '
   'ametlikust allikast; oma arvutus lähendusega; arvutatud jaotuseelduste põhjal; ei ole '
   'arvutatud. Täna on kaks rida tõendatud ja kaks on lahtised. Iga uus arvutus '
   'nihutab ühte rida.'),
}

for code, ex in T.items():
    p = os.path.join(L, code + '.json')
    d = json.load(open(p, encoding='utf-8'))
    d.update(ex)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(f'  {code}.json: p07r, p07p, ev_g7, ev_lede')

# Belegstand: Position 07 von Stufe 0 auf 2
b = open(os.path.join(HERE, 'build.py'), encoding='utf-8').read()
alt = "('p07pos', 'p07t', 0, 'ev_g7')"
assert alt in b, 'Belegzeile 07 nicht gefunden'
open(os.path.join(HERE, 'build.py'), 'w', encoding='utf-8').write(
    b.replace(alt, "('p07pos', 'p07t', 2, 'ev_g7')", 1))
print('  build.py: Position 07 auf Stufe 2')

# Anhang (nur de und en führen src_text)
ANH = {
 'de': ('  CO₂-Preis 100 → 150 € je Tonne',
        '''  CO₂: kein national gesetzter Preis. Mengen nach § 44 Abs. 2 BEHG
    (Drittes Änderungsgesetz): 2026 252,4 Mio t, 2030 180,6 Mio t.
    Preiskorridor § 10 Abs. 2 S. 4: 55 bis 65 EUR für 2026 und 2027.
    Ab 2028 marktbasierter Preis nach dem EU-ETS-1-Durchschnitt
    (§ 10 Abs. 3 S. 2 Nr. 4); Übergang in den ETS 2, dessen Start die
    Verordnung (EU) 2026/667 um ein Jahr verschoben hat. Der Preispfad
    ist deshalb eine europäische Forderung, keine nationale Setzung.
    Klimaschädliche Subventionen: UBA 2021, Datenjahr 2018, Summe
    65,4 Mrd EUR, davon aufkommenswirksam rund 47; 12,7 sind
    Entlastungen im Strompreis ohne Haushaltswirkung.'''),
 'en': ('  Carbon price 100 → 150 € a tonne',
        '''  Carbon: no nationally set price. Volumes under § 44(2) of the Fuel
    Emissions Trading Act (third amending act): 252.4 m t in 2026,
    180.6 m t in 2030. Price corridor under § 10(2) sentence 4: 55 to
    65 EUR for 2026 and 2027. From 2028 a market-based price following
    the EU ETS 1 average (§ 10(3) sentence 2 no. 4); transition into
    ETS 2, whose start Regulation (EU) 2026/667 postponed by a year.
    The price path is therefore a European demand, not a national one.
    Climate-damaging subsidies: Federal Environment Agency 2021, data
    year 2018, total 65.4 bn EUR, of which about 47 would raise revenue;
    12.7 are electricity-price reliefs with no budget effect.'''),
}
for code, (alt_a, neu_a) in ANH.items():
    p = os.path.join(L, code + '.json')
    d = json.load(open(p, encoding='utf-8'))
    if alt_a in d.get('src_text', ''):
        d['src_text'] = d['src_text'].replace(alt_a, neu_a, 1)
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        print(f'  {code}.json: Anhang CO₂ ersetzt')
    else:
        i = d.get('src_text', '').find('CO₂' if code == 'de' else 'arbon')
        print(f'  ! {code}: Ankerzeile nicht gefunden. Umfeld: '
              f'{d.get("src_text","")[max(0,i-60):i+90]!r}')
