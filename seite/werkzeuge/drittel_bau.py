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
VERSION = "v4.78"
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
    return [(NB[j]["dividende_erw_eur2026"] + interp(diff, j)) * VB.TOPF for j in JAHRE]


# v4.8: Regelwerte (Kinderanteil 0,8, Boden, Gini) aus dem Modell
spec_v = importlib.util.spec_from_file_location("v48_bau", Path(__file__).resolve().parent / "v48_bau.py")
VB = importlib.util.module_from_spec(spec_v)
spec_v.loader.exec_module(VB)
spec_vt = importlib.util.spec_from_file_location("v48_texte", Path(__file__).resolve().parent / "v48_texte.py")
VT = importlib.util.module_from_spec(spec_vt)
spec_vt.loader.exec_module(VT)

# ---- Zahlen der Gesamtrechnung durch die Drittel-Rechnung ersetzen
J = dict(SB.J)
basis = [NB[j]["dividende_erw_eur2026"] * VB.TOPF for j in JAHRE]   # v4.8: Topf bei Kinderanteil 0,8 (R1)
J["reihe_jahre"] = JAHRE
J["reihe_erw"] = {"1,0": basis, "0,5": dyn_reihe(2.8, 0.3, 0.0), "1,5": dyn_reihe(4.6, 0.6, 3.0)}   # Schlüssel der Vorlage: 1,0 = Grundpfad (Rechner, Spark)
J["erw_de_2028"], J["erw_de_2060"], J["kind_de_2028"] = basis[0], basis[-1], basis[0] * VB.S_KIND
deck = {j: PR[j]["deckung"] + PR[j]["progression"] for j in JAHRE}
gem = {j: V["quote_kern"] - PR[j]["dach_ohne_zins"] - PR[j]["dividende_ohne_trends_pct_bip"] for j in JAHRE}
J["reihe_a"] = [PR[j]["dach_ohne_zins"] for j in JAHRE]
J["reihe_div"] = [NB[j]["dividende_pct_bip"] for j in JAHRE]
J["b_fach"] = gem[2028]
J["quote"] = V["deckung"]
FGJ = json.loads((Path(__file__).resolve().parent.parent.parent / "daten" / "aggregate" / "fonds_geltend.json").read_text(encoding="utf-8"))   # v4.20
sq = {2028: SB.J["schuldenquote_2028"], **{int(k): v for k, v in FGJ["schuldenquote"].items()},
      FGJ["spitzenjahr"]: FGJ["schuldenquote_spitze"]}  # Spitze mitführen, sonst glättet die Interpolation sie weg
J["reihe_d"] = [round(interp(sq, j), 2) for j in JAHRE]
SB.J = J
SB.TARIF = [(G26 * x, s) for x, s in zip((1, 1.5, 2, 3), V["einkommen_saetze"][:4])] + [(None, V["einkommen_saetze"][-1])]

fall = lambda zu: next(f for f in H["faelle"] if f["jahr"] == 2028 and f["haushalt"] == "alleinstehend" and f["weitergabe_ag"] == 0.8
                       and f["vorsorge_satz"] == 0.1 and f["zuschlag_pct"] == zu)
ZU = max(f["zuschlag_pct"] for f in H["faelle"])
plus42 = VB.plus_monat("DE", 42000)   # v4.8: Regel Boden, Kinderanteil 0,8 (vorher haushalte33)
AB = FGJ   # v4.20: geltender Fonds der 30 Staaten
RM = MR["raum"]
FZ = json.loads((Path(__file__).resolve().parent.parent.parent / "daten" / "aggregate" / "fondszins.json").read_text(encoding="utf-8"))   # v4.19

