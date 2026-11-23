# A Woman's Trip to Alaska — Septima M. Collis (1890)

IA: womanstriptoalas00coll_0 (Getty Research Institute; 226 leaves, 500 ppi). Other scans: cihm_03388 (not looked at).
Eligibility: re-checked 2026-11-20 by the queue's vetting the same day; the text in Alexander Street's subscription database does not count (Tom, 2026-11-20). Author 1842–1917; Sherman's letter (d. 1891).

## Status
Stage reached: published v1 2026-11-20.   Next step: none.

## Page map
p0000, p0225 colour cards (hidden) · p0001 front cover (totem pole) · p0002–p0007 endpapers, blanks (p0006 library label) ·
p0008 folding frontispiece “Façade of Muir Glacier” (opened, complete; a crease) · p0009 portrait of the author · p0010 copyright
(vignette) · p0011 title · p0012 preface · p0013–p0014 Sherman's letter · p0015–p0018 contents (chapter summaries) · p0019–p0021 list of
illustrations · p0022 picture of an addressed envelope · p0023–p0216 text pp. 1–194 (leaf = page + 22 throughout; full-page plates take
page numbers) · p0217 map “Route of the Steamer Queen” · p0218–p0223 blank · p0224 back cover.
Chapters: I p0023 (opens “My dear Amelia:”; no heading); II p0032; III p0056; IV p0067; V p0079; VI p0089; VII p0098; VIII p0111;
IX p0147; X p0166; XI p0181; XII p0197; XIII p0208; “L'Envoi” only as a running head (p0215).
Plates (most sideways): p0042, p0047, p0057, p0081, p0113, p0124, p0129, p0139, p0168, p0178, p0187, p0199, p0211, p0213.
About 70 pictures set into the text, many with text running round them; a vignette at each chapter opening (drop capital in it).
Scan check (Opus subagent, 2026-11-20): all six sheets, about 20 leaves full size: GOOD.
Features: menu (p0045), dance programme (p0193), verse (p0215, p. 63), quoted prose pp. 150–153; “CHAPER II.” printed in the contents.

## Decisions
- The output filter refused 55 of 224 draft pages (printed pp. 2–190, ordinary prose, in runs and singly; listed in
  notes_on_text): `ocr_fallback.py` (tesseract + Opus) did all 55; all 55 audited (273/275 planted errors found, 0 real errors).
- Chapter I has no printed heading: its division starts at the envelope picture (p0022) and is titled “Chapter I”.
- Contents: the printed contents gives long lists of topics; the editions give short titles of the editor's made from them
  (toc_title per chapter), said in notes_on_text. The contents pages made plain lines; “Chaper II.” kept as printed.
- The chapter-opening vignettes (with the drop capital in them), the crest on p0023, the printer's device on p0010 and two
  tail-pieces (p0088, p0180) listed as ornaments (shown small). Text overlapping some vignettes and photographs was painted
  out of the crops with paper tone by the cropping subagents (about 23 crops).
- Drop capitals: the rest of the first word typed in full capitals as printed (judge, five chapter openings).
- p0179 and p0202: a picture at the page top before the continued paragraph moved after that paragraph so that `[[cont]]` joins.
- p0045: `[[cont]]` after the menu removed (a new sentence). p0099: `[[cont]]` added after the picture (mid-sentence).
- Printed so and kept: “Chaper II.” (contents), “W. B. Washburn” (caption), p0194's caption without its opening parenthesis.
- Corrected misreadings: p0068 “fête” (judge had “féte”), p0096 “ones” (draft “onés”), p0139 caption “Sitka” (draft “Sitká”).
- keep_hyphens p0100 (major-general). p0038 “water-marks” at a line end: the book hyphenates every water- compound (assumed).
- Preflight `conservation` (captions) failed though the caption lists were equal once squashed: the check sorts the captions
  before squashing them, and page captions with a straight apostrophe or a leading tag sort differently. Fixed in the book by
  curling the apostrophes in the captions and typing the <sc> captions in upper and lower case (lessons); no waiver. The
  check itself is to be fixed (sort after squashing), with a test, by a later session (metrics.md).
- Captions typed as <sc> in lower case (7) made upper and lower case, like the others (lessons: plates).
- Spot-read (Opus subagent): p0049 caption printed in italics (fixed); p0185 caption made upper and lower case; p0194's caption
  lacks its opening parenthesis in print; p0139 “Sitka” without an accent.
- p0049: `[[cont]]` added before “Brown, two leading citizens” (a paragraph cut by a picture before a capital; rendered look).
- Back cover not shown (cropped, not used); the endpapers after the map are blank leaves in the map's division.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| 1 | 2026-11-20 | preflight PASS: womans-trip-to-alaska-collis v1 — 0 to fix, 0 waived; to look at: hyphen-joins 7, contents 14, accents 5 — tools@7073865 2026-11-20 | 29/30 (6 pages) + 273/275 (the 55 fallback pages); 0 real errors | spot-read: front matter, menu, programme, verse, all 67 captions: 1 caption's italics fixed |
| draft | 2026-11-20 | Opus | 224 (169 drafted, 55 refused) | 11.34 | output filter: 55 pages |
| fallback | 2026-11-20 | tesseract + Opus | 55 | 3.91 | all done |
| corrections | 2026-11-20 | Sonnet | 224 | 7.24 | a first run stopped after a few minutes (cost not kept); 27 spots |
| judge | 2026-11-20 | Opus | 27 spots | 0.77 | draft 11 / verifier 15 / neither 1 (contents layout) |
| audit | 2026-11-20 | Opus | 6 | 0.37 | 29/30; 1 candidate (a heading's capitals): no error |
| audit, fallback pages | 2026-11-20 | Opus | 55 | 3.28 | 273/275; 2 candidates (water-marks, foot-hold at line ends): judged |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 2 | 2026-11-21 | womans-trip-to-alaska-collis v2 — 0 to fix, 0 waived; to look at: hyphen-joins 7, contents 14, accents 5 — tools@25267f47 2026-11-21 | as v1 (text unchanged except listed fixes) | “diminishes” for “diminishes.” (p. 143) (found by a sweep of all the books after a reader’s report (issue #117), checked on the scan). |
| 3 | 2026-11-22 | PASS, 0 to fix, 0 waived; to look at: hyphen-joins 7, contents 14, accents 5, rare-forms 3, serial-commas 7 — tools@ed86e62f 2026-11-22 | as v2 | A printer’s error of a dropped or transposed letter marked and corrected: “adminstration” for “administration”. Found by the review after fifty-five books (`rare-forms` extended), each checked on the scan by an Opus subagent. |
| 4 | 2026-11-22 | PASS: womans-trip-to-alaska-collis v4 — 0 to fix, 0 waived; to look at: hyphen-joins 7, contents 14, accents 5, rare-forms 2, serial-commas 7 — tools@528b2324 2026-11-22 | as before (text unchanged except the title page) | Title page typed line by line as printed (checked on the scan by an Opus subagent; 01.html looked at for two) |

## Known issues

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
