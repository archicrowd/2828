#!/usr/bin/env python3
"""Neustartverfahren: Wie ändern Schuldenschnitt und Kürzung der Altrenten den Altlastenfonds eines Staates (Logbuch v3.54)? Prüfrechnung.

Grundlage: moeglichkeitsraum33.py (eigener Fonds je Staat, Tilgung bis 2098, Zins 2,5 %, Wachstum 3 %). Varianten nach neustart33.toml.
Ausgabe: daten/aggregate/neustart33.json
"""
import contextlib, importlib.util, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "neustart33.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("mr", W / "modell" / "moeglichkeitsraum33.py")
MR = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(MR)


def main():
    erg = {}
    for c in P["staaten"]:
        a = MR.land(c, "2028")
        schuld0, k0 = MR.D["schuld"][c], MR.SZ.KUERZUNG
        reihe = []
        for s in P["schnitt"]:
            for k in P["altrenten_kuerzung"]:
                MR.D["schuld"][c] = schuld0 * (1 - s)
                MR.SZ.KUERZUNG = 1 - (1 - k0) * (1 - k)
                al = MR.altlasten(c, a["div_erw_pct_kopf"], a["deckung_pct_bip"])
                reihe.append(dict(schnitt=s, altrenten_kuerzung=k, schuld_nach=round(schuld0 * (1 - s), 1), **al))
        MR.D["schuld"][c], MR.SZ.KUERZUNG = schuld0, k0
        erg[c] = dict(name=MR.EW[c]["name"], schuld_2024=schuld0, varianten=reihe)
    E = dict(version=P["version"], status="Prüfrechnung", staaten=erg)
    (W / "daten" / "aggregate" / "neustart33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, e in erg.items():
        print(e["name"], " | ".join(f"Schnitt {v['schnitt']:.0%} Renten −{v['altrenten_kuerzung']:.0%}: Zuschlag {v['zuschlag_pct']} % (Spitze {v['spitze']})" for v in e["varianten"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
