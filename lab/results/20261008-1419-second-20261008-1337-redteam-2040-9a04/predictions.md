# Predictions (written before the decisive runs falsifier2.py / validate_oracle.py)

The checker's named experiment, done here: the E axis (every original case had
dE = 0), the escape-side crossing with a completed predicate, and the shipped
RK4/Binet validation. Anchors already on record and NOT held out for me: the
original run's P1–P5 (reproduced bit-for-bit above), and the checker's
measurements D1 (T_t 1.15e-3 at dE/E=1e-4 weak field), D2 (plunge-via-E at
dE=+1e-3, L=L_sep·1.001), D3 (escape fabrication, Δφ 6.55, T_t 89,621).
Everything else below is a genuine prediction. Physics I derived myself before
running: near parabolic T_t ∝ (1−E²)^(-3/2) gives relerr(T_t) ≈ (15/8)·(dE/(1−E))²
on the E axis (weak field); the plunge separatrix tilts at dL_sep/dE ≈ 18 near
E = 0.97, so a +E kick at fixed L moves toward plunge; the capture threshold for
E ≥ 1 is L_crit(E) (4.037 at E=1.005), so kicks past E=1 with L < L_crit plunge
rather than escape.

- E1 (dE/E = +1e-4, weak field from_band(50,200), anchored on D1):
  relerr(T_t) ∈ [8e-4, 2e-3]; relerr(Δφ) stays ~1e-9 (the Δφ map is nearly
  E-flat; T_t carries the whole E response). PREDICTION: the 1% band holds on
  both components, but the T_t error sits ≥ 5 orders above the matched dL kick
  (9.7e-12): the stored-derivative certificate must be per-axis.
- E2 (dE/E = +1e-4, strong field p=12, genuinely blind): relerr(T_t) ∈ [1e-6, 2e-4]
  (Kepler-curvature estimate 3e-5, separatrix-tilt contribution ~5e-6). Band holds.
- E3 (E-scan at weak field, f = dE/(1−E) ∈ 3e-3…0.3): relerr(T_t) ≈ C·f² with
  C ∈ [1, 3] (Newtonian 15/8); slope of the log-log fit 2.0 ± 0.1; the 1% band on
  T_t breaks at f* ∈ [0.04, 0.12]; relerr(Δφ) ≥ 100× smaller than T_t everywhere.
- E4 (scale-free: from_band(100,400), 1−E halved, same f): errors agree with E3
  within a factor 2 at every f (exponent universal, prefactor drifts with field).
- E5 (plunge-via-E, anchored on D2): truth plunge; the multiply-add fabricates
  Δφ ≈ 19.5, T_t ≈ 613 (±5%); predicate3 says plunge (correct), and so does the
  original is_bound (its failure mode is only on the escape side).
- E6a (escape: weak-field orbit kicked to E=1.02, anchored on D3): truth escape;
  fabricated Δφ ∈ [6.4, 6.7], T_t ∈ [5e4, 1.5e5]; the original is_bound returns
  True for this hyperbolic orbit (wrong); predicate3 says escape.
- E6b (E=1.005 with L=3.996 < L_crit): truth PLUNGE, not escape — E ≥ 1 does not
  imply escape; both predicates say plunge here.
- E6c (E=1.005 with L=4.2 > L_crit): truth escape just above the barrier;
  predicate3 escape; original is_bound wrong again.
- V1 (RK4-Binet vs quadrature at p≈80, shipped): relerr(Δφ) < 1e-6 and
  relerr(T_t) < 1e-6 at 400k steps, with the 200k/400k Richardson difference
  consistent with 4th order (the dossier's "2e-4" was a coarse-step bound, not
  the oracle's true accuracy).
- V2 (DOP853 proper-time periods): Δφ and T_t agree with the quadrature to
  < 1e-7 on weak, strong and near-separatrix seeds (independently re-confirming
  the checker's 2.5–5.3e-6 as an upper bound).
- V3 (tri-predicate vs independent grid truth, ~3.7k samples): zero
  disagreements outside the margin; margin exclusions (near-double roots,
  |1−E| < 5e-6, band pericentre within 1e-4 of 2M) ≤ 3% of samples.
- V4 (11 integrated orbits incl. the E5 kicked invariants): predicate3 =
  integrated behaviour = expected class, 11/11.

What would falsify the adoption claim: an E-axis error below the L-axis at
matched kick (cheap path safer than thought), a predicate disagreement with the
grid truth or an integrated orbit (criterion not complete), or the fabricated
cycles being somehow benign (they are not, if V4 holds).
