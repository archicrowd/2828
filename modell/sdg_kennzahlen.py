#!/usr/bin/env python3
"""Kennzahlen der UN-Nachhaltigkeitsziele aus der Verteilungsrechnung (Logbuch v4.67). Prüfrechnung, statisch.

SDG 1.2  Armutsgefährdungsquote: Anteil der Personen unter 60 % des Medians des äquivalenzgewichteten verfügbaren Einkommens (EU-Indikator
         für SDG 1, Eurostat ilc_li02). Relativ (Grenze am jeweiligen Median, heute und neu) und verankert (neue Einkommen gegen die heutige
         Grenze, damit eine allgemeine Anhebung nicht verschwindet).
SDG 10.1 Einkommenswachstum der unteren 40 % gegen das Mittel aller (statisch: Änderung heute → neu je Person, Personen nach dem heutigen
         Einkommen geordnet).

Verfahren wie gini.py (Rekonstruktion aus EU-SILC-Dezilen, Abbildung heute → neu, Band „untere/obere“ aus den Transfers der unteren Dezile,
Variante mit unveränderten Rentnerhaushalten). Ausgewiesen: amtliche Quote 2025 × (Quote neu / Quote der Rekonstruktion heute); additiv wie beim Gini ergäbe bei verankerter Grenze
in Polen einen negativen Wert.
Grenzen: statisch, ohne Kapitaleinkommen und Verhaltensänderung; Punkte gleich gewichtet (Personen); Paare und Kinder über die Äquivalenzskala.
Ausgabe: daten/aggregate/sdg_kennzahlen.json
"""
import contextlib, importlib.util, io, json, statistics, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "sdg_kennzahlen.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("gini_mod", W / "modell" / "gini.py")
G = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(G)
BK, RB, SL = G.BK, G.RB, G.SL


def quote(ys, grenze):
    return 100 * sum(1 for y in ys if y < grenze) / len(ys)


def land(c, j):
    ys, _ = G.verteilung(c)
    bs, hs = G.umkehr(c)
    lohn = [G.lohn_zu(y, bs, hs) for y in ys]
    g_ae = SL.HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * SL.HL.faktor(c) * BK.boden_faktor(RB.P["skala"]["kind"])
    grenze_heute = 0.6 * statistics.median(ys)
    arop_heute = quote(ys, grenze_heute)
    amt = P["armutsquote_amtlich_2025"][c]
    nr = max(1, round(1 / G.P["anteil_rentner"]))
    ordnung = sorted(range(len(ys)), key=lambda i: ys[i])
    unten = ordnung[: int(0.4 * len(ys))]
    erg, cache = {}, {}
    for name, eu in (("untere", BK.P["eigenanteil_unten"][1]), ("obere", BK.P["eigenanteil_unten"][0])):
        yn = [G.neu_punkt(c, y, b, j, eu, g_ae, cache) for y, b in zip(ys, lohn)]
        ym = [y if i % nr == 0 else v for i, (y, v) in enumerate(zip(ys, yn))]
        z = {}
        for var, werte in (("alle", yn), ("rentner_unveraendert", ym)):
            rel = quote(werte, 0.6 * statistics.median(werte))
            ank = quote(werte, grenze_heute)
            w40 = 100 * (sum(werte[i] for i in unten) / sum(ys[i] for i in unten) - 1)
            wall = 100 * (sum(werte) / sum(ys) - 1)
            # Skalierung mit dem Verhältnis zur Rekonstruktion (nicht additiv wie beim Gini): bleibt bei kleinen Quoten ≥ 0
            z[var] = dict(armutsquote_relativ=round(amt * rel / arop_heute, 1), armutsquote_verankert=round(amt * ank / arop_heute, 1),
                          einkommen_untere_40_pct=round(w40, 1), einkommen_alle_pct=round(wall, 1),
                          median_neu_zu_heute=round(statistics.median(werte) / statistics.median(ys), 3))
        erg[name] = z
    return dict(armutsquote_amtlich_2025=amt, armutsquote_rekonstruktion_heute=round(arop_heute, 1),
                grenze_heute_jahr=round(grenze_heute), jahr=j, **erg)


def main():
    j = P["jahr"]
    E = dict(version=P["version"], status="Prüfrechnung, statisch", jahr=j, quelle_armutsquote=P["quelle_armutsquote"],
             staaten={c: land(c, j) for c in ("DE", "FR", "IT", "ES", "PL")},
             hinweis="SDG 1.2: Armutsgefährdungsquote (60 % des Medians), amtlicher Wert 2025 × Verhältnis neu/heute der Rekonstruktion; relativ = Grenze am neuen Median, "
                     "verankert = heutige Grenze. SDG 10.1: Änderung des verfügbaren Einkommens der unteren 40 % (nach heutigem Einkommen) gegen alle, "
                     "Kaufkraft 2026, ohne Preisniveauschub. Band untere/obere wie gini.json. Hauptvariante: Rentnerhaushalte (25 %) unverändert – Variante „alle“ bildet Rentner wie Erwerbstätige ab und ist eine obere Grenze. Statisch, ohne Kapitaleinkommen und Verhaltensänderung.")
    (AGG / "sdg_kennzahlen.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in E["staaten"].items():
        print(c, "amtlich", x["armutsquote_amtlich_2025"], "Rekonstruktion", x["armutsquote_rekonstruktion_heute"])
        for b in ("untere", "obere"):
            for v, z in x[b].items():
                print(f"   {b:6} {v:22} relativ {z['armutsquote_relativ']:5} verankert {z['armutsquote_verankert']:5} "
                      f"untere 40 % {z['einkommen_untere_40_pct']:+6} alle {z['einkommen_alle_pct']:+6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
