#!/usr/bin/env python3
"""Preflight: every mechanical publication check in one command. Run it before publishing any book version.

  preflight.py BOOKDIR [--epubcheck JAR | --skip-epubcheck] [--report FILE] [-v]

BOOKDIR is wip/<slug> or books/<slug>. The book is built into a temporary directory (JSON, HTML, EPUB,
ODT) and the checks in CHECKS are run on the page files and on what was built. Exit status 0 = may be
published, 1 = not.

Two modes per check:
  enforce   every item must be fixed, or waived in book.json with a reason;
  observe   items are listed for a look and counted, but do not block. A new check starts here and is
            promoted once notes/metrics.md shows its alarms are mostly real.

Waivers (book.json):  "waivers": [{"check": "spacing", "match": "p0145", "why": "printed so: a spaced French quotation"}]
  `match` is a substring of the item line; `why` is required. Unused waivers are reported.

Rule (CLAUDE.md): this file is not edited, and no check is moved to observe, in a session that is
publishing a book the check is blocking. Waive with the reason, record the false alarm in
notes/metrics.md, fix the check (with a test) in a later session.

The last line printed is the stamp: copy it into the book's log.md.
"""
import argparse, collections, datetime, difflib, glob, json, os, re, shutil, subprocess, sys, tempfile, unicodedata, zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_site, compile_book, inline, render_html as rh  # noqa: E402

CHECKS = collections.OrderedDict([
    ("meta",            ("enforce", "book.json: required fields present and sane")),
    ("markup",          ("enforce", "page files: every [[…]] is a known form, inline tags balanced, no 〓")),
    ("compile",         ("enforce", "compile warnings other than page-break hyphen joins (notes, images, [[cont]], divisions)")),
    ("conservation",    ("enforce", "the words of the page files are in the JSON, and the reading parts in HTML, EPUB and ODT, in order, nothing else")),
    ("stray-markup",    ("enforce", "no markup ([[…]], escaped tags, 〓) shows in the reading editions")),
    ("straight-quotes", ("enforce", "no straight ' or \" in the text")),
    ("spacing",         ("enforce", "modern spacing: no space before ; : ! ? , . or inside quotation marks, no doubled spaces")),
    ("sc-caps",         ("enforce", "text inside <sc> is typed in lower case with real capitals, not in capitals")),
    ("heading-caps",    ("enforce", "headings, chapter titles and captions are in upper and lower case, not all capitals")),
    ("links",           ("enforce", "every link inside the book's web pages and EPUB has a target")),
    ("wellformed",      ("enforce", "HTML pages, EPUB documents and ODT XML parse")),
    ("nav",             ("enforce", "contents: at least one reading division; each has a title and text")),
    ("epubcheck",       ("enforce", "epubcheck: 0 fatals / 0 errors / 0 warnings")),
    ("odt",             ("enforce", "LibreOffice opens the ODT and converts it to PDF")),
    ("audit",           ("enforce", "book.json records the sampled audit of this version")),
    ("hyphen-joins",    ("observe", "page-break hyphen joins (hyphen removed) that the book does not settle: read the list once")),
    ("joins",           ("observe", "page joins: missing [[cont]]")),
    ("folios",          ("observe", "printed page numbers that break the sequence")),
    ("leaves",          ("enforce", "no leaf without a page file between the first and the last page file (a draft refused or lost); leaves IA hides do not count")),
    ("quote-balance",   ("observe", "paragraphs with a closing double quote and no opening one, or the reverse at the paragraph end")),
    ("image-splits",    ("enforce", "a paragraph cut in two by a picture: text before it unclosed, text after it in lower case (no [[cont]] after the caption)")),
    ("contents",        ("observe", "entries of the printed contents with no matching heading")),
    ("site-text",       ("enforce", "book.json text shown on the site (titles, summary, notes, contents entries): no straight ' or \"")),
    ("note-tail",       ("observe", "text after a page's notes that is not a note (a table or paragraph of a note set as body text)")),
    ("caption-tail",    ("observe", "a short line after a picture's caption (a cross-reference, “To face p. N”): part of the caption, or left out?")),
    ("image-before-heading", ("observe", "a picture above a # heading on the same page (not an ornament): it falls into the division before; move it after the heading?")),
    ("verse-joins",     ("observe", "verse continued at a page top ([[cont]]): stanza lengths on both sides, to compare on the scan")),
    ("cover",           ("enforce", "images/cover.jpg (or .png) exists: the front cover if its title is readable, otherwise the title page")),
    ("accents",         ("observe", "words the book spells with different accents (or with and without): look at each group on the scan")),
    ("misprints",       ("observe", "common words with a turned or wrong letter (tbe, aud, iu, conld …) not marked [[corr]]: look at each on the scan")),
    ("rare-forms",      ("observe", "words found once or twice in all the books, a confusable letter (n/u, b/h, c/e, l/i, t/f) away from a common word: look at each on the scan")),
    ("title-page",      ("observe", "the reading editions do not begin with the book's title page (divisions: kind \"titlepage\")")),
    ("serial-commas",   ("observe", "book.json text of ours with a list that may lack the comma before its last and/or (style.md §Site text)")),
    ("missing-stop",    ("observe", "a sentence-opening word (The, He, His, It, There …) after a lower-case word with no stop between: look at each on the scan")),
    ("images",          ("enforce", "image files not used by any page")),
    ("source",          ("enforce", "source.json: the Drive cache of the page images is recorded")),
])
INLINE_TAGS = inline.INLINE
PAGE_TAG = re.compile(r'</?(?:%s|blockquote|verse)>|<pref(?: to="\w+")?>|</pref>' % "|".join(INLINE_TAGS))


def squash(s):
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[\s\-­]+", "", s)


# ---------------------------------------------------------------- text streams

SIDE = re.compile(r"\s*\[\[side:\s*([^\[\]]*?)\s*\]\]\s*")


