# Dossier — 20261008-1757-dynamics-2a25 (dynamics lens)

**Claim.** The plane's per-frame event demand is a stable stream: the per-frame budget bifurcates
exactly at the *sustained mean* rate (below it the presentation lag diverges linearly; above it
the lag is bounded and self-healing with bit-identical outcomes), bursts of 8–15× the median need
no coverage, a player burn displaces the event calendar instead of creating work, and the
attractor rate does not ratchet — so the allocator should provision and forecast against the
mean, not the tail.

**Bottleneck.** #4, smoothness and the allocator (and the budget semantics under B15's p99).
What it deletes: provisioning and spike-shaping sized to the worst frame — the measured demand
has p99 = 13.5× the median (up to 51 events/frame at mean 3.4), yet a budget of 4 events/frame
(1.18× mean) holds rtf 100 with full recovery and the same digest as an unlimited budget. That is
an ~8× smaller reserved per-frame capacity than p99-provisioning for identical outcomes. It is an
operating-point and instrument result, not a speedup of the engine itself.

**Evidence** (plane scenario, seed 7, 48 fleet members, 1 thread, rtf 100, 6600 frames =
2.23·10⁹ ticks ≈ 2.7 h game, the 8 scripted burns of `crates/universe/tests/plane.rs`; probe:
`crates/universe/examples/stream.rs`, saved in this run's patch; analysis `work/analyze.py`,
output `work/evidence.txt`, digests `work/digests.txt`):

- **Attractor.** Demand decays from 9.5 to 3.40 events/frame as the battle winds down
  (~2500 frames), then is flat: 3.390 vs 3.397 across the last burns (+0.2%, no ratchet). The
  attractor is 79% fleet clock slices (2.69/frame); gravity's kicks are 0.39/frame.
- **Bursts.** Attractor p50 2, p99 27, max 51. Burst factor p99/p50 grows with members
  (10 at 6, 13.5 at 48, 30 at 192 — aligned schedules synchronise), and vanishes when the frame
  window aggregates 10× more (rtf 1000: burst 1.6): the clumping time is below one frame at
  rtf 100.
- **Calendar.** Top-16 harmonics explain 33% of attractor variance (shuffled control 5%): one
  fundamental family — 24.8, 12.4, 8.3, 6.2 frames (24.8 frames = 41.3 game-s) — present in both
  fleet slices and ship kicks. Real, but too small a share to carry a feedforward forecast alone.
- **Wake of a burn.** On the flat attractor (burns b3–b8), a burn produces spikes of +6…+36
  events at lags 5, 11, 17, 24 — the new step grid (the 6-frame family) — each compensated by
  quiet frames: net 30-frame excess −20…+13, inside the random-alignment control (±21, p05/p95);
  late tail +0.3…+0.5 vs control p95 0.7. The burn re-phases the calendar; it creates no work.
  (Burns b1–b2 sit inside the startup transient and are excluded; disclosed.)
- **Budget bifurcation.** Attractor mean 3.40 events/frame: b2 and b3 diverge (lag grows
  linearly, slope 0.6–0.8 frames/frame); b4 bounded (max lag 351 frames = 5.9 s at frame 871,
  then full recovery, realized rtf 103.6 — it repays debt in slack); b6 108 frames; b8 33;
  b16 2.8; b64 0. Max lag shrinks roughly as debt/(budget − mean): recovery time, not
  stability, is what the margin buys.
- **Determinism control.** Digest `9b9a5183…` identical at budgets 4, 6, 8, 16, 32, 64 and
  unlimited (twice): a budget moves when work is done, never what — measured, not just promised.

Commands (each ≤ 60 s on the lab box): `cargo build --release -p emergent-universe --example
stream`; then `…/release/examples/stream 110 100 7 48 <BUDGET> out.csv` with BUDGET 0 (unlimited,
also members 6/192, and rtf 1000) and 2,3,4,6,8,16,32,64; then `python3 analyze.py`.

**Predictions** (`predictions.md`, written before the decisive sweep). P3 no-ratchet: held
(+0.2%). P2 wake: held and sharpened — spikes last ≤ 3 frames (bound was 16), and the "total
excess" criterion was the wrong quantity: net excess is ~0 (displacement, not creation). P5 burst
growth with N: held (×3 from 6 to 192 members). P1 calendar share ≥ 60%: not held (33%, above
the 20% kill, below pass — a real calendar third, insufficient alone). P4: my danger branch is
**refuted** — mean < b < p99 does not diverge; the alternative (quiet-frame catch-up) is what
happens. Two of five pre-registered branches were wrong in the direction that favors simplicity.

**What would make it wrong.** A scene whose *sustained* demand exceeds any mean-tracking budget
(a calendar floor above the frame budget, e.g. a dense belt at 10⁶ bodies) — divergence is
linear there by construction; longer overloads near budget = mean (recovery time diverges, only
three bounded budgets measured); multithreaded popping order (measured single-threaded); I
counted events, not nanoseconds, so a per-event cost mixture that correlates with lag could move
the wall-time boundary. Single seed, single scenario, cloud Linux timings (orders of magnitude
only; the integrator re-measures on the M1).

**Cost of adopting.** None in code for the sizing rule (a comment in the allocator's budget
choice and B15's judge: gate the *lag attractor* under a mean-tracking budget, not raw frame
cost). Optionally seed `allocator::forecast`'s RLS with the calendar lines (one fundamental
family per scene) — a third of the variance for free; the contact-driven two-thirds still needs
the feedback fit.

**Fit with PRINCIPLES.** "minimize spike compute and average compute usage so that you get a
bigger simulation that runs smoothly" (OC#36): measured — spikes amortise, so average compute is
the binding constraint. "the algorithm that allocates the work to prevent those heavy tails, it's
the most important one" (CL 09-25 14:28): the tails are stable presentation debt with a repayment
law, not a stability risk. "No work for no reason" (CL 09-29): deferral does zero extra work
(digest invariance, six budgets).

**The lens.** Aggregate rates and alignments say nothing about per-body Lyapunov structure: a
chaotic contact phase could hide inside the "aperiodic two-thirds". The 2500-frame decay is a
transient I called an attractor after it flattens; a longer horizon could rebalance the battle
again. The wake of a *contact* (not a burn) and of continuous thrust is unmeasured here.
Kingman-style critical slowing at ρ→1⁻ is only bracketed (351/108/33 frames of max lag at
budget 4/6/8), not fitted.

**Artifacts.** `work/`: `main.csv`, `main2.csv`, `n6.csv`, `n192.csv`, `r1000.csv`,
`b{2,3,4,6,8,16,32,64}.csv`, `analyze.py`, `evidence.txt`, `digests.txt`, `pilot.csv`;
`n768.csv` is a partial corpse (killed at the lab's 2 GB cap; kept as the memory datum:
768 members exceed it). `r1000.csv` and `b{2,3,4,6}.csv` ran with the input-clamped probe
(as `tests/plane.rs` clamps); all other CSVs with the original — digest equality shows the clamp
changes nothing.
