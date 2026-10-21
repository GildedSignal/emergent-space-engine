#!/usr/bin/env python3
"""Verify the compiled representation-premises page against the old one.

Checks (mirrors lab/wiki.py's index() budget logic exactly):
  1. budgets: total lines <= 300, `## Current best` non-empty lines <= 15,
     open directions <= 8;
  2. runs: every old-page run id kept exactly once; grades = the run branch
     subjects (the page's own "(awaiting grade)" markers are stale);
  3. no supported number lost: every numeric token of the old page (dates and
     after normalizing unicode minus/plus and leading zeros.
"""
import os, re, subprocess, sys, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OLD = os.path.join(ROOT, "lab/wiki/representation-premises.md")
NEW = os.path.join(os.path.dirname(__file__), "wiki/representation-premises.md")

def norm(s):
    s = s.replace("\u2212", "-").replace("\u207a", "+")  # unicode minus/plus
    return unicodedata.normalize("NFKC", s)  # folds superscripts: 2⁻²⁰ -> 2-20

def tokens(text):
    t = norm(text)
    out = set()
    for m in re.finditer(r"\d+(?:\.\d+)?(?:e-?\d+)?", t, re.I):
        s = m.group(0).lower()
        s = re.sub(r"^(\d+)", lambda g: g.group(1).lstrip("0") or "0", s)
        out.add(s)
    return out

def sections(text):
    cb = re.search(r"^## Current best\s*\n(.*?)(?=^## )", text, re.M | re.S).group(1)
    od = re.search(r"^## Open directions\s*\n(.*?)(?=^## )", text, re.M | re.S).group(1)
    runs = re.findall(r"^- (\d{8}-\d{4}-[a-z0-9-]+)", text, re.M)
    return cb, od, runs

def best_lines(cb):
    # wiki.py: non-empty lines of the Current best block
    return len([l for l in cb.splitlines() if l.strip()])

def grade(run):
    r = subprocess.run(["git", "log", "-1", "--format=%s", f"origin/claude/lab-{run}"],
                       capture_output=True, text=True)
    m = re.search(r"Grade: (\w+)", r.stdout)
    return m.group(1) if m else "unknown"

old = open(OLD, encoding="utf-8").read()
new = open(NEW, encoding="utf-8").read()
fail = []

# 1. budgets
n_old, n_new = len(old.splitlines()), len(new.splitlines())
cb_o, od_o, runs_o = sections(old)
cb_n, od_n, runs_n = sections(new)
bl_o, bl_n = best_lines(cb_o), best_lines(cb_n)
od_n_items = len(re.findall(r"^\d+\.", od_n, re.M))
print(f"lines: old {n_old} -> new {n_new} (budget 300)")
print(f"current best non-empty lines: old {bl_o} -> new {bl_n} (budget 15)")
print(f"open directions: old {len(re.findall(chr(10)+r'\d+\.', chr(10)+od_o))} -> new {od_n_items} (budget 8)")
if n_new > 300: fail.append("over 300 lines")
if bl_n > 15: fail.append("current best over 15 lines")
if od_n_items > 8: fail.append("over 8 open directions")

# 2. runs
ids_o = [i for i in dict.fromkeys(runs_o)]
print(f"run lines: old {len(runs_o)} bullets / {len(ids_o)} distinct -> new {len(runs_n)} (each once: {len(runs_n)==len(set(runs_n))})")
if sorted(set(runs_o)) != sorted(set(runs_n)): fail.append("run id set changed")
if len(runs_n) != len(set(runs_n)): fail.append("duplicate run lines")
# index() counts this regex anywhere in the page:
cnt = len(re.findall(r"^- \d{8}-\d{4}-", new, re.M))
print(f"index run-count regex on new page: {cnt}")
# grades carried = branch grades
bad = []
for r in set(runs_n):
    g = grade(r)
    if f"({r} (" not in new and f"- {r} (" not in new:
        bad.append(r)
    line = [l for l in new.splitlines() if l.startswith(f"- {r} (")][0]
    if f"({g})" not in line and f"({g}," not in line:
        bad.append(f"{r}: page grade != branch grade {g}")
print("grades match branch subjects:", "yes" if not bad else bad)
if bad: fail.append("grade mismatch: " + "; ".join(map(str, bad)))

# 3. number survival
to, tn = tokens(old), tokens(new)
missing = sorted(to - tn)
print(f"numeric tokens: old {len(to)}, new {len(tn)}, old-missing-in-new {len(missing)}")
if missing:
    print("MISSING:", missing)
    fail.append(f"{len(missing)} numeric tokens lost")

print("VERDICT:", "FAIL: " + "; ".join(fail) if fail else "PASS (all checks)")
sys.exit(1 if fail else 0)
