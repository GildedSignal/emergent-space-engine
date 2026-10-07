Working...
Check complete. `check.md` written with grade **silver**.

**What I did (45-min window):**

1. **Reproduced everything from the shipped patch** on a clean tree (built offline, `CARGO_TARGET_DIR` shared at `/home/glmlab/lab-target-0`). Every counter line regenerates **bit-for-bit**: belt 1e-6 (1767 vs 2898, 0/0 of 63), the stale-record belt 1e-4 (4809 vs 2827, 0/0 of 73), belt 1e-8, orb=64 (1540 vs 2703, 0/0 of 257), ring 1e-6 (28650 vs 47600 — three identical runs, counters are process-deterministic), fleet 1e-6 (17068 vs 61452), seed 777, ε=1e-2, and the 20-minute 256-orbit inversion (27007 vs 2690, evals_q 26141 exact, wk_p95 30.8 µs).

2. **Ran the controls:** tests 7/7; killing terms 3b+6 makes `exact_at_kick_eps_1e6/1e4` fail exactly as claimed (1e-8 still passes); a pad=s probe gives 2202 vs 1767 evals/kick, confirming correction 1's direction and size.

3. **Adversarial cases of my own, all exact (0/0):** held-out seed 4242 (1.73× cut), κ=2.0 — harsher than any author case — cuts 4.4× (more kicks amortize the scan better), and fleet 1e-4, the author's unfinished exactness case, runs in 50 s at 0/0 of 1233 with parity economics — the record's only hole closes favourably.

4. **Predictions audit:** pre-registered before the work outputs; exactness predictions held; the long-horizon economics prediction was refuted (10× above always at 256 orbits, not 8× below), disclosed honestly with the pre-registered falsifier — which blocks gold, since gold requires held-out predictions to hold. Gain is 1.6–3.6× total evals (3.0–3.7× wall, p95/p99 tails down 3–4×), below the 10× bar.

5. **One artifact, mine:** my mid-batch rebuild raced one adversarial rerun (ring showed 30601); clean reruns reproduced the stored 28650 exactly — noted in check.md.

6. **Named the gold experiment:** implement and run the derived max-age refresh plus a cheaper initial scan; require no losing horizon, ≥5–10× on the belt, `belt10k` completed. Also flagged: the "~322→~210 per setup" narrative doesn't reconcile with shipped counters (~157→~126 measured), and the crossover age between 64 and 256 orbits is unmeasured.

Tree restored to clean (`git apply -R`), nothing else in the run folder touched, no commits or pushes.
