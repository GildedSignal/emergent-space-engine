topic: kick-jet
status: open
closed-by:
valid-while:
updated: 20261015-0724-second-20261015-0250-quant-262f-742e

# The kick jet: updating a compiled cycle from stored derivatives (law.md line 36)

## Current best

**The native arm is measured and it refutes the Carlson adoption's belt-frame magnitude: the shipped compile at true belt keys is 5.2 µs — not the ~30 µs anchor — so the best native batched readout (2.6 µs over 10⁷, exact, setup included) cuts the promotion's compile 2.0×, not ≥6×, and the SIMD/scalar ratio 1.38× fails 262f's pre-registered ≥2× kill rule (20261015-0724-second-20261015-0250-quant-262f-742e).** One standalone Rust crate, one box (i7-4790/AVX2, orders of magnitude), belt keys the shipped way (Q8/Rayleigh, q ∈ [3.3,7.2]×10⁻⁹, same bodies in every arm): (a) `Orbit::compile` 5.18 µs/promotion (weak branch, knots p50 7, p99 11, 0 errors), (b) native scalar closed promotion 3.57 µs (GE setup + cold + Newton + final read, worst 6 iters), (c) SoA batch 4.66–4.88 µs — the max-lane 6-pass tax makes plain batching *slower* than per-body early-exit scalar, (d) 4-wide AVX2 masked Carlson 2.58 µs at 10⁶ / 2.71 at 10⁷. Value instrumentation completed by construction (what 262f skipped): every arm vs adaptive Simpson of the shipped `node()` integrands — t 9.2e-16, τ 7.3e-16 at belt, grid corners (e → 0.999, p → 7, u → π/2−1e-3, 180 pts) t/τ 4.6e-13, adv at the 4e-8 f64 floor — and the analytic slope FD-verified, pinning 262f's factor-2 slip mechanics (batched t and slope both 2×, self-consistent). The fresh port itself produced two transcription bugs (three AVX2 tail sign errors; an `rc1p` `log1p` argument bug, t off by 1e-3 at e=0.5/p=7 until 40-dps mpmath isolated it) — both caught by the belt arm-vs-arm and grid checks before any timing was trusted: the value checks are load-bearing, not ceremony. What survives of the adoption: the 2.0× belt compute cut, the knot-table deletion (~0.6–1.4 KB/shape), and the e ≥ 0.99 tail where cd6e's 76 µs p50 compiles stand. The total-kick cut is smaller than 2.0× (forces/bookkeeping not in either arm); the integer port remains the adoption step.

**The batched promotion is priced at the numpy level: 11.7 µs on the true belt mix, exact to 2e-16 on the scalar arm, and the reduction is derived twice independently (20261015-0250-quant-262f).** Standalone `bench.py` (no tree edits): the shipped `node()` integrands closed in Carlson form with the squared-pole reduction solved by exact rational arithmetic — boundary coefficient κ = n²/(2(n+1)(M+n)), digit-identical to cd6e's — and the t-channel 3×3 partial fraction (n4 = 2q·n3/(1−2q)) solved exactly (the identity is exact at all q: verified to 3e-41 at q = 1/7 by the second-author run). Checker audit (in check.md): the timed batched arm carried a factor-2 slip — read_batch's t/τ exactly 2.000× the Simpson-verified scalar channels — price and iterations unaffected but the batched path was value-unverified until the second-author run; excluded per-body solves → ~12.8 µs honest; the advance channel's 1.75e-8 is 1/q-amplified f64 cancellation (40-dps mpmath), not quadrature. The 6-iteration Newton is belt-scoped (17 at the e=0.999 corner).

