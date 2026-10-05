#!/usr/bin/env python3
"""Lauf-Skript für TAX 28:28.

Liest modell/parameter.toml, prüft die Pflichtfelder und die Regeln für Euro-
Beträge und schreibt daten/aggregate/ergebnis.json. Enthält noch keine
Rechnung; Rechnungen kommen als eigene Skripte in modell/ hinzu und tragen
ihre Ergebnisse in die Ergebnisdatei ein.

Aufruf:  python3 modell/lauf.py [parameterfile] [ausgabedatei]
Rückgabe: 0 bei gültigem Parameterfile, 1 bei Fehlern (Fehler auf stderr).
"""
import hashlib
import json
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PARAMETER = WURZEL / "modell" / "parameter.toml"
AUSGABE = WURZEL / "daten" / "aggregate" / "ergebnis.json"

PFLICHT = ("name", "wert", "einheit", "bezugsjahr", "preisbasis", "quelle", "status")
PREISBASEN = {"nominal", "real", "keine"}
STATI = {"belegt", "groessenordnung", "modellrechnung", "annahme", "offen"}
NAME = re.compile(r"^[a-z0-9_]+$")
GELD = re.compile(r"\b(EUR|USD)\b", re.IGNORECASE)


def pruefe(p: dict, nr: int) -> list[str]:
    """Gibt die Fehler eines Parameters zurück (leere Liste = gültig)."""
    f = []
    marke = p.get("name", f"Eintrag {nr}")
    for feld in PFLICHT:
        if feld not in p:
            f.append(f"{marke}: Pflichtfeld '{feld}' fehlt")
    if f:
        return f
    if not NAME.match(p["name"]):
        f.append(f"{marke}: Name nur a-z, 0-9, Unterstrich")
    if isinstance(p["wert"], bool) or not isinstance(p["wert"], (int, float)):
        f.append(f"{marke}: 'wert' muss eine Zahl sein")
    if not isinstance(p["bezugsjahr"], int) or isinstance(p["bezugsjahr"], bool):
        f.append(f"{marke}: 'bezugsjahr' muss eine Ganzzahl sein")
    if p["preisbasis"] not in PREISBASEN:
        f.append(f"{marke}: preisbasis muss {sorted(PREISBASEN)} sein")
    if p["status"] not in STATI:
        f.append(f"{marke}: status muss {sorted(STATI)} sein")
    if GELD.search(p["einheit"]) and p["preisbasis"] == "keine":
        f.append(f"{marke}: Geldbetrag ('{p['einheit']}') braucht preisbasis nominal oder real")
    if p["preisbasis"] == "real" and not isinstance(p.get("preisjahr"), int):
        f.append(f"{marke}: preisbasis 'real' verlangt ein ganzzahliges 'preisjahr'")
    if p["status"] == "belegt" and p["quelle"].strip().lower() == "eigene setzung":
        f.append(f"{marke}: status 'belegt' verlangt eine Quelle, nicht 'eigene Setzung'")
    return f


def main() -> int:
    pfad = Path(sys.argv[1]) if len(sys.argv) > 1 else PARAMETER
    aus = Path(sys.argv[2]) if len(sys.argv) > 2 else AUSGABE
    roh = pfad.read_bytes()
    daten = tomllib.loads(roh.decode("utf-8"))
    liste = daten.get("parameter", [])

    fehler = []
    namen = set()
    for i, p in enumerate(liste, 1):
        fehler += pruefe(p, i)
        n = p.get("name")
        if n in namen:
            fehler.append(f"{n}: Name kommt doppelt vor")
        namen.add(n)

    if fehler:
        for e in fehler:
            print("FEHLER:", e, file=sys.stderr)
        print(f"{len(fehler)} Fehler, keine Ausgabe geschrieben.", file=sys.stderr)
        return 1

    ergebnis = {
        "modellstand": daten.get("modell", {}).get("version", "unbekannt"),
        "erzeugt": date.today().isoformat(),
        "parameterfile_sha256": hashlib.sha256(roh).hexdigest(),
        "parameter": liste,
        "ergebnisse": [],
    }
    aus.parent.mkdir(parents=True, exist_ok=True)
    aus.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(liste)} Parameter geprüft, geschrieben nach {aus}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
