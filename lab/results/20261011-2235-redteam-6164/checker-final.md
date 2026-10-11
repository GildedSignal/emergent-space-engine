Working...
Check complete: `lab/results/20261011-2235-redteam-6164/check.md` written, **Grade: gold**. Nothing else in the run folder touched.

**What the check did:**

- **Reproduction:** `python3 probe.py` in a clean `/tmp` tree (patch.diff is empty) → `probe_out.json` byte-identical to the author's, 4.0 s. Every dossier number traced to the JSON; I re-derived the ISCO-seed algebra (L_circ² = r²/(r−3), r_c² − L²r_c + 3L² = 0) by hand — all agree.
- **Pre-registration:** file times put `predictions.md` (22:42) 10 minutes before the decisive output (22:52). The two failed predictions are reported as failures, not spun.
- **Eight adversarial cases:** h-refinement (headline 1.887e-4 stable to 8 digits), mixed-sign kicks (E-channel is the envelope), extrapolation to r_apo = 10⁵ (C → 1.8, scaling holds), escape-side family exit (α ≥ 1e-4 at p=100, e=0.99), recompile saturation (measured N_floor = 1 at r_apo = 2000 — "every kick recompiles" confirmed), separatrix robustness to derivative step, and regeneration of the two precession ratios the shipped code doesn't emit (they're correct).
- **Doc claims all verified:** representation.md line 67 (the premise quote), line 32 (dead Minsky mechanism still taught as primary vs law.md line 20's darwin16), §7's r5/r6 vs `lab/rungs/` containing only r1–r4, r7–r10, no gate in law.md's B5–B19 table on the jet's validity domain, r1's ISCO seed line.
- **Novelty:** only prior is df81 (one orbit family, the unqualified "0.05 compiles/kick"); the domain map and corner correction are new.

**Nits recorded in "what the author missed":** two unregenerable oracle numbers (I closed them), the Kepler T-channel coefficient is 15/8·α² not 15/4, the "2.8 compiles/kick" figure is an unsaturable extrapolation (caps at 1), L-channel errors sit at the oracle's own noise floor, and B13's real kicks are larger than the α = 1e-3 tested — making the separatrix finding conservative.
