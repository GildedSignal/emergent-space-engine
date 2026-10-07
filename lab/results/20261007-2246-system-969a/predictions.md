# Predictions (written before the decisive experiment)

Hypothesis under test: the law's Catalogue key — quantized (p, k=1/(1+e)), 12+12 bits —
is itself the orbit's radial annulus. If so, ONE sorted key list serves (a) cycle reuse
(already true), (b) the encounter candidate tier (annulus-overlap windows over keys, not
bodies), (c) formation/phase certificates (bodies under one key, phase-ordered), with zero
new state. The plane's O(N)-Cartesian `PlayerNeighbourhood` scan and the research crate's
per-body float element sorts would be projections of this one store.

Scenes (one doll, mu=1): S2 dense belt (N=1500, a in [0.99,1.01], Rayleigh e 0.02),
S3 formation (a=1+-1e-5, e=0.001), S4 high-e belt (e in [0.7,0.9]), S5 = S2 with
GR-style apsidal precession 0.3 rad/orbit. Truth = brute-force sampled minimum distance
over one orbit, encounter radius R=5e-4. Held-out cases I did NOT tune on:

1. **Recall (decisive):** key-window candidates (window = quantized annulus widened by
   one key quantum each side plus R) contain every true encounter pair. Predict 0 misses
   on S2, S3, S4 AND S5 (precession changes nothing because the window never reads ϖ).
2. **Negative control A:** same window without the R-widening misses >= 1 true pair on
   S2 or S4 (a test that can fail; otherwise my recall check is a control that cannot fail).
3. **Negative control B:** window widened by R but NOT by the key quantum misses pairs
   (the quantized annulus is off the true annulus by up to one quantum) — the adopter's trap.
4. **GR tax on the orientation-aware filter:** the Kepler cone (ΔU² ≤ ΔV²+ΔW²) evaluated
   with stale ϖ (frozen at interval start) misses true pairs on S5. Predict misses > 0;
   and with current ϖ it needs per-body V,W refresh every precession cycle — work the
   key-only window never pays.
5. **Work per query:** for a sparse belt (N=2e5, a in [0.7,1.3], Rayleigh e 0.05),
   candidates per query ~ 1e2–1e3 (vs N Cartesian evaluations in the shipped plane);
   candidates per true encounter <= ~1e3 at fixed density.
6. **Kick maintenance:** after kicking 1% of bodies (delta-a/a ~ 1e-3), only kicked
   bodies move in the key list (insertions ~= kicked count, no global resort), and the
   moved distance is O(1) key cells.
7. **Formation blocks:** in S3, true partners of a body lie at small phase rank within
   its key block: median rank < 10, max < 50 (the gold measured rank <= 4 on an exact
   shared orbit; quantum spread should inflate it modestly, not catastrophically).
8. **High-e inflation:** candidates per true encounter on S4 exceed S2 by roughly the
   annulus-width ratio ~ (1+e)/(1-e) ~ 10-20x, but stay far below N and keep 0 misses.

If 1 or 8's recall fails, the unification is wrong or needs a two-level window; if 7
fails badly (rank ~ block size), the quantum spread breaks the phase certificate and the
single store degrades to the quadratic tier under concentration — that is the case that
breaks this unification.
