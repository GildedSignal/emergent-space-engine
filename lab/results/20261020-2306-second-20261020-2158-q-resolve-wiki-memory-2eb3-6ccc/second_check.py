#!/usr/bin/env python3
"""The checker's named gold experiment, decided mechanically (second_check.py).

Lands 87d0's +92/-9 patch at HEAD (one hand-merged hunk) plus the id-keyed Runs
union, then flies the real publisher: replay 2eb3's actual silver publish from its
base commit, measure one-line-per-run / 0 markers / flags / idempotence, then the
next publish (this run's page, carrying a corrected line). The pristine HEAD
wiki.py replays the same publish as the negative control, and the corpus ceiling
for the id-keyed fold is measured over every page. Reads only; writes inside tmp.
"""
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
os.chdir(REPO)
RUN = "lab/results/20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc"
RUNID = "20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc"
PRIOR = "20261020-2158-q-resolve-wiki-memory-2eb3"
BASE2EB3 = "9bf31c707a315a6cb2627b25ee13b146d548be0d"  # 2eb3's own base file
BASEMINE = open(f"{RUN}/base").read().strip()
RAW87 = f"{RUN}/work/patch-87d0-raw.diff"
MERGED = f"{RUN}/work/patch.diff"
PROPOSAL2EB3 = subprocess.run(["git", "show", f"origin/claude/lab-{PRIOR}:lab/results/{PRIOR}/wiki/wiki-memory.md"],
                              capture_output=True, text=True).stdout
PRE = subprocess.run(["git", "show", f"{BASE2EB3}:lab/wiki/wiki-memory.md"], capture_output=True, text=True).stdout
SHIPPED = open("lab/wiki/wiki-memory.md", encoding="utf-8").read()
LINE_MARK = re.compile(r"^(<{7}|={7}|>{7})")

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

