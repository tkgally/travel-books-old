# Cordillera and Pampa — Isaac G. Strain (1853)

IA: cordillerapampa00stra (The Library of Congress; 306 leaves, 500 ppi).
Eligibility: re-checked 2026-11-22: a web search found only the HathiTrust record; Isaac G. Strain 1821–1857.

## Status
Published v1 2026-11-22.

## Page map
Leaf = printed page + 4 throughout (roman included). Hidden: p0000, p0305.
p0001 cover (marbled boards, no title) · p0002 LC bookplate · p0005 title page · p0006 verso (copyright, printer) · p0007 dedication · p0009–p0012 Preface (signed J. G. S.) · p0013–p0015 Contents (titles only) · p0017 p. 13 head title and Chapter I · chapters II p0028 … VIII p0101 … XVIII p0277 · text ends p0299 (p. 295) · p0300 Errata (12 entries) · p0301–p0304 blanks, cover.
**p0099–p0100 are a second scan of pp. 93–94 (p0097–p0098); pp. 95–96 are missing from this scan.** Taken from cordilleraandpa01stragoog (Harvard, Google) n100 and n101 as leaves p0100a and p0100b (`source.extra_leaves`); p0099 and p0100 waived.
No illustrations. 50–60 footnotes (* †), some long; tables pp. 123–124 and p. 142; journal entries with italic dates from Chapter XII; Spanish words printed mostly without accents.
Scan check: all 8 sheets, a dozen leaves at full size, folios followed (Opus subagent), 2026-11-22. Book's picture: the title page.

## Decisions
- pp. 95–96 from cordilleraandpa01stragoog (Harvard, Google) n100–n101 as p0100a–b (`source.extra_leaves`); p0099–p0100 (duplicates of pp. 93–94) waived. Both noted in `notes_on_text`.
- p0189 (p. 185) refused by the output filter: `ocr_fallback.py` (tesseract corrected by Opus), then the Sonnet pass, judge, a word-by-word spot-read and a second audit (4/4).
- The 12 printed errata applied as `[[corr]]`, located line by line on the scan by a subagent (three fall a line after the errata's count; "a comma for a colon" on p. 91 read as the colon after "Osorio"; "Revenous" for the errata's "reveuons").
- Printer's errors marked besides: tedicus, clusteriug, Religicn (heading), belonge duntil, ladics, eivil, surrouuding, succesful, morever, acknowlege; missing stops after "visit" (p0215) and "guitar" (p0246). Left as printed: impassible, mattrasses, certâin, depôt of th, Propbet, matte/matté, caña/cana.
- Type lost in print, inferred: "[[supplied to be]]" and "[[supplied cr]]edit" (p0052 note); "con[[supplied s]]isted" (p0209, letter lost at the faded edge of the scan).
- Table p0128: two commas read as full stops in the draft, fixed.
- Head title above Chapter I a `front` division (n 1); the title page typed line by line (7 lines of the title).
- Book's picture: the title page (the cover is plain boards).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-22 | opus | 296 | 21.23 | p0189 refused by the output filter |
| fallback | 2026-11-22 | tesseract + opus | 1 | 0.07 | p0189 |
| corrections | 2026-11-22 | sonnet | 296 | 10.23 | 13 word spots |
| judge | 2026-11-22 | opus | 16 spots | 0.65 | draft 15 / verified 1 |
| spot-read | 2026-11-22 | opus subagents | about 30 | – | errata located; table; title lines; misprints |
| audit | 2026-11-22 | opus | 6 + 1 | 0.42 | 29/30 and 4/4 (fallback page), 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-22 | PASS, 0 to fix, 1 waived; look: hyphen-joins 10 (real), folios 5 (broken digits, plus the added leaves), accents 6 (as printed), rare-forms 4 (laud, bating, ketch, colon: real words), serial-commas 2 (no lists), missing-stop 1 (verse) — tools@6193dfaa | 33/34; 0 real | Claude $32.60 |
| 2 | 2026-11-22 | PASS, 0 to fix, 1 waived — tools@2454027b | as v1 | printed “th” for “the” (p. 2) marked `[[corr]]`, reported by a reader (issue #169); no model calls |

## Known issues
- The long footnote on p0299 is printed in three paragraphs; the markup has one.

## 2026-11-23: pictures reduced

Every picture reduced to at most 1000 px on its longest side, JPEG quality 75 (Tom; `preferences.md`). Not a new version: the text is unchanged. The full-size pictures are in his Drive backup `travel-books-main-backup-20261123.zip`.
