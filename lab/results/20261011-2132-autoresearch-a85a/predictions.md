# predictions — run 20261011-2132-autoresearch-a85a (written before the held-out runs)

Kept configuration so far (tuned ONLY on sets a/b/c/d/long + the kick belt rho=1e-4, all from the
shipped verify_set): numeric_window caches j's τ-grid states + (mi, mj), τ-grid k=16 (was: no cache,
k=32). Kick cost at rho=1e-4: 7,712 → 4,502 µs (−41.6%).

## Held-out cases (never used above)

Set **e** (fresh seeds 777001–777003, sigma_e=5e-2 unseen anywhere, rho=1e-3 at sigma 1e-2 unseen,
coorbital at width 1e-2 unseen), plus **kick at rho=1e-3** (unseen), plus event-identity against the
unmodified baseline binary on set e.

## Predictions

- **P1 (behaviour):** all three set-e belts report missed=0, false=0, dup=0 against the dense truth.
- **P2 (gain at rho=1e-3):** the shelf crawl scales as 1/rho (steps ∝ rho), so numeric windows carry a
  smaller share of the kick at rho=1e-3; predicted total kick gain vs the baseline binary shrinks to
  **12–30%** (from 41.6% at 1e-4).
- **P3 (identity):** on set e the new binary's event lists match the baseline binary's exactly
  (same truth_enc, method_enc, matched, checks, hits), with evals strictly lower.
- **P4 (edge, not kept):** k=8 also passes set e (it passed all shipped sets; kept at 16 anyway since
  its extra gain was <10%).

## Kill criterion

Any missed>0 or false>0 on set e, or any event-list mismatch vs the baseline binary on set e, kills
the k=16+cache configuration: revert to cache-only (k=32) and report the kill.
