Working...
Check complete: `lab/results/20261006-0346-redteam-df81/check.md` written, nothing else touched.

**Grade: gold.**

Verification performed:

- **Reproduction:** both scripts ran bit-identical to the stored outputs (F1 19.4 s, F2 23.0 s). `patch.diff` empty, tree clean, `predictions.md` (03:57) predates both outputs (04:01, 04:02).
- **Text and repo claims:** the attacked sentence, the "shortcuts add speed, never error" line, and the 50 ns/kick cost row are verbatim in representation.md; no re-anchor rule exists in either doc; `lab/rungs/` has no r5/r6; B5/B9 cover only unperturbed cycles. law.md line 35 makes the jet the *adopted* mechanism — the finding is live, not a strawman. Peters sizes check analytically: (128π/5)ν(M/a)^{5/2} = 1.1×10⁻²/1.1×10⁻³/2.0×10⁻⁴.
- **Adversarial cases:** (1) at the exact Peters kick sizes the Δt jet fails on kicks **1, 1, 4** at a = 20/50/100M — stronger than claimed; (2) C_E(Δt) is scale-free (1.76–1.85 ≈ Kepler's 15/8), so the weak field doesn't rescue the inspiral channel; (3) the view gather survives even at emitter β = 0.99 (min g′ = 0.01, max 9 iterations, zero escapes) — robust beyond the author's β_e ≤ 0.6 cap.
- **Predictions:** pre-registered; the P1 VOID rule fired and was honored; P4 failed and was honestly reported as failed — the falsification itself held everywhere I probed.
- **Novelty:** no HISTORY entry measures the jet's validity domain (the 5 Oct memo finding was hit rates; H0207's re-anchor was the Fermi frame).

Noted misses (in check.md): mode 'E' drifts E *toward* 1 (outspiral) while labeled "inspiral-like" — direction mislabeled, conclusion unaffected; "Δφ safe" under E-kicks overstated (n* = 290 at ε = 10⁻⁴); the resonant-sequence classification is argued, not measured.
