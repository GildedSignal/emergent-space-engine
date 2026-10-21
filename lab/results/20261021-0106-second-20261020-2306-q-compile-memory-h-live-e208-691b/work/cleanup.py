#!/usr/bin/env python3
"""Builds the proposed page: the live lab/wiki/memory-h-live.md with the four
`wiki.py apply` Runs-union artifacts removed (identified structurally, not by
line number), this run's line appended, and `updated:` bumped.

Artifact rule (Runs section only), per id/key group with >1 line:
  - a later line >= 30 chars longer than the kept one is a completion -> keep the longest
    (the two dangling dated half-lines and the dangling second-checker line);
  - otherwise keep the FIRST occurrence (the fc22-a7d0 near-exact duplicate:
    identical up to one space, and the first is the variant e208 kept).
Then: budgets by wiki.py's rule, dated ids each exactly once, and a sandboxed
`wiki.py index` dry-run on the live wiki with only this page swapped, proving
the index stays clean. Also proves the union-resurrection claim mechanically:
simulating wiki.py apply's Runs union on (live page, this proposal) must
re-produce the four artifact lines — i.e. apply cannot land the deletion.
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))  # work->run->results->lab->repo
LIVE = f"{REPO}/lab/wiki/memory-h-live.md"
ME = "20261021-0106-second-20261020-2306-q-compile-memory-h-live-e208-691b"
MY_LINE = (f"- {ME} (this run): second check passed at claim level: 0 lost, 31 run-id-fragment "
           "demotions; apply's four union artifacts named for hand deletion.")

live = open(LIVE, encoding="utf-8").read()
m = re.search(r"^## Runs\s*$", live, re.M)
head, runs_txt = live[:m.end()], live[m.end():]
lines = runs_txt.splitlines()

groups = {}
order = []
for i, l in enumerate(lines):
    if not l.startswith("- "):
        continue
    key = re.match(r"^- ((?:\d{8}-\d{4}|second-checker \(\d{8}-\d{4})-\S+\)|second-checker \(\d{8}-\d{4}-[a-z0-9-]+\))", l)
    k = key.group(1) if key else l[:40]
    if k not in groups:
        groups[k], order = [], order + [k]
    groups[k].append(i)

drop = set()
for k in order:
    idx = groups[k]
    if len(idx) < 2:
        continue
    keep = idx[0]
    for i in idx[1:]:
        if len(lines[i]) >= len(lines[keep]) + 30:
            drop.add(keep)
            keep = i
        else:
            drop.add(i)

dropped = [lines[i] for i in sorted(drop)]
kept = [l for i, l in enumerate(lines) if i not in drop and l.strip()]
page = (head.replace("updated: 20261020-2306-q-compile-memory-h-live-e208", f"updated: {ME}")
        + "\n" + "\n".join(kept + [MY_LINE]) + "\n")

out = f"{HERE}/../wiki/memory-h-live.md"
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write(page)

# ---- verification ------------------------------------------------------------
best = [l for l in page.split("## Current best", 1)[-1].split("\n## ", 1)[0].splitlines() if l.strip()]
dated = re.findall(r"^- (\d{8}-\d{4}-\S+)", page, re.M)
dupes = {i for i in dated if dated.count(i) > 1}
print(f"live: {len(live.splitlines())} lines, runs lines {len([l for l in lines if l.startswith('- ')])}")
print(f"artifacts dropped ({len(dropped)}):")
for d in dropped:
    print(f"  - {d[:130]}")
print(f"proposed: {len(page.splitlines())} lines, runs lines {len([l for l in kept + [MY_LINE]])}, "
      f"dated lines {len(dated)} ({len(set(dated))} ids), duplicated ids {sorted(dupes) or 'none'}, "
      f"current best {len(best)}")

fails = []
if len(page.splitlines()) > 300: fails.append("total>300")
if len(best) > 15: fails.append("best>15")
if dupes: fails.append(f"dupe ids {dupes}")
if len(dropped) != 4:
    # the integrator may have hand-deleted the artifacts after this dossier: then the
    # live page no longer matches any drop rule and the target state is already there
    already = [d for d in dropped] == [] and not dupes and len(page.splitlines()) <= 300
    note = ("(live page already clean upstream: nothing to drop, invariants hold, PASS)"
            if already else f"expected 4 artifacts, dropped {len(dropped)}")
    print(f"artifact note: {note}")
    if not already: fails.append(note)

# sandbox index dry-run
sb = tempfile.mkdtemp(prefix="idx-")
shutil.copytree(f"{REPO}/lab/wiki", f"{sb}/wiki", dirs_exist_ok=True)
shutil.copy(out, f"{sb}/wiki/memory-h-live.md")
shutil.copy(f"{REPO}/lab/wiki.py", f"{sb}/wiki.py")
# wiki.py is run in place on lab/wiki; emulate by chdir with a stub repo layout
os.makedirs(f"{sb}/lab", exist_ok=True)
os.replace(f"{sb}/wiki", f"{sb}/lab/wiki")
os.replace(f"{sb}/wiki.py", f"{sb}/lab/wiki.py")
r = subprocess.run([sys.executable, "lab/wiki.py", "index"], cwd=sb, capture_output=True, text=True)
assert r.returncode == 0, r.stderr
row = [l for l in open(f"{sb}/lab/wiki/index.md", encoding="utf-8").read().splitlines() if "memory-h-live" in l]
print("index dry-run row:", row[0] if row else "MISSING")
if row and ("over budget" in row[0] or "conflict" in row[0]):
    fails.append("index flags page")

# union-resurrection proof: simulate apply's Runs union (ours=live, theirs=proposed)
ours_runs = [l for l in lines if l.startswith("- ")]
mm = re.search(r"^## Runs\s*$", page, re.M)
theirs_runs = [l for l in page[mm.end():].splitlines() if l.startswith("- ")]
union = ours_runs + [l for l in theirs_runs if l not in ours_runs]
resurrected = [d for d in dropped if d in union]
print(f"apply-union simulation: union {len(union)} run lines; artifacts resurrected by the union: "
      f"{len(resurrected)} of {len(dropped)} -> {'apply CANNOT delete them (hand fix needed)' if resurrected else 'deletion lands'}")

# three-way body merge simulation (what `wiki.py apply` will do to the head)
import tempfile as tf
with tf.NamedTemporaryFile("w", suffix=".ours", delete=False) as f1, \
     tf.NamedTemporaryFile("w", suffix=".base", delete=False) as f2, \
     tf.NamedTemporaryFile("w", suffix=".theirs", delete=False) as f3:
    f1.write(live[:m.start()]); f2.write(live[:m.start()]); f3.write(page[:mm.start()])
    p1, p2, p3 = f1.name, f2.name, f3.name
r3 = subprocess.run(["git", "merge-file", "-p", "-L", "main", "-L", "run start", "-L", ME, p1, p2, p3],
                    capture_output=True, text=True)
print(f"three-way head merge (live base): {'CLEAN' if r3.returncode == 0 else 'CONFLICT'}; "
      f"head identical to live: {'yes' if r3.stdout == live[:m.start()] else 'no (updated: bumped)'}")
os.remove(p1); os.remove(p2); os.remove(p3)

# P6: readability residual, measured
cb = [l for l in page.split("## Current best", 1)[-1].split("\n## ", 1)[0].splitlines() if l.strip()]
lens = sorted(len(l) for l in cb)
print(f"P6 current-best line chars: min {lens[0]}, median {lens[len(lens)//2]}, max {lens[-1]}, total {sum(lens)}")

print("CLEANUP:", "ALL PASS" if not fails else "FAILS: " + ",".join(fails))
shutil.rmtree(sb)
sys.exit(1 if fails else 0)
