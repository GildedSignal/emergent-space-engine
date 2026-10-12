# H_live: the memory budget as numbers (scout, run 20261012-0311-scout-6759)

**Question (one sentence).** How many bits of *unshared, per-body* distinguishing
information does a kicked belt population create per game-second, and does that
flow stay inside the budget that lets 10⁹ real bodies live in 8 GB?

## The budget

| Quantity | Value | Source |
|---|---|---|
| Total unified memory | 8 GB | M1, goal |
| Approved live-state budget | 4 GiB = 3.44e10 bits | HANDOFF (approved plan budgets) |
| Bodies | 10⁹ | goal |
| **Live distinguishing stock per body** | **≤ 34.4 bits** | the above, everything: programs + scars + indices |
| Scar stock if programs/indices take half | ~17 bits/body | assumption, stated |
| Belt orbit at a = 2.7 AU | P = 4.44 yr = 1.40e8 game-s | Kepler |
| Kick cadence | 32 kicks/orbit | H0190 (taste log) |
| Store design | population program + exact integer scars, Elias–Fano | docs/law.md §populations |
| Naive per-body store | 157 bits/body | components-98bc (taste log) |
| Bijective belt program | 0.126 bits/body | components-98bc gold |

Derived flow budget: a stock of 34.4 bits/body must survive the session; at
rtf 100 a one-hour real session advances the belt 2.6e-3 orbits (3.6e5 game-s),
at rtf 10⁶ it advances 26 orbits (3.6e9 game-s). So the deciding quantity is
bits/body/orbit (and /game-s), scaled by whatever rtf the player flies.

## PRINCIPLES ties

- Goal + P24 (memory floor is information): 34.4 bits/body is the whole live
  information budget, not a byte-count target.
- P3 (compute only surprises) / P6 (store the generator, not the generated):
  between kicks a two-body program predicts everything; only kick-induced
  deviations are information. The question is how much of that deviation is
  *shared* (absorbable into one Δ-program for the population, P33: smaller
  influences enter as aggregates) versus *per-body* (a scar).
- P13 (errors never compound): scars are exact integer deltas on the law's grid;
  the experiment counts them, floats only carry the physics.
- P1 (cheapest compute is none) / P16 (32-bit words): quanta chosen at belt
  scale (q_a = 1 km, q_e = 1e-7, q_angle = 2π/2^24), all well inside 32-bit words.
- P32 (symmetry is found, not given): a smooth trend across the belt is exactly
  the symmetry that turns 10⁵ per-body numbers into one shared program.

## The model (what the falsifier implements)

Plane-native semantics: analytic two-body program (exact, no integrator), kick
layer = the perturber's impulse over each P/32 interval, quadrature along the
program arc (Encke's trick, 1852: integrate the deviation, never the orbit).
Planar belt around a Sun; Jupiter (m/M = 9.54e-4, a = 5.2 AU, e = 0.048) as the
only kicker. Osculating elements (a, e, ω, M) before/after each kick; deltas
quantized on the grid above; zero-order entropy of quantized deltas = naive
per-body cost; entropy after removing a smooth degree-9 polynomial in a = the
per-body residual (an *upper* bound on the true per-body floor: any shared
structure I fail to model counts as residual — conservative for the budget).

## Fields that faced this structure (ranked at the end; details in dossier)

LSM-tree compaction (deltas + idle-time reabsorption = write amplification),
video P-frames with motion compensation (shared motion field + per-block
residuals; the exact shape of Δ-program + scars), Encke's method (program +
deviation integration; 19th-century compute-starved astronomy), procedural
generation with edit overlays (No Man's Sky), Elias–Fano/Roaring (already in
law.md), Hashlife memoization (board candidate), restricted three-body secular
theory (Murray & Holman 1997: when structure stays shared).
