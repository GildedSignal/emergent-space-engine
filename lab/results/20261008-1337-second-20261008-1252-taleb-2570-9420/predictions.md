# Predictions — written before the ladder

Second-author run. The checker's named experiment for gold: rerun the ladder inside the real
range (`--members` clamps at 400, so the ladder is 48/96/192/384 — all unclamped), ≥ 3 seeds,
bracketing the zero-stall point, then freeze the service criterion on `rtf.lowest_1pct` as a
rung gate. Binary: the shipped `xtask` the author and checker both used
(sha256 cff18e98…), record verified by regenerating the original m192 row first.

Design: `xtask universe --bench --members M --seed S --rtf 100 --seconds 30` (paced, default
engine-ms 5, threads 1) for M ∈ {48, 96, 192, 384} × S ∈ {1, 7, 13}; plus digest-invariance
pairs (engine-ms 0.5 vs 50, unpaced, 15 s) at m48/s1 and m192/s13.

Held-out predictions (not tuned on):

- **P1 (the bracket, the load-bearing one).** Per-seed `rtf.lowest_1pct`: at m48 every seed
  ≥ 1 (passes the service floor); at m96 at least 2 of 3 seeds < 1; at m192 all seeds ≤ 2 with
  median ≈ 0; at m384 all seeds ≈ 0. So the stall cliff in the real range sits between 1× and
  2× design load on this box, and the frozen 4× gate KILLs the shipped service.
- **P2 (wall saturation).** In every ladder run, `worst_hitch_ms` ≤ 20 and at most 2 frames
  over 16.7 ms: the wall criterion is not the term that breaks; p99 frame ≤ 17 ms at all loads.
- **P3 (digest invariance in the real range).** At both m48/s1 and m192/s13, engine-ms 0.5 and
  50 give the identical digest at the same cut: the budget moves work, never decisions, also
  below the clamp (the checker only verified this at the clamped 400).
- **P4 (gather).** `view_gather.share` ∈ [0.45, 0.75] in every run, with gather max < 16 ms:
  dominant and unclamped but not the term that goes over the frame either.
- **P5 (controls both sides).** Under the frozen rung below, m48 (positive) passes every
  criterion and m384 (negative) fails the stall criterion, so the rung decides (KILL), never
  VOID. Median-over-seeds is the judged statistic (lab lesson: no worst-seed-of-a-noisy-
  estimator gates).

What would falsify the run's claim: a seed where m48 stalls below 1 (the cliff would sit at
design load itself, an engine bug not a load response), or a digest that moves with engine-ms
(budget leaking into decisions), or m384 passing the stall gate (the gate toothless).

## The frozen gate (written before the runs; verdict.py-ready)

```configs
plane-1x positive
plane-4x candidate
plane-8x negative
```

```criteria
stall behaviour rtf_low1_median >= 1.0
exact type digest_invariant >= 1
```

`rtf_low1_median` = median over the 3 seeds of `rtf.lowest_1pct` (the worst 1% of frames must
still present ≥ 1× real-time progress; zero-tick frames make it 0). `digest_invariant` = 1 iff
the run's digest equals its engine-ms-50 twin's at the same cut. Service reading: "no frame
presents zero ticks at 4× design load" judged on the shipped instrument, `rtf.lowest_1pct`.
