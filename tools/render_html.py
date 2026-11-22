#!/usr/bin/env python3
"""Book JSON -> XHTML-compatible HTML for the website and for the EPUB (shared block renderer).

Used by build_site.py and render_epub.py. Nothing here reads page files: the book JSON is the only input.
"""
import html, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compile_book, inline  # noqa: E402


SHORT_SUBTITLE = 80


def short_subtitle(text):
    """A chapter title or short summary (one line) is centred under the heading; a long list of topics is not."""
    return len(inline.plain(text)) <= SHORT_SUBTITLE

esc = lambda s: html.escape(s, quote=False)
attr = lambda s: html.escape(s, quote=True)


def whole_reading_divisions(book):
    """The divisions of the JSON that are in the reading editions, each whole."""
    return [d for d in book["divisions"] if d.get("reading")]


def reading_divisions(book):
    """The pages of the reading editions (a file each on the website and in the EPUB, a page break in the ODT):
    the reading divisions of the JSON, and for a division with "split" the parts it is divided into at its
    `sections` (Tom, 2026-11-22: a long text without chapters is read in sections, each with a title)."""
    out = []
    for d in whole_reading_divisions(book):
        out += split_division(d)
    return out


def split_division(d):
    """The parts of a division with "split": one for each of its `sections`, and one before them if the division
    has text before its first section. Each is a division of its own for the renderers: `id` (the division's id
    for the first, then id-2, id-3 …), `title` (the section's), its blocks and the notes they refer to, `of` (the
    division's id); `added` is the section's title when it is the editor's and the part does not open with the
    division's own heading (the renderers show it as a heading that is not the book's); `runs_on` says that the
    part does not begin the division, so its first paragraph is indented like any other."""
    secs = d.get("sections") or []
    if not d.get("split") or not secs:
        return [d]
    blocks = d["blocks"]
    lead = blocks[:secs[0]["block"]]
    has_lead = any(b["type"] not in ("heading", "image", "break") and b.get("role") != "subtitle" for b in lead)
    spans = [(0, secs[0]["block"], None)] if has_lead else []
    for k, x in enumerate(secs):
        start = 0 if k == 0 and not has_lead else x["block"]
        end = secs[k + 1]["block"] if k + 1 < len(secs) else len(blocks)
        spans.append((start, end, x))
    out, left = [], list(d["notes"])
    for k, (a, b, x) in enumerate(spans):
        part = blocks[a:b]
        refs = set(re.findall(r'<noteref to="([^"]+)"', " ".join(s for blk in part for s in strings(blk))))
        notes = [n for n in left if n["id"] in refs] if k + 1 < len(spans) else left
        left = [n for n in left if n not in notes]
        u = {key: v for key, v in d.items() if key not in ("sections", "split", "toc_title", "blocks", "notes")}
        u.update(id=d["id"] if k == 0 else f'{d["id"]}-{k + 1}', title=x["title"] if x else d["title"], blocks=part, notes=notes,
                 of=d["id"], first_leaf=part[0]["leaf"] if part else d["first_leaf"])
        if k:
            u["runs_on"] = True
            if x and x.get("editor", True) and not (part and part[0]["type"] == "heading"):
                u["added"] = x["title"]
        out.append(u)
    return out


def body_start(book):
    """The page of the reading editions where the narrative begins (the picture on the book's page links to it;
    Tom, 2026-11-22): the first chapter, not the title page, a dedication, a preface or an introduction.
    book.json "body_start": "p0041" names it (by its first leaf) when the first division of kind "chapter" is
    not the one."""
    rd = reading_divisions(book)
    want = book.get("body_start")
    for test in ((lambda d: d["first_leaf"] == want), (lambda d: d["kind"] == "chapter"),
                 (lambda d: d["kind"] in ("part", "introduction")), (lambda d: d["kind"] != "titlepage")):
        hit = next((d for d in rd if test(d)), None)
        if hit:
            return hit
    return rd[0] if rd else None


