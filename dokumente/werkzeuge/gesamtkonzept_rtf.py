#!/usr/bin/env python3
"""Baut die einführende Fassung des Gesamtkonzepts als RTF: dokumente/TAX-2828-Gesamtkonzept.rtf (seit v3.41).

Aufbau vom Kleinen zum Großen: der einzelne Mensch an seinem Ort, die Gemeinde, das gemeinsame Dach, die Kooperation
mehrerer Staaten im Möglichkeitsraum, die Rechnung. Der Text richtet sich an Lesende, die das Konzept zum ersten Mal sehen;
er verweist nicht auf frühere Fassungen. Keine Zahl von Hand: alle Zahlen kommen aus daten/aggregate/*.json und *.csv
(modell/gesamtrechnung.py und Folgestufen), das Quellenverzeichnis aus daten/quellen_verzeichnis.json.

Begriffe (statt der Arbeitsbegriffe des Logbuchs): „Staatengemeinschaft“ bzw. „teilnehmende Staaten“ statt „Klub“;
„das gemeinsame Dach“ statt „Ebene A“; „Gemeinde“ statt „Ebene B“; „Mindestniveau der Dividende“ statt „Boden“;
„Grundstücksabgabe“ statt „Bodenwertabgabe“.

Aufruf:  python3 dokumente/werkzeuge/gesamtkonzept_rtf.py
"""
import csv
import json
from pathlib import Path

W = Path(__file__).resolve().parents[2]
AGG = W / "daten" / "aggregate"
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
TF = json.loads((AGG / "tragfaehigkeit.json").read_text(encoding="utf-8"))
TG = json.loads((AGG / "tarif_grundbedarf.json").read_text(encoding="utf-8"))
NF = json.loads((AGG / "nachfrage.json").read_text(encoding="utf-8"))
QV = json.loads((W / "daten" / "quellen_verzeichnis.json").read_text(encoding="utf-8"))
RAUM = list(csv.DictReader(open(AGG / "moeglichkeitsraum.csv", encoding="utf-8")))
ZIEL = W / "dokumente" / "TAX-2828-Gesamtkonzept.rtf"


# ---------------------------------------------------------------- Zahlenformat
def de(x, nk=0):
    s = f"{x:,.{nk}f}"
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")


def pr(x, nk=1):
    return de(x, nk) + " %"


def eur(x, nk=0):
    return de(x, nk) + " €"


# ---------------------------------------------------------------- RTF-Bausteine
def esc(t):
    out = []
    for ch in t:
        o = ord(ch)
        if ch in "\\{}":
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\line ")
        elif o < 128:
            out.append(ch)
        else:
            out.append(f"\\u{o if o < 32768 else o - 65536}?")
    return "".join(out)


def runs(teile):
    """teile: str oder Liste aus str und (text, 'b'|'i'|'bi')."""
    if isinstance(teile, str):
        return esc(teile)
    s = []
    for x in teile:
        if isinstance(x, str):
            s.append(esc(x))
        else:
            t, f = x
            a = ("\\b " if "b" in f else "") + ("\\i " if "i" in f else "")
            e = ("\\b0" if "b" in f else "") + ("\\i0" if "i" in f else "")
            s.append("{" + a + esc(t) + e + "}")
    return "".join(s)


DOC = []


def P(teile, sb=0, sa=140, fs=21, ind=0):
    DOC.append(f"\\pard\\sa{sa}\\sb{sb}\\sl276\\slmult1\\li{ind}\\fs{fs} " + runs(teile) + "\\par\n")


def H1(t):
    DOC.append(f"\\pard\\keepn\\sb360\\sa160\\fs30\\b\\cf1 {esc(t)}\\b0\\cf0\\par\n")


def H2(t):
    DOC.append(f"\\pard\\keepn\\sb220\\sa100\\fs24\\b\\cf1 {esc(t)}\\b0\\cf0\\par\n")


def LISTE(punkte):
    for p in punkte:
        DOC.append("\\pard\\sa80\\sl276\\slmult1\\li360\\fi-240\\fs21 \\bullet\\tab " + runs(p) + "\\par\n")
    DOC.append("\\pard\\sa60\\par\n")


def TAB(kopf, zeilen, breiten, rechts=(), fett=()):
    """breiten in Twips; rechts: Spaltenindizes rechtsbündig; fett: Zeilenindizes fett."""
    def zeile(werte, kopfzeile=False, b=False):
        r = ["\\trowd\\trgaph80\\trleft0"]
        x = 0
        for w in breiten:
            x += w
            sh = "\\clcbpat2" if kopfzeile else ""
            r.append(f"{sh}\\clbrdrb\\brdrs\\brdrw4\\brdrcf3\\cellx{x}")
        r.append("\n")
        for i, v in enumerate(werte):
            al = "\\qr" if i in rechts else "\\ql"
            f = "\\b " if (kopfzeile or b) else ""
            r.append(f"\\pard\\intbl{al}\\sa40\\fs19 {f}{esc(str(v))}\\b0\\cell\n")
        r.append("\\row\n")
        return "".join(r)
    DOC.append(zeile(kopf, True))
    for i, z in enumerate(zeilen):
        DOC.append(zeile(z, b=i in fett))
    DOC.append("\\pard\\sa160\\par\n")


def NOTIZ(t):
    P([(t, "i")], sa=160, fs=18)


# ---------------------------------------------------------------- abgeleitete Größen
q, og = G["quote"], G["obergrenze"]
stufen = TG["stufen_de_2028"]
G28 = TG["grundbedarf_2028"]
saetze = TG["saetze"]
ld = G["tabelle_laender_div"]
deL = next(r for r in ld if r["land"] == "DE")
unter = [r["name"] for r in ld if r["v2_unter_boden"]]
p0, tp = G["tabelle_pfad"][0], G["tabelle_pfad"]
erw, kind = G["erw_de_2028"], G["kind_de_2028"]
europa = [r for r in RAUM if r["land"] not in ("US", "CA")]
raum_mio = sum(float(r["einwohner_mio"]) for r in europa)
us_mio = next(float(r["einwohner_mio"]) for r in RAUM if r["land"] == "US")
lk = G["deckung_luecke"]
st = NF["labelsatz_steuernd"]


def liste(a):
    return a[0] if len(a) == 1 else ", ".join(a[:-1]) + " und " + a[-1]


def steuer(x):
    s, u = 0.0, 0.0
    for g, p in zip(stufen + [float("inf")], saetze):
        if x > u:
            s += (min(x, g) - u) * p / 100
        u = g
    return s


# Rechenbeispiel: zwei Erwachsene, zwei Kinder, ein Einkommen
brutto = 42000
div_erw_jahr = erw * 12
st_verdiener = steuer(brutto + div_erw_jahr)
st_partner = steuer(div_erw_jahr)
div_hh = 2 * div_erw_jahr + 2 * kind * 12
st_hh = st_verdiener + st_partner

