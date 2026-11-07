#!/usr/bin/env python3
"""Staatenauswahl nach Rechtsstaatlichkeit und UN-Grundlagen (Logbuch v4.73). Vorbereitung der Entscheidungsvorlagen, kein Beschluss.

Erste Durchsicht (v4.73), vereinfacht in v4.74: Teilnahme bei Grundlagen (beide Menschenrechtspakte, Pariser Abkommen) und WJP ≥ 0,66, sonst Partner; SDG Index (SDSN 2026);
UN-Mi (SDSN 2026) nur ausgewiesen. Für die 30 Staaten des geltenden Fonds zusätzlich: Wirkung einer Auswahl auf Beitrag und Zuschlag des
gemeinsamen Fonds (gleiches Verfahren wie fonds_klub.py: BIP-gewichtetes Mittel der eigenen Beiträge, skaliert mit dem Beschluss).
Staaten außerhalb Europas sind im Fondsmodell nicht enthalten (Daten zu Rentenzusagen fehlen).
Ausgabe: daten/aggregate/staatenauswahl.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "staatenauswahl.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("fk", W / "modell" / "fonds_klub.py")
FK = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(FK)
S, T = P["staaten"], P["schwellen"]
FG = json.loads((W / "daten" / "aggregate" / "fonds_geltend.json").read_text(encoding="utf-8"))


def stufe(c):
    """v4.74 Spielregel 1: Grundlagen (UN-Mitglied, beide Menschenrechtspakte, Pariser Abkommen) und Rechtsstaat ≥ teilnahme_wjp."""
    wjp, sdg, _, k7, pakte, paris = S[c]
    if pakte < 2 or not paris:
        return "nicht erfüllt (Grundlagen)"
    if wjp == -1:
        return "ohne WJP-Wert (zweite Quelle nötig)"
    return "Teilnahme" if wjp >= T["teilnahme_wjp"] else "Partner"


def main():
    b10, _, _ = FK.klub(FK.ZEHN)
    _, z10, _ = FK.klub(FK.ZEHN)
    dreissig = list(FK.MRJ)
    stufen = {c: stufe(c) for c in S}
    def fonds(lst):
        b, z, _ = FK.klub(lst)
        return dict(staaten=len(lst), beitrag_pct_bip=round(FK.BU["beitrag_pct_bip"] * b / b10, 2),
                    zuschlag_pct=round(FK.BU["zuschlag_auf_alle_steuern_pct"] * z / z10, 1))
    kern = [c for c in dreissig if S[c][0] >= T["kern_wjp"]]          # nur zur Information (v4.73)
    teil = [c for c in dreissig if stufen[c] == "Teilnahme"]
    ohne = [c for c in dreissig if stufen[c] != "Teilnahme" and S[c][0] != -1]
    var = {"alle 30 (geltend)": fonds(dreissig),
           "Teilnahme (WJP ≥ 0,66), CH und IS eingeschlossen": fonds(teil + ["CH", "IS"]),
           "nur WJP ≥ 0,75 (Information), CH und IS eingeschlossen": fonds(kern + ["CH", "IS"])}
    eigen = {c: dict(beitrag_eigen_mr_pct_bip=round(FK.MRJ[c]["altlasten"]["beitrag_pct_bip"], 2),
                     schuld_2024_pct_bip=round(FK.MR.D["schuld"][c], 1)) for c in ohne}
    sdg_unter = sorted(c for c in S if S[c][1] < T["sdg"])
    E = dict(version=P["version"], status="Vorbereitung (Entscheidungsvorlagen), kein Beschluss; Daten maschinell gelesen, an der Quelle zu prüfen",
             schwellen=T, stufen=stufen,
             zaehlung={s: sorted(c for c in stufen if stufen[c] == s) for s in sorted(set(stufen.values()))},
             unter_sdg_schwelle=sdg_unter, fonds_varianten=var, staaten_unter_0_66=eigen, anteil_bip_unter_0_66_pct=round(sum(FK.MRJ[c]["bip_kopf_eur_2024"] * FK.MRJ[c]["einwohner_mio"] for c in ohne) / sum(FK.MRJ[c]["bip_kopf_eur_2024"] * FK.MRJ[c]["einwohner_mio"] for c in dreissig) * 100, 1),
             geltend_kontrolle=dict(beitrag_pct_bip=FG["beitrag_pct_bip"], zuschlag_pct=FG["zuschlag_auf_alle_steuern_pct"]),
             hinweis="v4.74 Spielregel 1: Grundlagen (beide Menschenrechtspakte, Pariser Abkommen) und WJP 2025 ≥ 0,66 = Teilnahme, sonst Partner; "
                     "SDG Index, UN-Mi und Zahl der sieben Kernabkommen nur ausgewiesen. Fonds: Abgrenzung des Möglichkeitsraums, skaliert mit dem Beschluss (wie fonds_klub.py); nur Staaten des Fonds der 30.")
    if abs(var["alle 30 (geltend)"]["beitrag_pct_bip"] - FG["beitrag_pct_bip"]) > 0.005:
        raise SystemExit(f"Kontrolle: alle 30 weicht vom geltenden Fonds ab: {var['alle 30 (geltend)']} / {FG['beitrag_pct_bip']}")
    (W / "daten" / "aggregate" / "staatenauswahl.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in E["zaehlung"].items():
        print(f"{k:38} {len(v):2} {' '.join(v)}")
    for k, v in var.items():
        print(f"{k:62} {v}")
    print("unter 0,66:", eigen)
    print("unter SDG-Schwelle:", sdg_unter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
