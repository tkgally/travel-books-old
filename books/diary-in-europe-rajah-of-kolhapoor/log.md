# Diary of the Late Rajah of Kolhapoor, during His Visit to Europe in 1870 — Rajaram, Rajah of Kolhapoor; ed. Edward W. West (1872)

IA: diaryoflaterajah00rajarich (University of California Libraries; 200 leaves, 400 ppi, greyscale). Other scans
looked at: diarylaterajahk00unkngoog (Google scan of a Michigan copy, 189 leaves; the queue's first choice — the
UC scan is a library scan at full greyscale, so it was used instead); in.ernet.dli.2015.72750 and
india.history.resource.85345 (Indian library scans, not opened).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv searched for
"kolhap"); a web search for the title finds only the 1872 edition, a Forgotten Books "Classic Reprint" (print on
demand) and a Marathi translation (Shivaji University, 2025: not an English edition). Written in English by the
Rajah (Introduction, p. xx: "The Diary now presented to the public was written by the Rajah in English").
Authors' deaths: the Rajah died at Florence on 30 November 1870 (the book). The editor, Capt. Edward W. West,
Bombay Staff Corps, Assistant Political Agent at Kolhapoor: **death date not found** (two web searches; not the
orientalist E. W. West, 1824–1905). A captain of the Staff Corps in 1870 had about twelve years' service, so was
born about 1840 or earlier and cannot have been alive in 1955. Tom, 2026-11-19: publish; standing rule that a person whose death date is unknown died before age 100
(`notes/selection.md` rule 5). The Supplement
quotes at length from an article in *Good Words* (June 1871) by Lady Verney (Frances Parthenope Verney, d. 1890).

## Status
Published, version 5 (2026-11-20). Nothing pending.

## Page map
p0001 front cover (decorated cloth) · p0002 front pastedown with bookplate · p0003–p0006 endpapers/flyleaves ·
p0007 printed presentation slip with a handwritten addressee ("To Lt. Col. H. C. Rawlinson K.C.B."), signed
Edward W. West · p0008 blank · p0009 IA card (not part of the book) · p0010 frontispiece portrait of the Rajah ·
p0011–p0012 blank · p0013 engraved title page with vignette "Gateway of the Palace, Kolhapoor." · p0014 blank ·
p0015 printed title page · p0016 blank · p0017 contents · p0018 blank · p0019–p0038 Introduction = printed v–xxiv
(offset: p0019 = v) · p0039 blank · p0040 plate, portrait (no caption seen at sheet size) · p0041 = printed 1
(offset 40) Diary 1–92 · p0133 = 93 Postscript (the contents says 94) · p0136 blank · p0137 Appendix divisional
title with list of appendices (97) · p0139 = 99 Appendix I · … · p0172 = 132 Appendix VII · p0173 plate
(photograph of a boy, presumably the adopted successor) · p0174 blank (plate verso) · p0175 = 133 · p0177 =
135 Supplement · p0189 = 147 end, signed and dated · p0190 printer's imprint · p0191 blank · p0192 library
date slip · p0193–p0201 endpapers, back cover, colour cards.
Scan check: all five contact sheets looked at 2026-11-19; full size: p0017, p0060; problems: none found (folios
to be confirmed by preflight `folios`).

## Decisions
- Transcribed p0007–p0190. The presentation slip (p0007) is printed matter issued with the book: JSON only, kind
  `front` (assumed).
- Cover image: the engraved title page p0013 (the cloth cover is dark with only a small stamp).
- Judge report checked on crops: p0170 the judge (Opus, "sure: high") kept the draft's "Chutraputee"; the scan
  has "Chutraputtee", as the verifier said: corrected. p0186: running head "SUPPLEMENT." dropped (verifier right).
  p0013: title line in capitals with large initials, typed as the verifier/judge read it. p0190 imprint: left.
- Structure: Introduction, Diary (one division: the book has no chapters), Postscript, Appendix (one division;
  each appendix a `##` section, its printed title folded into the heading line, since `[[subtitle]]` after `##`
  renders as a plain paragraph), Supplement (Lady Verney's article as `##` section in ordinary paragraphs, though
  printed in smaller type: it has its own heading and quotation marks; assumed). p0137 (list of the appendices)
  is a `contents` division, JSON only. Running heads "APPENDIX." typed as headings by the drafts removed.
