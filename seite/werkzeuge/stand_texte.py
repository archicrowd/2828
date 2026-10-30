"""Texte der Seite Stand C nach dem Projektstand v4.54 (Logbuch v4.55), sechs Sprachen.

Nur maßgebliche Änderungen seit dem Paket v4.45 (Beschlüsse und Rechnungen v4.46 bis v4.54):
  b2_p        Weitergabe nur aus den entfallenden Beiträgen zur sozialen Sicherung (E16, v4.52)
  b8_p        Label: günstigere Stufe über Zertifizierung bei zugelassenen, staatlich überwachten Stellen (E15, v4.49)
  b10_p,
  div_p1      Dividende: Lenkung und Digitalisierungsgewinne (Plattformen am Ort der Kundschaft) (E15, v4.49)
  b11_p       Pflichtvorsorge: Sperrkonto bis zur Altersgrenze, wenige Anlageoptionen, Standardfonds (E13, v4.49/v4.50)
  eff2_p,
  bess_r4b    Aufstockung auf Antrag, Hinweis und vorausgefüllter Antrag von Amts wegen (E12, v4.50)
  sich4_p     Kürzung der Altzusagen ab dem Stichtag für alle Rentenzahlungen, gleich wann die Rente begann (E14, v4.49)
  fuss_meth_p Ländermodelle gegen OECD Taxing Wages 2026 geprüft (v4.51)
Zahlen kommen weiter aus den Ergebnisdateien. Angewandt am Ende von drittel_bau.texte(); jede alte Stelle muss genau einmal vorkommen.
Übersetzungen maschinell, muttersprachlich gegenzulesen (P3).
"""

# (Schlüssel, alt, neu) je Sprache; neu = alt + Zusatz, wo nur ergänzt wird
_Z = lambda alt, zusatz: (alt, alt + zusatz)

