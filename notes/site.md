# The site as it grows

What the pages are, how the home page changes as books are added, and what to do at each size. The builder is
`tools/build_site.py`; the tests are `SiteLists`. Tom's brief for the site is in `preferences.md` (2026-11-19:
plain, minimal, accessible, no outside dependencies, "later perhaps a topical index"); on 2026-11-20 he asked
for a plan for the home page as the number of books grows. This is it. Change it when the site shows it is wrong.

## Pages

| Page | What | Built from |
|---|---|---|
| `index.html` | what the site is: a row of covers (the carousel, below), the name and two short paragraphs, nothing else (Tom, 2026-11-21) | `data/carousel.json`, `site/carousel/` |
| `books.html` | the books; the queue ("Books" in the header of every page) | `books/*/book.json`, `data/queue.json` |
| `places.html` | the books by part of the world; a book is listed under each part it covers | `regions` in `book.json` + `data/places.json` |
| `dates.html` | the books by the decade in which the journey began (first year in `period`; else the year of publication) | `period`, `year` |
| `authors.html` | the books by author, under letters — only when the Books page no longer lists every book | `authors[0].sort` |
| `japan-as-they-saw-it.html` | why some books come from the JATSI list; those published and queued; the whole list with scan links | `data/jatsi.json`, the queue |
| `about.html`, `json-format.html` | | `site/*.md` |
| `books/<id>/…` | a book's page, its chapters, EPUB, ODT, JSON | the book |

Every line for a book, in every list, is the same (`book_line`): short title, author, year; under it the places,
the time of the journey, and "JATSI" for a book of that list.

**Header and way home (Tom, 2026-11-21).** The logo and "Travel Books" in the header are the link to the home page
from every page; beside them "Books" (`books.html`), "About" and the settings button. The breadcrumb line exists
only on chapter pages and is the book's title (→ its page) › the chapter; no other page has one (`crumbs` of
`build_site.page`). `places.html`, `dates.html` and `authors.html` each say "Also listed by …" with links to the
other lists. On a book's page the picture of the cover links to the start of the narrative, and “Click to read”, in small italics on two lines to its right, has the same link (Tom, 2026-11-23); “Read on this site” goes to the title page.

## Stages

| Published books | Books page (until 2026-11-21 these lists were on the home page) | To do when the stage is reached |
|---|---|---|
| up to 30 (`HOME_FULL_LIST`) | every book, by author; a line linking the lists by place and by date; the whole queue | nothing: this is now |
| 31 to about 150 | the ten newest (`HOME_NEWEST`, by the time version 1 was published: `data/published.json`, written by `publish.py`; a new version does not move a book) and links to the three full lists; the whole queue | automatic. In the review session after the thirtieth book: look at the home page and the three lists on a narrow and a wide screen; move the queue to a page of its own (`queue.html`, one line on the Books page) if it has more than about 25 rows |
| about 150 and more | the same | a part of the world in `places.html` with more than about 40 books gets its countries as sub-headings (East Asia will be first, because of JATSI: Japan, then the rest); `dates.html` by decade stays. Consider one page per part of the world. Consider a search box only if Tom asks: it needs a script and an index file, and the rule is "JS only if needed" |

Not planned until a reader or Tom asks: a subject index (`subjects` in `book.json` is free text and would first
need a fixed list of terms, as `regions` has in `data/places.json`); feeds; covers in the lists (the home page has a row of them: below; in the lists they would make
the Books page heavy and the lists harder to scan).

## The home page (Tom, 2026-11-21 and 2026-11-22)

The header, the carousel, three paragraphs, the footer. No visible heading: the name is in the header (the `<h1>` is
in the page for screen readers and outlines, class `visually-hidden`). The first paragraph ends "The site now contains
N books, with more being added every day." — N is the number of books built, the same list the Books page counts, so
the two cannot differ. The third paragraph is the link "More about the project." (`build_site.build_index`; tests
`SerialCommas`, `SiteLists`.)

## A book's own page

