# Dossier — run 20261003-1842-taleb-3ec1 (lens: Taleb)

## Claim

The encounter structure's eager per-pair setup is a fragility, not a cost: on cold belts 99.4–99.6% of candidate pairs cannot propose a passage within 100 orbits yet the setup pays 98–99% of its numeric work on exactly those pairs; the numeric cost sits on a tangency cliff (3 orders of magnitude, and worst in the cold/ring case the engine will actually run at scale); one player-sized burn re-setups O(N) pairs (measured up to ~8 s extrapolated at 10⁶, single-threaded x86) — and the natural fix, deferring refinement to check time, is falsified (1.7–8× more work over a consumed horizon), leaving refine-on-first-activation as the open structure.

## Bottleneck

Board focus 3 (encounters without work per orbit or per element change) and 4 (smoothness, the allocator). The law's open cost is the setup, 2.5–24 µs per candidate pair per element change (law.md, finding encounters). Measured here: that cost is paid where nothing observable can happen soon, and its worst case is player-triggerable. Expected gain of the fix direction: 4–30× on the per-element-change constant (measured lazy 1.0–1.6 µs/pair vs eager 4.4–44 µs/pair), and up to ~100× if a sharp dormancy certificate is found (the 98–99% deletable fraction). It deletes nothing structural by itself; it would delete the numeric window from the kick path.

## Evidence

Cloud container, 2 vCPU EPYC, load ~2, single-threaded measurements (state in `machine.txt`); orders of magnitude only. New code: `lazy_sections` in `crates/encounters/src/pairs.rs` (cap-window sections, no numeric refinement), experiments `fragility` and `kicktail` in `crates/encounters/src/main.rs`. Data: `fragility-{a,c,d}.jsonl`, `kicktail.jsonl` in this folder.

Reproduce (each ≤ 60 s):
```
cargo build --release -p emergent-encounters
./target/release/encounters fragility a   # 4 belts, ~5 s
./target/release/encounters fragility c   # adversarial: narrow, coorbital, equal-period keys, ~9 s
./target/release/encounters fragility d   # hot/mixed/dense, ~6 s
./target/release/encounters kicktail      # < 1 s
```

