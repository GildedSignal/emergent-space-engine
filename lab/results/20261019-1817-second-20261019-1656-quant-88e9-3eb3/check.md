Grade: silver

**Abstract.** The named experiment flew to its box boundary, honestly: rung B passes all four criteria (regen 1.633/1.591, closures 0.954/0.930; my third seed 7 also passes), onset is confirmed a ~130k gs keep-horizon time on four fresh arms, and the 10⁵ wall is priced at 5.3/9.4 KB per kick of machinery, wall-life 2.30× (regen 2.32×). But my adversarial seed 3 at 5×10⁴ fails both registered ratio bands (stream 1.447 vs [1.73,2.11], slope 1.393 vs [1.70,2.15]): the locals' stream runs +24% over the scene-fixed L, so "holds at both rungs" is seed-1-specific at 5×10⁴; the mint identity itself survives everywhere post-onset. Part of rung C was already on the page (b911: K=10⁵ guard at 38,033 gs). Adoption cost unchanged.

## Reproduction

- regen.sh exit 0 (runner) and my read of its logs: every dossier number reproduces within run jitter ≤1%. Rung B: OFF 2,735/2,866 closure 0.9545; ON 1,675/1,801 closure 0.9301; ratios 1.633/1.591 (dossier 1.632/1.591). Rung A′: registered-window letter FAIL reproduced (closure 0.1576, hist falls 154,874→145,374); post-onset 2,854/3,112/0.9170 and ON 1,570/1,689/0.9295, ratios 1.818/1.842 (dossier 1.814/1.840); checker's window [140k,175k] closure 0.9127 (dossier 0.9126). Rung C: guards at 38,764/90,007 gs (author 38,640/88,856), machinery 5.3/9.4 KB per kick (author 5.3/9.9; kick-count jitter), wall-life 2.32× (author 2.30×). Calibration matches 88e9's OFF digits exactly (hist 61,299/61,945; gt1 275/351/30,061/30,063). Refusals 0, dead 0 on all seven flights and on my four.
- The patch is 88e9's verbatim plus exactly two deltas (verified by diff against the 88e9 branch): a `LADDER_SEED` dial defaulting to the shipped 1, and `kicks=` appended to the probe print reading the shipped `p.u.stats.kicks` (universe.rs:117). Calling the seed dial "print-only" is loose — it is an input dial, default-identical; arms flown without it (calibration, both 1e5 arms, 5×10⁴ seed 1) are on shipped behavior.
- Onset decomposition arithmetic checked: 1e5 OFF 238 base + 205,395×2.1 KB = 669 of 1,494 MB (45%); 3×10⁴ seed 2 ≈ 1,080 of ~1,131 MB (95%). Share-law arithmetic (B, L, 3,242/1,687/1,922; 5,018/1,909/2.629) all correct.

## Predictions

- v1 registered, then an in-file amendment after the first 10⁵ OFF flight refuted its own registration (unflightable), before the other arms. regen overwrote the flight-log mtimes, so the ordering cannot be independently confirmed — but v1 is preserved separately, and the amendment *kills* the author's own registered window rather than rescuing it. Honest on its face.
- Letter outcomes reported honestly: A′3/A′4 FAIL as registered, correction flagged POST-HOC; C2's trip (88.9k) is on the wrong side of the predicted 120–140k band and is reported as "worse than predicted". B1–B4 held; A′1/A′2/A′5 held.

## Attack (my own cases; two outside the author's grid)

