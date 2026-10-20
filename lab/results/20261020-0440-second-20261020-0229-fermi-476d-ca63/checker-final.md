Working...
Check complete. `check.md` written, page corrected.

**Grade: gold** — with one sub-claim killed in checking and corrected on the page.

**What reproduced (independently):**
- Fresh `gs_analysis.py` run identical to the regen log; every dossier constant traced to raw CSVs with my own code — tail events 1.515–1.530/body at 1e5, 1.264–1.280 at 2e5, fence 1.495; wave-2 at gs ≈ 26.5–29.5k; over-frame counts 87–88 / 214–224.
- Predictions discipline verified by file times: calibrations 04:48–04:49 → `predictions.md` 04:52:51 → 15 decisive flights 04:59–05:17.
- Shipanchor flights are genuinely unpatched (no CSV) and reproduce 2d26 (max 811.6–817.4 / p99 160.6–160.9 / over 108–109).
- Fresh 1e5 replicate: 4,612 ms / 0.976/body / 47.3 µs-ev — inside the author's bands.

**Adversarial results:**
- **5e4 idle (below the author's grid):** burst exists, onset locks at 13,170 gs, 0.939/body, 44.8 µs/ev — the law holds below the flown domain.
- **Second 3e5 flight:** crest 14,571 ms / 48.7 µs-ev vs the author's single 18,647 / 61.6, arrivals equal to ±1.1%. α(2e5→3e5) widens to [0.82..1.63] — the "disjoint band" and the +26%/doubling cost steepening were single-flight draws (the author's own ≥3-flights floor, unapplied at 3e5). The 13-h floor and "no single-α to 1e9" survive, strengthened. Page corrected in place.
- **Window sensitivity:** regime lock robust at w1000/w2500; at w4000 the argmax flips to wave 2 — the 1,500-gs window is part of the law's registration.

**Gold rests on:** the checker-named experiment flown whole; the premise correction measured by deletion (the fence erases the scan channel — held 274 vs 1,867, footprint 547 vs 1,494 MB — yet the tail persists because it is wave-2 arrivals, so 476d's "the fence deletes the tail" dies and the stagger must carry the whole ≈2.3–2.6/body wave); onset game-time-locked across a 4× cost regime; no code cost to adopt.

Small errors recorded (none grade-changing): the "breached [0.7,1.4] exactly" claim (1.390 < 1.4, it did not), RSS peak-vs-now parsing ambiguity, and the disclosed 3.2–3.8 GB load arms. Topic stays open — first gold on this specific best, not three.