def editor_figures(book, d, prefix=""):
    """The pictures the editor added (book.json "editor_images"), as HTML, for the page `d` of the reading editions
    where the narrative begins (body_start); "" for any other page. The renderers put them before the book's own
    text (outside <article> on the web, outside <section> in the EPUB): they and their captions are not the book's."""
    eds = book.get("editor_images") or []
    start = body_start(book)
    if not eds or start is None or d["id"] != start["id"]:
        return ""
    return "".join(f'<figure class="editor"><img src="{attr(prefix + e["src"])}" alt="{attr(e["alt"])}"/>'
                   f'<figcaption>{esc(e["caption"])}</figcaption></figure>\n' for e in eds)


def file_names(book, ext):
    """division id -> file name, for the divisions of the reading editions."""
    return {d["id"]: f"{i:02d}{ext}" for i, d in enumerate(reading_divisions(book), 1)}


def page_targets(book, names):
    """printed page number -> 'file#pg-N' for pages that start inside the reading editions (first occurrence wins)."""
    where = {}
    for d in reading_divisions(book):
        for n in page_starts(d):
            if n["n"] and n["n"] not in where:
                where[n["n"]] = f"{names[d['id']]}#pg-{anchor(n['n'])}"
    return where


def anchor(n):
    return re.sub(r"[^0-9A-Za-z]", "", n)


strings = compile_book.strings


def page_starts(div):
    out = []
    for b in div["blocks"]:
        out += b.get("pb", [])
        for s in strings(b):
            out += [{"n": html.unescape(n), "leaf": l} for n, l in re.findall(r'<pb n="([^"]*)" leaf="([^"]+)"/>', s)]
    return out


LONG_ITALIC_WORDS = 30     # a wholly italic paragraph or quotation of at least this many words is set in roman
LONG_ITALIC_LINES = 4      # a wholly italic piece of verse of at least this many lines likewise
ITALIC_SHARE = 0.9


def roman_long_italics(div):
    """A copy of a division for the reading editions (notes/style.md §Editions): long passages printed in italic
    — whole paragraphs, whole poems, chapter summaries, whole tables — are set in roman, and words that
    the print set in roman inside them, for contrast, in italic. The JSON keeps the italics as printed."""
    def stats(strs):
        it = tot = words = 0
        for s in strs:
            a, b, c = inline.italic_share(s)
            it, tot, words = it + a, tot + b, words + c
        return (it / tot if tot else 0), words

    def long_(strs, min_words):
        share, words = stats(strs)
        return share >= ITALIC_SHARE and words >= min_words
    out = dict(div)
    blocks = []
    for b in div["blocks"]:
        b = dict(b)
        t = b["type"]
        if t == "paragraph":
            if long_([b["text"]], 2 if b.get("role") == "subtitle" else LONG_ITALIC_WORDS):
                b["text"] = inline.swap_italics(b["text"])
        elif t == "quote":
            whole = long_([p["text"] for p in b["paragraphs"]], LONG_ITALIC_WORDS)
            b["paragraphs"] = [dict(p, text=inline.swap_italics(p["text"])) if whole or long_([p["text"]], LONG_ITALIC_WORDS) else p
                               for p in b["paragraphs"]]
        elif t == "verse":
            lines = [x for s in b["stanzas"] for x in s]
            if len(lines) >= LONG_ITALIC_LINES and long_(lines, 1):
                b["stanzas"] = [[inline.swap_italics(x) for x in s] for s in b["stanzas"]]
        elif t == "table":
            cells = [c for r in b["rows"] for c in r]
            if len(b["rows"]) >= 2 and long_(cells, 1):
                b["rows"] = [[inline.swap_italics(c) for c in r] for r in b["rows"]]
        blocks.append(b)
    out["blocks"] = blocks
    out["notes"] = [dict(n, text=inline.swap_italics(n["text"])) if long_([n["text"]], LONG_ITALIC_WORDS) else n for n in div["notes"]]
    return out


