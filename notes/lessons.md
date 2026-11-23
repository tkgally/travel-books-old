# Lessons — a checklist keyed to what the book has

Read **Always**, then only the sections whose trigger matches the book. Every line is something that went wrong
once, here or in pdf-to-epub ("p2e", the private project this pipeline came from). Rules for this file: a
lesson a script can check goes into `tools/preflight.py` or a test instead, and is listed under "Now checked by
tools"; otherwise one or two lines under the right trigger; when a section passes ~12 items, merge or delete.

## Now checked by tools

| What went wrong | Caught by |
|---|---|
| Markup showing in the book; `〓` left in | preflight `markup`, `stray-markup` |
| Straight quotes | compiler; preflight `straight-quotes` |
| Notes without references and the reverse | compiler; preflight `compile` |
| Text lost or reordered between page files and an edition | preflight `conservation` |
| A missing `[[cont]]` at a page top | preflight `joins` (observe; its other half, "[[cont]] after a closed sentence", was dropped at the review of 2026-11-20: 65 alarms, 0 real) |
| Misread or misprinted page numbers | preflight `folios` (observe) |
| Headings that differ from the printed contents | preflight `contents` (observe) |
| Small capitals typed as capitals; old spacing left in | `normalize.py`; preflight `sc-caps`, `spacing` |
| A builder change breaking an earlier book | test `Books` |
| Headings, chapter titles or captions left in capitals | preflight `heading-caps` |
| A missing illustration file crashing the EPUB build [found by the tests, 2026-11-19] | compiler warning; test |
| A finished book failing `conservation` because the compiler moved a plate or a captioned frontispiece [*Sketches Awheel*, 2026-11-19] | preflight compares image captions apart from the text; test `MovedImages` |
| A draft page refused by the output filter and left out unnoticed | `ocr_claude.py` says so at the end of the run; `ocr_fallback.py`; preflight `leaves` |
| A frontispiece left in the front matter, so missing from the reading editions [first book, 2026-11-19] | book.json `frontispiece`; test (set it whenever the book has one) |
| `setup_env.sh`'s https rewrite of the apt mirrors matched nothing (`\|` inside `s|…|`), so apt hung on plain http for 20 min [2026-11-19] | fixed; test `SetupEnv` |
| `drive_cache.py fetch --pages p2029b` refused leaves with a letter (added from another scan) [*Embassy*, 2026-11-20] | accepted; test `DrivePages` |
| `drive_cache.py fetch --pages a,b,c` read the list as one name and fetched the wrong parts without a word [2026-11-19] | lists and ranges accepted, anything else refused; test `DrivePages` |
| A part title with a `[[subtitle]]` ("Flying Leaves. / From the East.") taken for a chapter, so its chapters did not nest under it [*Flying Leaves*, found 2026-11-19] | compiler; test `Contents` |
| Side-notes (marginal notes) lost between page files and JSON, or shown in the editions [*Embassy to China*, 2026-11-20, before the first run] | preflight `conservation` (side-notes apart); test `SideNotes` |
| A paragraph moved by the verifier (before a picture → after its caption) judged one way at one end and the other way at the other, so `judge.py` dropped it [*Rambles*, p0092, 2026-11-20] | `judge.py` keeps the verifier's reading at both ends; test `test_judge_move_judged_both_ways_keeps_text` |
| A paragraph interrupted by an engraving in the middle of a page split in two (`[[cont]]` dropped) [*South by West*, 2026-11-19] | compiler joins it; test `ImageInParagraph` |
| A paragraph cut in two by an engraving mid-sentence: no `[[cont]]` after the caption, so the compiler cannot join it [*South by West* v1, four pages, found at the review of 2026-11-20] | preflight `image-splits` (enforce since the review after fifteen books); test `ImageSplits` |
| Straight apostrophes in book.json text written by hand (summary, subtitle, contents titles), shown on the site as written [*West Coast of Africa*, 2026-11-20; three earlier books] | preflight `site-text` (enforce since the review after twenty books); test `SiteText` |
| A word spelled with different accents in different places, misread by every stage [*Land of the North Wind*, 35 pages, 2026-11-20] | preflight `accents` (observe: a list of groups to look at on the scan); test `Accents` |
| The verifier dropped a letter's heading at a page top and the judge agreed, sure, taking it for a running head, so the spot never reached report.txt [*Summer Greetings from Japan*, 2026-11-20] | `judge.py` always reports a spot that touches a `#` line; test `test_judge_heading_spot_always_reported` |
| A footnote's table and second paragraph typed after the note on lines of their own, so set as body text [*My Life in Mongolia and Siberia*, 2026-11-20: caught only by the rendered look] | preflight `note-tail` (observe); test `NoteTail` |
| A correction on an unnumbered page listed by its leaf name on the book page | the division's title ("Contents, unnumbered page"); test `CorrectionPage` |
| The verifier left out a picture and the judge agreed, "sure: medium" [*Zephyrus* p0171, 2026-11-20] | `judge.py` keeps the draft's `[[image:]]` line unless the verifier put it elsewhere, and reports the spot; test `test_judge_never_drops_a_picture` |
| The verifier left out a plate's caption line and the judge agreed [*Western Wanderings* p0312, 2026-11-22] | `judge.py` keeps `[[caption]]` lines like pictures; test `JudgeKeepsCaptions` |
| Captions with a straight apostrophe or a leading tag made `conservation` (captions) fail though nothing was lost [*Alaska*, 2026-11-20] | captions sorted by their squashed text; test `CaptionOrder` |
| A stanza ending at a page foot joined to the next page's first stanza by `[[cont]]` [*Twelve Years in Canterbury*, 2026-11-20: caught by the rendered look] | preflight `verse-joins` (observe: stanza lengths on both sides); test `VerseJoins` |
| A book without `images/cover.jpg` | preflight `cover` (enforce since the review after thirty books) |
| The verifier dropped two page-top `[[cont]]` marks, applied unjudged as a markup change [*Nile without a Dragoman*, 2026-11-21] | `review.py` lists every `[[cont]]` added or removed; test `test_review_cont_changes` |
| A printed turned or wrong letter in a common word (“ean” for “can”, “aud”, “iu”, “conld”) copied faithfully by draft, verifier and judge and never marked [*Trans-Caspia*, a reader, 2026-11-21; 7 more in 6 books; “iustead”, “wc”, “ofl ive” in *The Bridal and the Bridle*, found only by the spot-read, 2026-11-22]; “th” for “the” at a line end, *Cordillera and Pampa* and *Bridal*, a reader, issue #169 | preflight `misprints` (observe: every item looked at on the scan); test `Misprints` |
| Printed misprints in less common words (“hnndred”, “numher”, “entranee”, “pertorm”) kept faithfully and never marked: 15 in 11 books [review after forty books]; a dropped or transposed letter (“magificent”, “clegyman”): 36 in 22 books [review after fifty-five books] | preflight `rare-forms` (observe: the collection as dictionary; confusable letters, and for words seen once a dropped or transposed letter); test `RareForms` |
| A full stop left out in print (“hard work and privation His orders”) copied faithfully by every stage and never marked [*The Golden Dagon*, a reader, issue #117, 2026-11-21; 15 more in 12 books] | preflight `missing-stop` (observe: every item looked at on the scan); test `MissingStop` |
| A plate's cross-reference (“[*See* page 107.”) or “To face p. N” typed as a line of its own after the caption, so the next page's `[[cont]]` text was right-aligned under the picture [*Uganda for a Holiday*, 3 plates; *Argentine Plains*, 26 lines: caught by the rendered look] | preflight `caption-tail` (observe); test `CaptionTail` |
| A picture printed above a chapter's title on the same page put at the end of the division before [*Present-Day Japan*, six chapters, 2026-11-22: caught by the rendered look] | preflight `image-before-heading` (observe: move the picture after the title and subtitle); test `ImageBeforeHeading` |
| A `compile` waiver passed preflight, but test `Books` failed once the book was merged and stopped the deploy of the site; the cause was two footnote tables set as body text (preflight `note-tail`, read and not acted on) [*Brown Men and Women* v1, 2026-11-22] | `publish.py` refuses compile warnings other than hyphen joins; test `test_publish_refuses_compile_warnings`. A table in a footnote is made one line of its note |

## Always

- **Never publish a single-model transcription.** Drafts run away, truncate, drop first lines, duplicate
  passages [p2e]. Two differently biased readings, differences judged.
- **Models silently restore what they think the text should be**: modern spellings, familiar place-names,
  regular grammar. A familiar title too: “Ta-ra-ra-ra-boom-de-ay” typed with three “ra” by every stage (*A Woman Alone*, 2026-11-22; found by the spot-read's tesseract comparison). The check is a second reading with a different bias, never the same model again [p2e].
- **Readers and judges are wrong about 1 time in 6–30** on the changes they propose [p2e]. A proposed change
  to a letter is looked at on a crop before it is accepted, above all one towards the more usual form.
- A page whose two readings differ in length by more than 5% needs a look (`review.py`): crop it before `pages/` is made. *Vacation Days* p0058: the Sonnet pass dropped two lines after a picture, the judge sided with it, and only the rendered look caught it (2026-11-22). Before publishing, compare each page's length in `draft/` and `pages/` by script.
- `review.py`'s "not applied" corrections are unjudged and can be real: a dropped word (*Gentle Jehu* p0089 “are”) and a
  misread word (*Nile* p0206 “outang”). Crop every one.
- More reasoning effort is not better OCR; text-only clean-up without the image is not worth doing [p2e].
- Take the bibliographic facts from the title page, not from IA's record.
- Start the model runs first and do page-map work while they run — but only after the scan check has come back: it reads the list of illustrations, where a photographer or illustrator is credited whose dates may not be known (*A British Officer in the Balkans*, 2026-11-23: “photographs taken by Mrs. Henderson” found after $27.60 of draft; the book waits for Tom).
- Screenshots are for layout only; preflight and the audit are for the text.
- Read the generated contents as a reader would before publishing: the first three books went out with
  chapter entries unlike one another (long summaries dropped) and a 90-page diary as one entry; Tom asked for
  contents decided book by book (`workflow.md` stage 4 "Contents") [2026-11-19].
- Centred italic subheadings inside chapters: the Sonnet pass dropped five as if running heads, and the judge's “could not undo” left them out of `judge/`; when `report.txt` says so, start `pages/` from the draft and re-apply the other spots by hand (*A Woman Alone*, 2026-11-22).
- Running heads that repeat the chapter title: the Sonnet pass dropped 26 chapter headings as running heads, the judge restored 17 and “could not undo” 9 (*Japan for a Week*, 2026-11-22); same remedy: `pages/` from the draft.
- List every `#` and `##` line after the judge: drafts type an odd running head (a chapter title on one page, "Index" on
  index pages, "List of Illustrations" on its second page) as a heading (*Path of the Conquistadores*: 4, 2026-11-20).
- `omitted_from_reading` names only what a division really leaves out: a printer's imprint after “The End” stays in the
  last chapter (*Kothari*, 2026-11-20: caught by the rendered look).
- A folded page corner (the right ends of the last four lines lost) passed the scan check by a subagent; the draft's 〓 marks showed it (*China and Japan*, p. 105, 2026-11-22). After the draft, `grep -l 〓 draft/*.txt` and look at each page at once: a damaged leaf is taken from another copy while the scan is at hand.
- Tables and multi-line letters inside quotations or footnotes: the markup has neither (a table in `<blockquote>` shows its pipes; lines after a `[[fn]]` become body text). Close the quotation round a table; join a letter in a note into the note line (*Venezuela*, 2026-11-22: preflight `conservation` and `note-tail` caught both).
- A model that returns "no corrections" in a few seconds may still be right: the audit's planted errors say
  whether that reader can see (first calibration: Sonnet 27/30, Opus 30/30).

## Trigger: plates (tipped-in leaves) and a frontispiece

- Pictures printed on the contents or list-of-illustrations pages go wherever those pages go (left out of the reading editions): say so in `omitted_from_reading` (*Present-Day Japan*, 2026-11-22).
- `ocr_claude.py --pages` takes leaf numbers (`7-355`), not names.
- Tissue guards: the draft transcribes what shows through them (the whole title page; the frontispiece as an `[[image:]]` with its caption), so the text appears twice (*Sunny Australia*, 2026-11-23: seen as a length change on p0010). Empty those leaves to `[[page ?]]` and say so in `notes_on_text`; better, leave them out of `--pages` when the scan check names them.
- Captions printed in small capitals: drafts type some as `<sc>…</sc>` in lower case and the rest in upper and lower
  case; grep `[[caption]] <sc>` and make all upper and lower case (12 of 148 in *Via Rhodesia*).

- A picture printed beside or above the `#` heading of a division left out of the reading editions (advertisements,
  title page) belongs after that heading in the page file; before it, it ends the previous chapter (*West Coast of
  Africa*: the royal arms of the advertisements showed at the end of the last chapter).
- A plate bound just before the page it faces, where a letter or section begins, ends the division before; `leaf_order` reads it after that page (*A Trip to Mexico*: 3 plates; caught by the rendered look).
- Tissue guards over plates show the plate or the facing text through: leave them out of the draft (they invite ghost text) and waive each in `leaves`.
- A picture printed above a chapter's `#` heading (a head-piece photograph) ends the previous chapter unless it is an ornament: put its `[[image:]]` after the heading (*Trans-Caspia* p0166: caught by the rendered look); and after the `[[subtitle]]` line, or the chapter's title drops out of the contents (*An Artist in the Himalayas*: 8 chapters, caught by reading the compiled contents).
- A `toc_title` written by hand is plain text: its italics are lost.
- Decorative chapter head-pieces and tail-pieces: drafts mark each as `[[image:]]`; keep them, crop them, list them
  in `book.json` `ornaments` (shown small; Tom, 2026-11-20).
- A picture can split a sentence before a capitalized word ("chief of the | Easterlings", *By Fell and Fjord* p0224):
  preflight `image-splits` looks only for lower case after the picture; read the text before each picture (for the review).
- A frontispiece printed sideways has no caption to show which way: crop it, look at both turns.
- Plates printed sideways: `crop_image.py --rotate 270` when the caption reads bottom to top along the right edge.
- Printed music (*Aloha!*, a line and a full page): a picture (`[[image:]]`, crop with the words under the notes); the description gives the words as printed, and is checked on the scan like text.
- “To face p. N” under a plate: not transcribed (the earlier books never kept it; the prompt says so since 2026-11-21). *Argentine Plains* kept 26, and the paragraph a plate interrupts was joined to that line, right-aligned (caught by the rendered look).
- Set `frontispiece` in book.json, with or without a caption (preflight follows moved images since 2026-11-19).
- A plate with a label or sub-captions on separate lines: one `[[caption]]`, parts separated by full stops; several
  `[[caption]]` lines fail preflight `conservation` (it compares caption lines; the compiler joins them) [*Corona and Coronet*, 2026-11-19].
- A folding map shot in two halves: crop each half; try joining them only if the shots overlap (they did not in
  *Corona and Coronet*: a strip at the fold was missing, said in `notes_on_text`).

- A cut at the top of a page with the paragraph from the page before running on under it: the verifier types `[[image]]`, caption, then `[[cont]]` text, which the compiler drops (“[[cont]] not at the top of a page”; *Camps in the Caribbees*: ten pages). Move the picture after the continued paragraph, which is where the editions would put it.

## Trigger: eighteenth-century printing

- Quotations with “ repeated at every line start: models keep the repeats, which then stand mid-sentence once lines
  are joined; `tools/running_quotes.py` after the judge, its list looked at (*Embassy*, 2026-11-20). A listed mark
  just after `[[cont]]` at a page top, inside a quotation still open, is a repeat: *Journal of a Residence* v1 kept two
  as "real opening marks" (fixed in v2, review 2026-11-20). In a book without the convention the list is of real marks
  (*South by West*'s six, checked on the scan at the review).
- Drafts set a page-top continuation of a running-quoted passage as `<blockquote>` (21 pages of *Embassy*); the book
  sets no quotation off, so the compiler found "[[cont]] with nothing to continue". Running marks also stand at the
  start of each row of a quoted table; `running_quotes.py` does not look in tables (*Embassy*, 2026-11-20).
- A leaf taken from another scan (`/page/nN.jpg`): open it at full size before using it. *Western Wanderings* took the plate's blank verso (n141 for n140, from a misread contact sheet), drafted and cached it; the crop subagent found it.
- Scans of old multi-volume sets: the scan check found a missing first page of text and a missing frontispiece
  (UC copy) that IA's own page numbers did not show; another library's scan supplied them page by page.

## Trigger: a carelessly printed book

- *Scouting for Stanley* (1890): 14 printed misprints, 11 of them transposed or dropped letters (“themsleves”, “argeed”, “vegtables”) that neither `misprints` nor `rare-forms` lists; the spot-read's tesseract comparison of every page found them. When preflight lists two or more misprints, ask the spot-read for a full-page tesseract comparison (and a check for such words is a candidate for the next review).
- The tesseract comparison done by script (session of 2026-11-22 21:44): hOCR of every page, the words aligned with the page file (difflib), and listed where tesseract read a word found nowhere in the collection while the file has a common word one or two letters away. *Brown Men and Women*: 80 items, 1 printed misprint (“scentific”) that no check had listed; *Letters from the Far East*: 48 items, 0. Cheap (no model calls); a candidate for a tool with a test at the next review.
- An italic word hyphenated across a page break (`<i>Bagh-</i>` | `<i>dad,</i>`) is not joined: put the hyphen outside the closing tag.

- A misprint split by a line-end hyphen (“disre-|pect”) is silently corrected by the draft, the verifier and the judge alike (*Surface Japan* p. 29); only the spot-read's tesseract comparison found it. “Tranquilty” on the same page was listed by no check (no “tranquility” in the collection to compare with).

## Trigger: broken type

- A damaged corner or edge (*Around the World through Japan* p. 95): draft, verifier, judge and a spot-read all filled the lost words with plausible ones (“away” for *free*, “little” for *shade*); only the two letters typed 〓 showed it. Read such lines from another scan or edition of the same setting (IA OCR text is enough to find the page); otherwise `[[supplied]]`/`[[gap]]`.
- A comma whose tail did not print looks like a full stop; both readers and the judge took "refreshing. and" as printed
  (*Journal of a Residence* p0271); a full stop before a lower-case word is worth a crop (grep `[a-z]\. [a-z]`).
- A letter dropped out of the type leaves a gap at the line start (*Short Leave* p0214 " anguage"): mark it `[[corr]]`
  even inside a quotation of broken English; the gap is the evidence.
- A worn or broken letter (an *n* whose stroke has gone, so it looks like *r*) is read by judges as the letter it looks like (*Asia Minor* p0119 "rame"). Look for the same break elsewhere on the page before calling it a misprint; a broken letter is transcribed as the letter set, not marked `[[corr]]`.

- An opening quotation mark left out in print (a reply set as “guns, They’re dreaming, Sir,”): preflight `quote-balance` lists it; look on the scan and mark `[[corr They’re|“They’re]]` (*Letters from China & Japan*, 2 places).

## Trigger: accented names and foreign words (many diacritics)

- Preflight `accents` lists every word spelled with different accents (or with and without); send the groups to an Opus
  subagent with crops (one leaf of each rarer form): in *Land of the North Wind* 23 groups, 35 pages wrong. A wide circumflex printed over two
  letters ("oû") was read as an acute, grave or breve on one of them; the Sonnet pass and the judge did not settle it.
- Not only foreign words: a speck or blot over a letter of an ordinary word was taken for an accent in four published
  books (“potatoës”, “Dŭrbar”, “gaïshas”); the `accents` list shows them beside the plain form. Read it for every book.

## Trigger: drop capitals at chapter openings

- Drafts type the capitals after a drop capital as small capitals (`T<sc>he</sc>`) on some chapters and as capitals
  on others; in both books so far the print had full capitals. Look at two openings on the scan and make all agree.

## Trigger: a printed contents with chapter summaries

- `[[corr]]` inside a `[[subtitle]]` line is not rendered: the editions showed the markup (*A Land of Mosques*, “Amiranté”, preflight `stray-markup`). Leave a heading as printed, or fix the compiler with a test.
- Drafts type such contents page by page differently (again in *Japan As We Saw It* and *Around the World through Japan*, three layouts in eight pages; the prompt asks for one layout since the review after fifty books: check that it holds): `##` headings and `[[subtitle]]`s on some pages, tables on
  others; and `[[cont]]` lands mid-page after a heading. Make it plain lines as printed (`[[center]]` number and
  title, the topics as a paragraph ending in `<pref>`), drop "PAGE" heads and dot leaders [*South by West*, 2026-11-19].
- A page that starts flush left after a closed sentence is still a continuation (`joins` lists it): look at the indent.

- A head-piece printed above such a half-title goes after the half-title's `#` line, just above the chapter's: before it, it falls into the omitted division and the chapter opens without it (*A Summer in Prairie-Land*: caught by the rendered look).
- A half-title printed above Chapter I on the same leaf: two `#` divisions at one `at`; `n` counts from 1, so the chapter is `"n": 2`. Without it the chapter's `toc_title` went to the half-title, which became a part with every chapter under it (*From West Africa to Palestine*, caught by the rendered look).

## Trigger: no printed contents, chapters without titles

- Numbered sections without titles made pages by `toc_entries`: anchor each entry on the numeral heading (`"starts": "IV"`), not on the first words of the text, or each numeral is left at the end of the page before (*Sunny Australia*, 2026-11-23: caught by the rendered look).

- Contents entries of the editor's: places and dates per chapter, proposed by a Sonnet subagent reading the draft text
  (no scans), checked at each chapter opening, said in `notes_on_text` (*Autumn Tour in Western Persia*, 2026-11-20).

## Trigger: quotations set in the text type

- Letters, reports and newspaper extracts printed in the text type with a little space round them: drafts make some of
  them `<blockquote>` and not others, and a `[[cont]]` at the top of the next page then has nothing to continue (compile
  warning). Look at the scan: same type and measure → plain paragraphs throughout (*Via Rhodesia*, 2026-11-20).

- Quotations in smaller type mixed with dialogue in the text type (yarns told in a smoking room, *Brown Men and Women* ch. II): drafts
  set about a fifth of them as `<blockquote>`. Line pitch tells the sizes apart where the eye cannot on a thumbnail: tesseract
  hOCR of every page (`OMP_THREAD_LIMIT=1`, 6 at a time: 300 pages in ~10 min), the y-step between lines (here 37 px text,
  30 px quotations, 24 px notes at 1800 px), each paragraph matched to its lines by word trigrams. Look at the pages it flags
  on the scan: a whole section set small for space (Reeves ch. X) is the author's text, not a quotation.

- Plate numbers printed under photographs (roman numerals): drafts type them as folios, caption prefixes or lines of their own, inconsistently; strip them by script after the judge (*Yankee on the Yangtze*: 82 plate pages).
- A leaf of text bound inside a paragraph (an unnumbered insert, the Sacred Edict in *Yankee on the Yangtze*): the next page's `[[cont]]` joins the insert's last line. Move the insert's text after the end of the interrupted paragraph and say so in the log (caught by the rendered look).
- Halftones set into the text column: the Sonnet pass moves them to the exact line with `[[cont]]` after the caption, mid-sentence (*Vacation Days*: 34). Move each after the end of its paragraph by script (picture + caption, then join the `[[cont]]` text to the paragraph before).

## Trigger: footnotes

- A table inside a footnote (a ship's log) ends the page as a body block, so the next page's `[[cont]]` has nothing to
  continue: set the table as one line of the note, entries separated by semicolons, and say so (*W.S.W.*, 2026-11-20).

- A note continued over the page arrives as a note with a new mark and no reference: make it `[[fn cont]]`.
- A signature under a note goes inside the note.
- A summary of 80 characters or less goes into the chapter's title (pager, breadcrumb, page title) while longer ones stay
  in `toc_title`, so titles differ in length; with `"toc": {"subtitles": "all"}` the compiler keeps every title short (since 2026-11-21).
- Two marks in the text for one printed note: the second is `[[fnref * again]]` (the compiler warns "has no note" otherwise).

## Trigger: appendices, documents, quoted articles

- Each appendix as `## I. Title` in one Appendix division: `[[subtitle]]` after `##` renders as a plain paragraph.
- Drafts type running heads ("APPENDIX.") as `#` headings on every page: list all `#` lines and delete them.
- Ditto marks in tables: type them as printed (low „ or turned “) in their own cell or place; preflight `spacing` reads a
  “ ditto as a quotation mark (waive the page, after looking), „ passes (*Journal of a Residence*, 2026-11-20).
- Spot-read every table and verse page against the scan: an Opus subagent given the page files and images, reporting
  differences only, did 38 pages in ten minutes and found a printer's error and a wrong join the pipeline had passed.
- Wide tables with blank cells (no dash) among dashed ones: drafts shift whole columns up or down a row (*Embassy* p2658,
  21 columns). Sum each column against the printed total by script, and read the blanks and dashes on a rotated crop.

## Trigger: quotations in another language

- Drafts close up the printed space after an elided Italian article ("l’ affare" → "l’affare") in some places and keep it
  in others (*Journey through the Caucasus*, 3 of about 20): a spot-read on the scan finds them; make them all as printed.

## Trigger: verse and quotations over page breaks

- A stanza that ends at a page foot: drafts put `[[cont]]` on the next page's first stanza, so the editions run two stanzas together (*Twelve Years in Canterbury*): preflight `verse-joins` lists each such join with the stanza lengths; look at every item on the scan.
- `[[cont]]` goes on the first line inside the second block, not before `<blockquote>`.
- A sentence that resumes after a set-off block at a page top must not get `[[cont]]`: it would be joined to
  the paragraph before the block [p2e].

## Trigger: index or in-book page references

- Drafts already tag some numbers: a blanket regex double-wraps them. Do not tag years.
- Set `[[page N]]` to the true number where the folio is misprinted, and say so in the log.

## Trigger: a book about Japan (the JATSI books)

- First one (*Rambles through Japan*, 1892, 2026-11-20): Kioto, Ozaka, Ko-ya-san, jinrikisha, *saké* all kept as
  printed; the only judge spot on such a word (*saké* vs *sakè*) the verifier had right on the crop; audit 30/30, 0
  candidates. Keep cropping every judge spot and audit candidate on a romanized word; Japanese script: none in it
  (`workflow.md` §"Not yet solved").
- Second (*On Short Leave to Japan*, 1894): no romanized word reached the judge; the judge's only wrong call was a
  closing quote the verifier added (p0046). A plate the List of Illustrations places in the text may be bound as the
  frontispiece in every copy: check a second scan before moving it.
- Third (*Cruise in the Mississippi*, 1860): a leaf cut at the edge in the chosen scan is replaced by the other scan's leaf as
  `pNNNNa` (`source.extra_leaves`); preflight `leaves` then counts the cut leaf as done, so no waiver. Dense small type on a
  large page: `--halves` on the draft; Sonnet changed only 3 words in 75 pages and the audit was 30/30.
- A book of letters with a photograph bound before each letter (*Summer Greetings from Japan*): the plate would end the previous
  letter; move the letter's `#` heading onto the plate leaf and say so in `notes_on_text`. Compare the `#` lines of draft and
  judge (`grep -c '^#'`) after the judge: the verifier dropped two letter headings.
- A book that prints two marks for the long vowel (ō and a tilde-like õ, even in the same word): the draft made most õ into ō (*Land of the Tatami*: 8, and the audit found a ninth). Send the `accents` groups and every õ/ō word to a subagent with enlarged crops.
- A long quotation in small type that fills whole pages: drafts set the full pages as body text and the part pages as `<blockquote>` (*Gentle Japs*: 4 pages; the compiler warned “[[cont]] with nothing to continue”). Look at each such warning on the scan.
- Preflight `misprints` lists “iu”: in a Japanese phrase it is a real word (*Gentle Japs* p. 117).
- Marginal decorations on every page (a bamboo frame and figure sketches “after Hokusai”, *Surface Japan*): the draft marks each as `[[image:]]` (158 in 157 pages), inconsistently; remove them after the judge with a script that keeps the plates by leaf, and say so in `notes_on_text` (Tom asked whether to show them: `preferences.md`).
- The year of the journey is often not printed: work it out from weekdays given with dates and from what the
  traveller could use (railways), and say in the summary that it is inferred.

## Trigger: Chinese or Japanese script in the text

- Chinese printed right to left (proverbs at chapter heads, *A Yankee on the Yangtze*, 2026-11-22): stored in reading order. The draft reversed most, the verifier "corrected" some back, and the judge sided both ways: 6 of 24 were left in printed order. Have the spot-read check every line's characters and direction on enlarged crops (it also found 天 typed 大, and a printed 宗 for 崇 to mark `[[corr]]`); say the rule in `notes_on_text`.
- The renderers tag Han and kana runs with `lang` (zh, or ja with kana); the site and EPUB show them with the readers' system fonts (checked in Chromium, 2026-11-22).

## Trigger: Google scan (`…goog` identifiers)

- Bitonal: halftones and many engravings come out blank. Good for supplying a missing leaf's text, not its picture
  (*Rambles* p. 114, 2026-11-20). Its page images are small (767 px wide): upscale to the working height.
- Often bilevel, with folded maps unopened and occasional pages with a hand over the text: the scan check
  must look at every sheet at a size where that would show.

## Trigger: output filter

- "Output blocked by content filtering policy" on a draft page: the refusal follows the page, not the model or
  the time (*South by West* 3 of 413; *Flying Leaves* 5 of 304, refused by Opus twice and by Sonnet). The
  pages are ordinary prose. `tools/ocr_fallback.py` is the route (workflow §2); the tools never retry.
- A session that set out to type such a page itself was ended by the same filter, and every later turn of
  that session failed at once (2026-11-19). Never do it, whoever asks; say why and use the fallback.
- *A Woman’s Trip to Alaska* (2026-11-20): 55 of 224 pages refused (a quarter of the book: ordinary prose about the
  journey, the Tlingit villages and the ship), the most so far; the fallback did all 55 at $0.07 a page and the audit of all
  55 found 273/275 planted errors. A book with many refusals is not a reason to stop: audit every fallback page.
- The corrections pass, the judge and the audit were not refused on those pages.
- *Our Ride through Asia Minor* (2026-11-20): 2 of 418 (p0347–p0348, ruins of Koniah, ordinary prose); the fallback and a 10/10 audit, no other trouble.

## Trigger: OpenRouter

- Check every `log.jsonl` for `finish` other than `stop` (some models' filters truncate silently) [p2e].
- Model names change monthly: read `/api/v1/models` first.

## Environment

- Set shell variables (`slug=…`) in their own command, not in an `a && b && cmd &` chain: the trailing `&` runs the whole chain in a subshell, the variables are lost, and `wip/$slug` became `wip/` (2026-11-22).
- Several tesseract processes at once (subagents' `crop_spot.py`, `ocr_fallback.py`, a bulk run) each take four threads
  and slowed one page to 15 minutes (2026-11-20): `OMP_THREAD_LIMIT=1` and at most four at a time.
- A subagent's reading of a single accent is a claim, not a check: the scan check said “chargè” was printed with a grave, and
  the session wrote it down as printed; a later spot-read found an acute (*Sheepshanks* p0141). Crop every `accents` group yourself or send it with crops.
- A subagent's page map can be one leaf off (*The Eastern Seas*: frontispiece, title and Chapter I each given one leaf late, so the frontispiece was not drafted): open the images of the frontispiece, title page and Chapter I yourself before setting the draft's `--pages`.
- A subagent's report of lost text is checked with `grep` on the page file before anything is re-run (*Land of the
  North Wind* p0317: "11 lines missing" were there; its view of the line was cut).

- CI (`pages.yml`) installs only Pillow before the tests: a test that needs another package must add it there (a test importing `crop_image` broke the deploy on 2026-11-19).
- `sleep` in a foreground command is blocked: run long commands in the background and do other work meanwhile.
- `publish.py` runs preflight again: `export EPUBCHECK_JAR=…` in the same command, or it fails on epubcheck.
- `tools/setup_env.sh` first (it switches apt to https mirrors: plain-http mirrors hang behind the session proxy). It
  takes a few minutes; preflight and the tests need only epubcheck and Pillow, so run it in the background. Headless calls: `claude -p` with only the Read tool (`ocr_claude.py`).
- Drive: uploads from a session are refused above about 3 MB per call (tested 2026-11-19: 2.86 MB went
  through; 9.9 MB and 40 MB did not). Downloads by `curl` with the file id work for any size because the
  folder is shared by link. The connector lists a folder a few files at a time: follow `nextPageToken`.
- www.gutenberg.org answers 503 to scripts; use the catalogue file. The Wikisource API rate-limits.
- IA: one download at a time; a 126 MB page-image zip took 14 seconds.
- `prep_pages.py` on 270 leaves: about a minute on 4 cores; 52 MB at the default size (19 Drive parts).
