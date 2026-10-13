topic: kick-jet
status: open
closed-by:
valid-while:
updated: 20261013-1428-components-2368

# The kick jet: updating a compiled cycle from stored derivatives (law.md line 36)

## Current best

**The jet is retired** (law.md:36, 12 October; HANDOFF item 4 is now struck through — "done in law.md (not in the shipped code)"): a kick recompiles its cycle exactly, as the plane does, and the kick's cost is now the frame-cost bottleneck. The six standing gold refutations are 4978, 9a04, a059, b33f, ee08, d617 (law.md:36 cites 4978, b33f, d617; df81, the run the law originally adopted, had one checker — 4978). The refutation, in one pass: the multiply-add's error is C·drift² with no bound (df81: the 10⁻⁶ floor crossed after ~730 correlated 10⁻⁶ kicks); it diverges at the Schwarzschild separatrix on the L axis (4978: one 10⁻³-of-L kick errs 10³–10⁹× the floor, and a plunge is fabricated as a bound cycle) and on the E axis (9a04: relerr(T_t) ≈ (15/8)·(δE/(1−…

**The exact replacement, priced on shipped code.** The rebind (fit → compile → readout) is 84.6% of a plane kick's wall (96b4, correcting ea6b's wrong-path table), the compile alone 49–62% on fleet leavers (1e74) — the same shape at the 97 µs era (0083: compile 64.5%, rebind 78.7%, forces 9%) and on the leaver tail (ec9d: Passage::compile is 89–97% of a 365–381 µs leaver rebind); the rebind runs ~270× above a two-integer floor, and 1,400–1,800× above a measured ~42–56 ns information floor (b063, gold; the board files it under frame-cost); the compile's uncounted interior (allocations, key search, ~182 i128 panels), not its ~2,300 counted Scalar ops (~3–5 µs), owns most of the ~25–27 µs (fa08, 30e1); the fired kick's generator update runs 9–16× above its floo…

**The interior is closed by elimination: allocations and key search are dead, the walk's arithmetic owns it (20261013-0236-fermi-061f).** On the cost_split path (ship 14, "made"-class, 32.7–34.2 µs — the wiki's own made band 34–38): a kick makes **9 allocations, 2,872 B** (2×16, 1×64, 1×128, 3×256, 2×512 — the compiled trajectory's tables carry the bytes), priced at 87.5 ns at the measured pair cost of that exact size mix (9.7–9.8 ns) = **0.3% of the kick**; a never-free bump arena moves the kick 0 to −4% (inside the system arm's own run-to-run spread) with the loop hash equal and **settle digests bit-identical** (system twice, bump once — the control repeat is equal, so the identity check is not vacuous). Key search is absent on the bind path by constructio…

**The division half of the interior is now measured — and it is at its hardware floor on x86 (20261013-0350-components-c914).** On the fast_quad operand shapes (dividend < 2^127, divisor ∈ [2^20, 2^62]): the compiler's soft u128/u128 division costs 30.2 ns (i128/i128 35.0; matches 061f's 30.9), the x86 128/64 `divq` instruction itself costs 31.4 ns (**1.04×**, exact), and an exact multiply-only Newton reciprocal (f64 seed, 3 integer iterations, exact ceil-pin, one correction; 0 mismatches on the domain) costs 31.6 ns (**1.05×**) — no cheaper exact division was found among {the soft routine, hardware divq, an exact Newton reciprocal} (checker c914: existence not disproved), and LLVM already emits near-optimal code (it even constant-folds naive measurement loo…

**The kill generalizes off-x86 only as a bound on the c914 prototype, not as a structural kill (20261013-1145-second-20261013-0350-components-c914-00d2).** The c914 kernels, verbatim, cross-built for aarch64 (musl, rust-lld, workspace profile) under QEMU-user TCG on the same operand shapes: the exact Newton reciprocal costs **2.8× the soft routine's TCG wall** (418 vs 147 ns/div, 3 runs each) and **1.49× its executed instructions** (253 vs 169.9/div, singlestep-exec census, difference method, cross-checked by an independent mnemonic census) — and the checker's attacks extend the loss to every divisor decade ([2^20,2^62], [2^62,2^63), [1,2^20), general dividends; the known d=3 failure reproduces on aarch64). **[Checker correction, second check: this run's str…

**The word-transition double compile, measured and deleted (digest-identical).** The shipped `bind` chose the integer word from the *compiled* entry (`word_for(&bound.entry)`), so every word transition compiled a full trajectory, read two exponents off it, threw it away and compiled again: on plane settles (600 s game, seeds 1/3, 48 and 400 members) transitions are 5.1–6.0% of binds but are the expensive binds (leaver-class; 278–310 µs discarded per transition against a ~104 µs mean bind), so the discarded first pass was 14.5–18.2% of all bind time (binds ≈ 43–50% of settle wall at 400 members). The word is a function of the fit's key (plus, for a passage, the compile edge — both known before compiling): `Rebinding::fit_of` (the fit without the compile) + `w…

**The division-primitive lever inside the walk is killed, and the node's arithmetic is a
three-way tie, not a division monopoly (20261013-0350-scout-7d2b).** Census on a 48-key
exact compile sweep: 674 u128 `/` divisions per compile on the `fast_quad` sites (min 89,
max 1,752; with `div_word`'s 26 — the census covers the four `fast_quad` sites and
`div_word` only; `isqrt`'s internal Newton divisions are uncensused, which is the gap to
061f's ~900/kick) and their
divisors **do not repeat** (31,776 distinct of 32,384; fraction 0.019) — they are
functions of the node's ψ — so Möller–Granlund reciprocal division has nothing to
amortize: cold it costs 40.4 ns against the `__udivti3` libcall's 23.6 (and the shipped
Knuth `div_word`'s 27.8; all bit-identical over a 10⁷-case fuzz, max 3 correction
steps); swapping `div_word` for the libcall cannot move the compile — the census bounds
the arm's effect at ~0.1 µs/compile (26 of ~700 divisions; sweep wall 53–74 µs across
invocations on the shared box, noise above any arm effect; 0/48 shape mismatches). Decomposition of the
~320 ns node: **4 divisions 29%, 1 u128 `isqrt` 30%, 1 `cos` 24%, multiplies ~5%** —
no division-only lever can beat ~1.4×; the co-owners are `isqrt` and `cos` (or panel
count, a law change). x86 ranking only; re-measure the primitives on the M1 before
believing the ordering (the no-repetition census is hardware-independent).

**The isqrt primitive, taken to its floor's edge, bit-identically (20261013-1145-components-9384).**
7d2b's named lever, built: the shipped `isqrt(u128)` (u64-Newton seed + 2–3 soft u128/u128
divisions) cost 96.3–98.7 ns on the compile's own operand shapes — ~4–9× above its
arithmetic floor (one correctly-rounded f64 seed + one refinement + ≤3 u64 square
comparisons ≈ 10–25 ns). The replacement (f64 seed + one soft-division Newton step +
exact square fix-ups) is exact by construction (isqrt is a unique integer): 24M fuzz cases
over the real call-site shapes, perfect squares ±1 and the u128 top corner, 0 mismatches;
54.2 ns/op (1.78×); `Orbit::compile` −9.5% on a 65-key grid (58.0→52.5 µs, A/B/A, digest
identical); 70/70 frozen-oracle tests; the plane digest `f5b8cd23…` bit-identical base vs
patched. Kick-level ≈−3–5%; the 1,400–1,800× kick idiot index is untouched (that is panel
 count, a law question). On this grid the measured drop (−9.5%) at the measured primitive ratio
 (1.78×) implies an isqrt compile share of ~22% (checker arms: 22–26%), between c914's 6–14%
 and 7d2b's 30%-of-node.

