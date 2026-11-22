#!/usr/bin/env python3
"""Book JSON -> EPUB 3. Deterministic: the same JSON and images give the same bytes.

  render_epub.py BOOK.json IMAGES_DIR OUT.epub
From Python: render(book, images_dir) -> bytes
"""
import io, json, os, re, sys, uuid, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_html as rh  # noqa: E402

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "assets", "book.css"), encoding="utf-8").read()

XHTML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head><meta charset="UTF-8"/><title>{title}</title><link rel="stylesheet" type="text/css" href="../style/book.css"/></head>
<body class="book{battr}">
{body}
</body>
</html>
"""
MEDIA = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".svg": "image/svg+xml"}


def title_page(book, transcribed=False):
    """The page about this edition. With transcribed=True the book's own title page is in the reading text (it
    is the page before this one: Tom, 2026-11-22) and this page has the note only; otherwise it is also a title
    page made from the metadata."""
    e = rh.esc
    src = book.get("source", {})
    lines = []
    if not transcribed:
        lines.append(f'<h1>{e(book["title"])}</h1>')
        if book.get("subtitle"):
            lines.append(f'<p class="tp-sub">{e(book["subtitle"])}</p>')
        lines.append(f'<p class="tp-author">{e(rh.authors_text(book))}</p>')
        imprint = ", ".join(x for x in (book.get("place"), book.get("publisher"), str(book.get("year", ""))) if x)
        lines.append(f'<p class="tp-imprint">{e(imprint)}</p>')
    note = [f'Travel Books edition, version {book["version"]}, {book["date"]}.']
    if src.get("ia_identifier"):
        note.append(f'Transcribed from the scan at the Internet Archive: <a href="https://archive.org/details/{src["ia_identifier"]}">archive.org/details/{e(src["ia_identifier"])}</a>.')
    note.append("The spelling and punctuation of the original are kept; printer’s errors that were corrected are listed on the book’s page at the project site. "
                "This transcription is in the public domain (CC0 1.0).")
    lines.append('<p class="tp-note">' + " ".join(note) + "</p>")
    return '<section class="titlepage">' + "\n".join(lines) + "</section>"


def render(book, images_dir):
    e = rh.esc
    names = rh.file_names(book, ".xhtml")
    ctx = rh.Ctx(book, "epub", names)
    files, manifest, spine = {}, [], []
    cover = next((f for f in ("cover.jpg", "cover.png") if images_dir and os.path.exists(os.path.join(images_dir, f))), None)
    if cover:
        files["images/" + cover] = open(os.path.join(images_dir, cover), "rb").read()
        manifest.append(f'<item id="cover-image" href="images/{cover}" media-type="{MEDIA[os.path.splitext(cover)[1]]}" properties="cover-image"/>')
        files["text/cover.xhtml"] = XHTML.format(title=e(book["title"]), battr=' cover-page',
            body=f'<div class="cover-page"><img src="../images/{cover}" alt="Cover of the book"/></div>')
        manifest.append('<item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>')
        spine.append('<itemref idref="cover"/>')
    rd = rh.reading_divisions(book)
    transcribed = bool(rd) and rd[0]["kind"] == "titlepage"

    def edition_pages():
        """The page about this edition and the contents: after the book's title page, or first if it has none."""
        files["text/title.xhtml"] = XHTML.format(title="This edition" if transcribed else e(book["title"]), battr="",
                                                 body=title_page(book, transcribed))
        manifest.append('<item id="title" href="text/title.xhtml" media-type="application/xhtml+xml"/>')
        spine.append('<itemref idref="title"/>')
        manifest.append('<item id="nav" href="text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
        spine.append('<itemref idref="nav"/>')
    if not transcribed:
        edition_pages()
    used = set()
    for i, d in enumerate(rd):
        body = ctx.blocks(d).replace('src="images/', 'src="../images/')
        used.update(re.findall(r'src="\.\./images/([^"]+)"', body))
        name = names[d["id"]]
        battr = ' part' if d["kind"] == "part" else ""
        etype = {"part": "part", "titlepage": "titlepage"}.get(d["kind"], "chapter")
        # the title of a section made for this edition (render_html.split_division) stands outside the book's text
        added = f'<h2 class="added">{e(d["added"])}</h2>\n' if d.get("added") else ""
        added += rh.editor_figures(book, d, "../")
        used.update(re.findall(r'src="\.\./images/([^"]+)"', added))
        files["text/" + name] = XHTML.format(title=e(d["title"]), battr=battr, body=f'{added}<section epub:type="{etype}">\n{body}\n</section>')
        manifest.append(f'<item id="c{name[:-6]}" href="text/{name}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="c{name[:-6]}"/>')
        if i == 0 and transcribed:
            edition_pages()
    for f in sorted(used):
        if not images_dir or not os.path.exists(os.path.join(images_dir, f)):
            continue                      # compile_book has warned; preflight fails on the warning
        files["images/" + f] = open(os.path.join(images_dir, f), "rb").read()
        manifest.append(f'<item id="img-{re.sub(r"[^A-Za-z0-9]", "-", f)}" href="images/{f}" media-type="{MEDIA[os.path.splitext(f)[1].lower()]}"/>')
    pages = "".join(f'<li><a href="{tgt}">{e(n)}</a></li>' for n, tgt in ctx.targets.items())
    pagelist = f'<nav epub:type="page-list" id="page-list" hidden=""><h2>Pages of the printed book</h2><ol>{pages}</ol></nav>' if pages else ""
    files["text/nav.xhtml"] = XHTML.format(title="Contents", battr="",
        body=f'<nav epub:type="toc" id="toc"><h2>Contents</h2>{rh.nav_list(book, names)}</nav>{pagelist}')
    files["style/book.css"] = CSS
    manifest.append('<item id="style" href="style/book.css" media-type="text/css"/>')
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, "travel-books/" + book["id"]))
    src = book.get("source", {})
    source = f'<dc:source>https://archive.org/details/{e(src["ia_identifier"])}</dc:source>' if src.get("ia_identifier") else ""
    creators = "\n".join(f'<dc:{"contributor" if a.get("role") == "editor" else "creator"}>{e(a["name"])}'
                         f'</dc:{"contributor" if a.get("role") == "editor" else "creator"}>' for a in book.get("authors", []))
    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" xml:lang="en" unique-identifier="pub-id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="pub-id">urn:uuid:{uid}</dc:identifier>
