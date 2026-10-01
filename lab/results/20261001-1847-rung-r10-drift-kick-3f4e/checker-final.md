Working...
Check complete. Deliverables written: `metrics-check.json` and `check.md` in the run folder (nothing else touched, no git commands run).

**Verdict (verdict.py, metrics-check vs metrics.json): VOID** — the positive control `truth` fails the jacobi criterion (1.345 > 0.2). No disputed outcomes: my metrics-check.json is **bit-for-bit identical** to the author's metrics.json, reproduced from the author's own workers in a clean copy.

Key findings:

1. **Full reproduction.** B12 truth series agree to 0.00e+00; all four jacobi exponents (symba 0.4132, wh-fixed 1.3900, soi-switch 0.5859, truth 1.3455), maxerrs, class/libration/cost all equal. Truth spot-checks on moons and resonant cases identical.
2. **Ports verified** against `sample.rs`/`fit.rs`/`handoff.rs`/`resonance.rs` (SplitMix64 seed, HANDOFF_KEPT, growth exponent, W = 2.5μ^(2/3)); the Jacobi formula is exact (smooth-ship truth at rtol 1e-13 keeps |ΔC_J/C_J| ≤ 2.1e-13).
3. **The VOID is the rung's own reference.** Barycentric DOP853@1e-12 drifts to 1.3e-8 on these chaotic ships; the Rust judge works planet-relative in the rotating frame — the representation the 1e-12 floor assumes. Same criterion family the taste log already flags for r2/r3.
4. **symba's central claim is killed by its own numbers** (0.413 vs ≤ 0.2, exactly the prediction the author flagged as killable), and the dossier still asserts the opposite while its metrics table was never filled (`PLACEHOLDER` remains).
5. **precession_match = 1.0 is vacuous** (0 rated moons — no circular birth develops a defined apse). I ran the missing eccentric candidates (the author's stage3 crashed on a one-line tuple bug with truth already merged): **symba 20/20 precession, 64/64 class; wh-fixed 0/20 with sign-flipped rates; soi-switch 20/20, 63/64.** The changeover genuinely works where it was never judged, at 96 evals/orbit — silver, one experiment from gold: all 16 frozen ships against a rotating-frame reference.

Also recorded: only 4 of 16 B12 ships ran (crossings 10–18, none meeting the ≥ 20 case rule), and the delivered folder cannot regenerate metrics.json (128-moon truth vs 64-moon candidates → stage_metrics raises IndexError).
