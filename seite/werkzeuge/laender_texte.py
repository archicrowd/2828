"""Länderbezug der Sprachversionen (Fassung 4.1 ff.): Texte, die sich je Referenzland ändern. Ergänzt drittel_texte.py und überschreibt dessen Werte.

Referenzland je Sprache: de → Deutschland, fr → Frankreich, it → Italien, es → Spanien, pl → Polen, en → Durchschnitt der 30 Staaten des
Möglichkeitsraums (Entscheidung der Initiative, 18.10.2026). Platzhalter wie in drittel_texte.py ({…} seite_bau.werte, «…» drittel_bau.py).
Quellen der Länderangaben: modell/heute_laender.toml, modell/laenderseiten.toml, daten/aggregate/laender_zeitreihen.json; Kapitalertragsteuern:
FR PFU 31,4 % (LFSS 2026, legifiscal.fr, Sekundärquelle); IT 26 % (D.L. 66/2014); ES base del ahorro 19–30 % (Ley 35/2006, art. 66 und 76);
PL 19 % (ustawa o PIT, art. 30a). Übersetzungen maschinell, gegenzulesen (B16).
"""

REFERENZ = {"de": "DE", "en": "EU30", "fr": "FR", "it": "IT", "es": "ES", "pl": "PL"}

# Satz zur Dividende: der frühere Satz „Jedes Land zahlt denselben Anteil seiner Wirtschaftsleistung aus" gilt im Drittel-System nicht mehr
# (die Dividende ist der Rest nach Dach, Gemeinden und Netz; Korrektur 62).
DIV_SATZ = {
    "de": ("Jedes Land zahlt denselben Anteil seiner Wirtschaftsleistung aus.", "Ihre Höhe folgt aus der Wirtschaftsleistung und den Aufgaben jedes Landes."),
    "en": ("Every country pays out the same share of its economic output.", "Its level follows from each country's economic output and tasks."),
    "fr": ("Chaque pays verse la même part de sa production.", "Son montant dépend de la production et des missions de chaque pays."),
    "it": ("Ogni paese versa la stessa quota del proprio prodotto.", "Il suo importo dipende dal prodotto e dai compiti di ciascun paese."),
    "es": ("Cada país reparte la misma parte de su producción.", "Su cuantía depende de la producción y de las tareas de cada país."),
    "pl": ("Każdy kraj wypłaca ten sam udział swojego produktu.", "Jej wysokość zależy od produktu i zadań każdego kraju."),
}

LAND = {}

LAND["de"] = {
    "fuss_sprache": "Referenzland dieser Sprachversion ist Deutschland.",
}