# ---- Geänderte Texte: seite/werkzeuge/drittel_texte.py (sechs Sprachen, «…»-Platzhalter hier sprachgerecht gefüllt)
spec_t = importlib.util.spec_from_file_location("drittel_texte", Path(__file__).resolve().parent / "drittel_texte.py")
TT = importlib.util.module_from_spec(spec_t)
spec_t.loader.exec_module(TT)
SPRACHEN = list(TT.TEXTE)
# v3.58: Mehrheitsaussage „9 von 10 Beschäftigten" nur, solange die Rechnung sie deckt (haushalte33, je Haushaltstyp)
_ANT = min(v for k, v in H["anteil_erwachsene_mit_mehr"].items() if k.startswith("beschluss|"))
assert _ANT >= 90, f"Aussage 9 von 10 nicht gedeckt: {_ANT} %"


_spec_s = importlib.util.spec_from_file_location("stand_texte", Path(__file__).resolve().parent / "stand_texte.py")   # v4.55
ST = importlib.util.module_from_spec(_spec_s)
_spec_s.loader.exec_module(ST)
_spec_k = importlib.util.spec_from_file_location("kommunen_texte", Path(__file__).resolve().parent / "kommunen_texte.py")   # v4.45
KT = importlib.util.module_from_spec(_spec_k)
_spec_k.loader.exec_module(KT)
spec_l = importlib.util.spec_from_file_location("laender_texte", Path(__file__).resolve().parent / "laender_texte.py")
LT = importlib.util.module_from_spec(spec_l)
spec_l.loader.exec_module(LT)
LT.FEIN_B["fr"], LT.FEIN_A["en"] = VT.FEIN_B_FR, VT.FEIN_A_EN   # v4.8
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
    j["kind_de_2028"] = j["erw_de_2028"] * VB.S_KIND
    j["reihe_div"] = L["dividende_pct_bip"]
    j["gemeinde_einw_de"], j["gemeinde_kind_de"] = L["gemeinde_einw"] * fx, L["gemeinde_kind"] * fx
    j["formel_einw"], j["formel_kind"] = J_DE["formel_einw"] * fx, J_DE["formel_kind"] * fx
    j["f_de"] = L["f_kopf"] * fx
    if "pfad" in L.get("fonds", {}):
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


ZU_VERR = {  # v4.38 (E11): Zuschlag des Staates 2028, Angleichung an den gemeinsamen Satz bis 2058
    "de": " (2028; bis 2058 Angleichung an den gemeinsamen Satz von {zg})", "en": " (2028; converging to the common rate of {zg} by 2058)",
    "fr": " (2028 ; convergence vers le taux commun de {zg} d'ici 2058)", "it": " (2028; convergenza verso l'aliquota comune del {zg} entro il 2058)",
    "es": " (2028; convergencia hacia el tipo común del {zg} hasta 2058)", "pl": " (2028; do 2058 r. zbieżność do wspólnej stawki {zg})"}


