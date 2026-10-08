# Predictions — run 20261008-1757-dynamics-2a25 (dynamics lens)

Question: what attractor does the plane's per-frame event **demand** settle onto (calendar,
battle-driven, chaotic?), what does a scripted player burn do to it (wake), and what per-frame
budget keeps the presented time on the attractor (bifurcation)? Measured on the shipped plane
(`crates/universe`, scenario `plane`, seed 7, scripted burns as in tests/plane.rs), rtf 100,
60 frames per wall second, one `advance` per frame.

Held-out cases (not tuned on; the pilot saw only 12 s of one run):

- **P1 calendar share.** In the battle-on steady state, a harmonic fit with fewer than 16
  periods explains ≥ 60% of the per-frame demand variance (line spectrum from the aligned
  block-step grid). KILL of the feedforward idea: share < 20% (the stream is effectively
  aperiodic at frame scale; RLS feedback stands).
- **P2 wake decay.** After each burn, demand excess returns inside the pre-burn band within
  ≤ 16 frames, and the total excess over baseline is ≤ 10× the direct decision count (8).
  Danger alternative: excess persisting > 100 frames or a heavy tail — the allocator must be
  wake-aware.
- **P3 no ratchet.** The post-battle attractor's mean rate is within ±20% of the pre-burn,
  battle-on baseline measured at equal battle activity. Danger: each burn permanently raises
  the rate (> +25%) — a compounding work leak a gate would have to catch.
- **P4 budget bifurcation.** With per-frame budget b, the lag (target − presented) stays
  bounded iff b ≥ roughly the p99 of demand (the bursts must be covered); for mean(demand) <
  b < p99(demand) the lag grows without bound (bursts arrive faster than any quiet-frame
  catch-up). Alternative: any b > mean(demand) suffices — the deferral catches up in quiet
  frames and budget can track the mean.
- **P5 N scaling.** Burst factor p99/p50 of demand grows with fleet members (bursts are
  many bodies sharing aligned boundaries), at least ×2 from 6 to 768 members. Alternative:
  burst factor is flat in N (bursts are single-body events, not synchrony).

Controls: shuffled series (spectrum peaks must vanish), random-tick alignment (wake must be
flat), digest identical across budgets and repeated runs (budget moves when work is done,
never what).
