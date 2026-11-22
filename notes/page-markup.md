# Page markup

One UTF-8 text file per IA leaf, `pNNNN.txt` (NNNN = the number in the scan's image file names). Written by the
models (`prompts/_format.md` is the wording they get), edited by the session, read by `tools/compile_book.py`.

| Markup | Meaning |
|---|---|
| `[[page N]]` (line 1) | printed page number as printed; `?` if none |
| `[[blank]]` | blank page |
| a line of text | one paragraph (paragraphs are separated by a blank line; a paragraph is never broken over lines) |
| `[[cont]]` at the start of the page's first paragraph | it continues the previous page's last paragraph (joined with a space; a page-final hyphen is removed unless the page is in `keep_hyphens`; no space at a dash) |
| `# ` / `## ` / `### ` | main division (starts a new division, file and contents entry) / section / subsection; typed in upper and lower case even if printed in capitals (`style.md`) |
| `[[subtitle]] text` | chapter title or summary printed under the chapter number; joined to the contents entry if short |
| `<i> <b> <sc> <sup> <sub>` | italic, bold, small capitals (typed in lower case), superscript, subscript; balanced within the paragraph, not nested in themselves |
| `[[right]] text`, `[[center]] text` | a short line set flush right / centred |
| `[[break]]` | a break between paragraphs marked by space or an ornament |
| `[[image: description]]` | illustration; file `images/pNNNN-k.jpg` (k-th image on the leaf); the description is the alt text |
| `[[caption]] text` | printed caption of the image just before |
| `[[fnref *]]` / `[[fn *]] text` | note reference / note (at the end of the page file); the k-th reference with a mark pairs with the k-th note with that mark in the division |
| `[[fnref * again]]` | a second printed reference to the note last referenced with that mark (one note, two marks in the text) |
| `[[fn cont]] text` | continuation of the previous page's last note |
| `<blockquote>` … `</blockquote>` (own lines) | set-off prose, one paragraph per line; `[[right]]`/`[[center]]` allowed at line start |
| `<verse>` … `</verse>` (own lines) | verse, one printed line per line, an empty line between stanzas |
| `[[cont]]` at the start of the first line inside a blockquote or verse at the top of a page | it continues the previous page's quotation (prose is joined mid-paragraph unless the previous line ended a sentence; verse continues as a new line of the same stanza) |
| `[[cont]]` at the start of a paragraph right after an `[[image: …]]` (and caption) in the middle of a page | the paragraph the picture interrupts goes on: joined to the paragraph before the picture, and the picture follows that paragraph in the editions |
| pipe rows `| a | b |` | table |
| `<pref>34</pref>`, `<pref to="34">text</pref>` | the book's own reference to its page 34: becomes a link when page 34 is in the reading editions |
| `[[side: text]]` | a marginal note (side-note), inside the paragraph immediately before the first word of the printed line it stands beside; kept in the JSON (`<side>`), left out of the reading editions (Tom, 2026-11-19, for Staunton's *Embassy*) and of plain text; preflight `conservation` compares the side-notes of the page files and the JSON apart |
| `[[stream]] text` | a line of a second stream of text printed on the same page apart from the main text (documents in small type along the foot of many pages, not footnotes: *Brown Men and Women* pp. 268–286). After the prefix, one-line markup as usual (`# ` heading at its start, `[[cont]]` at the top of a page). The compiler makes the stream a division of its own, after all the others, marked `"stream": true` (kind from book.json `stream_kind`, default appendix); the main text joins over the pages as if the stream were not there; preflight compares it apart |
| `[[corr printed|corrected]]` | a printer's error corrected by us (`style.md`) |
| `[[supplied e of]]` | letters lost in the scan (fold, tear, blot), not settled by another scan or edition, inferred from the context: marked in the JSON (`<supplied>`), plain text in the reading editions (Tom, 2026-11-20) |
| `[[gap]]` | letters lost in the scan that cannot be inferred: `[…]` in the JSON and the editions |
| `〓` | illegible character |

Editing by hand: never "fix" the author's spelling; only fix transcription and markup. Straight quotes typed
by hand are curled by the compiler (`'tis`-type elisions are recognised from a list in `tools/inline.py`: for
any other word-initial apostrophe type `’`).
