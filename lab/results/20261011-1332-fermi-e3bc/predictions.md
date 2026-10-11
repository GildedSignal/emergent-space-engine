# Predictions (written before the bench; run 20261011-1332-fermi-e3bc)

The decisive experiment is `crates/space/examples/fermi_budget.rs` run on this Linux/x86 box
(orders of magnitude only; the integrator re-measures on the M1). Inputs from the journal,
not tuned by me: kick cost on the plane 29 µs (H0210); 32.5 kicks/orbit unaveraged, 114× cut
by averaging (H0190 K1/K2); 0.6 core / 0.01 core per million low-orbit ships unaveraged /
averaged at ~50 µs per event (H0190 economics row); belt program 0.126 bits/body
(components-98bc); tube 16 B (law.md); jet re-anchoring ~0.05 compiles per kick (law.md,
redteam 20261006-0346-redteam-df81).

Held-out cases and expectations:

- **P1 compile cost.** `Orbit::compile` on belt/planet-range keys (periapsis 20–1000 M,
  e ≤ 0.6, B11's range) costs 3–30 µs each, median order 10⁻⁵ s. Consequence: the plane's
  29 µs kick is compile-dominated, as the taste log says (99% of kicks recompile).
- **P2 eval cost.** `Orbit::state(elapsed)` at a random phase costs 0.03–0.3 µs — at least
  100× below compile. Consequence: a jet-style kick (eval + integer delta, recompile every
  ~20 kicks) lands at ~0.1–1 µs per kick.
- **P3 kick floor.** The integer (E, L) += (ΔE, ΔL) update itself costs ≤ 2 ns. The gap
  between P3 and P2 is readout overhead; the gap between P2 and P1 is compile traffic.
- **P4 cycle bytes.** One compiled cycle (knots + crossings) costs 1–10 KB. Consequence:
  the shared cycle store fits ≤ ~10⁶ live cycles in a GB-scale budget, so it is a cache
  over dolls, never the store of a galaxy.
- **P5 memo collapse.** For a belt-like sample (p within one octave, e spread 0–0.6,
  N = 10⁵), the crate's own `memo_key()` (12 shape + 12 scale bits) collapses distinct keys
  by less than 10×: the 12+12-bit grid inside a belt's volume has ≥ 10⁶ cells, so a 10⁵
  body belt stays mostly distinct. If this holds, compile traffic does NOT amortize across
  a sparse belt's bodies; only dense formations (fleets, co-orbital clumps) share cycles.
- **P6 budget ranking (derived from journal numbers, the headline).** At 10⁹ bodies on the
  8-core M1, the terms rank: (1) ops per event — today 24–75× over budget even at real-time
  factor 1 (190–600 cores needed vs 8); (2) events per body — closed by averaging on stable
  orbits (10 cores at rtf 1, 1.25× over; with the jet ~0.2 cores, ~40× headroom); (3) memory
  bulk — programs at 0.126 bits/body are ~5 orders below 8 GB, but the 16 B tube as THE
  store is 2× over, so the tube can only be a cache; (4) bandwidth — binding only for
  O(N)-per-player-second sweeps at rtf ≥ 10 (one full sweep of a 5 GB store per
  player-second at rtf 100 needs ~500 GB/s vs 60).

What would make each wrong: P1/P2 wrong if compile is already memoized inside
`Orbit::compile` (then the plane's 29 µs is something else — the taste log says it isn't);
P5 wrong the other way if `quantize` is coarser than 12+12 effective bits over a belt's
volume. P6's ranking flips if the active fraction of a galaxy at play is ≪ 1% (then memory
scars, not events, bind first — that is H_live, measured by b-h-live, not here).
