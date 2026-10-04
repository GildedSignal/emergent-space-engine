# Predictions (written before reading any s2/s3 scheme rows)

Harness tuned on scene s1 only (pro 0.2/0.35/0.45, retro 0.5/0.7/0.85 at e0=0.05, e0.1@0.4).
Held out: s2 (e=0.3 @ 0.4 r_H prograde; retro @ 0.6 r_H; e=0.15 @ 0.85 r_H prograde) and
s3 (close planet-2 pass at 2.2 r_H minimum separation, moon @ 0.4 r_H). Reference precession
values were seen; no scheme row on s2/s3 has been read.

Gates frozen (B12/B14/B13 flavoured), same for every scheme:
- J: max |ΔJ/J0| ≤ 1e-4 over 50 planet orbits (no s3 J gate: planet 2 breaks the integral).
- P: apsidal precession rate within 10% of the dkd@512 reference (bound moons with defined apse).
- C: bound/escaped class matches the dkd@512 reference.
- S3: final osculating a and e within 1% / 10% of the reference's.

## Predictions

1. **dkd (the plane today, 64 kicks/orbit)** passes everything on s1 at K=64; its binding
   constraint on s1 is P on ret0.7 and e10-0.4 at K≈32, so its minimum full-pass K on s1 is 32.
2. **y4 (Yoshida-4, 3 kicks/step)** passes s1 at K=8 (net 24 kick-evaluations vs dkd's 32),
   i.e. a net ~1.3–2.7x kick cut, not 4x. Its J error keeps its dt^4 scaling (about x60 per
   halving) on every scene, including s3.
3. **dkd3 / dkd5 (WHFast correctors at outputs)** do NOT beat dkd on J anywhere (the Jacobi
   error of this split is already O(eps^2 dt^2)), and on P they are equal to dkd or worse
   (up to about 10x worse near e-vector noise). The corrector's coordinate fix will show in
   raw final-position error vs reference (dkd5 < dkd at equal K by ~3–10x), but that does not
   convert into a gate pass at larger step. Prediction: correctors are NOT a kick-reduction
   lever for the moon-tide split — the lens's hypothesis is wrong for this configuration.
4. **Held-out s2:** e=0.3@0.4 is the hardest: periapsis tide spikes concentrate the step error;
   dkd needs K≥64 for P; y4 passes at K=16–32 (net 48–96, roughly a wash vs dkd). retro@0.6
   behaves like ret0.7: dkd K=32, y4 K=8. e=0.15@0.85 escapes in all schemes (class C only,
   all match the reference).
5. **Held-out s3 (the pass):** all schemes that survive need K≥16 to keep final a within 1%;
   at K=8 dkd misclassifies or breaks the 1% a-error gate; y4@K=8 passes J-free gates because
   its error stays 4th order during the transient. The corrector stays harmless (no gate
   change) — the perturbation is not small during the pass, so the corrector's assumption is
   violated without changing the outcome materially.
6. **euler (negative control)** fails at least one gate at every K on every scene (J or C).
7. **Reference convergence:** ref512 vs ref2048 agree on P to <1% on all bound moons with a
   defined apse (spot-checked on s1: they do; predicting it holds on s2).

If (3) turns out wrong — corrector rows beat dkd at equal K on gates — my implementation of
the corrector sign/kernel order is the suspect, not the theory, and I say so in the dossier.
