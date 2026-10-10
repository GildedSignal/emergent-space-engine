Working...
Check complete. Verdict: **Grade: silver**, written to `lab/results/20261010-1816-components-6273/check.md`; tree restored to its pre-check state.

**What I did:**
- **Reproduced everything** from the dossier's commands after applying `work/patch.diff`: all four scan sweeps and the feedback run (1222→1222 and 1222→1215 events, distinct 587/587, 1389) regenerate **numerically identically**, bit-for-bit except timings. The dossier's table (2.4 bits/body at μ_b=10⁻¹⁸, 0.3–3.2 GB per 10⁹, 65× vs naive, coorbital rebind 4.7×) is faithful to the logs.
- **Found a provenance blemish:** the stored seed31/narrow logs lack the final build's `max_rel_dP` field — they predate the last code edit, undisclosed. All numbers regenerate, so benign, but noted.
- **Predictions:** 3 of 6 missed (P1, P2, P3), honestly reported; P6 held only at μ_b≥10⁻¹⁴.
- **Adversarial A1:** the claimed crossover "1.7×10⁻¹⁸" is an interpolation — my sweep gives 43.8% marks there and the measured 50% point at ≈2.2×10⁻¹⁸.
- **Adversarial A2 (the decisive one):** at exactly ship mass (μ_b=5×10⁻²², 10⁹ kg around a solar star), a co-orbital fleet marks **8.8%** of encounter-updates (0.87 bits/body per 50 orbits). The "ships never leave the program / forever" headline is refuted in the concentrated regime — and the author's own held-out coorbital file (2.1% at 10⁻²²) already contained the refutation.
- **Novelty:** confirmed — HANDOFF lists H_live as "not measured yet"; the genesis program and program+scars priors are properly cited.

Silver, one experiment from gold: the ship-mass fleet scene with the dual store actually allocating over a long horizon, and the crossover restated as scene-parameterized rate × kernel rather than one wide-belt number.
