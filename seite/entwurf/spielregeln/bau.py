#!/usr/bin/env python3
"""Entwurf der deutschen Webseite nach den Spielregeln (Logbuch v4.75). Nicht hochladen; die geltende Seite baut drittel_bau.py.

Liest seite/stand-c/de.html (geltender Stand), ersetzt die Abschnitte zum Dach, zum Klub und zu den Altlasten nach den Spielregeln vom
7.11.2026 (projekt/Spielregeln-Staaten-und-Fonds-2026-11-07.md) und ergänzt die Herleitung aus den Verträgen der Vereinten Nationen.
Ausgaben (im Ordner dieses Skripts):
  de.html            Entwurf der künftigen Seite
  de-kontrolle.html  Kontrollfassung: Ergänzungen grün, Streichungen rot hinterlegt
Zahlen zum Fonds 50/50 aus daten/aggregate/fonds_5050.json (vorläufig); Staatenliste aus daten/aggregate/staatenauswahl.json.
"""
import json, re
from pathlib import Path

W = Path(__file__).resolve().parents[3]
HIER = Path(__file__).resolve().parent
ALT = (W / "seite" / "stand-c" / "de.html").read_text(encoding="utf-8")
F55 = json.loads((W / "daten" / "aggregate" / "fonds_5050.json").read_text(encoding="utf-8"))
SA = json.loads((W / "daten" / "aggregate" / "staatenauswahl.json").read_text(encoding="utf-8"))

NAME = dict(AT="Österreich", BE="Belgien", BG="Bulgarien", CH="Schweiz", CY="Zypern", CZ="Tschechien", DE="Deutschland", DK="Dänemark",
            EE="Estland", EL="Griechenland", ES="Spanien", FI="Finnland", FR="Frankreich", HR="Kroatien", HU="Ungarn", IE="Irland", IS="Island",
            IT="Italien", LT="Litauen", LU="Luxemburg", LV="Lettland", MT="Malta", NL="Niederlande", NO="Norwegen", PL="Polen", PT="Portugal",
            RO="Rumänien", SE="Schweden", SI="Slowenien", SK="Slowakei", AU="Australien", BB="Barbados", CA="Kanada", CL="Chile", CR="Costa Rica",
            JP="Japan", KR="Republik Korea", NZ="Neuseeland", UK="Vereinigtes Königreich", UY="Uruguay", MU="Mauritius")
EUROPA = set(F55["laender"])


