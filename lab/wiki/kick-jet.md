topic: kick-jet
status: open
closed-by:
valid-while:
updated: 20261012-1621-q-wiki-kick-jet-9392

# The kick jet: updating a compiled cycle from stored derivatives (law.md line 35)

## Current best

**The jet is retired** (law.md:35, 12 October; HANDOFF: "six golds refute it; it is not wired into the plane"): a kick recompiles its cycle exactly, as the plane does, and the kick's cost is now the frame-cost bottleneck. The six standing gold refutations are 4978, 9a04, a059, b33f, ee08, d617 (law.md:35 cites 4978, b33f, d617; df81, the run the law originally adopted, had one checker — 4978). The refutation, in one pass: the multiply-add's error is C·drift² with no bound (df81: the 10⁻⁶ floor crossed after ~730 correlated 10⁻⁶ kicks); it diverges at the Schwarzschild separatrix on the L axis (4978: one 10⁻³-of-L kick errs 10³–10⁹× the floor, and a plunge is fabricated as a bound cycle) and on the E axis (9a04: relerr(T_t) ≈ (15/8)·(δE/(1−E))², 1.2×10⁸ stiffer than the matched dL kick; 2040), at every Kerr spin prograde and retrograde (ee08, 6164); law.md:35's own re-anchor policy cannot hold navigation (≤10⁻³ rad) and cost (≤700 crossing-evals/orbit) simultaneously inside s = (p−6−2e)/p ≲ 0.05–0.1 (a059, 075b); the near-plunge band μ = p−p_crit(e) ≤ 0.3 fails both frozen budgets with a one-signed drift while 30–40% of deep captures feed it and residents linger ~4×10⁴ kicks unseen by the shipped trigger (d617, 4808); and wired into shipped code the speed-up cancels the physics — 2.75× on the plane's kick median but B13 assists 60/64 → 41/64 and the lifecycle invariant 12× off (b33f), |Δa|/a median 1.5×10⁻³ on the belt with error ∝ threshold and compiles ∝ 1/threshold, so no threshold reaches the 10⁻⁶ floor (b18f). The recompile horizon is not the law's constant either: it scales (1−e²)^(2/3)·δ^(−2/3) — 25 kicks at e = 0.99 against 342 at e = 0.5 (7922, e86c).

**The exact replacement, priced on shipped code.** The rebind (fit → compile → readout) is 84.6% of a plane kick's wall (96b4, correcting ea6b's wrong-path table), the compile alone 49–62% on fleet leavers (1e74); the rebind runs ~270× above a two-integer floor, and the compile's uncounted interior (allocations, key search, ~182 i128 panels), not its ~2,300 counted Scalar ops (~3–5 µs), owns most of the ~25–27 µs (fa08, 30e1); the fired kick's generator update runs 9–16× above its floor (f797). Any carry's honest ceiling is 1.5× (made/player kicks) to 3.0–3.8× (leavers) against a ~26 µs fictitious-clock machinery floor that owns the rest (1e74; eea5: ~1.6× median, ~10× p99; 492f: 3×; 0ccd: 1.7–2.7×; 8c81: ~2.7×). The quantized (E, L) memo hits 92.5–95.1% at 0.55 µs against a 37–55 µs compile (~70×) but re-rounds the orbit at every kick — a random walk, **not adopted** (6c47; law.md:35). At 10⁹ bodies, measured crossing-state readouts (0.34–0.42 µs) and re-anchor rates ρ = 0.001–0.002/rebind close rtf 100 with ~2× margin on the exact path (c4ce, refuting e3bc's "jet 1.6× short" favorably — memory-h-live topic).

**Domain.** Tested: plane seeds 1–7 at rtf 30–1000, fleets to 200 members; the hlive belt (Jupiter 2⁻¹⁰, Saturn 2⁻¹², 24 game-years); Schwarzschild and equatorial Kerr χ ∈ {−0.9, 0.5, 0.9, 0.998}; e ≤ 0.99. Not tested: inclined Kerr, resonant kick trains against a carry, the dense order, and behaviour gates on any derivative-carrying build (see Contradictions). Inspiral is not a jet: Peters' a(t) is its generator (law.md:35; df81; the Peters flux drifting the tube's (E, L) is adoptable with measured contracts — 4c5b, silver, gravity-news topic).

## Refuted