A = dict((n, v) for n, v, _ in G["tabelle_a"])
B = dict((n, v) for n, v, _ in G["tabelle_b"])
a_ohne_v_zd = G["a_ohne_v"]

# ---------------------------------------------------------------- Text
DOC.append("{\\rtf1\\ansi\\ansicpg1252\\deff0\\uc1\n{\\fonttbl{\\f0\\fswiss Calibri;}}\n"
           "{\\colortbl;\\red31\\green56\\blue100;\\red242\\green242\\blue242;\\red191\\green191\\blue191;}\n"
           "{\\info{\\title TAX 28:28 - Das Gesamtkonzept}{\\author Initiative 28:28}}\n"
           "\\paperw11906\\paperh16838\\margl1418\\margr1418\\margt1134\\margb1134\\f0\\fs21\n")

DOC.append(f"\\pard\\sa60\\fs44\\b\\cf1 TAX 28:28\\b0\\par\n\\pard\\sa60\\fs30 Das Gesamtkonzept\\cf0\\par\n")
P([(f"Eine Einführung · Fassung {G['fassung']} · Modellstand {G['version']} · Initiative 28:28", "i")], fs=19, sa=300)

H1("Inhalt")
INHALT = ["1  Worum es geht",
          "2  Der einzelne Mensch an seinem Ort",
          "3  Die Gemeinde",
          "4  Das gemeinsame Dach",
          "5  Kooperation im Möglichkeitsraum",
          "6  Wie die Rechnung aufgeht",
          "7  Was noch offen ist",
          "8  Zahlengrundlage",
          "Quellenverzeichnis"]
for z in INHALT:
    P(z, sa=40)
DOC.append("\\pard\\sa200\\par\\page\n")

# 1 ---------------------------------------------------------------------------
H1("1  Worum es geht")
P("Die heutige Steuer- und Abgabenordnung ist über Jahrzehnte gewachsen, Schicht um Schicht, Ausnahme um Ausnahme. "
  "Wer heute arbeitet, zahlt Einkommensteuer, Sozialbeiträge, Mehrwertsteuer und eine Reihe weiterer Abgaben, jeweils "
  "mit eigenen Regeln. Fünf staatliche Ebenen – Gemeinde, Kreis, Land, Bund und Europäische Union – teilen sich Aufgaben "
  "und Geld und verhandeln ständig darüber. Eine Gemeinde, die etwas verändern will, bekommt Mittel, die zweckgebunden "
  "ankommen und über die anderswo entschieden wurde. Was sie spart, behält sie nicht.")
P(["TAX 28:28 schlägt ein neues Grundsystem vor. Es beruht auf drei Gedanken:"])
LISTE([[("Wenige, gleiche Regeln für jeden Menschen. ", "b"),
        "Höchstens 28 % auf Einkommen, keine Sozialbeiträge, keine Abzüge und Sonderregeln. Jeden Monat eine Dividende, "
        "also eine Auszahlung an jeden Menschen ohne Antrag."],
       [("Starke Gemeinden. ", "b"),
        "Die Gemeinde erhält den größten Teil des Geldes nach einer festen Formel und entscheidet selbst, was sie damit tut."],
       [("Ein schlankes gemeinsames Dach. ", "b"),
        "Darüber steht nur noch eine Ebene, die übernimmt, was keine Gemeinde allein kann. Sie darf höchstens einen "
        "festen Anteil dessen behalten, was sie einzieht."]])
P(["Der Name steht für den Satz: ", ("28 % ", "b"),
   "ist der höchste Satz auf Einkommen von Menschen und ebenso der Satz auf Gewinne von Unternehmen. Er bezeichnet "
   "nicht die gesamte Abgabenlast; die liegt höher, weil auch Konsum, Kapital, Erbschaften und Grundstücke beitragen "
   f"(Abschnitt 6)."])
P("Dieser Text beginnt beim einzelnen Menschen und seinem Wohnort, geht dann zur Gemeinde und zum gemeinsamen Dach "
  "und endet bei der Frage, warum es sich lohnt, das Dach mit anderen Staaten zu teilen. Zum Schluss zeigt er, wie "
  "die Rechnung aufgeht und was noch offen ist.")
P(["Alle Beträge sind für das Startjahr 2028 gerechnet, in Euro und Preisen von 2028, soweit nicht anders angegeben. "
   "Die Zahlen beruhen auf amtlichen Statistiken einer Gruppe von zehn europäischen Staaten (Abschnitt 8). "
   "Deutschland dient als Beispielland. Wo von Wirtschaftsleistung die Rede ist, ist das Bruttoinlandsprodukt (BIP) "
   "gemeint: der Wert aller Güter und Dienstleistungen, die in einem Land in einem Jahr erzeugt werden. Viele Größen "
   "sind als Anteil daran angegeben (% des BIP)."])

# 2 ---------------------------------------------------------------------------
H1("2  Der einzelne Mensch an seinem Ort")
H2("2.1  Das Maß: der Grundbedarf")
P(["Viele Regeln dieses Konzepts hängen an einer einzigen Größe, dem ", ("Grundbedarf", "b"),
   ". Gemeint ist das Geld, das ein Erwachsener im Jahr mindestens zum Leben braucht. Als Maß dient das steuerliche "
   "Existenzminimum: In Deutschland bleibt 2026 ein Einkommen von 12.348 € im Jahr steuerfrei (Grundfreibetrag, "
   f"§ 32a Einkommensteuergesetz). Mit 2 % Preissteigerung im Jahr fortgeschrieben sind das 2028 rund {eur(G28)}."])
P("In anderen Ländern gilt derselbe Gedanke mit dem dortigen Preisniveau: Wo das Leben teurer ist, ist der Grundbedarf "
  "höher, wo es günstiger ist, niedriger. Steigen die Preise, steigt der Grundbedarf mit – und mit ihm alle Grenzen, die "
  "an ihm hängen. Eine schleichende Mehrbelastung durch Inflation (kalte Progression) gibt es deshalb nicht.")

H2("2.2  Einkommen: ein Stufentarif mit fester Obergrenze")
P("Besteuert wird das gesamte Bruttoeinkommen eines Menschen, ohne Abzüge und ohne gemeinsame Veranlagung von "
  "Ehepaaren. Jeder Mensch wird für sich besteuert. Der Tarif hat fünf Stufen; jeder Satz gilt nur für den Teil des "
  "Einkommens, der in seiner Stufe liegt:")
grenzen_text = ["1", "1,5", "2", "3"]
zeilen = [[f"bis {eur(stufen[0])}", "0 %", "bis zum Grundbedarf"]]
for i in range(1, 4):
    zeilen.append([f"{eur(stufen[i-1])} bis {eur(stufen[i])}", f"{saetze[i]} %",
                   f"vom {grenzen_text[i-1]}- bis zum {grenzen_text[i]}-fachen Grundbedarf"])
