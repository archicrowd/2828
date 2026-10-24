"""Korrekturen der Initiative vom 24.10.2026 für die Länderfassungen (EN, FR, IT, ES, PL) der Seite Stand C (Logbuch v4.45).

1. „Gemeinde(n)“ → „Kommunen und Regionen“ (DE in drittel_texte.py/v48_texte.py, v4.43): municipalities and regions / communes et régions /
   comuni e regioni / municipios y regiones / gminy i regiony. Unverändert wie im Deutschen: heutiger Staatsaufbau (prob3_p), Dänemark und
   Schweiz (erf2, erf3), Fachleute der kommunalen Praxis (offen_lede).
2. Mehrheitsentscheid (sich5_p), Methodik (fuss_meth_p), Dividende „zuvor eingezahlt“ (zeit_lede), Gini-Fußnote ohne Dänemark/Schweden.
3. Neue Länderkarten Australien (Pflichtvorsorge) und Schweden (Prämienrente) in allen sechs Sprachen (erf5, erf6).
Angewandt in drittel_bau.texte() nach dem Zusammenführen der Texte (anwenden).
"""

NEU = {}   # vollständige Texte je Schlüssel
ERSATZ = {}  # (alt, neu) in bestehenden Texten

NEU["de"] = {
    "erf5_n": "Australien", "erf5_h": "Pflichtvorsorge aufs eigene Konto", "erf5_k": "seit 1992 · 12 % des Lohns seit 2025",
    "erf5_p": "Arbeitgeber zahlen verpflichtend in die eigene Altersvorsorge jedes Beschäftigten (Superannuation); das Geld gehört dem Konto, nicht dem Staat. Seit Juli 2025 sind es 12 % des Lohns.",
    "erf6_n": "Schweden", "erf6_h": "Ein Teil der Rente auf eigenem Konto", "erf6_k": "seit 2000 · 2,5 von 18,5 %",
    "erf6_p": "Von 18,5 % Rentenbeitrag fließen 2,5 Punkte in die Prämienrente auf einem eigenen Konto. Jeder wählt die Fonds selbst; wer nicht wählt, ist im staatlichen Standardfonds.",
}
ERSATZ["de"] = [("Dänemark und Schweden: amtlicher Wert 2025. ", ""), ("Frankreich: bei Abbildung", "Frankreich 2028: bei Abbildung")]

