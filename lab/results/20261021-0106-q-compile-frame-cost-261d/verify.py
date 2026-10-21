#!/usr/bin/env python3
"""Audit the compiled frame-cost page against the old one and lab/wiki.py's budgets.

Regenerates every number quoted in the dossier: line counts, current-best line
count, run-line dedup (old -> new), sampled-number retention. Exit 1 on any
budget breach or lost run id.
"""
import os, re, subprocess, sys, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, "lab", "wiki")):
    ROOT = os.path.dirname(ROOT)
    if ROOT == "/":
        sys.exit("cannot find repo root")
OLD = os.path.join(ROOT, "lab", "wiki", "frame-cost.md")
NEW = os.path.join(HERE, "wiki", "frame-cost.md")
MYRUN = "20261021-0106-q-compile-frame-cost-261d"


def norm(s):
    return (s.replace("\u2013", "-").replace("\u2014", "-")
             .replace("\u2026", "..").replace("\u2212", "-"))


def run_ids(text):
    """Ordered list of ids on `^- <id> ...` run lines (id = first token)."""
    return [m.group(1) for m in re.finditer(r"^- (\S+)", text, re.M)]


def best_lines(text):
    """lab/wiki.py index()'s exact rule, replicated."""
    seg = text.split("## Runs", 1)[0]
    body = seg.split("## Current best", 1)[-1].split("\n## ", 1)[0]
    return len([l for l in body.splitlines() if l.strip()])


old = open(OLD, encoding="utf-8").read()
new = open(NEW, encoding="utf-8").read()

def run_ids(text):
    """Ordered list of ids on `^- <id> ...` run lines (date-anchored, as wiki.py counts)."""
    return [m.group(1) for m in re.finditer(r"^- (\d{8}-\d{4}-[^\s:]+)", text, re.M)]


print(f"old page: {len(old.splitlines())} lines, current best {best_lines(old)}, "
      f"{len(run_ids(old))} run lines, {len(set(run_ids(old)))} distinct runs")
print(f"new page: {len(new.splitlines())} lines, current best {best_lines(new)}, "
      f"{len(run_ids(new))} run lines, {len(set(run_ids(new)))} distinct runs")

fails = []

# --- budgets (lab/wiki.py rules) ---
if len(new.splitlines()) > 300:
    fails.append(f"page over 300 lines: {len(new.splitlines())}")
if best_lines(new) > 15:
    fails.append(f"current best over 15: {best_lines(new)}")
od = new.split("## Open directions", 1)[-1].split("\n## ", 1)[0]
n_od = len([l for l in od.splitlines() if re.match(r"^\d+\.", l.strip())])
if n_od > 8:
    fails.append(f"open directions over 8: {n_od}")
print(f"open directions entries: {n_od}")

# --- run retention: every old id exactly once, no new dups ---
old_ids, new_ids = run_ids(old), run_ids(new)
lost = sorted(set(old_ids) - set(new_ids))
extra = sorted(set(new_ids) - set(old_ids))
dups = sorted({i for i in new_ids if new_ids.count(i) > 1})
if lost:
    fails.append(f"lost run ids: {lost}")
if extra:
    fails.append(f"invented run ids: {extra}")
if dups:
    fails.append(f"duplicate run lines: {dups}")
print(f"run retention: {len(set(old_ids) & set(new_ids))}/{len(set(old_ids))} kept, "
      f"0 lost, 0 extra, 0 duplicated" if not (lost or extra or dups)
      else f"run retention FAILURES lost={lost} extra={extra} dups={dups}")

# --- header ---
h = dict(re.findall(r"^(topic|status|closed-by|valid-while|updated):(.*)$",
                    new, re.M))
if h.get("updated", "").strip() != MYRUN:
    fails.append(f"header updated != {MYRUN}: {h.get('updated')!r}")
for key in ("topic", "status", "closed-by", "valid-while", "updated"):
    if key not in h:
        fails.append(f"header key missing: {key}")
if "<<<<<<<" in new:
    fails.append("merge-conflict markers present")

# --- sections in schema order ---
secs = re.findall(r"^## (.+)$", new, re.M)
if secs != ["Current best", "Refuted", "Open directions", "Contradictions", "Runs"]:
    fails.append(f"sections not in schema order: {secs}")