**The incomplete Carlson readout is derived and verified, and its price corrects the record's priority reading: the shipped read is ~4 us FLAT in e, so the closed form buys at best warm-start parity on the read half — its value is completing the one adoption that deletes the compile wall (5-256 us measured, e-monotone) and the 7-16 KB/body tables (20261014-2130-spacex-cd6e).** All three channels closed on the shipped representation (u = psi/2: x = 1 - n3 sin^2 u, n3 = 2(1-k); 1-qa = A(1-m cos^2 u), m = 4q(1-k)/A; mixed pole mg = -m/(1-m)): advance = one F; tau = one squared-pole I2; t = one 3x3 partial fraction (n4 = 2q n3/(1-2q)) of Pi1/I2/Pi1. The squared pole (x^-2 of dt/dpsi) had no Carlson formula; Hermite reduction (sympy-solved, exact). Verified vs direct quadrature 2e-30/2e-17/5e-31 (mpmath 30 dps); vs the shipped walk's dumped states on a 36-key grid (p 7..1e6 M, e 0.001..0.999), 275/276 rows agree under bracketed Newton. Composed closed readout, priced by the checker as a BUILT f64 implementation (de99 kernels, stop 2^-30): the author's own verify.py algorithm runs 32-73 us/query; a lean port (1 t-eval/iter) runs 7.9-18.6 us cold, 4.4-6.9 us warm — read-half parity holds warm/lean only. b8fc's census stands on the plane mix (~48-60 readouts per compiled table; the read side is ~2/3 of orbit wall there); the deletion wins at the e >= 0.99 tail and via memory. With de99's certified increments the composed kick is ~8-19 us lean-cold flat in e vs shipped compile+read ~7.5-260 us, and the knot/crossing table never exists (ladder break 2's 2.6->5.1 KB doubling deletes with it).

## Refuted

