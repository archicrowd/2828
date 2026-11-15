# Plattformen am Ort der Nutzung: Regel und Variante

Initiative 28:28 · 15. November 2026 · Modellstand v4.86 · Rechnung: `modell/plattformen33.py` (+ `.toml`) → `daten/aggregate/plattformen33.json`
Status: **Regel beschlossen (Empfehlungen übernommen, 15.11.2026); Aufkommen als Variante gerechnet, nicht in der Deckung.**

## 1 Regel (gilt für alle Unternehmen, nicht nur für Plattformen)

1. **Ort:** Umsätze mit Endkunden zählen dort, wo die Leistung genutzt wird (Gerät, Rechnungsadresse).
2. **Gewinn:** Der Konzerngewinn wird nach diesem Umsatzanteil auf die Staaten verteilt, darauf 33 %. Wo der Gewinn gebucht ist, spielt keine
   Rolle; das ist der Schutz gegen Gewinnverschiebung.
3. **Untergrenze:** 33 % auf eine pauschale Gewinnquote von 10 % des Umsatzes am Nutzungsort, also 3,3 % des Umsatzes. Sie wird auf die Steuer
   aus Schritt 2 angerechnet und greift bei Verlustausweis oder niedriger Marge. Ihre Höhe liegt in der Spanne der heutigen Digitalsteuern
   (2–5 %) und beim Vorschlag des UN-Musterartikels 12B (3–4 %).
4. **Mehrwertsteuer:** bleibt unverändert. Für elektronische Leistungen an Verbraucher gilt in der EU schon heute der Kundenort (eigene Kenntnis,
   an der Richtlinie zu prüfen). Sie trifft die Nutzer, nicht die Gewinne. Bei Werbeerlösen läuft sie wegen des Vorsteuerabzugs ins Leere.

## 2 Grundlage der Rechnung

Der Umsatz großer Digitalkonzerne mit Nutzern im Land ist aus dem Aufkommen der Digitalsteuern zurückgerechnet (Aufkommen geteilt durch Satz):

| Land | Jahr | Aufkommen | Satz | Umsatz in % BIP | Umfang | Quelle |
|---|---|---|---|---|---|---|
| UK | 2024/25 | 808 Mio. £ | 2 % | 1,42 | soziale Medien, Suche, Marktplätze | HM Treasury/HMRC, DST Review 2025 (amtlich); BIP eigene Kenntnis |
| FR | 2024 | 800 Mio. € | 3 % | 0,91 | Werbung, Vermittlung, Daten | Erwartung des Ministeriums nach Club Patrimoine (Sekundärquelle) |
| IT | 2024 | 454,7 Mio. € | 3 % | 0,69 | Werbung, Vermittlung, Daten | Unimpresa nach Corriere Comunicazioni (Sekundärquelle) |
| AT | 2023 | 103 Mio. € | 5 % | 0,42 | nur Onlinewerbung | BMF Österreich (amtlich); nur als Untergrenze |

**Grenzen der Grundlage:**
- Die Rückrechnung erfasst nur große Konzerne: Die Steuern greifen erst ab 750 Mio. € bzw. 500 Mio. £ Umsatz weltweit.
- Die Tatbestände unterscheiden sich je Land.
- Im Vereinigten Königreich mindern Ermäßigungen das Aufkommen, die Rückrechnung unterschätzt dort also eher.
- Für Italien liegt 2025 ein höheres Aufkommen vor (637 Mio. €), nach dem Wegfall der Inlandsschwelle.

## 3 Ergebnis

Fälle vorsichtig / mittel / hoch: Grundlage = kleinster / mittlerer / größter Länderwert.

**Annahmen:**
- Marge großer Digitalkonzerne: 15 / 25 / 35 %.
- Anteil der Umsätze von Konzernen mit Marge unter 10 %: 30 / 20 / 10 %.
- Anteil der Steuer, der heute schon im Land gezahlt wird: 20 / 10 / 5 %.

