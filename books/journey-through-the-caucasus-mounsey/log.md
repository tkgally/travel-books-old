# A Journey through the Caucasus and the Interior of Persia — Augustus H. Mounsey (1872)

IA: journeythroughca00moun (University of Toronto; 364 images, 500 ppi). The only IA scan used.
Eligibility: queued 2026-11-20 (Opus subagent); re-checked at the start the same day (not in pg_catalog.csv; a web
search of the title finds catalogue records, booksellers and the Kessinger print-on-demand reprint only). Author
1834–1882. Taken up 2026-11-20.

## Status
Published, version 2 (2026-11-20). Nothing pending.

## Page map
Scan check 2026-11-20 (Opus subagent: all 10 sheets; full size the map, title, contents, pp. 1, 123, 181, 220, 321, 336): PASS.
p0000, p0363 colour cards (hidden) · p0001 front cover · p0002–p0006 endpapers and blanks (p0004 IA "Digitized" leaf) ·
p0007 title page (i; pencilled "Nov 1872") · p0008 verso (ii; library stamp) · p0009–p0014 Preface pp. iii–viii (signed
Vienna, May 1872) · p0015–p0017 Contents pp. ix–xi (chapter summaries with pages) · p0018 blank (xii) · p0019 blank ·
p0020 folding map, opened and whole (greyscale: the route "coloured red" shows as dark lines) · p0021 = p. 1 (title head
over Chapter I) … p0353 = p. 333 · p0354 blank (334) · p0355–p0356 Appendix "Routes" pp. 335–336 (two-column tables, dot
leaders, mileages; printer's imprint) · p0357–p0362 blanks, endpapers, library pocket, back cover. No index, no
advertisements. Offset leaf − page = 20 throughout.
Chapters: I p0021 · II p0034 · III p0048 · IV p0057 · V p0071 · VI p0084 · VII p0103 · VIII p0128 · IX p0147 · X p0168 ·
XI p0190 · XII p0212 · XIII p0243 · XIV p0272 · XV p0304 · XVI p0336. Each opens with "CHAPTER N." and a small-capitals
summary (the same summaries in the contents).
Running heads (even: book title; odd: topic of the page) to be dropped. About 50 footnotes (* †), one running over
pp. 123–124; Italian quotations from Marco Polo (pp. 60, 121–123); verse p. 220 (Moore); a centred inscription p. 181;
sums in "l." italic. No non-Latin script, no side-notes.

## Decisions
- Draft without `--halves` (ordinary octavo). No pages refused.
- Corrections run in two halves (7–170 started while the draft was still running; 171–356 after).
- Judge: 4 spots, all for the draft, all checked on crops: p0017 "Appendix." (as printed), p0020 map title "Mr."
  (a superscript r with a point: typed "Mr."; the title reads "shewing"), p0031 "westernly" and p0188 "dysentry" (printed
  so; spellings of the time, not marked as errors). p0215: the paragraph break the verifier proposed is in the page file.
- Structure: the book title printed over Chapter I (p0021) left out, as in *W.S.W.*; chapter summaries typed without
  `<sc>` (as in every published book); printed contents made plain lines (`[[center]] Chapter N.`, topics with `<pref>`,
  "PAGE" dropped); the appendix as one division "Appendix. / Routes" with the ten routes as `## I. Poti to Tiflis.` etc.
- Contents: the printed contents gives every chapter's summary in full → `"toc": {"subtitles": "all"}`; 16 chapters,
  the preface and the appendix. No entries added.
- The folding map (p0020) cropped in colour (route in red), 2400 px wide, set as `frontispiece` so that it opens Chapter I.
- keep_hyphens: p0046 cartridge-cases, p0107 baggage-horses, p0131 hubble-bubbles, p0158 Kasr-Kajar.
- Spot-read (Opus subagent, 21 pages: contents, verse, Italian, the inscription, the letter, appendix tables with every
  column summed against the printed totals): p0201 "asistance" printed → `[[corr]]`; three Italian elisions closed up by
  the draft (p0141 "l’ affare", p0143 "l’ avessero", "d’ allora") spaced as printed, like the rest of the Italian
  (assumed: the space is kept as part of the Italian of the time, not treated as old spacing); straight apostrophes in
  the page files are curled by the compiler. Everything else as printed.
- Short titles set in `divisions` for Chapter I, Chapter XVI and the Appendix: their summaries are under 80 characters
  and would otherwise go into the title (long pager links), unlike the other chapters (rendered look, Opus subagent).
- Regions added to `data/places.json`: Georgia, Armenia, Azerbaijan (Western Asia). Turkey, Austria and Montenegro are
  passed through only and not listed.

## Runs
| Run | Model | Pages | Cost |
|---|---|---|---|
| draft | Opus | 350 | $22.42 |
| corrections | Sonnet | 350 | $11.05 (12 changes) |
| judge | Opus | 4 spots | $0.17 |
| audit | Opus | 6 (p0063, p0131, p0153, p0167, p0190, p0220) | $0.34: 30/30; 1 candidate (heading case: style, not an error) |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-20 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 5 (read) — tools@5aede16 | 30/30; 0 real errors / 6 pages | first publication; spot-read of 21 special pages; rendered look (Opus subagent): book page, preface, ch. I, VIII, XII, XVI, appendix at 390 and 1280, EPUB nav |
| 2 | 2026-11-20 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 5 — tools@1653f9e | record copied (text unchanged) | summary: one straight apostrophe curled (new check site-text) |
| 3 | 2026-11-21 | journey-through-the-caucasus-mounsey v3 — 0 to fix, 0 waived; to look at: hyphen-joins 5, accents 14 — tools@28b48c1e 2026-11-21 | as v2 (text unchanged except listed fixes) | p. 71 printed “tbe” → [[corr]] (sweep after issue #100) |
| 4 | 2026-11-22 | PASS, 0 to fix, 0 waived — tools@dc366c71 | as before | title page typed line by line as printed (from a `#` heading), checked on the scan; `01.html` looked at; no model calls |

## Known issues
- Footnotes printed in two paragraphs (p0057, p0143–p0144) are one paragraph each: the page markup has no paragraph
  break inside a note. Said in notes_on_text.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
