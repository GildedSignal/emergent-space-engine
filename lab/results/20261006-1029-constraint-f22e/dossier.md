# Dossier — 20261006-1029-constraint-f22e (lens: the constraint)

## Claim

The plane's frame constraint — at every measured operating point, and the first wall as
scenes grow — is the unbudgeted O(all bodies) view path (gather + serialise + wire,
56–93% of every frame), not the engine (6–30%, budgeted); the per-emitter Newton cache
the current fix targets is already near-perfect (≈1.1 readouts/body), so the remaining
lever is bounding the view loop itself (a perceptual LOD under the same budget
discipline the engine already has), which the frame needs before ~2,000 bodies and
which no frozen gate can see (B10 "cost against n" is not implemented).

## Bottleneck

The handoff's plane bottleneck list, item 2: "the view gather is 83% of a light frame;
cache per emitter" (a Sonnet job). Measured on main: the cache has landed
(`gather_cached`) and works — readouts ≈ 1.1 per body per frame — yet the gather is
still 56–61% of the frame and the whole view path (gather + view_json + wire) is
72–93%. The cost is not crossing quality; it is the loop's shape: `for i in
0..u.n_bodies()` (crates/universe/src/view.rs:294) plus all active fleet members
(view.rs:343), serial, every frame, unbudgeted — the one part of the frame that
violates plane.md foundation 7 ("nothing takes an unbounded synchronous claim on the
frame"; only the engine got the budget). Expected gain of bounding it to what is drawn
(O(K), K set by the player's differentiation floor): 10–100× on the view term at
10³–10⁴ bodies, and it deletes the json/wire scaling with it (they serialise every
seen emitter every frame). It does not touch the billion-scale view (the galaxy/
minimap instrument owns that); it unblocks the plane's own scope — battles of
thousands in one frame.

## Evidence

All on this shared Linux/x86 box (8 vCPU; load 1.0–1.4 during runs; orders of
magnitude only — the integrator re-measures on the M1). Raw JSON in `work/`.
Machine noise is real: the same rtf-1 scene measured frame p50 2.33 ms under load and
0.54 ms quiet (4×); the *shares* were stable (gather 60±5%), so the claims below rest
on shares and code shape, not absolute ms.

Frame composition, paced 60 Hz (shares of frame time):

| run (all `xtask universe --bench …`) | bodies | seen | frame p50/p99 ms | gather | json+wire | engine |
|---|---|---|---|---|---|---|
| `--seconds 30` (loaded) | 39 | — | 2.33 / 3.73 | **65.2%** | 28.1% | 6.7% |
| `--seconds 20` (quiet) | 39 | 76 | 0.54 / 0.80 | **60.5%** | 30.3% | 9.2% |
| `--rtf 100 --seconds 20` (loaded) | 76 | 59 | 3.59 / 9.80 | **60.6%** | 15.2% | 24.2% |
| `--rtf 100 --seconds 20` (quiet) | 76 | 59 | 0.90 / 2.46 | **58.5%** | 16.1% | 25.3% |
| `--rtf 100 --members 96` | 124 | 87 | 1.36 / 5.00 | **55.7%** | 14.7% | 29.6% |
| `--rtf 100 --members 512` | 428 | 260 | 3.84 / 10.39 | **56.8%** | 14.7% | 28.9% |

Linearity of the gather in bodies (quiet runs, rtf 100): 0.61 ms @ 76 → 0.92 @ 124 →
2.69 @ 428 bodies = **6.3–8.1 µs per body per frame, constant** — the O(N) read of the
code, measured. `view_units` (my instrumentation, saved as this run's patch):
readouts_median 44 @ 39 bodies (≈1.1/body), 64 @ 76, 90 @ 124, 255 @ 428 — the
crossing cache is near-perfect at every rtf measured, so caching is a spent lever.

The frame fills near a few thousand bodies: at 428 bodies (260 emitters serialised
each frame) frame p99 is 10.4 ms of the 16.7 ms budget, the gather alone is 2.7 ms,
and the engine — the budgeted part — is at its cap (engine p99 5.36 ms > 5.0 ms
budget, 133/1200 overflow frames, rtf lowest-1% 0.0). Linear extrapolation of the
measured per-body costs: the 16.7 ms frame is gone near ~2,000 bodies, the view path
the largest term at every step.

Engine unit costs on this box (unchanged from the handoff's picture, re-measured):
`xtask universe --kick-bench`: distinct-kick median **44.6 µs** (p99 65), leaver
kicks **365 µs (8× worse)**, exact memo hit rate 0.0% (agrees with the 5 October
correction), no refusals. Events/s: 61 @ rtf 1, 330 @ rtf 100 — the engine's cost
follows change, as designed; the view's does not (it pays per body per frame
regardless of change — the inversion of PRINCIPLES #3).

Gates: `xtask behave --law plane` (91 s) — every gate FAIL, but the failure type
matters: G1–G3, G5–G7, B7, B9, B11 report 0/N "within" with worst inf/NaN, i.e.
**unanswered** (the plane refuses those judge cases), not wrong answers; the real
physics failures are the known, already-owned ones (B12 growth exponent 1.604 vs
0.2 — Sonnet redesign in flight; B13 assists worst ΔE 1.26 — adjudicated as an
oracle-domain defect; B4 capture 5/10 misclassified). **B10 "cost against n" is not
implemented** — the judge is blind to exactly the scaling this run measured; no
frozen gate guards frame work as N grows.

Reproduce (each ≤ 60 s except behave):

```sh
cargo build --release -p xtask
xtask universe --bench --seconds 20                       # frame shares, rtf 1
xtask universe --bench --rtf 100 --seconds 20             # the advertised flight mode
xtask universe --bench --rtf 100 --members 512 --seconds 20
xtask universe --kick-bench                               # 0.1 s
xtask behave --law plane                                  # 91 s
```

(The `view_units` field needs this run's patch; `run.sh` saves it. Shares and
`where_the_time_goes_ms` are on main unmodified.)

## Predictions

Written before the instrumented runs in `predictions.md`. What happened:
1. Readouts/body in [1.5, 4] predicted; measured **≈1.1 at rtf 1 and ≈0.6–0.8 at the
   bigger scenes** — *better* than my range, i.e. below it. Held in the direction
   that matters for the claim (the cache is not the constraint; the loop is), but the
   number itself missed low: the slope-guess memo is even better than I guessed.
2. Crossing-vs-member cost split (≥10×): not isolated (would need per-emitter
   instrumentation); the linear 6–8 µs/body across scenes carries the claim without
   it. Unverified.
3. json ~linear in seen emitters at µs/emitter: held (1.5–1.8 µs/emitter quiet; ~4
   under load; the members-4096 run had json as the largest part, 46%).
4. Engine under budget at rtf ≤ 100: held on a quiet box (p99 1.6–3.1 ms); **under
   load or past ~400 bodies it does not** (engine p99 5.36 ms, 133 overflow frames) —
   the honest statement is: the engine budget binds at rtf ≥ 100 from ~400 bodies up,
   alongside the view; the view binds at every scale from 39 bodies up.

## What would make it wrong

- If the M1's gather constant is far smaller (different core, different malloc), the
  absolute saturation point moves; the shares and the O(N) code shape do not depend
  on the box. The integrator re-measures.
- If the view at the plane's real scope is supposed to show every emitter with no
  floor (Julien's immersion), then the LOD exploit is wrong-headed and the fix must
  be raw speed (the crossing is already ~1 readout; the loop would need
  parallelism/gather-by-doll). That is a design decision, not a measurement; my claim
  assumes PRINCIPLES' own floor ("the floor is what the player can differentiate").
- If the plane's battles never exceed a few hundred bodies before the population
  programs (shipmem) replace per-body storage, the saturation point is never reached
  on this path; the O(N) finding then only orders the *next* plane job, it does not
  gate the goal. The billion-scale view is a different instrument (galaxy/minimap)
  and is not judged here.

## Cost of adopting

One pass in `crates/universe/view.rs` + `xtask/src/universe/session.rs`: order the
gather near-to-far (or by last frame's angular size), spend a view budget like the
engine's, aggregate emitters below the differentiation floor into one summed
luminosity per doll, and serialise only what changed. No law change, no digest change
(the view is a pure read; plane.md foundation 5), no gate change — though B10, already
written but not implemented, is the natural place to judge "frame work at N" once
frozen properly.

## Fit with PRINCIPLES

- #3: "Nothing is evolved that can be derived when looked at (clocks, redshift,
  views)" — the view re-derives every emitter every frame; only what changed needs
  computing.
- #1: "The cheapest compute is compute not done. Delete before optimizing" — below
  the player's floor, the emitter is deleted from the frame, not made faster.
- #12: "i care about the p95/99 results i want the game to be smooth" — the gather is
  the largest term of the p50 *and* the p99 at every scale measured.
- #17: "the best part is no part."

## The lens

The constraint lens reads the frame as it is run and risks optimizing a part that
should be deleted: at billion scale the per-emitter gather may be the wrong part
entirely ("the zoom level is the minimap"), and this run says nothing about that
instrument. It also under-weights correctness constraints: the unanswered gates
(G1–G6, B7, B9, B11) and B12's exponent are the motion law v2's food and already
queued; a throughput lens can be tempted to call them noise. And its unit, the frame
of the plane, is one star system — the goal's frame at galaxy scale has a second doll
level the plane does not exercise yet.
