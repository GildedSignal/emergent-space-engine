# Predictions (written 13:52, before the decisive flights; smoke N=1000 burn 6 s disclosed above)

Question: what is the scan-answer freeze at 1e9 made of? 9ed1's checker priced the bite as
O(N_belt) at 4.2–4.4 µs/body ("~4 ks in one frame at 1e9"), inferred from three rungs at fixed
density. Code reading (encounter.rs/radial.rs) says there are TWO walks: the CAPTURE (radial index
bail → 0..n_bodies walk with a binding_at per body, on the frame's critical path) and the ANSWER
(one exact fixed-point cartesian + integer predicate per captured candidate, idle/drain). The
checker's law fits either; the decomposition decides the fix and the 1e9 price.

Arms (decisive, sequential, idle box): `ES_SCAN_TRACE=1 nladder <N> burn|coast 40 400` at
N = 1e5, 3e4 (both flights), plus coast control at 1e5. Each self-caps at 55 s.

- **P1 (the bail):** in the root doll with the belt, `radialbail why=occ` dominates captures:
  walk=1 on ≥ 80% of root-doll captures, cands/N = 0.3–1.0 (the window's velocity term × the
  binding interval spans the annulus; the N/4 occupancy rule gives up).
  Kill: if the index passes in the root doll (walk=0 dominant), the O(N) capture claim dies and
  the 1e9 price is window-limited, not N-limited.
- **P2 (capture cost):** walk_us = 0.1–1.0 µs/body (binding_at per body) → 10–100 ms per player
  item at 1e5, ON the critical path (prof class ENCOUNTERS / the player item).
  Kill: walk_us < 0.05 µs/body (capture < 5 ms at 1e5) → the capture is not the freeze's peer.
- **P3 (answer decomposition):** cand_us = 3–8 µs with cart_us ≥ 70% of it; cands/N and cand_us
  roughly flat 3e4→1e5 (so 4.3 µs/body = cands/N × cand_us, both constant at fixed density).
  Kill: cands/N < 0.1 at 1e5 → the window filters most of the belt and the 1e9 answer is ≥ 10×
  below the checker's 4 ks.
- **P4 (the composition):** at 1e9 fixed density: capture ≈ 1e9 × walk_us ≥ 100 s per player
  item; answer ≈ 1e9 × (cands/N) × cand_us ≥ 1,000 s per distinct scan. So a per-candidate cost
  cut alone (the retired cheap bound, 3–6×) leaves both walks ≥ 100 s: only a candidate-set cut
  (the Binet cone / incremental answering) closes. Kill: measured cands/N × cand_us × 1e9 < 100 s.
- **P5 (coast control):** coast shows the same root-doll bails and the same cands/N (the window
  is interval-driven, not burn-driven).
  Kill: coast's root-doll captures pass the index → the bail is a burn artifact only.

Calibration: N=1000 burn 6 s (above): player in doll=2, indexed (near 8–40), cand_us 4.3–7.3 µs,
cart_us ≈ 93% — the instrument reads the two halves separately.

## Appended after D1 (1e5 burn), before the re-flights (13:56)

D1 falsified P1/P2 as written: the radial index NEVER bailed (2,595/2,595 captures indexed,
walk=0), cands p50=94 max=1,804, capture ~0.66–0.85 µs/candidate. P3 held (cand_us p50 4.96 µs,
cart 93.9%). The max single answer is 8.1 ms (1,804 cands) — 9ed1's 442.9 ms frame is NOT one
answer. New prediction:

- **P6 (the freeze is a DRAIN, not an answer):** a frame that drains the held-scan backlog pays
  MANY distinct answers at once; the 0.4–1.2 s bites = (distinct answers drained) × (cands ×
  cand_us), with per-answer ms = cands × ~5 µs. With wall stamps on each answer I predict the
  bite frames show ≥ 50 answers inside one wall-millisecond cluster at 1e5-class cands.
  Kill: if bite frames carry ≤ 5 answers each, the drain story dies and the bite is elsewhere.
