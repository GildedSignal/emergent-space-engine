# Rung r8 v3 — the Binet cone and exact first hits, verified independently

**Claim.** The diophantine method on `main` (Binet-cone candidates + integer first-hit sections +
exact per-pair checks) finds **every** encounter of an independent dense truth (missed 0/18708)
at 1.16 exact checks per encounter, steady-state work 1.29× the encounter rate, check-work
exponent 0.98 in N, and kick-isolated re-certification — but it reports **one false encounter**
(false_fraction = 5.3×10⁻⁵; criterion `sound` ≤ 0.0): on a co-orbital pair its minimum-bracketing
(sign changes of Δr·Δv) fires on a numerical-noise tangency — g touches −3×10⁻¹⁸ without crossing —
and reports a point that is not a local minimum of the distance. Verdict on my numbers:
**KILL of the `diophantine` configuration as it stands**, with every control behaving (oracle
passes all seven criteria; conjunction-sampled fails `complete`, element-sort fails `steady`).

**Bottleneck.** Board item "finding encounters without work per orbit or per element change" and
the top scaling risk (candidate work must track real encounters). The defect is one guard at one
bracket (reject a sign change whose g magnitudes sit at the float-noise floor, or verify d rises
away from the refined point); everything else the representation claimed measured as designed.

## Evidence

Machine: GitHub Actions linux, 8 vCPU (timings are order-of-magnitude only). `$R` =
`lab/results/20261006-0030-rung-r8-encounters-v3-3501`; binaries built with
`cargo build --release --manifest-path $R/{rung,truth}/Cargo.toml`; run from the repo root.

