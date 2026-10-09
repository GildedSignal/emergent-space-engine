Working...
Check complete. `check.md` written to the run folder; nothing else touched (tree back to pristine main, only `lab/results/` untracked, no git commits/pushes).

**Grade: gold.**

**What I verified:**

- **Reproduction** — every deterministic quantity bit-identical: three digests (`06b78c…` bench m400, `557e9f…` kick-bench, `00ac05…` held-out seed 3), patched ≡ unpatched digest, paced ≡ unpaced digest. Timing numbers within noise (gather 3.16–3.18 ms vs 3.18; atom 10.9 vs 10.4 µs; readouts 272 = 272). The patch is pure instrumentation, as claimed.
- **Prediction discipline** — `predictions.md` (22:23:15) written after all tuning runs, before both held-out runs (22:23:34/46). Held-out held: atom in band, gather-largest-part, ≥10 % overflow with zero hitches above 16.7 ms; the readouts/body miss was disclosed by the author.
- **Adversarial** — unseen seed 11 (atom 9.8 µs, share 0.55, held); digest determinism under pacing; and the decisive one: I lifted the `--members 400` clamp (one line) and ran the "unrunnable" extrapolation — **1,501 live bodies → gather p50 14.7 ms ≈ readouts × atom (13.1 ms), first 36 ms hitches, 89 % overflow**. The frame dies exactly where the dossier predicted.
- **Novelty** — partially anticipated (H0210 already recorded "view gather is 83 % of a light frame" pre-cache; H0212's cache fixed the search, and this run shows the atom is now the cost). New: the post-cache quantification, the demonstrated foundation-7 violation at reachable scale, the confirmed linear law, and the paced-on-idle ~4× timing trap (verified from the author's own files: identical digest, load 0.58 vs 2.5).

**Gold clause:** shows a premise wrong — the board's engine-only focus misses that the unbudgeted O(live-bodies) view gather, not the budgeted engine, is the frame's constraint at plane scale — and is adoptable in one step (board entry + pacing discipline; nothing to merge).

**Missed by the author** (in check.md): json+wire are also O(N) so the frame dies *before* gather alone hits 16.7 ms; the 56–78 % gather band should read 53–71 %; the share order can flip at 28 bodies under contention; the atom is load-sensitive (I saw 9.7–16.4 µs); the `-idle` file is misnamed (load 2.4).
