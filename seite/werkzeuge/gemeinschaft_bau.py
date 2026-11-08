#!/usr/bin/env python3
"""Webseite nach den Spielregeln und der Gemeinschaft der Staaten, sechs Sprachen (Logbuch v4.80).

Nachfolger des Entwurfs seite/entwurf/spielregeln/bau.py (v4.75–v4.79, nur Deutsch). Läuft nach drittel_bau.py und formt
seite/stand-c/{de,en,fr,it,es,pl}.html an festen Stellen der Vorlage um (Aufbau in allen Sprachen gleich, daher Fundstellen nach Struktur,
nicht nach Wortlaut). Jede Fundstelle muss genau einmal vorkommen, sonst bricht das Skript ab.
  - Kopf, Ebenen, Formel, Forschung, Preispfad, Dividende, Zeitpfad: Texte aus gemeinschaft_texte.py
  - Abschnitt „sicherungen“: sechs Spielregeln für die Teilnahme, danach das Rechenspiel auf der Weltkarte (v4.80: hinter die Regeln gesetzt,
    zwei Ansichten statt vier)
  - Abschnitt „klub“: offene Gemeinschaft, was sie verbindet, Herleitung aus den Verträgen der Vereinten Nationen; Rubrik „Wohin die Reise geht“ entfällt
Karte: seite/werkzeuge/karte/karte.json (karte_bau.js), Ländernamen karte/namen.json (CLDR, namen_bau.js).
Zahlen: daten/aggregate/staatenauswahl.json, fonds_5050.json, moeglichkeitsraum.csv; Dividende 2060 im mittleren Pfad aus den Daten der Seite.
Zusätzlich: seite/entwurf/gemeinschaft/de-kontrolle.html (Ergänzungen grün, Streichungen rot, gegen die Ausgabe von drittel_bau.py).
Übersetzungen en/fr/it/es/pl: durch KI, gegenzulesen.
"""
import csv
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
W = HIER.parents[1]
ZIEL = W / "seite" / "stand-c"
AGG = W / "daten" / "aggregate"
MARKE = "<!-- gemeinschaft_bau v4.80 -->"
SPRACHEN = ["de", "en", "fr", "it", "es", "pl"]

spec = importlib.util.spec_from_file_location("gemeinschaft_texte", HIER / "gemeinschaft_texte.py")
GT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(GT)
T = GT.T

if any(MARKE in (ZIEL / f"{l}.html").read_text(encoding="utf-8") for l in SPRACHEN):
    subprocess.run([sys.executable, str(HIER / "drittel_bau.py")], check=True, stdout=subprocess.DEVNULL)

F55 = json.loads((AGG / "fonds_5050.json").read_text(encoding="utf-8"))
SA = json.loads((AGG / "staatenauswahl.json").read_text(encoding="utf-8"))
KARTE = json.loads((HIER / "karte" / "karte.json").read_text(encoding="utf-8"))
NAMEN = json.loads((HIER / "karte" / "namen.json").read_text(encoding="utf-8"))
with open(AGG / "moeglichkeitsraum.csv", encoding="utf-8") as f:
    MIO = {r["land"]: float(r["einwohner_mio"]) for r in csv.DictReader(f)}
# außerhalb Europas: UN World Population Prospects 2024, Stand 1.7.2023 (über eine Kopie der Wikipedia-Liste gelesen, Sekundärquelle, zu prüfen)
MIO.update(AU=26.451124, JP=124.370947, KR=51.748739, NZ=5.172836, CL=19.658835, UY=3.388081, CR=5.105525, BB=0.282336, MU=1.273588)
WELT = 8091.734930

EUROPA = set(F55["laender"])
EU27 = [c for c in EUROPA if c not in ("NO", "IS", "CH")]
st = SA["zaehlung"]
TEIL = st["Teilnahme"] + st.get("ohne WJP-Wert (zweite Quelle nötig)", [])
PARTNER = st["Partner"]
ISO2 = {c: {"EL": "GR", "UK": "GB"}.get(c, c) for c in TEIL + PARTNER}
ISO3 = dict(AT="AUT", BE="BEL", BG="BGR", CH="CHE", CY="CYP", CZ="CZE", DE="DEU", DK="DNK", EE="EST", EL="GRC", ES="ESP", FI="FIN", FR="FRA",
            HR="HRV", HU="HUN", IE="IRL", IS="ISL", IT="ITA", LT="LTU", LU="LUX", LV="LVA", MT="MLT", NL="NLD", NO="NOR", PL="POL", PT="PRT",
            RO="ROU", SE="SWE", SI="SVN", SK="SVK", AU="AUS", BB="BRB", CA="CAN", CL="CHL", CR="CRI", JP="JPN", KR="KOR", NZ="NZL", UK="GBR",
            UY="URY", MU="MUS")