LAND["fr"] = {
    "prob1_num": "«keil»",
    "prob1_p": "La moyenne en France – le troisième niveau le plus élevé des 38 pays de l'OCDE. La moyenne de l'OCDE est de {keil_oecd}.",
    "prob2_num": "31,4 %",
    "prob2_h": "sur les intérêts et les plus-values",
    "prob2_p": "Prélèvement forfaitaire unique (« flat tax ») depuis 2026 : 12,8 % d'impôt et 18,6 % de prélèvements sociaux. Un euro issu du capital contribue nettement moins qu'un euro issu du travail.",
    "prob3_num": "6 niveaux",
    "prob3_p": "Commune, intercommunalité, département, région, État et UE – le « millefeuille territorial ». L'argent et les missions passent d'un niveau à l'autre, les objectifs ne sont pas atteints.",
    "prob_quellen": "Sources : OCDE, Les impôts sur les salaires 2025 (personne seule, salaire moyen, 2024) ; loi de financement de la sécurité sociale pour 2026 (PFU 31,4 %).",
    "b1_p": "C'est le revenu brut qui est imposé – sans déductions, sans quotient familial. Le besoin de base reste exonéré ; au-delà, le travail paie à chaque tranche. Les tranches se situent à une, une fois et demie, deux et trois fois le besoin de base et évoluent avec lui.",
    "b2_p": "Le travail n'est plus taxé deux fois : ni cotisations salariales et patronales, ni CSG, ni CRDS. Les entreprises reversent au moins 80 % des cotisations patronales économisées dans les salaires. Le Danemark ne prélève déjà presque pas de cotisations sociales.",
    "rech_fein": "Aujourd'hui : cotisations salariales, CSG et CRDS, impôt sur le revenu avec quotient familial et décote, prime d'activité et allocations familiales selon le droit 2026 (modèle simplifié, comparé à l'OCDE, Les impôts sur les salaires). Tiers d'or : 80 % des cotisations patronales économisées dans le salaire, barème appliqué au salaire et au dividende, aucune cotisation sociale ni CSG, épargne obligatoire de 10 % du salaire sur un compte propre déduite, nouvelle TVA (étiquette) sur la consommation et surtaxe de «zu» du fonds propre des charges héritées incluses. Autres adultes sans revenu propre ; RSA et aides au logement non modélisés. Pouvoir d'achat actuel. Estimation du projet.",
    "gem_lede": "La répartition par le toit se résume à deux chiffres : {formel_einw} par habitant et {formel_kind} par enfant et par an (France ; chaque pays applique la même règle à sa production, en moyenne des pays {klub_einw} et {klub_kind}). Plus d'enfants signifie donc plus d'argent pour les écoles. Ce que la commune économise activement sur l'administration revient à ses habitants.",
    "zeit_lede": "Le dividende rend avant tout ce qui a été payé en impôts sur les produits et comportements nocifs. À mesure que les émissions nocives disparaissent, cette part diminue ; la santé et la dépendance coûtent plus avec le vieillissement. La croissance agit en sens inverse. Le dividende passe ainsi de {erw_2028} (2028) à {erw_2060} (2060). Plus de travail et d'automatisation le relèvent.",
    "js_schuld_l1": "France jusqu'à aujourd'hui",
    "js_schuld_l3": "Fonds propre des charges héritées",
    "js_schuld_text": "Les charges héritées sont l'affaire de chaque État. Si la France place ses dettes et ses promesses de retraite dans un fonds propre, la dette culmine à «spitze» en «sjahr» et tout est remboursé en 2098 – avec une surtaxe de «zu» sur tous les impôts. Un fonds commun avec d'autres États peut se financer à moindre coût.",
    "js_co2_unit": "Gaz à effet de serre de la France, millions de tonnes d'équivalent CO₂",
    "js_co2_l2": "Objectif : −40 % en 2030 par rapport à 1990, neutralité carbone en 2050",
    "js_co2_text": "«thg_minus» par rapport à 1990 – le plus dur reste à faire. Le Tiers d'or mise sur un prix européen commun du CO₂ et en reverse les recettes à tous par le dividende de transformation.",
    "fuss_sprache": "Le pays de référence de cette version linguistique est la France.",
}

