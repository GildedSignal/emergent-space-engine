# Predictions (written before any patched flight ran)

The checker's named experiment: implement the run's own fix — hold the player's scan when the
ship backlog it would read exceeds a threshold, so the pull never runs on a saturated queue —
and fly 2×10⁵–3×10⁵ burn past the wave showing a bounded worst frame with the digest unchanged.

The fix as implemented (details in `work/fix.diff`): the player's in-root item resolves at most
`PULL_HOLD = 64` ship items of its pull; over that, the rest is left to a budgeted drain inside
`advance` (key order, the pull's own order, one item a pass behind the same `spent_before` gate
as any other item), and the scan that needed the pull is held as a `Waiting` entry that captures
only once the ship lane is clear of its key (answered FIFO, folded into the digest like any held
scan). The children-only pull (player out of the root doll) is untouched. Set-up for the checks:
the engine carries a `#[doc(hidden)] set_pull_hold` so the deferral can be forced on (`0`) on
shipped scripted flights.

Kill criteria per prediction; all on this Linux box, 200 s flights, rtf 100, budget 12 ms,
seed 1 unless said, `NLADDER_MAX_S=260`.

- **F1 (the monster is gone, the frame is bounded).** worst frame at 2×10⁵ burn < 25 ms
  (shipped: 1,213 ms; the residue is the budget tail plus one started item plus the ≤64-slice,
  ~3 ms at 49 µs an event). Kill: any frame > 100 ms.
- **F2 (no unbudgeted batch).** max events/frame at 2×10⁵ burn ≤ 2,000 (shipped: 24,467; the
  budgeted drain carries ~235 an item-bounded frame, plus the 64-slice). Kill: > 5,000.
- **F3 (the freeze becomes lag, and recovers).** the same arm's worst lag ≥ 1.0 s (the drain is
  budget-saturated through the wave, as the coast control already was: 1.45 s) and frames are
  back under 12 ms by 190-200 s. Kill: frames still over budget at 190 s, or worst lag < 0.3 s
  with the wave passed (then work went missing, not moved).
- **F4 (bit-exactness on the shipped certificate).** `frame_digest` (the shipped harness,
  scripted flights, 4 schedules): every digest identical pristine vs fixed, and identical again
  with the deferral forced on (`set_pull_hold(0)`): the held scan's capture reads the same
  post-pull state, only later. Kill: any digest differs, or any schedule disagreement.
- **F5 (canonical equality on the belt flights themselves).** 2×10⁵ burn and coast, settled to
  the same canonical cuts past the wave (16,000 and 19,000 game-s): `digest()` identical
  pristine vs fixed (the drain reproduces the pull's resolution set and order, spread over
  frames; a settle's unlimited budget finishes every held pull below the cut). Kill: any cut
  differs. Known residual risk, watched for: a root-doll ship that dies between the item and
  the late capture changes the candidate filter's `alive` read (shipped captures before any
  such death resolves); belt flights have no root-doll deaths in the window, scripted flights
  may — if it fires, it is reported, not hidden.
- **F6 (the work is moved, not deleted).** events resolved by flight end at 2×10⁵ burn within
  3% of pristine (same items, other order). Kill: a gap > 10% (then the fix drops work).
- **F7 (the control arms are untouched).** coast, same seed: max frame and digest as pristine
  (the player never enters the root doll; the fix never engages). Kill: coast's frames or
  digest move. 10⁵ burn (checker's 5×10⁴ point is below this box's onset) engages the fix:
  worst frame < 20 ms there too (shipped 315 ms).
- **F8 (3×10⁵, if the box allows it).** the M1 record's arm re-flown here would exceed the
  2 GB process cap (~2.2 GB at 3×10⁵); if it is killed, the 2×10⁵ arms plus the M1's
  37,938-event demand (the drain's budget makes the per-frame share ~235) carry the scaling
  claim, and the cap is the stated reason.
