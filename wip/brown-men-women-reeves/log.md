# Brown Men and Women; or, The South Sea Islands in 1895 and 1896 — Edward Reeves (1898)

IA: brownmenwomenors00reevuoft (Robarts – University of Toronto; 312 leaves, 400 ppi). Six leaves from brownmenandwome01reevgoog (University of California copy, Google, greyscale, high resolution): p0088a = n93 (p. 77), p0088b = n94 (p. 78, with the picture “Simalesi in her native dress”), p0142a–d = n149–n152 (pp. 133–136, printed music). Other scan looked at: brownmenandwome00reevgoog (Michigan; its p. 78 picture is lost).
Eligibility: re-checked 2026-11-22: a web search finds booksellers, print on demand, and a PDF of the Toronto scan at mediatheque-polynesie.org (page images, not a text). Rule 5: Reeves's death date uncertain (1912 or 1925); an adult on the Hokitika goldfields about 1865, so born before about 1845 (rule 5, unknown death). Photographers not named.

## Status
Stage reached: (b) draft, Sonnet pass, judge done; `pages/` from the judge with fixes (below); pictures cropped (73 files, `images/`); book.json written (no audit yet). Meter at the checkpoint: 47% (session of 2026-11-22 17:43).
Next steps, in order:
1. **The yarns of Chapter II (p0045–p0070) and other quoted passages are printed in smaller type**: some are `<blockquote>` (p0048–p0049, p0063–p0064, p0067–p0068, p0118–p0119), most are plain paragraphs (e.g. p0049 from “Mind you”, all of p0050). Go through every page of Chapter II (and any other small-type passage; the quoted letters in Chapter V and X) against the scan and make them consistent: small type = `<blockquote>` on every page, with `[[cont]]` inside when it runs over (lessons: “quotations set in the text type”).
2. **“Excerpts from Tongan Official Documents”** runs in small type along the foot of pp. 268–286 under the main text of Chapter X, as a second stream. It is now typed as `[[fn cont]]` lines, which join it to note 3 of p0273 (wrong). Decide: (a) make it its own footnote at its first page (`[[fn ‡]]`-style with no mark in the text is not supported) or (b) move it to an appendix-like division of its own with a note in `notes_on_text` (the reading order changes; say so). (b) is easily changed later; assumed (b) unless a better markup is found. `workflow.md` §"Not yet solved" lists it.
3. Three `[[cont]]` warnings that are right as they are (p0038, p0122: the sentence resumes after a table that belongs to a footnote; p0143: after the four music pages): waive in `book.json` with that reason if preflight still lists them.
4. Preflight; spot-read (front matter, tables pp. 24–25, 31, 109–110, 245, verse epigraphs, footnote pages, Chapter X, the accents list: 14 groups, Polynesian macrons); rendered look; audit; publish.
Done so far besides the runs: p0029 torn corner read from the UC copy (n33): at, beauty, “savage,”, Queen’s, might think, one such person, I will illustrate, A quarter of (say so in `notes_on_text`); 31 superscript numerals in Chapter X typed as note references made `<sup>` (they refer to numbered documents); ditto marks „ (p0036, p0043, p0257); a duplicated picture removed (p0239); `[[cont]]` restored p0080, p0113; drop-capital openings all full capitals (p0267 fixed); printer’s errors technially (p0020), Europeans. and (p0286), something. and (p0287); p0263 labels added to the caption; p0257 alt text gives the seating plan’s words.

## Page map
p0001 cover (title readable: the book's picture) · p0002–p0004 endpapers · p0005 half-title · p0006 frontispiece “Calling on a Queen” · p0007 title · p0008 verso (blank) · p0009–p0010 contents (v–vi) · p0011 list of illustrations · p0012 blank · p0013 Chapter I p. 1 · leaf − page = 12 to p0088 (p. 76); [pp. 77–78 = p0088a–b]; 10 from p0089 to p0142 (p. 132); [pp. 133–136 = p0142a–d]; 6 from p0143 to p0300 (p. 294) · p0301 printer’s imprint · p0302–p0313 endpapers, cover, cards (no p0309 in IA's numbering).
Chapters: I p0013, II p0045, III p0071, IV p0111, V p0125, VI p0147, VII p0174, VIII p0201, IX p0233, X p0267. Pictures in the text pages (60 with the frontispiece); full-page ones with blank versos: p0015, p0085, p0135, p0139, p0149, p0153, p0229 (several sideways).
Scan check: all sheets and a dozen leaves at full size by an Opus subagent 2026-11-22. Missing from the Toronto scan: pp. 77–78, 133–136 (supplied as above) and the map of Tongatabu, which the text calls the frontispiece of Chapter III: in neither other scan (Tom, 2026-11-22: a book may be published without its map).
To take care of: epigraphs (verse) and drop capitals at chapter openings; small-capital section heads; many footnotes (Chapter X numbered past 150); tables (pp. 24–25, 31, 109–110, 245); printed music pp. 133–136 (pictures); Polynesian words with macrons and diaereses; Scots dialect.

## Decisions
- The six added leaves as in *Cordillera and Pampa* (`source.extra_leaves`); said in `notes_on_text`.
- The map: missing, said in `notes_on_text`.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-22 | opus | 302 | 23.15 | none refused |
| corrections | 2026-11-22 | sonnet | 302 | 10.84 | 47 words (mostly pictures moved to their printed place), 22 markup, 3 punctuation; 3 not applied (all right as the file has them) |
| judge | 2026-11-22 | opus | 50 spots | 1.41 | 5 draft, 43 verifier, 1 picture kept twice (fixed), 1 caption dropped (restored); spots checked on the scan by an Opus subagent |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
