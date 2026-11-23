# South by West; or, Winter in the Rocky Mountains and Spring in Mexico — Rose Georgina Kingsley; ed. Charles Kingsley (1874)

IA: southbywestorwin00king (University of California Libraries; 454 leaves, 400 ppi, greyscale). Other scans
looked at: none (this one is clean and complete).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv; Rose Kingsley's
*Children of Westminster Abbey* and *Roses and Rose Growing* are there, not this); The Online Books Page lists
only page images (a German library); a web search finds only print-on-demand reprints (Kessinger 2007/2010,
Creative Media Partners 2023, others). An ISBN with the Rio Grande Press prefix that came up in the same search
is Schwatka's *In the Land of Cave and Cliff Dwellers* (Open Library), not this book. Rose Georgina Kingsley
1845–1925; Charles Kingsley (editor, preface) 1819–1875. Engravers not named.

## Status
**Published, version 1** (2026-11-19, routine session). Nothing pending.

## Page map
p0000 colour card (hidden) · p0001 front cover (cloth, agave design stamped) · p0002 front pastedown, UC bookplate ·
p0003–p0004 endpapers · p0005 IA card · p0006 frontispiece "Monument Park" · p0007–p0008 tissue guard (hidden) ·
p0009 title page · p0010 verso (printer) · p0011 dedication "To my Father and Mother" · p0012 blank ·
p0013–p0016 Preface (v–viii?), signed Charles Kingsley · p0017–p0023 Contents · p0024 blank · p0025 List of
Illustrations · p0026–p0028 blank · p0029 = printed 1 (offset 28, constant to the end) Chapter I ·
p0439 = 411 end of text (Chapter XXIV, printer's imprint at foot) · p0440 blank · p0441 advertisement "Works by
Rev. Charles Kingsley" · p0442–p0446 endpapers, library slips, back pastedown · p0447–p0453 back cover, colour
cards, edges.
Chapters begin: I p0029, II p0052, III p0075, IV p0093, V p0105, VI p0115, VII p0126, VIII p0136, IX p0153, X
p0165, XI p0180, XII p0195, XIII p0206, XIV p0212, XV p0235, XVI p0260, XVII p0272, XVIII p0296, XIX p0313,
XX p0337, XXI p0364, XXII p0385, XXIII p0410, XXIV p0427 (from the contact sheets; to be confirmed by headings).
Illustrations (engravings in the text): p0006 (frontispiece), p0057, p0060, p0063, p0065, p0071, p0077, p0079,
p0102, p0103, p0116 (diagram of strata, "Grass." / "Plain."), p0118, p0133, p0142, p0185, p0215, p0226, p0263,
p0320, p0327, p0353. The List of Illustrations has 21 entries; "Monument Creek, 88" still to be matched (p0116
is a diagram; the frontispiece caption reads "Monument Park.—Page 88", so the list's "Monument Creek, 88" probably means this diagram or is a slip — check against the draft's captions).
Tables: p0170 (Raymond's table of Western coals, printed sideways), p0323, p0435 (figures in columns).
Footnotes: several (e.g. p0093, p0211, p0376, p0412–p0413, p0429–p0434).
Scan check: all 12 contact sheets looked at 2026-11-19; full size: p0025, p0116, p0170, p0412; problems: none.

## Decisions
- Drafted p0006 and p0009–p0441; covers, endpapers, IA card and tissue guards left out.
- Judge spots on crops: p0013 "Preface.", p0206 "Down the Pacific.", p0272 "…of the Lerma." (full stops printed: judge
  right); p0276 "Micho-|acan" a line-end break, "Michoacan" (judge right); p0263 the engraving splits a sentence, order as
  the judge has it; p0016, p0025 (list of illustrations), p0441 (advertisement): small capitals without taller
  capitals, the judge's readings kept (front matter and advertisement, JSON only).
- p0318 "where-|ever" broken at the line end; kept as "whereever" as the judge read it (the book has "wherever" six
  times; assumed, easily changed: it may be a misprint, but not unmistakably one).
- p0420 printed ‘<i>Vamonos!</i>” (single opening, double closing): `[[corr ‘|“]]` as in *Flying Leaves* p0207. The
  accent on "Vámonos" (both readers; a faint mark on the scan) kept.
- Contents (Tom's policy of 2026-11-19, `notes/workflow.md` stage 4 "Contents"), decided ahead of the structure
  pass: one entry per chapter, "Chapter N. Title" as the printed contents heads them, all 24 alike (the titles
  are short, so the default `toc` is enough). The printed contents also gives each chapter a long list of topics
  (about 25–30, "First land—Our pilot—…"); these are too long for entries and stay in the JSON (division
  `contents`, left out of the reading editions). The Preface and the List of Illustrations: the Preface is an entry,
  the List of Illustrations is not (kind `illustrations`). No editor's entries: the chapters are short (10–25 pages).

- Structure pass (2026-11-19, routine): the printed contents (p0017–p0023) made plain lines like the printed page
  (centred "Chapter N." and title, then the topics with the page reference); the drafts had typed them as `##`
  headings and tables. Column heads "PAGE" and dot leaders left out. Every chapter heading in the text has its title
  and its topics as `[[subtitle]]`s, matching the printed contents; "Over the Ratons" (p0121) is a `##` section,
  as printed. Divisions: frontispiece leaf front, title page, dedication (reading), preface, contents, list of
  illustrations, advertisement. Contents of the editions: Dedication, Preface, 24 chapters as "Chapter N. Title".
- The nine `joins` items (a page beginning a new sentence with `[[cont]]`) looked at on the scan: every one of those
  pages begins flush left, without the paragraph indent, so the paragraph goes on; kept.
- p0124 "Sam follows my example": no opening quotation mark in print inside a quoted story; kept, waived.
- p0170 the key to the sideways table of coals made a three-column table with the ditto marks as printed (one in the
  analyst column, two where the coal is also "ditto"); the stray mark near "Prof. E. T. Cox" read as the ditto of row
  10; waiver for the space before a ditto mark.
- `keep_hyphens` p0067 "snow-|fences" (the book hyphenates its snow- compounds); the other 26 hyphen joins read once.
- The frontispiece caption reads "Page 89" (checked; the log's earlier "88" was the list of illustrations).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-19 | opus | 413 of 432 | 27.37 | stopped at Tom's request; 3 pages refused by the output filter |
| draft | 2026-11-19 (routine) | opus | p0424–p0441 (18) | 1.18 | no refusals |
| fallback draft | 2026-11-19 (routine) | tesseract + opus corrections | p0076, p0109, p0189 | 0.20 | all three done |
| corrections | 2026-11-19 (routine) | sonnet | 434 | 13.91 | 39 word, 24 punctuation, 13 markup changes; NONE on the fallback pages |
| judge | 2026-11-19 (routine) | opus | 63 spots on 24 pages | 1.13 | draft 24, Sonnet 39; most on the contents and list of illustrations (markup) |
| audit | 2026-11-19 (routine 2) | opus | 6 random + 3 fallback pages | 0.56 | 30/30 and 15/15 planted; 1 candidate (p0189 “day-” at a line end), not an error |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-19 | PASS — 0 to fix, 2 waived; to look at: hyphen-joins 26, joins 9, contents 1 (all read) — tools@6b8af86 | 30/30 and 15/15 (fallback pages); 0 real errors / 9 pages | first publication; three pages by the OCR fallback |
| 2 | 2026-11-20 | PASS — 0 to fix, 2 waived; to look at: hyphen-joins 2, contents 1 — tools@920c2e8 | as v1 (text unchanged except the fixes) | found at the review after ten books: four paragraphs cut in two by an engraving mid-sentence (p0079, p0102, p0118, p0226: no `[[cont]]` after the caption) joined; new preflight check `image-splits` lists such cases. Built page looked at (p0079 joined). |
| 3 | 2026-11-20 | preflight PASS: south-by-west-kingsley v3 — 0 to fix, 2 waived; to look at: hyphen-joins 2, contents 1, accents 11 — tools@9de0b2b 2026-11-20 | record copied (text unchanged except listed fixes) | Accents checked on the scan at the review after twenty books (new preflight list `accents`). p0117: “potatoës” was a speck over the e; now “potatoes” as printed. p0322: a stray acute printed over “rode” is now marked as a printer’s error (rode). |
| 4 | 2026-11-21 | south-by-west-kingsley v4 — 0 to fix, 2 waived; to look at: hyphen-joins 2, contents 1, accents 11 — tools@d6d9a1f 2026-11-21 | as v1 (text unchanged except listed fixes) | stanza break(s) at page tops restored (review after thirty books, `verse-joins`, checked on the scan) |
| 5 | 2026-11-21 | south-by-west-kingsley v5 — 0 to fix, 2 waived; to look at: hyphen-joins 2, contents 1, accents 11, rare-forms 3 — tools@25267f47 2026-11-21 | as v4 (text unchanged except listed fixes) | “water” for “water.” (p. 368) (found by a sweep of all the books after a reader’s report (issue #117), checked on the scan). |
| 6 | 2026-11-22 | PASS, 0 to fix, 2 waived; to look at: hyphen-joins 2, contents 1, accents 11, rare-forms 3, serial-commas 2 — tools@ed86e62f 2026-11-22 | as v5 | A printer’s error of a dropped or transposed letter marked and corrected: “inumerable” for “innumerable”. Found by the review after fifty-five books (`rare-forms` extended), each checked on the scan by an Opus subagent. |

## Known issues
- Waivers: quote-balance p0124 (as printed), spacing p0170 (a ditto mark). The `contents` look item on p0021 is the
  Chapter XIX topics running over to p0022 (the check reads one page at a time).

- 2026-11-21 (Tom's session on the home page): `images/cover.jpg` is now the title page (leaf p0009, from the Drive cache), not the front cover, on which no title can be read (Tom: the picture on the book's page and in the carousel must have a readable title). No new version: the text is unchanged; the EPUB's cover picture changes with it.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
