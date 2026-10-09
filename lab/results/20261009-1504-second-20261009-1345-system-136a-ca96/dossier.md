# Dossier — run 20261009-1504-second-20261009-1345-system-136a-ca96 (second author, system lens)

## Claim

The checker's named gold experiment, run on the shipped crate, **refutes the caching half of
20261009-1345-system-136a's claim**: the Δϖ rotation that cached `sections()` tolerate with zero
missed encounters is ≈1×10⁻⁵ rad — ~24× below the fine Δϖ-band (2.4×10⁻⁴) the original assumed safe
(9.3% of encounters silently missed there; 99.5% at the wide band 1.5×10⁻²), the radial half of the
key fails too (18.5% missed at half-bucket e-drift), the dossier's own mitigation (per-kick ti/tj
refresh) recovers 30× but not zero (0.32% at the fine band) and window widening ×16–512 changes
nothing — so the binding staleness is the arc geometry θ_c, which only a re-setup recomputes. The
corrected zero-miss amortization is ×1.8 at the unaveraged cadence (residence 0.056 orbits ≈ 2
kicks) and pure loss (×0.02) at the averaged cadence. The **discovery half** of the original claim
(bucket tier as conservative candidate index, zero misses) is unaffected and reproduced.

## Bottleneck

The board's "finding encounters without work per orbit or per element change" and r8 v3's open
setup cost (2.5–24 µs per candidate pair per element change; this box measures `sections()` med
**2.21 µs**, p99 2.64 µs — the premise was right). The original's answer was to amortize that
setup behind a (bucket, bucket, Δϖ-band) cache; this run measures the band the sections actually
tolerate and finds it ~50× narrower than the drift per orbit at belt scale, deleting the
amortization idea and pointing the lever back at making the setup itself cheaper (or at caching
only what is rotation-invariant).

## Evidence

All from the shipped crate (`crates/encounters`): `make_belt` (n=4096, a∈[0.9,1.1], Rayleigh
σ_e=0.1, seed 1), `cone_pairs` (7,210,923 candidate pairs), `sections`/`run_section` (the method),
`truth_pair` (brute-force control). New code is only the drift application (ϖ+a+e perturbation of
one body, lam0 held: position-continuous cutover) and the cached-vs-exact matchup (tol 1e-3;
conjunctions are ≥40 time units apart). Every sweep runs the **full candidate population**, 20-orbit
horizon, ~10.1k encounters per sweep; pairs whose exact run has no events cannot miss and skip the
cached run. Counts only; floats never decide an outcome.

Reproduce (< 6 min total, ≤ 73 MB):

```
cd lab/results/20261009-1504-second-20261009-1345-system-136a-ca96
python3 regen/exp.py          # 7 s; regenerates the ORIGINAL metrics.json bit-for-bit (diff clean)
cd exp2 && cargo build --release  # binary at $CARGO_TARGET_DIR/release/exp2 (CARGO_TARGET_DIR=/home/glmlab/lab-target-0)
./run: $CARGO_TARGET_DIR/release/exp2   # 2:01 min, 72 MB; writes metrics2.json, run-out.jsonl
../exp2b: $CARGO_TARGET_DIR/release/exp2b  # 2:46 min, 61 MB; writes metrics2b.json, run-out2.jsonl
```

**Controls, both sides.** δ=0 sweep: 10,086 events, 0 missed, 0 extra (the harness cannot-pass
control passes). Truth control: on 48 event-holding pairs at δ ∈ {0, 2.4e-4, 1.5e-2}, brute-force
`truth_pair` vs exact re-setup: 48/48 matched, 0 missed — the reference is sound on drifted
geometry. Extra events = 0 in every sweep (a stale cache can only miss, never invent — the exact
check holds).

**A. Δϖ tolerance of the plain cache** (sections computed once at nominal ϖ, reused as-is; misses
are encounters the exact re-setup finds and the cache does not; [cross, wide, full]):

| δ (rad) | exact | missed | rate | by kind |
|---|---|---|---|---|
| 0 | 10,086 | 0 | 0 | — |
| 1e-6, 3e-6, 1e-5 | 10,085–10,098 | **0** | 0 | — |
| 3e-5 | 10,098 | 4 | 0.04% | [4,0,0] |
| 1e-4 | 10,099 | 205 | 2.0% | [205,0,0] |
| 1.5e-4 | 10,094 | 463 | 4.6% | all cross |
| **2.4e-4 (fine band)** | 10,084 | **935** | **9.3%** | [934,1,0] |
| 1e-3 | 10,040 | 4,731 | 47.1% | [4718,13,0] |
| 3e-3 | 9,954 | 8,995 | 90.4% | [8947,48,0] |
| **1.5e-2 (wide band)** | 10,161 | **10,112** | **99.5%** | [10052,60,0] |

Zero-miss tolerance δ* ∈ [1e-5, 3e-5). With the belt's differential drift 1.77×10⁻⁴ rad/orbit
(regenerated [B]): residence ≤ 0.17 orbits; savings ≤ ×5.4 unaveraged (×1.8 at the zero-miss
point), ×0.05 averaged — against the claimed ×43 / ×2705 / ×25.

