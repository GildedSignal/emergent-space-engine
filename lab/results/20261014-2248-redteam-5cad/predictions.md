# Predictions (written before the decisive run)

Target: representation.md, thesis point 2 — "Even chaos has invariant statistics, and by
the shadowing lemma a deterministic law with the right statistics is a true orbit of
nearby initial conditions."

Instrument: the standard map (area-preserving, mixed phase space — KAM islands + chaotic
sea + sticky layers, the universal Hamiltonian case), K = 1.2, torus [0, 2π)².
- The "law": exact float map.
- The "quantized law" (the doc's error model: one floor unit per event, never
  compounding by construction): state rounded to a grid of size Q after every step.
- The noise/shadowing test (Sauer–Yorke operational proxy): N copies with i.i.d.
  uniform ±Q/2 noise injected each step; if the pseudo-orbit is shadowable, ensemble
  deviation from the noise-free reference saturates at a bounded multiple of Q; if not,
  it grows without bound.

Cases I did NOT tune on (held out until after the sweep): the exact saturation factor
in the deep sea, the breakdown time at sticky initial conditions, the dose–response in
Q, and all dwell-tail numbers.

- **P1 (positive control, must pass):** regular (KAM) initial conditions: quantized and
  noisy orbits stay within ~10–100·Q of the reference for the whole run (bounded, no
  growth over 3 decades of time).
- **P2 (deep sea):** strongly chaotic initial conditions: noisy-orbit deviation
  saturates at ≤ ~10³·Q at Q = 10⁻³ — the doc's claim holds where the map is
  Anosov-like.
- **P3 (sticky layer):** sticky initial conditions (chaotic orbits near an island
  boundary): deviation does NOT saturate — it keeps growing decade over decade and
  reaches O(1) of the torus by ~10⁴–10⁵ steps; no bounded shadow factor exists there.
- **P4 (dwell tail — the player-visible one):** the quantized law crushes the
  dwell-time tail on sticky orbits: p99/p90 continuous dwell near the island drops by
  ≥ 10× versus true orbits from the same cells; for a tail quantized orbit that
  escapes at T_q, the majority of true orbits started in its own Q-cell still dwell
  beyond T_q (i.e. the quantized behaviour is not that of any nearby initial
  condition).
- **P5 (dose–response):** the dwell-tail damage grows with Q (present at 10⁻⁴,
  severe at 10⁻²).

Falsifier of my own attack: if P3 and P4 fail (sticky deviations saturate; tails
match), the shadowing premise survives its cheapest test and I report it as standing.
