# Ideas for enhancements

A list of possible improvements to the site and the editions, for Tom and for later sessions. Written 2026-11-23
from a brainstorming conversation with Tom, from ideas already in `notes/` (cited), and from a look at the site as
built that day (77 books). **Nothing here is decided.** When Tom decides on an item, the decision goes in
`notes/preferences.md` as usual, and the item here is marked accordingly or removed.

**Assumptions (Tom, 2026-11-23):** the site stays on GitHub Pages, built by GitHub Actions from this repository.
There is no database server, no sign-in, and nothing loaded from outside the site (the standing rule: no web fonts,
scripts, trackers or CDNs; the only outside content is links to IA and the optional IA viewer). Scripts stay in
`site/assets/site.js` or files like it, and the site keeps working without them. Anything that needs a reader's
data lives in that reader's browser.

**Difficulty:**

| Rating | Meaning |
|---|---|
| **1 Easy** | a few hours of one session: a builder change or a few dozen lines of script, with tests |
| **2 Moderate** | about one session: new code in the builders or `site.js`, new tests, a look in the browser |
| **3 Hard** | several sessions, or new data to make for every book |
| **4 Very hard** | a project of its own; new data, made and checked by models, for every book |

**Ongoing cost** says whether an item adds work to every future book (the pipeline) or is done once.

---

## 0. Urgent: the size of the site

**Done in part (Tom, 2026-11-23):** every picture reduced to at most 1000 px, quality 75 (726 MB → 267 MB); the
built site is now **869 MB** (EPUB 267 MB, ODT 260 MB). Still close to 1 GB and growing about 11 MB a book, so
0.1 below will be needed before long. A new single-commit repository is to replace this one so that the old
pictures leave the history.

