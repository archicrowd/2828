#!/usr/bin/env python3
"""Länderrechnungen nach dem Standard (modell/laender/STANDARD.md, Modellstand v3.27).

Ein gemeinsames Skript für alle Länder. Eingaben je Land: modell/laender/<cc>.toml.
Ausgabe: daten/aggregate/laender/<cc>.json und daten/aggregate/laender_vergleich.csv.
Keine Prognose des Autors: Fortschreibung mit den eingetragenen Eingaben.

Die Rechnung ist für alle Länder identisch. Der Gewichtungsschritt (Wirkung auf die Klubquote 2028)
läuft nur für Länder, die im Gewichtsbestand der Gesamtrechnung stehen (modell/rahmen/basis.py).
"""
import contextlib, csv, importlib.util, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parents[2]
PAR = W / "modell" / "laender"
AGG = W / "daten" / "aggregate"
OUT = AGG / "laender"
JAHRE = (2026, 2027, 2028)
PFLICHT = ["land", "name", "schuld_2025", "schuld_2025_quelle", "saldo_2025", "saldo_2025_quelle",
           "saldo_regierung", "quote_regierung", "regierung_quelle", "eingaben", "luecken"]

_gr = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell/gesamtrechnung.toml").read_text(encoding="utf-8"))["parameter"]}
G_NOM = float(_gr["wachstum_nominal"])
KLUB_SALDO = -2.93   # Klub-Gesamtsaldo wie in v3.23 (frankreich.py, ersetzt in v3.24); Prüfung unten gegen schuldenpfad.json

_spec = importlib.util.spec_from_file_location("basis", W / "modell" / "rahmen" / "basis.py")
_basis = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(_basis)
GDP = _basis.GDP
TOT = sum(GDP.values())

with open(AGG / "schulden_2010_2025.csv", encoding="utf-8") as _f:
    _rows = list(csv.DictReader(_f))
KLUB = {r["land"]: float(r["2025"]) for r in _rows}
SALDO25 = {r["land"]: float(r["defizit_2025"]) for r in _rows}   # Status quo je Land (Standard 2.4, seit v3.27)
_sp = json.loads((AGG / "schuldenpfad.json").read_text(encoding="utf-8"))
if abs(_sp["saldo_2025"] - KLUB_SALDO) > 0.01:
    sys.exit(f"Klub-Saldo {_sp['saldo_2025']:.3f} weicht von {KLUB_SALDO} ab; KLUB_SALDO anpassen und im Logbuch vermerken")
D_KLUB_25 = sum(GDP[k] * KLUB[k] for k in GDP) / TOT

# Wohnort (Standard 2.6): Dividendenboden und Tarifstufen nach Preisniveau, Euro 2028 nominal
with open(AGG / "preisniveau_2024.csv", encoding="utf-8") as _f:
    PLI_CSV = {r["land"]: float(r["preisniveau_eu27_100"]) for r in csv.DictReader(_f)}
PLI_DE = PLI_CSV["DE"]
ANKER_DE = float(json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))["anker_de"])
_tg = json.loads((AGG / "tarif_grundbedarf.json").read_text(encoding="utf-8"))
G28, SAETZE, STUFEN_REF = float(_tg["grundbedarf_2028"]), _tg["saetze"], _tg["stufen_laender_2028"]
_lv = json.loads((AGG / "laendervarianten.json").read_text(encoding="utf-8"))["zeilen"]
LV = {z["land"]: z for z in _lv}