zeilen.append([f"über {eur(stufen[3])}", f"{saetze[4]} %", "über dem 3-fachen Grundbedarf"])
TAB(["Einkommen im Jahr (Deutschland 2028)", "Satz", "Lage"], zeilen, [3300, 1100, 4600], rechts=(1,))
P(["Wer nur so viel verdient, wie er zum Leben braucht, zahlt nichts. Darüber steigt der Satz in kleinen Schritten "
   "bis 28 % und nicht weiter. Weil jede Stufe nur für ihren Teil gilt, bleibt von jedem zusätzlich verdienten Euro "
   "immer mindestens 72 Cent übrig. Die Dividende eines Erwachsenen (Abschnitt 2.7) zählt zu seinem Einkommen; die "
   "Dividende für Kinder bleibt steuerfrei."])

H2("2.3  Kapital, Erbschaft, Vermögen")
LISTE([[("Kapitalerträge ", "b"), "– Zinsen, Dividenden von Aktien, Gewinne aus dem Verkauf von Wertpapieren – werden "
        "mit 28 % besteuert, genauso hoch wie der höchste Satz auf Arbeit. Es lohnt sich dann nicht mehr, Arbeitslohn "
        "in Kapitalertrag umzuwandeln."],
       [("Erbschaften und Schenkungen ", "b"), "über 100.000 € je Empfänger werden mit 28 % besteuert, ohne "
        "Ausnahmen für bestimmte Vermögensarten. Wer einen Betrieb oder ein Haus erbt, kann die Steuer stunden: "
        "anfangs zum Zinssatz, zu dem sich der Staat Geld leiht, über zehn Jahre steigend bis zum marktüblichen "
        "Kreditzins. Niemand muss verkaufen, um zu zahlen; der offene Betrag wird beim Verkauf fällig."],
       [("Große Vermögen ", "b"), "über 2 Mio. € tragen eine Mindeststeuer von 1,5 % im Jahr. Vermögen darunter "
        "bleibt unberührt."]])

H2("2.4  Konsum: die Mehrwertsteuer als Label")
P("Auf alles, was gekauft wird, fällt Mehrwertsteuer an. Neu ist, dass ihr Satz wie ein Energielabel sichtbar macht, "
  "wie viele Ressourcen ein Produkt verbraucht. Eingestuft wird nach dem Ressourcen- und CO₂-Fußabdruck je Euro "
  "Kaufpreis, einschließlich der Transportwege – nicht nach dem Herkunftsland.")
TAB(["Stufe", "Satz", "Beispiele"],
    [["A+", "5 %", "Grundnahrungsmittel, Reparaturen, persönliche Dienstleistungen, Nahverkehr"],
     ["A", "11 %", "Gaststätten und Hotels, nachhaltige Güter"],
     ["B", "17 %", "Standardgüter, Kommunikation"],
     ["C", "22 %", "Kleidung, Einrichtung, Freizeitgüter, Haushaltsenergie"],
     ["D", "28 %", "Fahrzeuge, Kraftstoffe, Alkohol und Tabak"]],
    [900, 900, 7200], rechts=(1,))
P(f"Über den ganzen Einkauf eines durchschnittlichen Haushalts gerechnet ergibt das einen Satz von etwa "
  f"{pr(G['label_effektiv'])}; das liegt knapp über der heutigen Belastung mit deutschen Sätzen (rund "
  f"{pr(st['effektiv_heute_de_saetze_pct'], 0)}), die Preise bleiben im Mittel etwa gleich. "
  "Teurer werden ressourcenintensive Güter, günstiger Grundbedarf und Reparatur. Wohnungsmieten, Gesundheit und Bildung "
  "bleiben wie heute steuerfrei. Wie stark ein sichtbares Label das Kaufverhalten über den Preis hinaus lenkt, ist "
  "wissenschaftlich noch offen; die Rechnung setzt nur die Preiswirkung an.")

H2("2.5  Klima: ein gemeinsamer CO₂-Preis")
P("Wer fossile Energie verbraucht, zahlt einen Preis für das ausgestoßene CO₂. Der Preis folgt einem europäischen Pfad "
  "entlang der vereinbarten Klimaziele; die Rechnung setzt 100 € je Tonne an, steigend auf 150 €. Die Einnahmen fließen in den gemeinsamen "
  "Topf, aus dem die Dividende gezahlt wird. Wer wenig verbraucht, bekommt über die Dividende mehr zurück, als er über "
  "den CO₂-Preis zahlt. Steuervorteile für fossile Energie entfallen.")

H2("2.6  Keine Sozialbeiträge, aber ein Schutz für alle")
P(f"Heute werden auf jeden Lohn Sozialbeiträge erhoben, die Arbeit teurer machen; in den zehn gerechneten Staaten "
  f"zusammen sind es {pr(G['sb_heute'], 2)} der Wirtschaftsleistung. Diese Beiträge entfallen. Die Dividende übernimmt die "
  "Grundsicherung. Die Gesundheitsversorgung wird gesondert finanziert; wie, regelt dieses Konzept nicht, die Rechnung "
  f"setzt die heutigen Gesundheitsausgaben ({pr(G['gesundheit'], 2)} des BIP) außerhalb der Steuern an. Vorsorge darüber hinaus wird Sache des "
  "Einzelnen, der Tarifparteien und der Gemeinde. Dass ein Sozialstaat fast ohne Sozialbeiträge auskommt, zeigt "
  "Dänemark: Es erhebt Sozialbeiträge von 0,7 % der Wirtschaftsleistung und finanziert seine Sozialleistungen aus Steuern.")
P(["Damit niemand schlechter dasteht, gibt es eine ", ("Bestandsgarantie", "b"),
   ": Wer heute Bürgergeld, Grundsicherung oder BAföG erhält, bekommt mindestens das bisherige Niveau. Die Differenz "
   "zur Dividende trägt ein Härtefallfonds, der auch Wohnkosten, Pflege, Behinderung und besondere Lebenslagen abdeckt."])

H2("2.7  Die Dividende")
P(["Die ", ("Dividende", "b"), " ist eine monatliche Auszahlung an jeden Menschen, ohne Antrag und ohne Prüfung der "
   "Bedürftigkeit. Erwachsene erhalten den vollen Betrag, Kinder die Hälfte. Sie ist kein fester Betrag, den der Staat "
   "verspricht, sondern das, was vom gemeinsamen Steueraufkommen übrig bleibt, nachdem die Aufgaben der Gemeinde und des "
   "Daches bezahlt sind (Abschnitt 6). Darum steigt sie, wenn die Wirtschaft wächst oder wenn Verwaltung sparsamer wird."])
