# Dossier — inverting gold 20261006-0346-taleb-09b5 (the co-orbital phase certificate)

## Claim

The gold's "every real encounter lies within partner rank 4 along the orbit" is a **snapshot
property of phase-AND-element-coherent, isolated formations only**: with the eccentricity spread
any burn leaves (σ_e = 0.02–0.05), a k = 4 phase-neighbour certificate misses 60–88% of real
encounters; held in the gold's own tight regime, the ordering still moves at ≈ 1.5·(δa/a)·n ranks
per orbit, so a certificate refreshed once per orbit misses 1.9% (at 10-orbit lag, 94%); and 87%
of a fleet's encounters in a bath are fleet×belt pairs no body-level trigger can route. The
measured law is rank ≈ 4·σ_e·n/(2π) (the equation of the centre), so the trigger needs element
coherence, a shear-scaled refresh, and per-pair routing — three conditions, not one dimensionless
number.

## Bottleneck

Board item "encounters at N (the co-orbital certificate)" / the top scaling risk. The gold
promised to delete the quadratic tier (135× setup, ~40 TB at 10⁶) for concentrated workloads.
This run does not delete the certificate; it bounds **where it is valid**, which decides what the
encounters design may build on it. Expected gain: none claimed; a wrong-premise correction before
the certificate is wired (the same class as the 5 October correction).

## Evidence

Truth = the encounters crate's own `truth_pair` (every local distance minimum < ρ, rigorous
conservative advancement; 76–348 M steps/scene). Planar, μ = 1, a = 1, n = 600 (fleet) unless
said. Rank of an encounter = partners between i and j in circular mean-longitude order at the
given time (max of both directions).

| scene | events | rank at t_m med / >4 | lag 1 orbit med / >4 | t=0 med / >4 |
|---|---|---|---|---|
| A-control: tight circular formation, δa = 1.2ρ, 120 orbits | 10,128 | **0 / 0.0%** | 1 / 1.9% | 57 / 93.4% |
| B σ_e = 0.005 (identical periods, frozen phases), 60 orbits | 7,380 | 1 / 4.9% | = | = |
| B σ_e = 0.020 | 5,760 | 6 / **60.4%** | = | = |
| B σ_e = 0.050 | 6,000 | 14 / **88.0%** | = | = |
| C σ_e = 0.01, δa = 5e-3, ρ = 1e-4 (the r8 belt regime), 100 orbits | 927 | 3 / **29.3%** | 5 / **57.3%** | 170 / 96.9% |
| D fleet 200 (tight) in belt 800, 100 orbits | 29,918 | fleet-fleet 1 / 0.5%; fleet-belt 8 / 73.7% | — | — |

- **P1 control reproduces the gold**: A-control dynamic rank max = 3 over 10,128 encounters, zero
  misses at k = 4. Its claim is not strawmanned.
- **Element spread (the equation of the centre)**: rank medians 1 / 6 / 14 track 4σ_e·n/(2π) =
  1.9 / 7.6 / 19.1 across a 10× sweep. Two bodies on eccentric orbits can be physically within ρ
  while their mean longitudes differ by ~4e; mean longitude orders position only for e ≪ 2π/(n).
  C shows the crate's own belt default (σ_e = 1e-2, ρ = 1e-4) already misses 29% **at the moment
  of closest approach**.
- **Shear sets the refresh rate**: in A (e ≈ 0, so no e-coupling at all) a once-computed
  certificate misses 93%; refreshed each orbit it rides the edge (p90 = 3); at 10-orbit lag 94%.
  Lag-1-orbit medians follow (3/2)·(δa/a)·n: predicted ~4.5, measured 5 (C). So O(n·k) carries a
  maintenance term of ~(3/2)(δa/a)·n²/(2k) rank-updates per orbit that the gold's cost statement
  omits — the ordering is a derived, drifting structure, not a stored one (PRINCIPLES 6).
- **Composition**: fleet×belt = 9,427 of 10,796 encounters (87.3%) involving fleet bodies. A
  trigger that fires "concentrated" per body and replaces the quadratic tier for those bodies
  loses 87% of their contacts; the belt's own tier does not see fleet×belt pairs unless it runs
  on fleet bodies too — i.e. the quadratic tier returns exactly when a fleet crosses a bath.
  Routing must be per pair, not per body.

Reproduce (Linux x86, shared runner; orders of magnitude only):
```
cd lab/results/20261007-0800-inversion-7532/work/fleet
cargo build --release --offline          # ~5 s
../fleet-out.jsonl is the full output; rerun: $(printenv CARGO_TARGET_DIR)/release/fleet
```
Per-scene wall times 12–64 s (D 63.8 s, 4 threads, < 200 MB). Raw per-encounter rows (first
4,000/scene): `events.csv`. Aggregates: `fleet-out.jsonl`. Source: `work/fleet/fleet.rs` (uses
only the encounters crate's public API; no crate file edited).

## Predictions

Written before any scene ran (`predictions.md`): P1 reproduced (control 0% misses), P2's scaling
held within a factor of 2 at all three σ_e (60% and 88% misses at k = 4), P3's lag-1-orbit median
~(3/2)(δa/a)·n measured 5 vs predicted 4.5 with > 20% misses (57%), P4's ≥ 30% cross-fraction
measured 87.3%. All four held; no kill criterion fired.

## What would make it wrong

- If the gold's rank was defined in **true** longitude, not mean longitude: the e-coupling halves
  (2e, not 4e) but does not vanish; breaks 2 and 3 are unaffected. The gold's run folder is on
  its own branch and was not in this tree, so its exact definition was reconstructed from the
  crate's conventions — a misreading of its scope is the main risk to this dossier, not the
  measurements.
- Single seed per scene, single n = 600 (the σ_e sweep substitutes for an n sweep via the
  analytic law), planar only (inclination spread would add a third rank source), medians over
  events not pairs (B's equal-period fleets repeat each pair every orbit: 7,380 events from 115
  pairs — the per-pair picture is identical because the geometry is frozen).
- A fleet whose burn leaves σ_e ≤ ~0.01 and stays out of baths keeps a working certificate: the
  gold survives as a **per-population tier gated on element coherence (4σ_e·n/(2π) ≤ k), refreshed
  at the shear rate, with cross pairs routed to the window tier**.

Cost of adopting the correction: none in code (nothing is wired yet); the encounters design
(v2) must grow the trigger from one number to the three inequalities above, or order the
certificate by crossing longitude (Binet arc locality — the geometry that produces encounters)
instead of mean longitude. Fit: "A failed expectation is not automatically a failed method:
diagnose which one broke (H0183)" — the certificate is not killed, its scope is; "Compute only
surprises… nothing is evolved that can be derived when looked at" — the λ-ordering is derivable,
drifting state and should not be stored; #19 — mean longitude is the wrong water for this fish.

## The lens

Inversion attacked the newest adopted gold's silent assumptions and found the three scenes it
excludes; it also forced a control that reproduces the claim first (never strawman). What the
lens may have missed: I did not attack the gold's cost numbers (135×, 40 TB), only its
correctness premise; and an inversion lens underweights that the *repair* (order by crossing
longitude, not phase) may be the actual gold here — a builder's rung, not a checker's argument.
