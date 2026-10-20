Grade: silver

**Abstract.** Both O(N) walks of the player's encounter channel are typed per body on shipped code: capture walks the whole doll on the player's item (0.24–0.31 µs/body at 3e3–3e5; radial bail N/4+64 — encounter.rs's "scans already off the critical path" premise is false), and the answer costs 4.3–4.5 µs/body, 97% the per-candidate read, with the uncarried bound's skip ceiling 99.8–100% (my 3e3 arm measured a full-doll answer: skip 2715/2715). The drain guard locks after any answer > 6 ms ≈ 1.4k candidates — at every belt rung ≥ 3e3 — so belt-wide scans exit only via the 2048 cap (one uninterruptible lump, ~72 min [INFERENCE] at 1e9) or deletion. Adoption: carry the bound (ce694696/72b71c56) — named, not flown.

## Reproduction

Runner's regen exit 0; I re-analyzed both flights independently. Every dossier number regenerates within draw noise: a1 125 ALL walks (author 126), top 91.7 ms (91.3), top ALL cand 299,717 (299,715), max frame 2,650 ms/52,840 events (2,647/52,079), top answer 11.22 ms/2,612 cand, read 97.35%, skip 2607/2612, max answered cand 2,612 (belt-wide scan never answered); b1 126 ALL walks top 28.9 ms = 0.289 µs/body, 3,119 captures 3,040 ms, top answer 8.10 ms/1,804 = 4.49 µs/body read 97.2%, RSS 1,957 MB, held_max 1,375. Code anchors verified verbatim: `SCAN_BACKLOG=2048` (universe.rs:79), admission `room < 2·max(scan_ns, 750µs)` (:1190), 1/64 decay inside answered scans only (:1205), capture inside the player's item (:772→1163), `radial.rs:254` bail `> bodies/4 + 64`, `encounter.rs:58-60` quoted correctly; commits ce694696 and 72b71c56 exist.

## Predictions

predictions.md written after the anatomy draw a1 (disclosed), before b1. P3/P4 held. P1/P2 failed on draw 1 of the 3-seed kill bar and the author stopped there. I completed the bar: seed 2 unfenced 1e5 (draw 2 — no ≥300 ms single-answer frame; worst 854 ms = 17,186-event comb; 86 ALL walks 0.242 µs/body; top answer 4.39 µs/body skip 99.9%; max answered 1,761 ≪ 99,715 captured; held_max 1,517) and the 3e3 regime. The kill bar's letter (no single-answer frame) is confirmed; the author's sharpened reading — the channel locks rather than lumps — is what actually happens: b1's last answer lands 28.6% into the flight, immediately after the 8.1 ms answer, and none of the 246 later captures is ever answered.

## Adversarial arms (three outside the author's grid)

1. **3e3, unfenced (below the grid):** the filter still bails (215 ALL walks, 0.242 µs/body — the capture constant holds two decades down), and a full-doll belt-wide answer finally ran: 12.2 ms, cand 2,715, read 97%, **skip 100.0% (2715/2715)**, 4.50 µs/body. This validates the run's central extrapolation on the belt-wide object itself — the 99.8% was measured only on the largest *answered sub-window* before. It also pins the lock-in threshold: one answer > 6 ms (≈1.4k candidates) closes the guard — held_max 1,390 even at 3e3. The lock-in is not a big-N artifact; it is structural at every belt rung.
2. **Coast 1e5 (the scene the author did not fly):** zero ALL captures — all 3,029 captures idx-served (windows 5–208), held_max 181, channel healthy, top answer 1.25 ms skip 99.4%. The bail is the in-belt burn regime, exactly as the dossier's "what would make it wrong" names. The claim's domain is the shipped burn scene; the page now says so.
3. **Seed 2 (above): kill-bar draw 2.**

## Novelty (against the wiki and HISTORY)

The two headline O(N) facts are partly on the record: d7d1 (scan-queue) measured the bail walking the doll (99,715 of 100,028 at 1e5 in-band) and the seam's candidate flip; 1250 (scan-queue od 1/4) found the max-gated latch holding max above room/2 — the "latch's escape" is an open direction there; 9ed1's checker priced the answer bill 4.2–4.4 µs/body across rungs. New and real here: the per-body constants across rungs (0.24–0.31 capture, 4.3–4.5 answer, both now confirmed 3e3–3e5), the critical-path placement that falsifies encounter.rs's stated premise, the answer anatomy (97% the read), the skip ceiling raised 70–86% → 99.8% (→100% on my full-doll arm), the guard closure quantified at belt scale with the timeline evidence, and the fence measured as total channel deletion. The dossier presents the lock-in without citing 1250/d7d1; the page now carries the citations.

## Why silver, not gold

The premise corrections are measured and reproduce, but (a) the deletion lever — carrying the bound — is named, not flown ("bit-for-bit with its verify control when last carried" is a prior commit's record, not this run's); (b) P1/P2 failed on their letter and the kill bar was left at draw 1 of 3 (I completed it, but that is the checker's work); (c) the a1 3e5 flight peaked **5,101 MB, over the 2 GB runner cap, undisclosed** (b1's RSS is reported; a1's is not) — the same disclosure class 0a46's checker flagged; (d) the core O(N) structure extends d7d1/1250/9ed1 without citing them.

**The one experiment that would make it gold:** carry the uncarried bound (ce694696's design, the per-body remembered-position map of dropped 72b71c56) in front of the predicate on the shipped tree and measure both walks at 1e5–3e5 with digest identity — the run's own "what it deletes" is exactly that experiment, and everything here says it deletes ~99.8% of the dominant term on both walks.

## What the author missed

- The lock-in threshold is a *scale-free* law (one answer > 6 ms ≈ 1.4k candidates), so the channel is closed at every belt rung ≥ ~3e3 — stronger and simpler than "at these rungs"; a 3e3 flight would have shown it directly, and would have measured the full-doll skip (100%) the dossier instead infers.
- "97% the cartesian read" over-labels: the instrumented `read_ns` span includes the integer conversion (`integers`, `fixed`), not the read alone. The conclusion (per-candidate read-path dominates; the bound deletes it) is unaffected.
- The idx windows are not "cand ≤ 40" when the filter works: they reach 33,925 (a1) and 11,191 (b1) — answers of 47–146 ms, also unpayable, so the unpayable-answer finding is broader than the ALL bail (those scans were also never answered).
- Coast bounds the claim's domain and was one 25 s flight away.
- The 1e9 extrapolations inherit 9ed1's checker convention but the dossier does not re-say that the 1.2 s bite itself (backlog vs settle path) remains unobserved — it does say this; kept open correctly.

## Fit

Board focus 1 × 2 (bodies 28 → 10⁹; encounter work at 10⁹). PRINCIPLES 1 ("the cheapest compute is compute not done") and 19 ("a fix signals the wrong representation"): the certificate (apsidal radius) is the wrong water for a player inside the belt; distance memory deletes what it cannot prune. Principle 12: a lump 300× the budget is deletable, not schedulable. Principle 34: the exact predicate stays; the bound only skips what cannot hit. Respected.

## Record

My arms' raw outputs are in `work/` (c2_1e5_s2, c3_3e3_s1, c4_1e5_coast). The tree was restored (`git checkout -- crates/`) after the arms; nothing committed or pushed.
