# Predictions (written before the decisive experiment)

Component: the scan's candidate tier (`crates/universe/src/radial.rs`), promotion od 1(b)'s unflown arm.
Scanner: a mid-belt ship of the root doll (the in-band seam window 396d flew with the player; the
window geometry r, v, h is the same class, the scanner's own step the interval). The exact-truth
reference T is the sound window of radial.rs's own certificate with per-body terms: kept iff
|d_j(t)| ≤ (reach_p + radius_j)·2^10 + (v_s + v_j)·h, exact readouts. The phase filter F adds the
angular cut |wrap(θ_j − θ_s)| ≤ ω_j + 2c_j (equation-of-centre bound, phase.rs:39-41 form, true-
longitude anchor), sound by the same triangle inequality.

- P1 (the bail): at every flown N (10⁴, 10⁵), the shipped tier returns None at an in-band scan —
  the caller walks every body (cands = N − O(locals), 396d's law).
- P2 (the idiot index): |T|/N ≤ 0.15 at the belt mix (e Rayleigh 0.07 redraw 0.4): the walk
  overreads ≥ 6×; the binding_at walk stays near 396d's ~214 ns/body on this box (orders).
- P3 (soundness): T ⊆ F at every arm (zero misses), with |F|/|T| ≤ 2.5 (the e-widening dilutes,
  it does not flood).
- P4 (the cold belt, 396d's unflown arm): at e ≈ 0 the window collapses to the drift term
  ((v_s+v)·h ≈ 0.002-0.02 rad): |T|/N ≤ 0.005, ≥ 20× below the belt mix — the zone collapses to
  the angular window, and the residual truth is set by the interval h, not e.
- P5 (the index): a θ-sorted query at the anchor tick serves |F| in O(log N + |F|) — measured
  ≥ 50× under the brute per-body check at 10⁶ offline.
- P6 (the cost split): the phase filter's brute per-body check costs ≤ 40 ns/body (three adds and
  a compare on stored triples, no binding read) — ≥ 5× under the shipped walk's binding_at.

Kill criteria: any miss in P3 kills the filter's soundness claim; P1 failing (the tier returns a
list at the band) kills the premise that the seam bails at these N.
