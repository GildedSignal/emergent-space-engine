# Predictions — 20261010-1706-second (held-out cases, written before the behaviour run)

Tuned on: the first run's own seed (0x5EED_97CE_0000_0001, Jupiter, step_log2 7 and 4) — its
numbers are the record, not held out: reference reproduces the author bit-for-bit (406,220
events, 203,017 kicks, 1.0000 rekeys/kick); anchored gives compiles/kick 0.0160, wall 9.8→5.6 s.

Held out (never run before this file): seeds 2–6 (Jupiter), seeds 2–4 (Saturn 2⁻¹² at 9.58 AU),
the co-orbital scene under the re-anchor, determinism, and every behaviour deviation below.

1. **Compiles/kick at the engine's cadence (2⁷), Jupiter seeds 2–6: 0.010–0.030 each** (≤ the
   design's 0.05). Saturn (≈8× weaker tide): 0.002–0.020. The tuned seed gave 0.0160.
2. **Wall ratio anchored/reference: 1.5–1.9×** on every case (the checker's attribution: bind ≈
   43.7% of wall; this box is shared, so the ratio, not the absolute, is the number).
3. **Per-ship position deviation vs the reference law, |Δx|/r: median 1e-6–1e-4, max 1e-3–1e-2.**
   My reasoning, against the naive reading: law.md's error = C·drift² was measured for the *jet*
   (cycle increments updated by stored derivatives). This engine's offset-carry has **no
   derivatives**: between compiles the position follows the anchor orbit plus a constant, so the
   position error grows *first-order in time within each window* (∫carried dt), ~½·7.3e-4·v·τ_c
   with τ_c ≈ 63 kicks ≈ 0.65 ship-orbit ⇒ up to ~1e-3·r per window. If the measurement comes in
   below 1e-6 instead, the offset-carry is better than this analysis and the claim stands outright.
4. **Elements stay with the reference: |Δa|/a median < 1e-6, max < 1e-3; |Δe| max < 1e-2**
   (oscillatory tides are adiabatic for a; e ≈ 0.1). Behaviour is judged on distributions and
   elements (principle 20, the B-judges' statistics), not per-ship phase identity.
5. **No alive-difference on any case; anchored reruns of one seed are bit-identical** (integer
   threshold, integer arithmetic throughout).
6. **Co-orbital (strong field): max |Δx|/r 1e-3–1e-1, |Δa|/a up to 1e-2.** The tuned control
   already showed 11 compiles over 408 kicks (97% deferred): the law's √(floor/C) does *not*
   fall back per-kick near a planet; it recompiles on accumulated correlated drift. If |Δa|/a
   exceeds 1e-2 there, the strong field needs its own rule before adoption (the first run's
   lens said as much; this measures it).
7. **Cadence row (tuned seed, 2⁴): compiles/kick 0.09–0.13, above the 0.05 target** — already
   measured at 0.109: the re-anchor's cost follows accumulated drift per game-time (2,859
   compiles at 2⁴ vs 3,204 at 2⁷ for the same horizon), so a per-kick target is cadence-dependent
   by construction. Predicted to replicate on every seed.

## Kill criteria (pre-registered)

Gold needs, on the held-out set at the engine's own cadence: compiles/kick ≤ 0.05; wall ≥ 1.5×;
|Δa|/a max < 1e-3 and |Δe| max < 1e-2 on every belt seed; alive-diff 0; determinism bit-identical.
If |Δa|/a max ≥ 1e-3, or any ship dies differently, or determinism breaks, the wired re-anchor is
a law change rather than a memo (the 5 October precedent on the quantized cell), and the honest
report is a refutation of "adopt within one step" at this threshold.
