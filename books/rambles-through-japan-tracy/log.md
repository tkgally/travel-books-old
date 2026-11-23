# Rambles through Japan without a Guide — Albert Tracy [Albert Tracy Leffingwell] (1892)

IA: ramblesthroughja00leffrich (University of California Libraries; 316 leaves, 500 ppi, colour; the author's
presentation copy to the University library). Other scans looked at: ramblesthroughj00leffgoog (University of
Michigan, Google, bitonal, 313 leaves): same edition; used for the one leaf missing from the UC scan (below).
Eligibility: re-checked 2026-11-20: not in the Project Gutenberg catalogue (pg_catalog.csv: Leffingwell's
*An Ethical Problem* and *Vivisection* only); a web search finds only print-on-demand reprints (Forgotten Books,
Read Books, Kessinger). JATSI 86. Albert Tracy Leffingwell 1845–1916.

## Status
**Published, version 2** (2026-11-20): the 37 decorative head-pieces, tail-pieces and the boat vignette (p0079) added, shown small (Tom's answer). Nothing pending.

## Page map
p0001 front cover (cloth, decorated: a jinrikisha, title and author) · p0002 pastedown with the University of
California book-plate (gift of Dr. A. T. Leffingwell, Nov. 1893) · p0003 endpaper · p0004 IA card (hidden? no:
left out of the draft) · p0005 flyleaf inscribed "For the Library of the University of California / From the
Author" (library mark: left out) · p0006 frontispiece "The Road to Nikko" (no printed caption) · p0007 title page
(pencilled "(pseud.)" and the signature "Albert T. Leffingwell, M.D.": manuscript, not transcribed) · p0008 verso
(accession number only: left out) · p0009–p0012 Preface v–viii (signed Oxford, 1892) · p0013–p0018 Contents
ix–xiv (chapter titles and summaries) · p0019 List of Illustrations · p0020 epigraph (Lord Elgin, 1858) ·
p0021 = printed 1, Chapter I (offset 20; the illustrations are printed on text leaves and counted in the
pagination) · … · p0132 = 112 · **pp. 113–114 missing from the UC scan** (one leaf; the text runs from "They did"
at the foot of p. 112 to p. 115): supplied as p0132a, p0132b from ramblesthroughj00leffgoog n134, n135
(book.json `source.extra_leaves`) · p0133 = 115 (offset 18 from here) · … · p0304 Note (286) · p0305 = 287, end,
printer's imprint · p0306–p0309 blank · p0310 library date slip · p0311–p0316 back cover, colour cards.
Chapter openings: I p0021, II p0031, III p0040, IV p0049, V p0058, VI p0067, VII p0080, VIII p0085, IX p0104,
X p0120, XI p0135, XII p0151, XIII p0175, XIV p0189, XV p0204, XVI p0224, XVII p0245, XVIII p0268, XIX p0277,
XX p0288; Note p0304. Head-pieces and tail-pieces are decorative wood-cuts (not in the List of Illustrations).
Illustrations (List of Illustrations; all on text leaves): p0006 The Road to Nikko (frontispiece) · p0026
Yokohama (6) · p0029 An Anglo-Japanese Girl (9) · p0037 Tokio (17) · p0069 Temple at Nikko (49) · p0092 A Môrning
Call (72) · p0118 The Wayside Inn (98) · p0132b A Japanese Peasant (114: **blank in the Google scan**, which
drops halftones; the UC copy lacks the leaf: the picture cannot be supplied, caption kept) · p0192 A Buddhist
Temple, Kioto (174) · p0197 The Great Bell (179) · p0211 A Winter Costume (193) · p0220 A Japanese Theatre (202) ·
p0246 A Japanese Girl (228) · p0262 A Street in Ozaka (244) · p0282 A Southern Jinrikisha (264).
Scan check: all eight contact sheets looked at 2026-11-20; full size: p0132/p0133 (the gap), p0132a/b (Google
leaves, readable; p0132b is a low-resolution leaf, 767×1098, upscaled to 1800 high). Folios followed through:
the only gap is pp. 113–114. Library stamps on several pages (p0009, p0013, p0019, p0057, p0071, p0101, p0133,
p0163, p0195, p0220, p0239, p0289) do not cover text on the contact sheets; to be confirmed in the draft.

## Decisions
- Period 1881 (not stated in the book): "Friday, August 19" and "Wednesday, August 31" fit 1881 and 1887; he
  went from Tokyo to Honjo by stage-coach, and the railway reached Honjo in 1883; Murray's Handbook (Satow and
  Hawes, 1881) is cited in the diary. Against: on 14 July he writes that the Bastille fell "a hundred years ago"
  (loose for 1881, exact for 1889, but 19 August 1889 was a Monday). The summary says the year is inferred.
