#!/usr/bin/env python3
"""Dynamik je Regelstand neu bestimmt (Logbuch v4.102). Prüfrechnung, ändert die geltende Rechnung nicht.

Die geltende Dynamik (dynamik_geltend.py, v4.85) beruht auf festen Eingangswerten der statischen Rechnung v4.84: Impuls aus 442 € Mehr der
Haushalte, Netto-Anreiz für Fachkräfte ln(4.588/3.817), Arbeitsvolumen +4,6 % (dynamik33, v3.49: Grenzbelastung 56 → 36 %), Investition −0,5 %.
Hier werden diese vier Eingangswerte je Fall aus dem jeweiligen Regelstand bestimmt:
  geltend_v484   wie geltend (Gegenprobe)
  geltend_v497   geltende Regeln seit v4.97 (ein Drittel, belegte Einnahmen)
  satz38         Szenario 38 (v4.101): Satz 38 %, Regel L, Puffer, Glättung, R4, CO₂ K2
Grenzbelastung aus grenzbelastung33 (alleinstehend, je Euro Bruttolohn, heute ohne Bereinigung), Netto-Anreiz aus regel_boden/sozial_laender,
Mittel der Haushalte aus mikro_de. Dividende mit der fallbezogenen Dynamik über quote_optimum.pfad und netz33 (Rückwirkung), Fondsbeitrag mit
dynamik_geltend.fonds. Ausgabe: daten/aggregate/dynamik_satz.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "dynamik_satz.toml").read_text(encoding="utf-8"))


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / datei)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


S38 = lade("s38d", "szenario38.py")
QO, MD = S38.QO, S38.MD
DGM = lade("dgm", "dynamik_geltend.py")
GB = lade("gbd", "grenzbelastung33.py")
I = DGM.I
SATZ0 = S38.S0
DG0 = dict(QO.PJ.DG)
NZR0 = {j: dict(r) for j, r in QO.NZ.R.items()}
BASIS_DGM = dict(impuls=DGM.G["impuls_pct_bip"], dln=DGM.G["dln_netto_fachkraefte"], av=DGM.P["beschaeftigung"]["arbeitsvolumen_pct"][I],
                 inv=DGM.P["investition"]["bip_pct"][I])


def grenz(k, zu):
    base = list(GB.H.SAETZE)
    GB.H.SAETZE[:] = [x * k for x in base]
    try:
        o, _ = GB.neu(P["brutto_arbeit"], GB.P["schritt"], zu, 0.10)
    finally:
        GB.H.SAETZE[:] = base
    m, _ = GB.heute(P["brutto_arbeit"], GB.P["schritt"])
    return o, m


def dynamik(impuls, dln, av, inv):
    DGM.G["impuls_pct_bip"], DGM.G["dln_netto_fachkraefte"] = impuls, dln
    DGM.P["beschaeftigung"]["arbeitsvolumen_pct"][I], DGM.P["investition"]["bip_pct"][I] = av, inv
    reihe = {}
    for j in range(DGM.START, 2099):
        k = DGM.kanaele(j)
        fdy, fdp = DGM.fachkraefte(j)
        k["F1"] = fdy * 100
        dy = sum(k.values()) / 100
        reihe[j] = dict(dy=dy, kopf=(1 + dy) / (1 + fdp), kanaele=k)
    c = DGM.fonds({j: r["dy"] for j, r in reihe.items()})[0]
    DGM.G["impuls_pct_bip"], DGM.G["dln_netto_fachkraefte"] = BASIS_DGM["impuls"], BASIS_DGM["dln"]
    DGM.P["beschaeftigung"]["arbeitsvolumen_pct"][I], DGM.P["investition"]["bip_pct"][I] = BASIS_DGM["av"], BASIS_DGM["inv"]
    return reihe, c


def setze_dynamik(reihe):
    for j in QO.PJ.DG:
        QO.PJ.DG[j] = reihe[j]["kopf"] if j in reihe else DG0[j]
    for j, r in QO.NZ.R.items():
        if j in reihe and j in DG0:
            r["wachstum_je_kopf_faktor"] = NZR0[j]["wachstum_je_kopf_faktor"] * reihe[j]["kopf"] / DG0[j]


def zuruecksetzen():
    QO.PJ.DG.clear(); QO.PJ.DG.update(DG0)
    for j, r in NZR0.items():
        QO.NZ.R[j] = dict(r)


def eingaben(k, zu, mehr):
    o, m = grenz(k, zu)
    av = P["nachfrage_arbeit_pct"] + P["elastizitaet_angebot"] * math.log((1 - o) / (1 - m)) * 100
    s = SATZ0 * k
    inv = P["investition_mittel"] * ((s - P["satz_heute_kapital"]) + (s - P["satz_heute_gewinne"])) / ((SATZ0 - P["satz_heute_kapital"]) + (SATZ0 - P["satz_heute_gewinne"]))
    b = P["brutto_fachkraft"]
    dln = math.log(MD.RB.neu("DE", b, 1, 0) / MD.SL.heute("DE", b, 1, 0))
    impuls = P["impuls_bezug_pct_bip"] * mehr / P["mehr_bezug_eur"]
    return dict(impuls_pct_bip=round(impuls, 2), arbeitsvolumen_pct=round(av, 2), investition_pct_bip=round(inv, 2), dln_netto_fachkraefte=round(dln, 3),
                grenzbelastung_neu_pct=round(o * 100, 1), grenzbelastung_heute_pct=round(m * 100, 1))


def kurz(reihe):
    return {str(j): dict(bip_pct=round(reihe[j]["dy"] * 100, 2), je_kopf_pct=round((reihe[j]["kopf"] - 1) * 100, 2),
                         kanaele={c: round(v, 2) for c, v in reihe[j]["kanaele"].items()}) for j in (2028, 2030, 2035, 2045, 2060)}


def main():
    G = S38.P
    c_g = dynamik(BASIS_DGM["impuls"], BASIS_DGM["dln"], BASIS_DGM["av"], BASIS_DGM["inv"])
    reihe_g, c0 = c_g
    erg = dict(geltend_v484=dict(eingaben=dict(impuls_pct_bip=BASIS_DGM["impuls"], arbeitsvolumen_pct=BASIS_DGM["av"], investition_pct_bip=BASIS_DGM["inv"],
                                                dln_netto_fachkraefte=BASIS_DGM["dln"]), dynamik=kurz(reihe_g)))
    gp = QO.pfad(QO.system(SATZ0, False), "0", QO.V["punkte"]["2028"]["saldo"], 0.0)
    erg["geltend_v484"]["dividende_eur"] = gp["dividende_eur2026"]
    erg["geltend_v484"]["fonds_pct_bip"] = QO.FONDS

    # geltend v4.97: Eingaben aus dem geltenden Regelstand (Mikro: Mittel aller Haushalte)
    S38.setze()
    m_g = S38.mikro()
    ein = eingaben(1.0, GB.ZU, m_g["gesamt"]["mittel_eur"])
    reihe, c = dynamik(ein["impuls_pct_bip"], ein["dln_netto_fachkraefte"], ein["arbeitsvolumen_pct"], ein["investition_pct_bip"])
    setze_dynamik(reihe)
    r = QO.pfad(QO.system(SATZ0, False), "0", QO.V["punkte"]["2028"]["saldo"], 0.0)
    zuruecksetzen()
    erg["geltend_v497"] = dict(eingaben=ein, dynamik=kurz(reihe), dividende_eur=r["dividende_eur2026"], fonds_pct_bip=round(QO.FONDS * c / c0, 2))

    # Szenario 38 mit eigener Dynamik (Iteration über das Mittel der Haushalte)
    k = G["satz"] / SATZ0
    extra = G["co2_k2_pct_bip"] + json.loads((AGG / "szenario38.json").read_text(encoding="utf-8"))["rentner"]["kosten_pct_bip"]
    s38 = json.loads((AGG / "szenario38.json").read_text(encoding="utf-8"))
    mehr, verlauf = s38["haushalte_mikro"]["szenario38"]["gesamt"]["mittel_eur"], []
    d_prev, f_prev = s38["dividende"]["d0_eur"], s38["makro"]["zuschlag_pct"] / s38["makro"]["geltend"]["zuschlag_pct"]
    for it in range(P["iterationen"]):
        S38.setze(d_prev, f_prev, k)                       # Netto-Anreiz der Fachkräfte im Szenario
        ein = eingaben(k, GB.ZU * f_prev, mehr)
        S38.setze()
        reihe, c = dynamik(ein["impuls_pct_bip"], ein["dln_netto_fachkraefte"], ein["arbeitsvolumen_pct"], ein["investition_pct_bip"])
        setze_dynamik(reihe)
        d0, rr, pfad = S38.makro(extra)
        fonds = QO.FONDS * c / c0
        f = (fonds / rr["steuern_2028"]) / (QO.FONDS / 31.22)
        S38.setze(d0, f, k)
        m = S38.mikro()
        b = S38.beispiele()
        S38.setze()
        zuruecksetzen()
        verlauf.append(dict(iteration=it + 1, mehr_eur=m["gesamt"]["mittel_eur"], d0_eur=round(d0)))
        mehr, d_prev, f_prev = m["gesamt"]["mittel_eur"], d0, f
    sel = {str(x["jahr"]): x["dividende_eur"] for x in pfad if x["jahr"] in (2028, 2035, 2040, 2050, 2060)}
    erg["satz38"] = dict(eingaben=ein, dynamik=kurz(reihe), dividende_eur=sel, d0_eur=round(d0), fonds_pct_bip=round(fonds, 2),
                         zuschlag_pct=round(fonds / rr["steuern_2028"] * 100, 1), haushalte=dict(gesamt=m["gesamt"], erwerbsfaehige=m["erwerbsfaehige"],
                         dezile=m["dezile"]), beispiel_42000=b["42000"], iteration=verlauf,
                         ohne_eigene_dynamik=dict(dividende_eur={j: s38["dividende"]["pfad"][j]["dividende_eur"] for j in ("2028", "2035", "2040", "2050", "2060")},
                                                  gesamt=s38["haushalte_mikro"]["szenario38"]["gesamt"]))
    E = dict(version=P["version"], status="Prüfrechnung (Frage 21.11.2026); geltende Rechnung unverändert", faelle=erg,
             hinweis="Mittlerer Fall der Kanäle (Beschluss 14.11.2026). Euro je Erwachsenem und Monat, Kaufkraft 2026, Deutschland; Szenario 38 geglättet "
                     "(D0 × 1,01^t). Grenzbelastung alleinstehend 55.000 € (grenzbelastung33, heute ohne Bereinigung um den Rentenanspruch). "
                     "Investitionskanal linear im Abstand der Sätze (Annahme). Dieselbe Dynamik für alle 30 Staaten (Annahme wie geltend).")
    (AGG / "dynamik_satz.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for n, x in erg.items():
        print(n, x["eingaben"], "\n   Dynamik", {j: (v["bip_pct"], v["je_kopf_pct"]) for j, v in x["dynamik"].items()}, "\n   Dividende", x["dividende_eur"], "Fonds", x["fonds_pct_bip"])
    print(erg["satz38"]["iteration"], erg["satz38"]["haushalte"]["gesamt"], erg["satz38"]["haushalte"]["erwerbsfaehige"], erg["satz38"]["beispiel_42000"], erg["satz38"]["zuschlag_pct"])
    print("Kanäle 2045 geltend", erg["geltend_v484"]["dynamik"]["2045"]["kanaele"], "\n  v497", erg["geltend_v497"]["dynamik"]["2045"]["kanaele"], "\n  38", erg["satz38"]["dynamik"]["2045"]["kanaele"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
