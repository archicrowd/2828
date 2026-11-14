#!/usr/bin/env python3
"""Webseite als Fließtext in Word mit nachverfolgten Änderungen (Logbuch v4.85).

Aufruf: python3 seite/werkzeuge/word_korrektur.py ALT.html NEU.html ZIEL.docx [--titel "…"] [--autor "…"]
Liest den sichtbaren Text beider Fassungen der Seite in Lesereihenfolge (Überschriften, Absätze, Listen, Tabellenzeilen, Legenden,
Registerkarten; ohne Navigation, Impressum, Grafiken, Skripte und ausgeblendete Teile), vergleicht Absatz für Absatz und innerhalb geänderter
Absätze Wort für Wort und schreibt eine .docx-Datei, in der jede Änderung als Word-Überarbeitung steht (w:ins / w:del). Die Überarbeitung
ist im Dokument eingeschaltet, sodass weitere Korrekturen ebenfalls nachverfolgt werden.
Grenzen: Text, der erst im Browser durch Skripte entsteht (Rechner, Grafiken), fehlt; Tabellen erscheinen als Zeilen „Zelle | Zelle“.
"""
import argparse
import datetime as dt
import difflib
import re
import zipfile
from xml.sax.saxutils import escape

from bs4 import BeautifulSoup

BLOCK = ["h1", "h2", "h3", "h4", "p", "li", "summary", "tr", "figcaption", "button"]


def bloecke(pfad):
    s = BeautifulSoup(open(pfad, encoding="utf-8").read(), "html.parser")
    for t in s(["script", "style", "svg", "nav", "noscript"]):
        t.decompose()
    for h in s.find_all("h4"):                       # Impressum (Name des Verantwortlichen) nicht übernehmen
        if h.get_text(strip=True).startswith("Impressum"):
            h.parent.decompose()
    for t in s.select("[hidden]"):
        t.decompose()
    out = []
    for el in s.body.find_all(BLOCK + ["div", "span"]):
        if el.name in ("div", "span"):
            # Legenden und Kacheltitel ohne Blockelement: nur Text, der direkt im Element steht
            direkt = "".join(x for x in el.find_all(string=True, recursive=False)).strip()
            if not direkt or el.find_parent(BLOCK):
                continue
            if el.name == "div" and el.find(BLOCK):
                continue
            txt = el.get_text(" ", strip=True)
            art = "p"
        else:
            if el.find_parent(BLOCK) and el.name != "button":
                continue
            if el.name == "button" and el.find_parent(BLOCK):
                continue
            txt = " | ".join(c.get_text(" ", strip=True) for c in el.find_all(["td", "th"])) if el.name == "tr" else el.get_text(" ", strip=True)
            art = el.name if el.name in ("h1", "h2", "h3", "h4") else ("li" if el.name == "li" else "p")
        txt = re.sub(r"\s+", " ", txt).replace(" .", ".").replace(" ,", ",").strip()
        if txt:
            out.append((art, txt))
    # Registerkarten zu einer Zeile zusammenfassen (aufeinanderfolgende Schaltflächen)
    return out


class Doc:
    def __init__(self, autor, datum):
        self.autor, self.datum, self.n, self.teile = autor, datum, 1, []

    def _id(self):
        self.n += 1
        return self.n

    def lauf(self, text, art=None):
        t = escape(text)
        if art == "ins":
            return (f'<w:ins w:id="{self._id()}" w:author="{escape(self.autor)}" w:date="{self.datum}"><w:r><w:t xml:space="preserve">{t}</w:t></w:r></w:ins>')
        if art == "del":
            return (f'<w:del w:id="{self._id()}" w:author="{escape(self.autor)}" w:date="{self.datum}"><w:r><w:delText xml:space="preserve">{t}</w:delText></w:r></w:del>')
        return f'<w:r><w:t xml:space="preserve">{t}</w:t></w:r>'

    def absatz(self, stil, laeufe, marke=None):
        ppr = f'<w:pStyle w:val="{stil}"/>' if stil else ""
        if marke == "ins":
            ppr += f'<w:rPr><w:ins w:id="{self._id()}" w:author="{escape(self.autor)}" w:date="{self.datum}"/></w:rPr>'
        elif marke == "del":
            ppr += f'<w:rPr><w:del w:id="{self._id()}" w:author="{escape(self.autor)}" w:date="{self.datum}"/></w:rPr>'
        self.teile.append(f"<w:p><w:pPr>{ppr}</w:pPr>{''.join(laeufe)}</w:p>")


