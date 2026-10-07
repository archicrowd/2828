#!/usr/bin/env python3
"""Maschinenlesbare Projektkarte für Dritte (Menschen und KI-Agenten).

Schreibt projekt/manifest.json aus den Registern (bausteine.csv, nahtstellen.csv, daten/quellen.csv) und der
Gesamtrechnung. Prüft dabei, dass die Zugangsinformationen zusammenpassen:
  - jede quelle_id in daten/aggregate/eingangswerte.csv steht in daten/quellen.csv,
  - jeder Pfad, den daten/quellen.csv als Datei im Repository nennt, existiert,
  - jede in DATENZUGANG.md und AGENTS.md genannte Datei mit Backticks existiert.

Aufruf:  python3 projekt/manifest.py      Rückgabe 0 oder 2
"""
import csv
import json
import re
import sys
import tomllib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
FEHLER: list[str] = []


def lies(p):
    with open(WURZEL / p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    bausteine, naehte, quellen = lies("projekt/bausteine.csv"), lies("projekt/nahtstellen.csv"), lies("daten/quellen.csv")
    ids = {q["id"] for q in quellen}
    for r in lies("daten/aggregate/eingangswerte.csv"):
        if r["quelle_id"] not in ids:
            FEHLER.append(f"eingangswerte.csv: Quelle {r['quelle_id']} fehlt in daten/quellen.csv")
    for q in quellen:
        for teil in re.split(r";\s*", q["datei_im_repo"]):
            pfad = teil.split(" (")[0].strip()
            if "/" in pfad and not (WURZEL / pfad).exists():
                FEHLER.append(f"daten/quellen.csv {q['id']}: Datei fehlt: {pfad}")
    for doc in ("DATENZUGANG.md", "AGENTS.md"):
        text = (WURZEL / doc).read_text(encoding="utf-8")
        for pfad in set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:py|md|csv|json|toml|js|pdf|docx|sha256|cff))`", text)):
            optional = {"projekt/manifest.json", "daten/aggregate/eingangswerte_abgleich.csv"}  # entstehen erst beim Lauf
            if pfad in optional:
                continue
            if not any((WURZEL / basis / pfad).exists() for basis in ("", "modell", "daten/aggregate")):
                FEHLER.append(f"{doc}: genannte Datei fehlt: {pfad}")

    J = json.loads((WURZEL / "daten/aggregate/gesamtrechnung.json").read_text(encoding="utf-8"))
    version = tomllib.loads((WURZEL / "modell/parameter.toml").read_text(encoding="utf-8"))["modell"]["version"]
    manifest = {
        "projekt": "TAX 28:28",
        "modellstand": version,
        "fassung_gesamtkonzept": J["fassung"],
        "autor_und_projektverantwortung": "Arndt Hermann",
        "kontakt": "2828@archicrowd.de",
        "repository": "https://github.com/archicrowd/2828 (privat; Zugang auf Anfrage)",
        "lizenz": {"skripte": "MIT (LICENSE)", "texte_und_ergebnisse": "CC BY 4.0 (LICENSE-DOKUMENTE.md)",
                   "daten_dritter": "Bedingungen der Anbieter, siehe daten/quellen.csv Spalte weitergabe"},
        "einstieg": {"menschen": "DATENZUGANG.md", "ki_agenten": "AGENTS.md", "arbeitsregeln": "CLAUDE.md",
                     "uebersicht": "INDEX.md", "logbuch": "logbuch/Versionsgeschichte-TAX-2828-BandIII.md"},
        "befehle": {
            "alles_pruefen": "python3 modell/alles.py",
            "gesamtrechnung": "python3 modell/gesamtrechnung.py",
            "eingangswerte_verzeichnen": "python3 modell/eingangswerte.py",
            "eingangswerte_an_eurostat_pruefen": "python3 modell/eingangswerte.py --abrufen",
            "gesamtkonzept_bauen": "NODE_PATH=<pfad zu node_modules mit docx> node dokumente/werkzeuge/gesamtkonzept-bau.js && "
                                   "cd dokumente && soffice --headless --convert-to pdf TAX-2828-Gesamtkonzept.docx",
            "kurzfassung_bauen": "NODE_PATH=<...> node dokumente/werkzeuge/kurzfassung-bau.js && "
                                 "cd dokumente && soffice --headless --convert-to pdf TAX-2828-Kurzfassung.docx",
        },
        "voraussetzungen": {"python": ">= 3.11 (tomllib), nur Standardbibliothek",
                            "node": ">= 18 mit Paket docx (nur zum Bauen der Dokumente)",
                            "werkzeuge": "LibreOffice (soffice), poppler-utils (pdftotext, pdfinfo)"},
        "kernergebnisse": {k: J[k] for k in ("quote", "obergrenze", "mindestquote_streng", "klub_2028", "klub_2035",
                                              "klub_2060", "de_2028", "formel_einw", "formel_kind", "entlastung",
                                              "deckung_gesamt", "deckung_luecke", "zins_eff_2024", "pop_klub_mio",
                                              "bip28_klub_mrd")},
        "kernergebnisse_einheiten": "Quote, Obergrenze, Deckung in % (BIP bzw. Einzug); Dividenden EUR je Einwohner und Monat, "
                                    "Preise 2028; Formel EUR je Jahr 2028 nominal; BIP Mrd EUR 2028 nominal",
        "ergebnisdateien": {
            "daten/aggregate/gesamtrechnung.json": "alle Zahlen des Gesamtkonzepts, ungerundet",
            "daten/aggregate/gesamtrechnung_pfad.csv": "Zeitpfad 2028-2060",
            "daten/aggregate/gesamtrechnung_obergrenze.csv": "Risikofälle der Obergrenze",
            "daten/aggregate/deckung_quote.csv": "Deckung der Quote durch die Steuerpositionen (B12)",
            "daten/aggregate/eingangswerte.csv": "jeder amtliche Eingangswert mit Abruf-URL",
            "daten/aggregate/konzept_pruefung.csv": "Prüfung der Dokumente gegen die Rechnung",
            "daten/aggregate/projektstatus.md": "Ergebnis der Projektprüfung",
        },
        "bausteine": [{k: b[k] for k in ("id", "name", "pfad", "stand", "status", "pruefung", "anmerkung")} for b in bausteine],
        "nahtstellen": naehte,
        "quellen": quellen,
        "nicht_im_repository": ["Rohdaten jeder Art", "Taxplorer-Rohdatenbank (CC BY-NC-ND 4.0)",
                                "SOEP- und EU-SILC-Mikrodaten (Datenvertrag)", "Drittdateien (nur Manifest mit SHA-256)",
                                "Vorchat (Projektraum 2525 auf claude.ai, nicht öffentlich)"],
        "invarianten": [
            "Originalskripte in modell/rahmen/ werden nicht verändert (Prüfsummen).",
            "Dokumente nur über die Bauskripte erzeugen, nie von Hand ändern.",
            "Jede Rechnung ändert das Logbuch (neue Version, bewegte Zahl, Quelle).",
            "Korrekturnummern fortlaufend, nie neu vergeben; nächste freie Nummer steht in CLAUDE.md.",
            "Euro-Beträge immer mit Bezugsjahr und Preisbasis.",
            "OECD-Aufkommensrechnungen nur mit Panel _T.",
            "Eurostat je Land und Größe einzeln abrufen, alle Dimensionen festlegen.",
        ],
        "offene_punkte": "logbuch/Versionsgeschichte-TAX-2828-BandIII.md, Abschnitt 7",
    }
    (WURZEL / "projekt" / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    for f in FEHLER:
        print("  FEHLER:", f)
    print(f"projekt/manifest.json geschrieben ({len(bausteine)} Bausteine, {len(quellen)} Quellen); Fehler: {len(FEHLER)}")
    return 2 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