P(["Die Höhe richtet sich nach der Wirtschaftsleistung des eigenen Landes: Jedes Land zahlt denselben Anteil seiner "
   f"Wirtschaftsleistung je Kopf als Dividende aus. In Deutschland sind das 2028 ", (f"{eur(erw)} je Erwachsenem", "b"),
   f" und {eur(kind)} je Kind im Monat. Bei mittlerem Wachstum steigt der Betrag bis 2060 auf {eur(G['erw_de_2060'])} "
   "je Erwachsenem (Preise 2028)."])
P(["Als ", ("Mindestniveau", "b"), " soll die Dividende das halbe Existenzminimum decken, also die Hälfte des "
   f"Grundbedarfs: in Deutschland {eur(G['anker_de'])} je Erwachsenem und Monat. Die gesamte Abgabenlast ist so bemessen, "
   "dass dieses Mindestniveau im Durchschnitt aller teilnehmenden Staaten in jedem Jahr erreicht wird, auch wenn die "
   "Wirtschaft real nicht wächst (Abschnitt 6.1). In Ländern mit geringerer Wirtschaftsleistung liegt die Dividende zu "
   "Beginn darunter (Abschnitt 5.2)."])
H2("2.8  Ein Rechenbeispiel")
P(f"Ein Paar mit zwei Kindern in Deutschland; eine Person verdient {eur(brutto)} brutto im Jahr, die andere hat kein "
  "Einkommen.")
TAB(["", "Euro im Jahr"],
    [["Dividende: 2 Erwachsene und 2 Kinder", eur(div_hh)],
     [f"Einkommensteuer der verdienenden Person (auf {eur(brutto)} Lohn und {eur(div_erw_jahr)} Dividende)", eur(st_verdiener)],
     [f"Einkommensteuer der anderen Person (auf {eur(div_erw_jahr)} Dividende)", eur(st_partner)],
     ["Sozialbeiträge", "0 €"],
     ["Dividende abzüglich Einkommensteuer", eur(div_hh - st_hh)]],
    [6800, 2200], rechts=(1,), fett=(4,))
P("Hinzu kommt die Mehrwertsteuer auf den Konsum, die ungefähr auf heutigem Niveau liegt. Wie sich das neue System für "
  "jeden Haushaltstyp im Vergleich zu heute auswirkt, zeigt erst eine Haushaltssimulation (Abschnitt 7).")

# 3 ---------------------------------------------------------------------------
H1("3  Die Gemeinde")
H2("3.1  Was die Gemeinde trägt")
P("Die Gemeinde übernimmt alle Aufgaben, die vor Ort anfallen. Die folgende Tabelle zeigt, was die Gemeinden der zehn "
  "gerechneten Staaten heute für diese Aufgaben ausgeben, als Anteil am BIP. Was die Gemeinden heute tatsächlich "
  "tragen, bleibt bei ihnen; das Konzept verschiebt keine Aufgaben nach unten, ohne das Geld mitzugeben.")
TAB(["Aufgabe der Gemeinde", "% des BIP", "Mrd € 2028"],
    [[n, de(v, 2), de(m)] for n, v, m in G["tabelle_b"]], [5400, 1600, 2000], rechts=(1, 2), fett=(len(G["tabelle_b"]) - 1,))

H2("3.2  Die Formel: Geld je Einwohner und je Kind")
P("Die Gemeinde verhandelt nicht um Geld, sie erhält es nach einer Formel mit zwei Zahlen. Die Herleitung ist einfach: "
  "Von den sieben Aufgaben hängt nur eine vom Alter der Bevölkerung ab, die Schule. Alle anderen Kosten folgen der Zahl "
  "der Einwohner. Also wird das Schulbudget je Kind verteilt und der Rest je Einwohner:")
LISTE([[("je Kind ", "b"), f"(5 bis 19 Jahre): die Ausgaben für Schulen ({de(B['Schulen'], 2)} % des BIP), geteilt durch "
        f"die Zahl der Kinder ({de(G['kind_ant'], 2)} % der Bevölkerung);"],
       [("je Einwohner ", "b"), f"die übrigen Aufgaben ({de(G['b_fach'] - B['Schulen'], 2)} % des BIP), geteilt durch die "
        "Zahl der Einwohner."]])
P(["Jedes Land wendet diese Regel auf seine eigene Wirtschaftsleistung je Kopf an. Für Deutschland ergeben sich ",
   (f"{eur(G['gemeinde_einw_de'])} je Einwohner und {eur(G['gemeinde_kind_de'])} je Kind", "b"),
   " im Jahr (2028). Innerhalb eines Landes erhält jede Gemeinde für jeden Einwohner und jedes Kind denselben Betrag. "
   f"Eine Gemeinde mit 30.000 Einwohnern und 16 % Kindern hat damit in Deutschland ein Budget von rund "
   f"{de((30000 * G['gemeinde_einw_de'] + 30000 * 0.16 * G['gemeinde_kind_de']) / 1e6, 1)} Mio € im Jahr."])
TAB(["Land", "Wirtschaftsleistung je Kopf (Durchschnitt = 1)", "je Einwohner", "je Kind"],
    [[r["name"], de(r["bip_kopf_klub"], 2), eur(r["gemeinde_einw"]), eur(r["gemeinde_kind"])] for r in ld],
    [2000, 3200, 1900, 1900], rechts=(1, 2, 3))
NOTIZ("Euro im Jahr, 2028. Durchschnitt der zehn gerechneten Staaten: "
      f"{eur(G['formel_einw'])} je Einwohner und {eur(G['formel_kind'])} je Kind.")

H2("3.3  Eigene Einnahmen: Grundstücke")
P(["Die Gemeinde hat eine eigene Steuer, die ", ("Grundstücksabgabe", "b"),
   ". Sie bemisst sich allein am Wert des Grundstücks ohne das Gebäude darauf (Bodenwert). Den Satz legt die Gemeinde "
   "zwischen 0,1 und 1 % des Bodenwerts im Jahr fest. Wer baut oder saniert, zahlt dafür nicht mehr; unbebautes Bauland "
   "in guter Lage zahlt mit. Auf Mieten darf die Abgabe nicht umgelegt werden. Weil Bebauung den Bodenwert hebt, hat die "
   f"Gemeinde einen Anreiz, Entwicklung zuzulassen. Die Rechnung setzt {de(G['boden'], 2)} % des BIP an, rund "
   f"{eur(G['boden_kopf'])} je Einwohner und Jahr."])
P("Gewinne aus dem Verkauf von Grundstücken und Häusern werden mit 28 % besteuert; wer innerhalb von zwei Jahren "
  "Ersatz kauft, kann die Steuer aufschieben, und beim endgültigen Ausstieg bleiben einmalig 300.000 € frei.")