def z(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def liste(codes):
    return ", ".join(sorted(NAME[c] for c in codes))


st = SA["zaehlung"]
teil = st["Teilnahme"] + st.get("ohne WJP-Wert (zweite Quelle nötig)", [])
teil_eu, teil_welt = [c for c in teil if c in EUROPA], [c for c in teil if c not in EUROPA]
partner = st["Partner"]
de = F55["laender"]["DE"]
gem = F55["gemeinsamer_satz_teilnehmer"]

STEMPEL = re.search(r"Modellstand <b>v[0-9.]+ · [^<]+</b>", ALT).group(0)
R = []   # (alt, neu): jede alte Stelle muss genau einmal vorkommen

# Ebenen: Gemeinschaft der Staaten statt Dach (v4.76)
GK = json.loads((W / "daten" / "aggregate" / "gemeinschaft_kasse.json").read_text(encoding="utf-8"))["varianten"]["G1"]
R += [("<h2>Starke Kommunen und Regionen, starke Bürger, ein starkes europäisches Dach</h2>",
       "<h2>Starke Kommunen und Regionen, starke Bürger, eine starke Gemeinschaft der Staaten</h2>"),
      ("Kommunen und Regionen erhalten ihren Anteil direkt vom Dach, entscheiden selbst über Finanzen und delegieren Aufgaben an übergeordnete "
       "Verwaltungszusammenschlüsse (z. B. Infrastrukturverbünde). Das europäische Dach übernimmt nur, was Kommunen und Regionen allein nicht können "
       "– und darf sich nicht mehr nehmen, als im Vertrag steht.",
       "Kommunen und Regionen erhalten ihren Anteil nach fester Formel, entscheiden selbst über Finanzen und delegieren Aufgaben an "
       "übergeordnete Verwaltungszusammenschlüsse (z. B. Infrastrukturverbünde). Staat und Gemeinschaft der Staaten übernehmen nur, was Kommunen und "
       "Regionen allein nicht können – und behalten zusammen höchstens 32 % des Aufkommens."),
      ('<text x="180" y="44" text-anchor="middle" font-size="19" font-weight="700">Das gemeinsame Dach</text>',
       '<text x="180" y="44" text-anchor="middle" font-size="19" font-weight="700">Staat und Gemeinschaft</text>', "roh"),
      ('<text x="450" y="48" text-anchor="middle" font-size="20" font-weight="700">Das gemeinsame Dach</text>',
       '<text x="450" y="48" text-anchor="middle" font-size="20" font-weight="700">Staat und Gemeinschaft der Staaten</text>', "roh"),
      ("<div><h3>Dem Dach wird zugetraut,</h3><p>was nur gemeinsam geht: Verteidigung und digitale Souveränität, ein Binnenmarkt ohne Grenzen, "
       "gemeinsame Standards. Mehr nicht. Das Dach entscheidet mit der Mehrheit der Abgesandten der Zusammenschlüsse von Kommunen und Regionen.</p></div>",
       "<div><h3>Der Gemeinschaft der Staaten wird zugetraut,</h3><p>was nur gemeinsam geht: gemeinsame Forschung, Freizügigkeit, ein Markt ohne "
       "Grenzen, ein gemeinsames Gericht und gemeinsame Standards, allen voran das Label. Mehr nicht. In diesen Aufgaben entscheidet sie mit Mehrheit; "
       "die Spielregeln selbst ändern die Staaten nur gemeinsam.</p></div>"),
      ('<span><b style="background:var(--ink)"></b>Dach</span>', '<span><b style="background:var(--ink)"></b>Staat und Gemeinschaft</span>', "roh"),
      ("width:0;height:12px\"></b>Obergrenze des Dachs</span>", "width:0;height:12px\"></b>Obergrenze von Staat und Gemeinschaft</span>", "roh"),
      ("Im Jahr {j} behält das Dach {a} von {hundert}", "Im Jahr {j} behalten Staat und Gemeinschaft {a} von {hundert}", "roh"),
      ("Das Goldene Drittel setzt dafür auf einen gemeinsamen europäischen CO₂-Preis und gibt",
       "Das Goldene Drittel setzt dafür auf einen gemeinsamen CO₂-Preispfad der Gemeinschaft nach dem Pariser Abkommen und gibt", "roh"),
      ("Die Verteilung durch das Dach mündet in zwei Zahlen", "Die Verteilung nach der Formel mündet in zwei Zahlen"),
      ("Grundlagenforschung und Hochschulen gehören zu den gemeinsamen Aufgaben des Dachs (in der Gesamtrechnung 0,77 und 0,74 % der Wirtschaftsleistung).",
       "Grundlagenforschung ist eine gemeinsame Aufgabe der Gemeinschaft, Hochschulen tragen die Staaten (in der Gesamtrechnung 0,77 und 0,74 % "
       "der Wirtschaftsleistung). Forschende und Studierende arbeiten in einem gemeinsamen Forschungsraum."),
      ("Europäischer Preispfad · Rückgabe über die Transformationsdividende", "Gemeinsamer Preispfad nach dem Pariser Abkommen · Rückgabe über die Transformationsdividende"),
      ]

# Sicherungen → fünf Spielregeln
i = ALT.index('<section id="sicherungen">')
j = ALT.index("</section>", i) + len("</section>")
alt_sich = ALT[i:j]
renten = re.search(r"Bestehende Renten laufen weiter\..*?Kein Rentnerhaushalt fällt unter die heutige Grundsicherung\.", alt_sich).group(0)
neu_sich = f'''<section id="sicherungen">
  <div class="wrap">
    <h2>Sechs Spielregeln</h2>
    <p class="lede">Einfach und für jeden Staat gleich. Jeder Staat wendet die Regeln selbst an; was nur gemeinsam geht, trägt die Gemeinschaft der Staaten.</p>
    <div class="sich">
      <div><span><b>1 · Wer mitmacht</b><p>Jeder Staat, der Mitglied der Vereinten Nationen ist, beide Menschenrechtspakte von 1966 und das Pariser Klimaabkommen ratifiziert hat und rechtsstaatlich handelt (Rule of Law Index ab 0,66). Wer die Schwelle noch nicht erreicht, wendet die Regeln als Partner an.</p></span></div>
      <div><span><b>2 · Dieselben Regeln in jedem Land</b><p>Jeder Staat zieht seine Steuern selbst ein und misst alles an seinem eigenen Grundbedarf: Tarif, Label, Dividende, starkes Netz und die festen Beträge für Kommunen und Regionen. Staat und Gemeinschaft behalten zusammen höchstens 32 %. Formel statt Verhandlung: Niemand muss bitten, niemand kann kürzen.</p></span></div>
      <div><span><b>3 · Was nur gemeinsam geht</b><p>Die Gemeinschaft der Staaten sichert Freizügigkeit für alle Bürgerinnen und Bürger, einen Markt ohne Grenzen für Waren, Dienste und Kapital, einen gemeinsamen Forschungsraum und ein gemeinsames Gericht, an das sich auch jeder Einzelne wenden kann. Ein Label gilt überall; Versicherungsjahre zählen in jedem Staat. Für Forschung, Standards und Gericht zahlt jeder Staat denselben Anteil seiner Wirtschaftsleistung in eine gemeinsame Kasse – zum Beginn rund {z(GK["kasse_pct_bip"])} % (vorläufig). In diesen Aufgaben entscheidet die Gemeinschaft mit Mehrheit; die Spielregeln selbst ändern die Staaten nur gemeinsam.</p></span></div>
      <div><span><b>4 · Altlasten: halb selbst, halb gemeinsam</b><p>Alte Schulden und Rentenzusagen trägt jeder Staat zur Hälfte selbst; die andere Hälfte tragen alle Teilnehmer gemeinsam. Alles ist 2098 getilgt. Für Deutschland ergibt das einen Zuschlag von {z(de["geteilt_5050"]["zuschlag_pct"])} % auf alle Steuern – genau zwischen dem eigenen Satz ({z(de["eigen"]["zuschlag_pct"])} %) und dem gemeinsamen ({z(gem["zuschlag_pct"])} %), gerechnet mit 2,45 % Zins (vorläufig). Partner tragen ihre Altlast ganz selbst. Für überschuldete Staaten gibt es ein geordnetes Neustartverfahren. {renten}</p></span></div>
      <div><span><b>5 · Nachhaltig berichten</b><p>Jeder Staat berichtet mindestens alle vier Jahre an die Vereinten Nationen über die 17 Ziele für nachhaltige Entwicklung. Staaten mit hohem Einkommen gehen den Weg zu 0,7 % ihres Nationaleinkommens für Entwicklung.</p></span></div>
      <div><span><b>6 · Offen und freiwillig</b><p>Wer die erste Regel erfüllt, kann beitreten; wer austritt, nimmt seine Altlast mit. Alle Werte stehen öffentlich in einem Register und werden alle zwei Jahre neu festgestellt.</p></span></div>
    </div>
  </div>
</section>'''
R.append((alt_sich, neu_sich, "block"))

# Klub → offene Gemeinschaft, Herleitung aus den UN-Verträgen
i = ALT.index('<section id="klub">')
k0 = ALT.index('<h2>', i)
k1 = ALT.index('<h3 class="sub-h">Wohin die Reise geht</h3>', i)
alt_klub = ALT[k0:k1]
stub = ('<div hidden><div id="raumvor"></div><div id="raum"></div><span id="raumsum"></span><span id="raumn"></span><i id="raumbar"></i>'
        '<span id="raumus"></span><p id="raumtext"></p></div>')
herleitung = [
    ("Grundbedarf als Maß aller Stufen", "Recht auf einen angemessenen Lebensstandard (Sozialpakt Art. 11; Allgemeine Erklärung der Menschenrechte Art. 25)"),
    ("Dividende, starkes Netz, Kinderdividende", "Recht auf soziale Sicherheit (Sozialpakt Art. 9; Kinderrechtskonvention Art. 26 und 27; ILO-Empfehlung 202 zum sozialen Basisschutz; Ziel 1.3)"),
    ("Grundbedarf steuerfrei, höchstens ein Drittel", "Einsatz der verfügbaren Mittel nach Leistungsfähigkeit (Sozialpakt Art. 2 Abs. 1; Ziele 10.4 und 17.1)"),
    ("Kapital und Arbeit gleich besteuert", "eigene Entwicklung; folgt dem Gleichheitssatz (Zivilpakt Art. 26): gleiches Einkommen, gleiche Steuer, gleich woher es kommt"),
    ("Mehrwertsteuer als Label", "eigene Entwicklung; lenkt den Konsum im Sinne von Ziel 12 und des Pariser Abkommens (Art. 2 Abs. 1 c: Finanzflüsse im Einklang mit einem emissionsarmen Weg)"),
    ("Altlasten halb selbst, halb gemeinsam", "nach dem Vorbild der gemeinsamen, aber unterschiedlichen Verantwortung zum Wohl heutiger und künftiger Generationen (Klimarahmenkonvention Art. 3 Abs. 1)"),
    ("Gemeinschaft der Staaten", "Zusammenarbeit für sozialen Fortschritt und höheren Lebensstandard (UN-Charta Art. 1 Abs. 3, Art. 55 und 56); Recht auf Teilhabe am wissenschaftlichen Fortschritt und internationale Zusammenarbeit in der Forschung (Sozialpakt Art. 15); friedliche Streitbeilegung (UN-Charta Art. 33)"),
    ("Bericht zu den 17 Zielen, 0,7 % für Entwicklung", "Agenda 2030 (Resolution 70/1): Freiwillige Nationale Berichte an das Hochrangige Politische Forum; Ziel 17.2"),
    ("Besteuerung am Ort der Kunden", "Gegenstand der Verhandlungen über eine Rahmenkonvention der Vereinten Nationen zur Zusammenarbeit in Steuerfragen (seit 2025; ein Protokoll betrifft grenzüberschreitende Dienstleistungen einschließlich automatisierter digitaler Dienste)"),
]
rows = "".join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a, b in herleitung)
neu_klub = f'''<h2>Eine offene Gemeinschaft der Staaten auf dem Boden der Vereinten Nationen</h2>
    <p class="lede">Die Gemeinschaft der Staaten ist kein fester Kreis, sondern ein Angebot. Mitmachen kann jeder Staat, der die erste Spielregel erfüllt – gleich, wo er auf der Landkarte liegt. Gerechnet ist bisher der Bauplan für 30 Staaten Europas (EU, Norwegen, Island, Schweiz) mit 465,6 Mio. Menschen. Nach einer ersten Durchsicht erfüllen {len(teil)} Staaten die Regel; {len(partner)} weitere können als Partner beginnen.</p>
    {stub}
    <div class="effects">
      <div><h3>Teilnahme in Europa</h3><p>{liste(teil_eu)}.</p></div>
      <div><h3>Teilnahme weltweit</h3><p>{liste(teil_welt)}. Diese Staaten sind noch nicht gerechnet.</p></div>
      <div><h3>Partner</h3><p>{liste(partner)}. Sie wenden die Regeln an und tragen ihre Altlast selbst, bis sie die Schwelle erreichen.</p></div>
    </div>
    <p class="fineprint">Erste Durchsicht: Rule of Law Index 2025 (World Justice Project); Vertragsregister der Vereinten Nationen (Menschenrechtspakte, Pariser Abkommen). Für die Schweiz und Island gibt es keinen Indexwert; sie sind vorläufig eingeordnet.</p>
    <h3 class="sub-h">Was die Gemeinschaft verbindet</h3>
    <div class="effects">
      <div><h3>Freizügigkeit</h3><p>Leben, arbeiten und lernen in jedem Teilnehmerstaat. Dividende und Netz gelten dort, wo man wohnt; Versicherungsjahre aus allen Staaten zählen zusammen.</p></div>
      <div><h3>Ein Markt ohne Grenzen</h3><p>Waren, Dienste und Kapital bewegen sich frei. Ein Label, einmal zertifiziert, gilt überall; Plattformen versteuern am Ort ihrer Kunden.</p></div>
      <div><h3>Gemeinsam forschen</h3><p>Grundlagenforschung und große Anlagen aus der gemeinsamen Kasse; offener Zugang zu Hochschulen und Ergebnissen.</p></div>
      <div><h3>Ein gemeinsames Gericht</h3><p>Es entscheidet Streit über die Regeln und Freiheiten der Gemeinschaft – zwischen Staaten und auf Klage jedes Einzelnen.</p></div>
      <div><h3>Gemeinsame Standards</h3><p>Label, Register und Datenaustausch der Steuerverwaltungen, damit jede Regel überall gleich gilt.</p></div>
      <div><h3>Sicherheit als Angebot</h3><p>Wer will, beschafft und betreibt Verteidigung und digitale Infrastruktur gemeinsam. Das ist keine Bedingung der Teilnahme.</p></div>
    </div>
    <h3 class="sub-h">Abgeleitet aus den Verträgen der Vereinten Nationen</h3>
    <p class="lede">Jede Regel hat eine Grundlage, die fast alle Staaten der Welt unterschrieben haben. Zwei Regeln sind eigene Entwicklungen des Projekts; sie stehen im Mittelpunkt.</p>
    <div class="effects">{rows}</div>
    '''
