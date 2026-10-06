# Dossier — 20261005-2231-q-secular-008e (lens: secular phasors, R2 falsifier)

**Claim.** R2 (stable belt bodies as zero-kick secular phasors) is KILLED at two-planet
belt scale by its own pre-registered rule: over 2,000 Jupiter orbits with Jupiter AND
Saturn, only 20.5% of 1,024 belt bodies pass rate-within-5% AND e-vector-within-10%
under the strongest phasor variant (exact double averaging), 0% under first-order
Laplace–Lagrange, against a converged Wisdom–Holman truth — because the belt's free
amplitudes are modulated ±60–280% by nonlinear secular coupling that linear phasors
cannot represent at all, and the planets' own driver (their mutual LL modes) is wrong
by 5× in Saturn.

**Bottleneck.** The plane's measured dominant cost (kicks: ~24 µs median, 15 µs of it
rebinding; board focus "fewer kicks per orbit"). R2 promised to delete all 64 kicks/orbit
for stable bodies and keep belt populations at their 0.126-bit program instead of ~82 B
scars. This run says that promise holds only for the inner belt (a < 2.5 AU, 61% pass
there), not for a belt as a whole.

**Evidence** (all in this folder; scene and estimators frozen in predictions.md BEFORE
the decisive runs):

- Scene: Sun + J + S (mutual), 1,024 test bodies, a ~ U[2.0, 3.3], e_free ~ U[0.02, 0.23],
  T = 149,022 = 2,000 J-orbits (23.7 kyr). Truth WH h = 0.125 (dyadic); convergence pair
  (0.1875, 0.125): median |Δz̄| = 1e-4, p90 = 2e-4 (max 0.54 is ONE chaotic 2:1-zone body;
  h-sensitivity there is real chaos, not inconvergence).
- Selector (frozen, planet parameters only): admits 822/1024 = 80.3% (predicted 0.77–0.83).
  Rejections: 2:1J 76, 3:1J 38, 5:2J 32, 4:1J 22, 7:3J 15, 6:1S 7, rest ≤ 2 each.
- Laws vs truth on admitted bodies (metrics.json):
  | law | pass | rate err (med) | e-vector err / amp (med) |
  |---|---|---|---|
  | LL | 0/822 | 24% | 1.88 |
  | rings | 211/1024 = 20.5% | 7.6% (p90 52%) | 0.56 (p90 2.4) |
  | kick (plane) | — | — | 0.0019 |
  By a-bin, rings: [2.0,2.5): 61% pass, rate 0.7%, evec 8.3%; [2.5,2.9): 0%, 11%, 0.76;
  [2.9,3.3): 0%, 22%, 1.93. **Kill rule fires** (20.5% < 50%), and the leak clause too:
  20 admitted bodies ended inside a resonance width measured from run-averaged ⟨a⟩
  (chaotic a-diffusion the κ = 2 width model did not contain).
- Why (measured, not inferred): truth's FREE amplitude (after subtracting the rotating
  forced term) swings, e.g. 0.086 → 0.237 → 0.115 (a = 2.60) and 0.215 → 0.079 → 0.256
  (a = 2.85) on a ~12 kyr beat; LL conserves |free| exactly and so fails everywhere
  (p2's 1,910-yr single-planet run could not see this). Rings follows the swing in the
  inner belt and loses it outward. The driver is a measured culprit: the planets' mutual
  LL gives Saturn |z|(T) = 0.010 against truth 0.054 (5×; the near-5:2 J–S pair), with
  |Δz_S| up to 0.047 — the size of belt free amplitudes. A truth-driven rings diagnostic
  (`laws.py rings_tc`) was launched to isolate this but did not finish in the window.
- The kick law (the plane's 64/orbit, h = P(2 AU)/64) reproduces the 3:1 and 5:2
  depletion: 45% / 25% of zone bodies pump past 2× their initial e — the same bodies as
  truth — trajectory error medians 5.7e-5 / 9.4e-5. Predicted ✓.
- Bytes per body after the run (from the crate's own constants: tube 16 B, binding
  residual 4×i128 = 64 B, belt program 0.126 bits, `Body` 88 B): phasor law keeps the
  program valid (0.126 bits + one shared mode table per doll, zero new bytes per body);
  the kick law scars every body at its first kick ≈ 82 B. Ratio ≈ 5,000× — but only
  where a phasor law actually passes.

**Predictions** (predictions.md, written before the runs): admission 0.77–0.83 ✓ (0.803);
truth convergence ✓; kick-law depletion ✓; LL outer-belt rate failure ✓ but LL was
predicted 45–65% overall — actual 0% (the modulation, not the rate, kills it: missed);
rings ≥ 90% of admitted predicted — actual 26% (held-out prediction FAILED; the honest
core of this dossier); "no admitted body inside a width" FAILED (20 leaked via drift).

**What would make it wrong.** The 10%-of-free-amplitude yardstick assumes a stable free
amplitude; where truth modulates it, the phasor's trajectory error is dominated by the
modulation, not by rotation-rate error — one could argue for judging rate-only. That
argument does not rescue the engine claim: the kicked tube must still track the true
z-trajectory for the game's encounters and views. The rings implementation used LL-driven
planets and 24×16 quadrature (validated against analytic LL at low e to 0.5%); a
Touma–Tremaine 2-planet rings driver is the one named experiment that could revive the
mid/outer belt — one experiment away, not done here. Cost of adopting (conditional):
per-doll mode table + per-body zero kicks; delete the 64 kicks/orbit and the scars for
admitted bodies.

**Fit with PRINCIPLES.** "A failed experiment kills that configuration, never the method"
(#9): what dies is first-order phasors with linear-LL drivers at two-planet coupling; the
selector, the inner-belt rings result and the memory coupling survive as leads. "Compute
only surprises" (#3) keeps its candidate for a < 2.5 AU. " behaviours matter, not
continuum fidelity" (#2): the modulation IS the behaviour the law must reproduce.

**The lens.** A secular-phasics lens looks for integrable structure; it may have
underweighted that the DRIVER (the planets) is itself the strongest nonlinear element in
the scene, and that amplitude modulation — not precession rate — is the binding error.

**Reproduce:** `python3 selector.py` (2 s); `python3 wh_run.py truth|conv|kick` (21/9/12
min, over the 60 s ideal — noted); `python3 laws.py ll` (5 s); `python3 laws.py rings`
(8 min); `python3 analyze.py` (2 s). Files: `metrics.json` (all numbers above),
`*_zbar.npz`, `predictions.md`, `wh_run.py`, `laws.py`, `selector.py`.