NEU["en"] = {
    "meta_beschreibung": "At most one third on any income, a strong net without premiums and a transformation dividend every month. Municipalities and regions decide for themselves, a common roof protects common interests.",
    "nav_gemeinde": "Municipalities and regions",
    "hero_sub": "All taxes and levies are spread fairly across labour, capital and automation – at most one third on any income. Work pays, and the strong social net and the transformation dividend secure social peace. Municipalities and regions decide more independently, and a European roof protects common interests by majority vote.",
    "prob_lede": "Today's system has grown layer by layer. It burdens labour more heavily than anything else and leaves citizens, municipalities and regions frustrated.",
    "konz_h2": "Strong municipalities and regions, strong citizens, a strong European roof",
    "konz_lede": "The number of administrative levels is reduced. Municipalities and regions receive their share directly from the roof, decide on their own finances and delegate tasks to higher-level administrative associations (e.g. infrastructure partnerships). The European roof takes on only what municipalities and regions cannot do alone – and may not take more than the treaty allows.",
    "svg_weiter": "at least {mind} to municipalities and regions",
    "svg_gemeinde": "Municipalities", "svg_gemeinde_kurz": "Municipalities", "svg_gemeinde_sub": "and regions decide for themselves", "svg_gemeinde_sub_kurz": "and regions",
    "eff2_h": "Municipalities and regions are trusted",
    "eff2_p": "to run their own affairs: they receive fixed amounts per resident and per child, under the same rule in every country. They decide on membership in districts and associations and on local support programmes.",
    "eff3_p": "what can only be done together: defence and digital sovereignty, a single market without borders, common standards. Nothing more. The roof decides by a majority of the delegates of the associations of municipalities and regions.",
    "fluss_l2": "Tasks of municipalities and regions",
    "b5_pos": "Land · municipalities and regions", "b5_h": "Municipalities and regions tax the land",
    "gem_h2": "Municipalities and regions do their own sums",
    "gem_verw": "Administration's share of municipal and regional budgets",
    "gem_fein": "On average, {verw_klub} of municipal and regional budgets goes to administration. Their tasks differ from country to country, so a direct comparison of shares only goes so far.",
    "gem_bud": "Budget of municipalities and regions per year",
    "sich1_p": "The roof keeps at most {og} of what it collects for the municipalities and regions – and only what its tasks really cost.",
    "sich2_p": "Every euro above need goes to the municipalities and regions, into the strong net and the transformation dividend.",
    "sich3_p": "Municipalities and regions receive fixed amounts per resident and per child. Nobody has to ask, nobody can cut.",
    "js_fluss": "In {j} the roof keeps {a} of {hundert} – up to {cap} would be allowed. Municipalities and regions spend {b} on their tasks, the strong net {n}, and {d} goes to citizens as the transformation dividend.",
    "chan1_h": "Municipalities and regions invest in the next generation",
    "chan1_p": "For every child aged 5 to 19, municipalities and regions receive {formel_kind} each year – more children, more money. They fund schools, childcare and support locally. Children receive care, upbringing and education as services of municipalities and regions; the child dividend and the basic livelihood cover material needs.{chan1_zusatz}",
    "chan4_p": "Culture, sport and community stay with the municipalities and regions (1.22% of GDP in the overall calculation). They decide for themselves what to spend their money on – including what they save in administration.",
    "bess_r4b": "dividend without applying; top-up at one local office",
    "sich5_p": "The EU has recently lost its ability to act. An alliance in which individual members can block decisions with a veto cannot decide for everyone when the moment of decision comes. Hence a switch to majority voting – for the ability to act and to compete.",
    "fuss_meth_p": "All figures come from an open calculation that anyone can rerun, based on official statistics (Eurostat, OECD, national statistical offices and authorities) and published surveys; for Germany a synthetic microsimulation checks the distribution across all households. Every change and every error found is logged with a number. In October 2026 the website and the calculation were recomputed in three reviews commissioned by the initiative (including their own microsimulation); findings and responses are documented. Independent reviews are welcome, and the material is ready. Developed with the method of architectural design, using AI tools and AI-assisted calculation models. Scripts under MIT licence, texts under CC BY 4.0.",
    "erf5_n": "Australia", "erf5_h": "Mandatory saving into your own account", "erf5_k": "since 1992 · 12% of wages since 2025",
    "erf5_p": "Employers must pay into each employee's own retirement account (superannuation); the money belongs to the account, not the state. Since July 2025 it is 12% of wages.",
    "erf6_n": "Sweden", "erf6_h": "Part of the pension in your own account", "erf6_k": "since 2000 · 2.5 of 18.5%",
    "erf6_p": "Of the 18.5% pension contribution, 2.5 points go into the premium pension in an individual account. Everyone chooses their own funds; those who do not choose are in the state default fund.",
}
ERSATZ["en"] = [("Whatever the municipality actively saves on administration ends up with its citizens.", "Whatever municipalities and regions actively save on administration ends up with their citizens."),
                ("are handled locally by the municipality – under the country's rules, in one place.", "are handled locally by municipalities and regions – under the country's rules, in one place."),
                ("and local self-government.", "and self-government of municipalities and regions."),
                ("Above all, the dividend returns what was paid in taxes", "Above all, the dividend returns what was previously paid in taxes"),
                ("Denmark and Sweden: official value 2025. ", ""), ("France: if households", "France 2028: if households")]

