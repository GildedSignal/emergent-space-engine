Grade: silver

**Abstract (for the integrator).** Premise refutation, two-thirds real. The statistics
half of representation.md thesis 2's shadowing clause is dead: the quantized standard
map (K = 1.2) distorts sticky-orbit trapping tails non-monotonically — 14.1% permanent
spurious captures at Q = 10⁻³ (true 0%, same-size noise 1.2%), tail crushed 5.5× at
10⁻². Reproduced byte-identically; the checker's attacks extend it: K = 1.0 → 9.6% and
K = 1.4 → 38.7% capped; detectable down to Q = 3×10⁻⁵; and the design's own
integer-native-kick reading (r2) still yields 3.1% permanent traps at 10⁻³. The "no
shadow bound" half is retired: the noise-deviation instrument decorrelates a provably
shadowable cat map identically; the dwell data itself shows the trapped quantized
orbits unshadowable. Gain: drop the clause, freeze a trapping-statistics rung. Cost:
one doc edit, one rung. Adopt the refutation, not the instrument.

## Reproduction

Copied `dwell_tail.py`, `shadow_falsifier.py`, `regen.sh` to /tmp and re-ran regen.sh:
exit 0, every number byte-identical to the stored outputs (only `elapsed` lines differ:
45.4/41.3 s vs 44.4/39.6 s). All decisive dossier numbers match (true p50/p90/p99/max =
393/2821/14208/16654, capped 0; Q=10⁻⁴ 2.7%; Q=10⁻³ 14.1%, p90 = cap; Q=10⁻² p90 = 512,
3.1%; noise 1.2%, p99 77444; λ range 0.232–0.536). One number the shipped code does not
print: dossier's "reaches 2.25" (sea median deviation, Q=10⁻⁴, t=10⁵) — regen gives
2.71/2.05/2.28, median 2.28. Minor, and inside the arm retired below; but
author-final's "byte-identical numbers" is wrong on that one.

The quoted clause is verbatim in `docs/representation.md` (thesis 2) and §2's error
model ("at most one floor unit per event, carried forward") is read fairly. Not a
strawman.

## Predictions

`predictions.md` predates both scripts and the dossier by ~7 min (file mtimes; single
session, no intermediate commits exist to verify further — consistent, not provable).
Held/failed honestly reported: P4 wrong in direction (inflation, not crush — a
stronger refutation than predicted), P2 failed, P1 failed in phase distance and was
re-diagnosed without measuring actions; only P5 clearly held. Gold's letter ("the
held-out predictions held") is not met, though the conduct (failures named as
failures) is exactly right.

## My attacks (one outside the author's tested domain each)

1. **Cat-map control of the noise instrument** (different map entirely). The dossier's
   supporting arm reads torus-scale decorrelation of noisy copies from the same-IC
   reference as "no shadow bound". The Arnol'd cat map is Anosov — the shadowing lemma
   holds provably — yet the same protocol gives median deviation 0.37–0.44 (torus diag
   1.41; uniform-decorrelation median ≈ 0.38) at both Q = 10⁻⁴ and 10⁻³, at every
   checkpoint from t = 100. Deviation-from-reference measures mixing, not shadowing;
   the sentence "a shadowable (Anosov-like) system would saturate at a bounded multiple
   of Q" is true only of deviation from the *shadow* orbit, which the test never finds.
   Instrument retired; the wiki page is corrected in place. (Also: the dossier's "grows
   decade over decade without saturation" is contradicted by its own printout — it
   saturates at torus scale ~2.3 vs diag 4.44.)
2. **K-robustness of the decisive arm** (outside the author's K = 1.2). Same protocol,
   K = 1.0: quantized capped 9.6% vs true 0%, noise 0.8%. K = 1.4: quantized 38.7% vs
   true 0%, noise 1.2%; true max dwell 20158. Signature unchanged, stronger with K.
3. **Finer decade** (below the author's Q sweep). Q = 3×10⁻⁵: still 2.0% capped, p99 =
   cap. Q = 10⁻⁵: 0% capped (n = 256 detects ≳1%; p90 still −17% vs truth). The
   distortion is live a decade below the dossier's sweep.
4. **The design's own defense** (r2: "increments and kicks are integers native to the
   law, exact by construction"). Variant: only the kick quantized, momentum an exact
   integer grid index, x never rounded. At Q = 10⁻³ it still yields 3.1% permanent
   traps (vs 0% true, 1.2% noise). The exact-native reading does not dodge the
   pathology at game-relevant Q; it is ~4.5× weaker than state rounding. This closes
   the dossier's own "what would make it wrong" bullet 2 in the refutation's favour.

## Novelty

No `lab/wiki/` page, no docs/HISTORY.md entry, no rung tests trapping statistics
against an oracle (r5 = bit-identity between the two orders; the B12 family judges
error statistics, not behaviour-class preservation). The page is a new topic, folded
in faithfully except where corrected. Not a repetition.

## Goal fit

A premise red-team on bottleneck 0 (the representation), and the measured failure is
exactly an error-type flip — principle 2: "Behaviours matter, not continuum fidelity:
error type over error size." It proposes the missing rung with controls on both sides.
Cost of adoption: edit representation.md's clause, freeze the trapping-statistics
criterion (drafted, not frozen — that is the second step).

## Why silver, not gold

The headline claim is half rock, half retired: the statistics clause is refuted,
reproduced and now robust across K, a finer Q decade, and the integer-native reading —
but the "no shadow bound holds" half rested on an instrument my control breaks, and
the gold letter on held-out predictions is not met. Silver's one experiment: **run the
dwell arm on the shipped `es-space-v2` dense order around a co-orbital island at the
engine's Q** (quantized law vs float oracle: capped-fraction and p90), with a valid
shadowing instrument (Newton refinement that *finds* a shadow orbit) replacing the
retired noise test. If the distortion is there, the clause falls on the game's own law
and the rung freezes — gold.

## What the author missed

- The noise test was superfluous *and* invalid: the dwell data already implies the
  permanently-trapped quantized orbits are unshadowable (no sampled true orbit of the
  band survives past 1.7×10⁴; heavy-tail caveat: 0/256 capped bounds true permanent
  traps at ~1.2% (95%), still 12× under 14.1%). The strongest argument was left
  unstated; the broken one was printed.
- The direct test of the clause's second half (same-cell true-orbit comparison) never
  collected data (n = 3 in `dwell_tail.py`, n = 0 in `shadow_falsifier.py`); the
  dossier is silent about that.
- "Actions preserved" was asserted (page) but never measured; corrected in place.
- `shadow_falsifier.py`'s own dwell arm is dead code (R_DET = 1.1 vs a sticky
  classification built around a 1.6 disk → p50 = 0 in every arm); its dwell table in
  shadow_out.json carries no information.
- The "2.25" number (above), and a single-K dossier whose blind spot the author named
  but did not close — K = 1.4 alone would have tripled the effect.

All my processes: < 100 MB, ≤ 115 s each, on this Linux box — orders of magnitude only.
