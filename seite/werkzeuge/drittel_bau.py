#!/usr/bin/env python3
"""Webseite Fassung 4.0 „Das Goldene Drittel" in sechs Sprachen (Logbuch v4.0; entstanden als Entwurf v3.55–v3.58).

Grundsatz (Auftrag der Initiative, 17.10.2026): eng am Vorbild der Seite zum Stand B bleiben, nur geänderte Inhalte, Zahlen und Begriffe tauschen.
Technik: Vorlage (vorlage.html), Stylesheet und unveränderte Texte (sprachen/{sp}.json) aus seite_bau.py; dieser Baustein überschreibt
  - Texte, deren Inhalt sich geändert hat (drittel_texte.py, sechs Sprachen),
  - die Zahlen der Gesamtrechnung 28:28 durch die Ergebnisse der Drittel-Rechnungen (netz33, projektion33, dynamik33, altlasten,
    moeglichkeitsraum33, systemvarianten, haushalte33),
  - wenige Stellen der Vorlage (Wortmarke, Label-Stufen, viertes Segment „starkes Netz", Rechner, Schuldengrafik, Dokumente, Kontakt).
Ausgabe: seite/stand-c/{de,en,fr,it,es,pl}.html. Upload-Paket: seite/werkzeuge/paket_bau.py.
"""
import importlib.util
import json
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
AGG = WURZEL / "daten" / "aggregate"
ZIEL = WURZEL / "seite" / "stand-c"
VERSION = "v4.0"
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

# ---- Geänderte Texte: seite/werkzeuge/drittel_texte.py (sechs Sprachen, «…»-Platzhalter hier sprachgerecht gefüllt)
spec_t = importlib.util.spec_from_file_location("drittel_texte", Path(__file__).resolve().parent / "drittel_texte.py")
TT = importlib.util.module_from_spec(spec_t)
spec_t.loader.exec_module(TT)
SPRACHEN = list(TT.TEXTE)
# v3.58: Mehrheitsaussage „9 von 10 Beschäftigten" nur, solange die Rechnung sie deckt (haushalte33, je Haushaltstyp)
_ANT = min(v for k, v in H["anteil_erwachsene_mit_mehr"].items() if k.startswith("beschluss|"))
assert _ANT >= 90, f"Aussage 9 von 10 nicht gedeckt: {_ANT} %"


def werte_neu(sp):
    E = lambda x, nk=0: SB.eur(x, sp, nk)
    P = lambda x, nk=0: SB.pct(x, sp, nk)
    return {"p33": P(33), "plus42": "+" + E(plus42), "zu": P(ZU, 1), "e0": E(0), "e100k": E(100000),
            "staaten": str(RM["staaten"]), "einw": SB.zahl(RM["einwohner_mio"], 1, sp)}


def texte(sp):
    w = werte_neu(sp)
    out = {}
    for k, v in TT.TEXTE[sp].items():
        for n, x in w.items():
            v = v.replace("«" + n + "»", x)
        if "«" in v:
            raise SystemExit(f"{sp}/{k}: Platzhalter ohne Wert: {v}")
        out[k] = v
    return out


KONTAKT_ALT, KONTAKT_NEU = "2828@archicrowd.de", "tax.better@archicrowd.de"   # v3.57: neue Kontaktadresse, Links und Impressum

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
    ('<svg class="hero-mark" viewBox="0 0 560 300" role="img" aria-label="TAX 28:28">', '<svg class="hero-mark" viewBox="0 0 560 @@MARKE_H@@" role="img" aria-label="@@MARKE_NAME@@">'),
    ('<text x="60" y="168" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="196" fill="#0F3B5C" textLength="440" lengthAdjust="spacing">TAX</text>',
     '@@MARKE_ZEILEN@@'),
    ('<text x="60" y="286" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C" letter-spacing="-2" textLength="440" lengthAdjust="spacing">28:28</text>',
     ''),
    ('<a class="tb-left" href="#top">TAX 28:28</a>', '<a class="tb-left" href="#top">@@MARKE_NAME@@</a>'),
    # v3.56: Rechner mit Zeitstrahl und „mehr im Geldbeutel" statt Einkommensteuer
    ('<input type="range" id="brutto" min="0" max="150000" step="1000" value="42000">', '<input type="range" id="brutto" min="10000" max="150000" step="1000" value="42000">'),
    ('<div class="seg" id="rj"><button type="button" aria-pressed="true" data-v="2028">2028</button><button type="button" aria-pressed="false" data-v="2035">2035</button><button type="button" aria-pressed="false" data-v="2045">2045</button><button type="button" aria-pressed="false" data-v="2060">2060</button></div>',
     '<div class="bigval" id="rjval">2028</div><input type="range" id="rj" min="2028" max="2060" step="1" value="2028" style="width:100%;accent-color:var(--ink)" aria-label="@@rech_jahr@@">'),
    (RECHNER_ALT, RECHNER_NEU),
    ('<div><b class="v4">C · 22&nbsp;%</b>', '<div><b class="v4">C · 25&nbsp;%</b>'),
    ('<div><b class="v5">D · 28&nbsp;%</b>', '<div><b class="v5" style="background:#5b1a14">S · 33&nbsp;%</b>'),
    ('<i class="sb" id="sb"></i>', '<i class="sb" id="sb"></i><i class="sn" id="sn" style="background:#8FB8A0"></i>'),
    ('<span><b style="background:#6497B8"></b>@@fluss_l2@@</span>', '<span><b style="background:#6497B8"></b>@@fluss_l2@@</span><span><b style="background:#8FB8A0"></b>@@NETZ_NAME@@</span>'),
    ("function fluss(){const j=+$('jahr').value,i=idx(j);const a=D.a[i]/D.q*100,b=D.b/D.q*100,d=D.div[i]/D.q*100,c=D.og*D.einzugAnteil;",
     "function fluss(){const j=+$('jahr').value,i=idx(j);const q=D.qj[i],a=D.a[i]/q*100,b=D.bj[i]/q*100,n=D.n[i]/q*100,d=D.div[i]/q*100,c=D.og*D.einzugAnteil;"),
    ("[['sa',a],['sb',b],['sd',d]]", "[['sa',a],['sb',b],['sn',n],['sd',d]]"),
    ("fill(T.js_fluss,{j:j,a:eur(a),cap:eur(c),b:eur(b),d:eur(d),hundert:eur(100)})", "fill(T.js_fluss,{j:j,a:eur(a),cap:eur(c),b:eur(b),n:eur(n),d:eur(d),hundert:eur(100)})"),
    ("['mit',D.jahre,D.d]];lo=20;hi=100;step=20;", "['mit',D.jahre,D.d]];lo=0;hi=180;step=30;"),
    ('aria-pressed="false" data-v="0,5">@@zeit_t1@@', 'aria-pressed="true" data-v="1,0">@@zeit_t1@@'),
    ('aria-pressed="true" data-v="1,0">@@zeit_t2@@', 'aria-pressed="false" data-v="0,5">@@zeit_t2@@'),
    # v4.0: Dokumente des Drittel-Systems statt Gesamtkonzept und Kurzfassung 28:28
    ('dokumente/TAX-2828-Gesamtkonzept.pdf', 'dokumente/TAX-Drittel-Konzept.pdf'),
    ('dokumente/TAX-2828-Kurzfassung.pdf', 'dokumente/TAX-Drittel-Kurzfassung.pdf'),
]


