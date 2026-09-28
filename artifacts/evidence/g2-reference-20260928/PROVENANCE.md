# Step 2 reference floors (G2.1–G2.4), frozen 28 September 2026

These are the independent Arb reference answers for `es-lattice-gravity-v0`, step 2 scope ([contract](../../../docs/gravity-law.md)). The judge and generator live in `xtask/judge/` (branch `wt/judge`).
- Answers were computed by the judge at `84cff29`; R2 was computed at `ab712de`.
- Later commits change only the case generators, the driver's priority handling, caching and a rigorous speed bound. None changes the mathematics.
- Everything was computed before any evaluator gate run. Nothing was compared with `crates/geodesic`.

## Tools and machine

- Python 3.14.3 and python-flint 0.9.0 (FLINT 3.6.0, Arb ball arithmetic). No other package.
- MacBook Air M1, 8 GB, fanless, on battery (71 % → 34 %). Swap was 11.4 of 12.3 GB, and other agents kept the load at 5–9. Jobs ran at `nice` 5–15, two to six at a time.

## Method, and why it is independent of the crate

The crate evaluates Carlson symmetric integrals in Mino time on an integer interval ladder. The judge shares neither code nor formulation.

- **Exact integers decide the symbolic cases:**
  - T = T0 → x0, and T < T0 → `Before`;
  - radial motion (x0 × k0 = 0), where an axis coordinate stays exactly 0;
  - exact turning points: the sign of dr/dT and of R′(u0) comes from integers;
  - exact circles: k0·x0 = 0 and |k0|²r0 = MQ², with r0 an integer;
  - exact E = 1 (see below).
- **First integrals are balls:**
  - timelike: E = γ(1 + β·u) and L = γ x × v, with v = k/Q;
  - light: u = k/|k|, E = 1 + β·u and L = x × u.

  The real roots of R(u) = E² − ε + 2Mεu − L²u² + 2ML²u³ (u = 1/r) are certified by the interval Newton operator.
- **A phase that passes smoothly through turning points:**
  - between two roots: u = u1 + 2h sin²(χ/2);
  - from a root to the horizon or to infinity: u = u_t + σ²;
  - radial motion: the cycloid η, or w = √r.

  dT, dφ and dτ are integrated in that phase by rigorous Gauss–Legendre quadrature (`acb.integral`). The river-time integrand is rationalized, dT/dτ = (E² + 2Mu(ε + L²u²)) / (E − √(2Mu)·dr/dτ), so it stays regular at r = 2M and the two horizon logarithms never appear separately.
- **Inverting T → phase:** safeguarded Newton finds the phase, then the interval Newton operator certifies it. Bound orbits use certified period integrals, times the exact period count.
- **Range exit:**
  - A branch and bound runs over the phase pieces where r ≥ 2^96, using enclosures of X; each leaf leaves at most 3 candidate chronons, which are evaluated pointwise.
  - It is skipped when (2^96 − r0) > 2Q (T − T0), since |dX/dT| < 2c.
- **Precision:** every case starts at 256 bits. A comparison, floor or ceiling that its ball cannot decide restarts the whole case at 512, then 1024, then 2048 bits. A case still undecided at 2048 bits is `UNSETTLED`, never guessed. A floor is returned only when its ball excludes every integer.
- **Exact E = 1 test.** With n = |x0|², d = k0·x0, K = |k0|², A = 2M(d² − Q²n) and B = 4M²Q² + Kn, E = 1 ⇔ A + B√n = −4MdQ√(2M√n). Squaring twice, with the sign checks, gives: E = 1 ⇔ sign(A + B√n) = −sign(d), D = 32M³d²Q² − 2AB > 0, and (A² + B²n)² = D²n.

## Files

Each file holds one JSON object per line, gzipped. Every integer is a decimal string.

**`*.cases`** records `{id, rung, class, M, Q, t0, x, k, motion, T[]}`, plus construction notes.

**`*.answers`** records `{id, answers[{T, at, x | chronon, tau, dist, prec, …}], secs, diag?}`:
- `at` is one of `Free`, `Absorbed`, `OutOfRange`, `Before` or `UNSETTLED`;
- `tau` is proper time, in chronons;
- `dist` is the log2 of each coordinate's distance to the nearest integer (a diagnostic);
- `prec` is the precision (bits) that decided the case.

**R2** is not stored as cases: `geodesic_judge.r2_anchor_list()` regenerates it from the spec. `R2.answers` holds `[x, y, kx, ky, [answers for T = 1..8]]`, where each answer is `[⌊X⌋, ⌊Y⌋]`, `"A<chronon>"` or `"O<chronon>"`.