# übrige Mitglieder des Europarats (eigene Kenntnis, Stand 2026, zu prüfen): halbgrün, nicht wählbar
EUROPARAT = dict(ALB="AL", AND="AD", ARM="AM", AZE="AZ", BIH="BA", GEO="GE", LIE="LI", MDA="MD", MCO="MC", MNE="ME", MKD="MK", SMR="SM",
                 SRB="RS", TUR="TR", UKR="UA")
VON3 = {v: k for k, v in ISO3.items() if k in TEIL + PARTNER}
spec = importlib.util.spec_from_file_location("seite_bau", HIER / "seite_bau.py")
SB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SB)


def zahl(x, d, l):
    return SB.zahl(x, d, l)


def fertig(s, **kw):
    for k, v in kw.items():
        s = s.replace("{" + k + "}", str(v))
    return s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def abschnitt(H, sid):
    i = H.index(f'<section id="{sid}">')
    return i, H.index("</section>", i) + len("</section>")


def einmal(H, pat, flags=0, start=0, ende=None):
    """Genau eine Fundstelle eines regulären Ausdrucks im Bereich [start, ende)."""
    ende = len(H) if ende is None else ende
    m = list(re.finditer(pat, H[start:ende], flags))
    if len(m) != 1:
        raise SystemExit(f"Fundstelle {len(m)}× statt 1×: {pat[:70]}")
    return m[0].group(0)


