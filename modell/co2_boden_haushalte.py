#!/usr/bin/env python3
"""Hintergrundrechnung CO₂ und Bodenabgabe für Modell E (fester Anteil 30 % des Grundbedarfs), Logbuch v4.105. Prüfrechnung.

1. Haushalte 2028 (mikro_de, Kaufkraft 2026): Modell E mit Baranteil 30 % des Grundbedarfs, dazu
   CO₂: direkte Kosten (Heizen, Kraftstoffe) nach dem Emissionsprofil je Quintil, indirekte über die Preise nach dem Konsum (Mehr gegen heute);
   Boden: Eigentümer (Quote nach Alter und Rang) zahlen 2 % des kapitalisierten Bodenwerts statt der heutigen Grundsteuer; Mieter sparen die
   heutige Umlage (Variante: Umlage bleibt erlaubt); Vermieter tragen die Abgabe auf vermieteten Boden; Rentner mit Altersausgleich R4,
   Eigentümer ab 65 mit Stundung.
2. Fiskalisch: Stundungsbestand und Zinsvorteil; Einschleifen der Bodenabgabe bis 2037; Wirkung auf den festen Anteil (modell_e.rechne).
3. Vermögenswirkung: Wertverlust des Bodens durch Kapitalisierung.
Ausgabe: daten/aggregate/co2_boden_haushalte.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "co2_boden_haushalte.toml").read_text(encoding="utf-8"))


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / datei)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


ME = lade("me_h", "modell_e.py")
S38, MD, QO, ST = ME.S38, ME.MD, ME.QO, ME.ST
BIP = P["bip_2028_kaufkraft_2026_mrd"]
F24 = BIP / P["boden"]["bip_2024_mrd"]                         # Bodenwert 2024 → 2028 in Kaufkraft 2026 (wächst mit dem BIP, Annahme)


def gew_quantil(x, w, q):
    o = np.argsort(x)
    c = np.cumsum(w[o]) / w.sum()
    return x[o][np.searchsorted(c, q)]


def main():
    a = P["anteil_fest"]
    D = ME.ziel_eur(P["jahr"], a)                               # Dividende je Erwachsenem vor Kinderanteil
    steuern_e = 31.17 + sum(ME.SCHRAUBEN[n]["wirkung"][2028] for n in ("Boden 2.0 %", "Kapital 38 %", "Subventionen mittel")) + ST.P["co2"]["k3_minus_k2_2028"]
    f = (QO.FONDS / steuern_e) / (QO.FONDS / 31.22)
    S38.setze(D, f, 1.0)
    pop = MD.ziehe(MD.P["seeds"][0], MD.P["partner"]["basis_korrelation"])
    hh, rr = pop[0], pop[1]
    w, wr, _ = MD.eiche(*pop)
    wg = MD.P["szenarien"]["basis_weitergabe"]
    Z = MD.rechne(hh, rr, w, wr, [wg])
    S38.setze()
    assert len(Z) == len(hh) + len(rr)
    n = len(Z)
    wv = np.array([z["w"] for z in Z]); pv = np.array([z["p"] for z in Z])
    aeq = np.array([z["aeq"] for z in Z]); y0 = np.array([z["heute"] for z in Z]); y1 = np.array([z["neu"][wg][0] for z in Z])
    rent = np.array([z["status"] == "Rentner" for z in Z])
    miete = np.array([hh[i].get("miete", 0.0) * MD.P["lohn_2024_2026"] if i < len(hh) else 0.0 for i in range(n)])
    # Rang (Personen gewichtet) im Äquivalenzeinkommen heute
    o = np.argsort(aeq); cum = np.empty(n); cum[o] = np.cumsum((wv * pv)[o]) / (wv * pv).sum()
    quint = np.minimum((cum * 5).astype(int), 4)
    dez = np.minimum((cum * 10).astype(int), 9)
    # ---------------- CO₂
    C = P["co2"]
    mt28 = C["direkt_mt_2024"] * (1 - C["rueckgang"]) ** 4
    prof = np.array(C["profil_quintil"])[quint]
    e_hh = prof * mt28 * 1e6 / float((wv * prof).sum())         # t je Haushalt, skaliert auf die Summe 2028
    co2_dir = e_hh * (C["preis_neu"] - C["preis_heute"]) * (1 + C["aufschlag_label"])
    ind_mrd = (C["aufkommen_neu_pct_bip"] - C["aufkommen_heute_pct_bip"]) / 100 * BIP - mt28 * (C["preis_neu"] - C["preis_heute"]) / 1000
    kons = np.array([MD.HL.kq(max(y, 1.0), "DE") * max(y, 1.0) for y in y1])
    co2_ind = ind_mrd * 1e9 * C["anteil_haushalte_indirekt"] * kons / float((wv * kons).sum())
    co2 = co2_dir + co2_ind
    # ---------------- Boden
    B = P["boden"]
    v0_rate = B["grundsteuer_mrd_2024"] / (P["boden"]["haushalte_mrd_2024"] + 1598.5)     # heutige Grundsteuer je € Bodenwert (≈ 0,24 %)
    t_neu_eff = B["satz_neu"] * B["r"] / (B["r"] + B["satz_neu"] - v0_rate)   # 2 % auf den kapitalisierten Wert (Korrektur 97: gegen den heutigen Satz)
    wertverlust = 1 - t_neu_eff / B["satz_neu"]
    d_rate = t_neu_eff - v0_rate                                   # Mehr je € heutigem Bodenwert und Jahr
    # Eigentümerquote je Zeile: logistisch im Rang, Mittel je Altersgruppe getroffen
    def quote(mask, ziel):
        lo, hi = -10.0, 10.0
        for _ in range(60):
            c = (lo + hi) / 2
            p_ = 1 / (1 + np.exp(-(c + B["steigung"] * (cum - 0.5))))
            m = float((wv[mask] * p_[mask]).sum() / wv[mask].sum())
            lo, hi = (c, hi) if m < ziel else (lo, c)
        return 1 / (1 + np.exp(-((lo + hi) / 2 + B["steigung"] * (cum - 0.5))))
    p_own = np.where(rent, quote(rent, B["quote_65plus"]), quote(~rent, B["quote_unter65"]))
    eig_mio = float((wv * p_own).sum() / 1e6)
    v_selbst = B["haushalte_mrd_2024"] * B["anteil_selbstgenutzt"] * F24 * 1e9
    g = np.power(np.maximum(aeq, 1.0), B["bodenwert_elastizitaet"])
    v_hh = v_selbst * g / float((wv * p_own * g).sum())          # heutiger Bodenwert je Eigentümerhaushalt
    boden_eig = d_rate * v_hh                                     # Mehr je Jahr für Eigentümer
    v_verm = (B["haushalte_mrd_2024"] * (1 - B["anteil_selbstgenutzt"]) * F24 * 1e9)
    boden_verm = d_rate * v_verm * B["anteil_vermieter_in_mikro"] * miete / max(float((wv * miete).sum()), 1.0)
    mieter_heute = v0_rate * (v_verm + B["wohnungsunternehmen_mrd_2024"] * F24 * 1e9) / float((wv * (1 - p_own)).sum())   # heutige Umlage je Mieterhaushalt
    mieter_umlage_neu = t_neu_eff * (v_verm + B["wohnungsunternehmen_mrd_2024"] * F24 * 1e9) / float((wv * (1 - p_own)).sum())
    # ---------------- Rentner: Altersausgleich R4
    r4 = np.where(rent, P["rentner"]["altersausgleich_person_monat"] * 12 * pv, 0.0)
    # ---------------- Fälle: Eigentümer und Mieter als gewichtete Teilfälle
    def auswertung(mit_co2, mit_boden, stundung=True, umlage=False, mit_r4=True):
        W_ = np.concatenate([wv * p_own, wv * (1 - p_own)])
        base = np.concatenate([y1, y1]) + (np.concatenate([r4, r4]) if mit_r4 else 0.0)
        last = np.zeros(2 * n)
        if mit_co2:
            last += np.concatenate([co2, co2])
        if mit_boden:
            eig = boden_eig * np.where(rent & stundung, 0.0, 1.0)
            mie = (mieter_umlage_neu - mieter_heute) if umlage else -mieter_heute
            last += np.concatenate([eig + boden_verm, np.full(n, mie) + boden_verm])
        d = (base - last - np.concatenate([y0, y0])) / 12
        r2_ = np.concatenate([rent, rent]); dz = np.concatenate([dez, dez])
        eigm = np.concatenate([np.ones(n, bool), np.zeros(n, bool)])
        def st(mask):
            return dict(mit_mehr_pct=round(float(W_[mask & (d > 0)].sum() / W_[mask].sum() * 100), 1), mittel_eur=round(float((W_[mask] * d[mask]).sum() / W_[mask].sum())))
        alle = np.ones(2 * n, bool)
        return dict(gesamt=st(alle), erwerbsalter=st(~r2_), rentner=st(r2_), rentner_eigentuemer=st(r2_ & eigm), rentner_mieter=st(r2_ & ~eigm),
                    eigentuemer=st(eigm), mieter=st(~eigm), dezile=[st(dz == i) for i in range(10)])
    faelle = {
        "E ohne CO₂ und Boden (wie Mikrosimulation)": auswertung(False, False),
        "E mit CO₂": auswertung(True, False),
        "E mit CO₂ und Boden (Stundung ab 65, keine Umlage)": auswertung(True, True),
        "E mit CO₂ und Boden ohne Stundung": auswertung(True, True, stundung=False),
        "E mit CO₂ und Boden, Umlage auf Mieter erlaubt": auswertung(True, True, umlage=True),
        "E mit CO₂ und Boden, ohne Altersausgleich": auswertung(True, True, mit_r4=False),
    }
    ww = lambda x, m=None: float((wv * x).sum() / wv.sum()) if m is None else float((wv[m] * x[m]).sum() / wv[m].sum())
    # CO₂ je Dezil (Monat) und in % des Nettoeinkommens heute
    co2_dez = [dict(dezil=i + 1, eur_monat=round(ww(co2, dez == i) / 12), anteil_netto_pct=round(ww(co2, dez == i) / ww(y0, dez == i) * 100, 2)) for i in range(10)]
    # ---------------- Stundung (fiskalisch)
    S_ = P["stundung"]
    stund_mrd = float((wv * p_own * boden_eig * rent).sum() / 1e9)
    bestand = stund_mrd * S_["dauer_jahre"]                      # Bestand im eingeschwungenen Zustand (Zufluss × Laufzeit; Annahme)
    zinsvorteil = bestand * (S_["fondszins"] - S_["zins"])
    # ---------------- Wirkung auf den festen Anteil (Modell E)
    # Kasse: Altersausgleich R4 jedes Jahr; Stundung als Zufluss in den ersten 'dauer' Jahren ohne Rückflüsse danach (vorsichtig), Zinsvorteil laufend
    ausg_kasse = {j: P["rentner"]["altersausgleich_pct_bip"] + zinsvorteil / BIP * 100 + (stund_mrd / BIP * 100 if j - 2028 < S_["dauer_jahre"] else 0.0) for j in ME.JAHRE}
    e30_ohne = ME.rechne(dict(anteil_fest=a))
    e30 = ME.rechne(dict(anteil_fest=a, ausgaben=ausg_kasse))
    einschl = {str(b): ME.rechne(dict(anteil_fest=a, ausgaben=ausg_kasse, boden_einschleifen_bis=b)) for b in P["einschleifen"]["varianten"]}
    # Zinsfall (3,0 %) mit R4 und Stundung: nötiges Mehraufkommen, damit 30 % tragbar bleiben (Zinsregel), und welche Sätze das wären
    zf = P["zinsregel"]["zins"]
    def mit_extra(x, zins=zf):
        return ME.rechne(dict(anteil_fest=a, zins=zins, ausgaben={j: ausg_kasse[j] - x for j in ME.JAHRE}))
    lo_, hi_ = 0.0, 0.8
    for _ in range(10):
        m_ = (lo_ + hi_) / 2
        lo_, hi_ = (lo_, m_) if mit_extra(m_)["anteil_tragbar_pct"] >= a * 100 else (m_, hi_)
    x_zins = hi_
    e_zins0, e_zins = mit_extra(0.0), mit_extra(x_zins)
    b20 = ST.boden(0.02)
    tau_n = next(t / 10000 for t in range(200, 600) if ST.boden(t / 10000) - b20 >= x_zins)
    zinsregel = dict(zins_pct=zf, anteil_tragbar_ohne_regel_pct=e_zins0["anteil_tragbar_pct"], ruecklage_min_ohne_regel_pct_bip=e_zins0["ruecklage_min_pct_bip"],
                     mehraufkommen_noetig_pct_bip=round(x_zins, 2), boden_satz_dafuer_pct=round(tau_n * 100, 2),
                     anteil_tragbar_mit_regel_pct=e_zins["anteil_tragbar_pct"], ruecklage_min_mit_regel_pct_bip=e_zins["ruecklage_min_pct_bip"],
                     boden_satz_25_mehr_pct_bip=round(ST.boden(0.025) - b20, 2), boden_satz_30_mehr_pct_bip=round(ST.boden(0.03) - b20, 2))
    kurz = lambda e: dict(anteil_tragbar_pct=e["anteil_tragbar_pct"], ruecklage_min_pct_bip=e["ruecklage_min_pct_bip"], ruecklage_max_pct_bip=e["ruecklage_max_pct_bip"],
                          fortschritt=e["fortschritt"], paket={j: {k: v for k, v in x.items() if k in ("anteil_grundbedarf_pct", "bar_erwachsen", "bar_kind", "netz_x_je_einwohner", "gesamt_erwachsen", "gesamt_kind")} for j, x in e["paket"].items()},
                          fonds=e["fonds"])
    E = dict(version=P["version"], status="Prüfrechnung (Beschluss 21.11.2026: fester Anteil 30 %, Empfehlungen v4.104)",
             dividende_2028=dict(je_erwachsenem_vor_kinderanteil=round(D), bar_erwachsen=round(D * ME.TOPF), bar_kind=round(D * ME.S * ME.TOPF), zuschlag_faktor=round(f, 3)),
             co2=dict(direkt_mt_2028=round(mt28, 1), direkt_mrd=round(float((wv * co2_dir).sum() / 1e9), 1), indirekt_mrd=round(float((wv * co2_ind).sum() / 1e9), 1),
                      je_haushalt_monat=round(ww(co2) / 12), je_rentnerhaushalt_monat=round(ww(co2, rent) / 12), dezile=co2_dez),
             boden=dict(eigentuemer_mio=round(eig_mio, 1), grundsteuer_heute_je_eur_bodenwert_pct=round(v0_rate * 100, 3),
                        satz_neu_auf_heutigen_wert_pct=round(t_neu_eff * 100, 3), wertverlust_kapitalisierung_pct=round(wertverlust * 100, 1),
                        bodenwert_je_eigentuemer_mittel_eur=round(float((wv * p_own * v_hh).sum() / (wv * p_own).sum())),
                        mehr_je_eigentuemer_monat=round(float((wv * p_own * boden_eig).sum() / (wv * p_own).sum()) / 12),
                        mehr_je_rentner_eigentuemer_monat=round(float((wv * p_own * boden_eig * rent).sum() / (wv * p_own * rent).sum()) / 12),
                        wertverlust_je_eigentuemer_eur=round(float((wv * p_own * v_hh).sum() / (wv * p_own).sum()) * wertverlust),
                        mieter_umlage_heute_monat=round(mieter_heute / 12), mieter_umlage_neu_falls_erlaubt_monat=round(mieter_umlage_neu / 12),
                        vermieter_mehr_mrd=round(float((wv * boden_verm).sum() / 1e9), 1)),
             stundung=dict(zufluss_mrd_jahr=round(stund_mrd, 1), zufluss_pct_bip=round(stund_mrd / BIP * 100, 2), bestand_mrd=round(bestand), bestand_pct_bip=round(bestand / BIP * 100, 1),
                           zinsvorteil_mrd=round(zinsvorteil, 1)),
             haushalte=faelle,
             modell_e_30=dict(ohne_zusatz=kurz(e30_ohne), mit_r4_und_stundung=kurz(e30), **{f"mit_r4_stundung_einschleifen_bis_{b}": kurz(e) for b, e in einschl.items()}),
             zinsregel=zinsregel,
             vermoegen=dict(wertverlust_boden_haushalte_mrd=round(B["haushalte_mrd_2024"] * F24 * wertverlust), wertverlust_boden_alle_mrd=round((B["haushalte_mrd_2024"] + 1598.5) * F24 * wertverlust)),
             hinweis="Euro je Monat, 2028, Kaufkraft 2026, Deutschland. Eigentümerquote nach Einkommen, Bodenwert je Eigentümer, Vermieteranteil, indirekte "
                     "CO₂-Überwälzung und Stundungsdauer sind Annahmen (toml). Die Abgabe auf Boden von Unternehmen ist nicht den Haushalten zugerechnet.")
    (AGG / "co2_boden_haushalte.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: E[k] for k in ("dividende_2028", "co2", "boden", "stundung", "vermoegen")}, ensure_ascii=False))
    print("Zinsregel", zinsregel)
    for k, v in faelle.items():
        print(k, {x: v[x] for x in ("gesamt", "erwerbsalter", "rentner", "rentner_eigentuemer", "rentner_mieter", "eigentuemer", "mieter")})
        print("    Dezile", [(x["mit_mehr_pct"], x["mittel_eur"]) for x in v["dezile"]])
    for k, v in E["modell_e_30"].items():
        print(k, v["anteil_tragbar_pct"], v["ruecklage_min_pct_bip"], v["ruecklage_max_pct_bip"], [(x["jahr"], x["anteil_pct"]) for x in v["fortschritt"]], v["paket"]["2028"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