def wohnort(cc, pli):
    if pli is None:
        return dict(entfaellt="Preisniveau nicht eingetragen")
    if cc in PLI_CSV and abs(PLI_CSV[cc] - float(pli)) > 0.001:
        sys.exit(f"{cc}: Preisniveau {pli} weicht von preisniveau_2024.csv ({PLI_CSV[cc]}) ab")
    f = float(pli) / PLI_DE
    w = dict(preisniveau_2024=float(pli), faktor_gegen_de=round(f, 4),
             dividende_boden_2028_eur_monat=round(ANKER_DE * f, 2),
             dividende_boden_kind_2028_eur_monat=round(ANKER_DE * f / 2, 2),
             tarifstufen_2028_eur_jahr=[round(G28 * f * k) for k in (1, 2, 3, 4)], tarifsaetze_pct=SAETZE,
             einheit="Euro 2028, nominal. Dividende je Erwachsenem und Monat (Kinder zur Hälfte); Tarifstufen je Jahr",
             grundlage="Boden: halbes Existenzminimum am Wohnort (V3b, v3.20); Stufen: 1- bis 4-facher Grundbedarf (v3.22)")
    if cc in LV:
        if abs(LV[cc]["div_v3b"] - ANKER_DE * f) > 0.01:
            sys.exit(f"{cc}: Dividendenboden weicht von laendervarianten.json ab")
        w["dividende_ausgezahlt_v3a_2028_eur_monat"] = round(LV[cc]["div_v3a"], 2)
    else:
        w["dividende_ausgezahlt_v3a_2028_eur_monat"] = None
        w["hinweis_v3a"] = "V3a verteilt den Klubtopf und gilt nur im Gewichtsbestand der Gesamtrechnung; ausgewiesen ist der Boden"
    if cc in STUFEN_REF and STUFEN_REF[cc] != w["tarifstufen_2028_eur_jahr"]:
        sys.exit(f"{cc}: Tarifstufen weichen von tarif_grundbedarf.json ab")
    return w


def rund(d):
    return {str(j): round(v, 2) for j, v in d.items()}


def pfad(d25, saldo, g):
    d, out = d25, {}
    for j in JAHRE:
        gj = g[j] if isinstance(g, dict) else g
        d = d / (1 + gj / 100) - saldo[j]
        out[j] = d
    return out


def wachstum_implizit(d25, quote, saldo):
    d_prev, res = d25, {}
    for j in JAHRE:
        res[j] = (d_prev / (quote[j] + saldo[j]) - 1) * 100
        d_prev = quote[j]
    return res


def s_rest(laender):
    """Saldo der übrigen Länder: ihr eigener Saldo 2025, BIP-gewichtet (Status quo). Bis v3.26 war es der Rest-Saldo,
    der den Klub-Gesamtsaldo bei −2,93 % festhielt; dadurch wirkte jede Defizitabweichung neutral (Korrektur 57)."""
    rest = [k for k in GDP if k not in laender]
    return sum(GDP[k] * SALDO25[k] for k in rest) / sum(GDP[k] for k in rest)


def klub_mit_land(cc, s_land, g_land):
    d_rest = sum(GDP[k] * KLUB[k] for k in GDP if k != cc) / (TOT - GDP[cc])
    dr, df = d_rest, KLUB[cc]
    for j in JAHRE:
        dr = dr / (1 + G_NOM / 100) - s_rest({cc})
        df = df / (1 + g_land[j] / 100) - s_land[j]
    return (dr * (TOT - GDP[cc]) + df * GDP[cc]) / TOT


def klub_referenz():
    d = D_KLUB_25
    for _ in JAHRE:
        d = d / (1 + G_NOM / 100) - KLUB_SALDO
    return d


