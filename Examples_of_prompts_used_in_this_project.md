## Background

I began this project on November 19, 2026, by giving the first prompt shown below to Claude Fable 5.2. I wrote it in a Doutour coffee shop in Isezakicho, Yokohama, Japan. The prompt took me about an hour to write.

I had run similar experiments on and off for more than a year with having AI agents transcribe and proofread book scans. The most recent models and harnesses had improved enough to produce digital books that are, in my opinion, sufficiently accurate and well-formatted for smooth reading and online publication.

Perhaps the most novel part of the starting prompt is how it asks Claude to continually monitor, adjust, and improve the workflow itself. In subsequent sessions, Claude seems to be doing just that. For example, on the second day of the project, it was transcribing a book that included a short passage of Arabic. According to its later report to me, Claude added a feature to tag right-to-left text properly; I expect, though I haven’t confirmed it yet, that this feature will apply to all future transcribed books.

After the project was set up and the website live, I have had Claude made various changes and adjustments to the interface, style guidelines, etc. An example of an especially long follow-up prompt, which I wrote and gave to Claude three days after the start of the project, also appears below. Fable was able to implement almost all of my requested changes in a single session, though it left a few for later sessions.

The cost for this project is being covered by my Ultra subscription to Claude ($200 a month), which I also use for other projects. I am monitoring how much of my subscription this project consumes, and I will adjust the frequency of scheduled runs accordingly.

According to Claude’s reports at the end of each session, if I were paying for the use of Claude models through the API instead of my subscription, each book would cost between about $20 and $50 dollars to convert to text using this workflow. That’s more than I would be willing to pay.

Tom Gally

November 22, 2026

## Initial prompt to Fable 5.2

The connected repo travel-books, which I created just now, is for a new long-term, open-ended public project. The goal of the project is to create and publish to the public domain highly accurate and readable digital versions of first-person nonfiction travel books written and published in English before 1914. The books can be from any era, by any author or authors, and about travel to or in any part of the world. For the time being, the conditions for choosing books are as follows:

- A high-quality, complete scan of the book is available on the Internet Archive. The entire book must be readable and convertible to digital text, with no text or illustrations that are missing or obscured. Before a book is digitized, its quality and completeness must be checked. If one version at IA is inadequate, another scan at IA may be used instead if suitable.
- No digital version of the book's text (other than the IA's own OCR version, and other than brief excerpts) is already available on the Internet (such as on Project Gutenberg).
- No versions of the book, other than brief excerpts, were published in print after 1914.
- The books will be chosen by Claude, usually on its own using its own judgement and taste though also through occasional consultation with me. Priority will be give to publishing a variety of interesting and readable travel books that are not easily available anywhere except in libraries or in scans. My goal is to create a resource for modern readers to discover travel books from the past that they can enjoy reading, learn from, and do research based on.

The conversion to text form will be done by Claude models through my subscription. Other companies’ models will be used through OpenRouter only when a second opinion is necessary about difficult scans; the maximum OpenRouter spend per day for this project is $3.00. The text conversion will use a workflow developed and continuously improved by Claude for this project. The starting point for that workflow will be the one currently being used in my pdf-to-epub project (which I have attached to this session, but which will not be attached to future regular sessions of this project). The skills and guidelines for this project's text conversion will initially be based on those pertinent to English in pdf-to-epub but may evolve over time. The continuous improvement of the workflow will also be based on the system in pdf-to-epub, but that improvement process will be polished and improved independently for this travel-books project. Books that have already been digitized and published for this project may be revised and updated later if errors are found. Even if no specific errors have been found, a book might be processed again if any of the following occurs: a cleaner scan is found; the conversion workflow improves enough that a new pass is likely to correct a significant number of errors; or the style guidelines for books published through this site have evolved significantly and the books scanned earlier now deviate from them enough to be apparent to readers.

The digital versions will be published through this repo's website (GitHub Actions is now turned on for Pages). For the time being, the site will consist of the following:
- A landing page for the project with an index to the books already published and those in the queue to be later converted and published
- A separate landing page for each book. This page has bibliographic information about the book, a brief summary, download links for EPUB and ODT versions of the book, and links to the HTML version (chapter by chapter, usually). The EPUB and ODT versions will have, in general, the same text and paragraph styles for all books, though additional styles can be defined for individual books as necessary.
- An HTML version of each book, divided into chapters or other appropriate divisions; this version is intended for casual readers. The HTML versions of all books in the project share common CSS and (if necessary) JS. No external dependencies are used.
- A link to the landing page for the book at the IA and, if possible, an in-browser viewer for flipping through the scanned pages at the AI.
- A link to a JSON version of the book's text. This JSON version will be the base version for the EPUB, ODT, and HTML builds, so it contains the most complete version of the digitized text. It will, for example, contain the text for parts of the books, such as front matter and back matter, that are not included in the EPUB, ODT, or HTML versions, which are intended for human readers. This will allow the JSON to be used by scholars who need more information about the book.

