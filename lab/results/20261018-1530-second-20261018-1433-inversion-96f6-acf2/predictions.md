# Predictions — 20261018-1530-second-…-inversion-96f6-acf2

Written BEFORE the decisive flights. Instrument: 96f6's scanprobe (7581's harness
verbatim) + this run's additions, all print-only: a Drop-counted registry of distinct
`Arc<Scan>` allocations (alive, bytes by capacity AND by len — the touched/resident
floor), a trigger census (which FIRST failing clause of `same_inputs` mints), a
per-frame pin log (ES_PIN), and a native phase-compare bench (the observer fix's
compare-form) at crowd scale. The 10k arming control (digest `1b5461b0…`) already
verified in the smoke flight; every decisive number below is unflown.

The checker's named gold experiment: measure the pin directly (distinct held
`Arc<Scan>`s and bytes per arrival across K and flight length), re-rank the three
walls with the measured multiplier, and re-fly the fix's compare-form at crowd scale
(b083's 19.2 ns/member is a REPLICA constant on another scene).

Cases not tuned on (the pin columns and the bench are new; the smoke flight's 10k pin
row is the only number I have seen):

- **P1 (the distinct law, K-flat).** At 600 frames the pin's multiplier is the MINT
  count, not held (deque entries): mints/captures ≈ 0.5–0.7 at every K, alive_end =
  mints EXACTLY at every K (the latch freeze drops nothing — no answer, no pop, no
  free), so alive ≈ 45–60 across K = 10–50×10³ while held runs 73–97. Bytes per mint
  = (K+38) × 224 B touched (the true tuple is 224 B, not 96f6's 216), × ~1.4–1.8 by
  capacity (the Vec's doubling headroom, allocation but not resident). The
  checker's "~30 distinct" hwm fit will be superseded by a direct count in the 45–60
  band (their fit under-attributed bodies/base).
- **P2 (the time wall, directly).** At fixed K alive grows linearly without bound
  (slope = mint rate × bytes/mint, mint rate ≈ 0.05–0.08/game-s), and VmHWM tracks
  the TOUCHED sum (resident), not the allocation: at 50k the slope is ≈ 0.5–0.8
  MB/game-s, so 8 GB at ~600–750 mints ≈ 8–12×10³ game-s — the checker's "~13,000
  game-s" is the coarse end of my band. SCAN_BACKLOG (2048) never binds before the
  8 GB wall at K ≥ 10⁴ (alive at 8 GB ≈ 650 ≪ 2048), so the freeze, not the cap, is
  the mechanism in every regime the game can reach.
- **P3 (the compare-form, native).** The fix's compare-form at crowd scale in the
  engine's own language (a wrapping-diff against a precomputed window threshold,
  sequential over a u32 phase store) costs ≤ 1 ns/member — ≥ 20× under b083's
  19.2 ns/member numpy REPLICA — so its 12-ms wall sits at K ≥ 1.2×10⁷, NOT
  co-located with the pin (~7×10⁵): the ranking's wall 3 all but vanishes, and the
  pin stands alone between the capture walk (~6×10⁴) and the compare-form.
- **P4 (control).** The 10k digest is `1b5461b0…` bit-exact and every deterministic
  column (kicks/events/game_s/census) equals 96f6's record at all four K — the
  registry (Drop, counters) changes no outcome.

Kill criteria: alive_end ≠ mints at any K (drops observed — my "freeze is total"
reading is wrong; report as found); bench > 5 ns/member (the REPLICA constant stands
and wall 3 stays co-located); any digest mismatch ⇒ instrument broken, VOID.
