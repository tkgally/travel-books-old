# Journal of a Residence of Two Years and a Half in Great Britain — Jehangeer Nowrojee and Hirjeebhoy Merwanjee (1841)

IA: journalofresiden00jaha (Getty Research Institute; 538 leaves; 600 ppi, crisp). Other scans looked at: none needed.
Eligibility: re-checked 2026-11-20: not in `pg_catalog.csv`; one web search found only catalogue records and
scan-based e-books (Texas A&M, MPDL: page images); first check 2026-11-19 (queue row). Authors' dates not found
(Wadia family, the "Lowjee family" of the Bombay dockyard): both were working assistant builders in 1838 (the
preface: sons/nephew of the master builder Nowrojee Jamsetjee, 1774–1860), so born before about 1818; by
`selection.md` rule 5 (unknown death = died before 100, birth bounded by career) dead before 1918. The
frontispiece lithograph: G. Bragg del., J. R. Jobbins litho. (minor illustrators: Tom 2026-11-20, no bar).

## Status
**Published, version 1** (2026-11-20). Nothing pending. The model runs (draft/, verify/, judge/, audit/) are in the
git history of `wip/` (commits of 2026-11-20).

## Page map
p0000 colour card · p0001 cover (blind-stamped cloth) · p0002 blank · p0003 endpaper with a handwritten
presentation inscription (left out) · p0004–p0005 endpapers with library pencil notes (left out) · p0006
frontispiece (lithograph portrait of Nowrojee Jamsetjee, head builder, Bombay dockyard) · p0007 title ·
p0008 printer's line · p0009–p0010 dedication (to Sir Charles Forbes) · p0011–p0022 preface (printed iv–xvi) ·
p0023–p0030 contents (with chapter summaries) · p0031 = printed 1 (offset 30, constant to p0522 = 492: checked
from IA's scandata and the sheets) · chapters I–XXXV as in the contents (scandata chapter leaves: 31, 56, 60,
65, 69, 94, 106, 123, 128, 131, 141, 173, 180, 194, 216, 225, 246, 262, 276, 318, 330, 337, 342, 347, 349, 354,
372, 388, 392, 395, 415, 481, 495, 509, 517) · p0522 "Finis" and printer · p0523–p0534 publisher's catalogue
(12 pp., "Works relating to India") · p0535 blank · p0536 back cover · p0537 colour card.
Plates: p0006 (frontispiece) only. Tables: p0085, p0090–p0093 (bridges, population, corn), p0289, p0299–p0301
(dockyard), p0307–p0308, p0398–p0399 (newspaper costs), p0479 (tour table). Verse: p0294–p0298, p0312–p0315
(launch songs), p0496–p0508 (albums, epitaphs). Running quotation marks at line starts in long quotations
(p0137, p0167, p0195–p0199, p0264–p0266, p0376–p0383 etc.): `running_quotes.py` after the judge.
Scan check: all 14 sheets looked at 2026-11-20; full size p0006; problems: none (pencil marks in margins p0125).