AR = "\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff\ufb50-\ufdff\ufe70-\ufeff"
SCRIPT_RUNS = [(re.compile(f"[{AR}](?:[{AR}\\s\u200c\u200d]*[{AR}])?"), "ar"),
               (re.compile("[\u0590-\u05ff](?:[\u0590-\u05ff\\s]*[\u0590-\u05ff])?"), "he")]


KANA = "\u3040-\u30ff"
HAN = "\u3005\u3007\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff" + KANA
HAN_RUN = re.compile(f"[{HAN}](?:[{HAN}\\s\u3000-\u303f]*[{HAN}])?")


def tag_scripts(s):
    """Words in Arabic or Hebrew script get lang and dir="rtl", so that a screen reader picks a voice for them and
    the browser sets them right to left (*A Land of Mosques and Marabouts*, 2026-11-20; review 2026-11-21).
    Chinese characters get lang="zh", or "ja" when the run has kana, so that the browser picks a font with the
    right forms (*A Yankee on the Yangtze*, 2026-11-22)."""
    for rx, lang in SCRIPT_RUNS:
        s = rx.sub(lambda m: f'<span lang="{lang}" dir="rtl">{m.group(0)}</span>', s)
    s = HAN_RUN.sub(lambda m: '<span lang="%s">%s</span>' % (
        "ja" if re.search(f"[{KANA}]", m.group(0)) else "zh", m.group(0)), s)
    return s


