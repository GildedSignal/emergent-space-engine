# Predictions (written before the decisive runs)

Topic: nladder, open direction 4 — the passage/plunge tail (the seam's never-demote rule).

Notation: `w = log2(outer_radius / periapsis)` is a passage's window exponent. The tail
exists only when the compile's endpoint `x = periapsis/outer < 2^-10` (orbit.rs join),
then each panel shrinks x by 15/16.

- P1 (law curve): tail panels = 0 for w ≤ 10; above, ≈ 10.7 panels per octave of (w − 10),
  within ±1 panel of `ceil(ln(2^-(w-10))/ln(16/15))`. Held-out check at w = 13, 21, 29.
- P2 (the shipped constant): a no-tail passage stands at the knots + crossings only,
  ≈ a belt cycle's ~670 B; the shipped accounting constant 4096 B (body.rs:193)
  over-prices every in-plane passage ~6×.
- P3 (the certificate): re-mint identity. `Passage::compile(key, outer_radius)` is pure in
  its two arguments: compiling twice and reading `at_radius`/state at ≥ 50 sample radii
  across the window is bit-identical, 0 differing limbs, 0 refusals, at every w tested.
  If ANY bit differs, the never-demote rule is load-bearing and this run reports that.
- P4 (the plane's own mints): in the standard ladder flights (coast and burn, 10^3–10^4),
  every passage the plane mints has w ≤ 11 (doll edges are 2×SOI, periapses bounded below
  by surfaces; the root doll binds at the current radius): tails empty, standing ≈ knots.
- P5 (the edge case, the falsifier that matters at 10^9): a body unbound about the star,
  bound by the engine at r/periapsis = 2^16, compiles a passage with ~64 ± 6 panels and
  stands at 3–7 kB (panel = (Scalar, Integral)), 5–10× a belt body, and nothing in the
  shipped engine (nor the seam, which never demotes passages) ever deletes it.
- P6 (the rule's true domain): `Trajectory::key()` is `Some` for Cycle and Passage,
  `None` for Plunge — so the seam's demotion needs only the key + outer_radius for
  passages (56 B + 16 B + sense/unit ≈ the cycle's compact record), and never-demote is
  necessary for plunges alone (no key to re-mint from).

Kill criteria: P3 failing kills "demotion extends to passages" and this becomes a
refutation dossier. P1 off by > ±1 panel/octave means I misread the shrink loop;
diagnose before using the curve. A control that cannot pass (identity at w ≤ 10, where
compile must return Topology for outer ≤ periapsis) breaks the instrument, not the law.
