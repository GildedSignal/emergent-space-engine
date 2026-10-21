# Predictions — 20261021-1443-dynamics-99d7

Written before the ladder. All on `beltzone STEP PERIODS 6 CLASS`, 100 planet periods,
B12's frozen bar: worst |ΔJacobi|·r0 ≤ 1e-4. The census (ddeb) priced the composed desync
headroom at 78× conservative, 90× if the bridge certifies at 16/planet-period, 170×+ if the
3:1 zone bodies hold at 64; these runs pin which.

## P1 — controls (instrument identity)
- `strong` step 5: worst Jacobi ≈ 1.8e-5 (cbe6 to the digit); step 4: the cliff arrives as
  deaths (2/6 on cbe6's draw). If the strong control does not reproduce, the run is VOID.

## P2 — clean belt at the plane's e-law
- `belte` step 4 (16/planet-period): PASS, worst 2–4e-5 (cbe6 checker2's e-draw arm read
  3.2e-5). The e-law alone does not move the clean floor.

## P3 — the bridge (5.4–6.3 Hill, unflown interior geometry)
- `bridge` step 4: PASS. The tide is (6.3/5.4)³ ≈ 1.6× the certified 6.3–8.8 draws, and
  cbe6's step-4 margin was 10×, so I expect worst 2–6e-5: the bridge floor is 16 and the
  census's 64 there is 4× over-provisioned. Fail shape if wrong: step 4 fails, step 5-6 passes.

## P4 — the 3:1 zone at the belt's e-law (decisive)
Prior (probability): fails 4, fails 5, holds 6 (0.45); holds 5 (0.2); holds 4 (0.15);
needs 8 (0.15); no passing octave to 8 / deaths (0.05).
- Mechanism prediction: at a failing octave the zone's worst Δe is ≥ 10× the clean arm's at
  the same step (conjunction aliasing drives the resonant e-pump coherently; the certificate
  that moves with the step is the aliasing, not the pump), and at the passing octave φ
  (= 3λ_p − λ − 2ϖ) shows structure (|mean e^{iφ}| above the clean arm's) — the fine grid
  resolves libration, the coarse one smears it.
- Held-out: seed 2 (fresh zone draws) at the floor octave; horizon 400 periods at the floor
  (cbe6's checker held 4× the horizon); if the zone holds 4, the census's 256-floor for zone
  bodies is 16× over-provisioned and the headroom sentence moves to ≥ 90× regardless.

## What kills what
- Zone failing every octave ≥ 4× finer than clean (needs 256, i.e. ddeb's conservative
  choice exact): headroom stays 78× — the 17.8% tail pays the full 256 bill it was priced.
- Bridge failing 16: the 41% bridge class keeps its 64 → headroom stays ≤ 78× and the
  optimistic 90× bracket dies.