The picture links to the start of the narrative (`render_html.body_start`: the first division of kind `chapter`), with
the chapter's heading at the top of the window (`#start`); "Read on this site" links to the first page of the book,
the title page (Tom, 2026-11-22). The contents list every page of the editions; the sections of a split division are
nested under its title.
Safari on the Mac and the iPad left the heading half under the bar (Tom, 2026-11-22: the browser goes to `#start`
before `site.js` has made the bar and set `scroll-padding-top`), so `site.js` places the heading just below the bar
itself, at once and again after `load`, unless the reader has moved. Checked here in Chromium only (no WebKit in the
container); Tom confirmed it on Safari on the Mac and the iPad the same day.

## The carousel of covers on the home page (Tom, 2026-11-21)

His brief and his changes after trying it are in `preferences.md` (2026-11-21, "a carousel"). How it is built:

- **One picture for each book: `books/<slug>/images/cover.jpg`.** It is the picture on the book's page, the cover of
  the EPUB, and the thumbnail is made from it, so the two cannot differ. **The rule:** the cover if the title is
  clearly readable on it; otherwise the title page; if neither has a readable title, the first page of the first
  chapter or a similar representative page. The rule is applied when the book is made (`workflow.md` §5); a title
  page comes from the full-size leaf like any other crop.
- **The record and the thumbnails:** someone looks at the picture and runs `tools/carousel.py add SLUG --kind
  cover|title|page [--note …]`, which makes `site/carousel/<slug>.jpg` (at most 300 × 450, about 20 KB; the only
  pictures in the repo outside a book's `images/`) and writes `data/carousel.json` (what the picture is, its size,
  the sha256 of the `cover.jpg` it was made from). The kind words the alt text on the book's page ("Cover of the
  book", "Title page of the book", "A page of the book"; "Cover of the book" until the book is in the record).
  `carousel.py check` lists published books not yet in the record and thumbnails whose `cover.jpg` has changed.
  First set: 43 books, 17 covers and 26 title pages. For five the `cover.jpg` was a cover without a readable title
  and was replaced by the title page from the scan (no new version: the text is unchanged; noted in their logs):
  *Autumn Tour in Western Persia* (library tape covers the first letter of the title), *The Eastern Seas* (the
  log's page map was one leaf out: look at the leaf), *A Land of Mosques*, *South by West*, *Zephyrus*.
- **Brought up to date in the review session** (`improvement.md` step 6; Tom: "once every five sessions, when other
  maintenance tasks are run"). A new book is therefore not in the row until the next review. The build shows only
  books that are published, recorded and have a thumbnail, so nothing breaks in between.
- **The page:** `<nav class="carousel" aria-label="Some of the books">` between the header and `<main>` (so "Skip to
  the text" passes it), a list of links to the books' pages; each link is the picture, whose alt text ("Title, by
  Author") is the only text. In the page the books are in the order of their ids (the build stays deterministic);
  `site.js` shuffles them on every load.
- **Motion:** the row is an ordinary scrolling list with `scroll-snap-type: x mandatory`; three, four or five books
  are in view (`--n`, by the width of the window: under 26em, under 36em, wider) and the first book of each group
  has `scroll-snap-stop: always`, so a swipe moves one group and stops, by the browser alone. An arrow moves the
  row by one group in 650 ms with a slow–fast–slow curve (the script; at once if the device asks for reduced
  motion). Nothing moves by itself.
- **No end (Tom, after trying it):** each time the row comes to rest the script moves whole groups of books from
  the far end of the list to the other and shifts the row by the same distance in the same moment (`centre`), so
  the group in view is always in the middle and after the last book comes the first. No book is in the page twice
  (no copies: a screen reader and the Tab key meet each link once). It is not done while a link in the row has
  keyboard focus, so that Tab comes to the end of the list and leaves it; nor while a finger is on the row. It
  needs at least four groups of books.
- **Arrows only where there is a mouse** (`@media (hover: hover) and (pointer: fine)`; Tom: on phones and tablets
  readers swipe). Their disks are the page's colour at 62% (`color-mix`; solid on hover and in a browser without
  `color-mix`). They are always there: the row has no ends.
- **Without scripts:** the same row in the order of the page, with its scroll bar, its two ends and no arrows.
- **Tried by Tom** in Chrome and Firefox on the Mac and Safari on the Mac and iOS (the first version); the endless
  row and the arrows' new look were checked in Chromium only (clicks, the Tab key, touch swipes on a phone-sized
  screen). Not checked: real screen readers.

## The logo (Tom, 2026-11-21)

A stack of three books, chosen by Tom from twenty proposals. `site/assets/logo.svg` is the favicon (`<link
rel="icon">` in `build_site._page`), with its own light and dark colours; the same drawing is inline in the header
(`build_site.LOGO`, coloured by `.logo-*` in `site.css` so that it follows the reader's light, sepia or dark
setting). Change the two together: the test `test_logo_and_favicon_on_every_page` compares them.

## Rules for the lists

- **Newest** is ordered by `data/published.json` (slug → UTC time of version 1). Until 2026-11-21 it used the date of version 1, and books first published on the same day were ordered by id, so the day's newest books could be missing from the ten (*Argentine Plains* and *The Eastern Seas* were). Backfilled from the commit that added each `books/<slug>/book.json` (needs the full git history: `git fetch --unshallow`); `ledger.py check` reports a published book without a time.

- A new place name in a book's `regions` must be added to `data/places.json` with its part of the world (the
  test `test_every_region_of_a_published_book_has_its_part_of_the_world` fails otherwise). Use the names already
  in the file where they fit; a region inside a country (Hokkaido, Colorado) is listed beside the country.
