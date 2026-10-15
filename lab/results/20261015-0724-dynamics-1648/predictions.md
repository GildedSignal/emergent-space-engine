# Predictions (written before the decisive scenes d1, d2, h1)

Run 20261015-0724-dynamics-1648. Question: does the contact law's receding-skip gate
distort a cold dense gas's dynamics (equipartition attractor, relaxation rate), or is the
dropped grazing impulse a bounded perturbation? Instrument: `skipgas` (shipped Chronon v1
vs three f64 twins: `skip` = exact mirror of the shipped rule, `contact` = skip-class
pairs resolved at the true contact root |d| = reach, `cross` = skip-class pairs exchanged
at the bin-end separation, `tau` = 8144's proposed rule as worded).

## What already ran (instrument validation, before this file)

- c1 (vth = 8, deep control): zero skips in all arms; `skip` and old-fix twins identical
  (894 = 894 contacts, equal transport). The shipped arm at these crawl speeds (|k| ~ 8
  quanta) diverges from the twins (826 contacts, faster equilibration): velocity
  quantization is first-order there, not the skip — domain note, not the question.
- c2 (vth = 4000, fast control): shipped 90,263 contacts vs twins 89,870-90,021 (0.4%),
  skip fraction 49.7% vs 51.1-51.9%, classifier (tau* <= 1) agrees with observed
  revisions 88,391/90,263 (98%), energy ledger exact. The skip drops ~2.4e8 of ~5.0e8
  total transport: gross distortion, the negative control the instrument must see.
- First build's fix arm resolved at the closest-approach normal and applied ~0 impulse
  (3,665 total over 46.6k skip-class contacts): the tau-reflection is a no-op, proven
  analytically below. The `tau` arm now measures it in the final build.

## Pre-registered predictions for the decisive scenes

Scene constants: Q = 2^20, box 2^18 quanta, r = 1024 (reach 2048), masses 1 (hot, vth)
and 64 (cold, vth/16), T_A/T_B = 4 at birth, N = 200 (h1: 300, seed 13).

1. **d1 (vth = 150, 400k bins; fleet-relevant slow):** skip fraction of detected contacts
   between 0.3% and 4%. The `skip` arm's equipartition half-time t_half within 10% of the
   `contact` arm's; dropped transport < 5% of total; end temperatures per class within 5%.
2. **d2 (vth = 700, 200k bins; stress):** skip fraction 15-35%. `skip` vs `contact`
   relaxation differs by no more than the dropped-transport fraction (predicted 10-30%
   slower); temperatures still converge (bounded, no walk), end state statistically the
   same family. No runaway, no freeze.
3. **h1 (held-out: seed 13, N = 300, vth = 400, 250k bins):** skip fraction 5-15%;
   t_half(skip)/t_half(contact) in [0.85, 1.15].
4. **`cross` (the one-line fix):** within a few % of `contact` in relaxation at d1; may
   deviate more at d2/h1 where bin-end geometry is staler.
5. **`tau` (8144's rule as worded):** applied skip-class transport < 10^-3 of `contact`'s;
   tau's trajectory-class statistics identical to `skip` (it is a no-op).
6. **shipped vs `skip` twin** at d1/d2/h1 (|k| >= 150 quanta, quantum < 1%): skip
   fraction within ±25%, t_half within ±20%, end temperatures within 5% (f50d's
   quantization innocence extended to this scene class).

## Kill criteria (pre-registered)

- If `skip` vs `contact` t_half differs > 2x at d1: the skip changes fleet-scale dynamics
  at game-relevant closing speeds — a law defect, needs a gate; dossier claims danger.
- If shipped vs `skip` twin breaks the bounds of prediction 6, the float mirror cannot
  isolate the skip and the skip-vs-contact attribution is VOID (report shipped-vs-contact
  only, both real-integer questions).
- If the gas does not equilibrate measurably within the run (no t_half), the scene is
  under-collisional: extend, do not claim.

## The no-op, proven (for the record, before the decisive runs)

In the pair's centre-of-momentum frame the law's normal N = (d·P_s, E_tot·d) is purely
spatial (P_s = 0), so the reflection flips each momentum's component along d. At closest
approach d(tau*) is perpendicular to w, and in the COM frame both momenta are parallel to
w — the flipped component is zero for both bodies, for any masses: the reflection at the
tau* normal is the identity. The fix rule needs the contact root |d| = reach (irrational
in general: its direction carries depth/|w| under a square root), so "the v1 reflection
needs no root" is false at the only rational geometry.
