# Our Ride through Asia Minor — Mrs. Scott-Stevenson (1881)

IA: 39020025955066-ourridethrougha (George Washington University Libraries; 430 leaves, 300 ppi, grey; McGhee
collection book-plate label on the cover). Other scans looked at: ourridethrougha01stevgoog (Harvard, Google,
459 leaves): bilevel, the folding map not opened (only its left part shows): not used.
Eligibility: re-checked 2026-11-20: a web search finds no text edition (the Gutenberg hits are Burnaby's *On
Horseback through Asia Minor*, another book) and only Forgotten Books (print on demand). The author, Mary Esmé
Gwendoline Grogan, married Andrew Scott-Stevenson on 19 October 1871 (thepeerage.com), so was born before 1856;
her death date was not found: rule 5 met by the standing assumption (death before 100). The map was drawn by
Lieut. [H. H.] Kitchener, R.E. (d. 1916).

## Status
**Published, version 1** (2026-11-20). Nothing pending.

## Page map
p0000 front cover (half leather, library label) · p0001–p0003 black (endpapers shot dark: no text) · p0004 title ·
p0005 title verso (printer's imprint) · p0006 dedication (v) · p0007 black (blank verso) · p0008–p0011 Preface
(vii–x, signed Kyrenia, Cyprus, July 1881) · p0012–p0020 Contents (xi–xix, chapter titles and summaries) ·
p0021–p0022 black · p0023–p0024 folding map "Map illustrating Captain & Mrs. Scott-Stevenson's Journey in Asia
Minor, drawn by Lieut. Kitchener, R.E., 1881", shot in two halves (a strip at the fold is not shown in either:
parts of the title words are lost there) · p0025 black · p0026 = printed 1, Chapter I (offset 25, constant to the
end) · … · p0425 = 400, The End, printer's imprint · p0426–p0428 black · p0429 back cover.
Chapter openings: I p0026, II p0039, III p0055, IV p0075, V p0093, VI p0108, VII p0124, VIII p0137, IX p0149,
X p0165, XI p0188, XII p0199, XIII p0216, XIV p0235, XV p0249, XVI p0264, XVII p0279, XVIII p0293, XIX p0306,
XX p0315, XXI p0332, XXII p0346, XXIII p0361, XXIV p0380, XXV p0393, XXVI p0405, XXVII p0415.
No other illustrations; no advertisements; no index. Footnotes throughout.
Scan check: all 11 contact sheets looked at 2026-11-20; folios followed through (offset 25 from p0026 to p0425);
full size: the map (p0023–p0024). Problems: none in the text; the map's fold strip (as in *Corona and Coronet*).

## Decisions
- Draft pages p0347, p0348 (printed 322–323) refused by the output filter: OCR fallback (tesseract + Opus), then the Sonnet pass, judge and a second audit (10/10). No italics on either page (checked on the scan). Said in `notes_on_text`.
- Judge: 11 spots (draft 9, verifier 2). p0119 "rame" (judge) → "name": a broken *n* (the same page prints "expressi ng" with a damaged *n*); p0142 "Mr. Davis’ had written": printed so, kept; p0102 "mattrasses" as printed.
- Contents (p0012–p0020): made plain lines as printed (`[[center]]` number; small-capital title with `<pref>`; the summary as a paragraph); "PAGE" heads dropped. Chapter V is listed at 69 but begins on 68 (left as printed, said in `notes_on_text`). Editions' contents: the 27 chapter titles with every summary (`"toc": {"subtitles": "all"}`), as printed; entries alike.
- The half-title "Our Ride through Asia Minor." over Chapter I is a `[[center]]` line, so it falls at the end of the Map division (as *Rambles*).
- The map: a reading division "Map" (p0023) after the contents, two images (assumed; easily changed).
- keep_hyphens p0241 (Easter-time), p0313 (market-place: the book prints it elsewhere).
- preflight `joins`: 10 items, all flush-left continuations (looked at on the scan): none real.
- Footnotes signed by nobody but speaking of "Mrs. Scott-Stevenson" in the third person (p0037) are kept as printed.
- Cover: the title page (the binding is plain half leather with a library label).
- The map (two halves, p0023-1 and p0024-1) is shown as two images; not joined, since the strip at the fold is missing (as *Corona and Coronet*).
- Contents: printed contents pages to be made plain lines as printed (lessons, trigger "a printed contents with chapter summaries").

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-20 | opus | 418 | 27.71 | 0 errors; 2 refused (p0347, p0348) → OCR fallback (incl.) |
| corrections | 2026-11-20 | sonnet | 418 | 13.68 | 13 changes (5 words, 6 punctuation, 2 markup) |
| judge | 2026-11-20 | opus | 6 pages, 11 spots | 0.28 | draft 9 / verifier 2; 1 overturned on the scan (p0119) |
| audit | 2026-11-20 | opus | 6 + 2 | 0.46 | 30/30 + 10/10, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-20 | PASS, 4 waived (blank leaves p0007, p0021, p0022, p0025) — tools@b2206d8 | 30/30; 0 real / 6 pages; fallback pages 10/10 | total Claude cost $42.13 |
| 2 | 2026-11-20 | preflight PASS: our-ride-through-asia-minor-scott-stevenson v2 — 0 to fix, 4 waived; to look at: hyphen-joins 1, accents 10 — tools@9de0b2b 2026-11-20 | record copied (text unchanged except listed fixes) | Accents checked on the scan at the review after twenty books (new preflight list `accents`). p0410: “Zêna” corrected to “Zéna” as printed (a clear acute). |
| 3 | 2026-11-21 | our-ride-through-asia-minor-scott-stevenson v3 — 0 to fix, 4 waived; to look at: hyphen-joins 1, accents 10 — tools@636b1b8d 2026-11-21 | as v2 (text unchanged except listed fixes) | “eame” for “came” (p. 100) (review after forty books, sweep checked on the scan) |
| 4 | 2026-11-21 | our-ride-through-asia-minor-scott-stevenson v4 — 0 to fix, 4 waived; to look at: hyphen-joins 1, accents 10, rare-forms 4 — tools@7614af67 2026-11-21 | as v3 (text unchanged except listed fixes) | “all” for “all.” (p. 247) (found by a sweep of all the books after a reader’s report (issue #117), checked on the scan). |

## Known issues
- The map's fold strip is missing from the scan (`notes_on_text`).

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
