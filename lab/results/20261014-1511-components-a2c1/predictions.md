# Predictions (written after the N=10³ coast smoke run, before the decisive 10⁴/10⁵ arms)

The smoke run (N=10³ coast, 20 s) showed: 193 candidate calls, 183 None-by-density,
walked 196,361 total (~1,017 a call = the whole body list, all dolls), kept ~319 a call,
and the per-doll `speed_cap` rising 1.16e-4 → 9.76e-3 over the flight while the
unpoisoned window (early calls) keeps hit=15 + unb=2.

Cases I have NOT tuned on (the decisive arms), and what I expect there:

- **P1 (the None reason).** At N=10⁴ and 10⁵, coast and burn, the density rule
  (`hit + unbounded > bodies/4 + 64`) is the dominant reason a call returns None:
  width and nodoll stays ≈ 0, and ≥ 90% of calls walk the full body list
  (walked/total ≥ 0.9 per call, after the first second).
- **P2 (the certificate's own floor).** The keep set of an *unpoisoned* window
  (the flight's first calls, before any kick raises the caps) is ≤ 64 bodies at
  every N ≤ 10⁵: the player's 8-ish bins stay locally sparse (the belt is bins away).
  So walked/keep ≥ 100× at 10⁴ and ≥ 1,000× at 10⁵ on the critical path.
- **P3 (the poison is a minority).** The `speed_cap` is set by a small minority of
  the doll's registrations (hot-periapsis kicked tubes / leavers), not by the belt's
  bulk: `unb` (unbounded: passages, planets, moons) stays ≤ 30 at these N, and the
  poisoned `hit` (everything in ±9 r bins) is the belt sitting where the widened
  window now reaches, not the belt moving.
- **P4 (burn, held out).** The burn arm's window is wider than the coast's early
  window (the player's own `v` term), but the None share stays density-dominated and
  the walk stays O(total bodies) — the burn does not save the walk by shrinking `h`.

What would make the lever real: if P1+P2 hold, the scan's capture tier runs 10²-10³×
above its certificate's own keep set at ladder scale, all of it on the frame's
critical path (the ladder's 45-50 ns/body × N), and the named mechanism is a
monotone per-doll cap (never lowered by `note`, only raised; `rebuild` also only
raises) plus a full-list fallback walk that ignores doll membership.
