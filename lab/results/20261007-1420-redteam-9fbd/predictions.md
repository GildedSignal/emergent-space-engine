# Predictions — 20261007-1420-redteam-9fbd

Written **before** the decisive run (`falsifier.py`, float64, one process, < 60 s).

**Attack.** Premise 2/5 seam of `docs/representation.md`: "Light is the same equation without the M/L² term" (Binet band cells) feeding "Lensing adds crossings, from each doll's memoized deflection(b)". Every gate that judges light deflection (r1 `defl`, law gate B3, B16) draws b log-uniform in [10, 1000] = [1.92, 192]·b_crit with b_crit = 3√3 M ≈ 5.196M. But the player-visible strong-field images — the photon ring, every secondary image, every k-loop image — have b ∈ (5.196, ~6.5)M. The band law has never been measured there. The falsifier integrates r1's exact frozen band rule for light (u″ + (1 − 6u_k)·u = −3u_k², u and u′ continuous across bands, u_k at the band's geometric centre, bands r_k = 2^(k/m)) against the exact null Binet equation u″ + u = 3Mu², at m ∈ {16, 32, 64}, plus the same comparison for massive-orbit precession at p < 10 (r1's bound sampler draws p ∈ [10, 1000] only).

## Pre-registered expectations (not tuned on)

- **P1 (r1's edge must reproduce).** At b = 10 (b/b_crit = 1.924, α ≈ 0.56 rad), m=16 deflection error < 1% — r1's `defl` criterion passes at its own sampled edge. Control on the passing side.
- **P2.** At b/b_crit = 1.2 (α ≈ 1.8 rad): m=16 relative deflection error > 3%; m=32 > 1.5%.
- **P3 (the ring).** At b/b_crit = 1.05 (α ≈ 2.4 rad): m=16 error > 20%; m=32 > 10%.
- **P4 (capture intact).** No capture misclassification for b/b_crit ∈ {1.003 … 1.924} (all deflect) nor for b/b_crit ∈ {0.9, 0.97} (all captured), at any m — consistent with r1's `capture` result. The failure is deflection, not classification.
- **P5 (massive, below the sampler).** Circular p = 12, e = 0.5 orbit (inside r1's sampled regime): m=16 precession error < 1%. Circular p = 7 (outside; near-ISCO, precession ≈ 10.3 rad/orbit): m=16 error > 2%.
- **P6 (mechanism).** Error(m=32) ≈ Error(m=16)/2 — first order in band width, confirming it is the band lumping and not an integrator artifact.

## Held out for the checker (never run by me before submission)

b/b_crit ∈ {1.5, 1.1, 1.02, 1.01}; massive (p=8, e=0.3) and (p=20, e=0.5); m=64 at all b.

## Kill criterion for my own claim

If m=16 deflection error stays < 1% for all b > 1.05·b_crit **and** precession error < 1% at p = 7, the premise survives at the ring and this dossier reports a surviving premise, not a wound.

## Honest risk

r1's m16 passed 1% precession on 256 seeds where my back-of-envelope predicted 1–2% band-edge error (errors partially cancel across in-out crossings; the piecewise linearization is second-order accurate per crossing). The same cancellation may hold near the photon ring. Either outcome is reported.
