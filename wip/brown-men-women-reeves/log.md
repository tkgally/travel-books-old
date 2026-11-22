# Brown Men and Women; or, The South Sea Islands in 1895 and 1896 — Edward Reeves (1898)

IA: brownmenwomenors00reevuoft (Robarts – University of Toronto; 312 leaves, 400 ppi). Six leaves from brownmenandwome01reevgoog (University of California copy, Google, greyscale, high resolution): p0088a = n93 (p. 77), p0088b = n94 (p. 78, with the picture “Simalesi in her native dress”), p0142a–d = n149–n152 (pp. 133–136, printed music). Other scan looked at: brownmenandwome00reevgoog (Michigan; its p. 78 picture is lost).
Eligibility: re-checked 2026-11-22: a web search finds booksellers, print on demand, and a PDF of the Toronto scan at mediatheque-polynesie.org (page images, not a text). Rule 5: Reeves's death date uncertain (1912 or 1925); an adult on the Hokitika goldfields about 1865, so born before about 1845 (rule 5, unknown death). Photographers not named.

## Status
Stage reached: (c) everything done; **ready to publish when checks `markup` and `conservation` know `[[stream]]`** — both were extended in the session of 2026-11-22 21:44 +09:00 (new markup `[[stream]]`, test `SecondStream`), so by CLAUDE.md the next session publishes: `preflight.py wip/brown-men-women-reeves` (PASS at tools@e1d3cbb0 + later commits of that session, 0 to fix, 3 waived), then `publish.py brown-men-women-reeves`, versions row, metrics row. Meter at the checkpoint: 28%.
Done in that session:
- Small type set off as quotations: line pitch measured on tesseract hOCR (body text 37 px, quotations 30 px, footnotes and the stream 24 px at 1800 px); every paragraph of Chapter II (yarns) and elsewhere at 30 px made `<blockquote>`; the laws on pp. 115–116, the questions on p. 174; “Other useful regulations are:—” (p. 190) taken out of a quotation. Two paragraphs interrupted by a picture inside a quotation (p0053, p0054) joined before the picture. The struggle section of Chapter X (pp. 268–286) is set in the 30 px type throughout: it is the author’s narrative, left as paragraphs.
- “Excerpts from Tongan Official Documents” (pp. 268–286): `[[stream]]` lines, a division of its own (appendix) after Chapter X; the reference numbers in parentheses bold as printed (186); said in `notes_on_text`.
- Preflight items: eight paragraphs split by a picture given `[[cont]]` (p0041, p0075, p0095, p0167, p0178, p0235, p0238, p0242); two-line captions joined (p0085, p0149: the check compares captions one by one); keep_hyphens p0041 (well-furnished), p0213 (barrel-organful); waivers p0038, p0122, p0143 ([[cont]] after a footnote table / the music pages); printer’s errors permises (p. 122), cocoannt (p. 251), £25,0c0 (p. 30, footnote), scentific (p. 170: found by comparing every page with tesseract’s reading, words tesseract read as non-words where the file has a common word; 80 items, 1 real).
- Spot-read by three Opus subagents (100 pages: front matter, tables, verse, every footnote page, accents): table figures p0121 typed as printed (2001, 315: the draft had silently made them add up); L<sc>ady</sc> B<sc>rassey’s</sc> (p0215); accents: Sàmoa p0036, p0100 (a faint stroke, read as a grave like Nukualofà; assumed), Màngaia p0231; everything else as typed. As printed: “act The” (p0237), “in The” (p0241), “a against” (p0251), “do. and” (p0298), ‘I … him.” (p0223).
- Rendered look: book page (narrow), title page, Chapter II, the Excerpts page: right.
- Audit: 6 pages, 30/30, 1 candidate (cocoa-|nuts at a line end: not an error); 0 real errors.

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
| audit | 2026-11-22 | opus | 6 | 0.42 | 30/30; 1 candidate, not an error |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
