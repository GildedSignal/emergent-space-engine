# Predictions (written before the two probes; 2026-10-10)

Probe 1 — skin invalidation under co-orbital concentration (`probe_skin.py`):
N=2,000 bodies on one orbit belt vs a phase-packed formation (same N, phase dispersion shrunk 20×),
Verlet-style skin with margin factor m ∈ {1.5, 2, 3, 5}. Setups per kick and pair-checks per kick measured.

- P1.1 Belt: setups/kick falls ~linearly with m (the 12.6× direction; amortization works where neighbour flux is low).
- P1.2 Formation: setups/kick rises ≥ 5× over belt at the same m and N, because neighbour flux through the
  skin invalidates it; the skin factor's gain degrades toward ≤ 2× at m ≥ 3. (The taleb-09b5 concentration,
  now inside the skin rather than the window tier.)
- P1.3 Cost is U-shaped in m at fixed structure: pair-checks grow ~linearly with m, so total work has a finite
  optimum; a bigger skin is not free (Ries's local-efficiency trap).
- P1.4 The fix that survives concentration is a per-phase-neighbour skin (k nearest along the orbit), not a
  metric skin: I predict phase-skin setups/kick stays within 2× of belt levels under the formation.

Probe 2 — B12 statistic: average-of-maxima vs time-mean (`probe_b12stat.py`):
Bounded process (heavy-tailed noise, no drift) vs leak (noise + jump +δ on 1% of steps),
T=100 and T=1,000 steps, 200 seeds each, classifier = slope test on the statistic.

- P2.1 At T=1,000, per-seed max slope separates leak from bounded with ≥ 2× lower misclassification rate
  than time-mean slope.
- P2.2 At T=100, time-mean misclassifies > 20% of seeds; max-stat < 10%.
- P2.3 On always-on leaks (drift every step) both statistics are perfect — the difference only exists in the
  rare-actuation regime, which is the regime B12 must catch (chaotic ships actuate rarely).