| | vorsichtig | **mittel** | hoch |
|---|---|---|---|
| Umsatz am Nutzungsort | 0,69 % BIP | **0,91 % BIP** | 1,42 % BIP |
| Mehraufkommen | 0,025 % BIP | **0,059 % BIP** | 0,144 % BIP |
| Deutschland 2028 (nominal) | 1,2 Mrd. € | **2,9 Mrd. €** | 7,1 Mrd. € |
| Dividende je Erwachsenem und Monat | 1 € | **3 €** | 8 € |
| wirksame Belastung des Umsatzes | 4,5 % | **7,3 %** | 10,7 % |
| davon Aufstockung durch die Untergrenze | 0,005 % BIP | 0,004 % BIP | 0,003 % BIP |

**Lesart:**
- Die Regel belastet die Umsätze großer Digitalkonzerne im mittleren Fall wirksam mit rund 7 %. Das ist mehr als das Doppelte einer heutigen
  Digitalsteuer von 3 %.
- Das Aufkommen ist für die Dividende aber klein, rund 3 € je Erwachsenem.
- Die Untergrenze bringt im Aggregat wenig, weil die großen Anbieter hohe Margen haben. Ihr Wert liegt im Schutz gegen Verlustausweis und
  Gewinnverlagerung im Einzelfall.

## 4 Abgrenzung zur Prüfrechnung R6

R6 (OECD-Länderberichte) verteilt Konzerngewinne nach dem Umsatz am Ort der buchenden Gesellschaft. Digitale Umsätze, die in Irland oder den
Niederlanden gebucht werden, zählen dort. Die Plattformvariante ergänzt R6 um diesen Teil. Eine Doppelzählung bleibt möglich, soweit lokale
Vertriebsgesellschaften schon im Land buchen; das ist grob über „heute schon gezahlt“ erfasst.

## 5 Offen

1. Ob der Plattformanteil in die Deckung geht, entscheidet die Initiative erst nach dem Beleg der Unternehmensposition (Prüfbefund B-1).
2. **Bessere Grundlage:** Meldungen über die zentrale Mehrwertsteuer-Stelle der EU (Umsätze elektronischer Dienste an Verbraucher je Staat),
   sofern veröffentlicht; Geschäftsberichte nach Regionen.
3. **Drittstaaten:** Doppelbesteuerung ohne Anrechnung, Handelsstreit mit den USA (Zolldrohungen gegen Digitalsteuern); innerhalb der
   Gemeinschaft über gegenseitige Anrechnung lösbar.
4. Rechtsprüfung P1: Vereinbarkeit der Untergrenze mit Doppelbesteuerungsabkommen und dem Unionsrecht.

## 6 Quellen

- HM Treasury / HMRC (2025): Digital Services Tax Review, Tabelle 4.A. [GOV.UK](https://www.gov.uk/government/publications/digital-services-tax-review/digital-services-tax-review-report)
- BMF Österreich (2024): Digitalsteuer 2023. [BMF](https://www.bmf.gv.at/presse/pressemeldungen/2024/jaenner/digitalsteuer-2023.html)
- Club Patrimoine (2023): La taxe GAFA va rapporter 800 millions d'euros en 2024. [Club Patrimoine](https://www.clubpatrimoine.com/contenus/la-taxe-gafa-va-rapporter-800-millions-deuros-en-2024) (Sekundärquelle)
- Corriere Comunicazioni (2026): Web tax a 637 milioni (Unimpresa). [Corriere Comunicazioni](https://www.corrierecomunicazioni.it/digital-economy/web-tax-a-637-milioni-limposta-italiana-corre-piu-della-global-minimum-tax/) (Sekundärquelle)
- Osservatorio CPI (2025): Le imposte sui servizi digitali in Italia e in Europa. [Osservatorio CPI](https://osservatoriocpi.unicatt.it/pubblicazioni/2025/le-imposte-sui-servizi-digitali-in-italia-e-in-europa.html)
- UN DESA (2021): Article 12B und Kommentar; PwC (2021) zur Annahme von Artikel 12B (Sekundärquelle). [PwC](https://www.pwc.com/gx/en/tax/newsletters/tax-policy-bulletin/assets/pwc-un-tax-committee-adopts-article-12b.pdf)
- Projekt: `modell/rechnungen/oecd-cbcr/Befund-R6.md`
