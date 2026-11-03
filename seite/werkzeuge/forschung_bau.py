#!/usr/bin/env python3
"""Forschungsseite für die wissenschaftliche Diskussion (GitHub Pages, Ordner docs/), Logbuch v4.56.

Empfehlung an die Initiative (01.11.2026): Startseite mit einer Seite je Kernthema (42.000-€-Fälle, Fonds, Mehrwertsteuer-Faktoren,
Grenzbelastung), Prüfprotokolle als Download, Forschungs-Kit (PDF und Zahlen zum Zitieren), Kontakt; später Working Paper mit DOI.
Alle Zahlen kommen aus den Ergebnisdateien (daten/aggregate/), nicht von Hand. Aufruf in der Kette (modell/alles.py) hält sie aktuell.
PDFs (Prüfprotokolle, Kit) entstehen mit Chromium aus Markdown/HTML; ohne --pdf werden nur HTML und Daten geschrieben.
Ausgabe: docs/ (v4.57: englische Hauptfassung im Wurzelverzeichnis aus forschung_en.py, deutsche Fassung in docs/de/, gemeinsam style.css,
data/ und downloads/)
"""
import re, csv, hashlib, html, json, shutil, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parents[2]
AGG = W / "daten" / "aggregate"
OUT = W / "docs"
J = lambda n: json.loads((AGG / n).read_text(encoding="utf-8"))
VERSION = tomllib.loads((W / "modell" / "parameter.toml").read_text(encoding="utf-8"))["modell"]["version"]
KONTAKT = "tax.better@archicrowd.de"
SEITE = "https://www.archicrowd.de"
DATUM = "1. November 2026"
PAGES = "https://archicrowd.github.io/goldenes-drittel/"
REPO = "https://github.com/archicrowd/2828"   # öffentlich seit 2.11.2026 (Korrektur 84; vorher privat, Korrektur 82)
# Zenodo (Archiv des öffentlichen Repositorys goldenes-drittel, eingeschaltet 01.11.2026): Concept-DOI zeigt immer auf die neueste Version
DOI_KONZEPT = "10.5281/zenodo.23855733"
DOI_ARCHIV = {"v4.58": "10.5281/zenodo.23855734"}   # Modellstand → DOI der archivierten Fassung (Release v4.58.1)


def _korrekturen():
    """Höchste vergebene Korrekturnummer aus den Korrekturtabellen des Logbuchs (alle Nummern bis dahin besetzt; Korrektur 83)."""
    t = "".join((W / "logbuch" / n).read_text(encoding="utf-8") for n in ("Versionsgeschichte-TAX-2828-BandII.md", "Versionsgeschichte-TAX-2828-BandIII.md"))
    return max(int(m) for m in re.findall(r"^\| (\d+) \|", t, re.M))


def _stufen():
    t = (W / "modell" / "alles.py").read_text(encoding="utf-8")
    return len(re.findall(r'^\s*\("', t[t.index("STUFEN = ["):], re.M))


KORREKTUREN, STUFEN = _korrekturen(), _stufen()
GEPRUEFT = "v4.42"   # letzter von einer Prüfung erfasster Modellstand (dritte Prüfung, Commit 43f7888c)
# Änderungen seit dem geprüften Stand: (Version, was, bewegte Zahl) – aus dem Logbuch Band III; nach jeder Version mit Rechenwirkung ergänzen
SEIT_PRUEFUNG = [
 ("v4.46", "Antworten auf die dritte Prüfung: Korrekturen 73–76 (Ausweis), Raster Zins × Wachstum", "keine geltende Zahl"),
 ("v4.47", "Grenzbelastung bereinigt um Gegenwerte (Prüfrechnung, Z17)", "keine geltende Zahl"),
 ("v4.49–v4.50", "Gestaltungsentscheidungen E12–E15 (Aufstockung, Sperrkonto, Kürzung, Dividende, Label)", "keine Rechnung"),
 ("v4.51", "Ländermodelle gegen OECD Taxing Wages 2026; Korrekturen 77–79 (prime d'activité 59,85 %, forfait logement)", "Frankreich: heute bei halbem SMIC 1.219 → 1.136 € je Monat"),
 ("v4.52", "Weitergabe nur aus entfallenden Beiträgen zur sozialen Sicherung (Beschluss E16); Korrektur 80", "Durchschnittslohn, allein: FR +390 → +286 €, ES +350 → +321 €, PL +1.474 → +1.404 zł"),
 ("v4.53", "Kennzahlen maschinell gegen die Ergebnisdateien geprüft; Korrektur 81", "keine Rechnung; veraltete Angaben berichtigt"),
 ("v4.54", "Mehrwertsteuer nach Einkommen für Frankreich (Eurostat HBS 2020)", "FR Durchschnittslohn +286 → +276 €"),
 ("v4.57", "Haushaltstypen je Land (neue Ausgabe)", "keine geltende Zahl; neue Werte Z20–Z34 der englischen Fassung"),
 ("v4.58", "Prüfstand auf der Seite; Korrektur 83", "keine Rechnung"),
 ("v4.59", "Archiv auf Zenodo, DOI auf der Seite", "keine Rechnung"),
 ("v4.60", "Working Paper (Entwurf, englisch) aus den Ergebnisdateien", "keine Rechnung"),
 ("v4.61", "Working Paper: Ziele und Bewertung an den Zielen", "keine Rechnung"),
 ("v4.62", "Working Paper: Klima und Label als wirtschaftlicher Anreiz", "keine Rechnung"),
 ("v4.63", "Working Paper veröffentlicht (Seite, Kit)", "keine Rechnung"),
 ("v4.64", "Prüfprogramm der Nachprüfung bis v4.63 erweitert", "keine Rechnung"),
 ("v4.65", "Antworten auf B25–B29 (Ausweis), Webseite, Korrektur 84", "keine Zahl; neues Feld in fondszins.json"),
 ("v4.66", "Prüfungen als interne Prüfungen bezeichnet; Prüfbericht der Nachprüfung veröffentlicht", "keine Rechnung"),
]


def seit_pruefung_html(kopf=("Version", "Änderung", "Bewegte Zahl"), zeilen=None):
    return tabelle(list(kopf), [list(z) for z in (zeilen or SEIT_PRUEFUNG)])


def de(x, n=0):
    s = f"{abs(x):,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if x < 0 else "") + s


def wert(x):
    """Zahl zum Zitieren: Jahre ohne Tausenderpunkt, Dezimalstellen wie in der Ergebnisdatei."""
    if isinstance(x, str):
        return x
    if isinstance(x, int) or float(x).is_integer():
        return str(int(x)) if 1900 < x < 2200 else de(x)
    return de(x, len(repr(float(x)).split(".")[1]))


def pm(x, n=0):
    return ("+" if x > 0 else "") + de(x, n)


