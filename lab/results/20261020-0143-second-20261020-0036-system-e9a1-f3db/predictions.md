# Predictions (written before the decisive flights)

Probe: `ES_ITEM_PROBE=1`, print-only (env-gated eprintln; off = shipped bits). One `player_item` line
per player item (wall time and counts of its un-budgeted edges: the fleet loop's `resolve_fleet`
calls / slices / kicks minted / ns, the hand-out loop's calls / ns, the ship pull's ns, the scan's ns,
the item's own process ns) and one `frame_items` line per frame (top-level items by class, the worst
item's class and ns). ee4d's gold cure is carried verbatim, env-gated (`ES_ROOT_STREAM=1`), plus its
`naive` control (`ES_ROOT_STREAM=naive`), so the same probe flies disease, cure and control.

Scenes: shipped `nladder`, seed 1, rtf 1000, 12 ms budget, 20 s wall. Arms: `100000 burn` and
`200000 burn`, each flown three times (disease / cure / naive).

The claim under test (the checker's named experiment): the wave frame's 815 ms (1e5) / 1,633 ms (2e5)
is the player item's un-budgeted nested edges — the fleet loop and the hand-out loop — not the ship
pull (which e9a1 measured pulling zero); and ee4d's cure collapses the freeze by *deferring* the
player's item, not by anything it does to the pull.

- **P1 (the disease's mechanism, measured):** in the disease arms, the worst player item carries
  ≥ 70% of the worst frame's wall time inside its fleet loop + hand-out loop combined (the split
  between them is what this run measures), with `fleet_kicks` ≥ 5×10⁴ minted inside that one item at
  1e5; `pull_ms` ≈ 0 (e9a1's pulls = 0, now with the pull's wall time attached).
- **P2 (the cure defers, the law work is unchanged):** with `ES_ROOT_STREAM=1`, max_ms ≤ 30 at both
  rungs, every player item's `fleet_ms` ≤ 5 ms, and the flight's total kicks within 10% of the
  disease arm's (the same law work, moved behind the budget gate).
- **P3 (the naive control does not cure — ee4d's parenthetical falls):** with
  `ES_ROOT_STREAM=naive`, max_ms ≥ 300 at 1e5 (the freeze stays: the skipped pull is empty on this
  tree, so naive ≡ shipped bits). If naive also collapses the freeze, the mechanism is not the
  deferral and P1/P2's reading must be re-derived from the probe lines.
- **P4 (where the work went):** in the cure arms' worst frames, top-level items per frame ≥ 50
  (the wave minted as budgeted items, seen in `frame_items`), against ~1 item in the disease's
  worst frame.

Failure handling: P1 failing (the nested edges carry < 70%) means the freeze lives in the player
item's own `process` or the scan — the probe lines say which, and that becomes the result. P3
failing (naive cures too) kills the deferral reading and re-opens the mechanism; both are reportable
outcomes, not reasons to stop.
