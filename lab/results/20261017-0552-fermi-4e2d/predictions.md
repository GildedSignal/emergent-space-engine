# Predictions (written before the decisive flight and the ledger run)

Held-out cases: nothing below was tuned on. The two-comb identity and the per-event
costs come from 8ffc/9e75/4093's record (other boxes); my flight is the first time I
run them, on this box, at N=10^4 (8ffc's checker flew N=10^4 once: 1.008 kicks +
1.007 boundaries per belt body; my N and window differ in delivery).

## P1 — The stream constant from shipped code (`belt_first 10000`)

Prediction: the belt's first item p50 lands at ~14,072 game-s (the interval/2 comb
phase; 8ffc/4093 anchor 13,051–14,534), and the interval identity P_D(Cinder)/2^7 =
28,141.5 game-s reproduces from scenario constants to <1%.
Kill: if p50 differs by >25% (i.e. the comb phase is not interval/2), the ledger's
per-interval normalization is wrong and I must re-derive the whole stream from the
flight instead.

## P2 — The two-comb identity on this box (`nladder 10000 coast 46 900`)

One interval's window [~0, 41,400] game-s, before interval 2's kick comb (42,216):
Prediction: kicks/belt-body ≈ 1.00–1.02, boundaries/belt-body ≈ 1.00–1.02 over the
window (locals' comb excluded by scaling: locals ≈ 300 bodies, belt ≈ 9,700).
The stats line reports per-body rates over ALL bodies; with locals ~3% of bodies and
their fixed comb ~10.1 k events/interval, I expect all-body boundaries/body slightly
ABOVE the belt-only identity (locals add ~1 event/body-local/interval ⇒ +3% on the
all-body mean is 8ffc's fixed-comb reading).
Kill: if boundaries/body < 0.5 or > 1.5, the two-comb reading does not transfer to
this box/N and the +26% correction is box-specific.

## P3 — The composed 10^9 ledger (arithmetic; page constants, my anchors)

Written before running ledger.py, from the constants already on the pages:
- Shipped cadence, two-comb, M1-equivalent anchor: 120–140 cores at 10^9 rtf 100
  (e7ef said 104 kicks-only; the boundary comb adds ~25%).
- With the 8x BELT_SPLIT (both combs stretch) and the 61% hybrid delete:
  6–7 cores — still 1.5–1.8x over the 4-core budget.
- If BELT_SPLIT does NOT stretch the boundary comb: 25–30 cores — ~7x over; the
  boundary comb alone (12.9 µs/body/interval) would be ~70% of the composed stream.
  So kick-cadence's open direction 1 (does the split stretch the boundary) is worth
  a factor ~4 in the 10^9 ledger — the largest single unknown left in it.
- The encounter tier, at the adjudicated shipped-key anchor (f0a2): 0.03–0.6 cores
  (closes). I verified the anchor premise myself from `crates/space/src/lib.rs`:
  `Key::new` stores E absolutely in Q48 on scale 1 (0 < E <= 16).
- Promotion traffic of the compact wiring: CPU-free (the mint IS the kick's compile,
  cbc5's reconciliation; demote 0.08 µs); the wiring's cost is memory: live set =
  mint rate x dwell. After the levers, mint rate ~2–4x10^3 events/game-s at 10^9,
  so dwell must sit in a window: >= ~100 gs (below it, 8792's re-mint cliff) and
  <= ~300–600 gs (above it, live x 4.85 kB plateau busts ~1.5–3 GB). Non-empty by
  ~3x — my dwell-window claim, the one number here nobody has composed.
- Total memory at 10^9: compact stock 1.7–2.4 GB (self-stirred belt, 07b4) + live
  set (dwell law) + engine: 4–6 GB against the ~6 GB usable. Closes within ~1.5x.

What would make the ledger wrong: (a) P1/P2 fail (the stream normalization);
(b) the M1/x86 event-cost ratio 0.586 (29.3/50) is wrong — then every M1 row scales
by the same factor and the over-budget factor moves with it; (c) the hybrid delete's
61% does not apply at the 10^9 belt's legality mix (measured on the ladder belt at
10^3: 274/712 belt bodies deleted — if the 10^9 belt is more resonant, the delete
shrinks and the over-budget factor grows pro rata).