# ---------------- Daten
H = J("haushalte33.json")
FG = J("fonds_geltend.json")
FZ = J("fondszins.json")
GB = J("grenzbelastung33.json")
MV = J("mwst_verteilung.json")
ML = J("mwst_laender.json")
PN = J("preisniveau33.json")
GL = J("gesamtlast33.json")
NZ = J("netz33.json")
RB = J("regel_boden.json")
AL = J("altlasten.json")
MI = J("mikro_de.json")
RK = J("rentner_kombi.json")
VL = J("validierung_laender.json")
VH = J("verrechnung_haushalte.json")
ZR = GL["reihe"][0]
DIV_ERW = NZ["beschluss"]["reihe"][0]["dividende_erw_eur2026"] * RB["topf"]
TYPEN = ["alleinstehend", "alleinerziehend, 1 Kind", "Paar, ein Einkommen, 2 Kinder"]
ZU_DE = VH["laender"]["DE"]["zuschlag_verrechnung_2028"]


def fall(jahr, typ, wg, zu, vs, brutto=42000):
    f = next(f for f in H["faelle"] if f["jahr"] == jahr and f["haushalt"] == typ and f["weitergabe_ag"] == wg
             and abs(f["zuschlag_pct"] - zu) < 1e-9 and abs(f["vorsorge_satz"] - vs) < 1e-9)
    return next(z for z in f["zeilen"] if z["brutto"] == brutto)


MB = MI["basis"]["ergebnis"]["0.8"]
RE = RK["varianten"][4]

# ---------------- Zahlen zum Zitieren (je Zeile: Größe, Wert, Einheit, Bezug, Datei/Pfad, Status)
ZAHLEN = [
 ("Z01", "Transformationsdividende je Erwachsenem (Deutschland)", round(DIV_ERW), "€ je Monat", "2028, Kaufkraft 2026", "netz33.json beschluss/reihe/0 × regel_boden.json topf", "geltend"),
 ("Z02", "Transformationsdividende je Kind (Deutschland)", round(DIV_ERW * 0.8), "€ je Monat", "2028, Kaufkraft 2026", "wie Z01, Kinderanteil 0,8", "geltend"),
 ("Z03", "Vorteil alleinstehend, 42.000 € brutto (Deutschland)", fall(2028, TYPEN[0], 0.8, ZU_DE, 0.1)["differenz_monat"], "€ je Monat", "2028, Kaufkraft 2026; Weitergabe 80 %, Zuschlag DE 15,0 %, Pflichtvorsorge 10 %", "haushalte33.json faelle", "geltend"),
 ("Z04", "Vorteil Paar, ein Einkommen, 2 Kinder, 42.000 € brutto", fall(2028, TYPEN[2], 0.8, ZU_DE, 0.1)["differenz_monat"], "€ je Monat", "wie Z03", "haushalte33.json faelle", "geltend"),
 ("Z05", "Erwerbsfähige Haushalte mit mehr verfügbarem Einkommen (Deutschland)", MB["erwerbsfaehige_haushalte"]["anteil_mehr_haushalte_pct"], "%", "2028; synthetische Mikrosimulation, Weitergabe 80 %", "mikro_de.json basis/ergebnis/0.8", "Prüfrechnung"),
 ("Z06", "Alle Haushalte mit mehr verfügbarem Einkommen (Deutschland)", MB["gesamt"]["anteil_mehr_haushalte_pct"], "%", "wie Z05", "mikro_de.json basis/ergebnis/0.8/gesamt", "Prüfrechnung"),
 ("Z07", "Rentnerhaushalte mit mehr (Rentnerregel E)", RE["anteil_mehr_pct"], "%", "2028, Kaufkraft 2026", "rentner_kombi.json varianten/4", "geltend"),
 ("Z08", "Rentnerhaushalte, Veränderung im Mittel (Rentnerregel E)", RE["mittel_monat"], "€ je Monat", "wie Z07", "rentner_kombi.json varianten/4", "geltend"),
 ("Z09", "Beitrag zum gemeinsamen Fonds der 30 Staaten", FG["beitrag_pct_bip"], "% des BIP", "jährlich bis zur Tilgung", "fonds_geltend.json", "geltend"),
 ("Z10", "Altlastenzuschlag auf alle Steuern (gemeinsamer Satz)", FG["zuschlag_auf_alle_steuern_pct"], "%", "Fondszins 2,45 %", "fonds_geltend.json", "geltend"),
 ("Z11", "Schuldenquote des Fonds, Spitze", FG["schuldenquote_spitze"], "% des BIP", f"im Jahr {FG['spitzenjahr']}", "fonds_geltend.json", "geltend"),
 ("Z12", "Tilgung des Fonds abgeschlossen", FG["zieljahr"], "Jahr", "", "fonds_geltend.json", "geltend"),
 ("Z13", "Altrentenansprüche über der Dividende (Z)", AL["beschluss"]["verhandlungsmasse_z_2028_pct_bip"], "% des BIP", "2028, Mittel der Staaten", "altlasten.json beschluss", "geltend"),
 ("Z14", "Gesamtlast Steuern und Fonds", ZR["a_steuern_und_fonds"], "% des BIP", "2028; heute 40,76 % (Eurostat 2024)", "gesamtlast33.json reihe/0", "geltend"),
 ("Z15", "Gesamtlast mit Pflichtvorsorge (eigenes Konto)", ZR["b_mit_pflichtvorsorge"], "% des BIP", "2028", "gesamtlast33.json reihe/0", "geltend"),
 ("Z16", "Kosten des starken Netzes", NZ["beschluss"]["reihe"][0]["netz_pct_bip"], "% des BIP", "2028", "netz33.json beschluss/reihe/0", "geltend"),
 ("Z17", "Grenzbelastung bei 60.000 € brutto: heute / neu 2028", f"{de(GB['zeilen'][5]['heute_pct'], 1)} / {de(GB['zeilen'][5]['neu_2028_pct'], 1)}", "% je zusätzlichem Euro", "alleinstehend; neu ohne Pflichtvorsorge (eigenes Konto)", "grenzbelastung33.json zeilen/5", "Prüfrechnung"),
 ("Z18", "Mehrwertsteuer-Mehrbelastung, Faktor unterste / oberste Einkommensklasse (DE)", f"{de(MV['klassen'][0]['phi']['mit_vorsteuer'][0], 2)} / {de(MV['klassen'][-1]['phi']['mit_vorsteuer'][0], 2)}", "relativ zum Mittel", "EVS 2023", "mwst_verteilung.json klassen", "geltend"),
 ("Z19", "Preisniveauschub durch die Mehrwertsteuer 2028", f"{de(PN['reihe'][0]['mwst_spanne_pct'][0], 1)} bis {de(PN['reihe'][0]['mwst_spanne_pct'][1], 1)}", "%", "einmalig; mechanisch 2,47 %", "preisniveau33.json reihe/0", "Prüfrechnung"),
]