NEU["fr"] = {
    "meta_beschreibung": "Au plus un tiers sur tout revenu, un filet solide sans prime et chaque mois un dividende de transformation. Les communes et régions décident elles-mêmes, un toit commun protège les intérêts communs.",
    "nav_gemeinde": "Communes et régions",
    "hero_sub": "Tous les impôts et prélèvements sont répartis équitablement entre le travail, le capital et l'automatisation – au plus un tiers sur tout revenu. Le travail paie, et le filet social solide et le dividende de transformation assurent la paix sociale. Les communes et régions décident de façon plus autonome, un toit européen protège les intérêts communs par décision majoritaire.",
    "prob_lede": "Le système actuel s'est construit couche après couche. Il pèse plus lourdement sur le travail que sur tout le reste et laisse citoyens, communes et régions frustrés.",
    "konz_h2": "Des communes et régions fortes, des citoyens forts, un toit européen fort",
    "konz_lede": "Le nombre de niveaux administratifs est réduit. Les communes et régions reçoivent leur part directement du toit, décident elles-mêmes de leurs finances et délèguent des missions à des groupements administratifs de niveau supérieur (par exemple des syndicats d'infrastructure). Le toit européen n'assume que ce que les communes et régions ne peuvent pas faire seules – et ne peut pas prendre plus que ce que prévoit le traité.",
    "svg_weiter": "au moins {mind} aux communes et régions",
    "svg_gemeinde": "Communes", "svg_gemeinde_kurz": "Communes", "svg_gemeinde_sub": "et régions décident elles-mêmes", "svg_gemeinde_sub_kurz": "et régions",
    "eff2_h": "On fait confiance aux communes et régions",
    "eff2_p": "pour gérer leurs affaires : elles reçoivent des montants fixes par habitant et par enfant, selon la même règle dans chaque pays. Elles décident de leur adhésion à des groupements et intercommunalités et des programmes de soutien locaux.",
    "eff3_p": "ce qui ne se fait qu'ensemble : défense et souveraineté numérique, un marché intérieur sans frontières, des normes communes. Rien de plus. Le toit décide à la majorité des délégués des groupements de communes et de régions.",
    "fluss_l2": "Missions des communes et régions",
    "b5_pos": "Sol · communes et régions", "b5_h": "Les communes et régions taxent le sol",
    "gem_h2": "Les communes et régions font leurs propres comptes",
    "gem_verw": "Part de l'administration dans les budgets des communes et régions",
    "gem_fein": "En moyenne, {verw_klub} des budgets des communes et régions vont à l'administration. Leurs missions diffèrent d'un pays à l'autre ; une comparaison directe des parts a donc ses limites.",
    "gem_bud": "Budget des communes et régions par an",
    "sich1_p": "Le toit garde au plus {og} de ce qu'il perçoit pour les communes et régions – et seulement ce que coûtent réellement ses missions.",
    "sich2_p": "Chaque euro au-delà du besoin va aux communes et régions, au filet solide et au dividende de transformation.",
    "sich3_p": "Les communes et régions reçoivent des montants fixes par habitant et par enfant. Personne n'a à quémander, personne ne peut couper.",
    "js_fluss": "En {j}, le toit garde {a} sur {hundert} – jusqu'à {cap} seraient autorisés. Les communes et régions consacrent {b} à leurs missions, le filet solide {n}, et {d} reviennent aux habitants sous forme de dividende de transformation.",
    "chan1_h": "Les communes et régions soutiennent la relève",
    "chan1_p": "Pour chaque enfant de 5 à 19 ans, les communes et régions reçoivent chaque année {formel_kind} – plus d'enfants, plus d'argent. Elles financent ainsi écoles, accueil et soutien sur place. L'accueil, l'éducation et la formation sont des prestations des communes et régions ; le dividende enfant et le minimum vital couvrent les besoins matériels.{chan1_zusatz}",
    "chan4_p": "Culture, sport et vie associative restent aux communes et régions (1,22 % du PIB dans le calcul d'ensemble). Elles décident elles-mêmes de l'usage de leur argent – y compris de ce qu'elles économisent en administration.",
    "bess_r4b": "dividende sans demande ; complément à un seul guichet local",
    "sich5_p": "L'UE n'est récemment plus en mesure d'agir. Une alliance dans laquelle certains peuvent bloquer les décisions par un veto ne peut pas décider pour tous à l'heure de la décision. D'où le passage à la décision majoritaire – pour la capacité d'agir et la compétitivité.",
    "fuss_meth_p": "Tous les chiffres proviennent d'un calcul ouvert que chacun peut refaire, fondé sur des statistiques officielles (Eurostat, OCDE, instituts statistiques et administrations nationaux) et des enquêtes publiées ; pour l'Allemagne, une microsimulation synthétique vérifie la répartition sur l'ensemble des ménages. Chaque modification et chaque erreur trouvée sont consignées avec un numéro dans le journal. En octobre 2026, le site et le calcul ont été recalculés lors de trois examens commandés par l'initiative (dont une microsimulation propre) ; constats et réponses sont documentés. Des examens indépendants sont bienvenus, les pièces sont prêtes. Développé selon la méthode du projet architectural, à l'aide d'outils d'IA et de modèles de calcul assistés par IA. Scripts sous licence MIT, textes sous CC BY 4.0.",
    "erf5_n": "Australie", "erf5_h": "Épargne obligatoire sur un compte propre", "erf5_k": "depuis 1992 · 12 % du salaire depuis 2025",
    "erf5_p": "Les employeurs versent obligatoirement sur le compte de retraite propre de chaque salarié (superannuation) ; l'argent appartient au compte, pas à l'État. Depuis juillet 2025, c'est 12 % du salaire.",
    "erf6_n": "Suède", "erf6_h": "Une part de la retraite sur un compte propre", "erf6_k": "depuis 2000 · 2,5 sur 18,5 %",
    "erf6_p": "Sur 18,5 % de cotisation retraite, 2,5 points vont à la pension de prime sur un compte individuel. Chacun choisit ses fonds ; sans choix, l'argent va au fonds public par défaut.",
}
ERSATZ["fr"] = [("Ce que la commune économise activement sur l'administration revient à ses habitants.", "Ce que les communes et régions économisent activement sur l'administration revient à leurs habitants."),
                ("sont traités sur place par la commune – selon les règles de l'État, à un seul guichet.", "sont traités sur place par les communes et régions – selon les règles de l'État, à un seul guichet."),
                ("et libre administration des communes.", "et libre administration des communes et régions."),
                ("ce qui a été payé en impôts", "ce qui a été payé auparavant en impôts"),
                ("Danemark et Suède : valeur officielle 2025. ", ""), ("France : avec une représentation", "France 2028 : avec une représentation")]

