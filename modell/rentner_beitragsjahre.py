#!/usr/bin/env python3
"""Rentner: Kürzung nach Zusage je Versicherungsjahr (Logbuch v4.69; Sockel v4.71). Entwicklungsmodus, vorläufige Prüfrechnung, kein Beschluss.

Regel B: Jedes Versicherungsjahr schützt einen festen Teil der Zusage. Freibetrag F = min(Jahre, 45)/45 × f × G (G = Grundbedarf des
Staates). Gekürzt wird nur der Teil der Zusage über F, mit einem Satz s, der so gesucht wird, dass der Fonds so viel entlastet wird wie
unter Regel E (rentner_varianten.py). Vergleich mit E und N2/3 (Stufen nach der Höhe der Zusage allein).

Daten: Das Haushaltsmodell (rentner_kombi.py, EU-SILC 2025/ASID 2023) enthält keine Versicherungsjahre. Sie werden zugeschätzt
(Annahme): latente Jahre = a + b · ln(Zusage/Mittel) + c · Zufall, begrenzt auf 0–50; a, b, c so gewählt, dass Anteile und mittlere
Zusagen der Klassen unter 40 / 40–45 / ab 45 Jahren den Bestandszahlen der Rentenversicherung 2024 entsprechen (Rentenversicherungsbericht
2025, Übersichten A 3.1/A 3.2). Abgebildet wird damit nur der Zusammenhang Höhe–Jahre im Mittel, nicht die Streuung im Einzelfall
außerhalb der Kalibrierung; Beamte sind im Modell nicht getrennt (gleiche Zuschätzung).
Ausgabe: daten/aggregate/rentner_beitragsjahre.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "rentner_beitragsjahre.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rv", W / "modell" / "rentner_varianten.py")
RV = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RV)
RK, M, A, G = RV.RK, RV.M, RV.A, RV.G
VOLL = P["volle_laufbahn"]


def ziele():
    """Anteile und Mittel-Verhältnisse der Klassen <40, 40–45, ≥45 aus dem Rentenversicherungsbericht (Männer und Frauen zusammen)."""
    r = P["rvb2025"]
    n_all = r["maenner_alle"][0] + r["frauen_alle"][0]
    s_all = r["maenner_alle"][0] * r["maenner_alle"][1] + r["frauen_alle"][0] * r["frauen_alle"][1]
    n40 = r["maenner_ab40"][0] + r["frauen_ab40"][0]
    s40 = r["maenner_ab40"][0] * r["maenner_ab40"][1] + r["frauen_ab40"][0] * r["frauen_ab40"][1]
    n45 = r["maenner_ab45"][0] + r["frauen_ab45"][0]
    s45 = r["maenner_ab45"][0] * r["maenner_ab45"][1] + r["frauen_ab45"][0] * r["frauen_ab45"][1]
    m = s_all / n_all
    anteile = [(n_all - n40) / n_all, (n40 - n45) / n_all, n45 / n_all]
    mittel = [(s_all - s40) / (n_all - n40) / m, (s40 - s45) / (n40 - n45) / m, s45 / n45 / m]
    return anteile, mittel, dict(mittel_alle=round(m), mittel_klassen=[round(x * m) for x in mittel])


def klassen(jahre, z, w, zbar):
    k = np.digitize(jahre, [40, 45])
    an = [float(w[k == i].sum() / w.sum()) for i in range(3)]
    mi = [float(np.average(z[k == i], weights=w[k == i]) / zbar) if (k == i).any() else 0.0 for i in range(3)]
    return an, mi


def main():
    R, gw = M.ziehe(np.random.default_rng(RK.P["seed"]), RK.P["stichprobe"], 18.0, 6.3)
    pre = []
    for r in R:
        nh = r["netto_2024"] * 1.06
        pre.append((M.brutto_aus_netto(nh / r["n"], A), max(nh, M.bedarf_heute(r["n"])), r["n"]))
    zp = np.array([g * (A["grv"] + A["andere"]) for g, _, _ in pre])
    wp = gw * np.array([n for _, _, n in pre])                    # Personengewicht
    zbar = float(np.average(zp, weights=wp))
    eps = np.random.default_rng(P["seed_jahre"]).standard_normal(len(zp))
    lz = np.log(np.maximum(zp, 1.0) / zbar)

    # Kalibrierung (Gittersuche): Abweichung der Anteile und Mittelverhältnisse
    an_z, mi_z, info = ziele()
    best = None
    for a in np.arange(36.0, 46.01, 0.25):
        for b in np.arange(0.0, 20.01, 0.5):
            for c in np.arange(2.0, 14.01, 0.5):
                j = np.clip(a + b * lz + c * eps, 0, 50)
                an, mi = klassen(j, zp, wp, zbar)
                f = sum((x - y) ** 2 for x, y in zip(an, an_z)) + sum((x - y) ** 2 for x, y in zip(mi, mi_z)) * 0.25
                if best is None or f < best[0]:
                    best = (f, a, b, c, an, mi)
    _, a, b, c, an, mi = best
    jahre = np.clip(a + b * lz + c * eps, 0, 50)
    kal = dict(a=round(a, 2), b=round(b, 2), c=round(c, 2), ziel_anteile=[round(x, 3) for x in an_z], modell_anteile=[round(x, 3) for x in an],
               ziel_mittel_relativ=[round(x, 3) for x in mi_z], modell_mittel_relativ=[round(x, 3) for x in mi], rvb2025=info)

    boden = P["boden"]
    rows = list(zip(pre, jahre))

    def rechne(kf):
        out = [RV.neu(g, n, None, boden, kfun=(lambda z, J=J: kf(z, J))) for (g, h, n), J in rows]
        d = np.array([(y - h) / 12 for ((g, h, n), _), (y, _, _) in zip(rows, out)])
        auf = np.array([o[1] for o in out]); kb = np.array([o[2] for o in out])
        return d, float((gw * (kb - auf)).sum())

    ref_E = None
    zgr = np.searchsorted([1.0 * G, 1.5 * G, 2.0 * G, 3.0 * G], zp)
    jgr = np.digitize(jahre, [35, 40, 45])
    ZL = ["bis 1 G", "1–1,5 G", "1,5–2 G", "2–3 G", "über 3 G"]
    JL = ["unter 35 J.", "35–40 J.", "40–45 J.", "ab 45 J."]

    def kennzahlen(name, d, netto, extra):
        def anteil(m):
            return round(float(gw[m & (d > 0)].sum() / gw[m].sum() * 100)) if m.any() else None

        def mittel(m):
            return round(float(np.average(d[m], weights=gw[m]))) if m.any() else None
        lang_mittel = (jahre >= 40) & (zp <= 2 * G)
        kurz_hoch = (jahre < 35) & (zp > 2 * G)
        kurz_niedrig = (jahre < 35) & (zp <= 1.5 * G)
        return dict(name=name, **extra, anteil_mehr_pct=round(float(gw[d > 0].sum() / gw.sum() * 100), 1),
                    mittel_monat=round(float(np.average(d, weights=gw))),
                    lange_laufbahn_bis_2G=dict(anteil_mehr_pct=anteil(lang_mittel), mittel_monat=mittel(lang_mittel),
                                               anteil_personen_pct=round(float(wp[lang_mittel].sum() / wp.sum() * 100))),
                    kurze_laufbahn_ueber_2G=dict(anteil_mehr_pct=anteil(kurz_hoch), mittel_monat=mittel(kurz_hoch),
                                                 anteil_personen_pct=round(float(wp[kurz_hoch].sum() / wp.sum() * 100))),
                    kurze_laufbahn_bis_1_5G=dict(anteil_mehr_pct=anteil(kurz_niedrig), mittel_monat=mittel(kurz_niedrig),
                                                 anteil_personen_pct=round(float(wp[kurz_niedrig].sum() / wp.sum() * 100))),
                    nach_jahren={JL[i]: dict(mehr_pct=anteil(jgr == i), mittel=mittel(jgr == i)) for i in range(4)},
                    nach_zusage={ZL[i]: dict(mehr_pct=anteil(zgr == i), mittel=mittel(zgr == i)) for i in range(5)},
                    matrix_mehr_pct={JL[j]: {ZL[i]: anteil((jgr == j) & (zgr == i)) for i in range(5)} for j in range(4)},
                    entlastung_fonds_mrd=round(netto / 1e9, 1),
                    gegen_E_mrd=None if ref_E is None else round((netto - ref_E) / 1e9, 1))

    erg = []
    # Bezüge: E und N2/3 aus rentner_varianten (gleiche Stufen)
    rv = json.loads((W / "daten" / "aggregate" / "rentner_varianten.json").read_text(encoding="utf-8"))
    bez = {"E": rv["varianten"][0]["stufen"], "N2/3": next(v["stufen"] for v in rv["varianten"] if v["name"].startswith("N2/3"))}
    for nm, st in bez.items():
        st = [tuple(x) for x in st]
        d, netto = rechne(lambda z, J, st=st: RV.kuerzung(z, st))
        if ref_E is None:
            ref_E = netto
        faelle = {c["name"]: round(RV.kuerzung(12 * c["betrag"], st) / 12) for c in P["fall"]}
        erg.append(kennzahlen(nm, d, netto, dict(stufen=st, kuerzung_faelle_monat=faelle)))

    for v in P["variante"]:
        f, br, fa, vo, so = v["f"], v.get("breite"), v.get("faktor", 1.0), v.get("voll", VOLL), v.get("sockel", 0.0)

        def kf(z, J, s):
            F = max(so * G, min(J, vo) / vo * f * G)          # Sockel (v4.71): Freibetrag nie unter so × G
            if br is None:
                return s * max(0.0, z - F)
            return s * max(0.0, min(z, F + br * G) - F) + min(0.95, fa * s) * max(0.0, z - F - br * G)
        lo, hi = 0.0, 0.95
        for _ in range(30):
            s = (lo + hi) / 2
            d, netto = rechne(lambda z, J, s=s: kf(z, J, s))
            lo, hi = (lo, s) if netto > ref_E else (s, hi)
        faelle = {c["name"]: round(kf(12 * c["betrag"], c["jahre"], s) / 12) for c in P["fall"]}
        erg.append(kennzahlen(v["name"], d, netto, dict(f=f, voll=vo, sockel=so, kuerzung_faelle_monat=faelle, satz=round(s, 3), satz_oben=round(min(0.95, fa * s), 3) if br else None,
                                                         freibetrag_45_jahre_monat=round(f * G / 12), je_jahr_monat=round(f * G / 12 / VOLL, 1))))

    E = dict(version=P["version"], status="Entwicklungsmodus: vorläufige Prüfrechnung (Deutschland, 2028, Kaufkraft 2026), kein Beschluss",
             grundbedarf_monat=round(G / 12), kalibrierung_jahre=kal, varianten=erg,
             hinweis="Versicherungsjahre zugeschätzt (Annahme), kalibriert an Rentenversicherungsbericht 2025 Übersichten A 3.1/A 3.2 "
                     "(Bestand 31.12.2024, maschinell aus dem PDF gelesen). Freibetrag F = min(Jahre,45)/45 × f × G; Kürzung auf den Teil "
                     "über F; Satz neutral zur Entlastung des Fonds unter E gesucht. Gruppen nach Zusage je Person und zugeschätzten Jahren.")
    # v4.72: Übertrag in die geltende Regel prüfen (haushalte33.rente_regel = BS35, rente_jahre = Kalibrierung)
    H = RK.H
    bs = next(x for x in erg if x["name"].startswith("BS35"))
    rr, rj = H.P["rente_regel"], H.P["rente_jahre"]
    E["uebertrag_regel"] = dict(satz=bs["satz"], satz_oben=bs["satz_oben"], toml_satz=rr["satz"], toml_satz_oben=rr["satz_oben"],
                                kalibrierung=[kal["a"], kal["b"], kal["c"]], toml_kalibrierung=[rj["a"], rj["b"], rj["c"]])
    if abs(bs["satz"] - rr["satz"]) > 0.0005 or abs(bs["satz_oben"] - rr["satz_oben"]) > 0.0015 or \
            any(abs(x - y) > 1e-9 for x, y in zip(E["uebertrag_regel"]["kalibrierung"], E["uebertrag_regel"]["toml_kalibrierung"])):
        raise SystemExit(f"haushalte33.rente_regel / rente_jahre veraltet: {E['uebertrag_regel']}")
    (W / "daten" / "aggregate" / "rentner_beitragsjahre.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Kalibrierung", kal)
    for x in erg:
        print(f"{x['name'][:50]:50} mehr {x['anteil_mehr_pct']:5}% Satz {x.get('satz')} lang≤2G {x['lange_laufbahn_bis_2G']} "
              f"kurz>2G {x['kurze_laufbahn_ueber_2G']} Fonds {x['entlastung_fonds_mrd']} gegen E {x['gegen_E_mrd']}")
        print("   ", x["nach_jahren"])
        print("   ", x["nach_zusage"])
        print("   ", x["kuerzung_faelle_monat"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
