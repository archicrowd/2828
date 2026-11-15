#!/usr/bin/env python3
"""Varianten zu E5 (Logbuch v4.93): belegte Deckung durch die Kette rechnen, in einer Arbeitskopie des Repositorys.

Je Variante: Kopie ohne .git und Rohdaten, Datei modell/deckung_varianten.toml mit den Änderungen, dann die Stufen von systemvarianten bis
fonds_klub. Gelesen werden netz33.json (Beschluss-Reihe: Dividende, Netz) und fonds_klub_geltend bzw. fonds_klub.json (Fondsbeitrag).
Ausgabe: daten/aggregate/e5_varianten.json. Die geltenden Dateien im Repository bleiben unverändert.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "e5_varianten.toml").read_text(encoding="utf-8"))


def lies(wurzel):
    n = json.loads((wurzel / "daten" / "aggregate" / "netz33.json").read_text(encoding="utf-8"))["beschluss"]["reihe"]
    r = {str(x["jahr"]): x for x in n}
    g = json.loads((wurzel / "daten" / "aggregate" / "fonds_geltend.json").read_text(encoding="utf-8"))
    al = json.loads((wurzel / "daten" / "aggregate" / "altlasten.json").read_text(encoding="utf-8"))
    return dict(dividende_erw_eur2026={j: r[str(j)]["dividende_erw_eur2026"] for j in P["jahre"]},
                dividende_pct_bip={j: r[str(j)]["dividende_pct_bip"] for j in P["jahre"]},
                netz_pct_bip={j: r[str(j)]["netz_pct_bip"] for j in P["jahre"]},
                fonds_beitrag_pct_bip=g.get("beitrag_pct_bip"),
                z_2028_pct_bip=al.get("beschluss", {}).get("verhandlungsmasse_z_2028_pct_bip"))


def main():
    E = dict(version=P["version"], status="Variantenrechnung zu E5; geltende Rechnung unverändert", geltend=lies(W), varianten={},
             hinweis="Rückwirkung über die Altrenten über der Dividende (Z) enthalten; Lösungsbereich in der Kopie erweitert (loeserbereich); "
                     "CO₂-Änderung wirkt nur 2028, weil projektion33 den CO₂-Pfad selbst rechnet")
    for name, aend in P["varianten"].items():
        with tempfile.TemporaryDirectory() as t:
            k = Path(t) / "repo"
            shutil.copytree(W, k, ignore=shutil.ignore_patterns(".git", "roh", "*.pdf", "docs", "seite", "deckung_varianten.toml"))
            for datei, alt, neu in P["loeserbereich"]:     # Lösungsbereich erweitern (nur in der Kopie), sonst endet die Lösung am Rand
                f = k / datei
                s = f.read_text(encoding="utf-8")
                if s.count(alt) != 1:
                    raise SystemExit(f"Lösungsbereich: {datei} unerwartet")
                f.write_text(s.replace(alt, neu), encoding="utf-8")
            (k / "modell" / "deckung_varianten.toml").write_text(
                "[aenderung_pct_bip]\n" + "".join(f'"{a}" = {v}\n' for a, v in aend.items()), encoding="utf-8")
            for st in P["stufen"]:
                r = subprocess.run([sys.executable, st], cwd=k, capture_output=True, text=True)
                if r.returncode != 0:
                    raise SystemExit(f"{name}: {st} fehlgeschlagen: {r.stderr[-600:]}")
            E["varianten"][name] = dict(aenderung_pct_bip=aend, summe_pct_bip=round(sum(aend.values()), 2), **lies(k))
    (W / "daten" / "aggregate" / "e5_varianten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("geltend", E["geltend"])
    for n, v in E["varianten"].items():
        print(n, v["summe_pct_bip"], v["dividende_erw_eur2026"], v["dividende_pct_bip"], "Fonds", v["fonds_beitrag_pct_bip"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
