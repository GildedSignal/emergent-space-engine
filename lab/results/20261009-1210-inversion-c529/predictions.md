# Predictions (written before the held-out run; controls C1/E0 already run)

Certificate under test: partner rank in mean longitude at t=0 (symmetric min), k=4, the gold
20261006-0346's claim, as specified for the build in `lab/lenses/b-coorbital-cert.md`.
Instrument: `inversion heldout` (truth = per-pair conservative advancement over the radial
superset; controls passed: C1 miss(k=4)=0, k*=4, reproducing the gold).

Tuned on: C1 (gold scene shape) and E0 only. Everything below is held out.

## P1 — H1 (same fleet as C1, horizon 500 instead of 50 orbits)

Mechanism: orbital shear sweeps mean-longitude differences by 3π·(Δa/a)·H ≈ 0.47 rad
(= 22 spacings of a 300-ring). Encounter partners' rank at t0 spreads over the swept band.
- k_star ≥ 15.
- miss(k=4) between 20% and 80% of encounter events.
- silent_swaps ≈ 320 (they were 32 at H=50; order churns without encounters even in-regime).
Claim tested: "rank 4" is a horizon artifact, not a law of the clump.

## P2 — E1/E2 (equal exact periods, sigma_e 1e-2 / 3e-3, order frozen forever)

Mechanism: epicycle wobble (radial ±ae, tangential ±2ae) lets true positions approach with
Δλ up to ~2(e_i+e_j) ≫ rho; no re-rank cadence can fix a wrong partner set when order is frozen.
Fork, stated honestly:
- (a) kill: enc ≥ 100 and miss(k=4) > 5% with k_star > 4, or
- (b) self-suppression: enc < 50 (encounter needs near-matched epicycles), reported ambiguous.
My expectation: (a) for E1, and E2 in between (miss > 0 but smaller).

## P3 — B1/B2 (belt n=1000, a-spread 1e-2, sigma_e 1e-2 / 3e-4, 20 orbits)

Mechanism: shear 0.094 rad/orbit × 20 orbits = 300 spacings. Outside the certificate's intended
domain — this pins where the domain ends and whether sigma_e or a-spread rules it.
- B1 and B2 both: miss(k=4) > 80%, k_star > 100 (a-spread, not sigma_e, dominates).
- B1 silent_swaps / enc_swaps > 50 (encounter-less churn at belt scale).

## P4 — M1 (fleet + 20 crossing rogues, tau_band = 0.94 vs C1's 1.00)

- cross encounters (fleet×rogue) between 10 and 200; ≥ 95% of them missed by wholesale
  λ-rank-4 (cross_enc_rank4_and_cone ≈ 0), because a rogue's rank at t0 is unrelated to where
  it crosses the ring.
- 100% of cross encounters are Binet-cone candidates (cross_enc_cone = enc_cross): composition
  (rank intra-clump + cone for the rest) loses nothing.
- Any concentration threshold that fires for C1 (tau=1.00) fires for M1 (tau=0.94): a
  population-level trigger cannot gate the tier choice; the classification must be per pair.

## Kill criteria for my own claims

- If H1 has k_star ≤ 6 or miss(k=4) < 5%: the horizon law is wrong; the certificate is more
  robust than shear predicts. I would look for why before claiming anything.
- If M1's cross encounters are mostly λ-rank-4 at t0: the trigger-blindness claim dies.
- If E1/E2 show miss(k=4) = 0 with enc ≥ 100: the epicycle-amplitude assumption is false; the
  certificate is robust to station-keeping spread in equal-period formations.
