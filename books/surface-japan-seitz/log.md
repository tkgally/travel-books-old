# Surface Japan — Don C. Seitz (1911)

IA: surfacejapanshor00seit (The Library of Congress; 222 leaves, 300 ppi). Other scans: surfacejapanshor00seituoft (Toronto), not needed.
Eligibility: re-checked 2026-11-22: a web search of the title finds HathiTrust page images, booksellers and a print-on-demand reprint only. JATSI 239; Seitz 1862–1935 (LC).

## Status
Published v1 2026-11-22. Meter at publication: about 38% of the context.

## Page map
p0000 colour card (hidden) · p0001 cover (cloth, no readable title: picture = title page) · p0002–p0003 endpapers · p0004–p0009 blank flyleaves · p0010 frontispiece (photograph, uncaptioned: man in a straw rain cape on a lake) · p0011–p0012 tissue guard (hidden; not drafted) · p0013 title (in the frame) · p0014 verso (copyright 1911) · p0015 dedication · p0016 blank · p0017 half-title with a sketch · p0018 blank · p0019–p0214 = pp. 1–157 (leaf = page + 18 at first, +2 after each plate; +57 at the end) · p0215–p0217 blank · p0218–p0220 endpapers, back cover · p0221 card.
Plates (uncaptioned photographs in printed floral frames, each with a blank verso): p0023, p0037, p0049, p0057, p0069, p0077, p0089, p0097, p0109, p0117, p0129, p0137, p0149, p0157, p0169, p0177, p0189, p0197, p0209; sideways: p0037, p0049, p0057, p0077, p0089, p0097, p0109, p0117, p0129, p0137, p0169, p0197, p0209.
No contents, no chapters: one text, sections divided by a small centred ornament; “L’Envoi” p. 157. A coin diagram on p. 28 (p0052). Phrase lists, English and romanized Japanese, pp. 41–44 (about p0067–p0072).
Scan check: all sheets and a dozen leaves at full size by an Opus subagent 2026-11-22; p0019 and p0160 looked at by the session. Problems: none (a library stamp on the frame of p0214).

## Decisions
- Every text page is printed inside a bamboo frame with one or two small figure sketches “after Hokusai” in the margins (decoration in rotation, not related to the text). The frame and the running head are left out; **the marginal sketches are left out of v1** (assumed; question for Tom in `preferences.md`; easily added in a later version from the Drive cache). Said in `notes_on_text`.
- The small centred ornaments between sections: `[[break]]`, not cropped.
- No chapters: contents entries of the editor's at the section breaks, each a page of its own (Tom, 2026-11-22): eleven pages of 5–22 printed pages, titled by their main topics (proposed by a Sonnet subagent from the text, shortened). L’Envoi a division of its own.
- 158 `[[image:]]` lines for the frame and the sketches removed after the judge; the 20 plates, the coin diagram and the title-page device kept. Alt text: “printed sideways”, “floral border” taken out; two descriptions corrected on the crops (a shamisen, not a box; the coin labels).
- The phrase lists pp. 41–44 as one `<blockquote>` of lines continued across the pages (two pages had been typed as paragraphs).
- Printer’s errors: beween (p. 32), Tranquilty and disrepect (p. 29; the draft had silently corrected “disre-|pect” at a line end). “Ghengis” (p. 157) kept as printed (a spelling, not certainly the printer’s). “yăgaru” (p. 42): mark unclear on the scan, left as drafted.
- keep_hyphens: flip-flapping (p0047), music-halls (p0103).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-22 | opus | 203 | 13.75 | none refused |
| corrections | 2026-11-22 | sonnet | 203 | 6.77 | 2 words, 1 punctuation; 1 paragraph break not applied (real: applied by hand) |
| judge | 2026-11-22 | opus | 3 spots | 0.10 | all draft; 1 overturned on the crop (n’daro.) |
| audit | 2026-11-22 | opus | 6 | 0.36 | 30/30; 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-22 | PASS, 0 to fix, 0 waived; look: hyphen-joins 7 (read), joins 1 (dedication after the verso), accents 1 (à French), misprints 5 (iu: Japanese), rare-forms 5 (prating, fiber, bunt, shooing, relies: real), serial-commas 7 (pairs) — tools@92cc5898 | 30/30; 0 real | spot-read with tesseract comparison of every page: disrepect, list markup, coin captions, McNEILL; crops by the session: beween, Tranquilty; rendered look: book page, title page, first section, a narrow page, the phrase list; Claude $20.98 |