- The parts of the world and their order are the `areas` list of that file. Islands in mid-ocean visited on a
  voyage go under "Atlantic and Indian Ocean islands" so that a voyage to China is not listed under Europe for a
  call at Madeira.
- `period` must contain a four-digit year for the book to fall in the right decade.
- The lists have no script: they are plain pages of links, each with a row of in-page links to its headings.

## The JATSI books on the site (Tom, 2026-11-20)

The reader is told in three places, in plain words: the second paragraph of the home page; the label
"JATSI", linked to `japan-as-they-saw-it.html`, on each such book and queue row (Tom, 2026-11-21; before that
"(JATSI)", "JATSI (about)", and first "from Japan As They Saw It (about these books)"; `jatsi_label()`; not on `japan-as-they-saw-it.html` itself, where he found it redundant); and the row "Why it is here" in
the table on the book's own page. On the home page the name links to `japan-as-they-saw-it.html` (Tom, 2026-11-21); wherever else the name stands in running text or a label it links to Tom's project
(<https://www.gally.net/jatsi/index.html>; `jatsi_name()` in the builder, a Markdown link in `site/*.md`), and
"about these books" links to the page on this site.

**Links** (Tom, 2026-11-20): every link to another site opens in a new tab or window (`target="_blank"
rel="noopener"`, added to every page by `outside_links` in `build_site.page`); links within the site do not.
The EPUB and ODT are not touched. `site/about.md` §"Which books" says the same. Nothing in
the reading text of a book differs.

## Display settings (Tom, 2026-11-20)

What Tom decided is in `preferences.md` (2026-11-20, "display settings"). How it is built:

- **One script, `site/assets/site.js`, in the head of every page, not deferred**, so that the colours are set before
  the page is drawn. It keeps one object in `localStorage` (`tb-display`, only the values that differ from the
  defaults) and the reader's places in another (`tb-place`: per book, the chapter file and the number of the block
  at the top of the window; the newest 100 books). Values read back are accepted only if they are in the script's
  own lists.
- **The script only sets attributes and custom properties on `<html>`** (`data-theme`, `data-font`, `data-align`,
  `data-para`, `data-corr`, `data-links`, `--tb-size`, `--tb-lh`, `--tb-width`, `--tb-ls`, `--tb-ws`, class
  `showpb`); the rules are at the end of `site.css` ("Display settings"). The text of the page is not changed, so
  a screen reader reads the same document. **`book.css` is not touched: it is shared with the EPUB.**
- **Without scripts** nothing of this exists: the "Display" button and "Continue reading" (book page) are made by
  the script, the chapter pages keep the page-number checkbox (the script removes it and offers the same in the
  panel), and the dark colours still follow the device (`prefers-color-scheme`, `:root:not([data-theme])`).
