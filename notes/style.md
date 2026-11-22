# Style: the text, the editions, the site

Changes to this file change every future book and may make earlier ones look different; note the date of each
change at the foot, and see `workflow.md` §"New version" for when earlier books are redone.

## The text (Tom, 2026-11-19)

- **Faithful.** The author's words, spelling, capitals and punctuation marks exactly as printed, including old,
  inconsistent and foreign spellings and place-names.
- **Spacing is modern.** No space before `; : ! ?`, none inside quotation marks, contractions closed up
  (`do n't` → `don't`), dashes closed up. `tools/normalize.py` does this after every model step.
- **Printer's errors.** Only the unmistakable are corrected: transposed or doubled letters, a repeated word at
  a line end, a dropped letter in a common word, wrong fount, a missing full stop at the end of a paragraph, a
  quotation mark plainly missing or doubled. Each as `[[corr printed|corrected]]`. Not corrected: anything
  that could be the author's spelling or usage, proper names, dates and figures (even if wrong), grammar,
  inconsistency between two acceptable forms. In doubt, leave it. An errata slip printed in the book is
  applied the same way, with a line in `notes_on_text`.
- Line-end hyphens are resolved (the compound keeps its hyphen if the book hyphenates it elsewhere, or if it is
  one of `to-day`, `to-morrow`, `to-night` and the like in a book of that period; otherwise joined).
- Quotation marks curly, as printed (single or double as the book has them). A quotation opened and never
  closed in print is left so unless it is plainly a slip (then `[[corr]]`).
- **Quotation marks across lines and paragraphs follow modern practice** (Tom, 2026-11-20):
  - an opening mark repeated at the start of every printed line of a quotation (common before about 1800) is left
    out; the quotation keeps its own opening and closing marks (`tools/running_quotes.py`, which lists each one;
    the list is kept in the book's directory);
  - a quotation of several paragraphs marked by quotation marks (not set off by indenting or a smaller type) has an
    opening mark at the start of each paragraph and a closing mark only at the end of the whole quotation: a
    closing mark the print puts at the end of an inner paragraph is left out, and a missing opening mark at the start
    of an inner paragraph is supplied. These are changes of convention, not corrections: no `[[corr]]`; say in
    `notes_on_text` that the book's quotation marks follow modern practice.
- **Text lost in the scan** (Tom, 2026-11-20): letters lost at a fold, tear or blot, not settled by another scan or
  edition. Inferred reasonably well from the context → `[[supplied …]]`: the JSON marks them as supplied, the
  editions show them plainly (smooth reading). Not inferable → `[[gap]]`: `[…]` in the JSON and the editions. Only
  for short losses (about a word); a longer loss is a scan problem (`workflow.md` §1.4).
- Long s → s; ligatures fi, fl as letters; æ, œ kept. Greek and other scripts in the script. Illegible → `〓`
  (never published: resolve from another scan, or note it in `notes_on_text` and waive).
- Italics and small capitals as printed.
- **Headings and titles in upper and lower case** (Tom, 2026-11-19): a heading, chapter title or summary, or
  caption printed in capitals is typed with capitals only where ordinary title case has them (`# Chapter IV.`,
  `# Preface.`, `[[subtitle]] From Cairo to the First Cataract`; roman numerals stay in capitals; small words
  such as a, an, the, and, of, in, to, from, with stay lower case except first). The wording, spelling and
  punctuation are not changed. Book titles in `book.json` likewise. Captions are my extension of his
  instruction ("titles"): assumed. Text printed in capitals inside a paragraph stays as printed.
- Footnotes keep the book's marks. Illustrations are placed where the book has them (a plate facing a page:
  after the paragraph in which the facing page ends), with their printed captions.

## What goes where