def zahlen_dateien(ziel):
    (ziel / "data").mkdir(parents=True, exist_ok=True)
    kopf = ["id", "groesse", "wert", "einheit", "bezug", "datei_pfad", "status", "modellstand"]
    with open(ziel / "data" / "zahlen-zum-zitieren.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(kopf)
        for z in ZAHLEN:
            w.writerow(list(z) + [VERSION])
    (ziel / "data" / "zahlen-zum-zitieren.json").write_text(json.dumps(
        dict(modellstand=VERSION, stand=DATUM, lizenz="CC BY 4.0", zitiervorschlag=ZITAT,
             zahlen=[dict(zip(kopf, list(z) + [VERSION])) for z in ZAHLEN]), ensure_ascii=False, indent=1), encoding="utf-8")
    for n in ("haushalte33.json", "fonds_geltend.json", "fondszins.json", "grenzbelastung33.json", "mwst_verteilung.json",
              "mwst_laender.json", "preisniveau33.json", "validierung_laender.json", "mikro_de.json", "rentner_kombi.json",
              "altlasten.json", "gesamtlast33.json", "netz33.json", "regel_boden.json"):   # v4.65: Quellen von Z01/Z02, Z13–Z16 (Nachprüfung B25)
        shutil.copy(AGG / n, ziel / "data" / n)


ZITAT = (f"Initiative 28:28 (2026): Das Goldene Drittel – Forschungs-Kit und Zahlen zum Zitieren, Modellstand {VERSION}, {DATUM}. "
         f"Zenodo. https://doi.org/{DOI_KONZEPT}. Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0.")

# ---------------- HTML
CSS = """
:root{--ink:#0f3b5c;--text:#1d2a33;--muted:#5a7186;--line:#d8e1e8;--bg:#ffffff;--soft:#f3f6f8;--acc:#1b7a4b;--warn:#b4452f}
@media (prefers-color-scheme:dark){:root{--ink:#9cc3e4;--text:#e3e9ee;--muted:#a3b3c1;--line:#2c3a46;--bg:#121a21;--soft:#1a242d;--acc:#6cc79a;--warn:#e38b78}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.6 Georgia,"Times New Roman",serif}
header,main,footer{max-width:960px;margin:0 auto;padding:0 20px}
header{padding-top:28px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.marke{font:600 14px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.marke a{color:inherit;text-decoration:none}
nav{margin-top:10px;font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;flex-wrap:wrap;gap:4px 16px}
nav a{color:var(--ink)}nav a[aria-current]{font-weight:700;text-decoration:none}
h1{font:700 32px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);margin:32px 0 8px}
h2{font:700 22px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);margin:36px 0 8px}
h3{font:600 17px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif;margin:24px 0 6px}
p.lede{font-size:19px;color:var(--text)}
.meta{font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--muted)}
a{color:var(--ink)}
.karten{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:18px 0}
.karte{border:1px solid var(--line);border-radius:6px;padding:16px;background:var(--soft);text-decoration:none;color:var(--text);display:block}
.karte b{display:block;font:700 16px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);margin-bottom:6px}
.karte .wert{font:700 26px/1.2 ui-monospace,Menlo,Consolas,monospace;color:var(--acc);display:block;margin-bottom:4px}
.tab{overflow-x:auto;margin:12px 0}
table{border-collapse:collapse;width:100%;font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
th,td{border-bottom:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:600}
td.z,th.z{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.hl td{font-weight:700}
.hinweis{border-left:3px solid var(--ink);background:var(--soft);padding:10px 14px;font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;margin:16px 0}
.vorbehalt{border-left-color:var(--warn)}
code{font:14px ui-monospace,Menlo,Consolas,monospace}
footer{border-top:1px solid var(--line);margin-top:48px;padding-top:16px;padding-bottom:40px;font:14px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--muted)}
@media (max-width:560px){body{font-size:16px}h1{font-size:26px}td.z,th.z{white-space:normal}th,td{padding:6px 6px}}
"""

NAV = [("index.html", "Übersicht"), ("faelle-42000.html", "42.000-€-Fälle"), ("fonds.html", "Fonds"), ("mwst.html", "Mehrwertsteuer"),
       ("grenzbelastung.html", "Grenzbelastung"), ("pruefungen.html", "Prüfungen"), ("kit.html", "Forschungs-Kit"), ("index.html#kontakt", "Kontakt")]


def seite(datei, titel, inhalt, beschreibung):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == datei else ""}>{t}</a>' for h, t in NAV) + '<a href="../index.html" lang="en">English</a>'
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titel)} – Das Goldene Drittel (Forschung)</title><meta name="description" content="{html.escape(beschreibung)}">
<link rel="stylesheet" href="../style.css"></head><body>
<header><div class="marke"><a href="index.html">Das Goldene Drittel · Forschung und Prüfung</a></div><nav>{nav}</nav></header>
<main>{inhalt}</main>
<footer>Initiative 28:28 · Modellstand {VERSION} · Stand {DATUM} · Texte und Ergebnisse CC BY 4.0, Skripte MIT ·
Zahlen aus den Ergebnisdateien des Modells (<a href="../data/">data/</a>) · Kontakt <a href="mailto:{KONTAKT}">{KONTAKT}</a> ·
Impressum und Datenschutz: <a href="{SEITE}">{SEITE.replace("https://", "")}</a></footer>
</body></html>"""


def tabelle(kopf, zeilen, rechts=(), hl=()):
    th = "".join(f'<th{" class=z" if i in rechts else ""}>{k}</th>' for i, k in enumerate(kopf))
    tr = "".join(f'<tr{" class=hl" if j in hl else ""}>' + "".join(f'<td{" class=z" if i in rechts else ""}>{v}</td>' for i, v in enumerate(z)) + "</tr>"
                 for j, z in enumerate(zeilen))
    return f'<div class="tab"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def quelle(*dateien):
    return '<p class="meta">Daten: ' + ", ".join(f'<a href="../data/{d}"><code>{d}</code></a>' for d in dateien) + \
           f" · Modellstand {VERSION} · Zitierfähige Werte: <a href=\"kit.html\">Forschungs-Kit</a></p>"


def p_index():
    k = [("faelle-42000.html", "42.000-€-Fälle", pm(fall(2028, TYPEN[0], 0.8, ZU_DE, 0.1)["differenz_monat"]) + " €",
          "im Monat für Alleinstehende 2028 – mit allen Annahmen und Gegenproben"),
         ("fonds.html", "Gemeinsamer Fonds", de(FG["zuschlag_auf_alle_steuern_pct"], 1) + " %",
          f"Zuschlag auf alle Steuern; getilgt {FG['zieljahr']}, Empfindlichkeit für Zins und Wachstum"),
         ("mwst.html", "Mehrwertsteuer-Faktoren", de(MV["klassen"][0]["phi"]["mit_vorsteuer"][0], 2) + " – " + de(MV["klassen"][-1]["phi"]["mit_vorsteuer"][0], 2),
          "Mehrbelastung nach Einkommen relativ zum Mittel (EVS 2023, Frankreich HBS 2020)"),
         ("grenzbelastung.html", "Grenzbelastung", de(GB["zeilen"][5]["heute_pct"], 1) + " → " + de(GB["zeilen"][5]["neu_2028_pct"], 1) + " %",
          "je zusätzlichem Euro bei 60.000 €, bereinigt um Gegenwerte")]
    karten = "".join(f'<a class="karte" href="{h}"><b>{t}</b><span class="wert">{w}</span>{x}</a>' for h, t, w, x in k)
    inhalt = f"""
