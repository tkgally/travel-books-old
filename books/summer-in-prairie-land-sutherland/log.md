# A Summer in Prairie-Land — Alexander Sutherland (1881)

IA: 31383026813751 (Vancouver Public Library; 220 leaves, 500 ppi; Toronto, Methodist Book and Publishing House, 1881). Other scans looked at: none.
Eligibility: vetted 2026-11-21 (queue row); re-checked 2026-11-21: web search of the title finds only page-image scans (Canadiana, electriccanadian.com PDF of the IA scan, Toronto Public Library) and catalogue records; no reading edition. Sutherland 1833–1910.

## Status
Published v1 2026-11-21.

## Page map
Scan check (Opus subagent, all sheets and full-size leaves): every page iii–x, 1–198 present; no duplicates, cut-offs, blur, folding plates. A perforated library stamp crosses a few lines on p0005 (title), p0015 (p. 1), p0065 (p. 51); legible.
Leaf = page + 14 (p0015 = p. 1 … p0212 = p. 198), no change.
p0000 IA card · p0001 cover · p0002 library label · p0003 barcode label · p0004 blank · p0005 title (no half-title, no frontispiece) ·
p0006 copyright verso · p0007–p0010 Prefatory iii–vi (headpiece, drop capital) · p0011–p0014 Contents vii–x (with chapter
summaries; p0014 also List of Illustrations, 7) · p0015 Chapter I (book title above it).
Chapters I–XIX at p0015 0024 0035 0045 0059 0075 0084 0093 0103 0110 0122 0130 0146 0156 0166 0177 0186 0194 0202.
Full-page plates counted in the pagination: p0034 (p. 20), p0092 (78), p0114 (100), p0134 (120); sideways p0081 (67), p0137 (123), p0180 (166).
p0212 p. 198 end (tailpiece, imprint) · p0213–p0217 blank · p0218 back cover · p0219 IA card. No appendix, index or advertisements.
Has: engraved headpieces and drop capitals at every chapter; tailpieces; much verse; footnotes p0055 0079 0113 0184; speeches at an Indian council (p0104–p0108).

## Decisions
- Chapter headings as printed (“VI.” and its title); the printed contents gives a summary for each chapter, which stays in the JSON;
  the reading contents shows number and title. Chapter VI’s printed title is “At Morley—Sabbath Services.” though the contents
  gives “At Morley” (kept as printed).
- “A Summer in Prairie-Land.” printed above Chapter I: a `front` division (`n` 1), Chapter I `n` 2; the head-piece moved after that heading so that
  it opens Chapter I (caught by the rendered look: it had gone into the omitted division).
- Printed contents set as plain lines (the draft mixed a table and `##` headings); drop-capital openings typed with the first word in capitals throughout.
- Printer’s errors marked: “thcse” (p. 70), “agreeeable” (p. 185). Kept as printed: “you lodges” (p0108, in a translated speech), “falls” (p0101, verse).
- p0095 “left”: a broken f, not marked. p0040 folio misread as 20 (a broken 26). Cass-Cheney keeps its hyphen (`keep_hyphens` p0023).
- `[[cont]]` removed after verse at p0019, p0070, p0150 (the markup cannot continue a paragraph after a block).
- The Sonnet pass dropped the title line of the title page (listed by `review.py` as a length outlier; restored).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| 1 | 2026-11-21 | preflight PASS, 0 waived | 30/30, 0 candidates | spot-read (42 pages): an accent, three captions’ small capitals; look items: a folio, a broken letter |
| draft | 2026-11-21 | opus | 208 | 13.38 | none refused |
| corrections | 2026-11-21 | sonnet | 208 | 6.62 | 9 changes |
| judge | 2026-11-21 | opus | 6 spots | 0.25 | 5 to look at: 2 printer's errors, 1 drop-capital |
| audit | 2026-11-21 | opus | 6 | 0.34 | 30/30; 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
- After a verse quotation the paragraph that runs on starts a new paragraph (p0019, p0070, p0150).
- Verse indentation is not kept.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
