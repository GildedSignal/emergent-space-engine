# Predictions (written before the decisive grid; 2026-10-07 03:47 UTC)

Question: where does the plane's smooth 100× break, which stage crosses first, and is the
knee throughput-bound (cost ∝ ticks × members) or tail-bound (a latency blow-up the budget hides)?

Baseline measured already (members 48, rtf 100, 10 s, unpaced, seed 1, 1 thread):
engine p50 0.052 ms / p99 1.66 ms, view_gather p50 0.76 ms, frame p50 ≈ 0.95 ms, 3 overflow frames.

The decisive grid (all runs after this file): members sweep at rtf 100 (budget 5 ms),
rtf sweep at members 48, a true-cost sweep with `--engine-ms 500`, a paced run at the knee,
and seeds 2, 3 at the knee. All `xtask universe --bench`, ≤ 60 s each.

Held-out predictions (not tuned on):

- **P1 (stage order):** the engine advance binds first. At the knee its p99 pins at the
  5 ms budget and overflow frames climb, while view_gather p99 is still < 5 ms.
- **P2 (knee is throughput-bound, not tail-bound):** the knee shows as rtf_median falling
  with overflow frames climbing, while unpaced frame_ms p99.9 stays < 20 ms (the budget
  defers work rather than blowing the frame). No 50 ms hitches appear anywhere in the grid.
- **P3 (scaling law):** true per-frame engine cost (engine-ms 500) grows ∝ members^1 below
  ~3×10⁴ members and the knee members × rtf product is roughly constant (within 2×) across
  the rtf sweep — cost ∝ ticks × members, per-event ns flat. If instead the knee product
  falls ≥ 3× as rtf rises, per-tick overheads dominate and the constant-slope story is wrong.
- **P4 (the player order is cheap):** frames inside a burn window (nominal frame n with
  n % 240 < 20) cost ≤ 1.5× the coast frames' engine p99 at the same members; the fleet,
  not the decision, is the market.
- **P5 (capacity number):** at rtf 100, budget 5 ms, 1 thread, the plane holds
  rtf_median ≥ 0.95 × 100 up to ~10³ members and the knee (rtf_median < 0.9 × target)
  lands between 10³ and 10⁵ members. (Fermi: 0.23 ms mean engine at 48 members × linear.)

What would make each wrong, in advance: P1 fails if the view gather (also member-scaled)
crosses first; P2 fails if the budget overflows into 33/50 ms hitches; P3 fails if the
cost exponent is > 1.2 (per-event cost grows with N: cache or queue re-heapification);
P4 fails if burn frames spike ≥ 1.5× coast p99; P5 fails outside [10³, 10⁵].