**The cos primitive, closed by interleaving the panel's four chains — bit-identically (20261013-1428-components-2368).**
7d2b's other named lever, built. The shipped `cos` (thirteen nested floored factors = 26
dependent 64×64 multiply-highs) costs 41.9–44.9 ns and **unrolling alone buys 1.01–1.03×**
(the chain is latency-bound; loop overhead is nil). But a panel's four Gauss nodes are
independent, so `cos4` — the same floored products, four chains step-locked — amortizes
them to **14.07–14.76 ns/cos (2.96–3.07×)**. Wired into all four shipped walks
(`orbit.rs`'s `quad`, `weak_quad`, `fast_quad` and `lib.rs`'s Cycle `quad`; the general
`node` also stops recomputing the same cos through `self.x`): compile on an 85-key grid
**34.44/35.24 → 30.79/30.83 µs (−10.6% to −12.4%, A/B/A)**, knot digest
`b5ef99aabce2f641` unchanged in every arm, plane digest `c83e8285…` identical pristine vs
patched, pure kick resolve 33.2 → 28.3 µs on this box; 71/71 space tests pass and the fuzz
(65,542 dense + 2M random + mixed-lane) is now a crate test. Trap recorded: patching only
the `lib.rs` Cycle `quad` moved nothing (34.44 → 34.35) because the bench grid walks
`orbit.rs` — name the walk you bench. The gain is OoO-silicon-dependent (x86 measured;
the M1's 4-wide issue should transfer — the integrator's re-measure). With 9384's isqrt,
the node's three-way tie is now: divisions at their x86 hardware floor, isqrt closed,
cos closed; what remains in the node is the none-of-these 44–58%, interleaving the
division/isqrt chains themselves (function-call-shaped, untouched), and panel count (a law change).