H2("3.4  Selbst entscheiden")
P("Was die Gemeinde mit ihrem Geld tut, entscheidet sie selbst: welche Schule, welche Verwaltung, welche Angebote. Sie "
  "entscheidet auch, ob und welche Leistungen sie von Kreis, Region oder Land einkauft und wie viel sie dafür an diese "
  "Verwaltungen weitergibt. Kreis und Land werden damit nicht abgeschafft, sondern zu Partnern, deren Leistungen die "
  "Gemeinden wählen. Kleine Gemeinden müssen sich zu Verbänden zusammenschließen; den Partner wählen sie frei. "
  "Förderprogramme für Landwirtschaft, Wirtschaft und Arbeitsmarkt liegen ebenfalls bei den Gemeinden.")
P(["Hier schließt sich der Kreis: ", ("Was die Gemeinde spart, kommt bei ihren Bürgern an.", "b"),
   " Die Dividende ist der Teil des Geldes, der nach den Aufgaben übrig bleibt. Die Verwaltung der Gemeinden kostet "
   f"heute im Durchschnitt {pr(G['verw_anteil_pct'])} ihres Budgets. Arbeitet sie um ein Zehntel sparsamer, sind das "
   f"etwa {eur(G['verw_zehntel_eur'])} je Einwohner und Monat. Neue, von Beginn an digital umgesetzte Regeln sollen "
   "deutlich mehr möglich machen; in die Rechnung ist das nicht eingerechnet."])

# 4 ---------------------------------------------------------------------------
H1("4  Das gemeinsame Dach")
H2("4.1  Ein Einzug, eine Obergrenze")
P("Über der Gemeinde steht nur noch eine Ebene, das gemeinsame Dach. Es zieht alle Steuern ein – außer der "
  "Grundstücksabgabe, die bei der Gemeinde bleibt –, behält, was seine Aufgaben kosten, und gibt den Rest an die "
  "Gemeinden und als Dividende an die Menschen weiter.")
P(["Wie viel das Dach behalten darf, ist im Vertrag begrenzt: ", (f"höchstens {pr(og, 0)} dessen, was es einzieht.", "b"),
   f" Diese Grenze ist eine Schranke, kein Budget. Gebraucht werden 2028 {pr(G['a_2028'], 2)} des BIP; am meisten im Jahr "
   f"{G['a_hoechst_jahr']} mit {pr(G['a_hoechst'], 2)}, das sind {pr(G['tabelle_obergrenze'][0]['pct_einzug'])} des Einzugs. "
   "Was das Dach nicht braucht, fließt weiter. Eine Grenze, die nicht ausgeschöpft werden muss, kann nicht zum Anspruch "
   "werden. Abgeleitet ist sie aus dem höchsten Bedarf, auch wenn einzelne Finanzierungsrisiken eintreten (höhere Zinsen, "
   "schwächeres Wachstum, höhere Schulden zu Beginn), aufgerundet auf volle Prozent."])

H2("4.2  Was das Dach trägt")
P("Das Dach beschränkt sich auf Kernaufgaben: was nur gemeinsam geht und was für alle gleich gelten muss.")
TAB(["Aufgabe des Daches", "% des BIP", "Mrd € 2028"],
    [[n, de(v, 2), de(m)] for n, v, m in G["tabelle_a"]], [5400, 1600, 2000], rechts=(1, 2), fett=(len(G["tabelle_a"]) - 1,))
P([f"Die Verteidigung steht in der Tabelle mit ihrem Zielwert. Hinzu kommt der Zinsdienst für die bestehenden Staatsschulden ({pr(G['zd_2028'], 2)} des BIP im Jahr 2028, "
   "Abschnitt 5.3). Die Verteidigung ist im Startjahr mit "
   f"{pr(p0['v'], 2)} des BIP angesetzt, so viel geben die zehn Staaten heute nach der amtlichen Statistik aus, und "
   f"steigt bis 2035 auf {pr(A['Verteidigung und digitale Souveränität'], 2)}. Zur Verteidigung gehört heute auch die "
   "digitale Souveränität: eigene Netze, eigene Halbleiter, eigene Rechenkapazität."])
P(f"Der größte Posten, „Wirtschaftsraum, Agrar, Energie, Netze“, umfasst den gemeinsamen Binnenmarkt, überregionale "
  f"Netze und Energie. Er ist mit {de(A['Wirtschaftsraum, Agrar, Energie, Netze'], 2)} % des BIP angesetzt; das sind die "
  "heutigen Wirtschaftsausgaben der Staaten ohne den örtlichen Verkehr und ohne das, was gestrichen oder an die Gemeinden "
  f"abgegeben wird (zusammen {de(G['dach_kuerzung'], 2)} Punkte: Landwirtschaft, Industrie, die Hälfte der Energie und der "
  "allgemeinen Wirtschafts- und Arbeitsmarktförderung). Landwirtschaft wird dann nicht mehr über Zuweisungen gestützt, "
  "sondern über die Mehrwertsteuer nach Fußabdruck, die kurze Wege begünstigt.")

H2("4.3  Unternehmen: Besteuerung am Ort der Kunden")
P("Gewinne von Unternehmen werden mit 28 % besteuert, und zwar dort, wo ihre Kunden sitzen. Das gilt ausdrücklich für "
  "digitale Plattformen. Gewinne lassen sich in andere Länder verschieben, Kunden nicht. Diese Steuer zieht das Dach ein, "
  "weil ihre Grundlage beweglich ist und nur einheitlich erhoben werden kann. Eine eigene Gewinnsteuer der Gemeinden "
  "gibt es nicht.")

H2("4.4  Entscheiden mit Mehrheit")
P("Das Dach entscheidet mit der Mehrheit seiner Mitglieder. Ein Bündnis, in dem jedes Mitglied ein Veto hat, kann in "
  "einer Krise nicht handeln.")

# 5 ---------------------------------------------------------------------------
H1("5  Kooperation im Möglichkeitsraum")
H2("5.1  Warum mehrere Staaten")
P("Die Regeln für den einzelnen Menschen und die Gemeinde funktionieren auch in einem einzelnen Staat; dann ist der "
  "Staat selbst das Dach. Eine Kooperation mehrerer Staaten ist eine Möglichkeit, keine Bedingung. Sie macht das System "
  "aber stärker und gerechter:")
LISTE([[("Besteuerung am Ort der Kunden ", "b"), "wirkt umso besser, je größer der gemeinsame Raum ist. Gewinne, die "
        "heute in Länder mit niedrigen Steuern verschoben werden, werden dort besteuert, wo sie erwirtschaftet werden."],
       [("Eine gemeinsame Zinsgarantie ", "b"), "senkt die Kosten der bestehenden Staatsschulden für alle (Abschnitt 5.3)."],
       [("Verteidigung, digitale Souveränität und ein Binnenmarkt ", "b"), "sind gemeinsam günstiger und wirksamer als "
        "allein."],
       [("Gleiche Regeln ", "b"), "verhindern, dass Staaten sich gegenseitig mit Steuergeschenken unterbieten, und geben "
        "Ländern mit geringerer Wirtschaftsleistung dieselben Chancen."]])
