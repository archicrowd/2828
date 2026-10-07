#!/usr/bin/env python3
"""Verzeichnis aller amtlichen Eingangswerte der Gesamtrechnung, Wert für Wert, mit Abruf-URL.

Zweck: Dritte (Menschen oder KI-Agenten) sollen jeden Eingangswert einzeln an der Quelle nachprüfen können,
ohne die Skripte lesen zu müssen. Das Skript sammelt die Werte aus den Dateien, in denen die Rechnung sie
tatsächlich liest, und schreibt je Wert eine Zeile mit der Eurostat-API-Adresse, unter der er abrufbar ist.

  python3 modell/eingangswerte.py            schreibt daten/aggregate/eingangswerte.csv (ohne Netz)
  python3 modell/eingangswerte.py --abrufen  ruft jede URL einzeln ab (Pause 2 s) und schreibt
                                             daten/aggregate/eingangswerte_abgleich.csv; Rückgabe 2 bei Abweichung

Hinweise
- Eurostat-Sammelabrufe (mehrere Länder oder offene Dimensionen) liefern unvollständige oder falsch zugeordnete
  Werte (Logbuch Band I v3.1; Band III v3.11). Deshalb eine URL je Land und Größe, alle Dimensionen festgelegt.
- In der Arbeitsumgebung des Projekts erreicht die Shell ec.europa.eu nicht; die Abrufe vom 6.10.2026 liefen über
  ein Web-Abrufwerkzeug. Die Option --abrufen ist für Dritte mit Netzzugang gedacht und hier nicht getestet.
- Dimensionen, die im Projekt erfolgreich abgerufen wurden, tragen getestet=ja; die übrigen sind Vorlagen nach der
  Eurostat-Dokumentation und vor Gebrauch zu prüfen.
- Eurostat revidiert Daten. Eine Abweichung kann eine Revision sein und ist dann im Logbuch zu vermerken, nicht
  stillschweigend zu übernehmen.
"""
import contextlib
import csv
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
AGG = WURZEL / "daten" / "aggregate"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
LAENDER = ("DE", "FR", "ES", "NL", "IE", "BE", "AT", "DK", "SI", "EE")


def lade_daten():
    alt = list(sys.path)
    sys.path[:0] = [str(WURZEL / "modell" / "rahmen"), str(WURZEL / "modell" / "rechnungen" / "rahmen")]
    for n in ("basis", "daten"):
        sys.modules.pop(n, None)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import basis
            import daten
    finally:
        sys.path[:] = alt
    return basis, daten


def url(datensatz, geo, **dim):
    teile = ["format=JSON", "lang=EN", f"geo={geo}", "time=2024"] + [f"{k}={v}" for k, v in dim.items()]
    return API + datensatz + "?" + "&".join(teile)


