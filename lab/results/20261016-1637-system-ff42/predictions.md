# Predictions (written before the decisive experiment)

Question: is the crash search (`step::next_impact`, 45% of a flying kick per the frame-cost
census) structure-blind? The shipped code already holds the structural inverse
(`Cycle::at_radius` / `Passage::at_radius` in crates/space: knot lookup + one partial
quadrature, exact), wired ONLY as `next_exit`'s passage guess. Prediction: wiring the same
verified-guess pattern into `next_impact` collapses the search for cycles and passages alike.

Cases not tuned on (held out): random crash-course bindings at periapsis radii spanning
0.05–0.95 of the surface, both senses (clockwise/counter), inbound starts at random phases,
dolls with non-unity mass unit (`unity: false`), and e from 0.0 to 0.97.

Predictions:
1. **Tick-exact:** the guess-verified answer equals the shipped bisection's tick on ≥ 99.9%
   of held-out cases (the predicate is the same; failures fall back, so equality should be
   100% by construction — the risk is a compile/units bug, not drift).
2. **Probes:** readouts per call fall from the shipped class floor (~30 ≈ log2 of the 2^30
   half-orbit bracket) to ≤ 3 (two predicate verifications + rare fallbacks), i.e. ≥ 10×
   fewer, ~10-30× cheaper per call in ns.
3. **Fallback rate** (the blind spot — the residual offset the inverse cannot see, worst
   where dr/dt → 0 near periapsis): < 2% on held-out periapsis fractions ≥ 0.1; higher
   (up to ~20%) only for grazing periapsis within ~10^-3 of the surface, where the fall is
   slow and the sub-quantum offset moves the crossing by many ticks.
4. **Digest:** a shipped flight's digest is bit-identical patched vs pristine (the guess is
   verified against the shipped predicate; the fallback is the shipped bisection).
5. If 3 fails badly (> 50% fallback at mid periapsis fractions), the claim dies: the
   searches are then NOT one query and the offset is a real part of the crossing law.

Kill criterion: any digest change, or tick mismatch vs the inline shipped-loop reference on
any case (that is a wrong answer, not a policy difference).