**Domain.** Tested: plane seeds 1–7 at rtf 30–1000, fleets to 200 members; the hlive belt (Jupiter 2⁻¹⁰, Saturn 2⁻¹², 24 game-years); Schwarzschild and equatorial Kerr χ ∈ {−0.9, 0.5, 0.9, 0.998}; e ≤ 0.99. Not tested: inclined Kerr, resonant kick trains against a carry, the dense order, and behaviour gates on any derivative-carrying build (see Contradictions). Inspiral is not a jet: Peters' a(t) is its generator (law.md:36; df81; the Peters flux drifting the tube's (E, L) is adoptable with measured contracts — 4c5b, silver, gravity-news topic). The allocation census (20261013-0236-fermi-061f) adds: one ship class, one scene, tcache-warm single thread. The division-floor census (20261013-0350-components-c914) adds: x86-64 only at the time (i7-4790-class, shared), compile grids not a settle's kick stream, leaver `Passage::compile` under-sampled; the arm64 floor proxy (20261013-1145-second-...-00d2) extends it off-M1 (QEMU TCG + instruction census, see Current best). The divisor census (20261013-0350-scout-7d2b) adds: the four `fast_quad` sites plus `div_word` only; `isqrt`'s internal Newton divisions uncensused. The cos run (20261013-1428-components-2368) adds: x86-64 only (shared box), one 85-key grid and one plane seed for the digest; the `cost_split` kick arm is single-shot.

## Refuted
- "Exact division-by-multiplication where divisors repeat" as the walk's lever: the hot
  sites' divisors are functions of the node's ψ and do not repeat (0.019 fraction over
  32,384 censused divisions), the cold reciprocal costs 40.4 ns against the libcall's
  23.6, and `div_word`→libcall is bounded at ~0.1 µs/compile by the census (0/48
  mismatches; wall noise above any arm effect) — the lever is dead on x86, killed
  before being built (20261013-0350-scout-7d2b).
  Check2 (160-key grid, p 4–8192 × e 0–0.99): per-key repeat is exactly 0.000 for
  every e>0 key (through e 0.99, 1,968–2,080 divisions/compile); the 0.019
  aggregate lives in the e=0 corner (circular keys repeat 95%, but carry 80
  divisions, 25× cheaper keys). Cross-compile divisor sharing is 0.229 of
  instances (far-field divisors converge to common constants), yet even a free
  global reciprocal cache is bounded at ~4% of the compile (100% sharing caps at
  ~18%) — caching across compiles cannot revive it either.

