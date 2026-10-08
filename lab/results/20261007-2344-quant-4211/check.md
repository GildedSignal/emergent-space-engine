# Check — 20261007-2344-quant-4211 (quant lens: the deadline queue's capacity)

Grade: silver

**Abstract.** Claim: the plane's deadline calendar is O(N)/frame (rekey-all, drain, defer-requeue), capping 60 FPS/rtf 100 near 10⁴–10⁵ bodies; a dyadic wheel on event time plus a triangle-inequality skin on deadlines deletes the drain and rekey-all, 7–20× at 10⁶–3×10⁶, canonical states bit-identical. All 12 commands reproduce: every `sum_t` matches the author's and V0≡V4 in my runs; V4's churn counters match exactly (7,438 / 83,535 / 514,164 sqrts/frame); ratios 6.5–17.2× at load 5–7 (author 7.4–19.5× at load 10–14). The bench mechanics match shipped `universe.rs:493/790` and `calendar.rs` verbatim; law.md §"A body's state" confirms steps are powers of two. Cost to adopt: ~80 lines beside `Calendar`. Held-out prediction 5 failed (V3 not graceful — killed, disclosed).

## Reproduction

- Compiled `bench.rs` (0-byte `work/patch.diff`, nothing to apply) to /tmp and ran every command in `results.txt`. All `sum_t` values match exactly: M1e6/Hbeta `16289184286667`, Hrtf1k `138106832619467`, FLEET `16285934054275`, S3M `38709709126669` — V0≡V4 on every case, as claimed. V4's deterministic counters (sqrt/frame 7,438 at β=0.1; 83,535 at β=1; 514,164 at β·rtf=1000) match to the digit.
- Same-window ratios on my load (5–7): M1e6 17.2×, Hbeta 11.3×, Hrtf1k 1.6×, FLEET 8.3×, S3M 6.5× — against the author's 7.4/13.2/2.4/19.5/11 under load 10–14. Direction and order hold; individual ratios move with load both ways, which is why the author's in-window pairing was the right control.
- Fidelity to the ship: `Universe::rekey` (universe.rs:493) requeues every entity each frame; `advance` (universe.rs:790–830) peeks, `set(e, None)`+defers every `t > target`, requeues after the loop; `deadline_of` = `t + sqrt(dx²+dy²).min(4e18)` — the bench copies it including the clamp. The 4-ary sift logic is `calendar.rs` verbatim. Keys are `Scalar::integer` at the callsite (universe.rs:488). The "only a schedule" contract is universe.rs:16–17.
- `sweep-small.txt` clean-load numbers (V0 112.7 ms at 1e6, V2 rekey 8× under V0) consistent with my run.
- Peak RSS 793 MB at 10⁷ — inside the 2 GB cap.

## Predictions

`predictions.md` predates the outputs (mtime order: predictions 15 m before the final binary; the settle bugs it reports fixing came after). Held: capacity between 10⁴ and 10⁵; heap-over-sqrt (~85%); skin burst rate >30% at β·rtf=1000 (measured 51%); V0 position-blind under fleet concentration. Failed, both disclosed by the author: prediction 4/5 (V3 amortized <3 ns/entity, graceful degradation — V3 measured 57.6 ms at 1e6, killed as built) and prediction 3's "≥2×" for V2's frame (1.6×). Honest pre-registration with reported misses. Gold requires the held-out predictions to have held; they did not all hold.

## Attack (my cases)

