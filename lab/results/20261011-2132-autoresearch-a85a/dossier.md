# Dossier — 20261011-2132-autoresearch-a85a

**Claim.** Caching j's τ-grid states once per numeric window and halving the τ-grid (k=32→16) makes
the encounters crate's per-kick re-certification 1.72× cheaper at ρ=1e-4 and 2.08× at ρ=1e-3 with
bit-identical event lists.

**Bottleneck.** Board focus line 3 / top scaling risk: encounters without work per element change.
The 6 Oct gold (`components-4643`) already showed 92% of per-kick evals are window setup; this run
attacks that setup directly instead of deferring it. Measured structure (new `prof` experiment,
`target/release/encounters prof 100`): Wide sections are 0.7% of sections (986/161k) but ~80% of
setup evals; each numeric window costs 1,148 evals in 34.7 sweeps; **78% of sweeps sample D<3ρ** —
the conservative-advancement crawl across a near-miss shelf takes ρ-scale steps
((d−ρ)/vmax) and is structural to the Lipschitz certificate, so the lever left is cheaper sweeps.
Gain: 1.7–2.1× on the metric; deletes ~40% of all Kepler solves in setup (redundant j-states), and
half of the rest (grid over-resolution). Composes with, does not replace, the slack skin (12.6×).

**Evidence** (all commands ≤ 60 s; binary at `/home/glmlab/lab-target-1/release/encounters` after
`cargo build --release -p emergent-encounters`):

| measurement | baseline | kept config | ratio |
|---|---|---|---|
| kick ρ=1e-4, µs/kick (100 kicks, n=10k, horizon 1000 orbits) | 7,712 | 4,502 | −41.6% |
| kick ρ=1e-3 (held-out), µs/kick | 41,455 | 19,901 | −52.0% |
| verify set e (held-out), method_s | 0.34/0.673/1.884 | 0.207/0.202/0.708 | 0.61×/0.30×/0.38× |
| verify set e (held-out), evals | 1.86M/6.00M/21.0M | 1.07M/3.66M/13.8M | 0.58×/0.61×/0.66× |
| events (truth/method enc, checks, hits, dup) set e | 427/990/1967 | identical | 1.0× |

Commands: `encounters kick` (baseline: 7,712), `encounters kick 1e-3` (41,455), then with the patch:
4,502 and 19,901. Gate: `encounters verify a|b|c|d|long` → all 14 belts missed=0 false=0 (checked at
k=16 AND at the rejected k=8); held-out `encounters verify e`. The baseline binary was built by
`git stash push -- crates/encounters/src/pairs.rs` with `prof_exp` stripped from main.rs, then
restored; `cmp` confirmed the rebuilt new binary byte-identical to the saved one.

**Predictions** (`predictions.md`, written before the held-out runs): P1 (zero missed/false on
set e) held; P3 (event identity vs baseline) held exactly; P2 was **wrong in the conservative
direction** — predicted the gain shrinks to 12–30% at ρ=1e-3 (shelf steps ∝ ρ), measured 52%:
larger ρ widens ε_u, pushing more arcs past the 0.2-rad cross-window threshold into the numeric
path, so windows carry more of the kick exactly where I expected less. P4 (k=8 on set e) not run.

**What would make it wrong.** The τ-grid min can be overestimated if an interior minimum escapes
both the sampled values and the Δr·Δv sign-change bracketing; a coarser grid widens that window.
The evidence against: 14 shipped belts + 3 held-out belts (including adversarial, coorbital,
σ_e=0.1, a∈[0.5,3], 1000-orbit) at zero missed/false, and exact event identity against the k=32
baseline on the held-out set. The residual risk lives on unseen arc geometries with two interior
minima inside one 16-cell — a belt built to have those would be the adversarial case. Cost of
adoption: ~30 lines in `pairs.rs` (patch in `work/patch.diff`; also adds the `prof` experiment,
verify set `e`, and a ρ argument to `kick`). Fit with PRINCIPLES: "The cheapest compute is compute
not done" (identical Kepler solves deleted); "It's a game… 'exact' means deterministic and
reproducible" (behaviours, not trajectories, are the gate — identical event lists, not identical
floats); no new law, no new category.

**The lens.** The one idea that carried most of the gain: within one numeric window, j's τ-grid
states are invariant in s — pay once per window, not once per sweep. Blind spot: a local search
tunes the existing crawl; the structural change that would beat it is removing the crawl class —
78% of sweeps sit at D<3ρ because near-tangency has no cheap analytic window (cross_window's
linear model degenerates as the crossing angle→0). A tangency-native window (second-order model in
the tangent limit, the analogue of what cross_window does for transversal crossings) would delete
the shelf walk rather than halve it. Above both sits the slack skin (94.6% of re-certifications
skippable at ε=1e-9, `slack_skip_violations: 0`), which this run now makes 1.7–2.1× cheaper per
remaining kick.
