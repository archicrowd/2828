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
VERSION = "v4.1"
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


spec_l = importlib.util.spec_from_file_location("laender_texte", Path(__file__).resolve().parent / "laender_texte.py")
LT = importlib.util.module_from_spec(spec_l)
spec_l.loader.exec_module(LT)
LS, HL, ZR = lade("laenderseiten.json"), lade("heute_laender.json"), lade("laender_zeitreihen.json")
HT = __import__("tomllib").loads((WURZEL / "modell" / "heute_laender.toml").read_text(encoding="utf-8"))
FX = {"PL": HT["waehrung"]["PL"]}
J_DE = dict(J)


def land_j(c):
    """SB.J für das Referenzland c (Zahlen in Landeswährung)."""
    if c == "DE":
        return dict(J_DE)
    fx, L = FX.get(c, 1.0), LS["staaten"][c]
    de = LS["staaten"]["DE"]["dividende_erw_eur"]
    r = [x / y * fx for x, y in zip(L["dividende_erw_eur"], de)]
    j = dict(J_DE)
    j["reihe_erw"] = {k: [round(v * f, 1) for v, f in zip(J_DE["reihe_erw"][k], r)] for k in J_DE["reihe_erw"]}
    j["erw_de_2028"], j["erw_de_2060"] = j["reihe_erw"]["1,0"][0], j["reihe_erw"]["1,0"][-1]
    j["kind_de_2028"] = j["erw_de_2028"] / 2
    j["reihe_div"] = L["dividende_pct_bip"]
    j["gemeinde_einw_de"], j["gemeinde_kind_de"] = L["gemeinde_einw"] * fx, L["gemeinde_kind"] * fx
    j["formel_einw"], j["formel_kind"] = J_DE["formel_einw"] * fx, J_DE["formel_kind"] * fx
    j["f_de"] = L["f_kopf"] * fx
    if "fonds" in L:
        pf = {2028: L["fonds"]["start_2028"], **{int(k): v for k, v in L["fonds"]["pfad"].items()}}
        j["reihe_d"] = [pf[x] for x in JAHRE]
    return j


def zeitreihen(c):
    z = dict(SB.ZEITREIHEN_DE)
    if c in ZR["schuld"]:
        z.update(schuld_hist_jahre=ZR["schuld_jahre"], schuld_hist=ZR["schuld"][c], schuld_prog_jahre=ZR["schuld_prog_jahre"], schuld_prog=ZR["schuld_prog"][c])
    k = "EU27" if c == "EU30" else c
    if k in ZR["thg"] and c != "DE":
        z.update(co2_hist_jahre=ZR["thg_jahre"], co2_hist=[round(x, 1) for x in ZR["thg"][k]], co2_ziel_jahre=ZR["thg_ziel"][k]["jahre"],
                 co2_ziel=ZR["thg_ziel"][k]["werte"])
    return z


def werte_neu(sp, c):
    fx = FX.get(c, 1.0)
    E = lambda x, nk=0: SB.eur(x, sp, nk)
    P = lambda x, nk=0: SB.pct(x, sp, nk)
    w = {"p33": P(33), "e0": E(0), "e100k": E(100000 * fx), "e2m": E(2e6 * fx), "staaten": str(RM["staaten"]), "einw": SB.zahl(RM["einwohner_mio"], 1, sp)}
    if c == "DE":
        w.update(plus="+" + E(plus42), bsp=E(42000), zu=P(ZU, 1))
    elif c in HL["staaten"]:
        h = HL["staaten"][c]
        f = LS["staaten"][c]["fonds"]
        w.update(plus="+" + E(h["beispiel"]["plus_monat"]), bsp=E(h["beispiel"]["brutto"]), zu=P(f["zuschlag_pct"], 1), spitze=P(f["spitze"]),
                 sjahr=str(f["spitzenjahr"]), plus_aw="+" + E(h["beispiel_aw"]["plus_monat"]).replace("+-", "−"), aw=E(h["beispiel_aw"]["brutto"]),
                 keil=P(HT["oecd"]["keil"][c], 1), anteil=LT.ANTEIL_TXT.get(sp, "{a}–{b}").format(a=round(h["anteil_min"] / 10), b=round(h["anteil_max"] / 10)))
    else:
        fr = HL["staaten"]["FR"]
        w.update(fr_anteil=LT.ANTEIL_TXT.get(sp, "{a}–{b}").format(a=round(fr["anteil_min"] / 10), b=round(fr["anteil_max"] / 10)), zu=P(ZU, 1))
    k = "EU27" if c == "EU30" else c
    if k in ZR["thg_1990"]:
        w["thg_minus"] = LT.THG[sp].format(p=P(round(100 * (1 - ZR["thg"][k][-1] / ZR["thg_1990"][k]))))
        w["thg_spitze"] = LT.THG_SPITZE.get(sp, "{p}").format(p=P(round(100 * (1 - ZR["thg"][k][-1] / 444.09022))))   # nur ES: Höchststand 2007
    return w


