#!/usr/bin/env python3
"""P1 reconciliation: two-checker grades on the branch vs the assignment sheet."""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"

PAT = re.compile(r"grade[^\n]{0,40}?(\b(?:gold|silver|lead|void)\b)", re.I)


def show(ref: str) -> str:
    return subprocess.run(["git", "show", ref], capture_output=True, text=True).stdout


def grade_of(rid: str, which: str):
    txt = show(f"origin/claude/lab-{rid}:lab/results/{rid}/{which}")
    if not txt:
        return None
    m = PAT.findall(txt)
    return m[0].lower() if m else None


def main():
    sheet = {}
    for line in (WORK / "sheet_grades.txt").read_text().splitlines():
        rid, grade = line.split()
        sheet[rid] = grade
    assert len(sheet) == 81
    out = []
    disagree = []
    for rid, sg in sheet.items():
        if sg == "missing":
            continue
        g1 = grade_of(rid, "check.md")
        g2 = grade_of(rid, "check2.md")
        if g1 == "gold" and g2 == "gold":
            derived = "gold"
        elif g1 is None and g2 is None:
            derived = "unrecorded"
        elif "lead" in (g1, g2) and "gold" not in (g1, g2):
            derived = "lead"
        else:
            derived = "silver"
        mark = ""
        if derived not in (sg, "unrecorded"):
            mark = "   <-- MISMATCH"
            disagree.append((rid, g1, g2, derived, sg))
        out.append(f"{rid:64s} c1={g1}  c2={g2}  sheet={sg}{mark}")
    report = "\n".join(out)
    (WORK / "grades-out.txt").write_text(report + "\n")
    print(report)
    print(f"\nmismatches: {len(disagree)}")
    for d in disagree:
        print("  ", d)


if __name__ == "__main__":
    main()
