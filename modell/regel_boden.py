#!/usr/bin/env python3
"""Eine Regel für Boden, Erwerb und Vorsorge: „Der Grundbedarf ist der Boden, das eigene Einkommen zählt zur Hälfte“ (Logbuch v4.5). Prüfrechnung.

Auftrag der Initiative (18.10.2026): R2/R3 durch eine klare Regel nahe an der Konzeptphilosophie ersetzen – das Netz trägt, wird aber keine
Hängematte; enges Existenzminimum als Bezugspunkt, das schon ein Engagement zur eigenen Vorsorge verlangt. R1 (Kinderanteil 0,8) beschlossen.

Regel (eine Zahl, ein Maßstab, wie bei der Mindestrente, netz33.toml anrechnung_eigene_rente = 0,5):
  Boden F    = Grundbedarf G des Landes × OECD-modifizierte Skala (1 / 0,5 je weitere/n Erwachsene/n / 0,3 je Kind) – enges Existenzminimum
  Anrechnung = Dividende voll, eigenes Einkommen (nach Steuern) zur Hälfte; Aufstockung = max(0, F − Dividenden − ½ · eigenes Einkommen)
  Vorsorge   = 10 % des Lohns ab dem ersten Euro, nicht aufgestockt (eigener Beitrag auch am Boden)
  Alter      = Mindestrente mit derselben Halbanrechnung (unverändert)
Geprüft: Anteil der Beschäftigten mit mehr Geld, Beispielhaushalte, Abstand zwischen Arbeit und Boden (Effektivbelastung eines zusätzlichen Euros),
Kosten der Aufstockung für Beschäftigte gegen den Härtefallfonds (DE, grob), Vergleich mit v4.4 (R2/R3).
Ausgabe: daten/aggregate/regel_boden.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "regel_boden.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("sl", W / "modell" / "sozial_laender.py")
SL = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(SL)
S = P["kinderanteil"]


def topf(s):
    return (1 - SL.K / 2) / (1 - SL.K + s * SL.K)


def boden(c, e, k):
    g = SL.HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * SL.HL.faktor(c)
    sk = P["skala"]
    return g * (1 + sk["erwachsen"] * (e - 1) + sk["kind"] * k)


def dividenden(c, e, k, j=2028):
    d = SL.HL.LS["staaten"][c]["dividende_erw_eur"][SL.JAHRE.index(j)] * 12 * SL.HL.faktor(c) * topf(S)
    return d * (e + S * k)


def neu(c, b, e, k, j=2028, lohn_faktor=1.0, detail=False):
    """Verfügbares Einkommen nach der Regel: SL.neu ohne Boden, Vorsorge ab dem ersten Euro; Aufstockung mit Halbanrechnung vor der Vorsorge."""
    vs = SL.HL.P["vorsorge"] * b * lohn_faktor
    x = SL.neu(c, b, e, k, j, s=S, boden=False, lohn_faktor=lohn_faktor) + vs       # verfügbar vor Vorsorge (Steuern, MwSt., Zuschlag abgezogen)
    dv = dividenden(c, e, k, j)
    eigen = max(0.0, x - dv)
    auf = max(0.0, boden(c, e, k) - dv - P["anrechnung"] * eigen)
    r = x + auf - vs
    return (r, auf) if detail else r


def anteile(c):
    v = SL.verteilung(c)
    tot = sum(w for w, _ in v)
    return {n: round(sum(w for w, b in v if neu(c, b, e, k) > SL.heute(c, b, e, k)) / tot * 100) for n, e, k in SL.HAUSHALTE}


def faelle(c):
    aw = SL.HL.P["oecd"]["durchschnittslohn"][c]
    return {f"{f}": {n: round((neu(c, round(f * aw, -2), e, k) - SL.heute(c, round(f * aw, -2), e, k)) / 12) for n, e, k in SL.HAUSHALTE}
            for f in (0.15, 0.33, 0.5, 0.66, 1.0)}


def lohnabstand(c):
    """Verfügbares Einkommen je Monat bei 0 / ¼ / ½ / 1 × Vollzeit-Mindestlohn (bzw. ⅓ Durchschnitt in IT) und Belastung eines zusätzlichen Euros."""
    ml = SL.P["mindestlohn"]["monat_2026"].get(c)
    voll = ml * 12 if ml else SL.HL.P["oecd"]["durchschnittslohn"][c] / 3
    out = {}
    for n, e, k in SL.HAUSHALTE:
        z = {}
        for f in (0.0, 0.25, 0.5, 1.0):
            b = voll * f
            hn = SL.heute(c, max(b, 1.0), e, k) if b > 0 else None
            z[str(f)] = dict(neu=round(neu(c, b, e, k) / 12), heute=round(hn / 12) if hn is not None else None)
        db = voll * 0.05
        grenz_neu = 1 - (neu(c, voll * 0.5 + db, e, k) - neu(c, voll * 0.5, e, k)) / db
        grenz_heute = 1 - (SL.heute(c, voll * 0.5 + db, e, k) - SL.heute(c, voll * 0.5, e, k)) / db
        z["belastung_zusatzeuro_bei_halbem_mindestlohn"] = dict(neu=round(100 * grenz_neu), heute=round(100 * grenz_heute))
        out[n] = z
    return out


def kosten_de():
    """Aufstockung für Beschäftigte (grob): deutsche Lohnverteilung (Mio. Personen), je Haushaltstyp als wären alle Beschäftigten dieses Typs."""
    v = SL.verteilung("DE")
    return {n: round(sum(w * 1e6 * neu("DE", b, e, k, detail=True)[1] for w, b in v) / 1e9, 1) for n, e, k in SL.HAUSHALTE}


def main():
    erg = dict(regel=P, staaten={})
    for c in SL.LAENDER:
        erg["staaten"][c] = dict(boden_monat={n: round(boden(c, e, k) / 12) for n, e, k in SL.HAUSHALTE},
                                 anteil=anteile(c), faelle=faelle(c), lohnabstand=lohnabstand(c))
    erg["kosten_aufstockung_beschaeftigte_de_mrd"] = kosten_de()
    erg["haertefallfonds_de_mrd"] = 31.9
    E = dict(version=P["version"], status="Prüfrechnung", **erg,
             hinweis="Monatsbeträge in Landeswährung (PL: Zł), 2028, Kaufkraft 2026. Heute mit Bedarfsleistungen (sozial_laender.py). Grobe Lohnverteilung.")
    (AGG / "regel_boden.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in erg["staaten"].items():
        print(c, "Boden", x["boden_monat"], "| Anteil", x["anteil"])
        print("   Fälle", x["faelle"])
        for n, z in x["lohnabstand"].items():
            print("   ", n, {k: v for k, v in z.items()})
    print("Kosten Aufstockung Beschäftigte DE (Mrd. €, je Annahme Haushaltstyp):", erg["kosten_aufstockung_beschaeftigte_de_mrd"], "| Fonds 31,9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