Numbers (10 belts: the crate's verify sets a, c, d):

1. **Dormancy.** Fraction of candidate pairs whose first in-window passage (the engine's own integer first-hit, on the built section) lies beyond the horizon: 99.4–99.6% at H = 100 orbits and 93.8–95.7% at H = 1000 on the cold belts (σ_e = 1e-3…3e-2); 88–98% at H = 100 on hot/adversarial ones. The eager numeric work on eager-dormant pairs: **98–99% of all evals** (cold belts; 71–99% overall). The mean setup cost lies by ~2 orders of magnitude.
2. **The tangency cliff.** Per-pair numeric evals are bimodal: median 0 (Cross/Full sections) on every belt, while the near-tangency/merged-arc minority (|cone_gap|/eps_u < 2; 1–19% of pairs depending on coldness) carries ~100% of evals, up to 1.3k–8.3k evals per pair. The cold-ring case is the worst per pair (σ_e = 1e-3: 37.9 µs/pair vs 5.8 µs/pair at σ_e = 3e-2): cost is anti-correlated with encounter rate — the quiet belts that dominate at game scale pay the most per pair for encounters that almost never come.
3. **Sound cheap certificate.** A cap-window section (passage-overlap bound, a superset of the true encounter offsets by construction) plus one integer first-hit costs 1.0–1.6 µs/pair (4–29× below eager) and never missed an encounter: across 10 belts, 0 violations in 119 hit-pairs (no pair with hits within 100 orbits was cap-dormant), and the A/B run (exact checks over cap windows, with `pair_events`' dedup) reproduced every encounter list identically (diff_pairs = 0). But it certifies only 51–80% of cold-belt pairs dormant at H = 100 and covers only **2–59% of the numeric evals** — the expensive tangencies escape it.
4. **Falsified fix.** Wholesale deferral of refinement to check time (cap windows + exact checks over the arc) costs 1.7–8× more evals and wall time than eager when the horizon is fully consumed (narrow-adversarial: 435 ms vs 55 ms on the control sample). Correctness holds; the cost does not.
5. **The player tail.** One body kicked at the belt's dense end (a = 1.02, belt a ∈ [1, 1.5], σ_e = 1e-2): candidates 372→2500 of 2500, 1447→9999 of 10⁴, 26156→39995 of 4·10⁴ (e = 0.05→0.5), i.e. 1.2–12× the median body's, reaching the whole belt. Eager re-setup of that one body: 2.9–294.7 ms at N = 2.5k…40k (worst at e = 0.3, 12.1 µs/pair — the cliff is interior, not at the extreme: mid-e crossings vs a cold belt are the most tangential). Extrapolated linearly in N at fixed σ_e: **3.3–7.9 s at 10⁶ bodies, single-threaded** — hundreds of dropped frames from one player action. The lazy path bounds it to 0.7–1.1 s (still O(N): the U-scan itself is the floor; only a group certificate removes the O(N)).

## Predictions

`predictions.md` was written before the decisive run. Held: P1 (dormancy ≥ 99% at H = 100, ≥ 95% at 1000 — barely, 95.17% on the σ_e = 1e-2 belt), P3 (lazy ≤ 1/3 eager), P6 (0 violations, identical encounter lists). Failed, reported as held-out misses: P2 (≥ 80% of evals deletable by the cap certificate — measured 2–59%: the cap window is ~100× wider than the true window, so the expensive tangencies never certify dormant), and P5's concentration number (≥ 50× the median body's candidates — measured 12×; the median body already owns ~8% of the belt). P4 held in substance (cliff) but its "max ≥ 50× median" was vacuous (median is 0); the honest form is the bimodality above.

## What would make it wrong

The dormancy and cliff numbers are geometry (window fraction ~ρ/v_rel vs synodic phase; tangency → conservative advancement crawls), so they should transfer to the M1 up to constants; the kick-tail extrapolation is linear in N at fixed σ_e and could break if per-pair cost falls with density (it rose slightly here). The certificate's soundness rests on the cap window being a superset of encounter offsets — proven by arc confinement and confirmed on 119 hit-pairs, but it is the same class of assumption r8 v2's checker punctured for the conjunction-windowed reference; a checker should hunt a counter-example on merged-arc and near-Full geometry specifically. Adoption cost: small (`lazy_sections` is ~60 lines, uses only existing machinery); the design change — cap sections at kick time, refinement only at first in-horizon proposal — touches the queue, not the law. Fit with PRINCIPLES: "Compute only surprises" (3) — the eager setup computes where no surprise is possible for 100 orbits; "No work for no reason" (14); "the player is the only wildcard, and their influence travels at c" (5) — the burn's O(N) re-setup is the wildcard's price tag and must be budgeted by the allocator (12), not amortized by a mean.

## The lens

Taleb's lens prices ruin and tails, and it found the cost upside-down (quiet belts pay most; worst case at mid-e; the mean lies). What it may have missed: whether the 98–99% dormant waste even matters to a frame budget dominated by the ~0.5% active pairs and the kicks' other costs (29 µs each on the plane) — the integrator's measured-bottleneck discipline, not fragility aesthetics, must decide; and the barbell's speculative end (the sharp cheap window: a closed-form curve-distance bound in Binet space, the time-domain twin of r8 v3's skin) is named here but not built.

## Grade suggested

Silver: real, reproduced, controls on both sides (soundness A/B identical lists; falsified negative for the wholesale deferral), one named experiment from gold — build the refine-on-first-activation hybrid on the kick path and show the per-element-change cost falls ≥ 10× with no missed encounters at the engine's planning horizon.