def page_streams(pages, captions=None, sides=None, streams=None):
    """(main, notes) text of the page files, markup removed. With `captions` (a list), the captions of images
    are collected there instead of in main: the compiler may move an image (a plate inside a paragraph that
    runs over the page goes after the paragraph; the frontispiece goes to the start of the reading text)."""
    main, notes = [], []
    after_image = False          # as the compiler: a caption belongs to an image only directly after it
    for leaf, text in pages:
        for ln in text.splitlines():
            s = ln.strip()
            if re.match(r"\[\[image:", s):
                after_image = True
                continue
            if not s or re.fullmatch(r"\[\[(page [^\]]*|blank)\]\]", s):
                continue
            is_caption = s.startswith("[[caption]]") and after_image
            after_image = is_caption
            if s == "[[break]]" or re.fullmatch(r"</?(blockquote|verse)>", s):
                continue
            tgt = captions if is_caption and captions is not None else main
            if s.startswith("[[stream]]"):          # a second stream (compile_book.split_streams): its own division(s)
                s = s[10:].strip()
                tgt = streams if streams is not None else main
            m = re.match(r"\[\[fn ([^\]]+)\]\]\s*(.*)", s)
            if m:
                tgt, s = notes, m.group(2)
            s = re.sub(r"\[\[corr [^|\]]*\|([^\]]*)\]\]", r"\1", s)
            s = re.sub(r"\[\[supplied ([^\]]*)\]\]", r"\1", s).replace("[[gap]]", "[…]")
            if sides is not None:                       # side-notes apart: the JSON keeps them out of plain text
                sides += [re.sub(r"<[^<>]+>", "", x) for x in SIDE.findall(s)]
            s = SIDE.sub(" ", s)
            s = re.sub(r"\[\[fnref [^\]]+\]\]", "", s)
            s = re.sub(r"\[\[(cont|right|center|subtitle|caption)\]\]", "", s)
            s = PAGE_TAG.sub("", s)
            if s.startswith("|") and s.endswith("|"):
                if re.fullmatch(r"\|[-| :]+\|", s):
                    continue
                s = s.replace("|", " ")
            s = re.sub(r"^#{1,3} ", "", s)
            tgt.append(s)
    return " ".join(main), " ".join(notes)


def json_streams(book, reading_only=False, captions=None, sides=None, streams=None):
    """With `captions` (a list), image captions are collected there instead of in main (see page_streams);
    with `sides`, the side-notes are collected there (plain text leaves them out)."""
    main, notes = [], []
    for d in book["divisions"]:
        if reading_only and not d.get("reading"):
            continue
        for b in d["blocks"]:
            tgt = captions if captions is not None and b.get("type") == "image" else main
            if streams is not None and d.get("stream"):
                tgt = streams
            tgt += [inline.plain(s) for s in rh.strings(b)]
            if sides is not None:
                sides += [x for s in rh.strings(b) for x in inline.sides(s)]
        notes += [inline.plain(n["text"]) for n in d["notes"]]
    return " ".join(main), " ".join(notes)


def html_text(x):
    x = re.sub(r'<a class="pb"[^>]*>.*?</a>|<span class="pb"[^>]*>.*?</span>', "", x, flags=re.S)
    x = re.sub(r'<a class="note(?:ref|back)"[^>]*>.*?</a>|<span class="noteback">.*?</span>', "", x, flags=re.S)
    x = re.sub(r"</(p|h\d|td|figcaption|span)>|<br/>", " ", x)
    return inline.html.unescape(re.sub(r"<[^>]+>", "", x))


def html_streams(docs):
    """docs = list of body strings of the reading divisions (web article or EPUB section)."""
    main, notes = [], []
    for x in docs:
        a, sep, b = x.partition('<section class="notes"')
        main.append(html_text(a))
        if sep:
            notes.append(html_text("<" + b))
    return " ".join(main), " ".join(notes)


T = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"
SKIP_STYLES = {"Title", "Subtitle", "Author", "Imprint", "Edition_20_Note", "Section_20_Break", "VerseEnd",
               # the title of a section made for this edition (render_html.split_division): not book text; it
               # stands outside <article> on the web and outside <section> in the EPUB
               "Added_20_Heading",
               # the generated contents list after the title page (render_odt.contents): not book text
               "Contents_20_Heading", "Contents_20_1", "Contents_20_2", "Contents_20_3"}


def odt_streams(data):
    z = zipfile.ZipFile(data)
    root = ET.fromstring(z.read("content.xml"))
    body = root.find(".//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text")
    main, notes = [], []

    def text_of(el, with_notes=False):
        out = [el.text or ""]
        for c in el:
            if c.tag.endswith("}frame") or c.tag == T + "note-ref":
                pass                     # images; a second mark for a note (cross-reference)
            elif c.tag == T + "note":
                nb = c.find(T + "note-body")
                notes.append(" ".join(text_of(p) for p in nb))
            elif c.tag == T + "s":
                out.append(" " * int(c.get(T + "c", "1")))
            else:
                out.append(text_of(c))
            out.append(c.tail or "")
        return "".join(out)

    def walk(el):
        for c in el:
            if c.tag in (T + "p", T + "h"):
                if c.get(T + "style-name") in SKIP_STYLES:
                    continue
                main.append(text_of(c))
            else:
                walk(c)
    walk(body)
    return " ".join(main), " ".join(notes)


def caption_key(c):
    """The order in which captions are compared (the compiler moves some images, so captions are compared as a
    sorted list): by their squashed text without tags or case, so that a straight apostrophe or a leading <sc>
    does not sort a caption elsewhere and raise a false item (*A Woman’s Trip to Alaska*, 2026-11-20)."""
    return squash(re.sub(r"<[^>]*>", "", c)).lower()


def compare(a, b, label, limit=12):
    a, b = squash(a), squash(b)
    if a == b:
        return []
    items = []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False) if len(a) + len(b) < 60000 else None
    if sm is None:
        # long texts: cut the common start and end; if what is left is short, list every difference in it
        n = min(len(a), len(b))
        i = next((k for k in range(n) if a[k] != b[k]), n)
        e = next((k for k in range(n - i) if a[len(a) - 1 - k] != b[len(b) - 1 - k]), n - i)
        ma, mb = a[max(0, i - 30):len(a) - e], b[max(0, i - 30):len(b) - e]
        if len(ma) + len(mb) < 60000:
            return compare(ma, mb, label, limit) if ma != mb else []
        return [f"{label}: texts differ from character {i}: …{a[max(0, i - 30):i + 30]}… / …{b[max(0, i - 30):i + 30]}…"]
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            items.append(f"{label}: {op} …{a[max(0, i1 - 20):i1]}[{a[i1:i2][:60]}]→[{b[j1:j2][:60]}]{a[i2:i2 + 20]}…")
            if len(items) >= limit:
                break
    return items


# ---------------------------------------------------------------- checks on the page files

def check_markup(pages):
    items = []
    for leaf, text in pages:
        lines = text.splitlines()
        if not lines or not re.fullmatch(r"\[\[page [^\]]*\]\]", lines[0].strip()):
            items.append(f"{leaf}: first line is not [[page N]]")
        for ln in lines:
            rest = compile_book.MARK.sub("", ln)
            if "[[" in rest or "]]" in rest:
                items.append(f"{leaf}: unknown or broken [[…]]: {ln.strip()[:70]!r}")
            if "〓" in ln:
                items.append(f"{leaf}: illegible mark 〓: {ln.strip()[:70]!r}")
            body = PAGE_TAG.sub("", re.sub(r"\[\[corr [^\]]*\]\]", "", ln))
            if re.search(r"</?[A-Za-z][^<>]{0,30}>", body):
                items.append(f"{leaf}: unknown tag: {ln.strip()[:70]!r}")
            for m in re.finditer(r"<sc>(.*?)</sc>", ln):
                pass
            ln = re.sub(r"^\s*\[\[stream\]\]\s*", "", ln)     # a second stream's line may start with a heading
            if re.search(r"(?<!^)(?<!\|)\s#{1,3} \w", ln) and not ln.lstrip().startswith("#"):
                items.append(f"{leaf}: '#' inside a line (heading not on its own line?): {ln.strip()[:70]!r}")
        if re.search(r"\[\[(cont|right|center|subtitle|caption)\]\]\s*$", text, flags=re.M):
            items.append(f"{leaf}: a marker with no text after it")
    return items


