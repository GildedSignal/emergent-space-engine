# Predictions — 20261006-2240-b-belt-wire-a733

Written before the decisive run: `behave --law space --gates B18b` on the frozen RUNS
(three 2^20, two 2^23), then `--gates B18`. Tuned on: nothing from this set. What I did
run before writing this: one thorough judged 2^20 run at seed 20261008 through
`belt::judge_findings` (it passed), a 2^21 tail pre-check against the exact law
(`examples/belt_tail_check.rs`, bottom z -0.33, top z -0.77), and the unit tests.
The frozen seeds and both 2^23 sizes are held out.

1. **B18b passes every criterion on all five frozen runs.** Predicted worst statistics:
   chi2 |z| < 3 (limit 4.5), serial |z| < 4 (limit 5), per-column KS < 0.5 of critical,
   tail count |z| < 3 per run and pooled (limit 4.5), conditional tail mean |z| < 3 per run
   and pooled, other-columns KS < 0.9 of critical. The one systematic I can bound: the
   12-bit central quantization of e contributes at most ~1.2e-4 of KS distance against a
   critical value of 1.2e-3 at 2^23 (10% of budget).
2. **Bytes.** Birth store ≤ 32 B (parameters only: n, seed, spec; keys derived from the seed),
   declared info = the store at birth, ≤ 64 B cap. The store does not grow with n beyond the
   varint of n (≤ 1 byte between 2^20 and 2^23; limit 16). Bytes at 1e9: same ~31 B.
3. **Scars after 12 epochs at 1e-2.** m ≈ 11.4% of n distinct scarred; per-scar cost
   predicted ~10 B (varint ordinal gap ~1 B + four zigzag varint deltas ~9 B) against the
   window [0.5·floor, 2·floor + 2] ≈ [3.4, 15.6] B at floor ≈ 6.8 B (ordinal bits + 50-bit
   kick). Every scarred ordinal returns its scar; restore re-serializes identically.
4. **B18 (the memory ladder) for `space` is unchanged: FAIL, "not answered"** — it speaks to
   `bytes_per_body`/MemoryScene, a different interface this run does not touch. Before and
   after must read the same failure.
5. **Nothing else regresses**: the space law only gains two methods; shipmem's Prog loses
   Copy (Belt holds its derived table behind an Arc), and its existing tests pass. The
   workspace suite stays green.
6. **What would make it wrong** (named in advance): a long-range serial correlation in the
   mix() counter stream at lag 2^16 that the lab's 2^23 evidence did not cover; a pooled
   conditional-tail bias from the 64-cells-per-octave midpoint convention larger than my
   ~0.01σ estimate; the e-bottom tail failing reach at 2^23 (my deepest 2^21 draw was 90596
   against the required ~1.65e5 reach: margin ~1.8×, thin but real); scar per-body cost
   drifting above 15.6 B if the kick deltas varint fatter than measured (measured ~9.6 B on
   the lab's kick widths: not expected to move).
