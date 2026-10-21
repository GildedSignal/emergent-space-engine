# Predictions (written before the decisive run)

Instrument: the shipped `jacobi` example's own scene (star + Jupiter 2⁻¹⁰ at sep 5.27×10⁸),
copied verbatim into `beltcad.rs` with one added axis — the ship radius class — plus an
osculating-e drift tracker. Steps are the example's own dial: 2^step_log2 kicks per planet
period. Bar: B12's frozen 1e-4 Jacobi bar (the law's own instrument bar; not invented here).
Arms are equal-horizon: 100 planet periods, 6 ships, default (ramped) readout.

## Held-out cases (not tuned on)

- **P1 — the instrument still bites (positive control).** The strong class (1.5–3 Hill,
  7076's judged class) reproduces 7076's ladder within ~2×: worst Jacobi ≈ 5.1e-6 at step 6,
  ≈ 1.8e-5 at step 5, ≈ 3.2e-4 at step 4 (16/orbit), and a super-quadratic collapse at step 3
  (8/orbit) — error ≫ 1e-4, ships' e-pump visible.
- **P2 — the belt class starts far below the bar.** Interior circles at 2–3 AU (6–9 Hill from
  the planet; the plane's own belt draw, scenario.rs) at the shipped-fine step 7: worst Jacobi
  ≤ 1e-6 — at least ~30× below the strong class's same-step error (tide ∝ d⁻³, d 2–4× larger).
- **P3 — the ladder is n⁻² in the belt class too.** Each octave coarser multiplies the belt's
  worst error by ~4, down to step ~2–3.
- **P4 — the floor, and the cliff.** The belt's legal floor against 1e-4 sits at ≤ step 2
  (≤ 4 kicks per planet period ≈ ≤ 1.5 kicks per belt-orbit): at least 3 octaves (8×) coarser
  than the strong class's 16/orbit. Below it, conjunction aliasing (the tidal pulse sampled at
  h ≥ its width) breaks the ladder super-quadratically; if no cliff appears by step −1, the
  tide never binds the belt's cadence and the floor's owner is elsewhere (word scale,
  alignment, boundary) — that would be reported as such, not as an unbounded certificate.
- **P5 — no regime leak.** Belt ships log zero planet-doll captures (they stay on the root
  doll's clock: this is the belt's own stream, not the Hill regime's), zero lost, zero
  refusals at every passing octave.

## Kill criteria

- P1 failing (>2× off or no collapse at step 3) ⇒ the instrument or my copy is wrong: VOID,
  no claim.
- P2 failing (belt ≈ strong class at step 7) ⇒ the belt's coupling is NOT weaker in this
  instrument: the "floor can only be deeper" premise dies in the measured direction.
- P4's cliff absent by step −1 ⇒ report the floor as unowned by the tide; do not quote a
  cadence cut from it.
