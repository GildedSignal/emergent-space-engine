Working...
Check complete. `check.md` written to the run folder; nothing else touched there (patch empty, tree clean).

**Grade: silver.**

Summary of what I did and found:

- **Reproduced bit-for-bit**: the decisive run (s4=89.3% at 541 orbits, med4=6, exponent 0.57, occupancy, 12-band profile, late rate 0.0181), dtest, and the no-Jupiter control — all dossier commands run in ≤ 40 s as claimed.
- **Verified the instruments against the law**: memo key = 12 relative bits on periapsis and the `(1−e)/(1+e)` gap (`orbit.rs:16-17,75-101`); the script is faithful to within a 2× width detail (the crate's `quantize(12)` counts the leading bit, so its grid is ~2048/octave, not 4096 — real churn ~2× slower, order unchanged). 16 B/body = `law.md`'s Tube; Form P/seal = `shipmem/program.rs`; H_live = `plane.md:36`; HANDOFF said "not measured yet" — first measurement, novel against HISTORY and complementary to gold `components-98bc`.
- **Three adversarial cases of my own**, all *confirming* the finding: (1) the control the author omitted — no-Jupiter twins split only 4% vs 89.3%, so the splits are real forcing dynamics, not integrator chaos; (2) Jupiter/10 delays the 50% split ~10×, matching the claimed linear forcing scaling; (3) 775 vs 1550 steps/P_J at matched times agree — the decisive run is dt-converged.
- **Defects found, none fatal**: `dtest`'s arms end at different times (its "agreement" is not evidence); the crossing-rate instrument is checkpoint-density-dependent (jitter saturates at ~2/interval — the 0.018-vs-0.027 floor comparison mixes densities; at matched spacing the signal is ~4× above the floor, *stronger* than claimed); reband cost is 0.07% of kick-evals, not 7%; undisclosed scene change between predictions and decisive run; the 3:1 resonance band is ~15 points above the local trend despite "bands are not special".
- **Why silver, not gold**: held-out prediction 2 failed (89% split vs <20%) — honestly reported and it *is* the finding, but by the lab's own grading precedent that caps below gold; and the adoption-critical billing number (reband loop bytes/body, H_live residue) is still inferred. The named gold experiment: run the actual reband loop with `shipmem::program::infer` on cadence at the crate's true key width.
