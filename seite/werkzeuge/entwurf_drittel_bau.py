#!/usr/bin/env python3
"""Entwurf der deutschen Webseite nach dem Vorbild der veröffentlichten Seite (Stand B), umgestellt auf das Drittel-System (Logbuch v3.55).

Grundsatz (Auftrag der Initiative, 17.10.2026): eng am Vorbild bleiben, nur geänderte Inhalte, Zahlen und Begriffe tauschen.
Technik: Vorlage (vorlage.html), Stylesheet und Texte (sprachen/de.json) werden aus seite_bau.py übernommen; dieser Baustein überschreibt
  - Texte, deren Inhalt sich geändert hat (TX unten),
  - die Zahlen der Gesamtrechnung 28:28 durch die Ergebnisse der Drittel-Rechnungen (netz33.json, projektion33.json, dynamik33.json,
    altlasten.json, moeglichkeitsraum33.json, systemvarianten.json),
  - wenige Stellen der Vorlage (Label-Stufen, Name, vierter Teil im Steuer-Euro für das starke Netz, Skala der Schuldengrafik).
Ausgabe: seite/entwurf/drittel/de.html. Der frühere Entwurf mit eigener Gliederung (entwurf33_bau.py) ist damit abgelöst.
"""
import importlib.util
import json
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
AGG = WURZEL / "daten" / "aggregate"
ZIEL = WURZEL / "seite" / "entwurf" / "drittel"
spec = importlib.util.spec_from_file_location("seite_bau", Path(__file__).resolve().parent / "seite_bau.py")
SB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SB)


def lade(n):
    return json.loads((AGG / n).read_text(encoding="utf-8"))


SV, PJ, NZ, DY, AL, MR, H = (lade(n) for n in ("systemvarianten.json", "projektion33.json", "netz33.json", "dynamik33.json", "altlasten.json",
                                               "moeglichkeitsraum33.json", "haushalte33.json"))
V = next(x for x in SV["varianten"] if x["id"] == PJ["system"])
PR = {r["jahr"]: r for r in PJ["reihe"]}
NB = {r["jahr"]: r for r in NZ["beschluss"]["reihe"]}
JAHRE = list(range(2028, 2061))
G26 = 12348
de = lambda x, nk=0: SB.zahl(x, nk, "de")
eur = lambda x, nk=0: SB.eur(x, "de", nk)
pct = lambda x, nk=0: SB.pct(x, "de", nk)


def interp(punkte, j):
    xs = sorted(punkte)
    if j <= xs[0]:
        return punkte[xs[0]]
    for a, b in zip(xs, xs[1:]):
        if a <= j <= b:
            return punkte[a] + (punkte[b] - punkte[a]) * (j - a) / (b - a)
    return punkte[xs[-1]]


def dyn_reihe(b, ki, kv):
    """Dividende nach Beschluss plus Differenz eines Szenarios aus dynamik33 (Stützjahre 2028/2035/2045/2060, dazwischen linear)."""
    s = next(x for x in DY["szenarien"] if x["beschaeftigung_pct"] == b and x["ki_pp"] == ki and x["kapital_verschiebung_pp"] == kv)["reihe"]
    s0 = next(x for x in DY["szenarien"] if x["beschaeftigung_pct"] == 0 and x["ki_pp"] == 0 and x["kapital_verschiebung_pp"] == 0)["reihe"]
    diff = {int(j): s[j]["dividende_erw_eur2026"] - s0[j]["dividende_erw_eur2026"] for j in s}
    return [NB[j]["dividende_erw_eur2026"] + interp(diff, j) for j in JAHRE]


# ---- Zahlen der Gesamtrechnung durch die Drittel-Rechnung ersetzen
J = dict(SB.J)
basis = [NB[j]["dividende_erw_eur2026"] for j in JAHRE]
J["reihe_jahre"] = JAHRE
J["reihe_erw"] = {"1,0": basis, "0,5": dyn_reihe(2.8, 0.3, 0.0), "1,5": dyn_reihe(4.6, 0.6, 3.0)}   # Schlüssel der Vorlage: 1,0 = Grundpfad (Rechner, Spark)
J["erw_de_2028"], J["erw_de_2060"], J["kind_de_2028"] = basis[0], basis[-1], basis[0] / 2
deck = {j: PR[j]["deckung"] + PR[j]["progression"] for j in JAHRE}
gem = {j: V["quote_kern"] - PR[j]["dach_ohne_zins"] - PR[j]["dividende_ohne_trends_pct_bip"] for j in JAHRE}
J["reihe_a"] = [PR[j]["dach_ohne_zins"] for j in JAHRE]
J["reihe_div"] = [NB[j]["dividende_pct_bip"] for j in JAHRE]
J["b_fach"] = gem[2028]
J["quote"] = V["deckung"]
sq = {2028: SB.J["schuldenquote_2028"], **{int(k): v for k, v in AL["beschluss"]["schuldenquote"].items()},
      AL["beschluss"]["spitzenjahr"]: AL["beschluss"]["schuldenquote_spitze"]}  # Spitze mitführen, sonst glättet die Interpolation sie weg
