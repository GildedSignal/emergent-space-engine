# Dossier — inversion (run 20261006-0346-inversion-8cee)

## Claim

Inverted on the newest verified success (r8 v3's "missed 0/18708"; q-candidate-degree's "zero
misses"): the crate's per-passage **check — a fixed-k sign-change bracket inside a heuristic
window — is the last uncertified boundary in the encounter chain, and it misses real encounters in
exactly the two game-real regimes no frozen belt ever tested: high eccentricity (17/241 = 7.1% and
9/167 = 5.4% missed at e ∈ [0.60, 0.95]) and the clustered-phase fleet wall (2/3890 missed at
e ≤ 0.02) — every miss confirmed by two finders that share no decision rule (the crate's rigorous
truth and my dense comparison-based scan); meanwhile work per encounter does not track the
encounter rate *across distributions* (254k–505k state evals per encounter at high e vs 309 on the
control, 800–1600×).

## Bottleneck

Board item "finding encounters without work per orbit or per element change" and the top scaling
risk. The inversion found where that item's verification premise breaks: `make_belt` caps e at
0.5, so **every frozen verification belt in the r8 lineage (crate sets, r8 v2 sampler, r8 v3's 20
belts) tested only e ≤ 0.5, phase-mixed, and never a clustered-phase formation** — while the plane
(the flying product, #1 measured bottleneck) runs a fleet battle and B13 already starves
near-parabolic flybys. Expected gain from adopting the consequence: the motion law v2 (being
designed now, with the three silvers folded in) gets the certified check boundary and two scene
families added to every frozen encounter verify set — before the law freezes on an uncertified
bracket. Nothing is deleted; a guard is specified (below).

## Evidence

All in `lab/results/20261006-0346-inversion-8cee/` (binary `enc/target→CARGO_TARGET_DIR/invert`,
built from a copy of `crates/encounters` plus `enc/src/bin/invert.rs`; scenes construct `Body`
directly, bypassing the generator's e ≤ 0.5 cap). Machine: GitHub Actions linux, 8 vCPU, shared
(load 1.9–3.6 during runs); timings order-of-magnitude only. Each command ≤ 40 s, < 300 MB.

- `invert run <scene> <stride> <dense_orbits>` → one JSON line (saved as `<scene>.json`).
  Judges: crate truth (radial pairs, conservative advancement) over the full horizon, plus a
  dense fixed-grid third opinion (minima by **comparison** + golden-section refine, Halley states;
  no Δr·Δv brackets, no Newton-on-g) on strided pair samples — a mechanism shared by neither
  method nor truth.

| scene | truth_enc | missed | false | dense agrees | evals/enc | checks/enc |
|---|---|---|---|---|---|---|
| ctrl-coorbital (frozen set c) | 2093 | **0** | 0 | 3-way 0/0 | 309 | 0.95 |
| highe-align (e .60–.95, ϖ=0) | 241 | **17 (7.1%)** | 0 | yes, on sampled frame | 254,060 | 514 |
| highe-rand (e .60–.95, ϖ rand) | 167 | **9 (5.4%)** | 0 | yes | 505,314 | 1,305 |
| formation (fleet, phases spread) | 398 | 0 | 0 | yes | 24,901 | 1.26 |
| wall (fleet, phases clustered) | 3890 | **2** | 0 | — | 2,485 | 1.28 |

- **Miss anatomy** (`validate-*.txt`, each event found by truth AND dense, found by neither
  method-path): pair (28,121) highe: one Wide section, window ±6.34 time units, scanned at k=64 →
  sample step 0.11 while the sub-ρ dip lasts ~0.04 (`missed_profile`: d 4.96e-4 at centre, 2.9e-3
  at ±0.02) — the bracket never samples the sign change. Pair (6,17) wall: quasi-stationary
  formation pair; d ≈ 9.267e-4 < ρ across a flat terrace ≥ 0.24 wide against a section window of
  half-width 0.0023 — the encounter outlives the window's geometry assumption by 100×. Two
  opposite kinematics (fast-narrow dip; slow-flat terrace), one failure class: **the check's
  sample resolution and window are tuned, not certified**.
- **Cone tolerance is sound here**: 11/28,680 radial candidates rejected by the cone never come
  closer than 73–286 ρ in the horizon (`cone_rejected` lines) — the ε_u margin does not cause the
  misses.
- **Cross windows live on a 12% edge**: highe-rand `max_util_cross` = 0.876 with SAFETY = 1.1 —
  real encounters land at 88% of the half-width; one Taylor misestimate from dropping out. No
  Cross section exists at all in highe-align (all demote to Wide/Full: sections [0, 5696, 20180]).
- **Cost inversion across distributions** (q-candidate-degree's "constant at fixed density"
  confirmed *within* a family, broken *across* families): 309 → 24,901 → 254,060 → 505,314
  evals/enc from control → fleet → highe-align → highe-rand; setup (numeric Wide windows), not
  discovery, holds the cost — the silver's own 91%-tangency measurement, now measured in the
  crate itself at game-real scenes.

## Predictions

`predictions.md` written after only the controls had run. Held: misses at high e (1, main);
aligned ≥ random (2); cost inversion ≥ 5× (3, in fact 800×); fleet cost ≥ 10× baseline for
`formation` (6, first half). Failed, reported as held: my stated miss *mechanism* (Cross-window
Taylor undershoot) was wrong — there are no Cross sections at highe-align; the real mechanism is
the bracket/sample resolution (found by forensics, not predicted). Failed: false reports at high e
(4: zero everywhere; r8 v3's single g-noise false did not reproduce). Partially failed: fleet
correctness (5: `formation` 0/0 but `wall` missed 2) and `wall`'s cost (6, second half: 8×, and
its checks/enc is not the highest).

## What would make it wrong

The misses rest on two finders agreeing per event (truth + dense, distinct mechanisms; the
5-October lesson applied — I checked the events are distinct before counting). If the frozen
definition of an encounter excluded terrace minima or dips shorter than the sample step, the
`wall`/highe events would not count; the rung text says "every local minimum of the distance below
ρ", which they are. The dense scanner could itself miss dips narrower than its own grid step
h = ρ/(2·v_sum) — it cannot miss any dip wider than 4 grid steps, and every event it reports was
independently confirmed by truth. Cost of adoption: none for the measurement; the fix is one
certified-step guard in `check` (see below) plus two scene families in the frozen verify sets.
PRINCIPLES: "A failed experiment kills that configuration, never the method" — this kills the
*tuned bracket configuration* of `check`, not the Binet-cone/first-hit representation; "Floats may
explore; only integers decide canonical outcomes" — the bracket is exactly a float sign decision
deciding a canonical outcome at whatever resolution the tuner chose.

## The fix direction (for motion law v2, one law at every scale)

`check`'s sample step must be certified, not tuned: the same Lipschitz bound `numeric_window`
already proves in s (max relative speed × step ≤ ρ/2, or conservative advancement within the
scan) sizes k inside `check`; flat-D pairs (the wall) widen to Full sections by the same test that
demotes Cross to Wide. That is the existing law applied at its own next scale — no new mechanism.

## The lens

Inversion asked what the newest success silently assumes; it assumed the verifier's scene space
covers the game's. What this lens may have missed: the fix's cost (a certified step at highe
windows is ~10³ samples/check naively — the interesting design question is whether the certificate
can live in the integer first-hit layer instead); 3D inclination; and whether the plane's actual
fleet hand-out (doll-managed, B13 cadence) already avoids the wall geometry that breaks the crate.

## Reproduce

```
cd lab/results/20261006-0346-inversion-8cee/enc && cargo build --release
$CARGO_TARGET_DIR/release/invert run ctrl-coorbital 16 4     # control: 0/0
$CARGO_TARGET_DIR/release/invert run highe-align 24 3        # 17 missed
$CARGO_TARGET_DIR/release/invert run highe-rand 24 3         # 9 missed
$CARGO_TARGET_DIR/release/invert run formation 16 4          # 0/0, 25k evals/enc
$CARGO_TARGET_DIR/release/invert run wall 16 4               # 2 missed
$CARGO_TARGET_DIR/release/invert validate highe-align 28 121 10   # miss anatomy
$CARGO_TARGET_DIR/release/invert validate wall 6 17 20            # terrace anatomy
```
