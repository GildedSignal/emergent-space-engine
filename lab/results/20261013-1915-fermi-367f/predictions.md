# Predictions (written before the ladder runs; smoke test at members 48 only)

Smoke anchors (members 48, rtf 100, 4 s, seed 1): hand-out 1,316 µs/promotion
(bind 820, replan 471; 27/43 need the coarser re-fit, 614 µs each); kick item 200 µs;
player item 723 µs; rekey 33.9 µs/frame at 71 bodies (~0.48 µs/body);
leavers 2.2×10⁻³ per member per game-s; events ≈ 0.041 per member per game-s (battle regime).

Ladder: members {48, 400, 1500, 4000}, rtf 100 and rtf 1, paced 8 s (4 s at 4000), seed 1.

1. **rtf 100 (the sweep's pace): the event stream breaks first, ∝ N.**
   Event duty ≈ 0.041 events/member/game-s × ~150 µs ⇒ engine demand ≈ 0.6 µs/member/game-s
   ⇒ at rtf 100 that is ~62 µs/member per wall second. The 5 ms engine budget caps at
   ~80 members/frame worth of events; prediction: **rtf median collapses below 90 between
   members 400 and 1500**, engine p50 crosses 5 ms in the same interval, and `ship`
   items (kicks + promoted leavers) dominate `engine_cost_by_kind` at the top rung.
2. **rtf 1 (quiet): the every-frame walk tier is linear and breaks an order later.**
   rekey+requeue+take_due ≈ 0.3–0.7 µs/live body/frame ⇒ engine p50 crosses 5 ms at
   **~8–15×10³ live bodies**; below that the paced run stays smooth (no 16.7 ms hitches
   from compute).
3. **Memory.** Construction RSS ≈ 1–3 kB/member (compact fleet side); end-of-run RSS
   grows with leavers at ~5–20 kB per promoted body (BodyRec 448 B + shape + history),
   never demoted.
4. **The promotion is flat in N** (per-item cost): HANDOUT/call stays 1.0–1.5 ms at every
   rung; H_BIND 0.6–0.9 ms with the coarser re-fit firing on most handouts. If instead it
   grows with N, the promotion carries an O(N) rider (catalogue/scan) — that would be a
   finding, not a pass.
5. **Held-out: seed 3** at members 400 and 1500 (rtf 100): event rate and rtf median
   within 3× of seed 1; handout µs within 2×.
6. **Kill criterion for my premise:** if events/s at members 4000 is sublinear in N
   (< 3× the members-400 rate), the "battle events scale with members" premise is wrong
   and the break order must be re-derived.

Not measured here (disclosed): the M1 (this is a shared Linux/x86 box, orders of
magnitude only); demotion (no shipped path — the promotion is sticky by construction).
