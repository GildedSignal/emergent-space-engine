# Dossier — 20261010-1029-redteam-435b (lens: premise red-team)

**Claim.** The design's view contract — "each visible tube crosses the observer's past light cone once; Newton's method finds the crossing, starting from the previous frame's; lensing adds crossings, from each doll's memoized deflection(b)" (representation.md §2, law.md "Observation") — is false exactly where the game's showcase lives: near a compact mass, the single-deflection gather is blind over a ~41°-radius patch behind any black hole the player flies past (truth: two bright images, never absent), and where it does see, its image directions are wrong by up to 26° at 100 M standoff; **no rung and no gate judges the gather** (r6 was never frozen; B3/B16 judge the *forward* bend of one ray).

## Bottleneck

Target 5 of the lens (the view at the past light cone). The view is the product: P30 "what really matters is navigation, knowledge and dynamics those need to be perfect"; P28 "the view is an instrument"; P5 "the zoom level is the minimap" — the same gather feeds the map. Expected gain of the attack: it blocks adopting an observation contract that cannot be salvaged by tuning, and names the missing rung (r6) before anything is built. Not a 10× engine bottleneck: a correctness hole on the game's central instrument, at zero compute cost to fix at the design stage.

## Evidence

Float falsifier, 13.8 s total, < 100 MB: `python3 falsifier.py` (numpy only), writes `falsifier-out.json`. Truth = backward RK4 ray tracing of the exact equatorial null equation u″+u = 3Mu² — the same equation the law compiles (`Passage`, crates/space). "Memo gather" = the design's mechanism, *given the exact per-passage bend* (a tabulated α_d(b) computed by two independent methods that agree to 10⁻⁴ rad and match the b-form series 4M/b + (15π/4)(M/b)²; the crate's exact branch, not a strawman weak one): one bend event on the connecting straight line, |b| < b_c = 3√3 M ⇒ captured ⇒ no crossing. Static observer, static sources, M = 1, 2D plane (the game's plane).

**Controls.**
- **A, flat (must pass): passes.** One crossing per source, look angle equal to flat geometry to 6×10⁻⁶ rad (instrument floor); Newton on the retarded root from the previous frame's guess converges in **1 iteration** for an observer coasting at β up to 0.999 and sources closing at 0.9c. The premise's flat half is sound — this is what `crates/universe/src/view.rs` implements today ("Light is straight in the root frame (no lensing yet)").
- **B, weak field (r_o = 10⁴ M, r_s = 3×10⁴ M, b_line = 749 M): passes on count, misses on composition.** Exactly 1 true image; the one-kink memo lands within **5.2% of the bend** (2×10⁻⁴ rad at this geometry — star-scale lensing is safe in absolute terms). The 5% is the one-pass composition systematic (straight-line b instead of path b); a Newton that iterates *through* the bend closes it. Reported, not fatal.
- **Negative control:** the weak-only memo (4M/b form) fails at least as often as the exact-bend memo in every C scene — the failure is structural (single pass, single root), not bend accuracy.

**The attack (C, sources behind the hole, Δφ ∈ [π−0.6, π]).**

| Scene | memo-blind fraction | true ≥ 2 images | memo direction error (where it sees) |
|---|---|---|---|
| r_o = 10 M, r_s = 20/30/50 M (11 sources each) | **100%** | **100%** (every source, above a 1%-of-brightest magnification cut) | — (nothing found) |
| r_o = 100 M, r_s = 1000 M (7 sources) | 14% (exact alignment only) | 100% | median 2.1°, **max 26.5°**, >1° for 67%, >10° for 17% |
- At r_o = 10 M the missing sky is wide: every source within 41.3° of the anti-hole direction vanishes (the patch is 1.5× the true shadow's width, whose edge sits at 180° ± 27.7°), and every measured image pair sits outside that edge, straddling the anti-hole direction: 136.3°/223.7° at exact alignment — the physics cross-checks. Just outside the blind window the memo starts seeing again with large errors (cf. the r_o = 100 M row at b_line = 1.75 b_c: 26.5°).
- **The blind patch is structural.** Blind ⟺ the connecting line's b < b_c = 3√3 M: closed form for r_o = 10 M, r_s = 30 M gives half-width δ = 0.72 rad = 41.3°, and all 11 measured sources in δ ∈ [0, 0.6] are blind with b_line ≤ 4.24 < 5.196 — the mechanism fails by its own capture cut, not by bend accuracy.
- **Truth is never absent.** Every source in every scene has ≥ 2 crossings above the 1% cut; the full sequence is infinite, demagnified ~e^(−π) per wrap (the finer-grid convergence run finds the 3rd, below cut). So "crosses once" is not repairable by a small fix: the gather needs a count policy (brightness cut) and a branch solver; the design has neither.
- **Standing off does not cure it (C5, predicted ≥2×, measured ~11×).** At r_o = 100 M the >1° mislocation region (half-angle ≈ 29°, the Einstein radius scale) is ~11× wider than the 5.4°-wide blind patch.
- The moving-observer and moving-lens cases were **not** run; B16's forward tests cover the bend side. The structural blind/branch failure is independent of motion.

**Which rung should have caught it: none exists.** representation.md §7 promises "r6 view. Newton iterations and samples per frame for the gather" — `lab/rungs/` contains no r6 (nor r5) file; even as written r6 measures *cost* only, not completeness. B3/B16 judge the forward deflection of a single ray against an oracle; B7 judges clocks; B4 judges capture classification — the inverse problem (which crossings the observer finds) is gated nowhere. **Needed r6 criterion:** in scenes with a compact mass at r_o ∈ [10, 100] M and sources behind it, the gather must find every crossing above a 1%-of-brightest magnification cut with direction within 1% (B3's own tolerance), with the single-deflection memo as the planted negative. Controls on both sides exist already: flat gather (passes) and this memo (fails).

## Predictions

`predictions.md` was written before the decisive run. What happened: A passed as predicted (1 crossing, ≤3 Newton iterations — measured 1); B passed on count, but the memo's composition error is 5.2% of the bend, not the predicted ≤1% (a held miss: one pass is not enough; iterate the bend); C2 confirmed (blind 100% of the swept window; closed-form 41.3° half-width vs the predicted ~27.7°-scale patch — wider than my guess); C3 confirmed at r_o = 100 (67% > 1° vs predicted ≥20%); C4 confirmed (truth continuously ≥2 images, memo gap 1.44 rad wide); C5 confirmed (11× vs predicted ≥2×); C1 partially missed: wrapped images exist but sit *below* the 1% cut (I predicted ≥3 visible within 0.15 rad of alignment).

## What would make it wrong

- My truth tracer could be wrong. Checked three ways: flat control exact to 6 µrad; image pairs symmetric about the anti-hole direction at exact alignment and outside the analytic shadow edge; bend table agrees between two independent integrators and the b-form series. A tracer bug that *adds* images symmetrically outside the shadow edge is implausible.
- The design could mean something stronger by "the memo" than one bend per doll (e.g. a per-wrap branch-indexed memo α_d(b, n) plus a brightness cut). That mechanism is not written anywhere; if that is the intent, this run supplies the numbers to freeze it into r6.
- If players never approach a compact mass within ~100 M the failure is dormant — but B19 (rotating holes) exists because Julien asked for exactly that ("especially rotating black holes"), and at 10 M the blind patch covers 82° of sky. Lensing by stars (scene B) is safe: the everyday sky does not lie.

**Cost of adoption:** none for the engine (nothing is built yet — the live view is flat-space-only); the cost is one rung (r6) frozen before the gather is built, and a design decision in law.md's "Observation" section: crossings are found per branch (n = 0, 1, … with an explicit magnification cut), the memo gains a wrap index, and images are born at caustics with a stated rule (the previous-frame Newton has no predecessor there). The deflection machinery already exists (`Passage::deflection`'s strong branch diverges at b_c); what is missing is the inverse problem's branch structure.

**Fit with PRINCIPLES.** P30: "navigation, knowledge and dynamics those need to be perfect" — knowledge gathered at the light cone is the half of that contract this attack breaks. P34: "the oracles are guards, not shepherds" — B3/B16 shepherd the forward bend while the inverse gather walks unjudged; the gate must guard the player-visible behaviour. P10: "Build the simplest falsifying test first" — a static observer, a static source, one hole, 14 s of float.

**The lens.** A premise red-team overweights exotic corners; I ranked by player visibility, and this one is the tourist attraction (B19's rotating holes), not a corner. What the lens may still have missed inside my targets: the *moving* gather (observer at β → 1 sweeping past a lens: caustic crossings per frame, Newton seeding across aberration swings — B16's moving-lens forward tests do not cover the inverse); and target 4's practical half (dense≡sparse under the Fermi frame with v2) which I judged sound in principle but left unmeasured because r5 does not exist to freeze a probe against.

## Ranked attack list (the lens's deliverable)

1. **The gather near a compact mass (target 5): falsified, numbers above.** Rung: none exists; r6 must be frozen with the completeness criterion. *This is the run's result.*
2. **The gather in flat and weak-field space (targets 2/5): survives.** Unique crossing, Newton converges in 1 iteration at β ≤ 0.999; star-scale lensing single image, memo within 5% of bend (composition, curable by iterating the bend). Rung: B5, B7, and r6's cost criteria as written.
3. **Two-body doll, 1PN EOB (target 1): survives as gated.** r3 v3 and B11 confirm ν enters only through the energy map (1024/1024 precession, 632/632 periods); news gravity equals instantaneous to 10⁻⁷ for free-falling sources (q-gravity-at-c). Open letter, not premise: the "where it is now" extrapolation needs its frame named (root-clock keys, motion-law v2 step 4, in flight). Rung: B11, B12 (exist).
4. **Dense order bit-identical to sparse (target 4): sound in principle, ungated in practice.** The causal-poset argument holds (independent events commute; same-epoch batches have the canonical rule from redteam-6254), but r5 was never frozen and the Fermi frame under v2 is explicitly untested (motion memo §6). Rung that should catch it: B8 must add a relativistic dense scene (P6); r5 must exist.
5. **Kicks and cycle derivatives (target 3): survives in the re-anchored form.** The quantized-(E,L) memo was already killed (df81, gold-graded once, second checker never ran); the jet re-anchors at √(floor/C), ~0.05 compiles/kick. Rung: B12 probes + the re-anchor cadence (covered).
6. **≈0 cost for undisturbed bodies (target 6): survives on orders of magnitude.** Fermi check: 6×10⁴ kicks/game-second over 10⁹ bodies is one secular kick per body per ~4.6 h of game time — consistent with secular + encounter rates from r8/H0190. The open risk is memory (H_live, distinctions per game-second), already the board's top scaling risk with builds queued. Rung: B9/B10 (frozen), B18/B18b (frozen).

Nothing here was adopted or rejected by the integrator; grade as you find it.
