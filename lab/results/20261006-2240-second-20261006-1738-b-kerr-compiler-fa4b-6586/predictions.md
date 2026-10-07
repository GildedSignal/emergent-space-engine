# predictions.md

Written before the decisive experiments. The regeneration runs (gates, module tests,
gen_tables.py) are reproductions of the author's record, not predictions; the decisive
experiments are the two latent edges the second checker named in "What the author missed",
plus the mechanical silver diagnosis.

What I have tuned on so far: nothing in the module (I have only read it and re-derived the
a = 1 ISCO polynomial by hand: r² − 6r − 3 + 8√r = (√r − 1)³(√r + 3), non-negative on [1, 6]
with a triple root at the `lo` endpoint). The whirl construction and the tanh-sinh truth are
my own, written from the metric-level formulas in gen_tables.py.

## P1 — isco at the extremal limit (module `kerr::isco` vs Bardeen's closed form)

Scan a ∈ {0.5, 0.9, 0.998, 0.999, 0.9999, 1 − 2⁻³⁰, 1 − 2⁻⁵²} × {prograde, retrograde}:

- For every a < 1, both senses: |isco_module − isco_true| ≤ 1e-5 relative. The bracket stays
  valid for all a < 1 (poly(1) = −5 + 8a − 3a² < 0 strictly), but near a = 1 the root is a
  near-triple root and the polynomial is flat (poly ~ (r − r_isco)³ locally), so Scalar's
  ~2⁻⁵⁹ absolute rounding on terms of size ~8 becomes a root error of ~(2⁻⁵⁹)^{1/3} ≈ 1e-6.
  I predict the error grows from ~1e-13 (a = 0.998) to ~1e-6 (a = 1 − 2⁻⁵²) — still three
  orders below the gate's coarsest tolerance (1e-2) and below every margin isco feeds.
- At a = 1 exactly: prograde returns 6.0 (wrong; the true extremal ISCO is 1.0 — the triple
  root sits at the bracket's `lo` endpoint, `keep_positive` is true at every midpoint, and
  `bisect` returns `hi`). Retrograde returns 9.0 (the correct extremal value, reached by the
  same slide to `hi`, which happens to be the root).
- The a = 1 defect is unreachable through the judge: the adapter rejects χ ∉ [0, 1) (verified
  by reading `xtask/src/behave/space.rs` before this run; the gate's frozen spins are
  0.5/0.9/0.998).

## P2 — the CYCLE_MAX cap degrades silently for extreme whirls (module `kerr::cycle`)

Whirls built directly in (E, L): an unstable circular orbit at r_s between the photon orbit
and the ISCO of one sense, its (E_c, L_c) from R(r_s) = 0, R'(r_s) = 0, then L moved into the
bound window by relative steps 2⁻ᵏ, k = 8…56, at χ = 0.998 prograde (spot checks at χ = 0.5).
Truth: my own tanh-sinh quadrature in u (the module integrates in ψ with a doubling
trapezoid; different substitution, different quadrature, different root finder).

- The module's advance stays within 1e-9 of the truth while the needed panel count stays
  under the 2¹⁴ cap: the trapezoid's error is geometric until the periapsis peak (width
  ~√(u₃ − u_peri) in ψ) is narrower than the panel spacing.
- Because a double root splits like √δ, the cap binds only at δ ≲ 2⁻⁴⁵…2⁻⁵⁵ (u₃ − u_peri
  ≲ amp·(π/2¹⁴)²·O(1) ≈ 10⁻⁸·amp): I predict the module is still exact (≤ 1e-9) at δ = 2⁻³⁶
  and the cap binds somewhere in δ ∈ [2⁻⁵⁶, 2⁻⁴⁴], where the advance is in the hundreds of
  radians. There the returned value silently underestimates the truth by ≥ 1e-3 relative
  (a capped trapezoid misses peak mass), with no error flag — the second checker's claim.
- The exact separatrix orbit (perfect double root) errors out (`NoBoundOrbit` or `Range`),
  never returns a number.
- The gate's frozen cycle domain (p ≥ 1.1×separatrix, e < 0.7) never comes near the cap: the
  largest frozen-seed whirl advance is ≪ 100 rad, ≥ 10² rad below where the cap binds.

## P3 — the mechanical silver

`lab/run.sh:95-99` publishes gold only when `check2.md` contains a line starting exactly
`Grade: `. The branch's check2.md has no such line (its abstract and checker2-final.md say
gold, in other words). Predicted: `grep -m1 '^Grade: ' check2.md` returns nothing while the
same grep on check.md returns `Grade: gold` — the silver is a missing line, not a physics
disagreement. (This one is already verified by reading; it needs no run.)