def texte(sp, c):
    w = werte_neu(sp, c)
    quelle = dict(TT.TEXTE[sp])
    alt, neu = LT.DIV_SATZ[sp]
    assert alt in quelle["div_p1"], (sp, "div_p1")
    quelle["div_p1"] = quelle["div_p1"].replace(alt, neu)
    quelle.update(LT.LAND.get(sp, {}))
    anteil = HL["staaten"][c]["anteil_min"] if c in HL["staaten"] else _ANT
    if c == "EU30" or anteil >= 90:
        quelle["stamp3_val"], quelle["stamp3_lbl"] = LT.STAMP_A[sp]
        quelle["hero_fein"] = LT.FEIN_A[sp]
    else:
        quelle["stamp3_val"], quelle["stamp3_lbl"] = LT.STAMP_B[sp]
        quelle["hero_fein"] = LT.FEIN_B[sp]
    quelle["hero_fein"] = quelle["hero_fein"]
    out = {}
    for k, v in quelle.items():
        for n, x in w.items():
            v = v.replace("«" + n + "»", x)
        if re.search(r"«[a-z0-9_]+»", v):
            raise SystemExit(f"{sp}/{k}: Platzhalter ohne Wert: {v}")
        out[k] = v
    return out


def rr_de():
    """Rechner-Raster Deutschland im einheitlichen Format (heute und Arbeitgeberbeiträge je Beitragsregime)."""
    r = json.loads((AGG / "haushalte33_raster.json").read_text(encoding="utf-8"))["rechner"]
    ag = {reg: [round(c[0] * min(b, r["bbg_kv"]) + c[1] * min(b, r["bbg_rv"]), 1) for b in r["brutto"]] for reg, c in r["beitrag"].items()}
    return dict(brutto=r["brutto"], schritt=1000, start=42000, heute=r["heute"], ag=ag, jahre=r["jahre"], div=r["div"], eff=r["eff"],
                stufen=r["stufen"], saetze=r["saetze"], eff_alt=r["eff_alt"], weitergabe=r["weitergabe"], zuschlag=r["zuschlag"],
                vorsorge=r["vorsorge"], kq=r["kq"])