<dc:title>{e(book['title'])}</dc:title>
<dc:language>en</dc:language>
{creators}
<dc:date>{book.get('year', '')}</dc:date>
<dc:publisher>Travel Books</dc:publisher>
<dc:rights>Public domain. Transcription dedicated to the public domain under CC0 1.0.</dc:rights>
{source}
<meta property="dcterms:modified">{book['date']}T00:00:00Z</meta>
{'<meta name="cover" content="cover-image"/>' if cover else ''}
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine>
{chr(10).join(spine)}
</spine>
</package>
"""
    files["content.opf"] = opf
    container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""
    buf = io.BytesIO()
    stamp = (1980, 1, 1, 0, 0, 0)

    def put(zf, name, data, method):
        zi = zipfile.ZipInfo(name, stamp)
        zi.compress_type = method
        zi.external_attr = 0o644 << 16
        zf.writestr(zi, data if isinstance(data, bytes) else data.encode("utf-8"))
    with zipfile.ZipFile(buf, "w") as zf:
        put(zf, "mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        put(zf, "META-INF/container.xml", container, zipfile.ZIP_DEFLATED)
        for path in sorted(files):
            put(zf, "OEBPS/" + path, files[path], zipfile.ZIP_DEFLATED)
    return buf.getvalue()


if __name__ == "__main__":
    book = json.load(open(sys.argv[1], encoding="utf-8"))
    open(sys.argv[3], "wb").write(render(book, sys.argv[2]))
    print("wrote", sys.argv[3])
