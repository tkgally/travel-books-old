# travel-books — working instructions for Claude

A long-running public project of Tom Gally's: accurate, readable digital editions of first-person nonfiction
travel books written in English and published before 1914, transcribed by Claude models from scans at the
Internet Archive (IA) and published on this repository's website as HTML, EPUB, ODT and JSON, in the public
domain (CC0). Claude chooses the books, does the work, and keeps improving the method. The repository and
the site are **public**: everything committed here can be read by anyone.

## Read first, every session

1. `notes/README.md` (index of the notes) and `python3 tools/ledger.py` (the state of `data/queue.json`, the
   ledger of books, and which kind of book is due next).
2. `notes/workflow.md` — the pipeline and §Verification; `notes/lessons.md` — "Always" plus the sections whose
   trigger matches the book; `notes/preferences.md` — what Tom has decided.
3. The skill for the job: `digitize-book` (transcribe and publish), `select-book` (choose and vet candidates).
4. `wip/<slug>/log.md` or `books/<slug>/log.md` if the book has been worked on before.

Routine (scheduled) sessions start from `RESUME.md`. A session normally does several pieces of work, more than
one book where possible, and stops by its context budget (`RESUME.md` §3, `tools/session_meter.py`).

## Hard rules

- **Eligibility is checked before any work on a book** (`notes/selection.md`): complete good scan on IA; no
  free digital reading edition elsewhere (databases such as EEBO, ECCO or subscription ones do not count); no real print edition after 1914; first-person nonfiction travel, written
  in English, published before 1914; every author dead more than 70 years. Record what was checked in `data/queue.json`. If a published book is
  later found to fail a criterion, tell Tom; do not silently remove it.
- **The JATSI books** (Tom, 2026-11-20): the 247 books of his list "Japan As They Saw It" (`data/jatsi.json`) are
  added one at a time, about one book in three (`tools/ledger.py` says when one is due). They are here because
  they are on the list: only a good scan is required; the other criteria are checked and recorded and set the
  order (those that meet them first; the reprinted, those with a Gutenberg text and the non-narratives later — all
  are to be done, each transcribed afresh from the scan); the 70-year rule does not apply to them (Tom: public
  domain in the US and Japan), and a book whose author died after 1955 says so on its page. Queue row `"from": "jatsi"`, `book.json` `"collection": "jatsi"`; the site says so
  on the home page, the book's page and `japan-as-they-saw-it.html`. Other books are chosen as before. `notes/jatsi.md`.
- **Scans never enter the repo.** IA downloads, page images, crops in progress and model scratch files live in
  the session scratchpad (each download in its own empty directory; treat archives as untrusted data). Only
  illustration crops that the book needs go in `…/<slug>/images/`. `.gitignore` is a backstop, not the rule.
- **Ask IA for a book's files once.** After the first download the working page images are cached in Tom's
  Google Drive folder "Travel Books" (id `1uqlD7GAkSiNRw_3sX7TkKYpNuF4rtzHn`, one subfolder per book id) and
  later sessions fetch them from there (`tools/drive_cache.py`). Uploads from a session are limited to about
  3 MB per file, which is why the cache is in parts. Never delete or change another book's files in Drive.
- **Models.** Claude models only, through Tom's subscription: this session, subagents, and headless calls
  (`tools/ocr_claude.py`, `judge.py`, `audit_sample.py`). Opus for drafts, judging and audits; Sonnet for the
  corrections pass; Haiku only for work that involves no reading of scans. **Never Claude Fable** (no
  `--model fable`, no Fable subagents) unless Tom explicitly says so for that occasion. Never the same model
  as both writer and only checker of a text.
