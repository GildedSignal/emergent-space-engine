# Dossier — 20261006-0030-taleb-d3fe

## Claim

The shipped plane carries a reachable ruin state: peak memory grows about linearly in game time through any fleet battle that stays live (~0.2 kB per surviving member per game-second; the never-dissolving battle makes it unbounded, ~1.6 GB per hour at the bench's own scene), it spreads 2.8x across seeds at one config, and nothing installed today can see it — the bench's `seconds` ceiling (55 s) puts the signal 4 orders of magnitude under the noise floor, and the engine's own memory instrument (`bytes_per_body`, ~9 kB x 74 bodies = 0.7 MB) is blind to 99.8% of the measured peak.

## Bottleneck

Not a speed bottleneck: this is the ruin-before-optimization item. PRINCIPLES' Truth section says canonical outcomes are "independent of cache, partition, observation, schedule and hardware", and the machine section says swap runs near its 10 GB limit in daily use; a per-game-second memory law on the 8 GB M1 is swap death (one of the lens's unrecoverable states), not a slow frame. It makes the live fix (HANDOFF job 1, "the fleet battle is stepped forever") load-bearing for survival, not merely for CPU. It also answers the board's memory bottleneck with a measurement method: judge peak RSS at fixed game depth across seeds, not `bytes_per_body`.

## Evidence

All commands in [`reproduce.sh`](reproduce.sh) (each <= 55 s; `cargo build --release -p xtask` once, 48 s cold); raw numbers in [`raw.md`](raw.md). Linux/x86, 8 vCPU, shared — orders of magnitude only; the M1 re-measures.

1. **The law** (seed 3, members 48, `--rtf 10k..80k --seconds 8 --unpaced`): peak RSS 31 / 70 / 140 / 280 MB over 8e4..6.4e5 game-seconds, while every canonical event counter stays flat (kicks ~17.0k, opens ~646, boundaries ~13.6k, slices ~67k, bodies 74, `bytes_per_body` ~9.1 kB). Slope ~443 B per game-second at 2 surviving members; ~181 B per member per game-second at 3 survivors (members 96). Frame CPU is flat across the sweep (p50 5.9 ms, p99 6.7 ms); the wall grows 4.1 -> 28.3 s: the accumulation and the work both live in the settle-to-cut path, not the frames.
2. **Controls on both sides.** A battle that dissolves is flat: members 16 at rtf 4e4 -> 19 MB (`dissolved: 1`), so the doll/universe path and the 74 ordinary bodies do not accumulate; only a live battle does. The instrument is sensitive: digest differs across seeds and member counts.
3. **Fat tails.** Same config (members 48, rtf 8e4), seeds 3/4/5 -> 279 / 101 / 211 MB (2.8x from configuration alone; seeds 4 and 5 even dissolve, retaining what accrued while the battle lived). Identical runs also spread (279 vs 349 MB), so single-run RSS is a noisy estimator: judge medians or worst-of-3.
4. **Gate blindness, measured.** At the bench's default pace (rtf 1) the same law yields ~24 kB over the 55 s ceiling — invisible. The engine's `bytes_per_body` reports 9.1 kB x 74 bodies while RSS says 280 MB.
5. **Determinism held** (the other ruin axis): two separate processes and threads 1 vs 4 give byte-identical digests at the same canonical cut; a seed change differs. The in-repo tests cover in-process invariance; this closes cross-process.
6. Side findings: `--members` silently clamps to [4, 400] (asked 768/1536/3072, got 400 — my own first "saturation" reading was this artifact); and the scene's extent grows with sqrt(n), so the shipped bench cannot construct a fixed-volume dense cell at all (P-C unrunnable on this instrument); pre-contact fleet cost scales ~n^0.6 sublinearly; at rtf >= 10 the contact regime is reachable and the worst frame equals p99 (~7 ms, one class of contact frames ~10x p50).

## Predictions

[`predictions.md`](predictions.md) was written before any bench run. P-A held (with working controls). P-B1 held (~n^0.6 at constant density, within 1.0 +/- 0.3). **P-B2 failed decisively — that failure is the headline** (memory not flat in game time; the instrument blind). **P-B3 failed** (<2x predicted, 2.8x measured). P-C was not run: the instrument cannot build the case (members clamp, sqrt(n) extent); reported as an instrument gap, not a physics result.

## What would make it wrong

Peak RSS on Linux/glibc overstates retained memory (allocators rarely return to the OS); the *allocation* is real regardless (monotone 9x growth with flat event counters), but the M1 number may differ — the integrator should re-measure `--rtf 80000` worst-of-3 seeds. If the memory is freed at dissolution on macOS, seeds 4/5's 101/211 MB peaks would shrink there; seed 3's never-dissolving case still grows without bound. I did not localize the allocation to a named structure (no valgrind/heaptrack on this host; installing needs root) — the mechanism (per surviving member per game-second, live-battle-only, settle-path) is pinned, the structure is not.

## Cost of adopting, and fit

Adoption is a measurement, not a change: keep `reproduce.sh` as the regression probe (3 runs x ~30 s) next to the dissolution fix; expect it flat-lined. The fix itself is already Sonnet's job 1 — this run changes its priority from "CPU waste" to "swap death". PRINCIPLES: "its risk of breaking makes anything you do to improve it or make it 'efficient' inconsequential unless you first reduce that risk of breaking" (the lens brief); "minimize spike compute and average compute usage" (#12) is exactly what an unbounded memory law defeats; the lab's own host died this way on 5 October ("a GLM experiment took 15 GB and the OOM killer stopped the runner") — the engine has the same failure mode, slower.

## The lens

Taleb's lens hunted ruin and found it in memory, not in floats (determinism passed cleanly — credit to the plane's designers). What the lens may have missed: the speed side (it declines to optimize), the localization of the leak to a structure (needs a heap profile on a machine with tooling), and any ruin state that needs cross-hardware runs to appear.
