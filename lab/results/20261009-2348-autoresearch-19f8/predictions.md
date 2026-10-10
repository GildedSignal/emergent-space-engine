# predictions.md — held out before the final run

Held-out corpus (never tuned on): radius exponents {4, 12, 45, 60, 120}, eccentricities
{2^32, 1/5, ~1, 1/1000}, kick quantum 1024 (4× the tune set's), different LCG seed.
The kept configuration is two bit-identical deletions of redundant compute:
E3 (one duplicate `z·z` per bisection polynomial evaluation) and E5 (one duplicate
`cos ψ` + `x(ψ)` per quadrature node).

Predictions, written before the run:

1. **Digest unchanged on both sets.** tune stays `fd33f759b10e569f`, held-out stays
   `c45b567dfc5b395c` (bit-identity is the behaviour constraint; both changes compute
   the identical expression once instead of twice).
2. **Latency gain is small and of the same order on both sets: 1–3% at p50, lost in
   noise at p99.** The dedupes remove ~1 mul of ~68 poly evals and ~1 cos of ~70
   nodes; neither touches the division chain (~half the call).
3. **The held-out set's absolute cost stays within ×1.2 of tune** (its radii mix more
   weak-field orbits where the witness accepts, so the bisection is not slower).
4. The reverted experiments stay reverted: isqrt-via-div_word (E1) is exactly equal
   in both value and speed on this machine (1.00×); the add fast path (E2) gains
   nothing; the witness-tightened bisection start (E4) is NOT bit-identical (the
   rounded polynomial is not monotone at fine scales, so the full midpoint sequence
   defines the answer) — if a checker re-applies E4 it must expect a changed digest
   and a failing `witnessed_fit_keeps_the_full_search_key_at_kicks_and_boundaries`.

What would falsify the run's conclusion (bit-identity is cheap to keep, divisions are
the floor): a held-out digest change, or a held-out p50 gain ≥ 10% (which would mean
the tune set under-represented the dedupes' reach).
