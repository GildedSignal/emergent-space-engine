# Predictions — 20261008-1757-system-72ef

Written before the decisive run (μ = 9.5459e-4, N = 10 000, 4 500 kicks).
Tuned on nothing: only the μ = 0 control has run (it returns exactly zero
entropy and machine-precision scars, 20261008).

Scene: belt 2.1–3.3 AU (includes the 2:1 Jupiter resonance at a = 3.28 AU),
Rayleigh e (σ = 0.05), uniform angles, Jupiter at 5.2 AU, e_J = 0.048,
150 kicks per Jupiter orbit, ~187 yr horizon, quantum q = 1e-6 per channel.

1. **No channel grows linearly in bits.** Every angle scar is bounded mod 2π by
   construction; the only magnitude-walking channel is `da_rel` (and slowly,
   |e|). Prediction: total raw scar entropy ≤ 60 bits/body at the horizon, and
   its slope against log₂(#kicks) ≤ 1 bit per octave. If instead H_total grows
   linearly in #kicks (a constant ≥ ~1 bit/body/belt-orbit rate), the
   outside-review premise ("distinctions per game-second decide whether 1e9
   fit") is confirmed and this dossier's claim dies.
2. **Rate decays.** Bits per body per belt orbit, measured at the last octave,
   are ≤ 1/10 of the same rate over the first octave. The H_live rate → 0.
3. **Resonance is visible but bounded.** Bodies with |a − 3.28|/3.28 < 1%
   carry the largest `da_rel`/`dh` scars; their angle scars still saturate
   below log₂(2π/q) ≈ 22.6 bits.
4. **One rate per body is most of the secular structure.** A program that
   carries per-body linear rates of ϖ and λ (fitted on the first 30% of the
   horizon) plus the implied rotation of (h, k) cuts total entropy ≥ 3× at the
   horizon, because secular precession is a rotation and a rotation is
   bounded, not accumulated.
5. **Against the naive store** (a 32-bit delta per channel per kick, or the
   157-bit state per body): the scar store is ≥ 10³ cheaper in bits after the
   horizon, at the same information (exact regeneration of every body's state).

Kill criteria for the instrument itself: control nonzero (checked: it is zero);
entropy not computable; runtime > 60 s.
