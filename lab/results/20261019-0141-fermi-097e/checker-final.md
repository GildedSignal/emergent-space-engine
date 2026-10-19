Working...
Check complete. `check.md` written, page corrected, tree left clean (patch reverted; only the untracked run folder remains).

## Verdict: **silver**

**Reproduced in full** (clean tree, patch applied by me, my own build):
- Both flights match: `b_per_body` 2,463/2,348 B, total kicks ≈2,137 **identical** at 10⁴ and 10⁵ (the inert-belt census), held_max 1. `ledger.py` output JSON **bit-identical** to the shipped one; every one of ~20 page-cited constants verified on its wiki page (cd3b, 08d0, 1a29, a9d7, 4b55, 07b4, 0820, e3a4, e6c9, dcf1/99da, HANDOFF scoreboard); all totals recomputed exactly (10.8–16.6 cores, 363 conditional, 294×, 978×, τ = 43.57 gs, 66.8 GB).
- My adversarial arms, all outside the author's range: **N=3×10⁵ coast** (2,340 B/body on 99da's own value, belt still inert, frame flat, 705 MB) and **burn at 10⁵** (2,688 kicks = 1.26× coast but still O(1) in N, held_max 19) — both extend, neither breaks.
- Predictions: P1–P4, P6 held; P5 correctly did not fire; **P7 half-failed and is reported as failed** — the honest-miss pattern, and the miss (orbit-scale residency = 66.8 GB even for SOI promoters alone) is the run's most decision-relevant new number.

**Why not gold:** the two fresh flights measured nothing that dcf1/99da (byte-identical streams to 7×10⁵, coast *and* burn, same week) and the merged N1 gate (10⁶ flat) hadn't already measured — the wiki page's "census, new this run" overstated (corrected in place); the CPU composition existed piecewise (cd3b's own 5.3–8.4) and the encounters page holds competing compositions (1738's audited cube 0.077–3×10⁷ cores; 277d's 62–571) the ledger never squares against — the headline is the current-best *corner*, not a bound (domain note added); `ledger.py` hardcodes anchors that drift from its own logs in the 4th digit (2.139e-5 vs 2.133e-5). Also found: contacts (cd3b's 0.22/s) make the residency dial ~6× tighter than reported (≈395 GB at orbit scale) — added to the page.

**The one experiment to gold:** measure the promotion fraction — fly 5f36's tier on the ladder under a9d7's fired-kick stream; it converts the τ dial from arithmetic on a 5.1 KB assumption into a measured law.