All of the text written by Claude for the site will be plain and minimal, with no PR-sounding elements. The website design will also be straightforward, accessible, easily navigable, and responsive, with no attempt to be eye-catching or fancy.

As the site grows, other features may be added later, such as a topical index to the books.

Claude will obtain the necessary files for each book's digitization from the IA. To avoid accessing the IA's servers repeatedly for the same files and to keep this repo from getting too large, Claude will save the necessary files to the folder "Travel Books" in my Google Drive account and access the files from there when processing books. The public URL for that folder is (redacted). Before you start setting up this project, confirm that you can access that folder, save files to it, and create subfolders within it. My Google Drive account currently has over 4 TB of free space available.

If you have any questions about this project, please ask me now. After the project is set up and ready to go, I will create a scheduled Routine that will point Claude to a RESUME.md prompt at the repository root. For the time being, the routines will be run by Opus 5.5, which may assign work to subagent or headless instances of Haiku, Sonnet, or Opus. This session now is being done by Fable 5.2 only because it is the initial session; Fable will not be used in the future without my explicit permission.

I will adjust the frequency of the Routine firing after I have had a chance to monitor the token consumption. For the time being, I expect that the Routine will run once or twice a day.

This project is open-ended and has no fixed goal. I hope to keep it running for months or years. I will wait a few weeks before publicizing it, at which point I might get a domain name for it. For the meantime, it will be served from the GitHub repo with the GitHub URL.

## Example of a follow-up prompt given to Fable 5.2 a few days later

In this session, make the following tweaks and improvements to this project. This session is being run by Fable 5.2; future scheduled sessions will continue to be handled by Opus 5.5. If the tasks below cannot be finished in the current session, add them as appropriate to the to-do list for future scheduled sessions. I have turned off the routine temporarily while you work on these tasks, so there is no danger of conflict. I will turn it back on after you finish.

(1) The body text of Diary of the Rajah of Kolhapoor is a single chapter, which makes it difficult to navigate on a web page. In the case of this book and other books without chapter divisions, divide the body text into sections of appropriate length, give an appropriate title to each section, and make each section a separate webpage. Note that you have done so in the book index page. This new divisioning applies to the web, epub, and ODT versions of the book. The JSON should continue to be based the original structure (while noting the later divisions that you have decided as well).

(2) On each book's index page, change the link destination of the book image. Currently, the destination is the first page of the book. From now on, I would like it to be the first chapter or the first page of the book's body text. In other words, I want the user to be taken to the start of the book's narrative rather than to a preface, introduction, dedication, etc. The page should be scrolled so that "Chapter I" (or whatever) is the first line. Make this change both retroactively and going forward.

The link for "Read on this site (contents below)" further down on the book index page should continue to be the first page of the book. (Note that the first page will change for most books; see (5) below.)

(3) On the index.html page, add the following sentence after "Each can be read on this site or downloaded as EPUB, ODT or JSON.": "The site now contains XX books, with more being added every day."

The number XX should be updated whenever the number of books on the books.html page is updated, so the two numbers should match.

Move "About the project." to a new paragraph below the paragraph that ends "...about Japan than about other countries." and change it to "More about the project."

Also, on the same page, remove the heading "Travel Books" that is immediately below the carousel. The project title appears in the visible header; that should be enough.

(4) In text written by Claude for this site, use series commas and smart apostrophes and quotation marks (except in code excerpts, such as on the page explaining the JSON format). Fix the usage on all of the current pages, including the About page and all of the book summaries on the book index pages, and adopt this style convention going forward.

(5) For all books, include the text of the title page in the transcription that appears in the webpage, OCR, and EPUB. The title page will be the new first page of the book. I want the full title as it appears on the title page, the author's name as it appears on the title page (if it does), the publisher, the city, etc. to appear in the digital versions as in the printed one. If elements on the title page are centered, center them in the digital version as well. Currently the first page for most books is a preface or other front matter; this goes against the reader's expections for the first page of the book will be the title page.

If any text appears before the title page, such as a half title, printer's advertisements, etc., continue to exclude that from the built versions.

(6) I've noticed that in the HTML version of several books the paragraph immediately after an illustration begins unindented, even though the paragraph in the original scan is indented. One example is the paragraph beginning "In the Banda Oriental there is a fixed maximum amount..." in Zephyrus, which has a flush-left first line, even though the paragraph in the scan is indented. The paragraph indenting should follow the original scan unless there is a good reason to ignore that.

(7) Currently, scheduled routines for this project start to wind down after the context reaches 40%. If there is no danger of the accuracy of Opus's work being adversely affected, increase that threshhold to 50% or 60%.
