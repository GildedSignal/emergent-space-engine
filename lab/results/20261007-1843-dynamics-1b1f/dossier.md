# Dossier — 20261007-1843-dynamics-1b1f (lens: dynamics and attractors)

**Claim.** A stirred belt's encounter load is not stationary: it flows — from cold or hot
start alike — to a load attractor of about 0.1 encounters per body per orbit on a
stirring timescale t_stir that falls with body mass (measured 300–400 orbits at
m/M* = 1e-6, > 400 at 1e-7, ~150 at 1e-5), while the arrival process itself stays
near-Poisson (Fano 1.1–1.5); the pure-geometry encounter rate obeys an area law
(rate ∝ R_cap^2.0, ∝ N^0.9), so capture-radius cost grows quadratically and a belt's
encounter budget must be scheduled as a drifting mean, not a static program value.

**Bottleneck.** The board's top scaling risk (candidate work must track real
encounters) and bottleneck 4 (smoothness/allocator tails). q-candidate-degree froze
the belt and measured work per real encounter; this run measures what the real-encounter
*rate itself* does over game time. Gain: an order-of-magnitude law where the static
view is wrong by ×2 per t_stir, plus the validity horizon of the belt-as-program
(B18b, `components-98bc`: 0.126 bits/body) — the stirring rate de/dt is the scar-layer
accumulation rate PRINCIPLES 6 anticipates ("influences below one quantum accumulate").

**Evidence** (all Linux/x86 cloud, orders of magnitude only; model: planar Kepler
epicycles around one M*, elastic hyperbolic deflection at each conjunction b < R_kick,
`stir.py`; encounter := b < R_cap; hot belt N=300, W=0.08, Rayleigh e σ=0.05 unless
stated; T=400 orbits; 3 hot seeds, 2 cold seeds):

| run | m/M* | F=μ/(R_cap v²) | start | rate early→late (/body/orbit) | a_std 0→F | e_mean 0→F | Fano | fate |
|---|---|---|---|---|---|---|---|---|
| g1 | 1e-4 | ~27 | hot | 0.011→0.008 (peak .043 @14) | .04→.97 | .07→.35 | 0.9 | destroyed, decays |
| g2 | 1e-5 | ~2.7 | hot | 0.030→0.103 | .03→.07 | .06→.16 | **2.5** | survives, burstiest |
| g3/g5/g6 | 1e-6 | ~0.27 | hot | .054–.058→.099–.104 | ~.023→.033–.037 | .06→.08–.09 | 1.3–1.5 | converging up |
| g4 | 1e-7 | ~0.03 | hot | 0.067→0.073 | .023→.024 | .061→.062 | 1.1 | frozen |
| g12/k17 | 1e-6 | 0.27 | **cold** (σ=1e-4) | .058–.061→**.107/.110** | .024→.039–.041 | .001→.064–.066 | 1.3–1.4 | reaches hot attractor |
| k15 | 1e-5 | 2.7 | cold | .033→**.105** (hot g2 late: .103) | .026→.079 | .003→.167 | 2.2 | same attractor |
| k16 | 1e-7 | 0.03 | cold | .089→.087 | .023→.033 | .0003→.024 | 1.2 | still stirring at 400 |
| g7 | 1e-6 | — | **control, kicks off** | .046→.049 flat | frozen | frozen | 1.1 | instrument |
| c8/c9 | — | — | control, kicks off | R_cap 1e-3/1e-2 | frozen | frozen | — | geometry |
| c10/c11 | — | — | control, kicks off | N=150/600 | frozen | frozen | 1.0/1.4 | geometry |

- **Attractor:** cold and hot starts converge to rate ≈ 0.10 ± 0.01 per body per orbit
  for F ∈ {0.27, 2.7} (5 runs); still rising at orbit 400, so 0.10 is the value at the
  horizon, not a proven fixed point. Stirring rate de/dt (orbits 50–400, cold):
  1.1e-5 (m=1e-7), 7.0–7.6e-5 (1e-6), 2.3e-4 (1e-5) per orbit — sublinear in m (~m^0.5–0.8).
- **Area law:** frozen-geometry rate ∝ R_cap^2.00 (1e-3→3e-3 and 3e-3→1e-2) and ∝ N^0.89
  (150→600 at fixed W). With kicks on the same sweep reads 2.3–2.9: dynamics amplify it.
