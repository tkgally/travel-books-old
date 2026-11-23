# A Cruise in the U.S. Steam Frigate Mississippi — William F. Gragg (1860)

IA: cruiseinussteamf00grag (Library of Congress; 82 images, 400 ppi). JATSI 14.
Eligibility: queued 2026-11-20 (Opus subagent); re-checked at the start the same day (not in pg_catalog.csv; a web
search of the title finds only the IA scans). Author 1810–1864 (Bedford Historical Society). Taken up 2026-11-20.

## Status
Published, version 1 (2026-11-20). Nothing pending.

## Page map
Scan check 2026-11-20 (the session: all 3 contact sheets; full size p0078): PASS except the last leaf.
p0000 cover outside (dark) · p0001 front wrapper (printed: title within a rule border) · p0002 inside of wrapper, blank ·
p0003 title page · p0004 dedication "Respectfully Dedicated to Dr. Philip S. Wales, U.S.N. by the Author" (LoC stamp) ·
p0005 Prefatory Note · p0006 blank · p0007 = p. 5 "Cruise of the Mississippi." (text starts) … p0077 = p. 75 ·
p0078 = p. 76, last page: **cut at the right edge** (one to three letters a line lost) and a LoC barcode label above
the text → replaced by **p0078a** = UC copy acruiseinusstea01graggoog page n80 (bilevel, 600 ppi, complete), made
1800 px high grey; p0078 itself is not transcribed (preflight `leaves` counts p0078a for it; no waiver needed). · p0079 back wrapper · p0080–p0081 IA colour
cards · p0082–p0083 blank.
Printed-page offset: leaf − 2 throughout (p0007 = p. 5). No chapters, no contents, no illustrations, no index.
A running narrative in paragraphs; lists of officers (p0007) and of the deaths and distances may come up in the text.

## Decisions
- Draft with `--halves` (small type on a large page; 76 pages, so the extra cost is small).
- Judge: 3 spots. p0007 "dismised" and p0064 "Mississipi’s": printed so (crops) → `[[corr]]`. p0060 "hȧd": a speck → "had".
- p0007: "Stemb'e" is a broken *l* (the book prints "Stemble" later; the UC copy has the same break) → "Stemble", no corr.
  "G. 〓. Bacon": the initial is under a blot in the LoC copy; the UC copy (n9) reads "G. N. Bacon". Said in notes_on_text.
- Blank leaves p0002, p0006 given `[[blank]]` page files. keep_hyphens p0008 ("forty-five").
- Contents: no chapters, one division of 72 pages → 11 entries of the editor's (spans of dates and the ports, in the book's
  spellings), proposed by a Sonnet subagent from the draft and checked at paragraph starts. The dedication and the
  Prefatory Note are their own entries. Cover image: the title page (the printed wrapper is cut at the left and labelled).
- Regions added to `data/places.json`: Macau, Madeira, Barbados, United States Virgin Islands.
- Summary: Gragg's place in the crew is not stated in the book (the queue note's "surgeon's steward" is not printed; left out).

## Runs
| Run | Model | Pages | Cost |
|---|---|---|---|
| draft (`--halves`) | Opus | 75 | $8.01 |
| corrections | Sonnet | 75 | $2.58 (3 word changes, 1 markup) |
| judge | Opus | 3 spots | $0.12 |
| audit | Opus | 6 (p0018, p0035, p0039, p0043, p0049, p0056) | $0.37: 30/30, 0 candidates |
Total $11.08.

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-20 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 2 (read) — tools@84a74c2 | 30/30; 0 real errors / 6 pages | first publication; rendered look (Opus subagent): home, book page, 01–03 at 390 and 1280, contents links, notes, EPUB nav |
| 2 | 2026-11-21 | cruise-in-the-mississippi-gragg v2 — 0 to fix, 0 waived; to look at: hyphen-joins 2 — tools@636b1b8d 2026-11-21 | as v1 (text unchanged except listed fixes) | “hnndred” for “hundred” (p. 25); “numher” for “number” (p. 64); “resnlt” for “result” (p. 30) (review after forty books, sweep checked on the scan) |
| 3 | 2026-11-21 | cruise-in-the-mississippi-gragg v3 — 0 to fix, 0 waived; to look at: hyphen-joins 2 — tools@7614af67 2026-11-21 | as v2 (text unchanged except listed fixes) | “day” for “day.” (p. 13) (found by a sweep of all the books after a reader’s report (issue #117), checked on the scan). |
| 4 | 2026-11-22 | PASS, 0 to fix, 0 waived; to look at: hyphen-joins 2, rare-forms 1, serial-commas 4 — tools@ed86e62f 2026-11-22 | as v3 | 2 printer’s errors of a dropped or transposed letter marked and corrected: “wenty” for “twenty”, “exends” for “extends”. Found by the review after fifty-five books (`rare-forms` extended), each checked on the scan by an Opus subagent. |

## Known issues
- The list of corrections on the book page names the first correction by its leaf (p0007), because printed page 5 has
  no number (`[[page ?]]`); the same happens in any book with a correction on an unnumbered page.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