ERSATZ = {
 "de": [
  ("b2_p",) + _Z("Betriebe geben mindestens 80 % der gesparten Arbeitgeberbeiträge in den Lohn.",
                 " Das sind die Beiträge, die wegfallen – für Krankheit, Pflege, Rente, Arbeitslosigkeit und Familie; Unfallversicherung und Abgaben "
                 "für Ausbildung, Wohnungsbau und Verkehr bleiben beim Betrieb."),
  ("b8_p",) + _Z("33 % gelten nur für Schädliches.",
                 " Günstigere Stufen erreichen Anbieter durch Zertifizierung bei zugelassenen, staatlich überwachten Stellen – ein Wettbewerb um "
                 "Nachhaltigkeit."),
  ("b10_p", "Sie gibt vor allem zurück, was der Wandel einbringt.",
   "Sie beteiligt alle an dem, was der Wandel einbringt: Lenkungssteuern und die Gewinne der Digitalisierung."),
  ("div_p1", "– vor allem das, was der Wandel einbringt: CO₂-Preis und die Sonderstufe für Schädliches.",
   "– aus dem, was der Wandel einbringt: CO₂-Preis und Sonderstufe für Schädliches, dazu die Besteuerung digitaler Plattformen am Ort ihrer "
   "Kundschaft."),
  ("b11_p", "(10 % des Lohns aufs eigene Rentenkonto)",
   "(10 % des Lohns aufs eigene Rentenkonto, gesperrt bis zur Altersgrenze; wenige Anlageoptionen, ein Standardfonds für alle, die nicht wählen)"),
  ("eff2_p", "Sie zahlt Aufstockung und Härtefallhilfe vor Ort aus – Höhe und Anrechnung legt das Land fest.",
   "Sie zahlt Aufstockung und Härtefallhilfe vor Ort auf Antrag aus; wer nach Steuer- und Lohndaten Anspruch haben dürfte, erhält von Amts wegen "
   "einen vorausgefüllten Antrag. Höhe und Anrechnung legt das Land fest."),
  ("bess_r4b", "Aufstockung an einer Stelle der Kommunen und Regionen",
   "Aufstockung auf vorausgefüllten Antrag an einer Stelle der Kommunen und Regionen"),
  ("sich4_p", "werden auf den Teil über dem Grundbedarf um 15 % gekürzt;",
   "werden ab dem Stichtag auf den Teil über dem Grundbedarf um 15 % gekürzt, gleich wann die Rente begann;"),
  ("fuss_meth_p", "prüft eine synthetische Mikrosimulation die Verteilung über alle Haushalte.",
   "prüft eine synthetische Mikrosimulation die Verteilung über alle Haushalte; die Steuer- und Abgabenmodelle der Länder sind gegen die "
   "Vergleichsrechnung der OECD (Taxing Wages 2026) geprüft, Abweichungen sind im Logbuch erklärt."),
 ],
 "en": [
  ("b2_p",) + _Z("Employers pass at least 80% of the employer contributions they save into wages.",
                 " These are the contributions that disappear – for health, long-term care, pensions, unemployment and family; accident insurance and "
                 "levies for training, housing and transport stay with the employer."),
  ("b8_p",) + _Z("33% applies only to harmful goods.",
                 " Suppliers reach a lower rate through certification by approved, state-supervised bodies – a competition for sustainability."),
  ("b10_p", "Above all, it returns what the transformation brings in.",
   "It gives everyone a share of what the transformation brings in: steering taxes and the gains of digitalisation."),
  ("div_p1", "– above all what the transformation brings in: the carbon price and the special rate on harmful goods.",
   "– from what the transformation brings in: the carbon price and the special rate on harmful goods, plus the taxation of digital platforms "
   "where their customers are."),
  ("b11_p", "(10% of wages into your own pension account)",
   "(10% of wages into your own pension account, locked until retirement age; a few investment options and a default fund for anyone who does "
   "not choose)"),
  ("eff2_p", "under the same rule in every country.",
   "under the same rule in every country. They pay out the top-up and hardship support locally, on application; anyone whose tax and wage data "
   "suggest an entitlement receives a pre-filled application. The country sets the amounts and how income is counted."),
  ("bess_r4b", "top-up at one local office", "top-up on a pre-filled application at one local office"),
  ("sich4_p", "are reduced by 15% on the part above basic needs;",
   "are reduced from the start date by 15% on the part above basic needs, whenever the pension began;"),
  ("fuss_meth_p", "checks the distribution across all households.",
   "checks the distribution across all households; the countries' tax and contribution models are checked against the OECD's comparative "
   "calculation (Taxing Wages 2026), and deviations are explained in the log."),
 ],
 "fr": [
  ("b2_p",) + _Z("Les entreprises reversent au moins 80 % des cotisations patronales économisées dans les salaires.",
                 " Il s'agit des cotisations qui disparaissent – maladie, dépendance, retraite, chômage et famille ; les accidents du travail et les "
                 "contributions à la formation, au logement et aux transports restent à la charge de l'employeur."),
  ("b8_p",) + _Z("33 % ne s'appliquent qu'aux produits nocifs.",
                 " Les fournisseurs obtiennent un taux plus bas par une certification auprès d'organismes agréés et contrôlés par l'État – une "
                 "concurrence pour la durabilité."),
  ("b10_p", "Il rend avant tout ce que la transition rapporte.",
   "Il fait participer chacun à ce que la transition rapporte : taxes incitatives et gains de la numérisation."),
  ("div_p1", "– surtout ce que la transition rapporte : le prix du CO₂ et le taux spécial sur les produits nocifs.",
   "– à partir de ce que la transition rapporte : le prix du CO₂ et le taux spécial sur les produits nocifs, ainsi que l'imposition des "
   "plateformes numériques là où se trouvent leurs clients."),
  ("b11_p", "(10 % du salaire sur votre propre compte retraite)",
   "(10 % du salaire sur votre propre compte retraite, bloqué jusqu'à l'âge de la retraite ; quelques options de placement et un fonds par "
   "défaut pour qui ne choisit pas)"),
  ("eff2_p", "selon la même règle dans chaque pays.",
   "selon la même règle dans chaque pays. Elles versent sur place, sur demande, le complément et l'aide en cas de difficulté ; quiconque semble y "
   "avoir droit d'après ses données fiscales et salariales reçoit d'office une demande pré-remplie. Le montant et la prise en compte des revenus "
   "sont fixés par l'État."),
  ("bess_r4b", "complément à un seul guichet local", "complément sur demande pré-remplie à un seul guichet local"),
  ("sich4_p", "sont réduites de 15 % sur la part au-dessus du besoin de base ;",
   "sont réduites, à partir de la date d'entrée en vigueur, de 15 % sur la part au-dessus du besoin de base, quelle que soit la date de départ à "
   "la retraite ;"),
  ("fuss_meth_p", "vérifie la répartition sur l'ensemble des ménages.",
   "vérifie la répartition sur l'ensemble des ménages ; les modèles d'impôts et de cotisations des pays sont vérifiés par rapport au calcul "
   "comparatif de l'OCDE (Taxing Wages 2026), les écarts sont expliqués dans le journal."),
 ],
 "it": [
  ("b2_p",) + _Z("Le imprese trasferiscono nei salari almeno l'80% dei contributi risparmiati.",
                 " Si tratta dei contributi che vengono meno – malattia, assistenza, pensione, disoccupazione e famiglia; l'assicurazione contro gli "
                 "infortuni e i contributi per formazione, casa e trasporti restano a carico dell'impresa."),
  ("b8_p",) + _Z("Il 33 % vale solo per i prodotti dannosi.",
                 " I fornitori ottengono un'aliquota più bassa con la certificazione presso enti autorizzati e vigilati dallo Stato – una concorrenza "
                 "per la sostenibilità."),
  ("b10_p", "Restituisce soprattutto ciò che la trasformazione porta.",
   "Fa partecipare tutti a ciò che la trasformazione porta: imposte di orientamento e guadagni della digitalizzazione."),
  ("div_p1", "– soprattutto ciò che la trasformazione porta: il prezzo della CO₂ e l'aliquota speciale sui prodotti dannosi.",
   "– da ciò che la trasformazione porta: il prezzo della CO₂ e l'aliquota speciale sui prodotti dannosi, oltre alla tassazione delle "
   "piattaforme digitali dove si trovano i loro clienti."),
  ("b11_p", "(10% del salario sul tuo conto pensione)",
   "(10% del salario sul tuo conto pensione, vincolato fino all'età pensionabile; poche opzioni d'investimento e un fondo predefinito per chi "
   "non sceglie)"),
  ("eff2_p", "con la stessa regola in ogni paese.",
   "con la stessa regola in ogni paese. Erogano sul posto, su domanda, l'integrazione e l'aiuto nei casi di disagio; chi in base ai dati "
   "fiscali e salariali sembra averne diritto riceve d'ufficio una domanda precompilata. Importo e computo dei redditi li stabilisce lo Stato."),
  ("bess_r4b", "integrazione a un unico sportello locale", "integrazione su domanda precompilata a un unico sportello locale"),
  ("sich4_p", "sono ridotte del 15% sulla parte sopra il fabbisogno di base;",
   "sono ridotte, dalla data di introduzione, del 15% sulla parte sopra il fabbisogno di base, indipendentemente da quando è iniziata la "
   "pensione;"),
  ("fuss_meth_p", "verifica la distribuzione su tutte le famiglie.",
   "verifica la distribuzione su tutte le famiglie; i modelli fiscali e contributivi dei paesi sono verificati rispetto al calcolo comparativo "
   "dell'OCSE (Taxing Wages 2026), gli scostamenti sono spiegati nel registro."),
 ],
 "es": [
  ("b2_p",) + _Z("Las empresas trasladan al salario al menos el 80 % de las cotizaciones empresariales que ahorran.",
                 " Son las cotizaciones que desaparecen – contingencias comunes, desempleo y equidad intergeneracional; los accidentes de trabajo, "
                 "el FOGASA y la formación profesional siguen a cargo de la empresa."),
  ("b8_p",) + _Z("El 33 % solo se aplica a lo dañino.",
                 " Los proveedores alcanzan un tipo más bajo mediante la certificación de entidades autorizadas y supervisadas por el Estado: una "
                 "competencia por la sostenibilidad."),
  ("b10_p", "Devuelve sobre todo lo que aporta la transformación.",
   "Hace partícipes a todos de lo que aporta la transformación: impuestos correctores y ganancias de la digitalización."),
  ("div_p1", "– sobre todo lo que aporta la transformación: el precio del CO₂ y el tipo especial sobre lo dañino.",
   "– a partir de lo que aporta la transformación: el precio del CO₂ y el tipo especial sobre lo dañino, además de la tributación de las "
   "plataformas digitales donde están sus clientes."),
  ("b11_p", "(10 % del salario en tu propia cuenta de jubilación)",
   "(10 % del salario en tu propia cuenta de jubilación, bloqueada hasta la edad de jubilación; pocas opciones de inversión y un fondo por "
   "defecto para quien no elige)"),
  ("eff2_p", "con la misma regla en cada país.",
   "con la misma regla en cada país. Pagan en el lugar, previa solicitud, el complemento y la ayuda en casos difíciles; quien según sus datos "
   "fiscales y salariales pueda tener derecho recibe de oficio una solicitud prerrellenada. La cuantía y el cómputo de ingresos los fija el "
   "Estado."),
  ("bess_r4b", "complemento en una sola ventanilla local", "complemento con solicitud prerrellenada en una sola ventanilla local"),
  ("sich4_p", "se reducen un 15 % en la parte por encima de la necesidad básica;",
   "se reducen, desde la fecha de entrada en vigor, un 15 % en la parte por encima de la necesidad básica, sea cual sea la fecha de inicio de "
   "la pensión;"),
  ("fuss_meth_p", "comprueba la distribución en todos los hogares.",
   "comprueba la distribución en todos los hogares; los modelos de impuestos y cotizaciones de los países se contrastan con el cálculo "
   "comparativo de la OCDE (Taxing Wages 2026) y las desviaciones se explican en el diario."),
 ],
 "pl": [
  ("b2_p",) + _Z("Firmy przekazują do wynagrodzeń co najmniej 80% zaoszczędzonych składek pracodawcy.",
                 " Chodzi o składki, które znikają – emerytalne, rentowe i na Fundusz Pracy; składka wypadkowa i na Fundusz Gwarantowanych "
                 "Świadczeń Pracowniczych pozostają po stronie pracodawcy."),
  ("b8_p",) + _Z("Stawka 33 % dotyczy tylko produktów szkodliwych.",
                 " Niższą stawkę dostawcy uzyskują dzięki certyfikacji w uprawnionych jednostkach nadzorowanych przez państwo – to konkurencja "
                 "o zrównoważony rozwój."),
  ("b10_p", "Oddaje przede wszystkim to, co przynosi transformacja.",
   "Daje każdemu udział w tym, co przynosi transformacja: w podatkach sterujących i zyskach z cyfryzacji."),
  ("div_p1", "– przede wszystkim to, co przynosi transformacja: cenę CO₂ i stawkę specjalną na produkty szkodliwe.",
   "– z tego, co przynosi transformacja: z ceny CO₂ i stawki specjalnej na produkty szkodliwe, a także z opodatkowania platform cyfrowych "
   "w miejscu ich klientów."),
  ("b11_p", "(10% wynagrodzenia na własne konto emerytalne)",
   "(10% wynagrodzenia na własne konto emerytalne, zablokowane do wieku emerytalnego; kilka opcji inwestycyjnych i fundusz domyślny dla tych, "
   "którzy nie wybierają)"),
  ("eff2_p", "Na miejscu wypłacają dopłatę i pomoc w trudnych przypadkach – wysokość i zasadę zaliczania ustala państwo.",
   "Na miejscu, na wniosek, wypłacają dopłatę i pomoc w trudnych przypadkach; kto według danych podatkowych i płacowych może mieć do nich "
   "prawo, otrzymuje z urzędu wstępnie wypełniony wniosek. Wysokość i zasadę zaliczania ustala państwo."),
  ("bess_r4b", "dopłata w jednym okienku na miejscu", "dopłata na wstępnie wypełniony wniosek w jednym okienku na miejscu"),
  ("sich4_p", "są obniżane o 15% w części powyżej potrzeb podstawowych;",
   "są od dnia wprowadzenia obniżane o 15% w części powyżej potrzeb podstawowych, niezależnie od tego, kiedy emerytura się rozpoczęła;"),
  ("fuss_meth_p", "sprawdza rozkład we wszystkich gospodarstwach domowych.",
   "sprawdza rozkład we wszystkich gospodarstwach domowych; modele podatków i składek poszczególnych krajów są sprawdzane względem "
   "porównawczego rachunku OECD (Taxing Wages 2026), a odchylenia wyjaśnia dziennik."),
 ],
}


def anwenden(sp, texte):
    """Ersetzt in den fertigen Texten einer Sprache; jede alte Stelle muss im Schlüssel genau einmal vorkommen."""
    for k, alt, neu in ERSATZ.get(sp, []):
        t = texte.get(k, "")
        for z in (" ", "\xa0", "\u202f"):            # Leerzeichen vor % wie in der Vorlage (geschützt oder schmal)
            a, n = alt.replace(" %", z + "%"), neu.replace(" %", z + "%")
            if t.count(a) == 1:
                break
        else:
            raise SystemExit(f"stand_texte {sp}/{k}: Stelle nicht genau einmal gefunden: {alt[:60]}")
        texte[k] = t.replace(a, n)
    return texte
