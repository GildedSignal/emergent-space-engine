Working...
**Grade: gold** — written to `lab/results/20261017-0839-fermi-2b89/check2.md`, with five corrections applied to the author's proposed page.

**What I did as the blind second checker:**

1. **Reproduced bit-identically**: applied `work/patch.diff` to the clean tree; both `probe.out` and `compose.out` regenerate byte for byte (~10 s, well under the 60-s bar).

2. **Verified the premise in source, not just the probe**: `AU`/ship-radius/belt parameters (scenario.rs), `word_for` = exponent − 60 (bind.rs:193–205), coarsening-only regrow (bind.rs:231–245), the fire rule and 2⁻¹⁶-of-quantum carry (step.rs:136–146, 424–429). No module of `crates/universe` touches the legacy `space::Key` — the live store binds by `OrbitKey`; the legacy E-key lives only in the galaxy debug view and `shipmem`'s unwired compact store.

3. **Attacked beyond the author's domain**: a census of 15,100 belt bindings (fresh seed 5, N = 10⁴) — all ev ∈ {−73, −72}, zero Passage trajectories, nothing near f0a2's ≈ −48 world; rebind ladders on new body/axis/sign combinations — control stable, mint at 2¹²–2¹³, linear ×2/bit, kick 2³⁵ clears every threshold; hand-recomputed D*, b_flip, flux, conjunction rates, and core counts — all match. All cited cross-run constants (3294, c4d3, a765, efd4, 62f7, fermi-1738) exist in the wiki as cited.

4. **Predictions discipline confirmed**: `predictions.md` predates the probe; outcome A (p 0.8) landed; the one pre-registered failure was caught and disclosed honestly.

**Why gold**: reproduced, held-out predictions held, and it shows a premise is wrong on shipped integer code — the adjudicated "exact tier is empty" reading does not apply to the live path (gate deletes 0% at the measured word), the 0.03–0.6-core routing branch dies at today's width, and only the flux accumulator closes 10⁹ at any width. Adoption is one step: the page plus the named word-width dial decision.

**Page corrections I made in place**: the 2.7×10⁸ fineness slip (its own compose.out says 2.65×10¹¹), 2¹⁰ → 2¹² vs 277d, mint band widened to 2¹¹–2¹³, locals range −77…−74, the "fires and mints" headline scoped to the mint distance, and `shipmem` named as the legacy key's second home. Tree left with only the author's patch applied; my attack example removed; no commits.
