# Step 2 reference floors (G2.1–G2.4), frozen 28 September 2026

These are the independent Arb reference answers for `es-lattice-gravity-v0`, step 2 scope ([contract](../../../docs/gravity-law.md)). The judge and generator live in `xtask/judge/` (branch `wt/judge`).
- Answers were computed by the judge at `84cff29`; R2 was computed at `ab712de`, and G24edge, FB and R5 slice 0 at `2057ee1`.
- R5 slices 1–9 were computed by the integrator with this `solve` at `4dfcd4e`.
- Three R5 records (R5s-00711, R5s-00763, R5s-00792), UNSETTLED there, were re-solved at `fda6ee0`, which adds the whirl windows below; no other record was touched.
- The final judge revision is `2bbd029`: its self-checks are identical to `selfcheck.jsonl`, and every file's settled answers match a 512-bit-start re-solve.
- Later commits change only the case generators, the driver's priority handling, caching, a rigorous speed bound and the whirl windows. None changes a settled answer: R3, R5 slice 0 and G2.2 re-solved at `fda6ee0` are identical record for record apart from timing.
- Everything was computed before any evaluator gate run. Nothing was compared with `crates/geodesic`.

## Tools and machine

- Python 3.14.3 and python-flint 0.9.0 (FLINT 3.6.0, Arb ball arithmetic). No other package.
- MacBook Air M1, 8 GB, fanless. The first freeze ran on battery (71 % → 21 %), the R5 completion and the whirl fix on AC. Swap reached 11.4 of 12.3 GB, and other agents kept the load at 3–9. Jobs ran at `nice` 5–15, two to six at a time.

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
- **Whirl windows (near-separatrix two-root orbits,** u3 − u2 = δ < 2^-10 h):
  - there u3 − u = δ + 2h sin²(ψ/2), with ψ = χ − π (mod 2π), puts a branch point about √(2δ/h) from the real axis at every periapsis;
  - inside |ψ| < 3/2 the judge integrates in t, where sin(ψ/2) = κ sinh t and κ² = δ/(2h);
  - then u3 − u = δ cosh² t exactly, and dφ/dt = 1/(√(Mh) √(1 − κ² sinh² t)), dτ/dt and dT/dt are smooth;
  - outside the windows the χ quadrature is unchanged.
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
- **G24edge (band edge):** 59 exact E = 1 anchors on the same conics with 1.5·10^-6 ≤ | |L|/4M − 1 | ≤ 9.9·10^-6, taken from lines close to the tangent plane at the base point. There are 29 on the absorbed side and 30 on the escape side, and all behave as their side requires. In 11 of them ⌈T_h⌉ = T0 + 1, so the case has no free query before absorption.
- **FB (fallback, |X| ≤ 2^12):**
  - **Circular (150):** x0 = (r, 0), r = Mw², Q = w and k0 = (0, ±1), so X = r(cos, sin)(ΔT/r) exactly.
    - ΔT is chosen by LLL (a Kannan embedding) so that ΔT/r ≡ ±arccos(n/r) mod 2π. That puts X_x between 2^-35 and 2^-53 of the integer n (median 2^-43), above or below it.
    - The phase is kept below about 2^47·2π, so a 64-bit enclosure stays narrow.
  - **Other charts (150):** the nearest of a 1,500-anchor random search (2^-2.5 to 2^-16).
  - **`FB.widths`** records, per case, the boundary n, the side, the log2 distance, the two admissible results {n − 1, n} for the coordinate, and the judge's own certified width of X at 64 and at 128 bits:
    - the width is below 1/4 quantum for 298 of 300 cases, the eligible fallback cases (FB-0016 and FB-0098 are not eligible);
    - in 146 of them (all circular) the distance is below that width, so a 64-bit evaluation can straddle n and force the final-midpoint rule;
    - the 150 other-chart cases are small-magnitude near-integers that a 64-bit evaluation still decides.
- **R5 (secondary):** the pinned sampler, with 4,000 anchors in each of bound, unbound, plunging, radial and light (20,000), plus 300 in each of the eight constructed classes (2,400). `R5.cases` holds all 22,400. Slice i is cases i, i + 10, …, so every slice spans every class. `R5-slice0.answers` to `R5-slice9.answers` hold all 22,400 answers. The full R5 of G2.1 is the union of R0–R4, G2.4 and this file.

## Results

