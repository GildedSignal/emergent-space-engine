# Predictions — 20261018-1433-inversion-96f6

Written BEFORE the decisive flights. Instrument: 7581's `scanprobe` verbatim
(604c harness + f134 arms + scan census + prof stages + ES_DUMP per-frame rows),
reused from the run's published branch, rebuilt from a clean tree at base
a63c446b (= 7581's base). Question, inverted: the composed crowd cure's frame
claim is "bounded at 10⁴ pending the observer fix" (7581's checker: at K=5×10⁴,
max_ev 29, kicks 539, but over 33, game_s 747/898.6). What owns those 33 frames?
If the answer is a term the pending observer fix does not delete, the crowd path
has a second wall behind the first and the fix's letter understates it.

Cases not tuned on (I have not run any of these arms at these sizes):

- **P1 (the ownership).** At K=5×10⁴ composed, the over frames are NOT comb-owned:
  per-frame events in over frames stay ≤ ~40 (the metronome is deleted), and the
  prof table's encounter/scan stages own the overhang — I predict the
  "encounters: capture (cheap half)" stage at O(K) µs/frame (capture walks ~1.00·K
  candidates at ~0.3–0.4 µs each ⇒ a single capture ≈ 15–20 ms at K=5×10⁴, i.e.
  one capture alone breaks a 12-ms frame), while the kick/boundary/open item
  stages sum to ≲2 ms/frame.
- **P2 (the law).** The capture channel is linear in K with no term the composed
  law touches: capture µs per capture at 5×10⁴ ≈ 5× the 10⁴ value, and
  binding_at/scan ≈ 1.00·K. Then the crowd's frame breaks at the arrival rate of
  captures (λ ≈ 0.1/game-s ⇒ one over frame per capture ⇒ ~1 in 8 frames once
  λ·capture > budget), NOT at the metronome — so "bounded at 10⁴" is really
  "bounded at the K where one capture exceeds 12 ms", i.e. K ≈ 3–4×10⁴.
- **P3 (the inversion bite — arithmetic on measured constants, no flight).** The
  pending observer fix (b083/5f36's phase tier) is measured as a REPLICA at
  ~19–20 ns/member vectorised capture and 0.67 ms/scan at K=10⁶. If wired exactly
  as measured it deletes P1/P2's term (capture → ~1 ms at 10⁶) — but it does NOT
  touch the ANSWER path's 4.4 µs/candidate reads nor the candidates-Vec pin
  (224 B × C, 1fcf) — at K=10⁶, one answered scan's exact reads ≈ 353 × 1.9 µs
  ≈ 0.7 ms (fine) but the pin at held 43 × 1.00×10⁶ × 224 B ≈ 9.6 GB busts 8 GB
  before the frame does. Prediction: after the observer fix, the crowd's next
  wall is MEMORY (the pin), not CPU — the fix's "≈1×" letter is true only
  because the freeze (latch) stops answering, which is what pins.
- **P4 (control).** composed at K=10⁴ reproduces 7581's record (over 0, game_s
  ≈ 898.6, kicks ≈ 609, max_ev ≈ 31) — the harness is 7581's, so this is the
  arming control; if it fails, VOID.

Kill criteria: P1 fails if over frames carry >100 events (comb-owned after all);
P2 fails if capture cost is super- or sub-linear across the two K (then the
"pending fix" reading changes); P4 fails ⇒ instrument broken, VOID.