**Other files:**
- `selfcheck.jsonl`: the output of `selfcheck.py`;
- `precision-and-revision-compare.jsonl`: the two-precision and cross-revision comparisons;
- `SHA256SUMS`: the checksums.

**To regenerate** (in `xtask/judge`, with the venv python):
```
cases.py OUT R0 R1 R3 G22 R4 G24 G24edge FB R5
geodesic_judge.py solve OUT/X.cases.jsonl.gz OUT/X.answers.jsonl.gz
geodesic_judge.py r2 OUT/R2.answers.jsonl.gz
```
The seeds are in `cases.SEEDS`: 20260928x, with a per-rung suffix.

## Sampler and construction

- **Pinned sampler** (R3, R5):
  - log2 M ~ U[0, 80] and log2 Q ~ U[4, 40];
  - r/M log-uniform on (2, 2^96/M], with a uniform direction;
  - speed relative to the flow ~ U[0, 0.95c] in a uniform direction; light gets a uniform direction with |k| = 2^U[0,40];
  - T − T0 log-uniform on [1, T_max]. T_max is 10^4 radial periods (bound), 4 × the time to absorption (plunging), or twice the time to reach r = 2^97 at the asymptotic speed (escaping), capped at 2^80;
  - classes are the judge's classification of each draw, filled by rejection.
- **R0** is a control: T = T0 (100 cases), plus far-field hops on an axis (200) and in general position (300).
  - Read literally, the rung is empty: x0 + k0(T − T0) is an integer, so "the straight line's distance to the nearest integer" is 0.
  - The rung therefore keeps hops whose certified deviation from that line lies in [2^-30, 1 − 2^-30] for every moving coordinate. Such hops floor to the straight line.
  - Anchors on the negative axis or in the third quadrant make the pull point along +x and +y.
  - Hops whose deviation lies within 2^-30 of an integer went to R4.
- **R1:**
  - 340 radial cases: bound, inward, outward, light in and out, and 40 at rest in the flow (E = 1);
  - 200 exact stable circles;
  - 20 exact circles at r = 4M, which are unstable, have E = 1 and a double root.
- **R4** relies on the exact scale invariance of the metric: the anchor (λM, Q, λx0, k0, λ(T − T0)) gives the position λX.
  - For a base case in each chart, X is computed at 512 bits.
  - λ is the smallest continued-fraction denominator of frac(X_c) with |λ·frac(X_c) − p| < 2^-40 that stays within the ranges.
  - Every scaled case was then solved from scratch.
  - Counts: radial 200, circular 200, three-root 400 (202 bound), one-root 200 and light 200. All 1,200 are certified within 2^-40 of an integer, the farthest at 2^-40.003.
  - R4 also holds the 300 far-field hops set aside from R0. Their deviation from the integer line is certified in (0, 2^-30], down to 2^-118.
- **G2.2:**
  - 510 R3 anchors: 1,600 bound, 1,600 near-circular, 1,216 near-ISCO, 624 near-separatrix and 1,600 long-T, all with (p − p_sep)/p ≥ 10^-4 (p_sep = 6 + 2e), plus 95 scattering light anchors;
  - 16 query times each, log-uniform within 10 radial periods (for light, within the escape time scale);
  - `diag` gives p and e to 80 digits, the separatrix margin, the periods in T and τ, the advance per radial period, b, the deflection and r_min.
- **G2.4:**
  - **Infall from rest** (k0 = 0) at r0 ∈ {10M, 100M}. All T_h values match the closed form (cycloid t plus the river term, with the logarithms combined analytically, from `closed_form_infall_from_rest`) to better than 2^-200. Each case stores its closed-form T_h. The queries are ⌈T_h⌉ − 1, ⌈T_h⌉, ⌈T_h⌉ + 1 and ⌈T_h⌉ + 2^40.
  - **Exact E = 1 anchors**, moving inward at r0 = 2Mj² on an axis (j = 2, 3). They are integer points of the conic Q²(j² − 1) + 2aQj − a²j²(j² + 1) = k²j⁴, with k0 = (−a, k), rationally parametrized through (14, 3, 6) and (111, 28, 24).
  - The integer test proves E = 1 for every anchor. For all 120 anchors, the judge's class matched the side: plunging (absorbed) for |L| ≤ 4M(1 − 10^-6), unbound (escapes) for |L| ≥ 4M(1 + 10^-6).
  - Here |L|/4M − 1 lies between 8.5·10^-5 and 10^-2. `G24edge` (below) covers 10^-6 to 10^-5.
  - The generator also found the exact separatrix (Q, k0) = (14, (−3, 6)) at r0 = 8M, where E = 1 and L = 4M. The judge answers UNSETTLED there, so it is not in the set.

