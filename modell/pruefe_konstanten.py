#!/usr/bin/env python3
"""Prüft, ob die fest im Skript stehenden Konstanten der Originalskripte (modell/rahmen/) mit
modell/parameter.toml übereinstimmen.

Hintergrund: Die Originalskripte wiederholen dieselben Konstanten (Quote, Verteidigungsziel, Zins, ...) in
jedem Skript. Ändert jemand einen Parameter an einer Stelle, laufen die übrigen unbemerkt weiter mit dem
alten Wert. Dieses Skript liest die Zuweisungen auf Modulebene (ast, ohne Ausführung) und meldet Abweichungen.

Bekannt veraltet und nur informativ geprüft: modell/rechnungen/pfad/dyn.py (frühe Fassung, Verteidigung 3,5 %,
alte Klub-Basis).

Ergebnis: daten/aggregate/konstanten_pruefung.csv. Rückgabe 0, wenn alle aktuellen Skripte übereinstimmen.
"""
import ast
import csv
import sys
import tomllib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent

# Name im Originalskript -> (Parametername, Umrechnung)
ABBILDUNG = {
    "QUOTE": ("steuerquote_klub", 1.0),
    "B_AUFG": ("b_fachaufgaben_bip_2028", 1.0),
    "A_OHNE_V": ("a_ohne_verteidigung_zins_bip_2028", 1.0),
    "V_ZIEL": ("verteidigung_ziel_nato_2035", 1.0),
    "V_START": ("verteidigung_basis_cofog_2024", 1.0),
    "I_ALT": ("zins_effektiv_altbestand", 1.0),
    "I_ZIEL": ("garantiezins_klub", 1.0),
    "REST": ("restlaufzeit_schulden", 1.0),
    "G_NOM": ("wachstum_nominal", 0.01),
    "PREIS": ("preissteigerung", 0.01),
    "VERSPRECHEN": ("dividende_de_versprechen_monat", 1.0),
    "D_START": ("schuldenquote_klub_2028", 1.0),
    "F": ("fortschreibung_bip_2024_2028", 1.0),
}
AKTUELL = sorted((WURZEL / "modell" / "rahmen").glob("*.py"))
VERALTET = [WURZEL / "modell" / "rechnungen" / "pfad" / "dyn.py"]
TOL = 1e-6


def konstanten(pfad: Path) -> list[tuple[str, float]]:
    baum = ast.parse(pfad.read_text(encoding="utf-8"))
    ergebnis = []
    for knoten in baum.body:
        if not isinstance(knoten, ast.Assign):
            continue
        ziele, wert = knoten.targets, knoten.value
        for ziel in ziele:
            if isinstance(ziel, ast.Name) and isinstance(wert, ast.Constant) and isinstance(wert.value, (int, float)):
                ergebnis.append((ziel.id, float(wert.value)))
            elif isinstance(ziel, ast.Tuple) and isinstance(wert, ast.Tuple) and len(ziel.elts) == len(wert.elts):
                for n, w in zip(ziel.elts, wert.elts):
                    if isinstance(n, ast.Name) and isinstance(w, ast.Constant) and isinstance(w.value, (int, float)):
                        ergebnis.append((n.id, float(w.value)))
    return ergebnis


def main() -> int:
    with (WURZEL / "modell" / "parameter.toml").open("rb") as f:
        P = {p["name"]: float(p["wert"]) for p in tomllib.load(f)["parameter"]}
    zeilen, abweichungen = [], 0
    for gruppe, dateien in (("aktuell", AKTUELL), ("veraltet", VERALTET)):
        for pfad in dateien:
            for name, wert in konstanten(pfad):
                if name not in ABBILDUNG:
                    continue
                param, faktor = ABBILDUNG[name]
                soll = P[param] * faktor
                ok = abs(wert - soll) <= TOL
                if not ok and gruppe == "aktuell":
                    abweichungen += 1
                zeilen.append([str(pfad.relative_to(WURZEL)), name, wert, param, soll, "ja" if ok else "NEIN", gruppe])
    ziel = WURZEL / "daten" / "aggregate" / "konstanten_pruefung.csv"
    with ziel.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["datei", "konstante", "wert_im_skript", "parameter", "wert_parameter", "gleich", "gruppe"])
        w.writerows(zeilen)
    aktuell = [z for z in zeilen if z[-1] == "aktuell"]
    print(f"{len(aktuell)} Konstanten in {len(AKTUELL)} aktuellen Skripten geprüft, {abweichungen} abweichend.")
    for z in zeilen:
        if z[5] == "NEIN":
            print("  ", z[-1].upper(), z[0], z[1], z[2], "<>", z[3], z[4])
    return 2 if abweichungen else 0


if __name__ == "__main__":
    sys.exit(main())
