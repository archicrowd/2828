#!/usr/bin/env python3
"""Prüft den Zusammenhalt des Repositorys.

1. Bausteinregister (projekt/bausteine.csv): jeder Pfad existiert; jeder Ordner der zweiten Ebene
   unter modell/, seite/, dokumente/, daten/ gehört zu einem Baustein (keine verwaisten Teile).
2. Nahtstellen (projekt/nahtstellen.csv): Bausteine existieren; offene und fehlende Nähte werden gezählt.
3. Version: parameter.toml, README, INDEX und Logbuch Band III nennen denselben Modellstand.
4. Korrekturnummern: lückenlos von 1 bis zur höchsten; CLAUDE.md nennt die nächste freie Nummer.
5. Inhalt: keine E-Mail-Adressen außer der Projektadresse, keine Rohdatenformate, keine Datei über 5 MB,
   Dateinamen ohne Umlaute und Leerzeichen, 'PANELAI' nur in den dafür vorgesehenen Dateien.
6. Prüfsummen (projekt/pruefsummen.sha256): Originale (Rahmenskripte, Logbuch Band I, Gesamtkonzept)
   sind unverändert. Mit --aktualisieren werden die Summen neu geschrieben (bewusste Entscheidung,
   im Logbuch zu vermerken).

Ausgabe: daten/aggregate/projektstatus.md. Rückgabe 0, wenn kein Fehler vorliegt (offene Nähte sind kein Fehler).
"""
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PROJEKT_MAIL = "2828@archicrowd.de"
ERLAUBT_PANELAI = {"modell/rechnungen/oecd-cbcr/wirkung_28.py", "modell/rechnungen/oecd-cbcr/t1-panelAI.csv",
                   "CLAUDE.md", "projekt/pruefe_projekt.py", "logbuch/Versionsgeschichte-TAX-2828.md",
                   "modell/rechnungen/LIESMICH.md", "seite/stand-a-national/quelltext/oecd/wirkung_28.py"}
VERBOTENE_ENDUNGEN = {".zip", ".parquet", ".sav", ".dta", ".7z", ".gz"}
BEKANNTE_DOPPELTE_NUMMERN = {15, 16}  # Band I, Abschnitt 4 (siehe logbuch/HERKUNFT.md)
SUMMEN = WURZEL / "projekt" / "pruefsummen.sha256"
SUMMEN_DATEIEN = (
    ["logbuch/Versionsgeschichte-TAX-2828.md", "dokumente/archiv/TAX-2828-Gesamtkonzept-2026-10-04.pdf",
     "dokumente/archiv/TAX-2828-Gesamtkonzept-2026-10-04.docx"]
    + sorted(str(p.relative_to(WURZEL)) for p in (WURZEL / "modell" / "rahmen").glob("*.py"))
)

FEHLER: list[str] = []
HINWEISE: list[str] = []


def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=WURZEL, capture_output=True,
                         text=True, check=True).stdout.splitlines()
    return [WURZEL / p for p in out if (WURZEL / p).is_file()]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pruefe_register() -> list[dict]:
    with (WURZEL / "projekt" / "bausteine.csv").open(encoding="utf-8", newline="") as f:
        bausteine = list(csv.DictReader(f))
    abgedeckt = []
    for b in bausteine:
        for pfad in b["pfad"].split(";"):
            pfad = pfad.strip()
            if not (WURZEL / pfad).exists():
                FEHLER.append(f"Baustein {b['id']}: Pfad fehlt: {pfad}")
            abgedeckt.append(pfad)
    for wurzel in ("modell", "seite", "dokumente", "daten"):
        for kind in sorted((WURZEL / wurzel).iterdir()):
            rel = f"{wurzel}/{kind.name}" + ("/" if kind.is_dir() else "")
            if kind.name.startswith(".") or kind.name in ("__pycache__", "roh"):
                continue
            if not any(rel == a or rel.startswith(a) or a.startswith(rel) or a == f"{wurzel}/{kind.name}"
                       for a in abgedeckt):
                FEHLER.append(f"verwaist (kein Baustein): {rel}")
    ids = {b["id"] for b in bausteine}
    if len(ids) != len(bausteine):
        FEHLER.append("doppelte Baustein-ID")
    return bausteine


def pruefe_nahtstellen() -> list[dict]:
    with (WURZEL / "projekt" / "nahtstellen.csv").open(encoding="utf-8", newline="") as f:
        naht = list(csv.DictReader(f))
    for n in naht:
        if n["status"] in ("offen", "fehlt"):
            HINWEISE.append(f"Naht {n['id']} {n['status']}: {n['von']} -> {n['nach']}: {n['beleg_oder_offener_punkt']}")
    return naht


def pruefe_version() -> str:
    import tomllib
    with (WURZEL / "modell" / "parameter.toml").open("rb") as f:
        daten = tomllib.load(f)
    v_param = daten.get("version") or next((t["version"] for t in daten.values() if isinstance(t, dict) and "version" in t), "?")
    funde = {"parameter.toml": v_param}
    for name, pfad, muster in (("README", "README.md", r"Modellstand: (v[\d.]+)"),
                               ("INDEX", "INDEX.md", r"Modellstand (v[\d.]+)"),
                               ("Band III", "logbuch/Versionsgeschichte-TAX-2828-BandIII.md", r"Modellstand \*\*(v[\d.]+)\*\*")):
        m = re.search(muster, (WURZEL / pfad).read_text(encoding="utf-8"))
        funde[name] = m.group(1) if m else "?"
    if len(set(funde.values())) != 1:
        FEHLER.append(f"Modellstand uneinheitlich: {funde}")
    return v_param


