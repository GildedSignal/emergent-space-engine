#!/usr/bin/env python3
"""Independent marker census and content-preservation verifier.

Deliberately shares NO parsing logic with wiki.py's defuse: markers are counted
by line-regex, orphans by a per-line open/has-mid/close ledger (not a tree),
content preservation by line multiset. If defuse mis-pairs, this still sees it.
"""
import re, sys
from collections import Counter

OPEN, MID, CLOSE = re.compile(r"^<{7} (.*)$"), re.compile(r"^={7}$"), re.compile(r"^>{7} (.*)$")
UNMERGED = "**⚠ unmerged — two versions stand; the next run on this topic resolves them:**"


def census(text):
    lines = text.splitlines()
    o = [i for i, l in enumerate(lines) if OPEN.match(l)]
    m = [i for i, l in enumerate(lines) if MID.match(l)]
    c = [i for i, l in enumerate(lines) if CLOSE.match(l)]
    # orphan ledger: walk lines; a mid is orphan if no block is open-in-ours;
    # a close is orphan if no block is open; an open is unclosed if still on the stack at EOF
    stack, orphan_mids, orphan_closes = [], [], []
    for i, l in enumerate(lines):
        if OPEN.match(l):
            stack.append([i, False])
        elif MID.match(l):
            if stack and not stack[-1][1]:
                stack[-1][1] = True
            else:
                orphan_mids.append(i)
        elif CLOSE.match(l):
            if stack:
                stack.pop()
            else:
                orphan_closes.append(i)
    return dict(open=len(o), mid=len(m), close=len(c),
                orphan_mid=len(orphan_mids), orphan_close=len(orphan_closes),
                unclosed=len(stack), markers=len(o) + len(m) + len(c),
                lines=len(lines), labels=sum(1 for l in lines if l.startswith("*Version `")),
                banners=sum(1 for l in lines if l == UNMERGED))


def content(text):
    """Non-marker, non-label, non-banner lines as a multiset."""
    keep = []
    for l in text.splitlines():
        if OPEN.match(l) or MID.match(l) or CLOSE.match(l) or l == UNMERGED or l.startswith("*Version `"):
            continue
        keep.append(l)
    return Counter(keep)


def runs_list(text):
    mm = re.search(r"^## Runs\s*$", text, re.M)
    if not mm:
        return []
    rest = text[mm.end():]
    end = re.search(r"^## ", rest, re.M)
    return [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]


def preserved(before, after):
    """every content line of before present in after with >= multiplicity;
    returns (ok, lost, added) where added = after-content minus before-content (labels expected)."""
    cb, ca = content(before), content(after)
    lost = cb - ca
    added = ca - cb
    return (not lost, list(lost.elements()), list(added.elements()))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        t = open(path, encoding="utf-8").read()
        print(path, census(t))
