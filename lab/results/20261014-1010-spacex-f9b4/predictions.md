# Predictions — 20261014-1010-spacex-f9b4 (written before the decisive sweep)

Tuned on (dev): p = 20, e ∈ {0.1, 0.5, 0.9, 0.99}, arms 1:4, 2:4, a:4, a:6, m∈{1,2,4}
unmirrored. Frozen candidate: **a:4** — apoapsis-anchored geometric rungs only,
2 rungs/octave (isqrt taper), down to (x − floor_x) = floor_x >> 4, everything else
(cut, CAP, dyadic layer, 4-point Gauss quad, readout) shipped.

Certificate bar (the compile's verified certificate, 5a3b): summed error ≤ 2^-30
relative on all three channels vs an mpmath 50-dps reference. Control: the shipped
ladder arm must sit in the record's band (~2–6e-10 at p ≥ 20) or the run is VOID.

The decisive sweep (grid 8×9 + held-out 10 + 3 hyperbolic passages) has NOT been run.
Predictions:

- **P1 (certificate, grid + held-out):** a:4 holds ≤ 2^-30 on every key where the
  shipped ladder holds it; on keys where the ladder itself exceeds the bar (expected
  only in the p = 8-class m→1 tail at e ≥ 0.999, per 5a3b/21ba), a:4's max error is
  ≤ 2× the ladder's own error.
- **P2 (panels):** at e ≥ 0.9, a:4 panels ≤ ladder/3 at every grid key (dev: 3.5×
  at 0.9, 4.6× at 0.99); at e ≤ 0.5, a:4 panels ≤ ladder panels + 4 (nothing to win
  there; dev showed 6=6 at e 0.1, 14 vs 28 at 0.5).
- **P3 (time):** compile-time cut ≈ panel cut ± 30% at e ≥ 0.9 (cost ∝ panels at the
  measured 1.1–1.7 µs/knot); i.e. ≥ 3× at e ≥ 0.9, ~parity at e ≤ 0.1.
- **P4 (near-refusal edge):** held-out (6.7, 0.6) and (6.9, 0.45) — the p → 6+2e band
  where 5a3b's checker measured only 2.7–4.1× ladder/floor — a:4 error ≤ 2× ladder
  error, panels ≤ ladder/2.5.
- **P5 (internal negative):** the unmirrored m=1 arm fails ≥ 1 grid key at e ≥ 0.9
  (dev: 1.6e-9 at 0.9, 3.6e-9 at 0.99 — the apoapsis turning point is unresolved);
  m=1 mirrored with D=4 also fails at e ≥ 0.9 (dev: 1.8e-9). If m=1:4 passes the
  whole grid, my mechanism story is wrong and the dossier says so.
- **P6 (passages):** on the 3 hyperbolic keys, a:4 cuts panels ≥ 3× vs ladder
  (no certificate wired for the passage tail; count only).
- **P7 (arithmetic floor):** where a:4 and the ladder both pass, a:4's error is
  within 2× of the ladder's (the residual error is arithmetic, not panels; dev
  showed a:4 sometimes better, e.g. 2e-11 vs 2.1e-10 on t at e 0.9).

Failure of P1 at any held-out key where the ladder passes = the claim dies there and
the dossier reports the failing key and the smallest passing (m, D).
