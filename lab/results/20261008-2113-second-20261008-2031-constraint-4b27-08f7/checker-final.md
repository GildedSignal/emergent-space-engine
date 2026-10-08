Working...
Check complete. `check.md` written to the run folder; tree restored to pristine (`?? lab/results/` only).

**Grade: silver.**

What I did and found:

1. **Reproduction** — applied `work/patch.diff` to a clean tree, built the profile example, ran all five held-out cases with the dossier's commands. Bit-for-bit: identical max_dir/max_rel_ls/max_rel_shift, matched counts (2764/899/1368/2929/3056), worst-offender strings; timings differ only by load noise. The instrument's control is sound (gated cache vs cold exact `gather()` on the same state, same binary).
2. **Pre-registration** — mtimes confirm `predictions.md` (21:21:54) precedes every decisive output (21:24:28+). All seven predictions held; no kill criterion fired; the tuning-set discrepancy is disclosed.
3. **Attack (6 own cases)** — seeds 4–5, rtf 400×5400 (worst offender moves to a ship, so not Home-specific), rtf 1×5400, members 96/12. Worst error 6.6e-5 = 0.66× the quantum; the old 1.675e-4 leak is gone everywhere.
4. **Digest** — built pristine vs patched xtask binaries; bit-identical digests at seed 1 (`41343a14…`, matching the author) **and at fresh seed 2** (`798c0d9a…`), which the author never ran.
5. **Tests** — exactly the two frozen cache-purity tests fail, everything else green, as disclosed.

Why silver, not gold: the paced-frame gain is machine-state dependent — my quieter matched-state legs give **1.62–1.67×**, below the dossier's 2.4× and its own 2–4× band (the gated gather itself reproduces exactly at 0.21–0.22 ms; it's the baseline that swings 0.73–1.20 ms with load). No component is deleted (the exact solve stays for cold arcs), and adoption waits on the integrator's one-way decision to relax the 20261003 cache-purity contract. The one experiment to gold: freeze that contract and show the p99/hitch side on the M1.

Named misses: the 2.4× figure is the favorable end and should read 1.6–2.4×; the engine-p50 "same-state" control is itself load-sensitive (0.081 vs 0.124 ms on my legs) and shouldn't be quoted as evidence; "four interleaved legs" — only two are saved; the bound is only exercised to 0.66× tol (a tightening probe at 1e-5 would show the mechanism bounds rather than sits inside today's number); nothing on record runs past 5400 frames.
