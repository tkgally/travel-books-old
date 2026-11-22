# Choosing books

## What qualifies (Tom, 2026-11-19 — all five, for the time being)

1. **Scan.** A high-quality, complete scan is on the Internet Archive: every page readable, no text or
   illustration missing or obscured. Checked before any transcription (`workflow.md` §1.4). If one scan is
   inadequate another IA scan of the same edition may be used.
   **A missing map alone does not fail a book** (Tom, 2026-11-22): it is published without the map and says so in
   `notes_on_text`. A book that fails only for one or two other missing elements: ask Tom whether to make an exception
   (`preferences.md`, Questions for Tom) and set it aside meanwhile.
2. **No digital reading edition elsewhere.** No free text of the book made for reading is on the Internet: Project
   Gutenberg, Wikisource, Faded Page, A Celebration of Women Writers, or any other site that offers the whole text
   as a readable edition (web pages, EPUB and the like). Brief excerpts do not count. Nor do (Tom, 2026-11-20):
   - raw OCR, alone or behind page images (IA's own, HathiTrust, Google Books, the Qatar Digital Library);
   - texts in **subscription library databases** (Alexander Street, Adam Matthew, Gale and the like);
   - texts in **online scholarly databases not formatted for immersive reading**, such as EEBO-TCP, ECCO-TCP and
     Evans-TCP, even where they are free.
   Record such a text in the queue row's `eligibility` when one is found; it is not a reason to reject the book.
3. **Not reprinted.** No edition in print after 1914, other than brief excerpts. Print-on-demand reprints of
   the scan (Kessinger, Forgotten Books, Palala, Nabu, Wentworth, HardPress, Franklin Classics, BiblioLife,
   Creative Media Partners, Legare Street, Hansebooks, Sagwan, CreateSpace replicas and the like) do not
   count. A real new edition does: reset type, a publisher's or scholarly edition, or a facsimile from an
   established press (Cambridge Library Collection, Elibron/Adamant, Gorgias, Arno, Ganesha, Routledge,
   Virago, Eland, Dover …). A translation into another language is not an edition of the English book.
4. **The book.** First-person nonfiction account of the author's own travel, written in English (not a
   translation), published before 1914. Any era, author, or part of the world. Not a guidebook, compilation,
   or fiction; if scholars doubt the journey happened, leave it out.

5. **Public domain where the term is life plus 70 years** (Tom, 2026-11-19): every author (and editor or
   illustrator whose work is in the book) died more than 70 years before the start of the current year — in
   2026, in 1955 or earlier. Death date unknown (Tom, 2026-11-19): assume the person died before the age of 100, so a person known to be born (or, from their career, certainly born) before 1856 qualifies; record the birth year or the evidence for it in the queue row. If even the birth year cannot be bounded, leave the book out.
   A book that fails only this goes under `rejected` with the year it becomes eligible.
   A minor illustrator whose date of death cannot be found does not keep a drawing out (Tom, 2026-11-20, on the
   one plate "from a Drawing by Mr. Thompson" in *Corona and Coronet*): include it. A book whose illustrations are
   largely by a person known to have died less than 70 years ago still waits.
   **The JATSI books are exempt from this rule** (Tom, 2026-11-20: all are in the public domain in the United
   States and Japan). `jatsi.md`.

**Two kinds of exception, both Tom's.** A book he asks for by name (so far Staunton's *Embassy to China*; queue
row `"from": "tom"`). And the books of his list "Japan As They Saw It" (2026-11-20; queue rows `"from": "jatsi"`):
only rule 1 is required of them; rules 2–4 are checked and recorded and set the order in which they are done;
rule 5 does not apply — `jatsi.md`. Everything below about how to check applies to them too. For every
other book all five rules stand.

## How to check (record what was searched in the queue row's `eligibility`)

- **Project Gutenberg**: the site refuses scripted requests; search the catalogue file
  (`pg_catalog.csv`, e.g. from the gutenberg.pglaf.org mirror) by author and title words.
- **The Online Books Page** (`onlinebooks.library.upenn.edu/webbin/book/search?author=…&title=…`): indexes
  Gutenberg and many other free editions; a listing that points only to page images does not disqualify.
- **Wikisource**: title and author search; an index page with no pages transcribed does not disqualify, but
  note it and look again before starting.
- **Faded Page / Distributed Proofreaders Canada** author list; **A Celebration of Women Writers**. For books before
  1800 the **Text Creation Partnership** sets (EEBO-TCP, ECCO-TCP, Evans-TCP) cover nearly every seventeenth-century
  English travel book: a TCP text does not rule a book out (rule 2), but note it in the row.
- **A web search** of a distinctive sentence from the book (in quotation marks), which finds texts on small
  sites.
- **Reprints**: Open Library, a web search of title + author + "reprint"/"edition"; WorldCat when reachable.
  Hakluyt Society, Broadway Travellers and the like reprinted many early voyages.
- IA: `tools/ia.py search …`, `tools/ia.py meta <id>`; low download counts and library contributors
  (California, Toronto, Library of Congress, Getty, Smithsonian, Boston Public Library) are good signs;
  Google scans (`…goog`) are often bilevel and missing folded plates — look before trusting.

What cannot be checked (Distributed Proofreaders work in progress) is said so in the row.

Read the list of illustrations too: a plate credited to a named artist brings that person under rule 5 (but see
the rule: a minor illustrator with no findable dates does not keep a drawing out; a book whose many illustrations
are by a person who died less than 70 years ago waits).

## Before starting a queued book

Repeat checks 2 and 3 quickly (the catalogue and one web search), look at the Wikisource index if one was
noted, and do the scan check of `workflow.md` §1.4. Then set the row to `in progress`.

## Choosing among those that qualify

Tom's aim: a resource where modern readers find travel books from the past that they can enjoy, learn from
and use for research — books not easily available except in libraries or as scans. Claude chooses, by its own
judgement and taste, sometimes after asking Tom. So:

- **Readable first.** A voice, things seen and people met, a journey with some shape. Read twenty pages of
  IA's OCR text from the middle before queuing a book; a dull book is not rescued by being rare.
- **A wide range across the shelf, with no group preferred** (Tom, 2026-11-19): authors, nationalities,
  destinations, centuries, kinds of journey. Do not choose or pass over a book because of the author's gender
  (or nationality, or any such trait); the books already queued stay. Look at what is published and queued
  before adding, so that no one kind of author or destination comes to dominate.
- **Within the tools' reach**: single volume, 150–450 pages, plain layout, footnotes at the page foot. Books
  with side-notes, many tables, long passages in other scripts, or hundreds of plates wait until the tools
  handle them (`workflow.md` §"Not yet solved").
- Books of their time contain views that are offensive now. That is not a reason to leave a book out or to
  alter it; the About page says so once. A book whose main matter is abuse is not chosen.

The JATSI books will make Japan the largest single destination on the shelf: that is decided and is not a reason
to pass over, or to prefer, a Japan book among the *other* candidates — but with a dozen Japan books queued from
JATSI there is no need to look for more of them elsewhere.

Keep at least six books `queued` that are not from JATSI, and four that are (`python3 tools/ledger.py`). Rejected candidates stay in `data/queue.json` under `rejected` with the
reason, so that nobody checks them twice.
