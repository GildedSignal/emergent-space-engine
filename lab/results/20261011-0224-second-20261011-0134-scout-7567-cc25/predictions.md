# Predictions — written before the decisive 10× horizon run

Setup: the scout run's composite (derived-cap + ratio at 10×, law-only) evaluated on the REAL
frozen B12 ships (`sample::HANDOFF_KEPT`, judged subset, 14/16 here) with the REAL shipped laws
(`echo`, `Planted(Bounded|Compound|Drift|Kick)` through their real `Law` impls), plus two
unshipped controls (`const` 3e-8, `leak(e)` = bounded + e·walk on the real echo states). The
harness is the shipped `xtask/src/behave/**` verbatim (sha256-verified copies); only
`composite.rs`/`main.rs` are new. The 1× maxima are an exact prefix of the 10× series (same P/8
grid from t=0) — the checker's prefix-extension demand holds by construction.

Already seen in setup (8-period smoke, not the decisive run): every kept ship's C_J level set
opens the near-planet unbound channel — the osculating-a band is the law's own clip
[0, AXIS_CAP=10 sep] for all 16 ships (brute-force state sampling agrees: max a = 10). So the
derived cap is CAP_i = TOL_B·(10 − a₀)/(R_H/sep) ≈ 1.3e-5 at TOL_B = 1e-7 for every ship.

## Predictions for the 10× run (2000 planet periods)

1. **echo PASS**: conserving integrator, max err ~1e-13; noise window maxima grow ~σ√(2 ln m),
   so median ratio ≈ 1.05–1.15 ≪ 2.
2. **const PASS**: ratio 1.0, max 3e-8 ≪ cap.
3. **bounded — the decisive case.** The bounded error is a linear readout of a(t): max err at
   8 periods already spans 1.6e-7…1.8e-6 (a-range up to ±1.28 sep on ship 7), and the clip sits
   at err = 1e-7·(10−a₀)/(R_H/sep) ≈ 1.3e-5. The trace's a-range grows with horizon until it
   touches the clip, so I predict the median ratio max₁₀/max₁ **exceeds 2** (in [2, 10]) unless
   most ships saturate their a-range within 200 periods — from the smoke run's fast initial
   diffusion I estimate half the ships are still exploring. If the median ratio > 2 the
   composite **false-fails the bounded control on the real harness** (the checker's attack d,
   now measured), and the ratio clause must be re-derived (candidate: ratio judged against the
   fraction of the band explored, or the ratio clause replaced by cap-only at a longer horizon).
   If it passes, median ratio lands in [1.2, 2.0].
4. **compound FAIL via the ratio clause** (walk in encounter count: median ratio ≈ √10 ≈ 3.2,
   in [2.5, 4.5]); the cap clause misses it (cap 1.3e-5 ≫ expected max ~2–4e-6 at 10×).
5. **drift FAIL via the ratio clause**: the real Dormand–Prince drift at rtol 1e-12 (nothing
   holding the constant) grows with step count, ratio in [2.5, 13] (√10 if roundoff-random,
   ~10 if biased). If instead it stays bounded on this scene (ratio ≤ 2) the composite misses
   drift and the claim is broken — I consider that unlikely (< 10%).
6. **kick FAIL** on every clause (err 0.22 at 1× already ≫ cap; ratio ~35).
7. **Leak floor**: with the cap degenerate to the AXIS_CLIP, detection rides the bounded
   component, not the cap: leak(e) is caught iff e·|walk|₁₀ ≳ 2·max₁(bounded) ≈ 1e-6–4e-6 with
   |walk|₁₀ ≈ 20–40 → floor e* ≈ 3e-8–1e-7. Predict: 1e-7 FAIL (caught), 1e-8 PASS (missed),
   3e-8 and the 4e-8 seed panel mixed — the floor verdict is seed-fragile at its edge, exactly
   as the checker found on the synthetic.
8. **The dossier's floor scaling does not transfer**: "a leak is caught when its accumulated
   error exceeds ~5 % of the cap, floor ~ cap/√(encounters·H)" was derived against the
   synthetic's 5·(R_H/sep) closed band. On the real scene the cap is the AXIS_CLIP and the
   binding comparison is against the bounded law's own error, so the floor is set by
   2·max₁(bounded)/|walk|₁₀, not by the cap. The scout's headline floor formula is therefore
   wrong on the real harness even if every verdict lands right.

Machine: one Linux x86 runner (8 vCPU shared, other runs in the window); single machine — the
checker's "two machines" clause is NOT covered here and stays open. Timings are orders of
magnitude only.
