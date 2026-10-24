#!/usr/bin/env python3
"""Grenzbelastung je zusätzlichem Euro Bruttolohn: heute (Recht 2026) gegen Goldenes Drittel (33R), bereinigt um Gegenwerte (Logbuch v4.47).

Frage: Ist die Grenzbelastung des neuen Systems höher als heute? Ein Vergleich „Steuer neu“ gegen „Steuer heute“ trifft nicht, weil heute
Kranken-, Pflege- und Rentenversicherung über Beiträge finanziert werden, neu über Steuern. Bereinigt wird so:
  heute = Einkommensteuer + Soli + Beiträge der Beschäftigten, abzüglich des Teils des Rentenbeitrags, der einen eigenen Anspruch begründet
          (Äquivalenz, Band 0 / 0,5 / 1; Annahme). Kranken- und Pflegebeiträge zählen voll, weil die Leistung nicht von der Beitragshöhe abhängt.
  neu   = Einkommensteuer 33R + Altlastenzuschlag + Mehrbelastung aus der Mehrwertsteuer; die Pflichtvorsorge (10 %, eigenes Konto) zählt nicht
          als Abgabe, sondern als Ersparnis (zum Vergleich auch mit ihr).
Bezug: je Euro des eigenen Bruttolohns (heute: Bruttolohn; neu: Bruttolohn einschließlich Weitergabe). Alleinstehend, ohne Kinder, 2028, Kaufkraft 2026.
Die Arbeitgeberseite (heutige Arbeitgeberbeiträge; neu Weitergabe 80 % bis zum Deckel) ist nicht Teil dieses Satzes.
Ausgabe: daten/aggregate/grenzbelastung33.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "grenzbelastung33.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("h33", W / "modell" / "haushalte33.py")
H = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(H)
K = H.K
ZU = H.P["zuschlag_pct"][1]


def heute(b, d):
    n = lambda x: K.netto_heute(x, 0, False)["netto"]
    m = 1 - (n(b + d) - n(b)) / d
    rv = P["rv_an"] if b < K.BBG_RV else 0.0
    return m, rv


def neu(b, d, zu, vs):
    g = lambda x: x + P["weitergabe"] * H.ag(x)
    y = lambda x: H.neu(x, 0, False, P["weitergabe"], zu, vs, 2028) + vs * x     # Pflichtvorsorge als eigenes Vermögen zurückgerechnet
    yv = lambda x: H.neu(x, 0, False, P["weitergabe"], zu, vs, 2028)
    dg = g(b + d) - g(b)
    return 1 - (y(b + d) - y(b)) / dg, 1 - (yv(b + d) - yv(b)) / dg


def main():
    d = P["schritt"]
    zeilen = []
    for b in P["einkommen"]:
        m, rv = heute(b, d)
        z = dict(brutto=b, heute_pct=round(100 * m, 1), heute_bereinigt_pct={str(a): round(100 * (m - a * rv), 1) for a in P["rv_aequivalenz"]})
        for name, zu in (("2028", ZU), ("nach_tilgung", 0.0)):
            o, mitv = neu(b, d, zu, 0.10)
            z[f"neu_{name}_pct"] = round(100 * o, 1)
            z[f"neu_{name}_mit_vorsorge_pct"] = round(100 * mitv, 1)
        zeilen.append(z)
    E = dict(version=P["version"], status="Prüfrechnung", zuschlag_2028=ZU, rv_aequivalenz_band=P["rv_aequivalenz"], zeilen=zeilen,
             hinweis="Grenzbelastung in % je zusätzlichem Euro Bruttolohn, alleinstehend, ohne Kinder. heute: Recht 2026 (Kernmodell), ohne "
                     "Mehrwertsteuer; neu: mit der Mehrbelastung aus der Mehrwertsteuer (Labels gegen heute). Bereinigt heute: Rentenbeitrag zum Anteil "
                     "der Äquivalenz abgezogen (Annahme). neu ohne Pflichtvorsorge = Abgabenbelastung; mit Pflichtvorsorge = Abfluss vom verfügbaren Einkommen.")
    (W / "daten" / "aggregate" / "grenzbelastung33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for z in zeilen:
        print(z)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