<h1>Das Goldene Drittel – Rechnung, Prüfungen, Daten</h1>
<p class="lede">Ein Vorschlag für Steuern und soziale Sicherung in Europa: höchstens ein Drittel Steuer auf jeden Euro Einkommen, ein starkes Netz
ohne Prämien, eine monatliche Transformationsdividende. Diese Seiten sind für die wissenschaftliche Diskussion gedacht: Sie zeigen die
tragenden Rechnungen mit ihren Annahmen, die bisherigen Prüfungen und die Zahlen in zitierfähiger Form.</p>
<p class="meta">Die allgemeine Seite in sechs Sprachen: <a href="{SEITE}">{SEITE.replace("https://", "")}</a>. Modellstand {VERSION}, {DATUM}.</p>
<h2>Vier Kernthemen</h2><div class="karten">{karten}</div>
<h2>Wie die Zahlen entstehen</h2>
<p>Alle Werte stammen aus einer offenen Rechenkette ({STUFEN} Stufen) auf Grundlage amtlicher Statistiken (Eurostat, OECD, Statistisches Bundesamt,
Bundesagentur für Arbeit) und veröffentlichter Erhebungen. Jede Änderung und jeder gefundene Fehler steht mit Nummer im Logbuch; bisher sind
{KORREKTUREN} Korrekturen geführt. Die Rechnung ist statisch: Arbeitsangebot, Sparen und Wanderung reagieren nicht; Weitergabe, Überwälzung, Ausweichen und
Inanspruchnahme gehen als Annahmen oder Bänder ein. Eine qualitative Voruntersuchung der Verhaltenswirkungen liegt vor; die quantitative
Stufe ist offen.</p>
<div class="hinweis vorbehalt">Entwurf zur Diskussion, kein beschlossenes Programm. Die drei bisherigen Prüfungen sind <b>interne
Prüfungen</b> (mit einem anderen KI-Modell als die Rechnung) und erfassen den Modellstand bis {GEPRUEFT}; die Änderungen bis v4.63 werden nachgeprüft, D1 und D2 sind bestanden (Liste unter
<a href="pruefungen.html#seit">Prüfungen</a>). Unabhängige Prüfungen sind ausdrücklich erwünscht; die Unterlagen liegen bereit.</div>
<h2>Prüfungen und Forschungs-Kit</h2>
<p><a href="pruefungen.html">Prüfungen</a>: Prüfberichte und Stellungnahmen als PDF, mit allen Befunden und ihrer Umsetzung.
<a href="kit.html">Forschungs-Kit</a>: Kurzdarstellung als PDF, Zahlen zum Zitieren (CSV, JSON), Ergebnisdateien und Zitiervorschlag.
<a href="../downloads/Golden-Third-Working-Paper.pdf">Working Paper</a> (PDF, englisch): Ziele, Modell, Ergebnisse und Bewertung an den Zielen.</p>
<h2 id="kontakt">Kontakt</h2>
<p>Fragen, Einwände und Prüfangebote an <a href="mailto:{KONTAKT}">{KONTAKT}</a>. Skripte, Parameter und Logbuch liegen öffentlich im
Repository <a href="{REPO}">{REPO.replace("https://", "")}</a>. Archiv mit DOI: <a href="https://doi.org/{DOI_KONZEPT}">{DOI_KONZEPT}</a>; <a href="../downloads/Golden-Third-Working-Paper.pdf">Working Paper</a> (PDF, englisch).</p>"""
    return seite("index.html", "Übersicht", inhalt, "Rechnung, Prüfungen und zitierfähige Zahlen zum Vorschlag Das Goldene Drittel.")


def p_faelle():
    g = [fall(2028, t, 0.8, ZU_DE, 0.1) for t in TYPEN]
    z1 = [[t, de(x["netto_heute"]), de(x["netto_33"]), pm(x["differenz"]), "<b>" + pm(x["differenz_monat"]) + "</b>"] for t, x in zip(TYPEN, g)]
    var = []
    for wg in (0.8, 1.0):
        for zu, zt in ((ZU_DE, f"{de(ZU_DE, 1)} % (2028)"), (0.0, "0 (nach Tilgung)")):
            for vs, vt in ((0.1, "Pflichtvorsorge 10 %"), (0.186, "Vorsorge wie heute (18,6 %)")):
                x = fall(2028, TYPEN[0], wg, zu, vs)
                var.append([f"{int(wg * 100)} %", zt, vt, pm(x["differenz_monat"])])
    hl = [i for i, v in enumerate(var) if v[0] == "80 %" and v[1].startswith(de(ZU_DE, 1)) and v[2].startswith("Pflicht")]
    zins = [[v["fall"].replace("fest ", "").replace(".", ","), pm(v["haushalt_de"]["mehr_monat_42000"]["alleinstehend"])] for v in FZ["varianten"][:4]]
    inhalt = f"""
<h1>Die 42.000-€-Fälle</h1>
<p class="lede">Der Beispielhaushalt mit 42.000 € Bruttolohn im Jahr (rund zwei Drittel des Durchschnittslohns nach OECD Taxing Wages) zeigt,
wie Steuer, Dividende, Weitergabe, Pflichtvorsorge und Altlastenzuschlag zusammenwirken. Er ist ein Rechenbeispiel, keine Aussage über alle
Haushalte; die Verteilung zeigt die Mikrosimulation weiter unten.</p>
<h2>Geltende Rechnung, Deutschland 2028</h2>
{tabelle(["Haushalt", "verfügbar heute (€/Jahr)", "verfügbar neu (€/Jahr)", "Unterschied (€/Jahr)", "Unterschied (€/Monat)"], z1, rechts=(1, 2, 3, 4))}
<p class="meta">Kaufkraft 2026. Heute: Lohnsteuer, Solidaritätszuschlag und Sozialbeiträge der Beschäftigten nach Recht 2026, Kindergeld. Neu:
Tarif 0/11/19/25/33 % am Grundbedarf, Dividende ({de(DIV_ERW)} € je Erwachsenem, Kinder 80 %), Weitergabe von 80 % der wegfallenden
Arbeitgeberbeiträge, Mehrwertsteuer-Label nach Einkommen, Altlastenzuschlag Deutschlands nach Verrechnung ({de(ZU_DE, 1)} %), Pflichtvorsorge
10 % des Bruttolohns auf ein eigenes Konto (als Abfluss gerechnet, nicht als Vermögen).</p>
<h2>Wovon das Ergebnis abhängt (alleinstehend, €/Monat)</h2>
{tabelle(["Weitergabe", "Altlastenzuschlag", "Vorsorge", "Unterschied"], var, rechts=(3,), hl=hl)}
<p class="meta">Hervorgehoben: geltende Rechnung. Ohne jede Weitergabe bleibt der Vorteil in Deutschland positiv, in Frankreich und Spanien nicht
(Logbuch v4.12). Die Weitergabe ist deshalb gesetzlich vorgeschrieben, mit Rückfallregel.</p>
<h3>Fondszins</h3>
{tabelle(["Zins des Fonds", "Unterschied alleinstehend (€/Monat)"], zins, rechts=(1,))}
<h2>Gegenproben</h2>
<ul>
<li><b>Mikrosimulation Deutschland</b> (synthetisch, geeicht an amtlichen Eckwerten): erwerbsfähige Haushalte mit mehr
{de(MB['erwerbsfaehige_haushalte']['anteil_mehr_haushalte_pct'], 1)} %, alle Haushalte {de(MB['gesamt']['anteil_mehr_haushalte_pct'], 1)} %,
Hauptperson Minijob {de(MB['status']['Hauptperson Minijob']['anteil_mehr_haushalte_pct'], 1)} %, ohne Erwerb (Bürgergeld)
{de(MB['status']['ohne Erwerb (Bürgergeld)']['anteil_mehr_haushalte_pct'], 1)} %. Validierung 2025: Bruttolohnsumme
{de(MI['basis']['validierung_2025']['bruttolohnsumme']['abweichung_pct'], 1)} %, Lohnsteuer {de(MI['basis']['validierung_2025']['lohnsteuer']['abweichung_pct'], 1)} % gegen amtlich.</li>
<li><b>Rentner</b> (Regel E): {de(RE['anteil_mehr_pct'], 1)} % der Rentnerhaushalte haben mehr, im Mittel {de(RE['mittel_monat'])} € im Monat;
oberes Fünftel {de(RE['fuenftel_monat'][4])} €.</li>
<li><b>Ländermodelle</b> gegen OECD Taxing Wages 2026: {VL['bestanden'].replace('±2.0 Pp', '±2 Prozentpunkte')}; Abweichungen in Frankreich (Paar mit Kindern) und Polen sind erklärt
bzw. offen geführt.</li>
<li><b>Prüfungen</b>: Die Haushaltsformeln wurden in zwei Prüfungen in eigener Programmierung nachgebaut und bestätigt
(<a href="pruefungen.html">Prüfungen</a>).</li>
</ul>
{quelle("haushalte33.json", "fondszins.json", "mikro_de.json", "rentner_kombi.json", "validierung_laender.json")}"""
    return seite("faelle-42000.html", "42.000-€-Fälle", inhalt, "Beispielhaushalt 42.000 €: Rechnung, Empfindlichkeit und Gegenproben.")


def p_fonds():
    vz = FG["verrechnung"]["laender"]
    z1 = [[c, de(vz[c]["reihe"]["2028"]["beitrag_pct_bip"], 2), de(vz[c]["reihe"]["2028"]["zuschlag_pct"], 1)] for c in ("DE", "FR", "IT", "ES", "PL")]
    z2 = [[v["fall"].replace("fest ", "").replace(".", ","), de(v["beitrag_pct_bip"], 2), de(v["zuschlag_pct"], 1), f"{de(v['spitze_zehn'], 1)} ({v['spitzenjahr_zehn']})"]
          for v in FZ["varianten"]]
    z3 = [[de(r["zins"], 2) + " %", de(r["wachstum"], 1) + " %", de(r["beitrag_pct_bip"], 2), de(r["zuschlag_pct"], 1),
           de(r["beschlussbeitrag_fest"]["restschuld_2098_zehn"], 1)] for r in FZ["zins_wachstum"] if r["zins"] in (2.45, 3.5)]
    inhalt = f"""
