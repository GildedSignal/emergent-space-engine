Working...
Check complete. Verdict written to `lab/results/20261010-1706-second-20261010-1544-system-97ce-b18f/check.md`.

**Grade: gold** — as a refutation, the rubric's "shows that a premise is wrong" route.

What I did:
- **Reproduced** everything from a clean tree with the patch applied: reference row bit-for-bit (406,220 events, 1.0000 rekeys/kick — the first run's record), anchored 0.01598 compiles/kick, wall 1.81×, all held-out seed numbers, determinism, control (11/408), threshold falsifier (0.520 / 2.1×10⁻⁵), headroom, suite green at default off. Only wall times differed (shared box; counts identical).
- **Attacked** with three of my own cases — high-e, 2:1 resonance, doubled horizon. All *strengthen* the kill: high-e breaks the compute target itself (0.0552 > 0.05, |Δe| max 0.31, one alive-diff); resonance doesn't amplify (drift is secular); error grows ~linearly with horizon.
- **Found the mechanism sharper than the author stated**: in `readout`, `residual.velocity` never moves position — between compiles the carried kicks have *no position response at all*. Verified independently: forcing the threshold on makes the existing lifecycle pin fail with the ship's displacement exactly 0.0. The engine's own gate votes no.
- **Novelty**: the plain offset-carry at law.md's threshold was unmeasured (the red-team priced the jet *with* derivatives; H0207's re-anchoring was the battle frame's). The error∝threshold / compiles∝1/threshold trade-off is new and generalizes the kill.
- Tree restored clean; my throwaway removed; nothing else in the run folder touched.
