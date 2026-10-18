Working...
Check complete. `check.md` written to `lab/results/20261018-1433-redteam-915d/`; nothing else in the run folder touched (the author's wiki page needed no correction — every number in its new block matches `results.json`).

**Grade: gold.**

What I did, and what decided it:

1. **Reproduced**: `python3 falsifier.py` regenerates `results.json` bit-identically (8.4 s, only wall-clock differs). Work tree clean (`patch.diff` 0 bytes, as claimed).
2. **Two independent instruments, written from scratch** (no shared code): RK4 Fermi–Walker transport along the analytic constant-γ circle, and scaling-and-squaring exponentials. Both reproduce the author to the digit — off45 sky −18.04°/nose 12.06°/pos 6.61%, off135 sky −26.18°/nose 55.78°/0.2748 c/22.25% — and the law sky = −(γ−1)·ψ to <0.0001°. My first-pass instruments disagreed; both disagreements were my own bugs (ψ-parametrization, off-manifold RK4), fixed and re-run.
3. **Adversarial beyond the author's domain** (γ 10–62, the record's pump speeds, per high-gamma-clock's "pumped flight to γ 63"): the law holds to γ 62, and the off135 brake's nose error grows to **119.9° at γ 10 and 155.7° at γ 31.6** — the claim is *understated* at the game's daily speeds. Path-reversal control returns the sky to exactly 0.000000°.
4. **Closed the author's disclosed gap** ("a tree run should confirm the wiring"): verified in shipped source — `thrust.rs` `owed` L134–146 is the additive accumulator, `burn` matches the falsifier's replica verbatim in the flat limit, `view.rs` L293/L309/L420 feed that heading into the rendered state, `lorentz.rs` `Frame` is a pure boost, and grep finds no Thomas/Wigner term anywhere in the tree.
5. **Novelty**: e8f7 falsified additive doll-key shears and explicitly deferred the Wigner axis error to "the spatial turn machinery if anyone's" — this run is that owner (different organ, first-order, player-visible, with the closed forms e8f7 lacked). No H entry or page carries it.
6. **One prose error found** (noted in check.md): the dossier's P6 paragraph says the off45 burn turns the velocity "~45° in total"; the author's own trajectory data and my instrument give 10.8°. The miss verdict stands, and the wiki page does not repeat the figure.

Predictions were pre-registered (file times), 9/10 held with the miss honestly reported. Gold under the "shows a premise is wrong" arm: thesis 3 + L50 as the attitude law is dead at the game's own speeds, with controls on both sides and a freezable, behaviour-judged bar.