**The built site is about 2.2 GB** (measured 2026-11-23: EPUBs 702 MB, ODTs 683 MB, the rest mostly the same pictures
in the HTML). GitHub documents a **1 GB limit for a published Pages site** and recommends source repositories under
1 GB. Here, `books/` is 798 MB (697 MB of it images) and `.git` is 750 MB. Deploys still succeed, but an Actions log
elsewhere shows "Uploaded artifact size … exceeds the allowed size of 1 GB" with a warning that deployment might
fail, and an unofficial hard limit of about 10 GB is reported. Each new book adds about 25–30 MB to the site, so
at about 350 books the site would reach that 10 GB too. Deploys also time out after 10 minutes (the build takes
about 1 minute now). Sources: [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

Ways to shrink it, which can be combined:

- **Smaller pictures in the EPUB and ODT** (Moderate, done once). For example, at most 1600 px on the long side
  and JPEG quality about 80, so a phone reader gets a file of a few MB. *Pros:* probably halves the site; smaller
  downloads for readers. *Cons:* plates lose detail; folding maps (§2.6) need the full size somewhere.
- **EPUB and ODT as GitHub Release files** instead of files on the site (Moderate, done once, plus a step in
  `publish.py`). Releases are still GitHub, not an outside service, allow files up to 2 GB each, and have no
  documented total. *Pros:* the site drops to well under 1 GB. *Cons:* the download links point to
  `github.com/…/releases/…` rather than the site; every new version means a new release file; it adds a GitHub
  API step to publishing.
- **Smaller pictures on the web pages**, with a link to the full size (Easy to Moderate). Use `srcset` with a
  column-width picture and the full one beside it. *Pros:* faster pages on phones. *Cons:* by itself it adds files
  rather than removing them.
- **Keep only one copy of each picture in the repository, at a fixed size** (Moderate). `books/*/images` is part
  of the git history, so every re-crop is kept forever. *Pros:* slower growth of `.git`. *Cons:* the history
  already holds what it holds; rewriting it is not an option on a public repository others may have cloned.
- **Add a size check to CI** (Easy). The build reports the size of `_site/` and fails, or warns, above a set limit.
  *Pros:* the next size problem is seen before a deploy fails. *Cons:* none worth mentioning.

### 0.1 Hosting files in other repositories (Tom, 2026-11-23: "we do that for my jedict-1 project's audio files")

**How:** one or more extra repositories, each with its own GitHub Pages site (for example `travel-books-files-1`,
`travel-books-files-2`), holding the EPUBs, ODTs and, if needed, the pictures; the book pages link to them.
**Moderate**, done once, plus a line per book recording which repository holds it.

- **Each repository's Pages site has its own 1 GB limit**, so the files can be divided among several, a fixed set of
  books in each (say 40–50), recorded once per book (in `book.json` or a data file) so that links never move.
- **They share the address `tkgally.github.io`.** To the browser a picture at `tkgally.github.io/travel-books-files-1/…`
  comes from the same site as the book pages: nothing is loaded from outside, and offline reading (2.1) and the
  Library (§1) still work. Whether this counts as an "outside dependency" under the standing rule is Tom's decision
  (to go in `notes/preferences.md`).
- **The extra repositories need not hold copies of the books.** travel-books is public and its build is
  deterministic, so each files repository can have its own small workflow that checks out travel-books on a
  schedule (say hourly), builds only its share of the files, and deploys them. No token passes between
  repositories. Alternatively the main build triggers it at once, which needs one token set up by Tom.

**Size, measured 2026-11-23:** EPUB and ODT about 1.4 GB (about 18 MB a book); web pages and their pictures about
0.8 GB (about 10 MB a book). **Moving only the EPUBs and ODTs is not enough:** the main site would fall to about
0.8 GB and pass 1 GB again after about 20 more books. The pictures on the web pages must move too, or shrink (or the
main site keeps column-width pictures and the full-size ones go to the files repositories).

*Pros:* removes the size limit for a long time; readers see no difference; no outside service. *Cons:*

- **Delay:** after a new version, the book page can link to a new EPUB before the files repository has rebuilt (up
  to an hour on a schedule). A version number in the file name avoids wrong files, but the newest one is missing
  for a while.
- **The source repository still grows:** moving built files does not change the 700 MB of images in `books/` or the
  git history. If that becomes a problem, the source images too would move to a separate repository that the build
  checks out — a larger change.
- **GitHub's terms:** Pages is meant for websites, not mainly as free file hosting, and dividing one site among
  repositories to stay under its size limit is a grey area. Releases (above) are plainly meant for distributing
  files, which is a reason to prefer them at least for the EPUBs and ODTs.
- **Not suitable:** raw files from `raw.githubusercontent.com` (not meant for hosting a site; rate-limited) or a CDN
  such as jsDelivr (an outside dependency).

Recommendation: the size check and smaller pictures in the EPUB and ODT first; then move the EPUBs and ODTs to
Releases or to files repositories (0.1); then decide about the web pictures from how fast the main site grows.

---

## 1. A personal Library in the browser

From the conversation of 2026-11-23. `site.js` already keeps display settings and the reader's place in up to 100
books in `localStorage` (`tb-display`, `tb-place`). The Library would build on that.

### 1.1 Shelves — **Moderate**, done once
"Save this book" on each book's page, with shelves such as "To read", "Reading" and "Finished", and shelves the
reader names; a `library.html` page that the script fills in.
*Pros:* useful to regular readers; nothing leaves the browser. *Cons:* the data is lost with cleared site data,
in private windows, and in another browser; see 1.6.

### 1.2 Bookmarks with labels — **Moderate**, done once
Several per book. Each is stored as the chapter file, the block index (as the place is now), the nearest printed
page (`pg-N` ids already exist) and a few words of text, so that it can be found again after a new version of the
book moves things.
*Pros:* the most-asked-for reading feature in e-readers. *Cons:* finding a place again after a revision needs
care and tests with an invented book that changes between versions.

### 1.3 Notes — **Moderate**, done once
Attached to a bookmark or to a selected passage; listed on the Library page; exported as plain text or Markdown.
*Pros:* useful for students and researchers. *Cons:* readers may lose notes they care about; the export (1.5)
is a must, not an extra.

### 1.4 Highlights — **Hard**, done once
Coloured marks on selected text. *Pros:* familiar from e-readers. *Cons:* drawing marks over text that the
reader can restyle (size, width, font) and finding the text again after revisions is the hardest part of the
Library; leave until the rest has been used.

### 1.5 Export and import, with merging — **Moderate**, done once
"Save my library" downloads a small JSON file; "Load a library" merges it (each item with a timestamp; deletions
recorded so they carry over). Kept in iCloud Drive, Dropbox or Google Drive, the file gives manual sync.
*Pros:* works in every browser; no accounts; the site never sees the data. *Cons:* the reader has to do it.

### 1.6 Other ways to sync between browsers
- **A link or QR code** holding the compressed library in the part after `#` (never sent to the server):
  **Moderate**. *Pros:* quick to move shelves and bookmarks from computer to phone. *Cons:* too long for many
  notes; a QR code generator has to be written into `site.js` (no outside library).
- **Writing to a file in a synced folder automatically** (File System Access API): **Moderate**. *Cons:* Chrome and
  Edge on a computer only.
- **"Copy link to this passage"** so that the browser's own bookmarks, which sync between devices, do the work: see
  2.3.
- **True automatic sync** needs a store outside the reader's browser: the reader's own GitHub Gist, Google Drive,
  WebDAV, or a server for the project. **Outside the assumptions above**: listed in §9.

### 1.7 Things to know before building the Library
- **Safari** (and every browser on iPhone and iPad) may delete data a site saved through scripts after about **7
  days without a visit**, unless the site is added to the Home Screen (see 2.1). `navigator.storage.persist()`
  helps in some browsers.
- **A change of address** (for example to a domain of the site's own) leaves everything saved at the old address.
  Decide the long-term address before the Library is launched.
- All of Tom's GitHub Pages projects share the address `tkgally.github.io` and so the storage; keys keep the
  `tb-` prefix.

---

## 2. Reading on the site

### 2.1 Offline reading and "add to Home Screen" — **Moderate**, done once
A web-app manifest and a service worker (both plain files on the site): "Keep this book for offline reading"
stores its chapters and pictures in the browser.
*Pros:* reading on planes and trains; on Safari, a Home Screen site keeps its saved data (1.7). *Cons:* a service
worker that caches badly can show readers stale pages after a new version; it needs a version scheme and tests;
caching a whole book with plates can take tens of MB on a phone.

### 2.2 "Continue reading" — **Easy**, done once
The book's page shows "You were reading: Chapter 5" and the home or Books page lists the last few books opened, all
from the place `site.js` already stores. *Pros:* small, and builds on what exists. *Cons:* a book page that differs
from one reader to another (only for readers whose browser runs the script).

### 2.3 Links to a passage, and copying with a citation — **Easy to Moderate**, done once
Stable anchors for paragraphs (for example by printed page and paragraph: `#p37-2`), a "copy link" action, and
selected text copied with the book, page and URL after it.
*Pros:* readers can cite and share exact places; the browser's own synced bookmarks become useful. *Cons:* anchors
must survive new versions (by printed page they mostly do); one more control in a plain interface.

### 2.4 The scan beside the text — **Moderate**, done once
Page numbers already link to the leaf at IA. On a wide screen, a panel shows the scan of the page being read (the
IA image URL for that leaf, loaded only when asked, like the viewer now).
*Pros:* readers can check the text themselves; shows how the edition was made. *Cons:* depends on IA being up; IA's
image URLs are not a documented API and could change; it must stay optional and closed by default.

### 2.5 Whole book on one page — **Easy**, done once
An extra HTML file per book with every chapter, for printing, for the browser's find-in-page, and for "save page".
*Pros:* simple; helps readers who search inside a book (Ctrl-F works only within a chapter now). *Cons:* a large
page for long books; one more file per book (small: text only, pictures shared).

### 2.6 Large plates and folding maps at full size — **Moderate**, done once
`workflow.md` §"Not yet solved": a large map is shown at the column width, where its names cannot be read, and the
editions do not link a picture to its full-size file. A link from each picture to the full size, and a simple
zoom-and-pan view written in `site.js`.
*Pros:* maps become usable. *Cons:* pulls against §0 (keeping the full size); maps scanned in sections need joining.

### 2.7 Read aloud — **Moderate**, done once
The browser's own speech (`speechSynthesis`) reads from the reader's place, with play and pause in the chapter
bar. *Pros:* no outside service; helps readers with low vision or who listen. *Cons:* voices vary by browser and
some are poor; old spellings and foreign words are read badly; screen-reader users already have this.

### 2.8 Footnotes in place — **Easy**, done once
Footnote numbers open the note in a small box beside the text instead of jumping to the end of the chapter. *Pros:*
easier to read. *Cons:* must stay accessible (focus, Escape, screen readers); a setting may be needed for readers
who prefer the jump.

### 2.9 Keyboard shortcuts — **Easy**, done once
Left and right arrow keys (or `[` and `]`) for the previous and next chapter, as in the bar. *Pros:* quick. *Cons:*
must not clash with keys used by screen readers and the browser.

### 2.10 Printing — **Easy**, done once
A print stylesheet for chapter pages (`site.css` has one `@media print` rule now): no header, bar or buttons; page
numbers of the book in the margin if shown. *Pros:* cheap. *Cons:* none worth mentioning.

### 2.11 Pagination or page turning — **Hard**, done once
Tom asked about it on 2026-11-20 and decided "no pagination and no scrolling settings for now". Listed only so the
decision is not forgotten. *Cons:* hard to do well with the display settings; screen readers dislike it.

### 2.12 Showing side-notes and dates in the text — **Moderate**, policy first
`preferences.md` §"Questions for Tom": the side-notes that date entries in *Letters from Southern India & Ceylon*
are in the JSON only. A way to show them in the editions (a small run-in line) would serve such books.
*Pros:* the reader gets the dates. *Cons:* a change to a standing rule; earlier books may need new versions.

---

## 3. Finding books

### 3.1 Search — **Moderate** (titles and authors: **Easy**)
`notes/site.md`: "Consider a search box only if Tom asks: it needs a script and an index file." Titles, authors and
places: a small index built with the site. Full text: an index split into many small files (one per word range or
per book), written by the builder; no outside library.
*Pros:* the most direct way into a large collection; finds a name across all books. *Cons:* a full-text index for
hundreds of books is tens of MB (pulls against §0); old spellings need some care; a script the site does not have
yet.

### 3.2 Related books on each book's page — **Easy**, done once
"Other books on the same part of the world" and "other journeys of the same decade", from `regions` and `period`.
*Pros:* cheap, no new data. *Cons:* the lists grow long for East Asia (JATSI): show a few with a link to the list.

### 3.3 A topical (subject) index — **Hard**, ongoing
Tom, 2026-11-19: "later perhaps a topical index". `notes/site.md`: `subjects` in `book.json` is free text and would
first need a fixed list of terms, as `regions` has in `data/places.json`. Possible terms: mountaineering, cycling,
missions, sea voyages, hunting, rail, women travellers' accounts, and so on.
*Pros:* a way in for readers who care about a kind of journey, not a place. *Cons:* every book needs terms chosen
and checked; the list of terms needs Tom's approval.

### 3.4 Pages as the collection grows — **Easy**, planned
`notes/site.md` §Stages: `queue.html` when the queue passes about 25 rows; countries as sub-headings for a part of
the world with more than about 40 books (East Asia first); perhaps one page per part of the world; `authors.html`
once the Books page no longer lists every book. *Pros:* already planned. *Cons:* none.

### 3.5 A map of the world — **Moderate**, done once
An SVG world map drawn at build time (no map tiles), each part of the world shaded by its number of books and linked
to `places.html`. *Pros:* a quick picture of the collection. *Cons:* the outline data must be public domain (Natural
Earth is) and kept small; a map adds little for readers using screen readers, so the lists stay the main way.

### 3.6 Routes of journeys — **Very hard**, ongoing
Each book's places in order, plotted on a map. *Pros:* striking and useful. *Cons:* every book needs its places
extracted, put in order and given coordinates, and old place names identified; a lot of checking.

### 3.7 A timeline — **Moderate**, done once
The journeys drawn as bars by year (from `period`), linked to the books. *Pros:* shows the spread of the collection.
*Cons:* `dates.html` already does most of this as a list.

### 3.8 A feed of new books and versions — **Easy**, done once
An Atom file built from `data/published.json`. `notes/site.md`: "Not planned until a reader or Tom asks." *Pros:*
readers can follow the site without email lists. *Cons:* few people use feed readers now.

### 3.9 A random book or passage — **Easy**, done once
*Pros:* a light way to browse. *Cons:* a passage at random may be dull or offensive out of context.

### 3.10 Covers in the lists — **Easy**, done once
`notes/site.md` lists this as not planned: it would make the Books page heavy and harder to scan. Listed so the
reasoning is not lost.

### 3.11 Pages about the authors — **Moderate**, ongoing
Dates, the other books by the author on the site, and the evidence of the death date already gathered for the
70-year rule. *Pros:* the facts are already checked. *Cons:* a biography beyond dates is new writing and needs
sources; most authors have one book here.

### 3.12 A page of numbers about the collection — **Easy**, done once
Books by decade, by part of the world, pages and words in all, JATSI share, and errors found after publication. In
plain tables, from data the site already has. *Pros:* honest and cheap. *Cons:* none worth mentioning.

### 3.13 Search engines and link previews — **Easy**, done once
A `sitemap.xml`, a `<link rel="canonical">`, a short description in each page's `<meta>`, schema.org `Book` data,
and Open Graph tags so that a link shared elsewhere shows the title and cover. None exist now (checked 2026-11-23).
*Pros:* how most readers would find a book. *Cons:* none worth mentioning; no outside service involved.

### 3.14 A "page not found" page — **Easy**, done once
A plain `404.html` with links to the lists. *Pros:* readers following an old link are not lost. *Cons:* none.

---

## 4. Researchers and reuse

### 4.1 Citation details — **Easy**, done once
"Cite this edition" on each book's page: a plain citation, BibTeX and RIS, with the version and a link to that
version. *Pros:* scholars use the editions properly. *Cons:* none worth mentioning.

### 4.2 Plain text and Markdown downloads — **Easy**, done once
From the book JSON. *Pros:* for corpus work and for readers on simple devices. *Cons:* more files (small).

### 4.3 TEI XML — **Moderate**, done once
The standard format in the digital humanities; the JSON already holds what TEI needs (pages, corrections with the
printed reading, notes, side-notes). *Pros:* makes the editions usable in research projects and repositories.
*Cons:* TEI is large; a validator in CI means Java or a schema tool in the build.

### 4.4 The whole collection in one download — **Easy**, done once
All books' JSON (or text) in one ZIP, made at build time. *Pros:* for researchers. *Cons:* adds to §0 unless it is
text only or a Release file.

### 4.5 Version history per book — **Easy**, done once
What changed between versions, from the logs and the corrections list; perhaps a list of changed passages. *Pros:*
shows the work of correction. *Cons:* the logs are written for Claude, not readers; a reader's summary needs a
line in `publish.py`.

### 4.6 Accuracy on each book's page — **Easy**, done once
"Audit: N pages checked against the scan with deliberate errors added; M of M found; K errors reported since
publication", from the audit result in each log and `notes/errata.md`. *Pros:* the site's claim is accuracy; this
states what was checked. *Cons:* the numbers must be read correctly from the logs (they are not yet in
`book.json`).

### 4.7 Indexes of people and places in each book — **Very hard**, ongoing
Most old travel books have no index or a poor one. Drafted by a model, checked against the text. *Pros:* real added
value. *Cons:* editorial work beyond transcription; errors in it would be the project's own, not the author's.

### 4.8 Old and modern place names — **Hard**, ongoing
A list per book (or for the collection) such as Formosa → Taiwan, Yedo → Tokyo, Batavia → Jakarta. *Pros:* helps
readers. *Cons:* new editorial content; identifications can be wrong or disputed.

---

## 5. Readers improving the text

### 5.1 "Report an error here" — **Easy**, done once
Readers already report errors as GitHub issues (#100, #117, #169), following the About page. A link on each
chapter page (and on selected text) opening a new issue already filled in with the book, chapter, printed page and
the words selected. An email address is the alternative for readers without GitHub accounts.
*Pros:* more and better reports, straight into the `errata.md` process. *Cons:* reports need a GitHub account; an
email address on a public site gets spam.

### 5.2 A list of open and fixed reports — **Easy**, done once
A page built from `notes/errata.md`. *Pros:* readers see reports are acted on. *Cons:* the errata table is written
for Claude and would need a reader's column.

---

## 6. Accessibility and look

### 6.1 A full accessibility audit — **Moderate**, done once
Keyboard order, focus, ARIA in the settings panel and bar, contrast in all four themes, reduced motion, zoom to
400 %. *Pros:* Tom asked for "no problems for readers using screen readers" (2026-11-20). *Cons:* best done with a
real screen reader as well as automated checks.

### 6.2 Language tags on all foreign passages — **Moderate**, ongoing
Arabic and Chinese runs are tagged now (`render_html.py`); French, Latin, German, Malay and romanized Japanese are
not. A markup for marked passages, with the language, typed in the draft or the corrections pass. *Pros:* screen
readers read them in the right voice; hyphenation is right. *Cons:* more markup per book; needs a calibration run
before the prompts change (`notes/workflow.md` §"Choosing the pipeline").

### 6.3 Japanese script — **Moderate**, done once then per book
`workflow.md` §"Not yet solved": try a sample page through the pipeline and the three builders before the first
JATSI book with more than a few characters. *Pros:* needed for JATSI. *Cons:* fonts in EPUB readers and LibreOffice
vary.

### 6.4 Other unsolved kinds of printing
From `workflow.md` §"Not yet solved": endnotes linked to their numbers; footnotes of more than one paragraph; a
paragraph that runs on after a quoted verse; a second stream placed after its own chapter; multi-volume works on
real data; eighteenth-century printing (long s, catchwords). Each is **Moderate** and is done when a book needs it.

---

## 7. Formats

### 7.1 Check the EPUBs with EPUBCheck in CI — **Moderate**, done once
*Pros:* catches errors that some readers (Apple Books, Kobo) show and the browser does not. *Cons:* Java in the
build; the first run may list many warnings to sort out.

### 7.2 PDF — **Moderate**, done once
Made at build time (for example with WeasyPrint, a Python tool in CI; nothing on the site itself). *Pros:* some
readers and libraries want it. *Cons:* a large tool in the build; adds to §0; the HTML print stylesheet (2.10) does
much of the same for free.

### 7.3 Kindle — nothing to do
Amazon's "Send to Kindle" accepts EPUB. A line on the About page could say so (**Easy**).

---

## 8. Quality of the site's code

### 8.1 Screenshot tests in CI — **Moderate**, done once
Playwright pictures of a few pages, narrow and wide, in each theme, compared with stored pictures. *Pros:* catches
layout breaks before deploy. *Cons:* needs Chromium in CI; stored pictures go in the repo (small).

### 8.2 Link checking — **Easy**, done once
A weekly check of the links to IA and Tom's JATSI site (not on every deploy). *Pros:* IA items are occasionally
darkened or renamed; finding out quickly matters for the "good scan" claim. *Cons:* outside servers rate-limit; the
check must be gentle.

### 8.3 Safari and Firefox checks — **Moderate**, done once
Sessions can test only in Chromium; Safari bugs (the bar over `#start`, the reset tip) were found by Tom. Playwright
can run WebKit and Firefox if installed in CI. *Pros:* fewer bugs reaching Tom. *Cons:* bigger CI; WebKit in
Playwright is close to Safari but not the same.

---

## 9. Outside the assumptions (listed so they are not suggested again without reason)

These need an outside service, an account, or a server. Each is Tom's decision.

- **Automatic sync of the Library** through the reader's GitHub Gist (a token they paste), Google Drive (an OAuth
  client ID for the site and a sign-in), or WebDAV. *Pros:* sync without manual steps. *Cons:* outside requests
  from the site; sign-in screens; privacy; upkeep when those services change.
- **A DOI per version via Zenodo** (it archives each GitHub release). *Pros:* a permanent identifier libraries
  trust. *Cons:* connects an outside service to the repository, though nothing on the site changes.
- **Comments or discussions** (GitHub Discussions, or a comments service). *Cons:* needs moderation; against the
  plain design.
- **A mailing list** for new books. *Cons:* needs a service; the feed (3.8) does the same without one.
- **Analytics.** *Cons:* against the rule of no trackers. GitHub shows repository traffic only, not site traffic.
- **A domain of the site's own** (for example `travelbooks.example`): GitHub Pages supports it at no cost but a
  domain must be bought and kept. *Pros:* a stable address independent of the account name. *Cons:* everything
  saved in readers' browsers stays at the old address (1.7); old links need redirects.

## 10. Reaching readers (not changes to the site; each is Tom's decision)

- **Listings:** The Online Books Page, Wikipedia and Wikisource author pages, Wikidata, library catalogues via
  OCLC. *Pros:* most readers would find the books this way. *Cons:* outward actions in Tom's name; some sites have
  rules about adding links to one's own work.
- **Offering texts to Project Gutenberg or Standard Ebooks.** *Pros:* wide reach; the texts are CC0. *Cons:* their
  own proofing rules and formats; for many books here the point is that no other text exists, which would change.
- **Telling IA:** a review or link on each item's IA page pointing to the edition. *Pros:* readers of the scan find
  the text. *Cons:* outward action on another site.
- **Japanese summaries or a Japanese guide to the JATSI books** (**Moderate**): new writing beside the books, not a
  change to their text. *Pros:* readers in Japan, where JATSI began. *Cons:* translation must be checked; one more
  thing to keep up to date.

---

## Suggested order

1. **§0** the size check in CI, then smaller pictures in the EPUB and ODT, then the EPUBs and ODTs moved to Releases
   or files repositories (0.1), before the site grows further.
2. Cheap items that need no new data: 5.1 error-report links, 4.1 citations, 3.13 search-engine data and link
   previews, 3.14 a 404 page, 3.2 related books, 2.2 "continue reading", 2.10 printing, 2.5 whole book on one page.
3. The Library, in order: 1.1 shelves and 1.2 bookmarks, 1.5 export and merging, 2.3 passage links, 1.3 notes;
   2.1 offline reading alongside (it also protects Safari readers' data).
4. 3.1 search (titles first), 3.8 the feed, 4.6 accuracy on book pages, 6.1 the accessibility audit.
5. The larger, ongoing items only when Tom asks: 3.3 subject index, 4.7 indexes, 3.6 routes, 6.2 language tags.
