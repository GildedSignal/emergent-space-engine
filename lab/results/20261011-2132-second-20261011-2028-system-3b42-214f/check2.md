Grade: gold

Abstract: Second author closed both named gold experiments, and every load-bearing number reproduces exactly (belt 9/9 byte-identical; straggler 11/11 lines counter-identical; strongfield identical). The same-key certificate is the λ(0) arc window `W = 1.5(4e_hi+3e_hi²)+dn·t_end` (not rank-k): zero misses at both dials, n 400→3200, candidates per encounter constant 5.3→5.6; U(L)|E is monotone through the separatrix-adjacent bound domain (0/200 columns, math re-derived and verified), so the (E,L) key order needs no turning-point repair, and the 5×5-sub-grid compile is zero-miss. My attacks (unseen seed, 80%-phase-cluster, σ_e 0.15, 40-orbit horizon, fresh strong-field seeds) all held: misses 0 everywhere; the cluster kills rank-4 coverage (0.098) while the window stays sound. Cost: re-point the tier at the tube store plus the window rule. One inert instrument flagged (U-scan miss counter is tautological).

## Reproduction

- Clean tree + `git apply work/patch.diff` (adds only `crates/encounters/examples/second_lattice.rs`; no crate code touched). Built and ran all four modes (`cargo run --release -p emergent-encounters --example second_lattice --offline {belt,coorbital,straggler,strongfield}`, ~130 s total, single-threaded).
- `belt`: byte-identical to `metrics-belt.json` **and** to the original run's stored record (diffed against commit 852ecd2f). `coorbital`: all counters identical to the original (2093/1496 events, worst rank 2/10); only `truth_s` digits move, as the dossier discloses. `straggler`: all 11 lines counter-identical (events 562→34,132; misses 0/11; `arc_over_w_max` ≤ 0.850; `cand_per_enc` 5.3→5.6 engine, 1.8→2.1 closure-matched, 0.7→1.1 birth-fixed; negative control 94→5,317 at the engine dial, 0 at the closure-matched dial; kappa_req 0.081–0.110 constant; rank-4 coverage 0.916→0.245). `strongfield`: `u_turn_cols` 0/200, `turn_slack_min` 1.19e-4, `cell_violations` 0, `missed` 0 of 7,924,025, inflate 1.002 — all identical.
- One determinism finding: `naive_pairs` came out 2,762,410 vs the stored 2,762,416 (2×10⁻⁶ relative). Cause: `cells` is built from a `HashMap` (randomized iteration order per process) and the naive-pair predicate uses `lw` of the first cell in iteration order, which is asymmetric. Every canonical counter is exact; the "bit-identical in every counter" sentence is falsified only by this non-physical one. Fix before adoption: sort cells before the pair loop.

## Held-out check

`predictions.md` carries specific kill criteria. The straggler matrix content held exactly as pre-registered (zero misses, margin < 1, scaling constant within ±3%, kappa constant, negative control fires at the engine dial only). The birth-fixed kappa misprediction (0.019–0.035 vs the named 0.02–0.04-for-the-narrow-band) is honestly reported. Strict pre-registration is **not verifiable from file times** (predictions.md mtime is after metrics-straggler.json; the post-script edit is disclosed), and the strong-field predictions are admitted confirmations — I weight the content, which is falsifiable and matched, and note the caveat.

## Adversarial cases (mine, all outside the author's tuning)

1. **Unseen seed** (777001, same narrow band, n 800/1600, both dials): misses 0; `arc_over_w_max` ≤ 0.853; `cand_per_enc` 5.6/5.7 at the engine dial (constant in n); negative control fires (300/1275); rank-4 coverage decays 0.73→0.47.
2. **Phase cluster** (80 % of bodies in a 0.3 rad λ(0) arc — the rank killer, never run by the author): misses 0 at both dials while `rank4_cov` collapses to **0.098**; `cand_per_enc` 2.1, cost still tracks encounters. Independently confirms the run's central correction: rank-k is not the certificate; the per-pair algebraic window is.
3. **Eccentric band** (σ_e 0.08 and 0.15): misses 0; high-e cells saturate at the π cap exactly as the honest-limitations section says; margin ≤ 0.61.
4. **Doubled horizon** (40 orbits): misses 0; w grows 1.115→1.585; kappa_req grows 0.10→0.19 (the rank shadow worsens, the window does not).
5. **Fresh strong-field seeds** (999111 ρ=0.02, 999222 ρ=0.05): `u_turn_cols` 0/200 both, `cell_violations` 0, `missed` 0, inflate 1.002.

I also re-derived the Schwarzschild algebra independently: the radial cubic 2L²u³−L²u²+2u+(E²−1)=0, the double-root condition (1−E²)r²−(4−3E²)r+4=0, and L²=r²/(r−3) at both roots — the script's `turning_points` and `l_bounds` are correct, so the monotonicity scan covers the true bound domain [L_sep, L_circ].

## Novelty

No HISTORY entry covers the arc window, the rank-k correction, or the strong-field key order (greps for tube_lattice/rank/20261011: nothing; the original run is graded-silver on its branch, unmerged). This amends the adopted gold 20261006-0734 ("phase-neighbour certificate", rank-4) the way the board's own override clause anticipates: concentration breaks rank-k; the window replaces it at constant cost per encounter. law.md §tubes (key = quantized (E,L)) is the design this certifies.

## Goal fit

Board items 3 and 6: encounters without per-body state, candidate work tracking real encounters — measured constant per encounter at fixed distribution (the dilution caveat stays, as q-candidate-degree already established). PRINCIPLES #1 ("The cheapest compute is compute not done") and #19: the rank growth was the wrong unit, and the window dissolves it rather than patching it.

## What the author missed

- **The U-scan contiguity instrument is inert.** `lw` computes the *minimal* window covering every u_close partner, then `naive_miss` counts partners outside that window — 0 by construction, in any scene; prediction (6)'s `naive_miss = 0` is a control that cannot fail. Worse, the scene has no power for it: with e up to ~0.9 and ρ=0.05, the U-band set is 2,762,179 of 2,764,425 possible cell pairs (99.93 %), and the Newtonian control is likewise saturated (47,586 = every cell pair, e_hi hard-capped at 0.5). The "1.0001× tight" line is an artifact of a hot scene, not evidence of contiguity. The load-bearing strong-field content — monotonicity and the compile's zero-miss — is sound; but before anyone adopts the scan-cost figure, rerun the U-scan on a cold strong-field belt (small e, thin U-annulus) with an a-priori window width and a real miss counter.
- The `naive_pairs` HashMap nondeterminism above.
- The equal-period (birth-fixed) branch is only exercised on 3 discrete keys with spread ϖ; a many-key birth-fixed belt (the actual fleet case) was not run.
- The GR version of the arc bound (equation of centre compiled per key from the memo's Δφ) is derived but unmeasured — disclosed, and it gates adoption of the *GR* dial, not the Newtonian one.
