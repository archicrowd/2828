# -*- coding: utf-8 -*-
"""Fügt die Belegstand-Sektion und den Modellstand in alle acht Sprachfassungen ein.

Vier Stufen, kodiert als Zahl 0 bis 3. Die Stufe wird doppelt ausgegeben — als
Blockanzeige und als Wort — damit sie nicht allein von der Farbe abhängt.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(HERE, 'lang')

# ------------------------------------------------------------------ Belegstand
# (Positionsschlüssel, Behauptungsschlüssel, Stufe 0-3, Grundlagenschlüssel)
BELEG = [
    ('p01pos', 'p01t', 1, 'ev_g1'),
    ('p02pos', 'p02t', 1, 'ev_g2'),
    ('p03pos', 'p03t', 0, 'ev_g3'),
    ('p04pos', 'p04t', 0, 'ev_g4'),
    ('p05pos', 'p05t', 2, 'ev_g5'),
    ('p06pos', 'p06t', 1, 'ev_g6'),
    ('p07pos', 'p07t', 0, 'ev_g7'),
    ('p08pos', 'p08t', 3, 'ev_g8'),
    ('p09pos', 'p09t', 0, 'ev_g9'),
    ('p10pos', 'p10t', 1, 'ev_g10'),
]

# ---------------------------------------------------------------------- Texte
TXT = {
'de': dict(
 nav_ev='Belege', ev_h2='Belegstand',
 ev_lede='Welche Zahl worauf beruht, Position für Position. Vier Stufen: aus amtlicher '
   'Quelle gerechnet; eigene Rechnung mit Näherung; aus Verteilungsannahmen gerechnet; '
   'nicht gerechnet. Heute ist eine Zeile voll belegt, vier sind offen. Jede neue '
   'Rechnung verschiebt eine Zeile.',
 ev_c1='Position', ev_c2='Was behauptet wird', ev_c3='Stufe', ev_c4='Grundlage und nächster Schritt',
 ev_s3='belegt', ev_s2='Größenordnung', ev_s1='Modellrechnung', ev_s0='offen',
 ev_leg='■■■ aus amtlicher Quelle gerechnet und nachvollziehbar · ■■□ eigene Rechnung aus '
   'amtlicher Quelle, mit Entwurfsentscheidung oder Näherung · ■□□ aus Verteilungsannahmen '
   'gerechnet, ohne Primärdaten · □□□ nicht gerechnet.',
 ev_note='Diese Tabelle ist der Grund, warum der Entwurf prüfbar ist: sie sagt auch, wo die '
   'Zahlen dünn sind. Die Skripte liegen im Anhang, die Rechenschritte im Logbuch.',
 ver_label='Modellstand', ver_val='v0.5 · 1. Oktober 2026',
 ev_g1='Tarif und Rechengrößen 2026 sind belegt (§ 32a EStG). Das Aufkommen ist über die '
   'Einkommensverteilung in drei Rechenwegen geschätzt, nicht auf Primärdaten gerechnet. '
   'Nächster Schritt: amtliche Lohn- und Einkommensteuerstatistik nach Größenklassen.',
 ev_g2='Der Rechtsstand 2026 ist belegt. Die Aufkommenswirkung beruht auf einer '
   'Realisationselastizität von 0,7 bis 1,0 — das ist eine Annahme aus der Literatur. '
   'Nächster Schritt: Kapitalertragsteuerstatistik.',
 ev_g3='Nicht gerechnet. Die Erbschaft- und Schenkungsteuerstatistik weist Erwerbe nach '
   'Größenklassen und den Verschonungsabschlag getrennt aus. Damit wäre beides genau zu '
   'bestimmen: das Aufkommen bei 28 % und was die heutigen Verschonungen kosten.',
 ev_g4='Nicht gerechnet. Für die Bodenwertabgabe fehlt die Bemessungsgrundlage. Nächster '
   'Schritt: Wert des Grund und Bodens aus den sektoralen Vermögensbilanzen.',
 ev_g5='Eigene Auswertung der länderbezogenen Berichte der OECD, 2016 bis 2023, 63 '
   'Sitzstaaten. Geprüft mit zwei Verteilungsschlüsseln und im festen Kreis durchgängig '
   'meldender Staaten: für Deutschland +5 bis +14 Mrd. €, Median +8. Dass allein nach '
   'Umsatz verteilt wird, ist eine Entwurfsentscheidung — sie macht die Regel einseitig '
   'durchsetzbar, wirkt aber schwächer gegen Steueroasen.',
 ev_g6='Die fünf Stufen sind gesetzt, ihre Gewichte 10/10/20/30/30 sind angenommen. Daraus '
   'folgt der Effektivsatz von 20 %. Nächster Schritt: Konsumausgaben nach Verwendungszweck '
   'auf die Stufen abbilden.',
 ev_g7='Nicht gerechnet. Es fehlen der Minderungspfad und die Höhe der abzubauenden '
   'Subventionen. Nächster Schritt: nationale Treibhausgasbilanz auf dem Preispfad.',
 ev_g8='Höhe und Kopplung sind belegt: 50 % des amtlichen Existenzminimums 2026, Stufen bei '
   '55 und 60 %. Der Bruttoaufwand ist gerechnet. Ob er getragen wird, hängt an den '
   'übrigen Positionen.',
 ev_g9='Nicht gerechnet. Bestandsgarantie und Härtefallfonds brauchen eine Mikrosimulation '
   'auf Haushaltsebene. Das setzt einen Datenvertrag für SOEP oder EU-SILC voraus.',
 ev_g10='Beitragssätze und Bemessungsgrenzen 2026 sind belegt. Dass die Beiträge auf 28 und '
   'später 18 % sinken können, folgt aus der Gesamtrechnung und ist so belastbar wie diese.',
),
'en': dict(
 nav_ev='Evidence', ev_h2='Evidence status',
 ev_lede='What each figure rests on, position by position. Four levels: computed from an '
   'official source; own calculation with an approximation; computed from distributional '
   'assumptions; not computed. Today one row is fully substantiated and four are open. '
   'Every new calculation moves a row.',
 ev_c1='Position', ev_c2='The claim', ev_c3='Level', ev_c4='Basis and next step',
 ev_s3='substantiated', ev_s2='order of magnitude', ev_s1='model estimate', ev_s0='open',
 ev_leg='■■■ computed from an official source and reproducible · ■■□ own calculation from an '
   'official source, with a design choice or approximation · ■□□ computed from '
   'distributional assumptions, no primary data · □□□ not computed.',
 ev_note='This table is why the proposal can be checked: it also says where the figures are '
   'thin. The scripts are in the annex, the calculation steps in the logbook.',
 ver_label='Model version', ver_val='v0.5 · 1 October 2026',
 ev_g1='The 2026 schedule and parameters are documented (§ 32a German Income Tax Act). The '
   'revenue is estimated across the income distribution in three scenarios, not computed '
   'from primary data. Next step: the official income tax statistics by income bracket.',
 ev_g2='The 2026 legal position is documented. The revenue effect rests on a realisation '
   'elasticity of 0.7 to 1.0 — an assumption taken from the literature. Next step: the '
   'capital income tax statistics.',
 ev_g3='Not computed. The inheritance and gift tax statistics report transfers by size class '
   'and the business-asset relief separately. Both could therefore be determined precisely: '
   'the revenue at 28 % and what the present exemptions cost.',
 ev_g4='Not computed. The land value levy lacks a tax base. Next step: the value of land '
   'from the sectoral balance sheets.',
 ev_g5='Own analysis of the OECD country-by-country reports, 2016 to 2023, 63 reporting '
   'jurisdictions. Tested with two apportionment keys and on a constant panel of '
   'continuously reporting states: for Germany +5 to +14 bn €, median +8. Apportioning by '
   'sales alone is a design choice — it makes the rule unilaterally enforceable but works '
   'less strongly against tax havens.',
 ev_g6='The five tiers are set; their weights of 10/10/20/30/30 are assumed. The effective '
   'rate of 20 % follows from them. Next step: map consumption expenditure by purpose onto '
   'the tiers.',
 ev_g7='Not computed. The abatement path and the scale of the subsidies to be removed are '
   'missing. Next step: the national greenhouse gas inventory along the price path.',
 ev_g8='Level and indexation are documented: 50 % of the official 2026 subsistence minimum, '
   'with steps at 55 and 60 %. The gross cost is computed. Whether it can be carried depends '
   'on the other positions.',
 ev_g9='Not computed. The grandfathering guarantee and the hardship fund require a household '
   'microsimulation. That presupposes a data contract for SOEP or EU-SILC.',
 ev_g10='The 2026 contribution rates and ceilings are documented. That contributions can fall '
   'to 28 and later 18 % follows from the overall calculation and is only as sound as that.',
),
'fr': dict(
 nav_ev='Preuves', ev_h2='État des preuves',
 ev_lede='Sur quoi repose chaque chiffre, position par position. Quatre niveaux : calculé à '
   'partir d\'une source officielle ; calcul propre avec approximation ; calculé à partir '
   'd\'hypothèses de répartition ; non calculé. Aujourd\'hui une ligne est pleinement étayée '
   'et quatre sont ouvertes. Chaque nouveau calcul déplace une ligne.',
 ev_c1='Position', ev_c2='Ce qui est affirmé', ev_c3='Niveau', ev_c4='Base et prochaine étape',
 ev_s3='étayé', ev_s2='ordre de grandeur', ev_s1='estimation', ev_s0='non calculé',
 ev_leg='■■■ calculé à partir d\'une source officielle et reproductible · ■■□ calcul propre à '
   'partir d\'une source officielle, avec choix de conception ou approximation · ■□□ calculé '
   'à partir d\'hypothèses de répartition, sans données primaires · □□□ non calculé.',
 ev_note='Ce tableau est la raison pour laquelle le projet est vérifiable : il dit aussi où '
   'les chiffres sont minces. Les scripts sont en annexe, les étapes de calcul dans le '
   'journal.',
 ver_label='Version du modèle', ver_val='v0.5 · 1er octobre 2026',
 ev_g1='Le barème et les paramètres 2026 sont documentés. Le rendement est estimé sur la '
   'distribution des revenus selon trois scénarios, non calculé sur données primaires. '
   'Prochaine étape : la statistique officielle de l\'impôt sur le revenu par tranche.',
 ev_g2='L\'état du droit 2026 est documenté. L\'effet sur le rendement repose sur une '
   'élasticité de réalisation de 0,7 à 1,0 — une hypothèse issue de la littérature. '
   'Prochaine étape : la statistique des revenus du capital.',
 ev_g3='Non calculé. La statistique des droits de succession et de donation indique les '
   'transmissions par classe de taille et l\'abattement pour biens d\'entreprise séparément. '
   'Les deux pourraient donc être déterminés précisément : le rendement à 28 % et le coût '
   'des exonérations actuelles.',
 ev_g4='Non calculé. La taxe sur la valeur du sol manque de base d\'imposition. Prochaine '
   'étape : la valeur du sol dans les comptes de patrimoine sectoriels.',
 ev_g5='Analyse propre des déclarations pays par pays de l\'OCDE, 2016 à 2023, 63 États de '
   'résidence. Vérifiée avec deux clés de répartition et sur un panel constant d\'États '
   'déclarant sans interruption : pour l\'Allemagne +5 à +14 Md€, médiane +8. Répartir selon '
   'le seul chiffre d\'affaires est un choix de conception : la règle devient applicable '
   'unilatéralement, mais agit moins fortement contre les paradis fiscaux.',
 ev_g6='Les cinq niveaux sont fixés ; leurs pondérations de 10/10/20/30/30 sont supposées. Le '
   'taux effectif de 20 % en découle. Prochaine étape : rattacher les dépenses de '
   'consommation par destination aux niveaux.',
 ev_g7='Non calculé. Il manque la trajectoire de réduction et le montant des subventions à '
   'supprimer. Prochaine étape : l\'inventaire national des gaz à effet de serre sur la '
   'trajectoire de prix.',
 ev_g8='Le montant et l\'indexation sont documentés : 50 % du minimum vital officiel 2026, '
   'avec des paliers à 55 et 60 %. Le coût brut est calculé. Sa soutenabilité dépend des '
   'autres positions.',
 ev_g9='Non calculé. La garantie de maintien et le fonds de cas difficiles exigent une '
   'microsimulation des ménages. Cela suppose un contrat de données pour SOEP ou EU-SILC.',
 ev_g10='Les taux de cotisation et plafonds 2026 sont documentés. Que les cotisations puissent '
   'descendre à 28 puis 18 % découle du calcul d\'ensemble et n\'est pas plus solide que lui.',
),
'es': dict(
 nav_ev='Evidencia', ev_h2='Estado de la evidencia',
 ev_lede='En qué se basa cada cifra, posición por posición. Cuatro niveles: calculado a '
   'partir de una fuente oficial; cálculo propio con aproximación; calculado a partir de '
   'supuestos de distribución; no calculado. Hoy una fila está plenamente acreditada y '
   'cuatro están abiertas. Cada nuevo cálculo mueve una fila.',
 ev_c1='Posición', ev_c2='Lo que se afirma', ev_c3='Nivel', ev_c4='Base y siguiente paso',
 ev_s3='acreditado', ev_s2='orden de magnitud', ev_s1='estimación', ev_s0='abierto',
 ev_leg='■■■ calculado a partir de una fuente oficial y reproducible · ■■□ cálculo propio a '
   'partir de una fuente oficial, con decisión de diseño o aproximación · ■□□ calculado a '
   'partir de supuestos de distribución, sin datos primarios · □□□ no calculado.',
 ev_note='Esta tabla es la razón por la que el proyecto puede comprobarse: también dice dónde '
   'las cifras son débiles. Los scripts están en el anexo, los pasos de cálculo en el '
   'cuaderno de registro.',
 ver_label='Versión del modelo', ver_val='v0.5 · 1 de octubre de 2026',
 ev_g1='La tarifa y los parámetros de 2026 están documentados. El rendimiento se estima sobre '
   'la distribución de la renta en tres escenarios, no se calcula con datos primarios. '
   'Siguiente paso: la estadística oficial del impuesto sobre la renta por tramos.',
 ev_g2='La situación legal de 2026 está documentada. El efecto sobre el rendimiento se basa en '
   'una elasticidad de realización de 0,7 a 1,0, un supuesto tomado de la literatura. '
   'Siguiente paso: la estadística de rentas del capital.',
 ev_g3='No calculado. La estadística del impuesto sobre sucesiones y donaciones recoge las '
   'transmisiones por clases de tamaño y la reducción por activos empresariales por separado. '
   'Ambas cosas podrían determinarse con precisión: el rendimiento al 28 % y lo que cuestan '
   'las exenciones actuales.',
 ev_g4='No calculado. Al gravamen sobre el valor del suelo le falta la base imponible. '
   'Siguiente paso: el valor del suelo en los balances patrimoniales sectoriales.',
 ev_g5='Análisis propio de los informes país por país de la OCDE, 2016 a 2023, 63 Estados de '
   'residencia. Comprobado con dos claves de reparto y en un panel constante de Estados que '
   'informan sin interrupción: para Alemania +5 a +14 mil millones €, mediana +8. Repartir '
   'solo por ventas es una decisión de diseño: hace la regla aplicable unilateralmente, pero '
   'actúa con menos fuerza contra los paraísos fiscales.',
 ev_g6='Los cinco niveles están fijados; sus pesos 10/10/20/30/30 son supuestos. De ellos se '
   'deriva el tipo efectivo del 20 %. Siguiente paso: asignar el gasto de consumo por '
   'finalidad a los niveles.',
 ev_g7='No calculado. Faltan la senda de reducción y el volumen de las subvenciones a '
   'suprimir. Siguiente paso: el inventario nacional de gases de efecto invernadero sobre la '
   'senda de precios.',
 ev_g8='Importe y vinculación están documentados: 50 % del mínimo vital oficial de 2026, con '
   'escalones en el 55 y el 60 %. El coste bruto está calculado. Que pueda sostenerse depende '
   'de las demás posiciones.',
 ev_g9='No calculado. La garantía de mantenimiento y el fondo de casos difíciles requieren una '
   'microsimulación de hogares. Eso presupone un contrato de datos para SOEP o EU-SILC.',
 ev_g10='Los tipos de cotización y las bases máximas de 2026 están documentados. Que las '
   'cotizaciones puedan bajar al 28 y luego al 18 % se deriva del cálculo global y no es más '
   'sólido que él.',
),
'nl': dict(
 nav_ev='Onderbouwing', ev_h2='Stand van de onderbouwing',
 ev_lede='Waarop elk cijfer rust, positie voor positie. Vier niveaus: berekend uit een '
   'officiële bron; eigen berekening met benadering; berekend uit verdelingsaannames; niet '
   'berekend. Vandaag is één regel volledig onderbouwd en zijn er vier open. Elke nieuwe '
   'berekening verschuift een regel.',
 ev_c1='Positie', ev_c2='Wat wordt gesteld', ev_c3='Niveau', ev_c4='Basis en volgende stap',
 ev_s3='onderbouwd', ev_s2='orde van grootte', ev_s1='modelschatting', ev_s0='open',
 ev_leg='■■■ berekend uit een officiële bron en reproduceerbaar · ■■□ eigen berekening uit een '
   'officiële bron, met ontwerpkeuze of benadering · ■□□ berekend uit verdelingsaannames, '
   'zonder primaire gegevens · □□□ niet berekend.',
 ev_note='Deze tabel is de reden dat het ontwerp te controleren is: hij zegt ook waar de '
   'cijfers dun zijn. De scripts staan in de bijlage, de rekenstappen in het logboek.',
 ver_label='Modelversie', ver_val='v0.5 · 1 oktober 2026',
 ev_g1='Tarief en rekengrootheden 2026 zijn gedocumenteerd. De opbrengst is over de '
   'inkomensverdeling in drie scenario\'s geschat, niet op primaire gegevens berekend. '
   'Volgende stap: de officiële inkomstenbelastingstatistiek naar inkomensklasse.',
 ev_g2='De rechtstoestand 2026 is gedocumenteerd. Het opbrengsteffect rust op een '
   'realisatie-elasticiteit van 0,7 tot 1,0 — een aanname uit de literatuur. Volgende stap: '
   'de statistiek van kapitaalinkomsten.',
 ev_g3='Niet berekend. De successie- en schenkingsbelastingstatistiek vermeldt verkrijgingen '
   'naar grootteklasse en de bedrijfsvermogensvrijstelling afzonderlijk. Beide zouden dus '
   'precies te bepalen zijn: de opbrengst bij 28 % en wat de huidige vrijstellingen kosten.',
 ev_g4='Niet berekend. Voor de grondwaardeheffing ontbreekt de heffingsgrondslag. Volgende '
   'stap: de waarde van de grond uit de sectorale vermogensbalansen.',
 ev_g5='Eigen analyse van de landenrapporten van de OESO, 2016 tot 2023, 63 vestigingsstaten. '
   'Getoetst met twee verdeelsleutels en op een vast panel van onafgebroken rapporterende '
   'staten: voor Duitsland +5 tot +14 mld €, mediaan +8. Alleen naar omzet verdelen is een '
   'ontwerpkeuze: de regel wordt eenzijdig handhaafbaar, maar werkt zwakker tegen '
   'belastingparadijzen.',
 ev_g6='De vijf treden staan vast; hun gewichten 10/10/20/30/30 zijn aangenomen. Daaruit volgt '
   'het effectieve tarief van 20 %. Volgende stap: consumptieve bestedingen naar doel aan de '
   'treden toewijzen.',
 ev_g7='Niet berekend. Het reductiepad en de omvang van de af te bouwen subsidies ontbreken. '
   'Volgende stap: de nationale broeikasgasbalans op het prijspad.',
 ev_g8='Hoogte en koppeling zijn gedocumenteerd: 50 % van het officiële bestaansminimum 2026, '
   'met treden bij 55 en 60 %. De brutokosten zijn berekend. Of ze gedragen worden, hangt af '
   'van de overige posities.',
 ev_g9='Niet berekend. Bestaansgarantie en hardheidsfonds vergen een microsimulatie op '
   'huishoudniveau. Dat vooronderstelt een datacontract voor SOEP of EU-SILC.',
 ev_g10='Premiepercentages en maximumgrondslagen 2026 zijn gedocumenteerd. Dat de premies naar '
   '28 en later 18 % kunnen dalen, volgt uit de totaalberekening en is net zo hard als die.',
),
'da': dict(
 nav_ev='Dokumentation', ev_h2='Dokumentationsstatus',
 ev_lede='Hvad hvert tal hviler på, position for position. Fire niveauer: beregnet ud fra en '
   'officiel kilde; egen beregning med tilnærmelse; beregnet ud fra fordelingsantagelser; '
   'ikke beregnet. I dag er én række fuldt dokumenteret, og fire er åbne. Hver ny beregning '
   'flytter en række.',
 ev_c1='Position', ev_c2='Det der hævdes', ev_c3='Niveau', ev_c4='Grundlag og næste skridt',
 ev_s3='dokumenteret', ev_s2='størrelsesorden', ev_s1='modelberegning', ev_s0='åben',
 ev_leg='■■■ beregnet ud fra en officiel kilde og reproducerbart · ■■□ egen beregning ud fra en '
   'officiel kilde, med designvalg eller tilnærmelse · ■□□ beregnet ud fra '
   'fordelingsantagelser, uden primære data · □□□ ikke beregnet.',
 ev_note='Denne tabel er grunden til, at udkastet kan efterprøves: den siger også, hvor tallene '
   'er tynde. Scripterne ligger i bilaget, regneskridtene i logbogen.',
 ver_label='Modelversion', ver_val='v0.5 · 1. oktober 2026',
 ev_g1='Skala og beregningsstørrelser for 2026 er dokumenteret. Provenuet er skønnet over '
   'indkomstfordelingen i tre scenarier, ikke beregnet på primære data. Næste skridt: den '
   'officielle indkomstskattestatistik efter indkomstklasse.',
 ev_g2='Retstilstanden 2026 er dokumenteret. Provenuvirkningen hviler på en '
   'realisationselasticitet på 0,7 til 1,0 — en antagelse fra litteraturen. Næste skridt: '
   'statistikken over kapitalindkomster.',
 ev_g3='Ikke beregnet. Arve- og gaveafgiftsstatistikken opgør erhvervelser efter '
   'størrelsesklasse og virksomhedslempelsen særskilt. Begge kunne derfor bestemmes præcist: '
   'provenuet ved 28 % og hvad de nuværende lempelser koster.',
 ev_g4='Ikke beregnet. Grundværdiafgiften mangler et beregningsgrundlag. Næste skridt: '
   'jordens værdi fra de sektorale formueopgørelser.',
 ev_g5='Egen analyse af OECD\'s land for land-rapporter, 2016 til 2023, 63 hjemstedsstater. '
   'Prøvet med to fordelingsnøgler og på et fast panel af stater, der rapporterer '
   'uafbrudt: for Tyskland +5 til +14 mia. €, median +8. At fordele efter omsætning alene er '
   'et designvalg: reglen bliver ensidigt håndhævelig, men virker svagere mod skattely.',
 ev_g6='De fem trin er fastlagt; deres vægte 10/10/20/30/30 er antagelser. Den effektive sats '
   'på 20 % følger heraf. Næste skridt: henføre forbrugsudgifterne efter formål til trinnene.',
 ev_g7='Ikke beregnet. Reduktionsstien og omfanget af de subsidier, der skal afskaffes, '
   'mangler. Næste skridt: det nationale drivhusgasregnskab langs prisstien.',
 ev_g8='Niveau og kobling er dokumenteret: 50 % af det officielle existensminimum 2026, med '
   'trin ved 55 og 60 %. Bruttoomkostningen er beregnet. Om den kan bæres, afhænger af de '
   'øvrige positioner.',
 ev_g9='Ikke beregnet. Bestandsgarantien og hårdhedsfonden kræver en mikrosimulering på '
   'husstandsniveau. Det forudsætter en datakontrakt for SOEP eller EU-SILC.',
 ev_g10='Bidragssatser og bidragsgrænser for 2026 er dokumenteret. At bidragene kan falde til '
   '28 og senere 18 % følger af den samlede beregning og er kun så robust som den.',
),
'sl': dict(
 nav_ev='Dokazi', ev_h2='Stanje dokazov',
 ev_lede='Na čem temelji posamezna številka, postavka za postavko. Štiri ravni: izračunano iz '
   'uradnega vira; lastni izračun z približkom; izračunano iz predpostavk o porazdelitvi; ni '
   'izračunano. Danes je ena vrstica v celoti dokazana, štiri so odprte. Vsak nov izračun '
   'premakne eno vrstico.',
 ev_c1='Postavka', ev_c2='Kaj se trdi', ev_c3='Raven', ev_c4='Podlaga in naslednji korak',
 ev_s3='dokazano', ev_s2='velikostni red', ev_s1='modelski izračun', ev_s0='odprto',
 ev_leg='■■■ izračunano iz uradnega vira in ponovljivo · ■■□ lastni izračun iz uradnega vira, z '
   'odločitvijo o zasnovi ali približkom · ■□□ izračunano iz predpostavk o porazdelitvi, brez '
   'primarnih podatkov · □□□ ni izračunano.',
 ev_note='Ta razpredelnica je razlog, da je osnutek mogoče preveriti: povedo tudi, kje so '
   'številke šibke. Skripti so v prilogi, računski koraki v dnevniku.',
 ver_label='Različica modela', ver_val='v0.5 · 1. oktober 2026',
 ev_g1='Lestvica in računske velikosti za leto 2026 so dokumentirane. Prihodek je ocenjen po '
   'porazdelitvi dohodkov v treh scenarijih, ne izračunan iz primarnih podatkov. Naslednji '
   'korak: uradna statistika dohodnine po dohodkovnih razredih.',
 ev_g2='Pravno stanje 2026 je dokumentirano. Učinek na prihodek temelji na elastičnosti '
   'realizacije med 0,7 in 1,0 — to je predpostavka iz literature. Naslednji korak: '
   'statistika dohodkov od kapitala.',
 ev_g3='Ni izračunano. Statistika davka na dediščine in darila prikazuje pridobitve po '
   'velikostnih razredih in olajšavo za poslovno premoženje ločeno. Oboje bi bilo torej '
   'mogoče natančno določiti: prihodek pri 28 % in koliko stanejo današnje olajšave.',
 ev_g4='Ni izračunano. Dajatvi na vrednost zemljišč manjka davčna osnova. Naslednji korak: '
   'vrednost zemljišč iz sektorskih premoženjskih bilanc.',
 ev_g5='Lastna analiza poročil OECD po državah, 2016 do 2023, 63 držav sedeža. Preverjeno z '
   'dvema ključema razdelitve in na stalnem krogu držav, ki poročajo neprekinjeno: za '
   'Nemčijo +5 do +14 milijard €, mediana +8. Razdelitev samo po prihodkih od prodaje je '
   'odločitev o zasnovi: pravilo postane enostransko izvršljivo, a šibkeje deluje proti '
   'davčnim oazam.',
 ev_g6='Pet stopenj je določenih; njihove uteži 10/10/20/30/30 so predpostavljene. Iz njih '
   'izhaja efektivna stopnja 20 %. Naslednji korak: izdatke za potrošnjo po namenu '
   'razporediti na stopnje.',
 ev_g7='Ni izračunano. Manjkata pot zmanjševanja in obseg subvencij, ki jih je treba odpraviti. '
   'Naslednji korak: nacionalna bilanca toplogrednih plinov po cenovni poti.',
 ev_g8='Višina in vezava sta dokumentirani: 50 % uradnega eksistenčnega minimuma 2026, s '
   'stopnjama pri 55 in 60 %. Bruto strošek je izračunan. Ali ga je mogoče nositi, je '
   'odvisno od drugih postavk.',
 ev_g9='Ni izračunano. Jamstvo za obstoječe prejemke in sklad za težje primere zahtevata '
   'mikrosimulacijo na ravni gospodinjstev. To predpostavlja pogodbo o podatkih za SOEP ali '
   'EU-SILC.',
 ev_g10='Prispevne stopnje in osnove za leto 2026 so dokumentirane. Da se prispevki lahko '
   'znižajo na 28 in pozneje 18 %, izhaja iz skupnega izračuna in je le toliko zanesljivo '
   'kot ta.',
),
'et': dict(
 nav_ev='Tõendid', ev_h2='Tõendite seis',
 ev_lede='Millele iga arv tugineb, positsioon positsiooni haaval. Neli taset: arvutatud '
   'ametlikust allikast; oma arvutus lähendusega; arvutatud jaotuseelduste põhjal; ei ole '
   'arvutatud. Täna on üks rida täielikult tõendatud ja neli on lahtised. Iga uus arvutus '
   'nihutab ühte rida.',
 ev_c1='Positsioon', ev_c2='Mida väidetakse', ev_c3='Tase', ev_c4='Alus ja järgmine samm',
 ev_s3='tõendatud', ev_s2='suurusjärk', ev_s1='mudelarvutus', ev_s0='lahtine',
 ev_leg='■■■ arvutatud ametlikust allikast ja korratav · ■■□ oma arvutus ametlikust allikast, '
   'kavandiotsuse või lähendusega · ■□□ arvutatud jaotuseelduste põhjal, ilma esmaseid '
   'andmeid · □□□ ei ole arvutatud.',
 ev_note='See tabel on põhjus, miks kavandit saab kontrollida: see ütleb ka, kus arvud on '
   'õhukesed. Skriptid on lisas, arvutussammud päevikus.',
 ver_label='Mudeli versioon', ver_val='v0.5 · 1. oktoober 2026',
 ev_g1='2026. aasta astmestik ja arvestusnäitajad on dokumenteeritud. Laekumine on hinnatud '
   'tulujaotuse põhjal kolmes stsenaariumis, mitte arvutatud esmastest andmetest. Järgmine '
   'samm: ametlik tulumaksustatistika tuluklasside kaupa.',
 ev_g2='2026. aasta õiguslik seis on dokumenteeritud. Mõju laekumisele tugineb realiseerimise '
   'elastsusel 0,7 kuni 1,0 — see on kirjandusest võetud eeldus. Järgmine samm: '
   'kapitalitulu statistika.',
 ev_g3='Ei ole arvutatud. Pärandi- ja kinkemaksu statistika näitab omandamisi suurusklasside '
   'kaupa ja ärivara soodustust eraldi. Mõlemat saaks seega täpselt määrata: laekumise 28 % '
   'juures ja selle, mida praegused soodustused maksavad.',
 ev_g4='Ei ole arvutatud. Maa väärtuse maksul puudub maksubaas. Järgmine samm: maa väärtus '
   'sektoripõhistest varabilanssidest.',
 ev_g5='Oma analüüs OECD riigipõhistest aruannetest, 2016 kuni 2023, 63 asukohariiki. '
   'Kontrollitud kahe jaotusvõtmega ja püsival ringil riikidest, kes esitavad katkematult: '
   'Saksamaa puhul +5 kuni +14 miljardit €, mediaan +8. Jaotamine üksnes käibe järgi on '
   'kavandiotsus: reegel muutub ühepoolselt jõustatavaks, kuid mõjub maksuparadiiside vastu '
   'nõrgemalt.',
 ev_g6='Viis astet on paigas; nende kaalud 10/10/20/30/30 on eeldatud. Neist tuleneb '
   'efektiivne määr 20 %. Järgmine samm: siduda tarbimiskulutused otstarbe kaupa astmetega.',
 ev_g7='Ei ole arvutatud. Puuduvad vähendamise rada ja kaotatavate toetuste maht. Järgmine '
   'samm: riiklik kasvuhoonegaaside bilanss hinnarajal.',
 ev_g8='Suurus ja sidumine on dokumenteeritud: 50 % 2026. aasta ametlikust elatusmiinimumist, '
   'astmetega 55 ja 60 %. Brutokulu on arvutatud. Kas see on kantav, sõltub teistest '
   'positsioonidest.',
 ev_g9='Ei ole arvutatud. Senise taseme tagatis ja raskete juhtumite fond nõuavad '
   'leibkonnatasandi mikrosimulatsiooni. See eeldab andmelepingut SOEP või EU-SILC jaoks.',
 ev_g10='2026. aasta maksemäärad ja ülemmäärad on dokumenteeritud. See, et maksed võivad '
   'langeda 28 ja hiljem 18 protsendini, tuleneb kogujärjestusest ja on sama kindel kui see.',
),
}

# ------------------------------------------------------------ Sprachdateien
for code, extra in TXT.items():
    p = os.path.join(L, code + '.json')
    d = json.load(open(p, encoding='utf-8'))
    d.update(extra)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(f'  {code}.json: {len(extra)} Bausteine ergänzt, {len(d)} insgesamt')

# -------------------------------------------------------------------- tpl.py
tp = os.path.join(HERE, 'tpl.py')
t = open(tp, encoding='utf-8').read()

NAV_ALT = '      <a href="#club">{{nav_club}}</a>\n'
NAV_NEU = ('      <a href="#club">{{nav_club}}</a>\n'
           '      <a class="opt" href="#evidence">{{nav_ev}}</a>\n')
assert NAV_ALT in t, 'Navigationszeile nicht gefunden'
t = t.replace(NAV_ALT, NAV_NEU, 1)

SEC = '''<section id="evidence">
  <div class="wrap">
    <h2>{{ev_h2}}</h2>
    <p class="lede">{{ev_lede}}</p>
    {{_tbl_beleg}}
    <p class="fineprint">{{ev_leg}}</p>
    <div class="calibrate" style="margin-top:18px;margin-bottom:0">{{ev_note}}</div>
  </div>
</section>

<section id="annex">'''
assert '<section id="annex">' in t
t = t.replace('<section id="annex">', SEC, 1)

FT_ALT = '<div><h4>{{ft_m_h}}</h4><p>{{ft_m_p}}</p></div>'
FT_NEU = ('<div><h4>{{ft_m_h}}</h4><p>{{ft_m_p}}</p>'
          '<p class="verstamp">{{ver_label}} <b>{{ver_val}}</b></p></div>')
assert FT_ALT in t
t = t.replace(FT_ALT, FT_NEU, 1)
open(tp, 'w', encoding='utf-8').write(t)
print('  tpl.py: Sektion, Navigationspunkt und Modellstand eingefügt')

# -------------------------------------------------------------------- css.py
cp = os.path.join(HERE, 'css.py')
c = open(cp, encoding='utf-8').read()
CSS_NEU = '''
/* ---- Belegstand: Stufe doppelt kodiert, als Blockanzeige und als Wort ---- */
table.beleg{table-layout:fixed;width:100%;min-width:720px}
.beleg th,.beleg td{text-align:left;white-space:normal;vertical-align:top;
  font-family:var(--body);font-size:14px;line-height:1.5}
.beleg col.c1{width:15%}.beleg col.c2{width:21%}.beleg col.c3{width:16%}.beleg col.c4{width:48%}
.beleg tbody td:first-child{font-family:var(--mono);font-size:12px;color:var(--dim);
  text-transform:uppercase;letter-spacing:.03em;line-height:1.4}
.beleg tbody td.claim{font-weight:500;color:var(--ink);font-size:14.5px}
.beleg td.st{font-family:var(--mono);font-size:12px;letter-spacing:.02em}
.beleg td.st .w{display:block;margin-top:5px}
.meter{display:flex;gap:3px}
.meter i{width:10px;height:10px;border:1.4px solid var(--line);display:block;border-radius:1px}
.st.s3 .meter i{background:var(--accent);border-color:var(--accent)}
.st.s2 .meter i:nth-child(-n+2){background:var(--accent);border-color:var(--accent)}
.st.s1 .meter i:nth-child(1){background:#9A6B18;border-color:#9A6B18}
.st.s0 .meter i{border-color:var(--warn)}
.st.s3,.st.s2{color:var(--accent)}
.st.s1{color:#7A5413}
.st.s0{color:var(--warn)}
.verstamp{font-family:var(--mono);font-size:12px;margin-top:12px!important;color:var(--dim)}
.verstamp b{color:var(--accent);font-weight:500}
@media(max-width:720px){table.beleg{min-width:620px}.beleg col.c4{width:42%}}
'''
assert CSS_NEU.strip() not in c
c = c.rstrip()
if c.endswith('"""'):
    c = c[:-3] + CSS_NEU + '"""\n'
