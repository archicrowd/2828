#!/usr/bin/env python3
"""Frankreich: Schuldenfortschreibung 2026–2028 (Logbuch v3.23, Recherche länderspezifische Fassung).

Vergleicht drei Pfade für die Staatsschuldenquote Frankreichs (Gesamtstaat, % des BIP):
  A  Annahme wie im Klub (Schuldenpfad.py): Defizit 2025 bleibt gleich, nominales Wachstum 3,0 %
  B  Regierungspfad mit Regierungs-Defizit (PLF-Anhang / RESF 2027), Wachstum 3,0 %
  C  Regierungspfad mit dem Wachstum, das die Regierungs-Schuldenquote 2026–2028 impliziert
Die Schuldenquote wird mit d(t) = d(t−1)/(1+g) − saldo fortgeschrieben (Saldo negativ = Defizit), wie
in modell/schuldenpfad.py. Eingaben: daten/aggregate/frankreich_eingaben.md. Ausgabe: daten/aggregate/frankreich.json.

Keine Prognose des Autors: Die Pfade sind Rechnungen mit amtlichen Prognosen der französischen Regierung
(Sekundärbezug über den Agentenabruf, nicht selbst geprüft) und der Annahme des Klubs.
"""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"

D25 = 115.6                       # Schuldenquote 2025, INSEE IR78 (amtlich)
SALDO25 = -5.1                    # Finanzierungssaldo 2025, INSEE (amtlich)
REG_SALDO = {2026: -5.4, 2027: -5.0, 2028: -3.9}        # Regierungspfad, PLF-Anhang / RESF 2027 (Prognose)
REG_QUOTE = {2026: 119.3, 2027: 121.7, 2028: 122.4}     # Regierungs-Schuldenquote (Prognose)
G_NOM = 3.0                       # nominales Wachstum wie im Klub (Annahme)


def pfad(saldo_je_jahr, g):
    d, out = D25, {}
    for j in (2026, 2027, 2028):
        d = d / (1 + g / 100) - saldo_je_jahr[j]
        out[j] = d
    return out


def wachstum_implizit():
    """Nominales Wachstum, das die Regierungs-Schuldenquote mit ihrem Saldo reproduziert (je Jahr)."""
    d_prev, res = D25, {}
    for j in (2026, 2027, 2028):
        g = (d_prev / (REG_QUOTE[j] + REG_SALDO[j]) - 1) * 100
        res[j] = g
        d_prev = REG_QUOTE[j]
    return res


klub_saldo = {j: SALDO25 for j in (2026, 2027, 2028)}
A = pfad(klub_saldo, G_NOM)
B = pfad(REG_SALDO, G_NOM)
g_imp = wachstum_implizit()
C = {}
d_prev = D25
for j in (2026, 2027, 2028):
    d_prev = d_prev / (1 + g_imp[j] / 100) - REG_SALDO[j]
    C[j] = d_prev