def check_sc(pages):
    items = []
    for leaf, text in pages:
        for m in re.finditer(r"<sc>(.*?)</sc>", text):
            t = re.sub(r"<[^>]+>", "", m.group(1))
            letters = [c for c in t if c.isalpha()]
            if len(letters) > 1 and all(c.isupper() for c in letters):
                items.append(f"{leaf}: <sc>{t[:40]}</sc>")
    return items


def check_heading_caps(pages):
    items = []
    for leaf, text in pages:
        for ln in text.splitlines():
            m = re.match(r"\s*(?:#{1,3} |\[\[(?:subtitle|caption)\]\])(.*)", ln)
            if not m:
                continue
            t = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", m.group(1))
            words = [w for w in re.findall(r"[A-Za-z]{2,}", t) if not re.fullmatch(r"[IVXLCDM]+", w)]
            if words and all(w.isupper() for w in words) and sum(len(w) for w in words) > 3:
                items.append(f"{leaf}: {ln.strip()[:60]!r}")
    return items


def check_folios(pages):
    items, prev = [], None
    for leaf, text in pages:
        m = re.match(r"\[\[page (\d+)\]\]", text)
        if not m:
            continue
        n = int(m.group(1))
        if prev is not None and not (prev[1] < n <= prev[1] + 6):
            items.append(f"{leaf}: page {n} after page {prev[1]} ({prev[0]})")
        prev = (leaf, n)
    return items


def check_leaves(pages, hidden=(), items=None):
    """Leaves missing from the run of page files: the folios check cannot see a gap of a few pages.
    Leaves IA's viewer hides (book.json source.hidden_leaves: colour cards, tissue guards) are not missing.
    Anything else left out on purpose (an IA card) is waived in book.json with the reason.
    `items` (compile_book.scan_items) for a book from several IA items: each item's run is checked apart."""
    nums = sorted(int(re.findall(r"\d+", leaf)[-1]) for leaf, _ in pages)
    if not items:
        items = [(0, None, [int(h) for h in hidden])]
    out = []
    for k, (first, _, hid) in enumerate(sorted(items)):
        end = sorted(items)[k + 1][0] if k + 1 < len(items) else float("inf")
        run = [n for n in nums if first <= n < end]
        have = set(run) | {first + h for h in hid}
        out += [f"p{n:04d}: no page file" for n in range(run[0], run[-1] + 1) if n not in have] if run else []
    return out


def first_text(text):
    for ln in text.splitlines():
        s = ln.strip()
        if s and not re.fullmatch(r"\[\[(page [^\]]*|blank)\]\]", s) and not re.fullmatch(r"<(blockquote|verse)>", s):
            return s
    return ""


def last_text(text):
    for ln in reversed(text.splitlines()):
        s = ln.strip()
        if s and not s.startswith("[[fn ") and not re.fullmatch(r"</(blockquote|verse)>", s):
            return s
    return ""


WORD = r"[^\W\d_]+"


def word_forms(pages):
    """How the book prints its words: whole, hyphenated, and the first parts of hyphenated words (lower case)."""
    whole, hyph, first = collections.Counter(), collections.Counter(), collections.Counter()
    for _, t in pages:
        t = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", " ", t).rstrip()
        t = re.sub(rf"{WORD}-$", " ", t)                       # the broken word at the foot of the page
        for w in re.findall(rf"{WORD}(?:-{WORD})*", t):
            w = w.lower()
            if "-" in w:
                hyph[w] += 1
                first[w.split("-")[0]] += 1
            else:
                whole[w] += 1
    return whole, hyph, first


def base_form(w):
    return "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))


def check_accents(pages, limit=6):
    """Words printed with accents that the page files spell in more than one way (different accents, or with and
    without): *Land of the North Wind* had 23 such groups and 35 pages wrong, read by drafts, verifier and judge
    alike (2026-11-20). One item a group, with the leaves of each form, for a look on the scan."""
    forms = collections.defaultdict(lambda: collections.defaultdict(list))
    for leaf, t in pages:
        t = re.sub(r"<[^>]+>|\[\[(?!corr )[^\]]*\]\]", " ", t)
        t = re.sub(r"\[\[corr [^|\]]*\|([^\]]*)\]\]", r"\1", t)
        for w in re.findall(WORD, t):
            b = base_form(w).lower()
            forms[b][w.lower()].append(leaf)
    items = []
    for b, f in sorted(forms.items()):
        if len(f) > 1 and any(base_form(w) != w for w in f):
            items.append(f"{b}: " + "; ".join(f"{w} ({', '.join(sorted(set(ls))[:limit])}{'…' if len(set(ls)) > limit else ''})"
                                               for w, ls in sorted(f.items())))
    return items


# Common English words with a turned, wrong-fount or broken letter, as printed or as misread. None is an English
# word. Reported by a reader (*Trans-Caspia* “ean”, issue #100, 2026-11-21); the sweep that followed found six more
# in four published books (five printed, one a misreading), none listed by any stage of the pipeline.
MISPRINTS = {
    "tbe", "tlie", "thc", "tbat", "tliat", "wbich", "wliich", "wben", "tben", "aud", "aiid", "iu", "ean",
    "conld", "wonld", "shonld", "bnt", "uot", "fiom", "frorn", "rnore", "liave", "liis", "witli", "wbo", "wliat",
    "tbis", "tliis", "tbey", "tliey", "tbere", "tliere", "tbeir", "tlieir", "witb", "mncb", "mnch", "verv",
    "aaid", "beeu", "tbem", "tliem", "ouly", "anv", "bave",
    "iustead", "wc", "ofl",                 # *The Bridal and the Bridle* (2026-11-22): found by the spot-read only
    "th",                                   # “depôt of th Pacific” (*Cordillera and Pampa*, a reader, issue #169)
}


