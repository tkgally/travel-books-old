#!/usr/bin/env python3
"""Compile a book's page files and book.json into the book JSON (the base for EPUB, ODT and HTML).

  compile_book.py BOOKDIR [-o OUT.json]

BOOKDIR holds book.json, pages/pNNNN.txt (page markup, notes/page-markup.md) and images/.
From Python: compile_book(bookdir) -> (dict, warnings).

book.json keys used here (all keys: notes/book-json.md):
  id, version, date, title, ... bibliographic fields, copied through
  divisions     exceptions to "every # heading starts a chapter that is in the reading editions":
                [{"at": "p0013", "kind": "contents", "reading": false, "title": "Contents"}, ...]
                `at` = the page the division starts on. If there is no # heading on that page a division
                boundary is made at the top of the page (its title: `title`, or the kind).
                `n` (default 1) picks the n-th division starting on that page.
  keep_hyphens  pages whose join with the previous page keeps the page-final hyphen
  toc           {"subtitles": "all"}: every division whose summary was too long for its title gets `toc_title`
  toc_entries   [{"at": leaf, "starts": plain text, "title": ..., "editor": bool}] -> division `sections`

The title page (kind "titlepage") is the first division of the reading editions (Tom, 2026-11-22): divisions
before it (half-title, advertisements) are left out of them whatever book.json says. A long division with
`sections` gets "split": true: the reading editions give each section a page of its own (SPLIT_CHARS; a
`divisions` entry may say "split": true or false). The JSON keeps the division whole.
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inline  # noqa: E402

FORMAT = "travel-books-json/1"
KINDS = ("front", "titlepage", "dedication", "preface", "contents", "illustrations", "introduction", "part",
         "chapter", "appendix", "notes", "glossary", "index", "errata", "advertisements", "back")
MARK = re.compile(r"\[\[(?:page [^\[\]]*|blank|break|cont|stream|right|center|subtitle|caption|image:[^\[\]]*|fn [^\[\]]+|"
                  r"fnref [^\[\]]+|corr [^|\[\]]*\|[^\[\]]*|side:[^\[\]]*|supplied [^\[\]]+|gap)\]\]")
BLOCK_TAGS = ("blockquote", "verse")
NOT_READING = ("front", "contents", "illustrations", "index", "advertisements", "back", "errata")
SPLIT_CHARS = 50000     # a reading division with sections and more plain text than this is split at them


def page_files_sorted(names):
    """Page files in leaf order: p2029, p2029a, p2029b (leaves added from another scan, book.json
    source.extra_leaves), p2030."""
    return sorted(f for f in names if re.fullmatch(r"p\d+[a-z]?\.txt", f))


def page_files(pdir):
    return page_files_sorted(os.listdir(pdir))


def split_row(r):
    """A table row's cells; a | inside [[…]] (a [[corr printed|corrected]]) does not split a cell."""
    cells, cur, depth, i, r = [], "", 0, 0, r.strip()[1:-1] if r.strip().endswith("|") else r.strip()[1:]
    while i < len(r):
        if r.startswith("[[", i):
            depth += 1; cur += "[["; i += 2; continue
        if r.startswith("]]", i) and depth:
            depth -= 1; cur += "]]"; i += 2; continue
        if r[i] == "|" and not depth:
            cells.append(cur.strip()); cur = ""
        else:
            cur += r[i]
        i += 1
    cells.append(cur.strip())
    return cells