| File | Cases | Queries | Free | Absorbed | OutOfRange | Before | UNSETTLED | Share with some \|x_c\| ≥ 2^62 |
|---|---|---|---|---|---|---|---|---|
| R0 | 600 | 600 | 600 | 0 | 0 | 0 | 0 | 0.63 |
| R1 | 560 | 560 | 537 | 21 | 2 | 0 | 0 | 0.53 |
| R2 | 22,092 anchors | 176,736 | 12,736 | 164,000 | 0 | 0 | 0 | 0 |
| R3 | 1,300 (13 classes × 100) | 1,300 | 1,045 | 60 | 95 | 100 | 0 | 0.52 |
| R4 | 1,500 | 1,500 | 1,500 | 0 | 0 | 0 | 0 | 0.57 |
| G2.2 | 510 | 8,160 | 8,138 | 0 | 22 | 0 | 0 | 0.44 |
| G2.4 | 200 | 716 | 350 | 360 | 6 | 0 | 0 | 0.27 |
| G24edge | 59 | 136 | 78 | 58 | 0 | 0 | 0 | 0.23 |
| FB | 300 | 300 | 300 | 0 | 0 | 0 | 0 | 0 |
| R5 (10 slices) | 22,400 | 22,400 | 20,531 | 1,109 | 460 | 300 | 0 | 0.59 |

- R2's counts were verified: 22,092 valid anchors out of 23,409. Of the rest, 1,053 have r ≤ 2M and 264 are not below c relative to the flow.
- The R3 classes are those of G2.1: bound, unbound, plunging, radial, light, near-circular, near-ISCO, near-separatrix/whirl, near-horizon, T = T0, long-T (10^3–10^4 periods), range exit near ±2^96 and T < T0.
- **Two precisions.** Every file was re-solved from a 512-bit start. Every settled answer is identical: 0 differences out of 212,408 queries (R0–R4, G2.2, G2.4, FB and G24edge: 190,008; R5: 22,400, at `fda6ee0`, which for slices 1–9 is also a cross-revision check).
- **Two revisions.** R0, R2, R3, G2.2 and G2.4 were also solved by an earlier judge revision. That revision used a different phase formula, u = m − h cos χ, and a different cache. It gave 0 differences.
- **Compute.**
  - Per-case sums at the primary schedule: R5 895 s (22,389 cases decided at 256 bits, 11 at 512), R2 543 s, G2.4 546 s, G2.2 102 s, R3 93 s, R4 80 s, R0 30 s, R1 20 s.
  - The three whirl cases now take under 1 s each. Before the fix they ran for hours of CPU and ended UNSETTLED.
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
- **Whirl windows** (verification scripts not stored):
  - windowed and plain χ quadrature (evaluation limit 10^7) agree on 96 integrals of T, φ and τ over random intervals of four orbits with δ/h from 2·10^-4 to 10^-10: the balls overlap, and the largest relative difference is 1.2·10^-73;
  - full solves with windows and with plain quadrature give identical floors and 25-digit τ on three whirl orbits (margins 2.4·10^-7 to 2.5·10^-9);
  - R5s-00711, solved by plain quadrature from a 512-bit start, gives the same floor (−16, 45) and the same 30-digit τ;
  - an RK4 of the PG Hamilton equations in 160-bit arithmetic converges at 4th order onto the judge (Richardson agreement to 10^-4 quanta at 7·10^6 quanta), at margins 1.5·10^-4 and 2.4·10^-7;
  - float64 RK4 cannot be used there: its roundoff, amplified by the whirl, moves the position by about 10^-5 relative as the step changes.
  - the three repaired cases give identical floors at window half-widths 1.5 and 2.5, starting from 256 or 1024 bits (R5s-00792's 30-digit τ is identical too);
  - plain quadrature cannot settle R5s-00792 at all (a δ/h ≈ 10^-10 whirl, then an escape to 2^75 quanta), so for that case the window width and the precision are the independent variations.
- **Development cross-checks,** not stored as evidence: float RK4 on Hamilton's equations in PG Cartesian coordinates (an independent derivation) matches every chart to 10^-11–10^-15. That covers bound orbits over 20 periods, scattering, inner and outer plunges, one-root escapes, exact E = 1 orbits, radial motion and light. Range-exit chronons match the straight-line prediction and an independent binary search over integer times.

## Limitations

- **The judge is not a proof assistant.** Its rigour rests on Arb's ball arithmetic and on the formulas above, which match an independent RK4, the closed forms and the oracle. An error shared by these formulas and all three checks would go unnoticed.
- **Exact degeneracies that no integer test covers end as UNSETTLED.** One example is the exact separatrix, E = 1 and L = 4M. The frozen set contains none.
- **Near-separatrix orbits of the other charts are not windowed.** An inner plunge whirl (σ chart) or a one-root orbit near a complex double root has the same kind of near singularity at σ = 0. No frozen case of that kind failed, but a harder one could escalate towards UNSETTLED.
- **FB is weak outside the circle.** Only the circular fallback cases force the midpoint rule at 64 bits. The other charts reach 2^-16 at best at |X| ≤ 2^12, so a 64-bit evaluation still decides them.
- **The "reduced final width" is the judge's own** 64-bit Arb width. The crate's width W is still unproven.
