# Tom's decisions

## 2026-11-19 (project set-up)

- **Purpose:** a long-term, open-ended public project: highly accurate and readable digital versions of
  first-person nonfiction travel books written and published in English before 1914, given to the public
  domain; a resource for modern readers to discover such books, enjoy them, learn from them and do research.
  No fixed goal; months or years. He will publicise it after a few weeks and may then get a domain name
  (so: relative links everywhere).
- **Selection:** the four conditions in `selection.md`, "for the time being". Books are chosen by Claude,
  usually alone by its own judgement and taste, sometimes after consulting him. Priority: a variety of
  interesting, readable books not easily available except in libraries or scans.
- **Print-on-demand facsimile reprints do not count** as post-1914 editions; real new editions do.
- **Text:** faithful; clear misprints corrected and recorded; line-end hyphenation resolved; illustrations and
  captions included; footnotes linked; **modern conventions for spacing around punctuation**.
- **Licence:** CC0 for everything — texts, JSON, site text, tools, prompts, notes.
- **Models:** Claude models through his subscription. Routine runs on Opus, which may give work to Haiku,
  Sonnet or Opus subagents or headless instances. **Fable only with his explicit permission** (the set-up
  session ran on Fable by his choice). Other companies' models through OpenRouter only for a second opinion on
  difficult scans, **at most $3.00 a day**.
- **Workflow:** starts from the English workflow of his pdf-to-epub project and is improved continuously and
  independently here, including the improvement process itself. That repository is private and is not
  attached to routine sessions: nothing here may depend on it.
- **Revisions:** published books may be revised when errors are found, and redone when a cleaner scan turns
  up, the workflow has improved enough to correct a significant number of errors, or the style rules have
  changed enough that the difference shows.
- **Site:** landing page with the published books and the queue; a page per book (bibliography, brief
  summary, EPUB and ODT downloads, HTML by chapter, link to IA and a page viewer if possible, link to the
  JSON); the JSON is the base of the other formats and holds the parts left out of them; the same text and
  paragraph styles for all books, with additions per book only when needed; shared CSS (and JS only if
  needed); no external dependencies; plain, minimal text with nothing that sounds like publicity; a
  straightforward, accessible, easily navigable, responsive design that does not try to catch the eye.
  Later perhaps: a topical index, other features.
