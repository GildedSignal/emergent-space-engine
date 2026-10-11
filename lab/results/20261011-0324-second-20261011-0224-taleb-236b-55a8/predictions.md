# Predictions — 20261011-0324-second (second author on taleb-236b)

Written before running `probe2.py` (conj / dense / boundary / prec). Not tuned
on: the only runs so far are the author's own `probe.py` (regenerated above,
ex-timing identical) and a reading of checker 1's numbers in
`work/orig/check.md`. The theory behind each prediction is one line; the
measurement decides.

## Conjunction record (`conj`) — repairs the unverifiable side-claim

- **PA1:** S4 pairs whose ΔM crosses 0 within the 24-orbit horizon: **9,000–28,000**
  (checker 1's natural definition gave 10,077; my drift estimate allows up to
  ~20k — the shipped script settles the exact count).
- **PA2:** conjunction misses (exact distance at the ΔM=0 crossing) span
  **5e-5 to 0.8**; min ≈ 1e-4 (checker: 1.04e-4), i.e. the floor is ~300× below
  the author's "0.02" and only ~1× above R=1e-4.
- **PA3:** zero conjunction pairs with miss < 1e-4, but **1–10** with miss < 3e-4 —
  the proposition "conjunctions are non-encounters" is R-relative, not absolute.
- **PB (the author's "59 pairs, misses 0.02–0.33"):** it is a mislabeled
  subpopulation. Contact∩conjunction pairs: **150–700**, and their conjunction
  misses lie **mostly in 0.02–0.4** (they are crossing-offset contacts, so
  |Δϖ| ~ their offset). If some natural reading yields ≈59 I will report which.
- **PC (tail mechanism):** ≥ 80% of S4's rank≤4 contacts are pairs whose
  crossing offset |ΔM*| ≤ 5e-3 (≈ 4× mean phase spacing) with |Δϖ| in the
  bottom ~5% of the pair distribution — the degenerate co-elliptic (shear)
  branch hiding inside S4, not a failure of the offset picture. If instead the
  tail has fleet-typical (Δϖ, Δe), the offset representation is incomplete.

## Dense truth (`dense`) — removes the coarse-capture bias

- **PD1:** all-pairs spP=64 finds **900–950** contacts (checker 1's independent
  finder: 928); frac rank≤4 ∈ [2.5%, 4.5%]; median rank 60–80.
- **PD2:** spP=256 within 3% of spP=64 (converged); the finder at spP=16 misses
  ~5–8% of pairs (871 vs ~928), and the missed pairs have v_rel ≳ 0.03
  (the capture condition r_coarse ≥ R + v_rel·dt/2 is violated for them at
  dt = 2π/16).
- **PD3:** v_rel at contacts: median ≤ 0.01, p99 ≤ 0.05 — S4's crossings are slow.

## Boundary case (`boundary`) — shipped trigger boundary

- **PE:** S5 (σϖ=0.03, e pinned) has cone fraction 0.5–0.7 and still drops
  ≥ 90% of contacts beyond rank 4: frac rank≤4 **3–8%**, median rank **30–60**
  (checker 1: 4.9%, 46). Cone fraction cannot gate rank-4 vs pairwise.

## Precession (`prec`) — the missing experiment

- **PF1 (instrument):** rigid precession 5e-2 rad/orbit reproduces the κ=0
  structure: same events ±2%, same frac/median to reported precision
  (a common rotation cannot change pairwise distances).
- **PF2 (encounter rate):** events grow monotonically with σκ — ~871 (κ=0),
  1–2k (1e-3), 5–20k (1e-2), 30–90k (5e-2; ceiling 2 per pair = 89.7k) —
  because a pair contacts whenever its sweeping crossing offset ΔM*(t) meets
  its slowly-drifting ΔM(t); at full churn every pair meets.
- **PF3 (the claim survives):** at every σκ, frac rank≤4 ∈ [2%, 8%] and median
  rank ∈ [40, 130]. The contact offset stays pinned to the pair's ΔM (which
  lives in the fleet's phase clump), not to rank 0. **Refutation:** frac > 50%
  or median < 20 at any κ would mean precession rescues rank-locality.
- **PF4 (window cost):** per-contact |ΔM*(t*) − ΔM*(0)| ≈ |Δκ_ij|·t* with
  regression slope **0.5–1.5** — offsets drift 1:1 with differential
  precession, so window refresh cadence must satisfy κ·Δt ≲ window half-width.
- **PF5 (frozen certificate):** t=0-frozen rank-4 partner lists catch ≤ 20% of
  contacts at every κ, **including κ=0** (the ordering shears at σa=2e-4) —
  any phase certificate is a live structure; its maintenance cost is the
  element-change rate.
- **PF6:** mean-longitude ordering is no better than M-ordering anywhere
  (frac_λ ≤ frac_M + 2%), and strictly worse under precession (λ churns at κ).

## Kill criteria

- If the κ=0 leg of `prec` or the spP=16 finder leg of `dense` does not
  reproduce the author's 871 events, my fleet regeneration is broken: VOID.
- If PF3's refutation fires, the original claim is **refuted** (precession
  re-localizes encounters; the certificate's failure regime is narrower than
  claimed).
- If PD shows the dense-truth frac rank≤4 > 10% or median < 20, the original
  S4 numbers were finder-biased and the claim weakens materially.
