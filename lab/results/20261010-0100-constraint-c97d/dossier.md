# Run 20261010-0100-constraint-c97d — the constraint lens

## Claim

The plane's measured constraint is the **readout path** (per-body light-cone crossings at ~13–16 µs per universe body per frame, plus JSON at ~1.4–1.9 µs per seen entry), which costs **20–160× more per body per game-second than the engine's own advance** (≈0.1 µs per member per slice); the board's #1 focus (fewer kicks per orbit) works on the 3–5 % share and cannot buy smoothness at scale, while the engine's coast path is already within sight of the goal and memory at 10⁹ is solved (104 MB).

## Bottleneck

Board focus item 1 ("fewer kicks per orbit … kicks dominate the engine's cost") and item 5 (10⁹ in 8 GB). Measured on main (Linux x86 cloud, orders of magnitude only; the integrator re-measures on the M1):

| Measurement (command below) | Number |
|---|---|
| Plane frame p50, 39 bodies, 20 s | 0.63 ms — engine 4.6 %, **view_gather 72.7 %**, view_json 15.8 %, wire 6.8 % |
| Plane frame p50, `--members 400` (428 entries in view) | 1.62 ms — engine 3 %, gather 33 % (526 µs, **flat vs 441 µs at M=4**), **json 49 % (825 µs)** |
| Gather internals (instrumented) | `avg_seen` 32→76→428 with M=4/48/400; `avg_reads` ≈45 constant; bodies 28–39 constant |
| Engine per member | 1,203 slices / 1,200 frames regardless of M; 8→39 µs per slice for 4→400 members → **0.1–2 µs per member per slice** |
| Kicks (kick-bench) | median 50 µs, leavers 367 µs, exact memo hit rate 0 % (as the 5 Oct taste log says) |
| Galaxy `--ships 1e9` | **peak RSS 104 MB** (tubes+families dedupe), render median **32 ms/frame** (18.8 ns × 1.7 M samples), compile 0.41 s |
| Gates `behave --law plane` | matches the handoff (B13 60/64, B12 miscalibrated, B14 60.1 s > 60 s); G1–G7 unanswered without `--plane-step` |

Per body per game-second: view ≈ 780–960 µs per universe body (60 fps × 13–16 µs) + ≈114 µs per seen fleet member (JSON); engine ≈ 6 µs per member. **The frame is the view; the view is the constraint for smoothness at scale.** Expected gain from attacking it: the crossing loop caps a doll at ~1,200 bodies per 16.7 ms frame and JSON caps the visible set at ~9,000 entries — a formation of 10⁵ members (the co-orbital gold case) would pay ~190 ms/frame in JSON alone. Fixing the readout deletes the per-frame root-find for most bodies (they coast on compiled cycles whose light-cone crossing is analytic per segment) — a representation change, not a tuning pass.

## Evidence

Exact commands (each ≤ 60 s except the first build):

```
cargo build --release -p xtask                      # 38 s
T=/home/glmlab/lab-target-3/release/xtask           # target dir is outside the tree
$T universe --bench --seconds 20 --unpaced                       # → bench-l0.json (M=48)
$T universe --bench --seconds 20 --unpaced --members 4           # → bench-m4.json
$T universe --bench --seconds 20 --unpaced --members 400         # → bench-m400.json
$T universe --kick-bench --seconds 20                            # → kickbench.json
$T galaxy --bench --ships 1e9 --frames 200                       # → galaxy-1e9.json (104 MB RSS, 32 ms/frame)
$T behave --law plane                                            # 99 s; gates as the handoff says
```

JSONs and the instrumented re-runs are in this folder. The instrumentation is a lab-only patch
(`crates/universe/src/constraint_lab.rs` + one call in `view.rs::gather_with` + a
`gather_measure` field in the bench report) saved by `run.sh` as the run's patch; the stock
`where_the_time_goes_ms` numbers need no patch.

Attribution inside gather [INFERENCE from measured ratios]: 45 reads ≈ 440 µs ⇒ one
`state_rate` evaluation (doll-chain walk + `ramped`/`binding_at` + cartesian readout, observe.rs
`state_rate`) costs ~10 µs; the galaxy's tube sampling reads a body in ~19 ns — a ~500×
representation gap on the same quantity (where a body is).

## Predictions

Written before the decisive runs (`predictions.md`). What happened:

1. Gather ∝ M — **wrong**: gather is flat (441→537 µs over 13× more entries); the loop runs over
   *universe bodies*, not members. JSON ∝ entries — **right** (1.9 µs/entry).
2. Fleet item cost flat with M — **wrong in an interesting way**: per-slice cost grows 8→39 µs but
   per-*member* marginal cost falls 2→0.1 µs (the slice has a fixed cost; members are cheap).
3. Held-out seeds — **ran after the dossier draft** (`inst-s2.json`, `inst-s7.json`, M=48, seeds 2 and 7):
   gather 455 µs, JSON 100 µs, engine share 3.7–4.0 %, p99 0.71–0.73 ms — same orders as seed 1. The
   M=400 rerun under the instrumented build gives p99 2.01 ms, so prediction 2's "> 2 ms" is borderline
   (1.89 ms stock, 2.01 ms instrumented), not a clean miss.
4. Galaxy 10⁹ under 5 ms — **wrong**: 32 ms median (2× over budget); memory fine at 104 MB.
5. "Engine events are the wall" — **wrong locus**: the engine is 3–5 % of the frame; the readout
   is. My own arithmetic in prediction 5 used a wrong event model (slices are per-battle per-frame,
   not per-body); the measurement corrected it.

## What would make it wrong

- If the player's doll at the goal holds only ~10²–10³ bodies and fleets in view stay ≤ ~10³
  entries, the view fits the budget and the constraint moves back to the engine's event path
  (encounter storms, 50 µs/kick) — the board's candidate-degree risk. The co-orbital gold
  (10⁶-ship formations) says fleets in view will not stay small.
- If the browser, not the Rust side, dominates the real frame (this bench measures engine + gather
  + JSON + wire, no browser), the JSON share would shrink but the gather share would grow.
- Linux/x86 vs M1: orders of magnitude only; shares (not absolute times) are the claim.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt as code (the patch is a measure, deleted with the run). The design consequence:
the readout must become lazy and analytic — cross a compiled cycle's segment against the light
cone in closed form instead of root-finding per frame, bin what the frame's pixels cannot
distinguish, and reuse the galaxy's tube sampling for zoomed-out views. That is PRINCIPLES 3
("Nothing is evolved that can be derived when looked at (clocks, redshift, views)") applied to the
*derivation itself*, and 32 ("under the right representation many symmetries can appear"): the
crossing on a conic segment is where the math becomes trivial. It also honours 12 (p95/99 rule the
frame): the p99 is decided by the view today.

Goldratt read on the current plan: "an hour lost at the bottleneck is an hour lost for the whole
system; an hour saved elsewhere is a mirage." The kick-cadence work is real (it bounds
encounter-storm cost) but it is not the frame's constraint until the readout is fixed; the
constraint moves to encounter storms *after* the readout is lazy.

## The lens

The constraint lens sees throughput, not correctness: it underweights the gates (B12's redesign,
B13's marginal misses) and the GR behaviours that must be perfect (PRINCIPLES 30). It also trusts
the bench's part-shares; a shared-harness bias (the memo lesson) would hide inside `dash`. The
held-out misses above are reported as they happened.
