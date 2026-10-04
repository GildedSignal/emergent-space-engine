Working...
Check complete: `lab/results/20261004-2311-quant-fde3/check.md` written — **Grade: silver**, abstract at 118 words, nothing else touched in the run folder, no git operations.

**What I did**

1. **Reproduced** from the dossier's exact command in a clean `/tmp` tree (~12 s, load 0.2–0.4, same EPYC 7763): i32 sorted 0.96 ns/kick at 46 GB/s ≈ memcpy ceiling (author 0.98/45.1); f64/i32 = 1.88 vs author's 1.94 (byte ratio 2.0); wake 6.16 ns (confirms the 6–11× range across runs); checksums **bit-identical**; cell touch rates identical (deterministic seeded stream).
2. **Found the control bug (decisive):** `ustream >> F` is an arithmetic shift, so the `always` control floors every negative sub-quantum step to a full −1 quantum — measured drift −4095 to −6144 quanta per 8192 steps, touch rate ~50% at every scale. The "kill region −22% at 0.75q" is an artifact of that rounding mode; against the PRINCIPLES #6-compliant exact every-epoch control (my probe), the accumulator deletes **31.3/81.3/94.8%** and wins everywhere — the mechanism is stronger than reported, and the reported boundary doesn't exist.
3. **Broke the capacity bound:** batching 4 kicks/body/pass halves the cost to 0.816 ns/kick (20 B/kick; identical at 16 Mi bodies, so no L3 artifact) — "≥ 21 s/orbit" is really 6–21 s depending on batching. The infeasibility conclusion survives; the bound doesn't.
4. **Independently verified** the exactness identity on adversarial all-negative/constant streams (sound floor-mod arithmetic), and confirmed novelty (HANDOFF:107 lists the bandwidth probe as pending; no HISTORY entry; flagged the uncited "largest-remainder splits" lead).

Silver, not gold: the core bandwidth table and exactness are adoptable today, but one of the two headline mechanisms rests on a broken control and the capacity lower bound is unsound — both fixed by one ~15-minute rerun with three controls plus a batched-kick row, which is the named experiment in the check.
