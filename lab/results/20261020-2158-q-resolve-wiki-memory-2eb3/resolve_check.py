#!/usr/bin/env python3
"""Decides the predictions in predictions.md and the dossier's numbers, mechanically.

Run from the repo root (regen.sh does). Reads only; writes only inside a temp dir.
"""
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
RUN = "lab/results/20261020-2158-q-resolve-wiki-memory-2eb3"
RUNID = "20261020-2158-q-resolve-wiki-memory-2eb3"
MINE = open(f"{RUN}/wiki/wiki-memory.md", encoding="utf-8").read()
CUR = open("lab/wiki/wiki-memory.md", encoding="utf-8").read()
DE18 = subprocess.run(["git", "show", "origin/claude/lab-20261016-1835-inversion-de18:lab/results/20261016-1835-inversion-de18/wiki/wiki-memory.md"], capture_output=True, text=True).stdout
A87 = subprocess.run(["git", "show", "origin/claude/lab-20261016-2327-taleb-87d0:lab/results/20261016-2327-taleb-87d0/wiki/wiki-memory.md"], capture_output=True, text=True).stdout

spec = importlib.util.spec_from_file_location("wiki", "lab/wiki.py")
wiki = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiki)

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

LINE_MARK = re.compile(r"^(<{7}|={7}|>{7})")
def line_markers(t):
    return sum(1 for l in t.splitlines() if LINE_MARK.match(l))
def sub_markers(t):
    return sum(t.count(c * 7) for c in "<=>")

# --- the flag's mechanism, reproduced on the shipped page ---------------------
check("flag-source: current page has 0 line-start markers but quotes the substring",
      line_markers(CUR) == 0 and "<<<<<<<" in CUR,
      f"line-start={line_markers(CUR)}, substring occurrences={CUR.count('<<<<<<<')}")

# --- grades from the branches (the Runs lines rest on them) -------------------
g_de18, g_87 = wiki.grade("20261016-1835-inversion-de18"), wiki.grade("20261016-2327-taleb-87d0")
check("grades: de18 silver, 87d0 gold", (g_de18, g_87) == ("silver", "gold"), f"{g_de18}, {g_87}")

# --- my page's shape ----------------------------------------------------------
best = MINE.split("## Current best", 1)[1].split("\n## ", 1)[0]
best_lines = [l for l in best.splitlines() if l.strip()]
check("mine: no literal marker sequence anywhere (all three kinds)", sub_markers(MINE) == 0, f"count={sub_markers(MINE)}")
check("mine: shorter than the shipped page (88)", len(MINE.splitlines()) < len(CUR.splitlines()), f"{len(MINE.splitlines())} vs {len(CUR.splitlines())}")
check("mine: current best <= 10 nonblank lines (was 23)", len(best_lines) <= 10, f"{len(best_lines)} lines")
runs_lines = [l for l in MINE.split("## Runs", 1)[1].splitlines() if l.startswith("- ")]
ids = [l.split()[1] for l in runs_lines]
check("mine: one Runs line per run id, all three present",
      sorted(ids) == sorted({"20261016-1835-inversion-de18", "20261016-2327-taleb-87d0", RUNID}), str(ids))
words = [len(l.split(":", 1)[1].split()) for l in runs_lines]
check("mine: every Runs claim <= 20 words", all(w <= 20 for w in words), str(words))

# --- P2: index() flag clears with my page --------------------------------------
tmp = tempfile.mkdtemp()
shutil.copytree("lab/wiki", f"{tmp}/wiki")
wiki.WIKI = f"{tmp}/wiki"
wiki.index()
before = [l for l in open(f"{tmp}/wiki/index.md") if "wiki-memory" in l][0].strip()
shutil.copy(f"{RUN}/wiki/wiki-memory.md", f"{tmp}/wiki/wiki-memory.md")
wiki.index()
after = [l for l in open(f"{tmp}/wiki/index.md") if "wiki-memory" in l][0].strip()
check("P2: row before has both flags, after has neither, runs = 3",
      "**conflict to resolve**" in before and "**over budget" in before
      and "**conflict to resolve**" not in after and "**over budget" not in after
      and "| open | 3 |" in after, f"after: {after}")

# --- P5: main's publisher is unpatched at HEAD ---------------------------------
head_py = subprocess.run(["git", "show", "HEAD:lab/wiki.py"], capture_output=True, text=True).stdout
hits = [w for w in ("defuse", "heal", "skip") if w in head_py]
check("P5: HEAD wiki.py carries no defuse/heal/skip", not hits, f"found={hits}")

enc = open("lab/wiki/encounters.md", encoding="utf-8").read()
enc_ids = [l.split()[1] for l in enc.split("## Runs", 1)[1].splitlines() if l.startswith("- ")]
dup = sorted({i for i in enc_ids if enc_ids.count(i) > 1})
check("P4: encounters carries the same Runs-union artifact (same id on >1 line)", len(dup) >= 1, f"{dup}")

# --- the three damaged pages were folded by their next runs ----------------------
folded = []
for page, folder in (("nladder", "20261020-1210-library-a31c"), ("encounters", "20261019-1906-scout-f2f1"),
                     ("scan-queue", "20261018-0543-second-20261018-0431-system-0e9c-d7d1")):
    t = open(f"lab/wiki/{page}.md", encoding="utf-8").read()
    folded.append((page, line_markers(t), folder in t))