## Known issues
- Tom (2026-11-22): show one or two typical bordered pages as an illustration near the beginning, with a caption: **v2 ready to
  publish when check `images` knows `editor_images`** (session of 2026-11-22 21:44 +09:00 added the key `editor_images`
  to the compiler and renderers, and to preflight's `images` check, with test `EditorImages`; by CLAUDE.md the session
  that changed a check does not publish the book, so the next one does). Done and seen then: preflight PASS on v2,
  the rendered look of 03.html (both pictures above the narrative, captions in italics). To redo (2 minutes):
  `drive_cache.py fetch books/surface-japan-seitz/source.json $B/pages --pages p0019-p0019` (and p0160), then
  `crop_image.py --gray $B/pages/p0019.jpg books/surface-japan-seitz/images/editor-p0019.jpg 0.005,0.05,0.95,0.945` and
  `crop_image.py --gray $B/pages/p0160.jpg books/surface-japan-seitz/images/editor-p0160.jpg 0.035,0.05,0.985,0.94`,
  look at both, apply this change to book.json (`git apply`), preflight, look at 03.html, `publish.py`:
  ```diff
diff --git a/books/surface-japan-seitz/book.json b/books/surface-japan-seitz/book.json
index 6643a556..d5012760 100644
--- a/books/surface-japan-seitz/book.json
+++ b/books/surface-japan-seitz/book.json
@@ -1,6 +1,6 @@
 {
  "id": "surface-japan-seitz",
- "version": 1,
+ "version": 2,
  "date": "2026-11-22",
  "title": "Surface Japan",
  "subtitle": "Short Notes of a Swift Survey",
@@ -62,9 +62,23 @@
   }
  ],
  "frontispiece": "p0010-1",
+ "editor_images": [
+  {
+   "file": "editor-p0019",
+   "leaf": "p0019",
+   "alt": "Page 1 of the book as printed: the opening text inside a double frame of bamboo canes, with a drawing of a kneeling woman above the title and a man holding up a pole in the margin",
+   "caption": "Page 1, as printed. Every text page of the book is set inside a double frame of bamboo canes, with one or two small figure drawings “after Hokusai” in its margins, used in rotation. The text of this edition leaves the frame and the drawings out. (Picture added for this edition.)"
+  },
+  {
+   "file": "editor-p0160",
+   "leaf": "p0160",
+   "alt": "Page 114 of the book as printed: text inside the double frame of bamboo canes, with a drawing of a man hanging from the frame at the top left and a standing figure at the bottom right",
+   "caption": "Page 114, as printed. Every text page of the book is set inside a double frame of bamboo canes, with one or two small figure drawings “after Hokusai” in its margins, used in rotation. The text of this edition leaves the frame and the drawings out. (Picture added for this edition.)"
+  }
+ ],
  "omitted_from_reading": "The half-title is in the JSON only.",
  "notes_on_text": [
-  "Every text page of the book is printed inside a frame of bamboo canes, with one or two small figure drawings “after Hokusai” in its margins, used in rotation as decoration. The frame and the drawings are left out of this edition; the twenty photographs are included.",
+  "Every text page of the book is printed inside a frame of bamboo canes, with one or two small figure drawings “after Hokusai” in its margins, used in rotation as decoration. The frame and the drawings are left out of the text of this edition; two pages, 1 and 114, are shown as printed before the text, as pictures added by the editor. The twenty photographs are included.",
   "The book has no chapters, only sections separated by a small ornament. The contents entries and the page divisions of the web and EPUB editions, at those breaks, are the editor’s."
  ],
  "history": [
@@ -72,6 +86,11 @@
    "version": 1,
    "date": "2026-11-22",
    "note": "First publication."
+  },
+  {
+   "version": 2,
+   "date": "2026-11-22",
+   "note": "Pages 1 and 114 shown as printed, with the bamboo frame and the marginal drawings, as pictures before the text (Tom’s request)."
   }
  ],
  "toc_entries": [
@@ -133,15 +152,16 @@
  ],
  "summary": "Don C. Seitz, an American newspaper manager, made a short visit to Japan in the summer, a year or two before the book appeared in 1911 (the year of the visit is not given), and set down what he saw in short notes, from a paragraph to a few pages each. He lands at Yokohama, stays in Tokyo, calls on Count Okuma at Kodzu, and goes to Kyoto, Kobe and Osaka, the Inland Sea, Nikko, and Hakone. His notes are on customs and dress, women and their work, wrestlers and festivals, the press, poverty and taxes, education, conscription, and Japan’s place in Korea and Manchuria. A few pages give English phrases with their Japanese equivalents. The book has twenty photographs.",
  "audit": {
-  "version": 1,
+  "version": 2,
   "date": "2026-11-22",
   "pages": 6,
   "recall": "30/30",
   "real_errors": 0,
-  "fixed": 0
+  "fixed": 0,
+  "note": "text unchanged except listed fixes"
  },
  "keep_hyphens": [
   "p0047",
   "p0103"
  ]
-}
\ No newline at end of file
+}
  ```
- The marginal sketches are not in this version (question for Tom).
