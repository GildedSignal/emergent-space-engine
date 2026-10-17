# Predictions (written before the decisive arms: seeds and the BELT_SPLIT flight)

Context: de7b's claim is that the boundary comb is welded to the kick's own step, and that
`BELT_SPLIT` (98cb) transfers because it coarsens `Δs` through `ext::constants`. The first
checker named two gaps: the transfer was inferred from 98cb's 8.000× first-kick anchor
alone, and one seed only. Arm 7 seed 1 was rerun first as a record check (it matched de7b's
`arm7.txt` to the digit before this file was written; no parameter was tuned on it — the
scan points below come from published h values, not from any run here).

## S1. Shipped lever, new seeds (arm 7, seeds 2 and 3; N = 10⁴, scan 20k, end 60k)

The welding is mechanistic (one `full`, two items), so a new genesis draw must not change
the structure, only the per-body h draws:

1. h p50 within ±2% of 14,071 game-s at both seeds (the per-body spread at seed 1 is
   p01 13,375 / p99 14,473, so the p50 may wander a few ticks).
2. Welded pairs ≥ 99.9% of the 9,700 belt bodies at scan 20,000; B/2h, (K−B)/h,
   interval/2h all 1.0000 ± 0.0005; (B mod iv)/iv ≤ 0.0005.
3. Fired events per body p50 = 4 exactly; dead 0.

## S2. The direct split flight (BELT_SPLIT=1, the checker's named experiment)

Setup: 98cb's actual patch applied (their `plan_clock` wiring: bulk bodies get
`step_log2 − 3` = an effective lever of 4, 8× coarser than shipped), everything else off
(`IMPACT_GUESS=0`, no `STAGGER_GENESIS`). N = 10⁴, rtf 12,000 (the flight must cover
385k game-s inside the instrument's 55-s guard), scan 160,000 (between the expected kick
crest ~112,574 and boundary crest ~225,148), end 385,000 (past the kick at 3h ≈ 337,722).

Predictions, falsifiable in order of importance:

4. **The transfer itself:** the genesis first-kick distribution becomes two classes —
   split-class bodies at h ≈ 112,570 ± 60 (8× the shipped h; 98cb's anchor was 112,574 at
   their scene) and shipped-class bodies at h ≈ 14,071 (belt members inside 4 Hill radii of
   a source's band). I predict the split class is the majority: h≥60k ≥ 90% of the 9,700
   (98cb saw 100% of their 2,700; this scene's belt is 3.6× larger, so I allow an inner-edge
   minority).
5. **The boundary rode along:** at scan 160,000 every split-class body holds the welded pair
   {Boundary at 2h, Kick at 3h} with the identities measured on its OWN h: B/2h = 1.0000,
   (K−B)/h = 1.0000, interval/2h = 1.0000 (± 0.0005), (B mod iv)/iv ≤ 0.0005 — i.e. the
   boundary comb sits at 2h ≈ 225,148, 8× later than shipped, exactly at the stretched
   kick's midpoint. **Falsifier (the dead pinned branch):** B/2h ≈ 0.25 (boundary still at
   the shipped 2×14,071 against a stretched h), or boundaries outnumbering kicks ~8:1 in
   the window.
6. Fired events per body in the scan→end window (160k–385k = one split interval): split
   class p50 = 2 (one boundary at 2h + one kick at 3h); shipped class p50 = 16 (8 shipped
   intervals). The mixture in the p01/p50/p99 triplet should show it.
7. dead 0, ok = true (flight completes inside the guard).

## S3. Controls

8. Arm 6 and arm 8 (seed 1) rerun as the lever control must reproduce de7b's table to the
   digit (h p50 28,141 / 7,035; pairs 9,700 / 9,621+79; 2 / 8 events per body).
9. If S2.5 fails in the falsifier's direction, the claim's transfer clause is refuted and
   the 10⁹ ledger's pinned-boundary branch (the ~15.7-M1-core floor) returns: that would be
   a clean kill of the transfer, reported as such.
