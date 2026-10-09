Working...
Check complete. `check.md` written; nothing else in the run folder touched.

## Verdict: **Grade: silver**

**Reproduced (exact, from the dossier's commands):**
- `controls`: 25/25 ground truth, same five disclosed deviations.
- `inversion`: 3/3, identical numbers (56.7/52.5/49.2 vs 0.32/0.48/0.48).
- `wh` draw 0: line-for-line match once the pre-screen is honored (good settles at seed 4247, retard at 4244; 0/8 both; exponents 0.049/0.021).
- Horizon ≈ 0.2–0.3 and alias `T ≥ 4·P_max` (4/5 phases, phase-0 dodge) regenerate under my harness.

**Adversarial findings:**
1. **Part B's "bounded" family diverges** — `chaotic_sat`'s wander flips x negative, then e^λ multiplication runs away (max|x| = 1e35–1e94); the shipped 49–57 exponents measure divergence, not saturation. My corrected saturating model still inverts 3/3 (≈3.77 vs ≈0.4), so the diagnosis survives, but the shipped demonstration is an artifact.
2. **Part C as shipped is vacuous** — `int(round(s−s0))` at unit scale gives all-zero series (verified), so the recorded 0/8 flags say nothing; the "2^40 integerization" the dossier describes is absent from the code. My reimplementation at 2^40 regenerates the numbers (good 0/8 and 1/8 ≤ the pre-registered kill of 3/8).
3. **Long-memory bounded series false-flag reliably** — OU corr T/8 → 2/3, T/4 → 3/3, 1/f flicker 3/3 "leak": the author's hedged worry (a) is a measured weakness, worse than stated.
4. **Delivered the missing experiment, and it reframes it:** held-out draw 1 (never run — cancelled): control passes, inversion 2/2. retard10 confirmed scene-destroyer (10/10 seeds). retard3 (the author's own suggested gentler leak) settles but its J error *saturates* at 4×10⁻³ — the rule correctly calls it bounded — so no leak has yet been caught on the physical path; the gold experiment must bias the integrator itself.

**Silver, not gold:** real, exact, novel (no Allan/AVAR elsewhere in the repo), directly on the pending B12 redesign — but the physical-path leak detection is undelivered, Part C's shipped flags are empty evidence, Part B's shipped evidence is artifactual, and my false-positive family must be answered (multi-τ consistency, unbuilt). One experiment away, named in the check.
