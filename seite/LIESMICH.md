# seite/ — Webseite

**Stand A (national, Logbuch v2.0).** Die achtsprachige Seite hat den Rahmenwechsel zu Klub A/B
(v3.1 ff.) und die Quote 30,6 % **nie gesehen**. Sie ist inhaltlich überholt, technisch vollständig.

| Ordner | Inhalt |
|---|---|
| `stand-b/` | **Seite zum Stand B** in sechs Sprachen (`de`, `en`, `fr`, `it`, `es`, `pl`; seit v3.18), gebaut mit `werkzeuge/seite_bau.py` aus `werkzeuge/vorlage.html` und `werkzeuge/sprachen/*.json` aus `daten/aggregate/gesamtrechnung.json`; Stylesheet unverändert aus `stand-a-national/de.html`; Quellen der Länderbeispiele in `stand-b/QUELLEN.md`. Für die Veröffentlichung den Ordner `fonts/` der laufenden Seite daneben legen. Andere Sprachen folgen |
| `werkzeuge/` | Bauskript der neuen Seite |
| `stand-a-national/` | acht Sprachfassungen (`index` = EN, `de`, `fr`, `es`, `nl`, `da`, `sl`, `et`) und `quelltext/` (`build.py`, `css.py`, `tpl.py`, `lang/*.json`, `klub10.py`, vier Patch-Skripte). Tarif 0/9/16/21/26/28, Mehrwertsteuer 5/11/17/22/28. Der Quelltext passt zu genau diesem Build. Eigene `LIESMICH.md` |
| `stand-a-neuerer-build/` | späterer Build (`dist/`, Tarif 0/9/19/24/27/28, Mehrwertsteuer 5/11/20/25/28, Effektivsatz 21,5 %) mit drei Patch-Skripten und `qa_tarif.py`. Der dazugehörige Quelltext ist **nicht erhalten** |
| `rahmenstruktur-seiten/` | Seite zum Stand B (`rahmenstruktur-aktuell.html`, 506/472/651 €), alte deutsche Homepage, 3030-Haushaltspfad, Social-Grafik |

**Fehler auf der veröffentlichten Seite (Korrektur 53):** Der Kasten „Warum Estland im Klub ist" nennt für 2026 einen Satz von 24 %; Estland bleibt bei 22 %. Mit der Veröffentlichung von `stand-b/de.html` entfällt die Aussage.

**Veröffentlichte Seite.** `archicrowd.de` zeigt nach Abruf in dieser Sitzung (Kurzauszug, nicht
Zeile für Zeile verglichen) Tarif 0/9/16/21/26/28 und Mehrwertsteuer 5/11/17/22/28, also den Stand von
`stand-a-national/`, mit `noindex, nofollow`. Der spätere Build scheint nicht veröffentlicht zu sein.

**Wiederherstellung des späteren Builds** (Reihenfolge laut Begleitdatei des Vorchats, **nicht
ausgeführt**): im Ordner `stand-a-national/quelltext` nacheinander `patch_tarif.py`, `patch_ev.py`,
`patch_anhang.py` (aus `stand-a-neuerer-build/`), dann `klub10.py` und `build.py`. Die Patch-Skripte
schreiben `tpl.py` und `build.py` an Ort und Stelle um; vorher den Ordner sichern.

**Impressum der Seite:** nennt eine Person mit Namen und die Adresse 2828@archicrowd.de. Das
Repository ist privat (Abruf 6. Oktober 2026). Wird es öffentlich, steht dieser Name im Quelltext.
