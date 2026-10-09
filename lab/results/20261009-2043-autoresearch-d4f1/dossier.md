# Dossier — 20261009-2043-autoresearch-d4f1

## Claim

On the plane's kick resolver, **the orbit-shape compile (`Orbit::compile`) is the kick**: 57–85% of the rebinding and roughly half to two-thirds of all resolver compute per kick (65 µs of ≈ 97 µs mean, seed 1), while the exact root search everyone's certificates guard (`fit_key` + `root_witness`) is 4–12% and the resolver's whole front half (readout, secondaries, forces, sigma-delta) is under 19% — so only two levers can move kick cost at all: the shape memo (already Sonnet's) and the compile's heavy tail.

## Bottleneck

Board #1: "kicks dominate the engine's cost; fewer kicks per orbit at the same behaviour."
This run does not reduce it; it locates it, at ns-resolution, inside the resolver that the
plane actually runs (`xtask universe --kick-bench`, the pure resolver on the plane's own
deterministic scene). Expected gain for whoever owns the next step: the front half caps
micro-optimization at ≈ 1.2× (measured ≤ 19% across three seeds) — the same ceiling
shape the integrator found for deferred encounter setup (1.1–1.2×, 6 Oct); the compile tail
is the only ≥ 10× surface left inside the resolver.

## Evidence

Machine: the lab's Linux runner (8 vCPU i7-4790, shared with the window's other runs;
`machine_before/after` recorded inside each JSON; Linux/x86 ⇒ orders of magnitude only).
Commands (each ≤ 60 s; deterministic, same digest every repeat):

```
cargo build --release -p xtask
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 55 --seed 1   # tuned on
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 55 --seed 2   # held out
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 55 --seed 3   # held out
```

Raw outputs with the full phase breakdown: `work/kick-bench-seed{1,2,3}.json`.
Instrumentation patch (temporary, digest-neutral): `work/instrumentation.diff`.
Loop history: `log.md`. Baseline (uninstrumented, 3 repeats): median 46/45.6/47.3 µs.

| seed | kicks | median µs | p99 µs | bind/total | compile/bind | fit_key/total | front/total |
|---|---|---|---|---|---|---|---|
| 1 (tuned) | 37 | 48.5 | 455 | 0.78 | 0.85 | 0.05 | 0.06 |
| 2 (held out) | 33 | 61.8 | 104 | 0.61 | 0.57 | 0.12 | 0.19 |
| 3 (held out) | 32 | 45.5 | 906 | 0.83 | 0.85 | 0.04 | 0.07 |

Behaviour invariants, all three seeds: `refused = 0`; `replay_digest` stable per seed across
repeats and rebuilds (seed 1: `131a39825923d748…`, identical before and after every probe edit);
`crates/space` test suite 40/40 after instrumentation (the `root_witness` restoration included).

Distribution fact that matters: the compile's 65 µs is a *mean over kicks*, but the median
kick is 48 µs total — the compile cost is concentrated in tail kicks (the p99 ≈ 440–900 µs
ones), and every shape asked for is a `Cycle` (no passages). A handful of kicks per minute
carry the whole compile budget.

## Predictions

`predictions.md` was written before the held-out runs. Held: fit_key ≤ 15% (both seeds),
refusals 0 (both), medians within 2× (both), digests stable. **Missed, reported as held-out
misses:** the strong form of prediction 1 — seed 2's compile/bind is 0.57 against a predicted
≥ 0.75, and its front half is 19% against a predicted ≤ 15%. The compile share is
scene-dependent (seed 2's orbits compile cheaper), which is exactly the falsification
condition pre-registered there; the directional claim (compile is the single largest phase,
front half never dominant) held on all three seeds.

## What would make it wrong

- The M1's timing profile could reorder phases (i128 arithmetic and allocation behave
  differently on Apple Silicon); ratios, not µs, are the claim, and the integrator re-measures.
- If Sonnet's memo lands and hits ≈ 95% as the five earlier runs suggest, the compile's
  share collapses and this breakdown describes a dead configuration — the measurement then
  still stands as the *reason* the memo is the lever (the memo deletes the compile, the
  only ≥ 10× surface).
- Kicks are replayed per 60 Hz frame on one scene; a fleet-heavy scene (leavers, the bench's
  second population, empty here) could shift the front half up (more secondaries per kick).

## Cost of adopting, and fit

Nothing to adopt in the engine — the instrumentation is a probe, not a change; the tree is
restored by `run.sh` after the patch is saved. The adoptable outputs are the numbers and the
ceiling they set (front half ≤ 1.2×). PRINCIPLES: "Measure before claiming" (#10) and
"the cheapest compute is compute not done" (#1) — this run measures which compute is left
to delete, and finds the answer is not in the resolver's arithmetic but in the repeated
compile of nearly-identical shapes: "we know we have a fish, we need to find its water."
The next rung on this thread should split `Orbit::compile`'s tail kicks (symbolic-circle
path vs `OrbitShape::bound` band structure vs `from_shape` scale work) and ask why a weak
shape with q collapsed to zero still costs hundreds of µs on the tail kicks.

## The lens

An autoresearch hill-climb needs a change-measure loop, and I stopped it after three rounds
because every bit-exact-safe change left (allocation, preallocation, arithmetic order) is
bounded under 10% — the honest local-optimum statement. The structural change that would
beat this best configuration: a compile that reuses the previous kick's knot table for the
same body as a warm start (the shape key moves by quanta per kick), made bit-exact by
carrying the difference in the residual — that is the memo's exactness question, and it is
owned by the motion law v2, not by this lens. What the lens may have missed: I measured the
resolver only as the bench replays it (pure, no allocator); the allocator's interaction with
the compile's per-kick `Arc` churn is outside the sample and outside this run.
