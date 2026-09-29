# Dossier — rung canary: Kepler e = 0.5 at fixed h = T/200

## Claim
The canary holds: leapfrog (KDK velocity Verlet) passes E1/B1/C1 — bounded energy
oscillation with zero secular growth over 10^4 orbits — and euler, the negative, fails
on B1 (unbinds at orbit 77.7 of 10^4). Expected verdict PASS is confirmed.

## Bottleneck
Not a bottleneck mover — this is a calibration canary for the rung machinery itself
(metrics, criteria, verdicts) before real rungs count.

## Evidence
Cloud container, Linux/x86, 4 vCPU, load 0.06, 0.9/16 GB used, cold machine.
Full run (both configs, 2 x 2,000,000 steps, float64): 0.11 s wall.

| metric | leapfrog | euler | criterion |
|---|---|---|---|
| energy_growth_exponent | 2.98e-10 | -1.08e-9 | E1 <= 0.2 |
| bound_fraction | 1.0 | 0.007773 | B1 >= 1.0 |
| steps_per_orbit | 200 | 200 | C1 <= 256 |

leapfrog: max|dE| = 1.34e-3, final|dE| = 1.28e-3 — bounded oscillation, slope is noise
(3e-10). euler: first E >= 0 at step 15547 (orbit 77.7), then escapes and |dE| plateaus
at |E_inf - E0| = 0.537.

Commands (each well under 60 s), from this folder:
```
gcc -O2 -Wall -Wextra -o kepler_rung kepler_rung.c -lm && ./kepler_rung
python3 make_picture.py
```
Outputs: `metrics.json`, `summary.txt`, `picture.svg`, data files `traj_*.txt`,
`ener_*.txt`, `win_*.txt`.

## Predictions
`predictions.md` was written before the run. All held: leapfrog slope ~0 with
max|dE| in the predicted 1e-5…1e-3 band, bound 1.0, 200 steps/orbit; euler unbound
inside 500 orbits (77.7), bound_fraction 0.0078 in the predicted 0.005–0.05 band.

## Notes for the checker
- euler's E1 passes *vacuously* (slope ~0): it unbinds before t = 0.1*t_end, so all 20
  windows sit on the post-escape plateau and the secular drift is invisible to the
  exponent. B1 is what kills it. The metric works, but for escaped negatives the
  exponent alone is not diagnostic — worth remembering when reading future rungs.
- `steps_per_orbit` = 200 by construction (2e6 steps / 1e4 orbits, no substeps); C1 is
  a sanity bound, not a discriminator here.

## What would make it wrong
A leapfrog slope > 0.2 would have meant a real secular leak or a KDK ordering bug;
neither occurred. Adoption cost: none — no engine code touched. Fit: "A test that
cannot fail is a control" — euler is that control, and it failed as it must.

## Lens
Directed rung, no lens. What a lensless author may miss: nothing here is novel physics
(see H-entry-free canary); the value is calibration only.
