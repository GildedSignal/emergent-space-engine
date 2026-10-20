Grade: gold

## Abstract (for the integrator)

476d's named gold experiment flown whole, and its adoptable core holds: onset_gs locked to 13,107–13,270 across a 4× cost regime (regime shift of medians 1–9 gs while frames drift 449→1,393), arrivals 0.94–1.04 events/body K-flat and load-flat, per-event cost the only super-linear carrier. The fence deletes the scan channel (held_max 274 vs 1,867; end footprint 547 vs 1,494 MB) yet the tail persists — it is wave-2 arrivals (1.50/body extra at 1e5, 1.28 at 2e5), so 476d's "the fence deletes the tail" dies and the stagger must carry the whole ≈2.3–2.6/body wave. No single-α 1e9 composition; floor 13.2 h/wave. Adoption cost: none in code (repricing only). One sub-claim died in my checking: the α(2e5→3e5) disjointness and cost steepening rest on the single 3e5 flight (my second reads 14,571 vs 18,647 ms) — page corrected.

## Reasons

**1. Reproduction.** The runner's regen exited 0; my fresh `gs_analysis.py` run is identical to `regen.log`. I re-derived the load-bearing numbers independently from the raw CSVs with my own code (never importing the author's): tail events 1.515–1.530/body at 1e5 idle, 1.264–1.280 at 2e5, fence 1.495; over-frames 87–88 (1e5 idle), 214–224 (2e5 load); wave-2 sits at gs ≈ 26.5–29.5k, i.e. one full second burst of ≈1.0/body plus the ≈3k-events/1k-gs baseline. The 7 shipanchor flights are genuinely the unpatched binary (no CSV lines) and reproduce 2d26 (max 811.6–817.4 / p99 160.6–160.9 / over 108–109 vs 812.6/160.5/108). The instrument is behaviour-neutral (kicks_per_body_gs 4.863e-5 vs 4.866e-5 patched/unpatched).

**2. Held-out discipline.** File times: calibrations 04:48–04:49, `predictions.md` 04:52:51, all 15 decisive flights 04:59–05:17, dossier 05:20. Bands were pre-registered with kill bars. P1/P2/P3a/P5 held; P4 failed on its letter and fired K4 — and that failure IS the run's finding: K4's own parenthetical reads "tail ≠ held-scan channel", so its firing refutes 476d's attribution while the crest constants (P1/P2/P3a/P5) all held. The kill-header's blanket sentence ("any bar fires → crest law not adoptable") is over-broad — an instrument error the author disclosed prominently rather than hid. This is H0183 done right ("a failed expectation is not automatically a failed method").

**3. Attacks (three fresh flights, one below the author's grid; plus analysis-level probes).**
- **5e4 idle (below the grid):** the burst exists, onset_gs locks at 13,170, arrivals 0.939/body, 44.8 µs/ev. The law's claims hold below the flown domain. (476d's checker saw no 5e4 burst only under load-24 — crest-vs-amortized stays schedule-chosen, consistent with the record.)
- **Second 3e5 idle flight:** crest 14,571 ms / 48.7 µs-ev vs the author's single 18,647 / 61.6, with arrivals identical to ±1.1% (299,383 vs 302,837 events). α(2e5→3e5) widens from [1.427..1.632] to [0.82..1.63] — overlapping α(1e5→2e5). The "disjoint bands" and the "+26%/doubling steepening" are single-flight draws; the author's own ≥3-flights-per-rung floor was not applied at 3e5. What survives is stronger: no settled power law (even a rung-pair exponent swings 22% at n=2), the 13-h floor, and "no single-α to 1e9". Page corrected in place.
- **Fresh 1e5 idle replicate:** 4,612 ms / 0.976/body / 47.3 µs-ev — inside the author's bands.
- **Window sensitivity:** at w1000/w2500 the regime lock holds (idle-vs-load onset ≤ 240 gs); at w4000 the argmax flips to wave 2. The 1,500-gs window is part of the law's registration, stronger than the author's hazard note implied.

**4. Novelty.** Nothing in docs/HISTORY.md or the nladder page holds the tail-arrivals identity, the load-regime gs anchor, or the fence non-neutrality. 476d's checker bracket named this exact experiment as the gold path; the result reverses 476d's "the tail does not need the stagger" and re-prices 2d26's exit table (coverage bars 0.08–0.21 at 2e5, schedule-bound ebb).

**5. Page.** The author's block was faithful except where it overstated; corrected in place: cost steepening (single draw), exponent disjointness (overlapping at n=2), whole-wave arrivals ≈2.3–2.6 (1e5 idle measures 2.56–2.57), P3b draw-sensitivity, the ambiguous "6–12 big frames (60–200k events)" (their collective load: top-7 sums 62k/155k), a checker bracket, and the run-list grade. Topic stays open: this is the first gold on the wave's exit table specifically; no three-gold agreement on this best yet.

**6. Goal fit.** Board item 1 (bodies 28→1e9) and smoothness: the wave's exit design now knows the stagger's target is the whole arrival wave and that no single exponent composes to 1e9. "Measure before claiming, and never strawman" — the load dimension is now measured on both sides of every constant.

## Small errors found (recorded; none grade-changing)

- The dossier says the fence crest "breached P4's [0.7,1.4]× upper edge exactly": 6,466/4,651 = 1.390 < 1.4 — it did not breach (held_max ≤ 50 is the P4 clause that genuinely failed, at 274).
- RSS 547/1,050 MB are flight-end footprint peaks; `gs_analysis.py` prints the end-"now" values (503/971) — both from the same output line, but a checker regenerating only via the script sees the lower pair.
- Load-2e5 arms ran at 3.2–3.8 GB on an unenforced 2 GB cap (disclosed); counts are memory-insensitive, their ms carry the caveat.

## What the author missed

- The author's own instrument-floor lesson (≥3 flights per rung) was violated at 3e5, and the violation was load-bearing for the disjointness/steepening claim — it died on my first replicate.
- The 1,500-gs argmax window is a registration constant, not a footnote: at w4000 the detector anchors on wave 2; every future cross-rung comparison must pin the window or the "onset" is not the same object.
- The re-mint churn hypothesis for the fence's +39% crest is named but unprobed (a mints counter, one flight).
- One scene, one seed throughout: the gs lock across seeds is unmeasured (0c0f's checker saw seed-2 onset shift in frames); the claim's domain is the burn scene at seed 1 — the dossier says so for the tail, less loudly for the crest.
- Load-1e5 tails are censored (2 of 3 flights end before onset+20k; medians mix censored and full draws); the tail identity is pinned at idle only — disclosed, but the load tail medians (1,137 [199..6,005]) should not be quoted as regime-comparable.
