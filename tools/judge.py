#!/usr/bin/env python3
"""A fresh reading of every spot where the draft and the verifier disagree on words or punctuation.

  judge.py --spots spots.json --verified VERIFIED_DIR --images PAGES_DIR --out JUDGE_DIR [--model opus] [--workers 4]

For each page in spots.json (from review.py) one headless Claude call gets the page image and the numbered
spots, each with two readings labelled A and B (which is the draft's is shuffled per spot and not told),
and answers which the print shows, or what it shows if neither. Writes:
  JUDGE_DIR/pNNNN.txt     the verified page with every spot set to the judge's choice
                          (pages without spots are copied from VERIFIED_DIR unchanged)
  JUDGE_DIR/verdicts.jsonl, JUDGE_DIR/report.txt, log.jsonl
report.txt lists (1) spots where the judge sided with the draft against the verifier, (2) spots answered
"neither" — the judge's own reading is NOT applied: the verified reading stays and the SESSION must look at
a crop (tools/crop_spot.py) and edit the page file, (3) spots the judge was not sure of. Judges are wrong
about one time in 6 to 30: every (2) and (3), and every change towards a more modern or more usual spelling,
is checked on the scan before the book is published.
"""
import argparse, concurrent.futures as cf, hashlib, json, os, re, shutil, subprocess, sys, time
from refusal import is_refusal

TASK = """You are checking a transcription of one scanned page of a book printed in English before 1914.
The page image is the file {img} — open it with the Read tool first.

Two careful transcriptions of this page disagree at the numbered spots below. For each spot, find the place
on the scan (the context shows the surrounding words; ⏎ marks a paragraph break) and decide which reading
is what is PRINTED, letter for letter and mark for mark. The printed text wins even where it looks like a
misprint or an old spelling; do not prefer the more modern or more usual form. Ignore differences of
spacing, straight or curly quotes, and line-end hyphenation.

{spots}

Reply with one JSON object per spot, one per line, and nothing else:
{{"n": 1, "is": "A" | "B" | "neither", "print": "what the scan shows at this spot (same span as the readings)", "sure": "high" | "medium" | "low"}}
"""


def call(prompt, model, cwd):
    last = None
    for _ in range(3):
        t0 = time.time()
        try:
            r = subprocess.run(
                ["claude", "-p", prompt, "--model", model, "--output-format", "json",
                 "--system-prompt", "You are a meticulous proofreader of transcriptions of scanned book pages. "
                 "Follow the user's format instructions exactly.",
                 "--tools", "Read", "--allowedTools", "Read", "--strict-mcp-config", "--setting-sources", ""],
                capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL, cwd=cwd)
            j = json.loads(r.stdout)
            if j.get("is_error") or not (j.get("result") or "").strip():
                raise RuntimeError(str(j.get("result"))[:300])
            return j["result"], {"seconds": round(time.time() - t0, 1), "cost": j.get("total_cost_usd")}
        except Exception as e:  # noqa: BLE001
            last = repr(e)[:300]
            if is_refusal(last):
                break
            time.sleep(5)
    return None, {"error": last}


def labels(page, n):
    """True if reading A is the draft's for this spot (stable pseudo-random)."""
    return int(hashlib.sha1(f"{page}:{n}".encode()).hexdigest(), 16) % 2 == 0


def parse(reply):
    out = {}
    for ln in (reply or "").splitlines():
        ln = ln.strip().strip("`").rstrip(",")
        if ln.startswith("{"):
            try:
                d = json.loads(ln)
                out[int(d["n"])] = d
            except (ValueError, KeyError, TypeError):
                pass
    return out


def moves(spots):
    """Pairs of spot numbers (taken out, put in) where the verifier moved a passage: one spot removes text that
    another spot on the page inserts (e.g. a paragraph moved from before a picture to after its caption). Judged
    apart, such a pair can lose the passage (draft at one spot, verified at the other: *Rambles*, p0092)."""
    def piece(long, short):
        return long.replace(short, "", 1).strip() if short and short in long and len(long) > len(short) else ""
    out = []
    for s in spots:
        gone = piece(s["find"], s["replace"])
        if len(gone) < 20:
            continue
        for t in spots:
            if t is not s and gone in t["replace"] and gone not in t["find"]:
                out.append((s["n"], t["n"]))
    return out


def apply(verified_text, spots, verdicts, page):
    """Undo the verifier's change at every spot where the judge chose the draft. Returns (text, rows).
    A moved passage (`moves`) judged one way at one end and the other way at the other keeps the verifier's
    reading at both ends, so that nothing is lost or doubled; the rows say so, for a look at the scan."""
    rows, text = [], verified_text

    def side(s):
        v = verdicts.get(s["n"])
        if v is None or v.get("is") not in ("A", "B"):
            return None
        return "draft" if (v["is"] == "A") == labels(page, s["n"]) else "verified"
    split = set()
    for a, b in moves(spots):
        sa, sb = (side(next(s for s in spots if s["n"] == k)) for k in (a, b))
        if sa != sb:
            split |= {a, b}
    for s in spots:
        v = verdicts.get(s["n"])
        a_is_draft = labels(page, s["n"])
        if v is None:
            rows.append(("unanswered", s, None)); continue
        choice = v.get("is")
        who = "neither" if choice not in ("A", "B") else ("draft" if (choice == "A") == a_is_draft else "verified")
        if s["n"] in split:
            rows.append(("move judged both ways: verified kept", s, v)); continue
        if who != "draft" and dropped_images(s, spots):
            if text.count(s["replace"]) == 1 and s["replace"]:
                text = text.replace(s["replace"], s["find"]); who = "draft kept: the verifier dropped a picture"
            else:
                who = "the verifier dropped a picture (could not undo: edit by hand)"
        if who == "draft":
            if text.count(s["replace"]) == 1:
                text = text.replace(s["replace"], s["find"])
            else:
                who = "draft (could not undo: edit by hand)"
        rows.append((who, s, v))
    return text, rows


