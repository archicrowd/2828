#!/usr/bin/env python3
"""Satz und Puffer für eine auf Dauer leicht steigende Dividende (Logbuch v4.100). Prüfrechnung, ändert die geltende Rechnung nicht.

Je einheitlichem Satz s (quote_optimum.toml) und je Variante:
  Label  A: Label und Sonderstufen mit s skaliert;  B: Label fest 7/13/19/27 + Sonderstufe ein Drittel (Beschluss 16.11.2026)
  Regel  0: wie geltend, die Dividende ist Restgröße;  L: Lenkungsabgaben (CO₂, Sonderstufen, Verbrauchsteuern) gehen an den Fonds,
            der Fondsbeitrag aus den übrigen Steuern sinkt um ihre barwertgleiche Konstante; die Dividende erhält diese Konstante statt des
            fallenden Pfads (gleiche Gesamtlast über die Laufzeit des Fonds)
Deckung wie systemvarianten (33R), Einkommen mit eti; Kapital, Unternehmen, Erbschaft mit Verhaltensfaktoren des Kernmodells (Robust);
Pfad wie projektion33 (Verteidigung, Lenkung, Gesundheit, Progression, Dynamik). Ausgaben (Gemeinwesen, Netz, Verwaltung) unverändert;
Puffer als jährliche Ausgleichsrücklage. Ausgabe: daten/aggregate/quote_optimum.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
Q = tomllib.loads((W / "modell" / "quote_optimum.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("pj", W / "modell" / "projektion33.py")
PJ = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(PJ)
SVM, V = PJ.SVM, PJ.v
BASIS33 = dict(PJ.sy)
S0 = 33.333333
R = SVM.KERN.SZ["Robust"]
GL = json.loads((AGG / "gesamtlast33.json").read_text(encoding="utf-8"))
FONDS, ZUSCHLAG = GL["fonds"]["beitrag_pct_bip"], GL["fonds"]["zuschlag_pct"]


def system(s, label_mit):
    k = s / S0
    sy = dict(BASIS33, spitzensatz=s, einkommen_saetze=[x * k for x in BASIS33["einkommen_saetze"]])
    if label_mit:
        sy["label_saetze"] = [x * k for x in BASIS33["label_saetze"]]
        sy["label_sonder"] = {g: x * k for g, x in BASIS33["label_sonder"].items()}
    return sy


def deckung(sy):
    pos, eff = SVM.deckung(sy)
    s, t0 = sy["spitzensatz"], S0 / 100
    t = s / 100
    pos["Kapitalerträge"] *= ((1 - t) / (1 - t0)) ** R["eps"]
    pos["Unternehmen und Plattformen"] *= (s / S0) * math.exp(-R["semi"] * (s - S0) / 100)
    pos["Erbschaften"] *= (s / S0) * math.exp(-(s - S0) / 100)
    return pos, eff


def pfad(sy, regel, puffer, extra_ausgaben=0.0):
    PJ.sy.clear(); PJ.sy.update(sy); PJ._PROG.clear()
    pos, eff0 = deckung(sy)
    deck0 = sum(pos.values())
    eff_check = PJ.label(2028)
    eich = SVM.konsum(eff0) / SVM.konsum(eff_check)
    PJ.KONSUM_EICH = eich
    bedarf_ohne_div = V["punkte"]["2028"]["steuerbedarf"] - V["dividende_pct_bip_2028"] + extra_ausgaben
    k = SVM.G["anteil_minderjaehrige"] / 100
    f = PJ.P["preis_2026_zu_2028"]
    basis = {r["jahr"]: r for r in SVM.GR.pfad(V["quote_kern"], i_alt=0.0, i_ziel=0.0)}
    f_erw = SVM.GR.F_DE / (1 - k / 2) / f
    reihe, lenk = [], {}
    for j in range(2028, 2061):
        eff = max(PJ.label(j), eff_check)
        konsum = SVM.konsum(eff) * eich
        co2 = pos["CO₂-Preis"] * PJ.lin("co2_index", j)
        verbr = (PJ.P["energiesteuer_kraftstoffe_pct_bip"] * (1 - PJ.lin("kraftstoffe", j))
                 + PJ.P["tabak_alkohol_steuer_pct_bip"] * (1 - PJ.lin("alkohol_tabak", j)))
        deck = deck0 - pos["Konsum (Label)"] - pos["CO₂-Preis"] + konsum + co2 - verbr
        lenk[j] = co2 + konsum - PJ.konsum_ohne_sonder(j) + PJ.P["energiesteuer_kraftstoffe_pct_bip"] * PJ.lin("kraftstoffe", j) \
            + PJ.P["tabak_alkohol_steuer_pct_bip"] * PJ.lin("alkohol_tabak", j)
        b = basis[j]
        kopf = PJ.DG.get(j, 1.0)
        f_real = (b["kl_real"] / b["div"]) / (basis[2028]["kl_real"] / basis[2028]["div"]) * kopf
        prog = pos["Einkommen"] * (PJ.progression(f_real ** (1 - PJ.P["stufen_lohnanteil"])) - 1)
        da = b["a"] - basis[2028]["a"]                                   # Verteidigungspfad
        gp = PJ.lin("gesundheit_pflege_plus", j)
        steuern = deck + prog
        div = steuern - bedarf_ohne_div - da - gp - puffer
        reihe.append(dict(jahr=j, steuern=steuern, div=div, eur_je_punkt=b["kl_real"] * f_erw * kopf / b["div"]))
    lbar = 0.0
    if regel == "L":                                                     # barwertgleiche Konstante der Lenkung bis zum Zieljahr
        q = (1 + Q["wachstum_nominal"]) / (1 + Q["fonds_zins"])
        ws = [(q ** (j - 2028), lenk.get(j, lenk[2060])) for j in range(2028, Q["fonds_zieljahr"] + 1)]
        lbar = sum(w * x for w, x in ws) / sum(w for w, _ in ws)
        for r in reihe:
            r["div"] += lbar - lenk[r["jahr"]]
    for r in reihe:
        r["eur"] = r["div"] * r["eur_je_punkt"]
    e = {r["jahr"]: r["eur"] for r in reihe}
    ab35 = [e[j + 1] - e[j] for j in range(2035, 2060)]
    ok = min(ab35) >= -0.5 and e[2060] >= e[2028]
    # Glättung: Dividende wächst real mit g je Jahr ab D0; Überschuss früher Jahre in die Rücklage (ohne Zins, vorsichtig);
    # D0 so hoch, dass die Rücklage bis 2060 nie negativ wird
    glatt = {}
    for g in Q["glaettung_wachstum"]:
        lo, hi = 0.0, 1000.0
        for _ in range(50):
            d0 = (lo + hi) / 2
            rl, ok_g = 0.0, True
            for r in reihe:
                rl += r["div"] - d0 * (1 + g) ** (r["jahr"] - 2028) / r["eur_je_punkt"]
                ok_g &= rl >= -1e-9
            lo, hi = (d0, hi) if ok_g else (lo, d0)
        rl, rmax = 0.0, 0.0
        for r in reihe:
            rl += r["div"] - lo * (1 + g) ** (r["jahr"] - 2028) / r["eur_je_punkt"]
            rmax = max(rmax, rl)
        glatt[str(g)] = dict(d0_eur2026=round(lo), d2060_eur2026=round(lo * (1 + g) ** 32), ruecklage_hoechst_pct_bip=round(rmax, 2))
    s28 = reihe[0]["steuern"]
    zuschlag_neu = FONDS / s28 * 100        # Gesamtlast unverändert: Zuschlag bleibt 5,32 % BIP; bei Regel L gehen davon L̄ an die Dividende
    return dict(steuern_2028=round(s28, 2), steuern_2060=round(reihe[-1]["steuern"], 2), lenkung_2028=round(lenk[2028], 2), lenkung_konstante=round(lbar, 2),
                dividende_pct_bip={str(j): round(next(r["div"] for r in reihe if r["jahr"] == j), 2) for j in (2028, 2035, 2040, 2050, 2060)},
                dividende_eur2026={str(j): round(e[j]) for j in (2028, 2035, 2040, 2050, 2060)}, min_eur=round(min(e.values())),
                kriterium_erfuellt=ok, glaettung=glatt, zuschlag_pct=round(zuschlag_neu, 1), effektiver_spitzensatz=round(sy["spitzensatz"] * (1 + zuschlag_neu / 100), 1),
                last_steuern_und_fonds_2028=round(s28 + FONDS, 2), fonds_aus_zuschlag_pct_bip=round(FONDS - lbar, 2))


def main():
    erg = []
    for s in Q["saetze"]:
        for lab in (True, False):
            for regel in ("0", "L"):
                sy = system(s, lab)
                r = pfad(sy, regel, Q["puffer_pct_bip"])
                r.update(satz=round(s, 2), label="A mit s" if lab else "B fest", regel=regel)
                erg.append(r)
    # Empfindlichkeit Staatsebene für Label B, Regel L
    sens = []
    for s in Q["saetze"]:
        r = pfad(system(s, False), "L", Q["puffer_pct_bip"], Q["staatsebene_pct_bip"])
        r.update(satz=round(s, 2), label="B fest", regel="L", staatsebene=Q["staatsebene_pct_bip"])
        sens.append(r)
    geltend = pfad(system(S0, False), "0", V["punkte"]["2028"]["saldo"])
    PJ.sy.clear(); PJ.sy.update(BASIS33); PJ._PROG.clear()
    E = dict(version=Q["version"], status="Prüfrechnung (Auftrag 18.11.2026); geltende Rechnung unverändert", kriterium=Q["kriterium"],
             puffer_pct_bip=Q["puffer_pct_bip"], gegenprobe_geltend=geltend, varianten=erg, empfindlichkeit_staatsebene=sens,
             hinweis="% BIP; Euro je Erwachsenem und Monat, Kaufkraft 2026, Deutschland, mit Dynamik. Verhalten nur über die Elastizitäten des Kernmodells "
                     "(Robust); Label ohne Verhaltensreaktion. Regel L: Zuschlag bleibt 5,32 % BIP, davon gehen L̄ an die Dividende, der Fonds erhält dafür die Lenkung (Barwert bei Fondszins "
                     "2,45 % und Wachstum 3 % nominal; Lenkung nach 2060 konstant, Annahme).")
    (AGG / "quote_optimum.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("geltend", geltend["dividende_eur2026"], geltend["steuern_2028"])
    for r in erg + sens:
        print(f"{r['satz']:>6} {r['label']:<7} {r['regel']} {'+Staat' if 'staatsebene' in r else '      '} St28 {r['steuern_2028']:>5} Div% {r['dividende_pct_bip']} EUR {r['dividende_eur2026']} ok={r['kriterium_erfuellt']} glatt {r['glaettung']} Lbar {r['lenkung_konstante']} Zu {r['zuschlag_pct']} eff {r['effektiver_spitzensatz']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
