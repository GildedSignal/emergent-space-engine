Working...
Check complete: **Grade: gold**, written to `lab/results/20261014-1137-fermi-1738/check.md`.

**What I verified:**

- **Reproduction (independent).** Recomputed every audited number with my own script from primary constants: 90fb's "0.966/0.077 per cell" row re-derives as the billion's partitioned **total** (222/s × island wake), and that exact composition regenerates 90fb's own stored "max rtf on 4 cores = 5,216" to 0.06%. The decisive self-contradiction: a true per-cell cost is 9.66e-6 cores; ×10⁵ cells returns 0.966 — so the label cannot be literal, forced by 90fb's own bottom row. effb's `ledger.py:108` (`0.077·(N/1e4)`) then double-bills the kick stream, and its 1,925×/7,051× divide an rtf-100 term by rtf-1 terms. All 12 cube cells, walls, and kick-term numbers match `ledger2-out.txt`.
- **Fresh anchor.** Ran the shipped `kick` experiment myself: integers bit-identical (812.8, 0.0024, 0.9458), timings within 3%.
- **Outside-range attack.** Rebuilt 90fb's bench against the shipped crate and ran the pairs law at n=3×10⁶ — one decade beyond the entire measured record the cube extrapolates from: 51,187 vs 52,596 predicted (X=150, +2.8%), 259,309 vs 259,500 (narrow, +0.1%). The extrapolation to 10⁹ holds.
- **Novelty.** The mislabel propagates through 90fb's dossier, both of 90fb's checkers, effb's ledger and its checker, `lab/wiki/encounters.md:13`, HANDOFF:58 and the board — no prior document contains the audit.
- **Page.** The proposed fold-in is faithful; I corrected one overstatement in place (locality 2.3× → 2.2×, per the author's own ledger).

Gold because it's a premise correction with a one-line checkable proof ("shows that a premise is wrong"), fully reproduced, predictions pre-registered and held, adoptable in one step at zero code. Recorded misses: the "~10² (islands)" ratio mislabel in dossier Evidence 5, the κ-vs-κ/P conflation in the "457×" lever label, the unsourced 7,275.5 M1-factor divisor, and reliance on 90fb's stored (not re-run) verify/queue evidence.