1. **β=0** (stationary player): `sum_t` identical, V4 14.4× (158.6→11.0 ms). Skin never recomputes, as designed.
2. **Degenerate skin s=1**: `sum_t` identical; V4 still 4.7× — the wheel alone (drain deletion) carries the gain with the skin fully disabled.
3. **β=1, rtf=10⁴** (frame displacement 6.8×10⁷ ticks ≫ skin 2²⁴): `sum_t` identical, but **V4 loses: 28.9 ms vs V0's 24.6 ms (0.85×)**. The skin recomputes every deadline every frame (sqrt/fr ≈ N) while V4 also sweeps the full inbox (~10⁶ peeks); V0's drain exits after 381 peeks because the budget exhausts inside few bodies. Correctness never breaks; the *performance* envelope does, closer than the author's 2.4× point.
4. **Seeds 1, 2, 12345** (fresh copy with a seed arg): `sum_t` V0≡V4 per seed; ratios 14.8–15.0×, stable.
5. **Non-dyadic steps** (step = 2^k+1, odd, and steps 2¹⁷–2²⁴ including the wheel quantum 2¹⁸ itself): `sum_t` identical, V4 15.3×. The wheel is exact for arbitrary steps by construction (re-stash by exact t); the author's "the win rests on steps staying powers of two" is over-cautious — the claim is stronger than stated.
6. Current-binary V2 at 1e6: `sum_t` now matches V0 — the V2/V3 mismatches visible in `sweep-small.txt` are pre-fix-build artifacts.

## Novelty

No HISTORY entry or doc measures the calendar's frame cost or proposes a wheel/skin for it. The pre-pivot allocator/ladder work (H0157–H0173) addressed collision search and region scheduling, not this queue; H0210's plane records "one clock, one queue" with p99 2.45 ms at small scale, cost unexamined. plane.md foundation 7 (bounded work per frame) and bottleneck 4 (smoothness/allocator, the queue as the frame's O(N) floor) are the right homes. Timing wheels are classic external prior art (kernel timers), but principle 26 says steal what works; the triangle-inequality deadline skin transplanted from the encounter skin is the project's own.

## Goal fit

Real and PRINCIPLES-aligned: "minimize spike compute and average compute" (12), "deeply aware of von-neumann bottleneck" (17 — heap-over-sqrt measured at 85%), "we love 2" (16), schedule independence honoured bit for bit. But it is capacity work: today's flying scene is one star system (~10³ bodies, queue ≈ 0.1 ms/frame), so nothing hurts now; the gain is load-bearing only for the 10⁶-fleet gold. The author says this in "What would make it wrong" — correct call, and it is why this is not urgent adoption.

## The one experiment that would make it gold

Wire the wheel + skin into `crates/universe`'s `advance` (the ~80 lines the dossier sketches; `settle` drains the inbox, ties stay (tick, id)) and measure the real engine bench (`behave --law plane`) at its current scenes plus a 10⁶-body synthetic: digest identity across budgets/threads, frame p50/p99 gain, and the skin width derived from the frame's game-time advance (or a stated β·rtf envelope with fallback), closing the 0.85× regime I found.

## What the author missed

- **The sub-1× crossover.** At β·rtf=10⁴ V4 is a net loss (0.85×): once per-frame player displacement exceeds the skin width, V4 pays full rekey *plus* the full-N inbox sweep while V0's drain exits early on budget. The dossier says "the skin stops paying" (2.4×) but never states where the sign flips; the skin width must scale with the frame's game-time advance, not stay 2²⁴.
- **Capacity number stated tighter than the data**: 1.14 ms@10⁴ → 24.4 ms@10⁵ interpolates to ~7×10⁴ for a full 16.67 ms frame and ~1.2×10⁴ for a 10% share, vs the claimed ~3×10⁴/~2×10⁴. Same order; the digits overstate precision.
- **Stale evidence left in place**: `sweep-small.txt` is from the pre-fix build (its V2/V3 `sum_t` mismatch V0 at 1e6); its timings are quoted in `results.txt` without noting the binary differed.
- **The wheel does not need dyadic steps** (my case 5): the caveat undersells the result; exactness and speed hold for arbitrary steps.
- The remaining O(N) floor is the inbox re-sweep at overflow (0.7–1N peeks/frame at 10⁶–10⁷); the batched skip is named but unmeasured — at 10⁷ that stream, not the queue, is the frame's floor.