- **Files:** IA files are fetched once and kept in his Google Drive folder "Travel Books" to spare IA's
  servers and the repository; working set in parts of at most 3 MB (the connector's limit).
- **Routine:** a scheduled routine points a session at `RESUME.md`, once or twice a day at first; he adjusts
  the frequency after watching token use — so say what each session cost.

## 2026-11-19 (answers after set-up)

- **Exclude books still in copyright where the term is life plus 70 years** (his example: in copyright until
  2037). Rule as recorded in `selection.md`: every author dead more than 70 years. *A Sportswoman in India*
  (Savory, d. 1966) moved to `rejected`.
- **Regularize the capitalization of titles to upper and lower case** (headings such as CHAPTER IV. →
  Chapter IV.). Recorded in `style.md`; I extended it to chapter summaries and captions printed in capitals
  (assumed).

## 2026-11-19 (later the same day)

- Confirmed: captions and chapter summaries in upper and lower case too; the embedded IA page viewer is fine.
- **Italics:** preserve them in the JSON, but in the built versions render them as roman in long extended
  passages, such as entire paragraphs or tables of contents. Rule and thresholds: `style.md` §Editions.

## 2026-11-19 (answer on the Rajah of Kolhapoor diary)

- **Publish *Diary of the Late Rajah of Kolhapoor*.** And as a standing rule: **a person whose date of death is
  unknown is assumed to have died before the age of 100.** Recorded in `selection.md` rule 5 (with my reading:
  the birth year must still be known or bounded, e.g. from a career; otherwise the book is left out).

## 2026-11-19 (during the South by West session)

- **Skip *South by West* (Rose Kingsley) for the time being, and try it again in the future.** A problem had
  occurred: the output filter refused three pages of the draft. Queue row `waiting`; resume steps in its log.
- **Do not choose books by the author's gender.** The queue has come to have mostly women authors; those books
  can all stay, but from now on choose without preferring any group: the aim is a wide range of authors,
  nationalities and destinations, with no particular ones preferred. Recorded in `selection.md` §"Choosing among
  those that qualify" and in the `select-book` skill.
- **Next session: take the next book from the queue as normal** (asked whether to first look for candidates by
  other kinds of authors, since five of the twelve queued books are by women: no).

## 2026-11-19 (answer on the refused pages; recorded later from the session transcript)

- Asked whether a session may type the pages the output filter refused, Tom answered: **"Yes, try typing those
  pages, both in this book and the previous one that got blocked."** The session that received this died trying
  (the filter ends a session that types such a page), and its note of the answer was never committed. What stands
  from the answer: both *Flying Leaves* and *South by West* are to be finished, not left waiting; their queue rows
  are `in progress` again. How: `tools/ocr_fallback.py`, not typing (CLAUDE.md, the output filter).

## 2026-11-19 (diagnosis of the first routine sessions)

- Tom asked a session (run on Fable by his choice) to look at the day's Opus sessions, find what caused their
  problems and redesign the workflow to avoid them. What was found and changed: `improvement.md` review log.
  Two changes touch rules he set, for him to confirm or reverse (below).

## 2026-11-19 (answers to the three questions of the diagnosis session: yes to all)

- **The checks rule as rewritten stands:** a session may fix a check that is wrong about a kind of book (test with
  invented text first) but does not publish that book; the next session does. (CLAUDE.md.)
- **Pages the output filter refuses may be published from the fallback:** tesseract's reading corrected by Opus,
  then the Sonnet pass, the judge and the audit; the book says which pages in its notes on the text.
- **The death-date rule keeps the added condition:** unknown date of death = died before age 100, provided the
  birth year is known or bounded (e.g. from a career); otherwise the book is left out. (`selection.md` rule 5.)

## 2026-11-19 (tables of contents)

- **Tables of contents are decided book by book.** Basic policy: follow the format of the printed book's contents,
  but deviate from it where the digital version would be easier to read with a different format. The same
  principle applies to the HTML, the EPUB and the ODT. Entries are consistent within a book (his example:
  *Sketches Awheel* gave the chapter number and places for some chapters and only the number for others), and
  neither too many nor too few. Where the print has a single entry for a long text (his example: the body of the
  *Rajah of Kolhapoor* diary), the editions may add entries of the editor's own, such as spans of dates and the
  places visited. How: `workflow.md` stage 4 "Contents", `book-json.md` (`toc`, `toc_entries`).

## 2026-11-19 (Staunton's *Authentic Account of an Embassy … to the Emperor of China*, 1797)

- **Add the three IA items of Sir George Staunton's *An Authentic Account of an Embassy from the King of Great Britain
  to the Emperor of China* (London: G. Nicol, 1797) to the top of the queue**: `authenticaccount01stau` (vol. I),
  `authenticaccount02stau` (vol. II), `gri_33125008481562` (the folio volume of plates, Getty). They are long; several
  sessions may be needed.
- **Combine all three volumes into a single digital volume** (one book; the volumes as parts, the plates placed as the
  book directs or as a section of their own: decide when the plate volume has been looked at).
- **Leave out the marginal titles** (side-notes naming the place etc.) **in the built versions** (HTML, EPUB, ODT); as
  everywhere, the JSON keeps them.
- **An exception to the selection rules, by Tom's choice** ("these books might not meet the guidelines for inclusion
  in this project, but I have enjoyed reading it so we can make an exception"): not to be rejected for a reprint, an
  existing digital text, or for being compiled by Staunton from Macartney's and others' papers rather than a plain
  first-person narrative. The life-plus-70 rule is met (Staunton d. 1801; Macartney d. 1806; Gower d. 1814; the
  engravers and William Alexander, the draughtsman, all died long before 1955).

## 2026-11-20 (answer on running quotation marks, *Embassy to China*)

- **Running quotation marks:** in books where the opening quotation mark of a long quotation is repeated at the start
  of each line (common in 18th-century and earlier books), follow modern practice: keep only the opening and closing
  marks of the whole quotation.
- **Quotations of several paragraphs marked with quotation marks** (not set off by indenting or other formatting):
  follow standard modern practice: an opening mark at the start of each paragraph, a closing mark only at the end
  of the whole quotation.

## 2026-11-20 (answers on the *Embassy to China* assumptions, and text lost in the scan)

- **Confirmed** the session-2 assumptions for *Embassy to China*: engravers' and publishers' lines on plates left out;
  the letters lost at the fold of the coastal-views plate supplied; "pratique-boat" keeps its hyphen; the part title
  "The Folio Volume of Plates".
- **Text lost or obscured in the scan** (a short piece, typically a word or less), when no other scan or edition
  settles it — a standing rule for all books:
  - **cannot be inferred:** the gap is marked, in the JSON and in the built versions (e.g. square brackets);
  - **can be inferred reasonably well from the context:** the JSON marks the gap and says the letters are inferred;
    the built versions show only the inferred letters, with no sign that the scan was unclear or that they were
    guessed — for smooth reading.

## 2026-11-20 (the books of "Japan As They Saw It" join the project; session run on Fable by Tom's choice)

Tom gave a session the Sources page of his earlier project "Japan As They Saw It" (JATSI: descriptions of Japan by
American and British visitors, 1855–1912; 247 books, each with links to its Internet Archive scans). JATSI was
an initial inspiration for Travel Books. His instructions:

- **The JATSI books are to be added to Travel Books gradually, one at a time, at about one JATSI book for every
  three books added to the project.**
- **Say which books came from JATSI**, on the site, so that people who come across it know why the project will
  have a growing imbalance towards books about Japan (the imbalance itself is fine).
- **A separate, stored list of all the JATSI books** (bibliographic information and IA links). From it, a dozen or
  so **that meet most or all of the project's criteria** go into the main queue shown on the home page.
- **Non-JATSI books** are chosen for the queue by the policies already established.
- **The text policy is the same** for JATSI and non-JATSI books.
- Notes where appropriate that Tom Gally decided to add the JATSI books gradually.
- The same session: assess the state of the project and its workflows, improve where needed, and plan how the
  landing page is organized as the number of books grows. That session does not do the routine work of
  `RESUME.md`; the normal run resumes in the next session, on Opus as usual.

How this was carried out: `notes/jatsi.md`.

## 2026-11-20 (answers on the JATSI questions, and on links)

- **Links.** Wherever the project "Japan As They Saw It" is mentioned on the site, the name links to
  <https://www.gally.net/jatsi/index.html>. **Every link to an outside page (IA and all others) opens in a new
  tab or window; only links within the site stay in the same one.**
- **The pace is as understood:** JATSI, other, other.
- **JATSI books already on Project Gutenberg will be added eventually, digitized afresh by this project** (Gutenberg's
  data is not used). They can have lower priority than the others.
- **The non-narrative JATSI books also have lower priority.**
- **Round-the-world books with a short Japan section are treated like any other book of this project:** if they meet
  the project's criteria in other ways they are queued with normal priority (and marked as JATSI); if they do not
  meet the general criteria, lower priority, still to be done eventually.
- **The JATSI books are exempt from the 70-year rule** ("they should all be in the public domain in the US and Japan,
  and I want to be able to add links to our new digitized versions from the JATSI Sources page sooner rather than later").
- **The Thompson drawing is to be added to *Corona and Coronet*.** (So: a minor illustrator whose death date is not
  found does not keep a drawing out.) **The Sheldon book is exempt too** (its two-page introductory letter by Anna
  C. Hartshorne, d. 1957) and goes in the queue as appropriate.
- **The pace of the regular sessions may be picked up**, depending on how many tokens the project uses and on the
  models' efficiency in the months ahead: "I hope that the maturation of this project will not be 'years away'."
  (So nothing in the notes should plan on the lower-priority JATSI books being far off.)

## 2026-11-20 (answer on decorative head-pieces and tail-pieces)

- **Include the decorative head-pieces and tail-pieces as small images in the built versions** (asked after
  *Rambles through Japan* left them out). A standing rule for all books: ornaments printed at chapter openings and
  ends are cropped and shown small, not left out. *Rambles through Japan* gets them in a new version.

## 2026-11-20 (longer sessions; session run on Fable by Tom's choice)

- **Each routine session is to run longer: more than one book per session where possible, up to a reasonable
  fraction of the context window.** ("This project seems to be going ahead smoothly now.") `RESUME.md` and the
  other files are to make such sessions normal.
- He will run the new `RESUME.md` by hand a few times to see how much clock time a session takes, and then set the
  routine's interval so that sessions do not overlap and cause merge conflicts — so every session says when it
  started and ended (`notes/sessions.md`, and the final message).
- The routine sessions stay on **Opus 5.5**.

How this was carried out: `RESUME.md` §"How long a session runs", `tools/session_meter.py`, `improvement.md` review log.

## 2026-11-20 (answer on texts in databases)

- **Books whose text is in a subscription library database are eligible** (his answer on *A Woman's Trip to Alaska*, whose
  text is in Alexander Street's "North American Women's Letters and Diaries"). **So are books in online databases such as
  EEBO and ECCO whose texts are not formatted for immersive reading.** "Please revise the guidelines accordingly."
  How: `selection.md` rule 2.

## 2026-11-20 (display settings for the book text pages)

- Tom asked what controls could be added to the HTML pages of the book texts so that readers can set how the text
  is shown (font, size, weight, light/dark, colours, line height, justification, margins, pagination, animated
  scrolling or page turning), saved in the browser for all book pages (not necessarily the index pages).
- **Conditions for any such feature:** no external dependencies; falls back gracefully when JavaScript is blocked;
  an unobtrusive interface; no problems for readers using screen readers or other assistive devices or plugins.

- **Decided (same day): build them.** Font size, line height, justification, column width, serif / sans serif /
  browser default, letter spacing, word spacing, paragraph style, hiding the dotted underline on corrections,
  remembering the reader's place in the book, and a setting to turn the underlining of links on and off
  **throughout the site**. **No hosted fonts** (so no named fonts and no font weight). **Preset themes only** for
  colours. **No pagination and no scrolling settings for now.** **The light/dark choice applies to the entire site.**
- **The interface:** a "Display" button in the upper right-hand corner of the chapter pages, to the right of the
  About link. The settings menu has two levels, basic and advanced. Controls simple and self-explanatory,
  "avoiding words if possible (though having text appear as popovers for nontouch interfaces)".
- He will check the result after it is merged and get back.

- **After seeing it (same day):** the Display button goes on **all of the index pages as well**, and the settings
  apply to those pages similarly. **When the font size is changed, the title and navigation text in the page headers
  change too** ("a person with inhibited vision who sets the reading print size very large would have trouble reading
  the still-small navigation text"), **but only up to level 6 of the 9 sizes**: at sizes 7, 8 and 9 the header stays
  at level 6.

- **"Everything works."** One more change (same day): **on `about.html`, use series commas and curly apostrophes.**

- **The label of a JATSI book in the lists** (same day): in the book descriptions on all pages, "from Japan As They
  Saw It" becomes "**JATSI**" (still linked to his project) and "(about these books)" becomes "(**about**)" (still
  linked to this site's page).

- **On `japan-as-they-saw-it.html` the book descriptions have neither link** ("JATSI", "(about)"): they are
  redundant on that page (same day).

## 2026-11-21 (interface: JATSI wording and a reading bar; a session with Claude Fable, by Tom's choice)

- Tom ran this session with Claude Fable himself ("this special Fable session"), for changes to the interface and
  the site text only. The rule against Fable for the books stands.
- **Home page:** "a list of books about Japan that is being added to this site a book at a time" becomes "a list of
  books about Japan that are being added to this site one at a time."
- **The mark of a JATSI book in the lists** is now "**(JATSI)**", the word JATSI linked to
  `japan-as-they-saw-it.html` (before: "JATSI (about)", the word linked to his project).
- **`japan-as-they-saw-it.html` begins** "Japan As They Saw It (JATSI) is an earlier project of Tom Gally": the link
  to his site on the words "Japan As They Saw It" only, not on "(JATSI)".
- **A bar at the top of the chapter pages** (the pages with the text of a book; not the index pages), unobtrusive,
  which appears when the reader scrolls down. No words, only simple icons: on the far left, to the book's own
  page, at the top of its table of contents; in the middle, left and right arrows to the previous and next
  chapter; on the right, the Display settings, so that they can be changed while scrolled down in a page. With
  "Remember my place in each book" on, **the place in each chapter is remembered**, so that going to the next
  chapter and coming back returns to where the reader was. **A setting in the Display panel shows or hides the bar
  on all pages.**

- **After seeing the bar (same day):** when the bar is in view and the reader goes to the previous or next chapter by
  its arrows, the chapter that appears is scrolled either to just above its title or to the reader's earlier place
  in it, and **the bar stays in view**, so that the controls are visible and in the same position.

## 2026-11-21 (a logo and favicon)

- **The site has a logo and favicon: a stack of three books** (candidate 19 of twenty Tom was shown; the
  proposals are in the project files, `logo-proposals/`). One SVG, in the site's own ink and link blue, used as
  the favicon of every page and beside "Travel Books" in the header of every page. It follows the reader's
  light, sepia and dark setting.

## 2026-11-21 (header and navigation simplified)

- **The logo and "Travel Books" in the header are the link to the home page from every page.** The breadcrumb
  line therefore no longer begins "Travel Books ›": on chapter pages it begins with the book's title, and it does
  **not appear at all** on the book index pages, About, the Books page or the JATSI page.
- **"Display" in the header is replaced by the settings icon of the chapter bar**, on all pages, and it is in
  exactly the same position at the top of the page and in the bar when scrolled down, so that it seems fixed.
- **The left-most icon of the chapter bar opens a drop-down menu** (a new simple icon, designed by Claude) of
  three lines: (1) the site logo and "Travel Books" → the home page; (2) an open-book icon and the title of the
  book → the book's index page; a title too long for the menu (mobile) fades out over its last few letters at
  the right edge; (3) the three-line icon and "Contents" → the table of contents on the book's index page.
- **On a book's index page the picture of the cover or title page is a link** to the same page as "Read on this
  site", which stays as it is.
- **A new page "Books"** has the "Books" and "In the queue" sections that were on the home page; "Books" in
  every header links to it. The home page is the header, the title, the two paragraphs and the footer.
- The footer (public domain, report an error) stays on all pages.
- **In the lists of books "(JATSI)" becomes "JATSI"**, without parentheses, linked as before.
- **Less space between a decorative banner above a chapter title and the title** (e.g. *A Yachting Cruise in the
  South Seas*): there was too much.

- **Later the same day, the home page's second paragraph ends:** "Books are also being added from the project
  Japan As They Saw It, so the site has more books about Japan than about other countries." — the name linked
  to `japan-as-they-saw-it.html` on this site (not, here, to his project's own site), in place of "Others come
  from … (about these books); for that reason …".

## 2026-11-21 (a carousel of book covers on the home page; a session with Claude Fable, by Tom's choice)

- **The home page gets a carousel of thumbnails** of the covers or title pages of most or all of the books, to show
  people who happen upon the page a selection of what is on the site. It stands below the header and above the
  title "Travel Books".
- **Random order, shuffled each time the page loads.** Three to five thumbnails are in view, depending on the
  width of the window.
- **Unobtrusive arrows at the left and right sides**; a click scrolls that way and reveals more books. On tablets
  and phones the reader swipes. **Either way the action reveals as many books as were in view and then stops**: the
  scrolling does not go on indefinitely.
- **A click on a book goes to the book's index page.**
- **The picture is the cover if the title is clearly readable on it, otherwise the title page.** A book with
  neither a cover nor a title page with a readable title is not in the carousel.
- **Titles are text only for screen readers**, not visible.
- **The books in the carousel and their thumbnails are brought up to date once every five sessions**, when the
  other maintenance tasks are run.
- **Design: plain and simple, no borders**; the books and the arrows look as though they float slightly above the
  page, with faint shadows. **The motion is smooth, with gradual acceleration and deceleration.**
- **Later the same day, after trying it** (it works in Chrome and Firefox on the Mac and in Safari on the Mac and
  iOS):
  - **No arrows on smartphones and tablets**: readers will notice that they can swipe.
  - **On the desktop the arrows' disks are about 30% more transparent.**
  - **The carousel is continuous on every platform**: it does not end at the last book in either direction; the
    sequence goes on from the beginning. The desktop arrows are therefore always in view.
  - **The picture on a book's index page is the same as the one in the carousel** (they differed for *An Autumn Tour
    in Western Persia*, for example). **For the index pages, retroactively and from now on, the picture is chosen by
    the carousel's rule: the title must be readable** (the cover if it is, otherwise the title page).
  - **A future book with no cover or title page with a readable title: the first page of the first chapter, or a
    similar representative page, for both the index page and the carousel.** (This replaces "is not in the
    carousel" above.)

## 2026-11-21 (answer on *Uganda for a Holiday*)

- **Yes: *Uganda for a Holiday* (Treves, 1910) can be published without its folding map**, which is in neither IA
  scan. The book says that the map is missing from the scans (`notes_on_text`).

## 2026-11-22 (seven changes to the editions and the site; a session with Claude Fable, by Tom's choice)

Tom turned the routine off for this session; later scheduled sessions are Opus as before. What is not finished
goes to the to-do list for those sessions (`RESUME.md`).

1. **A body text without chapter divisions is divided into sections of suitable length, each with a suitable
   title and each a separate web page** (his example: the *Rajah of Kolhapoor* diary, a single chapter, hard to
   navigate on one page; the contents on the book's page already had such entries). The division applies to the
   web, EPUB and ODT versions. **The JSON keeps the original structure** and records the divisions made later.
2. **The picture on a book's index page links to the start of the narrative**: the first chapter, or the first
   page of the body text, not a preface, introduction or dedication; the page is scrolled so that "Chapter I"
   (or whatever it is) is the first line. Retroactively and from now on. **"Read on this site (contents below)"
   stays the link to the first page of the book** (which becomes the title page: 5).
3. **Home page:** after "Each can be read on this site or downloaded as EPUB, ODT or JSON." comes "The site now
   contains XX books, with more being added every day." (XX is always the number on the Books page.) "About the
   project." becomes "More about the project.", a new paragraph below the one ending "…about Japan than about
   other countries." The heading "Travel Books" below the carousel is removed (the name is in the header).
4. **Text written by Claude for the site uses serial commas and curly apostrophes and quotation marks** (not in
   code excerpts, such as on the page about the JSON format). All present pages fixed, the About page and every
   book summary included; the convention holds from now on.
5. **The title page is transcribed in the web, EPUB and ODT versions of every book, as the first page of the
   book**: the full title, the author's name if it is there, the publisher, the city and so on, as printed;
   elements centred on the title page are centred. Readers expect a book to begin with its title page, not a
   preface. **Anything before the title page (half-title, advertisements) stays out of the built versions.**
6. **A paragraph after an illustration is indented if the scan indents it** (his example: "In the Banda Oriental
   there is a fixed maximum amount…" in *Zephyrus* was flush left). Paragraph indents follow the scan unless there
   is a good reason not to.
7. **The routine's wind-down threshold** (40% of the context) may be raised to 50% or 60% if Opus's accuracy is
   in no danger.

## 2026-11-22 (answer on books whose only scan lacks a map)

- **A book may be published when the only thing missing from its scan is a map** (a folding map not opened, or absent): the book page says so in `notes_on_text`. (Asked after *Try Cracow and the Carpathians*; so *Wanderings & Wonderings*, Aubertin, JATSI 89, may be queued.)
- **Other books that would qualify except for one or two missing elements like that: ask Tom whether an exception should be granted**, case by case (record the question here and set the book aside meanwhile).

## 2026-11-22 (answers on *Through Atolls and Islands* and *Surface Japan*)

- **Moss, *Through Atolls and Islands*: yes, publish it** with the pages from the second scan; **if the truncated appendix page would seem strange, leave that appendix out completely** (said in `notes_on_text`).
- ***Surface Japan*: show only a typical page or two with the bamboo border and the marginal sketches, as an illustration near the beginning of the book, with a caption explaining them.** (The sketches are not otherwise shown.)

## 2026-11-23 (answer on *A British Officer in the Balkans*)

- **Publish Henderson's *A British Officer in the Balkans* in the next session, with the photographs** (taken by Mrs. Henderson, whose dates are unknown). The missing map is said in `notes_on_text`.

## Questions for Tom

- **Side-notes that date the entries of a letter or diary** (*Letters from Southern India & Ceylon*, Williams, 1877; 2026-11-22). The book prints
  the place and date of each new entry within a letter in the margin (“Poona, Friday, 8th Dec.”, about 30 of them). By the standing rule (from
  *Embassy to China*: side-notes are left out of the reading editions) they are in the JSON only, so the reading editions lose the dates of the
  entries; the book page says so. Should such side-notes be shown in the editions (for example as a small line or a run-in date at the start of
  the paragraph), for this book and others like it? Assumed for now: the standing rule; a new version can show them.
