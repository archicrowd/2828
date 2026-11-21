#!/usr/bin/env python3
"""Baranteil ein Drittel des Grundbedarfs in Modell E (Logbuch v4.106). Prüfrechnung, ändert die geltende Rechnung nicht.

Kosten wie v4.105 (Altersausgleich R4, Stundung ab 65 aus co2_boden_haushalte.json); Bodenabgabe 2 % in Schritten bis 2030 (bzw. 2032), Fehlbetrag
als Kredit des Fonds mit Rückzahlung als Annuität. Gesucht: der kleinste einheitliche Satz auf alle Einkommensarten außer Arbeit, mit dem ein Drittel
tragbar ist; dazu Vermögensteuer-Varianten als Ersatz für Satzpunkte und der Zinsfall 3,0 %.
Ausgabe: daten/aggregate/anteil_drittel.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "anteil_drittel.toml").read_text(encoding="utf-8"))
CB = json.loads((AGG / "co2_boden_haushalte.json").read_text(encoding="utf-8"))
VB = tomllib.loads((W / "modell" / "vermoegensbasis33.toml").read_text(encoding="utf-8"))


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / datei)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


ME = lade("me_d", "modell_e.py")
VBM = lade("vb_d", "vermoegensbasis33.py")
ST = ME.ST
A = P["anteil"]
BIP = P["bip_2028_mrd"]


def kosten_basis():
    """R4 und Stundung je Jahr in % BIP (wie co2_boden_haushalte, v4.105)."""
    s = CB["stundung"]
    r4 = 0.23
    return {j: r4 + s["zinsvorteil_mrd"] / BIP * 100 + (s["zufluss_pct_bip"] if j - 2028 < 12 else 0.0) for j in ME.JAHRE}


def uebergang(bis):
    """Fehlbetrag der eingeschliffenen Bodenabgabe (Fonds deckt) und Annuität der Rückzahlung, % BIP je Jahr."""
    U = P["uebergang"]
    voll = ST.boden(0.02)
    fehl = {j: voll * (1 - min(1.0, (j - 2027) / (bis - 2027))) for j in ME.JAHRE}
    i = U["fondszins"]
    k = sum(f * (1 + i) ** (U["rueckzahlung_ab"] - 1 - j) for j, f in fehl.items() if f > 0)
    ab = max(U["rueckzahlung_ab"], bis + 1)
    k *= (1 + i) ** (ab - U["rueckzahlung_ab"])
    ann = k * i / (1 - (1 + i) ** -U["rueckzahlung_jahre"])
    netto = {j: -fehl[j] + (ann if ab <= j < ab + U["rueckzahlung_jahre"] else 0.0) for j in ME.JAHRE}
    return netto, dict(kredit_pct_bip=round(k, 2), annuitaet_pct_bip=round(ann, 3), rueckzahlung=f"{ab}–{ab + U['rueckzahlung_jahre'] - 1}")


def vermoegen():
    """Mehraufkommen der Vermögensteuer-Varianten gegen 1,5 % über 2 Mio. € (% BIP 2028, nach Ausweichen)."""
    V = P["vermoegen"]
    n = VB["haushalte_mio_2021"] * 1e6
    f = VB["fortschreibung_2021_2028"]
    ph, d = VB["phf"], VB["diw"]
    m10 = ph["anteil_top10"] * ph["mittel"] / 0.1
    a_phf = m10 / (m10 - ph["p90"])
    a_diw = 1 / (1 - math.log(d["anteil_top1"] / d["anteil_top10"]) / math.log(0.1))
    m10d = d["anteil_top10"] * d["mittel_vgr"] / 0.1
    t90d = m10d * (a_diw - 1) / a_diw
    kal = {"PHF 2021 (Befragung)": (a_phf, ph["p90"]), "DIW (mit Spitze)": (a_diw, t90d)}

    def auf(alpha, t90, satz, schwelle):
        alt = VBM.P["schwelle"]
        VBM.P["schwelle"] = schwelle
        try:
            hh, ueber = VBM.pareto_ueber(alpha, t90, n)
        finally:
            VBM.P["schwelle"] = alt
        return hh, ueber * f * satz / 100 / 1e9 / VB["bip_de_2028_mrd"] * 100 * (1 - V["ausweichen"])

    out = []
    for v in V["varianten"]:
        z = dict(satz_pct=v["satz"], schwelle_eur=v["schwelle"])
        for name, (al, t9) in kal.items():
            hh, x = auf(al, t9, v["satz"], v["schwelle"])
            _, x0 = auf(al, t9, V["satz_heute"], V["schwelle_heute"])
            z[name] = dict(haushalte_mio=round(hh / 1e6, 2), position_pct_bip=round(x, 2), mehr_gegen_heute_pct_bip=round(x - x0, 2))
        out.append(z)
    return out


def lauf(ks, ausg, zins=None, extra=0.0):
    st = dict(anteil_fest=A, ausgaben={j: ausg[j] - extra for j in ME.JAHRE}, kapital_satz=float(ks), boden_einschleifen_bis=None)
    st.pop("boden_einschleifen_bis")
    if zins is not None:
        st["zins"] = zins
    return ME.rechne(st)


def kurz(e, ks):
    p = e["paket"]
    return dict(kapital_satz=ks, anteil_tragbar_pct=e["anteil_tragbar_pct"], ruecklage_min_pct_bip=e["ruecklage_min_pct_bip"],
                ruecklage_max_pct_bip=e["ruecklage_max_pct_bip"], bip_2045_pct=e["dynamik"]["2045"]["bip_pct"],
                investition_2045=e["dynamik"]["2045"]["kanaele"]["I1"], fonds_spitze_pct_bip=e["fonds"]["schuld_spitze_pct_bip"],
                paket={j: dict(bar_erwachsen=x["bar_erwachsen"], bar_kind=x["bar_kind"], netz_x=x["netz_x_je_einwohner"], gesamt_erwachsen=x["gesamt_erwachsen"],
                               gesamt_kind=x["gesamt_kind"], anteil_pct=x["anteil_grundbedarf_pct"]) for j, x in p.items()},
                fortschritt=[(x["jahr"], x["anteil_pct"]) for x in e["fortschritt"]])


def suche(ausg, zins=None, extra=0.0):
    """Kleinster Satz, bei dem ein Drittel tragbar ist."""
    for ks in P["kapital"]["saetze"]:
        e = lauf(ks, ausg, zins, extra)
        if e["anteil_tragbar_pct"] >= A * 100 - 0.05:
            return kurz(e, ks)
    return dict(kapital_satz=None, hinweis=f"bis {P['kapital']['saetze'][-1]} % nicht tragbar", letzter=kurz(e, ks))


def main():
    k0 = kosten_basis()
    E = dict(version=P["version"], status="Prüfrechnung (Vorgaben 21.11.2026: Anteil ein Drittel, Boden höchstens 2 %, Nicht-Arbeit gleichmäßig, Übergang über den Fonds)",
             kapital_mehr_je_satz_pct_bip={})
    with contextlib.redirect_stdout(io.StringIO()):
        k38 = ST.kapital(38)[0]
        for ks in P["kapital"]["saetze"]:
            E["kapital_mehr_je_satz_pct_bip"][str(ks)] = dict(mehr_gegen_38=round(ST.kapital(ks)[0] - k38, 3), wachstum_gegen_38_pct_bip=round(ST.P["kapital"]["wachstum_je_punkt"] * (ks - 38), 2))
    E["referenz_38_voll"] = kurz(lauf(38, k0), 38)                    # Boden voll ab 2028, ohne Übergang
    faelle = {}
    for bis in P["uebergang"]["bis"]:
        u, info = uebergang(bis)
        ausg = {j: k0[j] - u[j] * -1 if False else k0[j] + u[j] for j in ME.JAHRE}   # u < 0 in Übergangsjahren: Fonds deckt; > 0: Rückzahlung
        ref = kurz(lauf(38, ausg), 38)
        faelle[f"Boden in Schritten bis {bis}, Fonds überbrückt"] = dict(uebergang=info, bei_38=ref, noetiger_satz=suche(ausg))
    E["faelle"] = faelle
    u, _ = uebergang(P["uebergang"]["bis"][0])
    ausg = {j: k0[j] + u[j] for j in ME.JAHRE}
    E["vermoegen_varianten"] = vermoegen()
    best = E["vermoegen_varianten"][-1]["DIW (mit Spitze)"]["mehr_gegen_heute_pct_bip"]
    low = E["vermoegen_varianten"][-1]["PHF 2021 (Befragung)"]["mehr_gegen_heute_pct_bip"]
    E["mit_vermoegen_2_pct_ab_1_mio"] = dict(diw=suche(ausg, extra=best), phf=suche(ausg, extra=low))
    E["vermoegen_je_variante"] = [dict(satz_pct=v["satz_pct"], schwelle_eur=v["schwelle_eur"],
                                       noetiger_satz_phf=suche(ausg, extra=v["PHF 2021 (Befragung)"]["mehr_gegen_heute_pct_bip"]).get("kapital_satz"),
                                       noetiger_satz_diw=suche(ausg, extra=v["DIW (mit Spitze)"]["mehr_gegen_heute_pct_bip"]).get("kapital_satz"))
                                  for v in E["vermoegen_varianten"]]
    E["zinsfall_3_0"] = dict(ohne_vermoegen=suche(ausg, zins=P["zinsfall"]["zins"]), mit_vermoegen_diw=suche(ausg, zins=P["zinsfall"]["zins"], extra=best))
    E["hinweis"] = ("Euro je Monat, Kaufkraft 2026, Deutschland. Satz gilt für Kapitalerträge, Unternehmen und Plattformen, Erbschaften; Mieteinkünfte stehen in der "
                    "Position Einkommen (Stufentarif) und sind nicht gesondert erhöht. Mehraufkommen und Investitionskanal wie stellschrauben/dynamik_satz (Annahmen). "
                    "Vermögensteuer: Pareto über P90, 50 % Ausweichen (Annahmen). Fondskredit in % BIP ohne Wachstumsentlastung (vorsichtig).")
    (AGG / "anteil_drittel.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(E["kapital_mehr_je_satz_pct_bip"], ensure_ascii=False))
    r = E["referenz_38_voll"]; print("38 voll", r["anteil_tragbar_pct"], r["ruecklage_min_pct_bip"], r["bip_2045_pct"])
    for k, v in faelle.items():
        print(k, v["uebergang"], "| bei 38:", v["bei_38"]["anteil_tragbar_pct"], v["bei_38"]["ruecklage_min_pct_bip"])
        n = v["noetiger_satz"]; print("   nötig", n.get("kapital_satz"), n.get("anteil_tragbar_pct"), n.get("ruecklage_min_pct_bip"), n.get("bip_2045_pct"), n.get("paket", {}).get("2028"), n.get("fortschritt"))
    print("Vermögen", json.dumps(E["vermoegen_varianten"], ensure_ascii=False))
    for k, v in E["mit_vermoegen_2_pct_ab_1_mio"].items(): print("mit Vermögen", k, v.get("kapital_satz"), v.get("anteil_tragbar_pct"), v.get("bip_2045_pct"))
    print("je Variante", E["vermoegen_je_variante"])
    for k, v in E["zinsfall_3_0"].items(): print("Zins 3,0", k, v.get("kapital_satz"), v.get("anteil_tragbar_pct"), v.get("bip_2045_pct"), v.get("hinweis"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