def werte_neu(sp, c):
    fx = FX.get(c, 1.0)
    E = lambda x, nk=0: SB.eur(x, sp, nk)
    P = lambda x, nk=0: SB.pct(x, sp, nk)
    fzm = [v["zuschlag_pct"] for v in FZ["varianten"] if v["fall"] in ("fest 3.5 %", "fest 4.0 %")]   # v4.19: Marktzins Oktober 2026
    w = {"zins_fonds": P(FGJ["zins"], 2), "zu_markt": P(min(fzm), 1) + "–" + P(max(fzm), 1), "p33": P(33), "e0": E(0), "e100k": E(100000 * fx), "e2m": E(2e6 * fx), "staaten": str(RM["staaten"]), "einw": SB.zahl(RM["einwohner_mio"], 1, sp)}
    zg = P(FGJ["zuschlag_auf_alle_steuern_pct"], 1)                          # v4.38 (E11): gemeinsamer Satz, Ziel der Verrechnung
    w["zu_verr"] = ZU_VERR[sp].format(zg=zg) if FGJ.get("zuschlag_haushalte", {}).get("aktiv") else ""
    if c == "DE":
        w.update(plus="+" + E(plus42), bsp=E(42000), zu=P(ZU, 1))
    elif c in HL["staaten"]:
        h = HL["staaten"][c]
        f = LS["staaten"][c]["fonds"]
        fe = LS["staaten"][c]["fonds_eigen"]
        amin, amax = VB.anteil(c)
        pa = VB.plus_monat(c, h["beispiel_aw"]["brutto"])
        w.update(plus="+" + E(VB.plus_monat(c, h["beispiel"]["brutto"])), bsp=E(h["beispiel"]["brutto"]), zu=P(f["zuschlag_pct"], 1), spitze=P(f["spitze"]),
                 sjahr=str(f["spitzenjahr"]), zu_eigen=P(fe["zuschlag_pct"], 1), plus_aw=("+" if pa >= 0 else "−") + E(abs(pa)), aw=E(h["beispiel_aw"]["brutto"]),
                 keil=P(HT["oecd"]["keil"][c], 1), anteil=LT.ANTEIL_TXT.get(sp, "{a}–{b}").format(a=round(amin / 10), b=round(amax / 10)))
    else:
        amin, amax = VB.anteil("FR")
        w.update(fr_anteil=LT.ANTEIL_TXT.get(sp, "{a}–{b}").format(a=round(amin / 10), b=round(amax / 10)), zu=zg, zu_verr="")   # EU-Mittel: gemeinsamer Satz
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
    nt = VT.NEU[sp]
    for k, v in nt.items():
        if not k.startswith(("rech_fein_", "chan1_zusatz")):
            quelle[k] = v
    KT.anwenden(sp, quelle, json.loads((SB.SPRACHEN_DIR / f"{sp}.json").read_text(encoding="utf-8")))   # v4.45: Korrekturen 24.10.2026
    if nt["rech_fein_alt"] and nt["rech_fein_alt"] in quelle["rech_fein"]:
        quelle["rech_fein"] = quelle["rech_fein"].replace(nt["rech_fein_alt"], nt["rech_fein_neu"])
    quelle["rech_fein"] += nt["rech_fein_zusatz"]
    # v4.13: Weitergabe per Gesetz bis zum Stichtag (nach dem Satz mit „80“) und Niveau des Netzes (an b11_p)
    saetze = re.split(r"(?<=[.!?])\s+", quelle["b2_p"])
    i80 = next(i for i, x in enumerate(saetze) if "80" in x)
    quelle["b2_p"] = " ".join(saetze[:i80 + 1] + [VT.WEITERGABE_SATZ[sp]] + saetze[i80 + 1:])
    quelle["b11_p"] += VT.NETZ_NIVEAU[sp]
    if "svg_gemeinde_sub_kurz" not in quelle:      # 24.10.2026: ohne eigenen Text wie der Untertitel der großen Grafik
        quelle["svg_gemeinde_sub_kurz"] = quelle.get("svg_gemeinde_sub") or json.loads((SB.SPRACHEN_DIR / f"{sp}.json").read_text(encoding="utf-8"))["svg_gemeinde_sub"]
    quelle["sich4_p"] += VT.RENTEN_SATZ[sp]   # v4.14
    # 24.10.2026: Staatsschulden-Grafik entfällt; ihr Text zum gemeinsamen Fonds (ohne den ersten Satz) an den Abschnitt Altlasten
    quelle["sich4_p"] += " " + quelle["js_schuld_text"].split(". ", 1)[1]
    anteil = VB.anteil(c)[0] if c in VB.LAENDER else _ANT
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
    return ST.anwenden(sp, out)   # v4.55: Texte nach Projektstand v4.54


