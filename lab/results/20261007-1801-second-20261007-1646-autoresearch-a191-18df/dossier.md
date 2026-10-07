# Dossier — 20261007-1801-second-…a191-18df (lens: second author)

## Claim

The scope-free rebuild of the silver run's deletion regenerates its record from the patch alone
(made −18…−20 %, leavers −6…−10 %, digests bit-identical, suites green), and the cadence experiment
the checker named confirms the lever it exposes: resolver work per orbit tracks rebind count with
exponent ≈ 1.05 at flat per-kick cost, so each halving of kicks per orbit buys ≈ 1.86× less kick
work and costs ≈ 4× error on the frozen assist gate (B13) — the complete tradeoff table for
`q-cadence`, whose choice stays the integrator's.

## Bottleneck

Board focus line 1, "cheaper events". The silver run's named gaps: a record that did not regenerate
(the always-on prof scopes regressed leavers +9–12 %) and the cadence rung its profile justifies.
Closing both turns the silver into an adoptable deletion plus a measured one-way-door decision.

## Evidence

Commands (each ≤ 60 s of bench time; interleaved, ratios only — shared box):

```
# the adoption artifact (saves as its own patch; applies clean to HEAD):
git apply work/scope-free.patch && cargo build --release -p xtask
# A/B against a HEAD build (bin-base/bin-opt in work/): 6 scenes × 2–3 interleaved pairs
./bin-base|bin-opt universe --kick-bench [--members N] --rtf R --seconds 20   # tuned m48/rtf100, m24, m96, rtf60, m200, rtf10
cargo test --release -p emergent-universe -p emergent-space
# cadence (needs work/cadence-flag.patch, xtask-only): l2 ∈ {7,6,5,4}
./xtask universe --kick-bench --rtf 100 --seconds 20 --step-log2 $l2
./xtask behave --law plane --plane-step {7,6,5}     # frozen gates
cargo run --release -p emergent-universe --example jacobi -- {6,5} 100
```

**Regeneration** (work/analyze.py over data/*.json): made medians −17.8…−19.6 % on 5 scenes, m24
−34.3 %; leavers −5.9…−9.7 %, m24 −24.3 %; p99 within ±8 % except rtf10's 41-sample tail (medians
only, per the checker's own rule). `replay_digest` and canonical `digest` bit-identical on all 12
pairs (tuned: `eaef383e…`/`c8ab26da…`, the author's values); `refused` 0; 18 suites, 104 passed,
0 failed, 1 ignored. The prof-free patch contains zero `prof` references — the shipped code now
regenerates the numbers.

**Cadence cost** (work/cadence.py): kicks over the same sim span 949→507→287→173 (m48), 2100→353
(m96); per-kick medians flat (made 28.6→29.9 µs over 8× coarsening); total resolver work ×0.54 /
×0.30 / ×0.16 → exponent 1.05 (m48) and 1.03 (m96) against rebind count. Kicks fall slightly
slower than 2× per doubling (0.53×) — floors (MIN_STEP, thrust caps, exit caps, handoff stubs) hold
a cadence-independent event rate up.

**Cadence price** (`behave --law plane`): B13 assists 60/64 → 41/64 → 15/64 within 1e-2, worst
2.12e-2 → 8.47e-2 → 3.39e-1 (×4.0 per halving — second order, as the shipped
`the_readout_error_falls_as_the_step_squared` pins); B13's own runtime 2.03→1.06→0.57 s mirrors
the cost ladder. The `jacobi` example (its valid range, 6/5): worst readout error ×3.5–6 per
doubling, kicks exactly halved. B7/B9/B10/B11 are unanswered by the plane adapter at every cadence
(pre-existing) and B12's exponent is the gate the taste log already calls broken — neither side of
the tradeoff rests on them.

## Predictions

`predictions.md` written before both decisive runs. Held: regeneration ranges (made −16…−21 %,
leavers −6…−11.5 % — m24 exceeded both, disclosed), digest identity, suites green, cost linearity
(exponent ≈ 1, per-kick within ±15 %), Jacobi ≈ 4× per doubling, cadence digests differ (expected).
One prediction to correct: I predicted samples would fall ≈ 2× per halving; they fall ≈ 1.9× (floor
events), which is why the work exponent (1.05) slightly exceeds the naive 1.0.

## What would make it wrong

The ratios are from a shared box (medians of interleaved pairs; absolute µs are not load-bearing —
the integrator re-measures on the M1). The cadence cost ladder measures the kick resolver only;
frame-level totals include boundary and allocator work I did not measure, which should only add a
cadence-independent term (the same floors). The behaviour price is measured on B13's flyby tolerance
and the restricted Jacobi scene, not the full gate suite — B12 is being redesigned and could move
the affordable cadence either way. Found and reported, not caused: the `jacobi` example panics at
step_log2 7/8/4 (pre-existing at HEAD, stash-verified; its default is 6).

Fit with PRINCIPLES: "The cheapest compute is compute not done. Delete before optimizing" (§1) —
the deletion removes two exact solves per kick and nothing else moves; "Compute only surprises" /
"Nothing is evolved that can be derived when looked at" (§3) — the event-time proper time is
derived once and read. The cadence table is the right question for §19: the fix for a per-kick cost
that cannot shrink bit-identically (exact keys never repeat) is not a patch inside `compile` but
fewer rebinds — the integrator's one-way door, now priced.

## The lens

A second author inherits the first's frame: per-kick micro-cost and its wall. What it cannot see:
whether the floors that keep 0.53× kicks per halving (MIN_STEP, thrust and exit caps) are themselves
deletable at the same behaviour — that is cadence-adjacent but a different experiment; and whether
the B12 redesign shifts the affordable cadence. The absolute gain of the deletion stays 1.1–1.2×
per kick — below the 10× bar on its own; the case for gold is the closed regeneration gap plus the
priced lever, not a new order of magnitude.