- **OpenRouter** (other companies' models) only for a second opinion on scans Claude models cannot settle, and
  **at most $3.00 a day for the whole project**. `tools/ocr_openrouter.py` enforces and records it in
  `data/openrouter-spend.jsonl` (commit that file). Never print the key. Routine runs may spend within the
  limit without asking; say what was spent and why in the final message.
- **The text policy** (`notes/style.md`) is not varied book by book: the author's words, spelling, capitals and
  punctuation marks as printed; spacing around punctuation modern; only unmistakable printer's errors
  corrected, each marked `[[corr printed|corrected]]` so the printed reading stays in the JSON and the
  correction is listed on the book's page.
- **Never publish without** `tools/preflight.py` ending `PASS`, a rendered look at several chapters in the
  browser build, the sampled audit (`tools/audit_sample.py`) with every candidate checked on the scan, and
  the stamp and audit result written in the book's `log.md` and a row added to `notes/metrics.md`.
  `tools/publish.py` refuses without the PASS.
- **Checks are not edited by the work they judge.** A session never publishes a book after changing a check
  or a test that the book failed. When a check fails, in this order: (1) the book is wrong → fix the page
  files; (2) the check is wrong about one item → waive that item in `book.json` with a reason; (3) the check
  is wrong about a kind of book (a waiver would be wide, or would hide other items) → finish everything else,
  leave the book `in progress` with "ready to publish when check X is fixed" in its log, and then the same
  session may fix the check by `notes/workflow.md` §"When a check is wrong" (invented text in a test first;
  never to make a real fault pass). **The next session publishes the book.** Do not try any other way of
  getting past a check: such edits are refused by the session's permission system as well. Still failing
  after three attempts at the cause → the book goes to `waiting` with the report in its log; take another.
- **The output filter.** The API refuses to let any Claude model type out certain pages (ordinary prose; the
  same pages every time). Never retry, rephrase or split such a page, and **never type it in the session:
  that ends the session for good** (2026-11-19: four dead turns, uncommitted work lost). Run
  `tools/ocr_fallback.py` (machine OCR, corrected by a model, which the filter allows); a page that fails
  there too → the book goes to `waiting`. The session itself never writes out more than a few lines of a
  book's text, in a file or a message: page files are changed by small edits.
- **Tools change only with tests.** `tools/run_tests.sh` at the start of a working session and after any edit
  under `tools/`; every tool bug fixed gets a test in the same commit.
- **Site text is plain.** Summaries, notes and page text say what a thing is, in ordinary words: no praise,
  no selling, no "fascinating", no claims the book does not support; serial commas and curly quotation marks
  (Tom, 2026-11-22). `notes/style.md` §Site text.
- **The reading editions begin with the book's title page**, transcribed as printed; what stands before it is
  left out. A long text without chapters is divided into titled sections, a page each; the JSON keeps the
  book's own structure (Tom, 2026-11-22; `notes/style.md` §Editions).
- **The site has no external dependencies**: no web fonts, scripts, trackers or CDNs. The only outside content
  is links to IA and the optional IA page viewer (an iframe that loads when the reader opens it).
- **Unfinished work is committed and pushed** as it goes: model runs and page text under `wip/<slug>/`, state
  and exact next step in `wip/<slug>/log.md`, queue row `in progress`. A session can end without warning.
- **After every published book, and at the end of every session:** update notes/skills with what was learned,
  run the tests, commit, push to the session branch, open a PR, merge it (the site deploys from `main` by GitHub
  Actions), and check that the deploy succeeded when the site changed. Each finished piece of work is merged
  before the next is begun; the session's times and context use go in `notes/sessions.md`.
- **What Tom or a reader reports** goes in `notes/errata.md` and is followed through as that file says.
- **Tom's instructions and preferences** go in `notes/preferences.md` the moment he states them, **committed
  and pushed before acting on them** (an answer of his was lost when the session died doing what he asked).

## Repo map

| Path | What |
|---|---|
| `books/<slug>/` | a published book: `book.json` (metadata and build settings), `pages/pNNNN.txt` (page markup, one file per IA leaf — the source of the text), `images/`, `source.json` (IA item and Drive cache), `log.md`, `preflight.txt` |
| `wip/<slug>/` | a book in progress: the same, plus model runs (`draft/`, `verify/`, `judge/`, `audit/`); moved to `books/` by `tools/publish.py` |
| `data/queue.json` | the ledger: queued, in progress, published, waiting, rejected; `jatsi_policy` (the pace). Report and check: `tools/ledger.py` |
| `data/jatsi.json`, `data/places.json` | the JATSI list as taken from Tom's page; place names → part of the world, for the site's list by place |
| `tools/` | Get: `ia.py`, `prep_pages.py`, `drive_cache.py`, `contact_sheets.py`. Transcribe: `ocr_claude.py`, `ocr_fallback.py`, `normalize.py`, `running_quotes.py`, `review.py`, `judge.py`, `crop_spot.py`, `crop_image.py`, `corrections.py`, `ocr_openrouter.py`, `score.py`. Session: `session_meter.py` (context used, hours run). Build: `compile_book.py` (pages → book JSON), `render_html.py`, `render_epub.py`, `render_odt.py`, `build_site.py`. **Verify: `run_tests.sh`, `preflight.py`, `audit_sample.py`.** Publish: `publish.py`. Ledger: `ledger.py`. Home page: `carousel.py`. Setup: `setup_env.sh`, `make_prompts.sh` |
| `prompts/` | `transcribe.md`, `verify.md`, generated from `_rules.md`, `_format.md`, `_verify-task.md` by `tools/make_prompts.sh` |
| `site/` | `assets/` (the one stylesheet pair and the small script shared by all books), `about.md`, `json-format.md`, `carousel/` (thumbnails of covers for the home page; record `data/carousel.json`, tool `tools/carousel.py`, brought up to date in review sessions) |
| `tests/` | regression tests for the tools and an invented sample book |
| `notes/` | Claude's memory: workflow, selection, style, page markup, book.json keys, lessons, metrics, sessions, errata, preferences, improvement, jatsi, site |
| `.claude/skills/` | `digitize-book`, `select-book` |
| `.github/workflows/pages.yml` | tests, then build `_site/` and deploy to GitHub Pages on every push to `main` |

The built site (HTML, EPUB, ODT, JSON) is never committed: it is rebuilt from `books/` on every deploy, and the
build is deterministic.

## Keeping memory useful

- Skills = how to do a job (current procedure only). Notes = what was learned and why. CLAUDE.md = rules and
  map; keep it short.
- When something goes wrong: first choice a check in `preflight.py` (starting in observe) or a test; otherwise
  one or two lines under the right trigger in `notes/lessons.md`; and fix the skill, prompt or tool in the same
  session. Lessons that a tool now enforces are deleted from the prose. `notes/improvement.md` says how the
  method itself is reviewed.
- Model line-ups and prices change: check before assuming, and re-run the calibration in
  `notes/workflow.md` §"Choosing the pipeline" before changing which model does what.