P(["Die teilnehmenden Staaten bilden eine ", ("Staatengemeinschaft", "b"),
   " mit einem gemeinsamen Dach. Alle Zahlen dieses Textes sind für eine solche Gemeinschaft aus zehn Staaten gerechnet."])

H2("5.2  Gleiche Regeln, nationaler Ausgangspunkt")
P("Ausgangspunkt sind die Staaten, wie sie heute sind. Jedes Land wendet dieselben Regeln an: Es zahlt denselben Anteil "
  "seiner Wirtschaftsleistung je Kopf als Dividende aus und verteilt das Gemeindebudget nach derselben Formel. Wächst die "
  "Wirtschaft eines Landes, wachsen seine Dividende und seine Gemeindebudgets vollständig mit; das ist der Anreiz. "
  "Sonderregeln für einzelne Länder gibt es nicht.")
TAB(["Land", "Wirtschaftsleistung je Kopf", "Mindestniveau", "Dividende 2028", "2060"],
    [[r["name"], de(r["bip_kopf_klub"], 2), eur(r["boden"]), eur(r["v2_e2028"]) + (" *" if r["v2_unter_boden"] else ""),
      eur(r["v2_e2060"])] for r in ld],
    [1900, 2300, 1700, 1700, 1400], rechts=(1, 2, 3, 4))
NOTIZ("Euro je Erwachsenem und Monat, Preise 2028; Kinder erhalten die Hälfte. Wirtschaftsleistung je Kopf 2024, "
      "Durchschnitt der zehn Staaten = 1. Mindestniveau: halbes Existenzminimum am Wohnort. * unter dem Mindestniveau. "
      "2060 bei mittlerem Wachstum, ohne Annahme eines Aufholens.")
P(f"Im Jahr 2028 liegen {liste(unter)} unter dem Mindestniveau. Die Unterschiede werden für eine Übergangszeit "
  "hingenommen. Die Angleichung soll aus denselben Regeln entstehen: Wo Arbeit heute besonders hoch belastet ist, "
  "entlastet das System am stärksten, und wo Löhne und Preise niedriger sind, siedeln sich Unternehmen an. Hinzu kommen "
  "die Förderprogramme der Europäischen Union für strukturschwache Regionen. Wer innerhalb der Gemeinschaft umzieht, "
  "behält die Dividende des bisherigen Landes, bis er drei Jahre im neuen Land wohnt und dort Steuern gezahlt hat; "
  "für Kinder und Studierende genügen die drei Jahre.")

H2("5.3  Die bestehenden Schulden")
P(f"Die zehn Staaten zahlten 2024 zusammen {de(G['zinsausgaben24_mrd'])} Mrd. € Zinsen auf "
  f"{de(G['schuld24_mrd'])} Mrd. € Schulden, ein durchschnittlicher Zinssatz von {pr(G['zins_eff_2024'], 2)}. "
  "Das gemeinsame Dach übernimmt diesen Zinsdienst und garantiert allen Mitgliedern einen gemeinsamen Zins. Bezahlt wird "
  "er aus dem Anteil des Daches, also mit demselben Satz auf die Wirtschaftsleistung jedes Landes.")
P(f"Weil die Länder unterschiedlich viele Schulden mitbringen, entstünde so ein dauerhafter Transfer: Frankreich hat "
  f"Schulden von {pr(G['tabelle_aufschlag'][0]['schuld'])} seiner Wirtschaftsleistung, Estland von "
  f"{pr(next(r['schuld'] for r in G['tabelle_aufschlag'] if r['land'] == 'Estland'))}. Ausgeglichen wird das über einen "
  "Aufschlag auf den Anteil, den das Dach in einem Land behält: Länder mit hohen Schulden tragen mehr, Länder mit "
  "niedrigen weniger, in der Summe gleicht sich das aus. Der Aufschlag schmilzt über dreißig Jahre ab. Er erreicht "
  "weder die Gemeinden noch die Dividende; er bleibt eine Sache zwischen den Staaten und dem Dach. Die Garantie gilt, "
  "solange ein Staat Mitglied ist.")
P(f"Neue Schulden macht das Dach nicht. Weil die Wirtschaft wächst, sinkt die Schuldenquote trotzdem von "
  f"{pr(tp[0]['d'])} im Jahr 2028 auf {pr(tp[-1]['d'])} im Jahr 2060, ohne dass getilgt wird.")

H2("5.4  Der Möglichkeitsraum")
P(f"Die Gemeinschaft ist kein fester Kreis, sondern ein Angebot. In Frage kommen {len(europa)} europäische Staaten – die "
  f"27 der Europäischen Union, das Vereinigte Königreich, die Schweiz, Norwegen und Island – mit zusammen "
  f"{de(raum_mio, 1)} Mio. Menschen. Diesen Kreis nennt das Konzept den Möglichkeitsraum. Als Richtgröße für eine "
  f"wirksame Gemeinschaft dient die Einwohnerzahl der Vereinigten Staaten ({de(us_mio, 1)} Mio.). Schon sechs Staaten – "
  "Deutschland, das Vereinigte Königreich, Frankreich, Italien, Spanien und Polen – erreichen sie; jeder weitere Staat "
  "macht die Gemeinschaft stärker. Partner außerhalb Europas, etwa Kanada, sind denkbar.")
P("Die zehn Staaten, für die gerechnet wird, sind eine Stichprobe mit vollständigen Daten, nicht die vorgeschlagene "
  "Gemeinschaft: Belgien, Dänemark, Deutschland, Estland, Frankreich, Irland, die Niederlande, Österreich, Slowenien und "
  "Spanien. Die geltenden EU-Verträge verlangen für gemeinsame Steuerregeln Einstimmigkeit; eine Gemeinschaft, die mit "
  "Mehrheit entscheidet, braucht neue Vereinbarungen. Das Konzept geht davon aus, dass eine starke Gruppe von Staaten "
  "solche Vereinbarungen erreichen kann.")

# 6 ---------------------------------------------------------------------------
H1("6  Wie die Rechnung aufgeht")
H2("6.1  Die Abgabenquote ist abgeleitet, nicht gewählt")
P(["Die ", ("Abgabenquote", "b"), " ist der Anteil aller Steuern an der Wirtschaftsleistung. Sie ergibt sich aus drei "
   "Teilen, die sich addieren:"])
LISTE([f"was das Dach braucht (2028: {pr(G['a_2028'], 2)} des BIP, einschließlich Zinsdienst),",
       f"was die Gemeinden für ihre Aufgaben brauchen ({pr(G['b_fach'], 2)}),",
       "und die Dividende."])