check("the three healed pages stand marker-free, folded by the cited runs",
      all(m == 0 and c for _, m, c in folded), str(folded))

# --- P1: publish simulation through the SHIPPED apply() --------------------------
real_git = wiki.git
class R:  # stand-in for the git-show of the base page: exactly HEAD's page
    returncode, stdout, stderr = 0, CUR, ""
def fake_git(*a, check=True):
    if a and a[0] == "show":
        return R()
    return real_git(*a, check=check)
wiki.git = fake_git
sim = tempfile.mkdtemp()
os.makedirs(f"{sim}/results/{RUNID}/wiki")
open(f"{sim}/results/{RUNID}/DONE", "w").write("Grade: silver\n")
open(f"{sim}/results/{RUNID}/base", "w").write(subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout)
shutil.copy(f"{RUN}/wiki/wiki-memory.md", f"{sim}/results/{RUNID}/wiki/wiki-memory.md")
shutil.copytree("lab/wiki", f"{sim}/wiki")
wiki.WIKI = f"{sim}/wiki"
wiki.apply(f"{sim}/results", "HEAD")
merged = open(f"{sim}/wiki/wiki-memory.md", encoding="utf-8").read()
m_ids = [l.split()[1] for l in merged.split("## Runs", 1)[1].splitlines() if l.startswith("- ")]
c = Counter(m_ids)
check("P1: shipped apply() re-adds the stale lines (union on exact text, no skip)",
      len(m_ids) >= 5 and c["20261016-1835-inversion-de18"] >= 2 and c["20261016-2327-taleb-87d0"] >= 2,
      f"{len(m_ids)} runs lines, per id {dict(c)}, markers in merged body {line_markers(merged)}")

# --- P3: coverage — every supported claim of both sides survives in mine ---------
ASSERTS = [
    ("de18", "crafted window markers 1→4→8"), ("de18", "depth = count"), ("de18", "depth 2→3"),
    ("de18", "0→7 markers in one publish"), ("de18", "20261016-1637 window 19→46"), ("de18", "orphan mids 1→4"),
    ("de18", "5/5 worst case"), ("de18", "history census + crafted replay"),
    ("de18", "leak into the index row while authors stop compiling"),
    ("de18", "32 content sides preserved verbatim"), ("de18", "superseding its earlier 30-line form"),
    ("de18", "markers then hide the runs' conclusions"),
    ("87d0", "stack-pairing"), ("87d0", "drops orphan mid/close syntax"), ("87d0", "renders truncated tails recursively"),
    ("87d0", "summary()` never returns marker text"), ("87d0", "19 marker lines: 7/7/5, 1 orphan mid, 2 never-closed blocks"),
    ("87d0", "zero of all three kinds with zero content lines lost"), ("87d0", "instrument sharing no logic with the fix"),
    ("87d0", "Runs lists byte-identical, unmarked pages untouched, index leak 0"),
    ("87d0", "+2/+2 runs, 8 labeled banners"), ("87d0", "from the damaged start (13 banners), idempotent"),
    ("87d0", "dynamics-87fd is a no-op, vs 14 banners and +50 lines"), ("87d0", "+92/−9"),
    ("87d0", "one merge plus one `heal`"), ("87d0", "exactly seven `=`"), ("87d0", "all 27 pages checked"),
    ("87d0", "the disclosure, not the instrument, carries it"),
    ("87d0", "renamed id is not skipped"), ("87d0", "under a new id or fold by hand"),
    ("87d0", "anchors on the *first* header"), ("87d0", "duplicated a runs line and deleted a prose line"),
    ("87d0", "splits runs before `merge-file`"), ("87d0", "hoisting embedded headers in `heal`"),
    ("87d0", "zero markers and zero content loss on all three real pages"),
]
missing = [(s, a) for s, a in ASSERTS if a not in MINE]
check("P3: every claim assertion from both proposals matches the resolved page", not missing, f"missing={missing}")
# nothing was invented: every run id on my page comes from the two sides, the folded pages, or is this run
cited = set(re.findall(r"2026\d{4}-\d{4}-[a-z0-9-]+", MINE)) - {RUNID, "20261016-1835-inversion-de18", "20261016-2327-taleb-87d0"}
known = set(re.findall(r"2026\d{4}-\d{4}-[a-z0-9-]+", DE18 + A87)) | {
    "20261020-1210-library-a31c", "20261019-1906-scout-f2f1", "20261018-0543-second-20261018-0431-system-0e9c-d7d1",
    "20261017-1018", "20261017-1018-second-20261017-0839-inversion-2373-b509"}
check("P3: no invented run citations", cited <= known, f"unknown={cited - known}")

# --- verdict ---------------------------------------------------------------------
fails = [n for n, ok, _ in results if not ok]
for n, ok, d in results:
    print(f"{'PASS' if ok else 'FAIL'}  {n}" + (f"  [{d}]" if d else ""))
print(f"\n{len(results) - len(fails)}/{len(results)} checks pass")
sys.exit(1 if fails else 0)
