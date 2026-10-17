# Predictions — 20261017-1535-second-20261017-1447-system-6671-a60c

Written before the decisive runs (the two digest cases below were already launched as the
bit-exactness control; the timing matrix, the 10⁵ arms and every census number are still
unrun). The checker's named gold experiments: fly the (j,t) memo and measure real wall/p99;
measure the canonical-tick error at comb (pass) scale.

- **P1 (memo's real wall change).** At 10⁴ coast the memo moves engine p50 by −5…−15% and
  wall_s by the same order; p99 moves little (worst frames are event tails, not comb reads).
  Kill line: if the medians over ≥3 interleaved reps move < 2% (inside this shared box's
  noise), the memo's in-game win at 10⁴ is not measurable and the 1.7× stays a term ceiling,
  not a frame result.
- **P2 (flight hit rate ≈ census repetition).** memo hit_frac at 10⁴ coast ≈ 0.60–0.70
  (census: 64.5% at the secondaries site, diluted by the centre site's 6.8% repeated).
  If hit_frac < 0.3 the census's repetition was an artifact of its own per-call lock and the
  memo is dead.
- **P3 (comb-scale canonical-tick error — the prediction the first run misreported, now
  measured with an instrument that can see it).** Per pass (one `advance` = the frame's
  window, an upper bound on a drain slice), the source drift from the pass's first read:
  p99 < 1e-2 relative for every source — the author's own pre-registered line, which the
  whole-flight drift (3e-2…1e-1) crossed only because it accumulated over 35k game-s.
  Expect p99 ≈ 1e-4…1e-6. If any source crosses 1e-2 at pass scale, the structural half's
  "bounded quantization" premise fails for that source and I report it dead.
- **P4 (10⁵ and burn).** At 10⁵ coast hit_frac ≈ 0.35–0.45 (the checker's window-mixture:
  43.9% overall there) with the same structural split; p50/p99 change at 10⁵ at least as
  large as at 10⁴ (the read stream is N-linear). Burn: hit_frac a little lower than coast,
  conflicts still 0.
- **P5 (bit-exactness).** memo on ≡ off on every digest case and schedule, including the
  4-thread schedule (held for "coast through the wave": d2632de…, kicks 34537, both arms).
  Held-out here: "belt crossing L10" and "key mashing". Any difference kills the memo.

Baseline noise note: this box is shared; every wall number is a median over interleaved
A/B/A/B reps, and the digest (not wall) is the truth carrier.
