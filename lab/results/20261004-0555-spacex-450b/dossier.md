# Dossier — 20261004-0555-spacex-450b (SpaceX lens, question taken from board bottleneck 1)

## Claim

At behaviour tolerances (B14 precession 10%, B12-style Jacobi 1e-4), no splitting order buys the 4× kick cut the q-correctors brief asks for: Yoshida-4 beats the plane's DKD by at most 1.34× (24.7 vs 33 kicks/orbit), the plane's 1/64 is already within ~2× of the behaviour frontier on every judged case, and at 0.45 Hill radii prograde every scheme at every affordable setting silently gets the apsidal precession wrong (sign flipped, 10× error) while energy and eccentricity look perfect.

## Bottleneck

Board focus 1, "fewer kicks per orbit at the same behaviour (correctors, higher-order splits): kicks dominate the engine's cost", queued as `q-correctors`. Expected gain if the brief's gold bar held: ≥ 4× fewer kick events per orbit, hence ≥ 4× off the dominant engine cost. What it would have deleted: 3/4 of all rebinding work (`step.rs`: each kick rebinds a tube, ~24–29 µs of the ~29 µs event).

## Evidence

Float replica of the plane's exact split (`replica.rs`, mirroring `crates/universe/src/step.rs`'s documented law: exact Kepler drift in phase steps, one kick of weight h at the interval midpoint; the kick = the star's tide in the planet-centred frame; CRTBP scene, star 1.0 + planet 1e-3, moon a test particle, 50 planet orbits). References: dkd@4096 and y6@~8208 sub-kicks/orbit agree on the apsidal precession slope to ≤ 7.8e-5 relative on all seven cases (`ref.txt`) — the reference is converged, not a strawman.

Schemes: dkd (the law), y4 (Yoshida-4 triple jump, 3 sub-kicks/step), y6 (order 6, 9 sub-kicks/step), y4q (y4 with weights rounded to 1/256 — the dyadic-integer path). Cost = kick applications per orbit actually spent (phase stepping re-derives dt from the current orbit, as the law does; each application is a rebind).

Frontier (all gates: precession ≤ 10%, mean-e ≤ 10%, Jacobi ≤ 1e-4 relative, bound), from `sweep.txt`:

| Case | dkd min | y4 min | y6 min |
|---|---|---|---|
| A 0.30 R_H e=0.15 pro | 33.0 | 24.7 (ratio 1.34×) | 37.2 |
| B 0.30 R_H e=0.05 pro | 32.9 | 24.5 (ratio 1.34×) | 37.0 |
| C held-out e=0.30 | 33.2 | 49.8* | 37.2 |
| D held-out e=0.60 | 33.5 | 50.1* | grid gap |
| E held-out retrograde | 32.8 | 49.1* | grid gap |
| F held-out retro 0.60 R_H | 74.7 | grid gap* | grid gap |
| G held-out 0.45 R_H pro | FAILS all | FAILS all | FAILS all |

*grid gaps: my macro lists stopped before those frontiers; they bound nothing except that no larger cut exists below the listed settings. Reproduce: `rustc -O replica.rs -o replica && ./replica ref && ./replica sweep` (~60 s total, 2 vCPU cloud container, no other load recorded).

Key facts behind the claim:

1. **The binding gate is Jacobi, not precession.** dkd passes precession at ~17 kicks/orbit on A–E, but Jacobi ≤ 1e-4 needs ~33; on F (retro 0.6 R_H, 8× tide) it needs ~75 — the plane's current 1/64 is the *minimum* passing setting there. Under B14-only gates (moons: classification + precession + e) the margin is ~2–4× (A–E at ~17, F at ~38.5).
2. **Order stops paying at behaviour tolerances.** y4's best measured ratio is 1.34× on A/B; on the eccentric held-outs its passing setting is coarser-grid and no better than dkd's; y6 never wins anywhere. Consistent with the mechanism Wisdom et al. 2019 (arXiv:1908.03468) identify: correctors and higher-order kernels shrink the energy error by orders of magnitude but leave secular-frequency accuracy to gate at O(ε dt²)-type terms — our precession gate sits exactly there.
3. **The near-edge cliff (G).** At 0.45 R_H, references converge (7.6e-6) yet dkd@64 reports precession +0.49 vs the reference's −0.045 (12× off, wrong sign) with e_mean 0.2002 vs 0.2000 and Jacobi 8.6e-6 — a *silent* wrong behaviour. B14's "judged (non-chaotic) seeds" filter is load-bearing, and any kick-cutting must leave it alone.
4. **y4's negative sub-steps are fragile with phase stepping.** On F at macro=8 (21 kicks/orbit) y4 escapes outright (e→9000): the negative intermediate drift intervals collide with dt re-derived from a mid-sequence osculating orbit. dkd degrades gracefully at the same coarseness. A corrector class that adds backward sub-steps buys its accuracy with new blow-up modes near the edge.
5. **e = 0.60 costs nothing extra** (33.5 vs 33.0 kicks/orbit): phase stepping equalises cost across eccentricity, exactly as the law's doc claims ("a quasi-parabolic orbit costs no more kicks than a circle") — now measured, not asserted.
6. **y4q ≈ y4** (24.6 vs 24.7 on A; identical on B): rounding Yoshida weights to 1/256 loses nothing measurable — if any corrector is ever adopted, dyadic rational weights are a live integer path (a kick stays an integer sum with sigma-delta carries; only the weight set changes).
7. Byproduct: cost spent is state-dependent — a pumped orbit shrinks its own phase period and draws *more* kicks (dkd macro=2 spent 11.6, macro=4 spent 6.2). The law's cost tracks the body's surprise rate, which is the right sign for the allocator.

