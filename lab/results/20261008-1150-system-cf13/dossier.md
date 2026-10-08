# Dossier — one encounter certificate, not three

**Run:** 20261008-1150-system-cf13 · lens: the whole system · 8 October 2026

## Claim

The encounter finder needs one certificate, not three mechanisms: the phase-neighbour certificate
(taleb-09b5's O(n·k) tier and its dimensionless trigger) is the in-band readout of the crate's own
Binet-cone + Diophantine path — rank by mean longitude inside the widest frequency band the drift
bound allows, cone for cross-band pairs — and this one rule is exact on formations, co-orbital
swarms, crossing fleets and dispersed belts while cutting the formation's setup evals 59.7× (wall
53×) and touching zero physics code (the crate's `pair_events` runs unchanged; only candidate
selection changed).

## Bottleneck

The board's top scaling risk (5 October): candidate work must track real encounters. Under a
formation the candidate set is quadratic and the per-kick setup dominates (components-4643: 92% of
per-kick evals are window setup; taleb-09b5: setup goes quadratic, 135× work per encounter). The
design answer on the books is a second tier with a dimensionless trigger. Expected gain here:
~60× on formation setup, and one mechanism where three were planned (cone tier, slack skin,
phase certificate). What it deletes: the trigger, the separate tier machinery, and the formation's
quadratic setup.

## Evidence

Scenes (my own sampler, seed 0x5EED_2026_1008, the crate's own truth = conservative advancement on
every radially overlapping pair, Halley vs the method's Newton — no shared solver):

| scene | truth enc | crate as-is: pairs / evals / ms / missed | unified: pairs / evals / ms / missed |
|---|---|---|---|
| F1 fleet (N=500, a-spread 3e-5, σ_e=1e-3, ρ=1e-4, 30 orbits) | 275 | 124,750 / 11,197,808 / 749 / **0** | 2,000 / 187,453 / 14 / **0** |
| F2 swarm (N=600, a-spread 1e-4, σ_e=3e-3, ρ=3e-4, 20 orbits) | 676 | 179,700 / 15,530,779 / 985 / **0** | 4,957 / 439,206 / 32 / **0** (maximal band) |
| X crossing fleets (2×250, e≈0.2/0.16, ρ=1e-3, 30 orbits) | 2,279 | 124,750 / 34,857,427 / 2,859 / **0** | 90,153 / 17,067,309 / 1,446 / **0** |
| B belt (N=1000, a∈[1,1.5], σ_e=1e-2, ρ=1e-4, 100 orbits) | 203 | 42,219 / 813,788 / 91 / **0** | 41,802 / 813,788 / 90 / **0** |

False positives: 0 everywhere. Exact checks identical (318/318, 863/863, 4,439/4,439, 227/227) —
the unified certificate changes *which* pairs are materialized, never how a pair is judged.

The certificate's two scales, both derived, none tuned:
- **k** (rank cut) from the encounter geometry: at a meeting the true longitudes are equal, so
  |Δλ| ≲ 2(e_i+e_j); k = ceil(2.5·2·e_hi/spacing) + margin. Boundary measured on F1: k=1 misses
  12/275, k=2 misses 4/275, adaptive k=4 misses 0.
- **band width** from the drift bound: renew so in-band relative longitude moves ≤ one spacing;
  take the *widest* legal band (maximal-skin rule). F2 with the formula's 2 bands: 2.4M evals;
  with 1 band: 439k (5.5×). On B the bound refuses one band (margin 712 ≥ band size) and the rank
  path self-destructs into all-pairs — the cone path takes over with no cost change (91→90 ms):
  the tier choice is made by the certificate's own drift bound, a work measure, not a trigger.

Negative control (no bands, one global ranking): it does NOT miss — its margins swell instead
(X: k=138 of 500; B: all 499,500 pairs, 3,398 ms, 37× the band form). The band is load-bearing
for cost, not exactness: without it the same rule degenerates gracefully to quadratic.

Reproduce (each ≤ 9 s here, 6 threads, well under 2 GB):

```
cd lab/results/20261008-1150-system-cf13/exp
cargo build --release            # CARGO_TARGET_DIR=/home/glmlab/lab-target-1 on this runner
/home/glmlab/lab-target-1/release/exp F1   # or F2 | X | B ; one JSON line per config
BANDS=1 /home/glmlab/lab-target-1/release/exp F2    # maximal-band rule
K_OVERRIDE=2 /home/glmlab/lab-target-1/release/exp F1   # rank boundary (also K_OVERRIDE=1)
```

Raw lines: `f1.jsonl`, `f2.jsonl`, `x.jsonl`, `b.jsonl` beside this dossier.

## Predictions

Written before the run (`predictions.md`). P1 held (the crate as-is misses 0 on formations — the
taleb gold's "the window tier drops 4–6% of contacts" was the plane's two-tier window, not this
crate's sections machinery; the crate's `Full` kind already covers the degenerate regime). P2 held
(40,700 setup evals per real encounter on F1). P3 held (0 misses everywhere; 62× fewer pairs,
59.7× fewer evals, 53× faster on F1). P4 held (k=2 misses 4; the boundary is real). **P5
falsified in direction:** the no-band control does not miss cross-fleet encounters — its margins
swell to near-all-pairs — so the band buys cost, not correctness; my prediction had the failure
mode wrong and the run corrected it. P6 held (belt: identical evals, 1.01× wall).

## What would make it wrong

- **Eccentric swarms:** k ∝ e/spacing; at e≈0.2 (scene X) k≈33–84. A hot swarm (e→O(1)) with tight
  spacing makes rank ≈ all-pairs: the O(n·k) claim dies there and the cone path must carry it
  (exactness survives; the speedup does not). X already shows only 2×.
- **Kicks between renewals** change n and e; the drift bound assumes fixed frequencies over each
  renewal interval. The slack skin's element-drift budget covers this in principle (a kick forces a
  renewal) but I did not inject kicks — r8 v4's case (d) is the existing instrument for that, and
  the unified certificate should be judged by it before adoption.
- **Resonant / locked populations** (horseshoe librators) churn rank slowly; renewals cover it in
  principle, unmeasured.
- The truth is Newtonian Kepler (the crate's own); relativistic dolls change frequencies by
  precession per orbit — the drift bound absorbs it as extra dn, unmeasured.

## Cost of adoption, and fit

Adoption is a change to candidate selection in `crates/encounters` (a U-sorted index with per-band
phase order, the two derived scales, and renewals) plus the same element-drift skin already planned
(b-encounter-skin): the band's drift bound *is* the skin's rule read in frequency space — one
parameter, one rule. b-coorbital-cert's separate certificate and its trigger collapse into the
in-band path. Cost: one index structure and its renewal logic; no new physics code. Fit —
PRINCIPLES 32 ("under the right representation many symmetries can appear": the phase certificate
and the cone are two readouts of one rank/cone structure), 19 ("a fix signals the wrong
representation": the trigger was a fix for a missing band), 4 ("regimes are chosen by
dimensionless numbers": here even that is bettered — the regime chooses itself through the drift
bound's self-destruction), 1 (the tier and its machinery deleted), 33 (the band resolves only what
matters at its scale).

## The lens

The whole-system lens made me look for unifications and it found one; what it may have made me
miss: the experiment never touches the *kick* side (setup per element change under real kick rates,
the skin's actual amortization on top of bands), and never leaves the crate's Kepler world — the
plane's own encounter seam (`PlayerNeighbourhood`, O(doll) per find) and `shipmem`'s belts are
where the certificate must eventually live. The numbers above are Linux/x86 shared with other
runs: orders of magnitude, re-measured on the M1 by the integrator.