J["reihe_d"] = [round(interp(sq, j), 2) for j in JAHRE]
SB.J = J
SB.TARIF = [(G26 * x, s) for x, s in zip((1, 1.5, 2, 3), V["einkommen_saetze"][:4])] + [(None, V["einkommen_saetze"][-1])]

fall = lambda zu: next(f for f in H["faelle"] if f["jahr"] == 2028 and f["haushalt"] == "alleinstehend" and f["weitergabe_ag"] == 0.8
                       and f["vorsorge_satz"] == 0.1 and f["zuschlag_pct"] == zu)
ZU = max(f["zuschlag_pct"] for f in H["faelle"])
plus42 = next(z for z in fall(ZU)["zeilen"] if z["brutto"] == 42000)["differenz_monat"]
AB = AL["beschluss"]
RM = MR["raum"]

# ---- Geänderte Texte (alle übrigen Schlüssel bleiben wie in de.json)
TX = {
    "meta_titel": "Das Goldene Drittel",
    "meta_beschreibung": "Höchstens ein Drittel auf jedes Einkommen, ein starkes Netz ohne Prämie und jeden Monat eine Transformationsdividende. Gemeinden entscheiden selbst, ein gemeinsames Dach sichert die gemeinsamen Interessen.",
    "hero_btn1": "Eigene Rechnung prüfen",
    "hero_sub": "Alle Steuern und Abgaben werden gerecht auf Arbeit, Kapital und Automation verteilt. Arbeiten lohnt sich. Ein starkes Netz und die Transformationsdividende sorgen für sozialen Frieden. Höchstens ein Drittel auf jedes Einkommen. Gemeinden entscheiden selbst, ein gemeinsames europäisches Dach sichert die gemeinsamen Interessen.",
    "stamp1_lbl": "Transformationsdividende im Monat je Erwachsenem — {kind_2028} je Kind",
    "stamp2_val": "höchstens 33 %",
    "stamp3_val": "+" + eur(plus42) + "*",
    "stamp3_lbl": "mehr im Monat bei 42.000 € brutto",
    "hero_fein": "* Schätzung des Projekts: alleinstehend, 2028, heutige Kaufkraft, nach Pflichtvorsorge (10 %) und Altlastenzuschlag; 80 % der gesparten Arbeitgeberbeiträge gehen in den Lohn.",
    "svg_monat": "jeden Monat: die Transformationsdividende",
    "svg_monat2": "die Transformationsdividende",
    "div_h3": "Warum eine Transformationsdividende?",
    "div_p1": "Was wir heute erwirtschaften, ruht auf dem, was Generationen vor uns aufgebaut haben: Wissen, Technik, Infrastruktur. Immer mehr davon leisten Maschinen und Software. Die Dividende gibt jedem den gleichen Anteil zurück – vor allem das, was der Wandel einbringt: CO₂-Preis und die Sonderstufe für Schädliches. Jedes Land zahlt denselben Anteil seiner Wirtschaftsleistung aus. Sie wird kleiner, wenn Verbrenner und Emissionen verschwinden – das ist gewollt. Was trägt, ist das starke Netz.",
    "eff1_p": "mit seinem Geld umzugehen: höchstens ein Drittel Steuer, keine Beiträge, eigene Vorsorge auf dem eigenen Konto. Jeden Monat eine Dividende, ohne Antrag.",
    "fluss_l3": "Transformationsdividende",
    "bau_lede": "Jeder Baustein ist irgendwo auf der Welt schon erprobt. Das Goldene Drittel fügt sie zu einem System, das man auf einer Seite erklären kann.",
    "b1_h": "Stufentarif mit harter Obergrenze: das Goldene Drittel",
    "b1_p": "Besteuert wird das Brutto – ohne Abzüge, ohne Splitting. Der Grundbedarf bleibt frei; darüber lohnt Arbeit auf jeder Stufe. Die Stufen liegen beim Ein-, Eineinhalb-, Zwei- und Dreifachen des Grundbedarfs und wachsen mit ihm.",
    "b2_p": "Arbeit wird nicht länger doppelt belastet. Betriebe geben mindestens 80 % der gesparten Arbeitgeberbeiträge in den Lohn. Dänemark erhebt kaum Sozialbeiträge.",
    "b3_r": "33 % auf alle Erträge",
    "b4_r": "33 % über 100.000 € je Erwerb",
    "b7_r": "33 % am Ort der Nutzung",
    "b8_v4": "ressourcenintensiv, Luxus",
    "b8_v5": "Schädliches: Tabak, Alkohol, Kraftstoffe, Verbrenner",
    "b8_p": "Wie beim Energielabel sieht man auf einen Blick, was ein Produkt kostet und warum. Eingestuft wird nach dem Ressourcen- und CO₂-Fußabdruck, nicht nach der Herkunft. 33 % gelten nur für Schädliches.",
    "b9_r": "Europäischer Preispfad · Rückgabe über die Transformationsdividende",
    "baustein_div_titel": "Transformationsdividende: jeden Monat, für alle",
    "b10_p": "Erwachsene voll, Kinder zur Hälfte, ohne Antrag. Sie ist, was nach Dach, Gemeinden und Netz übrig bleibt – und gibt vor allem zurück, was der Wandel einbringt.",
    "b11_pos": "Das starke Netz",
    "b11_h": "Niemand fällt durch",
    "b11_r": "Grundversorgung ohne Prämie",
    "b11_p": "Geknüpft aus vielen Knoten – jeder hält mit, keiner fällt durch: Gesundheit, Pflege als Teilkasko, Mindestrente ab 67, Grundbedarf bei Invalidität und Arbeitslosigkeit. Keine Extras; was darüber geht, ist die eigene Route mit eigener Vorsorge (10 % des Lohns aufs eigene Konto).",
    "rech_lede": "Was Ihrem Haushalt im Goldenen Drittel mehr im Geldbeutel bleibt als heute – nach Steuern und Sozialabgaben, mit dem Arbeitgeberanteil im Lohn.",
    "rech_jahr": "Jahr",
    "rech_steuer": "Heute verfügbar im Monat",
    "rech_satz": "Im Goldenen Drittel verfügbar im Monat",
    "rech_sozial": "darin Transformationsdividende des Haushalts",
    "rech_mon": "Mehr im Geldbeutel im Jahr",
    "rech_bar1": "Heute im Monat",
    "rech_bar2": "Goldenes Drittel im Monat",
    "rech_fein": "Heute: Lohnsteuer, Solidaritätszuschlag und Sozialbeiträge der Beschäftigten nach Recht 2026, Kindergeld; ab 2035 Beitragssätze nach IGES-Projektion (eine Studie, Sekundärquelle), danach gleich gehalten. Goldenes Drittel: 80 % der gesparten Arbeitgeberbeiträge im Lohn, Tarif auf Lohn und Dividende, keine Sozialbeiträge, Pflichtvorsorge 10 % des Lohns aufs eigene Konto abgezogen, höhere Mehrwertsteuer auf den Konsum und Altlastenzuschlag " + pct(ZU, 1) + " (Beispiel) eingerechnet. Weitere Erwachsene ohne eigenes Einkommen; Bürgergeld und Wohngeld nicht gerechnet. Heutige Kaufkraft. Schätzung des Projekts, keine Steuerberatung.",
    "zeit_h2": "Die Transformationsdividende im Wandel",
    "zeit_lede": "Die Dividende gibt vor allem zurück, was Schädliches zahlt. Wenn Verbrenner und Emissionen verschwinden, sinkt dieser Teil; Gesundheit und Pflege kosten mit der Alterung mehr. Dagegen wirkt das Wachstum. So sinkt die Dividende von {erw_2028} (2028) und hält sich um {erw_2060} (2060). Mehr Arbeit und Automatisierung heben sie wieder an.",
    "zeit_t1": "Grundpfad",
    "zeit_t2": "Mehr Arbeit, KI mittel",
    "zeit_t3": "Kräftig",
    "zeit_unit": "Transformationsdividende je Erwachsenem und Monat, Euro in heutiger Kaufkraft",
    "zeit_l1": "Transformationsdividende",
    "sich2_p": "Jeder Euro über dem Bedarf geht an die Gemeinden, das starke Netz und die Transformationsdividende. Eine Grenze, die nicht ausgeschöpft werden muss, wird nie zum Anspruch.",
    "sich4_h": "Altlasten: Sache der Staaten",
    "sich4_p": "Alte Schulden und Rentenzusagen regelt jeder Staat selbst. Das Dach bietet Werkzeuge an: einen gemeinsamen Fonds mit gemeinsamem Zins, Tilgung bis spätestens 2098 – und für überschuldete Staaten ein geordnetes Neustartverfahren, das Netz und eigene Vorsorge schützt.",
    "erf_lede": "Nichts am Goldenen Drittel ist ein Experiment ins Blaue. Jeder Baustein läuft heute schon irgendwo – oft seit Jahrzehnten.",
    "klub_lede": "Das Dach ist kein fester Kreis, sondern ein Angebot. Gerechnet ist der Bauplan für " + str(RM["staaten"]) + " Staaten Europas (EU, Norwegen, Island, Schweiz) mit " + de(RM["einwohner_mio"], 1) + " Mio. Menschen – möglich sind auch Partner darüber hinaus. Wählen Sie selbst: Ab der Einwohnerzahl der Vereinigten Staaten spielt der Klub in derselben Liga.",
    "offen_lede": "Das Goldene Drittel wird unabhängig von Parteien und Interessengruppen entwickelt. Jede Zahl stammt aus amtlichen Statistiken, jede Rechnung lässt sich nachrechnen, jeder Fehler wird offen korrigiert. Gesucht sind Fachleute aus Finanzwissenschaft, Verwaltung, Kommunalpraxis, Recht und Statistik.",
    "js_fluss": "Im Jahr {j} behält das Dach {a} von {hundert} – erlaubt wären bis zu {cap}. Die Gemeinde verwendet {b} für ihre Aufgaben, das starke Netz {n}, {d} gehen als Transformationsdividende an die Bürger.",
    "js_rechner_sub": "mehr im Geldbeutel im Monat – im Jahr {j}, für {hh}",
    "js_schuld_l3": "Altlastenfonds, Beispiel für alle zehn",
    "js_schuld_text": "Altlasten sind Sache der Staaten. Legen alle zehn Schulden und Rentenzusagen in einen gemeinsamen Fonds, steigt dessen Quote bis " + str(AB["spitzenjahr"]) + " auf " + pct(AB["schuldenquote_spitze"]) + " und ist 2098 getilgt – mit einem Zuschlag von " + pct(AB["zuschlag_auf_alle_steuern_pct"], 1) + " auf alle Steuern.",
    "js_co2_text": "Seit 1990 fast halbiert – die zweite Hälfte steht noch bevor. Das Goldene Drittel setzt dafür auf einen gemeinsamen europäischen CO₂-Preis und gibt die Einnahmen über die Transformationsdividende an alle zurück.",
}