def pruefe_korrekturen() -> int:
    nummern = []
    for pfad in ("logbuch/Versionsgeschichte-TAX-2828.md", "logbuch/Versionsgeschichte-TAX-2828-BandII.md",
                 "logbuch/Versionsgeschichte-TAX-2828-BandIII.md"):
        text = (WURZEL / pfad).read_text(encoding="utf-8")
        abschnitt = text.split("## 4 |", 1)[1].split("## 5 |", 1)[0].split("## 7 |", 1)[0] if "## 4 |" in text else ""
        nummern += [int(m.group(1)) for m in re.finditer(r"^\| (\d{1,3}) \|", abschnitt, re.M)]
    menge = set(nummern)
    hoechste = max(menge)
    fehlend = [n for n in range(1, hoechste + 1) if n not in menge]
    if fehlend:
        FEHLER.append(f"Korrekturnummern fehlen: {fehlend}")
    doppelt = {n for n in menge if nummern.count(n) > 1} - BEKANNTE_DOPPELTE_NUMMERN
    if doppelt:
        FEHLER.append(f"Korrekturnummern doppelt vergeben: {sorted(doppelt)}")
    m = re.search(r"Nächste freie Nummer: (\d+)", (WURZEL / "CLAUDE.md").read_text(encoding="utf-8"))
    if not m or int(m.group(1)) != hoechste + 1:
        FEHLER.append(f"CLAUDE.md nennt nächste freie Nummer {m.group(1) if m else '?'}, erwartet {hoechste + 1}")
    return hoechste


def pruefe_inhalt() -> int:
    dateien = tracked_files()
    for p in dateien:
        rel = str(p.relative_to(WURZEL))
        if rel.startswith(".git/"):
            continue
        if p.suffix.lower() in VERBOTENE_ENDUNGEN:
            FEHLER.append(f"Rohdatenformat im Repository: {rel}")
        if p.stat().st_size > 5_000_000:
            FEHLER.append(f"Datei über 5 MB: {rel}")
        if re.search(r"[^\x00-\x7F ]| ", rel):
            FEHLER.append(f"Dateiname mit Umlaut oder Leerzeichen: {rel}")
        if p.suffix.lower() in {".md", ".py", ".csv", ".json", ".toml", ".txt", ".html", ".js", ".cff"}:
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for mail in set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", text)):
                if mail != PROJEKT_MAIL and not mail.endswith("@anthropic.com"):
                    FEHLER.append(f"E-Mail-Adresse in {rel}: {mail}")
            if "PANELAI" in text and rel not in ERLAUBT_PANELAI:
                FEHLER.append(f"'PANELAI' außerhalb der vorgesehenen Dateien: {rel}")
    return len(dateien)


def pruefe_summen(aktualisieren: bool) -> None:
    if aktualisieren:
        SUMMEN.write_text("".join(f"{sha(WURZEL / p)}  {p}\n" for p in SUMMEN_DATEIEN), encoding="utf-8")
        HINWEISE.append("Prüfsummen neu geschrieben (im Logbuch zu vermerken)")
        return
    soll = {}
    for zeile in SUMMEN.read_text(encoding="utf-8").splitlines():
        h, p = zeile.split("  ", 1)
        soll[p] = h
    for p in SUMMEN_DATEIEN:
        if p not in soll:
            FEHLER.append(f"Prüfsumme fehlt: {p}")
        elif sha(WURZEL / p) != soll[p]:
            FEHLER.append(f"Original verändert (Prüfsumme weicht ab): {p}")
    for p in soll:
        if not (WURZEL / p).exists():
            FEHLER.append(f"Original fehlt: {p}")


def schreibe_bericht(bausteine, naht, version, hoechste, anzahl) -> None:
    zeilen = [f"# Projektstatus (erzeugt von projekt/pruefe_projekt.py)", "",
              f"Modellstand {version} · höchste Korrekturnummer {hoechste} · {anzahl} Dateien im Repository", "",
              "## Bausteine", "", "| ID | Baustein | Stand | Status | Prüfung |", "|---|---|---|---|---|"]
    for b in bausteine:
        zeilen.append(f"| {b['id']} | {b['name']} | {b['stand']} | {b['status']} | {b['pruefung']} |")
    zeilen += ["", "## Nahtstellen", "", "| ID | von | nach | Status |", "|---|---|---|---|"]
    for n in naht:
        zeilen.append(f"| {n['id']} | {n['von']} | {n['nach']} | {n['status']} |")
    zeilen += ["", "## Ergebnis dieses Laufs", ""]
    zeilen += [f"- FEHLER: {f}" for f in FEHLER] or ["- keine Fehler"]
    zeilen += [f"- Hinweis: {h}" for h in HINWEISE]
    (WURZEL / "daten" / "aggregate" / "projektstatus.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")


def main() -> int:
    aktualisieren = "--aktualisieren" in sys.argv
    bausteine = pruefe_register()
    naht = pruefe_nahtstellen()
    version = pruefe_version()
    hoechste = pruefe_korrekturen()
    anzahl = pruefe_inhalt()
    pruefe_summen(aktualisieren)
    schreibe_bericht(bausteine, naht, version, hoechste, anzahl)
    print(f"Projektprüfung: {len(FEHLER)} Fehler, {len(HINWEISE)} Hinweise (Bausteine {len(bausteine)}, Nähte {len(naht)}).")
    for f in FEHLER:
        print("  FEHLER:", f)
    for h in HINWEISE:
        print("  Hinweis:", h)
    return 2 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
