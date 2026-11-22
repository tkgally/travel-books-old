# The JATSI books

"Japan As They Saw It" (JATSI, <https://www.gally.net/jatsi/index.html>) is an earlier project of Tom's:
passages about Japan by American and British visitors, with a Sources page listing 247 books (1855–1912) at the
Internet Archive. It was one of the starting points of this project. On 2026-11-20 Tom decided that those books
are to be added here gradually (`preferences.md`, that date). This file says how.

## What Tom decided

- One JATSI book at a time, at about one for every three books added to the project.
- The site says which books came from JATSI and why (the shelf will lean towards Japan; that is accepted).
- A stored list of all the JATSI books; a dozen or so that meet most or all of the criteria go in the main queue.
- Other books are chosen as before (`selection.md`). The text policy is the same for all books.

## Where things are

| What | Where |
|---|---|
| The whole list: number, year, title, author, JATSI's one-line summary, IA scans, Gutenberg numbers, `kind`, `vetted`, `died_after_1955` | `data/jatsi.json` (does not change when a book is queued or published) |
| A JATSI book's state | its row in `data/queue.json`: `"from": "jatsi"`, `"jatsi": <n>` |
| The pace | `queue.json` `jatsi_policy`; `python3 tools/ledger.py` says which kind of book is due next |
| A JATSI book in work or published | `book.json` `"collection": "jatsi"` (goes into the book JSON; the site labels the book from it) |
| The reader's explanation | the site page `japan-as-they-saw-it.html` (built from the two data files), the home page, `site/about.md` |
| Consistency of all this | `tools/ledger.py check`, run by the tests |

## The pace

`jatsi_policy`: `{"since": "2026-11-20", "others_before": 6, "others_per_jatsi": 2}`. Counting only books
started (in progress or published) since the policy began, a JATSI book is due whenever the other books started
number at least twice the JATSI books started: JATSI, other, other, JATSI, … (confirmed by Tom, 2026-11-20).
It is a pace, not a lock: when the JATSI book that is due cannot be started (a scan problem, a tool not ready),
take another book and let the count catch up. Tom may run the regular sessions more often later; he does not
want the lower-priority books to be "years away", so plan for all 247.

## Which rules apply to a JATSI book (`selection.md` has the rules; Tom's answers of 2026-11-20)

| Rule | For a JATSI book |
|---|---|
| 1. a complete, good scan at IA | **Required.** Not necessarily the scan JATSI links: look for a better one of the same edition (many JATSI links are Google or Digital Library of India scans). The edition JATSI lists is the one to transcribe when a good scan of it exists; otherwise the first edition, or the best-scanned one, said in `edition_statement` |
| 2. no digital text elsewhere | Not required; sets priority. A book with a Project Gutenberg text (`gutenberg` in `jatsi.json`, 44 of them) is still done, **transcribed afresh from the scan by the usual pipeline — Gutenberg's text is never used**, not even as a check |
| 3. not reprinted after 1914 | Not required; sets priority |
| 4. a first-person account of the author's own travel | Not required; sets priority (`kind`) |
| 5. every author dead more than 70 years | **Does not apply** (Tom: all are in the public domain in the United States and Japan, and he wants to link the new editions from the JATSI Sources page soon). Still find and record the dates. When an author, editor or credited illustrator died after 1955 (`died_after_1955` in `jatsi.json` has those known), say so in the book's `notes_on_text`: "… died in 1958; the book is in the public domain in the United States and Japan, and may still be in copyright in countries where the term is the author's life and 70 years." The site promises this |

The queue row's `eligibility` says, for each rule, met or not and what was searched, exactly as for other books,
and begins "JATSI <n>." so that nobody takes an unmet rule for an oversight. Nothing on the site may say of a
JATSI book that it has no other edition unless that was checked and is true.

## Priority

**Normal priority** — queued like any other book and taken in turn: a JATSI book that meets the project's general
criteria (rules 1–4). How much of it is about Japan does not matter: a round-the-world book with one chapter on
Japan that meets the criteria is queued like the rest, the whole book transcribed, and marked as JATSI.

**Lower priority, still to be done** — in roughly this order: narratives and mixed books that were reprinted
after 1914 (the more readable first: several are already queued, because the first batch was chosen before
this order was settled; they may be taken after the normal-priority rows); books with a text at Project
Gutenberg; the non-narratives (`kind: other`: histories, compilations, guidebooks, reference works, pamphlets,
picture books; multi-volume sets last).

Keep at least four JATSI rows `queued` (`ledger.py` says when there are fewer). To add more: take entries from
`data/jatsi.json` in the order above (those with `vetted` have been looked at: read it first), vet them by the
`select-book` procedure (the checks, the scan looked at, twenty pages read), and among equals prefer a spread
over the decades 1855–1912 and over kinds of writer (naval officers, diplomats, teachers, missionaries,
tourists, residents) and single volumes within the tools' reach. Correct `kind` in `jatsi.json` when reading
shows the one-line summary misled. A JATSI book with no usable scan gets a queue row `waiting` saying what was
looked at, to be tried again when IA has another.

Two entries are the same work twice: Oliphant's *Elgin's Mission* (n 13 British edition in two volumes, n 16
American edition in one); Dilke's "English Influence in Japan" (n 42) is a chapter of *Greater Britain* (n 25).
Do each work once and say on the queue row which entries it covers.

## What these books bring that the others have not

- **Japanese words and names in the author's romanization** (Yedo, Tôkiyô, Kiôto, Hakodadi, jinrikisha, daimio):
  exactly the place where models write the familiar form. Macrons and circumflexes as printed. Every judge spot
  and audit candidate on such a word gets a crop. `regions` in `book.json` uses the modern names.
- **Japanese script** (kanji, kana) printed in the text or on plates: untested (`workflow.md` §"Not yet solved").
  Look for it at the scan check; a book with more than a few characters waits until a sample has been tried.
- **Many halftone photographs** in the books after about 1895, often with captions set among the text.
- **Reprints**: many of the better-known titles were reprinted in facsimile in the Ganesha / Edition Synapse sets
  *Japan in English* (2002–04; the National Diet Library catalogue lists the volumes), by Elibron, or by Kegan Paul:
  expect rule 3 to fail often, and search those three by name.
- **Editions**: JATSI sometimes lists a late edition (the seventh of *The Mikado's Empire*) or a reissue; the year
  in `jatsi.json` is that of the copy listed.

## Log

| Date | What |
|---|---|
| 2026-11-22 | *Japan for a Week* (Thompson, 1911; n 238) published from the UC scan: a week in Japan on the way round by Siberia; romanized words as printed (Tennō and Tenno); no Japanese script. Next due: two other books, then JATSI. |
| 2026-11-22 | Twelve narratives vetted by three Opus subagents (n 12, 19, 20, 29, 43, 72, 76, 89, 205, 236, 238, 239): seven queued at normal priority (Thompson, Seitz, Maus, Lawrence, Fowler — rule 3 to settle —, Taylor, Floyd-Jones); Smith, D'Almeida, Maclay and Cornwallis reprinted by Ganesha (Cornwallis also Google-only with poor plates), Aubertin's map missing from both Google scans: `vetted` in `jatsi.json`. *Japan for a Week* (Thompson, n 238) started. |
| 2026-11-22 | *Present-Day Japan* (Davidson, 1904; n 179) published from the UC scan: letters arranged by place and subject; Japanese script only inside pictures (a kakemono, styles of writing, a katakana chart kept as a picture). Next due: two other books, then JATSI. |
| 2026-11-21 | *The Eastern Seas* (Bax, 1875; n 40) published from the Cornell scan: Japan is about a third (Kobé, Nagasaki, Fusi-yama, Yesso), the rest China, Formosa and Siberia; romanized names as printed (Haconé and Hacone both); no Japanese script. *Sketches of Life in Japan* (Knollys, n 73) set `waiting`: the only scan has lost parts of ten pages. Next due: two other books, then JATSI. |
| 2026-11-20 | *Japan: A Sailor’s Visit to the Island Empire* (Cook, 1891; n 83) published from the BYU scan: no Japanese script, romanized words without accents (one Ōtani). Next due: two other books, then JATSI. |
| 2026-11-20 | Fourth JATSI book published: *A Jaunt in Japan* (n 142; Jackson, 1899), Cornell scan; errata slip applied; no Japanese script. Next due: two other books, then JATSI. |
| 2026-11-20 | Third JATSI book published: *A Cruise in the U.S. Steam Frigate Mississippi* (n 14; Gragg, 1860), LoC scan with the cut last page from the UC (Google) scan. Romanized names as printed (Nangasaki, Simoda, Hakodadi, Jeddo, Kanagarva); no Japanese script. Next due: two other books, then JATSI. |
| 2026-11-20 | Second JATSI book published: *On Short Leave to Japan* (n 98), from the UC scan (500 ppi; the Cornell scan JATSI links not needed). No Japanese script in the text (some on a signboard in one photograph). Next due: two other books, then JATSI. |
| 2026-11-20 | First JATSI book published: *Rambles through Japan without a Guide* (n 86). One leaf missing from the UC scan, supplied from the Michigan (Google) scan; its engraving is blank there and is left out. Next due: two other books, then JATSI. |
| 2026-11-20 | Tom's answers: the pace confirmed; rule 5 lifted for JATSI; Gutenberg and non-narrative books lower priority but to be done, afresh; round-the-world books by the general criteria. Eight more rows queued (Sheldon, Kothari, Swainson, Davidson, Fisher, Murray, McLean, Bickersteth): 21 in all. |
| 2026-11-20 | List taken from the Sources page (247 entries); IA metadata and a Gutenberg catalogue match for all; `kind` assigned from the one-line summaries (narrative 105, mixed 39, other 103); 26 narratives vetted by Opus subagents: 13 queued (8 meet all five rules; 5 meet all but rule 3, having a Ganesha, Elibron or Cambridge reprint), the other 13 have what was found under `vetted` in `data/jatsi.json` (most are held by an author's unknown dates). First in line: *Rambles through Japan without a Guide* (n 86). Session run on Fable by Tom's choice. |
