#!/usr/bin/env python3
"""Folds this run's result into the kick-cadence page (copy of lab/wiki/kick-cadence.md
with the new current-best paragraph, the refuted entry, open direction 1 decided, and
the runs line). Run from the repo root; writes this run's wiki/ proposal."""
import pathlib, re

SRC = pathlib.Path("lab/wiki/kick-cadence.md")
DST = pathlib.Path("lab/results/20261017-1149-fermi-de7b/wiki/kick-cadence.md")
RUN = "20261017-1149-fermi-de7b"
page = SRC.read_text()

page = page.replace("updated: 20261017-0552-fermi-4e2d", f"updated: {RUN}", 1)

best = """**Open direction 1 is decided: the boundary comb is welded to the kick comb's own step and
rides every step-length lever.** `kick_clock` schedules both items from one `full`
(boundary at `t + full/2`, kick at `t + full`; `step.rs:705/717/718`; `boundary_clock` plans
nothing, and `ds` has no other cadence input), so no split can leave the boundary behind:
across three octaves of the shipped `step_log2` at N = 10⁴ the per-body belt stream scales
exactly (rate 0.2500× / 1.0000× / 4.0003× shipped, h p50 28,141 / 14,071 / 7,035 game-s —
the shipped arm 8ffc/3294's 14,071–14,072 to the digit — with B = 2h·j, K − B = h,
interval = 2h exact to 4 decimals and 2/4/8 events per body as typed integers, 100% of
9,700 belt bodies, dead 0), and `BELT_SPLIT` is a step lever by 98cb's own 8.000×
first-kick anchor — the boundary rides it too. The 10⁹ ledger's negative branch (a
~15.7-M1-core boundary floor no split touches) is dead; the riding branch stands: 9.96 M1
cores at split 8, S* ≈ 19.9× closes CPU (4e2d's 10.3 / 20.7 confirmed), the boundary term
the +25% CPU correction at every S. Build constraint for any split: coarsen Δs, never skip
planned kicks (a skipping split strands the boundary comb) (20261017-1149-fermi-de7b,
fermi)."""
page = page.replace("## Current best\n", "## Current best\n" + best + "\n\n", 1)

refuted = """- **"If `BELT_SPLIT` does not stretch the boundary comb, it becomes the composed stream's
  majority" (this page's open direction 1, the unclosable ~15.7-M1-core branch): dead by
  mechanism and flight — the boundary is scheduled from the kick's own `full` at its
  midpoint (`step.rs:717`), and three octaves of the step lever move both combs together
  with every per-body identity exact (20261017-1149-fermi-de7b)."""
page = page.replace("## Refuted\n", "## Refuted\n" + refuted + "\n", 1)

# Open direction 1: decided.
d1 = re.compile(r"1\. \*\*Does `BELT_SPLIT` stretch the boundary comb.*?\(20261017-0005-dynamics-8ffc\)\.\n", re.S)
decided = """1. **Decided (20261017-1149-fermi-de7b): the boundary comb rides any step-length lever with
   the kick comb** (it is the midpoint of the kick's own step; three octaves of
   `step_log2` measured, per-body identities exact). The constraint it leaves: splits must
   coarsen Δs, never skip planned kicks. What stays open is only the split's legality at
   S ≈ 20 (B-gates; 7f97/1db4's question).
"""
assert d1.search(page), "open direction 1 anchor not found"
page = d1.sub(decided, page, count=1)

runs = "- {RUN} (fermi, this run): the boundary comb rides the step lever (3 octaves, per-body identities exact, 100% of bodies); the 10⁹ pinned-boundary floor is dead; riding stands — 9.96 M1 cores at split 8, S* ≈ 19.9×.".replace("{RUN}", RUN)
if not page.endswith("\n"):
    page += "\n"
page += runs + "\n"

DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(page)
print(f"wrote {DST} ({len(page.splitlines())} lines)")
