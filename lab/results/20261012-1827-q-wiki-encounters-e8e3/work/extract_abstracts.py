#!/usr/bin/env python3
"""Re-extract the 65 clustered runs' checker abstracts from their refs.

Writes work/abstracts.md (first ~130 words of each check.md, plus grade lines),
the same raw input the compile read. The 5 branches without check.md are
recorded as NO check.md (rungs also get their verdict.txt shown)."""
import re, subprocess
from pathlib import Path

IDS = [l.strip() for l in open(Path(__file__).with_name("ids.txt")) if l.strip()]

def show(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

out = []
for rid in IDS:
    ref = f"origin/claude/lab-{rid}"
    check = show(ref, f"lab/results/{rid}/check.md")
    if check is None:
        verdict = show(ref, f"lab/results/{rid}/verdict.txt")
        extra = f"verdict: {verdict.strip()!r}" if verdict else "no graded record"
        out.append(f"\n===== {rid} : NO check.md ({extra}) =====\n")
        continue
    g = re.findall(r"(?i)grade[^.\n]*", check)[:3]
    head = " ".join(check.split()[:130])
    out.append(f"\n===== {rid} =====\nGRADE-LINES: {g}\nABSTRACT-130w: {head}\n")

dst = Path(__file__).with_name("abstracts.md")
dst.write_text("\n".join(out))
print(f"wrote {dst} for {len(IDS)} runs")
