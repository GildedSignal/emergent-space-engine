# Dossier — 20261018-1237-system-4875 (system lens)

**Claim.** The flyable frame (engine + view gather + JSON + wire, the loop `xtask universe`
serves) is view-owned from ~8×10² bodies: at 10⁴ ladder bodies the frame is 262 ms p50 with
the engine at 0.11 ms p50 / 4.6 ms p99 (inside its 5 ms budget) and 99.7% of the frame in
the view's three Θ(N) channels — so the scoreboard's "10⁶ smooth" is an engine-only
instrument reading a plane the player cannot fly past ~800 bodies, and the adoption order
for the furthest-behind gap inverts: the view's row-set deletion (2df1, built, unwired)
before any engine cure.

**Bottleneck.** The board's #1: bodies in the flyable engine (28 → 10⁶ → 10⁹). The measured
instrument gap is ~3 orders (flyable ≈ 8×10² against the ladder's 10⁶ headline). What it
deletes: the belief that engine-side cures (the composed law, the scan phase-word tier) can
reach the player past ~800 bodies; and the flyable binary's inability to load the ladder's
scene at all (before this patch `--members` clamps at 400 and there is no belt knob — the
plane Julien flies cannot even hold the scene the scoreboard credits).

**Evidence** (Linux/x86, 8 vCPU, load 0.8–1.2, orders of magnitude only; regen.sh
regenerates every number in ~5 min from shipped code + `work/patch.diff`, which adds
`--extra N` to `xtask universe` routing `scenario::plane_extra` into `Session::step`):

| arm | bodies | frame p50 ms | engine p50/p99 ms | gather p50 | json p50 | wire p50 | view+wire share |
|---|---|---|---|---|---|---|---|
| control `--extra 0` | 71 | 0.98 | 0.05 / 2.2 | 0.75 | 0.10 | 0.04 | 0.71 |
| `--extra 1000` | 1,071 | 22.0 | 0.10 / 4.6 | 19.3 | 1.9 | 0.6 | 0.97 |
| `--extra 10000` | 10,071 | 261.8 | 0.11 / 4.6 | 232.1 | 24.1 | 4.7 | 1.00 |
| ditto, seed 2 | 10,070 | 254.6 | 0.09 / 4.5 | 231.1 | 18.2 | 4.7 | 1.00 |
| ditto, rtf 1 | 10,028 | 257.3 | 0.05 / 0.09 | 228.9 | 23.3 | 4.8 | 1.00 |

- Slope 21 µs/body (0→10³), 26.6 µs/body (10³→10⁴): near-linear, mildly superlinear
  (cache); the flyable frame crosses 16.7 ms at ≈ **794 bodies**; every 10⁴ frame is over
  (360/360, 180/180 on both held-out arms), 593/600 at 10³.
- The engine half on the *same flights* reproduces the ladder's own record (f416ea93's
  flat-in-N): p99 ≤ 4.6 ms under the burn script, never blowing its 5 ms budget. Both
  halves of one frame, one instrument, for the first time.
- The wire carries one row per body: at 10⁴ that is ~2 MB/frame ≈ 120 MB/s at 60 Hz
  (arithmetic from row shape; json build 2.4 µs/row + serialize 0.46 µs/row measured).
- rtf 1 is identical (257 ms): the wall is per-frame, not per-event — flying slower does
  not dodge it.
- The control arm reproduces the shipped plane's known smooth dashboard (p50 0.98 ms,
  0 hitches) — the instrument is sane; the engine-p99-under-budget in every arm is the
  other side's control (if the engine had blown first, the ranking would soften; it did not).

Commands (the 10⁴ arm is 97 s wall — one frame there is 260 ms, so 360 frames cannot fit
60 s; the arms are sized to the run's budget and regen.sh stays under 5 of its 15 minutes):
`xtask universe --bench --unpaced --seconds {10,10,6,3,3} --rtf {100,100,100,100,1}
--extra {0,1000,10000,10000,10000} [--seed 2]`.

**Predictions** (`predictions.md`, written before the flights): engine flat and inside
budget — **held** (0.05–0.11 ms p50, ≤ 4.6 p99); linear gather — held in shape, **wrong on
the constant**: I predicted 6–10 µs/body, measured 19–23 (the belt's bodies are real tube
readouts up the doll chain, not the fleet members earlier view runs priced); json+wire
1–2 µs/row — held (2.9 µs/row combined); crossing at 1–2×10³ — held, at the low end
(≈ 8×10²); view-owned ≥ 80% at 10⁴ — held (99.7%). Seed 2 within load noise — held.

**What would make it wrong.** The browser half: the bench stops at the wire, and the page
must also parse those ~2 MB/frame, so the true served wall is *earlier* than 794 bodies —
my crossing is optimistic, not pessimistic. The ranking breaks if 2df1's row-set deletion
does not hold at belt zoom (62c1's own checker: belt zoom puts ~N rows on canvas) — then
the flyable belt stays Θ(N) and the view cure is zoom-scoped, not total. Adoption cost: the
`--extra` knob is 20 lines (this run's patch); the row-set deletion is 2df1's built branch;
nothing here changes the engine.

**Fit with PRINCIPLES.** "the goal is whatever leads us fastest to the finished product" and
#27 "The goal, never a proxy": the engine-only ladder is a proxy for the flyable plane; this
run prices the difference. #28 "The view is an instrument": here the view is the frame's
dominant term, and its cure is unwired. #12 (smoothness, the single worst frame): every
frame at 10⁴ is 15× over. #1 "the cheapest compute is compute not done": 99.96–99.98% of
the gather's rows are pixel-static between frames (62c1) — compute not done is the lever
already built.

**The lens (what it may have missed).** A whole-system reading can mistake instrument
boundary for architecture: the engine's Θ(1)-in-N event stream is real and measured here
too; the right conclusion is ranking (view first), not that engine work was wasted — the
engine's cures become the bind again past ~10⁶ once the row set lands. I also did not fly
the formation scene (needs 604c's patch), where the scan channel joins the view in the same
frame; and I take 2df1's 1–3 ms row-set figure on its page's authority, not re-measured.
