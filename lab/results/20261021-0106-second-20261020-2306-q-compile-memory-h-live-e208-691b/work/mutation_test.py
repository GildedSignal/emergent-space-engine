#!/usr/bin/env python3
"""Mutation test of the section-local instrument (a check that cannot fail is a control).

Takes the compiled page, mutates one number out of Current best (226 -> XXX, the
flat-pin figure that also survives in Refuted line 1), and re-runs the same
section-local logic: the mutation MUST surface as a substantive demotion or a
page-wide loss. Also mutates a Refuted number. Prints CAUGHT/ESCAPED per mutation.
"""
import re, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
compiled = open(f"{HERE}/compiled-page.md", encoding="utf-8").read()

def check(new_text):
    old = open(f"{HERE}/old-page.md", encoding="utf-8").read()
    def sect(t, n):
        m = re.search(rf"^## {n}\s*$", t, re.M)
        rest = t[m.end():]
        e = re.search(r"^## ", rest, re.M)
        return rest[:e.start()] if e else rest
    head = "".join(sect(new_text, s) for s in ["Current best", "Refuted", "Open directions", "Contradictions"])
    runs_t = new_text[re.search(r"^## Runs\s*$", new_text, re.M).end():]
    def present(c, hay): return re.search(rf"(?<![0-9.]){re.escape(c)}(?![0-9])", hay) is not None
    rid_nums = set()
    for tok in re.findall(r"\S*\d{8}-\d{4}\S*", new_text):
        for piece in re.findall(r"\d+", tok):
            rid_nums.update({piece, piece[-4:], piece[:4]})
    flagged = []
    for name in ["Current best", "Refuted"]:
        for c in set(re.findall(r"\d+(?:\.\d+)?", sect(old, name))):
            if not present(c, head):
                status = "demoted-substantive" if present(c, runs_t) and c not in rid_nums else \
                         ("demoted-fragment" if present(c, runs_t) else "PAGE-WIDE LOSS")
                if status != "demoted-fragment":
                    flagged.append((name, c, status))
    return flagged

# mutations must remove EVERY head occurrence (the instrument checks the head as a whole;
# single-site mutation legitimately survives via another section, as the first run showed)
runs_at = re.search(r"^## Runs\s*$", compiled, re.M)
head_txt, rest = compiled[:runs_at.start()], compiled[runs_at.start():]
m1 = head_txt.replace("226", "XXX") + rest            # flat-pin figure, head-wide
m2 = head_txt.replace("475", "XXX") + rest            # b77d's B/candidate, head-wide

for label, mut, needle in [("Current-best 226 -> XXX", m1, "226"),
                           ("Refuted 475 -> XXX", m2, "475")]:
    f = [x for x in check(mut) if x[1] == needle]
    print(f"mutation {label}: {'CAUGHT ' + str(f) if f else 'ESCAPED (instrument blind here)'}")
sys.exit(0)
