# Mitarbeit von außen

Das Repository ist privat; Zugang erhält, wer vom Projektverantwortlichen (Arndt Hermann,
2828@archicrowd.de) eingeladen wird. Vorgesehen sind Beiträge Dritter, vor allem
**Mikrosimulationen** (siehe `schnittstelle/MIKROSIMULATION.md`), Prüfungen einzelner Zahlen und
Korrekturen. Entwurf, noch nicht erprobt.

## Regeln (aus `CLAUDE.md`, für Dritte zugeschnitten)

1. **Quellen angeben.** Bei nur einer Quelle oder einer nicht amtlichen Quelle das im Text kennzeichnen
   („Sekundärquelle", „Annahme", „maschinell gelesen, an der Quelle zu prüfen").
2. **Einheit, Bezugsjahr, Preisbasis** (nominal oder real, mit Preisjahr) an jeder Euro-Zahl. Anteile
   am BIP und Euro-Werte nicht ohne Bezugsgröße nebeneinanderstellen (Korrekturen 42 bis 46).
3. **Keine Rohdaten und keine Mikrodaten** einchecken (Taxplorer, SOEP, EU-SILC, OECD-Rohdateien).
   Beiträge enthalten Skripte und Aggregate. Die Auflagen Ihres Datenvertrags gehen vor.
4. **Fehler offen führen**, auch eigene. Ein Beitrag, dessen Irrtümer offen liegen, ist überprüfbar.
5. **Ein Beitrag, ein Verzeichnis** unter `beitraege/`, mit `LIESMICH.md`, Skript und Ergebnisdatei.
6. Dateinamen ohne Umlaute und Leerzeichen.

## Ablauf

1. `python3 modell/alles.py` ausführen. Alle Stufen müssen ohne Fehler laufen, bevor und nachdem Sie
   etwas ändern.
2. Beitrag unter `beitraege/<kuerzel>-<jahr>/` ablegen; Ergebnisdatei mit
   `python3 schnittstelle/pruefe_beitrag.py beitraege/<kuerzel>-<jahr>/ergebnis.csv` prüfen.
3. Ändert Ihr Beitrag eine Zahl des Konzepts, nennen Sie die betroffenen Aussagen
   (`dokumente/aussagen.csv`, Spalte `id`) und die Parameter (`modell/parameter.toml`).
4. Der Projektverantwortliche entscheidet über die Aufnahme. Aufgenommene Beiträge erscheinen im Logbuch
   mit Autorin oder Autor, Datenquelle und Datum. Keine Zahl des Konzepts ändert sich ohne Eintrag im Logbuch.

## Was noch fehlt

Lizenz (seit v3.12): Skripte MIT (`LICENSE`), Texte und Ergebnisdateien CC BY 4.0 (`LICENSE-DOKUMENTE.md`), siehe `LIZENZ.md`. Ein Beitrag steht unter der Lizenz des Teils, in den er eingeht; das ist im Pull Request zu bestätigen.
