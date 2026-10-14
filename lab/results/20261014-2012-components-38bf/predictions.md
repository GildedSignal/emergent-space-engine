# Predictions (written before the decisive flights)

Scene: the ladder's wave scene on shipped main + this run's two edits (the `ES_PULL_CAP` bound on
`pull_ships`, default-unset; the `wave_input` bench). N=2×10⁵, seed 1, L8 burn from frame 60,
rtf 100, 12 ms budget, canonical cut at game 16,000 s (past the wave at 13.4-14.5 k game-s, before
the second at 26-29 k). All flights fly to the same cut and settle there.

- **P1 (baseline, cap unset, `plain`):** the wave reproduces — I expect monster frames in the wave
  window of order 0.1-1.4 s (6138 measured 1,213 ms at this N, seed 1, on a shared box), ≥ 10 frames
  over 12 ms, and the player in the root doll (0) when the wave lands (the L8 burn climbs out of
  Home's doll well before game 13 k s). If the player is NOT in the root doll at the wave, the whole
  exposure question changes shape (the pull then reads child ships only) and I must report that
  instead of the rest.
- **P2 (cap 64, `plain`):** bf21's certificate on my build — 0 frames over 12 ms, max ≤ 12 ms,
  digest **equal** to P1's (the cap changes no bit; the input histories are identical), worst lag of
  order 1-2 game-s recovering after the wave.
- **P3 (cap 64, `one` — a single no-op decision at the wave's p50):** the input call resolves the
  player's items up to `max(now, event_time)` — during the burn that is ~1 item, costing itself plus
  ≤ 64 pulled ship items (~50 µs each) plus one scan (~0.1-1.5 ms): I predict the call costs
  **2-8 ms**, lands inside one frame on top of its 12 ms budget, so **1-3 frames over budget, no
  monster** (max frame < 25 ms). Physics counters (kicks, events, encounters) **equal** to P2 —
  the no-op decision moves no bit; `decisions` differs by exactly 1 (and the digest with it, since
  the digest hashes the input log).
- **P4 (cap 64, `held` — the no-op decision every frame of the p01-p99 window, ~650 calls):** each
  call again resolves due player items; at 60 Hz this front-runs the queue's budgeted drain, so I
  predict **hundreds of frames over budget through the window**, max frame **15-40 ms** (each call a
  few ms unbudgeted), and the flight's total wall noticeably longer than P2's. Counters still equal
  to P2 (kicks/events/encounters within 0; `decisions` +~650).
- **P5 (the verdict this run is after):** the input seam's cost is **O(player items touched)×(cap),
  not O(backlog)** once the pull is bounded — i.e. the checker-2-bf21 "real untested exposure" is
  *bounded by the cap* on this scene, and what remains unbudgeted is the per-call constant (one
  player item + its scan). The falsifier: any input call in P3/P4 costing > 100 ms or resolving
  > 1,000 events (i.e. the cap not covering `input`'s path, or `event_time` being far ahead under
  burn so one input resolves many player items). If that fires, the hole is real and the exposure
  stands.

Held-out beyond this scene (named, not run): a *key-changing* input during the wave (it re-plans the
player, which a no-op does not), the player inside the belt band, and 4×10⁵ (this box's ceiling).
