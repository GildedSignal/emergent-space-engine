# Predictions (written before the decisive flights)

Question: the belt's BOUNDARY comb — its rate and per-item cost on the shipped belt stream, and the
row it adds to the 10^9 CPU ledger (budget-1e9 line: "the belt's boundary items are unpriced").

Cases I have NOT tuned on (held out from the run's own first flights; constants taken from the wiki
record, not from my instrument):

1. **Boundary rate.** The clock law (step.rs:717-718) inserts one Boundary and one Kick per interval,
   so I predict `rate_boundary/rate_kick` = 1.00 ± 0.05 at the belt rungs (3e4, 1e5), and both within
   3.0–4.0e-5/body/game-s at 1e5 (the record's kick rate 4.889e-5 includes ~300 locals firing faster;
   at 1e5 they are 0.3% of bodies and a few % of events).
2. **Boundary item cost.** Two record instruments disagree 2.1×: 8365's era split says 5.9–8.6 µs
   x86; 3aec says 18.4 µs x86. My direct per-kind timer (the full item: resolve_body incl. apply and
   the plan read, excl. requeue) I predict lands at **6–10 µs x86** — 15d7 showed the boundary comb
   never fires a certificate on the belt's own stream (no crash/leave/handoff), so the item is
   readout + norm + anchor + queue overhead, closer to 8365's number than 3aec's. If it lands at
   15–20 µs, 3aec's number stands and 8365's era split under-counted (a finding either way).
3. **Kick item cost** (control, the instrument's positive side): 40–50 µs x86 at the belt (8365:
   45.3–45.9; 3aec: 44.7 "the belt's own clock item"). If mine is far from that band, my timer is
   not measuring the same item and the boundary number is not to be trusted either.
4. **N-flatness.** Per-item costs flat from 3e4 to 1e5 within ±20% (the kick item is N-flat to 4e5
   per 3aec's checker; boundaries touch no catalogue work that grows with N).
5. **The composed row.** With rate_b ≈ rate_k ≈ 3.5e-5/body/gs and cost_b in [6, 10] µs x86:
   boundary row at 1e9, rtf 100 = 1e9 × 3.5e-5 × 100 × (6–10) µs = **21–35 cores x86** (≈ 12–20
   M1-adjusted at the record's 0.58 anchor) — i.e. the stream row grows from the page's 193 to
   ~215–230 cores at shipped cadence (+11–19%), and after the mandatory split8×survival (4.92× on
   both combs) from 39.3 to ~44–46 cores. The blended per-event bar for the two-comb stream at
   split8 and a 4-core budget moves from 4.9 to ~4.2–4.4 µs/event.
6. **Kill criterion for the row's importance:** if the boundary row lands under 10 cores x86
   (cost_b < 3 µs at the measured rate), it is under the page's "lever < 2×" bar on its own row and
   the dossier reports "unpriced no longer, and small".
