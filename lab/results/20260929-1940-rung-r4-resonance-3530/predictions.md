# predictions.md — written before the decisive run

Scene (frozen before any law run): pumped test body exterior at exact 2:1
(P1/P2 = 2), interior perturber m2/m0 = 3e-3 on a circular orbit, e1_0 = 0.05,
lambda2(0) = pi + w2, 200 synodic periods. Truth = barycentric velocity-Verlet
at 600/1200/2400 steps per orbit. Scene search (truth only, never the law)
found at mu = 3e-3: bounded eccentricity pumping in this geometry, but no
librating resonant angle in any of the grids I searched (interior-body 2:1:
ejection everywhere; exterior-body 2:1: theta = 2*lam1 - lam2 - w1 circulates).
The red-team's librating scene (truth C = 0.867) is not reproducible from the
rung text alone; I report that honestly and the lib criterion then measures
circulation against circulation.

Predictions, cases I have not tuned on (the law has not been run at all yet):

1. conj-quad: e_pump_ratio (max e1 law/truth) in [0.5, 1.3]: the quadrupole
   l=2 truncation misses ~ (a2/a1)^3 ~ 25% of the tide, and the linearized
   encounter spans ~ half a synodic period, so I expect the pumping amplitude
   right to within tens of percent, sign correct. Passes pump [0.8,1.25] with
   ~even odds; the direction of the octupole correction should push conj-oct
   above conj-quad.
2. conj-oct: e_pump_ratio closer to 1 than conj-quad.
3. Both candidates: kicks ~ 1 per synodic period (2:1 -> 1.0 per inner orbit,
   5:1 -> 4.0), so kicks_per_orbit median ~ 1.2, passing cost; dense_steps 0.
4. averaged: kills the phase dependence -> e1 stays within ~20% of e1_0 = 0.05
   while truth pumps to ~0.08-0.18 -> e_pump_ratio ~ 0.3-0.6 -> FAILS pump.
5. none: e1 constant 0.05 -> FAILS pump.
6. Controls: truth's secular e1 envelope near 0.05-0.08; the kick layer should
   track it within 20% at 5.0 and 2.55 (far from resonance); 2.15 is the risky
   one (closest to the 2:1 chaotic zone).
7. libration_ratio: with truth C ~ 0.06 (circulation), ratios land near 1
   vacuously unless the law's kick layer phase-locks spuriously.