- "A kick updates the cycle by a multiply-add" (representation.md §3) as a general law: error C·drift², floor crossed after ~730 correlated kicks (df81; 075b).
- The jet near the Schwarzschild separatrix, L axis: 10³–10⁹× the floor; plunge mispredicted as a bound cycle (4978; 2040).
- The jet on the E axis and both edges of the bound band: (15/8)(δE/(1−E))²; E ≥ 1 escapes and plunges misclassified by the shipped predicate (9a04).
- law.md:35's re-anchor policy in the strong-field skin s ≲ 0.05–0.1: saturation at 30–33 anchors/orbit (2.6–6.6× the whole fixed-step budget) or navigation lost (a059).
- The jet at every Kerr spin, prograde and retrograde: the same logarithmic separatrix divergence; the T-channel dominates the belt grid (ee08; 6164).
- The near-plunge band μ ≤ 0.3: one-signed drift 1.5×10⁻²–6.9×10⁻² rad per 10³ kicks; the band is fed and residents linger unseen (d617; 4808).
- The wired jet on the plane: speed real (2.75–2.79×), physics cancelled — B13 41/64, lifecycle invariant 12× off, because the Entry carries no (E,L) sensitivities (b33f; 0ccd's 1.7–2.7× prize).
- The derivative-free offset carry on the belt: |Δa|/a median 1.5×10⁻³ at the law's own threshold; error ∝ threshold, compiles ∝ 1/threshold (b18f).
- "≈0.05 compiles/kick" as a constant: the horizon scales (1−e²)^(2/3)·δ^(−2/3) (7922; e86c).
- The quantized (E, L) memo as a pure speedup: 92.5–95.1% hits but it re-rounds every kick, a random walk; a law change only (6c47; law.md:35).
- The jet's readout on high-e bodies: err 1.5 and 156 relative at e 0.9/0.99, where the plane's kicked bodies sit at median e = 0.94 (8ce2).
- Deferring a kick's application under a renewal quantum: energy walks linearly, exponent 1.01 (67f2 — kick-cadence topic).

## Open directions

1. **Cheapen the exact recompile** — the retired jet's replacement and the board's live question. Attack the compile's uncounted interior (allocations, key search, i128 panels) and the word-transition double-compile (f797's headroom scan: bind drops to 0.99× from_state at a word 2³ coarser), not arithmetic (~3–5 µs of ~25–27) (fa08, 30e1, f797); a crossing-read tier already reads at 0.34–0.42 µs (8c81, c4ce). Would change: the path 100% of kicks pay, where any carry tops out at 1.3–3.8× (1e74).
2. **The fate predicate at a kick.** 9a04's tri-predicate (bound ⇔ E < 1 ∧ three real roots ∧ middle root > 2M; escape ⇔ E ≥ 1 ∧ three real roots; plunge otherwise) is complete and freeze-ready for b-plunge-tubes; ee08 folds both failure families into one root-distance rule in u-space on roots darwin16 already factors, and d617 prices the domain guard (μ ≥ 0.3 plus a drift counter, ≈0.01 compiles/kick, residents only). Would change: deletes the plane's NoBoundOrbit refusals (4978) and guards the exact path's fate flips.
3. **Inspiral by Peters' generator, not kicks** (law.md:35; 4c5b: handoff = separatrix, re-key wall, 1PN flux contract measured; its circ_L √a artifact was corrected by the checker). Would change: deletes the GW channel's per-kick work.
4. **If a carry is ever reopened:** it must carry the (E,L) sensitivities (b33f) and the period derivatives ∂Δt/∂E, ∂Δt/∂L per band (fa08: without them it dies at kick 1–4), trigger on offset × window age, not offset alone (b242, ungraded), and face B12/B13/B17 and the lifecycle pin on the same build that holds drift (b33f; 2c68).

## Contradictions
- **Drift floor versus behaviour gates on the same mechanism.** A frozen-tube carry holds 10⁻⁶ for a median 34–790 kicks on real plane bodies (2c68, silver; its evidence rows were mislabeled but the predictions held on the intended bodies), while the wired carry fails B13 and the lifecycle invariant (b33f, gold). The ungraded second author (b242, no check.md) sides with b33f: 2c68's "bounded by construction" was a shadow-reset artifact — a rebind anchors to the carried state, not the truth, so the error compounds across rebinds (3.1×10⁻⁴ at 3000 kicks on held-out seeds). Unresolved only in grade: b242 has no checker; one behave-suite run on a derivative-carrying build decides it.
- **The belt-domain derivative jet.** 8306 (gold first check, silver second; standing silver) holds 10⁻⁶ at 0.0065 compiles/kick with per-anchor C at belt sizes; b18f refuted only the derivative-free carry, and no run has faced a derivative-carrying build against the behaviour gates. Unconfirmed, not refuted; the retirement sets the default to exact recompile either way.
- **The design doc lags the law.** representation.md line 67 still states "a cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add"; law.md:35 retired the jet on 12 October. The wiki records it; fixing the doc is the integrator's.

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
