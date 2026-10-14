# The crash-tick search: threading the retired binding's impact tick back as a verified seed

## Claim

The kick's crash-tick bisection — 45-57% of every fired kick, rebought on every rebind — is cut
38-54% (reads and µs, bit-identically, 6/6 arms incl. held-out seeds and flying pace) by threading
the binding each rebind retires has already found its impact tick back into the search as a
predicate-verified seed; the unseedable half is exactly the hand-out's first binding, and the
float Kepler model guess is measured dead in this regime (grazing dips).

## Bottleneck

The kick at ~75-160 µs against a ~50 ns floor (board line 3; the search is its non-bind half,
45% at the battle arm and 57% at flying pace, 20261014-0450-quant-1845). This run builds the one
lever 1845 only priced (−45%/kick) and verifies it as a digest-identical change on shipped code;
it also kills the alternative (analytic guess) with a measured reason, and names the half no
seed can cover (first bindings), which is the same half the word-fix does not touch.

## Evidence

All numbers from `regen.sh` (patched tree, `ES_IMP_WARM` env-gated; counters and an ns timer in
`next_impact`; the shipped path is the env-unset arm of the same binary). Six arms, unlimited
budget, 8 game-s, digest at the canonical cut, threads 1, i7-4790-class shared runner:

| arm | searches | reads/search off → on | µs/search off → on | first-guess hit rate | digest off = on |
|---|---|---|---|---|---|
| battle m4000 s3 | 2,064 | 29.50 → 18.17 | 109.5 → 67.8 | 921/1032 = 89% | `c0ab0b4b7d0d9d10` ✓ |
| battle m1500 s3 | 190 | 29.55 → 18.97 | 115.1 → 70.3 | 79/95 = 83% | `1d1b68c1e4d56fd8` ✓ |
| battle m4000 s7 (held-out) | 2,445 | 29.50 → 18.30 | 109.1 → 66.8 | 1079/1190 = 91% | `b7e0ee56738189b6` ✓ |
| battle m1500 s11 (held-out) | 176 | 29.39 → 18.22 | 106.7 → 65.5 | 78/88 = 89% | `a2933e02221a92c5` ✓ |
| flying m400 s3 rtf 100 | 3,842 | 29.88 → 13.81 | 109.2 → 50.6 | 2448/3615 = 68% | `b1feb4bf1157db69` ✓ |
| handout m16000 s3 | 13,741 | 29.50 → 18.13 | 109.6 → 66.7 | 6151/6867 = 90% | `61b321edbee921d8` ✓ |

Mechanism, measured: per-readout cost is constant (3.6-3.9 µs — each `inside(t)` is a full tube
readout that rebuilds a cell's panel quadrature), so µs/search tracks reads/search exactly. The
seed is the retired binding's `impact` tick; a kick moves the impact tick by only a handful of
ticks — every warm miss at the battle/16k arms is within 2⁶ ticks (histogram bin 0 = the tick
itself: 1,010/1,032 at m4000/s3), so even a miss pays a nearly-closed bracket. Wall: flying
1.28 → 1.06 s (−17%, the arm where the search is the biggest kick share); battles and 16k −3-6%
(bind-dominated). Structure: every fired kick pays two searches (the kick's rebind and the next
boundary's; each rebind resets `Binding.impact`, and the `a == after` memo holds only within one
binding) — both are seeded; the "no hint" half (1,032 of 2,064 at m4000/s3; 6,874 of 13,741 at
16k; 227 of 3,842 at flying) is the hand-out's first binding, for which no predecessor tube
exists.

Negative arm (`ES_IMP_GUESS`, the passage branch's own escape pattern applied to cycles: a float
Kepler inverse from the key's periapsis and shape): **0 hits at every arm**; it survives the
bracket filter on only ~2% of searches (56/2,064, 53/2,445) and those miss by 2²⁶ ticks (half an
orbit). Reason: the members' surface crossings are grazing dips of near-circular orbits — the
crossing tick is any radius-model error divided by a near-zero radial speed. A model is not a
seed here; a tick is.

Commands (each ≤ 60 s where possible; the 16k arm is ~11 s):
```
cargo build --release -p emergent-universe --example impact_probe
$CARGO_TARGET_DIR/release/examples/impact_probe            # off
ES_IMP_WARM=1  $CARGO_TARGET_DIR/release/examples/impact_probe   # warm seed on
ES_IMP_GUESS=1 $CARGO_TARGET_DIR/release/examples/impact_probe battle   # dead model arm
```

## Predictions
`predictions.md` was written before the held-out runs (tuned on m4000/s3 only). Held: identity at
6/6; hit rate ≥ 80% on the five battle/16k arms (83-91%); the unseedable half is exactly the
first bindings; µs/search falls with reads. Missed, reported: flying pace hit rate is 68% (not
≥ 80%) with a miss tail to 2¹³ (not ≤ 2⁸) — still cheap (a miss is a narrowed bisection), and the
arm still improves most (−54% reads).

## What would make it wrong

A digest moving anywhere (the crash tick is canonical history — identity is the whole claim; the
grazing regime is also where a wrong tick would hide). Adoption on the M1 must re-measure the
readout cost (3.6 µs here is the panel-walk rebuild; the M1's number is the integrator's to
take). The seed's safety rests on the branch's monotonicity (the code's own documented invariant:
"the radius falls monotonically on the way in"); a scene where that fails would make a verified
hit still exact (the predicate checks the tick and its predecessor) but could narrow wrongly —
no such scene exists in the engine's own doc, and none of the 22,458 searches here disagreed
with the shipped bisection.

Controls: the universe suite on the patched tree is green (`cargo test --release -p
emergent-universe`: 0 failed, ~70 passed, the clock flights ignored, 470 s); the off-arm of the
probe binary is the shipped path (the patch adds counters and env-gated branches only — the
`plan_terminal` hint read is a pure lookup). The canonical xtask bench digest (be78's
`7b33d0b866149e71`) was not re-anchored: the xtask build did not finish inside the window's
300 s budget on this box, so cross-run comparability rests on the 1845 entry's own reproduction
and on this run's internal identity, not on a shared script (disclosed, not hidden in a footnote).
## Cost of adoption, fit with PRINCIPLES

~40 lines in `step.rs` (a `next_impact_hinted` taking `Option<Tick>`, the `plan_terminal` thread
of `retired.last().b.impact`, the counters deleted on adoption). No new state, no law change —
"the cheapest compute is compute not done" and the passage branch's own house pattern (guess,
verify with the exact predicate, bisection as fallback: `next_exit_with`, step.rs). Fits
"compute only surprises": the impact a binding's predecessor already found is not a surprise.
Sits orthogonally under the adoption queue's bind levers (word fix, lazy tier) — different
function, composes on the same kick.

## The lens

The Quant lens priced the readout before the bet (per-readout cost constant ⇒ reads are the
currency), demanded the negative arm (the model guess — dead, with the reason measured), and
verified the winner on data it did not choose (held-out seeds, a decade up in members, the
flying pace). What it may have missed: the search's *product* may be mostly unwanted precision
(the crash tick is re-bought every kick but consumed rarely — a bracket, not a tick, is what
plan_terminal's callers need until the crash is imminent); that is a representation question,
not a latency one, and this run only measured its shadow (the two-searches-per-kick structure
and the grazing regime that makes precision expensive).
