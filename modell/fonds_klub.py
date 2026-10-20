#!/usr/bin/env python3
"""Gemeinsamer Altlastenfonds mit Italien und Polen und für alle 30 Staaten (Logbuch v4.19). Prüfrechnung.

Anlass: v4.17 – die Länderseiten IT und PL rechnen mit dem gemeinsamen Satz der zehn (15,8 %), obwohl beide nicht zu den zehn gehören.
Methode: Bei gleichem Zins, gleichem Wachstum und gleichem Zieljahr ist die Rekursion d(t+1) = d(t)(1+i)/(1+g) + Z(t) − c linear. Der
gemeinsame Beitrag eines Klubs ist dann das BIP-gewichtete Mittel der eigenen Beiträge (moeglichkeitsraum33.json, Abgrenzung 30 Staaten:
Schuld 2024, Altrenten nach Tabelle 29). Diese Abgrenzung weicht vom Beschluss (zehn Staaten, Stand-B-Basis) ab; übertragen wird deshalb
das Verhältnis: Beschluss × (Klub / zehn) – Annahme, dass die Abweichung der Abgrenzung für alle Klubs gleich wirkt.
Ausgabe: daten/aggregate/fonds_klub.json
"""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
MR = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))["laender"]
BJ = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))["beschluss"]
ZEHN = ["DE", "FR", "ES", "NL", "IE", "BE", "AT", "DK", "SI", "EE"]
KLUBS = {"zehn (Beschluss)": ZEHN, "zehn + Italien": ZEHN + ["IT"], "zehn + Polen": ZEHN + ["PL"],
         "zwölf (zehn + Italien + Polen)": ZEHN + ["IT", "PL"], "alle 30": list(MR)}


def klub(laender):
    bip = {c: MR[c]["bip_kopf_eur_2024"] * MR[c]["einwohner_mio"] for c in laender}
    s = sum(bip.values())
    beitrag = sum(bip[c] * MR[c]["altlasten"]["beitrag_pct_bip"] for c in laender) / s
    deckung = sum(bip[c] * MR[c]["altlasten"]["beitrag_pct_bip"] / MR[c]["altlasten"]["zuschlag_pct"] * 100 for c in laender) / s
    return beitrag, beitrag / deckung * 100


def main():
    b10, z10 = klub(ZEHN)
    erg = []
    for name, l in KLUBS.items():
        b, z = klub(l)
        erg.append(dict(klub=name, staaten=len(l), beitrag_mr_pct_bip=round(b, 2), zuschlag_mr_pct=round(z, 1),
                        beitrag_skaliert_pct_bip=round(BJ["beitrag_pct_bip"] * b / b10, 2), zuschlag_skaliert_pct=round(BJ["zuschlag_auf_alle_steuern_pct"] * z / z10, 1)))
    E = dict(version="v4.19", status="Prüfrechnung", beschluss=dict(beitrag_pct_bip=BJ["beitrag_pct_bip"], zuschlag_pct=BJ["zuschlag_auf_alle_steuern_pct"]),
             klubs=erg, hinweis="BIP 2024 (bip_kopf × Einwohner, moeglichkeitsraum33). Skaliert = Beschluss × Verhältnis zur Zehnergruppe in der Abgrenzung "
                                 "des Möglichkeitsraums (Annahme). Zins 2,5 %, Wachstum 3 %, Tilgung bis 2098 wie im Beschluss.")
    (AGG / "fonds_klub.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in erg:
        print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
