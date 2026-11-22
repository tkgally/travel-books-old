#!/usr/bin/env python3
"""Book JSON -> OpenDocument Text (.odt). Deterministic. Standard library only.

  render_odt.py BOOK.json IMAGES_DIR OUT.odt
From Python: render(book, images_dir) -> bytes

The same named styles are used for every book, so documents can be restyled or combined:
  paragraph  Title, Subtitle, Author, Imprint, Edition Note, Heading 1-3, Text Body, First Paragraph,
             Chapter Title, Chapter Summary, Quotation, Verse, Right Aligned, Centered, Caption, Figure, Table Contents,
             Section Break, Footnote, Contents Heading, Contents 1-3
  character  Italic, Bold, Small Caps, Superscript, Subscript
Notes are real footnotes; page starts of the printed book are bookmarks named "page-N". After the title page
a contents list (the same entries as the EPUB's and the website's, render_html.toc_tree) links to bookmarks
"div-ID" (start of a division) and "div-ID-sec-K" (an entry inside a division).
"""
import io, json, os, re, struct, sys, zipfile
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inline, render_html as rh  # noqa: E402

NS = ('xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
      'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
      'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
      'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
      'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
      'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" '
      'xmlns:xlink="http://www.w3.org/1999/xlink" '
      'xmlns:dc="http://purl.org/dc/elements/1.1/" '
      'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" '
      'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
      'office:version="1.3"')


def pstyle(name, display, parent="Standard", para="", text="", nxt=None, cls="text", outline=None):
    nx = f' style:next-style-name="{nxt}"' if nxt else ""
    par = f' style:parent-style-name="{parent}"' if parent else ""
    ol = f' style:default-outline-level="{outline}"' if outline else ""
    return (f'<style:style style:name="{name}" style:display-name="{display}" style:family="paragraph"{par}{nx}{ol} style:class="{cls}">'
            f'<style:paragraph-properties {para}/><style:text-properties {text}/></style:style>')