def check_misprints(pages):
    """Every word of `MISPRINTS` in the text outside [[corr]]: a misprint the book prints (mark it [[corr]]) or a
    misreading (fix it). The readers copy a printed turned letter faithfully and the judge never sees it."""
    out = []
    for leaf, t in pages:
        t = re.sub(r"\[\[corr [^\]]*\]\]|\[\[[^\]]*\]\]", " ", t)
        t = re.sub(r"<[^>]+>", "", t)                 # M<sc>c</sc>L<sc>ean</sc> is one word
        for m in re.finditer(WORD, t):
            w = m.group(0)
            if w.lower() == "th" and (re.search(r"\d\s*$", t[:m.start()]) or t[m.end():m.end() + 1] in ("’", "'")):
                continue                                # 4<sup>th</sup>, “5 th”; dialect “th’”
            if w.lower() in MISPRINTS and w != "Aud":      # Aud the Deeply Wealthy (*By Fell and Fjord*)
                out.append(f"{leaf}: “{m.group(0)}” in …{t[max(0, m.start() - 25):m.end() + 25].strip()}…")
    return out


STARTERS = ("The", "He", "His", "She", "We", "They", "It", "But", "This", "There", "Our", "Then", "When", "After")
# “of His mercy”, “that He has”: a capital pronoun after such a word is the divine one, not a new sentence.
DIVINE_AFTER = {"of", "to", "in", "on", "by", "at", "as", "with", "into", "unto", "upon", "that", "which", "whereby",
                "where", "here", "are", "beneath", "behold", "led", "for", "from", "whom", "and"}
MISSING_STOP = re.compile(r"\b([a-z]{2,})\s+(" + "|".join(STARTERS) + r")\s+([a-z]+)")


def check_missing_stop(pages):
    """A lower-case word followed by a sentence-opening word with no punctuation between, in prose outside verse,
    tables, headings, italics and markup: a full stop left out in print (mark it [[corr]]) or lost in reading.
    *The Golden Dagon* p. 7 “privation His orders” (a reader, issue #117, 2026-11-21). Divine pronouns (“that He
    has”) are listed too: they are looked at and passed."""
    out = []
    for leaf, t in pages:
        t = re.sub(r"<verse>.*?</verse>", "\n", t, flags=re.S)
        t = re.sub(r"<i>.*?</i>", " ; ", t, flags=re.S)
        for line in t.splitlines():
            if line.lstrip().startswith(("|", "#")):
                continue
            line = re.sub(r"\[\[corr [^\]]*\]\]", " ; ", line)
            line = re.sub(r"\[\[image:[^\]]*\]\]|\[\[side:[^\]]*\]\]", " ; ", line)
            line = re.sub(r"\[\[[^\]]*\]\]", " ", line)
            line = re.sub(r"<[^>]+>", "", line)
            for m in MISSING_STOP.finditer(line):
                if m.group(2) in ("He", "His") and m.group(1) in DIVINE_AFTER:
                    continue
                out.append(f"{leaf}: “{m.group(1)} {m.group(2)}” in …{line[max(0, m.start() - 25):m.end() + 10].strip()}…")
    return out


CONFUSABLE = [("n", "u"), ("u", "n"), ("h", "b"), ("b", "h"), ("e", "c"), ("c", "e"), ("i", "l"), ("t", "f")]


def _plain_words(pages):
    """(leaf, word) for each lower-case word outside italics, notes markup and [[corr]], leaving out the first word
    of a page that continues the last (it may be the end of a hyphenated word) and a word ending in a hyphen."""
    for leaf, t in pages:
        t = re.sub(r"\[\[corr [^\]]*\]\]|\[\[side:[^\]]*\]\]|<i>.*?</i>", " ", t, flags=re.S)
        t = re.sub(r"\[\[cont\]\]\s*\S*", " ", t)
        t = re.sub(r"\[\[[^\]]*\]\]", " ", t)
        t = re.sub(r"<[^>]+>", "", t)
        t = re.sub(r"[^\W\d_]+-\s*$", " ", t)
        for w in re.findall(WORD, t):
            if w.islower():
                yield leaf, w


def corpus_counts(root=None):
    """Lower-case word counts over every published book's page files (the collection is the dictionary)."""
    root = root or os.path.join(os.path.dirname(HERE), "books")
    cnt = collections.Counter()
    for d in sorted(glob.glob(os.path.join(root, "*", "pages"))):
        pages = [(os.path.basename(f)[:-4], open(f, encoding="utf-8").read()) for f in sorted(glob.glob(os.path.join(d, "p*.txt")))]
        cnt.update(w for _, w in _plain_words(pages))
    return cnt


def check_rare_forms(pages, corpus, rare=2, common=40):
    """Words of this book seen at most `rare` times in the whole collection (with this book) that become a word seen
    `common` times or more when one confusable letter is changed: “hnndred”, “numher”, “entranee”, “wili”. The review
    after forty books found 15 such printed misprints (and 2 misreadings) in 11 published books, unmarked; about one
    item in five was real (the rest names, dialect, foreign words)."""
    own = collections.Counter(w for _, w in _plain_words(pages))
    total = corpus + own if corpus is not None else own
    out, seen = [], set()
    for leaf, w in _plain_words(pages):
        if w in seen or total[w] > rare or len(w) < 3:
            continue
        for a, b in CONFUSABLE:
            hits = [w[:m.start()] + b + w[m.end():] for m in re.finditer(a, w)]
            best = max(hits, key=lambda v: total[v], default=None)
            if best and total[best] >= common:
                seen.add(w)
                out.append(f"{leaf}: “{w}” — “{best}” is common ({total[best]})")
                break
        else:
            # a letter dropped or two letters transposed (“vegtables”, “Christain”): words seen once in the whole
            # collection, five letters or more (review after fifty-five books: 11 misprints of *Scouting for
            # Stanley* found only by the spot-read; 228 items in 55 books, about four a book)
            if total[w] > 1 or len(w) < 5 or not w.isalpha():
                continue
            best = max(_letter_edits(w), key=lambda v: total[v])
            if total[best] >= common:
                seen.add(w)
                out.append(f"{leaf}: “{w}” — “{best}” is common ({total[best]}; a letter dropped or transposed?)")
    return out


def _letter_edits(w):
    """Words one dropped letter or one transposition of neighbouring letters away from w."""
    for i in range(len(w) - 1):
        if w[i] != w[i + 1]:
            yield w[:i] + w[i + 1] + w[i] + w[i + 2:]
    for i in range(len(w) + 1):
        for c in "abcdefghijklmnopqrstuvwxyz":
            yield w[:i] + c + w[i:]


def triage_hyphen_joins(items, pages):
    """The hyphen-join look list without the joins that give a word the book itself prints whole elsewhere
    (reviewed 2026-11-19: about three in four items of five books, none of them a compound to keep). A join
    whose hyphenated form, or whose first part with a hyphen (snow-, counter-), the book prints elsewhere is
    marked as a candidate for keep_hyphens; the rest are listed as before."""
    whole, hyph, first = word_forms(pages)
    out, attested = [], 0
    for it in items:
        m = re.search(r"…(.*)\|(.*)… \(hyphen removed", it)
        a = m and re.search(rf"({WORD})-$", re.sub(r"<[^>]+>", "", m.group(1)))
        b = m and re.match(rf"({WORD})", re.sub(r"<[^>]+>|⟦[^⟧]*⟧", "", m.group(2)))
        if not (a and b):
            out.append(it)
            continue
        x, y = a.group(1).lower(), b.group(1).lower()
        if hyph[f"{x}-{y}"]:
            out.append(f"{it} — the book prints “{x}-{y}” elsewhere: keep_hyphens?")
        elif whole[x + y]:
            attested += 1
        elif len(x) >= 4 and first[x]:
            out.append(f"{it} — the book hyphenates other “{x}-” words: keep_hyphens?")
        else:
            out.append(it)
    if attested:
        out.append(f"(and {attested} joins giving a word the book prints whole elsewhere: not listed)")
    return out


