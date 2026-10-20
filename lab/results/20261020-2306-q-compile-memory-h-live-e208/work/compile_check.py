#!/usr/bin/env python3
"""Compile-check for the memory-h-live page recompile (run 20261020-2306-q-compile-memory-h-live-e208).

Assembles $out/wiki/memory-h-live.md = work/head.md + ## Runs (run lines of the
original page, kept verbatim in order, with three duplicate/dangling lines merged),
then verifies, old page vs new page:
  - budgets (wiki.py's rules): total lines <= 300, Current-best non-blank lines <= 15;
  - every dated run line of the old page is present (one line each after dedup);
  - every digit-bearing token outside the old page's ## Runs appears in the new page
    (no supported number lost).
Prints PASS/FAIL per rule and the exact losses.
"""
import re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(RUN)))  # lab/results/<run>/work -> repo root
OLD = os.path.join(REPO, "lab", "wiki", "memory-h-live.md")
OUT = os.path.join(RUN, "wiki", "memory-h-live.md")
HEAD = os.path.join(HERE, "head.md")
old = open(OLD, encoding="utf-8").read()
m = re.search(r"^## Runs\s*$", old, re.M)
rest = old[m.end():]
end = re.search(r"^## ", rest, re.M)
run_lines = [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]

COMPLETE_SECOND_CHECKER = ("- second-checker (20261017-0238-inversion-470f): 20 of 22 fresh flights grew "
    "(8/8 under 8-way load, 8/8 with the counting allocator removed — not an instrument artifact — and 2/4 quiet).")
DROP_PREFIXES = (
    "- 20261012-1524-fermi-4b55 (silver): H_live term decomposition — rebinds,",           # dangling dup of the complete line
    "- 20261012-1621-second-20261012-1524-fermi-4b55-09a1 (this run): named",               # dangling dup
    "- 20261007-0933-second-20261007-0842-fermi-fc22-a7d0 (gold): fc22's \u2264 1 MB holds", # near-exact dup (kept the tighter one)
)
out_lines, dropped = [], []
for l in run_lines:
    if any(l.startswith(p) for p in DROP_PREFIXES):
        dropped.append(l)
        continue
    if l.startswith("- second-checker (20261017-0238-inversion-470f): 20 of 22 fresh flights grew (8/8 under 8-way"):
        l = COMPLETE_SECOND_CHECKER
        dropped.append("(completed dangling second-checker line)")
    out_lines.append(l)

head = open(HEAD, encoding="utf-8").read().rstrip("\n")
page = head + "\n\n## Runs\n" + "\n".join(out_lines) + "\n"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(page)

# ---- checks ------------------------------------------------------------------
def canon(t):
    return t.strip('`"\'()[]{}<>.,;:|/\\+*=~\u2014\u2013-')

def toks(s):
    out = set()
    for w in re.findall(r"[^\s]*\d[^\s]*", s):
        c = canon(w)
        if c:
            out.add(c)
    return out

def section(text, name, nxt):
    return text.split(name, 1)[-1].split(nxt, 1)[0]

fails = []

n_old_lines = len(old.splitlines())
n_new_lines = len(page.splitlines())
best_old = [l for l in section(old, "## Current best", "\n## Refuted").splitlines() if l.strip()]
best_new = [l for l in section(page, "## Current best", "\n## Refuted").splitlines() if l.strip()]

dated_old = sorted(set(re.findall(r"^- (\d{8}-\d{4}-\S+)", old, re.M)))
dated_new = sorted(set(re.findall(r"^- (\d{8}-\d{4}-\S+)", page, re.M)))

old_pre = old[:m.start()]
lost = toks(old_pre) - toks(page)

print(f"old: {n_old_lines} lines, current best {len(best_old)} non-blank, {len(dated_old)} dated run ids")
print(f"new: {n_new_lines} lines, current best {len(best_new)} non-blank, {len(dated_new)} dated run ids, "
      f"{len(out_lines)} run lines ({len(dropped)} merged/dropped: {dropped})")
print(f"refuted entries (new): {len([l for l in page.split(chr(10)+'## Refuted',1)[-1].split(chr(10)+'## Open directions')[0].splitlines() if l.startswith('- ')])}")
ok_lines = n_new_lines <= 300
ok_best = len(best_new) <= 15
ok_runs = dated_old == dated_new
ok_nums = not lost
print(f"budget total<=300: {'PASS' if ok_lines else 'FAIL'} ({n_new_lines})")
print(f"budget best<=15:   {'PASS' if ok_best else 'FAIL'} ({len(best_new)})")
print(f"runs preserved:    {'PASS' if ok_runs else 'FAIL'}")
if not ok_runs:
    print("  missing:", [r for r in dated_old if r not in dated_new])
    print("  extra:  ", [r for r in dated_new if r not in dated_old])
od_new = len([l for l in page.split("\n## Open directions",1)[1].split("\n## Contradictions",1)[0].splitlines() if re.match(r"^\d+\.", l.strip())])
print(f"open directions (new): {od_new}; at-risk old tokens: {len(toks(old_pre))}")
print(f"numbers preserved: {'PASS' if ok_nums else 'FAIL'} ({len(lost)} lost of {len(toks(old_pre))})")
for t in sorted(lost):
    print("  LOST:", t)
sys.exit(0 if (ok_lines and ok_best and ok_runs and ok_nums) else 1)
