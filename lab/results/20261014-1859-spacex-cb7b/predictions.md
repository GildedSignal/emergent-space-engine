# Predictions (written before the decisive runs)

The lever: the ladder's belt bodies are all born at tick 0 with one Δs, so their first kicks arrive as
one wave (13.0–14.5 k game-s wide ~1.2 k, 6138) and recur as a standing train (~27.5 k apart, bf21).
The stagger (bf21's "generation choice", unmeasured): at birth only, delay each ship's first clock kick
by a uniform draw over one step (2·half), so arrivals spread over ~2.8×10⁴ game-s. Env-gated
`ES_STAGGER=1`, Kind::Ship only (the player and the planets'-doll bodies untouched), birth only
(constants not yet derived). Nothing else changes.

Cases I have NOT tuned on, and what I expect:

- **P1 (census, belt_first at N=10⁵):** staggered first items span ≈ one step: max−min ≈ 2.6–3.0×10⁴
  game-s against the control's ≈ 1.2×10³; p50 moves to ≈ 26–28 k game-s; min stays ≈ 13 k.
- **P2 (the flight, 10⁵ burn, rtf 100, past the wave ≥ 16 k game-s):** the monster frames shrink with
  the arrival width: worst frame ≤ 40 ms (control on this box class: 315 ms at 10⁵, 6138); the worst
  frame's event count ≤ 3,000 (control 24,467: the pull's batch = wave density × item horizon);
  frames over 12 ms ≤ 150 (control 1,140). If the worst frame stays > 150 ms or the over-count falls
  < 3×, the arrival width is not the lever and the stagger is dead.
- **P3 (the one-shot physics cost, jacobi 7/100/6 and 5/100/6):** the stagger delays one kick per
  body by up to one step with the kick's weight still Δs (a first-interval phase error, one-shot).
  Worst |ΔJ|·r within 3× of the control at the same step_log2. If > 10×, the implementation is wrong
  (the first Δs must scale with the delay, a deeper change).
- **P4 (bits):** refusals 0, dead 0, player alive, in both flights; default runs (no env) bit-identical
  to pristine (env-gated).
- **P5 (held-out seed 7):** the same ratios hold (monster ≥ 8× down, census width ≈ one step).

Falsifier for the whole claim: any of P2's kill thresholds, or the wave re-forming inside the flight
(the stagger must persist: the clock plans each next half from the state its kick leaves, no shared
grid — if the second wave re-coheres inside 40 k game-s the lever buys only the birth transient).

## What happened (after the runs)
- **P1 HELD**: census width 1,491 → 30,109 game-s at 10⁵ (**20.2×**, ≈ one step as predicted; p50 14,072 → 28,122;
  min 13,051 → 13,288; the 300 locals identical to the tick in both arms; N=3,000 reproduces: 1,483 → 29,473).
- **P2 HELD**: max frame 338.1 → 34.4 ms (9.8×); events/frame max 6,712 → 338 (**19.9×**, the census ratio);
  wave-region over-budget frames 5 → **0** (control's wave frames 8,367-8,539 gone; the 31 remaining over-budget
  frames are all the second seam at 11,094+, 1-9 events each, present in both arms); lag equal (1.448 s, dominated
  by frames common to both arms); refusals 0, dead 0, player alive; boundaries 32,368=32,368, handoffs 1=1,
  lost 25=25, opens 433=433, catalogue 100,076=100,076 — every non-belt counter identical.
  Honest notes: kicks inside the window fall 2.3× (133,465 → 58,287) because ~40% of first kicks are deferred past
  the 21 k game-s cut (p50 28.1 k) — deferral, not deletion; and F1 is still red (31 seam frames over 12 ms).
- **P3 PARTIAL**: at step 7 the stagger's worst |ΔJ|·r is 2.7e-5 (the control run panicked mid-flight on a capture
  in this scene, so no paired number); at step 5 the stagger reaches 2.3e-4 against the control's 5.1e-6 on one
  ship (45×) — the literal "within 3×" FAILED. But the absolute errors sit inside the cadence's own error class
  (ad35's rho ≈ 0.5·n^-2.1 gives 3.6e-4 at n=32, 6.7e-5 at n=128), and the arms' trajectories have diverged
  (kicks +3.4%, different encounter histories), so per-ship worst is encounter-sampled, not a clean one-shot error.
  Held on the class bound, missed on the literal ratio; if the class bound is not acceptable, the first Δs must
  scale with the delay (named, unbuilt).
- **P4 HELD**: see P2; default-env runs are unchanged by construction (every change env-gated).
- **P5 NOT RUN** (window): seed 7 remains for the checker.
