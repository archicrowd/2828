#!/usr/bin/env python3
"""Effektiver Kürzungssatz der Rentenzusagen je Staat (Logbuch v4.37, R6; seit v4.72 Regel BS35). Prüfrechnung.

v4.72: Regel BS35 (Beschluss 5.11.2026) statt E. s(r) wird aus 400 Personen der deutschen Mikrosimulation mit Zusage relativ zum Mittel und
zugeschätzten Versicherungsjahren gerechnet (rentner_kombi.json, paare_rel_jahre): s(r) = E[Kürzung_BS35(X, J; G = r)] / E[X]. Annahme: gleiche
Verteilung von Zusagen und Jahren in allen Staaten (offen; in Staaten mit kürzeren Laufbahnen wirkt der Sockel stärker).
Bis v4.71:

Regel E (Beschluss 22.10.2026): 15 % auf den Teil der Zusage (staatliche Rente, Beamtenversorgung) über dem Grundbedarf je Person. In Deutschland
ergibt das effektiv 6,95 % aller Zusagen (rentner_kombi.py, Mikrosimulation). Bis v4.36 galt dieser Satz für alle 30 Staaten (Annahme).
Hier: Lage der Zusagen zum Grundbedarf je Staat. r_c = Grundbedarf / mittlere Zusage je Person ab 65; die mittlere Zusage aus COFOG GF1002 + GF1003
(% BIP) / Anteil 65+ × BIP je Kopf (moeglichkeitsraum33, wie sozialschutz.z_pfad), Grundbedarf nach Preisniveau (moeglichkeitsraum33).
Die Form der Verteilung (Zusage je Person relativ zum Mittel) kommt aus der deutschen Mikrosimulation (Annahme: gleiche Form in allen Staaten).
Der Abstand zwischen Makro- und Mikromittel in Deutschland (COFOG je Person ab 65 gegen Zusagen der Rentnerhaushalte) wird für alle Staaten gleich
angenommen: r_c = r_DE,mikro × r_c,makro / r_DE,makro. Satz k_c = k_DE × s(r_c) / s(r_DE), s(r) = 0,15 · E[max(0, X − r)] / E[X].
Der Boden (B1, sozialschutz.toml) bleibt deutsch skaliert (offen). Prüft, dass altlasten.toml [kuerzung_staat] den gerechneten Sätzen entspricht.
Ausgabe: daten/aggregate/kuerzung_laender.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
AL = tomllib.loads((W / "modell" / "altlasten.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("mr", W / "modell" / "moeglichkeitsraum33.py")
MR = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(MR)
MRJ = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))["laender"]
V = json.loads((AGG / "rentner_kombi.json").read_text(encoding="utf-8"))["verteilung_zusage"]
Q = np.array(V["quantile_rel"])
PAARE = np.array(V["paare_rel_jahre"])
spec = importlib.util.spec_from_file_location("h33", W / "modell" / "haushalte33.py")
H = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(H)
REGEL = H.P["rente_regel"]
SATZ = REGEL.get("satz", 0.15)


def s(r):
    """Anteil der Kürzung an allen Zusagen bei Grundbedarf r (in Vielfachen der mittleren Zusage), Regel BS35 (v4.72)."""
    g = dict(REGEL, freibetrag_monat=r / 12)
    return float(np.mean([H.kuerzung_bs35(x, j, g) for x, j in PAARE]) / PAARE[:, 0].mean())


def rechne():
    makro = {}
    for c in MRJ:
        kp = MR.kopf[c] * MR.P["bip_2024_zu_kaufkraft_2026_2028"]
        zusage = (MR.D["gf1002"][c] + MR.D["gf1003"][c]) / MR.D["anteil65"][c] * kp      # € je Person ab 65 und Jahr
        gb = MRJ[c]["z2028"]["grundbedarf_monat_eur"] * 12
        makro[c] = dict(zusage_monat=round(zusage / 12), grundbedarf_monat=round(gb / 12), r_makro=gb / zusage)
    r_de = V["r_grundbedarf_zu_mittel"]
    out = {}
    for c, m in makro.items():
        r = r_de * m["r_makro"] / makro["DE"]["r_makro"]
        out[c] = dict(m, r_makro=round(m["r_makro"], 3), r=round(r, 3), satz=round(AL["kuerzung"] * s(r) / s(r_de), 4))
    return out


def main():
    L = rechne()
    toml = AL.get("kuerzung_staat", {})
    abw = {c: (x["satz"], toml.get(c)) for c, x in L.items() if toml.get(c) is None or abs(toml[c] - x["satz"]) > 0.0005}
    E = dict(version="v4.72", status="Prüfrechnung (R6), Regel BS35", regel=REGEL, kuerzung_de=AL["kuerzung"], je_staat_aktiv=AL.get("kuerzung_je_staat", False),
             laender=L, hinweis="Zusage je Person ab 65 aus COFOG GF1002+GF1003 (2024, % BIP) × BIP je Kopf (Kaufkraft 2026–2028, Rechengröße); "
                                 "Verteilungsform aus der deutschen Mikrosimulation (Annahme); Euro je Monat, Preise 2026.")
    (AGG / "kuerzung_laender.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in sorted(L, key=lambda c: L[c]["satz"]):
        print(c, L[c])
    if E["je_staat_aktiv"] and abw:
        raise SystemExit(f"altlasten.toml [kuerzung_staat] veraltet: {abw}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
