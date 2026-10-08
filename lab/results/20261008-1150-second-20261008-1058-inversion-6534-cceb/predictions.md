# Predictions — 20261008-1150-second (before the decisive runs)

Written before any run at m ≥ 500. Prior exposure, disclosed: the original run's
published record (frozen-scene d-to-mean corridor, hits/evals ladders), the checker's
steep/tangent findings, and one m=25 crash-smoke of the three certificate variants on
the frozen scene (zero-miss there; no window was tuned — every half-width is a closed
function of ρ and the lane elements, margin 1.5 throughout).

The experiment (the checker's named one): build the crossing-time-rank exit on the
frozen scene, verify zero-miss vs truth at m ≥ 500, measure work per real encounter;
re-do the two flawed numbers (extrapolation double-÷4, corridor attribution).

Variants: `mean` = the checker's literal spec (shared star, corridor
dispersion + radial tolerance, mean motions). `own` = each B body ranked at its own
crossing longitude (removes the dispersion term). `rank` = conjunction-aware window
S_k = 1.5·[2ρ/n_a + tol_b·|1/n_a − 1/λ̇_B|] with tol_b the exact closed-form
longitude region where r_B ∈ annulus ± ρ — a necessity chain, not a fit.

1. **Zero-miss, frozen, m=500 and m=1000:** all three variants: missed = 0,
   truth_pairs_missed = 0, false = 0.
2. **Selectivity (pairs per real encounter), m-independent within ×1.5 across
   500 → 1000 → 2000:** mean ≈ 40–90; own ≈ 20–30; rank ≈ 2–5.
   At m=2000 the tier-2 product is 4·10⁶ pairs for 49 574 hits (~81/hit);
   rank cuts the enumerated pairs ~20–40×.
3. **Work per encounter:** rank ≤ 10 µs/hit at m ≥ 1000 (4-thread cloud wall),
   against the tier-2 block's ~66–97 µs/hit (3.3 s/49 574 at m=2000,
   1.19 s/12 299 at m=1000); generation (sort+merge) < 25% of the check time.
4. **Corridor attribution, frozen m=500 (xcorr):** d-to-mean reproduces the record
   (d50 ≈ 0.0104, d_max ≈ 0.029, none beyond 0.15); d-to-own-crossing is ~2–3×
   tighter (d50 ≈ 0.004–0.007); the passage-time mismatch dt (the quantity the
   rank windows on) has d99 < 0.004 — ~25× tighter than the longitude corridor,
   consistent with dt ≈ d_own · |ω_A − λ̇_B|/ω² (rate-mismatch contraction).
5. **Steep scene (e_B = 0.35, γ ≈ 19.8°, ρ/sin γ = 0.0029, 4.4× smaller than
   frozen):** d-to-mean d50 ≈ 0.010 — unchanged from frozen (reproduces the
   checker: the mean corridor is dispersion-set, not ρ/sin γ-set); d-to-own d50
   ≈ 0.003–0.006 (≈ tol_b, the radial-tolerance scale); rank zero-miss at m=500;
   rank window tighter than frozen's.
6. **Near-tangent scene (e_B = 0.092, γ ≈ 0.8°):** tol_b ≈ 0.08–0.10 (large);
   d-to-mean max grows to ≈ 0.10–0.15 with some encounters beyond 0.15;
   rank's S ≈ 0.9·10⁻² — small, because S keys on the rate mismatch, not 1/sin γ;
   I expect rank zero-miss here too (the neglected λ̇-variation term is
   ≈ tol_b²·|dλ̇/dλ|/λ̇² ≈ 2·10⁻⁴ ≪ S). Decision rule if it does miss: the
   miss bounds the domain — the γ-trigger routes to tier 2; a miss at tangent
   refutes robustness there, not the frozen/steep result.
7. **Corrected extrapolation (arithmetic, no measurement):** tier-2 at the
   measured 0.79–0.83 µs/pair (already 4-thread wall) gives 10¹⁰ pairs ≈ 2.2 h
   and 10¹² pairs ≈ 9.1 days per epoch (the original dossier's 30 min / 2 days
   divided by 4 twice). With rank: candidate work tracks real encounters
   (~3/hit × ~1 µs), so 10⁶×10⁶ at this lane width is ≈ 1.2·10¹⁰ encounters
   per 20-orbit epoch → hours per epoch, ~10³× under tier 2 — and at fixed
   encounter density (lanes widening with N) total work is O((n_A+n_B)·log n),
   which is the only reading under which the original dossier's O() claim is true.

**Kill criteria (pre-registered).** rank misses > 0 at frozen or steep (m ≥ 500):
the derivable-window exit is refuted; report the measured dt corridor as the
surviving invariant. pairs_per_hit(rank) growing more than ×2 from m=500 to
m=2000: the certificate does not track encounters; refuted. Both `mean` and `own`
missing where `rank` does not would isolate the dispersion/rate terms as
load-bearing.