- Decorative head-pieces and tail-pieces (37, incl. a small oval vignette of boats, p0079): left out of v1
  (assumed); Tom, 2026-11-20: include them, small → v2. Restored in the page files from the judged text (same
  positions), cropped from full-size leaves (`--max 600`, grey), listed in `book.json` `ornaments`. On p0021 the
  head-piece is placed after the half-title line (printed above it), so that it opens Chapter I.
- The half-title over Chapter I (p0021) is a `[[center]]` line, so it falls in the front matter with the epigraph.
- The printed contents gives Chapter III as page "2" (for 20): tagged `<pref to="20">2</pref>`, text as printed.
- The printer's imprint at the foot of the Note (p0305) stays in the Note as printed (assumed).
- Contents: the printed chapter titles with every summary (`"toc": {"subtitles": "all"}`); 22 entries, alike.
- pp. 113–114 from the Michigan (Google) scan of the same edition (`workflow.md` §1.4).
- The plate "A Japanese Peasant" (p. 114) is shown in neither scan: left out, caption kept, said in
  `notes_on_text` (assumed: as for a plate lost from a scan; easily changed if another copy turns up).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-20 | opus | 301 | 19.50 | 0 errors, 0 refused |
| corrections | 2026-11-20 | sonnet | 301 | 9.83 | 30 changes (13 punctuation, 12 words, 5 markup); 1 not applied (a no-op) |
| judge | 2026-11-20 | opus | 25 spots / 12 pages | 0.58 | draft 15, verified 8, a moved paragraph 2 (see below) |
| audit | 2026-11-20 | opus | 6 + 1 | 0.40 | 30/30, 0 candidates; p0132a 5/5, 0 candidates |

**Tool bug found:** on p0092 the verifier moved a paragraph from before the picture to after its caption (two
spots); the judge took the verifier's side at one end and the draft's at the other, and the paragraph was lost
from `judge/p0092.txt`. Found by a word count of draft/verify/pages at the structure pass. `judge.py` now keeps
the verifier's reading at both ends of such a move (test `test_judge_move_judged_both_ways_keeps_text`); re-applied
from the stored verdicts, no new calls. Published books keep no draft, so the same loss cannot be checked there.
Judge report items looked at: contents headings (reformatted by hand), p0054 *saké* (crop: verifier right),
p0092 caption (crop: A MORNING CALL.), p0116 folio 96 (right), p0118 (moved paragraph, consistent), p0305 imprint.
Preflight `joins`: 10 "[[cont]] after a closed sentence", all flush-left continuations on the scan (0 real);
p0225 lacked `[[cont]]` (added). `hyphen-joins`: door-post kept (p0146).

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 2 | 2026-11-20 | preflight PASS — 0 to fix, 1 waived; look: hyphen-joins 2, joins 10 | as v1 (text unchanged) | ornaments added |
| 1 | 2026-11-20 | preflight PASS — 0 to fix, 1 waived (leaves p0008: accession-number verso); look: hyphen-joins 2, joins 10 | 30/30, 0 real errors | first publication |

## Known issues
- "A Japanese Peasant" (p. 114) missing from both scans; to add if another copy is scanned.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
