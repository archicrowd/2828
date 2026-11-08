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

_i = ALT.index('<div class="timeline" style="margin-top:34px">')
ZEITLEISTE = ALT[_i:ALT.index("</div>\n  </div>\n</section>", _i) + len("</div>")]
STEMPEL = re.search(r"Modellstand <b>v[0-9.]+ · [^<]+</b>", ALT).group(0)
R = []   # (alt, neu): jede alte Stelle muss genau einmal vorkommen

# Ebenen: Gemeinschaft der Staaten statt Dach (v4.76)
GK = json.loads((W / "daten" / "aggregate" / "gemeinschaft_kasse.json").read_text(encoding="utf-8"))["varianten"]["G1"]
R += [("<h2>Starke Kommunen und Regionen, starke Bürger, ein starkes europäisches Dach</h2>",
       "<h2>Starke Kommunen und Regionen, starke Bürger, eine starke Gemeinschaft der Staaten</h2>"),
      ("Kommunen und Regionen erhalten ihren Anteil direkt vom Dach, entscheiden selbst über Finanzen und delegieren Aufgaben an übergeordnete "
       "Verwaltungszusammenschlüsse (z. B. Infrastrukturverbünde). Das europäische Dach übernimmt nur, was Kommunen und Regionen allein nicht können "
       "– und darf sich nicht mehr nehmen, als im Vertrag steht.",
       "Kommunen und Regionen erhalten ihren Anteil nach einer festen Formel und entscheiden freier über lokale Aufgaben und Finanzen. "
       "Staat und Gemeinschaft der Staaten übernehmen nur, was Kommunen und Regionen allein nicht können – und behalten für die übergeordneten "
       "Aufgaben höchstens ein Drittel des Aufkommens."),
      ('<text x="180" y="44" text-anchor="middle" font-size="19" font-weight="700">Das gemeinsame Dach</text>',
       '<text x="180" y="44" text-anchor="middle" font-size="19" font-weight="700">Staat und Gemeinschaft</text>', "roh"),
      ('<text x="450" y="48" text-anchor="middle" font-size="20" font-weight="700">Das gemeinsame Dach</text>',
       '<text x="450" y="48" text-anchor="middle" font-size="20" font-weight="700">Staat und Gemeinschaft der Staaten</text>', "roh"),
      ("<div><h3>Dem Dach wird zugetraut,</h3><p>was nur gemeinsam geht: Verteidigung und digitale Souveränität, ein Binnenmarkt ohne Grenzen, "
       "gemeinsame Standards. Mehr nicht. Das Dach entscheidet mit der Mehrheit der Abgesandten der Zusammenschlüsse von Kommunen und Regionen.</p></div>",
       "<div><h3>Der Gemeinschaft der Staaten wird zugetraut,</h3><p>was nur gemeinsam geht: gemeinsame Forschung, Freizügigkeit, ein Markt ohne "
       "Grenzen, ein gemeinsames Gericht und gemeinsame Standards. In diesen Aufgaben entscheidet sie mit einfacher Mehrheit der Mitgliedstaaten; "
       "die Spielregeln selbst ändern die Staaten mit Zweidrittelmehrheit.</p></div>"),
      ('<span><b style="background:var(--ink)"></b>Dach</span>', '<span><b style="background:var(--ink)"></b>Staat und Gemeinschaft</span>', "roh"),
      ("width:0;height:12px\"></b>Obergrenze des Dachs</span>", "width:0;height:12px\"></b>Obergrenze von Staat und Gemeinschaft</span>", "roh"),
      ("Im Jahr {j} behält das Dach {a} von {hundert}", "Im Jahr {j} behalten Staat und Gemeinschaft {a} von {hundert}", "roh"),
      ("Das Goldene Drittel setzt dafür auf einen gemeinsamen europäischen CO₂-Preis und gibt",
       "Das Goldene Drittel setzt dafür auf einen gemeinsamen CO₂-Preispfad der Gemeinschaft nach dem Pariser Abkommen und gibt", "roh"),
      ("Die Verteilung durch das Dach mündet in zwei Zahlen", "Die Verteilung nach der Formel mündet in zwei Zahlen"),
      ("<p>Was wir heute erwirtschaften, ruht auf dem, was Generationen vor uns aufgebaut haben: Wissen, Technik, Infrastruktur. Immer mehr davon leisten Maschinen und Software. Die Dividende gibt jedem den gleichen Anteil zurück – aus dem, was der Wandel einbringt: CO₂-Preis und Sonderstufe für Schädliches, dazu die Besteuerung digitaler Plattformen am Ort ihrer Kundschaft. Ihre Höhe folgt aus der Wirtschaftsleistung und den Aufgaben jedes Landes. Sie wird kleiner, wenn Verbrenner und Emissionen verschwinden – das ist gewollt. Was trägt, ist das starke Netz.</p>\n      <p>Und sie gleicht aus, was der Umbau von Arbeit, Energie und Wirtschaft jedem Einzelnen abverlangt: Wer sich neu orientieren muss, steht nicht mit leeren Händen da.</p>",
       "<p>Was wir heute erwirtschaften, ruht auf dem, was Generationen vor uns aufgebaut haben: Wissen, Technik, Infrastruktur. Immer mehr davon leisten Maschinen und Software. Die Dividende gibt jedem den gleichen Anteil zurück – aus dem, was dieser Wandel einbringt. Finanziert wird sie aus dem CO₂-Preis und der Mehrwertsteuer auf schädlichen Konsum, dazu aus der Besteuerung digitaler Plattformen am Ort ihrer Kundschaft. Die Höhe der Dividende folgt aus der Wirtschaftsleistung und den Aufgaben jedes Landes.</p>\n      <p>Sie gleicht aus, was der Umbau von Arbeit, Energie und Wirtschaft jedem Einzelnen abverlangt. Sie ist unbürokratisch und unser gemeinsames Erbe aus den Früchten des Fortschritts.</p>"),
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
    <p class="lede">Einfach und für jeden Staat gleich. Was nur gemeinsam geht, trägt die Gemeinschaft der Staaten.</p>
    <div class="sich">
      <div><span><b>1 · Wer mitmacht</b><p>Jeder Staat, der Mitglied der Vereinten Nationen ist, beide Menschenrechtspakte von 1966 und das Pariser Klimaabkommen ratifiziert hat und rechtsstaatlich handelt (Rule of Law Index ab 0,66), kann mitmachen. Wer die Schwelle noch nicht erreicht, kann die gemeinsamen Regeln als „Partner“ anwenden.</p></span></div>
      <div><span><b>2 · Dieselben Regeln in jedem Land</b><p>Jeder Staat misst alles an seinem eigenen Grundbedarf: Tarif, Label, Dividende, starkes Netz und die festen Beträge für Kommunen und Regionen. Staat und Gemeinschaft behalten zusammen höchstens ein Drittel der Einnahmen. Die feste Formel ersetzt ewige Verhandlungen. Niemand muss bitten, niemand kann kürzen.</p></span></div>
      <div><span><b>3 · Was nur gemeinsam geht</b><p>Die Gemeinschaft der Staaten sichert Freizügigkeit für alle Bürgerinnen und Bürger, einen Markt ohne Grenzen für Waren, Dienste und Kapital, einen gemeinsamen Forschungsraum und ein gemeinsames Gericht, an das sich auch jeder Einzelne wenden kann. Steuerregeln und Konsumlabel gelten überall gleich; Versicherungsjahre zählen in jedem Staat. Für Forschung, Standards und Gericht zahlt jeder Staat denselben Anteil seiner Wirtschaftsleistung in eine gemeinsame Kasse. In diesen Aufgaben entscheidet die Gemeinschaft mit einfacher Mehrheit; die Spielregeln selbst ändern die Staaten mit Zweidrittelmehrheit.</p></span></div>
      <div><span><b>4 · Altlasten: halb selbst, halb gemeinsam</b><p>Alte Schulden und Rentenzusagen trägt jeder Staat zur Hälfte selbst; die andere Hälfte tragen alle Teilnehmer, um gemeinsam stark zu sein. Alles ist 2098 getilgt. Partner tragen ihre Altlast so lange selbst, bis sie die gemeinsamen Standards voll erreicht haben. Für überschuldete Staaten gibt es ein geordnetes Neustartverfahren. Bestehende Renten laufen weiter. Alte Zusagen ohne eigene Deckung (z. B. aus der gesetzlichen Rente, Pensionen) bleiben nach 35 Versicherungsjahren bis zum doppelten Grundbedarf ungekürzt (bei kürzerer Laufbahn anteilig, nie unter dem Grundbedarf); darüber werden sie ab dem Stichtag gestuft gekürzt. Die eigene Vorsorge bleibt immer ungekürzt, und die Kranken- und Pflegebeiträge der Rentner entfallen. Kein Rentnerhaushalt fällt unter die heutige Grundsicherung.</p></span></div>
      <div><span><b>5 · Nachhaltig berichten</b><p>Jeder Staat berichtet regelmäßig an die Vereinten Nationen über die 17 Ziele für nachhaltige Entwicklung.</p></span></div>
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
    ("Bericht zu den 17 Zielen", "Agenda 2030 (Resolution 70/1): Freiwillige Nationale Berichte an das Hochrangige Politische Forum"),
    ("Besteuerung am Ort der Kunden", "Gegenstand der Verhandlungen über eine Rahmenkonvention der Vereinten Nationen zur Zusammenarbeit in Steuerfragen (seit 2025; ein Protokoll betrifft grenzüberschreitende Dienstleistungen einschließlich automatisierter digitaler Dienste)"),
]
rows = "".join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a, b in herleitung)