<h1>Der gemeinsame Fonds für Altlasten</h1>
<p class="lede">Staatsschulden und Rentenzusagen aus dem alten System bleiben Sache der Staaten. Der Bauplan bietet einen gemeinsamen Fonds mit
gemeinsamem Zins an. Er streckt die Last bis zur Tilgung im Jahr {FG['zieljahr']} und finanziert sich über einen Zuschlag auf alle Steuern.</p>
<h2>Geltende Rechnung</h2>
{tabelle(["Größe", "Wert"], [["Beitrag", de(FG['beitrag_pct_bip'], 2) + " % des BIP"], ["Zuschlag auf alle Steuern", de(FG['zuschlag_auf_alle_steuern_pct'], 1) + " %"],
   ["Schuldenquote des Fonds, Spitze", f"{de(FG['schuldenquote_spitze'], 1)} % des BIP ({FG['spitzenjahr']})"], ["Tilgung", str(FG["zieljahr"])],
   ["Zins", de(FG["zins"], 2) + " % (Mittel Euroraum 2006–2025)"], ["Altrentenansprüche über der Dividende (Z), 2028", de(AL['beschluss']['verhandlungsmasse_z_2028_pct_bip'], 2) + " % des BIP"],
   ["Gesamtlast Steuern und Fonds 2028", de(ZR['a_steuern_und_fonds'], 2) + " % des BIP (heute 40,76 %)"]], rechts=())}
<p class="meta">Fonds der 30 Staaten: Beschluss der zehn gerechneten Staaten, skaliert mit dem Verhältnis 30/10 aus dem Möglichkeitsraum (Annahme).
Rentnerregel E: Zusagen über dem Grundbedarf um 15 % gekürzt, eigene Vorsorge ungekürzt.</p>
<h2>Verrechnung je Staat, 2028</h2>
{tabelle(["Staat", "Beitrag (% BIP)", "Zuschlag (%)"], z1, rechts=(1, 2))}
<p class="meta">Jeder Staat trägt den Zuschlag nach seiner Verrechnung im Fonds; bis 2058 Angleichung an den gemeinsamen Satz.</p>
<h2>Empfindlichkeit: Zins</h2>
{tabelle(["Zins", "Beitrag (% BIP)", "Zuschlag (%)", "Spitze (% BIP, Jahr; zehn Staaten)"], z2, rechts=(1, 2, 3))}
<p class="meta">Marktzinsen Oktober 2026: Bundesanleihen rund 3,5 %, EU-Anleihen rund 4,0 % (Sekundärquellen).</p>
<h2>Empfindlichkeit: Zins und nominales Wachstum</h2>
{tabelle(["Zins", "Wachstum", "Beitrag (% BIP)", "Zuschlag (%)", "Restschuld 2098 bei festem Beitrag (% BIP)"], z3, rechts=(2, 3, 4))}
<div class="hinweis vorbehalt">Die Tragfähigkeit hängt am Verhältnis von Zins und Wachstum. Bei 2,45 % Zins und nur 2,0 % nominalem Wachstum bliebe
bei festem Beitrag 2098 eine Restschuld von {de(FZ['zins_wachstum'][0]['beschlussbeitrag_fest']['restschuld_2098_zehn'], 0)} % des BIP. Die Annahme,
dass Z in % des BIP vom Wachstum unabhängig ist, ist eine Vereinfachung.</div>
{quelle("fonds_geltend.json", "fondszins.json")}"""
    return seite("fonds.html", "Fonds", inhalt, "Gemeinsamer Fonds für Staatsschulden und Rentenzusagen: Rechnung und Empfindlichkeit.")


def p_mwst():
    z1 = [[k["klasse"] + " €", de(k["phi"]["mit_vorsteuer"][0], 2), de(k["phi"]["mit_vorsteuer"][1], 2), de(k["phi"]["sichtbar"][0], 2)] for k in MV["klassen"]]
    fr = ML["staaten"]["FR"]
    z2 = [[f"Q{q['fuenftel']}", de(q["aequivalent_jahr"]), de(100 * q["steuerpflichtig"], 1) + " %", de(q["phi"][0], 2), de(q["phi"][1], 2)] for q in fr["fuenftel"]]
    p0 = PN["reihe"][0]
    inhalt = f"""
