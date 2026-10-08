# Dossier — second author on 20261007-2246-system-969a: the timing tier stacked on the key cells

**Claim (one sentence).** The checker's named experiment holds and the original claim now
carries its measured half — the shipped timing tier (`sections` + `dioph::first_hit` +
exact check, byte-identical `crates/encounters` code) stacked on the run's 12+12-bit
Catalogue-key window recalls every fine-truth encounter on every scene inside the window's
sound domain (0 missed, 0 false; steady/dense/spread/formation), with marginal tier-2 work
**bit-identical** to the same tier fed the shipped cone candidates and the key-only
breadth costing zero tier-2 work, and r8 v4's frozen `steady` and `checks` gates passing
for both tier-1 sources (1.400 vs 1.296 at 10⁵ orbits, gate ≤ 2.0; 1.10 checks/hit, gate
≤ 1.5) — **but the sound domain ends at e ≈ 0.969, not the checker's e ≈ 0.9995**: there
the pad's 1/g term crosses the periapsis (g < √(2⁻¹²)), the u-interval inverts, tier-1
silently excludes 46% of bodies and the stacked tier misses **206/289 (71%)** of the fine
truth's encounters, a boundary the checker's extreme-e probe could not see because its
sampled truth was underpowered (10 pairs).


## Bottleneck

Board focus "finding encounters without work per orbit or per element change" and the top
scaling risk. The original run's silver hung on one unmeasured half: the deletion is sound
only if the timing tier stacks on the key cells. This run measures exactly that. The gain
is the deletion the original run named: the float element sorts, the radial sort and the
plane's Cartesian scan retire behind one key-sorted list the law already stores.

## Evidence

