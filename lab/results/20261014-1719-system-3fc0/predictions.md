# Predictions (written before the decisive run)

The change under test: `Universe::resolve_body`'s player branch synchronously drains
`pull_ships` (every ship item below the player's key) so the encounter scan never reads an
expired certificate. During the belt's first-kick wave this is an unbudgeted batch
(measured by 6138: up to 24,467 events, 315–1,213 ms single frames at 10⁵–2×10⁵ burn).
The patch bounds the pull to N items (env `ES_PULL_MAX`, deterministic, game-time) and,
when truncated, holds the scan (skips this item's `encounters_for_player`; the next
player item rescans, and the queue's budgeted drain feeds it) — 6138's named fix, built.

Scene: members = 100,000 (belt 199,700 bodies total per 6138's census at 2×10⁵; at 10⁵
the belt is ~99,7xx), seed 1, reverse L8 burn from wall-second 1, rtf 200, wall budget
12 ms, cut at 16,000 game-s (the wave is 13,037–14,542 game-s).

Cases not tuned on (I have not run anything yet):

- P1 (world bits): `digest` and `kicks` at the cut are **identical** pristine vs
  ES_PULL_MAX=256. Ground: the code's own invariant ("ships read only the sources, and
  the player reads no ship: resolving the player's item before theirs changes no bit"),
  already relied on for the out-of-root path. If P1 fails, the pull is load-bearing
  beyond ordering and the fix's certificate is false — that would refute 6138's "hold it"
  in its simple form.
- P2 (the instrument): `encounters`/`contacts` at the cut — I expect **a small difference
  or none**; this is the genuinely uncertain half. A skipped scan loses one look; if the
  wave's scans find nothing (belt far from the player), counters match exactly. If they
  differ, the held scan is observable in the encounter log and the deferral must carry
  the scan's own t (a stricter fix), which I will report as the boundary, not paper over.
- P3 (the point): worst `frame_to` wall time drops from the monster scale (hundreds of
  ms) to ≤ ~30 ms (256 items × ~49 µs + the frame's own work), and frames over 12 ms
  fall by an order of magnitude. If the monster persists, the pull was not the batch's
  only source and I must find the second one before claiming anything.
- P4 (schedule invariance): the digest at the cut is the same at ES_PULL_MAX=64 and 256
  (both truncate, differently) — the truncation count must not leak into the world's bits.

Kill criterion for my claim: P1 or P4 failing kills "the pull is deletable ordering";
P3 failing kills "the pull is the monster".
