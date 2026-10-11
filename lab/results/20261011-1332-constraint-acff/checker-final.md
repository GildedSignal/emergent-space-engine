Working...
Check complete. `lab/results/20261011-1332-constraint-acff/check.md` written — **Grade: silver**. Tree restored (slice constant `1 << 18`, patch reverted; only `lab/results/` untracked; no commits).

**What I did:** applied `work/patch.diff` to clean `a838a284`, rebuilt, and reran every decisive command plus adversarial cases of my own — 10 bench runs, one kick-bench, three slice rebuilds (2^17 at m48 **and** m400, 2^16, odd 2^17+1), and a threads-4 run on the unpatched binary.

**Verdict basis:**

- **Reproduced exactly:** every digest — m48 `41343a14…`, m400 `3db02d3d…`, rtf1000 `b35b3451…`, budget-invariance (0.5 ms ≡ 5 ms), thread-invariance, slice-invariance, kick-bench `eccc7f5a…` with memo exact hit 0.0 / quantized 95.47%. All structural claims reproduce (gather 62–70% of frame; single fleet items 5.4–6.3 ms > 5 ms budget; worst-5% in thirds; player per-item 389→1754 µs growing with N while ship per-item falls; player per-item flat in rtf — P5 independently confirmed).
- **Adversarial results strengthen it:** slice invariance holds at 428 bodies, at 2^16, and at an odd non-dyadic quantum — identical bits, and at 2^16 identical paced event counts. The unpatched-binary t4 run proves the trace patch doesn't touch the law.
- **Why not gold:** the held-out predictions did not hold (P1/P2/P4 wrong, P3 half — honestly reported, and P2's per-frame vs per-game-second correction is genuinely useful), and the run's strongest certificate (slice invariance) was not pre-registered — `run.log` is empty, so the claimed "written into the run log before the slice run" is unverifiable. It's also a diagnosis run: order-1 frame gain, no 10× move or deletion delivered.
- **Notable caveats recorded:** absolute timings swing 3–4× with machine state (author's quiet runs were *slower* — idle-host clock scaling; the "2.5%→22%" overflow headline is contention-dependent), 8.5 µs/body is the marginal slope not the average (15 µs/body at 428), and the "split handouts, chunked player work" half of the exploit claim is unmeasured — the player's 8 ms step stays an unbounded item.
- **Gold path:** wire deadline-sized slices and split handouts, sweep, and show overflow ≈ 0 with identical digests — one step, now de-risked by this check.
