Working...
Check complete. `lab/results/20261004-1525-scout-2098/check.md` written — nothing else in the run folder touched, no commits.

**Grade: silver.**

What I did:
- **Reproduced bit-identically**: all 102 result rows match; every dossier table number re-derived from my run. Predictions timing consistent (15:43:01 → 15:43:58, matching the claimed runtime).
- **Validated the reference independently**: RK4 (4000 steps/sun-orbit) agrees with plain-512 to 4–8e-4; nk=1024/2048 to ~1e-5; fit-window shifts the verdict by <0.5%.
- **Confirmed the kills**: correctors break where plain holds (123% vs 0.97% at f=0.3 nk=4; escapes at f=0.4), fr4 loses at equal evals everywhere, r9's averaging kill reproduces exactly, and the n=0-multipole mechanism checks out numerically (double average constant to 3e-10).
- **One material hit**: the headline "through ≥0.4 R_H" is seed-luck. Across 5 sun-phase seeds, f=0.4 at nk=6 escapes or errs 40% on 4/5 seeds; the robust frontier there is nk≈16 (2× cut). Through 0.3 R_H, nk=6 is robust across seeds and e0=0.05–0.3 births (5–8× cut, e0=0.3 measured at 0.3% error). Also found the cadence is non-monotone in nk (nk=5 → 71% at f=0.4) — free evidence for the author's own aliasing mechanism.
- **Novelty**: no prior H entry measures the plain-map cadence frontier or the corrector transplant; H0190/r9 lineage cited correctly.

Silver because the robust gain is 5–8× (not 10×) and the boundary needed correction. The gold experiment is named: phase-lock the kick grid to the synodic phase and test below 1 kick/orbit across seeds, horizons and births.
