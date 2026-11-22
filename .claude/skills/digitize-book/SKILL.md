---
name: digitize-book
description: Transcribe a pre-1914 English travel book from its Internet Archive scan and publish it on the travel-books site (HTML, EPUB, ODT, JSON). Use when starting, resuming or revising a book in wip/ or books/.
---

# Digitize a book

Follow `notes/workflow.md` stage by stage (commands are there); this skill is the order of thought and the
places where books actually go wrong. Rules: `CLAUDE.md`. Text decisions: `notes/style.md`.

## Before spending anything

1. The book's queue row is eligible today (`notes/selection.md` §"Before starting"). Set it `in progress` with
   `"started": "<date>"`. A JATSI row (`"from": "jatsi"`): `"collection": "jatsi"` in `book.json`, and read
   `notes/jatsi.md` §"What these books bring" (romanized Japanese, Japanese script, a better scan than the one listed).
2. Fetch once from IA, make page images, **look at every contact sheet** and a dozen pages at full size. A
   missing, cut-off or blurred page, or an unopened folding plate, stops the book here (try another scan).
3. Write the page map in `wip/<slug>/log.md`; cache the page images in Drive; extract full-size leaves for the
   plates and the book's picture (`images/cover.jpg`: the cover if the title is clearly readable on it, otherwise
   the title page — `notes/workflow.md` §5); commit.
4. Read `notes/lessons.md` "Always" and the triggers this book has. If the book has something in
   `notes/workflow.md` §"Not yet solved", either add the support first (tool + test + markup doc) or choose
   another book.

## Transcribe

Opus draft → `normalize.py` → Sonnet corrections → `normalize.py` → `review.py` → `judge.py` → scan checks.
Never Fable. Commit after each run. While runs go, do the page map, crops and metadata.
Draft pages refused by the output filter: `tools/ocr_fallback.py` straight after the draft run; never retry
them and never type them yourself (it ends the session). Name them in the log and audit them.

## Where these books go wrong (check each)

- **Proper names and foreign words**: models write the familiar form. Any judge spot or audit candidate on a
  name gets a crop.
- **Italics**: transcribe them as printed, always. The renderers turn long italic passages roman in the built versions (`notes/style.md` §Editions); never remove italics from page files for that reason.
- **Old spellings** (`shew`, `chuse`, `to-day`, `connexion`, `Hindoo`): must survive; a change towards the
  modern form is suspect.
- **Page joins**: every `[[cont]]`; hyphen joins (`keep_hyphens` for real compounds; preflight already
  leaves out the joins the book settles by printing the whole word elsewhere, and marks "keep_hyphens?" where it
  prints the hyphenated form).
- **Headings**: in upper and lower case (preflight `heading-caps`); one `#` per division, as the printed contents has them; chapter summaries `[[subtitle]]`;
  no running heads; parts before chapters.
- **Contents** (decided book by book, Tom 2026-11-19): follow the printed contents, deviate where a digital reader
  benefits; entries alike within the book, neither too many nor too few (`toc`, `toc_entries`: `notes/workflow.md`
  stage 4 "Contents"). Print the compiled entries and read them before the build; record the decision in the log.
- **Front and back matter**: `divisions` in `book.json`; what is left out of the reading editions and said so. The **title page** (kind `titlepage`, with its verso) is the first page of the editions: read it against the scan, every line `[[center]]` with capitals as printed; what stands before it is left out. Every `#` heading before the first chapter gets its kind (preface, introduction), because the picture on the book's page links to the first `chapter`.
- **A long text without chapters** (diary, letters): `toc_entries` of the editor's, chosen as pages (5–15 printed pages each, a title saying what it covers); the compiler splits the division at them (`notes/workflow.md` stage 4).
- **Notes**: marks pair; continued notes; notes on plates.
- **Verse, letters, inscriptions, tables, front matter, footnote pages**: spot-read against the scan (Opus subagent).
- **Illustrations**: every `[[image:]]` has a crop that was looked at; every preflight `caption-tail` item settled (a cross-reference goes into the caption line); captions; alt text says what is shown. A frontispiece in the front matter: set `frontispiece` in book.json.
- **Printer's errors**: few, certain, each `[[corr printed|corrected]]`. A turned or wrong letter is printed faithfully by every stage and never marked unless looked for: crop every item of preflight `misprints` and `rare-forms`.

## Metadata and summary

From the title page. Summary: 60–150 plain words (`notes/style.md` §Site text) — who, when, where, how, what
is in it, what a reader should know. No praise. Serial commas (“A, B, and C”) and curly quotation marks in everything written for the site (preflight `serial-commas` lists candidates: read them).

## Verify and publish

`preflight.py` PASS → browser look at the built pages → `audit_sample.py`, every candidate on a crop, record
in `book.json` → `publish.py` → log, metrics → tests, commit, PR, merge → open the live page.
A preflight item that is the check's mistake, not the book's: `notes/workflow.md` §"When a check is wrong"
(waive one item; for a kind of book, leave the book ready, fix the check with a test, and the next session
publishes). Three failed attempts at a cause in the book: the book waits.

## New version of a published book

Edit `books/<slug>/pages/`; bump `version`, `date`, `history`; preflight; audit record; `publish.py`; errata
follow-through (`notes/errata.md`).
