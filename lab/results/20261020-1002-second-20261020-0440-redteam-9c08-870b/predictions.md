# predictions.md — 20261020-1002-second-20261020-0440-redteam-9c08-870b

Written before the frozen run (rung sha256 ed91f4c0…91924, frozen above). The pilot at NS=2·10⁵
sized B and validated the instrument (quadrature reproduces the checker's constants exactly);
nothing below is tuned on the frozen run's numbers. Held-out relative to 9c08: the 2D p99 at every
case (9c08 never measured p99 in 2D), the fine-floor 3D rows at γθ_f = 4 and 8000, and the
max-over-cells colour metric (9c08 gated nothing and reported forward-cell means).

P1 (verdict): PASS — `exact-sum` passes all four criteria; `one-shift` fails `bright` and
`colour`; `flat-gamma` passes all (else VOID).
P2 (one-shift brightness, the 9c08 law on the new geometry): bright_p99 (max over cases)
0.75–0.80, set by the 2D sky at γθ_f = 8000 (9c08's checker: 2D saturation 77.14% mean; p99 sits
slightly above the mean). The 3D saturation contributes ≈ 0.687.
P3 (one-shift at γθ_f = 1, held out in 2D): 2D p99 0.24–0.28 (3D measured 0.271 at NS=2·10⁵;
the 2D forward cell carries a wider relative tail).
P4 (controls read zero): one-shift ctrl_bright_max ≤ 5·10⁻⁵ (9c08: 0.0025% at γ 1.33); exact-sum
and flat-gamma read exactly 0.0 (algebraic identity — the served value is the reference sum).
P5 (colour): one-shift colour_oct 0.7–0.9 (saturating near the 2D forward cell's full ln-span
in octaves); exact-sum colour_oct ≤ 0.05 at B = 128 (pilot worst case 0.0358; the bin-bound
argument gives ≤ 0.070 at γθ_f = 8000).
P6 (cost): extra_due_ops = +4 (exact-sum, flat-gamma) and −5 (one-shift); both inside ≤ 6.
P7 (the collapse): the two floors read the same per γθ_f to MC noise (the E(γ·θ_f) law; 9c08's
collapse, now at the p99 readout and in 2D).
P8 (the structural read, not a number): the record's CellSums stores Σ seen flux (each member's
own k⁴ folded at insert) — so the brightness half of 9c08's claim does not apply to the shipped
record; the rung's candidate is the record's own representation. If the serve path had rebuilt
brightness from `sh/lum`, P2 would instead be the candidate's number and the verdict KILL.

The miss I most expect: P3's 2D band (no prior measurement of the 2D p99; my ±15% band is a
guess at the weighting's effect on a 5-cell distribution).