def marke(sp):
    z = TT.MARKE[sp]
    h = 130 * len(z)
    zeilen = "".join(f'<text x="280" y="{112 + 130 * i}" text-anchor="middle" font-family="Space Grotesk,sans-serif" font-weight="700" '
                     f'font-size="116" fill="#0F3B5C">{t}</text>' for i, t in enumerate(z))
    return {"MARKE_H": str(h), "MARKE_ZEILEN": zeilen, "MARKE_NAME": TT.NAME[sp], "NETZ_NAME": TT.NETZ[sp]}


def main():
    vorlage = SB.VORLAGE
    for a, b in ERSETZE:
        if vorlage.count(a) < 1:
            raise SystemExit(f"Vorlage: Stelle nicht gefunden: {a[:70]}")
        vorlage = vorlage.replace(a, b)
    rr = json.loads((WURZEL / "daten/aggregate/haushalte33_raster.json").read_text(encoding="utf-8"))["rechner"]
    extra = dict(rr=rr, qj=[round(deck[j], 3) for j in JAHRE], bj=[round(gem[j], 3) for j in JAHRE], n=[NB[j]["netz_pct_bip"] for j in JAHRE])
    ZIEL.mkdir(parents=True, exist_ok=True)
    for sp in SPRACHEN:
        m = marke(sp)
        SB.VORLAGE = re.sub(r"@@(MARKE_H|MARKE_ZEILEN|MARKE_NAME|NETZ_NAME)@@", lambda x: m[x.group(1)], vorlage)
        T = json.loads((SB.SPRACHEN_DIR / f"{sp}.json").read_text(encoding="utf-8"))
        TX = texte(sp)
        fehlt = set(TX) - set(T)
        if fehlt:
            raise SystemExit(f"{sp}: unbekannte Schlüssel: {sorted(fehlt)}")
        T.update(TX)
        W = SB.werte(sp)
        W.update(version=VERSION, fassung=TT.FASSUNG[sp])
        html = SB.baue(sp, T, W)
        html = html.replace("\nconst T=D.T;", "\nObject.assign(D," + json.dumps(extra) + ");\nconst T=D.T;", 1)
        html = html.replace(KONTAKT_ALT, KONTAKT_NEU).replace("?subject=28%3A28", "?subject=" + TT.NAME[sp].replace(" ", "%20").replace("'", "%27"))
        # Einwohnerzahlen der Klub-Kacheln mit Einheit, zweizeilig
        html, k = re.subn(r'(<span class="nm">[^<]*</span><span>)([\d.,\s\u00a0]+)(</span></button>)', r"\1\2 " + TT.MIO[sp] + r"\3", html)
        assert k >= 30, (sp, k)
        html = html.replace("</style>", "#raum button{display:block;text-align:left}#raum button span{display:block}"
                                        "#raum button span:last-child{text-align:right;white-space:nowrap}</style>", 1)
        for alt in ("TAX 28:28", "28%3A28"):
            if alt in html:
                raise SystemExit(f"{sp}: Restbestand {alt!r} in der Seite")
        (ZIEL / f"{sp}.html").write_text(html, encoding="utf-8")
        print(f"geschrieben: {(ZIEL / f'{sp}.html').relative_to(WURZEL)} ({len(html)} Zeichen)")


if __name__ == "__main__":
    main()
