# Dossier — the kick resolver's floor

## Claim

The plane's kick resolver costs a median **75.6 µs per kick** while its information floor is **~42 ns**
(batched, 3-source field included) — an **idiot index of ~1,800×** — and **89% of the cost is the
rebind machinery** (the per-kick tube refit plus step re-derivation), not the physics: the field
evaluation is 4.4 µs and the drift readout 3.7 µs, so the lever is to delete the refit from the kick
path, exactly as representation.md §3 already prescribes ("a kick updates the cycle by a
multiply-add"), not to memoize it.

## Bottleneck

Board item 1 ("fewer kicks per orbit… kicks dominate the engine's cost") and the plane's own record
("kicks cost 29 µs", H0210). Expected gain: **~10²–10³× per kick** once the kick is an addition in
the state's own form; it deletes the per-kick catalogue fit, the per-kick history segment and the
per-kick `Arc` traffic (97% of kicks produce a new catalogue entry: 1,125 cycle rebinds in 1,158
samples).

## Evidence (all commands ≤ 60 s, Linux x86, 8 vCPU shared, load 1.2–2.3)

Current cost, pure resolver (readout + forces + sigma-delta + fit + remainder; scheduler,
application and view excluded), on the plane's own scene, seed 1, rtf 100, 30 s of game time
(this run's patched bench, whose diff run.sh saves, adds the `subphase` line):

```
cargo build --release -p xtask
CARGO_TARGET_DIR=… cargo run --release -p xtask -- universe --kick-bench --seconds 30 --rtf 100
# -> work/kickbench-decomposed.json (first line: subphase {read_us, field_us, kepler_us, rest_us})
```

- median **75.6 µs**/kick (`made` bodies 34.9, fleet leavers — the scalable population — 91.7),
  p99 370 µs, 1,158 samples, 0 refused; replay digest `0e02bf0f…` identical before and after the
  sub-phase instrumentation (the instrumentation only reads).
- Sub-phase medians (hot-cache lower bounds; their sum subtracted from the total leaves the rest as
  an upper bound): **readout 3.7 µs, sources+field 4.4 µs, kepler re-derive 0.26 µs, rest — the
  fit/rebind plus step machinery — 67.3 µs (89%)**.
- Memo on the same kicks: exact-shape hit **0%** (1,125 distinct shapes), quantized 12+12-bit hit
  95.5% — and the quantized key is a law change (5 October, board). Memoization cannot close this gap.

The floor, measured (`gcc -O3 -march=native work/floor.c`, batch of one kick per body on packed
16-byte state records, sigma-delta carry, u32 fixed-point 3-source field with table reciprocal +
2 Newton steps):

```
work/floor -b 4194304 -f      # 41.7 ns/kick, 64 MB working set, body-ordered (streaming)
work/floor -b 16777216        # 2.2 ns/kick, 256 MB set, add + memory only
work/floor -b 16777216 -o 1 -f  # 139–161 ns/kick in causal (random-body) order
```

So: memory traffic for the state is ~2 ns streamed (~140 ns randomly ordered); the field is the
arithmetic floor, ~14 ns per source in u32; total **~42 ns/kick** at the plane's source count.
The floor-adjacent design is measured at **~1× the floor** — that is the small version this run
built. Even the resolver's "physics-only" part (readout + field, 8.1 µs) sits ~190× above it,
because every `Scalar` op is an i128-plus-exponent checked exact op: the second stacked
representation debt, and block floating point per cell ("the virtual comma", representation.md §4)
is the sanctioned shrink for it.

## Predictions (`predictions.md`, written before the runs)

- P1 median in [5, 60] µs: **held for the plane's own bodies** (34.9), **missed for the fleet
  leavers** (91.7; I predicted one population) and the p99/median < 4 **missed** (4.9 — the leaver
  tail is heavy).
- P2 > 50% in the rebind path: **held, 89%**.
- P3 floor < 10 ns streamed / < 3 ns L2 / < 150 ns random: **held** (2.2 / 2.2–2.9 / 139, with the
  256 MB random case at 161 slightly above).
- P4 index ≥ 100×: **held** (~1,800× batched, ~500× random-order).
- P5 exact memo hit < 5%: **held** (0%).

## What would make it wrong

The sub-phase timings are hot-cache re-evaluations on the same snapshot, so `rest` is an upper
bound; if a large share of `rest` were the ext step-time Scalar conversions rather than the fit
itself, the lever shifts from "defer the fit" to "shrink the Scalar" — both are representation
debts, but they are different builds. Timing `bind()` alone inside `crates/space` would split it;
this run did not. The floor microbench is C on x86, not the plane's law: it bounds what the
mandatory work costs, not what any lawful implementation would cost. Cloud timings are
orders of magnitude only; the integrator re-measures on the M1.

## Cost of adoption, and fit with PRINCIPLES

Adoption is one builder item, not a patch: keep the state between kicks as additive integer
invariants (`ΔL = x×Δv` exactly, `ΔE = v·Δv + |Δv|²/2`, carries as today), fit the tube once per
*read* of the orbit-level form (plan tick, certificate, view gather) instead of once per kick —
reads are per frame per visible body and per boundary, kicks are 128 per radial period
(`step_log2 = 7`), so the ratio at scale is 10²–10³, and the fit stays exact (remainder carried,
no quantized key), so digests and gates survive where the memo could not. It touches
`crates/space`'s `bind` call sites, the `Binding`/history representation and the view's segments;
B12–B17 and the replay/tie digests are the acceptance.

- "The cheapest compute is compute not done" (P1): the refit is compute not needed by the kick.
- "Every quantity is kept in the form in which its change is an addition" (representation.md,
  thesis 3): the kick already is an addition; the tube is not.
- "A fix signals the wrong representation… bandaids accumulate" (P19): the memo was the bandaid;
  this is the boat.
- "Store the generator, not the generated" (P6): the tube is regenerated 97% of kicks.

## The lens (what it may have missed)

A component floor can move cost to its neighbours, and one neighbour was measured but not
redesigned: deferring the fit makes every *read* pay it, and the view reads the past through
history segments — at extreme kick-to-read ratios that still wins, but a scene where reads
outnumber kicks (a watched fleet at rtf 1) would not, and I did not measure the read side at
scale. The allocator is the other neighbour: my floor assumed epoch batching (body-ordered
streaming), which is a scheduler change the queue does not make today. And by staying inside the
plane I did not ask whether the kick *cadence* itself (128/orbit) is right — q-cadence's ground.