- **No cascade:** Fano stays 1.0–1.5 in every surviving regime, against a 1.0–1.4 frozen
  control; only the transitional m=1e-5 reaches 2.5. The violent F=27 belt destroys
  itself in ~30 orbits and its load then *decays* to 0.008 — ruin is self-limiting.
- Detection robustness: K=16 vs K=8 changes counts 0.8 % (g14 vs g3), consistent with
  the phase-neighbour rank-4 certificate (gold 20261006-0346).

**Commands** (each run is a one-liner; full grid `./grid.sh` ≈ 8.5 min, `./grid2.sh`
≈ 2 min, then `python3 analyze.py`):
```
python3 stir.py '{"n":300,"W":0.08,"sig_e":0.05,"m":1e-6,"R_cap":3e-3,"T":400,"seed":1,"tag":"g3"}'
python3 stir.py '{"n":300,"W":0.08,"sig_e":1e-4,"m":1e-6,"R_cap":3e-3,"T":400,"seed":2,"tag":"k17"}'
python3 stir.py '{"n":300,"W":0.08,"sig_e":0.05,"m":1e-6,"R_cap":3e-3,"T":400,"seed":1,"tag":"g7","kicks":false}'
python3 analyze.py g1 g2 g3 g4 g5 g6 g7 g8 g9 g10 g11 g12 g13 g14 c8 c9 c10 c11 k15 k16 k17
```

**Predictions** (`predictions.md`, written before the grid): P1 half-wrong (F* for
survival lies between 2.7 and 27, and m=1e-5 survives, heated); P2 wrong in the
interesting direction (rate is not flat: +80 % over 400 orbits even at F≈0.27); P3 held
(0.19 < 0.3 decay); P4 half-wrong (burstiness peaks transitional, not violent);
P5 instrument rejected (Φ ≈ 2.0 on the frozen control — the estimator, not the physics,
is clustered; Fano-vs-control is the honest statistic); P6 wrong: exponent 2.0, not 1
— an area law, the sharpest surprise; P7 half-wrong (m=1e-6 *does* stir itself to the
attractor inside 400 orbits; only m=1e-7 stays near-program). Five of eight bands
missed — the held-out cases are where the findings are.

**What would make it wrong.** Planar 2D (3D inclinations cut conjunction rates by the
scale-height factor — the attractor value and area law survive, the constant will not);
impulse-at-conjunction (exact hyperbola, no tidal term — marginal at m=1e-7 where
R_cap ≈ R_H); no ejection sink (1 body total); 400-orbit horizon cannot prove the
fixed point. A checker should rerun k17 with T=800 and sig_e=1e-4 and 3D inclinations
before adopting any constant; the *laws* (∝ R_cap², ∝ N, cold→hot convergence,
Poisson arrivals) are the adoptable part.

**Cost of adoption / fit.** No engine code changes; this sizes three contracts:
(1) the belt's scar budget (de/dt is the scar-accumulation rate), (2) the allocator's
encounter budget as a *drifting* mean (recompute per belt per t_stir; ×2 error if
static), (3) the encounters skin: cost ∝ R_cap² argues for the thinnest skin the
miss-rate tolerates. PRINCIPLES 4 "regimes are chosen by dimensionless numbers" — F
is that number for belt encounter dynamics; PRINCIPLES 21 "rough first, refine when a
certificate could break": the belt program's certificate horizon is t_stir.

**The lens may have missed:** single-belt, single-star; no resonance structure (keys=1
discrete-period belts, r8 v2's Diophantine conjunction structure, would couple phases
and could restore burstiness the random-phase belt lacks); no player (a fleet parked in
the belt changes the local F by its aggregate mass — PRINCIPLES 6's "ships' aggregate
mass can become a source" would move a local patch across the F threshold in hours).

**Reproducibility note.** A same-seed rerun (T=100) matches g3's first 100 orbits to
1746/1747 encounters (0.06 %): one conjunction-cooldown boundary event flips. The map
is a float exploratory instrument (floats explore, integers decide), so the *laws*
above are the deliverable, not any single count; per-orbit rate series agree to <0.1 %.
