# Predictions (written after the 1e4 validation arm, before every decisive arm)

The checker's named experiment: fly the cure env-gated (`ES_ROOT_STREAM=1`), show max_ms collapses to
~budget at every rung while the mint/answer identity holds to the canonical cut. The cure: when the
popped item is the player's and it lives in the root doll, resolve the earliest ship whose key is below
the player's first — as its own item behind the same budget gate, in the same key order `pull_ships`
uses — and only then the player's item (whose scan mints on those ships). Ships read only the sources
and the player reads no ship (the shipped comment's own argument), so the order change must be bit-free.

Arms flown under the same instrument as the disease (probe, one box, budget 12 ms):
cure-on 1e4/5e4/1e5/2e5 burn (2e5 with the 1750 MB cap), rtf 600, coast 1e5; disease contrast 1e4/1e5;
identity 1e4 and 5e4 with ES_IDENT=30000 (schedule the burn at tick 203e6, fly 20 s, settle to a fixed
cut, digest) off/on/naive plus a no-flight reference.

- **P1 (the collapse).** Every cure-on burn rung: `max_ms < 25 ms` (< ~2× budget) and
  `frames where one player item carried >500 nested kicks = 0`.
  Kill: any rung with max_ms > 50 ms or ≥ 1 such frame.
  Anchor: 1e4 validation read max 14.9 ms (disease 48.3), crest frame = 332 ship items, 0 mega.
- **P2 (p99).** Cure-on p99 ≤ 12.5 ms at every burn rung (the disease: 12.0–105 across rungs —
  the 105 was the gulp tail). Kill: p99 > 25 ms anywhere.
- **P3 (the law holds — the decisive one).** The canonical-cut digest is the SAME STRING with the cure
  on, with the cure off, and from the no-flight reference, at 1e4 and 5e4 (the cut is past the wave at
  ~14.3k game-s). The counters beside it (kicks, encounters, contacts, lost) match too.
  Kill: any mismatch. A mismatch means the cure is not adoptable, however smooth it is.
- **P4 (the negative control).** The naive variant (pull nothing in root, mint on stale bindings) gives
  a DIFFERENT digest at 1e4 — the waiting is load-bearing and the test can fail.
  If it does not differ: reported as the pull's exactness not biting at this scene (P3 unaffected).
- **P5 (the trade).** The cure defers the player's items behind the drain, so the presented time lags:
  cure-on `lag_s ≥ 0.9×` the disease's at 1e5, and the rtf delivered (game_s) within 2× of the
  disease's. Frames over budget collapse to ≤ 5 at 1e5/2e5 (disease: 71 at 2e5). No kill: measurement.
- **P6 (inert where the player is not in root).** Coast 1e5 cure-on: max_ms within ±25% of the
  checker's 17.7 ms coast number (the cure never fires out of root). Kill: none (control).

What would make the whole run void: the probe's decomposition showing the cure's items escaping the
budget gate (max back to seconds), or RSS > 2 GB killing a flight before its wave.