- **Belts** (r8 v2's sampler: one Python `random.Random(20261008)` stream, extended):
  `python3 $R/gen_belts.py` → 20 belts for (a), steady, three scale belts, kick belt.
- **The independent truth** (my own code, no shared path with the crate: Kepler by bracketing
  bisection, conservative advancement with a certified local-curvature bound, golden-section
  minima; coarse states carry an explicit position-error margin):
  `rung-truth $R <belt> <orbits> <out.bin> [sample phase]`, batched in `run_truth.sh`.
  (a): 18,708 encounters pooled, 6–59 s per belt. (b): the steady belt over the first 1000
  orbits as a 1-in-10 strided pair sample (rate 5.833×10⁻³ per body per orbit, 1750 hits on the
  sample). (c): n=10³ full (1982 encounters); n=10⁴ 1-in-32 (643×32 ≈ 20,576); n=10⁵ 1-in-512 (396 hits on 1.18M sampled pairs → 202,752) —
  dense belts force short certified steps, so the sampled rates carry the oracle's scale points
  (±4% statistics; the exponent criterion is ≤ 1.1).
- **Independence cross-check**: `rung xcheck $R a02 a11 narrow coorbital equalkeys hot` — the
  crate's own truth (Halley states, its own bounds) and mine agree event-for-event on all six
  belts, both directions (0 missed, 0 false). The one false report below is false against both.
- **(a) completeness and soundness** — `rung verify $R` (25 s), tolerance 10⁻³ on times:

  | config | truth | missed | false | checks/encounter |
  |---|---|---|---|---|
  | diophantine | 18708 | **0** | **1** | 1.164 |
  | conjunction-sampled | 18708 | 12391 (66.2%) | 0 | 100.3 |
  | element-sort | 18708 | 12391 (66.2%) | 0 | 10800 |
  | oracle | 18708 | 0 | 0 | 1.0 |

  The conjunction-based negatives leak exactly where the rung predicted: pairs whose synodic
  period exceeds the horizon (narrow belt: 2946/3133 missed) and Δn = 0 pairs (equalkeys:
  1419/1558 — no conjunction ever). Their false rates are 0: their checks are exact minima.
- **The one false report** — `rung false1 $R coorbital` → `false-report-coorbital.txt`: pair
  (155,218), reported t = 220.3955, d = 4.419×10⁻⁴ (< ρ = 10⁻³). The profile: g = Δr·Δv < 0 on
  [219.8, 220.88], touching −3.2×10⁻¹⁸ at t = 220.3955 (the float-noise floor; neighbours are
  ~10⁻¹⁰) and crossing transversally only at t = 220.8766, where the true minimum sits
  (d = 4.328×10⁻⁴) and both truths record it. d decreases monotonically through the "report":
  there is no local minimum at 220.40. `scan_minima`'s bracket caught a noise-level sign pair;
  Newton refined onto the terrace; d < ρ → reported. The crate's own belts never produce the
  case (no co-orbital tangency in its seeds), which is why its verify shows false = 0.
- **(b) steady** — `rung steady $R` (~20 s): method events (setups + checks) per body per orbit
  fall along 1/h over horizons 10 → 10⁵ orbits: 12.83 → 1.289 → 0.1345 → 0.0191 → 0.007526;
  against the truth rate 5.833×10⁻³ the ratio at the full 10⁵-orbit horizon is **1.290 ≤ 2.0**
  (one-time setups amortized; the checks carry the ~1.16 window margin). On the same 1000-orbit
  window the method matches the sampled truth exactly (missed 0, false 0, matched 1750/1750).
  element-sort: 1018 events per body per orbit → ratio 1.7×10⁵ (its per-bin-list swap multiplicity
  included — exact combinatorics, not simulation). conjunction-sampled: 0.425 → ratio 72.9.
- **(c) scaling** — `rung scale-dio $R` + `rung scale $R`: diophantine check work
  4450 → 42750 → 403000 at N = 10³/10⁴/10⁵ (ρ ∝ 1/N): fitted exponent **0.98 ≤ 1.1** — checks
  track real encounters, not the O(N²) candidate pairs. The candidates' footprint is real but
  ungated: per-body first-hit queries grow 1.7k → 17.5k across the decade (setup, paid once, the
  board's q-candidate-degree question). Conjunction-based configurations: exponent ≈ 2.0.
  Oracle: the measured true encounter counts (full/sampled truths above), exponent ≈ 1.0.
- **(d) kicks** — `rung kicks $R` (0.2 s), 100 kicks δa/a = 10⁻³ at t = 0: diophantine re-scans
  only the kicked body's U-range: median (pairs set up)/(kicked body's candidate count) =
  **1.0000**, other certificates recomputed = **0**. element-sort re-bins: 52 merged-neighbour
  certificates over 100 kicks (not isolated — a negative's extra failure). conjunction-sampled
  and oracle: ratio 1.0000, others 0.

`metrics.json`: `python3 $R/assemble_metrics.py`. Picture: `python3 $R/make_picture.py` —
events per body per orbit against the horizon (log-log), one series per configuration, the
truth's encounter rate as the red dashed line: the diophantine curve falls onto the truth line
as 1/h; the negatives sit 2–5 orders of magnitude above it; the oracle lies on it.

## Predictions (`predictions.md`)

Held: completeness (missed = 0 exactly), the leak range (66% pooled, inside my 10–80%),
element-sort failing steady by orders of magnitude, steady_ratio 1.2–1.5 (measured 1.29),
checks_per_encounter 1.05–1.35 (1.16), scale exponents 1.0/2.0/2.0/1.0, kick ratio 1.0 and
isolation. **Failed:** "false_fraction = 0.0" — exactly one false report, and not the
ρ-boundary knife-edge I hedged against but a g-tangency false positive (my surprise list named
the hot belt; it was the co-orbital belt). That failed prediction is the rung's result.

## What would make it wrong

The verdict rests on one event in 18,708, checked three ways: the dense distance profile
(monotone through the terrace — no local minimum at 220.40), my truth's list (minimum at
220.8766 recorded, nothing at 220.40), and the crate's own truth (identical list). The report
would have to be a true local minimum for the criterion to pass; it is not. If the law's
encounter were "any sub-ρ passage" instead of the rung's frozen "a local minimum of distance
below ρ", the report would be legitimate — the frozen text decides. The steady denominator is
a sampled, sub-horizon rate (stationarity: the method's own rate is flat across a 1000× horizon
range, and it matches the truth exactly on the 1000-orbit window).

Cost of adopting the fix: one bracket guard in `scan_minima`/`refine`, local, no representation
change. PRINCIPLES: "Certificates need independent, adversarial checks" — this rung is that,
working; "A failed expectation is not automatically a failed method: diagnose which one broke
(H0183)" — the bracket broke, not the cone, not the first-hit arithmetic, not the sections:
zero misses everywhere including co-orbital, equal-period and hot belts, 1.16 checks per
encounter, 1.29× steady state, exponent 0.98, kick isolation 0/1.0.

## What this run may have missed

The element-sort swap count is exact combinatorics of v2's per-bin lists (each co-listed pair
swaps at every conjunction), not a kinetic simulation; its per-conjunction check runs once per
distinct (pair, conjunction) with the list multiplicity counted as work. The equalkeys belt
draws a on 3 discrete values, so "identical memo keys" is stressed per-key only; no same-phase
collision was forced. The n=10⁴/10⁵ truth rates ride on strided pair samples (±4% and ±5%), adequate
for an exponent gate at 1.1 but not a precision rate measurement; the steady belt's own
completeness check covers the sampled pairs only. Cloud timings are Linux/x86 orders of
magnitude; the integrator re-measures on the M1.
