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
- 20261011-1814-second-20261011-1729-system-2c68-b242 (missing): no check.md; its dossier reports the carry compounds across rebinds (2c68's bound was a shadow artifact).
- 20261011-2235-redteam-6164 (silver): the multiply-add is false outside a corner: 190× the floor at p 100, e 0.9; every kick recompiles at r_apo 2000.
- 20261011-2306-second-20261011-2235-redteam-6164-ee08 (gold): Kerr confirms at every spin; the T-channel (15/8) dominates; one both-ends root-distance certificate.
- 20261012-0036-second-20261011-2306-system-3367-1e74 (gold): the jet pays 0.002–0.012 compiles/kick but cuts the kick only 1.3–3.8×; a ~26 µs machinery floor remains.
- 20261012-0358-components-fa08 (silver): the rebind is ~270× above a two-integer floor; the jet closes to 7–13× only with period derivatives.
- 20261012-1117-redteam-4808 (silver): a one-signed truncation error whose gain diverges at the plunge separatrix; no gate tests it.
- 20261012-1227-second-20261012-1117-redteam-4808-d617 (gold): fails both frozen budgets at μ ≤ 0.3; the band is fed by 30–40% of captures; residents linger.
- 20261006-0220-autoresearch-c3a5 (silver): a weak-hyperbolic quadrature shortcut is bit-identical and cuts the leaver-kick ladder 40–45%.
- 20261006-0437-constraint-ec9d (silver): the leaver-kick tail is Passage::compile (318–356 of 365–381 µs), not the rebind fit; every passage rebind is a leaver.
- 20261007-1843-second-20261007-1801-fermi-bb60-152f (silver): exact-key memo hit 0.0 on 3,108 distinct rebinds, held on unseen seeds and a 200-member fleet.
- 20261008-0234-spacex-0083 (silver): compile-bound kick: compile 64.5% of a 97 µs median, rebind 78.7%, forces 9%; the cheap jet is dead everywhere.
- 20261008-1419-components-620e (silver): the fired kick is ~25× above its floor: rebind 68%, shared secondaries 27%, forces 6%; integer evaluator not adoption-ready; gold first check, silver second.
- 20261008-1521-autoresearch-a48d (silver): fit_only deletes one dead trajectory decode per kick: −10.9% (33.1→29.5 µs), digest bit-identical, adoptable.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e)^(2/3); 25 kicks at e 0.99 versus 342 at 0.5; gold first check, silver second.
- 20261008-1719-second-20261008-1613-redteam-7922-e86c (silver): horizon 543·(1−e²)^(2/3) on the shipped law; the per-cycle curvature trigger holds everywhere; gold first check, silver second.
- 20261009-0521-second-20261009-0401-quant-ea6b-96b4 (silver): the rebind is 84.6% of kick wall; mean kick ≈79 µs; capacity ≈10⁴ ships/core; gold first check, silver second.
- 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 (gold): sharing one compiled cycle across co-orbital bodies buys 1.08–1.17× (tail 6.3×), not ≥40×: the shareable compile is 9–17%.
- 20261010-1947-autoresearch-2833 (silver): a proper_at_event cache plus cartesian-free orbit_state cuts the pure kick ~9–10%, bit-identical.
- 20261011-1729-system-2c68 (silver): the frozen-tube carry holds 10⁻⁶ for median 72/314/705 kicks on the intended plane bodies (dossier's 34–790 mixes mislabeled rows); cuts the kick 1.5–1.9×.
- 20261011-2235-redteam-6164 (silver): the multiply-add is false outside a corner: 190× the floor at p 100, e 0.9; every kick recompiles at r_apo 2000; gold first check, silver second.
- 20261013-0037-components-009b (this run, awaiting grade): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0236-fermi-061f (pending): the interior closed by elimination — 9 allocs/kick at 0.3%, bump within noise, digests identical; i128 division 30.9 ns; the lever is panel/division count.
- 20261013-0037-components-009b (pending): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261013-0350-components-c914 (this run, awaiting grade): the division half measured dead — divq 1.04×, exact Newton reciprocal 1.05×; divisions 20–35% of the compile, all three named ingredients 42–56%; open direction 1 bounded at ~1.4×.
- 20261013-0350-scout-7d2b (this run, awaiting grade): reciprocal division killed (repeat fraction 0.019, cold 40.4 > libcall 23.6 ns); division only 29% of the node — isqrt 30%, cos 24%.
- 20261013-1145-components-9384 (this run, awaiting grade): bit-identical isqrt (f64 seed + Newton + fix-ups) 96.5→54.2 ns, compile −9.5% A/B/A, digests identical; isqrt lever closed, mul-only reciprocal open.
- 20261013-1145-second-20261013-0350-components-c914-00d2 (silver, second check): the arm64 half of the division floor — Newton loses 2.8× (TCG wall) / 1.49× (instructions) on every decade tested; `__udivti3` executes ~2.8 `udiv`/div (the run's "zero udiv / multiply-only" was a print-cutoff artifact), so the lever stays open on M1 silicon.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e²)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0037-components-009b (silver): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e²)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0236-fermi-061f (silver): the interior closed by elimination — 9 allocs/kick at 0.3%, bump within noise, digests identical; i128 division 30.9 ns; the lever is panel/division count.
- 20261013-0350-components-c914 (silver): the division half measured dead — divq 1.04×, exact Newton reciprocal 1.05×; divisions 20–35% of the compile, all three named ingredients 42–56%; open direction 1 bounded at ~1.4×.
- 20261013-0350-scout-7d2b (silver): reciprocal division killed (repeat fraction 0.019, cold 40.4 > libcall 23.6 ns); division only 29% of the node — isqrt 30%, cos 24%.
- 20261013-1145-components-9384 (silver): bit-identical isqrt (f64 seed + Newton + fix-ups) 96.5→54.2 ns, compile −9.5% A/B/A, digests identical; isqrt lever closed, mul-only reciprocal open.
- 20261013-1428-components-2368 (this run, awaiting grade): cos closed bit-identically by 4-way interleaving of the panel's Gauss nodes — primitive 42→14.1 ns/cos (3.0×), compile −10.6–12.4% A/B/A, plane digest identical, kick resolve 33.2→28.3 µs; unrolling alone refuted (1.01–1.03×).
- 20261013-1428-scout-21ba (this run, awaiting grade): the φ channel of the shipped panel compile is one Carlson RF call, exact to the compile's Q30 quantum on every strong key; panels 5→176 (e→0.999, band cuts), wall 3.2→197 µs vs ~90–420 ns closed form (checker-corrected; the run's 37–39 ns was a timing artifact); panel-count lever now has a named replacement mechanism.
- 20261013-1915-second-20261013-1428-scout-21ba-de99 (awaiting grade): the honest Carlson kernel (paper-verbatim, r=10⁻¹⁵, black_box) delivers φ/τ/t as a drop-in to the walk's quantum on 29 keys; φ 129 ns flat, all-three ≤2.9 µs vs 307 µs walk (42–2378× per channel); walk degrades to 6.7×10⁻⁷ at m→1 where the kernel holds 10⁻¹⁰; first run's DE weight bug found and fixed.
- 20261014-1221-system-b8fc (this run): knot-table census — 8–10% of cells read, 13.4 point-evals re-integrated per readout, read side 66–69% of point-evals; the incomplete-form readout is the one deletion for kick cost, search cost and standing memory.
- 20261014-2130-spacex-cd6e (silver, this run): incomplete Carlson readout derived+verified