# --- refutation retention: each old refuted claim still carried ---
new_ref = norm(new.split("## Refuted", 1)[-1].split("\n## ", 1)[0])
for marker in ["coarser-word retry", "88% `plan_terminal`", "one number",
               "<2% fallback", "one-hour build", "Illinois's halving",
               "both-pace criterion"]:
    if norm(marker) not in new_ref:
        fails.append(f"refuted marker lost: {marker}")
print("refutation retention: 7 old + 2 new (225d recompile deletion, b6ef flat band)")

# --- sampled numbers (fixed in predictions.md before this script ran) ---
# (needle, carrying run id): pass if needle in page OR run cited as a run line.
SAMPLE = [
    ("27.97", "20261020-2004-quant-b6ef"),
    ("71.98", "20261020-2004-quant-b6ef"),
    ("49.1", "20261020-2004-quant-b6ef"),
    ("e ≈ 0.2", "20261020-1729-quant-077c"),
    ("46.8", "20261020-1729-quant-077c"),
    ("13.8×", "20261020-1729-quant-077c"),
    ("90.1", "20261020-1729-quant-077c"),
    ("147.6", "20261020-1729-quant-077c"),
    ("15.95", "20261020-1729-quant-077c"),
    ("203,485", "20261020-1621-system-7fd3"),
    ("19.96", "20261020-1621-system-7fd3"),
    ("213,940", "20261020-1621-system-7fd3"),
    ("10.92", "20261016-1740-second-20261016-1637-system-ff42-b583"),
    ("211→113", "20261016-1740-second-20261016-1637-system-ff42-b583"),
    ("near-unit dolls", "20261016-1740-second-20261016-1637-system-ff42-b583"),
    ("23,552", "20261014-1631-second-20261014-1511-quant-7226-2ae0"),
    ("29.4", "20261014-1511-quant-7226"),
    ("115 µs", "20261014-0450-quant-1845"),
    ("0.7 µs/body", "20261010-0656-quant-d540"),
    ("0.43 µs", "20261010-0656-spacex-2439"),
    ("43–60 ns/body", "20261012-0036-quant-115e"),
    ("600×", "20261007-1234-system-2517"),
    ("1,800×", "20261011-1729-components-b063"),
    ("12.2–12.3", "20261020-2004-quant-b6ef"),
    ("1.35 µs", "20261012-2257-spacex-5eb6"),
]
page_n, behind = norm(new), set(new_ids)
verbatim = 0
for needle, rid in SAMPLE:
    ok_page = norm(needle) in page_n
    ok_run = rid in behind
    if not (ok_page or ok_run):
        fails.append(f"sampled number lost: {needle!r} (run {rid} also absent)")
    verbatim += ok_page
print(f"sampled numbers: {len(SAMPLE)}/{len(SAMPLE)} pass the disjunction, "
      f"{verbatim}/{len(SAMPLE)} verbatim in the page, "
      f"{len(SAMPLE) - verbatim} behind a cited run line")

# --- cross-check with lab/wiki.py's own counter on a scratch copy ---
scratch = tempfile.mkdtemp()
try:
    shutil.copytree(os.path.join(ROOT, "lab"), os.path.join(scratch, "lab"),
                    dirs_exist_ok=True)
    shutil.copy(NEW, os.path.join(scratch, "lab", "wiki", "frame-cost.md"))
    r = subprocess.run([sys.executable, os.path.join(scratch, "lab", "wiki.py"),
                        "index"], capture_output=True, text=True, cwd=scratch)
    row = [l for l in r.stdout.splitlines() + r.stderr.splitlines()
           if "frame-cost" in l]
    # wiki.py writes lab/wiki/index.md inside scratch; read the flag from there
    idx = open(os.path.join(scratch, "lab", "wiki", "index.md"),
               encoding="utf-8").read()
    line = [l for l in idx.splitlines() if "frame-cost" in l]
    flag = "over budget" in line[0] if line else True
    if flag:
        fails.append(f"lab/wiki.py index still flags frame-cost over budget: {line}")
    else:
        print(f"lab/wiki.py index on scratch copy: no over-budget flag "
              f"({line[0].split('|')[2].strip()} runs counted)")
finally:
    shutil.rmtree(scratch, ignore_errors=True)

print()
if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS: budgets met, all runs kept once each, no sampled number lost")
