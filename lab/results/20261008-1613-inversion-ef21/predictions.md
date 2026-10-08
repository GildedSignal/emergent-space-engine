# Predictions (written before the decisive run)

Attack: gold 20261006-0346-taleb-09b5's certificate "every real encounter lies within
partner rank 4 along the orbit" (phase-neighbour certificate for co-orbital groups,
adopted into the encounters design, build lens `b-coorbital-cert.md`, memo §6).

Silent assumption I invert: a co-orbital group is radially **nested** (a train on one
track), so order along the orbit changes only through encounters. A fleet with the same
mean-motion concentration but **periapsis dispersion** (spread e and ϖ — a dispersed
ring, a blockade, battle debris at a common a) has crossing orbits: encounters happen at
ellipse-crossing points between ships whose mean-longitude offset at the crossing is
Δλ* = [ϖ₁ + M(f₁*)] − [ϖ₂ + M(f₂*)] ~ O(e), i.e. rank ~ n·e/π, not ≤ 4.

## Setup (all planar, exact analytic Kepler, μ=1, a=1, n=512 bodies, T=100 orbits)
- Concentration identical across fleet scenes: σ_a/a = 1e-2 (Δn/n ≈ 1.5e-2, a fleet band;
  a belt's Δn/n ~ 0.5). Any mean-motion concentration trigger fires on all fleet scenes.
- Rank = |index difference| in the fleet sorted by mean longitude λ = ϖ + M, measured
  **at the contact time** (most favorable to a dynamic certificate that re-sorts at
  lappings) and also at t=0.
- Truth: closed-form sieve over ellipse-crossing points and mean-longitude conjunctions
  (Diophantine arrival-time coincidences), refined by fine local sampling; validated
  against an independent brute-force all-pairs time grid on a small scene (must agree).

## Scenes (not tuned beyond construction)
1. TRAIN (positive control): e=0.3, ϖ=0 all, M₀ uniform — the gold's formation shape.
2. RING (attack): e ~ U[0.2, 0.4], ϖ ~ U[0, 2π), M₀ uniform.
3. RING-MILD (held-out boundary): e ~ U[0.02, 0.06], ϖ, M₀ uniform.
4. RING-BUNCH (held-out): as RING but M₀ clustered in a 30° arc (a deployment).
5. BELT (negative control, n=256, T=20): a ~ U[0.7, 1.3], e ~ U[0, 0.4] — the
   certificate must NOT apply here; shows the rank metric separates scenes.

## Point predictions
- TRAIN: contacts 1e3–1e4 at b=1e-3; ≥ 95% within rank ≤ 4 (contact-time); median ≤ 2.
- RING: contacts 1e2–1e3 at b=1e-3; median contact-time rank 30–90; **miss at k=4 ≥ 80%**.
- RING-MILD: median rank 4–12; miss at k=4 between 30% and 75% (the e-boundary).
- RING-BUNCH: rank distribution ≈ RING (Δλ* does not depend on M₀ density); miss ≥ 80%.
- BELT: median rank > 20; miss > 60% (rank ≤ 4 is not a triviality of the metric).
- Threshold robustness: miss fractions at b=1e-2 within ±10 points of b=1e-3.
- k needed for zero RING misses: 100–300 (grows ~ n·e, so the O(n·k) certificate is
  O(n²·e) at fixed e — the concentration it was bought to fix returns).

## Kill criterion (frozen now)
KILL of "rank ≤ 4 covers co-orbital groups": RING misses ≥ 20% of true contacts at k=4
while TRAIN misses ≤ 5%. VOID if TRAIN misses > 5% (my harness mis-models the gold's
formation), or if brute-force validation disagrees with the sieve (missed contacts or
>5% distance mismatch), or contacts < 20 in RING (no statistics).
