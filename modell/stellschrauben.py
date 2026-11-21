#!/usr/bin/env python3
"""Stabile Dividende als Maxime: ½ Grundbedarf je Erwachsenem; Arbeit bleibt bei ein Drittel (Logbuch v4.103). Prüfrechnung.

1. Bedarf: Dividende D*(j) = ½ Grundbedarf(j) (netz33: 12.348 € 2026, folgt zu 30 % den Löhnen) gegen das Verfügbare der geltenden Regeln
   mit Regel L und Puffer 0,5 % BIP, Dynamik Stand v4.97 (dynamik_satz, Korrektur 96). Gegengerechnet: weniger Aufstockung im Netz (netz33)
   und kleinere Altrenten über der Dividende im Fonds (Z hängt an der Dividende; Fonds mit dynamik_geltend.fonds).
2. Stellschrauben (stellschrauben.toml): Wirkung in % BIP je Jahr, Wachstumswirkung (BIP-Niveau), Rückwirkung des Wachstums auf den Bedarf
   (½ Grundbedarf wächst nur zu 30 % mit den Löhnen), Einordnung nach Verteilung und Einfachheit.
3. Pakete: erreichbarer Anteil am Grundbedarf je Jahr und das Jahr, ab dem ½ Grundbedarf trägt.
Ausgabe: daten/aggregate/stellschrauben.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "stellschrauben.toml").read_text(encoding="utf-8"))


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / datei)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


DS = lade("ds_st", "dynamik_satz.py")
QO, DGM, NZ = DS.QO, DS.DGM, DS.QO.NZ
JAHRE = range(2028, 2061)
GB26 = NZ.P["grundbedarf_eur_2026"]
r2 = lambda x: round(x, 2)


# ------------------------------------------------------------------ Dynamik Stand v4.97 und Fonds in Abhängigkeit von der Dividende
E97 = json.loads((AGG / "dynamik_satz.json").read_text(encoding="utf-8"))["faelle"]["geltend_v497"]["eingaben"]
REIHE97, _ = DS.dynamik(E97["impuls_pct_bip"], E97["dln_netto_fachkraefte"], E97["arbeitsvolumen_pct"], E97["investition_pct_bip"])
DY97 = {j: r["dy"] for j, r in REIHE97.items()}


def fonds_c(div28, dy, zieljahr=None):
    B = DGM.AL["beschluss"]
    k = DGM.ALM.G["anteil_minderjaehrige"] / 100
    z = [x * B["z_anteil"] for x in DGM.ALM.SZ.z_klub(div28 / (1 - k / 2))]
    zs = [z[t] / (1 + dy.get(2028 + t, dy[max(dy)])) for t in range(len(z))]
    i, g, d0 = B["zins"] / 100, DGM.ALM.G_NOM, DGM.ALM.G["schuldenquote_2028"]
    zj = zieljahr or B["zieljahr"]

    def pf(c):
        d, o = d0, []
        for t in range(zj - 2028):
            j = 2029 + t
            w = (1 + dy.get(j, dy[max(dy)])) / (1 + dy.get(j - 1, dy[max(dy)]))
            d = d * (1 + i) / ((1 + g) * w) + (zs[t] if t < len(zs) else 0) - c
            o.append(d)
        return o
    lo, hi = -5.0, 20.0
    for _ in range(80):
        c = (lo + hi) / 2
        lo, hi = (c, hi) if pf(c)[-1] > 0 else (lo, c)
    return hi, max(pf(hi))


def grundpfad():
    DS.setze_dynamik(REIHE97)
    r = QO.pfad(QO.system(QO.S0, False), P["regel"], P["puffer_pct_bip"], 0.0, mit_reihe=True)
    return {x["jahr"]: x for x in r["reihe"]}


BASIS = grundpfad()
C_G, SPITZE_G = fonds_c(QO.V["dividende_pct_bip_2028"], DY97)


def ziel(j, anteil=None):
    a = P["ziel_anteil_grundbedarf"] if anteil is None else anteil
    f = NZ.R[j]["wachstum_je_kopf_faktor"]
    return a * GB26 / 12 * f ** NZ.LA


def fonds_entlastung(div28):
    """Fondsbeitrag sinkt, wenn die Dividende steigt (weniger Altrenten über der Dividende); als % BIP an die Dividende (Gesamtlast gleich)."""
    c, sp = fonds_c(div28, DY97)
    return QO.FONDS * (1 - c / C_G), sp


def bilanz(extra, dlnf=None, anteil=None):
    """Verfügbar minus Bedarf je Jahr (% BIP) bei Dividende = Ziel; extra[j] = Wirkung der Stellschrauben; dlnf[j] = Wachstumswirkung (ln BIP)."""
    d28 = ziel(2028, anteil) / BASIS[2028]["eur_je_punkt"]
    ent, _ = fonds_entlastung(d28)
    out = {}
    for j in JAHRE:
        x = BASIS[j]
        g = (dlnf or {}).get(j, 0.0)
        bedarf = ziel(j, anteil) * math.exp(-(1 - NZ.LA) * g) / x["eur_je_punkt"]   # Wachstum: Grundbedarf folgt nur zu 30 % den Löhnen
        frei = x["div"] + QO.netz_korrektur(j, ziel(j, anteil)) + ent + extra.get(j, 0.0)
        out[j] = frei - bedarf
    return out, ent, d28


def erreichbar(extra, dlnf=None):
    """Größter Anteil am Grundbedarf je Jahr, den Verfügbares und Stellschrauben tragen (Bisektion je Jahr, Fondsentlastung beim Anteil 2028)."""
    res = {}
    for j in P["jahre"]:
        lo, hi = 0.0, 1.0
        for _ in range(25):
            m = (lo + hi) / 2
            b, _, _ = bilanz(extra, dlnf, m)
            lo, hi = (m, hi) if b[j] >= 0 else (lo, m)
        res[str(j)] = dict(anteil_grundbedarf_pct=round(lo * 100, 1), eur=round(ziel(j, lo)))
    return res


# ------------------------------------------------------------------ Stellschrauben
def boden(tau):
    b = P["boden"]
    v0 = b["bodenwert_mrd_2024"] / b["bip_2024_mrd"] * 100          # Bodenwert in % BIP
    t0 = b["bestand_pct_bip"] / v0
    v = v0 * b["r"] / (b["r"] + tau - t0)
    return tau * v - b["bestand_pct_bip"]


def kapital(s):
    sy0 = QO.system(QO.S0, False)
    pos0, _ = QO.deckung(sy0)
    sy = dict(sy0, spitzensatz=s)                                     # einkommen_saetze bleiben (Arbeit ein Drittel)
    pos, _ = QO.deckung(sy)
    d = sum(pos.values()) - sum(pos0.values())
    return d, P["kapital"]["wachstum_je_punkt"] * (s - QO.S0)


def ki_pfad():
    k = P["ki"]
    out, lnf = {}, 0.0
    for j in JAHRE:
        if j > 2028:
            lnf += math.log(1 + (k["pp"] if j <= 2040 else k["pp"] / 2) / 100)
        out[j] = lnf
    return out


def schrauben():
    S = {}
    stetig = lambda v: {j: v for j in JAHRE}
    for tau in P["boden"]["saetze"]:
        S[f"Boden {tau * 100:.1f} %"] = dict(wirkung=stetig(boden(tau)), wachstum=0.0, gruppe="Einnahmen",
                                            verteilung="Eigentümer, nach Bodenwert; Rentner mit Wohneigentum (Stundung wie Elternhaus nötig)",
                                            einfachheit="einfach: eine Bemessung (Bodenrichtwert × Fläche), digital aus Kataster und Grundsteuerwerten")
    for s in P["kapital"]["saetze"]:
        d, w = kapital(s)
        S[f"Kapital {s:.0f} %"] = dict(wirkung=stetig(d), wachstum=w, gruppe="Einnahmen", verteilung="oberes Zehntel",
                                       einfachheit="einfach (Satz), aber Ausweichen und Steuerwettbewerb")
    for v, n in zip(P["subventionen"]["pct_bip"], ("vorsichtig", "mittel", "hoch")):
        S[f"Subventionen {n}"] = dict(wirkung=stetig(v), wachstum=0.0, gruppe="Einnahmen", verteilung="je nach Posten; Verkehr, Energie",
                                      einfachheit="vereinfacht (weniger Ausnahmen)")
    c = P["co2"]
    co2 = {j: c["k3_minus_k2_2028"] * c["anteil_konstante"] for j in JAHRE}
    S["CO₂ 150 €/t (K3, über Regel L)"] = dict(wirkung=co2, wachstum=0.0, gruppe="Einnahmen", verteilung="Konsum; Rentner ohne Ausgleich belastet",
                                              einfachheit="einfach (ein Preis)")
    for a, n in zip(P["gesundheit"]["anteil"], ("vorsichtig", "mittel", "hoch")):
        S[f"Gesundheit digital {n}"] = dict(wirkung={j: a * (QO.NZ.SV["gesundheit"] + QO.PJ.lin("gesundheit_pflege_plus", j)) for j in JAHRE}, wachstum=0.0,
                                            gruppe="Ausgaben", verteilung="neutral", einfachheit="digital (Akte, Telemedizin, Abrechnung)")
    st = P["staatsebene"]
    S["Staatsebene nötig (EU-Maß)"] = dict(wirkung=stetig(-st["bedarf_pct_bip"]), wachstum=0.0, gruppe="Ausgaben (Risiko)", verteilung="–",
                                           einfachheit="heute nicht abgebildet")
    S["Staatsebene digital verschlankt"] = dict(wirkung=stetig(-st["digital_pct_bip"]), wachstum=0.0, gruppe="Ausgaben (Risiko)", verteilung="–",
                                                einfachheit="digital: Steuer ohne Erklärung, Leistungen aus einer Hand, ein Register")
    bk = P["buerokratie"]["bip_plus_pct"] / 100
    S["Bürokratieabbau 40 % (digital)"] = dict(wirkung=stetig(0.0), wachstum_pfad={j: math.log(1 + bk * DGM.aufbau(j, DGM.P["buerokratie"]["aufbau_bis"])) for j in JAHRE},
                                              gruppe="Dynamik", verteilung="breit", einfachheit="Kern der Vereinfachung: Lohn, Steuer, Leistungen automatisch")
    k = P["ki"]
    kp = ki_pfad()
    S["KI und Automatisierung (Trend)"] = dict(wirkung={j: k["kapital_verschiebung_pp"] * (j - 2028) / 32 * (k["belastung_kapital"] - k["belastung_arbeit"]) for j in JAHRE},
                                              wachstum_pfad=kp, gruppe="Trend", verteilung="Kapitalseite; Drittel besteuert jeden Euro gleich",
                                              einfachheit="digital; Wirkung unsicher (Acemoglu 2024 bis OECD 2024)")
    e = P["erbe"]
    erb = QO.deckung(QO.system(QO.S0, False))[0]["Erbschaften"]
    S["Erbschaftswelle (Trend)"] = dict(wirkung={j: erb * e["plus_2045"] * min(1.0, (j - 2028) / 17) for j in JAHRE}, wachstum=0.0, gruppe="Trend",
                                        verteilung="Erben großer Vermögen", einfachheit="unverändert")
    cl, spl = fonds_c(QO.V["dividende_pct_bip_2028"], DY97, P["fonds"]["zieljahr_lang"])
    S["Fonds gestreckt bis 2125"] = dict(wirkung=stetig(QO.FONDS * (1 - cl / C_G)), wachstum=0.0, gruppe="Fonds",
                                         verteilung="künftige Generationen tragen länger", einfachheit=f"Risiko: Schuld bis {spl:.0f} % BIP (bis 2098: {SPITZE_G:.0f} %)")
    return S


def bewerte(S):
    """Wirkung je Stellschraube: % BIP 2028/2045/2060 einschließlich Rückwirkung des Wachstums auf den Bedarf; Euro je Erwachsenem."""
    out = {}
    for n, s in S.items():
        if "wachstum_pfad" in s:
            dl = s["wachstum_pfad"]
        else:
            dl = {j: math.log(1 + s["wachstum"] / 100 * DGM.aufbau(j, 2040)) for j in JAHRE}
        b0, _, _ = bilanz({})
        b1, _, _ = bilanz(s["wirkung"], dl)
        out[n] = dict(gruppe=s["gruppe"], pct_bip={str(j): r2(b1[j] - b0[j]) for j in P["jahre"]},
                      eur_2028=round((b1[2028] - b0[2028]) * BASIS[2028]["eur_je_punkt"]),
                      bip_niveau_2045_pct=r2((math.exp(dl[2045]) - 1) * 100), verteilung=s["verteilung"], einfachheit=s["einfachheit"])
    return out


def stabil(extra, dlnf=None):
    """Größter fester Anteil am Grundbedarf 2028–2060, den Verfügbares und Stellschrauben mit einer Rücklage (ohne Zins, nie negativ) tragen."""
    lo, hi = 0.0, 1.0
    for _ in range(25):
        m = (lo + hi) / 2
        b, _, _ = bilanz(extra, dlnf, m)
        rl, ok = 0.0, True
        for j in JAHRE:
            rl += b[j]
            ok &= rl >= -1e-9
        lo, hi = (m, hi) if ok else (lo, m)
    b, _, _ = bilanz(extra, dlnf, lo)
    rl, rmax, pfad = 0.0, 0.0, {}
    for j in JAHRE:
        rl += b[j]
        rmax = max(rmax, rl)
        pfad[j] = rl
    return dict(anteil_grundbedarf_pct=round(lo * 100, 1), eur={str(j): round(ziel(j, lo)) for j in P["jahre"]}, ruecklage_hoechst_pct_bip=r2(rmax),
                ruecklage_2060_pct_bip=r2(pfad[2060]))


def paket(S, namen):
    ex, dl = {}, {}
    for n in namen:
        s = S[n]
        p = s.get("wachstum_pfad") or {j: math.log(1 + s["wachstum"] / 100 * DGM.aufbau(j, 2040)) for j in JAHRE}
        for j in JAHRE:
            ex[j] = ex.get(j, 0.0) + s["wirkung"][j]
            dl[j] = dl.get(j, 0.0) + p[j]
    b, ent, _ = bilanz(ex, dl)
    jahr = next((j for j in JAHRE if all(b[k] >= 0 for k in JAHRE if k >= j)), None)
    return dict(stellschrauben=namen, luecke_bei_halbem_grundbedarf_pct_bip={str(j): r2(-b[j]) for j in P["jahre"]},
                erreichbar=erreichbar(ex, dl), stabil=stabil(ex, dl), traegt_ab=jahr)


def main():
    S = schrauben()
    b0, ent, d28 = bilanz({})
    bed = {str(j): dict(ziel_eur=round(ziel(j)), bedarf_pct_bip=r2(ziel(j) / BASIS[j]["eur_je_punkt"]), luecke_pct_bip=r2(-b0[j]),
                        netz_entlastung_pct_bip=r2(QO.netz_korrektur(j, ziel(j)) - QO.netz_korrektur(j, QO.fixpunkt(BASIS[j]["div"], BASIS[j]["eur_je_punkt"], j))))
           for j in P["jahre"]}
    ohne = dict(erreichbar({}), stabil=stabil({}))
    bew = bewerte(S)
    pakete = {
        "A ohne neue Lasten auf Kapital (Boden 1,5 %, Subventionen mittel, CO₂ K3, Gesundheit digital mittel, Staatsebene digital, Bürokratie digital)":
            ["Boden 1.5 %", "Subventionen mittel", "CO₂ 150 €/t (K3, über Regel L)", "Gesundheit digital mittel", "Staatsebene digital verschlankt",
             "Bürokratieabbau 40 % (digital)"],
        "B wie A, dazu Kapital 38 %": ["Boden 1.5 %", "Subventionen mittel", "CO₂ 150 €/t (K3, über Regel L)", "Gesundheit digital mittel",
                                       "Staatsebene digital verschlankt", "Bürokratieabbau 40 % (digital)", "Kapital 38 %"],
        "C wie A, dazu Trends KI und Erbschaftswelle": ["Boden 1.5 %", "Subventionen mittel", "CO₂ 150 €/t (K3, über Regel L)", "Gesundheit digital mittel",
                                                        "Staatsebene digital verschlankt", "Bürokratieabbau 40 % (digital)", "KI und Automatisierung (Trend)",
                                                        "Erbschaftswelle (Trend)"],
        "D wie C, Boden 2 % und Kapital 38 %": ["Boden 2.0 %", "Subventionen mittel", "CO₂ 150 €/t (K3, über Regel L)", "Gesundheit digital mittel",
                                                "Staatsebene digital verschlankt", "Bürokratieabbau 40 % (digital)", "KI und Automatisierung (Trend)",
                                                "Erbschaftswelle (Trend)", "Kapital 38 %"],
        "E wie D, Fonds gestreckt bis 2125": ["Boden 2.0 %", "Subventionen mittel", "CO₂ 150 €/t (K3, über Regel L)", "Gesundheit digital mittel",
                                              "Staatsebene digital verschlankt", "Bürokratieabbau 40 % (digital)", "KI und Automatisierung (Trend)",
                                              "Erbschaftswelle (Trend)", "Kapital 38 %", "Fonds gestreckt bis 2125"],
    }
    pk = {n: paket(S, l) for n, l in pakete.items()}
    DS.zuruecksetzen()
    QO.PJ.sy.clear(); QO.PJ.sy.update(QO.BASIS33); QO.PJ._PROG.clear()
    E = dict(version=P["version"], status="Prüfrechnung (Auftrag 21.11.2026); geltende Rechnung unverändert", maxime="Dividende je Erwachsenem = ½ Grundbedarf",
             grundlagen=dict(regel=P["regel"], puffer_pct_bip=P["puffer_pct_bip"], dynamik="Stand v4.97 (dynamik_satz, Korrektur 96)", arbeit="ein Drittel",
                             label="7/13/19/27 fest", fonds_entlastung_pct_bip=r2(ent), dividende_2028_pct_bip=r2(d28)),
             bedarf=bed, ohne_stellschrauben=ohne, stellschrauben=bew, pakete=pk,
             hinweis="% BIP; Euro je Erwachsenem und Monat, Kaufkraft 2026, Deutschland. Wirkungen der Stellschrauben überwiegend Annahmen (toml); "
                     "Wachstum wirkt nur über den Bedarf (½ Grundbedarf folgt zu 30 % den Löhnen) und ist sonst nicht als Mehraufkommen gerechnet.")
    (AGG / "stellschrauben.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Bedarf", bed, "\nFonds-Entlastung", r2(ent), "\nohne", ohne)
    for n, x in bew.items():
        print(f"{n:<42} {x['pct_bip']} {x['eur_2028']:>4} € BIP45 {x['bip_niveau_2045_pct']}")
    for n, x in pk.items():
        print(n[:40], x["luecke_bei_halbem_grundbedarf_pct_bip"], x["erreichbar"], "STABIL", x["stabil"], x["traegt_ab"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
