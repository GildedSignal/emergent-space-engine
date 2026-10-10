# Predictions (written before the decisive runs)

Pilot (tuning) runs used seed 1, cohort 200, threads 1, 3e10 ticks: memo hit 56%, digest matched
OFF/ON, settle 3.00 s → 2.73 s. Everything below is predicted on cases not tuned on.

**P1 — Bit identity (the invariant).** With the state memo ON vs OFF (`ESPACEX_NOCACHE`), the
universe digest and the event counters are identical on every scenario: seed 7; cohort 0 (plain
plane); cohort 200; cohort 2000; threads 4. Any mismatch kills the memo's soundness argument
(a source's state at t is final before the first reader).

**P2 — Held-out seed, same structure.** Seed 7, cohort 200, threads 1: hit rate 50–65%, whole-settle
speedup from the memo 1.05–1.20× (state decodes are a minority of the event cost).

**P3 — Plain plane (no cohort).** Hit rate drops (few bodies share a step class): 20–45%; speedup
≤ 1.10×. The memo is not the plane's lever at 23 bodies.

**P4 — The player scan is the plane's bottleneck today.** At N = 213 bodies the neighbourhood scan
(a `binding_at` clone + doll test per body in the universe, per player item) takes 60–85% of the
whole settle, on both seeds. Its per-item cost grows ~linearly in N: at cohort 2000 (N ≈ 2213) the
scan's µs per player item is 8–12× the cohort-200 value. If the scan share is < 40% or does not
scale with N, this prediction is wrong and the exact check is not the bottleneck.

**P5 — Scan-free bound.** `ESPACEX_NOSCAN=1` (timing-only, outcomes differ by construction) drops
the settle of seed 7 / cohort 200 to 15–35% of the exact time — the rest of the engine (kicks,
boundaries, fleet) is what remains.

**P6 — Schedule independence with the memo.** threads 4 gives the same digest as threads 1 (memo
shards introduce no order dependence).