class Ctx:
    """What differs between the website and the EPUB."""
    def __init__(self, book, flavor, names):
        self.book, self.flavor, self.names = book, flavor, names
        self.targets = page_targets(book, names)
        self.seen_pg, self.seen_ref = set(), set()
        src = book.get("source", {})
        self.items = compile_book.scan_items(src)
        self.extra = src.get("extra_leaves", {})

    def scan_url(self, leaf):
        x = self.extra.get(leaf)
        if x:                     # a leaf taken from another scan of the same edition (book.json source.extra_leaves)
            return f"https://archive.org/details/{x['ia_identifier']}/page/n{x['n']}/mode/1up"
        n = int(re.search(r"\d+", leaf).group(0))
        for first, ia, hidden in self.items:
            if n >= first:
                n -= first
                n -= sum(1 for h in hidden if h < n)
                return f"https://archive.org/details/{ia}/page/n{n}/mode/1up"
        return None

    def pb(self, n, leaf):
        a = anchor(n)
        ident = ""
        if a and a not in self.seen_pg:
            self.seen_pg.add(a)
            ident = f' id="pg-{a}"'
        if self.flavor == "epub":
            if not ident:
                return ""
            return f'<span epub:type="pagebreak" role="doc-pagebreak"{ident} aria-label="{attr(n)}"></span>'
        url = self.scan_url(leaf)
        label = n or "–"
        title = f"Page {n} of the printed book: open the scan" if n else "Unnumbered page: open the scan"
        if url:
            return f'<a class="pb"{ident} href="{attr(url)}" title="{attr(title)}">{esc(label)}</a>'
        return f'<span class="pb"{ident}>{esc(label)}</span>'

    def inline(self, s):
        out, closers = [], []
        for t in inline.tokens(inline.drop_sides(s)):
            if t[0] == "text":
                out.append(tag_scripts(esc(t[1])))
            elif t[0] == "empty" and t[1] == "pb":
                out.append(self.pb(t[2].get("n", ""), t[2].get("leaf", "")))
            elif t[0] == "open":
                name, a = t[1], t[2]
                close = f"</{name}>"
                if name == "sc":
                    out.append('<span class="sc">'); close = "</span>"
                elif name == "noteref":
                    et = ' epub:type="noteref"' if self.flavor == "epub" else ""
                    # a second reference to the same note ([[fnref * again]]) gets no id: ids must be unique
                    ident = "" if a["to"] in self.seen_ref else f' id="r-{a["to"]}"'
                    self.seen_ref.add(a["to"])
                    # a screen reader reads a bare mark ("1", "*") as a digit or a star: name it (review 2026-11-21)
                    num = re.search(r"-n(\d+)$", a["to"])
                    label = f' aria-label="Note {num.group(1)}"' if num else ' aria-label="Note"'
                    out.append(f'<a class="noteref"{et} role="doc-noteref" href="#{a["to"]}"{ident}{label}>'); close = "</a>"
                elif name == "pageref":
                    tgt = self.targets.get(a.get("n", ""))
                    out.append(f'<a class="pageref" href="{attr(tgt)}">' if tgt else "")
                    close = "</a>" if tgt else ""
                elif name == "corr":
                    web = self.flavor == "web"
                    out.append(f'<span class="corr" title="Printed: {attr(a.get("orig", ""))}">' if web else "")
                    close = "</span>" if web else ""
                elif name in ("supplied", "gap"):     # the reading editions show the letters only (Tom, 2026-11-20)
                    out.append(""); close = ""
                else:
                    out.append(f"<{name}>")
                closers.append(close)
            elif t[0] == "close":
                out.append(closers.pop() if closers else "")
        return "".join(out)

    def blocks(self, div):
        div = roman_long_italics(div)
        body, prev = [], "paragraph" if div.get("runs_on") else None
        targets = section_targets(div)
        tp, leaf0 = div["kind"] == "titlepage", None
        for bi, b in enumerate(div["blocks"]):
            n0 = len(body)
            t = b["type"]
            # the verso of the title page is set apart (a frontispiece moved here from an earlier leaf is not a verso)
            newleaf = tp and leaf0 is not None and b["leaf"] > leaf0
            leaf0 = max(leaf0 or "", b["leaf"])
            pbs = "".join(self.pb(p["n"], p["leaf"]) for p in b.get("pb", []))
            if t == "heading":
                lv = b["level"]
                body.append(f'<h{lv}>{pbs}{self.inline(b["text"])}</h{lv}>')
            elif t == "paragraph":
                cls = []
                if b.get("role") == "subtitle":
                    cls += ["subtitle", "short"] if short_subtitle(b["text"]) else ["subtitle"]
                elif b.get("align"):
                    cls.append(b["align"])
                elif prev in (None, "heading", "break", "subtitle", "table", "quote", "verse"):
                    cls.append("first")
                c = f' class="{" ".join(cls)}"' if cls else ""
                body.append(f'<p{c}>{pbs}{self.inline(b["text"])}</p>')
            elif t == "quote":
                ps = []
                for i, p in enumerate(b["paragraphs"]):
                    c = f' class="{p["align"]}"' if p.get("align") else ""
                    ps.append(f'<p{c}>{pbs if i == 0 else ""}{self.inline(p["text"])}</p>')
                body.append("<blockquote>" + "".join(ps) + "</blockquote>")
            elif t == "verse":
                st = []
                for i, s in enumerate(b["stanzas"]):
                    lines = "".join(f'<span class="line">{pbs if i == 0 and j == 0 else ""}{self.inline(x)}</span>' for j, x in enumerate(s))
                    st.append(f'<p>{lines}</p>')
                body.append('<div class="verse">' + "".join(st) + "</div>")
            elif t == "image":
                cap = f'<figcaption>{self.inline(b["caption"])}</figcaption>' if b.get("caption") else ""
                fc = ' class="ornament"' if b.get("ornament") else ""
                body.append(f'<figure{fc}>{pbs}<img src="{attr(b["src"])}" alt="{attr(b["alt"])}"/>{cap}</figure>')
            elif t == "table":
                trs = "".join("<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in r) + "</tr>" for r in b["rows"])
                body.append(f'<div class="tablewrap">{pbs}<table>{trs}</table></div>')
            elif t == "break":
                body.append(f'<hr class="break"/>{pbs}')
            if bi in targets and len(body) > n0:
                # the anchor of a contents entry goes on the block's first element
                body[n0] = re.sub(r"^<(\w+)", lambda m: f'<{m.group(1)} id="{targets[bi]}"', body[n0], count=1)
            if newleaf and len(body) > n0:
                body.insert(n0, '<div class="tp-verso"></div>')
            # a paragraph after a picture is indented as it would be without the picture (Tom, 2026-11-22: the
            # scans indent them; a paragraph that runs on round a picture is joined by [[cont]] and never gets here)
            if t != "image":
                prev = "subtitle" if b.get("role") == "subtitle" else t
        if div["notes"]:
            items = []
            for n in div["notes"]:
                et = ' epub:type="footnote"' if self.flavor == "epub" else ""
                back = f'<a class="noteback" href="#r-{n["id"]}" aria-label="Back to the text">{esc(n["mark"])}</a>'
                items.append(f'<aside class="note"{et} role="doc-footnote" id="{n["id"]}"><p>{back} {self.inline(n["text"])}</p></aside>')
            body.append('<section class="notes" aria-label="Notes"><hr/>' + "\n".join(items) + "</section>")
        s = "\n".join(body)
        if tp:
            s = f'<div class="titlepage">\n{s}\n</div>'
        # a reference whose note is in the same file keeps its link; its back-link needs the reference to exist
        ids = set(re.findall(r' id="(r-[^"]+)"', s))
        s = re.sub(r'<a class="noteback" href="#(r-[^"]+)" aria-label="[^"]*">(.*?)</a>',
                   lambda m: m.group(0) if m.group(1) in ids else f'<span class="noteback">{m.group(2)}</span>', s)
        return s


def nav_tree(book):
    """[(division, [child divisions])] for the reading editions: chapters nest under the part before them."""
    tree, part = [], None
    for d in whole_reading_divisions(book):
        if d["kind"] == "part":
            part = (d, [])
            tree.append(part)
        elif d["kind"] == "chapter" and part is not None:
            part[1].append(d)
        else:
            part = None
            tree.append((d, []))
    return tree


def toc_title(d):
    """The division's entry in the contents: `toc_title` (e.g. the chapter summary in full) or its title."""
    return d.get("toc_title") or d["title"]


def section_id(k):
    return f"sec-{k + 1}"


def toc_tree(book):
    """[(title, division id, fragment or None, [children])] — the contents of the reading editions: divisions,
    chapters nested under their part, and a division's `sections` (book.json toc_entries) nested under it."""
    def node(d, kids):
        if d.get("split"):       # each section is a page of its own (split_division)
            subs = [(u["title"], u["id"], None, []) for u in split_division(d) if u["title"] != d["title"]]
        else:
            subs = [(x["title"], d["id"], section_id(k), []) for k, x in enumerate(d.get("sections", []))]
        return (toc_title(d), d["id"], None, subs + [node(c, []) for c in kids])
    return [node(d, kids) for d, kids in nav_tree(book)]


def section_targets(div):
    """block index -> anchor id, for the blocks the contents point at."""
    return {x["block"]: section_id(k) for k, x in enumerate(div.get("sections", []))}


def nav_list(book, names, prefix=""):
    def li(n):
        title, did, frag, kids = n
        inner = f'<a href="{prefix}{names[did]}{"#" + frag if frag else ""}">{esc(title)}</a>'
        if kids:
            inner += "<ol>" + "".join(li(k) for k in kids) + "</ol>"
        return f"<li>{inner}</li>"
    return "<ol>" + "\n".join(li(n) for n in toc_tree(book)) + "</ol>"


def authors_text(book):
    """'A, B' for the authors; '; edited by C' for those with "role": "editor"."""
    au = book.get("authors", [])
    main = ", ".join(a["name"] for a in au if not a.get("role")) or "Anonymous"
    eds = ", ".join(a["name"] for a in au if a.get("role") == "editor")
    return main + (f"; edited by {eds}" if eds else "")