def rechne(p):
    cc = p["land"]
    d25, s25 = float(p["schuld_2025"]), float(p["saldo_2025"])
    if cc in KLUB:
        if abs(KLUB[cc] - d25) > 0.051:
            sys.exit(f"{cc}: Schuld 2025 {d25} weicht von schulden_2010_2025.csv ({KLUB[cc]}) ab")
    sreg = dict(zip(JAHRE, map(float, p["saldo_regierung"])))
    A = pfad(d25, {j: s25 for j in JAHRE}, G_NOM)
    B = pfad(d25, sreg, G_NOM)
    gimp = None
    if p["quote_regierung"]:
        qreg = dict(zip(JAHRE, map(float, p["quote_regierung"])))
        gimp = wachstum_implizit(d25, qreg, sreg)
        C = pfad(d25, sreg, gimp)
        for j in JAHRE:
            if abs(C[j] - qreg[j]) > 0.01:
                sys.exit(f"{cc}: Pfad C reproduziert die Regierungsquote {j} nicht ({C[j]:.2f} gegen {qreg[j]})")
        pfad_c = dict(beschreibung="Regierungsquote, implizites Wachstum (reproduziert die Prognose)",
                      werte=rund(C), wachstum_implizit_pct=rund(gimp))
        if p.get("quote_regierung_hinweis"):
            pfad_c["hinweis"] = p["quote_regierung_hinweis"]
        g_reg = {int(k): float(v) for k, v in p.get("wachstum_nominal_regierung", {}).items()}
        if g_reg:   # Standard 2.3: Bestandsanpassung = Regierungsquote minus Fortschreibung mit Regierungswachstum
            sfa, d_prev = {}, d25
            for j in JAHRE:
                if j in g_reg:
                    sfa[j] = qreg[j] - (d_prev / (1 + g_reg[j] / 100) - sreg[j])
                d_prev = qreg[j]
            pfad_c["wachstum_nominal_regierung_pct"] = {str(j): v for j, v in g_reg.items()}
            pfad_c["bestandsanpassung_pct_bip"] = rund(sfa)
        abw = dict(B_minus_C_2028=round(B[2028] - C[2028], 2), A_minus_C_2028=round(A[2028] - C[2028], 2))
    else:
        C = None
        pfad_c = dict(entfaellt="keine Schuldenquoten-Prognose eingetragen")
        abw = None
    if cc in GDP:
        gew = dict(anteil_klub_bip_pct=round(GDP[cc] / TOT * 100, 1),
                   klub_2028_referenz=round(klub_referenz(), 2),
                   klub_2028_mit_land_status_quo=round(klub_mit_land(cc, {j: s25 for j in JAHRE}, {j: G_NOM for j in JAHRE}), 2),
                   klub_2028_mit_land_regierungsdefizit=round(klub_mit_land(cc, sreg, {j: G_NOM for j in JAHRE}), 2))
        if gimp:
            gew["klub_2028_mit_land_regierungsdefizit_und_wachstum"] = round(klub_mit_land(cc, sreg, gimp), 2)
        gew["hinweis"] = "Sensitivität, kein Ersatz für die Gesamtrechnung (Standard 2.4)"
    else:
        gew = dict(entfaellt="Land nicht im Gewichtsbestand der Gesamtrechnung (modell/rahmen/basis.py)")
    return dict(
        standard="modell/laender/STANDARD.md, Fassung 1.3 (v3.27)", land=cc, name=p["name"],
        bezugsjahr_ausgang=2025, preisbasis="Verhältniszahl (% des BIP), laufende Preise",
        wachstum_nominal_pct=G_NOM,
        ausgang=dict(schuld_2025_pct_bip=d25, quelle=p["schuld_2025_quelle"],
                     saldo_2025_pct_bip=s25, saldo_quelle=p["saldo_2025_quelle"]),
        regierung=dict(saldo_pct_bip=dict(zip(map(str, JAHRE), map(float, p["saldo_regierung"]))),
                       quote_pct_bip=(dict(zip(map(str, JAHRE), map(float, p["quote_regierung"]))) if p["quote_regierung"] else None),
                       quelle=p["regierung_quelle"]),
        pfade=dict(A_status_quo=dict(beschreibung="Saldo 2025 bleibt 2026 bis 2028", werte=rund(A)),
                   B_regierungsdefizit=dict(beschreibung="Regierungssaldo, nominales Wachstum 3,0 %", werte=rund(B)),
                   C_regierungsschuldenquote=pfad_c),
        abweichung_2028=abw, gewichtung=gew, wohnort=wohnort(cc, p.get("preisniveau_2024")),
        eingaben=p["eingaben"], luecken=p["luecken"],
    )