def paare(H, L):
    t = T[L]
    R = []   # (alt, neu, art): art text = Wortlaut, block = ganzer Abschnitt, roh = ohne Markierung
    m = re.search(r'<p class="sub">.*?</p>', H, re.S)
    R.append((m.group(0), "".join(f'<p class="sub">{p}</p>' for p in t["hero"]), "text"))
    a, b = abschnitt(H, "ebenen")
    h2 = einmal(H, r"<h2>[^<]*</h2>", 0, a, b)
    R.append((h2, f"<h2>{t['ebenen_h2']}</h2>", "text"))
    R.append((f'"{h2[4:-5]}"', f'"{t["ebenen_h2"]}"', "alle"))   # aria-label der beiden Ebenen-Grafiken
    m = re.search(r'(<meta name="description" content="[^"]*, )([^",]*)"', H)
    R.append((m.group(0), m.group(1) + t["meta_schluss"] + '"', "roh"))
    R.append((GT.CO2[L][0], GT.CO2[L][1], "roh"))   # Text der entfallenen CO₂-Grafik (Daten der Seite)
    R.append((re.search(r'<p class="lede">.*?</p>', H[a:b], re.S).group(0), f'<p class="lede">{t["ebenen_lede"]}</p>', "text"))
    for pat, neu in ((r'<text x="180" y="44"[^>]*>[^<]*</text>', t["staat_kurz"]), (r'<text x="450" y="48"[^>]*>[^<]*</text>', t["staat_lang"]),
                     (r'style="font-size:10px">[^<]*68[^<]*</text>', t["zwei_drittel"]), (r'y="72" text-anchor="middle">[^<]*</text>', t["zwei_drittel"])):
        alt = einmal(H, pat, 0, a, b)
        R.append((alt, re.sub(r">[^<]*</text>$", f">{neu}</text>", alt), "roh"))
    alt = re.findall(r"<div><h3>[^<]*</h3><p>[^<]*</p></div>", H[a:b])[2]
    R.append((alt, f"<div><h3>{t['zug_h3']}</h3><p>{t['zug_p']}</p></div>", "text"))
    for pat, neu in ((r'<b style="background:var\(--ink\)"></b>[^<]*</span>', t["leg_staat"]), (r'width:0;height:12px"></b>[^<]*</span>', t["leg_ober"])):
        alt = einmal(H, pat)
        R.append((alt, re.sub(r"</b>[^<]*</span>$", f"</b>{neu}</span>", alt), "roh"))
    alt = einmal(H, r'"js_fluss": "[^"]*"')
    R.append((alt, '"js_fluss": ' + json.dumps(t["js_fluss"], ensure_ascii=False), "roh"))
    R.append((einmal(H, r'"og": 32\.0,'), '"og": 33.3,', "roh"))
    # Gemeinde: Satzanfang bis zum ersten Doppelpunkt
    a, b = abschnitt(H, "gemeinde")
    lede = re.search(r'<p class="lede">([^:<]*):', H[a:b]).group(1)
    R.append((lede + ":", t["gem_start"] + ":", "text"))
    # Chancen: Forschungssatz (vierter Absatz bis zum ersten „).“)
    a, b = abschnitt(H, "chancen")
    p3 = re.findall(r"<p>(.*?)</p>", H[a:b], re.S)[2]
    R.append(("<p>" + p3[:p3.index(").") + 2], "<p>" + t["forschung"], "text"))
    # Preispfad (siebte Regelzeile im Label-Teil)
    rg = re.findall(r'<span class="regel">([^<]*)', H)[6].split(" · ")[0]
    R.append((f'<span class="regel">{rg} · ', f'<span class="regel">{t["preispfad"]} · ', "text"))
    # Dividende: Kasten mit zwei Absätzen
    box = einmal(H, r'<div class="box">.*?</div>', re.S)
    ps = re.findall(r"<p>.*?</p>", box, re.S)
    if len(ps) != 2:
        raise SystemExit("Kasten Dividende: nicht zwei Absätze")
    alt = ps[0] + box[box.index(ps[0]) + len(ps[0]):box.index(ps[1])] + ps[1]
    R.append((alt, f"<p>{t['div'][0]}</p>" + box[box.index(ps[0]) + len(ps[0]):box.index(ps[1])] + f"<p>{t['div'][1]}</p>", "text"))
    # Zeitpfad: letzter Satz der Einleitung, ergänzt um den mittleren Pfad 2060
    a, b = abschnitt(H, "zeitpfad")
    lede = re.search(r'<p class="lede">(.*?)</p>', H[a:b], re.S).group(1)
    letzt = lede[lede.rstrip(". ").rfind(". ") + 2:]
    satz28 = lede[:len(lede) - len(letzt)].rstrip()
    satz28 = satz28[satz28.rstrip(".").rfind(". ") + 2:]
    m28 = re.search(r"(\S*?)(\d[\d., ]*\d|\d)([  ]?[^\s(\d]*) \(2028\)", satz28)
    erw = json.loads(re.search(r'"erw": (\{.*?\})', H).group(1))
    jahre = json.loads(re.search(r'"jahre": (\[.*?\])', H).group(1))
    m60 = m28.group(1) + zahl(erw["0,5"][jahre.index(2060)], 0, L) + m28.group(3)
    lab = re.search(r'data-v="0,5">([^<]*)</button>', H).group(1)
    neu = fertig(t["zeit_mehr"], m=m60, lab=lab[:1].lower() + lab[1:])
    if L == "de":
        R.append((satz28 + " " + letzt, satz28.replace("So sinkt", "Im Grundpfad sinkt") + " " + neu, "text"))
    else:
        R.append((letzt + "</p>", neu + "</p>", "text"))
    alt = einmal(H, r'<details class="mehr"><summary>[^<]*</summary>')
    R.append((alt, f'<details class="mehr" open><summary>{t["summary"]}</summary>', "text"))
    alt = einmal(H, r'<div class="tabs" id="gtabs">.*?</div>', re.S)
    R.append((alt, alt.replace('aria-pressed="true"', 'aria-pressed="X"').replace('aria-pressed="false" data-v="0,5"', 'aria-pressed="true" data-v="0,5"')
              .replace('aria-pressed="X"', 'aria-pressed="false"'), "roh"))
    R.append((einmal(H, re.escape("seg('gtabs',chart);chart('1,0');")), "seg('gtabs',chart);chart('0,5');", "roh"))
    # Sicherungen → sechs Spielregeln für die Teilnahme, dahinter das Rechenspiel
    a, b = abschnitt(H, "sicherungen")
    regeln = "".join(f"<div><span><b>{k.split(' · ', 1)[1]}</b><p>{p}</p></span></div>" for k, p in t["regeln"])   # Nummer setzt das Stylesheet
    neu_sich = (f'<section id="sicherungen">\n  <div class="wrap">\n    <h2>{t["regeln_h2"]}</h2>\n    <p class="lede">{t["regeln_lede"]}</p>\n'
                f'    <div class="sich">{regeln}</div>\n    {spiel(L)}\n  </div>\n</section>')
    R.append((H[a:b], neu_sich, "block"))
    # Klub → offene Gemeinschaft; „Wohin die Reise geht“ entfällt
    a, b = abschnitt(H, "klub")
    k0 = H.index("<h2>", a)
    k1 = H.index('<h3 class="sub-h">', a)
    t1 = H.index('<div class="timeline"', k1)
    k2 = H.index("</div>\n  </div>\n</section>", t1) + len("</div>")
    if not (k0 < k1 < k2 < b):
        raise SystemExit("Abschnitt klub: Aufbau unerwartet")
    stub = ('<div hidden><div id="raumvor"></div><div id="raum"></div><span id="raumsum"></span><span id="raumn"></span><i id="raumbar"></i>'
            '<span id="raumus"></span><p id="raumtext"></p></div>')
    kacheln = "".join(f"<div><h3>{x}</h3><p>{y}</p></div>" for x, y in t["verbindet"])
    herl = "".join(f"<div><h3>{x}</h3><p>{y}</p></div>" for x, y in t["herleitung"])
    lede = fertig(t["klub_lede"], mio_30=zahl(sum(MIO[c] for c in EUROPA), 1, L), n_teil=len(TEIL), n_partner=len(PARTNER))
    neu_klub = (f'<h2>{t["klub_h2"]}</h2>\n    <p class="lede">{lede}</p>\n    {stub}\n'
                f'    <h3 class="sub-h">{t["verbindet_h3"]}</h3>\n    <div class="effects">{kacheln}</div>\n'
                f'    <h3 class="sub-h">{t["herleitung_h3"]}</h3>\n    <p class="lede">{t["herleitung_lede"]}</p>\n    <div class="effects">{herl}</div>')
    R.append((H[k0:k1], neu_klub, "block"))
    R.append((H[k1:k2], "", "block"))
    R.append((einmal(H, re.escape("seg('ztabs',chart2);chart2('co2');")), "", "roh"))
    R.append(("</body></html>", spiel_js(L) + "</body></html>", "roh"))
    R.append(("</head>", CSS_SPIEL + "</head>", "roh"))
    return R