NEU["it"] = {
    "meta_beschreibung": "Al massimo un terzo su ogni reddito, una rete forte senza premi e ogni mese un dividendo di trasformazione. Comuni e regioni decidono da sé, un tetto comune tutela gli interessi comuni.",
    "nav_gemeinde": "Comuni e regioni",
    "hero_sub": "Tutte le imposte e i contributi sono ripartiti in modo equo tra lavoro, capitale e automazione – al massimo un terzo su ogni reddito. Il lavoro conviene, e la rete sociale forte e il dividendo di trasformazione garantiscono la pace sociale. Comuni e regioni decidono in modo più autonomo, un tetto europeo tutela gli interessi comuni con decisioni a maggioranza.",
    "prob_lede": "Il sistema attuale è cresciuto strato dopo strato. Grava sul lavoro più che su ogni altra cosa e lascia cittadini, comuni e regioni frustrati.",
    "konz_h2": "Comuni e regioni forti, cittadini forti, un tetto europeo forte",
    "konz_lede": "Il numero dei livelli amministrativi si riduce. Comuni e regioni ricevono la loro quota direttamente dal tetto, decidono da sé sulle proprie finanze e delegano compiti a consorzi amministrativi sovraordinati (per esempio consorzi per le infrastrutture). Il tetto europeo si occupa solo di ciò che comuni e regioni non possono fare da soli – e non può prendere più di quanto previsto dal trattato.",
    "svg_weiter": "almeno il {mind} a comuni e regioni",
    "svg_gemeinde": "Comuni", "svg_gemeinde_kurz": "Comuni", "svg_gemeinde_sub": "e regioni decidono da sé", "svg_gemeinde_sub_kurz": "e regioni",
    "eff2_h": "A comuni e regioni si dà fiducia",
    "eff2_p": "di gestire i propri affari: ricevono importi fissi per abitante e per bambino, con la stessa regola in ogni paese. Decidono sull'adesione a enti e consorzi e sui programmi di sostegno locali.",
    "eff3_p": "ciò che si può fare solo insieme: difesa e sovranità digitale, un mercato interno senza frontiere, standard comuni. Niente di più. Il tetto decide a maggioranza dei delegati dei consorzi di comuni e regioni.",
    "fluss_l2": "Compiti di comuni e regioni",
    "b5_pos": "Suolo · comuni e regioni", "b5_h": "Comuni e regioni tassano il suolo",
    "gem_h2": "Comuni e regioni fanno i conti da sé",
    "gem_verw": "Quota dell'amministrazione nei bilanci di comuni e regioni",
    "gem_fein": "In media il {verw_klub} dei bilanci di comuni e regioni va all'amministrazione. I loro compiti differiscono da paese a paese; un confronto diretto delle quote ha quindi dei limiti.",
    "gem_bud": "Bilancio di comuni e regioni all'anno",
    "sich1_p": "Il tetto trattiene al massimo il {og} di quanto riscuote per comuni e regioni – e solo ciò che i compiti costano davvero.",
    "sich2_p": "Ogni euro oltre il fabbisogno va a comuni e regioni, alla rete forte e al dividendo di trasformazione.",
    "sich3_p": "Comuni e regioni ricevono importi fissi per abitante e per figlio. Nessuno deve chiedere, nessuno può tagliare.",
    "js_fluss": "Nel {j} il tetto trattiene {a} su {hundert} – sarebbero consentiti fino a {cap}. Comuni e regioni spendono {b} per i loro compiti, la rete forte {n}, e {d} vanno ai cittadini come dividendo di trasformazione.",
    "chan1_h": "Comuni e regioni investono nelle nuove generazioni",
    "chan1_p": "Per ogni bambino dai 5 ai 19 anni comuni e regioni ricevono ogni anno {formel_kind} – più bambini, più risorse. Finanziano così scuole, servizi per l'infanzia e sostegno sul territorio. Cura, educazione e istruzione arrivano ai bambini come servizi di comuni e regioni; il dividendo per i figli e il minimo vitale coprono il fabbisogno materiale.{chan1_zusatz}",
    "chan4_p": "Cultura, sport e comunità restano a comuni e regioni (1,22% del PIL nel calcolo complessivo). Decidono da sé come usare le loro risorse – anche ciò che risparmiano nell'amministrazione.",
    "bess_r4b": "dividendo senza domanda; integrazione a un unico sportello locale",
    "sich5_p": "Di recente l'UE non è più in grado di agire. Un'alleanza in cui singoli membri possono bloccare le decisioni con un veto non può decidere per tutti nell'ora della decisione. Da qui il passaggio alla decisione a maggioranza – per la capacità di agire e la competitività.",
    "fuss_meth_p": "Tutti i dati provengono da un calcolo aperto che chiunque può rifare, basato su statistiche ufficiali (Eurostat, OCSE, istituti statistici e amministrazioni nazionali) e indagini pubblicate; per la Germania una microsimulazione sintetica verifica la distribuzione su tutte le famiglie. Ogni modifica e ogni errore trovato sono registrati con un numero nel registro. Nell'ottobre 2026 il sito e il calcolo sono stati ricalcolati in tre verifiche commissionate dall'iniziativa (tra cui una propria microsimulazione); rilievi e risposte sono documentati. Verifiche indipendenti sono benvenute, il materiale è pronto. Sviluppato con il metodo del progetto architettonico, con l'uso di strumenti di IA e modelli di calcolo assistiti dall'IA. Script con licenza MIT, testi con CC BY 4.0.",
    "erf5_n": "Australia", "erf5_h": "Previdenza obbligatoria sul proprio conto", "erf5_k": "dal 1992 · 12% del salario dal 2025",
    "erf5_p": "I datori di lavoro versano obbligatoriamente nel conto previdenziale personale di ogni dipendente (superannuation); il denaro appartiene al conto, non allo Stato. Da luglio 2025 è il 12% del salario.",
    "erf6_n": "Svezia", "erf6_h": "Una parte della pensione su un conto proprio", "erf6_k": "dal 2000 · 2,5 su 18,5%",
    "erf6_p": "Del 18,5% di contributo pensionistico, 2,5 punti vanno nella pensione a premio su un conto individuale. Ognuno sceglie i propri fondi; chi non sceglie è nel fondo pubblico predefinito.",
}
ERSATZ["it"] = [("Ciò che il comune risparmia attivamente nell'amministrazione va ai suoi cittadini.", "Ciò che comuni e regioni risparmiano attivamente nell'amministrazione va ai loro cittadini."),
                ("li gestisce il comune sul posto – secondo le regole dello Stato, in un unico sportello.", "li gestiscono comuni e regioni sul posto – secondo le regole dello Stato, in un unico sportello."),
                ("e autonomia dei comuni.", "e autonomia di comuni e regioni."),
                ("ciò che è stato versato in imposte", "ciò che è stato versato in precedenza in imposte"),
                ("Danimarca e Svezia: valore ufficiale 2025. ", ""), ("Francia: rappresentando", "Francia 2028: rappresentando")]