LAND["it"] = {
    "prob1_num": "«keil»",
    "prob1_p": "La media in Italia – il quarto valore più alto dei 38 paesi OCSE. La media OCSE è del {keil_oecd}.",
    "prob2_num": "26 %",
    "prob2_h": "su interessi e plusvalenze",
    "prob2_p": "Imposta sostitutiva sui redditi finanziari (12,5 % sui titoli di Stato). Un euro dal capitale contribuisce molto meno di un euro dal lavoro.",
    "prob3_num": "5 livelli",
    "prob3_p": "Comune, provincia o città metropolitana, regione, Stato e UE. Soldi e compiti passano da un livello all'altro, gli obiettivi non vengono raggiunti.",
    "prob_quellen": "Fonti: OCSE, Taxing Wages 2025 (persona sola, salario medio, 2024); D.L. 66/2014 (aliquota del 26 %).",
    "b1_p": "Si tassa il reddito lordo – senza deduzioni né detrazioni. Il fabbisogno di base resta esente; oltre, il lavoro conviene a ogni scaglione. Gli scaglioni sono a una, una volta e mezza, due e tre volte il fabbisogno di base e crescono con esso.",
    "b2_p": "Il lavoro non è più tassato due volte: niente più contributi INPS a carico di lavoratori e imprese. Le imprese trasferiscono nei salari almeno l'80% dei contributi risparmiati. La Danimarca già oggi non preleva quasi contributi sociali.",
    "rech_fein": "Oggi: contributi INPS del lavoratore, IRPEF con detrazioni per lavoro dipendente e coniuge, misure del cuneo fiscale, trattamento integrativo, addizionali (media) e assegno unico secondo il diritto 2026 (modello semplificato, confrontato con OCSE Taxing Wages). Terzo d'oro: 80% dei contributi datoriali risparmiati nel salario, aliquote su salario e dividendo, nessun contributo sociale, previdenza obbligatoria del 10% del salario dedotta, nuova IVA (etichetta) sui consumi e sovrattassa del «zu» del proprio fondo degli oneri ereditati incluse. Altri adulti senza reddito proprio; assegno di inclusione e bonus affitto non calcolati. Potere d'acquisto attuale. Stima del progetto.",
    "gem_lede": "La ripartizione da parte del tetto si riduce a due numeri: {formel_einw} per abitante e {formel_kind} per figlio all'anno (Italia; ogni paese applica la stessa regola al proprio prodotto, in media tra i paesi {klub_einw} e {klub_kind}). Più figli significa quindi più soldi per le scuole. Ciò che il comune risparmia attivamente nell'amministrazione va ai suoi cittadini.",
    "zeit_lede": "Il dividendo restituisce soprattutto ciò che è stato versato in imposte su prodotti e comportamenti dannosi. Quando le emissioni dannose scompaiono, questa parte diminuisce; salute e assistenza costano di più con l'invecchiamento. La crescita agisce in senso opposto. Così il dividendo scende da {erw_2028} (2028) a {erw_2060} (2060). Più lavoro e automazione lo rialzano.",
    "js_schuld_l1": "Italia fino a oggi",
    "js_schuld_l3": "Fondo proprio degli oneri ereditati",
    "js_schuld_text": "Gli oneri ereditati sono competenza di ogni Stato. Se l'Italia conferisce debiti e promesse pensionistiche in un fondo proprio, il debito raggiunge il picco del «spitze» nel «sjahr» ed è tutto rimborsato entro il 2098 – con una sovrattassa del «zu» su tutte le imposte. Un fondo comune con altri Stati può finanziarsi a costi più bassi.",
    "js_co2_unit": "Gas serra dell'Italia, milioni di tonnellate di CO₂ equivalente",
    "js_co2_l2": "Neutralità climatica dell'UE nel 2050",
    "js_co2_text": "«thg_minus» rispetto al 1990 – il grosso deve ancora venire. Il Terzo d'oro punta su un prezzo europeo comune della CO₂ e ne restituisce i proventi a tutti tramite il dividendo di trasformazione.",
    "fuss_sprache": "Il paese di riferimento di questa versione linguistica è l'Italia.",
}

LAND["es"] = {
    "prob1_num": "«keil»",
    "prob1_p": "La media en España – el puesto 13 de los 38 países de la OCDE. La media de la OCDE es del {keil_oecd}.",
    "prob2_num": "19–30 %",
    "prob2_h": "sobre intereses y plusvalías",
    "prob2_p": "Base del ahorro del IRPF: tipos del 19 % al 30 %. Un euro del capital aporta mucho menos que un euro del trabajo.",
    "prob3_num": "5 niveles",
    "prob3_p": "Municipio, diputación provincial, comunidad autónoma, Estado y UE. Dinero y tareas pasan de un nivel a otro, los objetivos no se cumplen.",
    "prob_quellen": "Fuentes: OCDE, Taxing Wages 2025 (persona sola, salario medio, 2024); Ley 35/2006 del IRPF (base del ahorro).",
    "b2_p": "El trabajo deja de pagar dos veces: sin cotizaciones a la Seguridad Social de trabajadores ni de empresas. Las empresas trasladan al salario al menos el 80 % de las cotizaciones empresariales que ahorran. Dinamarca ya hoy apenas cobra cotizaciones sociales.",
    "rech_fein": "Hoy: cotizaciones del trabajador a la Seguridad Social (incluido el MEI), IRPF con reducción por rendimientos del trabajo, mínimos personal y familiar y tributación conjunta según el derecho de 2026 (modelo simplificado, comparado con OCDE Taxing Wages). Tercio de Oro: 80 % de las cotizaciones empresariales ahorradas en el salario, tarifa sobre salario y dividendo, sin cotizaciones sociales, ahorro obligatorio del 10 % del salario descontado, nuevo IVA (etiqueta) sobre el consumo y recargo del «zu» del fondo propio de cargas heredadas incluidos. Otros adultos sin renta propia; ingreso mínimo vital y ayudas autonómicas no calculados. Poder adquisitivo actual. Estimación del proyecto.",
    "gem_lede": "El reparto por el techo se resume en dos cifras: {formel_einw} por habitante y {formel_kind} por hijo al año (España; cada país aplica la misma regla a su producción, en la media de los países {klub_einw} y {klub_kind}). Más niños significa por tanto más dinero para las escuelas. Lo que el municipio ahorra activamente en administración llega a sus ciudadanos.",
    "zeit_lede": "El dividendo devuelve sobre todo lo que se pagó en impuestos sobre productos y conductas dañinos. Cuando desaparecen las emisiones dañinas, esta parte se reduce; la salud y los cuidados cuestan más con el envejecimiento. El crecimiento actúa en sentido contrario. Así el dividendo baja de {erw_2028} (2028) a {erw_2060} (2060). Más trabajo y automatización lo vuelven a subir.",
    "js_schuld_l1": "España hasta hoy",
    "js_schuld_l3": "Fondo propio de cargas heredadas",
    "js_schuld_text": "Las cargas heredadas son asunto de cada Estado. Si España aporta deudas y promesas de pensiones a un fondo propio, la deuda alcanza su máximo del «spitze» en «sjahr» y todo queda amortizado en 2098 – con un recargo del «zu» sobre todos los impuestos. Un fondo común con otros Estados puede financiarse más barato.",
    "js_co2_unit": "Gases de efecto invernadero de España, millones de toneladas de CO₂ equivalente",
    "js_co2_l2": "Objetivo: −23 % en 2030 respecto a 1990, neutralidad climática en 2050",
    "js_co2_text": "«thg_minus» respecto a 1990 y «thg_spitze» por debajo del máximo de 2007 – la mayor parte está por hacer. El Tercio de Oro apuesta por un precio europeo común del CO₂ y devuelve los ingresos a todos a través del dividendo de transformación.",
    "fuss_sprache": "El país de referencia de esta versión lingüística es España.",
}

