# Predictions — second author on 20261007-2246-system-969a

Written before any scene run. The checker's named experiment: stack the timing tier
(`dioph::first_hit`, i.e. the shipped `sections` + `pair_events`) on the key-window
candidate pairs at belt scale and on a formation; measure steady-state work per real
encounter (r8 v4 `steady`: events/body/orbit ÷ truth/body/orbit ≤ 2.0; `checks`:
exact checks per encounter ≤ 1.5) and recall against the fine truth.

Setup: `work/encounters_key` is a copy of `crates/encounters` with one added experiment
(`keytier`); `diff -r` shows the shipped files byte-identical. Tier-2 is the shipped
code path (`method_all` → `pair_events` → `sections`/`first_hit`/`check`), fed three
candidate lists: the key window (the run's 12+12-bit store), the shipped Binet cone,
and (truth only) radial overlap. Truth: the crate's conservative advancement (Halley;
the method uses Newton — no shared solver).

Scenes: dense S2-like (N=1000, a∈[0.99,1.01], Rayleigh e 0.02, ρ=5e-4), formation S3-like
(N=1000, a=1±1e-5, e≈1e-3, ρ=5e-4), highe S4-like (e∈U[0.7,0.9]), spread S8-like
(a∈[0.7,1.3], σ_e=0.05), extremee (checker's e∈U[0.95,0.985]), steady = r8 v4 case (b)
(N=3000, σ_e=1e-2, ρ=1e-4, a∈[1,1.5], seed 20261020).

## Pre-registered expectations

1. **Recall (complete + sound), all scenes, truth horizon 10 orbits:** tier-2 on key
   candidates: missed = 0 and false = 0. Same numbers for tier-2 on cone candidates.
   The key window is a superset of the cone on these scenes (both ⊇ truth), so the
   stacked tier must inherit zero misses.
2. **Steady gate (≤ 2.0) on the steady scene at horizon ≥ 100 orbits:** holds for BOTH
   tier-1 sources, and key/cone events within 1.5× of each other. Mechanism: extra
   key-only pairs pay setup once and their sections either return no window or never
   hit within the horizon (they are pairs the cone rejects as never approaching), so
   marginal per-orbit work is hit-driven, not candidate-driven.
3. **Checks gate (≤ 1.5) on the steady scene at long horizon:** holds for both tiers
   (each window hit that fails the exact check is a near-miss conjunction; the window
   is second order, so I expect checks/hit ≤ 1.5; if it fails, it fails for cone too —
   a tier-2 property, not a stacking property).
4. **Formation:** both tiers keep ~all N²/2 pairs (the gold's co-orbital finding), so
   the cost is setup, one-off; marginal per-orbit events per body (beyond setup) ≤ 1e-3
   at horizon 1000, key ≈ cone within 1.2×. The steady ratio against truth is not
   meaningful there (truth rate ~ initial coincidences only); I report marginal work
   instead of claiming the gate.
5. **High-e (e∈[0.7,0.9]):** the steady gate FAILS for both tiers at short-mid horizon
   (candidate set degenerates to ~everyone; r8 v2's "cost follows the candidate set").
   Prediction: at horizon 100, events/body/orbit ÷ truth/body/orbit > 2 for both, with
   key/cone within 1.3× — a shared candidate-regime failure, not evidence against the
   one-store deletion. If key/cone differ > 2×, the deletion claim weakens: the key
   window would be adding real work the cone avoids.
6. **Key-only pair share:** pairs in key ∧ ¬cone produce < 5% of all checks at the
   longest horizon on the steady scene (their sections never hit). If their share is
   large, the key window's extra breadth costs real tier-2 work and the dossier must
   say the deletion is not free.
7. **Extremee (e∈[0.95,0.985], no precession):** tier-2 on key: missed = 0, false = 0 at
   10 orbits (extends the checker's tier-1 finding through the timing tier). Note the
   checker's own boundary stands: e ≳ 0.9995 breaks tier-1 soundness (gap floor 2⁻¹²);
   I do not test past it.
8. **Identity:** for pairs present in both lists, the tier-2 event lists are identical
   (same code path); any difference in scene-level hit counts is exactly the key-only
   pairs' contribution.

Not measured here (out of my scope, said plainly): tier-2 under apsidal precession
(the crate's Body is a fixed Kepler ellipse; the sections' crossing longitudes and
windows would go stale as the apse precesses — a separate experiment), and the
`crates/universe` wiring + plane A/B (forbidden: no crate edits).
