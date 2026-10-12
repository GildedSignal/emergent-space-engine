#!/usr/bin/env python3
"""Full-text sweep of every non-cluster claude/lab-* branch for memory-h-live
primary runs.

For each branch outside the compiler run's 111-run cluster (work/runs.txt):
  - pull the FULL dossier.md text (not just its head);
  - pull the check.md head (grade);
  - score the dossier against memory-h-live markers (full text and Claim+Bottleneck).

Hits are printed with id, grade, and the Claim section for manual classification.
Runtime ~1-2 min (650 git shows).
"""
import pathlib, re, subprocess, sys

here = pathlib.Path(__file__).parent
cluster = {l.strip() for l in open(here / "runs.txt") if l.strip()}

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout

branches = [b.strip() for b in
            git("branch", "-r", "--format=%(refname:short)").splitlines()
            if b.strip().startswith("origin/claude/lab-")]
ids = [b[len("origin/claude/lab-"):] for b in branches]

# memory-h-live markers (recall-oriented; classification is manual after)
MARK = re.compile(
    r"(H_live|live information|live state|live memory|bits/body|bits per body"
    r"|b/body|B/body|bytes per body|kB per|bits/s\b|bits/game|GB at 10|GiB\b"
    r"|memory floor|information floor|scar stock|scar layer|scars? saturat"
    r"|standing representation|per-body (state|record|memory|store)"
    r"|store saturat|memory saturat|bits/(scarred|live|member|ship)"
    r"|resident|RSS|Elias|entropy of|bits per (kick|scar|rebind|body))",
    re.I)

def section(text, name):
    m = re.search(rf"^##\s+{name}\b(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return (m.group(1).strip() if m else "")

rows = []
for rid, br in zip(ids, branches):
    if rid in cluster:
        continue
    dos = git("show", f"{br}:lab/results/{rid}/dossier.md")
    if not dos.strip():
        rows.append((rid, "NO-DOSSIER", 0, 0, ""))
        continue
    chk = git("show", f"{br}:lab/results/{rid}/check.md")[:1100]
    g = re.search(r"Grade: (\w+)", chk)
    grade = g.group(1) if g else "missing"
    claim = section(dos, "Claim")
    bottleneck = section(dos, "Bottleneck")
    cb = claim + "\n" + bottleneck
    n = len(MARK.findall(dos))
    ncb = len(MARK.findall(cb))
    rows.append((rid, grade, n, ncb, claim.replace("\n", " ")[:400]))

rows.sort(key=lambda r: (-r[3], -r[2]))
nonc = len([r for r in ids if r not in cluster])
# discovery record: every non-cluster branch with >= 1 marker, full dossier text scanned
with open(here / "sweep-hits.txt", "w") as f:
    for rid, grade, n, ncb, claim in rows:
        if n >= 1:
            f.write(f"{rid}\t{grade}\t{n}\t{ncb}\t{claim}\n")
print(f"branches total {len(ids)}, non-cluster {nonc}, "
      f"hits n>=1: {sum(1 for r in rows if r[2] >= 1)}, n>=3: {sum(1 for r in rows if r[2] >= 3)}, "
      f"no-dossier: {sum(1 for r in rows if r[1] == 'NO-DOSSIER')}")
print(f"{'run':58s} {'grade':8s} {'full':4s} {'CB':3s} claim")
for rid, grade, n, ncb, claim in rows:
    if n >= 3:  # broad recall bar for the manual pass
        print(f"{rid:58s} {grade:8s} {n:<4d} {ncb:<3d} {claim[:340]}")