HEADING_LINE = re.compile(r"(?m)^#")
IMAGE_LINE = re.compile(r"\[\[image:[^\]]*\]\]")
# a caption line counts as part of its picture: the verifier dropped one and the judge agreed (*Western Wanderings*
# p0312, 2026-11-22)
KEEP_LINE = re.compile(r"\[\[image:[^\]]*\]\]|\[\[caption\]\][^\n]*")


def dropped_images(spot, spots):
    """The draft's [[image: …]] lines that the verifier's reading at this spot leaves out and that no spot on the
    page puts in elsewhere (a move): the verifier left a picture out and the judge agreed, "sure: medium"
    (*Zephyrus* p0171, 2026-11-20). A picture is never dropped by the judge."""
    out = []
    for m in KEEP_LINE.findall(spot.get("find", "")):
        if m in spot.get("replace", ""):
            continue
        if any(m in t.get("replace", "") for t in spots if t is not spot):
            continue
        out.append(m)
    return out


def must_look(who, sure, spot):
    """A spot goes in report.txt unless the judge took the verifier's reading and was sure — and always when either
    reading has a heading line: the verifier dropped two letter headings ("# Tenth Letter") and the judge, seeing
    a heading in small capitals at the page top, took them for running heads and agreed, sure (*Summer Greetings
    from Japan*, 2026-11-20)."""
    if HEADING_LINE.search(spot.get("find", spot.get("draft", ""))) or HEADING_LINE.search(spot.get("replace", spot.get("verified", ""))):
        return True
    if IMAGE_LINE.search(spot.get("find", spot.get("draft", ""))) or IMAGE_LINE.search(spot.get("replace", spot.get("verified", ""))):
        return True
    return who != "verified" or sure != "high"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spots", required=True); ap.add_argument("--verified", required=True)
    ap.add_argument("--images", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="opus"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if "fable" in a.model.lower() or "mythos" in a.model.lower():
        sys.exit("Fable is not used in this project without Tom's explicit permission (CLAUDE.md).")
    os.makedirs(os.path.join(a.out, "raw"), exist_ok=True)
    spots = json.load(open(a.spots, encoding="utf-8"))

    def work(page):
        raw = os.path.join(a.out, "raw", page + ".txt")
        if os.path.exists(raw):
            return None
        img = next((os.path.abspath(os.path.join(a.images, page + e)) for e in (".jpg", ".png") if os.path.exists(os.path.join(a.images, page + e))), None)
        if not img:
            return {"page": page, "error": "no image"}
        lines = []
        for s in spots[page]:
            d, v = s["draft"], s["verified"]
            A, B = (d, v) if labels(page, s["n"]) else (v, d)
            lines.append(f"Spot {s['n']}. Context: …{s['context']}…\n  A: {A!r}\n  B: {B!r}")
        reply, rec = call(TASK.format(img=img, spots="\n\n".join(lines)), a.model, a.out)
        if reply is not None:
            open(raw, "w", encoding="utf-8").write(reply)
        rec.update(page=page, model=a.model)
        return rec
    with cf.ThreadPoolExecutor(a.workers) as ex, open(os.path.join(a.out, "log.jsonl"), "a", encoding="utf-8") as log:
        for rec in ex.map(work, sorted(spots)):
            if rec:
                log.write(json.dumps(rec) + "\n"); log.flush()
    tally, rep, allv = {}, [], []
    for f in sorted(os.listdir(a.verified)):
        if not re.fullmatch(r"p\d+[a-z]?\.txt", f):
            continue
        page = f[:-4]
        text = open(os.path.join(a.verified, f), encoding="utf-8").read()
        if page in spots:
            raw = os.path.join(a.out, "raw", page + ".txt")
            verdicts = parse(open(raw, encoding="utf-8").read()) if os.path.exists(raw) else {}
            text, rows = apply(text, spots[page], verdicts, page)
            for who, s, v in rows:
                tally[who] = tally.get(who, 0) + 1
                allv.append({"page": page, "n": s["n"], "who": who, "draft": s["draft"], "verified": s["verified"], "judge": v})
                sure = (v or {}).get("sure", "")
                if must_look(who, sure, s):
                    rep.append(f"{page} #{s['n']} [{who}{', sure: ' + sure if sure else ''}] draft {s['draft']!r} | verified {s['verified']!r}"
                               + (f" | judge reads {v.get('print')!r}" if v else ""))
        open(os.path.join(a.out, f), "w", encoding="utf-8").write(text)
    with open(os.path.join(a.out, "verdicts.jsonl"), "w", encoding="utf-8") as fo:
        for v in allv:
            fo.write(json.dumps(v, ensure_ascii=False) + "\n")
    cost = sum(json.loads(x).get("cost") or 0 for x in open(os.path.join(a.out, "log.jsonl"), encoding="utf-8"))
    head = f"judge {a.model}: {sum(tally.values())} spots on {len(spots)} pages: {tally}; cost ${cost:.2f}"
    open(os.path.join(a.out, "report.txt"), "w", encoding="utf-8").write(head + "\n" + "\n".join(rep) + "\n")
    print(head)
    print(f"{len(rep)} spots to look at on the scan: {os.path.join(a.out, 'report.txt')}")


if __name__ == "__main__":
    main()
