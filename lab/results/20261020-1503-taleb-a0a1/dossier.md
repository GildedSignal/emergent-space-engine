# Dossier: the encounter channel's two O(N) walks — capture on the critical path, answer unanswerable

## Claim

The player's encounter channel is TWO belt-wide O(N) walks, both measured per body across
rungs, and the shipped design has no safe exit for either: **capture** (building the scan)
walks every body of the doll on the player's item — the frame's critical path — at a
constant **0.25–0.30 µs/body** (74–91 ms × 126 walks at 3e5; 28.9 ms at 1e5; the radial
apsidal filter bails to ALL on the belt, `radial.rs` N/4+64), and **answer** costs
**4.2–4.4 µs/body, 97% of it the cartesian read** (10.77 of 11.07 ms on the largest answered
scan), which can never fit a 12 ms frame budget — so every belt-wide scan (cand = 299,715
at 3e5) either piles toward the 2048 backlog cap, where the player's next item pays one
full answer uninterruptibly (9ed1's 1.2 s class; ~72 min at 1e9), or, fenced by the TTL
(ca63/9ed1's memory gate), is **silently dropped unanswered** — the fence does not delay
the channel, it deletes it. The uncarrried exact bound (`encounter.rs` L59: skips 70–86%,
"not carried since the scans are already off the critical path") attacks exactly the
measured dominant term on both walks, and its skip ceiling on real belt answers is
**99.8%** (2607/2612) — the premise for not carrying it is now measured false twice.

## Bottleneck

Board focus 1 (bodies: 28 → 10⁹) × focus 2 (encounter work). The two walks are the player's
own instruments at belt scale: at 1e9 capture ≈ 0.29 µs × 1e9 ≈ **290 s per player item on
the critical path**, answer ≈ 4.3 µs × 1e9 ≈ **72 min in one uninterruptible lump**. What it
deletes: the whole per-body walk (the bound turns both into ~0.2% of the doll), or the
channel itself (the unwired Binet cone tiers). The allocator cannot schedule its way out:
the guard's threshold is bounded by 2× the frame budget (≤ 24 ms) — 3,000× below the lump.

## Evidence (each flight ≤ 60 s wall, build ~10 s; commands in regen.sh)

Arms (shipped burn scene, `nladder` example, rtf 1300, 12 ms budget, unstaggered — no
stagger in this patch, disclosed): **a1** = 3e5 seed 1, TTL-fenced (ES_SCAN_TTL_S=16):
max frame 2,647 ms = 52,079 events × 51 µs — the UNSTAGGERED kick comb (9ed1's off-arm,
2,430 ms; composes, does not compete). CAP lines: 126 walks with `radial=ALL:300076`,
ns 74–91 M (top 91.3 ms), cand 299,715. ANS lines: 1,805 answers, largest 11.07 ms /
2,612 cand, read_ns 10.77 ms (97.3%), skip_dom 2607 (99.8%), enc 3; **no cand=299,715
scan was ever answered** (aged out at TTL). **b1** = 1e5 seed 1, unfenced: RSS peak
1,957 MB (P3 held; 9ed1 1,887), same 126 ALL captures (top 28.9 ms = 0.29 µs/body; P4
held: fence-independent), 3,107 captures totalling 2,986 ms of frame time, largest answer
8.0 ms / 1,804 cand = 4.4 µs/body — the 892 ms worst frame is again the comb (17,171
events), NOT an answer: P1/P2 failed on this draw (kill bar 3 seeds not reached — the
1e9-class single-answer frame is 9ed1's attribution on longer 8-era flights; my 45 s draws
cannot confirm which drain path fired their bite, and this stays open below).

**The guard is structurally closed at these rungs (both draws):** `drain_scans` admits an
answer only when `room ≥ 2·max(scan_ns, 750µs)`; room ≤ the 12 ms budget, and scan_ns
decays only inside answered scans — after any ~8–11 ms answer the threshold (16–22 ms)
exceeds every future room, so nothing further is ever admitted; the queue only grows
(held_max 1,399/2,048 in 45 s; 1,388 at 3e5). The two exits are the backlog cap (one full
answer inside the player's item — the freeze class) and the TTL (silent deletion). The
"decaying estimator guards a heavy-tailed cost" structure is the same one the frame's
item classes use (`item_ns`, 1/64 decay) — there it is bounded by the budget; here the
tail it guards is 300× the budget.

## Predictions

predictions.md was written after a1 and before b1 (time pressure disclosed; a1 is the
anatomy anchor, b1 the held-out draw). Score: P1, P2 FAILED on draw 1 of 3 (no single-answer
≥ 300 ms frame at 1e5 in 45 s — the comb owns the worst frame and the big scans never
answer in-window); P3 HELD (1,957 MB); P4 HELD (126 ALL captures, 0.29 µs/body,
fence-independent). The P1 failure sharpens the mechanism rather than killing it: the
lump requires the backlog cap (8-era flights) or a settle/flush call — neither occurs in a
45 s draw, which is itself the finding: **the answer channel's work is unpayable inside
the frame budget at every rung measured, by construction.**

## What would make it wrong

If the radial filter's bail-out is an artifact of the burn scene's window (a coasting or
in-system player whose window the index serves: CAP lines with `radial=idx:` and cand ≤ 40
exist in both draws — the filter works when the window is narrow), the capture walk is
belt-geometry-specific. The answer-side law (4.3 µs/body, read-dominated, 99.8% skip) is
scene-independent arithmetic: candidates × read cost. The 1e9 numbers are [INFERENCE]
(linear extrapolation of measured per-body constants, the same convention as 9ed1's
checker). Cost of adopting the bound: a per-body remembered-position map in the finder
(the design in dropped commit 72b71c56's doc), one float test per candidate; it was
bit-for-bit with its verify control when last carried.

## Fit with PRINCIPLES

Principle 1 ("the cheapest compute is compute not done") and 19 ("a fix signals the wrong
representation"): the bound deletes 99.8% of the walk instead of scheduling it; principle
12 (the allocator): a lump 300× the budget is not schedulable, it is deletable; principle
34 (oracles are guards): the exact predicate stays, the bound only skips what cannot hit.

## The lens (Taleb)

What this lens may have missed: the stagger arm (8365's gate) is absent from my patch, so
the comb dominates my worst frames and I could not isolate the single-answer frame 9ed1
attributed — the freeze's path attribution (backlog vs settle vs decay) rests on code
reading plus their 8-era record, not on a fresh observation. The convexity reading (guard
blind after quiet) is the same failure shape as the allocator-ratchet fires; the cure in
both cases is deletion of the lump, not a smarter estimator.
