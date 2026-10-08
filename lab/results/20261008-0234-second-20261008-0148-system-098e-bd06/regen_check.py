#!/usr/bin/env python3
"""Does the author's record regenerate from shipped code? toy_out_*.json in
this folder were produced by `python3 toy_news.py c30|c300|per` (regen_c*.txt
hold those runs' console output, ~50 s each); this compares their content
(elapsed time aside) against the committed record on
origin/claude/lab-20261008-0148-system-098e and reprints smear.py's headline."""
import json, subprocess, sys

BRANCH = "origin/claude/lab-20261008-0148-system-098e"
RUN = "lab/results/20261008-0148-system-098e"

def load_branch(path):
    return json.loads(subprocess.check_output(
        ["git", "show", f"{BRANCH}:{RUN}/{path}"]))

ok = True
for cfg in ("c30", "c300", "per"):
    mine = json.load(open(f"toy_out_{cfg}.json"))
    auth = load_branch(f"toy_out_{cfg}.json")
    mine.pop("elapsed_s", None); auth.pop("elapsed_s", None)
    same = json.dumps(mine, sort_keys=True) == json.dumps(auth, sort_keys=True)
    ok &= same
    print(f"toy_news {cfg}: bit-identical to the author's record: {same}")
smear = subprocess.check_output(["python3", "smear.py"], text=True)
line = [l for l in smear.splitlines() if "absolute lateness" in l][0]
print("smear.py:", line.strip())
print("(author's committed run: med 2.74 max 3.36; matches)")
sys.exit(0 if ok else 1)
