#!/usr/bin/env python3
"""Textentwurf der deutschen Seite zum Vorschlag Rentner E (Logbuch v4.25). Entwurf, nicht veröffentlichen.

Grundlage ist die gebaute Seite seite/stand-c/de.html (geltender Stand). Geändert werden nur die Stellen zu Renten; jede Änderung ist gelb
markiert. Zahlen des Vorschlags kommen aus daten/aggregate/rentner_kombi.json (Variante E); alle übrigen Zahlen der Seite bleiben beim Beschluss.
Ausgabe: seite/entwurf/rentner-e/de.html und seite/entwurf/rentner-e/AENDERUNGEN.md
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
QUELLE = W / "seite" / "stand-c" / "de.html"
ZIEL = W / "seite" / "entwurf" / "rentner-e"
RK = json.loads((W / "daten" / "aggregate" / "rentner_kombi.json").read_text(encoding="utf-8"))
T = tomllib.loads((W / "modell" / "rentner_kombi.toml").read_text(encoding="utf-8"))
E = next(v for v in RK["varianten"] if v["name"].startswith("E "))
VE = next(v for v in T["variante"] if v["name"].startswith("E "))
GB_MONAT = 1029


def eur(x, vz=False):
    s = f"{abs(x):,.0f}".replace(",", ".")
    return (("+" if x > 0 else "−" if x < 0 else "±") if vz else "") + s + " €"


SATZ = round(VE["satz"] * 100)
B1, B2 = VE["boden"]
F = E["fuenftel_monat"]
KUERZ = {r: round((r - GB_MONAT) * VE["satz"]) for r in (1500, 2500)}
M = '<span class="entwurf-neu">{}</span>'

AENDERUNGEN = [
    ("Hero, Fußnote zu „9 von 10“",
     'margin:16px auto 0">* Rechnung nach den Regeln des Projekts für Beschäftigte, 2028, heutige Kaufkraft, nach Pflichtvorsorge (10 %) und '
     "Altlastenzuschlag; zum Beispiel +608 € im Monat bei 42.000 € Jahreseinkommen.</p>",
     'margin:16px auto 0">* Rechnung nach den Regeln des Projekts für Beschäftigte, 2028, heutige Kaufkraft, nach Pflichtvorsorge (10 %) und '
     "Altlastenzuschlag; zum Beispiel +608 € im Monat bei 42.000 € Jahreseinkommen." + M.format(
         f" Rentnerhaushalte tragen einen Teil der alten Zusagen: im unteren Fünftel {eur(F[0], True)}, in der Mitte {eur(F[2], True)}, "
         f"im oberen Fünftel {eur(F[4], True)} im Monat.") + "</p>"),
    ("Chancen, neue Kachel „Im Alter“",
     "auch das, was sie in der Verwaltung sparen.</p></div>\n    </div>",
     "auch das, was sie in der Verwaltung sparen.</p></div>\n" + M.format(
         '<div class="mass"><div class="pos">Im Alter</div><h3>Der Grundbedarf ist sicher</h3><p>Niemand im Ruhestand erhält weniger als '
         f'die heutige Grundsicherung: mindestens {eur(B1)} allein, {eur(B2)} zu zweit, aufgestockt an einer Stelle der Gemeinde. Was jemand '
         'selbst angespart hat – Betriebs- oder Privatrente –, bleibt ungekürzt. Kranken- und Pflegebeiträge entfallen.</p></div>') + "\n    </div>"),
    ("Chancen, Vergleichstabelle: zwei Zeilen",
     '<span class="neu">Dividende ohne Antrag; Aufstockung an einer Stelle der Gemeinde</span></div></div>',
     '<span class="neu">Dividende ohne Antrag; Aufstockung an einer Stelle der Gemeinde</span></div>' + M.format(
         f'<div class="br"><span>Mindesteinkommen im Alter (allein)</span><span>{eur(B1)}, Grundsicherung auf Antrag</span>'
         f'<span class="neu">{eur(B1)}, Aufstockung an einer Stelle der Gemeinde</span></div>'
         f'<div class="br"><span>Rentnerhaushalte: Veränderung im Monat (unteres / mittleres / oberes Fünftel)</span><span>–</span>'
         f'<span>{eur(F[0], True)} / {eur(F[2], True)} / {eur(F[4], True)}</span></div>') + "</div>"),
    ("Chancen, Fußnote zur Tabelle",
     "Gini: amtlicher Wert 2025 (Eurostat) plus Modelländerung.</p>",
     "Gini: amtlicher Wert 2025 (Eurostat) plus Modelländerung." + M.format(
         " Rentnerhaushalte: Haushaltseinkommen nach EU-SILC 2025, Zusammensetzung der Alterseinkommen nach dem Alterssicherungsbericht 2024; "
         "Grundsicherung als Regelbedarf und durchschnittliche Wohnkosten (Annahme). Fünftel nach heutigem Haushaltsnetto.") + "</p>"),
    ("Sicherheit, Kachel „Altlasten“: Regel für Bestandsrenten",
     "Bestehende Renten laufen weiter, gekürzt um 7,5 % – weniger als die Kranken- und Pflegebeiträge, die Rentner heute zahlen und die entfallen "
     "(in Deutschland 12,35 %). Kleine Renten werden bis zum Grundauskommen aufgestockt.",
     M.format(f"Bestehende Renten laufen weiter – nach einer einfachen Regel. Der Grundbedarf ist garantiert: Kein Rentnerhaushalt erhält weniger "
              f"als die heutige Grundsicherung. Gesetzliche Renten und Pensionen beruhen auf Zusagen, die nicht angespart sind, sondern aus den "
              f"laufenden Einnahmen bezahlt werden. Auf den Teil über dem Grundbedarf ({eur(GB_MONAT)} je Person) werden sie um {SATZ} % gekürzt: "
              f"bei 1.500 € um {eur(KUERZ[1500])}, bei 2.500 € um {eur(KUERZ[2500])} im Monat. Eigene Vorsorge bleibt ungekürzt. "
              f"Kranken- und Pflegebeiträge entfallen.")),
]

BANNER = ('<div style="background:#FFF3B0;border-bottom:2px solid #C9A400;padding:10px 16px;font-family:IBM Plex Mono,monospace;font-size:13px;'
          'color:#0F3B5C">Entwurf, nicht veröffentlichen · Vorschlag Rentner E (Logbuch v4.25) · geänderte Stellen gelb markiert · '
          'alle übrigen Zahlen nach geltendem Beschluss</div>')


def main():
    s = QUELLE.read_text(encoding="utf-8")
    nb = lambda x: x.replace(" €", "\u00a0€").replace(" %", "\u00a0%")       # Seite setzt geschützte Leerzeichen vor € und %
    for name, alt, neu in AENDERUNGEN:
        a = next((x for x in (alt, alt.replace(" €", "\u00a0€"), nb(alt)) if s.count(x) == 1), alt)
        assert s.count(a) == 1, f"Stelle nicht eindeutig: {name}"
        s = s.replace(a, neu.replace(" €", "\u00a0€"))
    s = s.replace("</style>", ".entwurf-neu{background:#FFF3B0}.entwurf-neu .mass,.entwurf-neu .br{background:#FFF3B0}</style>", 1)
    s = s.replace("<body>", "<body>\n" + BANNER, 1)
    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / "de.html").write_text(s, encoding="utf-8")
    md = ["# Entwurf Webseite DE: Vorschlag Rentner E", "",
          "Stand: 22. Oktober 2026 (Logbuch v4.25). Grundlage: `seite/stand-c/de.html`. Zahlen: `daten/aggregate/rentner_kombi.json` (Variante E).",
          "Alle übrigen Zahlen der Seite bleiben beim Beschluss (7,5 % auf die ganze Rente); nach einem Beschluss für E sind Fonds, Zuschlag und",
          "Beispiele neu zu rechnen (Wirkung gegen den Beschluss rund −0,05 % BIP).", ""]
    import re, html
    klar = lambda x: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).replace(' margin:16px auto 0">', "").strip()
    for name, alt, neu in AENDERUNGEN:
        md += [f"## {name}", "", "**bisher:** " + klar(alt.split('auto 0">')[-1]), "", "**neu:** " + klar(neu.split('auto 0">')[-1]), ""]
    (ZIEL / "AENDERUNGEN.md").write_text("\n".join(md), encoding="utf-8")
    print("geschrieben:", ZIEL / "de.html", "| Änderungen:", len(AENDERUNGEN))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