RECHNER_ALT = """function rechner(){const br=+$('brutto').value,e=+val('erw'),k=+val('kin'),j=val('rj'),i=idx(j);
  const erw=D.erw['1,0'][i],mon=e*erw+k*erw/2,jahr=mon*12,st=steuer(br);
  $('bruttoval').textContent=eur(br);$('r-st').textContent=eur(st);$('r-soz').textContent=eur(0);
  $('r-satz').textContent=br?pct(st/br*100,1):'–';$('r-mon').textContent=eur(mon);
  const hh=fill(e>1?T.js_erw_n:T.js_erw_1,{n:e})+(k?T.js_und+fill(k>1?T.js_kind_n:T.js_kind_1,{n:k}):'');
  $('r-jahr').textContent=eur(jahr);$('r-jahrsub').textContent=fill(T.js_rechner_sub,{j:j,hh:hh});
  const m=Math.max(st,jahr,1);$('bi-st').style.width=st/m*100+'%';$('bi-dv').style.width=jahr/m*100+'%';
  $('b-st').textContent=eur(st);$('b-dv').textContent=eur(jahr);}
$('brutto').addEventListener('input',rechner);['erw','kin','rj'].forEach(x=>seg(x,rechner));rechner();"""
# Gleiche Formeln wie modell/haushalte33.py, neu(); „heute" aus dem Raster (Kernmodell, Recht 2026 bzw. IGES-Sätze ab 2035)
RECHNER_NEU = """const R=D.rr;
function agR(b,reg){const c=R.beitrag[reg];return c[0]*Math.min(b,R.bbg_kv)+c[1]*Math.min(b,R.bbg_rv);}
function estR(x){let s=0,u=0;const g=R.stufen.concat([Infinity]);for(let i=0;i<g.length;i++){if(x>u)s+=(Math.min(x,g[i])-u)*R.saetze[i]/100;u=g[i];}return s;}
function kqR(n){const p=R.kq;if(n<=p[0][0])return p[0][1];for(let i=1;i<p.length;i++){if(n<=p[i][0]){const a=p[i-1][0],x=p[i-1][1],b=p[i][0],y=p[i][1];return x+(y-x)*(n-a)/(b-a);}}return p[p.length-1][1];}
function neuR(b,e,k,j){const i=R.jahre.indexOf(j),DIV=R.div[i]*12,EFF=R.eff[i],reg=j>=2035?'2035':'2028';
  const brutto=b+R.weitergabe*agR(b,reg),st=estR(brutto+DIV)+(e-1)*estR(DIV),div=DIV*e+k*DIV/2,netto=brutto-st+div;
  const konsum=kqR(netto)*netto,mm=konsum*((1+EFF/100)/(1+R.eff_alt/100)-1),mb=konsum*EFF/(100+EFF);
  return {netto:netto-mm-R.zuschlag/100*(st+mb)-R.vorsorge*b,div:div};}
function rechner(){const br=+$('brutto').value,e=+val('erw'),k=+val('kin'),j=+$('rj').value;
  const reg=j>=2035?'2035':'2028',h=R.heute[reg+'|'+e+'|'+k][Math.round((br-R.brutto[0])/1000)],n=neuR(br,e,k,j),d=n.netto-h;
  const sg=x=>(x>=0?'+':'−')+eur(Math.abs(x));
  $('bruttoval').textContent=eur(br);$('rjval').textContent=j;
  $('r-st').textContent=eur(h/12);$('r-satz').textContent=eur(n.netto/12);$('r-soz').textContent=eur(n.div/12);$('r-mon').textContent=sg(d);
  const hh=fill(e>1?T.js_erw_n:T.js_erw_1,{n:e})+(k?T.js_und+fill(k>1?T.js_kind_n:T.js_kind_1,{n:k}):'');
  $('r-jahr').textContent=sg(d/12);$('r-jahrsub').textContent=fill(T.js_rechner_sub,{j:j,hh:hh});
  const m=Math.max(h,n.netto,1);$('bi-st').style.width=h/m*100+'%';$('bi-dv').style.width=n.netto/m*100+'%';
  $('b-st').textContent=eur(h/12);$('b-dv').textContent=eur(n.netto/12);}
$('brutto').addEventListener('input',rechner);$('rj').addEventListener('input',rechner);['erw','kin'].forEach(x=>seg(x,rechner));rechner();"""