<h1>Mehrwertsteuer-Faktoren nach Einkommen</h1>
<p class="lede">Die Mehrwertsteuer wird zum Label: A+ 5 %, A 11 %, B 17 %, C 25 %, Sonderstufe 33 % nur für Schädliches. Wie stark ein Haushalt
die Umstellung spürt, hängt davon ab, wie viel er konsumiert und was: Miete, Gesundheit, Bildung und Versicherungen sind steuerfrei.</p>
<h2>Deutschland (EVS 2023)</h2>
{tabelle(["Haushaltsnetto je Monat", "Faktor Mehrbelastung", "Faktor gezahlte Steuer", "nur sichtbare Steuer"], z1, rechts=(1, 2, 3))}
<p class="meta">Faktor 1 = bisherige Rechnung (effektiver Satz auf den ganzen Konsum). Sichtbare Mehrbelastung im Mittel {de(MV['sichtbar_mittel']['mehr_pct_konsum'], 2)} %
des Konsums gegen {de(MV['bisher']['mehr_pct_konsum'], 2)} % bisher; der Rest (Vorsteuer in steuerfreien Bereichen, Wohnungsbau) wird gleichmäßig je Euro
Konsum verteilt (Annahme). Klassenmitten der offenen Klassen und Aufteilung der EVS-Gruppen sind Annahmen.</p>
<h2>Frankreich (Eurostat HBS 2020)</h2>
{tabelle(["Fünftel", "äquivalentes Einkommen (€/Jahr)", "steuerpflichtiger Anteil", "Faktor Mehrbelastung", "Faktor gezahlte Steuer"], z2, rechts=(1, 2, 3, 4))}
<p class="meta">Struktur der Konsumausgaben nach Einkommensfünfteln (von Eurostat als geschätzt gekennzeichnet). Lage der Fünftel auf dem
äquivalenzgewichteten Einkommen (EU-SILC-Dezile) und Sätze je Position sind Annahmen. Italien, Spanien und Polen rechnen noch mit Faktor 1.</p>
<h2>Preisniveau</h2>
<p>Einmaliger Preisniveauschub 2028: mechanisch {de(p0['mechanisch_pct'], 2)} %, bei teilweiser Überwälzung und nur dem steuerpflichtigen Konsum
{de(p0['mwst_spanne_pct'][0], 1)} bis {de(p0['mwst_spanne_pct'][1], 1)} %. Die Literatur findet, dass Erhöhungen der Mehrwertsteuer drei- bis viermal
stärker in Preise weitergegeben werden als Senkungen (Benzarti u. a., JPE 2020); eine asymmetrische Variante ist offen.</p>
{quelle("mwst_verteilung.json", "mwst_laender.json", "preisniveau33.json")}"""
    return seite("mwst.html", "Mehrwertsteuer", inhalt, "Mehrwertsteuer-Label: Faktoren der Mehrbelastung nach Einkommen.")


def p_grenz():
    z = [[de(r["brutto"]) + " €", de(r["heute_pct"], 1), " / ".join(de(r["heute_bereinigt_pct"][a], 1) for a in ("0.5", "1.0")),
          de(r["neu_2028_pct"], 1), de(r["neu_nach_tilgung_pct"], 1), de(r["neu_2028_mit_vorsorge_pct"], 1)] for r in GB["zeilen"]]
    inhalt = f"""
<h1>Grenzbelastung, bereinigt um Gegenwerte</h1>
<p class="lede">Wie viel bleibt von einem zusätzlich verdienten Euro? Ein einfacher Vergleich „Steuer neu gegen Steuer heute“ trifft nicht, weil
heute Kranken-, Pflege- und Rentenversicherung über Beiträge finanziert werden, neu über Steuern. Die Rechnung bereinigt deshalb um Gegenwerte.</p>
{tabelle(["Bruttolohn", "heute", "heute bereinigt (Äquivalenz 0,5 / 1)", "neu 2028", "neu nach Tilgung", "neu 2028 mit Pflichtvorsorge"], z, rechts=(1, 2, 3, 4, 5))}
<p class="meta">Prozent je zusätzlichem Euro Bruttolohn, alleinstehend, ohne Kinder. Heute: Einkommensteuer, Soli und Beiträge der Beschäftigten
(Recht 2026); bereinigt um den Teil des Rentenbeitrags, der einen eigenen Anspruch begründet (Äquivalenz als Band, Annahme). Neu:
Einkommensteuer, Zuschlag Deutschlands ({de(GB['zuschlag_2028'], 1)} %, nach Tilgung 0) und Mehrbelastung aus der Mehrwertsteuer. Die
Pflichtvorsorge (10 %) geht auf ein eigenes, vererbbares Konto und zählt als Ersparnis; zum Vergleich ist sie in der letzten Spalte enthalten.</p>
<div class="hinweis vorbehalt">Nicht enthalten: Arbeitgeberseite, bedarfsgeprüfte Leistungen und die Aufstockung mit Anrechnung zur Hälfte.
Im unteren Bereich ist die Grenzbelastung deshalb noch nicht vollständig gerechnet (offener Punkt V1).</div>
{quelle("grenzbelastung33.json")}"""
    return seite("grenzbelastung.html", "Grenzbelastung", inhalt, "Grenzbelastung heute und neu, bereinigt um Gegenwerte.")


PRUEF = [
 ("Erste Prüfung, 19.10.2026", "Webseite und Repository; geprüft wurde irrtümlich der Vorläufer Stand B, weil die Einstiegsdokumente ihn als geltend nannten (Korrektur 66).",
  [("projekt/Stellungnahme-Pruefung-2026-10-20.md", "Stellungnahme der Initiative (v4.12)"),
   ("projekt/Rueckmeldung-Pruefung-2026-10-20.md", "Rückmeldung an die prüfende Instanz (v4.13)")]),
 ("Zweite Prüfung, 20.10.2026", "Rechenkern von Stand C in eigener Programmierung nachgebaut; zusammengefasster Bericht mit eigener Mikrosimulation.",
  [("projekt/Stellungnahme-Pruefung2-2026-10-20.md", "Stellungnahme zur zweiten Prüfung (v4.14)"),
   ("projekt/Stellungnahme-Pruefung3-2026-10-20.md", "Stellungnahme zum zusammengefassten Bericht (v4.17/v4.18)"),
   ("beitraege/kvribbeck-2028/LIESMICH.md", "Beitrag der Prüfung: Mikrosimulation „9 von 10 Beschäftigte“")]),
 ("Dritte Prüfung, 24.10.2026", "Modellstand v4.42 nach den Prüffragen der Prüfmappe; Rechenkern bestätigt, acht Befunde (B17–B24).",
  [("beitraege/kvribbeck-2028/pruefung3/STELLUNGNAHME-2026-10-24.md", "Prüfbericht"),
   ("projekt/Stellungnahme-Pruefung4-2026-10-24.md", "Stellungnahme der Initiative (v4.46)")]),
 ("Nachprüfung v4.42 → v4.63, seit 2.11.2026 (laufend)", "Prüfung der Änderungen seit der dritten Prüfung nach dem Prüfprogramm (D1–D9). Bisher bestanden: D1 (Raster Zins × Wachstum, 84/84 Werte) und D2 (Grenzbelastung, 77/77 Werte); Befunde B25–B29 beantwortet. Offen: D3–D7, D9.",
  [("beitraege/kvribbeck-2028/pruefung4/PRUEFBERICHT-2026-11-02.md", "Prüfbericht, Zwischenstand 2.11.2026 (enthält auch die erste bis dritte Prüfung)"),
   ("projekt/Stellungnahme-Nachpruefung-2026-11-02.md", "Stellungnahme der Initiative zum Zwischenstand (v4.65)"),
   ("projekt/Pruefprogramm-Delta-v4.42-v4.63.md", "Prüfprogramm")]),
 ("Für weitere Prüfungen", "Was geprüft werden soll, wie man nachrechnet, Setzungen und ihre Empfindlichkeit, Prüffragen.",
  [("projekt/Pruefmappe-Extern-2026-10-24.md", "Prüfmappe"),
   ("projekt/Verhaltenswirkungen-Voruntersuchung-2026-10-24.md", "Verhaltenswirkungen: qualitative Voruntersuchung")]),
]


def pdf_name(pfad):
    return Path(pfad).stem.replace("LIESMICH", "Beitrag-Mikrosimulation-2026-10-20").replace("STELLUNGNAHME-2026-10-24", "Pruefbericht-3-2026-10-24") + ".pdf"


def p_pruef():
    teile = []
    for titel, text, dok in PRUEF:
        li = "".join(f'<li><a href="../downloads/{pdf_name(p)}">{t}</a> (PDF)</li>' for p, t in dok)
        teile.append(f"<h2>{titel}</h2><p>{text}</p><ul>{li}</ul>")
    inhalt = f"""
