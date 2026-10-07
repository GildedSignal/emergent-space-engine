# Predictions (written before the decisive runs; nothing below was tuned on)

Runs: `cargo run --release -p xtask -- universe --bench` (shipped code, Linux runner, 8 vCPU shared).
Knobs: `--engine-ms` (wall budget of a frame's engine advance), `--threads`, `--members`
(fleet size), `--rtf` (game seconds per wall second = the load), `--unpaced`.

## P1 — the digest is budget-, thread- and pace-invariant (the "changes when, never what" premise)

seed 1, members 48, rtf 100, seconds 12, cut at the same canonical tick:
`digest` identical across engine_ms ∈ {5, 1}, threads ∈ {1, 4}, paced and unpaced.
I expect identity. Any difference is a bug finding, not noise.

## P2 — overload degrades smoothly: an RTF dip, never a tail explosion

members 400, rtf 1000, engine_ms 5 → 2 → 1 → 0.5 (seed 1, 12 s, threads 4):
- overflow_frames becomes > 0 somewhere below ~2 ms;
- rtf_median and lowest_1pct fall smoothly toward the budget; no cliff (no run where
  the game effectively freezes: rtf_median stays > 25% of the previous rung);
- hitch counts above 16.7 ms and the worst hitch stay at the CPU-bound level:
  frame_ms hitches match frame_cpu_ms hitches (a wall hitch with no CPU hitch = a
  stall, and stalls growing as the budget shrinks would be a policy artifact of the
  budget cut, not physics).

## P3 — the wave (dense order inside the queue) is worth a factor on fleet scenes

members 400, rtf 1000, engine_ms 5, threads 1 vs 4: engine p99 (where_the_time_goes_ms)
drops by ≥ 1.5× with 4 threads. If it barely moves, the wave is not the dense order
in practice and "one engine" rests on thinner ice than the code suggests.

## P4 — held out: where overload first bites

At members 48 the default 5 ms budget never overflows at rtf 1000 (overflow_frames = 0).
At members 400 it overflows at engine_ms ≤ 2. If it overflows at members 48 already,
the fleet's kick cost is much worse than the handoff numbers suggest and the
"allocator is not yet load-bearing" reading is wrong.

## What would kill the simplification

Any of: a digest difference (P1); wall hitches that appear without CPU hitches and
grow as the budget shrinks (P2) — that would be EDF starvation under the budget cut,
i.e. least-slack is load-bearing now; or the horizon mechanism failing to hold (a
frame presenting unresolved work shows as digest drift or rtf collapse, not a dip).

## Blind spot (named before the runs)

The plane is one star system: every deadline is the player's light cone, one queue,
one silicon budget. The hard case for deadline order is heterogeneous load at region
scale — a far dense battle whose *catch-up work* (not its deadline) should outrank
near cheap work (least-laxity vs EDF), plus memory pressure where off-screen lag is
the sacrifice, not time. None of that is exercised here; a pass licenses "one queue
is the allocator" only at the plane's scale, and the region-scale question stays open.
