# Predictions (written before the decisive run)

Run: 20261014-1511-scout-f0a2. Falsifier: `work/screen.c` (Kepler-true conjunction scan,
float replica of the belt, a=1.5 AU SI-anchored, Dohnanyi [70 m, 470 km], horizon 1000 orbits).

Cases not tuned on, and what I expect:

- **P1 (reproduction, the checker's regime):** per-Δa Kepler-true min-misses have a heavy left
  tail (quasi-periodic revisit), so the propagated gate's deletable fraction on the Dohnanyi
  spectrum lands in [0.93, 0.99] (0b81 checker: 0.955–0.978). If it lands > 0.995 I have
  reproduced the author's broken uniform model instead.
- **P2 (the screen's share, decisive):** the propagation-free contact screen with the sound
  velocity floor v_rel ≥ v_k·P/H deletes ≥ 0.90 of what the propagated gate deletes on the same
  pairs (the yield is mostly a birth constant). If the ratio is < 0.5, the yield lives in the
  b_min tail and the screen is dead.
- **P3 (the threshold):** the one-bit body threshold D* (equal-size pairs screen-deleted) lands
  in [0.5, 5] km at H = 1000 orbits — the neighborhood of the law's own m_crit ≈ 1.35-km rock.
  N(>D*) in a 10⁹ Dohnanyi belt lands in [10⁴, 10⁷].
- **P4 (the floor is sound):** no scanned pair has any conjunction with v_rel below
  v_k·P/H·0.9 (else the one-bit screen needs a pair-level floor and P2/P3 are optimistic).
- **P5 (costs):** the propagated scan costs ≥ 100 ns/pair in C at Δa/a = 0.05, so any
  per-refresh per-pair gate on the measured 0.0175–0.087·N pairs/kick stream is ≥ 10³ cores at
  10⁹ (arithmetic, not measured); the screen's route check is ≤ 5 ns.
- **P6 (held-out, the horizon dial):** shortening the horizon 10× lowers D* by ~√10 ≈ 3.2×
  (D* ∝ √(P/H)) and raises the refresh rate 10×, so the routing work N(>D*)·rate moves by less
  than 3× either way (work ∝ H^0.25 near the optimum — nearly flat). If it moves > 10×, the
  e-driven v_rel floor, not the tangential one, binds and the dial is stronger than I think.

Controls both sides (must behave, else VOID): an all-50-m belt screen-deletes 1.000000; an
all-470-km belt screen-deletes ~0; the deflection charge 2μ/(b·v_rel) matches an RK4 two-body
integration at ratio 0.99–1.01 in the weak-deflection regime.