P(["Festgelegt wird nicht die Quote, sondern das Mindestniveau der Dividende. Gesucht ist die kleinste Quote, bei der "
   "die Dividende im Durchschnitt aller Staaten in jedem Jahr bis 2060 mindestens das halbe Existenzminimum erreicht – "
   "und zwar auch dann, wenn die Wirtschaft real überhaupt nicht wächst. Das ergibt rechnerisch ",
   (f"{pr(G['mindestquote_streng'], 2)}", "b"), f", aufgerundet {pr(q)}. Im Startjahr verteilt sich das so:"])
TAB(["", "% des BIP", "€ je Kopf 2028"],
    [["Gesamtaufkommen", de(q, 2), de(G["tabelle_einzug"][0][2])],
     ["  davon zieht das Dach ein", de(q - G["boden"], 2), de(G["tabelle_einzug"][1][2])],
     ["  davon erhebt die Gemeinde selbst (Grundstücksabgabe)", de(G["boden"], 2), de(G["tabelle_einzug"][2][2])],
     ["Das Dach behält", de(G["a_2028"], 2), de(G["tabelle_einzug"][3][2])],
     ["Die Gemeinden erhalten für ihre Aufgaben", de(G["b_fach"], 2), de(G["tabelle_einzug"][5][2])],
     ["Dividende", de(p0["div"], 2), de(G["tabelle_einzug"][6][2])]],
    [5400, 1600, 2000], rechts=(1, 2), fett=(0, 5))
NOTIZ("Durchschnitt der zehn Staaten; Euro im Jahr, 2028, nominal.")

H2("6.2  Der Zeitpfad")
P("Vier Größen verändern sich über die Zeit: Die Verteidigung wird bis 2035 aufgebaut. Der Zinsdienst steigt zunächst, "
  "weil günstige alte Kredite auslaufen und zu höheren Zinsen ersetzt werden. Die Schuldenquote sinkt, weil die "
  "Wirtschaft wächst. Die Dividende ist der Rest.")
TAB(["Jahr", "Verteidigung", "Schulden", "Zinsdienst", "Dach gesamt", "Dividende", "€ im Monat"],
    [[str(r["jahr"]), pr(r["v"], 2), pr(r["d"]), pr(r["zd"], 2), pr(r["a"], 2), pr(r["div"], 2), de(r["klub"])] for r in tp],
    [800, 1350, 1200, 1300, 1350, 1300, 1700], rechts=(1, 2, 3, 4, 5, 6))
NOTIZ("Anteile am BIP; letzte Spalte: Dividende je Einwohner im Durchschnitt der zehn Staaten, Preise 2028, bei 3,0 % "
      f"nominalem Wachstum (davon 2,0 % Preissteigerung). Deutschland liegt wegen seiner höheren Wirtschaftsleistung je Kopf "
      f"um {de((G['f_de'] - 1) * 100, 1)} % darüber.")
P(f"Die Dividende sinkt bis {G['kl_tief_jahr']} leicht auf {eur(G['kl_tief'])} je Einwohner, weil der Aufbau der "
  "Verteidigung und der Anstieg der Zinsen zusammenfallen, und steigt danach mit der Wirtschaft. Ihr Anteil am BIP bleibt "
  f"fast gleich ({pr(G['div_2028'], 2)} im Jahr 2028, {pr(G['div_2060'], 2)} im Jahr 2060). Jede Eurozahl für spätere Jahre "
  "hängt also an der Annahme zum Wachstum:")
TAB(["reales Wachstum je Kopf und Jahr", "2035", "2060"],
    [[r["fall"].replace(" — Zentralfall", " (mittlerer Fall)").replace("0,98 % (3,0 % nominal)", "1,0 %"),
      eur(r["e2035"]), eur(r["e2060"])] for r in G["tabelle_sens"]],
    [4800, 2100, 2100], rechts=(1, 2))
NOTIZ("Deutschland, Euro je Einwohner und Monat, Preise 2028. Auch ohne Wachstum bleibt die Dividende über dem "
      "Mindestniveau.")

H2("6.3  Tragen die Steuern die Quote?")
P("Die Quote ist von der Ausgabenseite her bestimmt. Ob die Steuern sie tatsächlich aufbringen, ist eine eigene Rechnung. "
  "Sie liegt bisher für Deutschland vor, mit einem Modell der deutschen Einkommensverteilung in sieben Gruppen:")
KAT = [("Einkommen (Stufentarif, mit Dividende der Erwachsenen)", ("01",)), ("Kapitalerträge", ("02",)),
       ("Konsum (Mehrwertsteuer-Label)", ("06",)), ("Unternehmen und Plattformen", ("05",)),
       ("Erbschaften", ("03", "Erbschaft")), ("Große Vermögen", ("04c", "Vermögensteuer")),
       ("CO₂-Preis", ("07", "CO₂-Pfad")), ("Abbau klimaschädlicher Subventionen", ("Abbau",)),
       ("Übrige Steuern (Energie, Tabak u. a.)", ("Sonstige",)), ("Grundstücksabgabe der Gemeinden", ("04a",))]
zeilen, gezaehlt = [], 0
for name, praef in KAT:
    v = sum(x[1] for x in G["tabelle_deckung"] if x[0].startswith(praef))
    gezaehlt += sum(1 for x in G["tabelle_deckung"] if x[0].startswith(praef))
    zeilen.append([name, de(v, 2)])
assert gezaehlt == len(G["tabelle_deckung"]), "Deckungszeilen nicht vollständig zugeordnet"
zeilen += [["Summe", de(G["deckung_gesamt"], 2)], ["Abgabenquote", de(q, 2)],
           ["Überschuss" if lk <= 0 else "Fehlbetrag", de(abs(lk), 2)]]
TAB(["Steuer", "% des BIP"], zeilen, [7000, 2000], rechts=(1,), fett=(len(zeilen) - 3, len(zeilen) - 1))
P(f"Die Steuern tragen die Quote knapp, mit einem Überschuss von {de(-lk, 2)} Punkten. Das ist weniger als die Unsicherheit "
  "der Rechnung; einige Posten beruhen auf Annahmen (Zahl der Erbschaften über dem Freibetrag, Ausweichen bei der "
  "Vermögensteuer, Aufteilung der Wirtschaftsausgaben). Als stabil gilt das System, wenn die Steuern die Quote tragen "
  "und die Dividende danach noch um mindestens einen Punkt des BIP sinken könnte, bevor das Mindestniveau in einem Jahr "
  f"unterschritten wird. Dieser Abstand beträgt {de(TF['deckung']['reserve_mit_ueberschuss'], 2)} Punkte." if lk <= 0 else
  f"Es fehlen {de(lk, 2)} Punkte.")

