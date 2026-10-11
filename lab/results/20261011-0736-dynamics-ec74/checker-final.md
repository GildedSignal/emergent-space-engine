Working...
Check complete. `check.md` written to the run folder; nothing else touched, scratch removed, no git commands run against history.

**Grade: silver.**

**Reproduced bit-exact** — `sweep_final.py` in a clean copy, 65.5 s, every dossier number matched (λ 6.7e-5/6.0e-4/0.35, Fano 0.98→2186, both controls); `predictions.md` timestamps (07:58:04) precede the decisive run (07:58:43+). The self-voided first sweep is honestly kept.

**Adversarial findings:**
1. **RK4 control script missing from work/** — I rebuilt it: the b<3r_H domain rule holds and is *understated* (toy/RK4 1.05–1.25 inside r_H; 2.4→**19×** wrong outside, vs the reported 1.8–5.5).
2. **Gas regime seed-robust** (λ 7–8e-4, Fano≈1, σ_e flat on seeds 1–2); burst-regime *existence* robust on all 3 seeds, but the "18× birth burst" **inverts on seed 2** (0.084→0.571) and S=64→128 flips the strong count **44×**.
3. **The twin instrument is broken**: `run_pair` never folds angles to (−π,π] (D[0]=π from a 1e-9 perturbation) and leaves the final element as `np.empty` garbage (2.29e160; the author's own D_final=7.98e-321 is a denormal). P1's "no divergence / caches stay valid" is an instrument artifact — my run suggests order-unity twin separation by ~50 orbits at 3e-4.
4. Kepler round-trip 1e-15 ✓; Fermi map arithmetic (ships 2e-6, belts 2e-9) ✓; Fano exponent is w^0.73–0.91, not w^1.1.

**Why not gold:** the deletion headline outruns its measurement — nearest measured point (Ψ=3e-6) sits 10² above the author's own deletability line off 2 events; ships are only ~3× below it. **Gold experiment:** Ψ=1e-6 with real statistics (N≈3000, T≈300, ~10²–10³ events) plus the formation's true σ_e, an S-convergence certificate for the capture regime, and the D-metric fix. Also flagged: filling co-varies with Ψ along their sweep, so the regime boundary needs filling as a second axis.
