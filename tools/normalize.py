#!/usr/bin/env python3
"""Mechanical normalisation of page files after every model step (models do not follow spacing rules).

  normalize.py DIR [--check]        rewrites DIR/p*.txt in place (--check: only report what would change)

What it does (project text policy: the words are the book's, the spacing is modern):
  * no space before ; : ! ? , . and none just inside quotation marks or brackets;
  * old spaced contractions closed up (do n't -> don't, I 'll -> I'll, 't is stays);
  * spaced dashes closed up (word — word -> word—word), -- and --- -> —, doubled spaces -> one;
  * <sc>TEXT IN CAPITALS</sc> -> <sc>text in capitals</sc> (small capitals are typed in lower case);
  * tags closed and reopened across a space merged (<i>a</i> <i>b</i> -> <i>a b</i>); empty tags removed;
  * code fences and trailing spaces removed; one blank line between paragraphs; file ends with a newline.
It never changes a letter (except the case inside <sc>) or a punctuation mark other than hyphens-as-dashes.
"""
import os, re, sys

MARK = re.compile(r"(\[\[[^\]]*\]\])")


def norm_text(s):
    """One line of text outside [[...]] markers."""
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"(?<=\S) +(\[\[fnref [^\]]*\]\])", r"\1", s)   # a note mark set after a space (Strangford, 2026-11-22)
    s = re.sub(r"(?<=[A-Za-z0-9>]) ?(?:---|--)(?!-) ?(?=[A-Za-z<“‘\"'])", "—", s)
    s = re.sub(r"(?<=\w) — (?=\w)", "—", s)
    s = re.sub(r"(?<=[\w>”’\")]) +([;:!?])(?=[\s”’\")<]|$)", r"\1", s)
    s = re.sub(r"(?<=[\w>”’\")]) +([,.])(?=[\s”’\")<]|$)(?! \.)", r"\1", s)
    s = re.sub(r"([“‘(\[]) +(?=\S)", r"\1", s)
    s = re.sub(r"(?<=\S) +([”)\]])", r"\1", s)
    s = re.sub(r"\b([A-Za-z]+) (n[’']t)\b", r"\1\2", s)
    s = re.sub(r"\b([A-Za-z]+) ([’'](?:ll|ve|re|d|m|s))\b", r"\1\2", s)
    s = re.sub(r"<sc>(.*?)</sc>", lambda m: "<sc>" + (m.group(1).lower() if not re.search(r"[a-z]", m.group(1)) and len(re.sub(r"[^A-Za-z]", "", m.group(1))) > 1 else m.group(1)) + "</sc>", s)
    for t in ("i", "b", "sc"):
        s = re.sub(rf"</{t}>( ?)<{t}>", r"\1", s)
        s = re.sub(rf"<{t}>(\s*)</{t}>", r"\1", s)
    return s


def norm_page(t):
    t = re.sub(r"^```[a-zA-Z]*\n", "", t.strip())
    t = re.sub(r"\n```$", "", t)
    out = []
    for ln in t.splitlines():
        ln = ln.rstrip()
        if ln.strip().startswith("|"):
            out.append(ln.strip()); continue
        parts = MARK.split(ln)
        ln = "".join(p if MARK.fullmatch(p) else norm_text(p) for p in parts)
        ln = re.sub(r"^(\[\[(?:cont|right|center|subtitle|caption)\]\]) +", r"\1 ", ln.strip())
        ln = ln.replace("[[cont]] ", "[[cont]]") if ln.startswith("[[cont]] ") else ln
        out.append(ln)
    t = "\n".join(out)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip() + "\n"


def main():
    d = sys.argv[1]
    check = "--check" in sys.argv
    n = 0
    for f in sorted(os.listdir(d)):
        if re.fullmatch(r"p\d+[a-z]?\.txt", f):
            p = os.path.join(d, f)
            a = open(p, encoding="utf-8").read()
            b = norm_page(a)
            if a != b:
                n += 1
                if check:
                    print("would change", f)
                else:
                    open(p, "w", encoding="utf-8").write(b)
    print(f"{n} files {'would be ' if check else ''}changed in {d}")


if __name__ == "__main__":
    main()
