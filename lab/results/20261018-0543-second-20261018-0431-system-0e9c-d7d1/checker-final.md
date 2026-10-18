Working...
**Grade: silver** — written to `check.md`, with the author's `wiki/scan-queue.md` corrected in place where it overstated.

**What I did:**

1. **Reproduced from scratch**: applied `work/patch.diff` to the `base` commit, ran `regen.sh` end to end (exit 0). Every *structural* number reproduces bit-exactly across three independent executions (author, runner, mine): 13×4 frozen digests identical in all three arms, off-arm = shipped record on the 11 shared cases, seam census counters digit-for-digit (`captures=9280 bails=2920 fb_walk=5374600 …`), in-band probe 100,028→99,715 walked with `pass` identical, formation `e9043656…` digest identical, 551.25 walked/capture vs ~9,491, candidates ×2.56 at the seam.

2. **Eight adversarial cases, all outside the author's range**: K=500 formation (digest identical, 851.25 walked — exactly K-scaled), 3× flight with 418 encounters (identical), a **BAIL-only arm** the author never flew (candidate total = off's *exactly*, 157,290 — the cleanest proof the threshold, not the bail, moves candidates), belt at **10⁵** (digest identical — but the pristine arm bails 0/192 and walks 394/capture), in-band at seed 7 and 3×10⁵ (doll-served, `pass` identical).

3. **Three findings cap it at silver**:
   - The pre-registered P4 (candidate-total invariance) failed by its own kill criterion — honestly reported, and my BAIL-only arm confirms the diagnosis, but by lab precedent a failed held-out prediction is not gold.
   - The dossier's wall numbers don't regenerate: its own `regen.sh` prints capture 117→28 ms and p99 12.1→11.8 (unchanged) against the dossier's "350.9→33.7 (10.4×)" and "p99 36.3→12.8" — three reproductions scatter 3×; the p99 effect was machine load.
   - The "at a 10⁹ belt ~10⁹ reads against 551" sentence is overstated: the off arm's 10⁴ bails are **bin-span** bails (threshold-independent, incidental to the locals' redraw), and at a 10⁵ belt they vanish — the pristine walk is bail-gated, not belt-sized. What holds everywhere is the composed arm's doll bound (551.25 at both 10⁴ and 10⁵).

Tree left pristine (patch reverted); only `check.md` and the wiki corrections added. The named gold experiment: re-fly the formation pair with the regen's own wall numbers, pre-register the candidate-total movement, and add the bail-regime arm (10⁵ belt) so the 10⁹ sentence states its condition.