- **Scope** (Tom's second message, after seeing it): the button is on every page, to the right of "About". Colours,
  size, typeface, line, letter and word spacing, column width and link underlining apply to every page;
  justification, paragraph style and correction marks only to `article.book`.
- **Size:** `--tb-size` multiplies the root font size, so everything in `rem` grows with it (the column width too:
  the number of letters in a line stays about the same). **The header, the breadcrumbs and the panel follow it only
  up to 1.4, the sixth of the nine sizes** (`--tb-hs`; their font size is `1rem * hs / size`, and the panel's
  measures are in `em` for that reason). The side padding of the page does not grow. New rules for the site pages
  should use `rem` or `em`, not `px`, or they will not follow the setting.
- **The panel:** basic (colours, size, typeface, line spacing) and, behind "More settings", advanced (width,
  justified/ragged, paragraph style, letter and word spacing, four on/off buttons, reset). Controls are pictures;
  each has an `aria-label`, and the same words appear as a tip under it for a mouse (`hover: hover`) or keyboard
  focus — above it when there is no room below inside the panel (the panel in the reading bar scrolls, and Safari and
  Firefox cut off a tip past its foot: the reset button's tip was invisible there; Tom, 2026-11-23). Radio groups are real radio buttons; steppers announce the new value in a `role="status"` element.
- **A new theme** needs its six colours in `site.css` (`:root[data-theme="…"]`), a swatch (`.tb-sw-…`) and its name
  in `CHOICES.theme` in the script; the dark colours are written twice (device and choice) and a test keeps the two
  the same. Print always uses black on white.
- **The bar at the top of a chapter (Tom, 2026-11-21):** `nav.tb-bar`, made by the script on pages that have
  `article.book` and `nav.pager`, placed after the header, `position: fixed`. Four pictures, no words (each with an
  `aria-label` and a `title`): a compass that opens a menu (below), previous, next (their addresses are read from the
  page's pager; at the first or last chapter the arrow is a dimmed `span`), and a button that opens the same
  Display panel, which is moved into the bar while opened from there. In view (`tb-on`) when the header is out of
  view and the flag `bar` is on (default; `data-bar="off"` otherwise), and as long as the panel or the menu is open in it — so
  switching the bar off from the bar does not take the panel away. `scroll-padding-top` on `<html>` keeps anchors
  and keyboard focus from landing under it. Index pages have no bar.
  An arrow of the bar leaves the file name it goes to in `sessionStorage` (`tb-bar-nav`); the chapter that finds its
  own name there opens at the reader's place in it or, with none, just above its title, with the bar in view at
  once (`tb-now`: no sliding in), so the controls do not move (Tom, 2026-11-21). The pager's own links do not do this.
- **The menu of the bar (Tom, 2026-11-21):** `#tb-menu`, three links made from what the page already has: the logo
  and name (copied from the header's `.sitename a`) → home; an open book and the book's title (the first link of
  the breadcrumbs) → the book's page; the three-line picture and "Contents" → the pager's contents link. It is as
  wide as its longest line, at most the column; a title that does not fit is cut and its last 3em fade out
  (`tb-cut`, set when the menu opens, a CSS mask). Escape or a click elsewhere closes it; it and the panel are
  never open together.
- **The settings button is in the same place in the header and in the bar** (Tom, 2026-11-21: it should seem
  fixed). The header's (`.tb-btn`, the two-sliders picture, no word) is positioned from the top right corner of
  the header, the bar's by the bar's grid: both 2.4em square, the same distance from the top (a test compares the
  two numbers) and 0.5em beyond the column's right edge, with the same font size. If the header, the bar or
  either button is restyled, measure both pictures in a browser at the top of a chapter and scrolled down: they
  must have the same rectangle. The header has `padding-right` for it (only with the script).
- **The place in each chapter:** `tb-place` holds for each book `f`, `b`, `t` as before and `c`: chapter file →
  [block at the top of the reading area, the part of it (0–0.99) above the top]. Saved on scroll (every 400 ms)
  and on `pagehide`; a chapter opened by a link goes to its own saved place. A change in the panel keeps the same
  words at the top of the window (`spot`, `toSpot`).
- **Not built, by Tom's decision:** hosted fonts (so no named fonts or weights), free choice of colours,
  pagination, scrolling settings.
- **Checked in Chromium only** (desktop and phone widths, scripts off, dark device). Not checked: Safari, Firefox,
  and real screen readers (VoiceOver, NVDA, TalkBack) — Tom or a reader must try those.