def check_note_tail(pages):
    """Lines after a page's first `[[fn` that are not notes. A note printed with a table or a second paragraph was
    typed with them on lines of their own; the compiler took them for body text, so they showed in the chapter
    and broke the sentence continued on the next page (*My Life in Mongolia and Siberia* p. viii, review 2026-11-20)."""
    out = []
    for leaf, text in pages:
        seen = False
        for ln in text.splitlines():
            s = ln.strip()
            if s.startswith("[[fn"):
                seen = True
            elif seen and s:
                out.append(f"{leaf}: after the notes: {s[:60]!r}")
                break
    return out


def check_caption_tail(pages):
    """A short line straight after a `[[caption]]` (a `[[right]]` or `[[center]]` line, or under 40 letters of text):
    a cross-reference ("[See page 107.") or "To face p. N" typed as a paragraph of its own. Set apart, it took the
    next page's `[[cont]]` text with it, right-aligned under the picture (*Uganda for a Holiday*, 3 plates;
    *Argentine Plains*, 26 lines): it belongs in the caption line, or is left out ("To face")."""
    out = []
    for leaf, text in pages:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for a, b in zip(lines, lines[1:]):
            if not a.startswith("[[caption]]") or b.startswith(("[[image", "[[caption", "[[page", "#", "[[fn", "<")):
                continue
            plain = re.sub(r"\[\[[^\]]*\]\]|<[^>]+>", "", b).strip()
            if b.startswith(("[[right]]", "[[center]]")) or len(plain) < 40:
                out.append(f"{leaf}: after the caption: {b[:60]!r}")
    return out


def check_image_before_heading(pages, ornaments=()):
    """A picture printed above a chapter's title on the same page: its `[[image:]]` line stands before the `#` line,
    so the compiler puts it at the end of the division before (or leaves it out with the contents), not at the head
    of the chapter (*Present-Day Japan*, six chapters: caught only by the rendered look). Ornaments (head-pieces)
    open the division and are not listed."""
    out = []
    for leaf, text in pages:
        lines = text.splitlines()
        h = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
        if h is None:
            continue
        k = 0
        for ln in lines[:h]:
            if ln.startswith("[[image:"):
                k += 1
                if f"{leaf}-{k}" not in ornaments:
                    out.append(f"{leaf}: picture {leaf}-{k} above {lines[h][:40]!r}")
    return out


def _verse_stanzas(text, first):
    """Line counts of the stanzas of the first (first=True) or last <verse> block of a page."""
    blocks = re.findall(r"<verse>\n?(.*?)\n?</verse>", text, flags=re.S)
    if not blocks:
        return []
    b = blocks[0] if first else blocks[-1]
    return [len([x for x in st.splitlines() if x.strip()]) for st in re.split(r"\n\s*\n", b) if st.strip()]


def check_verse_joins(pages):
    """Every verse block at a page top that begins with [[cont]]: it joins the first stanza of this page to the
    last stanza of the page before. Drafts put [[cont]] there when a stanza had ended at the page foot, so two
    stanzas ran together (*Twelve Years in Canterbury*: 6 of 13; only the rendered look saw it). The item gives
    the line counts of the two stanzas (and of the stanzas round them): compare them and the rhymes on the scan."""
    out = []
    for (l0, t0), (l1, t1) in zip(pages, pages[1:]):
        body = re.sub(r"^\s*(\[\[page [^\]]*\]\]\s*)?", "", t1)
        if not re.match(r"<verse>\s*\[\[cont\]\]", body):
            continue
        before, here = _verse_stanzas(t0, first=False), _verse_stanzas(t1, first=True)
        out.append(f"{l1}: verse continued from {l0}: stanzas before {before[-3:]} | here {here[:3]} (a stanza ending at the page foot needs no [[cont]])")
    return out


def check_joins(pages):
    items = []
    for (l0, t0), (l1, t1) in zip(pages, pages[1:]):
        a, b = last_text(t0), first_text(t1)
        if not a or not b or a.startswith(("#", "[[image", "[[caption", "|")) or b.startswith(("#", "[[image", "|")):
            continue
        pa = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", a).strip()
        pb = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", b).strip()
        cont = b.startswith("[[cont]]")
        closed = bool(re.search(r"[.?!][”’\")\]]*$", pa))
        # "[[cont]] after a closed sentence" was dropped at the review of 2026-11-20: 65 alarms in ten books, 0 real.
        if not cont and (pa.endswith("-") or (not closed and pb[:1].islower())):
            items.append(f"{l1}: no [[cont]] but the page before ends …{pa[-25:]!r} and this one starts {pb[:25]!r}")
    return items


# ---------------------------------------------------------------- checks on what was built

def check_text(streams):
    stray, straight, spacing = [], [], []
    for label, text in streams:
        for m in re.finditer(r"\[\[|\]\]|</?(?:i|b|sc|sup|sub|pref|blockquote|verse|pb|corr|noteref|pageref|side|supplied|gap)\b|〓|[⟦⟧]|&(?:lt|gt|amp);", text):
            stray.append(f"{label}: …{text[max(0, m.start() - 30):m.end() + 30]!r}…")
        for m in re.finditer(r"['\"]", text):
            straight.append(f"{label}: …{text[max(0, m.start() - 25):m.end() + 25]!r}…")
        for m in re.finditer(r"\w [;:!?,](?!\S*[;:!?,.]{2})|(?<=\w) \.(?= |$)(?! \. )|[“‘] +\w|\w[,.;:!?]? +[”](?=[\s,.;:!?]|$)|\S  +\S", text):
            ctxt = text[max(0, m.start() - 25):m.end() + 25]
            if re.search(r"\. \. \.|\.\.\.", ctxt) and m.group(0).strip() in (".", " ."):
                continue
            spacing.append(f"{label}: …{ctxt!r}…")
    return stray[:40], straight[:40], spacing[:60]


def spacing_items(book):
    """Spacing is judged block by block on the JSON (the joins between blocks are not text)."""
    items = []
    for d in book["divisions"]:
        for b in d["blocks"] + d["notes"]:
            for s in rh.strings(b):
                t = inline.plain(s)
                items += [f"{b['leaf']}: {i[6:]}" for i in check_text([("x", t)])[2]]
                if t != t.strip():
                    items.append(f"{b['leaf']}: space at the start or end of a block: {t[:40]!r}")
    return items[:80]


