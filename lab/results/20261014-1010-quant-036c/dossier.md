# The crash search's warm start: built, certified, half the price

**Claim.** Threading the prior tube's found impact through `rebind` as a certified guess for the
new tube's `next_impact` bisection is bit-identical everywhere measured and halves the search's
cost (151→74 µs/call at the battle arm, 110→44 at flying pace), cutting the leaver kick median
30–35% where kicks dip and leaving digests untouched — but the guess settles only 42–69% of
searches, so the end-to-end kick moves −5% (made) to −30% (leavers), roughly half of
quant-1845's −45% price.

## Bottleneck

The kick at 75–160 µs against a ~50 ns floor (~10^3.3×, the board's third gap). quant-1845
decomposed the fired kick: 46% bind, **45% one `next_impact` bisection** (115 µs ≈ 25 readouts,
bracket half an orbit wide, rebought every kick because `rebind` resets `Binding.impact`), and
priced a warm-start bracket at −45%/kick without building it. This run builds it.

## Change (env-gated `ES_IMPACT_GUESS`, default off = shipped; ~20 lines)

- `rebind` keeps the old binding's `impact` found-tick as `Work::prior_impact` before it retires
  the tube; `plan_terminal` passes it to `next_impact`.
- `next_impact` accepts `guess: Option<Tick>`: on the monotone falling branch, if `inside(g) &&
  !inside(g−1)` the search returns `g` in **two readouts** (the exact certificate
  `next_exit_with` already uses for its own guess); otherwise the guess narrows the bracket
  (`hi = g` or `lo = g`) exactly as one bisection step would. The exact predicate decides the
  answer either way, so on and off must agree bit for bit.
- Probes: prof stages `IMPACT`/`IMPACT_GUESS` (24/25) around the search, printed by
  `--kick-bench`; the `--members` xtask clamp lifted env-gated (`ES_MEMBERS`, default 400
  unchanged); `xtask --features prof` passthrough.

## Evidence (Linux/x86 shared runner, i7-4790-class, orders of magnitude only)

Arms: `universe --kick-bench` off/on, one binary (prof build), `refused 0` everywhere:

| arm (members-seed-rtf) | made med µs | leaver med µs | all p99 | search µs/call | guess share |
|---|---|---|---|---|---|
| m4000-s3-rtf1 off→on | 65.4→61.9 (−5.4%) | 531.4→373.3 (−29.7%) | 612→550 (−10%) | 150.9→73.6 (−51%) | 0.45 |
| m400-s3-rtf100 off→on | 37.3→37.0 | 201.0→129.9 (−35.4%) | 465→442 | 109.7→44.2 (−60%) | 0.69 |
| m1500-s3-rtf1 off→on | 43.3→43.0 | 375.2→372.4 | 533→519 | 115.1→74.1 (−36%) | 0.42 |
| m1500-s7-rtf1 (held-out) off→on | 43.8→42.9 | 374.7→375.3 | 617→591 | 112.9→70.5 (−38%) | 0.43 |

- **Identity:** canonical digests and kick-bench replay digests bit-identical on/off at all 8
  kick-bench arms and both `--bench` arms (m4000/s8/rtf1: `2e97e58000cb9fd7` both arms); the
  plain (no prof, no env) build reproduces the prof-off digest (`76624237fc91e312` at m1500).
- `--bench` m4000/s8/rtf1: frame p50 32.3→31.9 ms, engine p50 4.10→4.25 ms on a loaded shared
  box — no frame-level claim (within noise; the item counts move with the wall, 366 vs 1,032
  kicks, digest fixed, as the page already records for paced runs).
- Suite `ES_IMPACT_GUESS=1 cargo test --release -p emergent-universe --tests`: **26 passed,
  0 failed, 1 ignored** across all targets. (A full `cargo test` with examples failed linking
  the `nladder` example under the box's memory pressure — not a source of mine; `--tests` is
  the suite of record.)

## Predictions (predictions.md, written before the arms)

- Identity held everywhere (prediction 1) — the load-bearing one.
- Kick medians: leavers −30%/−35% at m4000/flying (inside the predicted 30–50%); made kicks
  −0.7…−5.4%, far short of it — most made kicks carry no search; the prediction wrongly
  implied the median kick pays the bisection (partial fail, disclosed).
- Hit rate ≥60% at m4000 **failed**: 0.45 (0.42–0.69 across arms). quant-1845's −45% price
  assumed near-total deletion; at rtf 1 the battle's kicks are large enough to move the crossing
  by more than a tick, so the guess degrades to bracket-narrowing.
- Held-out seed 7 behaved like seed 3 (search −38%, digests equal).

## What would make it wrong

The guess is certified by the same monotone-branch predicate the bisection uses, so a wrong
answer requires the shipped bisection's own monotonicity assumption to break (a turning orbit
entirely inside the surface, `a_turning_orbit_inside_the_star…`, is the known edge — the guess
changes nothing there: it only short-circuits or narrows on the same branch). The measured
identity is the empirical check. The hit rate is a property of the workload (kick size vs tick
of fall), so a scene with gentler kicks buys more and a battle buys less.

## Cost of adoption, fit

~20 lines in `step.rs` (env gate deletable on adoption), no new state, no standing bytes
(`Work` is per-item scratch). PRINCIPLES #1 (delete before optimizing: the search's readouts are
derived from the tube the body just had), #2 (exact = deterministic: bit-identical), #13 (errors
never compound: no error introduced at all). Composes with the bind levers (word-before-bind,
lazy tier): the bind and the search are disjoint halves of the kick. Adoption value: the kick's
non-bind half at flying pace is 57% search (quant-1845) — there the lever is worth ~−35% of the
leaver kick; in resolved battles ~−30%; the residual after it is the ~74 µs bisection tail the
misses still pay (a next rung: float-screened predicate, or an analytic crossing from the
compiled orbit's anomaly as the guess).

## The lens

Quant priced the edge before betting and demanded fresh-seed confirmation; the multiple-testing
trap is mild here (one variant, one env, digests decide). What the lens missed: an HFT warm start
carries state that the exchange holds for you — here the "previous print" is a *different tube's*
crossing, and the honest frame is a stochastic bracket quality, not a cache hit; the 42–69% share
is the workload's kick-size distribution, which I did not measure ahead of the run and only saw
in the arms.
