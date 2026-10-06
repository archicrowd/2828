# TAX 28:28 — Webseite, acht Sprachfassungen

## Was hier liegt

| Datei | Sprache | Rolle |
|---|---|---|
| `index.html` | Englisch | Einstiegsseite, zugleich für Irland |
| `de.html` | Deutsch | Ursprungsfassung, hier wird redigiert |
| `fr.html` | Französisch | Frankreich, Belgien |
| `es.html` | Spanisch | Spanien |
| `nl.html` | Niederländisch | Niederlande, Belgien |
| `da.html` | Dänisch | Dänemark |
| `sl.html` | Slowenisch | Slowenien |
| `et.html` | Estnisch | Estland |

Jede Datei ist eigenständig: Aufbau, Stil, Rechner, Diagramm und alle Anlagen
stecken in der Datei selbst. Keine Inhalte von Dritten, keine Cookies, keine Tracker.
Die Schriften liegen bereits auf dem Server; die Pfade zu `fonts/` sind unverändert.

## Suchmaschinen sind gesperrt

Jede Seite trägt im Kopf

    <meta name="robots" content="noindex, nofollow">

Das hält die Seite aus den Trefferlisten von Google und Bing heraus. Über den Link
bleibt sie voll erreichbar — sie wird nur nicht zufällig gefunden. Vor einer offenen
Veröffentlichung diese Zeile entfernen: Sie steht einmal in `tpl.py`, danach neu bauen.

Die Sperre wirkt nicht gegen Weitergabe. Wer den Link hat, kann ihn beliebig teilen.

## Impressum

**Initiative 28 : 28 — Arndt Hermann, 2828@archicrowd.de**, dazu der Kontaktlink
„Kritik einreichen“ mit dem Betreff 28:28. Eine Anschrift ist auf Wunsch nicht
angegeben. Zur Kenntnis, ohne weitere Empfehlung: § 5 Digitale-Dienste-Gesetz
verlangt für geschäftsmäßige Telemedien Namen und Anschrift; ob ein
nicht-geschäftsmäßiges Projekt darunterfällt, wäre im Einzelfall zu beurteilen.

## Der Abschnitt „Ein Modell für viele Länder“

Zehn Länderdateien: Deutschland, Frankreich, Spanien, Niederlande, Irland,
Belgien, Österreich, Dänemark, Slowenien, Estland. Zusammen 257,2 Mio. Einwohner,
56,9 % der EU-Bevölkerung.

Neun Mitgliedstaaten sind die Schwelle für eine verstärkte Zusammenarbeit nach dem
EU-Vertrag. Zehn gerechnete Dateien lassen also einen Platz Spielraum — es müssen
nicht alle mitmachen.

Zwei Kästen heben Sonderfälle heraus: Estland (grün) als das Land, das dem
Bauprinzip heute am nächsten ist, und Irland (rot) als den schwierigsten Fall.

## Ändern

Die Dateien werden nicht von Hand bearbeitet, sondern neu gebaut:

    cd quelltext
    python3 klub10.py         # Länderrechnung, schreibt klub10-daten.json
    python3 build.py          # alle acht Seiten
    python3 build.py de en    # nur einzelne

- `lang/<code>.json` — sämtliche Texte, ein Schlüssel je Textbaustein
- `css.py` — das Stylesheet
- `tpl.py` — das HTML-Gerüst, das JavaScript und die noindex-Zeile
- `build.py` — Tabellen, Zahlenformate je Sprache, Zusammenbau

Fehlt ein Baustein in einer Sprachdatei, erscheint automatisch der englische;
der Build meldet das. Zahlen werden je Sprache formatiert.

## Herkunft der Zahlen

- Haushalte, Haushaltspfad, Szenarien: `modell-2828.py`
- Rechner auf der Seite: dieselbe Logik wie `rechner-2828.js`
- Zehn Länderdateien: `klub10.py`, Ergebnisse in `klub10-ergebnisse.txt`

Alle drei Quelltexte sind in jede Seite eingebettet und über den Abschnitt
„Rechenmodelle“ lesbar.

## Was offen ist

- Die Übersetzungen stammen von mir und sind fachlich nicht gegengelesen.
  Besonders die Fachbegriffe im Dänischen, Slowenischen und Estnischen sollte je
  eine muttersprachliche Fachperson prüfen. Der Hinweis steht im Fuß jeder Seite.
- Die Anlage „Annahmen und Quellen“ liegt nur auf Deutsch und Englisch vor.
- Das Median-Einkommen je Land stammt aus einer WKO-Zusammenstellung der
  EU-SILC-Daten, nicht aus der Primärstatistik. Für Österreich weichen zwei
  Lesungen derselben Tabelle voneinander ab (36.114 gegen 36.546 €); eingesetzt
  ist der höhere Wert, er ändert die österreichische Dividende um rund 6 €.
  Vor einer Veröffentlichung mit Anspruch sollten alle Werte direkt bei
  Eurostat geholt werden.
- Der Anteil der 0- bis 14-Jährigen ist für Estland, Irland, Belgien und
  Slowenien geschätzt, nicht belegt.
- Die Wirtschaftsquote der zehn Länder (rund 70 % der EU) vergleicht
  Länderprojektionen für 2026 mit der EU-Summe für 2025 und ist deshalb eher
  die Obergrenze. Die Bevölkerungsquote von 56,9 % ist belastbarer.
- Die Einstufung Belgiens als EU-Steueroase folgt Tørsløv, Wier und Zucman.
  Belgiens eigener Unternehmensteuersatz liegt bei 25 %; die Einstufung beruht
  auf zugeflossenen verlagerten Gewinnen (15 Mrd. USD im Jahr 2016), nicht auf
  dem Satz.
