#!/usr/bin/env python3
"""Audit: every grade and dead-run classification cited by the page and dossier
matches the primary record on the published branch (origin/claude/lab-<id>).

Exit 1 on any mismatch. Run by regen.sh after extract.sh."""
import re
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[2]


def show(run_id: str, file: str) -> str | None:
    p = subprocess.run(
        ["git", "show", f"origin/claude/lab-{run_id}:lab/results/{run_id}/{file}"],
        capture_output=True, text=True, cwd=REPO,
    )
    return p.stdout if p.returncode == 0 else None


def grade_of(run_id: str) -> str:
    """gold/silver/lead from check.md; 'missing' if no check.md."""
    txt = show(run_id, "check.md")
    if txt is None:
        return "missing"
    m = re.search(r"^Grade:\s*(\w+)", txt, re.M)
    return m.group(1).lower() if m else "no-grade-line"


def cited_runs(text: str) -> list[tuple[str, str]]:
    out = []
    for m in re.finditer(r"-\s+(\d{8}-\d{4}[a-z0-9\-]*[a-z0-9])\s+\((\w+)\)", text):
        out.append((m.group(1), m.group(2).lower()))
    return out


fail = 0
for fname in ("wiki/coorbital-cert.md", "dossier.md"):
    f = RUN / fname
    if not f.exists():
        print(f"FAIL missing {fname}")
        fail += 1
        continue
    for run_id, claimed in cited_runs(f.read_text()):
        got = grade_of(run_id)
        if got != claimed:
            print(f"FAIL {fname}: {run_id} claimed {claimed}, branch says {got}")
            fail += 1

# Dead-run classification: no check.md AND (checker-final ends in 429/deadline
# or verdict VOID or nothing at all).
DEAD = [
    "20260930-1245-rung-r8-encounters-5d80",
    "20261006-0519-rung-r8-encounters-v4-0e5d",
    "20261006-0521-rung-r8-encounters-v4-6cd5",
    "20261006-1931-b-coorbital-cert-152e",
    "20261008-2349-inversion-d1b0",
    "20261009-0521-inversion-b1c0",
    "20261011-0324-inversion-0981",
    "20261012-0753-spacex-96dc",
    "20261012-0753-taleb-59d4",
    "20261006-0519-taleb-48d6",
    "20261006-0521-taleb-dbee",
    "20261006-0519-spacex-ffd6",
    "20261006-0521-spacex-36cb",
]
for run_id in DEAD:
    if show(run_id, "check.md") is not None:
        print(f"FAIL dead-list: {run_id} HAS a check.md")
        fail += 1
    else:
        print(f"ok   dead: {run_id}")

# Load-bearing needles: each must appear verbatim in the named run's record.
NEEDLES = [
    ("20261006-0346-taleb-09b5", "predictions.md", "by current distance"),
    ("20261006-0346-taleb-09b5", "check.md", "135"),
    ("20261012-0311-second-20261012-0138-taleb-74a1-4ec3", "check.md", "31/31 result lines"),
    ("20261009-1259-second-20261009-1210-inversion-c529-154a", "check.md", "epicycle-scale-vs-spacing"),
    ("20261010-1407-second-20261010-1302-taleb-bb88-b612", "check.md", "1.003"),
    ("20261009-1259-inversion-2360", "check.md", "dormancy-priced"),
    ("20261009-1858-inversion-9d6d", "check.md", "= m·E|Δn|·H/W"),
    ("20261006-0916-inversion-f0be", "check.md", "exponent 2.000"),
    ("20261007-0842-inversion-0a7a", "check.md", "2e·n_c/σ_λ"),
    ("20261007-1106-inversion-e618", "check.md", "79.7"),
    ("20261006-1249-inversion-fd48", "check.md", "m̂ = 11.1"),
    ("20261007-2057-taleb-efc9", "check.md", "98.5%"),
    ("20261007-2155-inversion-7655", "check.md", "2Π+4"),
    ("20261008-1337-inversion-c5ab", "check.md", "n·σe ≲ 3–6"),
    ("20261008-1947-taleb-1b5d", "check.md", "N·|Δλ*|/π"),
    ("20261011-0736-second-20261011-0614-inversion-b292-5033", "check.md", "1.45×10¹¹"),
    ("20261010-0100-inversion-b063", "check.md", "0.34n"),
    ("20261010-1407-inversion-5c2a", "check.md", "519"),
    ("20261010-1706-inversion-3775", "check.md", "null plane"),
    ("20261011-0517-taleb-3ebf", "check.md", "n/2"),
    ("20261009-0208-inversion-a937", "check.md", "2·n_p·n_r"),
    ("20261011-1814-spacex-a110", "check.md", "epicyclic channel"),
    ("20261010-0306-taleb-8af8", "check.md", "94.3% cross setups never hit"),
    ("20261012-1117-inversion-5ffb", "check.md", "cost-blind"),
]
for run_id, fname, needle in NEEDLES:
    txt = show(run_id, fname) or ""
    if needle not in txt:
        print(f"FAIL needle: {needle!r} not in {run_id}/{fname}")
        fail += 1
    else:
        print(f"ok   needle: {needle!r} @ {run_id.split('-')[-1]}")

print(f"\naudit: {'PASS' if fail == 0 else f'{fail} FAILURES'}")
sys.exit(1 if fail else 0)