def rr_land(c, in_eur=False):
    h = HL["staaten"][c]
    r = h["raster"]
    f = 1 / FX.get(c, 1.0) if in_eur else 1.0
    m = lambda xs: [round(x * f, 2) for x in xs]
    heute = {}
    for reg in ("2028", "2035"):
        for k, v in r["heute"].items():
            heute[f"{reg}|{k}"] = m(v)
    return dict(brutto=m(r["brutto"]), schritt=r["schritt"] * f, start=round(h["beispiel"]["brutto"] * f, 2), heute=heute,
                ag={"2028": m(r["ag"]), "2035": m(r["ag"])}, jahre=r["jahre"], div=m(r["div"]), eff=r["eff"], stufen=m(r["stufen"]),
                saetze=r["saetze"], eff_alt=r["eff_alt"], weitergabe=r["weitergabe"], zuschlag=r["zuschlag"], vorsorge=r["vorsorge"],
                kq=[[x * f, y] for x, y in r["kq"]])


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
RECHNER_NEU = """let R=D.rr;
function estR(x){let s=0,u=0;const g=R.stufen.concat([Infinity]);for(let i=0;i<g.length;i++){if(x>u)s+=(Math.min(x,g[i])-u)*R.saetze[i]/100;u=g[i];}return s;}
function kqR(n){const p=R.kq;if(n<=p[0][0])return p[0][1];for(let i=1;i<p.length;i++){if(n<=p[i][0]){const a=p[i-1][0],x=p[i-1][1],b=p[i][0],y=p[i][1];return x+(y-x)*(n-a)/(b-a);}}return p[p.length-1][1];}
function neuR(i,b,e,k,j){const t=R.jahre.indexOf(j),DIV=R.div[t]*12,EFF=R.eff[t],reg=j>=2035?'2035':'2028';
  const brutto=b+R.weitergabe*R.ag[reg][i],st=estR(brutto+DIV)+(e-1)*estR(DIV),div=DIV*e+k*DIV/2,netto=brutto-st+div;
  const konsum=kqR(netto)*netto,mm=konsum*((1+EFF/100)/(1+R.eff_alt/100)-1),mb=konsum*EFF/(100+EFF);
  return {netto:netto-mm-R.zuschlag/100*(st+mb)-R.vorsorge*b,div:div};}
function rset(){const s=$('brutto');s.min=R.brutto[0];s.max=R.brutto[R.brutto.length-1];s.step=R.schritt;s.value=R.start;}
function rechner(){const i=Math.max(0,Math.min(R.brutto.length-1,Math.round((+$('brutto').value-R.brutto[0])/R.schritt))),br=R.brutto[i],e=+val('erw'),k=+val('kin'),j=+$('rj').value;
  const reg=j>=2035?'2035':'2028',h=R.heute[reg+'|'+e+'|'+k][i],n=neuR(i,br,e,k,j),d=n.netto-h;
  const sg=x=>(x>=0?'+':'−')+eur(Math.abs(x));
  $('bruttoval').textContent=eur(br);$('rjval').textContent=j;
  $('r-st').textContent=eur(h/12);$('r-satz').textContent=eur(n.netto/12);$('r-soz').textContent=eur(n.div/12);$('r-mon').textContent=sg(d);
  const hh=fill(e>1?T.js_erw_n:T.js_erw_1,{n:e})+(k?T.js_und+fill(k>1?T.js_kind_n:T.js_kind_1,{n:k}):'');
  $('r-jahr').textContent=sg(d/12);$('r-jahrsub').textContent=fill(T.js_rechner_sub,{j:j,hh:hh});
  const m=Math.max(h,n.netto,1);$('bi-st').style.width=h/m*100+'%';$('bi-dv').style.width=n.netto/m*100+'%';
  $('b-st').textContent=eur(h/12);$('b-dv').textContent=eur(n.netto/12);}
if(D.rrs){seg('rland',()=>{R=D.rrs[val('rland')];rset();rechner();});}
rset();$('brutto').addEventListener('input',rechner);$('rj').addEventListener('input',rechner);['erw','kin'].forEach(x=>seg(x,rechner));rechner();"""

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
    ("['mit',D.jahre,D.d]];lo=20;hi=100;step=20;", "['mit',D.jahre,D.d]];lo=0;[hi,step]=nice(Math.max(...Z.schuld_hist,...Z.schuld_prog,...D.d));"),
    ("lo=0;hi=1000;step=200;x1=2045;", "lo=0;[hi,step]=nice(Math.max(...Z.co2_hist));x1=Math.max(...Z.co2_ziel_jahre);"),
    ("// Wohin die Reise geht\n", "// Wohin die Reise geht\nfunction nice(m){const p=Math.pow(10,Math.floor(Math.log10(m)));const st=[1,2,2.5,3,5,10].map(k=>k*p/5*5/5).map(x=>x).find(x=>m/x<=6.5)||p*2;return [Math.ceil(m/st)*st,st];}\n"),
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
    SB.ZEITREIHEN_DE = dict(SB.ZEITREIHEN)
    eur_orig = SB.eur
    ZIEL.mkdir(parents=True, exist_ok=True)
    for sp in SPRACHEN:
        c = LT.REFERENZ[sp]
        fx = FX.get(c, 1.0)
        SB.J = land_j(c)
        L = LS["staaten"][c]
        SB.TARIF = [(g * fx, s) for g, s in zip(L["tarif_stufen"], V["einkommen_saetze"][:4])] + [(None, V["einkommen_saetze"][-1])]
        SB.ZEITREIHEN = zeitreihen(c)
        SB.eur = (lambda x, s_, nk=0: f"{SB.zahl(x, nk, s_)} zł") if c == "PL" else eur_orig
        m = marke(sp)
        v = re.sub(r"@@(MARKE_H|MARKE_ZEILEN|MARKE_NAME|NETZ_NAME)@@", lambda x: m[x.group(1)], vorlage)
        if c == "EU30":   # Rechner: Land wählen
            knoepfe = "".join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-v="{k}">{n}</button>' for i, (k, n) in enumerate(LT.EN_LAENDER))
            v = v.replace('<label class="lbl" for="brutto">', f'<label class="lbl">{LT.EN_LAND_LABEL}</label><div class="seg" id="rland">{knoepfe}</div>'
                                                             f'<label class="lbl" for="brutto">', 1)
        SB.VORLAGE = v
        T = json.loads((SB.SPRACHEN_DIR / f"{sp}.json").read_text(encoding="utf-8"))
        TX = texte(sp, c)
        fehlt = set(TX) - set(T)
        if fehlt:
            raise SystemExit(f"{sp}: unbekannte Schlüssel: {sorted(fehlt)}")
        T.update(TX)
        W = SB.werte(sp)
        W.update(version=VERSION, fassung=TT.FASSUNG[sp])
        html = SB.baue(sp, T, W)
        # Geldfluss je Land: Dach und Gemeinde nach Regel gleich, Netz und Dividende des Landes; Summe angepasst
        n_c = [NB[j]["netz_pct_bip"] for j in JAHRE] if c == "DE" else L["netz_pct_bip"]
        d_c = [NB[j]["dividende_pct_bip"] for j in JAHRE] if c == "DE" else L["dividende_pct_bip"]
        qj = [round(deck[j] + (n_c[i] - NB[j]["netz_pct_bip"]) + (d_c[i] - NB[j]["dividende_pct_bip"]), 3) for i, j in enumerate(JAHRE)]
        extra = dict(qj=qj, bj=[round(gem[j], 3) for j in JAHRE], n=n_c)
        if c == "DE":
            extra["rr"] = rr_de()
        elif c == "EU30":
            extra["rrs"] = {"DE": rr_de(), **{k: rr_land(k, in_eur=True) for k, _ in LT.EN_LAENDER if k != "DE"}}
            extra["rr"] = extra["rrs"]["DE"]
        else:
            extra["rr"] = rr_land(c)
        html = html.replace("\nconst T=D.T;", "\nObject.assign(D," + json.dumps(extra) + ");\nconst T=D.T;", 1)
        if c == "PL":
            js_alt = "const eur=(x,nk=0)=>EURPOS==='vor'?'€'+zahl(x,nk):zahl(x,nk)+'\u00a0€';"
            assert js_alt in html
            html = html.replace(js_alt, "const eur=(x,nk=0)=>zahl(x,nk)+'\u00a0zł';")
        html = html.replace(KONTAKT_ALT, KONTAKT_NEU).replace("?subject=28%3A28", "?subject=" + TT.NAME[sp].replace(" ", "%20").replace("'", "%27"))
        html, k = re.subn(r'(<span class="nm">[^<]*</span><span>)([\d.,\s\u00a0]+)(</span></button>)', r"\1\2 " + TT.MIO[sp] + r"\3", html)
        assert k >= 30, (sp, k)
        html = html.replace("</style>", "#raum button{display:block;text-align:left}#raum button span{display:block}"
                                        "#raum button span:last-child{text-align:right;white-space:nowrap}</style>", 1)
        for alt in ("TAX 28:28", "28%3A28"):
            if alt in html:
                raise SystemExit(f"{sp}: Restbestand {alt!r} in der Seite")
        (ZIEL / f"{sp}.html").write_text(html, encoding="utf-8")
        print(f"geschrieben: {(ZIEL / f'{sp}.html').relative_to(WURZEL)} ({len(html)} Zeichen), Referenz {c}")
    SB.eur = eur_orig


if __name__ == "__main__":
    main()
