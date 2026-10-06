# B12's statistic rebuilt from the requirement: the arrow of time at a fixed state

**Claim.** B12's compounding certificate should read the *arrow of time at a fixed state*: match
each early far-field sample of a ship to its nearest late return in the normalized slow state
(a, e), adjust the pair's signed Jacobi difference by the state difference it comes with, and
ask whether the residual grows with the time between the visits (Kendall's z, pooled over the
judged ships with its exact null variances) — this one statistic, with a derived threshold
(z ≤ 5) and no scene constant, passes echo, `scaled` and `planted-bounded` and fails
`planted-compound`, a leak, `planted-drift` and `planted-kick` with every margin ≥ 1.9×,
identically on two floating-point paths, on a ship set classified by a 15-run one-quantum
replica ensemble instead of one chaotic reference path.

**Bottleneck.** The motion law v2 is designed against B12 (HANDOFF); the growth exponent it
now uses cannot separate (the red-team 20261006-0737: the reference itself fails at every
tolerance, bounded state-only plants read 0.28–0.57, and echo fails B12 on Linux before any
statistic is read). This run replaces the deciding statistic and the judged-set rule. No frozen
threshold is weakened: the 1e-4 cap, the 1e-12 floor (reporting only), 16 ships, the ≥20-
crossing scene contract and the 10% exclusion budget are all preserved for the integrator to
re-hang on a re-frozen set; the exponent ≤ 0.2 is replaced by z ≤ 5.

## The statistic (frozen before the decisive runs)

Per judged ship, from the law's own states at the gate's samples (P/8, 200 periods):

1. **Pairs.** Far-field samples (planet farther than 3 R_H). Each sample of the first half is
   matched, one-to-one and in time order, to the nearest still-unused second-half sample in
   (a, e) normalized by the ship's own far-field spread, requiring a gap ≥ 12 P (two synodic
   periods: the fast state is mixed) and a normalized distance ≤ 0.4 (a recurrence, not a
   forced match). Ships that keep < 30 pairs carry no evidence and are reported, not judged.
2. **Adjustment.** The pair's signed difference d = c_late − c_early of the relative Jacobi
   error is fitted, through the origin, on (da, de). This deletes the drift confound that
   breaks every magnitude test: a chaotic ship's a diffuses with drift (ship #39: 1.19 → 2.1
   separations over the horizon), so any state-tied error's *magnitude* grows with time with no
   memory at all. Measured budget: `planted-bounded`'s adjusted residual is ~3e-12 against its
   1.3e-5 error — five orders of headroom, which is what licenses the 0.4 ball.
3. **The arrow.** The residual r is what the law gained at a fixed state between the visits.
   Kendall's rank correlation of |r| against the gap, as z = 3(C−D)/√(n(n−1)(2n+5)):
   a leak gives r a mean ∝ gap, a walk gives r a spread ∝ √gap — both raise |r| with the gap;
   a state-only error has exchangeable r at any gap (z ~ N(0,1)), and a constant offset gives
   r = 0, no comparisons, z = 0.
4. **The gate.** The ships are independent repetitions of one law, so the sufficient aggregate
   is the pool z_pool = Σ z_k w_k / √(Σ w_k²/2), w_k = √(n_k(n_k−1)(2n_k+5))/3 — again N(0,1)
   under no-memory. **PASS iff z_pool ≤ 5 and worst err ≤ 1e-4 over ≥ 9 evidence ships.** The
   threshold is derived, not fitted: 5 is ≥ 9.8σ on the exact null, ≥ 4.9σ allowing a 4×
   pair-dependence variance inflation. The test is one-sided: the requirement is growth with
   exposure; decay is not compounding.

**The horizon it certifies:** the frozen scene's 200 planet periods (≥ 20 handoffs on the
contract's ships). Power grows with the horizon (more pairs, wider gap range) at linear cost;
nothing in the statistic is tuned to 200.

