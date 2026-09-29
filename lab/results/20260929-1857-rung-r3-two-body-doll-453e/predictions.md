# Predictions (written before the decisive 256-binary / 64-flyby / 100-handoff runs)

Calibration used only 5 spot cases (p,e,nu in {20,100,450,1000} x {0,0.2,0.3,0.6} x {0.01..0.25});
nothing below was tuned on the 256 sampled seeds.

## eob-doll (candidate)
- precession: doll advance exceeds the 1PN oracle by a clean 2PN term ~ 8/p relative
  (measured +0.8% at p=1000, +8% at p=100, +69% at p=20, e=0.6). The 1% gate therefore
  passes only p >~ 800. With p log-uniform in [20,1000], predict
  precession_pass_fraction ~ 0.05 (fails >= 0.99): the exact-Schwarzschild EOB map is
  only 1PN-faithful; below p~800 the resummation's 2PN content dominates the gate.
- period: doll-oracle period error is 2PN-sized (~e-6 at p=1000, ~3e-4 at p=100, ~1.5e-2
  at p=20). Truncation-exclusion (>0.05%) should remove p <~ 100-150 (30-45% of cases);
  among the rest predict period_pass_fraction ~ 1.00.
- nu: the energy-map F=sqrt(1+2nu*x) timescale is exact 1PN; contamination is nu*2PN.
  Predict nu_effect_pass_fraction in [0.85, 1.00]; unsure whether small-p cases fail 10%.
- handoff: with per-encounter reference re-initialisation (resonant chaos would otherwise
  confound the metric; see dossier), errors are per-segment, predict exponent ~ 0 (< 0.2),
  per-exit |dE/E| ~ 1e-6..1e-4.
- assist: patched conics with a moving planet, error sources are the neglected star tide
  inside the SOI and the neglected planet pull outside it (~ b/(2 SOI) ~ 0.17 at b=50 R_p
  before cancellations). Predict assist_pass_fraction ~ 0.8-1.0, hardest at large b.
- events_per_orbit = 0 (generators only, no kicks/handoffs per binary radial period).

## test-mass (negative)
- precession: advance uses m1 instead of M -> deficit (1 - m1/M) >= ~1.005% even at
  nu=0.01, plus the same 2PN excess. Predict pass fraction ~ 0.
- period: Keplerian sqrt(M/m1) bias 0.5-25% >> 0.1%. Predict ~ 0.
- nu: only the m1(nu) mass scaling, not the 1PN nu term -> wrong size (and possibly
  sign) -> predict ~ 0.

## newton-doll (negative)
- precession: advance = 0 -> 100% error -> pass fraction 0.
- period: missing 1PN correction ~ 3/a (0.3%..15%) -> pass fraction ~ 0.
- nu: no nu dependence at all -> pass fraction 0.
- handoff/assist: patched conics are its own law; expect same as eob there.

## Verdict expectation
Candidate killed by `prec` (and marginally by nothing else); negatives fail exactly the
gates they were built to fail. The rung's real finding: the one-doll-per-mass EOB map is
1PN-faithful only above p~800 M; below that the gate needs either a 2PN map or a larger
p floor.