STYLES = f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles {NS}>
<office:font-face-decls>
<style:font-face style:name="Serif" svg:font-family="'Liberation Serif', 'Times New Roman', Georgia" style:font-family-generic="roman" style:font-pitch="variable"/>
</office:font-face-decls>
<office:styles>
<style:default-style style:family="paragraph">
<style:paragraph-properties fo:hyphenation-ladder-count="no-limit" style:writing-mode="lr-tb"/>
<style:text-properties style:font-name="Serif" fo:font-size="11pt" fo:language="en" fo:country="GB" fo:hyphenate="true" fo:hyphenation-remain-char-count="2" fo:hyphenation-push-char-count="2"/>
</style:default-style>
<style:style style:name="Standard" style:family="paragraph" style:class="text"><style:paragraph-properties fo:line-height="130%" fo:orphans="2" fo:widows="2"/></style:style>
{pstyle("Text_20_body", "Text Body", para='fo:text-indent="0.6cm" fo:text-align="justify" fo:margin-top="0cm" fo:margin-bottom="0cm"')}
{pstyle("First_20_Paragraph", "First Paragraph", "Text_20_body", para='fo:text-indent="0cm"', nxt="Text_20_body")}
{pstyle("Heading_20_1", "Heading 1", para='fo:text-align="center" fo:margin-top="2cm" fo:margin-bottom="0.8cm" fo:break-before="page" fo:keep-with-next="always"', text='fo:font-size="16pt" fo:hyphenate="false"', nxt="First_20_Paragraph", outline=1)}
{pstyle("Heading_20_2", "Heading 2", para='fo:text-align="center" fo:margin-top="0.8cm" fo:margin-bottom="0.5cm" fo:keep-with-next="always"', text='fo:font-size="13pt" fo:hyphenate="false"', nxt="First_20_Paragraph", outline=2)}
{pstyle("Heading_20_3", "Heading 3", para='fo:text-align="center" fo:margin-top="0.6cm" fo:margin-bottom="0.3cm" fo:keep-with-next="always"', text='fo:font-size="11.5pt" fo:font-style="italic" fo:hyphenate="false"', nxt="First_20_Paragraph", outline=3)}
{pstyle("Added_20_Heading", "Added Heading", para='fo:text-align="center" fo:margin-top="1.2cm" fo:margin-bottom="0.6cm" fo:break-before="page" fo:keep-with-next="always"', text='fo:font-size="11pt" fo:font-style="italic" fo:hyphenate="false"', nxt="Text_20_body", outline=2)}
{pstyle("Editor_20_Figure", "Editor Figure", parent="Figure", para='fo:text-align="center" fo:break-before="page"')}
{pstyle("Title_20_Page_20_Verso", "Title Page Verso", para='fo:text-align="center" fo:break-before="page"')}
{pstyle("Chapter_20_Title", "Chapter Title", para='fo:text-align="center" fo:margin-bottom="0.6cm" fo:keep-with-next="always"', text='fo:font-size="11pt" fo:hyphenate="false"', nxt="First_20_Paragraph")}
{pstyle("Chapter_20_Summary", "Chapter Summary", para='fo:text-align="start" fo:margin-left="1cm" fo:margin-right="1cm" fo:margin-bottom="0.6cm" fo:keep-with-next="always"', text='fo:font-size="10pt" fo:hyphenate="false"', nxt="First_20_Paragraph")}
{pstyle("Quotation", "Quotation", para='fo:text-align="justify" fo:margin-left="1cm" fo:margin-right="1cm" fo:margin-top="0.2cm" fo:margin-bottom="0.2cm"', text='fo:font-size="10.5pt"')}
{pstyle("Verse", "Verse", para='fo:text-align="start" fo:margin-left="2cm" fo:text-indent="-0.5cm" fo:margin-top="0cm" fo:margin-bottom="0cm"', text='fo:font-size="10.5pt" fo:hyphenate="false"')}
{pstyle("Right_20_Aligned", "Right Aligned", para='fo:text-align="end" fo:margin-top="0.1cm"')}
{pstyle("Centered", "Centered", para='fo:text-align="center" fo:margin-top="0.2cm" fo:margin-bottom="0.2cm"')}
{pstyle("Figure", "Figure", para='fo:text-align="center" fo:margin-top="0.5cm" fo:keep-with-next="always"')}
{pstyle("Caption", "Caption", para='fo:text-align="center" fo:margin-bottom="0.5cm"', text='fo:font-size="9.5pt"')}
{pstyle("Table_20_Contents", "Table Contents", para='fo:text-align="start"', text='fo:font-size="10pt"')}
{pstyle("Section_20_Break", "Section Break", para='fo:text-align="center" fo:margin-top="0.3cm" fo:margin-bottom="0.3cm"', nxt="First_20_Paragraph")}
{pstyle("Contents_20_Heading", "Contents Heading", para='fo:text-align="center" fo:margin-top="2cm" fo:margin-bottom="0.8cm" fo:break-before="page"', text='fo:font-size="16pt" fo:hyphenate="false"', cls="index")}
{pstyle("Contents_20_1", "Contents 1", para='fo:text-align="start" fo:margin-left="0.6cm" fo:text-indent="-0.6cm" fo:margin-top="0.15cm"', text='fo:hyphenate="false"', cls="index")}
{pstyle("Contents_20_2", "Contents 2", "Contents_20_1", para='fo:margin-left="1.4cm" fo:margin-top="0.05cm"', cls="index")}
{pstyle("Contents_20_3", "Contents 3", "Contents_20_1", para='fo:margin-left="2.2cm" fo:margin-top="0cm"', text='fo:font-size="10pt"', cls="index")}
{pstyle("Footnote", "Footnote", para='fo:text-align="justify" fo:margin-left="0.4cm" fo:text-indent="-0.4cm" fo:line-height="115%"', text='fo:font-size="9pt"', cls="extra")}
{pstyle("Title", "Title", para='fo:text-align="center" fo:margin-top="4cm" fo:margin-bottom="0.6cm"', text='fo:font-size="22pt" fo:hyphenate="false"', cls="chapter")}
{pstyle("Subtitle", "Subtitle", para='fo:text-align="center" fo:margin-bottom="1.5cm"', text='fo:font-size="13pt" fo:hyphenate="false"', cls="chapter")}
{pstyle("Author", "Author", para='fo:text-align="center" fo:margin-bottom="1.5cm"', text='fo:font-size="14pt"')}
{pstyle("Imprint", "Imprint", para='fo:text-align="center" fo:margin-bottom="3cm"')}
{pstyle("Edition_20_Note", "Edition Note", para='fo:text-align="start" fo:margin-bottom="0.2cm"', text='fo:font-size="9pt"')}
<style:style style:name="Italic" style:family="text"><style:text-properties fo:font-style="italic"/></style:style>
<style:style style:name="Bold" style:family="text"><style:text-properties fo:font-weight="bold"/></style:style>
<style:style style:name="Small_20_Caps" style:display-name="Small Caps" style:family="text"><style:text-properties fo:font-variant="small-caps"/></style:style>
<style:style style:name="Superscript" style:family="text"><style:text-properties style:text-position="super 58%"/></style:style>
<style:style style:name="Subscript" style:family="text"><style:text-properties style:text-position="sub 58%"/></style:style>
<style:style style:name="Footnote_20_anchor" style:display-name="Footnote anchor" style:family="text"><style:text-properties style:text-position="super 58%"/></style:style>
<style:style style:name="Graphics" style:family="graphic"><style:graphic-properties text:anchor-type="as-char" style:vertical-pos="top" style:vertical-rel="baseline"/></style:style>
<text:notes-configuration text:note-class="footnote" text:citation-body-style-name="Footnote_20_anchor" text:default-style-name="Footnote" style:num-format="1" text:start-numbering-at="chapter" text:footnotes-position="page"/>
</office:styles>
<office:automatic-styles>
<style:page-layout style:name="pm1"><style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm" fo:margin-top="2.5cm" fo:margin-bottom="2.5cm" fo:margin-left="3.5cm" fo:margin-right="3.5cm"/>
<style:footer-style><style:header-footer-properties fo:min-height="0.8cm" fo:margin-top="0.5cm"/></style:footer-style></style:page-layout>
<style:style style:name="FooterP" style:family="paragraph"><style:paragraph-properties fo:text-align="center"/><style:text-properties fo:font-size="9pt"/></style:style>
</office:automatic-styles>
<office:master-styles>
<style:master-page style:name="Standard" style:page-layout-name="pm1"><style:footer><text:p text:style-name="FooterP"><text:page-number text:select-page="current"/></text:p></style:footer></style:master-page>
</office:master-styles>
</office:document-styles>
"""
CHAR = {"i": "Italic", "b": "Bold", "sc": "Small_20_Caps", "sup": "Superscript", "sub": "Subscript"}
MEDIA = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def image_size(data):
    """(width, height) in pixels of a PNG or JPEG."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return 600, 800