LAND["pl"] = {
    "prob1_num": "«keil»",
    "prob1_p": "Średnia w Polsce – tuż poniżej średniej OECD ({keil_oecd}). Ale ponad cztery piąte tego klina to składki ZUS i składka zdrowotna.",
    "prob2_num": "19 %",
    "prob2_h": "od odsetek i zysków kapitałowych",
    "prob2_p": "Zryczałtowany podatek od dochodów kapitałowych („podatek Belki”). Złoty z kapitału wnosi znacznie mniej niż złoty z pracy.",
    "prob3_num": "5 szczebli",
    "prob3_p": "Gmina, powiat, województwo, państwo i UE. Pieniądze i zadania krążą między szczeblami, cele nie są osiągane.",
    "prob_quellen": "Źródła: OECD, Taxing Wages 2025 (osoba samotna, przeciętne wynagrodzenie, 2024); ustawa o podatku dochodowym od osób fizycznych, art. 30a (19 %).",
    "b2_p": "Praca nie jest już obciążana podwójnie: żadnych składek ZUS ani składki zdrowotnej. Firmy przekazują do wynagrodzeń co najmniej 80% zaoszczędzonych składek pracodawcy. Dania już dziś prawie nie pobiera składek społecznych.",
    "rech_fein": "Dziś: składki ZUS pracownika, składka zdrowotna, PIT z kwotą wolną, wspólnym rozliczeniem i ulgą na dzieci oraz 800+ według prawa 2026 (model uproszczony, porównany z OECD Taxing Wages). Złota Trzecia: 80% zaoszczędzonych składek pracodawcy w wynagrodzeniu, skala od wynagrodzenia i dywidendy, bez składek, obowiązkowe oszczędzanie 10% wynagrodzenia odjęte, nowy VAT (etykieta) od konsumpcji i dopłata «zu» z własnego funduszu obciążeń z przeszłości uwzględnione. Kwoty w złotych (4,24 zł za euro, średnia 2025). Pozostali dorośli bez własnego dochodu; świadczenia pomocy społecznej nie są liczone. Dzisiejsza siła nabywcza. Szacunek projektu.",
    "gem_lede": "Podział przez dach sprowadza się do dwóch liczb: {formel_einw} na mieszkańca i {formel_kind} na dziecko rocznie (Polska; każdy kraj stosuje tę samą zasadę do swojego produktu, średnio w krajach {klub_einw} i {klub_kind}). Więcej dzieci oznacza zatem więcej pieniędzy na szkoły. To, co gmina aktywnie zaoszczędzi na administracji, trafia do jej mieszkańców.",
    "zeit_lede": "Dywidenda oddaje przede wszystkim to, co wpłacono w podatkach od szkodliwych produktów i zachowań. Gdy szkodliwe emisje znikają, ta część maleje; zdrowie i opieka kosztują więcej wraz ze starzeniem się. Wzrost działa w przeciwną stronę. Dlatego dywidenda spada z {erw_2028} (2028) do {erw_2060} (2060). Więcej pracy i automatyzacji znów ją podnosi.",
    "zeit_unit": "Dywidenda transformacyjna na osobę dorosłą miesięcznie, złote w dzisiejszej sile nabywczej",
    "js_mio": "{x} mln zł",
    "js_schuld_l1": "Polska do dziś",
    "js_schuld_l3": "Własny fundusz obciążeń z przeszłości",
    "js_schuld_text": "Obciążenia z przeszłości to sprawa każdego państwa. Jeśli Polska wniesie długi i zobowiązania emerytalne do własnego funduszu, dług osiągnie szczyt «spitze» w roku «sjahr», a całość zostanie spłacona do 2098 – przy dopłacie «zu» do wszystkich podatków. Wspólny fundusz z innymi państwami może finansować się taniej.",
    "js_co2_unit": "Gazy cieplarniane Polski, mln ton ekwiwalentu CO₂",
    "js_co2_l2": "Neutralność klimatyczna UE w 2050",
    "js_co2_text": "«thg_minus» w porównaniu z 1990 – większość drogi przed nami. Złota Trzecia stawia na wspólną europejską cenę CO₂ i oddaje wpływy wszystkim przez dywidendę transformacyjną.",
    "b6_r": "1,5% powyżej ok. «e2m» (2 mln €)",
    "b6_p": "Majątek do ok. «e2m» (2 mln euro) pozostaje nietknięty. Powyżej obowiązuje podatek minimalny, zaliczany na poczet podatku dochodowego.",
    "fuss_sprache": "Krajem odniesienia tej wersji językowej jest Polska.",
}

