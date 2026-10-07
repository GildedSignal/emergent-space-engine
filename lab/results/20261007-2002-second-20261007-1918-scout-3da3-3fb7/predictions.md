# Predictions (written before the decisive run, 2026-10-07)

Decisive run: `python3 consumer-gate.py` — 5 seeds (11..55), 20 consumer orbits
at r=1.3 (~163 time units), riders at r=1.3 and r=1.8, medians over seeds judge
the gates. Held out: everything beyond the plumbing smokes (single seed, <= 3
orbits, used only to verify the harness runs and that fg ordering is physical:
G8 < G1 ~ K16 < DR1 < NN=far_share). The 20-orbit multi-seed medians, both
radii, and all gate verdicts below are predictions, not observations.

Gates (fixed before the run):
- mu: |mean_{last q} r(cfg) - mean_{last q} r(REF)| / r_c <= 0.05 (strict),
  <= 0.10 (adopt level, reported both).
- sg: |rms_{last q} r(cfg) - rms_{last q} r(REF)| / r_c <= 0.05.
- FLOOR must pass strict; else the scene's noise floor is above the gates -> VOID.
- K16 must fail at least one; else the gates cannot fail -> VOID.

1. **G8 (nu=8, the dossier's stated cap) passes** both gates at both radii at
   the strict level (medium confidence; smoke magnitudes suggest borderline).
2. **G1 (nu=1, the code's cap) fails strict mu, passes at the 0.10 level**
   (medium confidence). Its staleness error (fg_med ~ 0.1 in this disk) is
   dominated by the disk's own self-scattering, which is ~sqrt(1e6/256) = 62x
   stronger than an engine-scale population.
3. **K16 (kill control) fails mu** (predicted |Delta mean r|/r_c > 0.15): the
   star distribution evolves over 16 orbits and the stale far field misses it.
4. **DR1 fails mu and sg** (linear extrapolation of orbiting sources over up to
   one source orbit is geometrically wrong; fg ~ 2x NN).
5. **NN (no far news) fails sg** with SMALLER wander than REF: dropping the
   fluctuating far field over-smooths the orbit — the news carries real
   behaviour (the consumer's real radial excursions), not just correction.
6. **fg_med medians**: G8 in [3e-3, 1.5e-2]; G1 in [5e-2, 2e-1] ~ K16; DR1 ~
   2x NN ~ 0.3-0.6. All are >= 3 orders above the falsifier's eps=1e-6 quantum:
   the behaviourally relevant far-field error scale is ~1e-2..1e-1 in a disk
   62x more diffusive than the engine's populations.
7. **Scaling consequence** (if 2 holds): required cadence nu_req ~ sigma_dv^{2/3}
   ~ N^{-1/3} at fixed total mass, so at 1e6 bodies nu_req ~ nu_req(256)/16:
   the engine's cap nu=1 binds with ~16x margin; traffic stays at the cap x
   grid count, flat in N, and OC#50's wall stays dead. If only nu=32 works
   here, the engine still needs only nu ~ 2: 2x the capped traffic, still 1e6x
   below pairwise.

Kill criteria (pre-registered): FLOOR failing strict gates, or K16 passing
everything, voids the run's behavioural verdicts; the fg measurements and
scaling argument stand on their own as the fallback evidence.