def spiel(L):
    t, nm = T[L], NAMEN[L]
    kat = {ISO3[c]: ("t" if c in TEIL else "p") for c in TEIL + PARTNER}
    titel = lambda c: esc(f"{nm[ISO2[c]]} · {zahl(MIO[c], 1, L)} {t['mio']}")
    pf, kr = [], []
    for k, v in KARTE["laender"].items():
        if k in VON3:
            c = VON3[k]
            pf.append(f'<path class="k-{kat[k]}" data-k="{c}" data-x="{v["x"]}" d="{v["d"]}"><title>{titel(c)}</title></path>')
        elif k in EUROPARAT:
            pf.append(f'<path class="k-e" d="{v["d"]}"><title>{esc(nm[EUROPARAT[k]])} · {t["eur_tip"]}</title></path>')
        else:
            pf.append(f'<path class="k-r" d="{v["d"]}"/>')
    for k, (x, y) in KARTE["kreise"].items():
        if k in VON3:
            c = VON3[k]
            kr.append(f'<circle class="k-{kat[k]}" data-k="{c}" data-x="{int(x)}" cx="{x}" cy="{y}" r="3.2"><title>{titel(c)}</title></circle>')
        elif k in EUROPARAT:
            kr.append(f'<circle class="k-e" cx="{x}" cy="{y}" r="2.2"><title>{esc(nm[EUROPARAT[k]])} · {t["eur_tip"]}</title></circle>')
    svg = (f'<svg id="gskarte" viewBox="0 0 {KARTE["breite"]} {KARTE["hoehe"]}" role="img" aria-label="{t["karte_label"]}">'
           + "".join(pf) + "".join(kr) + "</svg>")
    kz = lambda k, i, cls="v": f'<div class="res-row" style="flex:1;border:none"><span class="k">{t[k]}</span><span class="{cls}" id="{i}"></span></div>'
    return f'''<h3 class="sub-h">{t["spiel_h3"]}</h3>
    <p class="lede">{t["spiel_lede"]}</p>
    <div class="flow">
      <div class="tabs" id="gsvor"><button type="button" aria-pressed="false" data-v="regel">{t["tab_regel"]}</button><button type="button" aria-pressed="true" data-v="alle">{t["tab_partner"]}</button></div>
      <div class="gs-karte">{svg}</div>
      <div class="legend gs-leg"><span><i class="k-t"></i>{t["tab_regel"]}</span><span><i class="k-p"></i>{t["tab_partner"]}</span></div>
      <div class="row">{kz("k_menschen", "gssum", "v new")}{kz("k_staaten", "gsn")}{kz("k_welt", "gswelt")}</div>
      <div class="schwelle"><i id="gsbar"></i><span class="us" id="gsus"><span>{t["us"]}</span></span><span class="us" id="gseu"><span>{t["eu"]}</span></span></div>
      <p class="fineprint" id="gstext" style="margin-top:0"></p>
    </div>
    <p class="fineprint">{t["fine_karte"]}</p>'''