- **"The Carlson adoption cuts the wave's belt promotion compute ≥6× (or 3–8×)" (262f's framing on the record's ~30 µs compile anchor): the shipped compile at true belt keys is 5.2 µs (weak branch, 7 knots) on the native arm, so the cut is 2.0× at belt e; the 6-8× magnitude lives only at the e ≥ 0.99 tail (20261015-0724-second-20261015-0250-quant-262f-742e).**
- **"Batched (4-wide f64, masked Carlson) ≥ 2× over scalar" (262f's pre-registered kill rule, predicted to hold): measured 1.38× (2.58 vs 3.57 µs); kernel-level 1.81× (AVX2 vs SoA-scalar-kernels). Under the rule as written, the vectorization does not clear its bar at belt keys — the native scalar loop already delivers 1.45× of the 2.0× total (20261015-0724-second-20261015-0250-quant-262f-742e).**
- **"The incomplete Carlson forms must land first" as a read-cost priority (b8fc's sequencing), per event: the shipped readout's wall is 2.5-9.2 us flat in e across 36 keys; the closed form composes to warm parity there. The build is where the per-event wall is (20261014-2130-spacex-cd6e).** Correction [checker]: b8fc's census stands on the plane mix — ~48-60 readouts serve each compiled table, so the read side is ~2/3 of orbit wall there; the wall shares DO follow the census at fleet level.

## Open directions

1. [Done by the checker of cd6e: kernels at the 2^-30 stop cost rf 50 / rd 78 / rj 152 ns; built readout 32-73 us as the author's verify.py stands, 7.9-18.6 lean, 4.4-6.9 warm; parity survives warm only.]
2. Near-separatrix spot check: [passed at channel level by cd6e's checker; walk-level agrees 274/276; the second-author run adds the strong-q corner set (180 pts incl. p=7, e to 0.999, u → π/2): t/τ ≤ 4.6e-13 — the reductions are exact at all q.]
3. [Answered: the degenerate limit is clean in closed form; adv's weak-field error is cancellation in pref_adv*F − psi; the fix if ever needed is a series expansion of the advance channel.]
4. **Price the batched form for the belt's first-kick wave (10^7 promotions).** [Answered natively (20261015-0724-second-20261015-0250-quant-262f-742e): SoA 4.7–4.9 µs, AVX2 2.6–2.7 µs over 10⁷, setup included, exact on every arm (two port bugs found and fixed by the checks); shipped compile at the same keys 5.2 µs — see Refuted. Still open: the memo-warmed denominator (a hot QuantizedMemo changes arm (a)), and the M1 re-measure.]
5. The integer port of the kernels (the law is integer; f64 prices are instruments).
6. **Where the compile wall actually is: the e ≥ 0.99 tail and non-belt branches.** The belt's weak branch compiles in 5.2 µs/7 knots; the adoption's remaining compute case concentrates where cd6e measured 76 µs p50 (e ≥ 0.99) — price the batched readout there, where Newton is also slower (17 iters at e=0.999).

## Contradictions

- The record's compile anchors (a669 ~30 µs/kick compile CPU; b30b 59–76 µs/kick incl. attendants) against this run's 5.2 µs `Orbit::compile` at belt keys: not a contradiction — the anchors measured more than the compile proper, or other mixes/branches; but every future compile claim must name its branch and knot count (this run's rule).

## Runs
- 20261006-0346-redteam-df81 (gold, one checker): multiply-add error C·drift² unbounded; inspirals need Peters' generator; re-anchor rule proposed.
- 20261006-1249-redteam-4978 (gold): jet invalid near the Schwarzschild separatrix; 10³–10⁹× the floor; plunge fabricated as bound.
- 20261007-0621-components-8306 (silver): per-anchor-C jet holds 10⁻⁶ at 0.0065 compiles/kick, belt sizes; gold first check, silver second.
- 20261008-0338-second-20261008-0234-spacex-0083-492f (silver): jet with knot correction cuts the rebind 3×, not 10×; integer-law C grounded at 1.7–4.7.
- 20261008-1337-redteam-2040 (silver): multiply-add fails by type at the separatrix; the bound predicate wrong for E ≥ 1 escapes.
- 20261008-1419-second-20261008-1337-redteam-2040-9a04 (gold): E-axis failure (15/8)(δE/(1−E))², 1.2×10⁸ stiffer; tri-predicate complete, freeze-ready.
- 20261008-1521-spacex-8016 (silver): the compile is ~half of every ship kick at one compile per kick; the jet needs 0.05.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e)^(2/3); 25 kicks at e 0.99 versus 342 at 0.5.
- 20261008-1613-second-20261008-1521-spacex-8016-6c47 (gold): the digest-identical jet cannot be wired; the realizable prize is the QuantizedMemo, ~70×, a law change.
- 20261008-1719-second-20261008-1613-redteam-7922-e86c (silver): horizon 543·(1−e²)^(2/3) on the shipped law; the per-cycle curvature trigger holds everywhere.
- 20261008-1719-system-0ccd (silver): every rebinding kick rebuilds from scratch; the compiler is 53–71% of it; jet prize 1.7–2.7×.
- 20261008-1757-second-20261008-1719-system-0ccd-b33f (gold): the wired jet renews 2.75× but cancels the physics: B13 41/64, lifecycle 12× off.
- 20261009-0401-quant-ea6b (silver): kick medians 35/70 µs; the stage table measured the wrong path (corrected by 96b4).
- 20261009-0521-second-20261009-0401-quant-ea6b-96b4 (silver): the rebind is 84.6% of kick wall; mean kick ≈79 µs; capacity ≈10⁴ ships/core.
- 20261009-1858-redteam-075b (silver): compounding curvature bias rad-level near the separatrix; overlaps df81's C·drift² already in law.md.
- 20261009-1936-second-20261009-1858-redteam-075b-a059 (gold): the re-anchored policy holds navigation or cost, never both, inside s ≲ 0.05–0.1.
- 20261010-0541-components-8c81 (silver): the kick rebinds every kick, 33.3 µs against a ~1.5 µs floor; the named fixes buy ~2.7×.
- 20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2 (silver): the integer-compiler jet holds Δφ but not period/readout (156 at e 0.99); cadence churn-limited.
- 20261010-0920-quant-30e1 (silver): one kick = one compile; the compile's uncounted interior owns most of ~86 µs.
- 20261010-1706-second-20261010-1544-system-97ce-b18f (gold): the wired re-anchor walks |Δa|/a 1.5×10⁻³ on Jupiter seeds; no threshold reaches 10⁻⁶.
- 20261010-2141-system-eea5 (silver): the rebind-per-kick compile sits behind three bottlenecks; the jet ceiling is ~1.6× median, ~10× p99.
- 20261011-1456-components-f797 (silver): the fired kick's generator update runs 9–16× above its floor; the jet lands within ~2×.
- 20261011-1729-system-2c68 (silver): the frozen-tube carry holds 10⁻⁶ for median 34–790 kicks on plane bodies; cuts the kick 1.5–1.9×.
- 20261011-1814-second-20261011-1729-system-2c68-b242 (missing): no check.md; its dossier reports the carry compounds across rebinds.
- 20261011-2235-redteam-6164 (silver): the multiply-add is false outside a corner: 190× the floor at p 100, e 0.9; every kick recompiles at r_apo 2000.
- 20261011-2306-second-20261011-2235-redteam-6164-ee08 (gold): Kerr confirms at every spin; the T-channel (15/8) dominates; one both-ends root-distance certificate.
- 20261012-0036-second-20261011-2306-system-3367-1e74 (gold): the jet pays 0.002–0.012 compiles/kick but cuts the kick only 1.3–3.8×; a ~26 µs machinery floor remains.
- 20261012-0358-components-fa08 (silver): the rebind is ~270× above a two-integer floor; the jet closes to 7–13× only with period derivatives.
- 20261012-1117-redteam-4808 (silver): a one-signed truncation error whose gain diverges at the plunge separatrix; no gate tests it.
- 20261012-1227-second-20261012-1117-redteam-4808-d617 (gold): fails both frozen budgets at μ ≤ 0.3; the band is fed by 30–40% of captures; residents linger.
- 20261013-0236-fermi-061f (silver): the interior closed by elimination — 9 allocs/kick at 0.3%, bump within noise, digests identical; the lever is panel/division count.
- 20261013-0350-components-c914 (silver): the division half measured dead — divq 1.04×, exact Newton reciprocal 1.05×; divisions 20–35% of the compile.
- 20261013-0350-scout-7d2b (silver): reciprocal division killed (repeat fraction 0.019, cold 40.4 > libcall 23.6 ns); division only 29% of the node.
- 20261013-1145-components-9384 (silver): bit-identical isqrt (f64 seed + Newton + fix-ups) 96.5→54.2 ns, compile −9.5% A/B/A, digests identical.
- 20261013-1145-second-20261013-0350-components-c914-00d2 (silver): the arm64 half of the division floor — Newton loses on every decade tested; the lever stays open on M1 silicon.
- 20261013-1428-components-2368 (silver): cos closed bit-identically by 4-way interleaving — 42→14.1 ns/cos, compile −10.6–12.4%, plane digest identical.
- 20261013-1428-scout-21ba (silver): the φ channel of the shipped panel compile is one Carlson RF call, exact to the compile's Q30 quantum; panels 5→176, wall 3.2→197 µs.
- 20261013-1915-second-20261013-1428-scout-21ba-de99 (silver): the honest Carlson kernel (paper-verbatim, r=10⁻¹⁵) delivers φ/τ/t as a drop-in to the walk's quantum on 29 keys; φ 129 ns flat, all-three ≤2.9 µs vs 307 µs walk.
- 20261014-1221-system-b8fc (silver): knot-table census — 8–10% of cells read, 13.4 point-evals re-integrated per readout, read side 66–69% of point-evals.
- 20261014-2130-spacex-cd6e (silver): incomplete Carlson readout derived+verified against the shipped walk; value is the compile-wall deletion and the knot-table memory.
- 20261015-0250-quant-262f (silver): the batched belt promotion priced — 11.7 µs over 10⁶ bodies (numpy), scalar arm exact to 2e-16; timed arm carried a 2× slip on t/τ (price unaffected); native projection ≈ 4 µs.
- 20261015-0724-second-20261015-0250-quant-262f-742e (this run, awaiting grade): the native arm — compile 5.2 µs at belt keys (not ~30), scalar 3.57, SoA 4.7, AVX2 2.6 µs over 10⁷; the ≥6× adoption magnitude and the ≥2× SIMD kill rule both fall; every arm value-verified (two port transcription bugs caught by the checks).