elif c.endswith("'''"):
    c = c[:-3] + CSS_NEU + "'''\n"
else:
    raise SystemExit('css.py endet nicht auf einen Zeichenkettenblock — bitte ansehen')
open(cp, 'w', encoding='utf-8').write(c)
print('  css.py: Stile ergänzt')

# ------------------------------------------------------------------ build.py
bp = os.path.join(HERE, 'build.py')
b = open(bp, encoding='utf-8').read()

FN = '''

# Belegstand: (Positionsschluessel, Behauptung, Stufe 0-3, Grundlage)
BELEG = ''' + repr(BELEG) + '''


def tbl_beleg(T, f):
    """Stufe erscheint als Blockanzeige UND als Wort — nie nur als Farbe."""
    h = ''.join('<th scope="col">%s</th>' % T[k]
                for k in ('ev_c1', 'ev_c2', 'ev_c3', 'ev_c4'))
    blocks = '<span class="meter"><i></i><i></i><i></i></span>'
    rows = ''
    for pos, claim, stufe, grund in BELEG:
        wort = T['ev_s%d' % stufe]
        rows += ('<tr><td>%s</td><td class="claim">%s</td>'
                 '<td class="st s%d">%s<span class="w">%s</span></td>'
                 '<td>%s</td></tr>'
                 % (T[pos], T[claim], stufe, blocks, wort, T[grund]))
    cols = ('<colgroup><col class="c1"><col class="c2">'
            '<col class="c3"><col class="c4"></colgroup>')
    return ('<div class="tscroll"><table class="beleg">%s<thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (cols, h, rows))
'''
ANK = '\ndef flags(T, f):'
assert ANK in b
b = b.replace(ANK, FN + ANK, 1)

CTX_ALT = "'_flags': flags(T, f),"
CTX_NEU = "'_flags': flags(T, f), '_tbl_beleg': tbl_beleg(T, f),"
assert CTX_ALT in b
b = b.replace(CTX_ALT, CTX_NEU, 1)
open(bp, 'w', encoding='utf-8').write(b)
print('  build.py: Tabellenbau und Platzhalter ergänzt')
print('\nFertig. Jetzt build.py laufen lassen.')
