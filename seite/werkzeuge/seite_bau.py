#!/usr/bin/env python3
"""Baut die Webseite zum Stand B in allen Sprachfassungen: seite/stand-b/<sprache>.html.

Gestaltung: Das Stylesheet wird unverändert aus der veröffentlichten Seite (seite/stand-a-national/de.html)
übernommen; neue Bauteile ergänzen es nur. Zahlen: ausschließlich aus daten/aggregate/gesamtrechnung.json
(modell/gesamtrechnung.py), laender_2024.csv und moeglichkeitsraum.csv. Texte: seite/werkzeuge/sprachen/<sprache>.json
(Deutsch ist die Referenz; jede Sprache muss dieselben Schlüssel haben). Referenzland aller Länderangaben: Deutschland.
Quellen der Länderbeispiele und Zeitreihen: seite/stand-b/QUELLEN.md.

Platzhalter in der Vorlage: @@schluessel@@ = Text der Sprache (darin {wert} = Zahl, sprachgerecht formatiert).

Aufruf:  python3 seite/werkzeuge/seite_bau.py
"""
import csv
import json
import re
import shutil
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
ALT = WURZEL / "seite" / "stand-a-national" / "de.html"
ZIEL = WURZEL / "seite" / "stand-b"
SPRACHEN_DIR = Path(__file__).resolve().parent / "sprachen"
SPRACHEN = ["de", "en", "fr", "it", "es", "pl"]
J = json.loads((WURZEL / "daten/aggregate/gesamtrechnung.json").read_text(encoding="utf-8"))
with open(WURZEL / "daten/aggregate/moeglichkeitsraum.csv", encoding="utf-8") as f:
    RAUM = list(csv.DictReader(f))

TARIF = [(12348, 0), (25000, 9), (40000, 16), (55000, 21), (70000, 26), (None, 28)]
# Eurostat-Kürzel -> ISO-Kürzel für die Ländernamen der Sprache (Intl.DisplayNames im Browser)
ISO = {"UK": "GB", "EL": "GR"}

# Zeitreihen der Grafik „Wohin die Reise geht" (Quellen: seite/stand-b/QUELLEN.md)
SP = json.loads((WURZEL / "daten/aggregate/schuldenpfad.json").read_text(encoding="utf-8"))
ZEITREIHEN = {
    "schuld_hist_jahre": SP["jahre"],
    "schuld_hist": [round(x, 2) for x in SP["klub"]],
    "schuld_prog_jahre": SP["prog_jahre"],
    "schuld_prog": [round(x, 2) for x in SP["prog"]],
    "co2_hist_jahre": list(range(2010, 2026)),
    "co2_hist": [942, 922, 926, 944, 904, 907, 911, 894, 858, 800, 730, 762, 750, 674, 650, 649],
    "co2_ziel_jahre": [2025, 2030, 2040, 2045],
    "co2_ziel": [649, 438, 150, 0],
}

# Zahlenformat je Sprache: Tausender, Dezimal, Euro vor/nach, Prozent mit/ohne Leerzeichen
FORMAT = {
    "de": (".", ",", "nach", " "), "en": (",", ".", "vor", ""), "fr": (" ", ",", "nach", " "),
    "it": (".", ",", "nach", " "), "es": (".", ",", "nach", " "), "pl": (" ", ",", "nach", " "),
}


def zahl(x, nk, sp):
    tau, dez, _, _ = FORMAT[sp]
    s = f"{x:,.{nk}f}"
    return s.replace(",", "\0").replace(".", dez).replace("\0", tau)


def eur(x, sp, nk=0):
    z = zahl(x, nk, sp)
    return f"€{z}" if FORMAT[sp][2] == "vor" else f"{z} €"


def pct(x, sp, nk=0):
    return f"{zahl(x, nk, sp)}{FORMAT[sp][3]}%".replace(" %", " %")


def stylesheet() -> str:
    s = ALT.read_text(encoding="utf-8")
    return s[s.find("<style>") + 7:s.find("</style>")]