E = dict(
    eingaben=dict(schuld_2025=D25, saldo_2025=SALDO25, regierung_saldo=REG_SALDO, regierung_quote=REG_QUOTE,
                  g_nominal_annahme=G_NOM),
    pfad_A_klub_annahme={str(k): round(v, 2) for k, v in A.items()},
    pfad_B_regierung_defizit_g3={str(k): round(v, 2) for k, v in B.items()},
    pfad_C_regierung_implizites_wachstum={str(k): round(v, 2) for k, v in C.items()},
    nominales_wachstum_implizit={str(k): round(v, 2) for k, v in g_imp.items()},
    regierung_quote=REG_QUOTE,
    abweichung_B_gegen_regierung_2028=round(B[2028] - REG_QUOTE[2028], 2),
    abweichung_A_gegen_regierung_2028=round(A[2028] - REG_QUOTE[2028], 2),
    hinweis="Pfad C reproduziert die Regierungsquote per Konstruktion. Pfad A entspricht der Klubannahme für Frankreich; "
            "die Klubannahme (gewichtet −2,93 %) gilt nicht für Frankreich allein.",
)
(AGG / "frankreich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"Ausgangslage 2025: {D25} % (INSEE), Saldo {SALDO25} %")
print(f"{'Jahr':<6}{'A Klub-Annahme':>16}{'B Regierung g3':>16}{'C Regierung g impl.':>21}{'Regierung':>12}  g impl.")
for j in (2026, 2027, 2028):
    print(f"{j:<6}{A[j]:>16.1f}{B[j]:>16.1f}{C[j]:>21.1f}{REG_QUOTE[j]:>12.1f}  {g_imp[j]:.2f} %")


# ---------------------------------------------------------------- Wirkung auf den Klub-Schuldenpfad
# Klub wie in schuldenpfad.py (BIP-gewichtet, Gewichte BIP 2024 aus basis.py). Gesamtsaldo des Klubs bleibt
# −2,93 %; Frankreich bekommt seinen eigenen Saldo, die übrigen Länder erhalten den Rest-Saldo. Das
# Wachstum: 3,0 % für die übrigen Länder, für Frankreich das Regierungs-Wachstum (Pfad C).
# Sensitivität, kein Ersatz für die Gesamtrechnung (Entscheidung der Initiative, Logbuch v3.23).
import contextlib, csv, importlib.util, io  # noqa: E402

_spec = importlib.util.spec_from_file_location("basis", W / "modell" / "rahmen" / "basis.py")
_basis = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(_basis)
GDP = _basis.GDP
TOT = sum(GDP.values())
WFR = GDP["FR"] / TOT
with open(AGG / "schulden_2010_2025.csv", encoding="utf-8") as _f:
    _ZEILEN = {r["land"]: r for r in csv.DictReader(_f)}
KLUB_SALDO = -2.93                                 # wie schuldenpfad.py
D_KLUB_25 = sum(GDP[k] * float(_ZEILEN[k]["2025"]) for k in GDP) / TOT
D_REST_25 = sum(GDP[k] * float(_ZEILEN[k]["2025"]) for k in GDP if k != "FR") / (TOT - GDP["FR"])
D_FR_25 = float(_ZEILEN["FR"]["2025"])


def s_rest(s_fr):
    return (KLUB_SALDO * TOT - s_fr * GDP["FR"]) / (TOT - GDP["FR"])


def klub_mit_frankreich(s_fr_je_jahr, g_fr_je_jahr, g_rest=G_NOM):
    dr, df = D_REST_25, D_FR_25
    for j, sf, gf in zip((2026, 2027, 2028), s_fr_je_jahr, g_fr_je_jahr):
        dr = dr / (1 + g_rest / 100) - s_rest(sf)
        df = df / (1 + gf / 100) - sf
    return (dr * (TOT - GDP["FR"]) + df * GDP["FR"]) / TOT, df


_s_reg = [REG_SALDO[j] for j in (2026, 2027, 2028)]
_g_imp = [g_imp[j] for j in (2026, 2027, 2028)]
_klub_annahme = D_KLUB_25
for _ in range(3):
    _klub_annahme = _klub_annahme / (1 + G_NOM / 100) - KLUB_SALDO
K_A, _ = klub_mit_frankreich([SALDO25] * 3, [G_NOM] * 3)
K_B, _ = klub_mit_frankreich(_s_reg, [G_NOM] * 3)
K_C, FR_C = klub_mit_frankreich(_s_reg, _g_imp)
E["klub_2028"] = dict(
    schulden_klub_2028_schuldenpfad_py=round(_klub_annahme, 2),
    klub_2028_fr_annahme_wie_klub=round(K_A, 2),
    klub_2028_fr_regierungsdefizit_g3=round(K_B, 2),
    klub_2028_fr_regierungsdefizit_und_wachstum=round(K_C, 2),
    fr_2028_pfad_c=round(FR_C, 2),
    fr_gewicht_klub_bip_pct=round(WFR * 100, 1),
    hinweis="Klubquote 2028 mit Frankreich auf eigenem Pfad. Die Klubquote im Konzept (81,3 %) bleibt bis zur Entscheidung unverändert.",
)
(AGG / "frankreich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Klub 2028: Klubmethode {_klub_annahme:.2f} | FR wie Klub {K_A:.2f} | FR Regierungsdefizit {K_B:.2f} | "
      f"FR Regierungsdefizit und -wachstum {K_C:.2f} (FR 2028: {FR_C:.1f}); FR-Gewicht {WFR*100:.1f} %")
