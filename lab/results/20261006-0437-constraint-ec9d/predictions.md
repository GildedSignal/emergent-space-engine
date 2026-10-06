# Predictions (written before the instrumented run)

Setup: `universe --kick-bench --seconds 20` on this tree, with per-phase timers inside
`step::kick` (readout / secondaries / tide / acceleration / rebind fit+compile). Baseline on
main, same machine, same seed: made-body kicks median ≈ 44 µs; leaver kicks median ≈ 365 µs
(8.3×); exact-memo hit rate 0.

Cases not tuned on (I have not yet seen any decomposition):

1. **Made bodies (44 µs):** rebind fit+compile is the largest phase, > 50% of the kick
   (consistent with HANDOFF's 15 of 29 µs on the M1). Readout, secondaries, tide,
   acceleration are each < 15%.
2. **Leavers (365 µs):** the 8× gap lives mostly in the *same* phase that dominates made
   kicks — the rebind fit — not in force gathering. Rationale: leavers leave a Fermi frame
   on a planetary orbit, so their state relative to the doll's dominant body is a
   near-parabolic/high-e passage, and an iterative fit pays per Newton step. I predict
   rebind ≥ 60% of the leaver kick, and the fit's cost scales with orbital eccentricity
   of the bound state, not with the number of sources.
   - Alternative I considered and predict against: tide/secondaries dominate because the
     fleet doll has many sources (if this is so, the constraint is force gathering, not
     the fit, and the exploit is different).
3. **The unaccounted remainder** (kick total − sum of phases: quantize, bookkeeping) is
   < 10% for both populations.
4. **Consequence if 2 holds:** the plane's p99 kick tail is a fit-geometry problem, so the
   cheapest exploit is to make the fit's iteration count uniform (a bounded-iteration fit
   with a carried residual), not to cache compiled cycles (the memo is dead: 0% exact hits).

Kill criterion for my claim: if rebind is < 30% of the leaver kick, the constraint is
elsewhere and I report that instead.