def rr_de():
    """Rechner-Raster Deutschland im einheitlichen Format (heute und Arbeitgeberbeiträge je Beitragsregime)."""
    r = json.loads((AGG / "haushalte33_raster.json").read_text(encoding="utf-8"))["rechner"]
    D = r["deckel_lohn"]   # v4.36: einheitlicher Deckel der Weitergabe (6 × Grundbedarf)
    ag = {reg: [round(c[0] * min(b, D, r["bbg_kv"]) + c[1] * min(b, D, r["bbg_rv"]), 1) for b in r["brutto"]] for reg, c in r["beitrag"].items()}
    heute = {key: VB.heute_mit_bedarf("DE", r["brutto"], v, int(key.split("|")[1]), int(key.split("|")[2])) for key, v in r["heute"].items()}
    return dict(brutto=r["brutto"], schritt=1000, start=42000, heute=heute, ag=ag, jahre=r["jahre"], div=r["div"], eff=r["eff"],
                stufen=r["stufen"], saetze=r["saetze"], eff_alt=r["eff_alt"], weitergabe=r["weitergabe"], zuschlag=r["zuschlag"], zu=r["zu"],
                vorsorge=r["vorsorge"], kq=r["kq"], **VB.rechner_felder("DE"))


def rr_land(c, in_eur=False):
    h = HL["staaten"][c]
    r = h["raster"]
    f = 1 / FX.get(c, 1.0) if in_eur else 1.0
    m = lambda xs: [round(x * f, 2) for x in xs]
    heute = {}
    for k, v in r["heute"].items():
        e_, k_ = (int(x) for x in k.split("|"))
        hv = m(VB.heute_mit_bedarf(c, r["brutto"], v, e_, k_))      # Bedarfsleistungen in Landeswährung, dann umrechnen
        for reg in ("2028", "2035"):
            heute[f"{reg}|{k}"] = hv
    return dict(brutto=m(r["brutto"]), schritt=r["schritt"] * f, start=round(h["beispiel"]["brutto"] * f, 2), heute=heute,
                ag={"2028": m(r["ag"]), "2035": m(r["ag"])}, jahre=r["jahre"], div=m(r["div"]), eff=r["eff"], stufen=m(r["stufen"]),
                saetze=r["saetze"], eff_alt=r["eff_alt"], weitergabe=r["weitergabe"], zuschlag=r["zuschlag"], zu=r["zu"], vorsorge=r["vorsorge"],
                kq=[[x * f, y] for x, y in r["kq"]], **VB.rechner_felder(c, f))


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
function neuR(i,b,e,k,j){const t=R.jahre.indexOf(j),DIV=R.div[t]*12*R.topf,EFF=R.eff[t],reg=j>=2035?'2035':'2028';
  const brutto=b+R.weitergabe*R.ag[reg][i],st=estR(brutto+DIV)+(e-1)*estR(DIV),div=DIV*e+k*DIV*R.s,netto=brutto-st+div;
  const konsum=kqR(netto)*netto,mm=konsum*((1+EFF/100)/(1+R.eff_alt/100)-1),mb=konsum*EFF/(100+EFF);
  const ZU=R.zu?R.zu[t]:R.zuschlag,x=netto-mm-ZU/100*(st+mb),F=R.gb*(1+0.5*(e-1)+R.kw*k),auf=Math.max(0,F-div-R.anr*Math.max(0,x-div));
  return {netto:x+auf-R.vorsorge*b,div:div};}
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
    # 24.10.2026 (Initiative): Länderkarten Australien und Schweden
    ('<div class="land"><div class="n">@@erf4_n@@</div><h3>@@erf4_h@@</h3><span class="k">@@erf4_k@@</span><p>@@erf4_p@@</p></div>', '<div class="land"><div class="n">@@erf4_n@@</div><h3>@@erf4_h@@</h3><span class="k">@@erf4_k@@</span><p>@@erf4_p@@</p></div>\n      <div class="land"><div class="n">@@erf5_n@@</div><h3>@@erf5_h@@</h3><span class="k">@@erf5_k@@</span><p>@@erf5_p@@</p></div>\n      <div class="land"><div class="n">@@erf6_n@@</div><h3>@@erf6_h@@</h3><span class="k">@@erf6_k@@</span><p>@@erf6_p@@</p></div>'),
    # 24.10.2026: eigener Untertitel für das schmale Feld der mobilen Grafik („Kommunen und Regionen“ passt dort nicht in eine Zeile)
    ('<text class="s" x="270" y="280" text-anchor="middle" style="font-size:10px">@@svg_gemeinde_sub@@</text>',
     '<text class="s" x="270" y="280" text-anchor="middle" style="font-size:10px">@@svg_gemeinde_sub_kurz@@</text>'),
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
    # v4.8: Abschnitt „Chancen“ mit Tabelle und Gini-Grafik; Dividendengrafik aufklappbar; CO₂ vor Staatsschulden; über Europa hinaus
    ('<a class="opt" href="#zeitpfad">@@nav_zeitpfad@@</a>', '<a class="opt" href="#chancen">@@nav_zeitpfad@@</a>'),
    ('<section id="zeitpfad">', '<section id="chancen">\n  <div class="wrap">\n    <h2>@@chan_h2@@</h2>\n    <p class="lede">@@chan_lede@@</p>\n    <div class="mass-grid">\n      <div class="mass"><div class="pos">@@chan1_pos@@</div><h3>@@chan1_h@@</h3><p>@@chan1_p@@</p></div>\n      <div class="mass"><div class="pos">@@chan2_pos@@</div><h3>@@chan2_h@@</h3><p>@@chan2_p@@</p></div>\n      <div class="mass"><div class="pos">@@chan3_pos@@</div><h3>@@chan3_h@@</h3><p>@@chan3_p@@</p></div>\n      <div class="mass"><div class="pos">@@chan4_pos@@</div><h3>@@chan4_h@@</h3><p>@@chan4_p@@</p></div>\n    </div>\n    <h3 class="sub-h">@@bess_h3@@</h3>\n    <p class="lede">@@bess_p@@</p>\n    @@bess_tab@@\n    <p class="fineprint">@@bess_fein@@</p>\n    <h3 class="sub-h">@@gini_h3@@</h3>\n    <p class="lede">@@gini_p@@</p>\n    <div class="chart-card">\n      <div class="unit">@@gini_unit@@</div>\n      @@gini_svg@@\n      @@gini_leg@@\n      <p class="fineprint" style="margin-top:12px">@@gini_fein@@</p>\n    </div>\n  </div>\n</section>\n\n<section id="zeitpfad">'),
    ('<div class="chart-card">\n      <div class="tabs" id="gtabs">', '<details class="mehr"><summary>@@zeit_mehr@@</summary><div class="chart-card">\n      <div class="tabs" id="gtabs">'),
    ('<span class="l-hist"><i></i>@@zeit_l2@@</span></div>\n    </div>', '<span class="l-hist"><i></i>@@zeit_l2@@</span></div>\n    </div></details>'),
    ('<button type="button" aria-pressed="true" data-v="schuld">@@reise_t1@@</button><button type="button" aria-pressed="false" data-v="co2">@@reise_t2@@</button>',
     '<button type="button" aria-pressed="true" data-v="co2">@@reise_t2@@</button>'),   # 24.10.2026: Staatsschulden-Grafik entfällt (ohne Vergleich zum heutigen Pfad)
    ("seg('ztabs',chart2);chart2('schuld');", "seg('ztabs',chart2);chart2('co2');"),
    ('<div><h3>@@klub_6_h@@</h3><p>@@klub_6_p@@</p></div>', '<div><h3>@@klub_6_h@@</h3><p>@@klub_6_p@@</p></div>\n      <div><h3>@@welt_h@@</h3><p>@@welt_p@@</p></div>'),
]


