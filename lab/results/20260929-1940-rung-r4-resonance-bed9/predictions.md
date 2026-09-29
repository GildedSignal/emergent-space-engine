# Predictions (written before the decisive metric runs)

Setup already validated (not tuned on the cases' outcomes): truth converged
(maxe1 and conc stable 600->1200->2400 to <0.1%); kick-integral quadrature
GL24 = 4xGL48 to 8 digits; `averaged` C1 precession 9.0028e-5 vs classical
quadrupole 9.0000e-5; truth C1 precession 1.09e-4 (+22%, consistent with
octupole-order corrections at a1/a2 = 0.34). Truth numbers known to me:
R1 maxe1 0.1570 conc 0.4611; R2 maxe1 0.1735 conc 0.5136;
C1 0.01030/0.0254; C2 0.01245/0.8186; C3 0.04414/0.8739.

I have NOT yet looked at any candidate-layer metric on any case (the earlier
conjunction-finder numbers were corrupted by a since-fixed wrap bug and I
discarded them). Predictions:

1. conj-quad over-pumps R1: e_pump_ratio in [1.4, 2.2]. Reason: at a1/a2 =
   0.63 the l=2 truncation overweights the m=2 synodic harmonic that drives
   the 2:1 eccentricity term; the full field's l>=3 terms partially cancel it.
   Its R1 libration ratio < 0.6 (phase decoheres while over-pumping).
2. conj-oct tracks R1/R2 better: e_pump_ratio_min >= 0.8 and max <= 1.35
   (borderline against the 1.25 gate), libration_ratio_min in [0.6, 1.1].
3. averaged: e1 stays at 0.01 -> pump ratio ~0.06 (R1) and ~0.058 (R2), and
   psi circulates at 2n2-n1-varpidot -> conc ratio < 0.4. Fails pump and lib.
   It also fails C3 (law 0.01 vs truth envelope 0.044).
4. none: same pump ratios as averaged's e; conc ~0.02-0.1 -> fails pump, lib;
   ctrl 2/3 (passes C1 and C2, fails C3).
5. Controls for the conjunction configs: C1 and C2 envelopes within 20% of
   truth (weak forcing, quadrupole accurate there); C3 is the risk - truth
   envelope 0.044 is strongly forced near the 2:1 edge; I predict conj-oct
   passes it (ratio in [0.85, 1.2]) and conj-quad is borderline ([0.7, 1.3]).
6. kicks_per_orbit ~0.5 for resonant cases (rising toward ~0.9 if a1 shrinks
   while pumping), 0.24-0.55 for controls; median ~0.5 for every kick config,
   0 for none. dense_steps = 0 by construction for all four.
7. Verdict: PASS with conj-quad killed on pumphi, conj-oct passing all six
   criteria; negatives both fail as designed. Alternative outcome I consider
   live (~30%): conj-oct also exceeds 1.25 on R1 -> KILL of both candidates,
   which would say the multipole kick layer at l<=3 cannot carry the 2:1
   resonance amplitude at this mass ratio.
8. The `averaged` precession check (9.00e-5) landing 18% below truth's C1
   drift (1.09e-4) predicts the averaged config also drifts varpi ~18% slow;
   irrelevant to its gates (it fails pump/lib regardless).
