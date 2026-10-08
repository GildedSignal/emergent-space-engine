# Dossier — the kick is compile-bound: 63% of its ~97 µs is a fresh Darwin cycle nobody needs

Run: 20261008-0234-spacex-0083, lens: SpaceX. Linux x86 cloud box (8 vCPU, load ~1.5–1.8,
no other run active); orders of magnitude only, per the lab rule.

## Claim (one sentence)

On the shipped plane, one kick costs ~97 µs median, and 63% of it is the fresh cycle/passage
compile inside the rebind (78% is the rebind itself; the forces — the actual physics — are 9%),
while rebinding the body's previous compiled shape through `Orbit::from_shape` costs 0.46 µs
(133× less than the compile), and every body stays inside one 12+12-bit quantized (E,L) cell for
its whole sampled life (0 cell changes in 663 kicks) even though the exact shape key changes on
98.5% of kicks — so the jet (law.md's designed fix, unbuilt) is worth a measured ~4.4× per kick,
and trivially reusing the old shape without derivative offsets is worth almost nothing (1.5% of
kicks), which kills the cheap version of the jet and prices the real one.

## Bottleneck

Board focus 1 ("fewer kicks per orbit at the same behaviour: kicks dominate the engine's cost")
and bottleneck 3 ("cheaper events"). Six runs bought nothing on cadence frontiers
(correctors/higher-order splits) and q-cadence showed the frontier is steep; nobody had
decomposed the kick itself on the shipped code. The idiot index here: a kick rebuilds a band
table whose quantized content changes by less than one part in 4096 per kick (measured: MemoCode
cells never change in-window) — 61 µs of quadrature per kick against a 0.46 µs reuse path that
already exists in the crate. Expected gain: ~4.4× per kick engine-wide (kicks are the engine's
unit of work), deleting ~653 fresh compiles and their `Entry`/knots allocations per 663 kicks.

## Evidence

All commands ≤ 60 s, from the repo root, after `git apply
lab/results/20261008-0234-spacex-0083/work/patch.diff` (adds `xtask universe --jet-bench` and
exposes `Orbit::from_shape`/`Orbit::shape_arc`; no behaviour change — visibility and one
accessor only), then `cargo build --release -p xtask`:

- `target/release/xtask universe --jet-bench --rtf 100 --seconds 10` → `jet-r1.json`,
  `jet-r2.json` in this folder (two runs, both complete). Raw JSONs are the record.
- Cross-check with the shipped bench (no patch needed): `xtask universe --kick-bench --rtf 100
  --seconds 10` → kick_us_all median 97.4 µs; my `full` column: 97.2 / 96.3 µs. Same scene,
  same digest `13cfe88b…` in all three.

Medians over 682 distinct pending ship kicks (deterministic 60 Hz plane snapshots, seed 1):

| part | µs | share of kick |
|---|---|---|
| full kick (`step::process`) | 97.2 | 100% |
| rebind (`bind`: fit + compile + decode + residual) | 75.9 | 78% |
| — fresh compile (`Orbit::compile`/`Passage::compile`) | 61.3 | 63% |
| — fit + decode + residual rest | 9.1 | 9% |
| forces (secondaries + tide + acceleration) | 8.6 | 9% |
| readout (exact integer state) | 3.7 | 4% |
| jet reuse (`Orbit::from_shape`, previous shape) | 0.46 | 0.5% |

Sanity: parts sum to 3.7+8.6+75.9 = 88 µs = 91% of the whole (the rest is quantize, apply, plan);
two reruns agree within 1%; the universe digest is identical across runs and equal to the
shipped bench's (the bench replays never feed the universe). Memo drift: 45 bodies, 663 cycle
kicks, **0** MemoCode cell changes (median 7 kicks per body sampled, p99 87); exact ShapeKey
changed on 653/663 kicks (98.5%); previous binding was a passage on 19 kicks (2.8%).

The jet's honest ceiling, from these numbers: readout 3.7 + forces 8.6 + fit/decode ~9 +
from_shape 0.46 + amortized re-anchors (61.3 µs / ~730 kicks at the 10⁻⁶ floor, the red-team
20261006-0346-redteam-df81 cadence ≈ 0.08 µs) ≈ **22 µs per kick, 4.4×**, without touching
cadence. The belt at 10⁹ pays this linearly per kick.

## Predictions

Written before the run in `predictions.md`. Held: P1 (compile ≥60%: 63%), P2 (rebind ≥70%:
78%), P3 (forces ≤15%: 8.8%), P4 (from_shape ≤10% of compile: 0.75%; jetted kick ≤35%: ~23%),
P5 (cell changes ≤20%/kick: 0.0%), P6 (sums within ±20%: 91%; reruns agree). One prediction was
wrong in an informative way: I expected trivial same-shape reuse to cover a meaningful share
(P5's "median ≥5 kicks per cell" was about the quantized cell, which indeed never changes — but
the exact ShapeKey still moves on 98.5% of kicks, so *trivial* reuse covers 1.5%). The jet
needs its derivative-offset path; without offsets it is worthless. That is the run's sharpest
result and it was not tuned for.

## What would make it wrong

- The replayed parts run after `step::process` on the same snapshot, cache-warm for the body;
  if compile cost were dominated by cold-cache effects the shares could shift (medians over 682
  samples on a quiet box make this unlikely, and the shipped bench's independent full-kick
  number matches).
- The 4.4× is a ceiling computed from the red-team's 730-kick re-anchor cadence, not from a
  built jet; the jet's offset arithmetic (additions on stored ∂/∂E, ∂/∂L tables) is unbuilt and
  unpriced, and `fit_rest` (9 µs) was kept whole though a real jet would not need all of it —
  both make the estimate conservative in opposite directions.
- Linux/x86 cloud: shares are robust, absolute µs are not (the integrator re-measures on the M1).
- If kicks per orbit fall far enough (q-cadence's frontier), the per-kick lever shrinks in
  total effect — but it multiplies whatever cadence wins, at any N.

## Cost of adopting, and fit with PRINCIPLES

Adoption is the jet build the law already names ("Not adopted: … strong-field reuse is the jet
(exact offset plus stored derivatives), re-anchored"): store per body its last exactly-compiled
shape plus the offset accumulators; on a kick, run the fit, correct the read tables by the
stored derivatives, re-anchor (full compile) when the accumulated offset reaches √(floor/C);
passages keep their compile (2.8% of kicks) or get their own jet later. Cost: one builder step
in `crates/space` + `crates/universe`'s rebind, judged by the existing gates (B5 error type must
stay ≤10⁻⁶-floor-bounded, B8 determinism, B9 cost per orbit). PRINCIPLES: "The cheapest compute
is compute not done" (1); "Cost follows change and entropy. Nothing is evolved that can be
derived when looked at" (3) — the band table is derived look-at-able structure being
re-integrated per kick; "a fix signals the wrong representation" (19) — the compile-per-kick is
the wrong representation of a slowly-drifting orbit, and the jet is the representation change,
not a bandaid.

## The lens (what SpaceX here may have missed)

This lens prices and deletes; it did not check whether the jet's derivative offsets keep B12's
Jacobi behaviour across handoffs (a correctness question, not a cost one), and it treated the
red-team's 730-kick cadence as given instead of re-deriving it on this scene (measurable: run
the offset error against exact rebinds — the natural next run). It also did not profile the
view (67% of frame wall time on this scene), which b-readout-cost owns.
