# About

This site publishes travel books from the past in forms that are easy to read and to use: web pages, EPUB, ODT, and JSON. The project began in November 2026 and is run by Tom Gally. The books are chosen, transcribed, and checked by Claude, an AI model made by Anthropic.

## Which books

For now a book is included only if all of these are true:

- It is a first-person, nonfiction account of the author’s own travels, written in English and published before 1914.
- A complete, good scan of it is at the [Internet Archive](https://archive.org/).
- No other edition of its text made for reading is freely available on the Internet. Automatic text recognition (such as the Internet Archive’s), short excerpts, and texts in subscription or scholarly databases (such as EEBO and ECCO) do not count.
- It has not been published in print since 1914, apart from short excerpts and print-on-demand copies of scans.
- Its author died more than 70 years ago.

Some books are here for a different reason. [Japan As They Saw It](https://www.gally.net/jatsi/index.html) is an earlier project of Tom Gally’s with a list of 247 books about Japan, published between 1855 and 1912 ([the list, and which of its books are here](japan-as-they-saw-it.html)). In November 2026 he decided to add the books of that list to this site gradually, about one in every three books published, so the site will have more books about Japan than about any other country. Those books are marked in the lists. They are included because they are on that list: some of them have been reprinted or have a digital text elsewhere, and some are not accounts of the author’s own travels. Nor does the rule about the author’s death apply to them: all are in the public domain in the United States and Japan, and where an author died less than 70 years ago the book’s page says so. Their texts are made in the same way as the others.

One other book is included as an exception to these rules, at Tom Gally’s choice: [*An Authentic Account of an Embassy from the King of Great Britain to the Emperor of China*](books/embassy-to-china-staunton/index.html) (1797), by Sir George Staunton, which has later reprints and other digital texts. Its page says so.

Among the books that qualify, the choice is Claude’s. The aim is a varied set of readable books that are otherwise found only in libraries or as page scans.

These books were written between about one and four centuries ago. They contain opinions about peoples, religions, women, empire, and animals that many readers now will find wrong or offensive. The texts are given as they were printed.

## How the texts are made

Each page of the scan is read by one Claude model and proofread against the page image by another. For a few pages the first reading is made by an OCR program (Tesseract) and corrected by a Claude model before the proofreading; a book that has such pages says so in its notes on the text. Where the two differ, a third reading decides, and uncertain places are checked against enlarged images of the print. Before a book is published, a set of automatic checks must pass, and a sample of pages is proofread again with deliberate errors added, to measure how many errors the proofreading finds.

No transcription is free of errors. If you find one, please [report it on GitHub](https://github.com/tkgally/travel-books/issues), giving the book and the page or a few words of the passage. Corrected versions are published as needed; each book’s page lists its versions.

## The text

- The author’s words, spelling, capital letters, and punctuation are kept as printed, including old and inconsistent spellings.
- Spaces around punctuation follow modern practice. So do quotation marks that run over several lines or paragraphs: where older books repeat the opening mark at the start of every line of a quotation, only the opening and closing marks are kept, and a quotation of several paragraphs has an opening mark at each paragraph and a closing mark at the end.
- Words divided at the ends of lines are joined.
- Clear printer’s errors are corrected. Each correction is listed on the book’s page and recorded in the JSON with the printed reading.
- Headings printed in capitals are given in upper and lower case.
- Long passages printed in italic, such as whole paragraphs, are given in ordinary type on the web pages and in the EPUB and ODT. The JSON records the italics as printed.
- Illustrations and their captions are included. Footnotes are linked.
- The web pages, EPUB, and ODT begin with the book’s title page. They leave out some parts of the printed book, usually what stands before the title page, the printed table of contents, the index, and the publisher’s advertisements. The JSON has everything that was transcribed.
- A long text that the book does not divide into chapters, such as a diary, is divided into sections for reading, each with a title that says what it covers. These titles are not part of the book, and the JSON keeps the text undivided.

On the web pages you can show the page numbers of the printed book. Each number links to that page of the scan.

## Formats

- **Web pages**: one page for the title page and one for each chapter or other division.
- **EPUB**: for e-readers and reading apps.
- **ODT**: OpenDocument Text, for LibreOffice, Word, and other word processors. All books use the same named styles.
- **JSON**: the complete transcription with its structure, page breaks, and corrections. The other formats are built from it. See [the JSON format](json-format.html).

## Copyright

The books were published before 1914. Apart from a few books of the Japan As They Saw It list, whose pages say so, every author died more than 70 years ago. The transcriptions, the markup, the text of this site, and the software that builds it are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). You may copy, change, and republish them without asking. The scans belong to the Internet Archive’s collections and the libraries that made them; this site links to them and does not copy them, except for the illustrations.

## How the site is built

The source of every book, the tools, and the working notes are in the [GitHub repository](https://github.com/tkgally/travel-books). The site uses no trackers, no cookies, and no fonts or scripts from other sites. The only outside content is the optional viewer of scanned pages on each book’s page, which comes from the Internet Archive when you open it.

## Display settings

Every page has a settings button at the top right (two sliders). It opens a panel of settings: the colours (light, sepia, dark, or as your device is set), the size of the text, the typeface (serif, sans serif, or the one set in your browser), and the space between lines. Under “More settings” are the width of the column, justified or ragged lines, indented or spaced paragraphs, the space between letters and between words, the underlining of links, the dotted marks under corrected misprints, the page numbers of the printed book, whether your place in each book is remembered, and whether a bar of buttons is shown at the top of a chapter. The last button puts everything back as it was. The settings apply to every page of the site, except those that concern only the text of a book (justified lines, paragraphs, corrections, page numbers). The title and links at the top of each page grow with the text up to the sixth of the nine sizes and no further.

On the pages with the text of a book, a narrow bar appears at the top of the window once you have scrolled down. Its first button (a compass) opens a short menu: the home page of the site, the book’s own page, and the book’s table of contents. The others lead to the previous chapter, to the next chapter, and to the display settings, which stay in the same place on the screen as at the top of the page. When your place is remembered, it is remembered in each chapter: going to another chapter and coming back returns you to where you were.

The settings and your place in each book are kept in your own browser and are sent nowhere. If your browser does not run scripts, the button does not appear and the pages are shown with the site’s own settings, in light or dark colours as your device is set.
