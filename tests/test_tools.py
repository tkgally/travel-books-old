"""Regression tests for the tools. A few seconds, no model calls, no network. Invented text only.

Run: tools/run_tests.sh        Rules (CLAUDE.md): run before trusting the tools in a session and after any
edit under tools/; every tool bug fixed gets a test here in the same commit; a test is never loosened to
get a book published.
"""
import copy, json, os, re, shutil, subprocess, sys, tempfile, unittest, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import build_site, carousel, compile_book, ledger, running_quotes, corrections, crop_image, drive_cache, inline, judge, normalize, preflight, render_epub, render_odt, review, session_meter  # noqa: E402
import render_html as rh  # noqa: E402

SAMPLE = os.path.join(REPO, "tests", "sample")
CFG = {"id": "t", "version": 1, "date": "2026-01-01", "title": "T", "authors": [{"name": "A", "sort": "A"}]}


def comp(pages, **cfg):
    c = dict(CFG, **cfg)
    return compile_book.compile_pages(c, [(f"p{i:04d}", t) for i, t in enumerate(pages, 1)])


def texts(book):
    return [s for d in book["divisions"] for b in d["blocks"] for s in rh.strings(b)]


class Quotes(unittest.TestCase):
    def test_curly(self):
        self.assertEqual(inline.smart_quotes('"Yes," he said, \'tis so; don\'t.'), "“Yes,” he said, ’tis so; don’t.")
        self.assertEqual(inline.smart_quotes("called 'a little damp.'"), "called ‘a little damp.’")
        self.assertEqual(inline.smart_quotes("<i>Paul</i>'s"), "<i>Paul</i>’s")

    def test_markup_untouched(self):
        self.assertEqual(inline.smart_quotes('[[fnref *]] "a"'), "[[fnref *]] “a”")


class Inline(unittest.TestCase):
    def test_convert(self):
        w = []
        s = inline.convert('A & B <i>c</i> [[corr teh|the]] p. <pref>34</pref>[[fnref *]]', w.append)
        self.assertEqual(s, 'A &amp; B <i>c</i> <corr orig="teh">the</corr> p. <pageref n="34">34</pageref><noteref mark="*"/>')
        self.assertEqual(w, [])

    def test_unbalanced_stripped(self):
        w = []
        self.assertEqual(inline.convert("a <i>b", w.append), "a b")
        self.assertEqual(len(w), 1)

    def test_plain(self):
        s = 'x <corr orig="teh">the</corr> <pb n="2" leaf="p0002"/>y<noteref to="d1-n1">*</noteref>'
        self.assertEqual(inline.plain(s), "x the y")
        self.assertEqual(inline.plain(s, corrected=False), "x teh y")