NEU["es"] = {
    "meta_beschreibung": "Como máximo un tercio sobre cualquier renta, una red fuerte sin primas y cada mes un dividendo de transformación. Los municipios y las regiones deciden por sí mismos, un techo común protege los intereses comunes.",
    "nav_gemeinde": "Municipios y regiones",
    "hero_sub": "Todos los impuestos y cotizaciones se reparten de forma justa entre trabajo, capital y automatización – como máximo un tercio sobre cualquier renta. Trabajar compensa, y la red social fuerte y el dividendo de transformación aseguran la paz social. Los municipios y las regiones deciden con más autonomía, un techo europeo protege los intereses comunes por mayoría.",
    "prob_lede": "El sistema actual ha crecido capa a capa. Grava el trabajo más que cualquier otra cosa y deja frustrados a ciudadanos, municipios y regiones.",
    "konz_h2": "Municipios y regiones fuertes, ciudadanos fuertes, un techo europeo fuerte",
    "konz_lede": "Se reduce el número de niveles administrativos. Los municipios y las regiones reciben su parte directamente del techo, deciden por sí mismos sobre sus finanzas y delegan tareas en agrupaciones administrativas de nivel superior (por ejemplo, consorcios de infraestructuras). El techo europeo solo asume lo que municipios y regiones no pueden hacer solos – y no puede quedarse con más de lo que dice el tratado.",
    "svg_weiter": "al menos el {mind} a municipios y regiones",
    "svg_gemeinde": "Municipios", "svg_gemeinde_kurz": "Municipios", "svg_gemeinde_sub": "y regiones deciden por sí mismos", "svg_gemeinde_sub_kurz": "y regiones",
    "eff2_h": "Se confía en los municipios y las regiones",
    "eff2_p": "para que gestionen sus asuntos: reciben importes fijos por habitante y por niño, con la misma regla en cada país. Deciden sobre su pertenencia a mancomunidades y asociaciones y sobre los programas de apoyo locales.",
    "eff3_p": "lo que solo se puede hacer juntos: defensa y soberanía digital, un mercado interior sin fronteras, normas comunes. Nada más. El techo decide por mayoría de los delegados de las agrupaciones de municipios y regiones.",
    "fluss_l2": "Tareas de municipios y regiones",
    "b5_pos": "Suelo · municipios y regiones", "b5_h": "Municipios y regiones gravan el suelo",
    "gem_h2": "Municipios y regiones hacen sus propias cuentas",
    "gem_verw": "Peso de la administración en los presupuestos de municipios y regiones",
    "gem_fein": "De media, el {verw_klub} de los presupuestos de municipios y regiones se destina a la administración. Sus tareas difieren entre países; una comparación directa de los porcentajes tiene por ello límites.",
    "gem_bud": "Presupuesto de municipios y regiones al año",
    "sich1_p": "El techo retiene como máximo el {og} de lo que recauda para los municipios y las regiones – y solo lo que sus tareas cuestan de verdad.",
    "sich2_p": "Cada euro por encima de la necesidad va a los municipios y las regiones, a la red fuerte y al dividendo de transformación.",
    "sich3_p": "Los municipios y las regiones reciben importes fijos por habitante y por hijo. Nadie tiene que pedir, nadie puede recortar.",
    "js_fluss": "En {j} el techo retiene {a} de cada {hundert} – se permitirían hasta {cap}. Municipios y regiones destinan {b} a sus tareas, la red fuerte {n}, y {d} van a los ciudadanos como dividendo de transformación.",
    "chan1_h": "Municipios y regiones apuestan por las nuevas generaciones",
    "chan1_p": "Por cada niño de 5 a 19 años, municipios y regiones reciben cada año {formel_kind} – más niños, más dinero. Con ello financian escuelas, cuidado infantil y apoyo en el lugar. Cuidado, educación y formación llegan a los niños como servicios de municipios y regiones; el dividendo infantil y el mínimo vital cubren las necesidades materiales.{chan1_zusatz}",
    "chan4_p": "Cultura, deporte y comunidad quedan en manos de los municipios y las regiones (1,22 % del PIB en el cálculo de conjunto). Deciden por sí mismos en qué emplean su dinero – también lo que ahorran en administración.",
    "bess_r4b": "dividendo sin solicitud; complemento en una sola ventanilla local",
    "sich5_p": "La UE ha dejado últimamente de ser capaz de actuar. Una alianza en la que algunos pueden bloquear las decisiones con un veto no puede decidir por todos en la hora de la decisión. De ahí el paso a la decisión por mayoría – por la capacidad de actuar y la competitividad.",
    "fuss_meth_p": "Todas las cifras proceden de un cálculo abierto que cualquiera puede repetir, basado en estadísticas oficiales (Eurostat, OCDE, institutos de estadística y administraciones nacionales) y encuestas publicadas; para Alemania, una microsimulación sintética comprueba la distribución en todos los hogares. Cada cambio y cada error encontrado se registran con un número en el diario. En octubre de 2026, la web y el cálculo se recalcularon en tres revisiones encargadas por la iniciativa (una con su propia microsimulación); hallazgos y respuestas están documentados. Se aceptan revisiones independientes; el material está listo. Desarrollado con el método del proyecto arquitectónico, con herramientas de IA y modelos de cálculo asistidos por IA. Scripts con licencia MIT, textos con CC BY 4.0.",
    "erf5_n": "Australia", "erf5_h": "Ahorro obligatorio en una cuenta propia", "erf5_k": "desde 1992 · 12 % del salario desde 2025",
    "erf5_p": "Los empleadores pagan obligatoriamente en la cuenta de jubilación propia de cada trabajador (superannuation); el dinero pertenece a la cuenta, no al Estado. Desde julio de 2025 es el 12 % del salario.",
    "erf6_n": "Suecia", "erf6_h": "Parte de la pensión en una cuenta propia", "erf6_k": "desde 2000 · 2,5 de 18,5 %",
    "erf6_p": "Del 18,5 % de cotización a la pensión, 2,5 puntos van a la pensión de prima en una cuenta individual. Cada uno elige sus fondos; quien no elige está en el fondo público por defecto.",
}
ERSATZ["es"] = [("Lo que el municipio ahorra activamente en administración llega a sus ciudadanos.", "Lo que municipios y regiones ahorran activamente en administración llega a sus ciudadanos."),
                ("los gestiona el municipio en el lugar – según las reglas del Estado, en una sola ventanilla.", "los gestionan municipios y regiones en el lugar – según las reglas del Estado, en una sola ventanilla."),
                ("y autonomía de los municipios.", "y autonomía de municipios y regiones."),
                ("lo que se pagó en impuestos", "lo que se pagó antes en impuestos"),
                ("Dinamarca y Suecia: valor oficial 2025. ", ""), ("Francia: representando", "Francia 2028: representando")]

