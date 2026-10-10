# Predictions — second author run (written before the ladder runs)

The checker's named experiment: a contention-controlled load ladder (pinned cores, CPU-time
attribution for the gather, 300–428 bodies, ≥ 8 seeds) fixing the cliff's location and the
gather share. The crate cannot be edited, so CPU attribution comes from (a) the dashboard's own
per-frame thread-CPU metric (`frame_cpu_ms`, incl. CPU hitch counts) against wall (`frame_ms`),
and (b) per-term wall times measured under per-run-validated zero descheduling (frame CPU ≈
frame wall at p50/p99/worst on a pinned, quiet core), with (c) an unpaced cross-check and (d) a
same-core spinner as the controlled-contention mechanism probe. perf is blocked on this box
(perf_event_paranoid=4) and the binary is stripped, so no external sampler.

Cases below were **not** tuned on: every ladder point is a fresh (members, seed) pair; the
spinner condition and the unpaced variant have no stored precedent at these points.

- **P1 (record regenerates).** Pinned rerun of the author's `det_repeat` (seed 1, rtf 10,
  5 s, members 48) reproduces digest `f8b75cec…` bit for bit from the shipped binary, no code
  edits (patch empty).
- **P2 (attribution is valid).** In the quiet pinned ladder, ≥ 30/32 runs have
  |wall worst − CPU worst| < 1.5 ms: frames' interiors are unstalled, so the four per-term wall
  times are CPU times to the same accuracy. Runs that fail this are excluded and re-run.
- **P3 (the CPU cliff).** With CPU hitch counts (> 16.7 ms of thread CPU) from 8 seeds per
  point: median count is 0 up to ~345 bodies and the crossing (median ≥ 1 per 30 s run, i.e.
  ≥ 60/gameplay-hour... scale: 1 hitch per 1,800 frames ≈ 20/hr) lies inside [380, 428] bodies.
  The stored record supports the top end: mem384 (406 bodies, load 1.27) had 1 CPU hitch,
  mem768 (428 bodies, load 3.9–5.0) had 0 CPU hitches but a 23.25 ms gather wall.
- **P4 (gather is the compute-dominant term).** Gather p99 (CPU, via P2) is 0.45–0.70 of
  frame p50 CPU at **every** point, rising with N from ~3.5–5 ms (~300 bodies) to ~6–9 ms
  (428); engine p99 stays ≤ ~6 ms (budget clips at 5 ms wall); json + wire stay ≤ 2.5 ms.
- **P5 (the author's 23 ms is wall-with-stall).** Same-core spinner at 428 bodies: frame wall
  worst ≥ 2× the same-seed quiet run and gather wall max ≥ 15 ms, while frame CPU worst stays
  within ±25% of the quiet same-seed value.
- **P6 (cliff is a many-seed quantity).** At members 400 over 8 seeds, CPU hitch counts span
  min 0 to max ≥ 5 (chaotic contact-cascade timing), so single-seed sweeps misplace the cliff;
  the wall-vs-CPU split per seed stays clean regardless.

**Kill criteria for the original claim.** P4 failing (gather CPU share < 0.3, or p99 < 3 ms at
428) kills the readout-skin premise in CPU terms. CPU hitches zero on all 8 seeds at 428 kills
the "cliff near 400 in compute" reading (then only a contention cliff exists). P2 failing
broadly breaks my attribution method, and the unpaced variant becomes the only admissible
evidence.
