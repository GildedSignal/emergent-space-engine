#!/usr/bin/env python3
"""The section-local claim-survival check (checker 1's named "honest stronger form").

The author's instrument proved page-global string survival; it cannot see a
number whose CLAIM left the head but whose string survives in a Runs citation
line. This instrument works section-locally:

  S1  old Current-best number cores NOT in the compiled page's HEAD sections
      (Current best + Refuted + Open directions + Contradictions) = demotions;
      split into "present in Runs" (string survives, claim demoted) and
      "absent page-wide" (a loss the author's canon could not see).
  S2  same for old Refuted, old Open directions, old Contradictions.
  S3  classify each demotion: citation fragment (part of a run id/date/time, or
      a universe.rs:<line> pin that also appears in a Runs line) vs substantive;
      print old context (+/-70 chars) for every substantive one -> cold-read list.

Exit 1 only on page-wide losses or head-section regressions (an old Refuted/
OD/Contradiction core vanishing page-wide); demotions are printed for adjudication.
"""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
old = open(f"{HERE}/old-page.md", encoding="utf-8").read()
new = open(f"{HERE}/compiled-page.md", encoding="utf-8").read()


def sect(text, name):
    m = re.search(rf"^## {name}\s*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    e = re.search(r"^## ", rest, re.M)
    return rest[:e.start()] if e else rest


def runs(text):
    m = re.search(r"^## Runs\s*$", text, re.M)
    return text[m.end():] if m else ""


def cores(s):
    return set(re.findall(r"\d+(?:\.\d+)?", s))


def present(needle, hay):
    return re.search(rf"(?<![0-9.]){re.escape(needle)}(?![0-9])", hay) is not None


HEAD_SECTIONS = ["Current best", "Refuted", "Open directions", "Contradictions"]
new_head = "".join(sect(new, s) for s in HEAD_SECTIONS)
new_runs = runs(new)
run_ids = set(re.findall(r"\d{8}-\d{4}-[a-z0-9-]+", new)) | set(re.findall(r"\d{4}", " ".join(re.findall(r"\d{8}-(\d{4})", new))))
run_date_fragments = set()
for rid in re.findall(r"\d{8}-\d{4}", new):
    run_date_fragments |= {rid, rid[:8], rid[9:]}

# numeric fragments that appear inside any run id on the page (citation plumbing)
rid_nums = set()
for rid in re.findall(r"[0-9a-z-]*\d{8}-\d{4}[0-9a-z-]*", new):
    for piece in re.findall(r"\d+", rid):
        for i in range(1, len(piece) + 1):
            rid_nums.add(piece[:i]) if False else None
# simpler: every maximal digit run inside run-id-like tokens, plus its 4-digit tail
for tok in re.findall(r"\S*\d{8}-\d{4}\S*", new):
    for piece in re.findall(r"\d+", tok):
        rid_nums.add(piece)
        rid_nums.add(piece[-4:])
        rid_nums.add(piece[:4])

lost_page_wide, demoted, report = [], [], []
for name in HEAD_SECTIONS:
    o, h = sect(old, name), ""
    for c in sorted(cores(o), key=lambda s: (len(s), s)):
        if present(c, new_head):
            continue
        if present(c, new_runs):
            demoted.append((name, c))
        elif present(c, new):
            lost_page_wide.append((name, c))  # in head-Runs boundary? shouldn't happen
        else:
            lost_page_wide.append((name, c))

print(f"S1/S2: old-head cores demoted to Runs-only: {len(demoted)}; absent page-wide: {len(lost_page_wide)}")
for s, c in lost_page_wide:
    print(f"  PAGE-WIDE LOSS [{s}]: {c}")

substantive = []
for name, c in demoted:
    if c in rid_nums or c in run_date_fragments:
        continue
    substantive.append((name, c))
print(f"S3: demotions that are NOT run-id/date fragments: {len(substantive)}")
for name, c in substantive:
    m = re.search(rf"(?<![0-9.]){re.escape(c)}(?![0-9])", sect(old, name))
    ctx = sect(old, name)[max(0, m.start() - 70):m.end() + 70].replace("\n", " ")
    in_runs = [l[:150] for l in runs(new).splitlines() if re.search(rf"(?<![0-9.]){re.escape(c)}(?![0-9])", l)]
    print(f"--- [{name}] core={c}")
    print(f"    old ctx: ...{ctx}...")
    for l in in_runs[:2]:
        print(f"    runs now: {l}")
sys.exit(1 if lost_page_wide else 0)
