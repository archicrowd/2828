#!/usr/bin/env python3
"""Zins des gemeinsamen Altlastenfonds: Beschluss (2,5 %) gegen Marktrenditen Oktober 2026 (Logbuch v4.19). Prüfrechnung.

Gleiche Rekursion wie modell/altlasten.py (Beschluss: Z voll, Rentenkürzung 7,5 %, Tilgung bis 2098, Startschuld 2028 der Gesamtrechnung):
  d(t+1) = d(t)·(1+i(t))/(1+g) + Z(t) − c,   gesucht c mit d(2098) = 0.
Varianten: fester Zins 2,5 / 3,0 / 3,5 / 4,0 %; Übergang vom Durchschnittszins 2028 auf den Marktzins über die Restlaufzeit.
Ausgabe: daten/aggregate/fondszins.json
"""
import contextlib
import importlib.util
import io
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "fondszins.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("al", W / "modell" / "altlasten.py")
AL = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(AL)
G, SV = AL.G, AL.SV
B = AL.P["beschluss"]
BJ = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))["beschluss"]
FGV = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))["grundlage"]   # v4.20
spec_rb = importlib.util.spec_from_file_location("rb", W / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec_rb)
with contextlib.redirect_stdout(io.StringIO()):
    spec_rb.loader.exec_module(RB)


def haushalt_de(zu):
    """Mehr im Monat bei 42.000 € brutto (DE, 2028, Kaufkraft 2026, regel_boden) und Anteil mit mehr, bei Zuschlag zu."""
    SL, alt = RB.SL, RB.SL.P["zuschlag_de"]
    gl = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))["zuschlag_auf_alle_steuern_pct"]
    SL.P["zuschlag_de"] = zu * alt / gl          # v4.38 (E11): Anteil Deutschlands nach Verrechnung (2028) auf den Zuschlag der Variante
    try:
        mehr = {n: round((RB.neu("DE", 42000, e, k) - SL.heute("DE", 42000, e, k)) / 12) for n, e, k in SL.HAUSHALTE}
        return dict(mehr_monat_42000=mehr, anteil_mit_mehr=RB.anteile("DE"))
    finally:
        SL.P["zuschlag_de"] = alt


def z_beschluss():
    k = G["anteil_minderjaehrige"] / 100
    vb = next(x for x in SV["varianten"] if x["id"] == B["system"])
    w = AL.SZ.gewicht()
    return [x * B["z_anteil"] for x in AL.SZ.z_klub(vb["dividende_pct_bip_2028"] / (1 - k / 2), w)], vb["punkte"]["2028"]["steuerbedarf"]


def pfad(c, z, zinsen, d0, n):
    d, out = d0, []
    for t in range(n):
        d = d * (1 + zinsen[t]) / (1 + AL.G_NOM) + (z[t] if t < len(z) else 0.0) - c
        out.append(d)
    return out


def loese(z, zinsen, d0, n):
    lo, hi = -5.0, 30.0
    for _ in range(80):
        c = (lo + hi) / 2
        lo, hi = (c, hi) if pfad(c, z, zinsen, d0, n)[-1] > 0 else (lo, c)
    return hi


def main():
    z, quote = z_beschluss()
    d0, n = G["schuldenquote_2028"], B["zieljahr"] - 2028
    start = G["zins_2028"]
    varianten = []

    def fall(name, zinsen_pct):
        zi = [x / 100 for x in zinsen_pct]
        c = loese(z, zi, d0, n)
        p = pfad(c, z, zi, d0, n)
        zu = round(c / quote * 100 * FGV["verhaeltnis_zuschlag_30_zu_10"], 1)            # v4.20: auf den Fonds der 30 übertragen
        varianten.append(dict(fall=name, beitrag_pct_bip=round(c * FGV["verhaeltnis_beitrag_30_zu_10"], 2), zuschlag_pct=zu, spitze_zehn=round(max(p), 1),
                              spitzenjahr_zehn=2029 + p.index(max(p)), zins_2028=round(zinsen_pct[0], 2), zins_ab_2036=round(zinsen_pct[min(8, n - 1)], 2),
                              beitrag_zehn_pct_bip=round(c, 2), haushalt_de=haushalt_de(zu)))

    for i in P["zinsen"]:
        fall(f"fest {i} %", [i] * n)
    for ziel in P["uebergang_ziel"]:
        fall(f"Übergang {start:.2f} → {ziel} %", [start + (ziel - start) * min(1.0, t / P["uebergang_jahre"]) for t in range(n)])
    basis = varianten[0]
    E = dict(version=P["version"], status="Prüfrechnung, Empfindlichkeit", wachstum_nominal=AL.G_NOM * 100, startschuld_2028=d0,
             durchschnittszins_2028=round(start, 2), markt_oktober_2026=dict(bund_10j=P["markt_bund_10j"], eu_10j=P["markt_eu_10j"],
             frankreich_10j=P["markt_frankreich_10j"], status="Sekundärquellen"), varianten=varianten,
             abgleich_beschluss=dict(altlasten_json_zehn=BJ["beitrag_pct_bip"], hier_zehn=basis["beitrag_zehn_pct_bip"]),
             hinweis="Zins über dem nominalen Wachstum (3 %): Die Schuld schmilzt nicht mehr von selbst, der Beitrag muss auch Zinsen tilgen. "
                     "Gemeinsame Anleihen (EU) rentieren derzeit über Bundesanleihen; günstiger als heute ist der Fonds für FR und IT, nicht für DE.")
    (AGG / "fondszins.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Abgleich Beschluss", E["abgleich_beschluss"], "| Startzins", E["durchschnittszins_2028"])
    for v in varianten:
        print(v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
