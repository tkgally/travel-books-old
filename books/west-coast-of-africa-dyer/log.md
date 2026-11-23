# The West Coast of Africa as Seen from the Deck of a Man-of-War — Hugh McN. Dyer (1876)

IA: westcoastofafric00dyer (Brandeis University; 202 images, 400 ppi). The only IA scan.
Eligibility: queued 2026-11-20 (Opus subagent); re-checked at the start the same day (not in pg_catalog.csv; a web
search of the title finds catalogue records only). Author 1832–1875; the book appeared after his death with an unsigned
introduction by friends. Taken up 2026-11-20.

## Status
Published, version 1 (2026-11-20). Nothing pending.

## Page map
Scan check 2026-11-20 (Opus subagent: all 6 sheets; full size p0006, p0008, p0013–p0015, p0036, p0042, p0043, p0102,
p0141, p0175, p0187; printed pages followed 1–171): PASS.
p0000 hidden · p0001 front cover (gilt "H.M.S. TORCH") · p0002 bookplate · p0003–p0005 endpapers, blank ·
p0006 frontispiece "H.M.S. 'Torch' manning and arming boats in the River Congo" (sideways; caption bottom-to-top on the
right) · p0007 title page (i) · p0008 verso (ii, printer's line) · p0009–p0011 Introduction (iii–v; unsigned, third
person, "the late" Commander) · p0012 blank · p0013–p0014 Contents (vii–viii; summaries; the page numbers are each
chapter's last page) · p0015 = p. 1, Chapter I (title repeated in blackletter under a head-piece; decorated drop
capital O) · p0035 blank · p0036 plate "H.M.S. 'Torch' in a Tornado" (sideways, same way) · p0037 = p. 21 … p0187 =
p. 171 (end; printer's imprint) · p0188 blank · p0189–p0192 publisher's advertisements (Griffin, naval books) · p0193
blank · p0194–p0196 endpaper, label, back cover · p0197–p0201 hidden.
Offsets: p0015–p0034 leaf − 14; p0037–p0187 leaf − 16.
Chapters (no titles): I p0015 · II p0042 · III p0066 · IV p0085 · V p0100 · VI p0111 · VII p0125 · VIII p0153 · IX p0177.
Verse: p0043 (boatmen's song, 7 lines, with a racial slur), p0175 (an oath, 5 lines). A sworn statement p0140–p0142.
No footnotes, no tables. "neeé Briton" p. 1 (misprint?). Running heads to drop.

## Decisions
- Draft without `--halves`; no pages refused. Corrections in two runs (6–102 during the draft, 103–192 after).
- Judge: 14 spots. Printer's errors marked `[[corr]]` after crops: p0019 "whicb", p0088 "diffculty", p0155 "elswhere",
  p0191 "triumpth" (advertisements), p0166 "some." (a full stop before a lower-case word). Kept as printed: p0110
  "accacia", p0042 "10th April" (probably for May; not corrected). p0172 "grief, but" (comma: verifier). p0187 the
  printer's imprint, dropped by the verifier, restored from the draft. Contents-page heading levels: see below.
- Structure: the book title over Chapter I left out (as in *W.S.W.*); printed contents made plain lines (it was a table
  on p0013 and headings on p0014); the two `#` lines of the advertisement title made one; the royal arms beside that
  title moved after the heading so that they stay in the advertisements (they had ended the last chapter).
- Contents: the chapters have only numbers in the text; the printed contents gives each a long summary (its page
  numbers are the chapters' last pages). Following the print, each entry is "Chapter N." and the summary in full
  (`toc_title` in `divisions`, apostrophes curled by hand; the ship names lose their italics there). (assumed)
- Images: frontispiece p0006 and plate p0036 (both sideways, `--rotate 270`), head-piece p0015 (`ornaments`), the
  publisher's device on the title page (p0007) and the royal arms (p0189). Cover: the gilt front cover.
- keep_hyphens: p0034 fellow-countrymen, p0039 "Where-ever" (joining would give "Whereever"), p0040 south-westerly.
- Spot-read (Opus subagent, 17 pages: title, introduction, contents, verse p0043 and p0175, Hardy's statement, the
  end): no text differences. quote-balance's three items are printed so (p0010 an opening mark missing in print;
  p0141 and p0175 quotations over several paragraphs).
- Regions added to `data/places.json`: Angola, Democratic Republic of the Congo, Liberia, Gabon, Equatorial Guinea,
  Senegal (Africa); Ascension Island.

## Runs
| Run | Model | Pages | Cost |
|---|---|---|---|
| draft | Opus | 187 | $12.05 |
| corrections | Sonnet | 187 | $6.09 (16 changes) |
| judge | Opus | 14 spots | $0.49 |
| audit | Opus | 6 (p0034, p0070, p0079, p0087, p0099, p0113) | $0.34: 30/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-20 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 1, quote-balance 3, contents 9 (read: the contents items are the summaries, which have no heading in the text) | 30/30; 0 real errors / 6 pages | first publication; spot-read of 17 pages; rendered look (Opus subagent) at 390 and 1280, EPUB nav |
| 2 | 2026-11-21 | west-coast-of-africa-dyer v2 — 0 to fix, 0 waived; to look at: hyphen-joins 1, quote-balance 3, contents 9 — tools@28b48c1e 2026-11-21 | as v1 (text unchanged except listed fixes) | pp. 107, 137 printed “aud”, “conld” → [[corr]] (sweep after issue #100) |
| 3 | 2026-11-21 | west-coast-of-africa-dyer v3 — 0 to fix, 0 waived; to look at: hyphen-joins 1, quote-balance 3, contents 9, rare-forms 1 — tools@25267f47 2026-11-21 | as v2 (text unchanged except listed fixes) | “jury” for “jury.” (p. 107) (found by a sweep of all the books after a reader’s report (issue #117), checked on the scan). |
| 4 | 2026-11-22 | PASS, 0 to fix, 0 waived; to look at: hyphen-joins 1, quote-balance 3, contents 9, rare-forms 3, serial-commas 2 — tools@ed86e62f 2026-11-22 | as v3 | A printer’s error of a dropped or transposed letter marked and corrected: “pefectly” for “perfectly”. Found by the review after fifty-five books (`rare-forms` extended), each checked on the scan by an Opus subagent. |

## Known issues
- The list of corrections names the advertisement correction (triumpth) by its leaf, p0191: the page has no number
  (as in *Cruise in the Mississippi*).

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