ZUSATZ_CSS = """
/* ---- Ergänzungen Stand B (gleiche Farben, Schriften, Linien) ---- */
.flow{border:1.5px solid var(--ink);border-radius:3px;background:#fff;padding:26px;margin-top:30px}
@media(max-width:640px){.flow{padding:16px}}
.flow .row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.flow .year{font-family:var(--mono);font-size:30px;font-weight:500}
.stack{display:flex;height:46px;border:1px solid var(--ink);border-radius:2px;overflow:hidden;margin:16px 0 8px;position:relative}
.stack i{display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:12.5px;font-style:normal;color:#fff;transition:flex-basis .35s;white-space:nowrap;overflow:hidden}
.stack .sa{background:var(--ink)}.stack .sb{background:#6497B8}.stack .sd{background:var(--accent)}
.stack .cap{position:absolute;top:-4px;bottom:-4px;border-left:2px dashed var(--warn)}
.flowleg{display:flex;gap:20px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;color:var(--dim)}
.flowleg b{display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-1px}
.ebenen{width:100%;height:auto;display:block;margin:6px 0 4px}
.ebenen .bx{fill:#fff;stroke:var(--ink);stroke-width:1.5}
.ebenen text{font-family:var(--disp);fill:var(--ink)}
.ebenen .s{font-family:var(--mono);font-size:12px;fill:var(--dim)}
.ebenen .ar{stroke:var(--ink);stroke-width:1.5;fill:none;marker-end:url(#pf)}
.ebenen .ag{stroke:var(--accent);stroke-width:2;fill:none;marker-end:url(#pg)}
.ebenen.mob{display:none;max-width:420px;margin:6px auto 4px}
@media(max-width:640px){.ebenen.wide{display:none}.ebenen.mob{display:block}}
#chart2{width:100%;height:auto;display:block}
#chart2 .grid{stroke:var(--line-soft)}
#chart2 .axis{font-family:var(--mono);font-size:12px;fill:var(--dim)}
#chart2 .hist{stroke:var(--ink);fill:none;stroke-width:2.5;stroke-linecap:round}
#chart2 .ohne{stroke:var(--warn);fill:none;stroke-width:2.5;stroke-dasharray:7 6;stroke-linecap:round}
#chart2 .mit{stroke:var(--accent);fill:none;stroke-width:3.5;stroke-linecap:round}
#chart2 .prog{stroke:var(--accent);fill:none;stroke-width:2.5;stroke-dasharray:6 6;stroke-linecap:round}
#chart2 .marker{stroke:var(--line);stroke-dasharray:3 4}
.legend .l-prog i{border-color:var(--accent);border-top-style:dashed}
.kicker{font-family:var(--disp);font-weight:700;font-size:clamp(34px,5.2vw,56px);line-height:1.05;letter-spacing:-.5px;margin-bottom:10px}
.kicker.alt{color:var(--warn)}.kicker.neu{color:var(--accent)}
.raum{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px;margin:14px 0 18px}
.raum button{font-family:var(--mono);font-size:12px;text-align:left;padding:7px 9px;border:1px solid var(--line);background:#fff;border-radius:3px;cursor:pointer;color:var(--dim);display:flex;justify-content:space-between;gap:6px}
.raum button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.raum button.neu{border-color:var(--accent)}
.raum button.neu[aria-pressed=true]{background:var(--accent);border-color:var(--accent)}
.raum button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.schwelle{position:relative;height:30px;background:var(--line-soft);border-radius:2px;overflow:visible;margin:8px 0 26px}
.schwelle>i{display:block;height:100%;background:var(--accent);border-radius:2px;transition:width .35s}
.schwelle>i.unter{background:var(--warn)}
.schwelle .us{position:absolute;top:-6px;bottom:-6px;border-left:2px dashed var(--ink)}
.schwelle .us span{position:absolute;top:38px;left:-40px;width:80px;text-align:center;font-family:var(--mono);font-size:11px;color:var(--ink)}
.land{border:1px solid var(--line);border-radius:3px;background:#fff;padding:20px 22px}
.land .n{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.land h3{font-family:var(--disp);font-size:17px;font-weight:500;margin:6px 0 6px}
.land p{font-size:15px;color:var(--dim);line-height:1.55}
.land .k{font-family:var(--mono);font-size:13px;color:var(--ink);background:var(--paper);border:1px solid var(--line-soft);border-radius:2px;padding:3px 8px;display:inline-block;margin:2px 0 8px}
.anl a{all:unset;cursor:pointer;border:1.5px solid var(--ink);border-radius:3px;padding:20px;background:#fff;display:block}
.anl a:hover{border-color:var(--accent)}
.anl a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
"""

VORLAGE = (Path(__file__).resolve().parent / "vorlage.html").read_text(encoding="utf-8")


def werte(sp):
    """Alle Zahlen, die in Texten vorkommen, sprachgerecht formatiert."""
    og = J["obergrenze"]
    return {
        "erw_2028": eur(J["erw_2028"], sp), "kind_2028": eur(J["kind_2028"], sp),
        "erw_2060": eur(J["erw_2060"], sp), "mehr": pct(J["anteil_mit_mehr_de"], sp),
        "keil_de": pct(J["abgabenkeil_de_2024"], sp, 1), "keil_oecd": pct(J["abgabenkeil_oecd_2024"], sp, 1),
        "abgeltung": pct(J["abgeltungsteuer_de"], sp, 1), "og": pct(og, sp), "mind": pct(100 - og, sp),
        "formel_einw": eur(J["formel_einw"], sp), "formel_kind": eur(J["formel_kind"], sp),
        "tief_jahr": str(J["kl_tief_jahr"]), "d0": pct(J["tabelle_pfad"][0]["d"], sp), "d1": pct(J["tabelle_pfad"][5]["d"], sp),
        "uk": zahl(next(float(x["einwohner_mio"]) for x in RAUM if x["land"] == "UK"), 1, sp),
        "ca": zahl(next(float(x["einwohner_mio"]) for x in RAUM if x["land"] == "CA"), 1, sp),
        "version": J["version"], "fassung": J["fassung"],
        "ee_verw": pct(5.8, sp, 1), "de_verw": pct(16.8, sp, 1), "eur100": eur(100, sp),
        "p0": pct(0, sp), "p28": pct(28, sp), "p01_1": f"{zahl(0.1, 1, sp)}–{pct(1, sp)}",
    }


