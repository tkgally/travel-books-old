# The Land of the North Wind; or Travels among the Laplanders and the Samoyedes — Edward Rae (1875)

IA: landofnorthwind00raee (Princeton Theological Seminary Library; 390 images, 360 ppi, colour).
Eligibility: queued 2026-11-20 (Opus subagent); re-checked at the start 2026-11-20: not in pg_catalog.csv; a web search
of the title finds HathiTrust and Doria (Helsinki) page images and PDFs only, contemporary reviews, and a Polar Record
article on the book's publication; no text edition. Author born 1847, death date not found: rule 5 met by Tom's rule
(selection.md). Plates not credited to an artist. Taken up 2026-11-20.

## Status
Published, version 1 (2026-11-20). Nothing pending.

## Page map
Scan check 2026-11-20 (Opus subagent: all 10 sheets; folio of every text leaf on crops; full size 4, 5, 8, 11, 13,
15–26, 27, 128, 194, 245, 257, 281, 382–384): PASS. p0128 (p. 102) faint and slightly soft but readable.
p0000 colour card (hidden) · p0001 cover (gilt skier) · p0002–p0003 board, bookplate · p0004 flyleaf · p0005 half-title
(i) · p0006–p0007 blank · p0008 frontispiece "Sledging over the Tûndras to Karoléon" (sideways) · p0009–p0010 hidden
(camera shots) · p0011 title (iii) with vignette (Samoyede costume) · p0012 blank · p0013 dedication (v) · p0014 blank
· p0015–p0016 To the Reader (vii–viii), epigraph · p0017–p0024 Contents (ix–xvi; chapter summaries, repeated at the
chapter heads) · p0025 List of Illustrations · p0026 Errata · p0027 = p. 1 (offset 26 to p0192 = p. 166) · p0193 blank
· p0194 plate "Ferry on the Dwina River" (sideways) · p0195 = p. 167 (offset 28 to p0280 = p. 252) · p0281 plate
"Samoyede Village" (sideways) · p0282 blank · p0283 = p. 253 (offset 30) … p0382 = p. 352, The End, imprint ·
p0383 folding map (Russian Lapland and the shores of the White Sea) · p0384 blank verso · p0385–p0388 endpapers,
back cover · p0389 hidden.
Chapters (leaf/page): I 27/1 · II 32/6 · III 49/23 · IV 68/42 · V 93/67 · VI 110/84 · VII 124/98 · VIII 140/114 ·
IX 157/131 · X 170/144 · XI 175/149 · XII 191/165 · XIII 211/183 · XIV 233/205 · XV 253/225 · XVI 276/248 ·
XVII 300/270 · XVIII 319/289 · XIX 335/305 · XX 346/316 · XXI 360/330 · XXII 373/343. No appendix, index or advertisements.
Verse epigraphs on 27, 175, 257, 274, 317, 341, 364 (others possible). Samoyede vocabulary, two columns, pp. 215–220
(p0243–p0248), italic words with diacritics. No head- or tail-pieces (small rules only). No Cyrillic seen.
Errata (p0026): p. 24 l. 5 from bottom I went → we went (p0050); p. 43 l. 9 means → meant (p0069); p. 127 l. 6 from
bottom quay on → quay in (p0153); p. 150 last line we did → we do (p0176); p. 161 l. 8 hung → hang (p0187);
p. 291 l. 9 I accuse them → I accused them (p0321).

## Decisions
- Drafted p0005, p0008, p0011, p0013, p0015–p0192, p0194–p0281, p0283–p0383; blanks p0006, p0007, p0012, p0014, p0193,
  p0282 waived; covers, boards, endpapers not transcribed.
- Judge: 22 spots (draft 13, verifier 7, neither 2); most were accents and contents heading levels.
- **Accents** (the book's weak spot): all accented words listed by base form; 23 groups spelled differently in
  different places went to an Opus subagent on crops. The book prints a single wide circumflex over "ou" (knout,
  moujik, Tjouma, Moudiuga, Samoyede words); the readers took it for an acute, grave or breve on one letter. Given as
  "oû" throughout (assumed: a convention; said in `notes_on_text`); 35 pages changed. Also Aåwasaksa → Aâwasaksa
  (5 pages), Kanúshin → Kanûshin (p0300), Lúûkos → Lûukos (p0130), "tchelég a" → tcheléga (p0202), the frontispiece
  caption Tûndras, five vocabulary words on p0243. Real variants in the book kept: Solómbola/Solômbola,
  Pietasâari/Piétasâari, tchaï/tchâi. Not checked: Sŭuari (one place).
- Printed contents (p0017–p0024): re-set as plain lines (centred chapter number, topics with page reference); "PAGE"
  heads and table rows removed; page numbers the draft had left bare made `<pref>`.
- Book title above Chapter I (p0027) left out (as in *A Jaunt in Japan*).
- Errata applied as `[[corr]]`: p0050, p0069, p0153, p0176 (p. 150, last line: "we did not mind"), p0187, p0321.
- Printer's error p0132 "makiug" (turned n; the draft had silently corrected it; found by the audit) → `[[corr]]`.
- p0272: two musical figures in the line (a crotchet marked flat, one marked sharp: the slang B-flat = bug,
  F-sharp = flea) given as ♭ and ♯, said in `notes_on_text`.
- p0015 "may of the most humble nature" is printed so (no "be"); kept.
- keep_hyphens p0094 (Kauto-keino), p0188 (long-cassocked).
- Contents: the printed summaries in full (`toc.subtitles all`), short titles "Chapter N".
- A spot-read subagent reported 11 lines missing on p0317; they were in the page file (its view was cut). An
  `ocr_fallback.py` re-reading of the page, made before that was seen, matched the page file and was discarded.

## Runs
| Run | Model | Pages | Cost |
|---|---|---|---|
| draft | Opus | 371 | $24.33 (0 refused) |
| corrections | Sonnet | 371 | $12.09 (16 word, 6 punctuation, 11 markup changes) |
| judge | Opus | 22 spots | $0.64 |
| audit | Opus | 6 (p0065, p0132, p0152, p0167, p0192, p0223) | $0.35: 30/30; 3 candidates, 2 real (p0192 tcheléga ×2, p0132 printer's error) |
| audit, 20 more | Opus | 20 | $1.17: 100/100; 2 candidates, none real (the left-out book title on p0027) |
| fallback re-reading p0317 | tesseract + Opus | 1 | about $0.10 (log discarded with the run) |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-20 | PASS — 0 to fix, 6 waived (blank leaves); to look at: hyphen-joins 4 (real word breaks; Tchôr-naya at a line end) — tools@3982785 | 130/130 on 26 pages; 2 real errors (p0192, p0132), fixed | first publication; spot-read of special pages and accent check on crops (Opus subagents); rendered look at 390 and 1280, EPUB nav |

## Known issues
- Chapter heads XIII and XXI print some topics without the dash the contents page has ("household God Magnificent
  Daylight", "Midnight Sun A Rainbow", "Mezén. Formidable"); kept as printed, so the contents entries show them so.
- The numerals table (Chapter XIV) is a little wider than a phone screen and scrolls inside its box.
- Each contents entry is the chapter's whole printed summary (as the printed contents), long in an e-reader's menu.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
