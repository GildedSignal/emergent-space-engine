topic: binet-cells
status: open
closed-by:
valid-while:
updated: 20261016-1207-second-20261016-1120-scout-79ed-cec1

# Binet cells: the in-cell law of r1, executed on the full frozen case set

## Current best

**The r1 case set has now been executed end to end (r1v2: the letter plus the named
band-constant rule), and the verdict splits cleanly: where the two rules differ the
refit wins everywhere, and where they agree the letter's law itself fails its own
capture bar at every m (20261016-1207-second-20261016-1120-scout-79ed-cec1, float64,
rebuilt walker reproducing 79ed's instrument to 1.3e-13 on 79ed's own draw, oracle = ports
shipped gr_oracle.rs / gr_oracle_extended.rs).** Arms: `centre` (frozen geometric
centre) vs `refit` (one-law: each visited band's u_k = geometric mean of the orbit's
attained u-extremes there, self-consistent fixed point; crossed bands keep the frozen
centre exactly). Channels, letter-pinned sampler draw: precession m16 refit 256/256
(median advance error 1.509e-4) vs centre 255/256 (1.856e-4); period m16 256/256 vs
255/256 — the refit fixes the centre's one sampler failure on both channels; m32
256/256 both, medians 3.85e-5 vs 4.40e-5; m8 refit precession 256/256 (centre 252/256,
0.984 < 0.99) but period 0.977 — m8 stays unlicensed. Deterministic worst-offset e=0
circles (60 rows/m): refit worst 1.6e-14 at every m (exact by construction), centre
worst 1.61e-1 (m16) / 8.85e-2 (m32), pass fraction 0.20 / 0.49 — fe85's first-order
family, now measured on a working walker. Light deflection 64/64 both arms (worst
2.4e-4 at m16, second order in width), refit ≈ centre. ISCO 2/2 at every m both arms.
Long runs (10⁴ cycles): shape and the letter's 1e-12 repeat bar pass everywhere —
worst drift 1.0e-14 relative (first execution of this bar by anyone), zero walk
exceptions. Hyperbolic strong-field rows (r_peri<6): walk correctly now, both arms,
errors second order in width, but the near-separatrix rows (p−6−2e≈0.3) miss the
letter's bars at m16 (4/6) and m32 (5/6: (6.5,0.1) period 1.4e-3 > 1e-3); m64 passes
both (4× per doubling; verified by the checker). Capture was reported 3/10
misclassified at every m, both arms — **[checker-corrected: that was an
instrument defect, not the law's.** The rebuilt walker's hyperbolic-turn branch records
u_new = up + 2√(A·B), valid only when A,B>0; for the infalling turn (A,B<0) the true
turn is up − 2√(A·B), so the orbit is teleported above the band (b=6 photon, m16:
recorded 0.648 vs true 0.2245; RK45 on the same piecewise ODE turns at u=0.2245
against GR's 0.2247) and walks to capture. With the one-line fix
(u_new = up + 2·sgn(A)·√(A·B)): capture **0/10 misclassified at every m ∈ {8,16,32,64},
both arms**, and the model's barriers converge to GR second order in band width —
photon b̂ = 5.1929 (m8) → 5.1954 (m16) → 5.1960 (m32) → 5.1960 (m64) against 3√3 =
5.1962; matter L̂ = 3.9985 → 3.9995 → 3.9995 → 3.9995 against 4; b=6 escapes with
deflection error 4.9e-4 at m16. The buggy barriers (7.26/7.38 and 4.23/4.25) are √54
and √18 = 4.2426 — exactly where the GR turn point crosses u=1/6 into hyperbolic
bands, i.e. the bug's signature, and the buggy bisection is not even monotone in m
(m64: an escape window inside the absorbed region). H0205's "capture passes" is
vindicated. The `capture ≤ 0` criterion passes every configuration once fixed.**]
79ed's instrument additionally did mis-launch E=1 rows at ~8× the correct inward speed
and leak orbits past u=1/2 — both fixed here, and those four fixes (F1–F4) are real.

**Adoption state: the band-constant rule question is settled (one-law refit, canon
change); after the checker's one-line walker fix (F5) no law change for turning is
needed** — the certificate's remaining blockers are the near-separatrix strong rows at
m16/m32 (m64 passes them) and m8's period tail.

## Refuted

- **"m=32 is the measured minimum for the primary in-cell law" (fe85's reading): on
  the frozen sampler the one-law refit passes precession 256/256 at every m including
  m=8 — the near-circular family no longer sets the m floor through precession
  (20261016-1120-scout-79ed; period at m=8 still fails — 250/256 on this letter-pinned
  draw, 253/256 on 79ed's — so m=8 is not licensed).**
- **"The scout run's circle/strong-field/capture channels are undecided" (the silver
  verdict's reason): now decided — the refit passes the circles exactly; the
  strong-field rows walk and show genuine second-order tails (near-separatrix bars
  fail at m16/m32, m64 passes), while the capture channel's "law limit" was an
  instrument bug (F5), corrected by this run's check (20261016-1207-second-...-cec1).**
- **"The capture bars fail both arms at every m: the law cannot turn inside a hyperbolic
  band, photon b̂→√54, matter L̂≈4.23" (this run's dossier): refuted by the checker —
  walker bug F5; fixed, capture is 0/10 at every m and the barriers converge to 3√3
  and 4, second order in width (H0205's capture-pass vindicated).**
- [Standing: fe85's own corrections — the m16-FAIL headline, the "never run" premise,
  the second-order claim (first order on near-circular), the strong-field attack rows
  that passed there.]

## Open directions

1. **[checker-corrected] Adopt the one-line hyperbolic-turn fix (F5:
   u_new = up + 2·sgn(A)·√(A·B)) and re-execute the freeze on the record:** the
   checker measured capture 0/10 at every m ∈ {8,16,32,64} both arms and barriers
   b̂ → 3√3, L̂ → 4 (second order, `barriers.py` logic on the fixed walker). No
   barrier "law fix" exists to price — the old direction 1 chased an instrument bug.
   The certificate then fails only on {strongf m16/m32, m8 period}.
2. [fe85's, narrowed] The integrator must now commit the r1v2 freeze (this run's
   `r1v2-rings-band-constant.md`, hashed before the run) naming the band-constant
   rule; the near-separatrix strong rows need either m=64 locally (the tree's own
   answer) or a relaxed bar for p−6−2e < 0.5.
3. The refit's integer form and its compile-time cost remain unpriced (unchanged from
   79ed).
4. [fe85's, standing] The multiply-add cycle update on the separatrix family
   (kick-cadence's territory); unguarded by any rung.

## Contradictions

None open: the capture misclassification is resolved as instrument bug F5 (no arm or
law attribution); the m=8 period failures under both arms remain fe85's second-order
tail.

## Runs
- H0205 checker execution, 29 September (DISPUTED, never graded): m16/m32 pass every r1
- 20261015-1450-redteam-fe85 (silver): first-order near-circular law measured (ratio
- 20261016-1120-scout-79ed (silver): the per-band u_k refit priced on the frozen
- 20261016-1207-second-20261016-1120-scout-79ed-cec1 (this run, awaiting grade): the
  full frozen case set executed; refit wins every differing channel; photon barrier
  b̂→√54 and matter L̂≈4.23 are the law's own, both arms, every m.
