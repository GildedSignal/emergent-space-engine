Working...
Check complete. `check.md` written to the run folder — nothing else touched, no git operations.

## Verdict: silver

**Reproduced** — `python3 probe.py` in a clean tree is byte-identical to `metrics.json` on every physics section (3.7 s, <100 MB; empty patch.diff). `predictions.md` (11:58) predates the final code (12:11) and decisive run (12:12); P2/P4/P6 held, P1/P3 failed and were disclosed (P1's ×10³ slip verified as a hand-conversion error — the formula is right: 3.44×10⁻⁶/s × 1.03×10⁸ s = 354).

**Attacks that held** — kernel vs leapfrog at 8 grid extremes including t=218 focusing (≤0.16%, except 1.7% at the transition point); flux integral by hand (356 vs 354.7); σ₀-independence in the dispersion regime (352.7 vs 354.7 at σ₀=200); scene generality (a=0.5 AU, hot belt: slope 1.00 bit/octave both); growth exponents σ∝t^0.5 / t^0.34; β continuity below the swept range. First measurement of H_live, the queued task (HANDOFF:70 "not measured yet").

**What kept it from gold:**
1. **Undisclosed scene composition** — `coldswarm` in code is Σ×2500 *and* cold; the dossier says only "cold swarm". I ran the sparse version: 40.3 bits after 16 384 orbits → **7.6 GB at 3 dof, inside 8 GB** — the cold-swarm "breaks 8 GB" reading depends on the undisclosed ×2500.
2. **Years slip** — 16 384 orbits = 534 years at warp 100, not "2.7×10⁸ game-s ≈ 8.5 years" (frames/game-s confusion; conservative direction).
3. **Estimator bias** — shape-entropy under-reports by 1.46 bits on a synthetic Gaussian through the exact pipeline (nb=10⁴ in 256² bins); all absolute H values ~1.4 bits low. Slopes exact, unflagged by the author.
4. **Non-regenerating digits** — 384 vs 375.36 mutations, 9.3×10⁻⁴ vs 8.66×10⁻⁴, floor-invariance triple — secondary numbers without reproducing commands (the lab's classic silver trap).

One experiment to gold: disclose/bracket the cold scene, fold the secondary digits into `metrics.json`, fix the conversion. Core claim (store log-bounded, churn binds, not memory) survived every attack.