def baue(sp, T, V):
    def t(k):
        return T[k].format_map(V)

    tarif = "\n".join(
        f'<div><b class="t{i}">{pct(s, sp)}</b><em>{t("tarif_bis").format(x=eur(g, sp)) if g else t("tarif_darueber")}</em></div>'
        for i, (g, s) in enumerate(TARIF, 1))
    r = J["reihe_erw"]["1,0"]
    xs = J["reihe_jahre"]
    lo, hi = min(r) * 0.97, max(r) * 1.02
    pts = " ".join(f"{(x - xs[0]) / (xs[-1] - xs[0]) * 280 + 10:.1f},{70 - (v - lo) / (hi - lo) * 55:.1f}" for x, v in zip(xs, r))
    spark = (f'<svg class="spark" viewBox="0 0 300 84" role="img" aria-label="{t("baustein_div_titel")}">'
             f'<polyline points="{pts}" fill="none" stroke="#1D7A4F" stroke-width="2.5"/>'
             f'<text x="10" y="82" font-family="IBM Plex Mono,monospace" font-size="10" fill="#5A7186">2028 · {eur(J["erw_2028"], sp)}</text>'
             f'<text x="290" y="12" text-anchor="end" font-family="IBM Plex Mono,monospace" font-size="10" fill="#1D7A4F">2060 · {eur(J["erw_2060"], sp)}</text></svg>')
    raum_knoepfe = "".join(
        f'<button type="button" aria-pressed="false" data-k="{x["land"]}" data-iso="{ISO.get(x["land"], x["land"])}" data-de="{x["name"]}"'
        + (' class="neu"' if x["land"] == "CA" else "")
        + f'><span class="nm">{x["name"]}</span><span>{zahl(float(x["einwohner_mio"]), 1, sp)}</span></button>'
        for x in RAUM if x["land"] != "US")
    q = J["quote"]
    daten = {
        "lang": sp, "fmt": FORMAT[sp], "jahre": J["reihe_jahre"], "erw": J["reihe_erw"], "a": J["reihe_a"],
        "div": J["reihe_div"], "b": J["b_fach"], "q": q, "og": J["obergrenze"], "einzugAnteil": (q - J["boden"]) / q,
        "einw": J["formel_einw"], "kind": J["formel_kind"], "fachKopf": J["tabelle_einzug"][5][2],
        "verwAnt": J["verw_anteil_pct"], "tarif": [[g if g else 1e12, s] for g, s in TARIF],
        "raum": {x["land"]: float(x["einwohner_mio"]) for x in RAUM}, "us": next(float(x["einwohner_mio"]) for x in RAUM if x["land"] == "US"),
        "d": J["reihe_d"], "zeit": ZEITREIHEN, "T": {k: T[k] for k in T if k.startswith("js_")},
    }
    sprachwahl = "".join(f'<a href="{s}.html"{" class=\"active\"" if s == sp else ""} lang="{s}">{s.upper()}</a>' for s in SPRACHEN)
    ersetz = {"CSS": stylesheet() + ZUSATZ_CSS, "DATA": json.dumps(daten, ensure_ascii=False), "LANG": sp,
              "SPRACHWAHL": sprachwahl, "TARIF": tarif, "SPARK": spark, "RAUM": raum_knoepfe,
              "KIND_ANT": f"{J['kind_ant']:.1f}", "VERW_ANT": f"{J['verw_anteil_pct']:.1f}"}

    def fuelle(m):
        k = m.group(1)
        if k in ersetz:
            return ersetz[k]
        if k in T:
            return t(k)
        raise KeyError(f"{sp}: Schlüssel fehlt: {k}")
    return re.sub(r"@@([A-Za-z0-9_]+)@@", fuelle, VORLAGE)


def main():
    ref = json.loads((SPRACHEN_DIR / "de.json").read_text(encoding="utf-8"))
    ZIEL.mkdir(parents=True, exist_ok=True)
    for sp in SPRACHEN:
        T = json.loads((SPRACHEN_DIR / f"{sp}.json").read_text(encoding="utf-8"))
        fehlt, zuviel = set(ref) - set(T), set(T) - set(ref)
        if fehlt or zuviel:
            raise SystemExit(f"{sp}: Schlüssel weichen von de.json ab: fehlt {sorted(fehlt)}, zu viel {sorted(zuviel)}")
        html = baue(sp, T, werte(sp))
        (ZIEL / f"{sp}.html").write_text(html, encoding="utf-8")
        print(f"geschrieben: seite/stand-b/{sp}.html ({len(html)} Zeichen)")
    (ZIEL / "dokumente").mkdir(exist_ok=True)
    for name in ("TAX-2828-Kurzfassung.pdf", "TAX-2828-Gesamtkonzept.pdf"):
        shutil.copy2(WURZEL / "dokumente" / name, ZIEL / "dokumente" / name)


if __name__ == "__main__":
    main()