NEU["pl"] = {
    "meta_beschreibung": "Najwyżej jedna trzecia od każdego dochodu, mocna sieć bez składek i co miesiąc dywidenda transformacyjna. Gminy i regiony decydują same, wspólny dach chroni wspólne interesy.",
    "nav_gemeinde": "Gminy i regiony",
    "hero_sub": "Wszystkie podatki i daniny są sprawiedliwie rozłożone na pracę, kapitał i automatyzację – najwyżej jedna trzecia od każdego dochodu. Praca się opłaca, a mocna sieć socjalna i dywidenda transformacyjna zapewniają spokój społeczny. Gminy i regiony decydują bardziej samodzielnie, europejski dach chroni wspólne interesy decyzjami większości.",
    "prob_lede": "Dzisiejszy system narastał warstwa po warstwie. Obciąża pracę bardziej niż cokolwiek innego i pozostawia obywateli, gminy i regiony sfrustrowanych.",
    "konz_h2": "Silne gminy i regiony, silni obywatele, silny europejski dach",
    "konz_lede": "Liczba szczebli administracji zostaje zmniejszona. Gminy i regiony otrzymują swój udział bezpośrednio od dachu, same decydują o finansach i przekazują zadania nadrzędnym związkom administracyjnym (np. związkom infrastrukturalnym). Europejski dach przejmuje tylko to, czego gminy i regiony nie zrobią same – i nie może wziąć więcej, niż przewiduje traktat.",
    "svg_weiter": "co najmniej {mind} dla gmin i regionów",
    "svg_gemeinde": "Gminy", "svg_gemeinde_kurz": "Gminy", "svg_gemeinde_sub": "i regiony decydują same", "svg_gemeinde_sub_kurz": "i regiony",
    "eff2_h": "Gminom i regionom ufamy,",
    "eff2_p": "że poprowadzą własne sprawy: otrzymują stałe kwoty na mieszkańca i na dziecko, według tej samej zasady w każdym kraju. Na miejscu wypłacają dopłatę i pomoc w trudnych przypadkach – wysokość i zasadę zaliczania ustala państwo. Decydują o członkostwie w powiatach i związkach oraz o lokalnych programach wsparcia.",
    "eff3_p": "to, co można zrobić tylko razem: obronność i suwerenność cyfrową, rynek wewnętrzny bez granic, wspólne standardy. Nic więcej. Dach decyduje większością delegatów związków gmin i regionów.",
    "fluss_l2": "Zadania gmin i regionów",
    "b5_pos": "Grunt · gminy i regiony", "b5_h": "Gminy i regiony opodatkowują grunt",
    "gem_h2": "Gminy i regiony liczą same",
    "gem_verw": "Udział administracji w budżetach gmin i regionów",
    "gem_fein": "Średnio {verw_klub} budżetów gmin i regionów przypada na administrację. Ich zadania różnią się w poszczególnych krajach; bezpośrednie porównanie udziałów ma więc ograniczoną wartość.",
    "gem_bud": "Budżet gmin i regionów rocznie",
    "sich1_p": "Dach zatrzymuje najwyżej {og} tego, co pobiera dla gmin i regionów – i tylko tyle, ile naprawdę kosztują jego zadania.",
    "sich2_p": "Każde euro ponad potrzeby trafia do gmin i regionów, do mocnej sieci i do dywidendy transformacyjnej.",
    "sich3_p": "Gminy i regiony otrzymują stałe kwoty na mieszkańca i na dziecko. Nikt nie musi prosić, nikt nie może obciąć.",
    "js_fluss": "W roku {j} dach zatrzymuje {a} ze {hundert} – dozwolone byłoby do {cap}. Gminy i regiony przeznaczają {b} na swoje zadania, mocna sieć {n}, a {d} trafia do mieszkańców jako dywidenda transformacyjna.",
    "chan1_h": "Gminy i regiony inwestują w młode pokolenie",
    "chan1_p": "Na każde dziecko w wieku od 5 do 19 lat gminy i regiony otrzymują co roku {formel_kind} – więcej dzieci, więcej pieniędzy. Finansują z tego szkoły, opiekę i wsparcie na miejscu. Opieka, wychowanie i edukacja trafiają do dzieci jako usługi gmin i regionów; dywidenda na dziecko i minimum życiowe pokrywają potrzeby materialne.{chan1_zusatz}",
    "chan4_p": "Kultura, sport i życie wspólnoty pozostają w gminach i regionach (w rachunku całościowym 1,22% PKB). Same decydują, na co wydają pieniądze – także to, co zaoszczędzą na administracji.",
    "bess_r4b": "dywidenda bez wniosku; dopłata w jednym okienku na miejscu",
    "sich5_p": "UE w ostatnim czasie nie jest już zdolna do działania. Sojusz, w którym pojedynczy członkowie mogą zablokować decyzje wetem, nie może w godzinie decyzji zdecydować za wszystkich. Stąd przejście na decyzje większością – dla zdolności do działania i konkurencyjności.",
    "fuss_meth_p": "Wszystkie liczby pochodzą z otwartego rachunku, który każdy może powtórzyć, opartego na oficjalnych statystykach (Eurostat, OECD, krajowe urzędy statystyczne i administracja) i opublikowanych badaniach; dla Niemiec syntetyczna mikrosymulacja sprawdza rozkład we wszystkich gospodarstwach domowych. Każda zmiana i każdy znaleziony błąd są zapisane z numerem w dzienniku. W październiku 2026 strona i rachunek zostały przeliczone w trzech kontrolach zleconych przez inicjatywę (w tym własna mikrosymulacja); ustalenia i odpowiedzi są udokumentowane. Niezależne kontrole są mile widziane, materiały są gotowe. Opracowane metodą projektu architektonicznego, z użyciem narzędzi AI i modeli obliczeniowych wspieranych przez AI. Skrypty na licencji MIT, teksty na CC BY 4.0.",
    "erf5_n": "Australia", "erf5_h": "Obowiązkowe oszczędzanie na własnym koncie", "erf5_k": "od 1992 · 12% płacy od 2025",
    "erf5_p": "Pracodawcy obowiązkowo wpłacają na własne konto emerytalne każdego pracownika (superannuation); pieniądze należą do konta, nie do państwa. Od lipca 2025 to 12% płacy.",
    "erf6_n": "Szwecja", "erf6_h": "Część emerytury na własnym koncie", "erf6_k": "od 2000 · 2,5 z 18,5%",
    "erf6_p": "Z 18,5% składki emerytalnej 2,5 punktu trafia do emerytury premiowej na indywidualnym koncie. Każdy sam wybiera fundusze; kto nie wybierze, jest w państwowym funduszu domyślnym.",
}
ERSATZ["pl"] = [("To, co gmina aktywnie zaoszczędzi na administracji, trafia do jej mieszkańców.", "To, co gminy i regiony aktywnie zaoszczędzą na administracji, trafia do ich mieszkańców."),
                ("rozwiązuje gmina na miejscu – według zasad państwa, w jednym okienku.", "rozwiązują gminy i regiony na miejscu – według zasad państwa, w jednym okienku."),
                ("i samorządność gmin.", "i samorządność gmin i regionów."),
                ("to, co wpłacono w podatkach", "to, co wcześniej wpłacono w podatkach"),
                ("Dania i Szwecja: wartość oficjalna 2025. ", ""), ("Francja: przy ujęciu", "Francja 2028: przy ujęciu")]

NEUE_SCHLUESSEL = {"erf5_n", "erf5_h", "erf5_k", "erf5_p", "erf6_n", "erf6_h", "erf6_k", "erf6_p", "svg_gemeinde_sub_kurz"}


def anwenden(sp, quelle, basis):
    """quelle: Texte der Seite (drittel_bau.texte), basis: sprachen/<sp>.json. Ersatz in quelle oder, wenn dort nicht vorhanden, in basis."""
    for k, v in NEU.get(sp, {}).items():
        quelle[k] = v
    for alt, neu in ERSATZ.get(sp, []):
        treffer = [k for k, v in list(quelle.items()) + [(k, v) for k, v in basis.items() if k not in quelle] if isinstance(v, str) and alt in v]
        if len(treffer) != 1:
            raise SystemExit(f"kommunen_texte {sp}: Ersatz nicht eindeutig ({len(treffer)}): {alt[:60]}")
        k = treffer[0]
        quelle[k] = (quelle[k] if k in quelle else basis[k]).replace(alt, neu)