- "Cheaper exact wide divisions" as a kick lever on arm64 — **refuted for the c914 prototype only** (checker-corrected, second check): the multiply-only Newton reciprocal loses in both proxy axes (2.8× TCG wall, 1.49× executed instructions) and on every divisor decade the checker attacked ([2^20,2^62], [2^62,2^63), [1,2^20), general dividends; the known d=3 failure reproduces). But the aarch64 `__udivti3` executes **~2.8 hardware `udiv` per division** on the fast_quad shapes — not zero (the run's census printed only its top-14 entries; the checker's full histogram and the static disassembly — 8 `udiv` sites — show it) — so the lever's mechanism exists on the target architecture and its fate is the M1 re-measure's to decide, against the 1.49×-instruction expe…
- "The kick's uncounted interior is allocations" (open direction 1's first suspect): 9 allocs/kick, 2,872 B, 0.3% priced; bump A/B within noise; digests bit-identical (20261013-0236-fermi-061f). Fleet-wide ceiling (check2): worst class 14 allocs ≈ 0.3% of its 44 µs. Also dead by the same run: "key search" on the bind path — nothing is searched at bind time (`Catalogue` is slots + free list).
- "A kick updates the cycle by a multiply-add" (representation.md §3) as a general law: error C·drift², floor crossed after ~730 correlated kicks (df81; 075b).
- The jet near the Schwarzschild separatrix, L axis: 10³–10⁹× the floor; plunge mispredicted as bound cycle (4978; 2040).
- The jet on the E axis and both edges of the bound band: (15/8)(δE/(1−E))²; E ≥ 1 escapes and plunges misclassified by the shipped predicate (9a04).
- law.md:36's re-anchor policy in the strong-field skin s ≲ 0.05–0.1: saturation at 30–33 anchors/orbit (2.6–6.6× the whole fixed-step budget) or navigation lost (a059).
- The jet at every Kerr spin, prograde and retrograde: the same logarithmic separatrix divergence; the T-channel dominates the belt grid (ee08; 6164).
- The near-plunge band μ ≤ 0.3: one-signed drift 1.5×10⁻²–6.9×10⁻² rad per 10³ kicks; the band is fed and residents linger unseen (d617; 4808).
- The wired jet on the plane: speed real (2.75–2.79×), physics cancelled — B13 41/64, lifecycle invariant 12× off, because the Entry carries no (E,L) sensitivities (b33f; 0ccd's 1.7–2.7× prize).
- The derivative-free offset carry on the belt: |Δa|/a median 1.5×10⁻³ at the law's own threshold; error ∝ threshold, compiles ∝ 1/threshold (b18f).
- "≈0.05 compiles/kick" as a constant: the horizon scales (1−e²)^(2/3)·δ^(−2/3) (7922; e86c).
- The quantized (E, L) memo as a pure speedup: 92.5–95.1% hits but it re-rounds every kick, a random walk; a law change only (6c47; law.md:36).
- The jet's readout on high-e bodies: err 1.5 and 156 relative at e 0.9/0.99, where the plane's kicked bodies sit at median e = 0.94 (8ce2).
- Sharing one compiled cycle across co-orbital bodies as a ≥40× lever: the shareable compile is 9–17% of a distinct kick, so sharing buys 1.08–1.17× (best tail 6.3×) (4cb2).
- Deferring a kick's application under a renewal quantum: energy walks linearly, exponent 1.01 (67f2 — kick-cadence topic).
- The integer word as a function of the compiled entry (the word-transition double compile): the word is a function of the fit's key (plus the passage edge) and can be chosen before the compile; bit-identical everywhere tested, deletes the discarded pass (009b).
- "Unroll the cos chain to speed the node": 1.01–1.03× measured — the serial cost is the chain's latency, not loop overhead; only interleaving independent chains moves it (20261013-1428-components-2368).

## Open directions

1. **Cheapen the exact recompile — every named primitive is now closed or at its floor; what remains is structure.** The interior: divisions 20–35% of the compile on x86 **at their hardware floor** (divq 1.04×, exact Newton reciprocal 1.05× — no lever there; 20261013-0350-components-c914; the arm64 QEMU/census proxy bounds the c914 prototype off-M1 — Newton 2.8× the wall, 1.49× the instructions — but the aarch64 baseline carries ~2.8 `udiv`/div, so M1 silicon decides the division lever: checker-corrected, 20261013-1145-second-...-00d2), allocations 0.3% and key search absent (061f), `isqrt` closed bit-identically at 54.2 ns / compile −9.5% (20261013-1145-components-9384), `cos` closed bit-identically by 4-way interleaving at 14.1 ns/cos / compile −10.6–12.4% (20261013-1428-components-2368), and 44–58% none of these (products, Scalar normalization, knot accumulation, scaffolding). What remains: fewer panel evaluations per compile (the law's π/4 quantum and band cuts — a law change with recertification, not an optimization), interleaving the four nodes' division/isqrt chains (the same ILP lever cos just proved, now on function-call-shaped code — inline or batch them as `cos4` batches cos), interleaving the four nodes' independent chains if the walk is latency-bound beyond cos, and the integrator's M1 re-measure of the division floor and the interleaved cos (the Newton prototype ships in `div_bench`; the expectation to falsify is 1.49× instructions / ≥1.5× wall — 00d2). The word-transition double-compile half is done (009b: −12.9 to −17.5% of bind time); a crossing-read tier already reads at 0.34–0.42 µs (8c81, c4ce). Digest-identical cuts already measured: fit_only deletes one dead trajectory decode per kick (−10.9%, a48d), a proper_at_event cache plus cartesian-free orbit_state cuts ~9–10% (2833), a weak-hyperbolic quadrature shortcut cuts the leaver ladder 40–45% (c3a5); ec9d's bounded Passage::compile projects ~10× off the leaver tail.
2. **The fate predicate at a kick.** 9a04's tri-predicate (bound ⇔ E < 1 ∧ three real roots ∧ middle root > 2M; escape ⇔ E ≥ 1 ∧ three real roots; plunge otherwise) is complete and freeze-ready for b-plunge-tubes; ee08 folds both failure families into one root-distance rule in u-space on roots darwin16 already factors, and d617 prices the domain guard (μ ≥ 0.3 plus a drift counter, ≈0.01 compiles/kick, residents only). Would change: deletes the plane's NoBoundOrbit refusals (4978) and guards the exact path's fate flips.
3. **Inspiral by Peters' generator, not kicks** (law.md:36; 4c5b: handoff = separatrix, re-key wall, 1PN flux contract measured; its circ_L √a artifact was corrected by the checker). Would change: deletes the GW channel's per-kick work.
4. **If a carry is ever reopened:** it must carry the (E,L) sensitivities (b33f) and the period derivatives ∂Δt/∂E, ∂Δt/∂L per band (fa08: without them it dies at kick 1–4), trigger on offset × window age, not offset alone (b242, ungraded), and face B12/B13/B17 and the lifecycle pin on the same build that holds drift (b33f; 2c68).

## Contradictions
- **Drift floor versus behaviour gates on the same mechanism.** A frozen-tube carry holds 10⁻⁶ for a median 34–790 kicks on real plane bodies (2c68, silver; on the intended bodies its checker measures medians 72/314/705, stable across seeds — the dossier's 34–790 range mixes in mislabeled rows), while the wired carry fails B13 and the lifecycle invariant (b33f, gold). The ungraded second author (b242, no check.md) sides with b33f: 2c68's "bounded by construction" was a shadow-reset artifact — a rebind anchors to the carried state, not the truth, so the error compounds across rebinds (3.1×10⁻⁴ at 3000 kicks on held-out seeds). Unresolved only in grade: b242 has no checker; one behave-suite run on a derivative-carrying build decides it.
- **The belt-domain derivative jet.** 8306 (gold first check, silver second; standing silver) holds 10⁻⁶ at 0.0065 compiles/kick with per-anchor C at belt sizes; b18f refuted only the derivative-free carry, and no run has faced a derivative-carrying build against the behaviour gates. Unconfirmed, not refuted; the retirement sets the default to exact recompile either way.
- **The design doc lags the law.** representation.md line 67 still states "a cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add"; law.md:36 retired the jet on 12 October. The wiki records it; fixing the doc is the integrator's.
- **061f's "~900 i128-division-equivalents own the interior" versus c914's measured split** (divisions 20–35%, and only 42–56% together with cos and isqrt): resolved by measurement, not contradiction — 061f's was a count-based inference; the division count is right, the attribution of the rest of the wall was incomplete (the cos polynomial alone matches or exceeds the divisions depending on method).

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
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e²)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261008-1719-second-20261008-1613-redteam-7922-e86c (silver): horizon 543·(1−e²)^(2/3) on the shipped law; the per-cycle curvature trigger holds everywhere; gold first check, silver second.
- 20261009-0521-second-20261009-0401-quant-ea6b-96b4 (silver): the rebind is 84.6% of kick wall; mean kick ≈79 µs; capacity ≈10⁴ ships/core; gold first check, silver second.
- 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 (gold): sharing one compiled cycle across co-orbital bodies buys 1.08–1.17× (tail 6.3×), not ≥40×: the shareable compile is 9–17%.
- 20261010-1947-autoresearch-2833 (silver): a proper_at_event cache plus cartesian-free orbit_state cuts the pure kick ~9–10%, bit-identical.
- 20261011-1729-system-2c68 (silver): the frozen-tube carry holds 10⁻⁶ for median 72/314/705 kicks on the intended plane bodies (dossier's 34–790 mixes mislabeled rows); cuts the kick 1.5–1.9×.
- 20261011-2235-redteam-6164 (silver): the multiply-add is false outside a corner: 190× the floor at p 100, e 0.9; every kick recompiles at r_apo 2000; gold first check, silver second.
- 20261013-0037-components-009b (silver): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e²)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0236-fermi-061f (silver): the interior closed by elimination — 9 allocs/kick at 0.3%, bump within noise, digests identical; i128 division 30.9 ns; the lever is panel/division count.
- 20261013-0350-components-c914 (silver): the division half measured dead — divq 1.04×, exact Newton reciprocal 1.05×; divisions 20–35% of the compile, all three named ingredients 42–56%; open direction 1 bounded at ~1.4×.
- 20261013-0350-scout-7d2b (silver): reciprocal division killed (repeat fraction 0.019, cold 40.4 > libcall 23.6 ns); division only 29% of the node — isqrt 30%, cos 24%.
- 20261013-1145-components-9384 (silver): bit-identical isqrt (f64 seed + Newton + fix-ups) 96.5→54.2 ns, compile −9.5% A/B/A, digests identical; isqrt lever closed, mul-only reciprocal open.
- 20261013-1145-second-20261013-0350-components-c914-00d2 (silver, second check): the arm64 half of the division floor — Newton loses 2.8× (TCG wall) / 1.49× (instructions) on every decade tested; `__udivti3` executes ~2.8 `udiv`/div (the run's "zero udiv / multiply-only" was a print-cutoff artifact), so the lever stays open on M1 silicon.
- 20261013-1428-components-2368 (this run, awaiting grade): cos closed bit-identically by 4-way interleaving of the panel's Gauss nodes — primitive 42→14.1 ns/cos (3.0×), compile −10.6–12.4% A/B/A, plane digest identical, kick resolve 33.2→28.3 µs; unrolling alone refuted (1.01–1.03×).
