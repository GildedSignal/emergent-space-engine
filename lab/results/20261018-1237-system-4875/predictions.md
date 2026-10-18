# Predictions (written before the decisive flights)

The question: the flyable frame (what `xtask universe` serves: engine advance + view gather
+ view JSON + wire, all inside the frame, engine budget 5 ms of a 16.7 ms frame) has never
been flown on the N ladder's own scene (the belt). Every ladder claim (N-flat to 10⁶) is
engine-only (`nladder`, which gathers once at the end); every view claim (Θ(N) gather) was
measured outside the flyable session. The flyable binary cannot even load the scene today
(`--members` clamps at 400; no `--extra`).

Arms (seed 1 unless said, rtf 100, 60 Hz, unpaced so the wall never couples, script = the
bench's own burn script): `--extra 0` (the control: the shipped flyable plane), `--extra
1000`, `--extra 10000` (6 s), held-out seed 2 at `--extra 10000`.

1. **Engine (the ladder's own record, so the control on that side):** p50 engine ms stays
   ≤ 1 ms and p99 ≤ ~5 ms through extra = 10⁴ (the belt's comb is N-flat on this scene,
   max ~40-100 events/frame). The control arm must reproduce a smooth dashboard (frame p50
   of ~1-3 ms); if it does not, the instrument is broken and the run is VOID.
2. **View gather:** linear, warm, ~6-10 µs/body → ~0.5-1 ms at 10³, ~60-80 ms at 10⁴.
3. **view_json + wire (the never-measured half):** linear in rows; I expect ~0.5-2 µs/row
   together, so ~1-2 ms at 10³ and ~10-20 ms at 10⁴. This is the number I am least sure
   of — it is the held-out quantity.
4. **The crossing:** the total frame crosses 16.7 ms at extra ≈ 1-2×10³ (view-owned), and
   at 10⁴ the frame is view+wire-owned (≥ 80% of the frame outside the engine), ≥ 4× over
   budget with the engine still inside its own 5 ms.
5. **Consequence I will test by arithmetic, not flight:** if 2-4 hold, then no engine-side
   cure (the composed law, the scan tier) changes what the player sees past ~2×10³ bodies
   until the view's row-set deletion (2df1, built, unwired) lands; the adoption order for
   the furthest-behind scoreboard gap is view-first.

What would make me wrong: the gather sub-linear on the belt (cache hits above the known
warm-start), json+wire negligible (< 0.1 µs/row), or the engine's belt comb blowing the 5 ms
budget at 10⁴ on the flyable script (then the engine co-owns the frame and the ranking
softens). Seed 2 holding the same law (within load noise) is the robustness check.