def spiel_js(L):
    t = T[L]
    d = dict(gs={c: [round(MIO[c], 1), "t" if c in TEIL else "p"] for c in TEIL + PARTNER}, us=round(MIO["US"], 1),
             eu=round(sum(MIO[c] for c in EU27), 1), welt=WELT, w=KARTE["breite"],
             vor=dict(regel=sorted(TEIL), alle=sorted(TEIL + PARTNER)), lang=L,
             t={k: t[k] for k in ("mio", "davon", "satz", "mehr", "weniger")})
    return """<script>(function(){const D=__D__;const $=id=>document.getElementById(id);const S=$('gskarte');
const ruhig=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
const f=(x,d)=>x.toLocaleString(D.lang,{minimumFractionDigits:d,maximumFractionDigits:d});const SK=1000;const auf=new Set();
const r=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(m,k)=>o[k]);const mio=x=>f(x,1)+'\\u00a0'+D.t.mio;
const el=k=>S.querySelectorAll('[data-k="'+k+'"]');
function lauf(){const on=[...auf];const sum=on.reduce((a,k)=>a+D.gs[k][0],0),p=on.filter(k=>D.gs[k][1]==='p').length;
 $('gssum').textContent=mio(sum);$('gsn').textContent=on.length+(p?' ('+r(D.t.davon,{p:p})+')':'');$('gswelt').textContent=f(sum/D.welt*100,1)+'\\u00a0%';
 $('gsbar').style.width=Math.min(sum/SK*100,100)+'%';$('gsus').style.left=(D.us/SK*100)+'%';$('gseu').style.left=(D.eu/SK*100)+'%';
 const v=sum>=D.us?r(D.t.mehr,{x:mio(sum-D.us)}):r(D.t.weniger,{x:mio(D.us-sum)});
 $('gstext').textContent=r(D.t.satz,{sum:mio(sum),n:on.length,diff:v});}
function setze(k,an,verz){el(k).forEach(n=>{n.style.transitionDelay=ruhig?'0ms':verz+'ms';n.classList.toggle('aus',!an);});an?auf.add(k):auf.delete(k);}
function vor(v){const s=new Set(D.vor[v]);Object.keys(D.gs).forEach(k=>{const x=+(el(k)[0]||{dataset:{x:0}}).dataset.x;setze(k,s.has(k),x/D.w*700);});
 document.querySelectorAll('#gsvor button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.v===v?'true':'false'));lauf();}
S.addEventListener('click',e=>{const n=e.target.closest('[data-k]');if(!n)return;const k=n.dataset.k;setze(k,!auf.has(k),0);
 document.querySelectorAll('#gsvor button').forEach(x=>x.setAttribute('aria-pressed','false'));lauf();});
$('gsvor').addEventListener('click',e=>{const b=e.target.closest('button');if(b)vor(b.dataset.v);});
Object.keys(D.gs).forEach(k=>setze(k,false,0));lauf();setTimeout(()=>vor('alle'),ruhig?0:350);})();</script>""".replace(
        "__D__", json.dumps(d, ensure_ascii=False))


