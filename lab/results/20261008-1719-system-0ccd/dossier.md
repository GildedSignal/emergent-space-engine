# Run 20261008-1719-system-0ccd — the kick and the compile are one renewal, paid as two

## Claim

On the flying plane, every rebinding kick rebuilds its compiled cycle from scratch
(`crates/universe/src/bind.rs:226` → `Rebinding::from_state` → `Orbit::compile`, no lookup, no
increment), so the compiler — a mechanism the law says the kick should *renew*, not rebuild —
is 53–71% of every rebinding kick; wiring the law's already-adopted re-anchored jet
(docs/law.md, "Not adopted: a quantized (E,L) memo … strong-field reuse is the jet,
re-anchored") buys a measured 1.7–2.7× on the plane's kick cost, and no item in the build
queue owns it.

## Bottleneck

Board focus 1 ("kicks dominate the engine's cost") and 3 ("cheaper events"). The queue attacks
*cadence* (q-cadence, correctors killed); nothing attacks the *price of a kick*. The law
adopted the jet on 6 October from lab run 20261006-0346-redteam-df81 (error C·drift²,
re-anchor at √(floor/C), ≈0.05 compiles per kick, graded gold by one checker; the second never
ran), but the plane's rebind path never consults any memo: `Catalogue` is a slot allocator,
`bind_in` always constructs a fresh `Entry`. `crates/space/examples/certified_bank.rs` (a
compiled-cycle bank with certificates) exists unwired. Expected gain: ~2× on the kick layer
(orders of magnitude: one), deleting the per-kick compile from the hot path.

## Evidence

New read-only probe (`xtask universe --jet-probe`, patch in `work/`; it replays each distinct
pending ship kick through the pure resolver like `--kick-bench`, then times the parts; the
universe's digest is unchanged — `1a0dae74…`, identical to `--kick-bench` at the same
settings). Machine: shared Linux x86 runner, orders of magnitude only.

```
cargo build --release -p xtask                                   # 39 s cold
cargo run --release -q -p xtask -- universe --kick-bench --seconds 30 --rtf 30        # baseline
cargo run --release -q -p xtask -- universe --jet-probe --seconds 30 --rtf 30 --seed S # S in 1,2,3,7
cargo run --release -q -p xtask -- universe --jet-probe --seconds 30 --rtf 100
```

Raw JSON in `data/`. Each probe run finishes in < 2 s.

| run | rebinding kicks | carried (sub-quantum) | kick med µs | compile med µs | share | cell residence med/mean/max | ceiling |
|---|---|---|---|---|---|---|---|
| seed 1, rtf 30 | 630 | 0 | 88.9 | 63.5 | 71% | 6 / 13.6 / 78 | 2.7× |
| seed 2, rtf 30 | 415 | 0 | 60.9 | 32.8 | 54% | 6 / 8.7 / 40 | 1.7× |
| seed 3, rtf 30 | 792 | 1 | 63.5 | 33.9 | 53% | 10 / 17.5 / 126 | 1.8× |
| seed 7, rtf 30 | 770 | 1 | 73.7 | 47.8 | 65% | 7 / 16.8 / 85 | 2.3× |
| seed 1, rtf 100 | 1158 | 0 | 75.6 | 51.2 | 68% | 10 / 22.1 / 141 | 2.5× |

Supporting facts:

- Wholesale `bind` re-timed on the same states: median 70.1 µs (seed 1) ≈ compile (63.5) +
  decode/turn/residual — the decomposition is self-consistent; the rest of a kick (forces,
  readout, sigma-delta, planning) is ~20–26 µs, and one readout is 3.3–3.4 µs (the proxy for a
  jet increment).
- Ceiling = kick_med / (kick_med − compile_med + compile_med/R_mean + readout_med), i.e.
  recompile only on cell exit, increment at one readout. With the lab's own jet validity
  (~20 kicks between re-anchors) the ceiling saturates at ≈3×: the compile *share*, not the
  residence, binds. This is a ≤3× lever, not a 10× one.
- p99: kick 395 µs vs compile 152 µs. The rebind's tail (`bind` p99 348 ≈ two compiles) is the
  word-refit double compile; the jet removes most of the tail too, since a recompile happens
  1/R of the time.
- Sub-quantum kicks essentially never occur at the plane's cadence (0–1 in 415–1158): at
  1/64 of the radial period every kick crosses the velocity quantum, so the sigma-delta carry
  absorbs nothing. Cadence and the jet multiply: fewer kicks × cheaper kicks.
- Passage rebinds (flybys, no cycle) are 3% here; the jet does not apply to them.

## Predictions

`predictions.md` was written before the probe ran. All four held: compile ≥ 50% (53–71%);
carried < 20% (0–1); doll-ship cell residence ≥ 4 (median 6–10, mean 8.7–22.1); ceiling ≥ 2×
on 4 of 5 runs (seed 2 gave 1.7× — the honest low end). Held out and *not* tuned on: the seed
variation of the share (54–71%) and the residence tail (max 141).

## What would make it wrong

- The jet's increment could cost far more than one readout (the exact turn+residual compose
  with the offset is unbuilt); if it costs ≥ compile/2 the lever dies. The lab's redteam-df81
  measured the error law, not the increment's price.