## Decisions
- Cover image: the title page (the cloth cover is plain blind-stamped).
- Left out of the drafts: p0000–p0005, p0535–p0537 (colour cards, covers, blank and annotated endpapers).
- Printed contents (p0023–p0030): drafted three ways (## headings, ### lines, centred capitals); made alike:
  `[[center]]` chapter number and page, `[[center]]` title in title case, the topics as a paragraph.
- Contents of the editions: the 35 chapter titles as printed (all under 80 characters, so all shown); for
  Chapter XXXI (66 pages, the tour) six entries of the editor's by date and place (`toc_entries`). Chapter XIX
  (42 pages, Chatham dockyard) left as one entry: one place, no natural breaks by date.
- Chapter openings: small capitals on the first word up to Chapter XXVI and in a few later ones; the later
  chapters print plain roman (checked on the scan): kept as printed.
- Chapter XXXIII printed "Chapter XXXII." → `[[corr]]`. Printer's errors also p0415 "a." and p0506 "ean" → `[[corr]]`.
- p0271 "refreshing. and": the mark sits below the line, a comma whose tail did not print → comma (broken type).
- Ditto marks in tables: „ (p0092–p0093, printed as low commas) and “ (p0299–p0300, printed as turned commas);
  spacing check waived on p0299–p0300 (it reads “ as a quotation mark). „ is not flagged.
- Frontispiece: publisher's line and artists' names left out of the caption (as for *Embassy*); said in notes_on_text.
- Poem titles in Chapter XXXIII typed without small capitals (some drafts had them): title case like the rest.
- Running quotation marks: the drafts already left them out; `running_quotes.py` listed 6, all real opening
  marks (not applied). p0309–p0310: a quoted report interrupted by "(alluding to ourselves)" resumes with a new
  opening mark: printed so, quote-balance waived.
- Joins: 7 "[[cont]] after a closed sentence" alarms, all flush left on the scan (real continuations); p0199 a
  missing `[[cont]]` (real, added); `[[cont]]` removed after verse at p0313 and p0350 and after a table at p0308
  (the sentence resumes after a set-off block); p0238 a page-top continuation drafted as `<blockquote>`, unwrapped.
- keep_hyphens: p0251 saw-mills, p0454 well-executed.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| 1 | 2026-11-20 | preflight PASS — 0 to fix, 8 waived; look: hyphen-joins 4, joins 12, folios 1, contents 26 — tools@65bef57 | 30/30 (p0150, p0164, p0188, p0217, p0396, p0521) + 5/5 on p0212; 0 real errors | first publication; Claude ≈ $50.78 |
| 2 | 2026-11-20 | PASS — 0 to fix, 8 waived; to look at: hyphen-joins 4, joins 1, folios 1, contents 26 — tools@852fcc3 | as v1 (text unchanged except the fixes) | found at the review after ten books (an Opus subagent on the scan): two of the six marks `running_quotes.py` listed were page-top repeats inside an open quotation, not opening marks (p0220 “stand charged…”, p0223 “Yes, I'd swear…”): removed; notes_on_text says the quotation marks follow modern practice. |
| Draft | 2026-11-20 | Opus | 529 (p0006–p0534) | 33.26 | p0212 (printed 182, Houses of Parliament chapter, ordinary prose) refused by the output filter |
| Fallback | 2026-11-20 | tesseract + Opus | 1 (p0212) | 0.06 | audited with `--pages p0212`: 5/5 |
| Corrections | 2026-11-20 | Sonnet | 529 | 16.56 | 38 changes (2 words, 18 punctuation, 18 markup); 5 not applied (already in the draft) |
| Judge | 2026-11-20 | Opus | 20 spots on 12 pages | 0.51 | draft 14 / verifier 6; scan overturned the judge twice (p0212 a speck read as "."; p0499 "yield," → "yield.") |
| Spot-read of tables and verse | 2026-11-20 | Opus subagent | 38 pages | (subscription) | every column total checked; found p0506 "ean" (printed), a wrong `[[cont]]` at p0505, straight apostrophes in verse (the compiler curls them) |
| Audit | 2026-11-20 | Opus | 6 random + p0212 | 0.39 | 30/30 + 5/5; 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 3 | 2026-11-21 | journal-of-a-residence-nowrojee-merwanjee v3 — 0 to fix, 8 waived; to look at: hyphen-joins 4, joins 1, folios 1, contents 26, verse-joins 2, accents 1 — tools@d6d9a1f 2026-11-21 | as v1 (text unchanged except listed fixes) | stanza break(s) at page tops restored (review after thirty books, `verse-joins`, checked on the scan) |
| 4 | 2026-11-21 | journal-of-a-residence-nowrojee-merwanjee v4 — 0 to fix, 8 waived; to look at: hyphen-joins 4, joins 1, folios 1, contents 26, verse-joins 2, accents 1 — tools@636b1b8d 2026-11-21 | as v3 (text unchanged except listed fixes) | “reprcsented” for “represented” (p. 114) (review after forty books, sweep checked on the scan) |
| 5 | 2026-11-21 | journal-of-a-residence-nowrojee-merwanjee v5 — 0 to fix, 8 waived; to look at: hyphen-joins 4, joins 1, folios 1, contents 26, verse-joins 2, accents 1, rare-forms 2 — tools@7614af67 2026-11-21 | as v4 (text unchanged except listed fixes) | “leads” for “leads.” (p. 359); “father” for “father.” (p. 456) (found by a sweep of all the books after a reader’s report (issue #117), checked on the scan). |
| 6 | 2026-11-22 | PASS, 0 to fix, 8 waived; to look at: hyphen-joins 4, joins 1, folios 1, contents 26, verse-joins 2, accents 1, rare-forms 5, serial-commas 2 — tools@ed86e62f 2026-11-22 | as v5 | 8 printer’s errors of a dropped or transposed letter marked and corrected: “posseses” for “possesses”, “assembed” for “assembled”, “tasefully” for “tastefully”, “perod” for “period”, “aferwards” for “afterwards”, “permissoin” for “permission”, “acompanied” for “accompanied”, “possesions” for “possessions”. Found by the review after fifty-five books (`rare-forms` extended), each checked on the scan by an Opus subagent. |

## Known issues
- Waivers: spacing on p0299 and p0300 (6 items: ditto marks “); quote-balance p0309 (printed so).
- The contents check lists the 26 topic paragraphs of the printed contents (no headings for them): expected.
- Two sums in the print do not add up (p0091 Wales row; p0398 "Two Reading Boys"): transcribed as printed.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
