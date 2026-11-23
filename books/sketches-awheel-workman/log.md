# Sketches Awheel in Modern Iberia — Fanny Bullock Workman and William Hunter Workman (1897)

IA: sketchesawheelin00work (Library of Congress; 338 leaves, 500 ppi, greyscale). Other scans looked at: none (this
one is clean and complete).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv: no Workman); the
Wikisource index (Index:Sketches awheel in modern Iberia.djvu) still has 0 of 336 pages created and no main-namespace
text; web search finds catalogue records, short excerpts on Cervantes Virtual (an anthology page, not an edition)
and Forgotten Books (print on demand). Fanny Bullock Workman 1859–1925; William Hunter Workman 1847–1937.

## Status
**Published, version 2, 2026-11-19** (contents redesign, `notes/errata.md`): the contents now give every chapter its summary in full (book.json `"toc": {"subtitles": "all"}`, `notes_on_text`).
**Published, version 1, 2026-11-19.** The frontispiece (p0008-1) is in the reading editions (book.json `frontispiece`),
at the head of the first reading division as in the Rajah's diary. Rendered look (browser build): book page, Dedications
with the frontispiece, Chapter XI at phone width, Chapter XIII's footnote (p0233), the map division; 31 figures.

## Page map
p0000 colour card · p0001 front cover (plain cloth) · p0002 front pastedown, Library of Congress bookplate ·
p0003–p0007 endpapers, blank · p0008 frontispiece (Puerta del Castillo, Cuenca) · p0009 title page ·
p0010 copyright · p0011 dedications (F. B. W., W. H. W.) · p0012 blank · p0013–p0016 Preface (v–viii, dated Munich,
October 6, 1896) · p0017–p0018 Contents (ix–x) · p0019–p0020 Illustrations (xi–xii, 30 plates) ·
p0021–p0026 Introduction, "Spanish Roads" (xiii–xviii) · p0027 half-title · p0028 blank ·
p0029 = printed 1 (Chapter I). Text pp. 1–242, ends p0328 "The End."
Plates (each with a blank verso, unnumbered, so the offset grows by 2 at each): p0039, p0053, p0061, p0079,
p0085, p0091, p0101, p0115, p0121, p0129, p0135, p0141, p0157, p0163, p0173, p0181, p0189, p0201, p0215, p0219,
p0231, p0237, p0255, p0265, p0283, p0289, p0295, p0315, p0325; many printed sideways.
Chapters (from the contents): I 1, II 6, III 21, IV 34, V 43, VI 55, VII 71, VIII 81, IX 92, X 105, XI 130, XII 149,
XIII 162, XIV 171, XV 182, XVI 194, XVII 211, XVIII 228.
p0329–p0334 endpapers, back pocket · p0335 folding map of Spain (opened, from the back pocket; not in the list of
illustrations) · p0336 back cover · p0337 colour card.
Footnotes seen: p0233 (p. 162). Scan check: all 9 contact sheets looked at 2026-11-19; IA's page numbers run 1–242
without a gap; full size: the plates, p0009, p0335; problems: none.

## Decisions
- Draft range p0008–p0328; the 31 blank leaves in it (plate versos, p0012, p0028) have `[[blank]]` page files
  written by hand, not drafted.
- Cover image: the title page (the cloth cover is plain).
- The map (p0335): an image page at the end, a division of kind `back` titled "Map of Spain" with `reading: true`
  (the title is the editor's, said in `notes_on_text`) (assumed; easily changed). p0329–p0334 (endpapers, the
  pocket) given `[[blank]]` page files.
- Chapter openings are a drop capital followed by full-size capitals ("WE had", "THE twenty-seventh"), so typed as
  plain capitals; seven openings drafted as `X<sc>yy</sc>` (p0021, p0127, p0144, p0192, p0230, p0291, p0310)
  corrected on the scan; the judge's 8 other `<sc>` spots sided with the draft and the scan agrees.
- Small capitals kept in the list of illustrations (p0019–p0020) as printed; p0018 `[[page x]]` (the judge took the
  Sonnet "X"; the folio is lower-case roman).
- "Introduction. Spanish Roads." (p0021): "Spanish Roads" as `[[subtitle]]`.
- The repeated title at the head of Chapter I (p0029) as a `[[center]]` line; it falls in the half-title division
  (JSON only). The half-title p0027: division `front`.
- The six `[[cont]]` after a full stop (p0036, p0111, p0119, p0150, p0168, p0271): first lines flush on the scan; kept.
- Hyphen joins read: all ordinary words (p0166 "honeysuckle" is the book's spelling on p0103 and p0170).
- Spots checked on the scan: p0015 "their number." (broken full stop, kept); p0293 "café" (acute); p0016
  "Munich, October 8, 1896"; p0019 "Montserrat" in the list (the plate caption p0061 has "Monserrat"; both as printed).
- Plate crops by an Opus subagent, all 31 looked at on one sheet by the session; plates printed sideways turned
  with `crop_image.py --rotate 270`; the map in colour at 2400 px.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-19 | opus | p0008–p0328 less 31 blanks (290) | 17.04 | no refusals |
| Corrections | 2026-11-19 | sonnet | 321 | 9.52 | 43 word, 3 punctuation, 9 markup changes |
| Judge | 2026-11-19 | opus | 46 spots on 17 pages | 0.79 | draft 43, Sonnet 3; scan checks above |
| Audit | 2026-11-19 | opus | 6 | 0.33 | 30/30 planted errors found; 0 other differences |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-19 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 31, joins 6 (all read) — tools@e27975f | 30/30 recall; 0 real errors / 6 pages | first publication; held one session for the `conservation` check fix |
| 2 | 2026-11-19 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 31, joins 6 — tools@6b8af86 2026-11-19 | as version 1 (text unchanged) | contents: full chapter summaries in every entry; ODT contents list (errata 2026-11-19) |
| 3 | 2026-11-22 | PASS, 0 to fix, 0 waived; to look at: hyphen-joins 8, accents 2, rare-forms 2, serial-commas 6 — tools@ed86e62f 2026-11-22 | as v2 | 2 printer’s errors of a dropped or transposed letter marked and corrected: “thrity” for “thirty”, “speading” for “spreading”. Found by the review after fifty-five books (`rare-forms` extended), each checked on the scan by an Opus subagent. |

## Known issues

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
