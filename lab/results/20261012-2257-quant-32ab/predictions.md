# Predictions — 20261012-2257-quant-32ab

Written before the decisive runs. Premise under test (HANDOFF item 5 / gate F1, `wt/frame`):
the sweep's L8+ stutter ("the frame hits its 12 ms budget, presented time lags up to 1.6 s")
is a frame-cost problem whose named fix is lazy re-keying + the incremental deadline — i.e. the
Θ(N)-per-frame fixed tier (rekey/drain/requeue). At 48–428 bodies that tier is measured at
~15 µs/frame (762d-119f), three orders of magnitude below 12 ms, so the premise needs the 12 ms
to come from somewhere else. This run measures where it comes from, on shipped code, in the
flight regime (which no frame-cost run has measured: prior runs measured zero-event populations,
fleet openings, and view gather, never the player in flight at levels).

Setup: `frame_split` (new example, this run's patch), the sweep's exact flights (seed 1, Sparse,
1 thread, members 48, forward hold from wall second 1.0), 60 Hz `frame_to`, `Budget::unlimited`
for demand and the page's 12 ms cap for paced. Per frame: CPU µs, events; per flight: engine
`Stats` deltas (kicks/opens/boundaries/handoffs/slices/decisions; items+cost_ns by kind
planet/moon/ship/player/fleet).

- **P1 (the falsifier).** At members 48, demand mode, rtf 100, L8+: the attributed event work
  (Σ cost_ns[0..5]) owns the frame; the unattributed remainder (Σcpu − Σcost_ns: rekey, queue,
  take_due) stays under 5% of Σcpu. If the remainder owns ≥ 50%, the fixed-tier premise survives
  and this run's claim dies.
- **P2 (density).** Events per frame grow with burn level above L6 (the ship's own items
  accelerate): ev_fr_p99 at L15 ≥ 10× the coast baseline, roughly monotone in level while alive.
- **P3 (capacity, not prologue).** Demand CPU per frame scales ≈ ∝ rtf at fixed level (25/100/400),
  matching 762d-119f's "delivered = throughput ÷ event density"; a flat-in-rtf ~12 ms component
  would instead vindicate a per-frame floor.
- **P4 (per-event cost).** The player's per-item cost (us_player over it_player) grows with level
  (hyperbolic-key compiles at growing E): ≥ 2× from L0 to L15. Alternative outcome: flat
  per-item cost, density alone explains the frame — either way it is measured.
- **P5 (population).** members 400 vs 48 at the same level: total demand per frame grows < 2×
  (the O(N) tier and the player scan are small at this scale).
- **P6 (coast control).** Coast at rtf 100: p99 frame ≤ 300 µs. A coast already over 1 ms would
  mean the sweep's baseline differs from the page's idle frame and I must say so.

Held-out cases (not tuned on): rtf 25 and 400, members 400, and the levels between the calibrating
ones (I calibrate on nothing — all levels run once, one pass, no re-runs except OS noise checks).
