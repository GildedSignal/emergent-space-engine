#!/usr/bin/env python3
"""The completeness sweep: grade + abstract for every published lab branch.

Regenerates sweep.jsonl (654 branches, ~3 s) so a checker can re-derive the
fold set: filter these rows for cadence-primary claims not already homed
(see dossier.md 'The sweep'). Usage: python3 sweep.py [outfile].
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
refs = subprocess.run(
    ["git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin"],
    capture_output=True, text=True, cwd=RUN.parents[2]).stdout.split()
refs = [r for r in refs if re.match(r"origin/claude/lab-", r)]
out = open(sys.argv[1], "w") if len(sys.argv) > 1 else sys.stdout
for r in sorted(refs):
    rid = re.match(r"origin/claude/lab-(.+)$", r).group(1)
    for f in ("check.md", "checker-final.md"):
        c = subprocess.run(["git", "show", f"{r}:lab/results/{rid}/{f}"],
                           capture_output=True, text=True, cwd=RUN.parents[2])
        if c.returncode == 0 and c.stdout.strip():
            g = re.search(r"^Grade:\s*(\w+)", c.stdout, re.M)
            ab = re.search(r"\*\*Abstract\.\*\*(.{0,700})", c.stdout, re.S)
            print(json.dumps({"id": rid, "file": f,
                              "grade": g.group(1) if g else None,
                              "abstract": re.sub(r"\s+", " ", ab.group(1)) if ab else ""}),
                  file=out)
            break
    else:
        print(json.dumps({"id": rid, "file": None, "grade": None, "abstract": ""}), file=out)