**The smallest detectable leak** (total relative Jacobi error per horizon, measured, both
paths agreeing): a bare leak is detected down to **1e-15** (z = 13.7/22.7), the floor being the
1.5e-16-relative rounding of recomputing C_J; 1e-16 passes (z = −1.7/+1.5). Under a bounded
error of amplitude A ≈ 1e-5 (`planted-bounded` at full size) the leak is detected down to
**1e-11** (z = 10.2/18.3; 1e-12 passes at z = 2.7/0.0), set by the bounded residual noise
(~3e-12), i.e. ≈ A/1000 — three to four orders below the level-test invisibility bound
A/horizon ≈ 5e-8 that the lens named. The lens's rule of thumb is a *level* test's limit; the
conditional test does not share it.

**How a chaos-sensitive ship's fate is judged:** not by one reference path (the red-team: 16 of
16 closest approaches move > 50% under one ulp; echo fails B12 on Linux through two flips) but
by the median over 15 deterministic one-quantum replicas (integer bit-offset patterns: ±1, ±2
ulp on each word and two paired corners). A ship is in the oracle's domain iff its median
closest approach ≥ 1 planet radius; its crossing count is reported per ship.

## Evidence

All from `work/b12arrow` (a standalone crate on copies of the judge's own reference
`restricted.rs`, sampler and plants; the crates and gates untouched). Reproduce:

```
cd lab/results/20261006-1545-q-b12-design-9242/work/b12arrow
cargo build --release                                   # ~1 s; CARGO_TARGET_DIR is honored
$CARGO_TARGET_DIR/release/b12arrow          > ../final15-plain.txt 2>&1   # 16 s
$CARGO_TARGET_DIR/release/b12arrow --fma    > ../final15-fma.txt   2>&1   # 16 s
$CARGO_TARGET_DIR/release/b12arrow --sweep       > ../sweep2-plain.txt    # 35 s
$CARGO_TARGET_DIR/release/b12arrow --sweep --fma > ../sweep2-fma.txt
```

Peak RSS 2.8 MB; Linux x86 (8 vCPU, load ~2); orders of magnitude only, per the lab rules.

**The seven controls** (z_pool; margin to 5; worst err):

| Law | plain | fma | verdict | worst err |
|---|---|---|---|---|
| echo (the conserving reference) | −2.68 (1.9×) | −0.20 (25×) | **PASS** | 2.3e-15 |
| scaled 1e-11 | +1.50 (3.3×) | −0.31 (16×) | **PASS** | 2.9e-11 |
| planted-bounded | +0.90 (5.5×) | −2.55 (2.0×) | **PASS** | 1.3e-5 |
| planted-compound | +27.65 (5.5×) | +17.28 (3.5×) | **FAIL** | 9.8e-7 |
| leak 3e-9 | +44.29 (8.9×) | +60.74 (12×) | **FAIL** | 3.0e-9 |
| planted-drift (the plain reference) | +36.90 (7.4×) | +23.97 (4.8×) | **FAIL** | 2.4e-9 |
| planted-kick | +42.03 (8.4×) | +47.59 (9.5×) | **FAIL** | 2.1e-4 > 1e-4 |

