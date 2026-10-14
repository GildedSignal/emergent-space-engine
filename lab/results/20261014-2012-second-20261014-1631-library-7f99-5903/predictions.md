# Predictions — second author on 20261014-1631-library-7f99 (run 5903)

Written 20:2x, before any build or run of this session. The checker's named experiment:
delete the doll-wide `speed_cap` sensor and the all-dolls density rule (library lesson 3),
rerun a2c1's 10³ arm; the sticky-promotion half (lesson 4, the chatter case) is assessed
for reachability separately below.

## The design under test (fixed before the runs)

- Registration widens each body's bins by **its own** speed bound `v_j · H`
  (`range_of`'s third component), not by any doll-wide cap; `H` is one documented
  constant, the scan horizon (overridable by `ES_SCAN_H` for controls), default
  `2.0e12` doll-time units — above the largest interval the ladder's scenes ask
  (a2c1's coast census: `h = 1.100e12` at every scan; burn is finer).
- `candidates()` drops `speed_cap` from the window (`reach = (near + v_player·h)·1.01`),
  drops the density rule entirely, and keeps exactness by construction: any scan with
  `h > H` returns `None` (the caller walks every body, as before the index — exact).
- The walk-all fallback in `encounter.rs` stays (it is the exact degenerate path for
  `nodoll`, `width`, and now `h > H`).

## Predictions

- **P1 (the 10³ arm, the named ~60×).** `nladder 1000 coast 20`: `why=density` fires
  0/193 times (it is deleted); walked/call falls from a2c1's 1,017 to **≤ 60**
  (the certificate's keep set ~17 plus the hull-of-history widening that a2c1 measured
  growing over the flight, plus the unbounded list ~23). I expect kept/call ≈ 15–40.
  The walked cut on that call is ≥ 17×; if it lands ≤ 25 the "~60×" headline holds
  nearly clean.
- **P2 (the 10⁴–10⁶ domain).** `nladder 100000 coast 20`: walked/call falls from 194
  to **≤ 40** (keep ~17 + unb ~23; the belt never enters the player's doll, so the
  window's population does not grow with N).
- **P3 (the certificate control — the prediction that can fail).** The universe digest
  (printed by my probe after `settle` at the flight's end) is **identical** between the
  shipped build and the deletion build on every arm. A differing digest means the
  sensors were load-bearing after all (a missed encounter) and the run reports a
  refutation of lesson 3, not a deletion.
- **P4 (the horizon guard control).** With `ES_SCAN_H=1` (h always > H) the patched
  build walks every body (`why=horizon` ≈ all calls, walked ≈ total) and the digest is
  still identical — the guard path is the exact fallback. If the digest instrument were
  insensitive, this control cannot catch that alone; the suite's planted
  `sloppy_reuse` finder (which must give another digest) is the sensitivity control.
- **P5.** The universe test suite is green on the deletion build (no law change).
- **P6 (the chatter half, scoped honestly).** The "shipped chatter case (retrograde
  0.49 R_H)" is **not shipped**: it is the 18d2 checker's probe on the lead-graded
  single-surface branch (`claude/lab-20261006-1738-b-handoff-surface-18d2`, its
  `work/patch.diff`), whose probe code is not preserved in the record. If the window
  allows: rebuild that branch, re-emit the probe (retrograde circular birth 0.49 R_H,
  count handoffs over 20 periods — expect ≈ 210), then gate its surface predicate on
  the refit's refusal and predict **0 handoffs** (the body is representable in both
  dolls at 0.49 R_H, so the refusal filter never fires). If the window does not allow
  it, this file records that the case is one branch-rebuild away, and the dossier says
  so explicitly rather than claiming it.

## Kill criteria

- P3 fails (digest differs) → lesson 3's deletion is refuted as unsafe; report the
  miss, keep the guard design as the diagnosis.
- P1 lands > 200 walked/call → the poison was not the cap; the library's pricing of
  the sensor is wrong in size even if right in sign.
