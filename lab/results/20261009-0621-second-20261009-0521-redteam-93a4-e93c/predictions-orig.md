# Predictions — redteam-93a4 (gravity-is-news, kicked sources)

Written before the decisive runs. Scene D: dominant fixed mass M=1 (G=1, c=1);
source S (m=1e-3) on a circular orbit at r_S with v_S/c = kappa; perturber J
(m=1e-3) circular at r_J = 2.17 r_S (detuned, ~3.2:1); reader T (negligible
mass) circular at r_T = R r_S. Laws compared in lockstep from identical states,
same Verlet dt = P_S/2500:

- TRUTH: everyone feels M, S, J instantaneously (Newtonian).
- NEWS-tube (the design's read): M instantaneous for all; S, J, T read every
  other massive body as "the tube as the reader's past light cone last saw it":
  interpolate the source's state (x,v,a) at t_ret, propagate along the pure-M
  Kepler drift to t_now (exact for the circle the source was born on), pull
  toward that position with magnitude Gm/|x_tube - x_reader|^2.
- NEWS-naive (control): pull toward the retarded position itself (Laplace).
- NEWS-carlip: tube plus (1/2) a(t_ret) tau^2.

Metric: Delta E_T(t) = E_T^law - E_T^truth with E_T = v^2/2 - GM/r_T
- G m_S/|x-x_S| - G m_J/|x-x_J| evaluated in each law's own instantaneous
  state; checkpoints at t = 3, 10, 30 P_T. Also delta_S = |x_S^law - x_S^truth|.

## Predictions

1. **Control (naive, kappa=0.3, R=5):** secular spiral. |Delta E_T|/E reaches
   >= 1e-2 within < 3 P_T. (Laplace; near-certain.)
2. **Free-fall floor (tube, m_SJ interaction removed: S,J only perturb T, not
   each other):** tube-now == present for circular free-fall sources, so
   |Delta E_T|/E <= 1e-9 over 30 P_T. This reproduces q-gravity-at-c's
   "news equals instantaneous for free-falling planets" in my harness.
3. **Held-out decisive case C (tube, kappa=0.3, m_S=m_J=1e-3, R=5, 30 P_T):**
   the extrapolation misses only J's kicks on S inside the light time,
   delta_x_S ~ (1/2) a_J tau^2 ~ 6e-3 (in units r_S = 11.1), direction error
   ~1.4e-4 rad. I predict |Delta E_T|/E lands in [1e-7, 1e-4] and is
   **bounded**: decade ratio (max at 30 P_T)/(max at 10 P_T) <= 2.5.
   Confidence 55%: the conjunction phase rotates (synodic), so the error is
   not phase-locked; but no symmetry forces exact cancellation either.
4. **Solar-like D (kappa=0.05, m=1e-3, R=5, ~3 P_T only, cost-limited):**
   amplitude <= 1e-8, bounded.
5. **Stronger kicks E (kappa=0.3, m=1e-2, R=10):** amplitude ~ 10x case C
   (linear in m_J; Delta E rate ~ m_S m_J), still bounded.
6. **Carlip fix F (C + (1/2) a tau^2):** amplitude >= 10x below C. If instead
   it barely helps, the residual is the tau^3 term and the design should not
   bother carrying accelerations in tubes.
7. **Beyond-domain G (mutual binary, no dominant mass, straight-line tube,
   kappa=0.1, R=5):** the missed curvature is the full mutual gravity, not a
   small kick; I predict visible secular drift (this case is the doll
   boundary: two comparable masses must form a doll, and the tube read alone
   is not expected to survive here).

## Kill criterion (frozen)

The "gravity is news" tube-read premise is broken for adoption if an in-domain
configuration (C, D or E: dominant mass present, secondaries <= 1e-2 M,
kappa <= 0.3, R <= 10) shows secular Delta E_T growth: decade ratio >= 3 on a
monotone trend, reaching >= 1e-3 relative within <= 30 P_T. If only G fails,
the premise survives in-domain with the bound measured and the boundary named.
