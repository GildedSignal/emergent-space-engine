topic: binet-cells
status: open
closed-by:
valid-while:
updated: 20261016-1120-scout-79ed

# Binet cells: the in-cell law of r1, measured and margined

## Current best

**The per-band u_k refit is priced on the frozen r1 sampler, and the one-law form is the
one that carries the win: u_k = the geometric mean of the u-extremes the orbit itself
attains inside the band (a self-consistent fixed point; for every band the orbit merely
crosses this IS the frozen centre exactly, so the law has no regime branch) lifts the
frozen 256-seed sampler to 256/256 precession at every m ∈ {8,16,32} — including m=8,
which the frozen law fails at 250/256 — at −25% median advance error (1.45e-4 vs 1.83e-4
at m=16, 5.52e-4 vs 7.68e-4 at m=8), crossings and exact cycle-2 repeat unchanged
(20261016-1120-scout-79ed, float64, oracle = ports of the shipped gr_oracle.rs /
gr_oracle_extended.rs; the frozen arm reproduces fe85's m=16 median 1.83e-4 exactly).**
The price, measured: the refit moves the turning bands' constants of essentially every
bound orbit (256/256 seeds' advances change >1e-6 at m=16, 242/256 at m=32) — a canon
change, not an overlay; and the period channel shows no gain at m=8 (253/256 both arms),
so the second-order tail still gates m=8. The letter's contained-only form (fe85's open
direction 2 as written) never fired on this draw (0 seeds changed at m=16) — no measured
win. Instrument limits, honest: the deterministic e=0 circle family, the strong-field
held-out rows, capture and ISCO are broken in this run's own walker (all four reported
undefined, not physics verdicts; the frozen arm misclassifies 5/10 capture rows, proving
the defect is the instrument's); the pre-registered kill bar is undecided, not passed.

**[Checker held-out (this run's check, author's module unmodified): the claim is
draw-independent and the near-circular limit holds.** A fresh 1024-seed draw (different
RNG, next decade of N): m=16 GEO 1024/1024 on precession AND period (frozen 1018/1024
both), median 1.49e-4 vs 1.96e-4; m=8 GEO prec 0.999 vs frozen 0.955, period 0.976 — m=8
stays unlicensed. Near-circular family (e ∈ {1e-4…3e-2}, 96 rows): GEO worst advance
1.66e-8 at e=1e-4 vs frozen 3.0e-2 (the e→0 limit of the undecided kill-bar row, without
needing the broken e=0 channel); family 96/96 vs 61/96. One reversal: at e≈0.03
(straddling, excursion ≈ band width) GEO is mildly worse than frozen (3.1e-3 vs 2.2e-3),
both far inside the 1% bar. Fixed point converges 3–5 rounds on all 352 seeds tested;
moderate strong rows (u_apo < 1/6) show no GEO regression; m=64 continues the pattern
(9.9e-6 vs 1.1e-5). **]**

**[fe85's mechanism and margins stand: the first-order near-circular family, its law
2π(1/√(1−6u_k)−1), m16's one-seed margin at the frozen sampler, m8's two failures, the
strong-field rows that passed there. The refit row above composes with them: it attacks
the same family through the band constant.]**

## Refuted

- **"m=32 is the measured minimum for the primary in-cell law" (fe85's reading of their
  own family): on the frozen sampler the one-law refit passes precession 256/256 at every
  m including m=8 — the near-circular family no longer sets the m floor through the
  precession channel (20261016-1120-scout-79ed; the period channel at m=8 still fails
  3/256, so m=8 is not licensed, only unblocked on precession).**
- [Standing: fe85's own corrections — the m16-FAIL headline, the "never run" premise, the
  second-order claim (first order on near-circular), the strong-field attack rows that
  passed.]

## Open directions

1. [fe85's, narrowed] Re-freeze r1 with m ∈ {16, 32}, a deterministic near-circular case
   and an integer-holdable repeat bar; the lab has still never graded r1. The freeze must
   now NAME the band-constant rule (frozen centre vs the one-law refit) — they differ on
   every orbit's turning bands.
2. **[this run] Fix the circle-family instrument and decide the one-law vs contained-only
   forms:** the deterministic worst-offset e=0 circles are exactly where the two forms
   differ most (contained: the refit makes the band ODE's circular solution coincide with
   the GR circle — advance and period exact by construction; one-law: same limit plus the
   turning-band shift everywhere else). This run's walker breaks there (and at
   strong-field rows, capture, ISCO); fe85's checker-extended code on its branch is the
   faster path. Also unpriced: the fixed point's integer form and its compile cost.
3. [fe85's, standing] The multiply-add cycle update on the separatrix family
   (kick-cadence's territory); unguarded by any rung.

## Contradictions

None. (fe85's near-circular weak flank and 6765's algebraic near-radial convergence
remain composed; the refit touches the near-circular family and the turning bands only.
The m=8 period failures under both arms are consistent with fe85's m8 period FAIL —
second-order tail, not contradiction.)

## Runs
- H0205 checker execution, 29 September (DISPUTED, never graded): m16/m32 pass every r1
- 20261015-1450-redteam-fe85 (silver): first-order near-circular law measured (ratio
- 20261016-1120-scout-79ed (this run, awaiting grade): the per-band u_k refit priced on