Every verdict identical on both rounding paths (`--fma` contracts the reference's hot kernels
with mul_add: a different machine's arithmetic). The reference's own numbers move between
paths (echo −2.68 → −0.20; drift's worst err 2.4e-9 → 8.1e-10) — its decisions do not: that is
the machine independence the lens asked for, shown on the reference itself. Extras: leak 1e-8
and leak+bounded 1e-8 both FAIL (+44.2/+60.7) — the |b+l| kink that inverted the red-team's
pair statistic is gone because the adjustment happens on the signed difference; a rerun is
byte-identical (timing aside); the strict parameters (ball 0.25, gap 20 P) give the same
verdicts (compound +22.2, echo −2.9, all seven unchanged).

**The judged set, and what the ensemble found.** With 15 replicas, 16 of 16 ships are in the
oracle's domain on the plain path; ship #6 is a fate-split ship (replica closest approaches
from 0.79 to 24 planet radii) and flips to excluded on the fma path — the only residual
machine dependence, and every law verdict is invariant to it either way (both tables above
differ on #6 and agree on all verdicts). **The freeze's own criterion does not survive the
ensemble:** the crossing-count medians are 14, 20, 12, 14, 16, 26, 22, 22, 16, 30, 30, 8, 26,
12, 12, 22 — nine of the sixteen frozen ships robustly cross R_SOI fewer than the contract's
20 times (their single M1 paths crossed ≥ 20: the freeze selected lucky paths), and at five
replicas two ships' median closest sits inside the planet. Dispositions for the integrator:
re-freeze `HANDOFF_KEPT` under the ensemble criteria (median crossings ≥ 20, median closest
≥ 1 radius, and drop fate-split ships); until then this run judges the domain ships and
reports the counts. Ship #11 keeps no pairs at all (it lingers inside 3 R_H) and is reported,
not judged.

**The gray case, stance included.** A bounded error periodic in absolute time (1e-7·sin) has
no envelope growth; it reads z_pool = −14.4 (plain) / −3.4 (fma) and passes the one-sided
gate. Principle 13 forbids *compounding*; a time-periodic offset is bounded by construction at
any horizon, and the 1e-4 cap still bounds it. If the integrator prefers to catch clock bugs,
make the gate two-sided and this law fails — a one-word change, stated here so it is a
decision, not a discovery.

## Predictions

`predictions.md` holds the original pre-run predictions, a failed first decisive attempt, an
amendment, and the final ones. Held: echo/scaled/bounded calm and passing (P1'); drift, kick
and both leaks failing on both paths with the stated margins (P3', P4'); the sweep edges (P7':
bare-leak detection below 3e-9 — measured far lower, at 1e-15/1e-11, since the rank test is
scale-free down to the arithmetic noise); identical verdicts across paths (P6'); the periodic
gray case reading large negative z and passing one-sided (P5'). Missed, and fixed by disclosed
iteration: the original pair sign test read the walk at median −0.89 (a zero-mean walk moves
the spread, not the mean) and inverted under a composed leak (the |b+l| kink); the Kendall
version with a per-ship *median* read the walk at 4.5 against 5 (per-ship realization noise:
one walk path per ship, ~50 encounter steps); the *pool* — the same test aggregated with its
exact variances, since ships are independent repetitions of one law — reads it at 17–28. Three
design iterations in all, each recorded before the next run; the final statistic was frozen
before the decisive runs above, and nothing after them was changed.

## What would make it wrong, the cost, the fit

Wrong if: a real law's bounded error is so steep in (a, e) that the linear adjustment leaves a
residual that trends with the gap (the bounded control's five-order headroom says the margin
is large, but a real law is not the plant); or a compounding error grows *downward* faster
than upward (the one-sided gate passes it — decay is not compounding, but a sawtooth that only
dips is invisible); or a law compounds only on one ship (the pool needs z ≈ 18 on a single
ship to trip — the median has the same weakness in the other direction). Cost: one pass over
the law's own samples, ~0.1 s per law per 16 ships at P/8, plus the 15-replica ensemble (~13 s
once per process, reference-free thereafter); the exponent fit it replaces already walked the
same series. Fit: principle 13, "errors never compound", is enforced as error *type* — an
arrow of time at a fixed state — which is what "types of errors and not just errors" (OC#42)
asks; principle 32, "symmetry is found, not given": the symmetry used is the exchangeability
of a chaotic ship's returns, found in the dynamics, not imposed; principle 22: the ships' own
returns decide the pairs, no fitted scale enters (the normalization is each ship's own spread,
the gap bound is two synodic periods, the threshold is the null's).

## The lens

The design lens kept the statistic requirement-derived, but it worked on one scene (Jupiter,
circular), synthetic plants, and laws that answer on the reference's own states; the real
plane was never run through it (it cannot be, from this folder), so "the plane fails the
replacement" rests on `planted-drift` (the reference's measured mechanism) and the leak
plants, not on the plane. Multi-planet scenes, where no Jacobi constant exists, are outside
B12 today and outside this run. The iteration count (three designs) is itself a lens artifact:
the red-team's rejected pair (A and B) pointed here, but neither it nor the memo names the
state-adjustment-plus-gap-rank form, and finding it took the failed attempts rather than
prediction.