class Odt:
    def __init__(self, book, images_dir):
        self.book, self.images_dir = book, images_dir
        self.notes, self.pics, self.seen_pg, self.nfig = {}, {}, set(), 0
        self.seen_ref = set()
        self.pages = set()
        for d in rh.reading_divisions(book):
            for p in rh.page_starts(d):
                if p["n"]:
                    self.pages.add(rh.anchor(p["n"]))

    def pb(self, n):
        a = rh.anchor(n)
        if not a or a in self.seen_pg:
            return ""
        self.seen_pg.add(a)
        return f'<text:bookmark text:name="page-{a}"/>'

    def text(self, s):
        s = escape(s)
        s = re.sub(r" {2,}", lambda m: f' <text:s text:c="{len(m.group(0)) - 1}"/>', s)
        return s

    def inline(self, s, in_note=False):
        out, closers = [], []
        for t in inline.tokens(inline.drop_sides(s)):
            if t[0] == "text":
                out.append(self.text(t[1]))
            elif t[0] == "empty" and t[1] == "pb":
                out.append(self.pb(t[2].get("n", "")))
            elif t[0] == "open":
                name, a = t[1], t[2]
                close = "</text:span>"
                if name in CHAR:
                    out.append(f'<text:span text:style-name="{CHAR[name]}">')
                elif name == "noteref":
                    n = self.notes.get(a.get("to"))
                    if n is not None and not in_note and n["id"] in self.seen_ref:
                        # a second reference to a note already placed ([[fnref * again]]): a cross-reference to it
                        out.append(f'<text:span text:style-name="Superscript"><text:note-ref text:note-class="footnote" '
                                   f'text:reference-format="text" text:ref-name={quoteattr(n["id"])}>')
                        close = "</text:note-ref></text:span>"
                    elif n is None or in_note:
                        out.append('<text:span text:style-name="Superscript">')
                    else:
                        self.seen_ref.add(n["id"])
                        mark = n["mark"]
                        label = "" if mark.isdigit() else f' text:label={quoteattr(mark)}'
                        out.append(f'<text:note text:id="{n["id"]}" text:note-class="footnote"><text:note-citation{label}>{escape(mark)}</text:note-citation>'
                                   f'<text:note-body><text:p text:style-name="Footnote">{self.inline(n["text"], True)}</text:p></text:note-body></text:note>'
                                   '<text:span text:style-name="Hidden">')
                        close = "</text:span>"
                elif name == "pageref":
                    tgt = rh.anchor(a.get("n", ""))
                    if tgt in self.pages:
                        out.append(f'<text:a xlink:type="simple" xlink:href="#page-{tgt}">'); close = "</text:a>"
                    else:
                        out.append(""); close = ""
                else:
                    out.append(""); close = ""
                closers.append(close)
            elif t[0] == "close":
                out.append(closers.pop() if closers else "")
        s = "".join(out)
        # the mark text inside a noteref is already shown by the note citation
        return re.sub(r'<text:span text:style-name="Hidden">.*?</text:span>', "", s)

    def p(self, style, content):
        return f'<text:p text:style-name="{style}">{content}</text:p>'

    def frame(self, b):
        """An image block (or an editor's picture) as a frame, or a bracketed description if the file is missing."""
        f = os.path.basename(b["src"])
        path = os.path.join(self.images_dir or "", f)
        if not os.path.exists(path):
            return self.text("[Illustration: " + b["alt"] + "]")
        data = open(path, "rb").read()
        self.pics[f] = data
        w, h = image_size(data)
        scale = min(14.0 / w, 19.0 / h, 2.54 / 110)
        if b.get("ornament"):            # a decorative head- or tail-piece: small
            scale = min(scale, 5.0 / w, 2.5 / h)
        self.nfig += 1
        return (f'<draw:frame draw:style-name="Graphics" draw:name="Figure{self.nfig}" text:anchor-type="as-char" '
                f'svg:width="{w * scale:.2f}cm" svg:height="{h * scale:.2f}cm">'
                f'<draw:image xlink:href="Pictures/{f}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>'
                f'<svg:title>{escape(b["alt"])}</svg:title></draw:frame>')

    def division(self, d):
        d = rh.roman_long_italics(d)
        self.notes = {n["id"]: n for n in d["notes"]}
        out, prev = [], "paragraph" if d.get("runs_on") else None
        marks = {i: f'div-{d["id"]}-{v}' for i, v in rh.section_targets(d).items()}
        tp, leaf0 = d["kind"] == "titlepage", None
        if d.get("added"):        # the title of a section made for this edition: a heading that is not the book's
            out.append(f'<text:h text:style-name="Added_20_Heading" text:outline-level="2">{self.text(d["added"])}</text:h>')
        if rh.editor_figures(self.book, d):    # the editor's pictures, before the narrative (render_html.editor_figures)
            for e in self.book["editor_images"]:
                out.append(self.p("Editor_20_Figure", self.frame(e)))
                out.append(self.p("Edition_20_Note", self.text(e["caption"])))
        for bi, b in enumerate(d["blocks"]):
            n0 = len(out)
            t = b["type"]
            if tp and leaf0 is not None and b["leaf"] > leaf0:       # the verso of the title page: a new page
                out.append(self.p("Title_20_Page_20_Verso", ""))
                n0 = len(out)
            leaf0 = max(leaf0 or "", b["leaf"])
            pbs = "".join(self.pb(x["n"]) for x in b.get("pb", []))
            if t == "heading":
                lv = b["level"]
                out.append(f'<text:h text:style-name="Heading_20_{lv}" text:outline-level="{lv}">{pbs}{self.inline(b["text"])}</text:h>')
            elif t == "paragraph":
                if b.get("role") == "subtitle":
                    st = "Chapter_20_Title" if rh.short_subtitle(b["text"]) else "Chapter_20_Summary"
                elif b.get("align") == "right":
                    st = "Right_20_Aligned"
                elif b.get("align") == "center" or tp:
                    st = "Centered"
                elif prev in (None, "heading", "break", "subtitle", "table", "quote", "verse"):
                    st = "First_20_Paragraph"
                else:
                    st = "Text_20_body"
                out.append(self.p(st, pbs + self.inline(b["text"])))
            elif t == "quote":
                for i, q in enumerate(b["paragraphs"]):
                    st = {"right": "QuoteRight", "center": "QuoteCenter"}.get(q.get("align"), "Quotation")
                    out.append(self.p(st, (pbs if i == 0 else "") + self.inline(q["text"])))
            elif t == "verse":
                for i, stz in enumerate(b["stanzas"]):
                    for j, line in enumerate(stz):
                        st = "VerseFirst" if j == 0 and i > 0 else "Verse"
                        out.append(self.p(st, (pbs if i == 0 and j == 0 else "") + self.inline(line)))
                out.append(self.p("VerseEnd", ""))
            elif t == "image":
                out.append(self.p("Figure", pbs + self.frame(b)))
                if b.get("caption"):
                    out.append(self.p("Caption", self.inline(b["caption"])))
            elif t == "table":
                cols = max(len(r) for r in b["rows"])
                self.ntab = getattr(self, "ntab", 0) + 1
                rows = "".join("<table:table-row>" + "".join(
                    f'<table:table-cell office:value-type="string">{self.p("Table_20_Contents", self.inline(c))}</table:table-cell>'
                    for c in r + [""] * (cols - len(r))) + "</table:table-row>" for r in b["rows"])
                out.append(f'<table:table table:name="Table{self.ntab}"><table:table-column table:number-columns-repeated="{cols}"/>{rows}</table:table>')
            elif t == "break":
                out.append(self.p("Section_20_Break", pbs + "* * *"))
            names = ([f'div-{d["id"]}'] if bi == 0 else []) + ([marks[bi]] if bi in marks else [])
            if names and len(out) > n0:
                bm = "".join(f'<text:bookmark text:name="{x}"/>' for x in names)
                for j in range(0 if bi == 0 else n0, len(out)):
                    new = re.sub(r"<text:(p|h)\b[^>]*>", lambda m: m.group(0) + bm, out[j], count=1)
                    if new != out[j]:
                        out[j] = new
                        break
            if t != "image":      # as in render_html: a paragraph after a picture is indented
                prev = "subtitle" if b.get("role") == "subtitle" else t
        return "\n".join(out)

    def contents(self):
        """The contents list after the title page: the same entries as the EPUB's navigation."""
        out = [self.p("Contents_20_Heading", "Contents")]

        def walk(nodes, level):
            for title, did, frag, kids in nodes:
                target = f"div-{did}" + (f"-{frag}" if frag else "")
                out.append(self.p(f"Contents_20_{min(level, 3)}",
                                  f'<text:a xlink:type="simple" xlink:href="#{target}">{self.text(title)}</text:a>'))
                walk(kids, level + 1)
        walk(rh.toc_tree(self.book), 1)
        return "\n".join(out)

    def title_page(self, transcribed=False):
        """The note about this edition; with transcribed=False (the book's title page is not in the text) under
        a title page made from the metadata."""
        b = self.book
        src = b.get("source", {})
        out = []
        if not transcribed:
            out.append(self.p("Title", self.text(b["title"])))
            if b.get("subtitle"):
                out.append(self.p("Subtitle", self.text(b["subtitle"])))
            out.append(self.p("Author", self.text(rh.authors_text(b))))
            out.append(self.p("Imprint", self.text(", ".join(x for x in (b.get("place"), b.get("publisher"), str(b.get("year", ""))) if x))))
        else:
            out.append(self.p("Title_20_Page_20_Verso", ""))
        out.append(self.p("Edition_20_Note", self.text(f'Travel Books edition, version {b["version"]}, {b["date"]}.')))
        if src.get("ia_identifier"):
            url = f'https://archive.org/details/{src["ia_identifier"]}'
            out.append(self.p("Edition_20_Note", f'Transcribed from the scan at the Internet Archive: <text:a xlink:type="simple" xlink:href="{url}">{url}</text:a>'))
        out.append(self.p("Edition_20_Note", self.text("The spelling and punctuation of the original are kept; printer’s errors that were corrected are listed on the book’s page at the project site. This transcription is in the public domain (CC0 1.0).")))
        return "\n".join(out)

    def content(self):
        rd = rh.reading_divisions(self.book)
        if rd and rd[0]["kind"] == "titlepage":     # the book's own title page, then the note on this edition
            body = [self.division(rd[0]), self.title_page(True), self.contents()] + [self.division(d) for d in rd[1:]]
        else:
            body = [self.title_page(), self.contents()] + [self.division(d) for d in rd]
        auto = """<style:style style:name="QuoteRight" style:family="paragraph" style:parent-style-name="Quotation"><style:paragraph-properties fo:text-align="end"/></style:style>
<style:style style:name="QuoteCenter" style:family="paragraph" style:parent-style-name="Quotation"><style:paragraph-properties fo:text-align="center"/></style:style>
<style:style style:name="VerseFirst" style:family="paragraph" style:parent-style-name="Verse"><style:paragraph-properties fo:margin-top="0.3cm"/></style:style>
<style:style style:name="VerseEnd" style:family="paragraph" style:parent-style-name="Verse"><style:text-properties fo:font-size="4pt"/></style:style>"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-content {NS}>
<office:automatic-styles>
{auto}
</office:automatic-styles>
<office:body><office:text>
{chr(10).join(body)}
</office:text></office:body>
</office:document-content>
"""