Setup: `work/encounters_key` is a copy of `crates/encounters` where `diff` proves every
shipped file byte-identical (only `main.rs` gains a `keytier` experiment and a dump mode);
tier-2 is the shipped code path (`method_all` → `pair_events`), fed three candidate lists:
the key window (a faithful port of the author's `store_probe.py` — verified below), the
shipped `cone_pairs`, and their difference. Truth: the crate's `truth_all` over
`radial_pairs` (independent candidate source, Halley states vs the method's Newton — no
shared solver), i.e. much finer than the original run's 128–384 samples/orbit.

Reproduce (this folder): `python3 check_port.py $CARGO_TARGET_DIR/release/encounters`
(0 s), `cd work/encounters_key && cargo build --release`, then
`$BIN keytier <scene> [long]` for `steady dense formation spread highe400 extremee400` —
logs: `keytier_belt.log`, `keytier_rest.log` (steady+dense+formation ≈ 6.5 min, the
formation's Full-section setup dominates; spread ≈ 40 s; the full-size `highe` scene's
tier-2 runs exceed 10 min/pair-set at N=1000 and were capped: `highe400` carries the
comparison).

**Port validation.** `check_port.py`: Rust `key_window_pairs` u-intervals vs the author's
`store_probe.py` formulas on identical bodies: max relative diff **0.0** (50 bodies, dense
scene); pair counts equal (498,987). `keydump` membership cross-checked against the
author's Python sweep including its exact 590,153 count on the steady scene.

| Scene (N, ρ) | truth events | key tier missed/false | cone tier missed/false | tier-2 marginal work key vs cone |
|---|---|---|---|---|
| steady, r8 v4 case (b) (3000, 1e-4), 50 orbits | 922 | **0 / 0** (922 matched) | 0 / 0 | checks 1095 = 1095, qsteps 5 025 057 = 5 025 057, evals 7 455 335 = 7 455 335 |
| dense S2-family (1000, 5e-4), 10 orbits | 1657 | **0 / 0** | 0 / 0 | checks 2401 = 2401, qsteps, evals equal |
| spread S8-family (1000, 5e-4), 10 orbits | 528 | **0 / 0** | 0 / 0 | checks 746 = 746, qsteps, evals equal |
| formation S3-family (1000, 5e-4), 2 orbits | 369 | **0 / 0** | 0 / 0 | identical (pair sets equal: 499 500 = all) |
| highe S4-family (1000, 5e-4), 10 orbits | 1628 | 184 / 0 | (capped by time) | — |
| highe400, e∈[0.7,0.9] (400, 5e-4), 10 orbits | 268 | 36 / 0 | **36 / 0 — bit-identical** | checks 503 730 = 503 730, qsteps 407 602 = 407 602, evals 262 001 258 = 262 001 258; tier-1 sets equal (all pairs), so the high-e misses are the **shipped tier-2's** limit, inherited, not created |
| **extremee400, e∈[0.95,0.985]** (400, 5e-4), 10 orbits | 289 | **206 / 0** | **0 / 0** (all 79 800 pairs) | not comparable — the key window itself excludes (below) |
| extremee N=1000 (tier-1 sets; tier-2 capped by time) | 1670 | key pairs 163 461 / 499 500 (33%) | cone = radial = all pairs | — |

**Steady state (r8 v4 `steady`, gate ≤ 2.0; truth rate 0.006147/body/orbit):**

| horizon (orbits) | key events/body/orbit | ratio | cone events/body/orbit | ratio | keyonly checks |
|---|---|---|---|---|---|
| 10 | 19.681 | 3203 | 13.296 | 2163 | 0 |
| 100 | 1.974 | 321 | 1.336 | 217 | 0 |
| 1 000 | 0.2033 | 33.1 | 0.1395 | 22.7 | 0 |
| 10 000 | 0.02631 | 4.28 | 0.01993 | 3.24 | 0 |
| **100 000 (r8 v4's case-b horizon)** | **0.008605** | **1.400 ✓** | **0.007967** | **1.296 ✓** | **0** |

The ratio is one-off setup amortizing at exactly 1/H (setups 590 153 vs cone's 398 583);
the marginal rate beyond setup is checks-only: 0.006640/body/orbit vs truth 0.006147 =
**1.08×**, flat in H. `checks_per_hit` = 1.1027 both tiers (gate ≤ 1.5 ✓; 1.14–1.19 at
shorter horizons, 1.449 worst-case dense@10).

**Key-only breadth is free.** `key ∧ ¬cone`: 191 570 pairs (steady), 15 783 (dense),
50 831 (spread), 0 (formation, highe, extremee). At every horizon to 10⁵ orbits: 0
sections, 0 checks, 0 hits, 0 qsteps, 0 evals — `sections()` returns empty for
cone-rejected pairs (ΔU gap beyond ε(ρ)), so the wider tier-1 costs only the sorted-list
sweep, not tier-2.

**Formation (the gold's degenerate regime).** Both tier-1 sources keep all pairs;
tier-2 is identical bit-for-bit. Work per encounter 3.90 events/hit at 1000 orbits
(2.87 one-off setups + 1.03 checks), checks/hit 1.0279, falling in 1/H. The 2-orbit
snapshot (checks/hit 2.60) fails the 1.5 gate identically for the cone: a tier-2
Full-section property, inherited, not created, by the key store.

**The e ≈ 0.969 boundary (new; corrects the checker's find 4).** At e ∈ [0.95, 0.985]
the key window holds only 33% of the pairs (cone and radial keep all), and the stacked
tier misses **206/289 = 71%** of the fine truth while the cone tier misses none.
Mechanism (measured and analytic, `keydump` + the author's own formulas): the pad
`r_apo·(qp + qp/g) + r_peri·qp` carries a 1/g term that diverges as the gap shrinks;
pad > r_peri ⟺ g < √qp = 2⁻⁶ ⟺ **e > 0.9692**. There the widened inner radius crosses
zero, `u_hi = 1/(r_peri − pad − ρ)` turns negative, the u-interval inverts, and the
sweep pairs that body with nobody — a silent exclusion, not an unsound window. On the
extremee scene, 45.6% of bodies invert (measured), predicting key ≈ 29.6% of pairs vs
the observed 32.7%/33%. The checker's soundness sweep reported the boundary at
e ≈ 0.9995 (the apoapsis-side gq clip) and its extreme-e probe reported "0 misses" —
that probe's truth was sampled (10 pairs) and underpowered against fast periapsis
passes; the rigorous conservative-advancement truth (289 events) exposes the miss. The
one-line fix for the integrator: when pad ≥ r_peri, set the inner u-edge to +∞ (admit
the body everywhere) — sound by construction, and it makes key ≡ cone ≡ radial in that
regime, where radial overlap carries no information anyway (r8 v2's sentence).

**High-e (e∈[0.7,0.9]).** Both tiers keep all pairs; tier-2 is bit-identical (highe400)
and misses 36/268 = 13% for both, with checks/hit 2187 (gate fails, both tiers equally).
This is the shipped tier-2's known limit at long arcs, not a stacking defect.

## Predictions

In `predictions.md`, written before any scene ran. Held: 1 (0 missed / 0 false on every
scene, both tiers), 3 (checks ≤ 1.5 at long horizon: 1.10–1.14), 4 (formation marginal
checks 1.8e-4/body/orbit ≤ 1e-3, key = cone exactly — though my framing "truth ≈ initial
coincidences" was wrong: the formation keeps producing encounters at 0.17/body/orbit and
the stacked tier tracks them at 1.03 checks/hit), 6 (key-only share of checks < 5% —
measured 0.0%), 8 (bit-identical tier-2 on shared pairs: checks/qsteps/evals equal).
Failed as written: 2 (steady ratio ≤ 2.0 "at horizon ≥ 100 orbits" — it needs r8 v4's
actual case-b horizon 10⁵ orbits, where it passes at 1.400; my horizon was wrong, the
mechanism — setup amortization at 1/H — was right). Resolved after prediction: 5 HELD
(highe: the steady gate fails for both tiers — 2251 at 10 orbits — and the two tiers are
bit-identical there, within my 1.3× bound as equality); 7 **FAILED and became the run's
second finding** — I predicted 0 missed at e∈[0.95,0.985]; the fine truth shows 206/289
missed, because the pad rule itself excludes bodies at e ≳ 0.969 (the prediction assumed
the checker's e ≈ 0.9995 boundary was the only one; the periapsis-side zero-crossing is
earlier and stricter). One harness bug found and disclosed: my first sweep stored pairs
in u-sort order instead of (min,max); it made the first steady run report 458 phantom
misses (`diag_steady.py` documents the diagnosis; the author's Python and the fixed port
agree exactly). Lesson echoing the 5 October correction: equal counts are not equal sets
— I now check membership, not sizes.

## What would make it wrong

- **The wiring is unmeasured and outside lab authority** (never edit the crates): the key
  index behind `Encounters` in `crates/universe` and the plane-scan A/B are the adopting
  step; this run proves the measurement the checker named, not the merge.
- **Tier-2 under apsidal precession** remains unmeasured: `Body` is a fixed Kepler
  ellipse; the sections' crossing longitudes and windows would go stale as the apse
  precesses (the original run's orientation-free claim covers tier-1 only). One rung with
  a precessing truth would close it.
- **The shipped tier-2's own limits are inherited**: 184/1628 missed at e∈[0.7,0.9]
  (identical tier-1 sets, so not a stacking defect — `highe400` confirms the cone tier
  behaves the same), and the checks gate fails in the tight formation at short horizons
  for both tiers equally.
- **Tier-1's sound domain ends at e ≈ 0.969** (the pad zero-crossing, this run), which
  strictly tightens the checker's e ≈ 0.9995 apoapsis-clip boundary; without the one-line
  inner-edge fix, sungrazer-class bodies are silently excluded and the stacked tier misses
  71% of their encounters. With it, the key window is sound everywhere but loses all
  selectivity for e ≳ 0.97 (≡ cone ≡ radial there — the honest regime).

## Cost of adoption, fit with PRINCIPLES

Adoption is what the original run priced: a key-sorted body index behind `Encounters`,
the float sorts retire; this run adds that the timing tier needs no second index and no
extra work (0 marginal events; the 32–38% wider list dies in `sections()`'s empty return).
PRINCIPLES: "Store the generator, not the generated" (6); "the cheapest compute is compute
not done" (1); "under the right representation many symmetries appear" (32).

## The lens

The second-author lens trusts the checker's named experiment and runs it; what it may
have missed is everything the named experiment did not name: the N-scaling of the stacked
tier (r8 v4 case (c) not run; tier-1 scaling is covered by the adopted q-candidate-degree
silvers, tier-2 marginal work is candidate-source-independent as measured, but the joint
exponent is unproven), precession (above), and chirality (prograde-only scenes; the
checker already noted the window must ignore the Catalogue's chirality bit — still
unexercised).