H2("6.4  Was es kostet")
TAB(["", "heute", "TAX 28:28"],
    [["Steuern", de(G["steuern_heute"], 2), de(q, 2)],
     ["Sozialbeiträge", de(G["sb_heute"], 2), "0,00"],
     ["Gesundheit, gesondert finanziert", "in den Beiträgen enthalten", de(G["gesundheit"], 2)],
     ["Gesamtlast", de(G["last_heute"], 2), de(G["last_entwurf"], 2)]],
    [4200, 2400, 2400], rechts=(1, 2), fett=(3,))
NOTIZ("Prozent des BIP, zehn Staaten, 2024 bzw. 2028.")
P(f"Die Gesamtlast sinkt um {de(G['entlastung'], 2)} Punkte des BIP, rund {de(G['entlastung_mrd'])} Mrd. € im Jahr. "
  "Entlastet wird vor allem die Arbeit, weil die Sozialbeiträge entfallen. Getragen wird das von Konsum, CO₂, "
  "Grundstücken und Unternehmensgewinnen. Mit den Sozialbeiträgen entfallen auch die Verfahren, die sie erheben und "
  "verteilen; die Verwaltung der Sozialversicherungen kostet in Deutschland heute rund 1,1 % des BIP.")

# 7 ---------------------------------------------------------------------------
H1("7  Was noch offen ist")
LISTE([[("Haushaltssimulation. ", "b"), "Wie es einzelnen Haushalten ergeht, etwa einer Alleinerziehenden mit zwei "
        "Kindern, zeigt erst eine Simulation mit Daten einzelner Haushalte. Bis dahin sind Tarifstufen und Sätze "
        "vorläufig."],
       [("Steuerbasen aller Staaten. ", "b"), "Die Rechnung, ob die Steuern die Quote tragen, liegt nur für Deutschland "
        "vor; für die Gemeinschaft fehlen die Steuerbasen der übrigen Staaten."],
       [("Aufgabenliste des Daches. ", "b"), "Welche Programme im Einzelnen gestrichen oder an die Gemeinden abgegeben "
        "werden, steht aus."],
       [("Produktliste des Labels. ", "b"), "Die Zuordnung der Produkte zu den Stufen nach ihrem Fußabdruck ist zu "
        "erarbeiten."],
       [("Ausgleichsrücklage. ", "b"), "Ein Mechanismus, der Schwankungen des Aufkommens ausgleicht, ist noch nicht "
        "gerechnet."],
       [("Rechtlicher Rahmen. ", "b"), "Der Vertrag der Staatengemeinschaft und sein Verhältnis zu den EU-Verträgen "
        "sind rechtlich nicht geprüft."],
       [("Verteidigung. ", "b"), "Ob 2,5 % des BIP genügen, ist keine Frage dieses Modells; acht der zehn Staaten haben "
        "in der NATO 3,5 % zugesagt."]])

# 8 ---------------------------------------------------------------------------
H1("8  Zahlengrundlage")
P(f"Alle Struktur- und Aufkommenszahlen stammen aus der amtlichen Statistik der Europäischen Union (Eurostat), Berichtsjahr "
  f"2024, in Einzelabrufen je Land. Die zehn gerechneten Staaten kommen 2024 auf {de(G['bip24_klub_mrd'])} Mrd. € "
  f"Wirtschaftsleistung und {de(G['pop_klub_mio'], 1)} Mio. Menschen. Fortgeschrieben auf 2028 mit den nominalen "
  f"Wachstumsraten der Bundesregierung (Frühjahrsprojektion 2026, für 2028 vorsichtig +3,0 %) sind das "
  f"{de(G['bip28_klub_mrd'])} Mrd. € oder {eur(G['kopf_klub'])} je Kopf. Die Schuldenquote 2028 ({pr(G['schuldenquote_2028'])}) "
  "ist aus den heutigen Defiziten fortgeschrieben. Die deutsche Wachstumsrate auf alle Staaten anzuwenden, ist eine "
  "Vereinfachung.")
P("Annahmen sind im Text als solche benannt. Jede Rechnung liegt als Skript vor und lässt sich nachrechnen; ein Logbuch "
  "führt jede Änderung und jeden gefundenen Fehler. Rechnung: modell/gesamtrechnung.py, Ergebnis "
  "daten/aggregate/gesamtrechnung.json.")
P([("Text: Initiative 28:28, Lizenz CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Eingangsdaten Dritter "
    "unterliegen deren Bedingungen. Entwurf zur Diskussion.", "i")], fs=18)

# Quellen ---------------------------------------------------------------------
DOC.append("\\page\n")
H1("Quellenverzeichnis")
P("Alle externen Quellen der Rechnungen und Texte des Projekts, einschließlich der Länderrechnungen. Abruftag ohne "
  "Uhrzeit. Ein Vermerk in Klammern kennzeichnet Quellen, deren Original nicht eingesehen oder deren Link nicht geprüft "
  "wurde, sowie Sekundärquellen.", fs=19)
REIHE = ["Amtliche Statistik", "Wissenschaftliche Arbeiten", "Amtliche Dokumente und Rechtstexte",
         "Institutionen und Programme", "Länderquellen", "Sekundärquellen"]


def vermerk(q):
    h = (q.get("hinweis") or "").lower()
    v = []
    if q["gruppe"] == "Sekundärquellen" or h.startswith("sekundärquelle"):
        v.append("Sekundärquelle")
    if "nicht abrufbar" in h or "nicht abgerufen" in h or "original nicht" in h or "nicht eingesehen" in h:
        v.append("Original nicht eingesehen")
    if "nicht geöffnet" in h or "link nicht geprüft" in h or "nicht geprüft" in h and q.get("link"):
        v.append("Link nicht geprüft")
    if "maschinell" in h:
        v.append("maschinell gelesen")
    return f" ({', '.join(dict.fromkeys(v))})" if v else ""


for gr in REIHE:
    eintraege = sorted((q for q in QV if q["gruppe"] == gr), key=lambda q: (q["autor"].lower(), q["jahr"]))
    if not eintraege:
        continue
    H2(gr)
    for q in eintraege:
        t = f"{q['autor']} ({q['jahr'] or 'o. J.'}): {q['titel']}."
        if q.get("link"):
            t += f" {q['link']}"
            t += f", abgerufen am {q['abruf']}." if q.get("abruf") else "."
        elif q.get("abruf"):
            t += f" Abgerufen am {q['abruf']}."
        t += vermerk(q)
        DOC.append("\\pard\\sa60\\sl252\\slmult1\\li360\\fi-360\\fs18 " + esc(t) + "\\par\n")

DOC.append("}")
ZIEL.write_text("".join(DOC), encoding="ascii")
print(f"geschrieben: {ZIEL.relative_to(W)} ({ZIEL.stat().st_size} Bytes), {len(QV)} Quellen")
