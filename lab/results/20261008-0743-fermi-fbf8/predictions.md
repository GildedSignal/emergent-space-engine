# Predictions (written before the decisive experiment)

Run: 20261008-0743-fermi-fbf8. Question: does H_live (bits of live distinguishing
information per game-second) bound or break the 10^9-body budget, and which budget
term breaks first?

Held-out cases (not tuned on; the experiment below has not been run yet):

1. **Encounter rate.** A r8-like belt (N bodies, a in [1, 1.5] uniform, Rayleigh
   sigma_e = 0.01, random angles, mu = 1), threshold rho = 1e-3: I predict
   **2e-4 .. 2e-3 encounters per body per orbit** (r8 v2's belt 0 implied ~2.7e-4
   at its N; rate per body must be flat in N at fixed density — the board's premise).
2. **Kick size.** Per encounter below rho = 1e-3, the eccentricity kick scales as
   delta_e ~ 2m/(d * v_rel) with d ~ rho, v_rel ~ few x 1e-2: at m = 1e-10 (star-mass
   units) I predict **delta_e ~ 1e-5 .. 1e-4** per encounter.
3. **Distinction time.** With element quantum q_e = 1e-3 (the law's scar grid is
   coarser than this), first-distinction time t_d ~ (q_e/delta_e)^2 / R orbits:
   at m = 1e-10 I predict **t_d > 10^6 orbits**; the belt program never dies in any
   play horizon. t_d scales as m^-2.
4. **Mass threshold.** The per-body mass where t_d drops below 10 orbits (a long
   campaign at high RTF) is **m* ~ 1e-8 .. 1e-7 star masses**, i.e. an aggregate
   belt mass of 10..100 M_star at 10^9 bodies — unphysical for any real system.
5. **Budget verdict.** At 10^9: generator memory ~16 MB (0.126 bits/body, gold
   components-98bc); scar memory from belt physics < 10 MB per campaign;
   steady-state encounter compute << 1% of the M1. **Memory never breaks first.
   The first-breaking term is one-time candidate setup/qualification**
   (2.5-24 us/pair, r8) at ~10^3-10^4 s for 10^9 bodies unless paid in idle time,
   plus the known concentrated-fleet (co-orbital) risk.
6. **Claim check.** "190 cores for 10^9 at today's rates" (board, 29 September):
   re-derived from the pre-pivot per-body-step model (350-700 steps/orbit x ~10^2
   ops / 10^10 ops/s) I get ~10^2-10^3 cores — consistent. Post-pivot (events-only,
   B9: zero work per orbit until an event) the same estimate collapses to ~0 per
   orbit steady state.

What would make me wrong: if the sampled conjunction geometry gives encounter
kick variances much larger than delta_e ~ 2m/(rho v_rel) (e.g. pile-ups at very
small d from gravitational focusing), t_d could fall by the square of that factor;
if R grows with N beyond fixed-density scaling, the co-orbital gold's caveat applies.