- Two `*` references to one footnote on p0037 and p0049: new markup `[[fnref * again]]` (compiler, HTML, ODT;
  test). Preflight's JSON→ODT conservation reads the ODT cross-reference mark as text: **waived** in book.json;
  `tools/preflight.py` `odt_streams` should skip `text:note-ref` like it skips frames — a change to the check,
  so for a session not working on this book (the attempt in this session was refused, rightly).
- Page joins: all 8 `[[cont]]` after a full stop checked on the scan: each page begins flush left, so they are
  continuations. Hyphen joins: dis-cussion, intro-duced, Canter-bury joined; "rectangular-shaped" kept
  (`keep_hyphens` p0167). Contents look list: the appendix headings are worded differently from the printed
  contents (checked on the scan: II. "The Durbar at Poona.", III. "Laying the Foundation-Stone of the Kolhapoor
  High School."); left as printed.
- West is an editor: `"role": "editor"` (new key; shown "edited by").
- The Supplement says the design on the cloth covers is copied from the Rajah's note-paper; the cover itself
  (p0001) was not cropped. Possible addition for a later version.
- Day ordinals ("20<i>th.</i>—"): the drafts put the full stop inside or outside the italic; made uniform
  (inside, as most pages had it), 2026-11-19.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-19 | opus | p0007–p0190 (184; p0009 output deleted) | 12.54 | no errors; 229 s wall with 6 workers |
| Corrections | 2026-11-19 | sonnet | 183 | 6.07 | 22 changes proposed (7 words, 12 markup, 3 punctuation), 1 not applied |
| Judge | 2026-11-19 | opus | 10 spots on 8 pages | 0.38 | sided with draft 7, verifier 2; 9 to look at |
| Audit | 2026-11-19 | opus | 6 (p0047, p0080, p0089, p0096, p0108, p0122) | 0.37 | recall 30/30; 0 other differences |
| **Total** | | | | **19.36** | no OpenRouter |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-19 | preflight PASS: diary-in-europe-rajah-of-kolhapoor v1 — 0 to fix, 1 waived; to look at: hyphen-joins 3, joins 8, contents 5 — tools@5c27d52 2026-11-19 | 6 pages, recall 30/30, 0 real errors | First publication. Waiver: conservation JSON→ODT (second reference to a footnote, p0037, p0049) |
| 2 | 2026-11-19 | preflight PASS: diary-in-europe-rajah-of-kolhapoor v2 — 0 to fix, 1 waived; to look at: hyphen-joins 3, joins 8, contents 5 — tools@6c5ee39 2026-11-19 | copied from v1 (text unchanged) | Frontispiece shown in the reading editions (new book.json key `frontispiece`); found on the live site after v1 |
| 3 | 2026-11-19 | preflight PASS: diary-in-europe-rajah-of-kolhapoor v3 — 0 to fix, 0 waived; to look at: hyphen-joins 3, joins 8, contents 5 — tools@15199cb 2026-11-19 | copied from v1 (text unchanged) | Waiver dropped: preflight now skips the ODT cross-reference (`text:note-ref`) for a second mark to one note (session of South by West). |
| 5 | 2026-11-20 | PASS — 0 to fix, 1 waived; to look at: hyphen-joins 1, contents 5 — tools@1653f9e | record copied (text unchanged) | summary and omitted_from_reading: four straight apostrophes curled (new check site-text) |
| 6 | 2026-11-20 | preflight PASS: diary-in-europe-rajah-of-kolhapoor v6 — 0 to fix, 1 waived; to look at: hyphen-joins 1, contents 5, accents 2 — tools@9de0b2b 2026-11-20 | record copied (text unchanged except listed fixes) | Accents checked on the scan at the review after twenty books (new preflight list `accents`). p0184: “Dŭrbar” was a blot over the u, read as a breve; now “Durbar” as printed elsewhere. |

Waiver added 2026-11-19 without a new version (text and editions unchanged): `leaves` p0009, the IA card left
out on purpose, when the leaves check became enforced.
| 4 | 2026-11-19 | PASS — 0 to fix, 1 waived; to look at: hyphen-joins 3, joins 8, contents 5 — tools@6b8af86 2026-11-19 | as version 1 (text unchanged) | contents: entries inside the diary (dates and places), appendices by title; ODT contents list (errata 2026-11-19) |

## Known issues
- Waiver above (an artefact of the check, not of the text).

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