def main():
    ergebnisse = []
    for datei in sorted(PAR.glob("*.toml")):
        p = tomllib.loads(datei.read_text(encoding="utf-8"))
        fehlend = [k for k in PFLICHT if k not in p]
        if fehlend:
            sys.exit(f"{datei.name}: Pflichtfelder fehlen: {fehlend}")
        if len(p["saldo_regierung"]) != 3 or len(p["quote_regierung"]) not in (0, 3):
            sys.exit(f"{datei.name}: saldo_regierung braucht 3 Werte, quote_regierung 0 oder 3")
        ergebnisse.append(rechne(p))
    OUT.mkdir(parents=True, exist_ok=True)
    # Standard 2.4, gemeinsame Wirkung: alle Länder mit Regierungspfad C im Gewichtsbestand zugleich auf ihrem Pfad,
    # die übrigen Länder bleiben bei ihrem eigenen Saldo 2025 (Status quo), Wachstum 3,0 %.
    L = [r for r in ergebnisse if r["land"] in GDP and "werte" in r["pfade"]["C_regierungsschuldenquote"]]
    if L:
        w_l = sum(GDP[r["land"]] for r in L)
        rest = TOT - w_l
        d_rest = sum(GDP[k] * KLUB[k] for k in GDP if k not in {r["land"] for r in L}) / rest
        d_l = {r["land"]: KLUB[r["land"]] for r in L}
        for j in JAHRE:
            s = {r["land"]: r["regierung"]["saldo_pct_bip"][str(j)] for r in L}
            g = {r["land"]: r["pfade"]["C_regierungsschuldenquote"]["wachstum_implizit_pct"][str(j)] for r in L}
            s_rest_j = s_rest(set(s))
            d_rest = d_rest / (1 + G_NOM / 100) - s_rest_j
            for c in d_l:
                d_l[c] = d_l[c] / (1 + g[c] / 100) - s[c]
        k_gem = (d_rest * rest + sum(d_l[c] * GDP[c] for c in d_l)) / TOT
        gem = dict(laender=[r["land"] for r in L], anteil_klub_bip_pct=round(w_l / TOT * 100, 1),
                   klub_2028_referenz=round(klub_referenz(), 2), klub_2028_gemeinsam=round(k_gem, 2),
                   hinweis="Alle genannten Länder zugleich auf ihrem Regierungspfad (Saldo und implizites Wachstum); "
                           "Sensitivität, kein Ersatz für die Gesamtrechnung (Standard 2.4)")
        (AGG / "laender_klub.json").write_text(json.dumps(gem, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Klub 2028 gemeinsam ({', '.join(gem['laender'])}, {gem['anteil_klub_bip_pct']} % des Klub-BIP): "
              f"{gem['klub_2028_gemeinsam']} gegen Referenz {gem['klub_2028_referenz']}")
    for r in ergebnisse:
        (OUT / f"{r['land'].lower()}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(AGG / "laender_vergleich.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["land", "name", "schuld_2025_pct_bip", "saldo_2025_pct_bip", "A_2028", "B_2028", "C_2028", "B_minus_C_2028",
                    "preisniveau_2024", "dividende_boden_2028_eur_monat", "tarifstufe1_2028_eur_jahr"])
        for r in ergebnisse:
            c, wo = r["pfade"]["C_regierungsschuldenquote"], r["wohnort"]
            w.writerow([r["land"], r["name"], r["ausgang"]["schuld_2025_pct_bip"], r["ausgang"]["saldo_2025_pct_bip"],
                        r["pfade"]["A_status_quo"]["werte"]["2028"], r["pfade"]["B_regierungsdefizit"]["werte"]["2028"],
                        c.get("werte", {}).get("2028", ""), (r["abweichung_2028"] or {}).get("B_minus_C_2028", ""),
                        wo.get("preisniveau_2024", ""), wo.get("dividende_boden_2028_eur_monat", ""),
                        (wo.get("tarifstufen_2028_eur_jahr") or [""])[0]])
    for r in ergebnisse:
        a, b = r["pfade"]["A_status_quo"]["werte"], r["pfade"]["B_regierungsdefizit"]["werte"]
        print(f"{r['land']}: 2025 {r['ausgang']['schuld_2025_pct_bip']} % | A {a['2026']} / {a['2027']} / {a['2028']} | "
              f"B {b['2026']} / {b['2027']} / {b['2028']}")
        if "werte" in r["pfade"]["C_regierungsschuldenquote"]:
            cc_ = r["pfade"]["C_regierungsschuldenquote"]["werte"]
            print(f"   C (Regierung) {cc_['2026']} / {cc_['2027']} / {cc_['2028']}")
        if "bestandsanpassung_pct_bip" in r["pfade"]["C_regierungsschuldenquote"]:
            print(f"   Bestandsanpassung (Regierungsquote gegen Regierungswachstum): "
                  f"{r['pfade']['C_regierungsschuldenquote']['bestandsanpassung_pct_bip']}")
        if "dividende_boden_2028_eur_monat" in r["wohnort"]:
            wo = r["wohnort"]
            print(f"   Wohnort: PLI {wo['preisniveau_2024']} | Dividendenboden {wo['dividende_boden_2028_eur_monat']} EUR/Monat | "
                  f"Stufen {wo['tarifstufen_2028_eur_jahr']} | V3a {wo['dividende_ausgezahlt_v3a_2028_eur_monat']}")
        if "klub_2028_referenz" in r["gewichtung"]:
            g = r["gewichtung"]
            print(f"   Klub 2028: Referenz {g['klub_2028_referenz']} | mit Land Status quo {g['klub_2028_mit_land_status_quo']} | "
                  f"Regierungsdefizit {g['klub_2028_mit_land_regierungsdefizit']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
