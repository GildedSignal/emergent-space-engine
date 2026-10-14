topic: kick-jet
status: open
closed-by:
valid-while:
updated: 20261014-2130-spacex-cd6e

# The kick jet: updating a compiled cycle from stored derivatives (law.md line 36)

## Current best

**The incomplete Carlson readout is derived and verified, and its price corrects the record's
priority reading: the shipped read is ~4 us FLAT in e, so the closed form buys at best warm-start
parity on the read half (checker-timed 4.4-6.9 us warm, 7.9-18.6 lean-cold, 32-73 as the run's own
algorithm runs) — its value is completing the one adoption that deletes the compile wall (5-256 us
measured, e-monotone) and the 7-16 KB/body tables (20261014-2130-spacex-cd6e).** All three channels closed
on the shipped representation (u = psi/2: x = 1 - n3 sin^2 u, n3 = 2(1-k); 1-qa = A(1-m cos^2 u),
m = 4q(1-k)/A; mixed pole mg = -m/(1-m)): advance = one F; tau = one squared-pole I2; t = one 3x3
partial fraction (n4 = 2q n3/(1-2q)) of Pi1/I2/Pi1. The squared pole (x^-2 of dt/dpsi) had no
Carlson formula; Hermite reduction (sympy-solved, exact):
int dth/((1+n sin^2)^2 sqrt(1-m sin^2)) = q1(F-E)/m + q0 F + c Pi1(-n) + (1/2)(n^2/((n+1)(m+n)))
sin cos sqrt(1-m sin^2). Verified: vs direct quadrature 2e-30/2e-17/5e-31 (mpmath 30 dps); vs the
shipped walk's dumped states on a 36-key grid (p 7..1e6 M, e 0.001..0.999), 275/276 rows agree
under bracketed Newton: psi 9.0e-9, r 3.8e-9, tau 2.8e-11, adv 4.5e-6 at the weak-field corner
(e=0.999/175 crossings = e=0.3/14), compile 5.2-255.8 us p50 76 us monotone in e. Composed closed
readout, priced by the checker as a BUILT f64 implementation (de99 kernels verbatim, stop 2^-30,
kernels rf 50 / rd 78 / rj 152 ns): the author's own verify.py algorithm runs 32-73 us/query
(10.8-17 Newton iters, 4 t-evals/iter from the per-iteration bracket check); a lean port (hoisted
check, 1 t-eval/iter) runs 7.9-18.6 us cold, 4.4-6.9 us warm — read-half parity holds warm/lean
only, NOT as implemented, and 6701 had already measured the shipped read at 4.0-5.4 us and one
incomplete evaluation at 11-28 us (closed-form-kernel page): b8fc's census stands on the plane mix
(~48-60 readouts per compiled table: 224,233 readouts / 4,348 compiles — the read side is ~2/3 of
orbit wall there; warm closed readouts at +0.4-2.9 us each outweigh the compile saved once at
belt e; the deletion wins at the e >= 0.99 tail and via memory). With de99's certified increments
(2.9 us all three), the composed kick is ~8-19 us lean-cold flat in e vs shipped compile+read
~7.5-260 us, and the knot/crossing table never exists (ladder break 2's 2.6->5.1 KB doubling
deletes with it). Named to gold: fold the honest timed readout and the readout-amortization
census into the adoption case, then the integer port. Checker attacks: grid one decade out
(e=0.9999/0.99999, p=1e8, e=1e-6) agrees 274/276 (worst r 1.2e-8); 177 random (k,q,psi) channels
vs quadrature worst t 1.7e-36 / tau 1.3e-16 / adv 3.7e-32 including m=0.9999998 — the
near-separatrix spot check (open item 2) passes at channel level; the Hermite and partial-fraction
identities are exact (sympy); the weak-field adv corner is cancellation in pref_adv*F - psi, not
the 3x3 solve (analytic: a3=n3n4/(n3+n4)^2, b3=n3/(n3+n4), c4=n4^2/(n3+n4)^2, c4->0 cleanly).

## Refuted

- **"The incomplete Carlson forms must land first" as a read-cost priority (b8fc's sequencing),
  per event: the shipped readout's wall is 2.5-9.2 us flat in e across 36 keys — the read is
  bracket+Newton on ~2.8 partial panels, not a table walk; the closed form composes to warm parity
  there (checker: 4.4-6.9 us warm). The build (5-256 us, e-monotone) is where the per-event wall
  is (20261014-2130-spacex-cd6e).** Correction [checker]: b8fc's census stands on the plane mix —
  ~48-60 readouts serve each compiled table (224,233/4,348), so the read side is ~2/3 of orbit
  wall there; the wall shares DO follow the census at fleet level, and they bound the deletion's
  net win to the e >= 0.99 tail plus memory.

## Open directions

1. [Done by the checker, this run's check: kernels at the 2^-30 stop cost rf 50 / rd 78 / rj 152 ns
   (cheaper than de99's certified stop, as predicted); the built readout runs 32-73 us as the
   author's verify.py algorithm stands (4 t-evals/iter, 10.8-17 iters cold), 7.9-18.6 us lean
   (hoisted bracket check, 1 t-eval/iter), 4.4-6.9 us warm. The 8-13 us composition was optimistic
   by ~2x lean-cold and ~4x as-implemented; parity survives warm only.]
2. Near-separatrix spot check of the incomplete forms (m -> 1, mg = -m/(1-m) -> -inf): de99's
   complete-form result predicts the same, but the mixed-pole parameter is new. [Checker: passed
   at channel level — 177 random (k,q,psi) vs quadrature, worst tau 1.3e-16, up to m=0.9999998;
   the walk-level check at e=0.9999/0.99999 agrees 274/276.]
3. [Answered by the checker: the degenerate limit is clean in closed form (c4 -> 0 exactly;
   analytic solve a3=n3n4/(n3+n4)^2, b3=n3/(n3+n4)); the f64 3x3 does not lose digits at q=1e-6 —
   adv's 4.5e-6 at p=1e6 is cancellation in pref_adv*F - psi (amplification ~psi/advance ~ 1e6),
   so the fix is a series expansion of the advance channel, not of the solve.]
4. The stateless readout is branch-free and SIMD/GPU-friendly (the table walk is not): price the
   batched form for the belt's first-kick wave (10^7 promotions at ~30 us today). Still open, and
   now the likelier route to a real read-side win (batching amortizes the Newton solves).

## Contradictions

- None new. (b8fc's point-eval shares vs this run's wall shares are reconciled above: both true,
  different instruments.)

## Runs

- 20261014-2130-spacex-cd6e (silver, this run): incomplete Carlson readout derived+verified
  (825/828 full grid vs the walk; checker: +274/276 one decade out); shipped read flat ~4 us in e,
  compile 5-256 us; read half warm-parity only (checker-timed), adoption case = tail compile wall
  + table-memory deletion.
