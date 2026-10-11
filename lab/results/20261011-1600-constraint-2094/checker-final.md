Working...
Check complete. **Grade: silver** — written to `lab/results/20261011-1600-constraint-2094/check.md`.

**What reproduced:**
- `gather_scaling` (patch applied, clean tree): 15.45 vs author's 15.41 µs/emitter at 100k emitters, 1.98 readouts both, dead linear over three decades.
- Baseline bench: gather 69.5% share both runs; engine 17.5% behind its 5 ms budget.
- Gate-artifact claim verified: plane law answers None outside B12–B14; G1–G6 pass under `--law space`; B12/B13/B14 match HANDOFF's known state.

**What broke (the silver, not gold):**
- The "scene saturates at 428 bodies — the collision frontier sets the hand-out rate" finding is **false**: `--members` is hard-clamped to `clamp(4, 400)` in xtask (line 32, since the plane's first flight). m480 and m4800 carry **identical digests** — the two held-out runs were one configuration run twice, and a scene mechanism was invented for a CLI clamp.
- My adversarial run (clamp raised, one line, `--members 4800 --seconds 10`): **3744 bodies and climbing, gather still 60.7% of a collapsed 51 ms frame, player item 24.5 ms — the author's prediction 2 actually held at true N**; the clamp cost them their own strongest confirmation.

**The gold experiment:** rerun the sweep with the clamp raised and report the corrected finding — every physics claim survives it (my 10-second probe already contains the numbers).

Tree restored (patch and my clamp edit reverted); nothing in the run folder touched but `check.md`; no commits made.
