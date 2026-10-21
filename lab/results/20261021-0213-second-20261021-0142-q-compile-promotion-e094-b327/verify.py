#!/usr/bin/env python3
"""Audit work/record.json against the sandbox boxes replay.py left on disk.

Run via regen.sh (replay.py must have just built the boxes); standalone it
needs a prior replay. Recomputes the dossier's headline numbers straight from
the healed pages and the staged proposals, without touching git, so a silent
edit to record.json (or to a box) shows up as a mismatch.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, "work")
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location("wiki_b327", os.path.join(HERE, "..", "..", "..", "lab", "wiki.py"))
wiki = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiki)
split_runs = wiki.split_runs

rec = json.load(open(os.path.join(W, "record.json")))
checks, bad = [], []


def ck(name, cond, detail=""):
    checks.append(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        bad.append(name)


def stats(path):
    lines = split_runs(open(path, encoding="utf-8").read())[1]
    ids = [re.match(r"^- (\S+)", l).group(1) for l in lines if re.match(r"^- (\S+)", l)]
    return len(lines), len(set(ids)), len(ids) - len(set(ids))


# P4 — the named experiment's landed state, recomputed from the box
p4 = f"{W}/p4/lab/wiki/promotion.md"
if os.path.exists(p4):
    n, ids, dups = stats(p4)
    ck("P4 box: promotion 14/14/0", (n, ids, dups) == (14, 14, 0), f"{n}/{ids}/{dups}")
    prop = f"{W}/p4/results/20261021-0142-q-compile-promotion-e094/wiki/promotion.md"
    ck("P4 box: healed Runs == staged e094 proposal's Runs",
       split_runs(open(p4).read())[1] == split_runs(open(prop).read())[1])
    row = next(l for l in open(f"{W}/p4/lab/wiki/index.md") if "promotion" in l)
    ck("P4 box: index row open|14, no flag", "| open | 14 |" in row and "over budget" not in row)

# P6 — the window's four pages, and the corpus delta, recomputed
if os.path.isdir(f"{W}/p6/lab/wiki"):
    for page, want in [("promotion.md", 15), ("budget-1e9.md", 10), ("cell-rebind.md", 4), ("kick-jet.md", 57)]:
        p = f"{W}/p6/lab/wiki/{page}"
        n, ids, dups = stats(p)
        ck(f"P6 box: {page} {want} lines, 0 dups", n == want and dups == 0, f"{n}/{ids}/{dups}")
    out = json.loads(os.popen(f"python3 {HERE}/measure.py {W}/p6/lab/wiki").read())
    # 468 - 76 (the window's four pages, healed at P6) - 4 (wiki-memory, healed by P9's
    # mechanism replay in the same box) = 388 standing on older topics until their sweep/heal
    ck("P6 box: corpus dup total 388 after P6+P9", out["dup_lines_total"] == 388, str(out["dup_lines_total"]))

# P7b — the one-time heal cleared the standing corpus
if os.path.isdir(f"{W}/p7b/lab/wiki"):
    out = json.loads(os.popen(f"python3 {HERE}/measure.py {W}/p7b/lab/wiki").read())
    ck("P7b box: corpus dup total 0 after heal", out["dup_lines_total"] == 0, str(out["dup_lines_total"]))

# P9 — the next-publish mechanism replay
for page, want in [("promotion.md", (15, 15, 0)), ("wiki-memory.md", (5, 5, 0))]:
    p = f"{W}/p6/lab/wiki/{page}"
    if os.path.exists(p):
        n, ids, dups = stats(p)
        ck(f"P9 box: {page} {want[0]}/{want[1]}/{want[2]}", (n, ids, dups) == want, f"{n}/{ids}/{dups}")

# record.json self-consistency: verdict PASS and the dossier's headline numbers
ck("record: verdict PASS", rec.get("verdict") == "PASS", rec.get("verdict", ""))
d = rec.get("disease", {})
ck("record: disease 29/40 pages, 468 dups, promotion 32/14/18",
   (d.get("diseased"), d.get("pages"), d.get("dup_lines")) == (29, 40, 468)
   and d.get("promotion") == {"lines": 32, "ids": 14, "dups": 18}, json.dumps(d))
ck("record: 02:12 window added 34", sum(d.get("window_added", {}).values()) == 34,
   json.dumps(d.get("window_added")))

print("\n".join(checks))
print(f"VERIFY: {'PASS' if not bad else 'FAIL: ' + ', '.join(bad)}")
sys.exit(1 if bad else 0)