<h1>Prüfungen</h1>
<p class="lede">Im Oktober 2026 wurden Webseite und Rechnung in drei Prüfungen nachgerechnet. Alle Befunde sind mit ihrer Bewertung und Umsetzung
dokumentiert; gefundene Fehler stehen als nummerierte Korrekturen im Logbuch.</p>
<div class="hinweis vorbehalt">Die Prüfungen sind <b>interne Prüfungen</b>: von der Initiative veranlasst und mit einem anderen KI-Modell durchgeführt als dem, mit dem die Rechnung entwickelt wurde. Sie ersetzen keine unabhängige Begutachtung. Die Prüfberichte tragen teils andere Bezeichnungen (etwa „unabhängig“); maßgeblich ist diese Einordnung. Die
Stellungnahmen geben den Stand ihrer Version wieder; spätere Rechnungen können Zahlen darin geändert haben. Geltende Werte: <a href="kit.html">Forschungs-Kit</a>.
Die erste und zweite Prüfung sind im Prüfbericht der Nachprüfung mit enthalten (Abschnitte 1 bis 7).</div>
{''.join(teile)}
<h2 id="seit">Seit der letzten Prüfung ({GEPRUEFT}) geändert, noch nicht geprüft</h2>
<p>Die dritte Prüfung erfasste den Modellstand {GEPRUEFT}. Seitdem haben sich folgende Rechnungen und Angaben geändert (Logbuch Band III);
die Nachprüfung dieser Änderungen läuft (D1 und D2 bestanden, D3–D7 und D9 offen).</p>
{seit_pruefung_html()}"""
    return seite("pruefungen.html", "Prüfungen", inhalt, "Prüfberichte und Stellungnahmen zum Modell Das Goldene Drittel.")


def p_kit():
    z = [[x[0], x[1], f"<b>{wert(x[2])}</b>", x[3], x[4], x[6]] for x in ZAHLEN]
    inhalt = f"""
<h1>Forschungs-Kit</h1>
<p class="lede">Für Forschung, Presse und Prüfung: eine Kurzdarstellung, die tragenden Zahlen mit Herkunft und Status, die Ergebnisdateien
und ein Zitiervorschlag.</p>
<h2>Downloads</h2>
<ul>
<li><a href="../downloads/Golden-Third-Working-Paper.pdf">Working Paper</a> (PDF, englisch): Ziele, Regeln, Modell, Ergebnisse, Empfindlichkeit, Bewertung an den Zielen</li>
<li><a href="../downloads/Forschungs-Kit-Goldenes-Drittel.pdf">Kurzdarstellung mit Zahlen zum Zitieren</a> (PDF)</li>
<li><a href="../data/zahlen-zum-zitieren.csv">Zahlen zum Zitieren</a> (CSV) · <a href="../data/zahlen-zum-zitieren.json">JSON</a></li>
<li><a href="../data/">Ergebnisdateien</a> der hier gezeigten Rechnungen (JSON)</li>
</ul>
<h2>Zahlen zum Zitieren</h2>
{tabelle(["Nr.", "Größe", "Wert", "Einheit", "Bezug", "Status"], z, rechts=(2,))}
<p class="meta">„geltend“: Rechnung nach den Beschlüssen der Initiative; „Prüfrechnung“: Gegenprobe oder Empfindlichkeit. Bitte Nummer und
Modellstand angeben. Abgrenzungen: <code>KENNZAHLEN.md</code> im Repository.</p>
<h2>Zitiervorschlag</h2>
<p>{html.escape(ZITAT)} {SEITE.replace("https://", "")}</p>
<p class="meta">Der DOI {DOI_KONZEPT} verweist immer auf die neueste archivierte Fassung. Archivierte Fassungen: {", ".join(f"Modellstand {v}: <a href=\"https://doi.org/{d}\">{d}</a>" for v, d in DOI_ARCHIV.items())}.
Working Paper (englisch): <a href="../downloads/Golden-Third-Working-Paper.pdf">The Golden Third – a static costing and distributional model</a> (PDF, Modellstand {VERSION}).</p>"""
    return seite("kit.html", "Forschungs-Kit", inhalt, "Zahlen zum Zitieren, Ergebnisdateien und Zitiervorschlag.")


def kit_html():
    zeilen = "".join(f"<tr><td>{x[0]}</td><td>{html.escape(x[1])}</td><td class=z><b>{wert(x[2])}</b></td>"
                     f"<td>{x[3]}</td><td>{html.escape(x[4])}</td><td>{x[6]}</td></tr>" for x in ZAHLEN)
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
body{{font:10.5pt/1.45 Georgia,serif;color:#1d2a33;margin:0}}h1{{font:700 20pt/1.2 Arial,sans-serif;color:#0f3b5c;margin:0 0 4pt}}
h2{{font:700 12.5pt/1.3 Arial,sans-serif;color:#0f3b5c;margin:14pt 0 4pt}}.meta{{font:8.5pt/1.4 Arial,sans-serif;color:#5a7186}}
table{{border-collapse:collapse;width:100%;font:8.5pt/1.35 Arial,sans-serif}}td,th{{border-bottom:.5pt solid #d8e1e8;padding:3pt 4pt;text-align:left;vertical-align:top}}
th{{color:#5a7186}}td.z{{text-align:right;white-space:nowrap}}ul{{margin:4pt 0}}
</style></head><body>
<h1>Das Goldene Drittel – Forschungs-Kit</h1>
<p class="meta">Initiative 28:28 · Modellstand {VERSION} · {DATUM} · CC BY 4.0 · Kontakt {KONTAKT}</p>
<h2>Worum es geht</h2>
<p>Ein Vorschlag für Steuern und soziale Sicherung in Europa: kein Euro wird mit mehr als einem Drittel besteuert (Tarif 0/11/19/25/33 % am
Grundbedarf); Sozialbeiträge entfallen, Betriebe geben mindestens 80 % der wegfallenden Arbeitgeberbeiträge in den Lohn; ein starkes Netz
(Gesundheit, Pflege, Mindestrente, Grundbedarf) ohne Prämien; eine monatliche Transformationsdividende für jeden Erwachsenen; Pflichtvorsorge
10 % auf ein eigenes, bis zur Altersgrenze gesperrtes Konto; Mehrwertsteuer als Label; Altlasten in einem gemeinsamen Fonds.</p>
<h2>Methode und Grenzen</h2>
<ul><li>Offene Rechenkette ({STUFEN} Stufen), amtliche Statistiken (Eurostat, OECD, Destatis, BA) und veröffentlichte Erhebungen; jede Korrektur
nummeriert im Logbuch (bisher {KORREKTUREN}).</li>
<li>Statisch: keine Verhaltensreaktionen beim Arbeitsangebot, Sparen und Wandern; Weitergabe, Überwälzung, Ausweichen und Inanspruchnahme als
Annahmen oder Bänder. Qualitative Voruntersuchung der Verhaltenswirkungen liegt vor.</li>
<li>Drei interne Prüfungen, mit einem anderen KI-Modell als die Rechnung (Oktober 2026), zuletzt Modellstand {GEPRUEFT}: Rechenkern bestätigt, Befunde dokumentiert. Spätere Änderungen (bis {VERSION}) sind noch nicht geprüft. Unabhängige Prüfung erwünscht.</li>
<li>Größte unbelegte Position: Basis der Unternehmensbesteuerung am Ort der Kunden.</li></ul>
<h2>Zahlen zum Zitieren</h2>
<table><thead><tr><th>Nr.</th><th>Größe</th><th>Wert</th><th>Einheit</th><th>Bezug</th><th>Status</th></tr></thead><tbody>{zeilen}</tbody></table>
<p class="meta">Herkunft je Zahl (Datei und Pfad): zahlen-zum-zitieren.csv. „geltend“: nach den Beschlüssen der Initiative; „Prüfrechnung“:
Gegenprobe oder Empfindlichkeit.</p>
<h2>Zitiervorschlag</h2><p>{html.escape(ZITAT)}</p>
</body></html>"""


