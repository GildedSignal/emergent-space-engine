# Predictions — run 20261007-1234-second-20261007-1106-fermi-443e-d57e

Written before the decisive runs, after only the N=12/M=8 smoke test (which showed: 8/8 crossers hand
off, same-doll delta ~29.7 bits/event, reabsorption 1.04 over 1 orbit, doll-change re-reference 52 bits,
bytes/body 3,119 after prune). The smoke numbers seed the ranges below; nothing at N=1000 or seed 2 has
been run.

The checker's gold experiment: `hlive` on a concentrated belt/fleet (B18b scale, handoffs present, the
restricted class), rate anchored per doll binding event, kicks-per-binding reported, predictions
pre-registered, tally clean.

Runs planned:
- decisive: `hlive_belt 1000 5 1 2048 96` (1,000 ring ships, 5 planet periods ≈ 1.9e9 game-s, seed 1)
- held-out seed: `hlive_belt 1000 3 2 2048 96` (never tuned on)
- scale row: `hlive_belt 10000 1 1 2048 96`
- plane regeneration: `hlive 3600 1 400` (the original record)

| # | prediction | range |
|---|---|---|
| 1 | handoffs = one per surviving crosser | 90–96 (birth refusals may drop a few) |
| 2 | same-doll delta bits/event (varint stream) | 25–40 bits (smoke 29.7); still zlib-incompressible (<10% saving) |
| 3 | doll-change (handoff) re-reference, new-doll residual | 40–70 bits / 4 components (smoke 52) |
| 4 | reabsorption ratio late/early (5 planet periods) | < 1.3 (bounded; smoke 1.04 at 1 orbit) |
| 5 | bindings/body/game-s (doll binding events, the anchor) | 5e-7 – 1.2e-6, and the N=10^4 run's per-body rate within ×1.5 of N=10^3's |
| 6 | kicks per binding | 1.0–2.0 (near-complete capture at spo 2048/orbit) |
| 7 | bytes/body after chunked prune (steady-state cache) | 2–6 KB, no growth with N |
| 8 | H_live creation at 10^9 from the belt anchor | ≤ 5 KB/s (≥10^7× under the M1's 60 GB/s): the premise kill generalizes to belt scale |
| 9 | held-out seed 2: reabsorption ratio and delta bits | ratio < 1.3, bits/event within ±30% of seed 1 |

Kill criterion (pre-registered): if the reabsorption ratio exceeds 1.5 on any belt run, or per-body
binding rate grows with N (superlinear concentration of live distinctions), the original claim's
"H_live is not the binding term" does NOT generalize to concentrated belts and the run reports that.