# Änderung 8 (8.11.2026): Rechenspiel „Bauen Sie die Gemeinschaft“ statt „Klub mit Raum zum Wachsen“
import csv
with open(W / "daten" / "aggregate" / "moeglichkeitsraum.csv", encoding="utf-8") as f:
    MIO = {r["land"]: float(r["einwohner_mio"]) for r in csv.DictReader(f)}
# außerhalb Europas: UN World Population Prospects 2024, Stand 1.7.2023 (über eine Kopie der Wikipedia-Liste gelesen, Sekundärquelle, zu prüfen);
# CA, UK, US aus moeglichkeitsraum.csv
MIO.update(AU=26.451124, JP=124.370947, KR=51.748739, NZ=5.172836, CL=19.658835, UY=3.388081, CR=5.105525, BB=0.282336, MU=1.273588)
WELT = 8091.734930
EU27 = [c for c in EUROPA if c not in ("NO", "IS", "CH")]
GS = {c: [NAME[c], round(MIO[c], 1), "e" if c in teil_eu else "w" if c in teil_welt else "p"] for c in teil + partner}
spiel_daten = json.dumps(dict(gs=GS, us=round(MIO["US"], 1), eu=round(sum(MIO[c] for c in EU27), 1), welt=WELT,
                              vor=dict(regel=sorted(teil), dreissig=sorted(EUROPA), alle=sorted(teil + partner), europa=sorted(teil_eu))), ensure_ascii=False)
