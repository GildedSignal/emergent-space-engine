Working...
Check complete. `lab/results/20261009-2043-scout-a1a4/check.md` written: **Grade: silver**, abstract exactly 120 words, grade line first per convention.

**Verdict basis:**

*Reproduced* — both scripts regenerate every printed number (timings same order: 0.57 ms compile / 3.13 µs readout / 7.21 ms DOP853).

*Verified beyond the author's harness* — my independent forward r-space oracle (no cubic, no ψ; v from t + r*):
- C/D/E/F and adversarial E=1.05·0.999L_c, E=10⁶·0.99L_c all at 0.9–4e-12; the EF-time identity also re-derived by hand.
- **Their flagged k=6–7 kink resolved in their favor**: careful 50-digit split u-quadrature gives Δφ = 17.3290/20.5854/23.8417, differences 3.2564/3.2563 — the log divergence continues at exactly the predicted slope (their mp40 reference collapsed, as they diagnosed). True 512-panel errors 4.2e-7/1.8e-4/7.4e-3: conclusion stands, their error column was 2 orders pessimistic.
- The P3 pair-precision table (whose script is missing from `work/`) regenerates exactly for k≥4; u₁ at 0–2 ulp.
- Photon near-critical and γ=10⁶: nothing new breaks.

*Why silver, not gold — the record, not the physics:*
1. **P4 substituted**: predicted bracket+Newton <20 µs; the shipped 3.08 µs times linear interpolation accurate to only **6.2e-6** (six orders below the table), my Newton runs 36.5 µs at 1.2e-7 — the dossier marks P4 ✓ without disclosing the swap.
2. One headline table has no generating script (I regenerated it — genuine).
3. Two prose numbers wrong: "b ∝ δ" (it's √δ), "2×10⁻⁹" (measured 3.95e-8).

The one experiment to gold: honest readout timing+accuracy over a winding sweep, ship the missing script, fix the two numbers. Also disclosed: my reproduction overwrote `work/plunge_main.json`'s six `compile_ms` timing floats (the script writes into its own evidence folder; deterministic physics fields unchanged).