ERSETZE = [  # (alt, neu) in der Vorlage; jede Stelle muss genau einmal vorkommen
    # v3.56: Wortmarke „Das Goldene Drittel" in drei Zeilen, alle Zeilen in derselben Schriftgröße
    ('<svg class="hero-mark" viewBox="0 0 560 300" role="img" aria-label="TAX 28:28">', '<svg class="hero-mark" viewBox="0 0 560 390" role="img" aria-label="Das Goldene Drittel">'),
    ('<text x="60" y="168" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="196" fill="#0F3B5C" textLength="440" lengthAdjust="spacing">TAX</text>',
     '<text x="280" y="112" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C">Das</text>'
     '<text x="280" y="242" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C">Goldene</text>'),
    ('<text x="60" y="286" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C" letter-spacing="-2" textLength="440" lengthAdjust="spacing">28:28</text>',
     '<text x="280" y="372" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C">Drittel</text>'),
    ('<a class="tb-left" href="#top">TAX 28:28</a>', '<a class="tb-left" href="#top">Das Goldene Drittel</a>'),
    # v3.56: Rechner mit Zeitstrahl und „mehr im Geldbeutel" statt Einkommensteuer
    ('<input type="range" id="brutto" min="0" max="150000" step="1000" value="42000">', '<input type="range" id="brutto" min="10000" max="150000" step="1000" value="42000">'),
    ('<div class="seg" id="rj"><button type="button" aria-pressed="true" data-v="2028">2028</button><button type="button" aria-pressed="false" data-v="2035">2035</button><button type="button" aria-pressed="false" data-v="2045">2045</button><button type="button" aria-pressed="false" data-v="2060">2060</button></div>',
     '<div class="bigval" id="rjval">2028</div><input type="range" id="rj" min="2028" max="2060" step="1" value="2028" style="width:100%;accent-color:var(--ink)" aria-label="@@rech_jahr@@">'),
    (RECHNER_ALT, RECHNER_NEU),
    ('<div><b class="v4">C · 22&nbsp;%</b>', '<div><b class="v4">C · 25&nbsp;%</b>'),
    ('<div><b class="v5">D · 28&nbsp;%</b>', '<div><b class="v5" style="background:#5b1a14">S · 33&nbsp;%</b>'),
    ('<i class="sb" id="sb"></i>', '<i class="sb" id="sb"></i><i class="sn" id="sn" style="background:#8FB8A0"></i>'),
    ('<span><b style="background:#6497B8"></b>@@fluss_l2@@</span>', '<span><b style="background:#6497B8"></b>@@fluss_l2@@</span><span><b style="background:#8FB8A0"></b>Das starke Netz</span>'),
    ("function fluss(){const j=+$('jahr').value,i=idx(j);const a=D.a[i]/D.q*100,b=D.b/D.q*100,d=D.div[i]/D.q*100,c=D.og*D.einzugAnteil;",
     "function fluss(){const j=+$('jahr').value,i=idx(j);const q=D.qj[i],a=D.a[i]/q*100,b=D.bj[i]/q*100,n=D.n[i]/q*100,d=D.div[i]/q*100,c=D.og*D.einzugAnteil;"),
    ("[['sa',a],['sb',b],['sd',d]]", "[['sa',a],['sb',b],['sn',n],['sd',d]]"),
    ("fill(T.js_fluss,{j:j,a:eur(a),cap:eur(c),b:eur(b),d:eur(d),hundert:eur(100)})", "fill(T.js_fluss,{j:j,a:eur(a),cap:eur(c),b:eur(b),n:eur(n),d:eur(d),hundert:eur(100)})"),
    ("['mit',D.jahre,D.d]];lo=20;hi=100;step=20;", "['mit',D.jahre,D.d]];lo=0;hi=180;step=30;"),
    ('aria-pressed="false" data-v="0,5">@@zeit_t1@@', 'aria-pressed="true" data-v="1,0">@@zeit_t1@@'),
    ('aria-pressed="true" data-v="1,0">@@zeit_t2@@', 'aria-pressed="false" data-v="0,5">@@zeit_t2@@'),
]