knoepfe = "".join(f'<button type="button" aria-pressed="false" data-k="{c}" class="{dict(e="", w="neu", p="partner")[GS[c][2]]}">'
                  f'<span class="nm">{GS[c][0]}</span><span>{z(GS[c][1])} Mio.</span></button>'
                  for c in sorted(GS, key=lambda x: -GS[x][1]))
spiel = f'''<h3 class="sub-h">Bauen Sie die Gemeinschaft</h3>
    <p class="lede">Wählen Sie aus, wer mitmacht. Schwarz: Teilnahme in Europa · grün umrandet: Teilnahme weltweit · gestrichelt: Partner.</p>
    <div class="flow">
      <div class="tabs" id="gsvor"><button type="button" aria-pressed="true" data-v="regel">Alle, die die erste Regel erfüllen</button><button type="button" aria-pressed="false" data-v="alle">Mit Partnern</button><button type="button" aria-pressed="false" data-v="europa">Nur Europa</button><button type="button" aria-pressed="false" data-v="dreissig">Die 30 gerechneten</button></div>
      <div class="raum" id="gsraum">{knoepfe}</div>
      <div class="row"><div class="res-row" style="flex:1;border:none"><span class="k">Menschen in der Gemeinschaft</span><span class="v new" id="gssum"></span></div><div class="res-row" style="flex:1;border:none"><span class="k">Staaten</span><span class="v" id="gsn"></span></div><div class="res-row" style="flex:1;border:none"><span class="k">Anteil an der Weltbevölkerung</span><span class="v" id="gswelt"></span></div></div>
      <div class="schwelle"><i id="gsbar"></i><span class="us" id="gsus"><span>USA</span></span><span class="us" id="gseu"><span>EU</span></span></div>
      <p class="fineprint" id="gstext" style="margin-top:0"></p>
    </div>
    <p class="fineprint">Einwohner: Eurostat 2024, Statistics Canada 2025, US Census Bureau 2025, sonst Vereinte Nationen (World Population Prospects 2024, Stand 2023). Gerechnet sind bisher nur die 30 Staaten Europas. Die Vereinigten Staaten, Singapur und Botswana erfüllen die Grundlagen der ersten Regel nicht.</p>'''
