# predictions.md — q-correctors run 20261001-2353

Written before the decisive sweeps. Tuning happened only on the e₀ = 0.05 moons
(validate.py: error scaling of each scheme against a conserved energy). Held-out
cases below have not been run at the time of writing.

Bar (from the lens and the gates it names): same behaviours as the plane's dkd at
1/128 kicks per orbit — precession within 10% (B14), resonance e-pump ratio in
[0.8, 1.25], libration amplitude ratio >= 0.8, regime match (B17), Jacobi error
<= 1e-4 with exponent <= 0.2 (B12). Cost counted in kicks per orbit per body
(drifts are tube reads, free; a kick is a force evaluation plus a rebind).

## Predictions

1. **S1 moons (e0 = 0.05, tuning set).** dkd holds 10% precession down to ~64
   kicks/orbit (k=6) and breaks (wrong rate) at 32 (k=5). saba2 (2 kicks/step)
   holds to 16 kicks/orbit (k=3), saba3 to 12 (k=2), whc3 to 10 (k=1) — i.e. the
   corrector/higher-order schemes cut kicks per orbit by ~4–8x at equal behaviour.
   whc3b (corrector applied only at the two ends, 1 kick/step) matches whc3's
   trajectory to better than 1e-6 of the semi-major axis over 50 orbits: the
   corrector is a conjugation and conjugations telescope, so its per-step cost
   is zero for a single kicked body whose sources are exact tubes.
2. **S1h held out: e0 = 0.3 moons.** dkd needs ~2x more kicks than at e = 0.05
   (Kepler shear at periapsis: the tau^2 error rides the periapsis passage);
   it breaks at ~128 kicks/orbit (i.e. the plane's own 1/128 step is marginal
   there). saba2/whc3 degrade less: still hold at ~24–40 kicks/orbit. The cut
   ratio improves at high e.
3. **S2 resonance (2:1 and 3:2).** At mu = 3e-5 and 3e-4 all schemes that hold
   the conjunction timing hold the behaviours down to ~32 kicks/orbit of the
   inner orbit (the synodic clock needs ~10+ kicks per conjunction). At mu = 3e-3
   the detuned libration amplitude is the first thing to go: dkd loses regime
   match below 128, whc3/saba2 keep it to ~40. Prediction: the resonance gate,
   not precession, sets the floor, and the cut is ~3–4x, slightly under the
   precession cut.
4. **S3 Jacobi / flybys.** dkd holds 1e-4 over 30+ sphere-of-influence crossings
   down to 32 kicks/orbit; whc3 and saba2 hold to ~8. The flyby (deep passage)
   cases hold for every scheme: the drift is the exact Kepler passage, and the
   tide is smooth on the passage timescale.
5. **S4 held out: close planet pass.** The WHFast corrector's sub-drifts are
   large (a1 = 0.418 tau, a2 = 0.837 tau per step): during a close pass its
   extra kicks sample the interaction at positions displaced by a large fraction
   of a step, so I predict whc3 gives a worse post-pass eccentricity than dkd at
   equal kicks per orbit (its displaced kicks straddle the conjunction), while
   saba2 (all sub-drifts within the step) is safe. If this holds, correctors are
   adopted for the smooth regimes with the SyMBA changeover switching to the
   plain kernel inside the shells.
6. **The gold bar (4x)**: met by saba2/whc3 on precession and Jacobi, marginal
   on resonance. The cheapest universal answer is whc3b: the 3rd-order
   corrector as a boundary conjugation — cost 1 kick/step (none extra), the
   same step count as today but 4x fewer of them, and its integer path is just
   two extra kick sums per binding event, applied once per tube.

## What would make it wrong

- If whc3b diverges from whc3, the corrector does not telescope in the plane's
  setting (time-dependent sources break the conjugation), and the honest cost
  is 5 kicks/step — the 4x cut then needs the step to grow 20x, which I doubt.
- If the resonance gate breaks for every scheme below 64 kicks/orbit at mu=3e-3,
  the cut is capped at 2x for the resonant regime and the dossier is silver.
