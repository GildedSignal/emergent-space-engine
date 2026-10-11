# Predictions (written before the decisive runs, after smoke tuning only)

Run set: belt a∈[2.0,3.5], σ_e=0.02 (one hot run σ_e=0.08), stirrer μ=1e-3, a_p=1.6, e_p=0.05,
dt=2π/64, po=300 (rings po=600), N=4000 (rings N=2000), grids 4/8/12/16 bits per axis.
Smoke runs (po≤40, seeds 1) tuned the harness only; numbers below are predictions, not fits.

1. **Mechanism of churn (naive crossings).** Cumulative naive crossings grow ~linearly in t
   (exponent fit 0.95–1.05), and the rate scales with the cell size like 1/q (adjacent grid
   steps differ by 16×): med rate ratios bits16/bits12 and bits12/bits8 each in [8, 32].
   (If diffusion dominated instead, ratios would be ~256 and the t-exponent ~0.5–0.7.)
   Physical reading: synodic/secular oscillation of L sweeps cells; this is predictable
   response, not new information — a program that includes the law's averaged kicks
   predicts it away.
2. **Program half-life scales with the quantum.** hl(bits16) < 0.1 P_p (smoke: 0.077);
   hl(bits12) ∈ [0.5, 3] P_p; hl(bits8) ∈ [10, 60] P_p; hl(bits4) not reached in 300 P_p.
3. **Residual (smoothed-key) rate at 16 bits.** Belt-wide median 5–15 per P_p; in the
   600-P_p off-resonance ring the smoothed cumulative grows sub-linearly (fit < 0.8);
   in the 2:1 resonance ring it grows ~linearly (fit 0.85–1.05): coherent pumping, not
   diffusion. Resonance/off-resonance median rate ratio ≥ 3.
4. **Fat tail over ships.** In the stirred belt, p99/median of the smoothed rate ≥ 2,
   and the worst 1% of ships carry ≥ 10% of all residual crossings (top1pct_share ≥ 0.10).
5. **Controls.** μ=0: naive median 0, smoothed median 0, deadband median 0, smoothed
   departed fraction < 2%; deadband cuts the control's naive p99 (≈1.4/P_p) by ≥ 10×
   (roundoff boundary-flip artifact removed). μ=1e-3 is the positive side: crossings
   plentiful at every grid (counter works).
6. **Departure at the law's likely keys.** f_departed at bits12 exceeds 50% within the
   300 P_p run (~600 yr); domain exits stay < 5%.
7. **Entropy (the mature footprint).** Plug-in joint entropy of (a,L) on the 16-bit grid
   grows by 1–4 bits over 300 P_p and ends in [20, 32] bits/ship; the distribution stays
   far from the uniform floor (occupied cells ≪ 2^32): stirred belts stay compressible as
   a distribution; it is per-ship key churn (identity), not distribution spread, that
   creates live distinctions.
8. **Memory verdict.** Mature live bits/ship ≈ final H_joint + O(10) phase bits ≈ 25–40,
   against a total budget of 51.2 bits/ship for everything at 10⁹ bodies in 8 GB: a
   billion-body stirred belt alone consumes half-to-three-quarters of the whole machine
   budget unless reprogramming runs continuously in idle time.
