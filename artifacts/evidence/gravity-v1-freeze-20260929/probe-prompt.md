You are running the premise probe for a draft physics law. Write and run pure Python 3 (standard library only). You may create files only in /private/tmp/glm-scratch/gv1/ and in this clone. Do not touch anything else. Do not run git commands.

Read docs/gravity-law.md (the draft contract: its "Premise probe" section has the frozen kill criteria; do not change them) and xtask/src/gr_oracle.rs plus xtask/src/gr_oracle_extended.rs (the exact-GR oracle formulas). Use G = c = M = 1.

**The probe.** A 64-bit float version of the law: test-body motion around a Schwarzschild mass, in Painlevé–Gullstrand (river) coordinates or any equivalent formulation, integrated with a TIME-SYMMETRIC (reversible) drift-kick or splitting integrator. Step = η times the local dynamical time √(r³/M), a function of the current state only.
1. **Precession.** For η ∈ {1/16, 1/32, 1/64, 1/128}, and for 2nd and 4th order (a Yoshida composition of the 2nd-order step), measure the periapsis advance per orbit at p = 20 and p = 1000 (e = 0.2 and 0.5). Compare with the oracle's exact advance (elliptic formula). Report the relative error and the steps per orbit.
2. **Energy.** Measure energy error growth over 10^4 orbits at p = 20, e = 0.2, fitting the growth exponent.
3. **Capture.** Inward E = 1 anchors at r0 = 100 with L = 4(1 ± δ), δ ∈ {0.02, 0.01, 0.005}: absorbed (reaches r ≤ 2) or escapes?
4. **Light.** Deflection at b = 10 and 30 against the oracle; capture for b just below and above 3√3.
5. **Events per orbit** against p.

Keep every script under 60 s of wall time.

**Output (your final reply).** A table giving each kill criterion as PASS or KILL against its frozen threshold, the formulas and integrator you used, run times, and limitations. Where your implementation might be wrong rather than the premise, say so plainly. This is orders of magnitude plus 1% tolerances; don't overclaim.