def zeilen():
    basis, daten = lade_daten()
    with open(AGG / "laender_2024.csv", encoding="utf-8") as f:
        pop = {r["land"]: float(r["einwohner_mio_2024"]) * 1e6 for r in csv.DictReader(f)}
    with open(AGG / "zinsausgaben_2024.csv", encoding="utf-8") as f:
        zins = {r["land"]: (float(r["zinsausgaben_mio_eur_2024_nominal"]), r["status"]) for r in csv.DictReader(f)}
    Z = []

    def z(qid, ds, land, groesse, wert, einheit, u, datei, status, getestet, faktor=1.0):
        Z.append(dict(quelle_id=qid, datensatz=ds, land=land, groesse=groesse, wert=wert, einheit=einheit,
                      url=u, faktor_api_zu_wert=faktor, datei_im_repo=datei, status=status, getestet=getestet))

    for k in LAENDER:
        z("Q01", "nama_10_gdp", k, "BIP 2024", basis.GDP[k], "Mio EUR",
          url("nama_10_gdp", k, unit="CP_MEUR", na_item="B1GQ"), "modell/rahmen/basis.py (GDP)",
          "uebernommen, Abruf 2.-4.10.2026", "nein")
        z("Q02", "demo_gind", k, "Einwohner 2024 (Jahresdurchschnitt)", round(pop[k]), "Personen",
          url("demo_gind", k, indic_de="AVG"), "daten/aggregate/laender_2024.csv",
          "abgerufen 6.10.2026", "ja")
        z("Q03", "gov_10dd_edpt1", k, "Schuldenquote 2024", basis.SCHULD[k], "% des BIP",
          url("gov_10dd_edpt1", k, unit="PC_GDP", sector="S13", na_item="GD"), "modell/rahmen/basis.py (SCHULD)",
          "uebernommen, Abruf 2.-4.10.2026", "nein")
        z("Q04", "irt_lt_mcby_a", k, "Rendite zehnjähriger Staatsanleihen 2024", basis.RENDITE[k], "%",
          url("irt_lt_mcby_a", k, int_rt="MCBY"), "modell/rahmen/basis.py (RENDITE)",
          "uebernommen, Abruf 2.-4.10.2026", "nein")
        w, st = zins[k]
        z("Q05", "gov_10a_main", k, "Zinsausgaben 2024 (D41PAY)", w, "Mio EUR",
          url("gov_10a_main", k, unit="MIO_EUR", sector="S13", na_item="D41PAY"), "daten/aggregate/zinsausgaben_2024.csv",
          "geschaetzt (Abruf gescheitert)" if st == "annahme" else "abgerufen 6.10.2026", "ja")
        for cof in ("GF02", "GF07"):
            i = daten.F.index(cof)
            z("Q06", "gov_10a_exp", k, f"Staatsausgaben {cof} 2024", daten.S13[k][i], "% des BIP",
              url("gov_10a_exp", k, unit="PC_GDP", sector="S13", na_item="TE", cofog99=cof),
              "modell/rechnungen/rahmen/daten.py (S13)", "uebernommen, Abruf 2.10.2026", "nein")
        for j, code in enumerate(daten.T):
            na = "D2_D5_D91_D61_M_D995" if code == "TOTAL" else code
            wert = daten.TAX[k][j]
            if wert is None:
                z("Q07", "gov_10a_taxag", k, f"Steuern und Beiträge {na} 2024", "", "% des BIP",
                  url("gov_10a_taxag", k, unit="PC_GDP", sector="S13_S212", na_item=na),
                  "modell/rechnungen/rahmen/daten.py (TAX)", "nicht gemeldet (None), in der Summe als 0 gezählt", "nein")
                continue
            z("Q07", "gov_10a_taxag", k, f"Steuern und Beiträge {na} 2024", wert, "% des BIP",
              url("gov_10a_taxag", k, unit="PC_GDP", sector="S13_S212", na_item=na),
              "modell/rechnungen/rahmen/daten.py (TAX)", "uebernommen, Abruf 2.10.2026", "nein")
    z("Q07", "gov_10a_taxag", "DK", "D995 2024 (Gegenprobe B14)", 0.3, "% des BIP",
      url("gov_10a_taxag", "DK", unit="PC_GDP", sector="S13", na_item="D995"), "Logbuch Band III v3.11",
      "abgerufen 6.10.2026", "ja")
    # Eingänge ohne einzelne Abruf-URL (Modellsetzungen oder abgeleitete Größen), damit die Liste vollständig ist
    z("Q08", "demo_pjangroup", "Klub", "Anteil der 5- bis 19-Jährigen", 15.86, "% der Bevölkerung", "",
      "modell/rahmen/pfad.py (KIND_ANT)", "übernommen, Abruf nicht dokumentiert (B15)", "nein")
    z("Q10", "Frühjahrsprojektion", "DE", "Fortschreibungsfaktor 2024-2028", basis.F2428, "Faktor", "",
      "modell/rahmen/basis.py (RATEN 3,3/2,8/3,8/3,0 %)", "übernommen; 2028 gesetzt (B15)", "nein")
    z("Q06", "gov_10a_exp", "Klub", "Ebene A ohne Verteidigung / Ebene B (Summen der Posten)", "6.44 / 10.35",
      "% des BIP", "", "modell/rahmen/pfad.py (A_POSTEN, B_POSTEN)",
      "Zuordnung COFOG -> Posten nicht als Tabelle dokumentiert (B19)", "nein")
    z("Q06", "Setzung", "Klub", "Bodenwertabgabe (Ebene B)", 0.82, "% des BIP", "",
      "modell/rahmen/pfad.py (BODEN)", "Setzung, Herleitung im Logbuch Band II zu prüfen (B19)", "nein")
    # Abrufformen, die im Projekt erfolgreich getestet wurden (Prüfagent 7.10.2026: nama_10_gdp, gov_10dd_edpt1, gov_10a_exp)
    for r in Z:
        if r["datensatz"] in ("nama_10_gdp", "gov_10dd_edpt1", "gov_10a_exp") and r["url"]:
            r["getestet"] = "ja"
    return Z


def wert_aus_json(antwort: dict):
    v = antwort.get("value") or {}
    if len(v) != 1:
        return None
    return float(next(iter(v.values())))


def main() -> int:
    Z = zeilen()
    felder = list(Z[0].keys())
    with open(AGG / "eingangswerte.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        w.writeheader()
        w.writerows(Z)
    print(f"{len(Z)} Eingangswerte nach daten/aggregate/eingangswerte.csv "
          f"({sum(r['getestet'] == 'ja' for r in Z)} mit getesteter Abrufform)")
    if "--abrufen" not in sys.argv:
        return 0
    abw = 0
    aus = []
    for r in Z:
        if not r["url"]:
            continue
        try:
            with urllib.request.urlopen(r["url"], timeout=30) as resp:
                ist = wert_aus_json(json.load(resp))
        except Exception as e:  # Netzfehler, Ratenbegrenzung
            ist, fehler = None, str(e)[:80]
        else:
            fehler = "" if ist is not None else "kein eindeutiger Wert (Dimensionen prüfen)"
        ok = ist is not None and r["wert"] != "" and abs(ist * r["faktor_api_zu_wert"] - float(r["wert"])) <= max(0.051, 1e-4 * abs(float(r["wert"])))
        abw += not ok
        aus.append({**r, "abgerufen": ist, "gleich": "ja" if ok else "NEIN", "fehler": fehler})
        time.sleep(2)
    with open(AGG / "eingangswerte_abgleich.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(aus[0].keys()))
        w.writeheader()
        w.writerows(aus)
    print(f"Abgleich: {len(aus)} Werte, davon abweichend oder nicht abrufbar: {abw}")
    return 2 if abw else 0


if __name__ == "__main__":
    sys.exit(main())
