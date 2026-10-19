# Predictions (written before the decisive flights)

The decisive experiments: (A) the per-reader arm under the far pin — `ES_READER_OLDEST=1` +
`ES_PIN_OLDEST=D`, same binary, same scene (nladder K=3×10⁴ seed 1, coast, 12 ms budget,
rtf 800, ≥ one wave period past the pin, d839 protocol) — against the same binary's global arm
(pin alone, 4a71's dial D = 6×10⁹ and 1.2×10¹⁰ ticks) and its controls; (B) the frozen
`ladder_digest` 13-case suite run with the flag on vs off; (C) a burn arm through the SOI doll
switch (handoffs read centre bodies across dolls, step.rs:795/804) with the flag and pin on.

- **P1 (the deletion flies).** In the per-reader+pin arms, the census stays at the control's:
  retained per body 1.00–1.10 (control band 1.02–1.07) and RSS end 150–160 MB, while the same
  binary's global arm staircases on 4a71's law (≈2.9/body at D=6e9, ≈5.0/body at 1.2e10,
  RSS 279/384 MB). If retained > 1.2/body or RSS > 170 MB in a per-reader+pin arm, the pin
  still holds near bodies through a path the rule missed: the deletion fails.
- **P2 (the pin's frame cost is deleted with it).** Per-reader+pin arms keep the control's frame
  profile: over-12 ms frames ≤ 10, game time within 2% of the control at the same wall cap —
  against the global arm's 383/683 over and −6/−14% game time. The `prunable` walk (the
  O(N)-a-frame term 4a71's checkers measured) shrinks back with the census.
- **P3 (outcome neutrality, counts).** Every arm (pin, reader, both) keeps the deterministic
  content at the control's values: kicks/events per body per game-s equal to the control's at
  equal game time, `stats.refused` 0, held refusals 0, dead 0, player alive, view gather `seen`
  equal to the control's (a scan-side over-prune would drop `seen` or move contacts).
- **P4 (digest neutrality, the soundness gate).** The 13-case `ladder_digest` suite with
  `ES_READER_OLDEST=1` prints digests, kicks, encounters and contacts byte-identical to the same
  suite with the flag off (timings stripped): all four schedules agree in both. One bit that
  moves names a reader outside the rule (the library run's cross-doll falsifier) and refutes the
  proxy's soundness.
- **P5 (doll-edge crossings).** The burn arm with flag+pin: `stats.handoffs` and the player's
  doll sequence (frame, doll) equal to the control burn's, handoff refusals 0 — the centre-body
  reads at step.rs:795/804 never hit pruned history (the rule holds every doll centre by every
  doll's items that can cross it).
- **P6 (the no-pin difference at one star is nil).** Reader without pin: census ≤ the control's
  (the rule can only relax the hold, never tighten it), RSS within ±5 MB of the control,
  same counts. The negative pin (D = 2²⁶, below the natural gap) with the flag on is inert:
  census equal to the control's at matched game time.
- **P7 (the global calendar still sees the far item).** `gap_s` in the per-reader+pin arms reads
  D exactly (59,105.9 s at 1.2×10¹⁰): the far item exists in the universe's calendar; the census
  shows it holds nothing. The instrument and the deletion are measured in the same run.
