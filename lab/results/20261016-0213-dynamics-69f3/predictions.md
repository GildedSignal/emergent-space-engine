# Predictions (written before the decisive arms; pilot = N=1000 rtf600 only)

Scene: `ES_BELT_PLAYER` (player born 2.5 AU circular, root doll), rtf 600, one sustained
prograde burn at level 0 (frames 120–600), coast after; engine budget 5.0 ms; paced 60 Hz.
Pilot at N=1000 (already seen, so not a prediction there): arrivals ≈ 14.5 held/s during burn
(mints 7.25/s, the rest reuses), answers = 1 in 16 s, S ≈ 2.97 ms/answer.

Model: the queue is a birth process with a frozen death rate. `drain_scans` answers only while
`room ≥ 2·scan_ns`; `scan_ns` is a running max that decays only through cheap answers. So once
one answer costs S > b/2 (b = engine budget), service latches off permanently: pure birth,
B(t) = λt, until the count cap (2048) forces inline answers at the player's item.

- **P1 (N=500, subcritical):** S ≈ 1.5 ms < b/2 = 2.5 ms, so the drain serves: during coast the
  backlog falls to 0, answers ≈ mints; drain is a finite avalanche (predicted drain time
  ≈ B_end·S/(b − engine work) ≈ a few seconds).
- **P2 (N=1000, the latch):** answers stay ≤ 2 for the whole 16 s (frozen after the first
  expensive answer); B grows through burn and never falls. [The pilot already showed answers=1;
  the prediction is that this holds on a fresh seed (7) too.]
- **P3 (N=2000, supercritical birth):** λ ≈ 14–15 held/s (N-independent, the arrivals are the
  player's own binding changes), B(14 s) ≈ 170–220, answers ≤ 2, and the held scans pin memory
  at ≈ 110–120 B/body each: RSS slope ≈ λ·115 B·N ≈ 3–4 MB/s → end RSS ≈ 55–75 MB.
- **P4 (the freeze threshold):** N_freeze = b/(2·s), s = S/N ≈ 3.0 µs/body → ≈ 830. Its two
  sides are N=500 (serves) and N=1000 (frozen); the number itself is a prediction, unflown
  between 500 and 1000.
- **P5 (no fence, no cap):** at these N the byte bill stays far under the fence and
  SCAN_BACKLOG=2048 is never reached in 16 s; the ruin at belt scale is taleb-51b7's, reached
  at t = 2048/λ ≈ 140 s (count-cap path) or when 2048·115 B·N exceeds RAM (memory path),
  whichever comes first — neither arm reaches either in 16 s.

Held-out: seed 7 for the N=1000 arm (P2); N=500 and N=2000 never flown before this file.
