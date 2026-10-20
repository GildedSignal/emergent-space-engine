# Predictions (v2, written before the decisive long flights)

Run 20261020-0548-fermi-3557. **Amendment, disclosed:** v1 (written 05:5x, before any
decisive flight) specified 45 s arms. The first attempt at those arms (05:57, logged in
`work/logs/decisive.log` alongside the 10 s coast calibration) revealed an instrument flaw,
not a result: `frame_to` advances game time per call without sleeping, so a "45 s" coast arm
presents only ~4.4k game-s and ends before the belt's first clock wave (f80a: saturation at
gs 11k–16k) — the counters were byte-identical at 1e4 and 3e4 (7,593 kicks both), i.e. pure
player-doll stream. The flights are extended to 240 s nominal (14,400 frames ≈ 24k game-s,
guard raised to 150 s wall) so the window contains the belt's waves. The prediction bands
below are v1's, unchanged, written before any long flight.

Decisive arms: coast 1e4, burn 1e4, coast 3e4, burn 3e4; 240 s nominal, rtf 100, budget
12 ms, seed 1, threads 1.

The question (budget-1e9 open direction 6): is the mint's per-kick byte traffic MARGINAL
(charged to the fired item's own scope) or BASE (frame-owned)? f623's window-OLS could not
decide (slopes −1.1 to +5.3 KB/kick). Direct counters decide it here.

- **P1 (anchor to f623).** With the belt's waves in the window, naive per-kick bytes rise
  toward f623's constants (12.3–12.7 KB/kick coast, 21.5 burn; band: within 3× either way),
  and burn naive exceeds coast naive (1.2–2.5×).
- **P2 (the decision).** item_share > 0.5 in every arm including burn: most allocated bytes
  are charged to the resolving item itself (nested wave kicks included — ITEM_SCOPE stays 1
  through them), so the marginal reading is real and direct attribution replaces the OLS.
- **P3 (the scratch split).** The >2 KiB scratch bytes are majority BASE-scoped on coast
  (prune, scan drains, frame bookkeeping), but the burn's EXTRA naive bytes are majority
  item-scoped (the fired item's own scratch).
- **P4 (the base row).** Base bytes stay < 15 KB/game-s at 1e4 coast and grow sub-linearly
  to 3e4 (< 4×); composed at 10⁹, rtf 100, base traffic < 10 GB/s — the item-scoped row
  dominates the ledger's byte-traffic term.

**Kill criteria.** If item_share < 0.3 in the burn arm, the marginal-kick reading dies: the
wave's bytes are frame-base, pooling the fired item's scratch cannot cut marginal traffic,
and the 10⁹ row must be recomposed on the base law alone. If naive misses P1's band in BOTH
arms, my window is not comparable to f623's and only within-run ratios count.