def render(book, images_dir):
    o = Odt(book, images_dir)
    content = o.content()
    meta = f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta {NS}><office:meta>
<dc:title>{escape(book["title"])}</dc:title>
<meta:initial-creator>{escape(rh.authors_text(book))}</meta:initial-creator>
<dc:creator>{escape(rh.authors_text(book))}</dc:creator>
<dc:date>{book["date"]}T00:00:00</dc:date>
<dc:language>en</dc:language>
<dc:description>Travel Books edition, version {book["version"]}. Public domain (CC0 1.0).</dc:description>
</office:meta></office:document-meta>
"""
    man = ['<manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text"/>',
           '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>',
           '<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>',
           '<manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>']
    for f in sorted(o.pics):
        man.append(f'<manifest:file-entry manifest:full-path="Pictures/{f}" manifest:media-type="{MEDIA.get(os.path.splitext(f)[1].lower(), "image/jpeg")}"/>')
    manifest = ('<?xml version="1.0" encoding="UTF-8"?>\n<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">\n'
                + "\n".join(man) + "\n</manifest:manifest>\n")
    buf = io.BytesIO()
    stamp = (1980, 1, 1, 0, 0, 0)

    def put(zf, name, data, method=zipfile.ZIP_DEFLATED):
        zi = zipfile.ZipInfo(name, stamp)
        zi.compress_type = method
        zi.external_attr = 0o644 << 16
        zf.writestr(zi, data if isinstance(data, bytes) else data.encode("utf-8"))
    with zipfile.ZipFile(buf, "w") as zf:
        put(zf, "mimetype", "application/vnd.oasis.opendocument.text", zipfile.ZIP_STORED)
        put(zf, "content.xml", content)
        put(zf, "styles.xml", STYLES)
        put(zf, "meta.xml", meta)
        for f in sorted(o.pics):
            put(zf, "Pictures/" + f, o.pics[f], zipfile.ZIP_STORED)
        put(zf, "META-INF/manifest.xml", manifest)
    return buf.getvalue()


if __name__ == "__main__":
    book = json.load(open(sys.argv[1], encoding="utf-8"))
    open(sys.argv[3], "wb").write(render(book, sys.argv[2]))
    print("wrote", sys.argv[3])
