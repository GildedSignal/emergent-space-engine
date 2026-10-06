# dossier.md — run 20261005-2231-q-cadence-7d0d (lens: q-cadence)

**Claim.** Not gold: the decisive mixed-scene validation did not complete (the
window's machine ran at load 15 on 8 vCPU; every sweep grid timed out). What
landed: a validated float replica of the plane's kick layer whose micro-frontier
shows the moon cadence is set by the **Hill position** (N* = 4, 8, 16 kicks per
orbit at f = 0.2, 0.3, 0.45 R_H; flat in e at a 12-orbit horizon), i.e. the
cadence surface is steep in f and the eccentricity term that earlier runs
measured is a *horizon* effect, not a spectral one — which means a horizon-free
local cadence rule is not derivable from these gates without first fixing the
error type, and the prior disagreements (4–6 vs 8 vs 16 vs 64) are one surface
read at different (f, horizon, resonance-distance) points.

## Bottleneck

Board focus 1: fewer kicks per orbit at the same behaviour. The rule proposed
here: `N*(body) = ceil2( KAPPA · Φ(f) · (1+e)^γ · n/|n − n_p| )`, with routing
out of the kick layer inside resonance bands (|q n − p n_p| < 2 W_pq) and
beyond the unpredictability wall (1 − a/a_p > 1.0·μ^{1/4}), decided from
compiled integers only. Expected gain if validated: 16–32× vs today's 128 for
the predictable bulk (f ≤ 0.3), which is where most bodies live (principle 33).

## Evidence

All in this folder; the machine was oversubscribed (load 5–15), so each
command's wall time exceeded its CPU estimate; timings are orders of magnitude
only, as the lab's rule requires.

1. **Replica (cad.py), validated three ways** (positive controls):
   - drift exactness: 2000 round trips at e = 0.01–0.99 and hyperbolic e = 1.4,
     energy conserved to ≤ 8×10⁻¹² (validate.py's drift block, 2 s);
   - one-step DKD vs a hand-written RK4 at h = 10⁻⁵ on the exact CRTBP (tide
     included): agreement to the kick's size;
   - an earlier version passed drift-energy checks while being wrong: the
     eccentricity-vector formula had both signs flipped (ϖ off by π), which
     conserves energy but rotates every orbit. Only a DOP853 control carrying
     the *dominant* force caught it (a tide-only control cannot; my first one
     was tide-only and masked it). Lesson recorded below.
2. **Micro-frontier (the run's one new measurement):** moons at f ∈
   {0.2, 0.3, 0.45} R_H, e0 ∈ {0.1, 0.3}, μ_p = 10⁻³, horizon 12 planet
   orbits, gate = apsidal rate within 10% of the N = 256 reference and e-max
   ratio in [0.8, 1.25] on both phases:
   `N* = 4 (f=.2, e=.1)`, `4 (.2, .3)`, `8 (.3, .1)`, `8 (.3, .3)`, `16 (.45, .1)`.
   Fit: N* ≈ 4·(f/0.2)^1.7, equivalently N* ∝ τ^0.57 (τ = f³/3), with the
   e-exponent consistent with **zero** at this horizon.
3. **The disagreement table explained** (each prior number is a point on the
   surface; my points confirm the low-f end):
   - scout-2098's 4–6 at f ≤ 0.4, e = 0.1, 20 planet orbits ✓ matches my
     4–8 at 12 orbits (horizon widens it);
   - f341's 16 at f = 0.3, e = 0.3, **18 planet orbits** and 13ae's ≥ 64 at
     f = 0.3, e = 0.3, **30 planet orbits** vs my 8 at 12 orbits: the frontier
     doubles roughly per ×1.5 horizon ⇒ the low-cadence error **walks** (does
     not saturate). The e-dependence those runs measured is the walk speed,
     which e feeds, not a spectral requirement;
   - 27ce's 8 for a belt (e ≤ 0.2, far from 2:1) ✓ consistent: belt bodies sit
     at f_eff ≪ 0.2 of Jupiter (τ_J on them is tiny), so the surface's floor
     (4–8) binds;
   - quant-5022's 64 at H1 and a9c2's ∞ inside the band are the *routing*
     branch, not the cadence branch: no rate holds there (a9c2), so the rule
     must not size it — it must detect it (compiled frequencies, law.md line
     29) and hand the pair to the resonant representation.
4. **Rule module** (rule.py + RULE constants): KAPPA = 4 (the deep-interior
   floor), Φ(f) = (f/0.2)^1.7, γ = 0 pending a horizon-controlled re-fit,
   routing at 2 W and at the μ^{1/4} wall, all from integers (n from E, n_p
   from the doll's table). The B12 ship branch is horizon-sized in Jacobi-walk
   (quant-5022's rate ∝ μ·H at every cadence) — an error-type defect of the
   time-dependent midpoint kick, not a cadence quantity; b12.py (two dolls,
   SyMBA levels, handoff at R_SOI/4 in and R_SOI out, 200-period horizon,
   gate ERR 10⁻⁴ / exponent 0.2 as in handoff.rs) is built but its sweep never
   got CPU. It is the named next experiment.

## Predictions

predictions.md was written before any mixed-scene run (none ran — VOID there,
reported as such). Its falsifiable core stands untested except the f-scaling,
which held at the three measured points.

## What would make it wrong

The walk interpretation (horizon-grown frontier) could be seed luck: 2 phases
per point is thin, and scout-2098 showed adjacent-N jumps of 306% → 0.8% from
aliasing. The τ^0.57 vs synodic-sampling parametrizations are degenerate on 3
f-points; the moon grid that separates them (240 jobs, grid_moons.py, ~15 CPU-
minutes on a quiet machine) is ready and did not finish here. The routing
constants are inherited from a9c2/0c67, not re-measured. Fit with PRINCIPLES:
"the simulation tells us what's next not us" (OC#36) — the rule reads only
local compiled quantities; "A failed experiment kills that configuration,
never the method" (9) — the killed configurations here are the naive DOP
control and the horizon-free reading of the gates, not the local rule.

## Cost of adopting

One function in `step.rs` (`step_for`'s per_period_log2 becomes per-body),
plus the resonance router the law already specifies. Nothing else changes; the
cadence still changes only at events, decided in integers.

## The lens (what it may have made me miss)

The cadence lens presumes kicks are the unit of cost; the Opus memo's R2 says
the prior question is which part of the perturbation is integrable (secular
phasors need zero kicks). A horizon-free rule may be impossible *because* the
right representation removes the walking error rather than sizing it — my
walk finding is equally evidence for R2 as against naive cadence.
