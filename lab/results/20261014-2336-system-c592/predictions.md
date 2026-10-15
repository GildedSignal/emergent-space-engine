# Predictions (written before any arm ran)

Question: is the in-band scan ruin (625b/d7e3/c481) the absence of one structure — the doll's
candidate table held once per table-change instead of once per player kick — and does sharing it
delete the ruin without moving one bit?

Scene: `plane_extra` bit for bit except the player is a circular 2.5 AU body of doll 0 (in the belt
band), seed 1, L8 burn at frame 60, rtf 100, 12 ms budget, canonical cut 16,000 game-s, then
`settle(cut)` (625b's protocol). Linux VmRSS/VmHWM from /proc.

The patch: the scan's `candidates: Vec<(usize, Binding, Scalar)>` (a full clone of the doll's
binding table per mint, held until answered) becomes an immutable shared epoch: a base `Arc<Vec<..>>`
plus an overlay of the entries that changed since (copy-on-write, materializing a fresh base when
the overlay passes half the base). Consecutive mints then share the base by `Arc`; a mint's own
standing memory is its delta. Digest identity holds by construction (same values, same ascending
order — the radial ids are ascending and the fallback is `0..N`).

## P1 (certificate): digest identity.
At N = 10^3, in-band burn, the patch leaves the universe digest, kicks, encounters, contacts and
held-max exactly equal to pristine main. Fails → the patch changes semantics → killed.

## P2 (the ruin reproduces here): pristine N = 5×10^4 in-band burn is killed.
The box limit is 2 GB per process. Prediction: RSS climbs monotonically (~0.4-0.7 GB/s during the
burn's re-plan cadence) and the process is killed before the cut, matching d7e3/625b. If pristine
completes under 2 GB, the ruin does not reproduce on this box and the claim shrinks to 10^5.

## P3 (the deletion works): patched N = 5×10^4 completes bounded.
Prediction: completes the cut with VmHWM under ~1.6 GB; held scans still accumulate (~10^3: the
drain still starves — this patch does not touch the drain), but standing per mint is the mint's
delta, not the table.

## P4 (the systems number): the table is the doll's standing state.
Consecutive mints' tables agree on ≥ 99% of entries; the per-mint delta is the belt's rebinds
between mints ≈ N × 3.5×10⁻⁵ /body/game-s × ~84 game-s ≈ 10²-10³ entries at 10⁴-10⁵ — KBs, not
29.4 MB. Measured directly (per-mint delta histogram). If the delta is a constant fraction ≥ 1% of
the table every mint, sharing still pays but the "O(changes)" reading is wrong — report which.

## P5 (adversarial/controls, run by me or the checker):
- In-band coast (no burn): few or no mints (the player never rebinds; reuse or nothing), memory
  flat in both arms.
- Out-of-band (player at Home) N = 10^3 burn: digest identity again (the patch is scene-neutral).
- The wave: during the first kick wave the per-mint delta can spike (many belt rebinds between
  mints); prediction: the flight still completes; if the delta-driven retention during the wave
  alone exceeds the box, that is the named hole of this patch.

## Kill criteria
- Any digest/counter moves (P1) → killed as a law change.
- Patched 5×10^4 still climbs past the box limit → the deletion does not delete; report the
  measured residual (expected site if so: per-mint overlay snapshots accumulating within one
  epoch, or wave-time deltas).