def parse_page(text, leaf):
    """One page file -> (printed number, blank?, list of raw blocks)."""
    lines = text.splitlines()
    number, blank, blocks, img_n = "", False, [], 0
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        i += 1
        m = re.fullmatch(r"\[\[page ([^\]]*)\]\]", s)
        if m:
            number = "" if m.group(1).strip() == "?" else m.group(1).strip()
            continue
        if s == "[[blank]]":
            blank = True
            continue
        if not s:
            continue
        m = re.match(r"<(blockquote|verse)>", s)
        if m:
            kind = m.group(1)
            rest = s[len(kind) + 2:]
            inner, closed = [], False
            if f"</{kind}>" in rest:
                inner, closed = [rest.replace(f"</{kind}>", "")], True
            elif rest.strip():
                inner = [rest]
            while not closed and i < len(lines):
                x = lines[i].rstrip()
                i += 1
                if f"</{kind}>" in x:
                    closed = True
                    x = x.replace(f"</{kind}>", "")
                    if not x.strip():
                        break
                inner.append(x)
            inner = [x.strip() for x in inner]
            while inner and not inner[0]:
                inner.pop(0)
            while inner and not inner[-1]:
                inner.pop()
            cont = bool(inner) and inner[0].startswith("[[cont]]")
            if cont:
                inner[0] = inner[0][8:].strip()
            if kind == "blockquote":
                inner = [x for x in inner if x]
            blocks.append({"t": "quote" if kind == "blockquote" else "verse", "lines": inner, "cont": cont, "closed": closed})
            continue
        m = re.match(r"\[\[image:\s*(.*?)\]\]$", s)
        if m:
            img_n += 1
            blocks.append({"t": "image", "alt": m.group(1), "file": f"{leaf}-{img_n}"})
            continue
        if s.startswith("[[caption]]"):
            blocks.append({"t": "caption", "text": s[11:].strip()})
            continue
        m = re.match(r"\[\[fn ([^\]]+)\]\]\s*(.*)", s)
        if m:
            blocks.append({"t": "fn", "mark": m.group(1).strip(), "text": m.group(2)})
            continue
        m = re.match(r"(#{1,3}) (.*)", s)
        if m:
            blocks.append({"t": "h", "level": len(m.group(1)), "text": m.group(2).strip()})
            continue
        if s.startswith("|") and s.endswith("|") and len(s) > 1:
            rows = [s]
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            rows = [split_row(r) for r in rows if not re.fullmatch(r"\|[-| :]+\|", r)]
            blocks.append({"t": "table", "rows": rows})
            continue
        if s == "[[break]]":
            blocks.append({"t": "break"})
            continue
        b = {"t": "p"}
        if s.startswith("[[subtitle]]"):
            b["role"], s = "subtitle", s[12:].strip()
        elif s.startswith("[[right]]"):
            b["align"], s = "right", s[9:].strip()
        elif s.startswith("[[center]]"):
            b["align"], s = "center", s[10:].strip()
        if s.startswith("[[cont]]"):
            b["cont"], s = True, s[8:].strip()
        b["text"] = s
        blocks.append(b)
    return number, blank, blocks


def no_side(text):
    """Text without its side-notes (for messages that quote the words of a join)."""
    return re.sub(r"\[\[side:[^\[\]]*\]\]\s*", "", text)


def pbtok(leaf, number):
    return f"⟦pb:{leaf}:{number}⟧"


def join_text(prev, text, leaf, number, keep, warn, what=""):
    tok = pbtok(leaf, number)
    if prev.endswith("-"):
        if leaf in keep:
            return prev + tok + text
        warn(f"hyphen join{what} at {leaf}: …{prev[-15:]}|{no_side(text)[:15]}… (hyphen removed; check)")
        return prev[:-1] + tok + text
    if prev.endswith("—") or text.startswith("—"):
        return prev + tok + text
    return prev + " " + tok + text


def scan_items(src):
    """The IA items a book's leaves come from: [(first leaf number, identifier, hidden leaves)], last first.
    One item: leaf pNNNN is IA's leaf NNNN. Several (a work in volumes, book.json source.items): the leaves of
    the item whose "first_leaf" is p2000 are p2000, p2001 … for IA's leaves 0, 1 …"""
    items = src.get("items") or ([{"ia_identifier": src["ia_identifier"], "first_leaf": "p0000",
                                   "hidden_leaves": src.get("hidden_leaves", [])}] if src.get("ia_identifier") else [])
    out = [(int(re.search(r"\d+", it.get("first_leaf", "p0000")).group(0)), it["ia_identifier"], [int(h) for h in it.get("hidden_leaves", [])])
           for it in items]
    return sorted(out, reverse=True)


