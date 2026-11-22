# Camps in the Caribbees (Frederick A. Ober, 1880) — log

IA `campsincaribbees00oberiala` (University of California, 400 ppi, 410 images).

## Status
Stage reached: (b)/(c): draft (16 pages by ocr_fallback), Sonnet pass, judge, `pages/` from the judge with fixes; pictures cropped; book.json written; preflight fails only on the audit. Running at the checkpoint: spot-read (three Opus subagents), audit (6 pages + the 16 fallback pages as a second run), hOCR for the tesseract and line-pitch checks.
Next: apply the spot-read; tesseract comparison and small-type check (scripts as in the Floyd-Jones log); audit record; rendered look; publish.
Fixes so far: ten pictures at a page top before a `[[cont]]` paragraph moved after it (p0059, p0075, p0111, p0137, p0276, p0287, p0323, p0329, p0347, p0375); `[[cont]]` after the picture on p0147; species headings of the appendix all `###`, the repeated “Catalogue of Birds.—Continued.” removed (p0383); the line “Camps in the Caribbees” above Chapter I a front division; printer's device p0012 cropped (ornament); keep_hyphens p0172 sea-side, p0274 seed-time, p0283 mid-winter.
Judge spots: 20 (10 draft: drop-capital words in capitals, as printed; 10 verifier: pictures moved to their printed place, p0339 page number, p0397 2¾ seen on the crop).

## Page map
p0001 cover · p0002–p0004 endpapers, library slips, IA notice · p0005–p0007 blank flyleaves (p0007 a library stamp; no half-title) · p0008 frontispiece “The Island of Cocoa Palms” (sideways) · p0009–p0010 tissue guard (not transcribed: waiver) · p0011 title page (verse motto; library stamp, “576” by hand) · p0012 verso · p0013 dedication · p0014 blank · p0015–p0017 preface v–vii · p0018 blank · p0019–p0026 contents ix–xvi (synopses) · p0027–p0028 list of illustrations xvii–xviii · p0029 Ch. I p. 1 … p0400 p. 366 · p0401–p0411 blanks, slips, covers, colour cards (no p0407 in the prepared images).
Offset leaf − page: 28 to p. 52; 30 from p. 53 (plate p0081/0082); 32 from p. 185 (plate p0215/0216); 34 from p. 213 (plate p0245/0246).
Chapters (leaf, page): I 0029 1 Dominica · II 0040 12 · III 0053 25 · IV 0068 40 · V 0080 52 (verse epigraph, Lucy Larcom) · VI 0103 73 · VII 0120 90 · VIII 0142 112 · IX 0160 130 · X 0177 147 · XI 0192 162 · XII 0214 184 · XIII 0240 208 · XIV 0263 229 · XV 0279 245 · XVI 0297 263 · XVII 0314 280 · XVIII 0332 298 · XIX 0356 322 Ascent of the Guadeloupe Soufrière. Appendix (by George N. Lawrence): p0380 blank p. 346; p0381–p0384 catalogue of birds (a table, pp. 347–350; “NATICNAL” printed for National); p0385–p0400 descriptions of new species (pp. 351–366). No index, no advertisements, no errata.
Plates (verso blank): p0008 frontispiece; p0081 The Boiling Lake; p0215 Volcano and Lava River of St. Vincent (sideways); p0245 Captain George and his Family (sideways). p0187 a full-page cut on p. 157 (sideways), the Hercules beetle. Cuts in the text: p0037 0042 0059 0075 0089 0111 0116 0124 0137 0147 0151 0169 0176 0203 0238 0257 0271 0276 0287 0299 0313 0320 0321 0323 0329 0336 0347 0357 0375 (many with the text running round them).
To take care of: chapter synopses in small capitals; drop capitals; French, Creole, Carib and Latin in italics; Carib vocabulary pp. 99–106; inscriptions in capitals (p0334–p0335, p0344); footnotes (p0070, p0109, p0121, p0261, p0343 …); verse quotations; the appendix in small type with fractions, numbered species in italics, MALE/FEMALE/REMARKS run-in small capitals; the bird table.
Scan check: all sheets and 15 leaves at full size by an Opus subagent 2026-11-22: complete and good; all 34 engravings present.

## Decisions
- Pictures (34) cropped by an Opus subagent with `--gray` (p0008 rotate 270; p0187, p0215, p0245 rotate 90); four with text set into a notch (p0075, p0151, p0169, p0276) were cropped from a copy with the text lines whited out, so the notch shows as paper. Cover: the title page (the front cover has no title). Looked at by the session.
- Places added to data/places.json: Dominica, Martinique, Saint Vincent and the Grenadines, Guadeloupe.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-22 | opus | 391 | 25.99 | 16 refused by the output filter: p0110, p0112, p0125, p0126, p0128, p0241, p0242, p0249–p0256, p0391 |
| corrections | 2026-11-22 | sonnet | 391 | 13.13 | 18 words, 10 markup, 2 punctuation; 1 not applied (right as typed) |
| judge | 2026-11-22 | opus | 20 spots | 0.73 | 10 draft, 10 verifier |
| fallback | 2026-11-22 | tesseract + opus | 16 | 1.12 | all 16 done; audit them as a second run |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