def check_quote_balance(book):
    items = []
    for d in book["divisions"]:
        if not d.get("reading"):
            continue
        for b in d["blocks"]:
            if b["type"] != "paragraph":
                continue
            t = inline.plain(b["text"])
            depth = 0
            for c in t:
                if c == "“":
                    depth += 1
                elif c == "”":
                    depth -= 1
                    if depth < 0:
                        break
            if depth < 0:
                items.append(f"{b['leaf']}: closing ” with no opening “: {t[:60]!r}")
            elif depth > 1:
                items.append(f"{b['leaf']}: {depth} quotations left open: {t[:60]!r}")
    return items


def check_image_splits(book):
    """Review 2026-11-20 (*South by West* v1: four paragraphs split mid-sentence by an engraving)."""
    items = []
    for d in book["divisions"]:
        if not d.get("reading") or d.get("kind") == "titlepage":   # a title page's lines are not sentences
            continue
        last, pic = None, False   # the last paragraph; whether only pictures have stood since it
        for b in d["blocks"]:
            if b["type"] == "paragraph":
                t = inline.plain(b["text"]).strip()
                if pic and last is not None and t[:1].islower() and not re.search(r"[.?!:;—][”’\")\]]*$", last):
                    items.append(f"{b['leaf']}: …{last[-25:]!r} | picture | {t[:25]!r}")
                last, pic = t, False
            elif b["type"] == "image":
                pic = True
            else:
                last, pic = None, False
    return items


def norm_title(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def check_contents(book):
    cont = [d for d in book["divisions"] if d["kind"] == "contents"]
    if not cont:
        return []
    heads = set()
    for d in book["divisions"]:
        heads.add(norm_title(d["title"]))
        for b in d["blocks"]:
            if b["type"] == "heading" or b.get("role") == "subtitle":
                heads.add(norm_title(inline.plain(b["text"])))
    blob = " | ".join(sorted(heads))
    items = []
    for d in cont:
        for b in d["blocks"]:
            for s in rh.strings(b):
                t = norm_title(re.sub(r"[\d ivxlc.]+$", "", inline.plain(s).strip(), flags=re.I))
                t = re.sub(r"^(chapter|chap|part|book|letter) [ivxlc\d]+ ?", "", t)
                if len(t) < 6 or t in ("contents", "page"):
                    continue
                key = " ".join(t.split()[:5])
                if key not in blob:
                    items.append(f"{b['leaf']}: {inline.plain(s).strip()[:70]!r}")
    return items


def check_links(out_dir, slug, epub_bytes):
    items = []
    bdir = os.path.join(out_dir, "books", slug)
    docs = {f: open(os.path.join(bdir, f), encoding="utf-8").read() for f in os.listdir(bdir) if f.endswith(".html")}
    z = zipfile.ZipFile(epub_bytes)
    edocs = {os.path.basename(n): z.read(n).decode("utf-8") for n in z.namelist() if n.endswith(".xhtml")}
    for label, group, base in (("web", docs, bdir), ("epub", edocs, None)):
        ids = {f: set(re.findall(r' id="([^"]+)"', x)) for f, x in group.items()}
        for f, x in group.items():
            for dup in {i for i in re.findall(r' id="([^"]+)"', x) if re.findall(r' id="([^"]+)"', x).count(i) > 1}:
                items.append(f"{label} {f}: id {dup!r} used twice")
            for href in re.findall(r' href="([^"]+)"', x):
                if re.match(r"[a-z]+:", href) or href.startswith("../"):
                    continue
                path, _, frag = href.partition("#")
                tgt = path or f
                if tgt in group:
                    if frag and frag not in ids[tgt]:
                        items.append(f"{label} {f}: link to missing anchor {href!r}")
                elif base is None or not os.path.exists(os.path.join(base, tgt)):
                    items.append(f"{label} {f}: link to missing file {href!r}")
            for src in re.findall(r' src="([^"]+)"', x):
                if label == "web" and not src.startswith(("http", "../")) and not os.path.exists(os.path.join(base, src)):
                    items.append(f"{label} {f}: missing image {src!r}")
    return items


def check_wellformed(out_dir, slug, epub_bytes, odt_bytes):
    items = []
    bdir = os.path.join(out_dir, "books", slug)
    for f in sorted(os.listdir(bdir)):
        if f.endswith(".html"):
            x = open(os.path.join(bdir, f), encoding="utf-8").read().replace("<!DOCTYPE html>", "", 1)
            try:
                ET.fromstring(x)
            except ET.ParseError as e:
                items.append(f"web {f}: {e}")
    for label, data in (("epub", epub_bytes), ("odt", odt_bytes)):
        z = zipfile.ZipFile(data)
        if z.testzip():
            items.append(f"{label}: damaged zip")
        if z.infolist()[0].filename != "mimetype" or z.infolist()[0].compress_type != zipfile.ZIP_STORED:
            items.append(f"{label}: mimetype is not the first, uncompressed entry")
        for n in z.namelist():
            if n.endswith((".xhtml", ".xml", ".opf")):
                try:
                    ET.fromstring(re.sub(rb"<!DOCTYPE html>", b"", z.read(n), count=1))
                except ET.ParseError as e:
                    items.append(f"{label} {n}: {e}")
    return items


def check_site_text(cfg):
    """Straight quotes in the book.json text that the site and the editions show as it is written (the compiler
    curls the quotes of the page files, not these): West Coast of Africa, 2026-11-20."""
    items, fields = [], []
    for k in ("title", "subtitle", "short_title", "summary", "notes_on_text", "omitted_from_reading", "edition_statement"):
        v = cfg.get(k)
        for x in (v if isinstance(v, list) else [v] if v else []):
            fields.append((k, x))
    for d in cfg.get("divisions", []):
        for k in ("title", "toc_title"):
            if d.get(k):
                fields.append((f"divisions {d.get('at')} {k}", d[k]))
    for e in cfg.get("toc_entries", []):
        if e.get("title"):
            fields.append((f"toc_entries {e.get('at')}", e["title"]))
    for where, x in fields:
        for m in re.finditer(r"['\"]", x if isinstance(x, str) else ""):
            items.append(f"book.json {where}: …{x[max(0, m.start() - 30):m.end() + 20]}…")
    return items


SERIAL = re.compile(r",\s[^,;:.()—–“”]{1,60}?\s(?:and|or)\s")


def check_serial_commas(cfg):
    """Tom, 2026-11-22: text written for the site has the comma before the last "and" or "or" of a list of three
    or more. Lists every place where a comma is followed, before the next comma or stop, by "and"/"or": most are
    lists; a pair after a comma ("In 1870, he sailed and returned") is not, and is left."""
    items = []
    fields = [(k, x) for k in ("summary", "notes_on_text", "omitted_from_reading")
              for x in (cfg.get(k) if isinstance(cfg.get(k), list) else [cfg.get(k)] if cfg.get(k) else [])]
    fields += [(f"toc_entries {e.get('at')}", e["title"]) for e in cfg.get("toc_entries", []) if e.get("title") and e.get("editor", True)]
    for where, x in fields:
        for m in SERIAL.finditer(x if isinstance(x, str) else ""):
            items.append(f"book.json {where}: …{x[max(0, m.start() - 30):m.end() + 20]}…")
    return items[:40]


def check_title_page(book):
    """Tom, 2026-11-22: the title page is the first page of the reading editions."""
    rd = [d for d in book["divisions"] if d.get("reading")]
    if rd and rd[0]["kind"] != "titlepage":
        return [f"the first division of the reading editions is {rd[0]['kind']} ({rd[0]['first_leaf']}): give the title page "
                'a "divisions" entry of kind "titlepage" (the half-title and what else stands before it stay out)']
    return []


def check_meta(cfg, bookdir):
    items = []
    need = ("id", "version", "date", "title", "authors", "place", "publisher", "year", "regions", "summary", "source", "history")
    for k in need:
        if not cfg.get(k):
            items.append(f"book.json: missing {k!r}")
    if cfg.get("id") != os.path.basename(os.path.normpath(bookdir)):
        items.append(f"book.json: id {cfg.get('id')!r} is not the directory name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(cfg.get("id", ""))):
        items.append("book.json: id must be lower-case words joined by hyphens")
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", str(cfg.get("date", ""))):
        items.append("book.json: date must be YYYY-MM-DD")
    if isinstance(cfg.get("year"), int) and cfg["year"] > 1913:
        items.append(f"book.json: year {cfg['year']} is not before 1914")
    if not (cfg.get("source") or {}).get("ia_identifier"):
        items.append("book.json: source.ia_identifier missing")
    if not any(h.get("version") == cfg.get("version") for h in cfg.get("history", [])):
        items.append("book.json: history has no entry for this version")
    for a in cfg.get("authors", []):
        if not a.get("name") or not a.get("sort"):
            items.append("book.json: each author needs name and sort")
    s = cfg.get("summary", "")
    s = " ".join(s) if isinstance(s, list) else s
    if s and not (30 <= len(s.split()) <= 220):
        items.append(f"book.json: summary has {len(s.split())} words (30–220 expected)")
    return items


def run_epubcheck(epub_path, jar):
    r = subprocess.run(["java", "-jar", jar, epub_path], capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r"Messages: (\d+) fatals? / (\d+) errors? / (\d+) warnings?", out)
    if m and m.groups() == ("0", "0", "0"):
        return []
    return [ln for ln in out.splitlines() if re.match(r"(FATAL|ERROR|WARNING)", ln)][:30] or [out.strip()[-300:] or "epubcheck gave no result"]


def run_soffice(odt_path, tmp):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        return ["LibreOffice (soffice) is not installed: cannot check the ODT"]
    r = subprocess.run([exe, "--headless", f"-env:UserInstallation=file://{tmp}/lo", "--convert-to", "pdf", "--outdir", tmp, odt_path],
                       capture_output=True, text=True, timeout=600)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(odt_path))[0] + ".pdf")
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 2000:
        return [f"LibreOffice did not convert the ODT: {(r.stdout + r.stderr).strip()[-200:]}"]
    return []