1. **3×10⁴, seed 7, both arms, matched [140k,245k]** (third seed — outside the grid): B1 1.769 ∈ [1.50,2.10] ✓; closures 0.960/0.934 ✓; B4 2,437 ✓; B3 stream 1.721 — inside [1.43,1.75] but +8.4% over share 1.587, so the dossier's "nil seed spread on the primitive" (from one seed) is refuted by one more seed.
2. **5×10⁴, seed 3, both arms** (seed≠1 at the top flightable rung — outside the grid, no guard trip, refusals 0, dead 0): the onset mechanism *holds* (registered-window closure 0.211 suppressed; post-onset 0.896/0.906), but **both registered ratio bands FAIL**: stream ratio 1.447 vs [1.73,2.11], slope ratio 1.393 vs [1.70,2.15]; ON stream 2,039 vs share 1,687 (+21%, outside ±10%). Mechanism isolated: the locals are not scene-fixed — quiet-region cuts read L ≈ 1,813–1,832 at seed 3 vs 1,466–1,486 at seed 1 on identical windows (+24%), present in both arms. The mint identity survives (quiet-region closure 0.952). So the share law's ±10% precision at 5×10⁴ is seed-1-specific; the named experiment's success condition ("flight-verified at two rungs beyond tuning") is not met in the seed dimension.
3. **Onset as time constant** (free, from the shipped seed-2 logs): 3×10⁴ pre-onset [20k,105k] closures 0.246/0.331 vs post-onset 0.888–0.955 — the ~130k gs transition holds at the lower rung with a different wave count, confirming the keep-horizon reading against the wave-index reading. My best-verified result of the run.
4. Guard-mismatch note: wall-life 2.30× compares trips under 1,750 (OFF) vs 1,800 (ON) guards; matched guards give ≈2.2× — still well under the stream share 2.63, so the conclusion stands.

Logs: `/tmp/adv/{ap_off_50k_s3,ap_on_50k_s3,b_off_30k_s7,b_on_30k_s7}.log`; commands exactly regen.sh's with `LADDER_SEED=3`/`7`.

## Novelty

- New and confirmed: the onset correction (kills 88e9's and the first checker's wave-index reading; now on 3 seeds × 2 rungs), the ON-arm 10⁵ trip + wall-life 2.30×, the per-kick machinery pricing, and the premise-inversion reading of the 10⁵–10⁹ column. ÷S dead at every rung (1.45–2.36 ≪ 8).
- Already on the page: 10⁵ unflightability at ~38k gs (the b911 block records K=10⁵ guard at gs 38,033, slopes 67–90 MB/1k gs; this run's OFF trip 38,764 re-measures it without citing that), and f80a already showed non-binding memory (channel 2) co-equal with bindings at 3×10⁴. The dossier presents rung C's unflightability as this run's finding — overstates.
- docs/HISTORY.md has no earlier entry for the share law's seed spread or the wall-life ratio; not a repetition of 88e9 (it is the named successor).

## The page

Faithful on the numbers; corrected in place: a bracketed checker note added (seed-3 failure at 5×10⁴, seed-7 B3 margin killing "nil spread", the b911 prior-art line, wall-life guard caveat), and the Runs line's "awaiting grade" replaced with the grade. The f80a/b911 conflict resolution keeps both sides — legitimate per schema. Not three agreeing golds: topic stays open.

## Goal fit

Board items 1 and 4. The run re-prices an adoption expectation before anyone pays for it and kills a wrong reading with a mechanism (PRINCIPLES: "A failed expectation is not automatically a failed method: diagnose which one broke", H0183), and 33 — at 10⁵ the memory that matters is the machinery every kick pays, not the ratchet the cadence divides. Measured on shipped code, orders of magnitude only, honestly bounded.

## The one experiment for gold

A seed ensemble at 5×10⁴ (≥5 seeds, both arms; the ON quiet-region cut already separates L(seed) from B/8 at zero extra cost), re-registered as stream = B + L(seed) with L measured per flight and bands on the belt term and the ratio widened to the measured seed spread. If the ratio holds within the re-registered bands across seeds, the two-rung verification stands and the scaling column's first entry is measured; if it wanders 1.45–1.92 as my two seeds hint, the share law demotes from identity to mean law and the 10⁶–10⁹ rows become estimates — either outcome is gold-grade because it decides the column.

## What the author missed

- The seed axis at the top flightable rung: their own lens note flags "one new point, not an ensemble" at 3×10⁴ but the headline claims 5×10⁴ unconditionally; one flight (seed 3) breaks it.
- "Nil seed spread on the primitive" — refuted by a single additional seed at either rung (+8% at seed 7, +24% locals at seed 3).
- Rung C's unflightability is prior art on this page (b911's 38,033 gs); the new content is the ON trip, wall-life, and per-kick decomposition, and should have been claimed as such.
- The wall-life 2.30× mixes guard thresholds (1,750/1,800); matched guards give ≈2.2×.
- `analysis.py` hardcodes "38640" in the C1 print while the decomposition reads the live guard value — cosmetic, the logs carry the true digits.
