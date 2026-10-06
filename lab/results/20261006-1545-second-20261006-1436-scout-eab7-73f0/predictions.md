# Predictions (written before the sweep; only rg=0 4-epoch sizing pilots ran)

Setup: same two arms as the scout run (baseline per-kick re-setup vs skin slack 0.5, widen 2.0),
driven by the law's own kick stream: 32 kicks/orbit (H0190 cadence), each body's apsidal line
advancing at its own compiled ϖ̇(a,e) = 3n·rg/(a(1−e²)) [1PN] + ϖ̇_tide [numerically
double-averaged exterior perturber μ_p=1e-3 at a_p=5.2, validated to 7% against (3/4)nμ_pα³;
prograde]. a, e, period, tp are invariant (axisymmetric secular dynamics), so the Binet drift is
a pure rotation of each body's (V, W) at radius e/p — the systematic shear the scout run's random
walk understated. rg=1e-2 → GR precession ≈ 0.19 rad/orbit (11°/orbit); rg=1e-4 → 1.9e-3 rad/orbit;
rg=0 → tide only ≈ 3.6e-5 rad/orbit (the solar-belt-like case).

Expected cache lifetime (validity is per body vs its own snapshot):
τ ≈ slack·eps_u / ((e/p)·ϖ̇) = slack·eps_u·32 / ((e/p)·g_per_orbit), with eps_u ≈ 0.02–0.03,
e/p ≈ 0.105 (belt σ_e 0.1), 0.021 (tang σ_e 0.02), 0.05 (coorb σ_e 0.05):
- belt: τ(rg=1e-2) ≈ 22 epochs, τ(3e-3) ≈ 73, τ(3e-2) ≈ 7, τ(1e-4) ≈ 2200, τ(0) ≈ 1.1e5
- tang: τ(1e-2) ≈ 77; coorb: τ(1e-2) ≈ 29.

| Case | Setup (scene n=120, ρ 0.01, seed 4242 unless said) | Prediction |
|---|---|---|
| B0 | belt, rg=0 (tide only), 64 ep | repairs=0 (τ ≫ 64), misses 0, extras small; cut = horizon 64× |
| B1 | belt, rg=1e-2, 128 ep | repairs ≫ 0, lifetime ≈ 15–35 epochs, **misses = 0**; setups/kick cut ≈ τ ≥ 10×; skin run_evals ≈ 1.9–2× baseline |
| B1b | B1, seed 777 (held out) | same |
| B2 | belt, rg=3e-3, 128 ep | lifetime ≈ 50–110 epochs, misses 0, cut ≥ 10× |
| B3 | belt, rg=3e-2, 64 ep | boundary: τ ≈ 5–10; misses may appear (q-skin's window-width term under tangential drift) — either outcome reported as boundary mapping, not as failure |
| B4 | belt, rg=1e-4, 64 ep | repairs=0 (τ ≈ 2200), misses 0; cut = horizon; mechanism number is τ, not the horizon ratio |
| G1 | tang σ_e 0.02, rg=1e-2, 128 ep | τ ≈ 60–100, **misses = 0** (the tangential geometry is where q-skin's slack broke) |
| G1b | G1, seed 777 (held out) | same |
| G2 | tang, rg=3e-2, 64 ep | boundary as B3 |
| O1 | coorb σ_e 0.05, rg=1e-2, 64 ep | τ ≈ 20–40, misses 0 (Full sections: timing set by period spread, unchanged by the stream) |
| O2 | coorb, rg=1e-4, 64 ep | repairs=0, misses 0 |
| N1 | negative: belt rg=1e-2, slack 0.5, **widen 0**, 64 ep vs B1's truth | **misses > 0** (stale windows under systematic drift); if misses = 0 the miss detector is insensitive → VOID |

## Kill criteria (pre-registered)

1. Any miss > 0 at rg ≤ 1e-2 on any scene: the slack-0.5/widen-2 pairing is unsound under the
   law's own stream → the scout run's claim does not transfer; killed.
2. Setups-per-kick cut < 10× at rg = 1e-2 (τ < 10): the mechanism does not pay at the plane's
   real cadence; killed as a lever.
3. N1 misses = 0: comparison insensitive → VOID.
4. Skin run_evals blow-up (≥ 5× baseline, wall ratio ≥ 1): widening overhead eats the saving.

## What the horizon confound should resolve to

The scout run's 8× was its horizon (8 epochs, zero repairs). Here the mechanism number is the
measured mean cache lifetime in epochs (cache_hits/repairs) at rg where repairs occur, and the
horizon ratio is reported only as a lower bound where τ exceeds it (B0, B4, O2).
