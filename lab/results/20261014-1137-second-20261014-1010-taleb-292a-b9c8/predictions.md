# Predictions — 20261014-1137-second-...-b9c8 (written before the decisive depth-256 run)

Disclosure: a depth-64 smoke run on the full 864-chain grid preceded this file (the build
check). Its headlines are therefore observations, not predictions: 864/864 chains complete
to depth 64 with ZERO refusals (the μ arm runs; the 2⁴⁰ unit jump is gone), 792/864 walk
(unique64 = 64), e = 0 circles drift 1.64–1.98 of the radius at every phase with the
radius itself exactly preserved (dr_rel = 0), and exact key-level fixed points exist at
true phases (60 chains, cycle_len 1; only 22 of them also fix w). Everything below is
about the depth-256 record and the breakdowns not yet computed. The checker's probe
(check.md) informs PD1–PD3; I cannot be blind to it.

- PD1 (μ arm, the checker's claim to confirm): paired per (p, e, φ, shift), the μ-doll
  walking chains' drift is within 2× of the unity chains' on ≥ 80% of pairs (benign-to-
  helpful), and the μ arm keeps refusals ≤ 5% of its 432 chains to depth 256.
- PD2 (saturation): for walking chains with drel64 ≥ 10⁻³, drel256/drel64 < 2 (median);
  a linear compounder would read ~4. The strong walkers saturate.
- PD3 (the refusal class): at least one refusal lands beyond step 64 (mid-walk, the
  promote-to-live trigger the checker saw at n = 68), on strong-field or high-e arms.
- PD4 (more closure at depth): the cyclic count at 256 exceeds the 72 seen at 64 by
  ≥ 10% (chains that close late), and no walking chain with unique64 = 64 repeats a key
  before step 256.
- PD5 (circles): at depth 256 the e = 0 position drift stays in [1.5, 2.1] and dr_rel
  stays 0 — the lottery is orientation-only, the orbit never deforms.
- PD6 (word dependence flips near closure): per-config drift is NOT word-invariant near
  the fixed-point boundary: ≥ 5 (p, e, φ) configs where one shift closes (cyclic) and
  another walks. The always-walking classes (e = 0 lottery, strong walkers) stay within
  2× across shifts +0/+4/+8, preserving the graded run's invariance finding where it
  applies.
- PD7 (the w lottery persists): per-crossing |Δw| ≥ 0.05 turns somewhere in every phase
  class at depth 256, including on chains whose key is fixed (w wobbles on a fixed key —
  the column row (p, e, w, t) never settles even when the key does).

Kill criteria for the adopted sentence: if the μ arm walks like unity (PD1 fails on the
median pair) the "μ conversion benign" claim dies; if walking chains compound linearly
to 256 (PD2 fails) the hazard is worse than reported and the anchor-first conclusion
strengthens rather than weakens.
