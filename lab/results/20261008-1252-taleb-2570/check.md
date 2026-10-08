Grade: silver

**Abstract.** Claim: at 100× RTF the plane's wall cost saturates (~14–17 ms worst) while failure moves into silent zero-progress frames, and the canonical digest stays invariant across budgets/threads/pacing at that cliff. Reproduced bit-for-bit: digests `41343a14…` (m48), `77d106d9…` (m192), `29662bc6…` (m768/m1536 and at engine budgets 0.5↔50 ms, where overflow goes 799→0 and rtf.lowest_1pct 0→100); the zero-stall reproduces at m192 and already at m96. Two dossier errors: `--members` clamps at 400 (`xtask/src/universe/mod.rs:32`), so "32× load" is really ≤ 8.3×, and m768≡m1536 is the clamp, not generator saturation. Gain: retargets the smoothness gate to `rtf.lowest_1pct`; cost: measurement only.

## Reproduction (clean tree, empty patch.diff, same binary the author used)

`/home/glmlab/lab-target-3/release/xtask universe --bench …`, JSONs in `/tmp/chk-*.json`. My two command chains overlapped, so my wall numbers ran under contention; digests are unaffected.

| run | mine | author's | verdict |
|---|---|---|---|
| m48 r100 s30 | digest `41343a14…`, low1% 19.8, p99 10.4, worst 11.0 | `41343a14…`, 9.90, 10.67, 12.45 | digest identical; shape identical |
| m192 r100 s30 | digest `77d106d9…`, low1% **0.0**, worst 16.0, 0 >16.7 ms | `77d106d9…`, 0.00, 16.60, 0 | reproduced |
| m768(=400) s15, engine-ms 0.5 --unpaced | digest `29662bc6…`, overflow 799/900 | `29662bc6…`, 792/900 | reproduced |
| m768(=400) s15, engine-ms 50 --unpaced | digest `29662bc6…`, overflow 0, low1% 99.9998 | same | reproduced: budget moves work, never decisions |
| m1536 s15 | digest `29662bc6…`, bodies 417 | same | reproduced |

The stored JSONs match the dossier's table everywhere I checked (p50/p99/worst, overflow, ev/s, gather share 0.64/max 9.71 ms, engine max 8.52 ms). `predictions.md` (9 m) predates every result JSON (8→2 m) by file time. P3, the load-bearing prediction, held and reproduces.

## Adversarial cases

1. **The members knob.** `universe --members 1536 --describe` prints "1 fleet(s) of **400** members": `--members` is `clamp(4, 400)` (`xtask/src/universe/mod.rs:32`). So the ladder's "32×" top is 8.3×, and the m1536≡m768 digest equality is two runs of the same 400-member universe — **not** "generator saturation past ~768 (dropped-at-genesis, H0170)". The author's own proposed proof refutes their mechanism. Confirmed independently: m384 (real, unclamped) gives a different digest (`d6ab2add…`, bodies 400 vs 417).
2. **Below the claimed cliff.** m96 (2×): low1% **0.029** — the stall starts nearer 2× than the claimed 4×. The author's baseline m48 already dips to 9.9×/19.8× (10–20% of target) with 33–45 overflow frames: the cliff location is load- and seed-sensitive, as the dossier concedes for the M1.
3. **Seed 7 at m192**: low1% 1.81 — collapse to ≈0 holds across seeds; the exact 0.00 is not seed-invariant. Digest changes with seed as expected.

## Novelty

H0210/H0211 benched the plane at the default 48 members ("frame p99 2.45–2.72 ms, no hitch", gather 83% of a light frame) and H0210 already claimed "one digest across budgets and threads" at that load — the shipped bench's own `digest_note` states the invariant by design. New here: the ladder above default load, the silent zero-RTF stall category that wall percentiles cannot see, the invariance *verified at overload* (overflow frames, stalls), engine single-item budget overruns (max 8.5 ms against 5 ms), and the members clamp (mechanism misdiagnosed). H0212's taleb-c271 (canonical-tick replays) is adjacent instrument work.

## Goal fit

Bottleneck 4. Julien: "i care about the p95/99 results i want the game to be smooth"; "the algorithm that allocates the work to prevent those heavy tails, it's the most important one". A gate on wall hitches alone certifies a service that freezes: retargeting to `rtf.lowest_1pct` is the right consequence, and the unclamped gather (56–70% of the frame across runs, not the dossier's 64–69%) is a real §7-plane.md-shaped finding. The zero-tick reading is verified in code: `dash.rs` `rtf_low1` is the 1st percentile of per-frame `game_ticks·TICK_SECONDS / wall_dt`.

## Why silver, not gold

The core reproduces bit-for-bit, but two load-bearing wrapper claims are wrong as written — "32× load" (really ≤ 8.3×) and the H0170 generator-saturation mechanism for m1536≡m768 (it is a CLI clamp at 400) — and the author's headline cliff ("from 4× on") is really ~2× on this box. An integrator adopting the proposed kill criterion would calibrate it to wrong locations. Also "P4 held" is generous: `lost_bodies` is nonempty everywhere (26–213 "Armada (left its frame)" leavers, the known H0210 limitation); the prediction as written failed, though the numbers and the schedule-dependence reading (identical digests, differing counters) are disclosed honestly.

**The one experiment for gold:** rerun the ladder inside the real range (members ≤ 400), ≥ 3 seeds, bracketing the zero-stall point (48/96/192), with the clamp and the corrected gather-share range stated, and freeze the service criterion ("no frame presents zero ticks at 4× design load" on `rtf.lowest_1pct`) as the rung gate. One cheap step on the shipped bench.

## What the author missed

- The `clamp(4, 400)` five source lines below the flag they built the ladder on; their own `--describe` check, run, kills the H0170 reading.
- Seed robustness: one seed per rung; the exact 0.00 is seed-dependent (1.8 at seed 7), the collapse is not.
- The digest invariance is designed and already claimed (H0210, the bench's `digest_note`); the run's real contribution is verifying it *at overload* — the dossier presents it as more open than it was.
- The gather share range (64–69%) excludes their own m1536 file (56%).
