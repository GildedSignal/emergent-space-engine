# Check 2 — 20261018-1433-redteam-915d (independent checker, blind to check.md)

Grade: gold

## Abstract

Claim: the additive heading accumulator (`thrust.rs` `owed`, representation.md thesis 3 + L50) cannot
store the non-abelian part of SO(2,1): a constant-γ turn through ψ rotates the true frame by exactly
(γ−1)·ψ, and the miss corrupts sky, nose and trajectory. Reproduced bit-exact (`regen.sh`, only
`timing_s` differs). Independently confirmed: my expm-free Fermi–Walker RK4 gives (γ−1)ψ exactly
(γ 2, 1.25); the author's instrument, run by me beyond its certified range, holds to γ 70.7
(γ 63, ψ 90°: −5580.02° vs 5580.00°); two-boost Wigner matches both closed forms to 1e-15 on
unequal pairs; my literal translation of the Rust `burn`/`owed` reproduces the flights exactly
(off135 γ 2: nose 55.776°, 0.2748 c, 22.25% of path), invariant over 16× flush refinement — structural.
Gain: kills a premise of bottleneck 0; adoption = the doc's own §1 split-quaternion attitude plus a
named rung bar. Cost: 4 numbers per thrusting body, one multiply per flush (argued, not measured).

## Reasons

1. **Reproduction.** `regen.sh` rerun: results.json identical to the runner's except `timing_s`
   (8.29 vs 8.33 s). Every dossier number checked against the JSON: closed form 42.8961988683°,
   contamination 9.8e-15, collinear sky 0.0 / β err 1.4e-14, pure turn −1.8e-13°, sweep grid to
   (γ−1)ψ within 0.005°, off45/off135/reversal flights as quoted.

2. **Predictions.** `predictions.md` (30 m) predates `falsifier.py` (14 m) and `results.json`; P1–P8
   verified against the JSON, 9/10 held. P6 missed and is reported as missed, with the correct
   diagnosis (the off45 burn nearly doubles γ — final γ 4.53 — instead of turning the velocity; the
   >30° skies belong to real turns). Honest miss, correctly attributed.

3. **Independent physics confirmation (three methods, none sharing the author's harness).**
   - Fermi–Walker ODE on SO(2,1), RK4, correct ηBᵀη inverse, no matrix series: β 0.866/ψ 180° →
     180.000°; β 0.6/ψ 360° → 90.000° — exactly (γ−1)ψ. (My first two attempts disagreed; both were
     my own bugs — a wrong "inverse" valid only for symmetric matrices, and a pure-lab-boost chain.
     The latter is instructive: it converges cleanly to exactly (1−1/γ)ψ, deriving where the
     refuted competitor comes from — composing pure lab boosts silently de-rotates the frame.)
   - The author's verbatim `prescribed_turn`, run by me past its certified domain: γ 22.37
     (−3845.93° vs 3845.93°, rel 4e-6 at N 128k), γ 63 (−5580.02° vs 5580.00°), γ 70.71
     (−6273.76° vs 6274.12°). The law holds across the record's pump speeds.
   - Two perpendicular boosts: exact products of closed-form matrices match both candidate formulas
     (2·atan(tanhφ/2·tanhψ/2) ≡ atan2(sinhφ sinhψ, coshφ+coshψ)) to 1e-15 on unequal pairs
     (0.5/0.99, 0.3/0.8, 0.999/0.6) — the closed form is not overfit to φ=ψ; order swap flips the
     sign exactly.

4. **No strawman.** My own literal translation of `thrust.rs`'s `burn` (flat limit f=1) + `owed`'s
   accumulator reproduces the author's shipped-model numbers to all printed digits, and the
   divergence from the exact model is invariant over N = 10k→160k flushes — the accumulator's best
   case (fine flushing), so the measured error is structural, not flush granularity. Shipped
   grounding verified in the tree: `view.rs` L54/L293 (heading from `owed`) and L309
   (velocity-only aberration), `lorentz.rs` `Frame` = rotation–boost–rotation, `representation.md`
   thesis 3 (L9), L50, L40 verbatim; no Thomas/Wigner term anywhere in `crates/`.

5. **Adversarial beyond the author's range.** γ 10 off135 brake: nose error 119.9°. Unequal-boost
   Wigner pairs. Flush-granularity invariance. γ 63/70.7 turns (above). All consistent with the
   claim; the claim's stated domain (γ ≤ 7.09 certified) is honest and I extend it.

6. **Novelty.** No Thomas/Wigner/attitude entry in `docs/`, `lab/wiki/`, or HISTORY. The record's
   prior nose-lag (high-gamma-clock: 24.6°–163.5° at L0–L5) is turn-tier rate saturation — a
   different mechanism (controller too slow) from this run's structural non-commutativity (no
   additive law can represent it at any rate). e8f7 killed the same disease in doll keys
   (lab/wiki/handoff.md L141) and left the "Wigner axis error… owned by the spatial turn machinery
   if anyone's" (L157) unowned; this run is that owner. §7's ladder (r1–r7) has no attitude rung;
   the proposed bar (a γ ≥ 1.1 turning flight must carry (γ−1)ψ; negative control = the accumulator)
   is freezable as written.

7. **Goal fit.** Kills a premise of bottleneck 0 (the representation), the gold bar's "shows that a
   premise is wrong". Principle 19: "if you find yourself fixing things that's oftentimes a signal
   that it is the wrong representation" — the accumulator is the wrong representation and §1 L40
   already holds the right one. Principle 6: a held burn is a generator ("Store the generator, not
   the generated"). Principle 13/2: a missing group component is an error of type, not size — no
   carry width shrinks it (r2's lesson, cited correctly). Principle 30: "navigation, knowledge and
   dynamics those need to be perfect" and "I want the player to feel what a human would feel in
   space" — the player's own turning flight is the core loop. Determinism is unaffected: the fix is
   a different exact law, not a float oracle.

8. **Page.** The proposed `wiki/representation-premises.md` diff is exactly one NEW block, one
   Refuted entry, one Runs line, `updated:` bumped; every number in it matches the JSON and my
   reproductions; "certified to 0.02°" is conservative (worst grid point 0.005°). No overstatement
   found; no correction needed. The topic stays open (first gold on this premise; not three
   agreeing golds).

## What the author missed

- The cure's cost claims (one quaternion multiply per flush; closed-form flush for held burns) are
  group-theoretically sound (held keys = constant body-frame generator = one-parameter subgroup,
  B(τ) = B₀·exp(Aτ)) but unmeasured; the rung should price the flush and the view's one extra
  rotation per frame on the M1 path.
- The instrument's certification ends at γ 7.09 because N=16000 discretization pumps at high γ
  (1.6% off at γ 63); the frozen bar must pin N per γ (or use the certified closed form as the
  reference) above γ ≈ 10.
- The refuted (1−1/γ)ψ form's provenance (pure-lab-boost chains de-rotate the frame) deserves a
  line on the page: anyone "simplifying" the instrument that way silently reintroduces the wrong
  competitor — my own first attempt did exactly this.
- The shipped binary was never flown (disclosed); my code reading closes the wiring question for
  the letter of the law, but one off-axis burn on the tree would close it for the build.
- The field half (geodetic/Fermi precession in curved dolls) is named open but untouched; the
  flat-frame structural term is the one this run certifies, correctly.