- Fast-drifting bodies (14 of 45 cell runs have length 1: resonant or freshly-handed-off
  ships) never reuse; a scene dominated by them shrinks the mean toward the median and the
  ceiling toward ~1.5×.
- If `Orbit::compile` itself can be made ~10× cheaper (Astra owns the compiler's speed), the
  jet's remaining value collapses. Both levers should be priced before building.
- Behaviours: recompiling only on cell exit must keep B5 (error type), B12 (Jacobi exponent)
  and B17 (resonance) green — the cell rule is a conservative stand-in for the offset rule
  √(floor/C), which recompiles *less* often.

Cost of adopting: wire the jet in `Work::kick`'s rebind path behind a flag (the Entry carries
the derivatives the offset needs; `certified_bank.rs` already models the structure), then
`behave --law plane` B12/B13/B17 plus the universe tests, plus this probe for the realized
saving. It composes with q-cadence and needs nothing from the frozen gates.

Fit with PRINCIPLES: "the cheapest compute is compute not done" (1); "Averaging an orbit … an
orbit is stable an predictable" — the same trust in predictability is why a cycle survives
many kicks unchanged (Julien, 30 September, in law.md's kicks); "an event is a certificate
expiring" (archive/engine.md) — the kick renews the tube's formula, and today it rebuilds the
formula instead; "we only care about changes" (14): a kick that moves (E,L) by one quantum in
a stable cell changes the *formula* by almost nothing, and the plane pays a full compile to
learn that.

## The lens (system)

The unification: the kick, the compile and (in the design) the certificate are one event —
*renew the formula* — and the plane has split them into two mechanisms joined the expensive
way (perturbation layer → stateless compiler service). The same "increment, don't rebuild"
pattern is already law elsewhere: encounters re-set only the kicked body's candidates (r8 v3),
shipmem stores scars not bodies. What this lens may have missed: I measured the plane's small
scene (39 bodies, one fleet), not a belt — belts drift slower (longer residence, ceiling →
~3×) but I did not run one; the checker should run the probe on a denser scene if one exists.
I also did not price the compiler's own optimization path (Astra's owner could make the
compile cheap and delete the jet's reason); and elegant-renewal unifications hide the hard
case: **the passage and the plunge** — bodies with no cycle (flybys, `NoBoundOrbit`) recompile
by nature, and a battle-heavy or inspiral-heavy scene pays the compile per event with no
reuse. That case is exactly the queued plunge-tube build's territory; the two should be
designed together, not as strangers.

Grade suggested: **silver** — real, reproduced across seeds and rates, one named experiment
from gold (wire the jet, run the frozen gates, re-measure with this probe).