LAND["en"] = {
    "prob1_num": "up to 52.6%",
    "prob1_h": "in taxes on an average wage",
    "prob1_p": "In Belgium; Germany 47.9%, France 47.2%, Italy 47.1%, Spain 40.6%. The OECD average is {keil_oecd}.",
    "prob2_num": "19–31.4%",
    "prob2_h": "on interest and capital gains",
    "prob2_p": "Flat taxes on capital income in Europe's large states: Poland 19%, Italy 26%, Germany 26.4%, Spain up to 30%, France 31.4%. A euro from capital contributes far less than a euro from work.",
    "prob3_num": "up to 6 levels",
    "prob3_p": "Municipality, inter-municipal body, county or province, region, state and EU. Money and tasks are passed back and forth, goals are missed.",
    "prob_quellen": "Sources: OECD, Taxing Wages 2025 (single person, average wage, 2024); national capital income tax rates 2026.",
    "rech_lede": "How much more a household keeps in its pocket under the Golden Third than today – after taxes and social contributions, with the employer share in the wage. Choose the country for the comparison.",
    "rech_fein": "Today: simplified national tax and contribution models under 2026 law for Germany, France, Italy, Spain and Poland (checked against OECD Taxing Wages). Golden Third: 80% of saved employer contributions in the wage, rates at the country's basic needs applied to wage and dividend, no social contributions, mandatory savings of 10% of wages deducted, new VAT (label) on consumption and the legacy surcharge of the country's own fund (Germany: common fund) included. Further adults without own income; minimum income schemes and housing benefits not modelled. Euros at today's purchasing power (Poland converted at 4.24 zł per euro). Project estimate.",
    "gem_lede": "Distribution by the roof comes down to two numbers: {formel_einw} per inhabitant and {formel_kind} per child per year (average of the 30 states; every country applies the same rule to its economic output). More children therefore means more money for schools. Whatever the municipality actively saves on administration ends up with its citizens.",
    "zeit_lede": "Above all, the dividend returns what was paid in taxes on harmful products and behaviour. As harmful emissions disappear, this part shrinks; health and care cost more as the population ages. Growth works the other way. On average across the 30 states the dividend falls from {erw_2028} (2028) to {erw_2060} (2060). More work and automation raise it again.",
    "zeit_unit": "Transformation dividend per adult per month, average of the 30 states, euros at today's purchasing power",
    "js_co2_unit": "EU-27 greenhouse gases, million tonnes CO₂ equivalent",
    "js_co2_l2": "Target: −55% by 2030 (net), climate neutrality 2050",
    "js_co2_text": "«thg_minus» since 1990 – the larger part is still to come. The Golden Third relies on a common European carbon price and returns the revenue to everyone through the transformation dividend.",
    "fuss_sprache": "This language version refers to the 30 European states calculated (average); the debt chart shows the club of ten.",
}