## Predictions

`predictions.md` was written before the sweep; references and scenes were fixed first (stated there). Score: #2, #3, #4, #8 confirmed (y4 ≤ 1.5×, y6 never pays, dyadic weights survive, no gold). #1 refuted — I predicted dkd passes at 8 kicks/orbit; Jacobi binds at 33, so the deletion margin in the plane's 1/64 is ~2×, not 8×. #5 refuted — e = 0.6 costs nothing extra (phase stepping vindicated). #6 half — F needs the full 1/64 (right), y4 blows up below ~50 rather than passing at 6–12 (wrong, and informative). #7 half — G's references agree and the moon stays bound (not chaotic), yet no coarse scheme gets its precession right: worse than predicted, because the failure is silent.

## What would make it wrong

- A single trajectory per case, one seed, float replica: the frontier ratios (1.34×, 2×) carry seed noise; medians over B14's 256 seeds could move them by tens of percent, though not from 1.34× to 4× — the gap to gold is a factor of 3 in ratio, larger than any plausible seed spread at fixed gate.
- The Jacobi gate's 1e-4 is imported from B12 (handoffs); if moons are judged by B14 only, the available deletion doubles (to ~1/16–1/32 of the period). The choice of binding gate decides the answer — that is the finding, not a weakness of it.
- My exponent fit (running max, log-log) shows ~0.9 for dkd at every N, which would fail a naive B12 exponent ≤ 0.2 everywhere; but the max scales as h² (33→66 kicks/orbit: 7.6× drop) and sits on a roundoff walk at 4096 — the exponent measure, not the law, is too crude here. A rung must pin the exponent above a noise floor before it judges moons.
- SABA-family schemes with built-in correctors (SABACL4's O(ε dt⁶ + ε² dt⁴)) were not run — coefficients could not be fetched from primary sources in time, and I refused to guess them. If the ε dt⁶ term dominates our gate regime, SABAC could outperform plain y4; the 2019-paper mechanism (their Fig.: SABACL4 ≈ WHCKL ≈ WHC for secular frequencies) argues it will not reach 4× either, but that is inference, not measurement.

Cost of adopting the nothing: zero. Cost of adopting the byproducts: none — #5, #6, #7 are facts about the existing law, not changes. Fit with PRINCIPLES: "Measure before claiming" (#10) — the 4× hope is now measured false at behaviour tolerances; "A failed expectation is not automatically a failed method" (#9/H0183) — this kills the *expectation* that splitting order is the lever, not symplectic splitting itself; "the simulation tells us what's next not us" (#22) — the binding gate (Jacobi on the deepest tide, or the near-edge seed exclusion) is where the next kick-cost work must aim, not the composition order.

## The lens (what SpaceX made me miss)

The idiot index pushed me toward the kick's arithmetic and splitting order — implementation-adjacent levers — when the measured truth is that the *gate structure* (which gate binds, which seeds are judged) sets the available cut, and the one-way doors (frozen gates, B14's seed filter) are exactly what my lens treats as deletable overhead. The lens also under-weighted that "delete 10% and see what breaks" is unsafe next to a frozen law: G shows the breakage is silent.

## Grade request

Silver-to-lead: no gold (no 4×, nothing adoptable as a scheme change). What stands: the q-correctors question is answered by measurement (order is not the lever at behaviour tolerances; the margin in 1/64 is ~2× and gated by the deepest tide in the scene), plus three reusable facts (phase stepping equalises eccentricity cost; dyadic weights preserve y4; near-edge precession fails silently at every affordable setting, so B14's judged-seeds filter is load-bearing). The named next experiment: freeze which gate owns moon kick cost (B12-style Jacobi vs B14-only) and pin the exponent-above-noise-floor rule; that decision doubles or halves the only real cut available.