def apply_leaf_order(pages, orders):
    """book.json "leaf_order": [["p1469", "p1470", "p1467", "p1468"], …]: leaves bound out of order in the scanned
    copy are read in the order given, in the places the same leaves hold in the scan."""
    pages = list(pages)
    idx = {leaf: i for i, (leaf, _) in enumerate(pages)}
    for order in orders or []:
        missing = [x for x in order if x not in idx]
        if missing:
            raise ValueError(f"leaf_order: no page file for {missing}")
        slots = sorted(idx[x] for x in order)
        moved = [pages[idx[x]] for x in order]
        for i, pg in zip(slots, moved):
            pages[i] = pg
        idx = {leaf: i for i, (leaf, _) in enumerate(pages)}
    return pages


def load(bookdir):
    cfg = json.load(open(os.path.join(bookdir, "book.json"), encoding="utf-8"))
    pdir = os.path.join(bookdir, "pages")
    pages = [(f[:-4], open(os.path.join(pdir, f), encoding="utf-8").read()) for f in page_files(pdir)]
    return cfg, apply_leaf_order(pages, cfg.get("leaf_order"))


def split_streams(pages):
    """A second stream of text printed on the same pages apart from the main text (Reeves, *Brown Men and Women*:
    “Excerpts from Tongan Official Documents” in small type along the foot of pp. 268–286, under the main text):
    each of its lines in the page files starts `[[stream]]` (then any one-line markup: `# ` heading, `[[cont]]`).
    Returns (main pages, stream pages), the stream pages with the page's `[[page N]]` and only the stream lines."""
    main, stream = [], []
    for leaf, text in pages:
        keep, st = [], []
        for ln in text.splitlines():
            if ln.lstrip().startswith("[[stream]]"):
                st.append(ln.lstrip()[10:].strip())
            else:
                keep.append(ln)
        main.append((leaf, "\n".join(keep)))
        if st:
            m = re.search(r"\[\[page [^\]]*\]\]", text)
            stream.append((leaf, (m.group(0) if m else "[[page ?]]") + "\n\n" + "\n\n".join(st)))
    return main, stream


def compile_pages(cfg, pages, images=None):
    """cfg = book.json dict, pages = [(leaf, text)], images = {stem: filename} or None (then not checked).
    The lines of a second stream (split_streams) become division(s) of their own, marked "stream": true, after all the
    others: in the reading editions they follow the last reading division (book.json "stream_kind", default
    "appendix", is the kind of the stream's first division)."""
    main, stream = split_streams(pages)
    book, warnings = _compile_pages(cfg, main, images)
    if not stream:
        return book, warnings
    scfg = {k: cfg[k] for k in ("id", "version", "date", "title", "authors", "keep_hyphens", "ornaments") if k in cfg}
    scfg["divisions"] = [{"at": stream[0][0], "kind": cfg.get("stream_kind", "appendix")}]
    sub, sw = _compile_pages(scfg, stream, images)
    warnings += [f"{w} (second stream)" for w in sw]
    n0 = len(book["divisions"])
    ren = lambda x: re.sub(r"\bd(\d{3})\b", lambda m: f"d{int(m.group(1)) + n0:03d}", x)
    sdivs = json.loads(ren(json.dumps(sub["divisions"], ensure_ascii=False)))
    for d in sdivs:
        d["stream"] = True
    book["divisions"] += sdivs
    book["corrections"] += [dict(c, division=ren(c["division"])) for c in sub["corrections"]]
    return book, warnings