# ---------------------------------------------------------------- main

def run(bookdir, epubcheck=None, skip_epubcheck=False, skip_odt=False, verbose=False):
    bookdir = os.path.normpath(bookdir)
    cfg, pages = compile_book.load(bookdir)
    res = collections.OrderedDict((k, []) for k in CHECKS)
    skipped = []
    tmp = tempfile.mkdtemp(prefix="preflight-")
    try:
        book, warnings = build_site.build_book(tmp, bookdir)
        slug = book["id"]
        bdir = os.path.join(tmp, "books", slug)
        epub_path, odt_path = os.path.join(bdir, slug + ".epub"), os.path.join(bdir, slug + ".odt")
        res["meta"] = check_meta(cfg, bookdir)
        res["site-text"] = check_site_text(cfg)
        res["serial-commas"] = check_serial_commas(cfg)
        res["markup"] = check_markup(pages)
        res["accents"] = check_accents(pages)
        res["misprints"] = check_misprints(pages)
        res["missing-stop"] = check_missing_stop(pages)
        pub = os.path.join(os.path.dirname(HERE), "books")
        corpus = corpus_counts(pub)
        if os.path.normpath(os.path.dirname(bookdir)) == os.path.normpath(pub):
            corpus.subtract(w for _, w in _plain_words(pages))   # a published book is not counted twice
        res["rare-forms"] = check_rare_forms(pages, corpus)
        if not any(os.path.exists(os.path.join(bookdir, "images", f)) for f in ("cover.jpg", "cover.png")):
            res["cover"].append("images/cover.jpg is missing (the front cover if the title is clearly readable on it, otherwise the title page)")
        res["sc-caps"] = check_sc(pages)
        res["heading-caps"] = check_heading_caps(pages)
        res["hyphen-joins"] = triage_hyphen_joins([w for w in warnings if w.startswith("hyphen join")], pages)
        res["compile"] = [w for w in warnings if not w.startswith("hyphen join")]
        res["folios"] = check_folios(pages)
        res["leaves"] = check_leaves(pages, items=compile_book.scan_items(cfg.get("source") or {}))
        res["joins"] = check_joins(pages)
        res["note-tail"] = check_note_tail(pages)
        res["verse-joins"] = check_verse_joins(pages)
        res["caption-tail"] = check_caption_tail(pages)
        res["image-before-heading"] = check_image_before_heading(pages, set(cfg.get("ornaments") or []))
        # conservation
        pc, jc = [], []          # image captions apart: the compiler moves some images (see page_streams)
        ps, js = [], []          # side-notes: in the JSON, not in the reading editions
        pst, jst = [], []        # a second stream (compile_book.split_streams): moved after the other divisions
        pm, pn = page_streams(pages, captions=pc, sides=ps, streams=pst)
        jm, jn = json_streams(book, captions=jc, sides=js, streams=jst)
        res["conservation"] += compare(" ".join(pst), " ".join(jst), "pages→JSON second stream")
        res["conservation"] += compare(" ".join(ps), " ".join(js), "pages→JSON side-notes")
        res["conservation"] += compare(pm, jm, "pages→JSON text") + compare(pn, jn, "pages→JSON notes")
        res["conservation"] += compare(" ".join(sorted(pc, key=caption_key)), " ".join(sorted(jc, key=caption_key)), "pages→JSON captions")
        jm, jn = json_streams(book)
        rm, rn = json_streams(book, reading_only=True)
        names = rh.file_names(book, ".html")
        web = []
        for d in rh.reading_divisions(book):
            x = open(os.path.join(bdir, names[d["id"]]), encoding="utf-8").read()
            web.append(re.search(r'<article class="book">(.*)</article>', x, flags=re.S).group(1))
        wm, wn = html_streams(web)
        z = zipfile.ZipFile(epub_path)
        ep = []
        for d in rh.reading_divisions(book):
            x = z.read("OEBPS/text/" + names[d["id"]].replace(".html", ".xhtml")).decode("utf-8")
            ep.append(re.search(r"<section epub:type=[^>]*>(.*)</section>\s*</body>", x, flags=re.S).group(1))
        em, en = html_streams(ep)
        om, on = odt_streams(odt_path)
        res["conservation"] += compare(rm, wm, "JSON→web text") + compare(rn, wn, "JSON→web notes")
        res["conservation"] += compare(rm, em, "JSON→EPUB text") + compare(rn, en, "JSON→EPUB notes")
        res["conservation"] += compare(rm, om, "JSON→ODT text")
        if sorted(squash(inline.plain(n["text"])) for d in rh.reading_divisions(book) for n in d["notes"]) != \
                sorted(squash(x) for x in odt_notes(odt_path)):
            res["conservation"].append("JSON→ODT notes: the footnotes of the ODT are not the notes of the JSON")
        res["stray-markup"], res["straight-quotes"], _ = check_text(
            [("text", jm), ("notes", jn), ("web", wm + " " + wn), ("epub", em + " " + en), ("odt", om)])
        # the same item in all formats is one problem: keep the JSON ("text"/"notes") report when it exists
        for k in ("stray-markup", "straight-quotes"):
            base = [i for i in res[k] if i.startswith(("text:", "notes:"))]
            res[k] = base or res[k]
        res["spacing"] = spacing_items(book)
        res["quote-balance"] = check_quote_balance(book)
        res["image-splits"] = check_image_splits(book)
        res["contents"] = check_contents(book)
        res["title-page"] = check_title_page(book)
        res["links"] = check_links(tmp, slug, epub_path)
        res["wellformed"] = check_wellformed(tmp, slug, epub_path, odt_path)
        rd = rh.reading_divisions(book)
        if not rd:
            res["nav"].append("no division is in the reading editions")
        for d in rd:
            if not d["title"] or d["title"].startswith("[Untitled"):
                res["nav"].append(f"{d['id']} ({d['first_leaf']}): no title")
            if not d["blocks"]:
                res["nav"].append(f"{d['id']} ({d['first_leaf']}): empty")
        idir = os.path.join(bookdir, "images")
        if os.path.isdir(idir):
            used = {os.path.basename(b["src"]) for d in book["divisions"] for b in d["blocks"] if b["type"] == "image"} | {"cover.jpg", "cover.png"}
            used |= {os.path.basename(e["src"]) for e in book.get("editor_images", [])}      # render_html.editor_figures
            res["images"] = [f"images/{f} is not used" for f in sorted(os.listdir(idir)) if f not in used]
        a = cfg.get("audit") or {}
        if a.get("version") != cfg.get("version") or not a.get("pages") or "real_errors" not in a or "recall" not in a:
            res["audit"].append('book.json "audit" must record this version: {"version", "date", "pages", "recall", "real_errors", "fixed"}')
        sj = os.path.join(bookdir, "source.json")
        if not os.path.exists(sj):
            res["source"].append("no source.json")
        else:
            src = json.load(open(sj, encoding="utf-8"))
            missing = [p["name"] for p in src.get("parts", []) if not p.get("drive_id")]
            if not src.get("parts") or missing:
                res["source"].append(f"Drive cache incomplete: {len(missing)} parts without a drive_id" if src.get("parts") else "no parts recorded")
        if skip_epubcheck:
            skipped.append("epubcheck")
        else:
            jar = epubcheck or os.environ.get("EPUBCHECK_JAR")
            res["epubcheck"] = run_epubcheck(epub_path, jar) if jar and os.path.exists(jar) else ["epubcheck jar not found (set EPUBCHECK_JAR; tools/setup_env.sh installs it)"]
        if skip_odt:
            skipped.append("odt")
        else:
            res["odt"] = run_soffice(odt_path, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    waivers = cfg.get("waivers", [])
    used_w = [0] * len(waivers)
    waived = 0
    for k in res:
        keep = []
        for item in res[k]:
            w = next((i for i, w in enumerate(waivers) if w.get("check") == k and w.get("match", "") in item and w.get("why")), None)
            if w is None:
                keep.append(item)
            else:
                used_w[w] += 1
                waived += 1
        res[k] = keep
    lines, fails, observed = [], 0, []
    for k, (mode, what) in CHECKS.items():
        n = len(res[k])
        if k in skipped:
            status = "SKIPPED"
        elif mode == "enforce":
            status = "ok" if n == 0 else f"FAIL ({n})"
            fails += n
        else:
            status = "ok" if n == 0 else f"look ({n})"
            if n:
                observed.append(f"{k} {n}")
        lines.append(f"[{status:>9}] {k}: {what}")
        show = res[k] if (verbose or mode == "enforce") else res[k][:40]
        lines += [f"            - {i}" for i in show]
        if len(show) < n:
            lines.append(f"            … {n - len(show)} more (-v)")
    for i, w in enumerate(waivers):
        if not used_w[i]:
            lines.append(f"[   unused] waiver matches nothing: {w}")
        if not w.get("why"):
            lines.append(f"[  invalid] waiver without a reason: {w}")
    try:
        rev = subprocess.run(["git", "-C", HERE, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "?"
    except Exception:
        rev = "?"
    verdict = "PASS" if fails == 0 and not skipped else ("FAIL" if fails else "INCOMPLETE")
    stamp = (f"preflight {verdict}: {cfg.get('id')} v{cfg.get('version')} — {fails} to fix, {waived} waived"
             f"{'; skipped: ' + ', '.join(skipped) if skipped else ''}"
             f"{'; to look at: ' + ', '.join(observed) if observed else ''} — tools@{rev} {datetime.date.today().isoformat()}")
    lines.append(stamp)
    return verdict, "\n".join(lines), res


def odt_notes(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("content.xml"))
    out = []
    for n in root.iter(T + "note"):
        out.append("".join(n.find(T + "note-body").itertext()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bookdir")
    ap.add_argument("--epubcheck")
    ap.add_argument("--skip-epubcheck", action="store_true", help="tests only: the result is then INCOMPLETE, never PASS")
    ap.add_argument("--skip-odt", action="store_true", help="tests only")
    ap.add_argument("--report")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()
    verdict, report, _ = run(a.bookdir, a.epubcheck, a.skip_epubcheck, a.skip_odt, a.v)
    print(report)
    if a.report:
        open(a.report, "w", encoding="utf-8").write(report + "\n")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