CSS_SPIEL = ("<style>.gs-karte{background:#f3f7f4;border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:14px 0}"
             "#gskarte{width:100%;height:auto;display:block}#gskarte path,#gskarte circle{stroke:#fff;stroke-width:.4;transition:fill .5s ease}"
             "#gskarte .k-t{fill:#1d6b3a}#gskarte .k-p{fill:#4c9a5f}#gskarte .k-e{fill:#9fcca9}#gskarte .k-r{fill:#dcebdf}"
             "#gskarte .aus{fill:#dcebdf}#gskarte [data-k]{cursor:pointer}#gskarte [data-k]:hover{stroke:#0F3B5C;stroke-width:1}"
             ".gs-leg i{display:inline-block;width:14px;height:10px;margin-right:6px;border-radius:2px;vertical-align:middle}"
             ".gs-leg .k-t{background:#1d6b3a}.gs-leg .k-p{background:#4c9a5f}"
             "@media (prefers-reduced-motion:reduce){#gskarte path,#gskarte circle{transition:none}}"
             ".schwelle #gseu{border-left-color:var(--accent)}.schwelle #gseu span{top:-22px}</style>")
TOK = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<[^>]+>|[^<]+", re.S)


def markiere(h, cls, tag):
    return "".join(x if x.startswith("<") or not x.strip() else f'<{tag} class="{cls}">{x}</{tag}>' for x in TOK.findall(h))


def anwenden(H, R, kontrolle=False):
    for alt, neu, art in R:
        if art == "alle":
            if H.count(alt) < 1:
                raise SystemExit(f"Stelle nicht gefunden: {alt[:80]}")
            H = H.replace(alt, neu)
            continue
        if H.count(alt) != 1:
            raise SystemExit(f"Stelle {H.count(alt)}× gefunden: {alt[:80]}")
        if kontrolle and art == "text":
            neu = markiere(alt, "k-weg", "del") + markiere(neu, "k-neu", "ins")
        elif kontrolle and art == "block":
            neu = '<div class="k-block-weg">' + markiere(alt, "k-weg", "del") + "</div>" + markiere(neu, "k-neu", "ins")
        H = H.replace(alt, neu)
    return H


for L in SPRACHEN:
    alt = (ZIEL / f"{L}.html").read_text(encoding="utf-8")
    R = paare(alt, L)
    neu = anwenden(alt, R).replace("<head>", "<head>" + MARKE, 1)
    (ZIEL / f"{L}.html").write_text(neu, encoding="utf-8")
    if L == "de":
        K = anwenden(alt, R, kontrolle=True)
        css = ("<style>ins.k-neu{background:#c8ecc9;color:#0b3d12;text-decoration:none}del.k-weg{background:#f6c6c0;color:#5a1a12}"
               ".k-block-weg{outline:3px solid #e8a39a;margin-bottom:28px;opacity:.85}"
               "#k-hinweis{position:sticky;top:0;z-index:9999;background:#0F3B5C;color:#fff;font:14px/1.45 system-ui,sans-serif;padding:8px 16px}"
               "#k-hinweis ins{background:#c8ecc9;color:#0b3d12;text-decoration:none}#k-hinweis del{background:#f6c6c0;color:#5a1a12}</style>")
        hinweis = ('<div id="k-hinweis">Kontrollfassung (v4.80): deutsche Seite nach den Spielregeln gegen die Fassung v4.79. '
                   '<ins>grün = neu</ins> · <del>rot = entfällt</del>. Fonds- und Kassenzahlen vorläufig (noch nicht in den Haushaltsrechnungen).</div>')
        K = re.sub(r"(<body[^>]*>)", r"\1" + hinweis, K.replace("</head>", css + "</head>", 1), count=1)
        ziel = W / "seite" / "entwurf" / "gemeinschaft"
        ziel.mkdir(parents=True, exist_ok=True)
        (ziel / "de-kontrolle.html").write_text(K, encoding="utf-8")
    print(f"{L}: {len(R)} Stellen umgeformt")
