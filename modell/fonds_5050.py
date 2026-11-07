#!/usr/bin/env python3
"""Altlastenfonds mit geteilter Verantwortung 50/50 (Logbuch v4.74). Entwicklungsmodus, vorläufige Prüfrechnung, kein Beschluss.

Regel: Jeder Staat trägt die Hälfte seiner Altlast (Schulden und ungedeckte Rentenzusagen) selbst, mit dem Satz, den sein eigener Fonds bräuchte;
die andere Hälfte tragen alle Teilnehmer gemeinsam, mit dem gemeinsamen Satz. Beitrag je Staat = ½ × eigener Beitrag + ½ × gemeinsamer Beitrag,
dauerhaft (statt Verrechnung, die in 30 Jahren von eigen auf gemeinsam übergeht). Partner unter der Rechtsstaatsschwelle tragen ihre Altlast
ganz selbst. Verfahren wie fonds_klub.py: eigene Beiträge in der Abgrenzung des Möglichkeitsraums, skaliert mit dem Beschluss (Annahme: gleicher
Faktor für eigene und gemeinsame Beiträge). Tilgung bis 2098, Zins 2,45 %.
Ausgabe: daten/aggregate/fonds_5050.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "fonds_5050.toml").read_text(encoding="utf-8"))
SA = tomllib.loads((W / "modell" / "staatenauswahl.toml").read_text(encoding="utf-8"))["staaten"]
spec = importlib.util.spec_from_file_location("fk", W / "modell" / "fonds_klub.py")
FK = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(FK)
FG = json.loads((W / "daten" / "aggregate" / "fonds_geltend.json").read_text(encoding="utf-8"))


def main():
    b10, z10, _ = FK.klub(FK.ZEHN)
    fb, fz = FK.BU["beitrag_pct_bip"] / b10, FK.BU["zuschlag_auf_alle_steuern_pct"] / z10
    alle = list(FK.MRJ)
    a = P["anteil_gemeinsam"]
    teil = [c for c in alle if SA[c][0] >= P["schwelle_wjp"] or c in P["ohne_wert_teilnahme"]]
    b30, z30, _ = FK.klub(alle)
    bt, zt, _ = FK.klub(teil)
    bip = {c: FK.MRJ[c]["bip_kopf_eur_2024"] * FK.MRJ[c]["einwohner_mio"] for c in alle}

    def eigen(c):
        return fb * FK.MRJ[c]["altlasten"]["beitrag_pct_bip"], fz * FK.MRJ[c]["altlasten"]["zuschlag_pct"]
    zeilen = {}
    for c in alle:
        be, ze = eigen(c)
        v = FG["verrechnung"]["laender"][c]["reihe"]
        if c in teil:
            b55, z55 = a * fb * bt + (1 - a) * be, a * fz * zt + (1 - a) * ze
        else:
            b55, z55 = be, ze
        zeilen[c] = dict(stufe="Teilnahme" if c in teil else "Partner (trägt ganz selbst)",
                         eigen=dict(beitrag_pct_bip=round(be, 2), zuschlag_pct=round(ze, 1)),
                         gemeinsam_alle_30=dict(beitrag_pct_bip=round(fb * b30, 2), zuschlag_pct=round(fz * z30, 1)),
                         geltend_verrechnung_2028=v["2028"], geltend_ab_2058=v["2058"],
                         geteilt_5050=dict(beitrag_pct_bip=round(b55, 2), zuschlag_pct=round(z55, 1)))
    # Summenkontrolle: BIP-gewichtetes Mittel des Beitrags bleibt bei voller Teilnahme gleich
    b_mittel_alle = sum(bip[c] * (a * fb * b30 + (1 - a) * eigen(c)[0]) for c in alle) / sum(bip.values())
    if abs(b_mittel_alle - fb * b30) > 1e-6:
        raise SystemExit("Summenkontrolle 50/50 verletzt")
    E = dict(version=P["version"], status="Entwicklungsmodus: vorläufige Prüfrechnung, kein Beschluss", anteil_gemeinsam=a,
             teilnehmer=teil, partner=[c for c in alle if c not in teil],
             gemeinsamer_satz_teilnehmer=dict(beitrag_pct_bip=round(fb * bt, 2), zuschlag_pct=round(fz * zt, 1)),
             laender=zeilen,
             hinweis="Beitrag in % des eigenen BIP und Zuschlag auf alle Steuern des Staates, dauerhaft. Eigener Satz = eigener Fonds (Tilgung bis 2098) "
                     "in der Abgrenzung des Möglichkeitsraums, skaliert mit dem Beschluss (Annahme). Geltend: Verrechnung 2028 und gemeinsamer Satz ab 2058.")
    (W / "daten" / "aggregate" / "fonds_5050.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("gemeinsam Teilnehmer", E["gemeinsamer_satz_teilnehmer"], "Partner", E["partner"])
    for c in sorted(alle, key=lambda x: -zeilen[x]["eigen"]["zuschlag_pct"]):
        r = zeilen[c]
        print(f"{c} {r['stufe'][:9]:9} eigen {r['eigen']['zuschlag_pct']:5} | 50/50 {r['geteilt_5050']['zuschlag_pct']:5} | geltend 2028 {r['geltend_verrechnung_2028']['zuschlag_pct']:5} ab 2058 {r['geltend_ab_2058']['zuschlag_pct']:5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