# Kurzformen für „x % weniger als 1990" je Sprache
THG = {"de": "Rund {p} weniger", "en": "Down about {p}", "fr": "Environ {p} de moins", "it": "Circa il {p} in meno", "es": "Alrededor de un {p} menos",
       "pl": "Około {p} mniej"}
THG_SPITZE = {"es": "un {p}"}

# Hinweis zur Hero-Zahl je Sprache: Fall A (≥ 90 % mit mehr) und Fall B (Mehrheitsaussage trägt nicht)
FEIN_A = {
    "de": "* Rechnung nach den Regeln des Projekts für Beschäftigte, 2028, heutige Kaufkraft, nach Pflichtvorsorge (10 %) und Altlastenzuschlag; zum Beispiel «plus» im Monat bei «bsp» Jahreseinkommen.",
    "fr": "* Calcul selon les règles du projet pour les salariés, 2028, pouvoir d'achat actuel, après épargne obligatoire (10 %) et surtaxe des charges héritées ; par exemple «plus» par mois pour un revenu annuel de «bsp».",
    "it": "* Calcolo secondo le regole del progetto per i lavoratori dipendenti, 2028, potere d'acquisto attuale, dopo la previdenza obbligatoria (10%) e la sovrattassa per gli oneri ereditati; per esempio «plus» al mese con un reddito annuo di «bsp».",
    "es": "* Cálculo según las reglas del proyecto para asalariados, 2028, poder adquisitivo actual, tras el ahorro obligatorio (10 %) y el recargo por cargas heredadas; por ejemplo «plus» al mes con una renta anual de «bsp».",
    "pl": "* Wyliczenie według zasad projektu dla zatrudnionych, 2028, dzisiejsza siła nabywcza, po obowiązkowym oszczędzaniu (10%) i dopłacie na obciążenia z przeszłości; na przykład «plus» miesięcznie przy rocznym dochodzie «bsp».",
    "en": "* In Germany, Italy, Spain and Poland, calculated under the project's rules (2028, today's purchasing power, after mandatory savings of 10% and the legacy surcharge). In France, according to the model, only «fr_anteil» in 10, because the prime d'activité and family benefits are lost.",
}
STAMP_B = {
    "fr": ("«plus_aw»", "par mois avec un salaire moyen*"),
}
FEIN_B = {
    "fr": "* Calcul selon les règles du projet : personne seule, salaire moyen de «aw», 2028, pouvoir d'achat actuel, après épargne obligatoire (10 %) et surtaxe des charges héritées. Pour les bas salaires et les familles modestes, le modèle donne moins qu'aujourd'hui (perte de la prime d'activité et des allocations familiales) : «anteil» salariés sur 10 ont plus.",
}
STAMP_A = {"de": ("9 von 10", "Beschäftigten haben mehr im Geldbeutel*"), "en": ("9 in 10", "employees have more in their pocket*"),
           "fr": ("9 sur 10", "salariés ont plus dans leur porte-monnaie*"), "it": ("9 su 10", "lavoratori dipendenti hanno più in tasca*"),
           "es": ("9 de cada 10", "asalariados tienen más en el bolsillo*"), "pl": ("9 na 10", "zatrudnionych ma więcej w portfelu*")}
ANTEIL_TXT = {"fr": "{a} à {b}", "en": "{a} to {b}"}

# Rechner der englischen Fassung: Land wählen
EN_LAENDER = [("DE", "Germany"), ("FR", "France"), ("IT", "Italy"), ("ES", "Spain"), ("PL", "Poland")]
EN_LAND_LABEL = "Country for the comparison"