## Results (first freeze: R0–R4, G2.2, G2.4)

| File | Cases | Queries | Free | Absorbed | OutOfRange | Before | UNSETTLED | Share with some \|x_c\| ≥ 2^62 |
|---|---|---|---|---|---|---|---|---|
| R0 | 600 | 600 | 600 | 0 | 0 | 0 | 0 | 0.63 |
| R1 | 560 | 560 | 537 | 21 | 2 | 0 | 0 | 0.53 |
| R2 | 22,092 anchors | 176,736 | 12,736 | 164,000 | 0 | 0 | 0 | 0 |
| R3 | 1,300 (13 classes × 100) | 1,300 | 1,045 | 60 | 95 | 100 | 0 | 0.52 |
| R4 | 1,500 | 1,500 | 1,500 | 0 | 0 | 0 | 0 | 0.57 |
| G2.2 | 510 | 8,160 | 8,138 | 0 | 22 | 0 | 0 | 0.44 |
| G2.4 | 200 | 716 | 350 | 360 | 6 | 0 | 0 | 0.27 |

- R2's counts were verified: 22,092 valid anchors out of 23,409. Of the rest, 1,053 have r ≤ 2M and 264 are not below c relative to the flow.
- The R3 classes are those of G2.1: bound, unbound, plunging, radial, light, near-circular, near-ISCO, near-separatrix/whirl, near-horizon, T = T0, long-T (10^3–10^4 periods), range exit near ±2^96 and T < T0.
- **Two precisions.** Every rung was re-solved from a 512-bit start. Every settled answer is identical: 0 differences out of 189,572 queries.
- **Two revisions.** R0, R2, R3, G2.2 and G2.4 were also solved by an earlier judge revision. That revision used a different phase formula, u = m − h cos χ, and a different cache. It gave 0 differences.
- **Compute.**
  - Per-case sums at the primary schedule: R2 543 s, G2.4 546 s, G2.2 102 s, R3 93 s, R4 80 s, R0 30 s, R1 20 s.
  - The second-precision runs took about 3× that.
  - Generation took about 25 minutes of CPU.

## Self-checks (`selfcheck.jsonl`, all pass)

- **The oracle's single-mass rows** (H0178/H0183, `gr-oracle-20260928/rows.jsonl`) agree at ≤ 2.7·10^-15, against a threshold of 10^-12, over all 38 rows:
  - 8 periapsis advances (the e = 0 row is evaluated with the exact double root);
  - 10 radial periods in t and in τ;
  - 6 light deflections;
  - 4 Shapiro delays;
  - 10 clock rates (static and circular, from the flow-frame Lorentz factor).
- **The contract's examples:**
  - M = 1, Q = 25, x0 = (30, 40), k0 = (−3, −4): T = 1 gives (26, 35), T_h = 496/75, and the singularity falls at 20/3;
  - M = 1, Q = 3, x0 = (9, 0), k0 = (0, 1) is the stable circle at r = 9M, with Ω = 1/9 per chronon.
- **Newtonian limit:** at r/M = 10^6, 10^8 and 10^10, the deviation from Kepler is 1.0·10^-6, 9.9·10^-9 and 2.3·10^-10 of r (∝ M/r), and (P/P_N − 1)/(3/a) = 1.0000 (1PN).
- **Closed-form infall from rest:** agreement to 10^-150 at M up to 2^79.
- **Development cross-checks,** not stored as evidence: float RK4 on Hamilton's equations in PG Cartesian coordinates (an independent derivation) matches every chart to 10^-11–10^-15. That covers bound orbits over 20 periods, scattering, inner and outer plunges, one-root escapes, exact E = 1 orbits, radial motion and light. Range-exit chronons match the straight-line prediction and an independent binary search over integer times.

## Limitations

- **The judge is not a proof assistant.** Its rigour rests on Arb's ball arithmetic and on the formulas above, which match an independent RK4, the closed forms and the oracle. An error shared by these formulas and all three checks would go unnoticed.
- **Exact degeneracies that no integer test covers end as UNSETTLED.** One example is the exact separatrix, E = 1 and L = 4M. The frozen set contains none.
- **The fallback cases (`FB`)** and the G2.4 band-edge file (`G24edge`) come in a follow-up commit. R5 is secondary, and only its finished slices are frozen (see `R5-STATUS`, when present).
