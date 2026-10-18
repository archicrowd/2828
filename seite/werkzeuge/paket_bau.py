#!/usr/bin/env python3
"""Upload-Paket der Webseite. Seit v4.0: Fassung 4.0 „Das Goldene Drittel" (seite/stand-c, gebaut mit drittel_bau.py); vorher Stand B (v3.22.1).

Stellt zusammen, was auf dem Server die Seite zum Stand A ersetzt:
  de, en, fr, it, es, pl .html     aus seite/stand-c/ (gebaut mit drittel_bau.py)
  dokumente/*.pdf                  Konzept und Kurzfassung des Drittel-Systems (dokumente/entwurf/TAX-Drittel-*.pdf)
  index.html                       neu: leitet nach Browsersprache weiter (ohne Cookies), sonst Englisch
  da, nl, sl, et .html             neu: Weiterleitung auf en.html, weil diese Sprachen entfallen
Nicht im Paket: fonts/ (liegt auf dem Server und bleibt unverändert; Dateinamen werden geprüft).

Aufruf: python3 seite/werkzeuge/paket_bau.py [Zielordner]   (Vorgabe: seite/paket, nicht im Repository)
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

W = Path(__file__).resolve().parents[2]
QUELLE = W / "seite" / "stand-c"
PDFS = [W / "dokumente" / "entwurf" / "TAX-Drittel-Konzept.pdf", W / "dokumente" / "entwurf" / "TAX-Drittel-Kurzfassung.pdf"]
TITEL = "Das Goldene Drittel"
ZIEL = Path(sys.argv[1]) if len(sys.argv) > 1 else W / "seite" / "paket"
SPRACHEN = ["de", "en", "fr", "it", "es", "pl"]
ENTFALLEN = {"da": "Dansk", "nl": "Nederlands", "sl": "Slovenščina", "et": "Eesti"}
NAMEN = {"de": "Deutsch", "en": "English", "fr": "Français", "it": "Italiano", "es": "Español", "pl": "Polski"}
SCHRIFTEN_ALT = W / "seite" / "stand-a-national" / "de.html"

KOPF = """<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{titel}</title>{extra}
<style>body{{margin:0;background:#F5F5F3;color:#0F3A5F;font-family:'IBM Plex Mono',monospace;display:flex;
min-height:100vh;align-items:center;justify-content:center;text-align:center;padding:16px;box-sizing:border-box}}
h1{{font-family:system-ui,sans-serif;font-size:32px;margin:0 0 16px}}a{{color:#0F3A5F;margin:0 8px;line-height:2}}</style>
</head><body><main>"""


def index_html():
    links = " ".join(f'<a href="{s}.html" hreflang="{s}">{NAMEN[s]}</a>' for s in SPRACHEN)
    skript = ("<script>(function(){var s=%s,l=(navigator.languages||[navigator.language||'en']);"
              "for(var i=0;i<l.length;i++){var k=String(l[i]).slice(0,2).toLowerCase();"
              "if(s.indexOf(k)>=0){location.replace(k+'.html');return}}location.replace('en.html')})();</script>"
              % str(SPRACHEN).replace(" ", ""))
    return KOPF.format(lang="en", extra=skript, titel=TITEL) + f"<h1>{TITEL}</h1><p>{links}</p></main></body></html>\n"


def weiterleitung(sp):
    return (KOPF.format(lang=sp, extra='\n<meta http-equiv="refresh" content="0; url=en.html">', titel=TITEL)
            + f'<h1>{TITEL}</h1><p>{ENTFALLEN[sp]}: <a href="en.html">English</a> · '
            + " ".join(f'<a href="{s}.html">{NAMEN[s]}</a>' for s in SPRACHEN if s != "en")
            + "</p></main></body></html>\n")


def main() -> int:
    # Schriften: neue Seiten dürfen nur Dateien verlangen, die die alte Seite schon verlangt (liegen auf dem Server)
    muster = re.compile(r"url\('(fonts/[^']+)'\)")
    alt = set(muster.findall(SCHRIFTEN_ALT.read_text(encoding="utf-8")))
    for sp in SPRACHEN:
        neu = set(muster.findall((QUELLE / f"{sp}.html").read_text(encoding="utf-8")))
        if not neu <= alt:
            sys.exit(f"FEHLER: {sp}.html verlangt Schriften, die auf dem Server fehlen könnten: {sorted(neu - alt)}")
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    (ZIEL / "dokumente").mkdir(parents=True)
    for sp in SPRACHEN:
        shutil.copy2(QUELLE / f"{sp}.html", ZIEL / f"{sp}.html")
    for pdf in PDFS:
        shutil.copy2(pdf, ZIEL / "dokumente" / pdf.name)
    (ZIEL / "index.html").write_text(index_html(), encoding="utf-8")
    for sp in ENTFALLEN:
        (ZIEL / f"{sp}.html").write_text(weiterleitung(sp), encoding="utf-8")
    dateien = sorted(p for p in ZIEL.rglob("*") if p.is_file())
    zipname = ZIEL.parent / "Webseite-v4.0.zip"
    with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as z:
        for p in dateien:
            z.write(p, p.relative_to(ZIEL))
    for p in dateien:
        print(f"{p.relative_to(ZIEL)!s:<38}{p.stat().st_size:>9} Bytes")
    print(f"Schriften geprüft: {len(alt)} Dateien in fonts/ werden verlangt, alle schon von der alten Seite. "
          f"Paket: {zipname}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
