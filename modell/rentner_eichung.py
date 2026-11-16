#!/usr/bin/env python3
"""Rentnerregel nach der Umstellung v4.97 neu eichen (Logbuch v4.98). Prüfrechnung, ändert die geltende Rechnung nicht.

1. Zerlegung: Wie viel der Verschlechterung der Rentnerhaushalte (BS35) stammt aus Tarif (Grundbedarf 12.072 €), Satz ein Drittel,
   Label +2 Punkte und Zuschlag? Je Baustein wird der Wert v4.96 zurückgesetzt (Reihenfolge Tarif, Satz, Label, Zuschlag).
2. Varianten R0–R4 (rentner_eichung.toml): Anteil mit mehr, Mittel, Fünftel, Kosten gegen BS35 in % BIP und Wirkung auf die Dividende der
   Erwerbstätigen (Kosten × Euro je BIP-Punkt; Näherung, ohne Rückwirkung auf den Zuschlag).
Rentnerhaushalte und Rechenweg wie rentner_kombi.py (mikro_rentner_de: EU-SILC 2025, ASID 2023). Ausgabe: daten/aggregate/rentner_eichung.json
"""
import contextlib, copy, importlib.util, io, json, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "rentner_eichung.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rk_e", W / "modell" / "rentner_kombi.py")
RK = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RK)
M, H, HL, A, DE, PK = RK.M, RK.H, RK.HL, RK.A, RK.DE, RK.P
BS = copy.deepcopy(H.P["rente_regel"])
NEU = dict(stufen=list(DE["tarif_stufen"]), eff=M.EFF, zu=M.ZU, saetze=list(RK.TARIF_C))
BODEN = PK["variante"][-1]["boden"]


def netto(g, n, eps, regel, ausgleich=0.0, k=NEU):
    p, an, b, v, e = (g * A[x] for x in ("grv", "andere", "bav", "privat", "erwerb"))
    zusage = p + an
    kb = H.kuerzung_bs35(zusage, H.jahre_zu(zusage, eps), regel)
    eink = zusage - kb + b + v + e + PK["weitergabe"] * H.ag(e)
    st = HL.stufen(eink, k["stufen"], k["saetze"]) * n
    y = eink * n - st
    kon = HL.kq(y, "DE") * y
    fm, fb = HL.mwst_phi("DE", y)
    y = y - fm * kon * ((1 + k["eff"] / 100) / (1 + HL.eff_alt("DE") / 100) - 1) - k["zu"] / 100 * (st + fb * kon * k["eff"] / (100 + k["eff"]))
    y += 12 * ausgleich * n
    bod = 12 * BODEN[n - 1]
    return max(y, bod), max(0.0, bod - y), kb * n