class Compile(unittest.TestCase):
    def test_join_and_hyphen(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nThe road was with-", "[[page 2]]\n[[cont]]out end, and long", "[[page 3]]\n[[cont]]as well."])
        t = texts(book)
        self.assertEqual(t[1], 'The road was with<pb n="2" leaf="p0002"/>out end, and long <pb n="3" leaf="p0003"/>as well.')
        self.assertEqual(len([x for x in w if x.startswith("hyphen join")]), 1)

    def test_keep_hyphen(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nat the water-", "[[page 2]]\n[[cont]]side."], keep_hyphens=["p0002"])
        self.assertIn('water-<pb n="2" leaf="p0002"/>side.', texts(book)[1])
        self.assertEqual(w, [])

    def test_dash_join_has_no_space(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nHe stopped—", "[[page 2]]\n[[cont]]then went on."])
        self.assertIn('stopped—<pb n="2" leaf="p0002"/>then', texts(book)[1])

    def test_cont_skips_notes_and_images(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nIt began[[fnref *]] and\n\n[[fn *]] A note.", "[[page ?]]\n[[image: a map]]",
                        "[[page 3]]\n[[cont]]went on."])
        self.assertIn("and <pb", texts(book)[1])
        self.assertTrue(texts(book)[1].endswith("went on."))
        self.assertEqual(w, [])

    def test_notes_pair_by_occurrence(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b.\n\n[[fn *]] First.", "[[page 2]]\nC[[fnref *]] d.\n\n[[fn *]] Second."])
        d = book["divisions"][0]
        self.assertEqual([n["id"] for n in d["notes"]], ["d001-n1", "d001-n2"])
        self.assertIn('to="d001-n1"', texts(book)[1])
        self.assertIn('to="d001-n2"', texts(book)[2])
        self.assertEqual(w, [])

    def test_note_referenced_twice(self):
        # [[fnref * again]]: a second printed reference to the note already referenced with that mark
        book, w = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b[[fnref * again]] c.\n\n[[fn *]] One note."])
        self.assertEqual(w, [])
        d = book["divisions"][0]
        self.assertEqual(len(d["notes"]), 1)
        t = texts(book)[1]
        self.assertEqual(t.count('to="d001-n1"'), 2)
        html = rh.Ctx(book, "web", {d["id"]: "d001.html" for d in book["divisions"]}).inline(t)
        self.assertEqual(html.count('id="r-d001-n1"'), 1)      # ids stay unique
        self.assertEqual(html.count('href="#d001-n1"'), 2)
        self.assertEqual(html.count('aria-label="Note 1"'), 2)  # a screen reader says "Note 1", not "star"
        o = render_odt.Odt(book, None)
        o.notes = {n["id"]: n for n in d["notes"]}
        x = o.inline(t)
        self.assertEqual(x.count("<text:note "), 1)  # the note is placed once
        self.assertEqual(x.count('text:ref-name="d001-n1">*</text:note-ref>'), 1)

    def test_arabic_script_tagged(self):
        """Arabic script in the text is tagged with lang and dir (review 2026-11-21). Invented text."""
        h = rh.tag_scripts("he wrote بسم الله, then left")
        self.assertEqual(h, 'he wrote <span lang="ar" dir="rtl">بسم الله</span>, then left')
        self.assertEqual(rh.tag_scripts("Kairwan, 1894"), "Kairwan, 1894")

    def test_han_script_tagged(self):
        """Chinese characters get lang="zh", a run with kana lang="ja", no dir (A Yankee on the Yangtze, 2026-11-22).
        Invented text."""
        h = rh.tag_scripts("天下無難事 there is, said he")
        self.assertEqual(h, '<span lang="zh">天下無難事</span> there is, said he')
        self.assertEqual(rh.tag_scripts("the sign 東京 ふじ"), 'the sign <span lang="ja">東京 ふじ</span>')
        self.assertEqual(rh.tag_scripts("Tokio (no script)"), "Tokio (no script)")

    def test_editor_role(self):
        b = {"authors": [{"name": "A. Writer"}, {"name": "E. Ditor", "role": "editor"}]}
        self.assertEqual(rh.authors_text(b), "A. Writer; edited by E. Ditor")
        self.assertEqual(rh.authors_text({"authors": []}), "Anonymous")

    def test_frontispiece(self):
        pages = ["[[page ?]]\n[[image: a portrait]]", "[[page ?]]\nTITLE", "[[page 1]]\n# ONE\n\nText."]
        book, w = comp(pages, frontispiece="p0001-1")
        self.assertEqual(w, [])
        one = [d for d in book["divisions"] if d["reading"]][0]
        self.assertEqual((one["blocks"][0]["type"], one["blocks"][0]["src"]), ("image", "images/p0001-1.jpg"))
        self.assertFalse(any(b["type"] == "image" for d in book["divisions"] if not d["reading"] for b in d["blocks"]))
        _, w = comp(pages, frontispiece="p0009-1")
        self.assertTrue(any("frontispiece" in x for x in w))

    def test_frontispiece_of_each_volume(self):
        """Two volumes, each with its frontispiece in its front matter (Staunton's Embassy, 2026-11-20): each goes to
        the first reading division after it, not both to the first of the book."""
        pages = ["[[page ?]]\n[[image: portrait one]]", "[[page 1]]\n# ONE\n\nText.",
                 "[[page ?]]\n[[image: portrait two]]", "[[page ?]]\nTITLE TWO", "[[page 1]]\n# TWO\n\nMore."]
        divs = [{"at": "p0003", "kind": "front"}]
        book, w = comp(pages, frontispiece=["p0001-1", "p0003-1"], divisions=divs)
        self.assertEqual(w, [])
        one, two = [d for d in book["divisions"] if d["reading"]]
        self.assertEqual(one["blocks"][0]["src"], "images/p0001-1.jpg")
        self.assertEqual(two["blocks"][0]["src"], "images/p0003-1.jpg")
        self.assertFalse(any(b["type"] == "image" for d in book["divisions"] if not d["reading"] for b in d["blocks"]))

    def test_note_problems_reported(self):
        _, w = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b.\n\n[[fn †]] Orphan."])
        self.assertEqual(len(w), 2)

    def test_note_continued(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b.\n\n[[fn *]] It runs", "[[page 2]]\nC.\n\n[[fn cont]] over."])
        self.assertEqual(inline.plain(book["divisions"][0]["notes"][0]["text"]), "It runs over.")

    def test_divisions(self):
        book, w = comp(["[[page ?]]\nTITLE", "[[page ?]]\nCONTENTS\n\nOne, 1", "[[page 1]]\n# PART I.", "[[page 2]]\n# CHAPTER I.\n\n[[subtitle]] The Start\n\nText.",
                        "[[page 3]]\n# INDEX\n\nA, 1"],
                       divisions=[{"at": "p0002", "kind": "contents"}, {"at": "p0005", "kind": "index"}])
        got = [(d["kind"], d["reading"], d["title"]) for d in book["divisions"]]
        self.assertEqual(got, [("front", False, "Front matter"), ("contents", False, "Contents"), ("part", True, "PART I"),
                               ("chapter", True, "CHAPTER I. The Start"), ("index", False, "INDEX")])
        self.assertEqual(w, [])
        self.assertEqual([d["title"] for d, kids in rh.nav_tree(book)], ["PART I"])

    def test_unused_division_override_reported(self):
        _, w = comp(["[[page 1]]\n# ONE\n\nText."], divisions=[{"at": "p0009", "kind": "index"}])
        self.assertEqual(len(w), 1)

    def test_verse_and_quote_continue(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\n<verse>\nLine one,\nLine two;\n\nLine three,\n</verse>", "[[page 2]]\n<verse>\n[[cont]]Line four.\n</verse>\n\n<blockquote>\nA letter that runs\n</blockquote>",
                        "[[page 3]]\n<blockquote>\n[[cont]]over the page.\n[[right]]J. D.\n</blockquote>"])
        b = book["divisions"][0]["blocks"]
        self.assertEqual(b[1]["stanzas"], [["Line one,", "Line two;"], ["Line three,", '<pb n="2" leaf="p0002"/>Line four.']])
        self.assertEqual(b[2]["paragraphs"], [{"text": 'A letter that runs <pb n="3" leaf="p0003"/>over the page.'}, {"text": "J. D.", "align": "right"}])

    def test_corrections_listed_with_leaf(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nA long", "[[page 2]]\n[[cont]]line with [[corr teh|the]] error."])
        self.assertEqual(book["corrections"], [{"leaf": "p0002", "division": "d001", "printed": "teh", "corrected": "the"}])

    def test_caption_and_table(self):
        book, w = comp(["[[page 1]]\n# ONE\n\n[[image: a cart]]\n[[caption]] THE CART.\n\n| a | b |\n| c | d |"], )
        b = book["divisions"][0]["blocks"]
        self.assertEqual(b[1]["caption"], "THE CART.")
        self.assertEqual(b[2]["rows"], [["a", "b"], ["c", "d"]])


class LongItalics(unittest.TestCase):
    """Tom, 2026-11-19: italics stay in the JSON; the built versions set long italic passages in roman."""
    LONG = "<i>" + "word " * 39 + "end.</i>"

    def div(self, *pages):
        book, _ = comp(list(pages))
        return book, book["divisions"][0]

    def test_json_keeps_italics_and_reading_drops_them(self):
        book, d = self.div("[[page 1]]\n# One\n\n" + self.LONG + "\n\nHe sailed in the <i>Coronet</i> that year.")
        self.assertIn("<i>word", d["blocks"][1]["text"])
        r = rh.roman_long_italics(d)
        self.assertNotIn("<i>", r["blocks"][1]["text"])
        self.assertIn("<i>Coronet</i>", r["blocks"][2]["text"])           # short italics stay
        self.assertIn("<i>word", d["blocks"][1]["text"])                    # the JSON division is not changed
        self.assertEqual(inline.plain(r["blocks"][1]["text"]), inline.plain(d["blocks"][1]["text"]))

    def test_roman_words_inside_become_italic(self):
        s = "<i>" + "word " * 30 + "</i>Coronet<i>, " + "word " * 10 + "end.</i>[[fnref *]]"
        _, d = self.div("[[page 1]]\n# One\n\n" + s + "\n\n[[fn *]] Note.")
        t = rh.roman_long_italics(d)["blocks"][1]["text"]
        self.assertEqual(t.count("<i>"), 1)
        self.assertIn("<i>Coronet</i>,", t)
        self.assertIn("<noteref", t)

    def test_short_italic_paragraph_stays(self):
        _, d = self.div("[[page 1]]\n# One\n\n<i>A short motto in italic.</i>")
        self.assertIn("<i>", rh.roman_long_italics(d)["blocks"][1]["text"])

    def test_summary_verse_and_table(self):
        _, d = self.div("[[page 1]]\n# One\n\n[[subtitle]] <i>The Start—The River</i>\n\n<verse>\n<i>One,</i>\n<i>Two,</i>\n<i>Three,</i>\n<i>Four.</i>\n</verse>\n\n"
                        "<verse>\n<i>One,</i>\n<i>Two.</i>\n</verse>\n\n| <i>Cairo</i> | <i>Egypt</i> |\n| <i>Smyrna</i> | <i>Asia</i> |")
        b = rh.roman_long_italics(d)["blocks"]
        self.assertNotIn("<i>", b[1]["text"])
        self.assertNotIn("<i>", str(b[2]["stanzas"]))
        self.assertIn("<i>", str(b[3]["stanzas"]))                          # two lines: stays italic
        self.assertNotIn("<i>", str(b[4]["rows"]))


class Sample(unittest.TestCase):
    """The sample book in tests/sample goes through every builder and every check."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.dir = os.path.join(cls.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, cls.dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_preflight_clean(self):
        verdict, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        enforce = {k: v for k, v in res.items() if preflight.CHECKS[k][0] == "enforce" and v}
        self.assertEqual(enforce, {}, report)
        self.assertEqual(verdict, "INCOMPLETE")       # a run with skipped checks can never say PASS

    def test_deterministic(self):
        book, _ = compile_book.compile_book(self.dir)
        idir = os.path.join(self.dir, "images")
        self.assertEqual(render_epub.render(book, idir), render_epub.render(copy.deepcopy(book), idir))
        self.assertEqual(render_odt.render(book, idir), render_odt.render(copy.deepcopy(book), idir))

    def test_reading_editions_leave_out_index(self):
        out = os.path.join(self.tmp, "site")
        book, _ = build_site.build_book(out, self.dir)
        bdir = os.path.join(out, "books", book["id"])
        self.assertEqual(sorted(f for f in os.listdir(bdir) if f[0].isdigit()), ["01.html", "02.html", "03.html", "04.html", "05.html", "06.html"])   # title page, preface, chapter I in three, chapter II
        j = json.load(open(os.path.join(bdir, book["id"] + ".json"), encoding="utf-8"))
        self.assertIn("index", [d["kind"] for d in j["divisions"]])
        z = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".epub"))
        self.assertNotIn("INDEX", "".join(z.read(n).decode() for n in z.namelist() if n.endswith(".xhtml")))
        page = open(os.path.join(bdir, "04.html"), encoding="utf-8").read()
        self.assertIn('href="05.html#pg-4"', page)                      # "see p. 4" links to where page 4 starts
        self.assertIn("archive.org/details/samplejourney00doe/page/n4/", page)   # leaf 5, one hidden leaf before it

    def planted(self, leaf, old, new):
        d = os.path.join(self.tmp, "planted", "sample-journey-doe")
        shutil.rmtree(os.path.dirname(d), ignore_errors=True)
        shutil.copytree(SAMPLE, d)
        p = os.path.join(d, "pages", leaf + ".txt")
        t = open(p, encoding="utf-8").read()
        self.assertIn(old, t)
        open(p, "w", encoding="utf-8").write(t.replace(old, new))
        _, _, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
        return res

    def test_catches_unknown_marker(self):
        self.assertTrue(self.planted("p0009", "So we paid", "[[contd]] So we paid")["markup"])

    def test_catches_spacing(self):
        self.assertTrue(self.planted("p0009", "and slept,", "and slept ;")["spacing"])

    def test_catches_capital_small_caps(self):
        self.assertTrue(self.planted("p0009", "<sc>The Landlord.</sc>", "<sc>THE LANDLORD.</sc>")["sc-caps"])

    def test_catches_heading_in_capitals(self):
        self.assertTrue(self.planted("p0007", "# Chapter II.", "# CHAPTER II.")["heading-caps"])
        self.assertTrue(self.planted("p0007", "[[caption]] The Carrier's Cart.", "[[caption]] THE CARRIER'S CART.")["heading-caps"])
        self.assertEqual(preflight.check_heading_caps([("p1", "# Chapter XIV.\n\n## II.\n\n[[subtitle]] A Day at Sea")]), [])

    def test_catches_orphan_note(self):
        self.assertTrue(self.planted("p0004", "[[fnref *]]", "")["compile"])

    def test_catches_illegible(self):
        self.assertTrue(self.planted("p0009", "slept", "sl〓pt")["markup"])

    def test_catches_missing_image(self):
        d = os.path.join(self.tmp, "noimg", "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        os.remove(os.path.join(d, "images", "p0007-1.jpg"))
        _, _, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
        self.assertTrue(res["compile"])

    def test_join_check_sees_missing_cont(self):
        # (until the review of 2026-11-20 this planted "[[cont]] after a closed sentence"; that half was dropped)
        res = self.planted("p0005", "[[cont]] The road", "the road")
        self.assertTrue(res["joins"])

    def test_waiver(self):
        d = os.path.join(self.tmp, "waived", "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        p = os.path.join(d, "pages", "p0009.txt")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("and slept,", "and slept ;"))
        c = json.load(open(os.path.join(d, "book.json"), encoding="utf-8"))
        c["waivers"] = [{"check": "spacing", "match": "p0009", "why": "test"}]
        json.dump(c, open(os.path.join(d, "book.json"), "w", encoding="utf-8"))
        _, report, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["spacing"], [])
        self.assertIn("1 waived", report)


    def test_odt_note_ref_is_not_text(self):
        # a second printed mark for one note ([[fnref * again]]) is a text:note-ref in the ODT: not body text
        import io
        x = ('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
             'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:body><office:text>'
             '<text:p>One<text:note text:id="n1"><text:note-citation>*</text:note-citation><text:note-body>'
             '<text:p>The note.</text:p></text:note-body></text:note> and two'
             '<text:note-ref text:note-class="footnote" text:ref-name="n1">*</text:note-ref> marks.</text:p>'
             '</office:text></office:body></office:document-content>')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("content.xml", x)
        buf.seek(0)
        main, notes = preflight.odt_streams(buf)
        self.assertEqual(main, "One and two marks.")
        self.assertEqual(notes, "The note.")

    def test_odt_contents_list_is_not_text(self):
        # the generated contents list after the title page (2026-11-19) is not book text; ordinary paragraphs
        # inserted next to it still count, so an inserted line is still caught
        import io
        x = ('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
             'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:body><office:text>'
             '<text:p text:style-name="Contents_20_Heading">Contents</text:p>'
             '<text:p text:style-name="Contents_20_1"><text:a>Chapter I. The Ford</text:a></text:p>'
             '<text:p text:style-name="Contents_20_2"><text:a>3-9 May: Leeds</text:a></text:p>'
             '<text:p text:style-name="Text_20_body">An inserted line.</text:p>'
             '<text:h text:style-name="Heading_20_1">Chapter I.</text:h>'
             '</office:text></office:body></office:document-content>')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("content.xml", x)
        buf.seek(0)
        main, _ = preflight.odt_streams(buf)
        self.assertEqual(main, "An inserted line. Chapter I.")


class Normalize(unittest.TestCase):
    def test_spacing(self):
        self.assertEqual(normalize.norm_page("[[page 3]]\n\n\n“ Well ! ” said he ; “ I do n't know .”  Then -- nothing."),
                         "[[page 3]]\n\n“Well!” said he; “I don't know.” Then—nothing.\n")

    def test_small_caps_lowered_and_tags_merged(self):
        self.assertEqual(normalize.norm_text("T<sc>HE MORNING</sc> was <i>very</i> <i>fine</i>"), "T<sc>he morning</sc> was <i>very fine</i>")
        self.assertEqual(normalize.norm_text("<sc>Cairo</sc>"), "<sc>Cairo</sc>")

    def test_space_before_note_reference(self):
        self.assertEqual(normalize.norm_text("covered with thorns [[fnref *]] and flowers. 52,000. [[fnref †]]"),
                         "covered with thorns[[fnref *]] and flowers. 52,000.[[fnref †]]")

    def test_letters_never_change(self):
        s = "He shewed us the waggon to-day, . . . and Mr. B——'s connexion."
        self.assertEqual(normalize.norm_text(s), s)

    def test_markers_untouched(self):
        self.assertEqual(normalize.norm_page("[[page 3]]\n[[image: a man ; a cart]]\n| a | b |"), "[[page 3]]\n[[image: a man ; a cart]]\n| a | b |\n")


class Corrections(unittest.TestCase):
    def test_apply(self):
        out, n, sk = corrections.apply("the cat sat on the mat", '{"find": "cat sat", "replace": "cat sits"}\n{"find": "the", "replace": "a"}\nNONE')
        self.assertEqual((out, n, len(sk)), ("the cat sits on the mat", 1, 1))

    def test_review_cont_changes(self):
        """The corrections pass dropped two page-top [[cont]] marks as a 'markup' change, applied without a spot and
        never listed (*The Nile without a Dragoman* p0038, p0064, 2026-11-21). Invented text."""
        d = "[[page 4]]\n\n[[cont]]and so we went on.\n\nThen we stopped."
        self.assertEqual(review.cont_change(d, d.replace("[[cont]]", "")), "removed")
        self.assertEqual(review.cont_change(d.replace("[[cont]]", ""), d), "added")
        self.assertIsNone(review.cont_change(d, d.replace("Then", "So")))

    def test_review_kinds(self):
        self.assertEqual(review.kind_of("shew", "show"), "words")
        self.assertEqual(review.kind_of("so, then", "so; then"), "punctuation")
        self.assertEqual(review.kind_of("a <i>b</i>", "a b"), "markup")

    def test_judge_heading_spot_always_reported(self):
        s = {"n": 1, "find": "# Tenth Letter\n\n", "replace": "", "draft": "# Tenth Letter\n\n", "verified": ""}
        self.assertTrue(judge.must_look("verified", "high", s))
        plain = {"n": 2, "find": "THAT", "replace": "T<sc>hat</sc>", "draft": "THAT", "verified": "T<sc>hat</sc>"}
        self.assertFalse(judge.must_look("verified", "high", plain))
        self.assertTrue(judge.must_look("draft", "high", plain))
        self.assertTrue(judge.must_look("verified", "medium", plain))

    def test_judge_apply(self):
        spots = [{"n": 1, "find": "we shew", "replace": "we show", "draft": "shew", "verified": "show"},
                 {"n": 2, "find": "so, then", "replace": "so; then", "draft": "so, t", "verified": "so; t"}]
        a1 = "A" if judge.labels("p0001", 1) else "B"          # the label of the draft's reading at spot 1
        v2 = "B" if judge.labels("p0001", 2) else "A"          # the label of the verifier's reading at spot 2
        text, rows = judge.apply("Here we show it; so; then on.", spots, {1: {"is": a1}, 2: {"is": v2}}, "p0001")
        self.assertEqual(text, "Here we shew it; so; then on.")
        self.assertEqual([r[0] for r in rows], ["draft", "verified"])

    def test_judge_move_judged_both_ways_keeps_text(self):
        """The verifier moved a paragraph from before a picture to after its caption: two spots. The judge took
        the verifier's side at one and the draft's at the other, and the paragraph was lost (Rambles p0092,
        2026-11-20). Invented text."""
        moved = "went on to the next town, twenty miles away, and was paid for his trouble"
        draft = f"He drew me until he had {moved}\n\n[[image: a cart]]\n[[caption]] <sc>a cart.</sc>"
        verified = f"He drew me until he had\n\n[[image: a cart]]\n[[caption]] A Cart.\n\n[[cont]]{moved}"
        spots = [{"n": 1, "find": f"had {moved}", "replace": "had", "draft": moved, "verified": ""},
                 {"n": 2, "find": "[[caption]] <sc>a cart.</sc>", "replace": f"[[caption]] A Cart.\n\n[[cont]]{moved}",
                  "draft": "<sc>a cart.</sc>", "verified": f"A Cart. {moved}"}]
        self.assertEqual(judge.moves(spots), [(1, 2)])
        lab = lambda n, who: ("A" if judge.labels("p0001", n) else "B") if who == "draft" else ("B" if judge.labels("p0001", n) else "A")
        text, rows = judge.apply(verified, spots, {1: {"is": lab(1, "verified")}, 2: {"is": lab(2, "draft")}}, "p0001")
        self.assertEqual(text.count(moved), 1)
        self.assertTrue(all(r[0].startswith("move judged both ways") for r in rows))
        text, rows = judge.apply(verified, spots, {1: {"is": lab(1, "draft")}, 2: {"is": lab(2, "draft")}}, "p0001")
        self.assertEqual(text, draft)                          # judged the same way at both ends: applied as before

    def test_judge_never_drops_a_picture(self):
        """The verifier left out a picture line and the judge agreed (Zephyrus p0171, 2026-11-20). Invented text."""
        img = "[[image: two ostriches by a fence]]\n[[caption]] Ostriches."
        draft = f"We rode on.\n\n{img}\n\nAt noon we halted."
        verified = "We rode on.\n\nAt noon we halted."
        spots = [{"n": 1, "find": f"on.\n\n{img}\n\nAt", "replace": "on.\n\nAt", "draft": img, "verified": ""}]
        ver = "B" if judge.labels("p0001", 1) else "A"
        text, rows = judge.apply(verified, spots, {1: {"is": ver, "sure": "high"}}, "p0001")
        self.assertEqual(text, draft)
        self.assertTrue(rows[0][0].startswith("draft kept"))
        self.assertTrue(judge.must_look("verified", "high", spots[0]))
        # a picture the verifier moved (taken out here, put in at another spot) is not doubled
        spots2 = spots + [{"n": 2, "find": "halted.", "replace": f"halted.\n\n{img}", "draft": "", "verified": img}]
        self.assertEqual(judge.dropped_images(spots2[0], spots2), [])



class JudgeKeepsCaptions(unittest.TestCase):
    """The verifier left out a plate's caption line and the judge agreed, "sure: medium" (*Western Wanderings*
    p0312, 2026-11-22). Invented text."""

    def test_caption_kept(self):
        img = "[[image: a river with a railway]]"
        draft = f"{img}\n[[caption]] View on the River.\n\nWe went on."
        verified = f"{img}\n\nWe went on."
        spots = [{"n": 1, "find": f"{img}\n[[caption]] View on the River.\n\nWe", "replace": f"{img}\n\nWe",
                  "draft": "[[caption]] View on the River.", "verified": ""}]
        self.assertEqual(judge.dropped_images(spots[0], spots), ["[[caption]] View on the River."])
        ver = "B" if judge.labels("p0001", 1) else "A"
        text, rows = judge.apply(verified, spots, {1: {"is": ver, "sure": "medium"}}, "p0001")
        self.assertEqual(text, draft)
        # a caption the verifier only reworded is not "dropped" when the other spot puts it in
        spots2 = [{"n": 1, "find": "[[caption]] View on the River.", "replace": "", "draft": "", "verified": ""},
                  {"n": 2, "find": "x", "replace": "x\n[[caption]] View on the River.", "draft": "", "verified": ""}]
        self.assertEqual(judge.dropped_images(spots2[0], spots2), [])


class CaptionOrder(unittest.TestCase):
    """Captions are compared as a sorted list; sorting before squashing put a caption with a straight apostrophe
    or a leading tag elsewhere, so equal lists gave items (Alaska, 2026-11-20). Invented captions."""

    def test_equal_lists_with_quotes_and_tags(self):
        pc = ["The Captain's House", "The Captains Mule", "A Mule"]
        jc = ["The Captain’s House", "The Captains Mule", "A Mule"]
        self.assertNotEqual(preflight.compare(" ".join(sorted(pc)), " ".join(sorted(jc)), "c"), [])   # the old way
        k = preflight.caption_key
        self.assertEqual(preflight.compare(" ".join(sorted(pc, key=k)), " ".join(sorted(jc, key=k)), "c"), [])
        self.assertNotEqual(preflight.compare(" ".join(sorted(pc, key=k)), " ".join(sorted(jc[:2], key=k)), "c"), [])



class VerseJoins(unittest.TestCase):
    """A verse block at a page top that begins with [[cont]] is listed with the stanza lengths on both sides
    (Twelve Years in Canterbury: stanzas ending at the page foot were joined). Invented verse."""

    def test_listed_with_stanza_lengths(self):
        p1 = "Prose.\n\n<verse>\nOne line\nTwo line\n\nThree line\nFour line\n</verse>"
        p2 = "[[page 9]]\n<verse>\n[[cont]]Five line\nSix line\n</verse>\n\nMore prose."
        items = preflight.check_verse_joins([("p0001", p1), ("p0002", p2)])
        self.assertEqual(len(items), 1)
        self.assertIn("[2, 2] | here [2]", items[0])
        self.assertEqual(preflight.check_verse_joins([("p0001", p1), ("p0002", p2.replace("[[cont]]", ""))]), [])


class Ornaments(unittest.TestCase):
    """Decorative head-pieces and tail-pieces (Tom, 2026-11-20: include them, small). book.json "ornaments" lists
    their image ids; a head-piece printed above a chapter heading opens that chapter. Invented text."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        pages = os.path.join(self.dir, "pages")
        p = os.path.join(pages, "p0004.txt")
        t = open(p, encoding="utf-8").read()
        self.assertTrue(t.startswith("[[page 1]]\n# Chapter I."))
        open(p, "w", encoding="utf-8").write(t.replace("[[page 1]]\n", "[[page 1]]\n[[image: head-piece: a bird among leaves]]\n\n", 1))
        p = os.path.join(pages, "p0003.txt")
        open(p, "a", encoding="utf-8").write("\n[[image: tail-piece: a spray of flowers]]\n")
        for f in ("p0004-1.jpg", "p0003-1.jpg"):
            shutil.copy(os.path.join(self.dir, "images", "p0007-1.jpg"), os.path.join(self.dir, "images", f))
        bj = os.path.join(self.dir, "book.json")
        cfg = json.load(open(bj, encoding="utf-8"))
        cfg["ornaments"] = ["p0004-1", "p0003-1"]
        json.dump(cfg, open(bj, "w", encoding="utf-8"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_head_piece_opens_the_chapter_and_both_are_small(self):
        book, w = compile_book.compile_book(self.dir)
        self.assertEqual([x for x in w if "image" in x], [])
        ch1 = next(d for d in book["divisions"] if d["first_leaf"] == "p0004")
        self.assertEqual(ch1["blocks"][0]["type"], "image")
        self.assertTrue(ch1["blocks"][0].get("ornament"))
        self.assertEqual(ch1["blocks"][1]["type"], "heading")
        self.assertTrue(ch1["title"].startswith("Chapter I"))
        tail = [b for d in book["divisions"] for b in d["blocks"] if b.get("src") == "images/p0003-1.jpg"]
        self.assertEqual(len(tail), 1)
        self.assertTrue(tail[0].get("ornament"))
        plain = [b for d in book["divisions"] for b in d["blocks"] if b.get("src") == "images/p0007-1.jpg"]
        self.assertFalse(plain[0].get("ornament"))            # an ordinary illustration is not one
        html = rh.Ctx(book, "web", rh.file_names(book, ".html")).blocks(ch1)
        self.assertIn('<figure class="ornament">', html)
        odt = render_odt.render(book, os.path.join(self.dir, "images"))
        x = zipfile.ZipFile(__import__("io").BytesIO(odt)).read("content.xml").decode()
        frames = re.findall(r'svg:width="([\d.]+)cm"[^>]*>\s*<draw:image xlink:href="Pictures/([^"]+)"', x)
        size = {f: float(w) for w, f in frames}
        self.assertLessEqual(size["p0004-1.jpg"], 5.0)
        self.assertGreater(size["p0007-1.jpg"], 5.0)
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["conservation"], [], report)
        self.assertEqual(res["images"], [], report)


class ImageInParagraph(unittest.TestCase):
    """A picture in the middle of a page that interrupts a paragraph: `[[cont]]` after it joins the paragraph again
    (the compiler dropped it and split the paragraph; South by West, 2026-11-19). Invented text."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        p = os.path.join(self.dir, "pages", "p0005.txt")
        t = open(p, encoding="utf-8").read()
        old = "<pref>4</pref>, and by noon"
        self.assertIn(old, t)
        open(p, "w", encoding="utf-8").write(t.replace(old, "<pref>4</pref>, and by\n\n[[image: a mill by a river]]\n"
                                                         "[[caption]] The Mill.\n\n[[cont]]noon", 1))
        shutil.copy(os.path.join(self.dir, "images", "p0007-1.jpg"), os.path.join(self.dir, "images", "p0005-1.jpg"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_joined_and_picture_after_paragraph(self):
        book, w = compile_book.compile_book(self.dir)
        self.assertEqual([x for x in w if "[[cont]]" in x], [])
        blocks = [b for d in book["divisions"] for b in d["blocks"]]
        i = next(k for k, b in enumerate(blocks) if "and by noon we had made" in b.get("text", ""))
        self.assertIn("out a halt", blocks[i]["text"])               # and still joined over the page
        self.assertEqual(blocks[i + 1].get("caption"), "The Mill.")
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["conservation"], [], report)

    def test_cont_mid_page_without_picture_still_warned(self):
        p = os.path.join(self.dir, "pages", "p0005.txt")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("[[image: a mill by a river]]\n[[caption]] The Mill.\n\n", "", 1))
        _, w = compile_book.compile_book(self.dir)
        self.assertTrue(any("not at the top of a page" in x for x in w), w)

    def test_publish_refuses_compile_warnings(self):
        import publish
        self.assertEqual(publish.deploy_blockers(self.dir), [])
        p = os.path.join(self.dir, "pages", "p0005.txt")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("[[image: a mill by a river]]\n[[caption]] The Mill.\n\n", "", 1))
        self.assertTrue(any("not at the top of a page" in x for x in publish.deploy_blockers(self.dir)))


class Drive(unittest.TestCase):
    def test_pack_parts_are_independent_and_small(self):
        tmp = tempfile.mkdtemp()
        try:
            pages = os.path.join(tmp, "pages")
            os.makedirs(pages)
            for i in range(7):
                open(os.path.join(pages, f"p{i:04d}.jpg"), "wb").write(os.urandom(1000))
            src = os.path.join(tmp, "source.json")
            json.dump({"ia_identifier": "x"}, open(src, "w"))
            drive_cache.pack(pages, os.path.join(tmp, "parts"), src, limit=3500)
            s = json.load(open(src))
            self.assertEqual(s["ia_identifier"], "x")
            self.assertEqual(sum(len(p["files"]) for p in s["parts"]), 7)
            self.assertTrue(all(p["bytes"] <= 3500 for p in s["parts"]))
            drive_cache.setid(src, "pages-001.zip", "ID1")
            drive_cache.pack(pages, os.path.join(tmp, "parts"), src, limit=3500)      # repacking keeps the ids of unchanged parts
            self.assertEqual(json.load(open(src))["parts"][0].get("drive_id"), "ID1")
            before = json.load(open(src))["parts"]
            open(os.path.join(pages, "p0003a.jpg"), "wb").write(os.urandom(1000))     # a leaf added later
            drive_cache.pack(pages, os.path.join(tmp, "parts"), src, limit=3500, append=True)
            after = json.load(open(src))["parts"]
            self.assertEqual(after[:len(before)], before)                            # old parts untouched
            self.assertEqual([p["files"] for p in after[len(before):]], [["p0003a.jpg"]])
            self.assertEqual(after[-1]["name"], f"pages-{len(before) + 1:03d}.zip")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class DrivePages(unittest.TestCase):
    """fetch --pages: a comma list was read as one name and fetched the wrong parts (2026-11-19)."""
    def test_list_and_ranges(self):
        keep = drive_cache.page_filter("p0036,p0111, p0150-p0152")
        got = [f for f in ["p0035.jpg", "p0036.jpg", "p0111.jpg", "p0150.jpg", "p0152.jpg", "p0153.jpg", "leaves.json"] if keep(f)]
        self.assertEqual(got, ["p0036.jpg", "p0111.jpg", "p0150.jpg", "p0152.jpg", "leaves.json"])
        self.assertIsNone(drive_cache.page_filter(None))

    def test_bad_item_stops(self):
        with self.assertRaises(SystemExit):
            drive_cache.page_filter("116-118")

    def test_leaves_with_a_letter(self):
        names = ["p2028.jpg", "p2029.jpg", "p2029a.jpg", "p2029b.jpg", "p2030.jpg"]
        self.assertEqual([f for f in names if drive_cache.page_filter("p2029b")(f)], ["p2029b.jpg"])
        self.assertEqual([f for f in names if drive_cache.page_filter("p2029")(f)], ["p2029.jpg", "p2029a.jpg", "p2029b.jpg"])
        self.assertEqual([f for f in names if drive_cache.page_filter("p2028-p2029")(f)], names[:4])


class SetupEnv(unittest.TestCase):
    """setup_env.sh must turn the Ubuntu apt mirrors to https (plain http hangs behind the proxy); the first
    version's sed used | as delimiter with \\| inside, matched nothing, and apt hung for 20 minutes (2026-11-19)."""
    def test_apt_mirrors_become_https(self):
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "sources.list.d"))
            f = os.path.join(tmp, "sources.list.d", "ubuntu.sources")
            open(f, "w").write("URIs: http://archive.ubuntu.com/ubuntu/\nURIs: http://security.ubuntu.com/ubuntu/\n"
                               "URIs: http://example.org/other/\n")
            subprocess.run(["bash", os.path.join(REPO, "tools", "setup_env.sh"), "--apt-https-only", tmp], check=True)
            self.assertEqual(open(f).read(), "URIs: https://archive.ubuntu.com/ubuntu/\nURIs: https://security.ubuntu.com/ubuntu/\n"
                                             "URIs: http://example.org/other/\n")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class CropImage(unittest.TestCase):
    def test_rotate_turns_sideways_plate_upright(self):
        from PIL import Image
        im = Image.new("RGB", (400, 200), "white")
        im.paste((0, 0, 0), (0, 0, 20, 200))          # dark band along the left edge of a wide picture
        out = crop_image.crop(im, (0, 0, 1, 1), rotate=90, longest=1600)
        self.assertEqual(out.size, (200, 400))
        self.assertLess(out.getpixel((100, 395)), (60, 60, 60))   # left edge turned counter-clockwise -> bottom
        self.assertGreater(out.getpixel((100, 5)), (200, 200, 200))

    def test_box_and_size(self):
        from PIL import Image
        out = crop_image.crop(Image.new("RGB", (1000, 2000), "white"), (0.1, 0.1, 0.6, 0.6), longest=500)
        self.assertEqual(out.size, (250, 500))

    def test_default_size_is_the_limit(self):
        from PIL import Image
        out = crop_image.crop(Image.new("RGB", (3000, 4000), "white"), (0, 0, 1, 1))
        self.assertEqual(max(out.size), crop_image.MAX)

    def test_shrink_brings_a_large_picture_within_limits(self):
        from PIL import Image
        tmp = tempfile.mkdtemp()
        try:
            for mode, size in (("RGB", (1600, 1200)), ("L", (800, 1500)), ("L", (600, 400))):
                p = os.path.join(tmp, f"{mode}{size[0]}.jpg")
                im = Image.effect_noise(size, 40).convert(mode)
                im.save(p, "JPEG", quality=90)
                self.assertIsNotNone(crop_image.within_limits(p))      # too large, or quality 90
                before, after = crop_image.shrink(p)
                self.assertLess(after, before)
                self.assertIsNone(crop_image.within_limits(p))
                out = Image.open(p)
                self.assertEqual(out.mode, mode)
                self.assertEqual(max(out.size), min(max(size), crop_image.MAX))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_within_limits_names_the_fault(self):
        from PIL import Image
        tmp = tempfile.mkdtemp()
        try:
            big, fine = os.path.join(tmp, "big.jpg"), os.path.join(tmp, "fine.jpg")
            Image.new("RGB", (crop_image.MAX + 1, 10)).save(big, "JPEG", quality=crop_image.QUALITY)
            self.assertIn("longest side", crop_image.within_limits(big))
            Image.new("RGB", (100, 10)).save(fine, "JPEG", quality=crop_image.QUALITY + 10)
            self.assertIn("quality", crop_image.within_limits(fine))
            Image.new("RGB", (100, 10)).save(fine, "JPEG", quality=crop_image.QUALITY)
            self.assertIsNone(crop_image.within_limits(fine))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class ImageLimits(unittest.TestCase):
    """Every picture in books/ and wip/ is within crop_image's limits (Tom, 2026-11-23: the site and repository stay small)."""
    def test_pictures_in_the_repository(self):
        import glob
        bad = []
        for p in sorted(glob.glob(os.path.join(REPO, "books", "*", "images", "*")) +
                        glob.glob(os.path.join(REPO, "wip", "*", "images", "*"))):
            why = crop_image.within_limits(p)
            if why:
                bad.append(f"{os.path.relpath(p, REPO)}: {why}")
        self.assertEqual(bad, [], "pictures over the limits (tools/crop_image.py --shrink FILE ...):\n" + "\n".join(bad[:20]))


class Books(unittest.TestCase):
    """Every published book still compiles without warnings other than hyphen joins (a builder change must not break one)."""
    def test_published_books_compile(self):
        bdir = os.path.join(REPO, "books")
        for slug in sorted(os.listdir(bdir)) if os.path.isdir(bdir) else []:
            if os.path.exists(os.path.join(bdir, slug, "book.json")):
                _, w = compile_book.compile_book(os.path.join(bdir, slug))
                self.assertEqual([x for x in w if not x.startswith("hyphen join")], [], slug)


def shelf_book(i, **kw):
    """An invented book as the site lists see it (the fields of the book JSON that the lists use)."""
    return dict({"id": f"book-{i:02d}", "title": f"Journey {i}", "year": 1850 + i, "authors": [{"name": f"Author {i}", "sort": f"{chr(65 + i % 26)}uthor, {i}"}],
                 "regions": ["Spain"], "period": str(1840 + i), "date": f"2026-12-{i + 1:02d}",
                 "history": [{"version": 1, "date": f"2026-12-{i + 1:02d}", "note": "First publication."}]}, **kw)


class SiteLists(unittest.TestCase):
    """The home page and the lists of books as the shelf grows; books from the JATSI list are marked (Tom, 2026-11-20)."""
    PLACES = {"areas": ["East Asia", "Europe"], "regions": {"Spain": "Europe", "Japan": "East Asia", "Hokkaido": "East Asia"}}

    def setUp(self):
        self.out = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.out, True)

    def read(self, name):
        return open(os.path.join(self.out, name), encoding="utf-8").read()

    def test_home_lists_every_book_while_they_are_few(self):
        books = [shelf_book(1), shelf_book(2, collection="jatsi", regions=["Japan"])]
        queue = [{"title": "Queued One", "author": "Q", "year": 1880, "status": "queued", "ia": "queuedone00q", "from": "jatsi", "jatsi": 3},
                 {"title": "Queued Two", "author": "R", "year": 1881, "status": "queued", "ia": "queuedtwo00r"},
                 {"title": "Rejected", "author": "S", "year": 1882, "status": "rejected", "ia": "x"}]
        build_site.build_index(self.out)
        build_site.build_books(self.out, books, queue)
        # the home page: the header, the title, two paragraphs, the footer; the lists are on the Books page (Tom, 2026-11-21)
        home = self.read("index.html")
        # the introduction: the name of the list links to this site's page about it (Tom, 2026-11-21)
        self.assertIn('Books are also being added from the project <a href="japan-as-they-saw-it.html">Japan As They Saw It</a>, so the site\n'
                      'has more books about Japan than about other countries.</p>', home)
        self.assertNotIn("about these books", home)
        main = home[home.index("<main"):home.index("</main>")]
        self.assertEqual((main.count("<h1"), main.count("<p>"), main.count("<h2"), main.count("<li")), (1, 3, 0, 0))
        self.assertNotIn("The site now contains", home)          # no books given: no count
        self.assertIn("The transcriptions on this site are in the public domain", home)
        h = self.read("books.html")
        self.assertIn("<h1>Books</h1>", h)
        self.assertIn('<h2 id="queue">In the queue</h2>', h)
        self.assertIn("The transcriptions on this site are in the public domain", h)
        for page in (home, h):
            self.assertIn('<li><a href="books.html">Books</a></li>', page)     # "Books" in the header of every page
            self.assertNotIn('class="crumbs"', page)
        self.assertIn("Journey 1", h)
        self.assertIn("Journey 2", h)
        self.assertNotIn("authors.html", h)
        # the mark of a JATSI book in the lists: "JATSI", without parentheses, linked to this site's page (Tom, 2026-11-21): one book, one queue row
        self.assertEqual(h.count('<a href="japan-as-they-saw-it.html">JATSI</a>'), 2)
        self.assertNotIn('(<a href="japan', h)
        self.assertNotIn(">about</a>", h)
        self.assertNotIn("· from <a", h)
        # the project's name links to the project, in a new tab, wherever it stands (Tom, 2026-11-20)
        self.assertEqual(h.count("Japan As They Saw It"), h.count('<a href="https://www.gally.net/jatsi/index.html" target="_blank" rel="noopener">Japan As They Saw It</a>'))
        self.assertIn("Queued Two", h)
        self.assertNotIn("Rejected", h)

    def test_outside_links_open_in_a_new_tab_and_inside_links_do_not(self):
        build_site.build_index(self.out)
        build_site.md_page(self.out, "about.html", "About", os.path.join(REPO, "site", "about.md"))
        for name in ("index.html", "about.html"):
            links = re.findall(r"<a [^>]*>", self.read(name))
            outside = [a for a in links if re.search(r'href="https?://', a)]
            self.assertTrue(outside and len(outside) < len(links), name)
            for a in links:
                self.assertEqual('target="_blank" rel="noopener"' in a, a in outside, a)
                self.assertEqual(a.count("target="), 1 if a in outside else 0, a)
        self.assertEqual(build_site.outside_links('<a target="x" href="https://e.org/">'), '<a target="x" href="https://e.org/">')

    def test_page_numbers_linking_to_the_scan_open_in_a_new_tab(self):
        d = os.path.join(self.out, "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        book, _ = build_site.build_book(os.path.join(self.out, "site"), d)
        h = open(os.path.join(self.out, "site", "books", book["id"], "02.html"), encoding="utf-8").read()
        pbs = re.findall(r'<a class="pb"[^>]*>', h)
        self.assertTrue(pbs and all('target="_blank"' in a for a in pbs))
        self.assertNotIn("target=", "".join(re.findall(r'<a [^>]*href="(?!https?://)[^>]*>', h)))
        z = zipfile.ZipFile(os.path.join(self.out, "site", "books", book["id"], book["id"] + ".epub"))
        self.assertNotIn('target="_blank"', "".join(z.read(n).decode() for n in z.namelist() if n.endswith(".xhtml")))

    def test_display_settings_script_on_every_page_and_the_pages_work_without_it(self):
        """Tom, 2026-11-20: the reader's display settings. The colours and the underlining of links are for every
        page, so every page loads the one script, in the head and not deferred (the colours are set before the page
        is drawn). Nothing in the built pages depends on it: the settings button is made by the script on every page (it
        looks for the header), and the
        checkbox for the page numbers stays in the chapter pages for a browser that runs no scripts."""
        d = os.path.join(self.out, "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        site = os.path.join(self.out, "site")
        book, _ = build_site.build_book(site, d)
        build_site.build_index(site)
        chapter = open(os.path.join(site, "books", book["id"], "02.html"), encoding="utf-8").read()
        landing = open(os.path.join(site, "books", book["id"], "index.html"), encoding="utf-8").read()
        home = open(os.path.join(site, "index.html"), encoding="utf-8").read()
        for h, root in ((chapter, "../../"), (landing, "../../"), (home, "")):
            self.assertEqual(re.findall(r"<script[^>]*>", h), [f'<script src="{root}assets/site.js">'])
            self.assertLess(h.index("<script"), h.index("</head>"))
            self.assertNotIn("tb-", h)                      # no control of the settings in the page itself
        self.assertIn('<input type="checkbox" id="showpb"/>', chapter)
        self.assertIn('<article class="book">', chapter)   # what the script looks for before it makes the button
        self.assertIn('<h2 id="contents">', landing)       # where "Continue reading" goes
        self.assertIn('<header class="site">', chapter)
        # the button: the picture of the bar's, and in the same place in the window as the bar's (Tom, 2026-11-21)
        js = open(os.path.join(REPO, "site", "assets", "site.js"), encoding="utf-8").read()
        css = open(os.path.join(REPO, "site", "assets", "site.css"), encoding="utf-8").read()
        self.assertNotIn("textContent = 'Display'", js)
        self.assertRegex(js, r"'class': 'tb-btn'[^;]*'aria-label': 'Display settings'[^;]*svg\('display'\)\);\s+header\.appendChild\(btn\)")
        top = re.search(r"\.tb-btn \{ position: absolute; top: ([\d.]+)em; right: -0\.5em;[^}]*width: 2\.4em; height: 2\.4em;", css)
        bar = re.search(r"\.tb-bar > div > button, \.tb-none \{[^}]*width: 2\.4em; height: 2\.4em; padding: 0; margin: ([\d.]+)em 0;", css)
        self.assertEqual(top.group(1), bar.group(1))
        self.assertIn(".tb-bar > div > .tb-set-btn { justify-self: end; margin-right: -0.5em; }", css)

    def test_breadcrumbs_on_chapter_pages_only_and_from_the_book(self):
        """Tom, 2026-11-21: the logo and name in the header are the way home, so the breadcrumb line of a chapter
        begins with the book; the book's own page, the lists, About and the JATSI page have no such line. On the
        book's page the picture of the cover links to where "Read on this site" goes."""
        d = os.path.join(self.out, "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        site = os.path.join(self.out, "site")
        book, _ = build_site.build_book(site, d)
        build_site.build_lists(site, [shelf_book(1)], self.PLACES)
        build_site.build_jatsi(site, [], [], {"books": []})
        build_site.md_page(site, "about.html", "About", os.path.join(REPO, "site", "about.md"))
        rd = lambda *n: open(os.path.join(site, *n), encoding="utf-8").read()
        chapter = rd("books", book["id"], "02.html")
        crumbs = re.search(r'<nav class="crumbs" aria-label="Breadcrumb"><ol>(.*?)</ol></nav>', chapter).group(1)
        self.assertRegex(crumbs, r'^<li><a href="index\.html">[^<]+</a></li><li><a href="02\.html">[^<]+</a></li>$')
        landing = rd("books", book["id"], "index.html")
        for h in (landing, rd("places.html"), rd("dates.html"), rd("about.html"), rd("japan-as-they-saw-it.html")):
            self.assertNotIn('class="crumbs"', h)
            self.assertIn('<p class="sitename"><a href="', h)
        self.assertIn('Also listed by <a href="books.html">author</a> and by <a href="dates.html">date of the journey</a>.', rd("places.html"))
        if os.path.exists(os.path.join(d, "images", "cover.jpg")):
            # the picture leads to the start of the narrative; "Read on this site" to the title page (Tom, 2026-11-22)
            self.assertIn('<a class="cover" href="02.html#start" title="Start reading"><img class="cover" src="images/cover.jpg" alt="Cover of the book"/></a>', landing)
        self.assertIn('<li><a href="01.html">Read on this site</a> (contents below)</li>', landing)
        book2, _ = comp(["[[page 1]]\n# ONE\n\nText."])
        page = build_site.book_page(book2, rh.file_names(book2, ".html"), True)
        self.assertIn('<a class="cover" href="01.html#start" title="Start reading"><img class="cover"', page)
        # "Click to read" beside the picture, two lines, with the same link (Tom, 2026-11-23)
        self.assertIn('</a><a class="cover-label" href="01.html#start">Click<br/>to read</a></div>', page)
        self.assertIn('<div class="cover-row"><a class="cover" href="01.html#start"', page)
        self.assertNotIn("cover-label", build_site.book_page(book2, rh.file_names(book2, ".html"), False))
        self.assertIn('<li><a href="01.html">Read on this site</a> (contents below)</li>', page)

    def test_head_piece_stands_close_to_its_heading(self):
        """Tom, 2026-11-21: less space between a decorative banner above a chapter title and the title."""
        css = open(os.path.join(REPO, "site", "assets", "book.css"), encoding="utf-8").read()
        m = re.search(r"\.book figure\.ornament \+ h1, \.book figure\.ornament \+ h2 \{ margin-top: ([\d.]+)em; \}", css)
        self.assertLess(float(m.group(1)), 1)

    def test_logo_and_favicon_on_every_page(self):
        """Tom, 2026-11-21: a logo (a stack of books) as the favicon and beside the name of the site on every page.
        The favicon is the one file assets/logo.svg; the header copy is inline, in the page's colours, and hidden
        from screen readers, whose name for the link stays "Travel Books"."""
        d = os.path.join(self.out, "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        site = os.path.join(self.out, "site")
        book, _ = build_site.build_book(site, d)
        build_site.build_index(site)
        for name, root in ((os.path.join("books", book["id"], "02.html"), "../../"),
                           (os.path.join("books", book["id"], "index.html"), "../../"), ("index.html", "")):
            h = open(os.path.join(site, name), encoding="utf-8").read()
            head = h[:h.index("</head>")]
            self.assertEqual(re.findall(r'<link rel="icon"[^>]*>', head),
                             [f'<link rel="icon" href="{root}assets/logo.svg" type="image/svg+xml"/>'])
            self.assertIn(f'<p class="sitename"><a href="{root}index.html">{build_site.LOGO}Travel Books</a></p>', h)
        self.assertIn('aria-hidden="true"', build_site.LOGO)
        svg = open(os.path.join(REPO, "site", "assets", "logo.svg"), encoding="utf-8").read()
        self.assertNotIn("href", svg)                       # nothing from outside
        self.assertLess(len(svg), 2000)
        for shape in re.findall(r"<(?:rect|path) [^>]*>", build_site.LOGO):   # the same drawing in both
            self.assertIn(re.sub(r'class="logo-(\w)"', r'class="\1"', shape), svg)

    def test_reading_bar_is_made_by_the_script_from_the_pager_of_a_chapter(self):
        """Tom, 2026-11-21: a bar at the top of the chapter pages once the reader has scrolled down — the book's
        contents, the previous and next chapter, the Display settings — which a setting switches off. On the left
        (same day, later) a button opens a menu of three lines: the site (its logo and name), the book (its title,
        which fades out at the right when it is too long for the menu), the contents of the book. The script
        makes it from the links of the page's own pager, so a page without scripts has nothing that does nothing."""
        d = os.path.join(self.out, "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        site = os.path.join(self.out, "site")
        book, _ = build_site.build_book(site, d)
        chapter = open(os.path.join(site, "books", book["id"], "02.html"), encoding="utf-8").read()
        pager = re.search(r'<nav class="pager" aria-label="Chapters">(.*?)</nav>', chapter).group(1)
        self.assertRegex(pager, r'<a rel="prev" href="01\.html">← [^<]+</a><a href="index\.html#contents">Contents</a>'
                                r'<a rel="next" href="03\.html">[^<]+ →</a>')
        assets = os.path.join(REPO, "site", "assets")
        js = open(os.path.join(assets, "site.js"), encoding="utf-8").read()
        css = open(os.path.join(assets, "site.css"), encoding="utf-8").read()
        for q in ("'nav.pager'", "'a[rel=prev]'", "'a[rel=next]'", "'a:not([rel])'"):
            self.assertIn(q, js)
        self.assertRegex(js, r"DEF = \{[^}]*\bbar: 1 \}")                    # shown unless the reader switches it off
        self.assertRegex(js, r"FLAGS = \[[^\]]*'bar'\]")
        self.assertIn("if (!article || !pager) return;", js)                 # chapter pages only
        for name in ("menu", "book", "contents", "prev", "next", "display"):                 # pictures, no words: each has its drawing
            self.assertRegex(js, rf"\b{name}: 'M")
        self.assertEqual(len(re.findall(r"'aria-label': [^,]+,\s+title: ", js)), 4)   # and each its name, read out and on hover
        for q in ("header.querySelector('.sitename a')", "document.querySelector('.crumbs a')", "svg('book', 'tb-ic')",
                  "svg('contents', 'tb-ic'), 'Contents'", "t.classList.toggle('tb-cut', t.scrollWidth > t.clientWidth + 1)"):
            self.assertIn(q, js)
        self.assertLess(js.index("line(home.getAttribute('href')"), js.index("line(crumb.getAttribute('href')"))
        self.assertLess(js.index("line(crumb.getAttribute('href')"), js.index("line(toc.getAttribute('href')"))
        self.assertRegex(css, r"\.tb-menu a > span\.tb-cut \{[^}]*mask-image: linear-gradient\(to right, #000 calc\(100% - 3em\), transparent\)")
        self.assertIn(".tb-menu a > span { flex: 1; min-width: 0; overflow: hidden; }", css)
        self.assertIn('html.tb-hasbar:not([data-bar="off"]) { scroll-padding-top:', css)
        self.assertRegex(css, r"@media print \{[^@]*\.tb-bar[^@]*display: none")
        self.assertIn("prefers-reduced-motion", css)
        # the reader's place is kept for each chapter of a book, not only the last one read
        self.assertIn("c[file] = [at.i, at.o]", js)
        # a chapter reached by an arrow of the bar opens with the bar in view, at its title or the reader's place there
        self.assertIn("sessionStorage.setItem(BARNAV, from.getAttribute('href'))", js)
        self.assertIn("sessionStorage.removeItem(BARNAV)", js)
        self.assertIn(".tb-bar.tb-now, .tb-bar.tb-now.tb-on { transition: none; }", css)

    def test_display_settings_use_nothing_from_outside_and_every_theme_is_complete(self):
        assets = os.path.join(REPO, "site", "assets")
        css = open(os.path.join(assets, "site.css"), encoding="utf-8").read()
        js = open(os.path.join(assets, "site.js"), encoding="utf-8").read()
        for text in (css, js):
            self.assertIsNone(re.search(r"https?:|//[a-z]|@import|url\(|@font-face", text))
        self.assertNotRegex(js, r"\b(fetch|XMLHttpRequest|sendBeacon|document\.cookie|eval)\b")
        names = ["--fg", "--bg", "--muted", "--link", "--visited", "--line"]
        rules = re.findall(r"(:root[^{]*)\{([^}]*--fg[^}]*)\}", css)
        # light; dark for a device set to dark; dark and sepia chosen by the reader; print
        self.assertEqual(len(rules), 5, [r[0] for r in rules])
        for sel, body in rules:
            self.assertEqual(re.findall(r"(--[a-z]+):", body), names, sel)
        dark = [body for sel, body in rules if "not([data-theme])" in sel or '"dark"' in sel]
        self.assertEqual(len(dark), 2)
        self.assertEqual(re.findall(r"--[a-z]+: #[0-9a-f]+", dark[0]), re.findall(r"--[a-z]+: #[0-9a-f]+", dark[1]))
        # every theme the script offers has its colours, and every attribute it sets has a rule
        for theme in re.search(r"theme: \[([^\]]*)\]", js).group(1).replace("'", "").split(", "):
            if theme != "auto":
                self.assertIn(f':root[data-theme="{theme}"]', css)
        # the header's text follows the size of the text up to the sixth of the nine sizes, and no further (Tom, 2026-11-20)
        sizes = [float(x) for x in re.search(r"size: \[([^\]]*)\]", js).group(1).split(", ")]
        self.assertEqual(len(sizes), 9)
        self.assertIn(f"--tb-hs: min(var(--tb-size, 1), {sizes[5]:g});", css)
        self.assertRegex(css, r"header\.site \{ font-size: calc\(1rem \* var\(--tb-hs\) / var\(--tb-size, 1\)\)")
        self.assertRegex(css, r"html \{[^}]*font-size: calc\(112\.5% \* var\(--tb-size, 1\)\)")
        for a in ("data-font", "data-align", "data-para", "data-corr", "data-links", "data-bar", "--tb-size", "--tb-lh", "--tb-width",
                  "--tb-ls", "--tb-ws"):
            self.assertIn(a, css)

    def test_home_shows_the_newest_when_there_are_many(self):
        books = [shelf_book(i) for i in range(build_site.HOME_FULL_LIST + 3)]
        build_site.build_books(self.out, books, [])
        h = self.read("books.html")
        self.assertIn('href="authors.html"', h)
        listed = re.findall(r"<cite>Journey (\d+)</cite>", h)
        self.assertEqual(listed, [str(i) for i in range(build_site.HOME_FULL_LIST + 2, build_site.HOME_FULL_LIST + 2 - build_site.HOME_NEWEST, -1)])

    def test_books_page_headings_in_order(self):
        """Review after forty-five books (live pass): "Newest" was an h3 straight after the page's h1."""
        books = [shelf_book(i) for i in range(build_site.HOME_FULL_LIST + 3)]
        build_site.build_books(self.out, books, [])
        levels = [int(x) for x in re.findall(r"<h([1-6])[ >]", self.read("books.html"))]
        self.assertTrue(all(b - a <= 1 for a, b in zip(levels, levels[1:])), levels)

    def test_newest_follows_the_time_of_first_publication(self):
        """2026-11-21: fourteen books were first published on one day, so the date tied and the id decided the order
        ("Yachting" before the day's last books). data/published.json keeps the time; new versions do not move a book."""
        books = [shelf_book(i, date="2026-12-09", history=[{"version": 1, "date": "2026-12-01"}, {"version": 2, "date": "2026-12-09"}])
                 for i in range(build_site.HOME_FULL_LIST + 3)]
        times = {b["id"]: f"2026-12-01T{10 + i % 12:02d}:{i:02d}:00Z" for i, b in enumerate(books)}
        build_site.build_books(self.out, books, [], times)
        listed = re.findall(r"<cite>Journey (\d+)</cite>", self.read("books.html"))
        want = [b["id"] for b in sorted(books, key=lambda b: times[b["id"]], reverse=True)][:build_site.HOME_NEWEST]
        self.assertEqual(["book-%02d" % int(n) for n in listed], want)

    def test_publish_records_the_first_publication_time_once(self):
        import publish
        d = tempfile.mkdtemp(); self.addCleanup(shutil.rmtree, d)
        f = os.path.join(d, "published.json")
        publish.record_first_publication(f, "a-book", 1, "2026-12-01T10:00:00Z")
        publish.record_first_publication(f, "a-book", 2, "2026-12-05T10:00:00Z")    # a new version: unchanged
        publish.record_first_publication(f, "b-book", 1, "2026-12-02T10:00:00Z")
        self.assertEqual(json.load(open(f)), {"a-book": "2026-12-01T10:00:00Z", "b-book": "2026-12-02T10:00:00Z"})

    def test_lists_by_place_and_date(self):
        books = [shelf_book(1), shelf_book(2, regions=["Japan", "Hokkaido", "Spain"], period="June 1878 to 1879"),
                 shelf_book(3, regions=["Atlantis"], period="")]
        build_site.build_lists(self.out, books, self.PLACES)
        p = self.read("places.html")
        self.assertLess(p.index('id="east-asia"'), p.index('id="europe"'))               # the order of places.json
        self.assertEqual(p.count("Journey 2</cite>"), 2)                                # once under each area, not once per region
        self.assertIn('id="other-places"', p)                                           # a region the table lacks is still listed
        d = self.read("dates.html")
        self.assertIn('id="d1840"', d)
        self.assertIn('id="d1870"', d)                                                  # the first year of the period
        self.assertIn('id="d1850"', d)                                                  # no period: the year of publication
        self.assertFalse(os.path.exists(os.path.join(self.out, "authors.html")))

    def test_authors_page_when_many(self):
        build_site.build_lists(self.out, [shelf_book(i) for i in range(build_site.HOME_FULL_LIST + 1)], self.PLACES)
        a = self.read("authors.html")
        self.assertEqual(a.count('<li><a href="books/'), build_site.HOME_FULL_LIST + 1)

    def test_jatsi_page(self):
        j = {"books": [{"n": 1, "year": 1860, "title": "First Visit", "author": "A. One", "scans": [{"label": "scan", "ia": "firstvisit00one", "url": "https://archive.org/details/firstvisit00one"}]},
                       {"n": 2, "year": 1860, "title": "Second Visit", "author": "B. Two", "note": "second edition", "scans": [], "gutenberg": [123]},
                       {"n": 3, "year": 1875, "title": "Third Visit", "author": "", "scans": []}]}
        queue = [{"slug": "book-01", "title": "First Visit", "author": "A. One", "year": 1860, "status": "published", "from": "jatsi", "jatsi": 1},
                 {"slug": "third", "title": "Third Visit", "author": "", "year": 1875, "status": "queued", "from": "jatsi", "jatsi": 3, "ia": "t"},
                 {"slug": "other", "title": "Elsewhere", "author": "C", "year": 1870, "status": "queued", "ia": "e"}]
        build_site.build_jatsi(self.out, [shelf_book(1, collection="jatsi")], queue, j)
        h = self.read("japan-as-they-saw-it.html")
        self.assertIn('<a href="books/book-01/index.html">on this site</a>', h)
        self.assertIn("gutenberg.org/ebooks/123", h)
        self.assertIn("(second edition)", h)
        self.assertEqual(h.count("— in the queue"), 1)
        self.assertNotIn("Elsewhere", h)
        self.assertLess(h.index('id="y1860"'), h.index('id="y1875"'))
        self.assertIn("list of 3 books", h)
        # on this page the books do not carry the mark "JATSI": it would say what the page says (Tom, 2026-11-20)
        self.assertIn("Journey 1", h)
        self.assertNotIn(">JATSI</a>", h)
        # the name with its short form; the link to Tom's project is on the name only (Tom, 2026-11-21)
        self.assertIn('<p><a href="https://www.gally.net/jatsi/index.html" target="_blank" rel="noopener">Japan As They Saw It</a> (JATSI) is an earlier project of Tom Gally', h)
        self.assertNotIn(">about</a>", h)

    def test_book_page_says_why_a_jatsi_book_is_here(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nText."], collection="jatsi")
        self.assertEqual(book["collection"], "jatsi")                                    # in the book JSON
        self.assertIn("Why it is here", build_site.book_page(book, rh.file_names(book, ".html")))
        book, _ = comp(["[[page 1]]\n# ONE\n\nText."])
        self.assertNotIn("Why it is here", build_site.book_page(book, rh.file_names(book, ".html")))

    def test_every_region_of_a_published_book_has_its_part_of_the_world(self):
        places = build_site.load_places()
        bdir = os.path.join(REPO, "books")
        for slug in sorted(os.listdir(bdir)) if os.path.isdir(bdir) else []:
            f = os.path.join(bdir, slug, "book.json")
            if os.path.exists(f):
                for r in json.load(open(f, encoding="utf-8")).get("regions", []):
                    self.assertIn(r, places["regions"], f"{slug}: add {r!r} to data/places.json")
        self.assertEqual(set(places["regions"].values()) - set(places["areas"]), set())


class Ledger(unittest.TestCase):
    """data/queue.json and data/jatsi.json: which kind of book is due, and the consistency check."""
    POLICY = {"others_before": 2, "others_per_jatsi": 2}

    def q(self, *rows):
        return {"jatsi_policy": self.POLICY, "books": [dict({"slug": f"s{i}", "title": "T", "author": "A", "year": 1900, "eligibility": "x", "ia": "i"}, **r)
                                                         for i, r in enumerate(rows)]}

    def test_one_jatsi_book_in_three(self):
        o, j = {"status": "published"}, {"status": "published", "from": "jatsi"}
        before = [o, o]                                       # published before the policy began: not counted
        seq = []
        rows = list(before)
        for _ in range(7):
            k = ledger.next_kind(self.q(*rows))
            seq.append(k)
            rows.append(j if k == "jatsi" else o)
        self.assertEqual(seq, ["jatsi", "other", "other", "jatsi", "other", "other", "jatsi"])

    def test_queued_and_waiting_books_do_not_count(self):
        rows = [{"status": "published"}] * 2 + [{"status": "in progress", "from": "jatsi"}, {"status": "queued"}, {"status": "waiting"}]
        self.assertEqual(ledger.next_kind(self.q(*rows)), "other")
        self.assertEqual(ledger.next_kind({"books": []}), "other")           # no policy, no JATSI turn

    def test_check_finds_what_is_wrong(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        os.makedirs(os.path.join(tmp, "books", "s0"))
        json.dump({"id": "s0", "collection": "jatsi"}, open(os.path.join(tmp, "books", "s0", "book.json"), "w"))
        os.makedirs(os.path.join(tmp, "wip", "stray"))
        json.dump({"id": "stray"}, open(os.path.join(tmp, "wip", "stray", "book.json"), "w"))
        j = {"books": [{"n": 1}, {"n": 2}]}
        q = self.q({"status": "published"},                                  # book.json says JATSI, the row does not
                   {"status": "queued", "from": "jatsi", "jatsi": 9},      # no such number
                   {"status": "done"},                                       # not a status
                   {"status": "published", "from": "jatsi", "jatsi": 2})   # published, no book
        got = "\n".join(ledger.check(q, j, tmp))
        for want in ("disagree about JATSI", "is not a number in data/jatsi.json", "status 'done'", "book.json is missing", "wip/stray: no row",
                     "s0: published but has no time in data/published.json"):
            self.assertIn(want, got)
        good = self.q({"status": "published", "from": "jatsi", "jatsi": 1})
        shutil.rmtree(os.path.join(tmp, "wip"))
        os.makedirs(os.path.join(tmp, "data"))
        json.dump({"s0": "2026-12-01T10:00:00Z"}, open(os.path.join(tmp, "data", "published.json"), "w"))
        self.assertEqual(ledger.check(good, j, tmp), [])

    def test_waiting_book_may_keep_its_wip_folder(self):
        """A book set to `waiting` mid-way keeps wip/<slug>/ and its log (RESUME.md §2.3; *Uganda for a Holiday*,
        2026-11-21: the check called that an error)."""
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        for d in ("wip", "books"):
            os.makedirs(os.path.join(tmp, d, "s0"))
            json.dump({"id": "s0"}, open(os.path.join(tmp, d, "s0", "book.json"), "w"))
        shutil.rmtree(os.path.join(tmp, "books"))
        self.assertEqual(ledger.check(self.q({"status": "waiting"}), {"books": []}, tmp), [])
        os.makedirs(os.path.join(tmp, "books", "s0"))
        json.dump({"id": "s0"}, open(os.path.join(tmp, "books", "s0", "book.json"), "w"))
        self.assertIn("is in books/", "\n".join(ledger.check(self.q({"status": "waiting"}), {"books": []}, tmp)))

    def test_the_real_ledger_is_consistent(self):
        q, j = ledger.load()
        self.assertEqual(ledger.check(q, j), [])
        self.assertIn("Next new book", ledger.report(q, j))


class SessionMeter(unittest.TestCase):
    """tools/session_meter.py: the context in use and the time elapsed, from an invented transcript."""

    def lines(self, *rows):
        d = tempfile.mkdtemp(); self.addCleanup(shutil.rmtree, d)
        p = os.path.join(d, "t.jsonl")
        with open(p, "w") as f:
            for r in rows:
                f.write((r if isinstance(r, str) else json.dumps(r)) + "\n")
        return p

    def reply(self, ts, inp, cache=0, out=0, side=False):
        return {"type": "assistant", "isSidechain": side, "timestamp": ts,
                "message": {"usage": {"input_tokens": inp, "cache_read_input_tokens": cache, "cache_creation_input_tokens": 0, "output_tokens": out}}}

    def test_context_is_the_last_main_reply(self):
        p = self.lines({"type": "user", "timestamp": "2026-01-01T10:00:00.000Z"},
                       self.reply("2026-01-01T10:01:00.000Z", 10, 30000, 500),
                       self.reply("2026-01-01T10:30:00.000Z", 5, 900000, 100, side=True),     # a subagent: not counted
                       self.reply("2026-01-01T11:00:00.000Z", 20, 59000, 980),
                       '{"type": "assistant", "message": {"usa')                               # a line being written
        m = session_meter.read(p)
        self.assertEqual((m["tokens"], m["peak"], m["compactions"]), (60000, 60000, 0))
        import datetime
        r = session_meter.report(m, 200000, now=datetime.datetime(2026, 1, 1, 12, 30, tzinfo=datetime.timezone.utc))
        self.assertEqual((r["percent"], r["hours"], r["start"]), (30, 2.5, "2026-01-01 10:00"))

    def test_a_summarized_conversation_is_counted(self):
        p = self.lines(self.reply("2026-01-01T10:00:00.000Z", 0, 150000), self.reply("2026-01-01T10:05:00.000Z", 0, 40000),
                       self.reply("2026-01-01T10:06:00.000Z", 0, 45000))
        self.assertEqual(session_meter.read(p)["compactions"], 1)
        p = self.lines(self.reply("2026-01-01T10:00:00.000Z", 0, 150000), {"type": "system", "subtype": "compact_boundary"},
                       {"type": "user", "isCompactSummary": True}, self.reply("2026-01-01T10:05:00.000Z", 0, 140000))
        self.assertGreaterEqual(session_meter.read(p)["compactions"], 1)

    def test_finds_the_session_and_says_when_it_cannot(self):
        home = tempfile.mkdtemp(); self.addCleanup(shutil.rmtree, home)
        self.assertIsNone(session_meter.find_transcript(home, "abc"))
        d = os.path.join(home, ".claude", "projects", "x"); os.makedirs(d)
        for n in ("abc", "other"):
            open(os.path.join(d, n + ".jsonl"), "w").close()
        self.assertTrue(session_meter.find_transcript(home, "abc").endswith("abc.jsonl"))
        self.assertEqual(session_meter.main(["--transcript", os.path.join(home, "none.jsonl")]), 2)
        self.assertEqual(session_meter.window("1000000"), 1000000)
        self.assertEqual(session_meter.window("x"), session_meter.WINDOW)


if __name__ == "__main__":
    unittest.main()


class MovedImages(unittest.TestCase):
    """The compiler moves some images; conservation must follow them (it failed a finished book, 2026-11-19)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        img = os.path.join(self.dir, "images", "p0007-1.jpg")
        for leaf, old, new in (
                # a plate at the foot of a page whose paragraph runs on to the next page
                ("p0004", "for an hour, while\n", "for an hour, while\n\n[[image: a cart in a ford]]\n[[caption]] The Cart at the Ford.\n"),
                # a captioned frontispiece in the front matter
                ("p0001", "1861\n", "1861\n\n[[image: portrait of a woman]]\n[[caption]] The Author.\n")):
            p = os.path.join(self.dir, "pages", leaf + ".txt")
            t = open(p, encoding="utf-8").read()
            self.assertIn(old, t)
            open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
            shutil.copy(img, os.path.join(self.dir, "images", leaf + "-1.jpg"))
        c = json.load(open(os.path.join(self.dir, "book.json"), encoding="utf-8"))
        c["frontispiece"] = "p0001-1"
        json.dump(c, open(os.path.join(self.dir, "book.json"), "w", encoding="utf-8"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_plate_in_paragraph_and_captioned_frontispiece_pass(self):
        book, _ = compile_book.compile_book(self.dir)
        first = next(d for d in book["divisions"] if d["reading"])
        self.assertEqual(first["kind"], "titlepage")       # the picture is on the title page, which is in the editions
        self.assertIn("The Author.", [b.get("caption") for b in first["blocks"]])
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["conservation"], [], report)
        self.assertEqual(res["compile"], [], report)

    def test_caption_lost_is_still_caught(self):
        pages = [("p0001", "[[page 1]]\nText.\n[[image: x]]\n[[caption]] A Caption.")]
        book = {"divisions": [{"reading": True, "notes": [], "blocks": [
            {"type": "paragraph", "text": "Text."}, {"type": "image", "caption": "Another Caption."}]}]}
        pc, jc = [], []
        self.assertEqual(preflight.page_streams(pages, captions=pc)[0], preflight.json_streams(book, captions=jc)[0])
        self.assertTrue(preflight.compare(" ".join(sorted(pc)), " ".join(sorted(jc)), "captions"))

    def test_caption_not_after_an_image_stays_in_the_text(self):
        pc = []
        main, _ = preflight.page_streams([("p0001", "[[page 1]]\nText.\n[[caption]] Stray.")], captions=pc)
        self.assertEqual((main.split(), pc), (["Text.", "Stray."], []))

    def test_long_texts_list_each_difference(self):
        a = "".join(f"word{i} " for i in range(12000))
        b = a.replace("word50 ", "", 1).replace("word9000 ", "wurd9000 ", 1)
        items = preflight.compare(a, b, "t")
        self.assertEqual(len(items), 1)                       # two far apart: the first, as before
        items = preflight.compare(a, a.replace("word9000 ", "", 1).replace("word9005 ", "wurd9005 ", 1), "t")
        self.assertEqual(len(items), 2, items)                # close together: each is listed, so a waiver can name one
        self.assertEqual(preflight.compare(a, a, "t"), [])


class SideNotes(unittest.TestCase):
    """Marginal notes (Staunton's Embassy, 2026-11-20): kept in the JSON, left out of the reading editions."""

    def test_convert_plain_and_drop(self):
        s = inline.convert('at [[side: Occasion of the "Embassy."]] the Embassy was')
        self.assertEqual(s, 'at <side>Occasion of the “Embassy.”</side>the Embassy was')
        self.assertEqual(inline.plain(s), "at the Embassy was")
        self.assertEqual(inline.drop_sides(s), "at the Embassy was")
        self.assertEqual(inline.sides(s), ["Occasion of the “Embassy.”"])
        end = inline.convert("He sailed. [[side: <i>Lion</i> sails.]]")
        self.assertEqual((end, inline.drop_sides(end)), ("He sailed.<side><i>Lion</i> sails.</side>", "He sailed."))

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        p = os.path.join(self.dir, "pages", "p0004.txt")
        t = open(p, encoding="utf-8").read()
        old = "The carrier had promised nothing;"
        self.assertIn(old, t)
        t = t.replace("W<sc>e</sc> left", "[[side: Leaving the town.]] W<sc>e</sc> left", 1)
        open(p, "w", encoding="utf-8").write(t.replace(old, "The [[side: The carrier.]] carrier had promised nothing;", 1))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_json_keeps_editions_drop(self):
        book, _ = compile_book.compile_book(self.dir)
        js = [x for d in book["divisions"] for b in d["blocks"] for s in rh.strings(b) for x in inline.sides(s)]
        self.assertEqual(js, ["Leaving the town.", "The carrier."])
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        for k in ("conservation", "markup", "stray-markup", "compile"):
            self.assertEqual(res.get(k, []), [], report)
        out = os.path.join(self.tmp, "site")
        build_site.build_book(out, self.dir)
        bdir = os.path.join(out, "books", book["id"])
        html = "".join(open(os.path.join(bdir, f), encoding="utf-8").read() for f in os.listdir(bdir) if f.endswith(".html"))
        self.assertNotIn("Leaving the town", html)
        self.assertIn("The carrier had promised nothing", html)
        odt = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".odt")).read("content.xml").decode("utf-8")
        self.assertNotIn("Leaving the town", odt)
        epub = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".epub"))
        self.assertFalse(any("Leaving the town" in epub.read(n).decode("utf-8", "replace") for n in epub.namelist() if n.endswith(".xhtml")))

    def test_hyphen_join_over_a_side_note(self):
        book, w = comp(["[[page 1]]\n# One\n\nHe was accompa-", "[[page 2]]\n[[cont]][[side: Teneriffe.]] nied by two."])
        self.assertEqual(inline.plain(texts(book)[1]), "He was accompanied by two.")
        self.assertIn("accompa-|nied by two", w[0])               # the word after the join, not the side-note
        tri = preflight.triage_hyphen_joins(w, [("p0001", "x accompanied y")])
        self.assertEqual(tri, ["(and 1 joins giving a word the book prints whole elsewhere: not listed)"])

    def test_lost_side_note_is_caught(self):
        pages = [("p0001", "[[page 1]]\n[[side: A note.]] Text.")]
        ps, js = [], []
        book = {"divisions": [{"reading": True, "notes": [], "blocks": [{"type": "paragraph", "text": "Text."}]}]}
        self.assertEqual(preflight.page_streams(pages, sides=ps)[0].split(), preflight.json_streams(book, sides=js)[0].split())
        self.assertEqual(ps, ["A note."])
        self.assertTrue(preflight.compare(" ".join(ps), " ".join(js), "side-notes"))


class LostText(unittest.TestCase):
    """Text lost in the scan (Tom, 2026-11-20): letters inferred from the context are marked in the JSON only
    ([[supplied …]] → <supplied>, plain in the editions); a loss that cannot be inferred is [[gap]] → […] everywhere."""

    def test_convert_and_plain(self):
        s = inline.convert("from the anchorag[[supplied e of]] the Hindostan and [[gap]] by sea")
        self.assertEqual(s, "from the anchorag<supplied>e of</supplied> the Hindostan and <gap>[…]</gap> by sea")
        self.assertEqual(inline.plain(s), "from the anchorage of the Hindostan and […] by sea")

    def test_editions_and_preflight(self):
        tmp = tempfile.mkdtemp()
        try:
            d = os.path.join(tmp, "sample-journey-doe")
            shutil.copytree(SAMPLE, d)
            p = os.path.join(d, "pages", "p0004.txt")
            t = open(p, encoding="utf-8").read()
            old = "The carrier had promised nothing;"
            self.assertIn(old, t)
            open(p, "w", encoding="utf-8").write(t.replace(old, "The car[[supplied rier]] had promised [[gap]] nothing;", 1))
            book, _ = compile_book.compile_book(d)
            js = " ".join(s for dv in book["divisions"] for b in dv["blocks"] for s in rh.strings(b))
            self.assertIn("car<supplied>rier</supplied> had promised <gap>[…]</gap> nothing", js)
            _, report, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
            for k in ("conservation", "markup", "stray-markup", "compile"):
                self.assertEqual(res.get(k, []), [], report)
            out = os.path.join(tmp, "site")
            build_site.build_book(out, d)
            bdir = os.path.join(out, "books", book["id"])
            html = "".join(open(os.path.join(bdir, f), encoding="utf-8").read() for f in os.listdir(bdir) if f.endswith(".html"))
            self.assertIn("The carrier had promised […] nothing", html)
            self.assertNotIn("supplied", html)
            odt = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".odt")).read("content.xml").decode("utf-8")
            self.assertIn("The carrier had promised […] nothing", odt)
            epub = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".epub"))
            x = "".join(epub.read(n).decode("utf-8") for n in epub.namelist() if n.endswith(".xhtml"))
            self.assertIn("The carrier had promised […] nothing", x)
            self.assertNotIn("supplied", x)
        finally:
            shutil.rmtree(tmp)


class Volumes(unittest.TestCase):
    """A work in several IA items, and leaves bound out of order (Staunton's Embassy, 2026-11-20)."""
    SRC = {"ia_identifier": "vol1", "items": [
        {"ia_identifier": "vol1", "first_leaf": "p1000", "hidden_leaves": [0, 7]},
        {"ia_identifier": "vol2", "first_leaf": "p2000", "hidden_leaves": [0, 24, 25]}]}

    def test_scan_links_per_item(self):
        ctx = rh.Ctx({"source": self.SRC, "pages": [], "divisions": []}, "web", {})
        self.assertEqual(ctx.scan_url("p1068"), "https://archive.org/details/vol1/page/n66/mode/1up")
        self.assertEqual(ctx.scan_url("p2030"), "https://archive.org/details/vol2/page/n27/mode/1up")
        one = rh.Ctx({"source": {"ia_identifier": "x", "hidden_leaves": [0]}, "pages": [], "divisions": []}, "web", {})
        self.assertEqual(one.scan_url("p0005"), "https://archive.org/details/x/page/n4/mode/1up")

    def test_leaf_from_another_copy(self):
        src = dict(self.SRC, extra_leaves={"p2029b": {"ia_identifier": "getty2", "n": 30}})
        ctx = rh.Ctx({"source": src, "pages": [], "divisions": []}, "web", {})
        self.assertEqual(ctx.scan_url("p2029b"), "https://archive.org/details/getty2/page/n30/mode/1up")
        self.assertEqual(ctx.scan_url("p2030"), "https://archive.org/details/vol2/page/n27/mode/1up")
        self.assertEqual(compile_book.page_files_sorted(["p2030.txt", "p2029b.txt", "p2029.txt", "p2029a.txt"]),
                         ["p2029.txt", "p2029a.txt", "p2029b.txt", "p2030.txt"])

    def test_leaves_checked_per_item(self):
        items = compile_book.scan_items(self.SRC)
        pages = [(f"p{n:04d}", "") for n in list(range(1001, 1007)) + list(range(1008, 1011)) + list(range(2001, 2024)) + [2026, 2028]]
        self.assertEqual(preflight.check_leaves(pages, items=items), ["p2027: no page file"])

    def test_book_page_lists_every_item(self):
        src = copy.deepcopy(self.SRC)
        src["items"][0]["label"], src["items"][1]["label"] = "Volume I", "Volume II"
        book = {"id": "t", "title": "T", "version": 1, "date": "d", "source": src, "pages": [], "divisions": []}
        x = build_site.book_page(book, {})
        self.assertEqual(x.count("<iframe"), 2)
        self.assertIn("The scan of Volume II at the Internet Archive", x)
        self.assertIn('archive.org/embed/vol2', x)

    def test_leaf_order(self):
        pages = [(f"p{n}", n) for n in (1466, 1467, 1468, 1469, 1470, 1471)]
        out = compile_book.apply_leaf_order(pages, [["p1469", "p1470", "p1467", "p1468"]])
        self.assertEqual([x for x, _ in out], ["p1466", "p1469", "p1470", "p1467", "p1468", "p1471"])
        with self.assertRaises(ValueError):
            compile_book.apply_leaf_order(pages, [["p1469", "p9999"]])


class RunningQuotes(unittest.TestCase):
    """Opening marks repeated at each printed line of a quotation (1797 printing, 2026-11-20)."""

    def test_repeats_removed_and_carried_over_the_page(self):
        pages = [("p0001", '[[page 1]]\nHe wrote, “that the “bar was “crossed,” and that ‘one’ called it “a little damp.”\n\n“In the ab“sence of wind'),
                 ("p0002", "[[page 2]]\n[[cont]][[side: Rio.]] “we lay still.”\n\n“A new paragraph.”")]
        out, ch = running_quotes.process(pages)
        self.assertEqual(out[0][1].split("\n")[1], "He wrote, “that the bar was crossed,” and that ‘one’ called it “a little damp.”")
        self.assertEqual(out[0][1].split("\n")[3], "“In the absence of wind")
        self.assertEqual(out[1][1], "[[page 2]]\n[[cont]][[side: Rio.]] we lay still.”\n\n“A new paragraph.”")
        self.assertEqual(len(ch), 4)

    def test_notes_and_new_paragraphs_untouched(self):
        pages = [("p0001", "[[page 1]]\n“Open quote\n\n[[fn *]] “A note “with marks.")]
        out, ch = running_quotes.process(pages)
        self.assertEqual((out, ch), (pages, []))


class Fallback(unittest.TestCase):
    """Pages the output filter refuses get a machine-OCR draft that a model corrects (tools/ocr_fallback.py)."""

    def test_to_markup(self):
        import ocr_fallback
        raw = "106 A HEAD.\n\nThe first para-\ngraph runs on to twenty-\nThird Street\nhere.\n\n  \nSecond one.\n"
        self.assertEqual(ocr_fallback.to_markup(raw),
                         "[[page ?]]\n\n106 A HEAD.\n\nThe first paragraph runs on to twenty-Third Street here.\n\nSecond one.\n")

    def test_refused_pages_from_the_log(self):
        import ocr_fallback
        d = tempfile.mkdtemp()
        try:
            refusal = "RuntimeError('API Error: Output blocked by content filtering policy')"
            recs = [{"page": "p0001", "cost": 0.1}, {"page": "p0002", "error": refusal}, {"page": "p0003", "error": "timeout"},
                    {"page": "p0004", "error": refusal}, {"page": "p0004", "cost": 0.1}, {"page": "p0005", "error": refusal}]
            open(os.path.join(d, "log.jsonl"), "w").write("\n".join(json.dumps(r) for r in recs) + "\n")
            open(os.path.join(d, "p0005.txt"), "w").write("x")          # already has a draft
            self.assertEqual(ocr_fallback.refused_pages(d), ["p0002"])
        finally:
            shutil.rmtree(d)

    def test_page_lists(self):
        import ocr_claude, ocr_fallback
        self.assertEqual(ocr_claude.page_numbers("20-22"), [20, 21, 22])
        self.assertEqual(ocr_claude.page_numbers("116-118,128"), [116, 117, 118, 128])
        self.assertEqual(ocr_fallback.parse_pages("p0116-p0118,128"), [116, 117, 118, 128])


class Refusal(unittest.TestCase):
    """The output filter's refusal is never retried; corrections mode makes no call for a page with no draft."""

    def setUp(self):
        import ocr_claude, judge as jd, audit_sample  # noqa: F401
        self.mods = (ocr_claude, jd, audit_sample)
        self.tmp = tempfile.mkdtemp()
        self.calls = 0

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def fake_run(self, *a, **k):
        self.calls += 1
        class R:
            stdout = json.dumps({"is_error": True, "result": "API Error: Output blocked by content filtering policy"})
        return R()

    def patched(self, mod):
        from unittest import mock
        return mock.patch.multiple(mod, time=mock.DEFAULT), mock.patch.object(mod.subprocess, "run", self.fake_run)

    def test_is_refusal(self):
        from refusal import is_refusal
        self.assertTrue(is_refusal("RuntimeError('API Error: Output blocked by content filtering policy')"))
        self.assertFalse(is_refusal("RuntimeError('timeout')"))
        self.assertFalse(is_refusal(None))

    def test_ocr_not_retried(self):
        from types import SimpleNamespace
        ocr = self.mods[0]
        args = SimpleNamespace(out=self.tmp, context_text=None, halves=False, corrections=False, model="opus")
        a, b = self.patched(ocr)
        with a, b:
            rec = ocr.do_page(args, "prompt", os.path.join(self.tmp, "p0001.jpg"))
        self.assertEqual(self.calls, 1)
        self.assertIn("content filtering", rec["error"])

    def test_judge_and_audit_not_retried(self):
        for mod in self.mods[1:]:
            self.calls = 0
            a, b = self.patched(mod)
            with a, b:
                res, info = mod.call("prompt", "opus", self.tmp)
            self.assertIsNone(res)
            self.assertEqual(self.calls, 1, mod.__name__)

    def test_corrections_without_draft_makes_no_call(self):
        from types import SimpleNamespace
        ocr = self.mods[0]
        ctx = os.path.join(self.tmp, "draft"); os.makedirs(ctx)
        args = SimpleNamespace(out=self.tmp, context_text=ctx, halves=False, corrections=True, model="sonnet")
        a, b = self.patched(ocr)
        with a, b:
            rec = ocr.do_page(args, "prompt", os.path.join(self.tmp, "p0002.jpg"))
        self.assertEqual(self.calls, 0)
        self.assertIn("no draft", rec["error"])


class Leaves(unittest.TestCase):
    """A leaf with no page file inside the run (a refused draft) is listed; folios alone cannot see it."""

    def test_gap(self):
        pages = [("p0010", "[[page 1]]"), ("p0011", "[[page 2]]"), ("p0014", "[[page 5]]")]
        self.assertEqual(preflight.check_leaves(pages), ["p0012: no page file", "p0013: no page file"])
        self.assertEqual(preflight.check_folios(pages), [])

    def test_none(self):
        self.assertEqual(preflight.check_leaves([("p0001", ""), ("p0002", "")]), [])
        self.assertEqual(preflight.check_leaves([]), [])

    def test_hidden_not_missing(self):
        pages = [("p0006", ""), ("p0009", ""), ("p0011", "")]
        self.assertEqual(preflight.check_leaves(pages, [0, 7, 8, 450]), ["p0010: no page file"])

    def test_enforced(self):
        self.assertEqual(preflight.CHECKS["leaves"][0], "enforce")


class Joins(unittest.TestCase):
    """Review 2026-11-20 (ten books): the "[[cont]] after a closed sentence" half gave 65 alarms, 0 real (pages that
    start flush left go on with the paragraph), so it was dropped; the "missing [[cont]]" half found real ones."""

    def test_cont_after_closed_sentence_not_listed(self):
        pages = [("p0010", "He went home."), ("p0011", "[[cont]] The next day it rained.")]
        self.assertEqual(preflight.check_joins(pages), [])

    def test_missing_cont_still_listed(self):
        pages = [("p0010", "He went home and"), ("p0011", "slept till noon.")]
        self.assertEqual(len(preflight.check_joins(pages)), 1)
        pages = [("p0010", "a hyphen-"), ("p0011", "ated word.")]
        self.assertEqual(len(preflight.check_joins(pages)), 1)


class ImageSplits(unittest.TestCase):
    """Review 2026-11-20: four paragraphs of *South by West* v1 were split in two by an engraving in mid-sentence (no
    `[[cont]]` after the caption); the compiler cannot know, so preflight lists them."""

    def book(self, *blocks):
        return {"divisions": [{"reading": True, "blocks": [dict(b, leaf="p0001") for b in blocks]}]}

    def test_split_listed(self):
        b = self.book({"type": "paragraph", "text": "four cups, but no"}, {"type": "image", "src": "x"},
                      {"type": "paragraph", "text": "saucers; and we"})
        self.assertEqual(len(preflight.check_image_splits(b)), 1)

    def test_title_page_not_listed(self):
        # 2026-11-22: the title page is in the reading editions; a device between "1898" and "copyright, 1898" is no split
        b = self.book({"type": "paragraph", "text": "1898"}, {"type": "image", "src": "x"}, {"type": "paragraph", "text": "copyright, by a. b."})
        self.assertEqual(len(preflight.check_image_splits(b)), 1)
        b["divisions"][0]["kind"] = "titlepage"
        self.assertEqual(preflight.check_image_splits(b), [])

    def test_closed_or_capital_or_verse_not_listed(self):
        b = self.book({"type": "paragraph", "text": "He went home."}, {"type": "image", "src": "x"},
                      {"type": "paragraph", "text": "and then"},
                      {"type": "paragraph", "text": "the song goes"}, {"type": "verse", "lines": []},
                      {"type": "paragraph", "text": "and so on"},
                      {"type": "paragraph", "text": "so far as"}, {"type": "image", "src": "x"},
                      {"type": "paragraph", "text": "The next day"})
        self.assertEqual(preflight.check_image_splits(b), [])

    def test_enforced(self):
        # review after fifteen books (2026-11-20): 10 alarms in three books, 10 real
        self.assertEqual(preflight.CHECKS["image-splits"][0], "enforce")


class CorrectionPage(unittest.TestCase):
    """A correction on an unnumbered page was listed on the book page by its leaf name ("p0013"), which means
    nothing to a reader (*Cruise*, *West Coast*, *From West Africa to Palestine*; open since the review of 2026-11-19)."""

    def test_unnumbered_page_named_by_division(self):
        book = {"divisions": [{"id": "d005", "title": "Contents."}]}
        c = {"leaf": "p0013", "division": "d005", "printed": "Maderia", "corrected": "Madeira"}
        self.assertEqual(build_site.correction_page(book, c, {"p0013": ""}), "Contents, unnumbered page")

    def test_abbreviation_kept(self):
        book = {"divisions": [{"id": "d020", "title": "Publications of J. Griffin & Co.,"}]}
        c = {"leaf": "p0400", "division": "d020", "printed": "x", "corrected": "y"}
        self.assertEqual(build_site.correction_page(book, c, {}), "Publications of J. Griffin & Co., unnumbered page")

    def test_numbered_page_keeps_number(self):
        c = {"leaf": "p0042", "division": "d009", "printed": "a", "corrected": "b"}
        self.assertEqual(build_site.correction_page({"divisions": []}, c, {"p0042": "36"}), "36")


class NoteTail(unittest.TestCase):
    """*My Life in Mongolia and Siberia* (2026-11-20): a footnote with a table and a second paragraph typed on lines
    of their own after `[[fn 1]]`; the compiler set them as body text (caught only by the rendered look)."""

    def test_table_after_note_listed(self):
        pages = [("p0011", "[[page viii]]\nText.[[fnref 1]]\n\n[[fn 1]] Figures for the years.\n| a | 1 |\nMore of the note.\n")]
        items = preflight.check_note_tail(pages)
        self.assertEqual(len(items), 1)
        self.assertIn("p0011", items[0])

    def test_notes_only_pass(self):
        pages = [("p0012", "[[page ix]]\nText.[[fnref *]] More.[[fnref †]]\n\n[[fn *]] One.\n\n[[fn †]] Two.\n"),
                 ("p0013", "[[page x]]\n[[fn cont]] the rest of a note.\n")]
        self.assertEqual(preflight.check_note_tail(pages), [])

    def test_observe(self):
        self.assertEqual(preflight.CHECKS["note-tail"][0], "observe")


class ImageBeforeHeading(unittest.TestCase):
    """*Present-Day Japan* (2026-11-22): a picture printed above "CHAPTER I" fell into the division before."""

    def test_picture_above_heading_listed(self):
        pages = [("p0025", "[[page 1]]\n[[image: a junk]]\n[[caption]] A Junk.\n\n# Chapter I\n\nOUR first glimpse.\n"),
                 ("p0026", "[[page 2]]\n# Chapter II\n\n[[image: a boat]]\n[[caption]] A Boat.\n\nText.\n"),
                 ("p0027", "[[page 3]]\n[[image: a band of leaves]]\n# Chapter III\n\nText.\n")]
        items = preflight.check_image_before_heading(pages, {"p0027-1"})
        self.assertEqual([i.split(":")[0] for i in items], ["p0025"])

    def test_observe(self):
        self.assertEqual(preflight.CHECKS["image-before-heading"][0], "observe")


class CaptionTail(unittest.TestCase):
    """*Uganda for a Holiday* (2026-11-21): a plate's cross-reference ("[See page 107.") typed as a `[[right]]` line
    after the caption became a paragraph that the next page's `[[cont]]` joined, so text was right-aligned under the
    picture; *Argentine Plains* the same with "To face p. N" lines. Only the rendered look saw it."""

    def test_line_after_caption_listed(self):
        pages = [("p0118", "[[page ?]]\n[[image: men]]\n[[caption]] Kikuyu Station.\n\n[[right]] [<i>See</i> page <pref>107</pref>.\n"),
                 ("p0119", "[[page 79]]\n[[cont]]zebras in thousands.\n"),
                 ("p0120", "[[page ?]]\n[[image: a lake]]\n[[caption]] The Lake.\nTo face p. 80.\n")]
        items = preflight.check_caption_tail(pages)
        self.assertEqual([i.split(":")[0] for i in items], ["p0118", "p0120"])

    def test_caption_then_picture_or_text_pass(self):
        pages = [("p0140", "[[page ?]]\n[[image: a street]]\n[[caption]] Nairobi.\n[[image: a lake]]\n[[caption]] Lake Naivasha. [<i>See</i> page <pref>115</pref>.\n"),
                 ("p0141", "[[page 9]]\n[[image: a hut]]\n[[caption]] A hut.\n\nThe road went on for many miles through the long grass, and we saw no one.\n")]
        self.assertEqual(preflight.check_caption_tail(pages), [])

    def test_observe(self):
        self.assertEqual(preflight.CHECKS["caption-tail"][0], "observe")


class SiteText(unittest.TestCase):
    """*West Coast of Africa* (2026-11-20): contents titles written by hand in book.json kept straight apostrophes,
    which reached the site and the EPUB nav; the text checks read only the page files."""

    def test_straight_quotes_in_book_json_listed(self):
        cfg = {"title": "A Book", "summary": ["He said \"no\"."], "notes_on_text": ["The book's title"],
               "divisions": [{"at": "p0015", "toc_title": "Chapter I. A Missionary's Funeral"}],
               "toc_entries": [{"at": "p0020", "title": "May 1872: Lagos"}]}
        items = preflight.check_site_text(cfg)
        self.assertEqual(len(items), 4)  # both marks of "no" count
        self.assertTrue(any("p0015" in i for i in items))

    def test_every_quote_in_a_field_listed(self):
        self.assertEqual(len(preflight.check_site_text({"summary": "The Sun's and the Rajah's"})), 2)

    def test_curly_quotes_pass(self):
        cfg = {"title": "A Book", "summary": "The book’s “title”.", "omitted_from_reading": "All in the JSON."}
        self.assertEqual(preflight.check_site_text(cfg), [])

    def test_enforced(self):
        # review after twenty books (2026-11-20): 7 alarms in three books, 7 real; the other books none
        self.assertEqual(preflight.CHECKS["site-text"][0], "enforce")


class Accents(unittest.TestCase):
    """*Land of the North Wind* (2026-11-20): 23 words spelled with different accents in different places, 35 pages
    misread; found only by a hand-made list. Review after twenty books: preflight lists such groups."""

    def test_variant_groups_listed(self):
        pages = [("p0010", "The village of Kuhrúd lay *below* the pass."), ("p0011", "We left Kuhrud at dawn; the café."),
                 ("p0012", "[[corr Tehrán|Tehran]] and Tehran."), ("p0013", "A colossál statue, a colossal one.")]
        items = preflight.check_accents(pages)
        self.assertEqual(len(items), 2)
        self.assertTrue(items[0].startswith("colossal: colossal (p0013); colossál (p0013)"))
        self.assertIn("kuhrud (p0011); kuhrúd (p0010)", items[1])

    def test_consistent_or_unaccented_not_listed(self):
        pages = [("p0001", "The café and the café; a cafe-chantant."), ("p0002", "Plain words only, Words.")]
        # "cafe" (from the hyphened compound) against "café" is a real variant group
        self.assertEqual(len(preflight.check_accents(pages)), 1)
        self.assertEqual(preflight.check_accents([("p0001", "Saké and saké. Words and WORDS.")]), [])

    def test_observe(self):
        self.assertEqual(preflight.CHECKS["accents"][0], "observe")
        self.assertEqual(preflight.CHECKS["cover"][0], "enforce")


class Misprints(unittest.TestCase):
    """*Trans-Caspia* “we ean not” (a reader, issue #100, 2026-11-21): a printed turned letter copied faithfully by
    every stage and never marked. Preflight lists such forms of common words."""

    def test_listed(self):
        pages = [("p0001", "We ean not go; tbe road is shut, aud it rains."), ("p0002", "All is well <i>iu</i> here.")]
        items = preflight.check_misprints(pages)
        self.assertEqual([i.split(":")[0] for i in items], ["p0001", "p0001", "p0001", "p0002"])
        self.assertIn("“ean”", items[0])

    def test_marked_or_real_words_not_listed(self):
        pages = [("p0001", "We [[corr ean|can]] not; the tide; Kiushiu and Tean; audible; [[page 12]] and."),
                 ("p0002", "[[image: tbe house]] The house of Aud; M<sc>c</sc>L<sc>ean</sc>.")]
        self.assertEqual(preflight.check_misprints(pages), [])

    def test_bridal_forms(self):
        """*The Bridal and the Bridle* (2026-11-22): “iustead”, “wc”, “ofl ive” printed, found only by the spot-read."""
        pages = [("p0101", "far when, iustead of his overtaking us, wc met him"), ("p0224", "a brazier ofl ive coals")]
        self.assertEqual(len(preflight.check_misprints(pages)), 3)

    def test_th_for_the(self):
        """*Cordillera and Pampa* “depôt of th Pacific” (a reader, issue #169) and *The Bridal and the Bridle* “was th
        response”: a letter dropped at a line end. “4<sup>th</sup>” and “th’” (dialect) are not listed."""
        pages = [("p0017", "the depôt of th Pacific coast"), ("p0097", "was th response"),
                 ("p0041", "on the 4<sup>th</sup> of May, the 21th day; 5 th. Wi’ th’ lads")]
        self.assertEqual([i.split(":")[0] for i in preflight.check_misprints(pages)], ["p0017", "p0097"])

    def test_observe(self):
        self.assertEqual(preflight.CHECKS["misprints"][0], "observe")


class TableCorr(unittest.TestCase):
    """*Argentine Plains* p0028 (2026-11-21): a printer's error marked [[corr a|b]] in a table cell (the list of
    illustrations) was split at the | of the mark, so the markup showed in the editions."""

    def test_corr_inside_a_cell_stays_whole(self):
        _, _, blocks = compile_book.parse_page("| [[corr Entensibilty|Extensibility]] of a Body | <pref>18</pref> |\n| Plain | 2 |", "p0001")
        rows = [b for b in blocks if b["t"] == "table"][0]["rows"]
        self.assertEqual(rows[0], ["[[corr Entensibilty|Extensibility]] of a Body", "<pref>18</pref>"])
        self.assertEqual(rows[1], ["Plain", "2"])


class MissingStop(unittest.TestCase):
    """*The Golden Dagon* p. 7 “hard work and privation His orders” (a reader, issue #117, 2026-11-21): a full stop
    left out in print, copied faithfully by every stage and never marked. Preflight lists a sentence-opening word
    after a lower-case word with no stop between."""

    def test_listed(self):
        pages = [("p0001", "A season of privation His orders were plain.\n\nWe sat till midnight It was late."),
                 ("p0002", "[[cont]]all day There we stayed.")]
        items = preflight.check_missing_stop(pages)
        self.assertEqual([i.split(":")[0] for i in items], ["p0001", "p0001", "p0002"])
        self.assertIn("privation His", items[0])

    def test_marked_or_set_apart_not_listed(self):
        pages = [("p0001", "of [[corr privation|privation.]] His orders; <i>sur la mer The</i> x; the story. It was; thank God that He has given; the veil of His protection."),
                 ("p0002", "<verse>\nO for a lodge in some vast wilderness\nThe boundless contiguity of shade\n</verse>"),
                 ("p0003", "| a field | The house |\n# Chapter the First The end\n[[image: a field The house]]")]
        self.assertEqual(preflight.check_missing_stop(pages), [])

    def test_observe(self):
        self.assertEqual(preflight.CHECKS["missing-stop"][0], "observe")


class RareForms(unittest.TestCase):
    """Review after forty books: 15 printed misprints in 11 books (“hnndred”, “numher”, “entranee”), none marked;
    the collection itself serves as the dictionary."""

    def test_listed_against_corpus(self):
        import collections
        corpus = collections.Counter({"hundred": 50, "number": 45, "the": 900, "fell": 3})
        pages = [("p0001", "Five hnndred men and a large numher of boats."),
                 ("p0002", "[[cont]][[side: A note.]] numher fell; <i>hnndred</i> and [[corr numher|number]] and the hnn-")]
        items = preflight.check_rare_forms(pages, corpus)
        self.assertEqual([i.split(":")[0] for i in items], ["p0001", "p0001"])
        self.assertIn("“hnndred” — “hundred”", items[0])

    def test_common_or_far_words_not_listed(self):
        import collections
        corpus = collections.Counter({"hundred": 50, "hnndred": 5, "tea": 100})
        self.assertEqual(preflight.check_rare_forms([("p0001", "A hnndred cups; a zebra.")], corpus), [])
        self.assertEqual(preflight.CHECKS["rare-forms"][0], "observe")

    def test_dropped_or_transposed_letter_listed(self):
        """Review after fifty-five books: *Scouting for Stanley* printed “vegtables”, “Christain”, “themsleves”."""
        import collections
        corpus = collections.Counter({"vegetables": 60, "themselves": 80, "garden": 70, "gardn": 0})
        pages = [("p0010", "Fresh vegtables for themsleves; a fine garden."),
                 ("p0011", "Then Kiwanjo came, and the cat.")]
        items = preflight.check_rare_forms(pages, corpus)
        self.assertEqual([i.split(":")[0] for i in items], ["p0010", "p0010"])
        self.assertIn("“vegtables” — “vegetables”", items[0])
        self.assertIn("transposed", items[1])

    def test_edit_needs_a_rare_long_word(self):
        import collections
        corpus = collections.Counter({"vegetables": 60, "vegtables": 3, "cats": 100})
        self.assertEqual(preflight.check_rare_forms([("p0001", "Vegtables and cts here.")], corpus), [])


class Contents(unittest.TestCase):
    """Contents decided book by book (Tom, 2026-11-19): full summaries, entries inside a division, parts."""
    LONG = "The Start—" + "A Very Long Morning on the Road—" * 3 + "The Inn"

    def test_subtitles_all(self):
        pages = [f"# Chapter I.\n\n[[subtitle]] {self.LONG}\n\nText one.", "# Chapter II.\n\n[[subtitle]] The River\n\nText two."]
        book, w = comp(pages)
        self.assertEqual([d["title"] for d in book["divisions"]], ["Chapter I", "Chapter II. The River"])
        self.assertNotIn("toc_title", book["divisions"][0])
        book, w = comp(pages, toc={"subtitles": "all"})
        d1, d2 = book["divisions"]
        self.assertEqual(d1["title"], "Chapter I")                     # pager and page title stay short
        self.assertEqual(d1["toc_title"], "Chapter I. " + self.LONG)
        self.assertEqual(d2["title"], "Chapter II")                    # short summaries too: titles alike (2026-11-21)
        self.assertEqual(d2["toc_title"], "Chapter II. The River")
        self.assertEqual([n[0] for n in rh.toc_tree(book)], ["Chapter I. " + self.LONG, "Chapter II. The River"])

    def test_toc_title_in_divisions(self):
        book, _ = comp(["# Diary.\n\nText."], divisions=[{"at": "p0001", "kind": "chapter", "toc_title": "The Diary"}])
        self.assertEqual(book["divisions"][0]["title"], "Diary")
        self.assertEqual(rh.toc_tree(book)[0][0], "The Diary")

    def test_part_with_subtitle(self):
        book, _ = comp(["# Flying Leaves.\n\n[[subtitle]] From the East.", "# Leaf I.\n\nText.", "# Leaf II.\n\nMore."])
        self.assertEqual([d["kind"] for d in book["divisions"]], ["part", "chapter", "chapter"])
        tree = rh.toc_tree(book)
        self.assertEqual(len(tree), 1)
        self.assertEqual([k[0] for k in tree[0][3]], ["Leaf I", "Leaf II"])

    def test_entries(self):
        pages = ["# Diary.\n\n<i>Sunday</i>, June 12<i>th</i>.—Paris.\n\n13<i>th</i>.—Calais.",
                 "[[page 2]]\n\n1<i>st</i> July.—London.\n\nIn the evening, the theatre."]
        entries = [{"at": "p0001", "starts": "Sunday, June 12th", "title": "12–13 June: Paris and Calais"},
                   {"at": "p0002", "starts": "1st July", "title": "July: London"},
                   {"at": "p0002", "starts": "No such day", "title": "x"}]
        book, w = comp(pages, toc_entries=entries)
        d = book["divisions"][0]
        self.assertEqual(d["sections"], [{"title": "12–13 June: Paris and Calais", "block": 1, "editor": True},
                                         {"title": "July: London", "block": 3, "editor": True}])
        self.assertEqual(w, ["toc_entries: no block on p0002 starts with 'No such day'"])
        names = rh.file_names(book, ".xhtml")
        nav = rh.nav_list(book, names)
        self.assertIn('<li><a href="01.xhtml">Diary</a><ol><li><a href="01.xhtml#sec-1">12–13 June: Paris and Calais</a></li>', nav)
        html = rh.Ctx(book, "web", names).blocks(d)
        self.assertIn('<p id="sec-1" class="first">', html)
        self.assertIn('<p id="sec-2">', html)
        # the ODT's contents list links to bookmarks that exist
        odt = render_odt.render(book, None)
        content = zipfile.ZipFile(__import__("io").BytesIO(odt)).read("content.xml").decode()
        links = re.findall(r'xlink:href="#([^"]+)"', content)
        marks = set(re.findall(r'text:bookmark text:name="([^"]+)"', content))
        self.assertEqual(links, ["div-d001", "div-d001-sec-1", "div-d001-sec-2"])
        self.assertTrue(set(links) <= marks, (links, marks))

    def test_sample_with_entries_preflight_clean(self):
        tmp = tempfile.mkdtemp()
        try:
            d = os.path.join(tmp, "sample-journey-doe")
            shutil.copytree(SAMPLE, d)
            cfg = json.load(open(os.path.join(d, "book.json")))
            cfg["toc"] = {"subtitles": "all"}
            cfg["toc_entries"] = [{"at": "p0006", "starts": "The road is long", "title": "The carrier’s song"}]
            json.dump(cfg, open(os.path.join(d, "book.json"), "w"))
            verdict, report, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
            enforce = {k: v for k, v in res.items() if preflight.CHECKS[k][0] == "enforce" and v}
            self.assertEqual(enforce, {}, report)
            book, _ = compile_book.compile_book(d)
            self.assertEqual(sum(len(x.get("sections", [])) for x in book["divisions"]), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class HyphenJoins(unittest.TestCase):
    """Review 2026-11-19: the look list drops joins the book itself settles (the whole word printed elsewhere)
    and marks those whose hyphenated form it prints elsewhere."""

    def warn(self, leaf, a, b):
        return f"hyphen join at {leaf}: …{a}|{b}… (hyphen removed; check)"

    def test_triage(self):
        pages = [("p0001", "In the afternoon we took the stepping-stones and a snow-plough."),
                 ("p0002", "We walked in the after-"), ("p0003", "[[cont]]noon; then the stepping-"),
                 ("p0004", "[[cont]]stones, the snow-"), ("p0005", "[[cont]]fences and a rare dis-"),
                 ("p0006", "[[cont]]cussion of <i>ship-</i>"), ("p0007", "[[cont]]<i>wreck</i>.")]
        items = [self.warn("p0003", "lked in the after-", "noon; then the "),
                 self.warn("p0004", " then the stepping-", "stones, the sno"),
                 self.warn("p0005", "ones, the snow-", "fences and a ra"),
                 self.warn("p0006", " and a rare dis-", "cussion of <i>s"),
                 self.warn("p0007", "of <i>ship-</i>", "<i>wreck</i>.")]
        out = preflight.triage_hyphen_joins(items, pages)
        self.assertEqual(len(out), 5)
        self.assertIn("“stepping-stones” elsewhere", out[0])
        self.assertIn("other “snow-” words", out[1])
        self.assertEqual(out[2:4], items[3:5])                  # not settled by the book (italics too): as before
        self.assertEqual(out[4], "(and 1 joins giving a word the book prints whole elsewhere: not listed)")

    def test_unparsed_item_listed(self):
        it = "hyphen join around an image at p0009: …is responsi-|[[image: x]]… (hyphen removed; check)"
        self.assertEqual(preflight.triage_hyphen_joins([it], []), [it])


class ShortSubtitle(unittest.TestCase):
    """Review 2026-11-19: a short chapter title under the heading is centred (it looked like a stray indented
    paragraph); a long list of topics stays a left-aligned summary. HTML/EPUB class and ODT style."""

    def test_classes_and_styles(self):
        long_ = "Topic—" * 20 + "End."
        book, _ = comp(["# Chapter VIII\n\n[[subtitle]] A Hawaiian Journey\n\n[[subtitle]] " + long_ + "\n\nText."])
        d = book["divisions"][0]
        html = "".join(rh.Ctx(book, "web", {x["id"]: "d.html" for x in book["divisions"]}).blocks(d))
        self.assertIn('<p class="subtitle short">A Hawaiian Journey</p>', html)
        self.assertIn('<p class="subtitle">Topic', html)
        odt = zipfile.ZipFile(__import__("io").BytesIO(render_odt.render(book, None))).read("content.xml").decode()
        self.assertIn('text:style-name="Chapter_20_Title">A Hawaiian Journey', odt)
        self.assertIn('text:style-name="Chapter_20_Summary">Topic', odt)


class Carousel(unittest.TestCase):
    """The carousel of covers on the home page (Tom, 2026-11-21): the record and thumbnails (tools/carousel.py), the
    row of links in the page, and the styles and script that make a swipe or a click move one group of books."""

    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo, True)
        from PIL import Image
        for slug in ("book-01", "book-02", "book-03"):
            d = os.path.join(self.repo, "books", slug, "images")
            os.makedirs(d)
            open(os.path.join(self.repo, "books", slug, "book.json"), "w").write("{}")
            Image.new("RGB", (800, 1400), "#234").save(os.path.join(d, "cover.jpg"))

    def test_record_thumbnails_and_check(self):
        self.assertEqual(len(carousel.check(self.repo)), 3)                    # nothing decided yet
        w, h = carousel.add("book-01", "cover", repo=self.repo)
        self.assertTrue(w <= carousel.BOX[0] and h <= carousel.BOX[1] and h == carousel.BOX[1])
        carousel.add("book-02", "title", "the cover has no title", repo=self.repo)
        carousel.add("book-03", "page", repo=self.repo)        # no readable title anywhere: a page of the text (Tom, 2026-11-21)
        d = carousel.load(self.repo)["books"]
        cover = os.path.join(self.repo, "books", "book-01", "images", "cover.jpg")
        self.assertEqual(d["book-01"], {"image": "cover", "width": w, "height": h, "sha256": carousel.sha(cover)})
        self.assertEqual((d["book-02"]["image"], d["book-02"]["note"], d["book-03"]["image"]), ("title page", "the cover has no title", "page of the text"))
        self.assertEqual(carousel.check(self.repo), [])
        self.assertEqual(sorted(os.listdir(os.path.join(self.repo, "site", "carousel"))), ["book-01.jpg", "book-02.jpg", "book-03.jpg"])
        # the book's picture replaced (the thumbnail must be the same picture as on the book's page), a thumbnail
        # lost, a book unpublished: each reported
        from PIL import Image
        Image.new("RGB", (700, 1100), "#eee").save(cover)
        os.remove(os.path.join(self.repo, "site", "carousel", "book-02.jpg"))
        shutil.rmtree(os.path.join(self.repo, "books", "book-03"))
        self.assertEqual(carousel.check(self.repo), [
            "in the record but not a published book: book-03",
            "thumbnail missing: site/carousel/book-02.jpg",
            "the picture has changed since the thumbnail was made: books/book-01/images/cover.jpg (look at it; carousel.py add)"])
        carousel.add("book-01", "title", repo=self.repo)
        self.assertEqual(len(carousel.check(self.repo)), 2)
        with self.assertRaises(SystemExit):
            carousel.add("book-09", "cover", repo=self.repo)

    def test_the_picture_on_the_book_page_is_named_for_what_it_is(self):
        d = os.path.join(self.repo, "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        book, _ = compile_book.compile_book(d)
        names = rh.file_names(book, ".html")
        for kind, alt in ((None, "Cover of the book"), ("cover", "Cover of the book"), ("title page", "Title page of the book"),
                          ("page of the text", "A page of the book")):
            self.assertIn(f'<img class="cover" src="images/cover.jpg" alt="{alt}"/>', build_site.book_page(book, names, True, kind))

    def test_home_page_has_the_row_above_the_title_outside_main(self):
        books = [shelf_book(2, title='A "Quoted" Journey'), shelf_book(1), shelf_book(3), shelf_book(4)]
        record = {f"book-{i:02d}": {"image": "cover", "width": 300, "height": 450} for i in (1, 2, 3)}     # 4: not in the record
        html_ = build_site.carousel_html(books, record, {"book-01.jpg", "book-02.jpg"})                    # 3: no thumbnail
        self.assertEqual(re.findall(r'<li><a href="books/(book-\d\d)/index.html">', html_), ["book-01", "book-02"])
        self.assertIn('<img src="carousel/book-01.jpg" alt="Journey 1, by Author 1" width="300" height="450" loading="lazy"', html_)
        self.assertIn('alt="A &quot;Quoted&quot; Journey, by Author 2"', html_)
        self.assertEqual(re.sub(r"<[^>]+>|\s", "", html_), "")              # no visible text: the titles are alt text only
        self.assertEqual(build_site.carousel_html(books, {}, set()), "")
        build_site.build_index(self.repo, html_)
        home = open(os.path.join(self.repo, "index.html"), encoding="utf-8").read()
        self.assertLess(home.index("</header>"), home.index('<nav class="carousel" aria-label="Some of the books">'))
        self.assertLess(home.index('<nav class="carousel"'), home.index('<main id="main">'))
        self.assertLess(home.index("</ul></nav>"), home.index('<h1 class="visually-hidden">Travel Books</h1>'))
        build_site.build_index(self.repo)
        self.assertNotIn("carousel", open(os.path.join(self.repo, "index.html"), encoding="utf-8").read())

    def test_every_recorded_book_is_published_and_has_its_thumbnail(self):
        """The repository itself: nothing in the record without a book and a thumbnail of the recorded size, no
        stray thumbnails. (A published book not yet decided is not an error: the review session decides it.)"""
        self.assertEqual([x for x in carousel.check() if not x.startswith("not decided")], [])
        from PIL import Image
        for slug, r in carousel.load()["books"].items():
            im = Image.open(os.path.join(REPO, "site", "carousel", slug + ".jpg"))
            self.assertEqual(im.size, (r["width"], r["height"]), slug)
            self.assertTrue(im.size[0] <= carousel.BOX[0] and im.size[1] <= carousel.BOX[1], slug)

    def test_styles_and_script(self):
        css = open(os.path.join(REPO, "site", "assets", "site.css"), encoding="utf-8").read()
        js = open(os.path.join(REPO, "site", "assets", "site.js"), encoding="utf-8").read()
        # a control's tip goes above it when there is no room below inside the panel (the panel in the bar scrolls,
        # and Safari and Firefox cut off a tip past its foot: the reset button, Tom 2026-11-23)
        tipfn = js[js.index("function showTip("):js.index("panel.addEventListener('mouseover'")]
        self.assertIn("r.top - p.top + panel.scrollTop - tip.offsetHeight - 4", tipfn)
        self.assertIn("> p.bottom", tipfn)
        # three, four or five in view, and a stop at the first book of each group, so that a swipe moves one group
        self.assertEqual(re.findall(r"\.carousel \{ --n: (\d); \}", css), ["4", "5"])
        self.assertIn(".carousel { --n: 3;", css)
        for n in (3, 4, 5):
            self.assertIn(f".carousel li:nth-child({n}n+1) {{ scroll-snap-align: start; scroll-snap-stop: always; }}", css)
        self.assertIn("scroll-snap-type: x mandatory", css)
        rules = css[css.index("/* The carousel of covers"):css.index("@media print")]
        self.assertNotIn("border:", rules.replace("border: 0", ""))            # no borders (Tom)
        self.assertIn("box-shadow", rules)
        self.assertIn(".carousel { display: none; }", css[css.index("@media print"):])
        # a new order on every load; the arrows have names for screen readers; slow-fast-slow, and no motion if not wanted
        fn = js[js.index("function carousel()"):]
        for piece in ("Math.random()", "'aria-label': 'More books'", "'aria-label': 'Earlier books in the row'",
                      "prefers-reduced-motion", "p < 0.5 ? 4 * p * p * p"):
            self.assertIn(piece, fn)
        # the row has no end: whole groups go from one end of the list to the other (no book twice in the page),
        # but not under a reader who is going through the links with the Tab key
        for piece in ("list.insertBefore(list.lastElementChild, list.firstElementChild)", "list.appendChild(list.firstElementChild)",
                      "* n;", "f.matches(':focus-visible')) return;"):
            self.assertIn(piece, fn)
        self.assertNotIn("cloneNode", fn)
        self.assertNotIn("disabled", fn)
        # arrows only where there is a mouse (Tom: on phones and tablets readers swipe); their disks let the page show through
        self.assertRegex(rules, r"\.carousel button \{[^}]*display: none;")
        self.assertIn("@media (hover: hover) and (pointer: fine) { .carousel button { display: block; } }", rules)
        self.assertIn("color-mix(in srgb, var(--bg) 62%, transparent)", rules)


class TitlePageFirst(unittest.TestCase):
    """Tom, 2026-11-22: the title page is transcribed in the reading editions, as their first page; what stands
    before it stays out; the picture on the book's page leads to the first chapter. Invented text."""
    PAGES = ["[[page ?]]\n[[center]] A JOURNEY\n\n[[image: portrait]]\n[[caption]] The Author.",
             "[[page ?]]\n[[center]] A JOURNEY\n\nBY A. TRAVELLER\n\n[[right]] <i>Motto</i>\n\n[[center]] LONDON: 1861",
             "[[page ?]]\n[[center]] PRINTED BY B. AND CO.",
             "[[page v]]\n# Preface.\n\nA word.",
             "[[page 1]]\n# Chapter I.\n\nWe set out.\n\n[[image: a cart]]\n\nThe cart was slow.\n\n[[image: a ford]]\n\n[[cont]] and we walked."]
    DIVS = [{"at": "p0001", "kind": "front", "reading": True}, {"at": "p0002", "kind": "titlepage"}, {"at": "p0004", "kind": "preface"}]

    def setUp(self):
        self.book, self.w = comp(self.PAGES, divisions=self.DIVS, frontispiece="p0001-1")

    def test_title_page_opens_the_editions_and_the_half_title_stays_out(self):
        rd = rh.reading_divisions(self.book)
        self.assertEqual([(d["kind"], d["title"]) for d in rd], [("titlepage", "Title Page"), ("preface", "Preface"), ("chapter", "Chapter I")])
        self.assertTrue(any("before the title page" in x for x in self.w))
        self.assertFalse(self.book["divisions"][0]["reading"])

    def test_frontispiece_follows_the_title_page_and_precedes_its_verso(self):
        tp = rh.reading_divisions(self.book)[0]
        self.assertEqual([(b["leaf"], b["type"]) for b in tp["blocks"]][-2:], [("p0001", "image"), ("p0003", "paragraph")])

    def test_lines_are_centred_and_the_verso_set_apart(self):
        names = rh.file_names(self.book, ".html")
        html_ = rh.Ctx(self.book, "web", names).blocks(rh.reading_divisions(self.book)[0])
        self.assertTrue(html_.startswith('<div class="titlepage">'))
        self.assertIn('<p class="right">', html_)
        self.assertEqual(html_.count('<div class="tp-verso"></div>'), 1)
        x = zipfile.ZipFile(__import__("io").BytesIO(render_odt.render(self.book, None))).read("content.xml").decode()
        self.assertIn('<text:p text:style-name="Centered">BY A. TRAVELLER</text:p>', x)     # unmarked line: centred
        self.assertLess(x.index("PRINTED BY B. AND CO."), x.index("Travel Books edition"))  # then the note, the contents
        self.assertNotIn('text:style-name="Title"', x)                                      # no title page made from the metadata
        z = zipfile.ZipFile(__import__("io").BytesIO(render_epub.render(self.book, "")))
        opf = z.read("OEBPS/content.opf").decode()
        self.assertLess(opf.index('<itemref idref="c01"/>'), opf.index('<itemref idref="title"/>'))
        self.assertIn('epub:type="titlepage"', z.read("OEBPS/text/01.xhtml").decode())

    def test_body_start_is_the_first_chapter(self):
        self.assertEqual(rh.body_start(self.book)["title"], "Chapter I")
        b2, _ = comp(self.PAGES, divisions=self.DIVS[1:2])                  # "# Preface." left as a chapter: named in book.json
        self.assertEqual(rh.body_start(b2)["title"], "Preface")
        b3, _ = comp(self.PAGES, divisions=self.DIVS[1:2], body_start="p0005")
        self.assertEqual(rh.body_start(b3)["title"], "Chapter I")

    def test_paragraph_after_a_picture_is_indented(self):
        """*Zephyrus*: "In the Banda Oriental…" stood flush left after a picture; the scan indents it."""
        ch = rh.reading_divisions(self.book)[-1]
        html_ = rh.Ctx(self.book, "web", rh.file_names(self.book, ".html")).blocks(ch)
        self.assertIn('<p class="first">We set out.</p>', html_)
        self.assertIn("<p>The cart was slow. and we walked.</p>", html_)
        x = zipfile.ZipFile(__import__("io").BytesIO(render_odt.render(self.book, None))).read("content.xml").decode()
        self.assertIn('<text:p text:style-name="Text_20_body">The cart was slow.', x)

    def test_preflight_lists_a_book_without_its_title_page(self):
        self.assertEqual(preflight.check_title_page(self.book), [])
        b2, _ = comp(self.PAGES[3:])
        self.assertEqual(len(preflight.check_title_page(b2)), 1)
        self.assertEqual(preflight.CHECKS["title-page"][0], "observe")


class SplitSections(unittest.TestCase):
    """Tom, 2026-11-22: a body text without chapters (the *Rajah of Kolhapoor* diary) is read in sections, each a
    page with a title; the JSON keeps the division whole. Invented text."""
    PAGES = ["[[page 1]]\n# Diary.\n\n1st.—Left home.[[fnref *]]\n\n2nd.—Rain.\n\n[[fn *]] By coach.",
             "[[page 2]]\n3rd.—At sea.[[fnref *]]\n\n4th.—Landed.\n\n[[fn *]] A steamer.",
             "[[page 3]]\n5th.—In town.\n\n# Appendix.\n\nPapers."]
    TOC = [{"at": "p0001", "starts": "1st.", "title": "1–2 May: the road"}, {"at": "p0002", "starts": "3rd.", "title": "3–4 May: the sea"},
           {"at": "p0003", "starts": "5th.", "title": "5 May: the town"}]

    def test_short_division_is_not_split_and_a_long_one_is(self):
        book, w = comp(self.PAGES, toc_entries=self.TOC)
        self.assertNotIn("split", book["divisions"][0])
        self.assertEqual(len(rh.reading_divisions(book)), 2)
        long_ = [self.PAGES[0], self.PAGES[1], self.PAGES[2].replace("# Appendix", "\n\n".join(["Words and more words. " * 80] * 40) + "\n\n# Appendix")]
        book, w = comp(long_, toc_entries=self.TOC)
        self.assertTrue(book["divisions"][0]["split"])
        book, w = comp(long_, toc_entries=self.TOC, divisions=[{"at": "p0001", "split": False}])
        self.assertNotIn("split", book["divisions"][0])

    def test_sections_become_pages_with_their_notes_and_titles(self):
        book, w = comp(self.PAGES, toc_entries=self.TOC, divisions=[{"at": "p0001", "split": True}])
        self.assertEqual(w, [])
        self.assertEqual(len(book["divisions"][0]["blocks"]), 6)               # the JSON: one division, whole
        rd = rh.reading_divisions(book)
        self.assertEqual([(d["id"], d["title"], d.get("added")) for d in rd],
                         [("d001", "1–2 May: the road", None), ("d001-2", "3–4 May: the sea", "3–4 May: the sea"),
                          ("d001-3", "5 May: the town", "5 May: the town"), ("d002", "Appendix", None)])
        self.assertEqual([[n["text"] for n in d["notes"]] for d in rd[:3]], [["By coach."], ["A steamer."], []])
        names = rh.file_names(book, ".html")
        self.assertEqual(rh.toc_tree(book)[0], ("Diary", "d001", None, [("1–2 May: the road", "d001", None, []),
                         ("3–4 May: the sea", "d001-2", None, []), ("5 May: the town", "d001-3", None, [])]))
        ctx = rh.Ctx(book, "web", names)
        self.assertIn('<p class="first">1st.', ctx.blocks(rd[0]))
        second = ctx.blocks(rd[1])
        self.assertTrue(second.startswith("<p><"), second[:40])         # runs on: indented, with its page number
        self.assertNotIn("3–4 May", second)                                     # the added title is not in the book's text
        self.assertIn('href="#d001-n2"', second)
        x = zipfile.ZipFile(__import__("io").BytesIO(render_odt.render(book, None))).read("content.xml").decode()
        self.assertIn('<text:h text:style-name="Added_20_Heading" text:outline-level="2"><text:bookmark text:name="div-d001-2"/>3–4 May: the sea</text:h>', x)
        z = zipfile.ZipFile(__import__("io").BytesIO(render_epub.render(book, None)))
        self.assertIn('<h2 class="added">3–4 May: the sea</h2>\n<section epub:type="chapter">', z.read("OEBPS/text/02.xhtml").decode())

    def test_text_before_the_first_section_is_a_page_under_the_division_title(self):
        toc = self.TOC[1:]
        book, _ = comp(self.PAGES, toc_entries=toc, divisions=[{"at": "p0001", "split": True}])
        self.assertEqual([d["title"] for d in rh.reading_divisions(book)], ["Diary", "3–4 May: the sea", "5 May: the town", "Appendix"])


class EditorImages(unittest.TestCase):
    """Tom, 2026-11-22 (*Surface Japan*): a typical printed page, with the border the text leaves out, shown as the
    editor's picture before the narrative, with a caption written for this edition. Not the book's: kept out of the
    divisions in the JSON and out of the book's text in every edition. Invented text."""
    PAGES = ["[[page i]]\n# Preface.\n\nA word.", "[[page 1]]\n# Chapter I.\n\nThe start.", "[[page 2]]\n# Chapter II.\n\nMore."]
    ED = [{"file": "editor-p0002", "leaf": "p0002", "alt": "Page 1 as printed", "caption": "Page 1 as printed, with its \"border\"."}]

    def test_json_keeps_them_apart(self):
        book, w = comp(self.PAGES, editor_images=self.ED)
        self.assertEqual(w, [])
        self.assertEqual(book["editor_images"], [{"src": "images/editor-p0002.jpg", "leaf": "p0002", "alt": "Page 1 as printed",
                                                  "caption": "Page 1 as printed, with its “border”.", "editor": True}])
        self.assertNotIn("Page 1 as printed", json.dumps(book["divisions"], ensure_ascii=False))
        _, w = compile_book.compile_pages(dict(CFG, editor_images=self.ED), [(f"p{i:04d}", t) for i, t in enumerate(self.PAGES, 1)], {})
        self.assertTrue(any("editor_images" in x for x in w))
        self.assertNotIn("editor_images", comp(self.PAGES)[0])

    def test_shown_before_the_narrative_outside_the_text(self):
        book, _ = comp(self.PAGES, editor_images=self.ED, divisions=[{"at": "p0001", "kind": "preface"}])
        rd = rh.reading_divisions(book)
        self.assertEqual([bool(rh.editor_figures(book, d)) for d in rd], [False, True, False])
        x = zipfile.ZipFile(__import__("io").BytesIO(render_epub.render(book, None))).read("OEBPS/text/02.xhtml").decode()
        self.assertIn('<figure class="editor"><img src="../images/editor-p0002.jpg" alt="Page 1 as printed"/>'
                      '<figcaption>Page 1 as printed, with its “border”.</figcaption></figure>\n<section epub:type="chapter">', x)
        odt = render_odt.render(book, None)
        c = zipfile.ZipFile(__import__("io").BytesIO(odt)).read("content.xml").decode()
        self.assertIn('<text:p text:style-name="Editor_20_Figure">', c)
        self.assertLess(c.index("Page 1 as printed, with"), c.index("The start."))
        main, _ = preflight.odt_streams(__import__("io").BytesIO(odt))
        self.assertNotIn("border", main)                     # the caption is not counted as the book's text
        self.assertIn("The start.", main)


class SecondStream(unittest.TestCase):
    """Reeves, *Brown Men and Women*: documents printed in small type along the foot of many pages, under the main
    text and apart from it (not footnotes). `[[stream]]` lines become a division of their own after the others; the
    main text joins over the pages as if they were not there. Invented text."""
    PAGES = ["[[page 1]]\n# Chapter I.\n\nThe story begins and\n\n[[stream]] # Papers.\n\n[[stream]] (1) A first paper, which goes",
             "[[page 2]]\n[[cont]]goes on here.\n\nAn end.\n\n[[stream]] [[cont]]on over the page.\n\n[[stream]] (2) A second.",
             "[[page 3]]\n# Chapter II.\n\nMore."]

    def test_stream_is_a_division_after_the_others(self):
        book, w = comp(self.PAGES)
        self.assertEqual(w, [])
        self.assertEqual([(d["id"], d["title"], d["kind"], d.get("stream")) for d in book["divisions"]],
                         [("d001", "Chapter I", "chapter", None), ("d002", "Chapter II", "chapter", None), ("d003", "Papers", "appendix", True)])
        t = [inline.plain(b["text"]) for b in book["divisions"][0]["blocks"] if b["type"] == "paragraph"]
        self.assertEqual(t, ["The story begins and goes on here.", "An end."])
        st = book["divisions"][2]["blocks"]
        self.assertEqual(inline.plain(st[1]["text"]), "(1) A first paper, which goes on over the page.")
        self.assertIn('leaf="p0002"', st[1]["text"])                  # its page break, linked to the scan
        self.assertEqual([p["division"] for p in book["pages"]], ["d001", "d001", "d002"])

    def test_preflight_compares_the_stream_apart(self):
        pages = [(f"p{i:04d}", t) for i, t in enumerate(self.PAGES, 1)]
        book, _ = comp(self.PAGES)
        ps, js = [], []
        pm, _ = preflight.page_streams(pages, streams=ps)
        jm, _ = preflight.json_streams(book, streams=js)
        self.assertEqual(preflight.compare(pm, jm, "t"), [])
        self.assertEqual(preflight.compare(" ".join(ps), " ".join(js), "t"), [])
        self.assertIn("A second.", " ".join(js))
        self.assertEqual(preflight.check_markup(pages), [])
        self.assertTrue(preflight.check_markup([("p0001", "[[page 1]]\nSome text # Heading inside a line")]))
        bad = [(l, t.replace("(2) A second.", "(2) A secnd.")) for l, t in pages]
        ps = []
        preflight.page_streams(bad, streams=ps)
        self.assertNotEqual(preflight.compare(" ".join(ps), " ".join(js), "t"), [])


class SerialCommas(unittest.TestCase):
    """Tom, 2026-11-22: text written for the site has serial commas and curly quotation marks."""

    def test_candidates_listed(self):
        cfg = {"summary": "He saw Java, Singapore and Hong Kong. In 1870, he left.", "notes_on_text": ["Tea, silk, and rice."],
               "toc_entries": [{"at": "p1", "title": "London, Paris and Rome"}, {"at": "p2", "title": "A, B and C", "editor": False}]}
        items = preflight.check_serial_commas(cfg)
        self.assertEqual(len(items), 2)
        self.assertEqual(preflight.CHECKS["serial-commas"][0], "observe")

    def test_markdown_pages_curl_quotes_but_not_code(self):
        d = tempfile.mkdtemp()
        src = os.path.join(d, "x.md")
        open(src, "w", encoding="utf-8").write("# T\n\nThe book's \"title\" and `{\"a\": 'b'}`.\n\n```\n\"k\": 'v'\n```\n")
        build_site.md_page(d, "x.html", "T", src)
        h = open(os.path.join(d, "x.html"), encoding="utf-8").read()
        self.assertIn("The book’s “title” and <code>{\"a\": 'b'}</code>.", h)
        self.assertIn("<pre><code>\"k\": 'v'</code></pre>", h)
        shutil.rmtree(d)

    def test_home_page_counts_the_books_and_has_no_visible_title(self):
        d = tempfile.mkdtemp()
        build_site.build_index(d, "", 54)
        h = open(os.path.join(d, "index.html"), encoding="utf-8").read()
        self.assertIn("downloaded as EPUB, ODT, or JSON. The site now contains 54 books, with more being added every day.</p>", h)
        self.assertIn('<p><a href="about.html">More about the project.</a></p>', h)
        self.assertLess(h.index("than about other countries.</p>"), h.index("More about the project."))
        self.assertNotIn("<h1>", h)
        shutil.rmtree(d)
