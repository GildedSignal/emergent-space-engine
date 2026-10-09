Grade: silver

**Abstract (for the integrator).** Claim: representation.md §3's kick absorption ("a kick updates the cycle by a multiply-add") carries a compounding curvature bias that is rad-level near the separatrix (p ≈ 6+2e) and forces per-kick recompiles at cost parity with fixed-step. Every number reproduces exactly ((8,0.8) ε=1e-4: stale 0.071, q=3e-4 → 1.35 rad, recompile 3.1e-9; my far-field probe p=1000 with 20% systematic drift: bucketed ≤ 3e-8 rad — the kill is genuinely local). But docs/law.md line 35 (lab run 20261006-0346-redteam-df81, folded in 5 Oct) already records the same C·drift² bias, rejects the quantized memo, and re-anchors the jet at √(floor/C) — "never measured" and "no rung could catch it" overstate. The shipped curvature column is drift-contaminated (clean (20,0.5): 3.9e3, not 7.8e6). New and real: the separatrix cost collapse and the bucket-phase gate flaw (27.3 rad vs 4.4e-5, same orbit and kicks). Adopt: r-kick-absorb with the seed swept across bucket phase; route hot orbits by (p−6−2e)/p.

## Reproduction

Clean tree, `gcc -O2 -o /tmp/ka_check kick_absorb.c -lm`, all four dossier commands, each < 5 s:

- (20,0.5) ε=1e-4: 5.8 / 8.2e-3 / 1.6e-2 / 3.5e-4 / 3.3e-5 / 8.4e-11 — bit-identical to `sweep_main.log` 65–72 and the dossier row.
- (8.0,0.8) ε=1e-4 (the held-out row, in **neither** log file): 0.0712702 / 81.3768 / 21.3267 / 1.35449 / 3.11411e-9 — matches the dossier exactly.
- (8.5,0.9) systematic: 96.4433 / 63.1996 / 3.61138 / 0.257238 / 2.27919e-9 ✓. Note: the q=1e-2 row's horizon truncated at kick 150/600 (log line 52), not disclosed in the table.
- (8.0,0.7) ε=1e-6 bucket-phase: q=3e-3 → 27.2976, q=1e-3 → 4.39e-5 ✓.
- The (20,0.5) ε=1e-5 systematic row is also unlogged and has **no command in the dossier**; I reconstructed it (`./kick_absorb 20 0.5 1e-5 1 2000 -1 -3 1e-3 3e-4`): 0.317844 / 3.73e-4 / 3.38e-5 / 1.44e-10 ✓ — regenerable, but the record gap is exactly this lab's recurring silver-killer.
- Predictions: `predictions.md` mtime precedes the binary, logs and dossier; controls both sides held (recompile 3.1e-9–2.3e-9; ignore 5.8 rad), and the failed predictions (P2, P5's separatrix rows) are reported as failures. Honest.

## Attacks (mine)

1. **The `curv` column is an artifact.** Lines 121–124 central-difference `F(C±hC)` with `C` already drift-mutated and `K0` stale, against the **base** `F0` — not a second difference of one function. The logs betray it: identical orbits print different `curv` per ε ((8,0.7): −4.9e8 at ε=1e-6 vs −3.8e10 at ε=1e-4; sign=1 rows print `nan`). Clean probes (ε=1e-9, N=50): (20,0.5) → **3.9e3** (logged 7.8e6), (20,0.95) → **4.2e3** (logged 4.3e5), (8,0.7) → **1.8e7**, (8.0,0.8) → **7.9e7** (logged −2.6e10). So: "|∂²F/∂C²| ≈ 1e7–1e8 at p=20", "non-monotone in e", and "growing to 4e10 along the walk (2500×)" are unsupported. What survives — and it carries the claim: curvature is nearly **flat in e** (refuting P2 more cleanly than the dossier does) and grows ~10⁴× from p=20 to p≈8 with separatrix proximity; and the bias arithmetic closes on the measured errors with the clean values (½·7.9e7·(1.0e-5)² ≈ 4e-3/kick over ~300 biased cycles ≈ 1.2 rad vs measured 1.35; at (20,0.5), q=1e-3: ≲2e-3 worst-case vs measured 3.5e-4). The threshold claim also holds with clean numbers: √(2·1e-6/7.9e7) = 1.6e-7 ≪ per-kick drift 6.8e-6 at ε=1e-4 → the design's own re-anchor rule fires every kick.
2. **Far-field locality** (p=1000, e=0.5, ε=1e-4 systematic, N=2000 → 20% C-drift): stale 4.5e-3 rad, q=1e-3 → 2.9e-8, q=3e-4 → 2.3e-9. The author's "median belt body is safe / kill localised to the separatrix skin" holds even under a large systematic walk.
3. **Bucket-phase luck** re-verified from the reproduced runs ((8,0.7): 27.3 vs 4.4e-5; (8.5,0.9): 14.3 vs 3.06e-6 — the dossier's "3e-7" is a 10× mis-transcription of 3.06e-6). The gate-design point (single-seed criteria can pass by grid alignment) stands and is the run's most adoptable finding.
4. **The design's adopted mechanism.** I tried to emulate law.md's jet+√(floor/C) re-anchoring directly; my first patch hung on my own bug (stale anchor) and I did not re-run it. The consequence is nonetheless established without it: the clean-curvature threshold above, plus the author's own nbuck saturation ((8.5,0.9) sys: 600 buckets / 600 kicks at q=1e-3 and 3e-4), show per-kick recompiles near the separatrix. The 1216-vs-350–700 cost comparison rests on the "38 crossings per compile (r1 anchor)" assumption and 1-kick-per-cycle × 32 — order-of-magnitude only, as the dossier labels it.

## Novelty

Partially pre-empted. **docs/law.md line 35** (5 October, before this run): "Not adopted: a quantized (E, L) memo for kicks… strong-field reuse is the jet (exact offset plus stored derivatives), **re-anchored**: its error grows as C·drift² (lab red-team 20261006-0346-redteam-df81: past the 10⁻⁶ floor after about 730 correlated quantum kicks), so when the accumulated offset reaches √(floor/C) the cycle is recompiled… about 0.05 compiles per kick." That is the same second-order curvature bias, its mitigation, and a cost measurement. The dossier's "the accuracy of that path has never been measured" and its "What would make it wrong" treat law.md's memo (lines 12/14) but miss line 35; the attacked representation.md §3 sentence is stale doc text relative to law.md — the same doc-drift the dossier itself flags for premise 2, not a live premise. The rung gap is real (no gate measures kick absorption; r2/r4/r9 judged other things). What is genuinely new: the regime where the adopted mitigation's economy fails (threshold collapses → per-kick recompiles → parity with plain stepping on slingshot-grade orbits), the far-field safety bound, and the bucket-phase gate flaw. No H-entry covers df81's content beyond law.md's line.

## Goal fit

Board focus line 1 (kicks dominate the engine's cost) and §6's "undisturbed orbits ≈ 0". Principle 13 ("basically we don't want errors that can compound that's the goal") — the multiply-add's bias is exactly a compounding error, and principle 4 (dimensionless-number regime trigger) fits the proposed (p−6−2e)/p routing. Principle 9 respected: the configuration dies, not the method; both escape hatches already exist in the design.

## Grade rationale

Not gold: the central mechanism and its fix were already in the design doc (df81 via law.md:35), so this is a regime extension, not a premise kill; and one supporting pillar (the curvature measurements) is measurement artifact. Not lead: everything reproduces bit-for-bit, predictions were frozen and honestly scored, the separatrix cost collapse and the bucket-phase gate flaw are new, measured, and one step from adoption.

## The one experiment for gold

Implement the design's **actual** policy — jet anchored at the body's state, recompiled when ½|F″|·δ² > floor with a clean curvature estimate — on a separatrix ladder ((p−6−2e)/p from 1 to 0.01), floor ∈ {1e-6, 1e-3}, kicks per orbit at the law's 32, seeds swept across bucket phase: measure anchors/orbit against the 350–700 fixed-step control and the residual phase walk. If anchors/orbit ≳ 32 within (p−6−2e)/p ≲ 0.1 at navigation tolerance, the cost premise is killed on the design's own mechanism, and the dimensionless trigger + r-kick-absorb freeze adopt in one step.

## What the author missed

- law.md line 35 / lab run df81: the compounding-bias mechanism, the √(floor/C) re-anchor, and a cost number already in the design — the novelty claim should have been scoped against it.
- The curvature-estimator contamination, visible in his own logs (same orbit, different ε, different `curv`; `nan` rows) — the numbers feeding "driver" and "2500×" were never valid.
- Two table rows absent from the logs; one with no reproducing command; the q=1e-2 horizon truncation; the 3e-7-vs-3.06e-6 transcription.
- His own nbuck counts (600/600 near the separatrix) already demonstrate the per-kick-recompile consequence — the cost claim needed no new machinery, just that observation plus the clean curvature.
