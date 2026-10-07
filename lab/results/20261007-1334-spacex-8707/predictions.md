# Predictions (written before the decisive runs; smoke tuning was N≤6000, ≤200 yr)

Decisive runs: belt N=30000, 1000 yr, dt=0.1, seeds {7,8,9}; null control; convergence pair dt=0.05 vs 0.1 (N=4000, 300 yr). Scene: star GM=1, Jupiter-analogue (m=1e-3, a=5.2, e=0.048), belt a∈[2.0,3.3], Rayleigh e σ=0.05.

Held-out cases (not tuned on):

1. **Null control** (m_p=0, same code path): max |Δa|/a ≤ 1e-11 and max |Δe| ≤ 1e-11 over 1000 yr. (Measured 2e-13/3e-14 at 50 yr.) If larger, the harness invents distinctions and every other number is void.
2. **Residual growth exponent** (rms of secular-reabsorbed e-residual, 50→1000 yr): between 0.5 and 0.7. Smoke suggested ~0.62 at 200 yr; if it reaches ≥ 1.0 the linear secular reabsorption fails outright and scars are dominated by coherent unmodelled drift (a different, worse verdict).
3. **Resonance differentiation** at 1000 yr: crossing-rate ratio near/far (within ±0.05 AU of a ∈ {2.50, 2.82, 2.96, 3.28}) at q=3e-3 ≥ 2. At 200 yr it was only 1.5 — the prediction is that a full Gyr-like span separates the Kirkwood structure; if it stays < 2, the resonance fingerprint is not resolvable at this N and the near/far split must be dropped from the verdict.
4. **Fit noise control**: in-sample crossing rate at q=1e-3 within 30% of out-of-sample. If in-sample is much lower, the poly fit overfits and the crossing rates are an artifact of the fit, not physics.
5. **Coherence floor**: cell means over (Δa=0.05 AU, Δλ=5°) cells with ≥10 members capture ≥ 80% of the cumulative kick field variance at 1000 yr (residual ≤ 20%). Smoke at 200 yr gave 71% at the coarse cell (0.1 AU, 10°) on a 2000-subsample.
6. **Session scale lag**: at q=1e-3, fraction of bodies crossed within the first 2 game-years < 5% (the secular model absorbs the early coherent drift; scars start after a lag).
7. **Memory verdict shape**: at q=1e-3 and 16 B per scar, 1e9 bodies crossed (~frac→1 by ~200 yr in smoke) exceed 8 GB; the refit period T* that keeps the scar store ≤ 4 GB (frac ≤ 0.25) lies in [10, 300] yr of simulated time. I predict T* ≈ 30–100 yr.

What would make the claim wrong: null control failing (void), fit-noise control failing (crossings are instrument, not physics), or growth exponent ≥ 1 with coherence < 80% (the belt's distinctions are neither reabsorbable nor aggregable — the population-program memory story dies at billion scale for Jupiter-perturbed belts).