| Part | JSON | HTML / EPUB / ODT |
|---|---|---|
| Cover, half-title, anything else before the title page | yes (kind `front`) | no |
| Title page and its verso (kind `titlepage`) | yes | yes: the first page of the editions (Tom, 2026-11-22), every line centred unless marked `[[right]]`; the frontispiece follows the title page's first leaf; then, in the EPUB and ODT, a note on this edition and the contents |
| Dedication, preface, introduction, chapters, appendices, author's notes, glossary | yes | yes |
| Printed contents, list of illustrations | yes | no (a generated contents replaces them, decided book by book: `workflow.md` stage 4 "Contents") |
| Index | yes, page numbers tagged `<pref>` | no |
| Errata slip | yes | no (applied) |
| Publisher's advertisements, library book-plates and stamps | advertisements yes; library marks no | no |

Say what was left out in `book.json` `omitted_from_reading`. A long appendix of tables or documents may be
left out of the reading editions if it is not narrative; say so.

## Editions

- All books share `site/assets/book.css` (web and EPUB) and the named styles of `tools/render_odt.py`. A book
  gets `css_extra` only when its text needs a style the others do not have; if two books need it, it moves
  into the shared file.
- **Long italic passages are set in roman in the HTML, EPUB and ODT; the JSON keeps the italics as printed**
  (Tom, 2026-11-19: "long extended passages, such as entire paragraphs or in tables of contents"). The rule
  is applied by the renderers (`render_html.roman_long_italics`), never in the page files: a wholly italic
  paragraph, quotation or note of 30 words or more; a wholly italic piece of verse of four lines or more; a
  chapter summary; a table set all in italic. "Wholly" = at least 90% of its letters; the few words the print
  set in roman inside such a passage, for contrast, become italic. Shorter italics stay. The thresholds are
  mine: change them in one place if books show they are wrong.
- **A long text that the book does not divide** (a diary, a run of letters, one long chapter) is read in sections, each
  a page of its own with a title of the editor's (Tom, 2026-11-22): the `toc_entries` of the division, which the compiler
  marks `"split": true` when it is long (`book-json.md`). The title is shown as a heading that is not the book's (italic,
  outside the text); the JSON keeps the division whole.
- **Paragraph indents follow the scan** (Tom, 2026-11-22): a paragraph after a picture is indented like any other; the
  first paragraph after a heading, a break, a quotation, verse or a table is not.
- Web: one page per division (or section of a split division); page numbers of the printed book hidden until the reader asks, each linking to
  that page of the scan at IA.
- EPUB: EPUB 3, epubcheck-clean, page list, pop-up footnotes. ODT: real footnotes, bookmarks at page starts.

## Site text

Plain and minimal. Say what the thing is; a reader should learn the facts and decide for themselves.

- **Summary of a book** (`book.json` `summary`, 60–150 words): who the author was (a clause), when and where
  they went and how, what the book contains, anything a reader should know before starting (dialect,
  attitudes of the time stated factually, missing maps). No adjectives of praise ("fascinating", "vivid",
  "remarkable", "delightful"), no "takes the reader", no rhetorical questions, no claims about importance
  unless a fact supports them (e.g. "the first account in English by an Indian visitor" only if established).
- Titles in the lists: short title, author, year. Regions as plain modern names, with the period name in
  `notes_on_text` if it helps.
- No exclamation marks, no second person, no calls to action beyond the link itself.
- **Serial commas, and curly apostrophes and quotation marks** (Tom, 2026-11-22), in everything written for the site:
  summaries, notes on the text, contents entries of the editor's, history notes, the About page, the text in
  `build_site.py`. “Java, Singapore, and Hong Kong”; not in words quoted from a book or titles taken from print, and not
  in code excerpts (the JSON format page). Preflight: `site-text` (straight quotes, enforced), `serial-commas` (observe:
  read each item; pairs after a comma are not lists). The Markdown pages are curled by the builder outside `code`.

## Changes

- 2026-11-19: first version.
- 2026-11-19: headings, chapter titles and captions in upper and lower case, not as printed in capitals (no book yet published, none to redo).
- 2026-11-19: long italic passages roman in the built versions, italic in the JSON.
- 2026-11-20: text lost in the scan: `[[supplied …]]` and `[[gap]]` (Tom).
- 2026-11-22: the title page opens the editions; long undivided texts in sections; indents after pictures; serial commas (Tom). Applied to all 54 books by the tools; no book version changed.