def main():
    R, gw = M.ziehe(np.random.default_rng(PK["seed"]), PK["stichprobe"], 18.0, 6.3)
    pre = [(M.brutto_aus_netto(r["netto_2024"] * 1.06 / r["n"], A), max(r["netto_2024"] * 1.06, M.bedarf_heute(r["n"])), r["n"], r["eps"]) for r in R]
    hs = np.array([h for _, h, _, _ in pre])
    grp = np.searchsorted(np.quantile(hs, [.2, .4, .6, .8]), hs)
    bip = PK["bip_2028_mrd"]

    def lauf(regel, ausgleich=0.0, k=NEU):
        x = [netto(g, n, e, regel, ausgleich, k) for g, h, n, e in pre]
        d = np.array([(y - h) / 12 for (y, _, _), (_, h, _, _) in zip(x, pre)])
        kosten = float(sum(w * 12 * ausgleich * n for w, (_, _, n, _) in zip(gw, pre)))   # Altersausgleich (Kasse)
        kb = float(sum(w * c for w, (_, _, c) in zip(gw, x)))
        bo = float(sum(w * a for w, (_, a, _) in zip(gw, x)))
        return dict(anteil_mehr_pct=round(float(gw[d > 0].sum() / gw.sum() * 100), 1), mittel_monat=round(float(np.average(d, weights=gw)), 1),
                    fuenftel_monat=[round(float(np.average(d[grp == i], weights=gw[grp == i]))) for i in range(5)],
                    kuerzung_mrd=kb / 1e9, boden_mrd=bo / 1e9, ausgleich_mrd=kosten / 1e9)

    # 1. Zerlegung
    al = P["alt"]
    stufen = [("alles wie v4.96", dict(stufen=al["tarif_stufen"], eff=al["label_eff"], zu=al["zuschlag"], saetze=al["saetze"])),
              ("+ Grundbedarf im Tarif 12.072 €", dict(stufen=NEU["stufen"], eff=al["label_eff"], zu=al["zuschlag"], saetze=al["saetze"])),
              ("+ Satz ein Drittel", dict(stufen=NEU["stufen"], eff=al["label_eff"], zu=al["zuschlag"], saetze=NEU["saetze"])),
              ("+ Label 7/13/19/27 (effektiv " + str(NEU["eff"]) + " %)", dict(stufen=NEU["stufen"], eff=NEU["eff"], zu=al["zuschlag"], saetze=NEU["saetze"])),
              ("+ Zuschlag DE " + str(NEU["zu"]) + " % (alles v4.97)", NEU)]
    zerl = []
    for name, k in stufen:
        r = lauf(BS, 0.0, k)
        zerl.append(dict(schritt=name, anteil_mehr_pct=r["anteil_mehr_pct"], mittel_monat=round(r["mittel_monat"])))
    for i in range(1, len(zerl)):
        zerl[i]["wirkung_mittel_monat"] = zerl[i]["mittel_monat"] - zerl[i - 1]["mittel_monat"]

    # 2. Varianten
    ziel = P["ziel_mittel_monat"]
    erg, basis = [], None
    for v in P["variante"]:
        art, para = v["art"], {}
        if art == "bs35":
            rg, au = BS, 0.0
        elif art == "saetze":
            f = lambda s: (dict(BS, satz=BS["satz"] * s, satz_oben=BS["satz_oben"] * s), 0.0)
            lo, hi = 0.0, 1.0
            for _ in range(40):
                m = (lo + hi) / 2
                (lo, hi) = (lo, m) if lauf(*f(m))["mittel_monat"] < ziel else (m, hi)
            s = (lo + hi) / 2; rg, au = f(s); para = dict(faktor_saetze=round(s, 3), satz=round(rg["satz"] * 100, 1), satz_oben=round(rg["satz_oben"] * 100, 1))
        elif art == "freibetrag":
            f = lambda s: (dict(BS, sockel=BS["sockel"] * s, faktor=BS["faktor"] * s), 0.0)
            lo, hi = 1.0, 4.0
            for _ in range(40):
                m = (lo + hi) / 2
                (lo, hi) = (m, hi) if lauf(*f(m))["mittel_monat"] < ziel else (lo, m)
            s = (lo + hi) / 2; rg, au = f(s)
            G = BS["freibetrag_monat"]
            para = dict(faktor_freibetrag=round(s, 3), sockel_monat=round(rg["sockel"] * G), voll_monat=round(rg["faktor"] * G))
        elif art == "oben":
            rg, au = dict(BS, satz_oben=v["satz_oben"]), 0.0
            para = dict(satz_oben=v["satz_oben"] * 100)
        elif art == "ausgleich":
            lo, hi = 0.0, 300.0
            for _ in range(40):
                m = (lo + hi) / 2
                (lo, hi) = (m, hi) if lauf(BS, m)["mittel_monat"] < ziel else (lo, m)
            rg, au = BS, (lo + hi) / 2; para = dict(ausgleich_person_monat=round(au))
        r = lauf(rg, au)
        netto_staat = r["kuerzung_mrd"] - r["boden_mrd"] - r["ausgleich_mrd"]
        basis = netto_staat if basis is None else basis
        kosten = (basis - netto_staat) / bip * 100
        erg.append(dict(id=v["id"], name=v["name"], parameter=para, anteil_mehr_pct=r["anteil_mehr_pct"], mittel_monat=round(r["mittel_monat"]),
                        fuenftel_monat=r["fuenftel_monat"], kuerzung_mrd=round(r["kuerzung_mrd"], 1), boden_mrd=round(r["boden_mrd"], 1),
                        ausgleich_mrd=round(r["ausgleich_mrd"], 1), kosten_gegen_r0_mrd=round(basis - netto_staat, 1), kosten_gegen_r0_pct_bip=round(kosten, 2),
                        dividende_erw_monat_eur=round(-kosten * P["eur_je_bip_punkt_2028"])))
    E = dict(version=P["version"], status="Prüfrechnung (2028, Kaufkraft 2026); geltend bleibt BS35 bis zur Entscheidung", zerlegung_v496_v497=zerl,
             ziel_mittel_monat=ziel, varianten=erg,
             hinweis="Rentner erhalten keine Dividende zusätzlich (Korrektur 65); deshalb wirken Label, Tarif und Zuschlag voll. Kosten nur 2028 und nur DE; "
                     "Wirkung auf die Dividende als Näherung ohne Rückwirkung auf Zuschlag und Fonds der 30. Versicherungsjahre zugeschätzt (Annahme, v4.69).")
    (W / "daten" / "aggregate" / "rentner_eichung.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for z in zerl:
        print(z)
    for x in erg:
        print(x["id"], x["parameter"], x["anteil_mehr_pct"], x["mittel_monat"], x["fuenftel_monat"], x["kosten_gegen_r0_pct_bip"], x["dividende_erw_monat_eur"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
