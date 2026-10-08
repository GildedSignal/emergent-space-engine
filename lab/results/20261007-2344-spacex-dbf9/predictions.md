# Predictions (written before the decisive runs)

H_live = the tube ledger defined in `dossier.md`: per body, the minimal delta-encoding bits of its
current binding against its birth binding (doll re-anchors carry the ledger and charge 1 flag bit);
created/reabsorbed are the positive/negative parts per event; the player's decision words add 8 bits
when the word changes. Measured by `xtask universe --bench` (patch adds the `h_live` report).

Held-out cases (not tuned on):

1. **Swallowed kicks (distinct-kick accounting, the 5 Oct lesson).** Share of kick rebinds where the
   tube's own fields (key, angle, periapsis time) do not move at all: I expect a majority,
   40–90%. (The quantized-cell memo artifact hit 94.5%, but that was re-timed kicks; these are
   resolved kicks with their actual old→new deltas.)
2. **Channel mix.** For the plane's scene at 30 game-seconds, the decision channel (the scripted
   player, ~7.5 decisions/s, 8 bits on a word change) dominates the tube channels by at least 10×:
   bodies at AU scale kick once per ~10³ game-seconds each, so tube bits/game-second is small.
3. **Not bounded within the run.** `live_now` (net live bits) grows monotonically-ish over 30
   game-seconds: reabsorption is nonzero but creation exceeds it (scars accumulate slowly). I expect
   net/live ratio > 0.5 at the cut.
4. **The 10⁹ question (the board's decision).** Per-body creation rate: if a body suffers ~10⁻³
   kick-events per game-second at ~30–60 bits each, 10⁹ bodies × 1 hour lands at 1–20 GB of scars —
   the same order as the 8 GB budget, NOT safely below it. I predict the measured per-body rate puts
   an hour of 10⁹ bodies within a factor of ~3 of 8 GB either way, so reabsorption and the
   interaction rate (not the body count) decide the fit. If instead it lands ≥ 100× below 8 GB, the
   memory question closes outright and the board item should fall.
5. **Digest invariance.** The patch changes no outcome: the universe test suite (which pins replay
   and digest identities) passes unchanged, and two bench runs at one seed and cut give one digest.