def _compile_pages(cfg, pages, images=None):
    """cfg = book.json dict, pages = [(leaf, text)], images = {stem: filename} or None (then not checked).
    Returns (book dict, warnings)."""
    warnings = []
    warn = warnings.append
    keep = set(cfg.get("keep_hyphens", []))
    flat, page_list = [], []
    for leaf, text in pages:
        number, blank, raw = parse_page(text, leaf)
        page_list.append({"leaf": leaf, "number": number, "blank": blank or not raw})
        first = True
        for b in raw:
            b["leaf"] = leaf
            if b["t"] == "fn":
                if b["mark"] == "cont":
                    prevfn = next((x for x in reversed(flat) if x["t"] == "fn"), None)
                    if prevfn is None:
                        warn(f"[[fn cont]] with no earlier note: {leaf}")
                    else:
                        prevfn["text"] = join_text(prevfn["text"], b["text"], leaf, number, keep, warn, " in a note")
                    continue
                flat.append(b)
                continue
            if b["t"] == "caption":
                img = flat[-1] if flat and flat[-1]["t"] == "image" else None
                if img is None:
                    warn(f"[[caption]] not after an image, kept as a centred line: {leaf} {b['text'][:40]!r}")
                    flat.append({"t": "p", "text": b["text"], "align": "center", "leaf": leaf, "pb": []})
                else:
                    img["caption"] = (img.get("caption", "") + " " + b["text"]).strip()
                continue
            if first:
                first = False
                if b.get("cont"):
                    j = len(flat) - 1
                    while j >= 0 and flat[j]["t"] in ("fn", "image", "break"):
                        j -= 1
                    prev = flat[j] if j >= 0 else None
                    if b["t"] == "p" and prev is not None and prev["t"] == "p" and prev["leaf_end"] != leaf:
                        prev["text"] = join_text(prev["text"], b["text"], leaf, number, keep, warn)
                        prev["leaf_end"] = leaf
                        continue
                    if b["t"] in ("quote", "verse") and prev is not None and prev["t"] == b["t"] and prev["leaf_end"] != leaf:
                        open_para = b["t"] == "quote" and not re.search(r"[.?!][”’\")\]]*$", re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", prev["lines"][-1]).strip())
                        if prev["lines"] and b["lines"] and (open_para or prev["lines"][-1].endswith("-")):
                            what = " in a quotation" if b["t"] == "quote" else " in verse"
                            prev["lines"][-1] = join_text(prev["lines"][-1], b["lines"][0], leaf, number, keep, warn, what)
                            prev["lines"] += b["lines"][1:]
                        else:
                            if b["lines"]:
                                b["lines"][0] = pbtok(leaf, number) + b["lines"][0]
                            prev["lines"] += ([""] if b["t"] == "verse" and b.get("stanza_break") else []) + b["lines"]
                        prev["leaf_end"] = leaf
                        continue
                    warn(f"[[cont]] with nothing to continue, treated as a new block: {leaf}")
                b["pb"] = [{"leaf": leaf, "n": number}]
            elif b.get("cont"):
                # a paragraph interrupted by a picture in the middle of the page (South by West, 2026-11-19):
                # join it to the paragraph before the picture, which then follows the paragraph
                j = len(flat) - 1
                while j >= 0 and flat[j]["t"] in ("fn", "image", "break"):
                    j -= 1
                prev = flat[j] if j >= 0 else None
                if (b["t"] == "p" and any(x["t"] == "image" and x["leaf"] == leaf for x in flat[j + 1:])
                        and prev is not None and prev["t"] == "p" and prev["leaf_end"] == leaf):
                    if prev["text"].endswith("-") and leaf not in keep:
                        warn(f"hyphen join around an image at {leaf}: …{prev['text'][-15:]}|{no_side(b['text'])[:15]}… (hyphen removed; check)")
                        prev["text"] = prev["text"][:-1] + b["text"]
                    elif prev["text"].endswith(("-", "—")) or b["text"].startswith("—"):
                        prev["text"] += b["text"]
                    else:
                        prev["text"] += " " + b["text"]
                    continue
                warn(f"[[cont]] not at the top of a page, dropped: {leaf}")
            b.setdefault("pb", [])
            b["leaf_end"] = leaf
            flat.append(b)

    # divisions
    toc_cfg = cfg.get("toc") or {}
    overrides = {}
    for d in cfg.get("divisions", []):
        overrides[(d["at"], d.get("n", 1))] = d
    h1_leaves = {b["leaf"] for b in flat if b["t"] == "h" and b["level"] == 1}
    forced = {d["at"] for d in cfg.get("divisions", [])} - h1_leaves
    divs, cur, count_at = [], None, {}
    ornaments = set(cfg.get("ornaments", []))   # decorative head- and tail-pieces: shown small (Tom, 2026-11-20)

    def start(leaf, title, from_heading):
        nonlocal cur
        count_at[leaf] = count_at.get(leaf, 0) + 1
        o = overrides.get((leaf, count_at[leaf]), {})
        used.add((leaf, count_at[leaf]))
        kind = o.get("kind", "chapter" if from_heading else "front")
        if kind not in KINDS:
            warn(f"unknown division kind {kind!r} at {leaf}")
        if kind == "titlepage":      # whatever heading the page has, the division is called "Title Page"
            title, from_heading = o.get("title") or "Title Page", False
        cur = {"id": f"d{len(divs) + 1:03d}", "kind": kind, "title": o.get("title") or title or (None if from_heading else kind.capitalize()),
               "reading": o.get("reading", kind not in NOT_READING),
               "first_leaf": leaf, "blocks": [], "notes": [], "_fns": [], "_auto_title": not o.get("title") and kind != "titlepage",
               "_toc_title": o.get("toc_title"), "_split": o.get("split")}
        divs.append(cur)

    used = set()
    seen_leaf_start = set()
    for b in flat:
        leaf = b["leaf"]
        if b["t"] == "h" and b["level"] == 1:
            # a head-piece (book.json "ornaments") printed just above the heading opens the new division
            moved = []
            while cur is not None and cur["blocks"] and cur["blocks"][-1]["t"] == "image" \
                    and cur["blocks"][-1]["file"] in ornaments and cur["blocks"][-1]["leaf"] == leaf:
                moved.insert(0, cur["blocks"].pop())
            start(leaf, None, True)
            seen_leaf_start.add(leaf)
            cur["blocks"].extend(moved)
        elif cur is None:
            start(leaf, "Front matter", False)
            seen_leaf_start.add(leaf)
        elif leaf in forced and leaf not in seen_leaf_start and b["t"] != "fn":
            seen_leaf_start.add(leaf)
            start(leaf, None, False)
        if b["t"] == "fn":
            cur["_fns"].append(b)
        else:
            cur["blocks"].append(b)
    for k in overrides:
        if k not in used:
            warn(f"book.json divisions entry matches no division start: at {k[0]} n {k[1]}")

    # the title page opens the reading editions: what stands before it is left out (Tom, 2026-11-22)
    tp = next((i for i, d in enumerate(divs) if d["kind"] == "titlepage" and d["reading"]), None)
    for d in divs[:tp or 0]:
        if d["reading"]:
            warn(f"division {d['id']} ({d['first_leaf']}, {d['kind']}) stands before the title page: left out of the reading editions")
            d["reading"] = False

    def conv(text, leaf):
        return inline.convert(text, warn, leaf)

    for d in divs:
        out = []
        for b in d["blocks"]:
            t = b["t"]
            nb = {"leaf": b["leaf"]}
            if b.get("pb"):
                nb["pb"] = b["pb"]
            if t == "h":
                nb.update(type="heading", level=b["level"], text=conv(b["text"], b["leaf"]))
            elif t == "p":
                nb.update(type="paragraph", text=conv(b["text"], b["leaf"]))
                for k in ("align", "role"):
                    if b.get(k):
                        nb[k] = b[k]
            elif t == "quote":
                paras = []
                for x in b["lines"]:
                    if x.startswith("[[right]]"):
                        paras.append({"text": conv(x[9:].strip(), b["leaf"]), "align": "right"})
                    elif x.startswith("[[center]]"):
                        paras.append({"text": conv(x[10:].strip(), b["leaf"]), "align": "center"})
                    else:
                        paras.append({"text": conv(x, b["leaf"])})
                nb.update(type="quote", paragraphs=paras)
            elif t == "verse":
                stanzas, cur_st = [], []
                for x in b["lines"]:
                    if not x:
                        if cur_st:
                            stanzas.append(cur_st)
                        cur_st = []
                    else:
                        cur_st.append(conv(x, b["leaf"]))
                if cur_st:
                    stanzas.append(cur_st)
                nb.update(type="verse", stanzas=stanzas)
            elif t == "image":
                f = (images or {}).get(b["file"])
                if images is not None and not f:
                    warn(f"missing image file for {b['file']} ({b['alt']})")
                nb.update(type="image", src="images/" + (f or b["file"] + ".jpg"), alt=inline.smart_quotes(b["alt"]))
                if b["file"] in ornaments:
                    nb["ornament"] = True
                if b.get("caption"):
                    nb["caption"] = conv(b["caption"], b["leaf"])
            elif t == "table":
                nb.update(type="table", rows=[[conv(c, b["leaf"]) for c in r] for r in b["rows"]])
            elif t == "break":
                nb.update(type="break")
            out.append(nb)
        d["blocks"] = out
        # notes: the k-th reference with a mark pairs with the k-th note with that mark in the division
        notes, count = [], {}
        for f in d.pop("_fns"):
            count[f["mark"]] = count.get(f["mark"], 0) + 1
            notes.append({"id": f"{d['id']}-n{len(notes) + 1}", "mark": f["mark"], "k": count[f["mark"]],
                          "leaf": f["leaf"], "text": conv(f["text"], f["leaf"])})
        refcount = {}

        def resolve(m):
            mark = inline.html.unescape(m.group(1))
            again = mark.endswith(" again")  # [[fnref * again]]: one more reference to the previous note with that mark
            if again:
                mark = mark[:-len(" again")].strip()
            else:
                refcount[mark] = refcount.get(mark, 0) + 1
            n = next((x for x in notes if x["mark"] == mark and x["k"] == refcount.get(mark, 0)), None)
            if n is None:
                warn(f"note reference {mark!r} (occurrence {refcount.get(mark, 0)}{', again' if again else ''}) has no note in division {d['id']} ({d['first_leaf']}…)")
                return f"<sup>{inline.html.escape(mark)}</sup>"
            n["_ref"] = True
            return f'<noteref to="{n["id"]}">{inline.html.escape(mark)}</noteref>'

        def walk(x):
            if isinstance(x, str):
                return re.sub(r'<noteref mark="([^"]*)"/>', resolve, x)
            if isinstance(x, list):
                return [walk(y) for y in x]
            if isinstance(x, dict):
                return {k: (walk(v) if k in ("text", "paragraphs", "stanzas", "rows", "caption") else v) for k, v in x.items()}
            return x
        d["blocks"] = walk(d["blocks"])
        for n in notes:
            n["text"] = re.sub(r'<noteref mark="([^"]*)"/>', lambda m: f"<sup>{m.group(1)}</sup>", n["text"])
            if not n.pop("_ref", False):
                warn(f"note {n['mark']!r} on {n['leaf']} has no reference in division {d['id']}")
            del n["k"]
        d["notes"] = notes
        # title
        if d.pop("_auto_title") and not d["title"]:
            h = next((b for b in d["blocks"] if b["type"] == "heading" and b["level"] == 1), None)
            t = inline.plain(h["text"]).strip() if h else ""
            i = d["blocks"].index(h) + 1 if h else 0
            whole = t
            if h and i < len(d["blocks"]) and d["blocks"][i].get("role") == "subtitle":
                sub = inline.plain(d["blocks"][i]["text"]).strip()
                whole = t.rstrip(".") + ". " + sub
                # with "toc": {"subtitles": "all"} every title stays the heading alone, so that the pager and page
                # titles are alike (*Caucasus*, *Jaunt in Japan*, *Sailor's Visit*: short summaries had gone into
                # some titles and long ones not; review 2026-11-21)
                if len(sub) <= 80 and toc_cfg.get("subtitles") != "all":
                    t = whole
            d["title"] = t.rstrip(".") if t else f"[Untitled, {d['first_leaf']}]"
            # book.json "toc": {"subtitles": "all"}: the contents show every chapter summary in full, so that the
            # entries are alike (Sketches Awheel, 2026-11-19); the title (pager, page title) stays short
            if toc_cfg.get("subtitles") == "all" and t and whole.rstrip(".") != d["title"]:
                d["toc_title"] = whole.rstrip(".")
        if d.get("_toc_title"):
            d["toc_title"] = d["_toc_title"]
        d.pop("_toc_title", None)
        # a division with only a heading and its subtitle is a part title (Flying Leaves: "From the East")
        if not any(b["type"] in ("paragraph", "quote", "verse", "table", "image") and b.get("role") != "subtitle"
                   for b in d["blocks"]) and d["kind"] == "chapter":
            d["kind"] = "part" if cfg.get("auto_parts", True) else d["kind"]

    # frontispiece (book.json "frontispiece": "p0010-1"): the image is moved from the front matter to the start of
    # the first reading division, so the reading editions show it (style.md, "What goes where")
    # A list (one per volume of a work in several volumes): each goes to the first reading division after it.
    fronts = cfg.get("frontispiece") or []
    for fr in ([fronts] if isinstance(fronts, str) else fronts):
        want = "images/" + (images or {}).get(fr, fr + ".jpg")
        src = next(((i, d, b) for i, d in enumerate(divs) if not d["reading"] for b in d["blocks"]
                    if b["type"] == "image" and b["src"] == want), None)
        first = None if src is None else next((d for d in divs[src[0]:] if d["reading"]), None)
        if first is None:
            # an image already in the reading editions (on the title page, now their first page) stays where it is
            if not any(b["type"] == "image" and b["src"] == want for d in divs if d["reading"] for b in d["blocks"]):
                warn(f"frontispiece {fr!r}: no such image outside the reading divisions")
        else:
            src[1]["blocks"].remove(src[2])
            at = 0
            if first["kind"] == "titlepage" and first["blocks"]:
                # on the title page the picture follows the title page's own text (its first leaf), before the verso
                lf = first["blocks"][0]["leaf"]
                at = max(i for i, b in enumerate(first["blocks"]) if b["leaf"] == lf) + 1
            first["blocks"].insert(at, src[2])

    # entries of the contents inside a division (book.json "toc_entries", notes/book-json.md): the printed contents'
    # titles of sections whose headings are shorter, or the editor's own entries (spans of dates and places in a
    # diary). Each points at the block that starts on page `at` with the plain text `starts`.
    for e in cfg.get("toc_entries", []):
        hit = None
        for d in divs:
            for i, b in enumerate(d["blocks"]):
                if b["leaf"] == e["at"] and inline.plain(b_text(b)).strip().startswith(e["starts"]):
                    hit = (d, i)
                    break
            if hit:
                break
        if hit is None:
            warn(f"toc_entries: no block on {e['at']} starts with {e['starts']!r}")
            continue
        d, i = hit
        if not d["reading"]:
            warn(f"toc_entries: {e['at']} {e['starts']!r} is in a division left out of the reading editions")
        d.setdefault("sections", []).append({"title": e["title"], "block": i, "editor": e.get("editor", True)})
    for d in divs:
        want = d.pop("_split", None)
        if d.get("sections"):
            d["sections"].sort(key=lambda x: x["block"])
            if len({x["block"] for x in d["sections"]}) < len(d["sections"]):
                warn(f"toc_entries: two entries point at the same block in division {d['id']}")
            size = sum(len(inline.plain(x)) for b in d["blocks"] for x in strings(b))
            if d["reading"] and (want if want is not None else size > SPLIT_CHARS and len(d["sections"]) > 1):
                d["split"] = True
        elif want:
            warn(f"book.json divisions: \"split\" at {d['first_leaf']}, but the division has no toc_entries")

    leaf_div = {}
    for d in divs:
        for b in d["blocks"]:
            leaf_div.setdefault(b["leaf"], d["id"])
            for m in re.finditer(r'<pb n="[^"]*" leaf="([^"]+)"/>', json.dumps(b, ensure_ascii=False).replace('\\"', '"')):
                leaf_div.setdefault(m.group(1), d["id"])
    for p in page_list:
        if p["leaf"] in leaf_div:
            p["division"] = leaf_div[p["leaf"]]

    corrections = []

    def collect(x, leaf, div):
        if isinstance(x, str):
            for m in re.finditer(r'<corr orig="([^"]*)">(.*?)</corr>', x):
                pbs = re.findall(r'<pb n="[^"]*" leaf="([^"]+)"/>', x[:m.start()])
                corrections.append({"leaf": pbs[-1] if pbs else leaf, "division": div,
                                    "printed": inline.html.unescape(m.group(1)), "corrected": inline.plain(m.group(2))})
        elif isinstance(x, list):
            for y in x:
                collect(y, leaf, div)
        elif isinstance(x, dict):
            for k in ("text", "paragraphs", "stanzas", "rows", "caption"):
                if k in x:
                    collect(x[k], x.get("leaf", leaf), div)
    for d in divs:
        for b in d["blocks"] + d["notes"]:
            collect(b, b["leaf"], d["id"])
    meta_keys = ("title", "subtitle", "short_title", "authors", "author_note", "publisher", "place", "year", "edition_statement",
                 "volumes", "language", "regions", "period", "subjects", "collection", "summary", "source", "notes_on_text",
                 "omitted_from_reading", "history", "body_start")
    book = {"format": FORMAT, "id": cfg["id"], "version": cfg["version"], "date": cfg["date"],
            "license": "CC0-1.0",
            "license_note": "This transcription and its markup are dedicated to the public domain (CC0 1.0). "
                            "The book itself was published before 1914.",
            **{k: cfg[k] for k in meta_keys if k in cfg},
            "corrections": corrections, "pages": page_list, "divisions": divs}
    # pictures added by the editor (book.json "editor_images"; Tom, 2026-11-22, *Surface Japan*: a typical printed
    # page with its decorated border, which the text leaves out). Not the book's: kept apart from the divisions, with
    # the caption written for this edition; the renderers show them before the start of the narrative.
    eds = []
    for e in cfg.get("editor_images", []):
        f = (images or {}).get(e["file"])
        if images is not None and not f:
            warn(f"editor_images: missing image file for {e['file']}")
        eds.append({"src": "images/" + (f or e["file"] + ".jpg"), "leaf": e["leaf"], "alt": inline.smart_quotes(e["alt"]),
                    "caption": inline.smart_quotes(e["caption"]), "editor": True})
    if eds:
        book["editor_images"] = eds
    return book, warnings


def strings(x):
    """Every inline string of a block or note, in reading order."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from strings(y)
    elif isinstance(x, dict):
        for k in ("text", "paragraphs", "stanzas", "rows", "caption"):
            if k in x:
                yield from strings(x[k])


def b_text(b):
    """The first text of a block (for matching a toc entry)."""
    if b.get("text"):
        return b["text"]
    if b.get("paragraphs"):
        return b["paragraphs"][0]["text"]
    if b.get("stanzas"):
        return b["stanzas"][0][0]
    if b.get("caption"):
        return b["caption"]
    return ""


def compile_book(bookdir):
    cfg, pages = load(bookdir)
    idir = os.path.join(bookdir, "images")
    images = {os.path.splitext(f)[0]: f for f in sorted(os.listdir(idir))} if os.path.isdir(idir) else {}
    return compile_pages(cfg, pages, images)


def dumps(book):
    return json.dumps(book, ensure_ascii=False, indent=1) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bookdir")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    book, warnings = compile_book(a.bookdir)
    out = a.out or os.path.join(a.bookdir, book["id"] + ".json")
    open(out, "w", encoding="utf-8").write(dumps(book))
    print(f"wrote {out}: {len(book['divisions'])} divisions, {len(book['pages'])} pages, {len(warnings)} warnings")
    for w in warnings:
        print("  WARN", w, file=sys.stderr)


if __name__ == "__main__":
    main()
