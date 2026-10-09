# Run 20261009-2212-constraint-2380 — lens: the constraint

## Claim

On today's plane the frame's constraint is not the engine but the synchronous view gather: one light-cone readout costs a stable ~10.5 µs, the gather is O(live bodies) per frame with no budget while the engine is budgeted and deferrable, and at ~1,600 live bodies the gather alone consumes the whole 16.7 ms frame — so the plane violates its own foundation 7 ("nothing takes an unbounded synchronous claim on the frame, … or a gather") at a scale the `--members 400` clamp hides.

## Bottleneck

The board's focus list is engine-only (kicks, changeover, encounters, memory). Measured on the whole plane (`universe --bench`), the frame's compute splits: **gather 56–78 %, engine 4–22 %, json+wire the rest** — at every scale and seed tried (28–428 bodies, rtf 1–100). The gather is the one part with no budget, no LOD and no culling; it is also the part the board does not name. Expected gain from putting it on the list: the view path currently caps live visible bodies at ~1,600 (10⁵–10⁹ is the goal), and deleting per-frame re-derivation for emitters whose image did not change is the same "compute only surprises" lever the engine already uses — order 10×+ on the frame path at belt scale.

## Evidence

Machine: the lab's Linux runner, 8 vCPU, load 0.6–2.5 during the window (recorded per run in the JSONs' `uptime_before/after`). All commands ≤ 60 s. Binary: `cargo build --release -p xtask`, then `~/lab-target-2/release/xtask` (shared target dir).

| run (seed, rtf, members) | bodies | gather p50 | engine p50 | µs/readout | readouts/body | overflow frames |
|---|---|---|---|---|---|---|
| 7, 1, 48 | 28 | 2.31 ms* | 0.14 ms* | — | — | 0 |
| 7, 100, 48 | 70 | 0.81 ms | 0.12 ms | 10.9 | 0.84 | 2/900 |
| 7, 100, 4 | 32 | 0.55 ms | 0.04 ms | 10.6 | 1.3 | 0 |
| 7, 100, 400 | 405 | 3.18 ms | 0.88 ms | 10.4 | 0.67 | 171/720 |
| 3, 100, 400 (held out) | 428 | 2.75 ms | 0.28 ms | 11.2 | 0.54 | 94/720 |
| 3, 1, 48 (held out) | 28 | 0.47 ms | 0.03 ms | 9.6 | 1.57 | 0 |

\* the two starred numbers are the first runs, paced on an idle machine; see the trap below. All other rows: load ~2.5 or unpaced.

Raw JSONs sit next to this dossier (`bench-*`, `prof-*`, `heldout-*`, `kickbench-seed7.json`, `behave-plane.txt`). Reproduce with:

    cargo build --release -p xtask
    ~/lab-target-2/release/xtask universe --bench --seed 7 --seconds 12 --rtf 100 --members 400
    ~/lab-target-2/release/xtask universe --kick-bench --seed 7 --seconds 20

The per-part gather profile (`gather_profile_last`: player/bodies/fleets ns, readouts) needs this run's `work/patch.diff` (`git apply` it first); everything else is main. The patch is pure instrumentation: digests matched the unpatched binary on every rerun (m4, m400, m48-15s).

Findings behind the table:

1. **The atom.** The bodies loop is the gather (fleets loop 4–20 µs; player reads 24–50 µs). One readout — `state_rate`, the doll-chain ramped tube readout plus clock rate — costs 9.6–11.2 µs, stable across seeds and scales. The gather cache already achieves ~1 readout per live emitter (H0212's relativistic cache works); the cost is the readout itself, not the search.
2. **The scaling law.** gather ≈ readouts × 10.5 µs ≈ live_bodies × 10.5 µs per frame at 60 Hz. Break-even with the 16.7 ms frame: ~1,600 live visible bodies; a belt (10⁵) would need 1.05 s/frame. The engine, in contrast, is bounded by its 5 ms budget: at 405 bodies 24 % of frames overflow and the *real-time factor* degrades (lowest 1 % = 0), but no hitch ever crosses 16.7 ms — smoothness survives by design, time-compression pays. The view has no such valve: it is a synchronous per-frame claim that grows with N until the frame dies.
3. **Kick resolver (context).** `--kick-bench`: median 43 µs per distinct kick, p99 77 µs — the board's "kicks dominate the engine's cost" is true *inside* the engine (fleet item 29–46 µs, ship 74–200 µs, player up to 2.2 ms/item with the doll-wide neighbourhood read), but the engine is not the frame's constraint at any scale measured.
4. **A timing trap for every lab run (the * starred rows).** The same binary, seed and digest measured gather p50 3.31 ms and engine p50 0.29 ms when paced at 60 Hz on an idle machine (load 0.6), and 0.74–0.81 ms / 0.12 ms under concurrent load (2.5) or unpaced — a ~4× swing from DVFS wake/idle cores on the shared runner, not compute. The `frame_cpu_ms ≈ frame_ms` note in the dashboard does not catch it. Any lab number taken paced-on-idle here inflates per-frame compute; the M1's failure mode (hot throttle) is the opposite direction. Cloud timings: orders of magnitude only — this is now measured, not assumed.

## Predictions

`predictions.md` was written before the held-out runs. Outcome: the atom held (11.2 and 9.6 µs, predicted 9–13), gather-share-as-largest-part held (0.71 at rtf 1, predicted > 0.5), engine-overflow ≥ 10 % with zero hitches held (13 %). Miss: readouts/body on seed 3 came in 0.54 against a predicted 0.8–1.3 band (more dead bodies and light-cone geometry than the band allowed); the gather total still matched readouts × atom within 6 %. The 1,600-body break-even is an extrapolation, not a run — `--members` clamps at 400 and the 60 s limit kept me from scripting a bigger doll.

## What would make it wrong

- If the belt/population scope renders through aggregates and never materialises visible bodies, the O(N) gather never meets its break-even; but foundation 5 ("observation is a pure function of the state") plus "every body real" still makes the *decision* of what the player sees O(candidates), so the culling question survives in another form.
- If the M1's readout is materially cheaper than 10.5 µs (different CPU, hot core), the break-even moves but the asymmetry (unbudgeted view vs budgeted engine) stands — it is structural, not a constant.
- The 4× idle-DVFS swing is x86-runner-specific; the integrator should re-measure the starred rows' conditions on the M1 before believing any absolute gather millisecond.

## Cost of adoption, fit

Nothing to merge: this run adds a measured bottleneck and a trap to the board. The next run it names: make the gather bounded the way foundation 7 already demands — cull before the light cone (doll-level spatial/brightness LOD, "the view is an instrument", PRINCIPLES 28) and make the gather incremental (re-derive only emitters whose crossing or image changed — "Nothing is evolved that can be derived when looked at… redshift and co are not derived but emergent", PRINCIPLES 3, applied to the view layer for the first time). Fit: "Compute only surprises" is the whole finding; the view currently computes everything every frame.

## The lens

The constraint lens made me measure the whole frame before the engine, which is what surfaced the view; what it may have made me miss: the physics gates (I ran `behave` once, badly, and moved on), and the gather's *correctness* (aberration, shift, retardation) which I took as given — a cheaper gather that subtly changes what the player sees would be a law change, not an optimization (the 5 October memo lesson, in the view's mirror).
