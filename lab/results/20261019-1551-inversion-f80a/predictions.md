# Predictions — 20261019-1551-inversion-f80a

Written before any flight on this tree. Scene: `nladder 30000 burn <wall_s> 1000 12`
(seed 1, L8 burn from frame 60, rtf 1000 — the game-time laws (mint rate per game-s,
TTL in game-s, keep windows in ticks) are rtf-invariant; rtf only sets frames per
game-second, which I do not measure). Probe every 1,000 game-s; RSS guard 1,600 MB.
Binary: e181's patch verbatim + the frame-loop `prune()` call RESTORED (its checker's
named correction (a)) + `history_census` in the probe (527a's fields). With
`ES_SCAN_TTL_S` unset the tree is shipped behaviour again.

The inverted claim under test: e181's "expiring held scans past 16 game-s deletes the
burn-mode memory ratchet" — measured only to 41.9k game-s (and only with `prune()`
deleted from the frame loop). 527a measured a second, later channel (history
retention behind the receding observer, onset ~95–130k game-s at 3×10⁴) that the
fence does not touch. The fence's flatness has never been flown past that onset.

- **P1 (control, the OFF arm: TTL unset, prune restored ≡ shipped).** The census
  ratchets with play time past ~95–130k game-s: `hist_gt1` climbs toward ~30,000 of
  30,076 bodies and `hist_total` grows by ~+30k bindings per ~28k-game-s kick wave
  (527a's law), with RSS staircasing; the arm guard-stops (channel 1's scans dominate
  bytes) or ends at the wall cap with the census visibly climbing. Falsifier of my
  reading: the census stays ~1 binding/body flat to 150k game-s → channel 2 does not
  reproduce on a prune-restored tree, and 527a's channel 2 was an artifact of the
  1b3f-tree state; I report that and the run's headline flips to a positive
  certificate for the fence.
- **P2 (scoped reproduction, the ON arm: TTL=16, prune restored).** Below the onset
  the fence holds as e181 measured: `held` ≤ a few at every probe, RSS flat-ish
  (~250–700 MB band, no channel-1 staircase, slope ≪ 4447's 3–5 MB/1k game-s), counter
  identity mints = answers + expired (+ held_end).
- **P3 (decisive, held-out: the ON arm past ~130k game-s).** The fence does NOT
  delete the ratchet, only its scan half: `hist_total` climbs at the OFF arm's rate
  (+~30k/wave, K-linear bytes ~2 KB/binding) and RSS staircases again from the onset,
  slope ~55–65 MB per 28k game-s at 3×10⁴ — the composed adoption (byte-capped scans
  first, per-reader oldest second) leaves the burn flight dead at channel 2's horizon,
  roughly 0.3–1×10⁶ game-s at 3×10⁴, later at lower K, earlier at higher K.
- **P4 (mechanism check).** In the ON arm the census onset tick is within ~±30k
  game-s of the OFF arm's onset on the same tree (channel 2 is scan-independent: the
  fence moves bytes, not the retention law). If the onset MOVES (earlier/later by more
  than that), the two channels are coupled and I report the coupling, not the
  independence.
- **P5 (frame sanity, not a target).** At rtf 1000 frames carry ~10× the events of
  rtf 100; over-budget frames and lag are expected and are NOT part of any claim
  (memory channels only).

Kill criterion for my own claim: if P3's ON-arm census stays flat (< 1.1 bindings/body
at 240k+ game-s with RSS slope < 5 MB/1k game-s past 150k), then e181's headline
survives its own unflown horizon on a corrected tree and the fence is stronger than
the record believes — also a result, reported as such.