def main():
    vorlage = SB.VORLAGE
    for a, b in ERSETZE:
        n = vorlage.count(a)
        if n < 1:
            raise SystemExit(f"Vorlage: Stelle nicht gefunden: {a[:70]}")
        vorlage = vorlage.replace(a, b)
    SB.VORLAGE = vorlage
    T = json.loads((SB.SPRACHEN_DIR / "de.json").read_text(encoding="utf-8"))
    fehlt = set(TX) - set(T)
    if fehlt:
        raise SystemExit(f"unbekannte Schlüssel: {sorted(fehlt)}")
    T.update(TX)
    W = SB.werte("de")
    W.update(erw_2028=eur(J["erw_de_2028"]), kind_2028=eur(J["kind_de_2028"]), erw_2060=eur(J["erw_de_2060"]), p28=pct(33))
    html = SB.baue("de", T, W)
    # zusätzliche Daten für den vierten Teil des Steuer-Euros
    extra = dict(rr=json.loads((WURZEL / "daten/aggregate/haushalte33_raster.json").read_text(encoding="utf-8"))["rechner"], qj=[round(deck[j], 3) for j in JAHRE], bj=[round(gem[j], 3) for j in JAHRE], n=[NB[j]["netz_pct_bip"] for j in JAHRE])
    html = html.replace("\nconst T=D.T;", "\nObject.assign(D," + json.dumps(extra) + ");\nconst T=D.T;", 1)
    html = re.sub(r"(<body[^>]*>)", r'\1<div style="background:#B03A2E;color:#fff;font-family:monospace;padding:8px 16px;text-align:center">'
                  r'ENTWURF ZUR PRÜFUNG – Drittel-System, nach dem Vorbild der veröffentlichten Seite – nicht veröffentlichen</div>', html, count=1)
    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / "de.html").write_text(html, encoding="utf-8")
    print(f"geschrieben: {(ZIEL / 'de.html').relative_to(WURZEL)} ({len(html)} Zeichen)")


if __name__ == "__main__":
    main()
