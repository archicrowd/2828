# -*- coding: utf-8 -*-
"""Rechner raus, fairer Regeltext rein. Stundung nach Modell B.

MODELL B
  Laufend zu zahlen ist nur der Zins. Der offene Betrag bleibt als Last auf
  dem geerbten Gegenstand und wird bei Verkauf oder Weitergabe fällig.
  Zinsleiter unverändert: Refinanzierungssatz des Staates im ersten Jahr,
  über zehn Jahre steigend auf den marktüblichen Kreditzins.

WARUM DER RECHNER GEHT
  Er setzte die lesende Person in den Stuhl des Zahlenden; jede Zahl war
  eine Belastung für sie. Nach der Halbierung des Freibetrags lieferte er
  Belege gegen die Position, für die er gebaut war.

OHNE RECHENWERTE
  Der neue Text nennt die Regel, keine Beispielbeträge.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, 'lang')

WEG = ['erb_lede', 'erb_lbl', 'erb_r1', 'erb_r2', 'erb_r3', 'erb_r4', 'erb_sub',
       'erb_frei', 'erb_fine', 'erb_aria', 'erb_j1', 'erb_j10', 'erb_raten']

T = {
'de': dict(
 erb_h3='Keine Ausnahme, aber ein fairer Übergang',
 erb_p1='Die heutige Verschonung des Betriebsvermögens wirkt am stärksten dort, wo die größten '
   'Vermögen übergehen. Sie fällt ersatzlos weg. Wer einen Betrieb oder ein Haus erbt, steht '
   'damit vor einer Steuer auf Vermögen, das keine Zahlungsmittel sind.',
 erb_p2='An ihre Stelle tritt eine Stundung. Verzinst wird sie zunächst zu dem Satz, zu dem sich '
   'der Staat selbst refinanziert; über zehn Jahre steigt der Satz auf den marktüblichen '
   'Kreditzins. Laufend zu zahlen ist nur der Zins. Wer auch den nicht tragen kann, dem wird er '
   'dem offenen Betrag zugeschlagen. Dieser bleibt als Last auf dem geerbten Gegenstand und wird '
   'fällig, wenn er verkauft oder weitergegeben wird.',
 erb_p3='Damit muss niemand verkaufen, um die Steuer zu zahlen – und niemandem wird etwas '
   'geschenkt. Erlassen wird nichts, verjähren kann nichts. Die Stundung bleibt eine Stundung.'),
'en': dict(
 erb_h3='No exemption, but a fair transition',
 erb_p1='Today’s relief for business assets works most strongly where the largest fortunes change '
   'hands. It is abolished outright. Anyone inheriting a business or a home therefore faces a tax '
   'on assets that are not cash.',
 erb_p2='A deferral takes its place. Interest runs at first at the rate at which the state '
   'refinances itself; over ten years it rises to the market lending rate. Only the interest is '
   'payable as it falls due. For anyone who cannot carry even that, it is added to the outstanding '
   'balance. That balance stays as a charge on the inherited asset and falls due when the asset is '
   'sold or passed on.',
 erb_p3='So nobody has to sell in order to pay the tax – and nobody is given anything. Nothing is '
   'written off, nothing can lapse. The deferral stays a deferral.'),
'fr': dict(
 erb_h3='Aucune exonération, mais une transition équitable',
 erb_p1='L’exonération actuelle des biens d’entreprise agit le plus fortement là où passent les '
   'plus grandes fortunes. Elle disparaît purement et simplement. Qui hérite d’une entreprise ou '
   'd’un logement fait donc face à un impôt sur des biens qui ne sont pas des liquidités.',
 erb_p2='Un report prend sa place. Il porte d’abord intérêt au taux auquel l’État se refinance ; '
   'sur dix ans, ce taux monte jusqu’au taux du crédit de marché. Seuls les intérêts sont exigibles '
   'au fil du temps. Pour qui ne peut même pas les porter, ils s’ajoutent au solde. Celui-ci reste '
   'une charge sur le bien hérité et devient exigible lors de sa vente ou de sa transmission.',
 erb_p3='Ainsi personne n’a à vendre pour payer l’impôt – et rien n’est offert à personne. Rien '
   'n’est remis, rien ne peut se prescrire. Le report reste un report.'),
'es': dict(
 erb_h3='Ninguna exención, pero una transición justa',
 erb_p1='La exención actual de los activos empresariales actúa con más fuerza allí donde cambian '
   'de manos los mayores patrimonios. Se suprime sin sustituto. Quien hereda una empresa o una '
   'vivienda se enfrenta por tanto a un impuesto sobre bienes que no son dinero.',
 erb_p2='En su lugar entra un aplazamiento. Devenga intereses al principio al tipo al que el '
   'Estado se refinancia; a lo largo de diez años el tipo sube hasta el tipo de crédito de '
   'mercado. Sólo los intereses son exigibles de forma corriente. A quien no pueda soportar ni '
   'eso, se le añaden al saldo pendiente. Ese saldo queda como carga sobre el bien heredado y '
   'vence cuando se vende o se transmite.',
 erb_p3='Así nadie tiene que vender para pagar el impuesto, y a nadie se le regala nada. No se '
   'condona nada ni puede prescribir nada. El aplazamiento sigue siendo un aplazamiento.'),
'nl': dict(
 erb_h3='Geen uitzondering, wel een eerlijke overgang',
 erb_p1='De huidige vrijstelling voor ondernemingsvermogen werkt het sterkst daar waar de grootste '
   'vermogens overgaan. Zij vervalt zonder vervanging. Wie een bedrijf of een huis erft, staat '
   'daarmee voor een belasting op vermogen dat geen geld is.',
 erb_p2='Daarvoor in de plaats komt uitstel. De rente loopt eerst tegen het tarief waartegen de '
   'staat zich herfinanciert; in tien jaar stijgt zij naar de marktrente voor krediet. Alleen de '
   'rente is lopend verschuldigd. Wie ook die niet kan dragen, krijgt haar bij het openstaande '
   'bedrag geteld. Dat blijft een last op het geërfde goed en vervalt bij verkoop of overdracht.',
 erb_p3='Zo hoeft niemand te verkopen om de belasting te betalen – en krijgt niemand iets cadeau. '
   'Er wordt niets kwijtgescholden, niets kan verjaren. Het uitstel blijft uitstel.'),
'da': dict(
 erb_h3='Ingen undtagelse, men en fair overgang',
 erb_p1='Den nuværende lempelse for virksomhedsformue virker stærkest dér, hvor de største formuer '
   'skifter hænder. Den bortfalder uden erstatning. Den der arver en virksomhed eller et hus, står '
   'dermed over for en skat på formue, der ikke er penge.',
 erb_p2='I stedet træder henstand. Den forrentes først til den sats, hvortil staten selv '
   'refinansierer sig; over ti år stiger satsen til markedets udlånsrente. Kun renten forfalder '
   'løbende. Den der heller ikke kan bære den, får den lagt til restbeløbet. Dette bliver som en '
   'byrde på det arvede aktiv og forfalder, når det sælges eller gives videre.',
 erb_p3='Dermed behøver ingen at sælge for at betale skatten – og ingen får noget forærende. '
   'Intet eftergives, intet kan forældes. Henstanden forbliver henstand.'),
'sl': dict(
 erb_h3='Nobene izjeme, a pravičen prehod',
 erb_p1='Današnja oprostitev za poslovno premoženje deluje najmočneje tam, kjer prehajajo '
   'največja premoženja. Odpade brez nadomestila. Kdor podeduje podjetje ali hišo, se tako znajde '
   'pred davkom na premoženje, ki ni denar.',
 erb_p2='Na njeno mesto stopi odlog. Obrestuje se najprej po stopnji, po kateri se država sama '
   'refinancira; v desetih letih stopnja naraste na tržno posojilno obrestno mero. Tekoče se '
   'plačujejo le obresti. Komur tudi teh ni mogoče nositi, se mu pripišejo k neporavnanemu '
   'znesku. Ta ostane breme na podedovanem predmetu in zapade ob prodaji ali prenosu.',
 erb_p3='Tako nikomur ni treba prodati, da bi plačal davek – in nikomur ni nič podarjeno. Nič se '
   'ne odpiše, nič ne more zastarati. Odlog ostane odlog.'),
'et': dict(
 erb_h3='Erandeid ei ole, kuid üleminek on õiglane',
 erb_p1='Praegune ärivara soodustus mõjub kõige tugevamalt seal, kus lähevad üle suurimad '
   'varandused. See kaob asendamata. Kes pärib ettevõtte või maja, seisab seega maksu ees varalt, '
   'mis ei ole raha.',
 erb_p2='Selle asemele tuleb ajatamine. Intressi arvestatakse esmalt määraga, millega riik ise '
   'end refinantseerib; kümne aasta jooksul tõuseb määr turu laenuintressini. Jooksvalt tuleb '
   'tasuda üksnes intressi. Kes ka seda kanda ei suuda, sellele liidetakse see tasumata jäägile. '
   'See jääk jääb koormiseks päritud esemele ja muutub sissenõutavaks selle müügil või edasiandmisel.',
 erb_p3='Nii ei pea keegi müüma, et maksu tasuda – ja kellelegi ei kingita midagi. Midagi ei '
   'kustutata, midagi ei saa aeguda. Ajatamine jääb ajatamiseks.'),
}

for code, ex in T.items():
    p = os.path.join(L, code + '.json')
    d = json.load(open(p, encoding='utf-8'))
    for k in WEG:
        d.pop(k, None)
    d.update(ex)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(f'  {code}.json: {len(WEG)} Bausteine entfernt, {len(ex)} gesetzt')

# ------------------------------------------------------------------ tpl.py
tp = os.path.join(HERE, 'tpl.py')
t = open(tp, encoding='utf-8').read()

i = t.index('    <div class="erbbox">')
j = t.index('  </div>\n</section>\n\n<section id="calc">')
NEU = '''    <div class="erbbox">
      <h3 class="sub-h">{{erb_h3}}</h3>
      <p>{{erb_p1}}</p>
      <p>{{erb_p2}}</p>
      <p>{{erb_p3}}</p>
    </div>
'''
t = t[:i] + NEU + t[j:]

# Rechnerlogik und Balken aus dem Skript nehmen
a = t.index('\n/* ---- Stundungsrechner zu Position 03 ----')
bnd = t.index(" w.addEventListener('input',zeig); zeig();})();")
t = t[:a] + t[bnd + len(" w.addEventListener('input',zeig); zeig();})();"):]
open(tp, 'w', encoding='utf-8').write(t)
print('  tpl.py: Rechner durch Regeltext ersetzt, Skriptblock entfernt')

# ------------------------------------------------------------------ css.py
cp = os.path.join(HERE, 'css.py')
c = open(cp, encoding='utf-8').read()
for block in ['\n/* ---- Stundungsrechner zu Position 03: leichter als der Hauptrechner ---- */',
              '\n/* Die zehn Jahresraten als Balken — zeigt, dass die Rate sinkt */']:
    if block in c:
        s = c.index(block)
        e = c.index('\n', c.index('@media', s)) if '@media' in c[s:s+900] else s
        e = c.index('}\n', e) + 2
        c = c[:s] + c[e:]
VER = '''
/* ---- Regeltext zur Stundung unter den Positionen ---- */
.erbbox{margin-top:36px;max-width:760px}
.erbbox .sub-h{margin-top:0}
.erbbox p{font-size:16px;line-height:1.65;color:var(--ink);margin-bottom:14px}
.erbbox p:last-child{margin-bottom:0;color:var(--dim)}
'''
assert '.erbbox{margin-top:36px;max-width:760px}' not in c
c = c.rstrip()
assert c.endswith('"""')
open(cp, 'w', encoding='utf-8').write(c[:-3] + VER + '"""\n')
print('  css.py: Rechnerstile entfernt, Textstile gesetzt')

# ------------------------------------------- Anhang: Barwert auf Modell B
for code, alt, neu in [
 ('de', 'Barwert für den Staat über 10 Jahre 103 je 100 — kein Verlust.',
        'Laufend zu zahlen ist nur der Zins; der offene Betrag bleibt Last\n'
        '    auf dem Gegenstand. Barwert für den Staat je 100 EUR: 102 nach\n'
        '    fünf, 108 nach zehn, 121 nach zwanzig Jahren — kein Verlust,\n'
        '    und je länger gestundet wird, desto mehr.'),
 ('en', 'Present value to the state over 10 years 103 per 100 — no loss.',
        'Only the interest is payable as it falls due; the balance stays\n'
        '    a charge on the asset. Present value to the state per 100 EUR:\n'
        '    102 after five, 108 after ten, 121 after twenty years — no loss,\n'
        '    and the longer the deferral, the more.')]:
    p = os.path.join(L, code + '.json')
    d = json.load(open(p, encoding='utf-8'))
    if alt in d['src_text']:
        d['src_text'] = d['src_text'].replace(alt, neu, 1)
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        print(f'  {code}.json: Anhang auf Modell B')
    else:
        print(f'  ! {code}: Barwertzeile im Anhang nicht gefunden')