spiel_js = """<script>(function(){const D=__D__;const $=id=>document.getElementById(id);
const f=(x,d)=>x.toLocaleString('de-DE',{minimumFractionDigits:d,maximumFractionDigits:d});const SK=1000;
function lauf(){const on=[...document.querySelectorAll('#gsraum button[aria-pressed=true]')].map(b=>b.dataset.k);
 const sum=on.reduce((a,k)=>a+D.gs[k][1],0),p=on.filter(k=>D.gs[k][2]==='p').length;
 $('gssum').textContent=f(sum,1)+' Mio.';$('gsn').textContent=on.length+(p?' (davon '+p+' Partner)':'');$('gswelt').textContent=f(sum/D.welt*100,1)+' %';
 $('gsbar').style.width=Math.min(sum/SK*100,100)+'%';$('gsus').style.left=(D.us/SK*100)+'%';$('gseu').style.left=(D.eu/SK*100)+'%';
 const v=sum>=D.us?f(sum-D.us,1)+' Mio. mehr als die USA':f(D.us-sum,1)+' Mio. weniger als die USA';
 $('gstext').textContent='Die Gemeinschaft hätte '+f(sum,1)+' Mio. Menschen in '+on.length+' Staaten – '+v+'. Jeder weitere Staat stärkt die gemeinsamen Regeln, vor allem die Besteuerung am Ort der Kunden.';}
function vor(v){const s=new Set(D.vor[v]);document.querySelectorAll('#gsraum button').forEach(b=>b.setAttribute('aria-pressed',s.has(b.dataset.k)?'true':'false'));
 document.querySelectorAll('#gsvor button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.v===v?'true':'false'));lauf();}
$('gsraum').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');
 document.querySelectorAll('#gsvor button').forEach(x=>x.setAttribute('aria-pressed','false'));lauf();});
$('gsvor').addEventListener('click',e=>{const b=e.target.closest('button');if(b)vor(b.dataset.v);});vor('regel');})();</script>""".replace("__D__", spiel_daten)
neu_klub = f'''<h2>Eine offene Gemeinschaft der Staaten auf dem Boden der Vereinten Nationen</h2>
    <p class="lede">Die Gemeinschaft der Staaten ist kein fester Kreis, sondern ein Angebot. Mitmachen kann jeder Staat, der die erste Spielregel erfüllt – gleich, wo er auf der Landkarte liegt. Gerechnet ist bisher der Bauplan für 30 Staaten Europas (EU, Norwegen, Island, Schweiz) mit 465,6 Mio. Menschen. Nach einer ersten Durchsicht erfüllen {len(teil)} Staaten die Regel; {len(partner)} weitere können als Partner beginnen.</p>
    {stub}
    {spiel}
    <p class="fineprint">Erste Durchsicht: Rule of Law Index 2025 (World Justice Project); Vertragsregister der Vereinten Nationen (Menschenrechtspakte, Pariser Abkommen). Für die Schweiz und Island gibt es keinen Indexwert; sie sind vorläufig eingeordnet. Partner wenden die Regeln an und tragen ihre Altlast selbst, bis sie die gemeinsamen Standards voll erreichen.</p>
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
R += [("<p class=\"sub\">Alle Steuern und Abgaben werden gerecht auf Arbeit, Kapital und Automation verteilt – höchstens ein Drittel auf jedes Einkommen. Arbeit lohnt sich, und das starke soziale Netz und die Transformationsdividende sorgen für sozialen Frieden. Die Kommunen und Regionen entscheiden eigenständiger, ein europäisches Dach sichert die gemeinsamen Interessen mit Mehrheitsentscheid.</p>",
       "<p class=\"sub\">Steuern können die Welt verändern! Sie können lenken, dass Menschen sich nach gemeinsamen Zielen verhalten, einfach weil es sich für sie lohnt. Und weil Regeln akzeptiert werden, wenn sie fair sind. Niemand versteht, warum eine Pflegerin mehr auf ihr Einkommen bezahlen soll als ein Plattformanbieter im Internet oder ein Anlageprofi auf seinen Profit. Darum verteilt das „Goldene Drittel“ alle Steuern und Abgaben gleichmäßig auf Arbeit, Kapital und Automation.</p><p class=\"sub\">Das Konzept entwickelt und rechnet international anwendbare Regeln: nach den Grundsätzen der Vereinten Nationen und dem Pariser Abkommen, fair für die junge Generation und auf breiten, nachhaltigen Wohlstand zielend.</p>"),
      (ZEITLEISTE, "", "block"),
      ('<div class="tabs" id="ztabs"><button type="button" aria-pressed="true" data-v="co2">CO₂-Emissionen</button></div>',
       '<div class="tabs" id="ztabs"><button type="button" aria-pressed="true" data-v="gini">Ungleichheit</button><button type="button" aria-pressed="false" data-v="co2">CO₂-Emissionen</button><button type="button" aria-pressed="false" data-v="eink">Verfügbares Einkommen</button></div>'),
      ("seg('ztabs',chart2);chart2('co2');", "REISEJS", "roh"),
      ('y="72" text-anchor="middle">mindestens 68\u00a0% an Kommunen und Regionen</text>', 'y="72" text-anchor="middle">mindestens zwei Drittel an Kommunen und Regionen</text>', "roh"),
      ('style="font-size:10px">mindestens 68\u00a0% an Kommunen und Regionen</text>', 'style="font-size:10px">mindestens zwei Drittel an Kommunen und Regionen</text>', "roh"),
      ('"og": 32.0,', '"og": 33.3,', "roh"),
      ("So sinkt die Dividende von 354\u00a0€ (2028) und hält sich um 227\u00a0€ (2060). Mehr Arbeit und Automatisierung heben sie wieder an.",
       "Im Grundpfad sinkt die Dividende von 354\u00a0€ (2028) und hält sich um 227\u00a0€ (2060). Mehr Arbeit und Automatisierung heben sie wieder an: Im mittleren Pfad (mehr Arbeit, KI mittel) liegt sie 2060 bei 271\u00a0€."),
      ('<details class="mehr"><summary>Verlauf der Dividende bis 2060 anzeigen</summary>', '<details class="mehr" open><summary>Verlauf der Dividende bis 2060</summary>'),
      ('<button type="button" aria-pressed="true" data-v="1,0">Grundpfad</button><button type="button" aria-pressed="false" data-v="0,5">Mehr Arbeit, KI mittel</button>',
       '<button type="button" aria-pressed="false" data-v="1,0">Grundpfad</button><button type="button" aria-pressed="true" data-v="0,5">Mehr Arbeit, KI mittel</button>', "roh"),
      ("seg('gtabs',chart);chart('1,0');", "seg('gtabs',chart);chart('0,5');", "roh"),
      ("</body></html>", "SPIELJS</body></html>", "roh"),
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
GI = json.loads((W / "daten" / "aggregate" / "gini.json").read_text(encoding="utf-8"))["staaten"]["DE"]
GINI = dict(heute=GI["gini_amtlich_2025"], j=[r["jahr"] for r in GI["reihe"] if r["jahr"] <= 2040], v=[r["mitte"] for r in GI["reihe"] if r["jahr"] <= 2040])
REISE = """
// Wohin die Reise geht (Entwurf v4.78): drei Karten bis 2040
const GINI=__G__;
function reise(t){const W=900,H=360,L=60,RR=30,TP=20,B=40,x1=2040;let ser,lo=0,hi,step,x0,fy=x=>zahl(x),fl=null,txt;
  if(t==='gini'){x0=2025;lo=20;hi=32;step=2;fy=x=>zahl(x);fl=x=>zahl(x,1);
    ser=[['ohne',[2025,2040],[GINI.heute,GINI.heute]],['mit',[2025].concat(GINI.j),[GINI.heute].concat(GINI.v)]];
    $('zunit').textContent='Gini-Koeffizient des verfügbaren Einkommens in Deutschland (0 = alle gleich, 100 = einer hat alles)';
    $('zleg').innerHTML='<span class="l-ohne"><i></i>heute (2025, amtlich; gleichbleibend angenommen)</span><span class="l-mit"><i></i>Goldenes Drittel (Modell)</span>';
    txt='Die Ungleichheit sinkt: Der Gini-Koeffizient fällt von '+zahl(GINI.heute,1)+' (2025) auf '+zahl(GINI.v[0],1)+' (2028) und liegt 2040 bei '+zahl(GINI.v[GINI.v.length-1],1)+'. Statische Modellrechnung ohne Verhaltensänderung.';}
  else if(t==='co2'){const Z=D.zeit;x0=2010;const zj=[],zv=[];Z.co2_ziel_jahre.forEach((j,k)=>{if(j<=x1){zj.push(j);zv.push(Z.co2_ziel[k]);}});
    ser=[['hist',Z.co2_hist_jahre,Z.co2_hist],['ohne',zj,zv]];[hi,step]=nice(Math.max(...Z.co2_hist));
    $('zunit').textContent=T.js_co2_unit;
    $('zleg').innerHTML='<span class="l-hist"><i></i>'+T.js_co2_l1+'</span><span class="l-ohne"><i></i>'+T.js_co2_l2+'</span>';txt=T.js_co2_text;}
  else{x0=2028;const rr=D.rr,i=rr.brutto.indexOf(42000),cur=R;R=rr;const js=[],h=[],n=[];
    for(let j=2028;j<=x1;j++){js.push(j);h.push(rr.heute[(j>=2035?'2035':'2028')+'|1|0'][i]/12);n.push(neuR(i,42000,1,0,j).netto/12);}R=cur;
    ser=[['hist',js,h],['mit',js,n]];[hi,step]=nice(Math.max(...h,...n));fy=x=>eur(x);
    $('zunit').textContent='Verfügbares Einkommen im Monat bei 42.000 € Jahresbrutto, alleinstehend, Euro in heutiger Kaufkraft';
    $('zleg').innerHTML='<span class="l-hist"><i></i>heutiges System</span><span class="l-mit"><i></i>Goldenes Drittel</span>';
    txt='Bei 42.000 € Jahresbrutto bleiben 2028 '+eur(n[0])+' statt '+eur(h[0])+' im Monat ('+(n[0]>=h[0]?'+':'−')+eur(Math.abs(n[0]-h[0]))+'); 2040 sind es '+eur(n[n.length-1])+' statt '+eur(h[h.length-1])+'. Die Dividende sinkt mit den Emissionen, die Beiträge im heutigen System steigen mit der Alterung. Nach Pflichtvorsorge und Altlastenzuschlag; ohne Lohnwachstum.';}
  const X=x=>L+(x-x0)/(x1-x0)*(W-L-RR),Y=y=>TP+(hi-y)/(hi-lo)*(H-TP-B);let g='';
  for(let y=lo;y<=hi+1e-9;y+=step)g+=`<line class="grid" x1="${L}" x2="${W-RR}" y1="${Y(y)}" y2="${Y(y)}"/><text class="axis" x="${L-8}" y="${Y(y)+4}" text-anchor="end">${fy(y)}</text>`;
  const ticks=t==='co2'?[2010,2015,2020,2025,2030,2035,2040]:t==='gini'?[2025,2028,2030,2035,2040]:[2028,2030,2035,2040];
  ticks.forEach(x=>{g+=`<text class="axis" x="${X(x)}" y="${H-12}" text-anchor="middle">${x}</text>`;});
  ser.forEach(([c,xs,ys])=>{g+=`<path class="${c}" d="${xs.map((x,k)=>(k?'L':'M')+X(x)+','+Y(ys[k])).join(' ')}"/>`;
    const k=ys.length-1;g+=`<text class="axis" x="${X(xs[k])}" y="${Y(ys[k])-8}" text-anchor="end">${(fl||fy)(ys[k])}</text>`;});
  $('chart2').innerHTML=g;$('ztext').textContent=txt;}
seg('ztabs',reise);reise('gini');""".replace("__G__", json.dumps(GINI))
CSS_SPIEL = ("<style>.raum button.partner{border-style:dashed}.schwelle #gseu{border-left-color:var(--accent)}"
             ".schwelle #gseu span{top:-22px}</style>")
NEU = NEU.replace("REISEJS", REISE).replace("SPIELJS", spiel_js).replace("</head>", CSS_SPIEL + "</head>", 1)
K = K.replace("REISEJS", REISE).replace("SPIELJS", spiel_js).replace("</head>", CSS_SPIEL + "</head>", 1)
(HIER / "de.html").write_text(NEU, encoding="utf-8")
css = ("<style>ins.k-neu{background:#c8ecc9;color:#0b3d12;text-decoration:none}del.k-weg{background:#f6c6c0;color:#5a1a12}"
       ".k-block-weg{outline:3px solid #e8a39a;margin-bottom:28px;opacity:.85}"
       "#k-hinweis{position:sticky;top:0;z-index:9999;background:#0F3B5C;color:#fff;font:14px/1.45 system-ui,sans-serif;padding:8px 16px}"
       "#k-hinweis ins{background:#c8ecc9;color:#0b3d12;text-decoration:none}#k-hinweis del{background:#f6c6c0;color:#5a1a12}</style>")
hinweis = ('<div id="k-hinweis">Kontrollfassung (v4.78): künftige deutsche Seite mit den Änderungen der Initiative vom 8.11.2026 gegen die geltende Seite. '
           '<ins>grün = neu</ins> · <del>rot = entfällt</del>. Fonds- und Kassenzahlen vorläufig (noch nicht in den Haushaltsrechnungen). Nur zur Durchsicht.</div>')
K = K.replace("</head>", css + "</head>", 1)
K = re.sub(r"(<body[^>]*>)", r"\1" + hinweis, K, count=1)
(HIER / "de-kontrolle.html").write_text(K, encoding="utf-8")
print(f"Entwurf geschrieben: {n} Ersetzungen")