R.append((alt_klub, neu_klub, "block"))
R += [("<div class=\"y\">2027 · Gemeinschaften bilden</div><div class=\"t\">Kommunen und Regionen finden Partner, Länder prüfen den Beitritt.</div>",
       "<div class=\"y\">2027 · Teilnahme prüfen</div><div class=\"t\">Staaten prüfen die erste Spielregel; die Werte stehen in einem öffentlichen Register.</div>"),
      ("<div class=\"y\">Ab 2028 · In kleinen Verbünden beginnen</div>", "<div class=\"y\">Ab 2028 · Mit den ersten Staaten beginnen</div>"),
      ("Jedes weitere Land stärkt den Klub – vor allem bei der Besteuerung am Ort der Kunden.",
       "Jeder weitere Staat stärkt die Gemeinschaft – vor allem bei der Besteuerung am Ort der Kunden."),
      (STEMPEL, STEMPEL.replace("Modellstand <b>", "Modellstand <b>Entwurf nach den Spielregeln · "), "roh"),
      ]

TOK = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<[^>]+>|[^<]+", re.S)


def gruen(h):
    """Sichtbaren Text eines HTML-Stücks grün hinterlegen (Tags, Skripte und Grafiken bleiben unberührt)."""
    return "".join(t if t.startswith("<") or not t.strip() else f'<ins class="k-neu">{t}</ins>' for t in TOK.findall(h))


