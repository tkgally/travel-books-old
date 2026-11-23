# Flying Leaves from East and West — Emily Pfeiffer (1885)

IA: flyingleavesfrom00pfeirich (University of California Libraries, Bancroft copy; 322 leaves, 500 ppi, greyscale).
Other scans looked at: none (this one is clean and complete).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv has only Ida Pfeiffer's
books); web searches of the title and of a sentence from p. 73 ("The hotel—in form of an elephant, with an
observatory in the howdah") find no text and no edition. Emily Pfeiffer 1827–1890 (Welsh-born poet).

## Status
**Published, version 2, 2026-11-19** (contents redesign, `notes/errata.md`): the two part titles ("From the East", "From the West") are now parts and the Leaves nest under them in the contents (compiler fix); each Leaf's entry adds, in the editor's words, its places or subject (Tom asked, 2026-11-19; book.json `divisions` `toc_title`); every edition gets a generated contents (the ODT for the first time).
**Published, version 1, 2026-11-19.** The five leaves refused by the output filter (p0116–p0118, p0128–p0129) came by
`ocr_fallback.py` and went through stage 3 in a scratch directory: Sonnet corrections pass, no change proposed on any of
them, so 0 spots for the judge; the session compared all five with the scan (reading only): they agree, apart from the
spacing of "John P—— and" (p0116), corrected; `[[cont]]` at p0117, p0118, p0119, p0129, p0130 right, p0116 and p0128 begin
new paragraphs (indented on the scan); italics on p0118 (*cuisine*, *hors d’œuvres*) as printed. Same spacing fix at
p0100 ("E—— delivers", seen on the scan). Second audit on the five: 25/25, 0 other differences (`audit-fallback/`).
`notes_on_text` names printed pages 106–108 and 118–119 as first read by OCR.

## Page map
p0001 front cover (plain cloth) · p0002 front pastedown, Bancroft Library plate · p0003–p0005 endpapers, blank ·
p0006 IA card · p0007 half-title "Flying Leaves from East and West" · p0008 blank · p0009 title page ·
p0010 verso (library stamps, Leadenhall Press device) · p0011 = printed [1] part half-title "Flying Leaves. From the
East." · p0012 blank · p0013 = printed 3 (offset 10, constant to the end).
From the East — Leaves begin: I p0013, II p0023, III p0038, IV p0049, V p0057, VI p0067; ends p0079 (69).
p0080 blank · p0081 part half-title "Flying Leaves. From the West." · p0082 blank.
From the West — Leaves begin: I p0083 (73), II p0098, III p0114, IV p0126, V p0138, VI p0150, VII p0163,
VIII p0169, IX p0178, X p0190, XI p0199, XII p0215, XIII p0227, XIV p0237, XV p0242, XVI p0255, XVII p0272,
XVIII p0283, XIX p0297; ends p0312 (302, "The End.").
p0313–p0323 endpapers, back cover, colour cards (p0319 not in the archive's numbering).
No contents page, no preface, no index, no advertisements, no plates. Footnotes seen on p0030, p0150, p0171,
p0187. Verse quotations e.g. p0083, p0132, p0181, p0312.
Scan check: all 9 contact sheets looked at 2026-11-19; full size: p0009, p0079–p0083, p0187; problems: none.

## Decisions
- Cover image: the title page (p0009, full size); the cloth cover is plain.
- Structure (assumed): two parts, "Flying Leaves. From the East." and "… From the West." (the printed part
  half-titles, p0011 and p0081), each with its Leaves as chapters (both parts number from Leaf I).
- Chapter openings are a drop capital followed by full-size capitals ("THE bazaars"), so typed as plain capitals;
  the two drafts that had `O<sc>ur</sc>` / `T<sc>wo</sc>` (p0038, p0138) corrected. The 9 corrections-pass
  proposals to `<sc>` openings and 3 on p0010 were rejected by the judge and the scan agrees.
- p0207: printed ‘I guess … long,” (single opening, double closing quotation mark): `[[corr ‘|“]]`.
- p0232 "pistils and stamen": as printed (judge and scan), kept.
- p0133: no `[[cont]]` after the verse at the foot of p0132 (lessons: a sentence resuming after a set-off block).
- The six `[[cont]]` after a full stop (p0025, p0054, p0079, p0130, p0135, p0141): first lines not indented on the
  scan; kept.
- keep_hyphens p0176: "counter-|check" (the author hyphenates counter-appeals, counter-excitements, counter-movement).
- Title-page monogram (p0009-1) and publisher's device (p0010-1) cropped; the IA blind stamp crosses the monogram.
- p0008 (blank) given a page file by hand.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-19 | opus | p0007, p0009–p0312 (305) | 19.04 | 5 refused by the output filter (p0116–p0118, p0128–p0129), each tried 3 times by the tool as it then was |
| Draft retry | 2026-11-19 (later session) | opus | the same 5 | 0.00 | all 5 refused again |
| Fallback draft | 2026-11-19 (diagnosis session) | tesseract + opus corrections | the same 5 | 0.28 | all 5 done; 2–7 corrections each; Sonnet draft of the 5 tried first: refused |
| Corrections | 2026-11-19 | sonnet | 300 | 9.40 | 13 word and 3 markup changes, all applied |
| Judge | 2026-11-19 | opus | 13 spots on 11 pages | 0.50 | sided with the draft 13/13; scan agrees |
| Audit | 2026-11-19 | opus | 6 | 0.34 | 30/30 planted errors found; 0 other differences |
| Corrections, fallback pages | 2026-11-19 | sonnet | 5 | 0.16 | NONE on all five (`verify/log-fallback.jsonl`) |
| Audit, fallback pages | 2026-11-19 | opus | 5 | 0.29 | 25/25 planted errors found; 0 other differences |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-19 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 18, joins 5 (read) — tools@75f0f85 | 30/30 and 25/25 (fallback pages); 0 real errors / 11 pages | first publication; five pages by the OCR fallback |
| 2 | 2026-11-19 | PASS — 0 to fix, 0 waived; to look at: hyphen-joins 18, joins 5 — tools@6b8af86 2026-11-19 | as version 1 (text unchanged) | contents: parts nest their Leaves; places or subject in each Leaf entry; ODT contents list (errata 2026-11-19) |

## Known issues

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
