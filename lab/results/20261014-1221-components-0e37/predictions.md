# Predictions (written before the decisive run)

Decisive run: `cache_census 100000 80 200` (N=10⁵ belt, 80 wall s, rtf 200 → ~16,000 game s,
past the first-kick wave at 13,051–14,534 game s). Tuned on nothing: the only earlier execution
was a smoke run at N=2,000 for 8 wall s (pre-wave, game 1,597 s), which fixed the instrument, not
these numbers. The N=2,000 smoke's flight rate (195 decodes/frame) is the small end of P1's
scaling prediction, not evidence for it.

- **P1 (flight reads are O(1) in N).** During the headless flight (no view gather running), the
  per-frame decode count is set by the fixed cast (the player's seam, the 48, the planets, the
  locals), not by N: at 50× the bodies it stays within ~3× (≤ ~600/frame). Then reads per held
  table per game-second land at ~10⁻⁴ or below at N=10⁵ — the held tables are, for the engine's
  own work, **write-only**: read only when their own body's next kick rebinds. Falsified if
  decodes/frame grows ≥10× when N grows 50×.
- **P2 (the wave doubles the standing shape bytes).** Crossing game 13,051–14,534 s, history
  segments jump by ≈ +N (one retired binding per belt body), retired shape bytes ≈ current shape
  bytes (the belt band's tables are small, e ~0: expect shape ~0.5–1 KB/body per generation, not
  the plane's 4 KB), so accounted standing goes from ~1.1 to ~1.8–2.2 KB/body and the footprint
  jumps correspondingly. Falsified if retired shape ≢ current shape within ~2×, or history grows
  by materially less than N.
- **P3 (nothing reads the retired belt tables).** Retired segments' tables get ≈0 reads in
  flight; the only mass reader is the view's gather, which walks Θ(N) rows at ~9 decodes per row
  (measured 8.91 on the smoke run) — i.e. the knots are deletable for compute, and blocked from
  deletion only by the view's far-row walk (view.md's tax). Falsified if flight decodes exceed
  P1's prediction by an order of magnitude, or a gather reads retired tables at a rate ~1/row.
- **P4 (the cache is exactly the key).** Orbit::compile(key) reproduces 100% of sampled current
  Cycle tables bit-for-bit on knot/crossing counts and the three channel increments. Falsified by
  any mismatch (which would name a hidden input beyond the OrbitKey).
- **Floor (not a prediction, an accounting):** the law-mandated standing state per kicked body is
  BodyRec 464 + plan (~1 item × 16 B) + one Segment 208 ≈ ~690 B, plus ~0.5–1 KB of derived
  knots per generation of table. If P1–P3 hold, the derived share is deletable down to a bounded
  reader working set, and the belt-band idiot index (standing/floor) drops from ~2–3× to ~1× —
  the memory lever is then the rec/segment width itself (BodyRec 464 B), not the knots.
