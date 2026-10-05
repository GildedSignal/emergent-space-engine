# Predictions (written before the decisive probes)

Run 20261005-2129-m-meso-motion-15d6. Candidate C1: the encounter is ONE exact
event (the interaction leg is the pair's two-body flow, integrated exactly by
two Kepler maps over a window 2w), replacing the SyMBA substep cascade and the
per-conjunction quadrature.

Tuned on: the window multiplier (w = k·b/U) is tuned only on in-range flybys
(periapsis 2–30 planet radii, v∞ 5–15 km/s, Jupiter mass at 5.2 AU). Nothing
below is tuned.

## Held-out cases and expectations

1. **Fast+deep flyby (q_p = 1.2 r_p, v∞ = 20 km/s):** heliocentric ΔE and ΔL
   within 0.5% of the integrated truth. (The event is near-exactly the
   two-body flow; only the Sun's tide across the window errs.)
2. **Slow+distant flyby (q_p = 50 r_p, v∞ = 5 km/s):** still within 1% (the
   B13 gate), but the worst of the set — the window is longest, so the Sun's
   tide and the planet's orbital curvature during it dominate the error.
3. **Negative control (straight-line impulse, fixed planet):** fails the 1%
   gate somewhere inside the B13 range — I expect several-percent to
   tens-of-percent errors at the deep end (missing hyperbolic curvature).
4. **Repeated crossings (B12-like, 16 seeds, ≥20 Hill-edge crossings each):**
   the event law's own Jacobi drift ≤ 10⁻⁴ relative over the run, growth
   exponent ≤ 0.2; per-crossing error dominated by the Sun's tide across the
   window, so bounded/systematic, not a random walk.
5. **Held-out geometry (first conjunction on the trailing side, and encounters
   where the body passes outside vs inside the planet's orbit):** same error
   scale as the tuned leading-side cases (no geometry-dependent blow-up).
6. **The crossover b\*:** for single conjunctions sampled across b/r_H, the
   event-only relative error in Δv stays below 10⁻² out to b\*/r_H somewhere
   in **2–6**, and beyond ~10 r_H the flyby treatment is the WRONG channel
   (straight-line impulse error > 10% there; the relative path is
   shear-dominated, not a flyby) — so distant conjunctions must belong to the
   secular channel (q-secular), never to this event.
7. **Cost and sparsity:** the event costs ~2 exact Kepler propagations + one
   ternary refinement (µs in Python, table-scheduled Newton + Paeth rotation
   in the integer law); conjunctions per body per orbit are |1 − n′/n| ≈ 2–5
   on a 2.2–3.3 AU belt, versus the plane's 64 kicks per orbit. In a cold
   (Rayleigh-e, non-resonant) belt, close events (b < 3 r_H) per body per
   10³ orbits ≈ 0 — the belt's perturbation is secular; the event channel
   matters for near-planet, NEA-like, fleet and player scenes.

## What would kill C1

- Any B13-range flyby outside 1% after tuning w only in-range.
- Jacobi drift that walks (exponent > 0.2) across repeated crossings.
- The error at b ~ r_H scale not improving over the straight-line impulse
  (then "exact leg" buys nothing where it must).
- Per-event cost not far below a SyMBA cascade of equal accuracy (then it is
  a relabelling, not a deletion).