STIL = {"h1": "Heading1", "h2": "Heading1", "h3": "Heading2", "h4": "Heading3", "li": "ListBullet", "p": None}


def woerter(s):
    return re.findall(r"\S+\s*", s)


def saetze(s):
    return re.findall(r".+?(?:[.!?:](?=\s)|$)\s*", s)


def wortdiff(D, a, b):
    wa, wb, out = woerter(a), woerter(b), []
    for o, p1, p2, q1, q2 in difflib.SequenceMatcher(a=wa, b=wb, autojunk=False).get_opcodes():
        if o == "equal":
            out.append(D.lauf("".join(wb[q1:q2])))
        else:
            if p2 > p1:
                out.append(D.lauf("".join(wa[p1:p2]), "del"))
            if q2 > q1:
                out.append(D.lauf("".join(wb[q1:q2]), "ins"))
    return out


def vergleiche(D, a, b):
    """Satzweise: ähnliche Sätze Wort für Wort, sonst ganzer Satz gestrichen und neu (lesbarer als reine Wortdifferenz)."""
    sa, sb, out = saetze(a), saetze(b), []
    for o, p1, p2, q1, q2 in difflib.SequenceMatcher(a=sa, b=sb, autojunk=False).get_opcodes():
        if o == "equal":
            out.append(D.lauf("".join(sb[q1:q2])))
            continue
        A, B = sa[p1:p2], sb[q1:q2]
        if len(A) == len(B) and all(difflib.SequenceMatcher(a=x, b=y).ratio() > 0.6 for x, y in zip(A, B)):
            for x, y in zip(A, B):
                out += wortdiff(D, x, y)
        else:
            if A:
                t = "".join(A)
                out.append(D.lauf(t if t.endswith(" ") or not B else t + " ", "del"))
            if B:
                out.append(D.lauf("".join(B), "ins"))
    return out


def main():
    a = argparse.ArgumentParser()
    a.add_argument("alt"), a.add_argument("neu"), a.add_argument("ziel")
    a.add_argument("--titel", default="Webseite")
    a.add_argument("--autor", default="Claude")
    a.add_argument("--hinweis", default="")
    x = a.parse_args()
    alt, neu = bloecke(x.alt), bloecke(x.neu)
    D = Doc(x.autor, dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    D.absatz("Title", [D.lauf(x.titel)])
    if x.hinweis:
        D.absatz(None, [D.lauf(x.hinweis)])
    sm = difflib.SequenceMatcher(a=[t for _, t in alt], b=[t for _, t in neu], autojunk=False)
    n_ins = n_del = n_mod = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for art, t in neu[j1:j2]:
                D.absatz(STIL[art], [D.lauf(t)])
            continue
        A, B = alt[i1:i2], neu[j1:j2]
        # geänderte Absätze paarweise nach Ähnlichkeit zuordnen, Rest als ganz gelöscht / ganz neu
        k = 0
        while k < min(len(A), len(B)) and difflib.SequenceMatcher(a=A[k][1], b=B[k][1]).ratio() > 0.35:
            laeufe = vergleiche(D, A[k][1], B[k][1])
            D.absatz(STIL[B[k][0]], laeufe)
            n_mod += 1
            k += 1
        for art, t in A[k:]:
            D.absatz(STIL[art], [D.lauf(t, "del")], marke="del")
            n_del += 1
        for art, t in B[k:]:
            D.absatz(STIL[art], [D.lauf(t, "ins")], marke="ins")
            n_ins += 1
    body = "".join(D.teile)
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + body +
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1418" w:bottom="1134" w:left="1418" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>'
           '</w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:lang w:val="de-DE"/></w:rPr></w:rPrDefault>'
              '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
              '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="23"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr></w:style>'
              '</w:styles>')
    settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:trackRevisions/>'
                '<w:defaultTabStop w:val="708"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/></Relationships>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(x.titel)}</dc:title><dc:creator>Initiative 28:28</dc:creator></cp:coreProperties>')
    with zipfile.ZipFile(x.ziel, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/settings.xml", settings)
        z.writestr("word/_rels/document.xml.rels", drels)
        z.writestr("docProps/core.xml", core)
    print(f"{x.ziel}: {len(neu)} Absätze; geändert {n_mod}, neu {n_ins}, gestrichen {n_del}")


if __name__ == "__main__":
    main()