def md_html(pfad):
    import markdown
    text = (W / pfad).read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
body{{font:10pt/1.45 Georgia,serif;color:#1d2a33}}h1{{font:700 17pt/1.25 Arial,sans-serif;color:#0f3b5c}}h2,h3{{font:700 12pt/1.3 Arial,sans-serif;color:#0f3b5c}}
table{{border-collapse:collapse;width:100%;font:8pt/1.35 Arial,sans-serif;margin:6pt 0}}td,th{{border:.5pt solid #d8e1e8;padding:3pt;vertical-align:top}}
code{{font:8.5pt Menlo,monospace}}.fuss{{font:8pt Arial,sans-serif;color:#5a7186;border-top:.5pt solid #d8e1e8;margin-top:14pt;padding-top:4pt}}
</style></head><body>{body}<p class="fuss">Quelle im Repository der Initiative 28:28: {pfad} · als PDF veröffentlicht mit Modellstand {VERSION}, {DATUM} ·
Der Inhalt gibt den Stand seiner Version wieder.</p></body></html>"""


def pdfs(ziel):
    from playwright.sync_api import sync_playwright
    (ziel / "downloads").mkdir(parents=True, exist_ok=True)
    auftraege = [(kit_html(), "Forschungs-Kit-Goldenes-Drittel.pdf")] + [(md_html(p), pdf_name(p)) for _, _, d in PRUEF for p, _ in d]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        s = b.new_page()
        for h, name in auftraege:
            s.set_content(h, wait_until="load")
            s.pdf(path=str(ziel / "downloads" / name), format="A4", margin=dict(top="18mm", bottom="18mm", left="18mm", right="18mm"))
        b.close()


def main():
    OUT.mkdir(exist_ok=True)
    DE = OUT / "de"
    DE.mkdir(exist_ok=True)
    for alt in ("index.html", "faelle-42000.html", "fonds.html", "mwst.html", "grenzbelastung.html", "pruefungen.html", "kit.html"):   # bis v4.56 im Wurzelverzeichnis
        if (OUT / alt).exists() and alt != "index.html":
            (OUT / alt).unlink()
    if (OUT / "daten").exists():
        shutil.rmtree(OUT / "daten")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    for name, f in (("index.html", p_index), ("faelle-42000.html", p_faelle), ("fonds.html", p_fonds), ("mwst.html", p_mwst),
                    ("grenzbelastung.html", p_grenz), ("pruefungen.html", p_pruef), ("kit.html", p_kit)):
        (DE / name).write_text(f(), encoding="utf-8")
    zahlen_dateien(OUT)
    import importlib.util
    spec = importlib.util.spec_from_file_location("forschung_en", Path(__file__).resolve().parent / "forschung_en.py")
    EN = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(EN)
    EN.schreiben(OUT)
    liste = "".join(f'<li><a href="{p.name}">{p.name}</a></li>' for p in sorted((OUT / "data").glob("*")) if p.name != "index.html")
    (OUT / "data" / "index.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                                             f'<title>Result files</title><link rel="stylesheet" href="../style.css"></head><body><main><h1>Result files · Ergebnisdateien</h1>'
                                             f'<p class="meta">Model version {VERSION} · CC BY 4.0. Keys of the result files are German; field descriptions in figures-to-cite.csv.</p>'
                                             f'<ul>{liste}</ul><p><a href="../index.html">English</a> · <a href="../de/index.html">Deutsch</a></p></main></body></html>',
                                             encoding="utf-8")
    # Stand der PDFs: Prüfsumme über die Quellen (Kit-HTML ohne Datum, Markdown der Protokolle); ohne --pdf nur prüfen
    wp = W / "dokumente" / "working-paper"
    if (wp / "Golden-Third-Working-Paper.pdf").exists():   # v4.63: Working Paper auf der Seite; Stand über seine Text-Prüfsumme
        shutil.copy(wp / "Golden-Third-Working-Paper.pdf", OUT / "downloads" / "Golden-Third-Working-Paper.pdf")
    quellen = (wp / "quellen.sha256").read_text(encoding="utf-8") if (wp / "quellen.sha256").exists() else ""
    quellen += kit_html().replace(DATUM, "") + EN.kit_html().replace(EN.DATUM, "") + "".join((W / p).read_text(encoding="utf-8") for _, _, d in PRUEF for p, _ in d)
    summe = hashlib.sha256(quellen.encode("utf-8")).hexdigest()
    marke = OUT / "downloads" / "quellen.sha256"
    if "--pdf" in sys.argv:
        pdfs(OUT)
        EN.pdf(OUT)
        marke.write_text(summe + "\n", encoding="utf-8")
    elif not marke.exists() or marke.read_text(encoding="utf-8").strip() != summe:
        print("PDFs veraltet: Zahlen oder Protokolle haben sich geändert – neu bauen mit: python3 seite/werkzeuge/forschung_bau.py --pdf")
        return 1
    print(f"docs/: englisch 7 Seiten, deutsch 7 Seiten (de/), {len(ZAHLEN)} + {len(EN.FIGURES)} Zahlen zum Zitieren, Modellstand {VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
