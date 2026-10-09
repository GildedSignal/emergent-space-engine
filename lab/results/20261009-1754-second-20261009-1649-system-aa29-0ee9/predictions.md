# Predictions (held out)

Frozen before any held-out run was simulated or evaluated. Calibration =
`data/calib.json` (mu 1e-3, e0 0.02, [1.32,2.08]), `data/calib_o23.json` (mu 1e-3,
e0 0.02, order-2/3 dense window [1.55,1.85]), `data/calib_e010.json` (mu 1e-3,
e0 0.10, [1.32,2.08]). All three at T=512, n=300, two phases, 600 seeds.

Frozen from calibration only, shipped in `gate2.py` (one constant set each,
quoted verbatim here — gate2.py == predictions.md == dossier):
- LOCK judge: lockR = max(R1, R2), R_k = |mean exp(i k psi)| over conjunction
  phases, NO linear detrend; LOCK iff lockR >= 0.90; chaos = a_drift > 0.05
  excluded and counted separately; pos = (FAIL_pump or LOCK) and not chaos.
- F1 (frozen per-order constants, run 1649's needed form): K = {1: 0.100,
  2: 0.110, 3: 0.093, 4: 0.070} (pooled zero calibration misses).
- F2 (response-scaled): K_o(mu,e0) = K_o^0 (mu/1e-3)^(2/3) (e0/0.02)^gamma_o,
  K^0 = {1: 0.100, 2: 0.0696, 3: 0.0147, 4: 0.0696}, gamma = {0, 0.278,
  1.157, 1.157}, from per-run zero-miss boundaries at e0 in {0.02, 0.10}.
- Calibration reference points (measured, not predicted): F1 on calibration
  recalls 0.96-1.00 of pos but flags 68-80% of non-chaotic seeds (precision
  0.06-0.40); order-1 boundary is e0-robust (0.088-0.100 across e0 x5),
  order-2/3 boundaries move x2.1/x6.3.

Held-out runs (not yet simulated): H1 mu 3e-4 e0 0.02, H2 mu 3e-3 e0 0.02,
H3 mu 1e-3 e0 0.05, H4 mu 3e-4 e0 0.10, H5 mu 3e-3 e0 0.10, H6 mu 1e-4 e0 0.02;
all [1.32,2.08], n 300, T 512.

1. **F1 recall (the claim's headline under one set).** F1 recalls >= 0.95 of pos
   on non-chaotic seeds in all six held-out runs — its constants cover the
   widest (e0 0.10) responses, so lower-mu/e0 runs shrink inside them. F1's
   cost: it flags >= 0.50 of non-chaotic seeds in every held-out run.
2. **F2 transfer.** F2 accuracy beats F1 accuracy by >= 5 points at mu <= 3e-4
   (H1, H6). At (3e-4, 0.10) (H4) F2's extrapolated order-2/3 constants are too
   narrow (gamma fitted only between e0 0.02 and 0.10 at mu 1e-3): F2 recall
   lands 0.75-0.95, below F1's.
3. **F2 recall floor.** F2 recall >= 0.90 in H1, H3, H6 (mu <= 1e-3, e0 <= 0.05).
4. **No cliff, both sides quantified.** In every held-out run the pos fraction
   among non-chaotic seeds in the F2 shell [K, 2K) is <= 0.08, while in
   [0.5K, K) it is >= 0.15: a fat inner shoulder and a thin outer tail — a
   slope over a factor ~2 in gate coordinate, not a boundary.
5. **Lock judge validity (the separation the checker named).** Lock-only seeds
   (island interiors: locked, not pumping) exist and lie inside the gate: F2
   recall of LOCK >= 0.95 in every run. At e0 = 0.02 the order >= 2 LOCK count
   is 0 (no subharmonic islands at low e; the 5:3 FAILs are pure forced-beat
   cusp), while at e0 = 0.10 order >= 2 interiors do lock. Lock never appears
   on the plateau (x > 2K everywhere).
6. **FP cost, the missing number.** Owned fraction (flagged under F2, union
   chaos) is monotone in mu at e0 = 0.02: <= 0.15 at mu 1e-4 (H6), >= 0.55 at
   mu 3e-3 (H2, chaos ~0.40 included).

What would make the claim wrong: if F2 recall of pos collapses below 0.90 at
mu <= 1e-3 (the mu^(2/3) width law is wrong even as a response scaling), the
CF pass does not carry the gate even with response-scaled constants, and
law.md's compiled-frequency detector keeps its job. If P5 fails (lock outside
the gate, or order-2 islands at e0 0.02), the conjunction rotation does not
read the resonance structure and the unification is dead, not just unthresholded.
