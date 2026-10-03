# Predictions (written before the decisive experiment)

Question: the encounter structure (`crates/encounters`, the Binet cone + Diophantine sections) pays an
eager per-pair setup (sections with numeric windows, 2.5–24 µs per candidate pair per element change,
per law.md) at every kick. Where does that cost actually land? Cases below are the ones I have NOT
tuned on; the belts are the crate's own verify sets (a, c, d) and steady-style cold belts.

Notation: a pair is *dormant at H* if its first in-window passage (integer first-hit on the built
section) lies beyond H orbits. A pair is *lazy-dormant at H* if the first passage under the cheap
cap window (no numeric refinement, a superset of the true window) lies beyond H — the sound
certificate that lets the engine skip building the section at all.

- **P1 (dormancy on cold belts).** For the σ_e = 1e-2, ρ = 1e-4 belts (set a): ≥ 99% of candidate
  pairs are dormant at H = 100 orbits, ≥ 95% at H = 1000 orbits. Rationale: the in-window fraction
  per conjunction is ~ρ/(v_rel·T) ~ 1e-5, conjunctions every few orbits, so the first hit is
  thousands of orbits out for almost everyone. If dormancy at 100 orbits is < 90%, the waste claim
  dies.
- **P2 (deletable waste).** ≥ 80% of eager setup *evals* (the numeric-window cost) sit on pairs that
  are lazy-dormant at H = 100 orbits. The interesting gap: the expensive pairs (tangencies) may be
  over-represented among the non-dormant, pulling this below the dormancy rate.
- **P3 (lazy cost).** The lazy per-pair setup (arcs + cap window + one integer first-hit) costs
  ≤ 1/3 of the eager per-pair wall time.
- **P4 (the tangency cliff).** Per-pair eager evals are right-skewed: max ≥ 50× the median, and the
  near-tangency bucket (|cone_gap|/eps_u < 0.5) carries ≥ 3× the median bucket's evals per pair —
  cost peaks exactly where the geometry grazes, including pairs that never encounter.
- **P5 (the player tail).** A body kicked to e = 0.5 at the belt's low-a end gathers ≥ 50× the
  median body's candidates; at N = 10⁴ its eager re-setup alone is ≥ 20 ms single-threaded, so
  ≥ 2 s at 10⁶ (linear extrapolation in N at fixed σ_e) — a frame-destroying stall the player can
  trigger at will. The lazy path cuts it ≥ 3× but stays O(N); only a group certificate removes the
  O(N).
- **P6 (soundness control, must hold).** On every belt tested, including the adversarial sets c
  (narrow, coorbital, equal-period-keys): zero pairs with any encounter within H = 100 orbits among
  lazy-dormant pairs, and every pair with hits has its eager first-hit ≤ H. One violation kills the
  dormancy certificate as unsound (and would itself be a finding about the cap-window superset).

Cloud container (Linux x86, 2 vCPU, shared): timings are orders of magnitude only.
