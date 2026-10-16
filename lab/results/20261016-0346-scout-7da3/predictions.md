# Predictions — 20261016-0346-scout-7da3 (written before any flight of this run)

The rung: nladder open direction 1 — fly the staggered first-kick wave **budget-free** on main
(ed3a's `ES_STAGGER` patch applied verbatim, default off = shipped) at 10⁵ and 3×10⁵, far enough
to cover the first **and the second** wave (no published staggered flight has ever passed wave 1;
f82a flew ~22k game-s, wave 1 only). Arms: coast, player at Home, rtf 1000, 60 s of page time
(≈ 60k game-s), engine budget disabled (budget 1e9 ms). Unstaggered arms regenerate the record
(fermi-1a1c) and are the controls.

Arithmetic I can do before flying (no tuning):

- At 10⁵ the unstaggered wave-1 peak frame is 487 events / 22.95 ms budget-free (fermi-1a1c, this
  box class ~47–51 µs/event); at 3×10⁵ it is 1,328 / 71.7 ms. These are my regeneration anchors
  (P4) — if they fail, the instrument is wrong, not the stagger.
- The stagger spreads each belt body's first kick uniformly over one step (2·half, the offset
  range in the patch). 3294's census puts the belt kick interval (the doll grid) at ≈ 28,141.5
  game-s; at rtf 1000 one 1/60-s frame spans ≈ 16.67 game-s. A uniform spread of N first kicks
  over ~28.1k game-s ≈ 1,689 frames gives an expected per-frame mean of N/1,689 (59 at 10⁵) and a
  peak of roughly 1.3–1.6× the mean under Poisson fluctuations — ~75–95 at 10⁵. fermi-1a1c's own
  prediction (≈ 487/16.7 ≈ 29) assumed the spread buys the full 16.7× it measured at genesis on
  the standing train; my uniform-over-one-step arithmetic says ~3× that. Both agree the peak drops
  by ≥ 5×; the difference is which model of the spread width is right. Pass bar set between them.

Pre-registered predictions:

- **P1 (staggered wave-1 peak at 10⁵):** max events/frame < 150 (i.e. ≥ 3.2× under the 487
  unstaggered anchor) and max frame ms < 8 ms (≥ 2.9× under the 22.95 ms anchor). Expected
  60–100 events. If the peak stays ≥ 300 events, the stagger does not spread the wave at rtf-1000
  flight and the rung is VOID (instrument divergence from the record).
- **P2 (N-scaling of the staggered peak):** staggered wave-1 peak at 3×10⁵ within 2.4–3.6× of the
  10⁵ peak (linear-ish in N, exponent 0.8–1.2). Expected ~180–300 events. If it superlines
  (> 4.5×), the staggered wave has its own quadratic term and the staggered-break-N cannot be
  extrapolated linearly.
- **P3 (the second wave — the rung's decisive held-out case, never flown staggered anywhere):**
  the train stays flat past wave 1: peak events/frame in the wave-2 window (first kicks' interval
  after wave 1, ≈ 13–14.5k + ~28k ≈ 41–43k game-s) ≤ 2× the staggered wave-1 peak at the same N.
  **Kill criterion for ES_STAGGER's adoption case:** if the wave-2 peak climbs back to ≥ 50% of
  the *unstaggered* wave-1 anchor (≥ 250 events at 10⁵), the stagger is a one-wave cure (the
  offsets shear/fold back into a spike within one interval) and the 10⁶ staggered-break
  (~1.4×10⁶) and the composed 10⁹ letter (0.5–2.7×) die with it.
- **P4 (regeneration anchors):** unstaggered arms reproduce the record at this box's µs/event:
  10⁵ wave-1 ≈ 487 events (±10%), 3×10⁵ ≈ 1,328 (±10%); µs/event 40–55 on the peak frames.
- **P5 (frame letter, staggered, M1-projected):** with peaks from P1/P2 and the measured
  µs/event, the staggered 12-ms-letter break-N recomputes to ≥ 10⁶ (vs the record's unstaggered
  8.4×10⁴) — i.e. the stagger moves the wave-letters break past the wave-throughput break
  (~1.0×10⁶ unstaggered). If it recomputes below 3×10⁵ the stagger buys less than one decade on
  the letter and its load-bearing sentence weakens.

Held-out for the checker (I will not run them before the dossier closes): seed 3 (never flown
here), and the 10⁴ staggered arm at wave 2 (cheap, different N).