def rot(h):
    return "".join(t if t.startswith("<") or not t.strip() else f'<del class="k-weg">{t}</del>' for t in TOK.findall(h))


NEU, K, n = ALT, ALT, 0
for eintrag in R:
    a, b = eintrag[0], eintrag[1]
    art = eintrag[2] if len(eintrag) > 2 else "text"
    for x in (NEU, K):
        if x.count(a) != 1:
            raise SystemExit(f"Stelle {x.count(a)}× gefunden: {a[:80]}")
    NEU = NEU.replace(a, b)
    if art == "roh":
        K = K.replace(a, b)
    elif art == "block":
        K = K.replace(a, '<div class="k-block-weg">' + rot(a) + "</div>" + gruen(b))
    else:
        K = K.replace(a, rot(a) + gruen(b))
    n += 1
(HIER / "de.html").write_text(NEU, encoding="utf-8")
css = ("<style>ins.k-neu{background:#c8ecc9;color:#0b3d12;text-decoration:none}del.k-weg{background:#f6c6c0;color:#5a1a12}"
       ".k-block-weg{outline:3px solid #e8a39a;margin-bottom:28px;opacity:.85}"
       "#k-hinweis{position:sticky;top:0;z-index:9999;background:#0F3B5C;color:#fff;font:14px/1.45 system-ui,sans-serif;padding:8px 16px}"
       "#k-hinweis ins{background:#c8ecc9;color:#0b3d12;text-decoration:none}#k-hinweis del{background:#f6c6c0;color:#5a1a12}</style>")
hinweis = ('<div id="k-hinweis">Kontrollfassung (v4.76): künftige deutsche Seite – Gemeinschaft der Staaten und sechs Spielregeln – gegen die geltende Seite. '
           '<ins>grün = neu</ins> · <del>rot = entfällt</del>. Fonds- und Kassenzahlen vorläufig (noch nicht in den Haushaltsrechnungen). Nur zur Durchsicht.</div>')
K = K.replace("</head>", css + "</head>", 1)
K = re.sub(r"(<body[^>]*>)", r"\1" + hinweis, K, count=1)
(HIER / "de-kontrolle.html").write_text(K, encoding="utf-8")
print(f"Entwurf geschrieben: {n} Ersetzungen")