def load(path, env_wiki=None):
    os.environ["LAB_WIKI"] = env_wiki or "lab/wiki"
    spec = importlib.util.spec_from_file_location(f"wiki-{abs(hash(path))}", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def runs_of(text):  # line-anchored exactly like the tool's split_runs (prose mentions do not split)
    m = re.search(r"^## Runs\s*$", text, re.M)
    if not m:
        return []
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    return [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]

def body_of(text):
    m = re.search(r"^## Runs\s*$", text, re.M)
    return text[:m.start()].rstrip("\n") if m else text.rstrip("\n")

def markers3(text):
    return sum(1 for l in text.splitlines() if LINE_MARK.match(l))

tmp = tempfile.mkdtemp()

# --- S0: patched index() is byte-identical on the current corpus (no regression) ---
s0 = f"{tmp}/s0"; shutil.copytree("lab/wiki", s0)
patched = load("lab/wiki.py", s0)
patched.index()
check("S0: patched index() on the current corpus is byte-identical to the shipped index",
      open(f"{s0}/index.md", encoding="utf-8").read() == open("lab/wiki/index.md", encoding="utf-8").read())

# --- S1 (P1): the raw patch fails at HEAD in exactly its index hunk; the merged one applies clean ---
def pristine_tree(tag):
    d = f"{tmp}/{tag}"
    os.makedirs(f"{d}/lab")
    open(f"{d}/lab/wiki.py", "w").write(subprocess.run(["git", "show", "HEAD:lab/wiki.py"],
                                                      capture_output=True, text=True).stdout)
    return d

r = subprocess.run(["git", "apply", "--check", os.path.abspath(RAW87)], capture_output=True, text=True,
                   cwd=pristine_tree("p1"))
check("S1a: 87d0's raw +92/-9 patch fails git apply --check at pristine HEAD (its index hunk)",
      r.returncode != 0 and "lab/wiki.py:83" in r.stderr, r.stderr.strip().replace("\n", "; "))

d2 = pristine_tree("p2")
applied = subprocess.run(["git", "apply", "--check", os.path.abspath(MERGED)], capture_output=True, text=True, cwd=d2)
shutil.rmtree(d2)
check("S1c: the merged patch (work/patch.diff) applies cleanly to pristine HEAD wiki.py",
      applied.returncode == 0, applied.stderr.strip())

d3 = pristine_tree("p3")
subprocess.run(["git", "apply", "--reject", os.path.abspath(RAW87)], capture_output=True, text=True, cwd=d3)
rej = [p for p in os.listdir(f"{d3}/lab") if p.endswith(".rej")]
one_hunk = rej == ["wiki.py.rej"] and "has_markers" in open(f"{d3}/lab/wiki.py.rej").read()
shutil.rmtree(d3)
check("S1b: exactly the index hunk rejects (the hand-merged one); the other four apply", one_hunk,
      f"rejects={rej}")

# --- S2 (P2): the real publish, replayed through the patched publisher -----------
wiki = patched
sim = f"{tmp}/sim"; shutil.copytree("lab/wiki", sim)
open(f"{sim}/wiki-memory.md", "w").write(PRE)  # the page as it stood at 2eb3's base
res = f"{tmp}/results"
os.makedirs(f"{res}/{PRIOR}/wiki")
open(f"{res}/{PRIOR}/DONE", "w").write("Grade: silver\n")
open(f"{res}/{PRIOR}/base", "w").write(BASE2EB3 + "\n")
open(f"{res}/{PRIOR}/wiki/wiki-memory.md", "w").write(PROPOSAL2EB3)
wiki.WIKI = sim
wiki.apply(res, BASE2EB3)
wiki.index()
landed = open(f"{sim}/wiki-memory.md", encoding="utf-8").read()
l_ids = [l.split()[1] for l in runs_of(landed)]
c = Counter(l_ids)
row = [l for l in open(f"{sim}/index.md") if "wiki-memory" in l][0].strip()
check("S2a: landed page has exactly 3 Runs lines, one per id {de18, 87d0, 2eb3}",
      len(l_ids) == 3 and max(c.values()) == 1 and set(c) == {"20261016-1835-inversion-de18", "20261016-2327-taleb-87d0", PRIOR},
      f"{len(l_ids)} lines, per id {dict(c)}")
de18 = [l for l in runs_of(landed) if "inversion-de18" in l][0]
a87 = [l for l in runs_of(landed) if "taleb-87d0" in l][0]
check("S2b: the graded wordings stand (de18 silver, 87d0 gold) — the stale variants are gone",
      "(silver)" in de18 and "compounds conflicts" in de18 and "(gold)" in a87 and "awaiting grade" not in de18 and "awaiting grade" not in a87,
      f"de18: {de18[:60]}... | 87d0: {a87[:60]}...")
check("S2c: body above ## Runs is byte-identical to what the shipped publish landed",
      body_of(landed) == body_of(SHIPPED))
check("S2d: zero marker lines of all three kinds, no UNMERGED banner",
      markers3(landed) == 0 and wiki.UNMERGED not in landed)
check("S2e: index row is '| open | 3 |' with neither flag",
      row.startswith(f"| [wiki-memory](wiki-memory.md) | open | 3 |") and "**conflict to resolve**" not in row and "**over budget" not in row,
      row[:70])
landed_hash = hashlib.sha256(landed.encode()).hexdigest()

# --- S3 (P3): re-publishing the same run is a byte-identical no-op ---------------
wiki.apply(res, BASE2EB3)
again = open(f"{sim}/wiki-memory.md", encoding="utf-8").read()
check("S3: second apply of the same run leaves the page byte-identical (the skip)",
      hashlib.sha256(again.encode()).hexdigest() == landed_hash)
row3 = [l for l in open(f"{sim}/index.md") if "wiki-memory" in l][0].strip()
check("S3b: index row unchanged after the no-op re-publish", row3 == row)

# --- S4 (P4): the next publish (this run's page, with a corrected 2eb3 line) ------
os.makedirs(f"{res}/{RUNID}/wiki")
open(f"{res}/{RUNID}/DONE", "w").write("Grade: silver\n")  # stand-in: the gate checks membership in {gold, silver}
open(f"{res}/{RUNID}/base", "w").write(BASEMINE + "\n")
shutil.copy(f"{RUN}/wiki/wiki-memory.md", f"{res}/{RUNID}/wiki/wiki-memory.md")
wiki.apply(res, BASEMINE)
wiki.index()
final = open(f"{sim}/wiki-memory.md", encoding="utf-8").read()
f_ids = [l.split()[1] for l in runs_of(final)]
cf = Counter(f_ids)
rowf = [l for l in open(f"{sim}/index.md") if "wiki-memory" in l][0].strip()
check("S4a: 4 Runs lines, one per id (6ccc appended), still 0 markers, flags clear",
      len(f_ids) == 4 and max(cf.values()) == 1 and RUNID in cf and markers3(final) == 0
      and "**conflict to resolve**" not in rowf and "**over budget" not in rowf,
      f"{len(f_ids)} lines, per id {dict(cf)}")
p2 = [l for l in runs_of(final) if l.split()[1] == PRIOR]
check("S4b: the corrected 2eb3 line ('silver') REPLACED 'awaiting grade', not added beside it",
      len(p2) == 1 and "(silver)" in p2[0] and "awaiting grade" not in p2[0], f"{p2}")
check("S4c: no id carried by either side was lost across both publishes",
      set(cf) == {"20261016-1835-inversion-de18", "20261016-2327-taleb-87d0", PRIOR, RUNID})

# --- S5 (P5): negative control — the same replay through pristine HEAD wiki.py ----
sim2 = f"{tmp}/sim2"; shutil.copytree("lab/wiki", sim2)
open(f"{sim2}/wiki-memory.md", "w").write(PRE)
res2 = f"{tmp}/results2"
shutil.copytree(res, res2, ignore=shutil.ignore_patterns(RUNID))  # only the prior run, as it really happened
pristine_py = f"{tmp}/pristine-wiki.py"
open(pristine_py, "w").write(subprocess.run(["git", "show", "HEAD:lab/wiki.py"], capture_output=True, text=True).stdout)
pw = load(pristine_py, sim2)
real_git = pw.git
def fake_git(*a, check=True):
    if a and a[0] == "show":  # the base page, served from git at the run's true base
        class R2: returncode, stderr = 0, ""
        r2 = R2(); r2.stdout = PRE
        return r2
    return real_git(*a, check=check)
pw.git = fake_git
pw.WIKI = sim2
pw.apply(res2, BASE2EB3)
shipped_land = open(f"{sim2}/wiki-memory.md", encoding="utf-8").read()
s_ids = [l.split()[1] for l in runs_of(shipped_land)]
cs = Counter(s_ids)
check("S5: control — the shipped publisher re-adds the stale lines (6 lines: de18×3, 87d0×2, 2eb3×1)",
      len(s_ids) == 6 and cs["20261016-1835-inversion-de18"] == 3 and cs["20261016-2327-taleb-87d0"] == 2 and cs[PRIOR] == 1,
      f"{len(s_ids)} lines, per id {dict(cs)}")
check("S5b: control lands the page HEAD carries today (the replay is the real publish)",
      body_of(shipped_land) == body_of(SHIPPED) and runs_of(shipped_land) == runs_of(SHIPPED))

# --- S6 (P6): the corpus ceiling for the id-keyed fold ---------------------------
pages = [p for p in sorted(os.listdir("lab/wiki")) if p.endswith(".md") and p not in ("index.md", "README.md")]
dup_pages, lines_before, lines_after, lost = [], 0, 0, []
for p in pages:
    t = open(f"lab/wiki/{p}", encoding="utf-8").read()
    lines = wiki.split_runs(t)[1]
    ids = [l.split()[1] for l in lines if l.startswith("- ") and len(l.split()) > 1]
    if len(ids) != len(set(ids)):
        dup_pages.append((p, len(ids) - len(set(ids))))
    folded = wiki.fold_runs(lines, [])
    lines_before += len(lines); lines_after += len(folded)
    f_ids = [l.split()[1] for l in folded if l.startswith("- ") and len(l.split()) > 1]
    if set(ids) != set(f_ids):
        lost.append(p)
    if len(f_ids) != len(set(f_ids)):
        lost.append(p + "(still dup)")
check("S6: >=25 of 40 pages carry duplicate run ids today; the id-keyed fold clears every page and loses no id",
      len(pages) == 40 and len(dup_pages) >= 25 and not lost,
      f"{len(dup_pages)}/{len(pages)} pages dup ({sum(d for _, d in dup_pages)} dup lines), {lines_before}->{lines_after} lines, problems={lost}")

fails = [n for n, ok, _ in results if not ok]
for n, ok, d in results:
    print(f"{'PASS' if ok else 'FAIL'}  {n}" + (f"  [{d}]" if d else ""))
print(f"\n{len(results) - len(fails)}/{len(results)} checks pass")
shutil.rmtree(tmp)
sys.exit(1 if fails else 0)
