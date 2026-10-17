Working...
Check complete. **`Grade: gold`** written to `lab/results/20261017-0839-dynamics-b966/check.md`.

**What I did:**

- **Reproduced** (applied `work/patch.diff` myself, rebuilt, reran): chunked batch crashes 3/3 in the runner's regen and 1/1 in my battery with a **fresh scene seed** (10/10 across all sessions); single-call batch, quiet, and rate 300 never crash (0/2, 0/8, 0/12); frames-mode crash reproduced in **every** session — author's six documented panics, regen's nA (768→816), my h3 at n=240 rate 600 (800→832, gap 32 = 2 strides).
- **Predictions held:** `predictions.md` predates the first `drift` output by 5 s (mtime order); P1–P5 all held in shape, with the author's one honest miss disclosed.
- **Mechanism verified in shipped source:** `alloc.rs:1451` is the quoted assert; `certify` returns stride starts; `sh.publish` runs after every worker commit; `run_frames` is the frame-thread harness.
- **Adversarial:** rate 800 (untested band interior) 0/3; `ahead` 0.05/1.0 s 0/2 each (cap question stays open); fresh-seed frames 0/3. I also solved the folder's `r300*` anomaly: `r1200b` survived at 612 chronons/s, proving those files ran at the default rate 600 (positional-arg slip) — so "rate 300 never crashes" stands, but the author window's 14-draw count is only partially reconstructable.
- **The one finding against the headline:** the 11/19 incidence at rate 600 does **not** regenerate — two fresh windows gave 0/10 at n=120 (only the n=240 arm crashed, 1/3 each). Reachability, not incidence, is the reproducible deliverable; gold rests on that, plus the premise it kills (the crash is not a batch-driver artifact — the frame harness is exposed, PRINCIPLES §25/§34).

**Page corrected in place** where it overstated: incidence folded across four windows (11/29 at n=120, 2/9 at n=240, rate 300 0/12, chunked 10/10), gap range fixed (16–48 frames, 75 chunked), and "the harness the player runs" softened to "the frame-thread loop built as the player's path; no player binary wires it yet". Tree restored (scratch example and patch removed; only `lab/results/` untracked, as at start; no git commands run).
