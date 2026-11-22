# The JSON format

Each book has one JSON file, `books/<id>/<id>.json`. It holds everything that was transcribed from the scan, including parts that the web pages, EPUB, and ODT leave out. Those formats are built from it. The format name is in the `format` field (`travel-books-json/1`); it will change if the structure changes in a way that could break a program reading it.

## Top level

| Field | Meaning |
|---|---|
| `format` | `travel-books-json/1` |
| `id`, `version`, `date` | the book’s identifier on this site, the version of the transcription, and its date |
| `license` | `CC0-1.0` |
| `title`, `subtitle`, `short_title`, `authors`, `place`, `publisher`, `year`, `edition_statement` | bibliographic description of the printed book that was transcribed |
| `regions`, `period`, `subjects`, `summary` | where and when the journey took place; a short description |
| `collection` | optional: `jatsi` for a book that is on this site because it is on the list of [Japan As They Saw It](https://www.gally.net/jatsi/index.html) ([about these books](japan-as-they-saw-it.html)) |
| `source` | `ia_identifier`: the scan at the Internet Archive; `hidden_leaves`: scan images the Archive’s viewer does not show |
| `notes_on_text`, `omitted_from_reading`, `history` | editorial notes, what the reading formats leave out, and the list of versions |
| `corrections` | printer’s errors that were corrected: `leaf`, `division`, `printed`, `corrected` |
| `pages` | every image of the scan that was transcribed, in order: `leaf` (`p0123` = image 123 of the scan), `number` (the printed page number, or empty), `blank`, `division` |
| `divisions` | the text |
| `editor_images` | optional: pictures added by the editor, not part of the book’s text (for example a page shown as printed, with a decorated border that the text leaves out): `src`, `leaf` (the scan image it is taken from), `alt`, `caption` (written for this edition), `editor`: `true`. The reading formats show them before the start of the narrative. |

## Divisions

A division is a chapter or another main part of the book.

| Field | Meaning |
|---|---|
| `id` | `d001`, `d002`, … in the order of the book |
| `kind` | `front`, `titlepage`, `dedication`, `preface`, `contents`, `illustrations`, `introduction`, `part`, `chapter`, `appendix`, `notes`, `glossary`, `index`, `errata`, `advertisements`, or `back` |
| `title` | the heading (with a short chapter summary), as used in page titles and links between chapters |
| `toc_title` | optional: the entry in the contents of the web pages, EPUB, and ODT when it differs from `title` (for example the chapter summary in full) |
| `stream` | optional: `true` for a division made from a second stream of text that the printed book runs along the foot of its pages, apart from the main text (not footnotes); it is placed after the other divisions, and its page numbers say where it was printed |
| `sections` | optional: entries of the contents inside the division: `title`, `block` (the index in `blocks` of the block it points at), `editor` (`true` for an entry of this edition’s, such as a span of dates in a diary; `false` for one taken from the printed book) |
| `reading` | `true` if the division is in the web pages, EPUB, and ODT |
| `split` | optional, `true`: the web pages, EPUB, and ODT divide this division at its `sections`, each section a page of its own under its `title` (a long text that the book does not divide, such as a diary); the JSON keeps the division whole |
| `first_leaf` | the scan image on which it starts |
| `blocks` | its contents, in order |
| `notes` | its footnotes: `id`, `mark` (as printed), `leaf`, `text` |

## Blocks

Every block has `type` and `leaf` (the scan image on which it starts). A block that begins at the top of a printed page also has `pb`, a list of `{"leaf", "n"}` (`n` is the printed page number, or empty).

| `type` | Other fields |
|---|---|
| `heading` | `level` (1 to 3), `text` |
| `paragraph` | `text`; optional `align` (`right` or `center`); optional `role` (`subtitle`: a chapter title or summary printed under the chapter number) |
| `quote` | `paragraphs`: a list of `{"text"}` with optional `align` — prose set off from the text, such as a letter |
| `verse` | `stanzas`: a list of stanzas, each a list of lines |
| `image` | `src` (a path beside the JSON file), `alt` (a description), optional `caption` |
| `table` | `rows`: a list of rows, each a list of cells |
| `break` | a break in the narrative marked in print by space or an ornament |

## Inline markup

Every text string is a well-formed XML fragment. The characters `&`, `<` and `>` in the text are written `&amp;`, `&lt;` and `&gt;`.

| Element | Meaning |
|---|---|
| `<i>`, `<b>`, `<sc>`, `<sup>`, `<sub>` | italic, bold, small capitals, superscript, subscript |
| `<pb n="97" leaf="p0123"/>` | printed page 97 (scan image 123) starts here, inside the block |
| `<noteref to="d004-n3">*</noteref>` | reference to the note with that `id` in the same division; the content is the printed mark; where the book prints two marks for one note, two `noteref`s have the same `to` |
| `<pageref n="34">34</pageref>` | the book’s own reference to its page 34 |
| `<corr orig="teh">the</corr>` | a printer’s error corrected; `orig` is the printed reading |
| `<supplied>e of</supplied>` | letters lost in the scanned copy (at a fold, a tear, or a blot) and supplied by the editors from the context; the reading editions show them without a mark |
| `<gap>[…]</gap>` | letters lost in the scanned copy that could not be supplied; the reading editions show […] |
| `<side>Arrival at Macao.</side>` | a marginal note (side-note) printed beside the line that starts with the word after it; the HTML, EPUB, and ODT editions leave side-notes out |

To get the plain text of a string, remove the elements and keep their content, except `noteref` (drop the mark) and `side` (drop the side-note, or keep it apart). To get the text exactly as printed, replace each `corr` element by its `orig`.

## What is normalized

Words divided at line ends are joined. Spaces around punctuation follow modern practice, and so do quotation marks over several lines or paragraphs (an opening mark repeated at the start of each line is left out; a quotation of several paragraphs has an opening mark at each paragraph and a closing mark at the end). Ligatures such as fi are written as separate letters, and the long s is written s. Running heads, page numbers at the head or foot of the page, and printers’ signature marks are left out; page numbers are kept in `pb` and `pages`. Headings, chapter summaries, and captions printed in capitals are given in upper and lower case. Nothing else in the wording, spelling, or punctuation is changed without a `corr` element, and letters lost in the scanned copy are marked by `supplied` or `gap`.

Italics are recorded as printed. The web pages, EPUB, and ODT show long italic passages in ordinary type; the JSON does not.

## Linking to the scan

Image `p0123` of a book whose `source.ia_identifier` is `X` is shown at `https://archive.org/details/X/page/nN/mode/1up`, where N is 123 minus the number of `hidden_leaves` smaller than 123.
