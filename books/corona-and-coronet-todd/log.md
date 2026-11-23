# Corona and Coronet — Mabel Loomis Todd (1898)

IA: coronacoronetbei00toddiala (University of California Libraries; 504 leaves + colour cards, 400 ppi,
greyscale). Other scans looked at: none (this one is clean and complete); another IA scan exists
(coronacoronetbei00todd).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv: only Todd's
editions of Emily Dickinson); The Online Books Page lists only the IA scan; web searches find only a print-on-demand
OCR reprint (General Books, 2009) and dealers' copies of the 1898 and 1899 Houghton Mifflin printings; a PDF of
one chapter ("The Eclipse") on the New England Fireball/astronomy society site nefas.org is a brief excerpt.
Wikisource search rate-limited today (none found at the first check). Mabel Loomis Todd 1856–1932; Arthur
Curtiss James (author of "Deep-Sea Yachting", pp. xxiii–xxxvii) 1867–1941. **One drawing** ("Lighthouse on the
Beach at Esashi (from a Drawing by Mr. Thompson)", p0423) is by E. A. Thompson, the expedition's mechanician,
"a young man" in 1896 (p0074): death date not found, birth not before 1856 → under `selection.md` rule 5 the
drawing was left out of version 1 (caption kept, with a note). Tom, 2026-11-20: add it → version 2.

## Status
Published, version 3 (2026-11-20). Nothing pending.

## Page map
p0001 front cover (cloth, crowns stamped; title and author) · p0002 pastedown · p0003 endpaper with an owner's
inscription (1898) · p0004 blank · p0005 blank · p0006 frontispiece "Mr. James's Schooner Yacht Coronet" (sideways)
· p0007 tissue guard · p0008 blank · p0009 title page · p0010 verso (copyright 1898; Riverside Press) · p0011
dedication · p0012 blank · p0013–p0016 Preface (signed M. L. T., Observatory House, Amherst, October 1898) ·
p0017–p0018 Contents · p0019–p0020 List of Illustrations (36 entries) · p0021–p0029 Introductory (xiii–) ·
p0030 blank · p0031–p0046 Deep-Sea Yachting by Arthur Curtiss James (xxiii–xxxvii) · p0047 = printed 1,
Chapter I (plates are unnumbered leaves, so the offset grows) · … · p0489 = 375 end of text (eclipse corona
vignette) · p0490 blank · p0491–p0497 Index (377–383) · p0498 library slip · p0499 back pastedown · p0500–p0505
back cover, colour cards.
Chapter openings (contact sheets): I p0047, II p0054, III p0062, IV p0074, V p0080, VI p0094, VII p0112,
VIII p0124, IX p0134, X p0146, XI p0155, XII p0166, XIII p0175, XIV p0189, XV p0205, XVI p0221, XVII p0240,
XVIII p0251, XIX p0258, XX p0264, XXI p0281, XXII p0292, XXIII p0305, XXIV p0321, XXV p0336, XXVI p0348,
XXVII p0358, XXVIII p0386, XXIX p0418, XXX p0431, XXXI p0440, XXXII p0449, XXXIII p0467.
Plates (full-page, each followed by a blank verso): p0006, p0057, p0069, p0087, p0103, p0119, p0137, p0157,
p0163, p0167, p0199, p0225 (map of Japan), p0249, p0277, p0285, p0289, p0307, p0317, p0329, p0343, p0353,
p0383, p0395, p0401, p0411, p0423 (Thompson drawing: left out), p0427, p0445, p0471, p0487;
p0462–p0463 folding map "Route of the Amherst Eclipse Expedition and Cruise of Mr. James's Schooner Yacht
Coronet, 1895–97", photographed opened in two halves (left and right) with a small overlap.
In-text cuts: p0365 (electric commutator), p0369, p0373, p0489 (corona vignette).
Music (staff notation, to be images): p0089, p0090, p0220 (Japanese national air), p0261, p0356, p0466.
Japanese characters: p0334 (a printed date, one line).
Footnotes: a few (p0086, p0113, p0115, p0183, p0391 …). Verse epigraphs at every chapter head; songs with
numbered verses (p0089–p0090, p0197–p0198, p0459).
Scan check: all 13 contact sheets looked at 2026-11-19; full size: p0017, p0019, p0020, p0021, p0462, p0463;
problems: none (every printed page present; the folding map was opened).

## Decisions
- Drafted p0006 and p0009–p0497; covers, endpapers with the owner's inscription, tissue guard, library slip and
  colour cards left out.
- The folding map: the two halves joined into one image (assumed; easily changed).
- Thompson's drawing (p0423) left out: the page file has its caption as a centred line (no `[[image:]]`) and
  `notes_on_text` says why (assumed; question for Tom in `notes/preferences.md`). To restore: put back
  `[[image: …]]` + `[[caption]]` and crop `full/p0423.jpg` (sideways engraving, --rotate 270 --gray).
- The folding map could not be joined: the two photographs do not overlap and a narrow strip at the fold is
  missing (a few letters: "Sa|cisco", "CORO|T", the "120" longitude label). Shown as two images p0462-1, p0463-1;
  said in `notes_on_text`. The other IA scan (coronacoronetbei00todd) is the 1899 printing, Wellesley; not used.
- Judge spots on crops: p0139 "unfamilar", p0270 "incongrously" printed so → `[[corr]]`; p0209 "devasted" printed
  so, kept (an old form, not certainly a misprint); p0452 "as-|toronomical" printed so in a quoted guide's English,
  kept; p0167 caption "…1820, and Liliha his Wife" (Sonnet right; already so in the page file).
- p0047: "Corona and Coronet" printed above Chapter I is a `#` division of kind `front` (half-title, JSON only).
- Captions printed as separate lines on one plate (p0249 label "U. S. S. Olympia"; p0487 two sub-captions) are one
  `[[caption]]` with the parts separated by full stops, as the draft had done on p0411 (preflight conservation
  compares caption lines; the compiler joins them).
- p0090, p0201: a sentence resuming after verse had `[[cont]]`; removed (it would join the paragraph before the verse).
- Joins look list (9): all eight pages start flush left on the scan → continuations; kept. p0010 front matter.
- keep_hyphens: p0041 out-of-the-way, p0299 stepping-stones (so twice elsewhere), p0457 rose-pink.
- Contents: as printed (33 chapters with titles; Introductory; Deep-Sea Yachting with "by A. C. James" as printed).
  No editor's entries: chapters are 6–30 pages.
- p0018: page numbers made `<pref>` like p0017.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-19 | opus | 490 | 29.46 | no page refused |
| corrections | 2026-11-19 | sonnet | 490 | 14.68 | 11 word, 3 punctuation, 13 markup changes |
| judge | 2026-11-19 | opus | 14 spots on 11 pages | 0.47 | draft 12, Sonnet 2; 3 printer's errors found on crops |
| audit | 2026-11-19 | opus | 6 | 0.34 | 30/30 planted; 1 candidate (heading capitals), not an error |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-19 | PASS — 0 to fix, 2 waived (leaves p0007 tissue guard, p0008 blank); to look at: hyphen-joins 44, joins 9, contents 1 (all read) — tools@9999377 | 30/30; 0 real errors / 6 pages | first publication; one drawing left out (Thompson) |
| 4 | 2026-11-21 | corona-and-coronet-todd v4 — 0 to fix, 2 waived; to look at: hyphen-joins 9, joins 1, contents 1, verse-joins 2, accents 7 — tools@28b48c1e 2026-11-21 | as v3 (text unchanged except listed fixes) | p. 255 “tbe” misread for “the” (found by the sweep after issue #100) |
| 5 | 2026-11-22 | PASS, 0 to fix, 2 waived — tools@dc366c71 | as before | title page typed line by line as printed (from a `#` heading), checked on the scan; `01.html` looked at; no model calls |

| 2 | 2026-11-20 | PASS — 0 to fix, 2 waived; to look at: hyphen-joins 9, joins 9, contents 1 — tools@20307e9 | as v1 (text unchanged) | the plate "Lighthouse on the Beach at Esashi" added: one leaf fetched again from IA (viewer page n420, full size), cropped `0.03,0.125,0.905,0.88 --gray --rotate 270`; looked at in the browser build |
| 3 | 2026-11-20 | PASS — 0 to fix, 2 waived; to look at: hyphen-joins 9, joins 1, contents 1 — tools@1653f9e | record copied (text unchanged) | subtitle: two straight apostrophes curled (new check site-text, review after fifteen books) |

## Known issues
- The folding map lacks a narrow strip at the fold (scan).

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