**B. The radial half of the key also breaks.** e-drift within one k-bucket: de_rel = 2.44e-4
(half bucket) misses 18.5%; 4.883e-4 (full bucket) misses 40%; corner (da 1e-4 + de 2.44e-4)
misses 85.7%. So neither half of (bucket, bucket, band) certifies section reuse; the bucket
envelope is conservative for *discovery* (original part A, reproduced) but the windows are far
more brittle than the envelope.

**C. Mechanism: not the window, the arc.** The dossier's stated mitigation — recompute ti/tj per
use (exact integer `passage_tick`) — cuts the fine-band misses 935 → 32 (0.32%) and half-bucket
radial 1847 → 40, i.e. the stale *phase* explains ~30×; but not to zero (1e-3: 681 missed; 1.5e-2:
90.3%). Widening the cached windows (safety 16 at the fine band: 46 missed; safety 64 and 512 at
the wide band: 90.5% still missed) changes nothing: the binding staleness is the crossing longitude
θ_c and its arc, which rotates with Δϖ (amplified ~|e_i/p_i|/|Δ(V,W)| for near-tangent pairs) and
is recomputed only by a full `sections()`. Predicted-by-me mechanism (window width) was wrong;
diagnosed by the safety sweep.

**D. Wall-clock.** `sections()` per candidate pair: med 2.21 µs, p90 2.39, p99 2.64, max 4.2 ms
(numeric-window tail). Full 20-orbit method pass: 4.8 µs/pair (setup ≈ 46% of a pair's 20-orbit
cost). At the plane's unaveraged cadence the setup is 32 × 2.21 µs ≈ 71 µs/orbit/pair — the wall
the cache was meant to delete stands; with the measured tolerance the cache saves ≤ 2 setups per
invalidation and costs a re-setup every ~2 kicks plus the ti/tj refresh.

## Predictions

`predictions.md` was written before exp2/exp2b ran. Held: P2 (misses are Cross-dominated; Full
never misses), P5 (both controls), P6 (extra = 0 everywhere), P7 (2.21 µs med, r8 v3's range).
**Failed, and reported as failed:** P1 (predicted 0 misses at 2.4e-4; measured 9.3% — the
arc-width argument ignored the amplification of dθ_c for near-tangent pairs and the arc-clamp in
`check`), P3 (direction right, cliff ~50× lower: first misses at 3e-5, not in [2.4e-4, 1.5e-2)),
P4 (half-bucket e-drift was predicted safe; it misses 18.5%). My mechanism guess in P1/P2 (window
width binding) was wrong; the safety sweeps (C) diagnose it as the arc.

## What would make it wrong

1. My drift is a step rotation of one body at fixed lam0 (differential Δϖ = δ, position-continuous
   cutover). A different phase bookkeeping (m0 held) shifts ti/tj by O(δ/n) — the same order the
   ti/tj-refresh already absorbs; it cannot move a 9.3% miss rate at 2.4e-4 to zero when even
   safety ×512 leaves 90% at the wide band.
2. The belt is 2-D Newtonian at ρ=1e-4, 20-orbit horizon (the crate's own verify scale). A game
   scene with far slower apsidal drift (weak field) would stretch residence ∝ 1/dω — but then the
   unaveraged plane is not that scene, and the original's own numbers (1.77e-4/orbit) are the drift
   in question.
3. Only Cross/Wide sections exist here (Full: 0 misses everywhere — nearly-identical orbits are the
   robust case; a formation-heavy scene would cache better than the belt, but the belt is the claim's
   own workload).
4. A different cache content — e.g. storing the *envelope* arc and re-deriving θ_c per kick — might
   yet amortize something; that is a new design, not the claimed key.

## Cost of adopting, and fit with PRINCIPLES

Adopt the refutation: delete the (bucket, bucket, Δϖ-band) section-cache from the encounters
design's next step (it was silver, unadopted — nothing to remove from code). Keep what survives:
the bucket tier as the discovery index (part A, zero misses, reproduced), and the measured facts
that `sections()` is 2.2 µs med and that its arc geometry — not its integer timing — is what a kick
invalidates. The next lever the numbers point at: make the setup itself kick-incremental (update
θ_c/arc from the Binet delta, which is closed-form) rather than caching it behind a band.
PRINCIPLES: "A failed experiment kills that configuration, never the method" (9) — the
configuration (band-keyed section cache) dies, the unification (one key space for storage and
discovery) stands; "Compute only surprises" (3) — the surprise here is the arc rotation, and it
arrives ~50× faster per orbit than the claimed band; "we know we have a fish, we need to find its
water" — Binet space is still the water, but its buckets tolerate discovery-slack, not
window-slack.

## The lens

The system lens sees structures to unify and may under-weight the different tolerance scales of
what it unifies: one key space, two very different conservatism requirements (candidate envelopes
vs encounter windows). I also inherited the original's belt-only view: the formation/Full-section
regime (where caching would be safest) is 0.5% of this workload. And this checker-named experiment
was run by the second author with the original author's harness conventions (matchup tol, drift
bookkeeping) — the 30× mitigation effect is robust to those choices, the exact 32-vs-46 missed
comparison at fine band is not (both nonzero, same order).

Wall (exp2 + exp2b + regen): ~6 min; peak 73 MB.