def _pfad(text, size, cx, base, breite=540):
    """Wortmarke als Umriss (v4.65): unabhängig von Schriftladen und Ligaturen (Space Grotesk verbindet sonst „tt“ in „Drittel“)."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    global _FONT
    if "_FONT" not in globals():
        _FONT = TTFont(str(Path(__file__).resolve().parent / "schrift" / "SpaceGrotesk-Bold.ttf"))
    gs, cmap, upm = _FONT.getGlyphSet(), _FONT.getBestCmap(), _FONT["head"].unitsPerEm
    w = sum(gs[cmap[ord(ch)]].width for ch in text)
    s = min(size / upm, breite / w)
    x0, x, d = cx - w * s / 2, 0, []
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x0 + x * s, base)))
        d.append(pen.getCommands())
        x += gs[g].width
    return re.sub(r"(\.\d\d)\d+", r"\1", " ".join(d))


def marke(sp):
    z = TT.MARKE[sp]
    h = 130 * len(z)
    d = " ".join(_pfad(t, 116, 280, 112 + 130 * i) for i, t in enumerate(z))
    zeilen = f'<path fill="#0F3B5C" d="{d}"/>'
    return {"MARKE_H": str(h), "MARKE_ZEILEN": zeilen, "MARKE_NAME": TT.NAME[sp], "NETZ_NAME": TT.NETZ[sp]}


MONATE = {"de": None, "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
          "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
          "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
          "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
          "pl": ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"]}
MONATE_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


def stand_datum(sp):
    """Datum des Modellstands aus dem Logbuch (v4.65; vorher fest „18. Oktober 2026“, Korrektur 84)."""
    lb = (WURZEL / "logbuch" / "Versionsgeschichte-TAX-2828-BandIII.md").read_text(encoding="utf-8")
    i = lb.index(f"### {VERSION} ")
    m = re.search(r"(\d{1,2})\. (" + "|".join(MONATE_DE) + r") (\d{4})", lb[i:i + 2000])
    tag, mon, jahr = int(m.group(1)), MONATE_DE.index(m.group(2)), m.group(3)
    if sp == "de":
        return f"{tag}. {MONATE_DE[mon]} {jahr}"
    if sp == "en":
        return f"{tag} {MONATE['en'][mon]} {jahr}"
    if sp == "es":
        return f"{tag} de {MONATE['es'][mon]} de {jahr}"
    return f"{tag} {MONATE[sp][mon]} {jahr}"


FORSCHUNG = "https://archicrowd.github.io/goldenes-drittel/"
WP = FORSCHUNG + "downloads/Golden-Third-Working-Paper.pdf"
DOI = "10.5281/zenodo.23855733"
# v4.65: Verweise auf Working Paper, Forschungsseite und Archiv (DE von der Initiative freigegeben; übrige Sprachen maschinell übersetzt, gegenzulesen)
KACHELN = {
    "de": (("Working Paper", "Ziele, Modell, Ergebnisse und Zielkonflikte, 14 Seiten (englisch).", "PDF"),
           ("Forschung und Prüfung", "Prüfberichte, Zahlen zum Zitieren, Ergebnisdateien. Archiv mit DOI.", "Forschungsseite"),
           "Working Paper, Prüfberichte und Zahlen zum Zitieren: <a href=\"{f}de/\">Forschungsseite</a>; Archiv <a href=\"https://doi.org/{doi}\">doi.org/{doi}</a>. "
           "Die internen Prüfungen erfassen den Modellstand bis v4.42; die Änderungen seither werden nachgeprüft."),
    "en": (("Working paper", "Objectives, model, results and trade-offs, 14 pages.", "PDF"),
           ("Research and review", "Review reports, figures to cite, result files. Archived with DOI.", "Research site"),
           "Working paper, review reports and figures to cite: <a href=\"{f}\">research site</a>; archive <a href=\"https://doi.org/{doi}\">doi.org/{doi}</a>. "
           "The internal reviews cover the model up to version v4.42; the changes since are being reviewed."),
    "fr": (("Working paper", "Objectifs, modèle, résultats et arbitrages, 14 pages (en anglais).", "PDF"),
           ("Recherche et vérification", "Rapports de vérification, chiffres à citer, fichiers de résultats. Archivé avec DOI.", "Site de recherche"),
           "Working paper, rapports de vérification et chiffres à citer : <a href=\"{f}\">site de recherche</a> ; archive <a href=\"https://doi.org/{doi}\">doi.org/{doi}</a>. "
           "Les examens internes portent sur la version v4.42 du modèle ; les modifications ultérieures sont en cours de vérification."),
    "it": (("Working paper", "Obiettivi, modello, risultati e conflitti tra obiettivi, 14 pagine (in inglese).", "PDF"),
           ("Ricerca e verifica", "Rapporti di verifica, dati da citare, file dei risultati. Archiviato con DOI.", "Sito di ricerca"),
           "Working paper, rapporti di verifica e dati da citare: <a href=\"{f}\">sito di ricerca</a>; archivio <a href=\"https://doi.org/{doi}\">doi.org/{doi}</a>. "
           "Le verifiche interne riguardano il modello fino alla versione v4.42; le modifiche successive sono in corso di verifica."),
    "es": (("Working paper", "Objetivos, modelo, resultados y conflictos entre objetivos, 14 páginas (en inglés).", "PDF"),
           ("Investigación y revisión", "Informes de revisión, cifras para citar, ficheros de resultados. Archivado con DOI.", "Sitio de investigación"),
           "Working paper, informes de revisión y cifras para citar: <a href=\"{f}\">sitio de investigación</a>; archivo <a href=\"https://doi.org/{doi}\">doi.org/{doi}</a>. "
           "Las revisiones internas abarcan el modelo hasta la versión v4.42; los cambios posteriores se están revisando."),
    "pl": (("Working paper", "Cele, model, wyniki i konflikty celów, 14 stron (po angielsku).", "PDF"),
           ("Badania i weryfikacja", "Raporty z weryfikacji, liczby do cytowania, pliki wyników. Archiwum z DOI.", "Strona badawcza"),
           "Working paper, raporty z weryfikacji i liczby do cytowania: <a href=\"{f}\">strona badawcza</a>; archiwum <a href=\"https://doi.org/{doi}\">doi.org/{doi}</a>. "
           "Wewnętrzne kontrole obejmują model do wersji v4.42; późniejsze zmiany są weryfikowane."),
}


# v4.66: Prüfungen als interne Prüfungen bezeichnen (Vorgabe der Initiative, 3.11.2026); Ersatz im fertigen Methodik-Absatz
PRUEF_ALT_NEU = {
    "de": ("in drei Prüfungen im Auftrag der Initiative nachgerechnet (darin eine eigene Mikrosimulation)",
           "in drei internen Prüfungen nachgerechnet, durchgeführt mit einem anderen KI-Modell als dem, mit dem die Rechnung entwickelt wurde (darin eine eigene Mikrosimulation)"),
    "en": ("in three reviews commissioned by the initiative (including their own microsimulation)",
           "in three internal reviews, carried out with a different AI model from the one used to build the calculation (including their own microsimulation)"),
    "fr": ("lors de trois examens commandés par l'initiative (dont une microsimulation propre)",
           "lors de trois examens internes, menés avec un autre modèle d'IA que celui utilisé pour le calcul (dont une microsimulation propre)"),
    "it": ("in tre verifiche commissionate dall'iniziativa (tra cui una propria microsimulazione)",
           "in tre verifiche interne, condotte con un modello di IA diverso da quello usato per il calcolo (tra cui una propria microsimulazione)"),
    "es": ("en tres revisiones encargadas por la iniciativa (una con su propia microsimulación)",
           "en tres revisiones internas, realizadas con un modelo de IA distinto del utilizado para el cálculo (una con su propia microsimulación)"),
    "pl": ("w trzech kontrolach zleconych przez inicjatywę (w tym własna mikrosymulacja)",
           "w trzech wewnętrznych kontrolach, przeprowadzonych innym modelem AI niż ten użyty do rachunku (w tym własna mikrosymulacja)"),
}


def forschung_einbauen(sp, html):
    alt, neu = PRUEF_ALT_NEU[sp]
    assert html.count(alt) == 1, (sp, alt[:40])
    html = html.replace(alt, neu)
    k1, k2, satz = KACHELN[sp]
    zz = "".join(f'<a href="{u}"><span class="t">{t}</span><span class="d">{d}</span><span class="f">{f}</span></a>\n      '
                 for u, (t, d, f) in ((WP, k1), (FORSCHUNG + ("de/" if sp == "de" else ""), k2)))
    i = html.index('<div class="anl">')
    j = html.index("</a>", html.index("</a>", i) + 4) + 4          # nach Kurzfassung und Gesamtkonzept
    html = html[:j] + "\n      " + zz.rstrip() + html[j:]
    assert html.count('<p class="verstamp">') == 1
    html = html.replace('<p class="verstamp">', f'<p>{satz.format(f=FORSCHUNG, doi=DOI)}</p><p class="verstamp">', 1)
    return html.replace("</style>", "html{font-variant-ligatures:no-common-ligatures}</style>", 1)


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
        fehlt = set(TX) - set(T) - set(VT.NEU[sp]) - KT.NEUE_SCHLUESSEL   # 24.10.2026: neue Schlüssel nur für Stand C
        if fehlt:
            raise SystemExit(f"{sp}: unbekannte Schlüssel: {sorted(fehlt)}")
        T.update(TX)
        W = SB.werte(sp)
        W.update(version=VERSION, fassung=stand_datum(sp))
        nm = VT.LAENDER_NAME[sp]
        bc = c if c in VB.LAENDER else "DE"
        GF = json.loads((AGG / "gini_frankreich.json").read_text(encoding="utf-8"))["staaten"]["FR"]   # v4.9, Korrektur 64
        gz = lambda v: SB.zahl(v, 1, sp)
        W.update(fr_deckel_1=gz(GF["gini_weitergabe_gedeckelt_1x"]), fr_deckel_15=gz(GF["gini_weitergabe_gedeckelt_1_5x"]),
                 fr_familie=gz(GF["gini_abbildung_familie"]), fr_2028=gz(VB.GINI["staaten"]["FR"]["reihe"][0]["mitte"]))
        nc = c if c in VB.LAENDER else "DE"
        fxn = FX.get(nc, 1.0) if nc == c else 1.0
        netz_pct = NB[2028]["netz_pct_bip"] if nc == "DE" else LS["staaten"][nc]["netz_pct_bip"][0]
        W.update(gk_land=VT.LAENDER_NAME[sp][nc], gk1=SB.eur(VB.RB.boden(nc, 1, 0) / 12, sp), gk4=SB.eur(VB.RB.boden(nc, 2, 2) / 12, sp),
                 netz_pct=SB.pct(netz_pct, sp, 1))
        W.update(chan1_zusatz=VT.NEU[sp]["chan1_zusatz_de"] if c == "DE" else "", bess_land=nm[bc] if c in VB.LAENDER else VT.BEISPIEL_EN)
        dez = "." if sp == "en" else ","
        svg, leg = VB.gini_svg(nm, c, T["gini_l1"], T["gini_l2"], T["gini_l3"], T["gini_ref"], T["gini_unit"])
        T.update(gini_svg=svg.replace("@@DEZ@@", dez), gini_leg=leg,
                 bess_tab=VB.bess_tab(sp, bc, T, lambda x: SB.eur(x, sp), lambda x: SB.pct(x, sp)))
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
        html = html.replace("</style>", VB.CSS + "#raum button{display:block;text-align:left}#raum button span{display:block}"
                                        "#raum button span:last-child{text-align:right;white-space:nowrap}</style>", 1)
        html = forschung_einbauen(sp, html)
        for alt in ("TAX 28:28", "28%3A28"):
            if alt in html:
                raise SystemExit(f"{sp}: Restbestand {alt!r} in der Seite")
        (ZIEL / f"{sp}.html").write_text(html, encoding="utf-8")
        print(f"geschrieben: {(ZIEL / f'{sp}.html').relative_to(WURZEL)} ({len(html)} Zeichen), Referenz {c}")
    SB.eur = eur_orig


if __name__ == "__main__":
    main()
