Grade: gold

Abstract: Claim: the plane's engine core is schedule-independent (one digest per cut across nine adversarial paths, 3 seeds, repeats), but the shipped interactive loop logs key changes at the frame's presented tick (`session.rs:80`), so the same physical play writes different canonical histories at different frame rates and under load. Reproduced bit-for-bit from the dossier's commands in a clean tree: 16/16 matrix lines, 12/12 play lines, all three control digests (encounters 68–102, contacts 0–14, kicks 6474–6481). Adversarially extended: the leak persists at rtf 1 (the page's default pace) and at 512 members; thread count is a further axis through the same seam. Adoption: two lines (quantize the decision tick to scheduled game time) plus a play60/play30 equal-digest regression test. The core negative independently confirms adba97a's five-run validation.

## Reproduction

Applied `work/patch.diff` to a clean tree, built `CARGO_TARGET_DIR=/tmp/x-target cargo build --release -p emergent-universe --bin determinism` (8.9 s). Every run ≤ 6 s, well inside the time budget.

- Matrix (`/tmp/check-matrix.txt`): seeds 11/22/33 subset (direct, events1, events8, wall, frame-starve, frame-rich, frame-obs, ckpt; thr8) — every line bit-identical to `work/matrix.txt` (digest and all counters; only `wall_ms` and the `direct`/`direct-thr8` tag spelling differ). One digest per seed across all paths: `9dbf38e4…` / `9001b877…` / `ff0ff6d7…`; only events/slices counters move, exactly the pre-registered split.
- Play (`/tmp/check-play.txt`): 12/12 lines bit-identical to `work/play.txt`, including `play60-starve` seed 11 (`f7e17f7e…`, encounters 68, contacts 14 — the ruin form: same machine, same fps, different load).
- Control: `fixed-input` = `direct` at the 80 M cut for all three seeds, digests matching the dossier's quoted `49a1b20b…` / `264b1bee…` / `9fbcaa5f…`. Mechanism isolated as claimed: `input()` on the frame loop at fixed canonical ticks is canonical; only the wall-derived tick values move the canon.
- Code audit: `session.rs:78-82` and `kick_bench.rs:68` are the only `input(now, …)` callsites; `Universe::input` takes the decision immediately at the passed tick, and the digest hashes both the input log and the rolling encounter digest (`universe.rs:947-952, 1061-1069`), so the leak's effects are in canonical state, not just log bytes.

## Predictions

`predictions.md` (06:23:15) precedes `matrix.txt` (06:24:38) and `play.txt` (06:28:28); content pre-registers P1–P5 with probabilities and a frozen kill criterion. All five held. The play seam was honestly declared post-hoc and isolated by the control pair, which I reproduced.

## Adversarial cases (mine)

1. **rtf 1** — the author's admitted unmeasured magnitude (an `rtf 1.0` variant of the probe). The leak persists at the shipped default pace: digests split across fps for both seeds tested (seed 11: `973d2a04`/`f60472c9`/`17a3190d`; seed 22: `4ff6fc14`/`07c755ae`/`0d64b693`), and the load-only form splits for seed 22 (`4ff6fc14` vs `dea83e92`). Encounter/contact counters happened to be stable at rtf 1 in this sample, but the player's canonical position moves — the history is still not regenerable from the physical input timeline.
2. **512 members**: `play60` vs `play60-starve` still split (contacts 4 vs 12). Not specific to the 1024-member scene.
3. **Threads on the play path** (the matrix tested threads only on `direct`): `play60` thr8 = thr1 (no new axis unstarved), but `play60-starve` thr8 ≠ thr1 (`6c75a5de` vs `f7e17f7e`). `frame-starve` thr8 digest = thr1 = direct, so the core remains thread-clean; the difference flows through the same decision-tick seam — thread count is one more schedule axis the author did not list.

## Novelty

- **Section 1 (core negative) is confirmatory, not new.** The builder already measured "one digest over five schedules and budgets" (H0213; commit adba97a, 5 October: two paced runs, unpaced, engine budget 0.5 ms with 480 overflow frames, 4 threads), and plane.md foundation 2 asserts it. The dossier's claim that nothing audits it is true only of *lab* runs; adba97a's validation is unacknowledged. The run's value there is independent adversarial breadth (events1/wall/frame-starve/frame-obs/ckpt go beyond the builder's five).
- **Section 2 is novel as a measured result.** adba97a fixed replays and bench-scheduled inputs and deliberately left the live loop logging at the presented tick (documented in session.rs). law.md's frozen Ties rule (5 October) says "A player's decision takes effect at the canonical tick written in the input log, never at a wall-derived one" — the shipped live loop *writes wall-derived ticks into that log*, so the rule's premise fails exactly where the player plays. No HISTORY entry, board item or commit measures the consequence; the magnitude (encounters 68–102, contacts 0–14, four digests per seed, the same-fps load-only form) and the mechanism isolation are new.

## Goal fit

AGENTS.md Truth: "Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware" — violated at the one reachable seam, restored by the fix. PRINCIPLES #13 (errors never compound: a flipped contact rewrites the battle's history) and #25 (avoid ruin). Method fits: simplest falsifying probe, controls on both sides, kill criterion frozen before the run, honest post-hoc declaration.

## Reasons for the grade

Every number regenerates bit-for-bit; predictions pre-registered and held; the finding shows a frozen premise wrong at the shipped seam and is adoptable within one step (fix direction plus the regression test the author specifies — my rtf-1 and members-512 runs say the test should also pin the load-only pair, which is the ruin form). The blemishes are reporting-level, not evidence-level: the HANDOFF misquote below and the uncited prior validation of section 1. They belong in the record, not between this and gold.

## What the author missed

- **HANDOFF is misquoted.** "Risks to attack first" (current) names: candidate work at scale, H_live, the B12 instrument, simultaneity across dolls, no-tube orbits — it does *not* name silent nondeterminism. The bottleneck framing stands on AGENTS Truth and plane.md alone.
- rtf 1 (the page's default) and members scaling: both measured by me, both leak. The dossier's "unmeasured at real-time pace" gap is closed on the negative side.
- Thread count as a leak axis on the starved play path.
- adba97a / H0213 as prior art for section 1.
- The older fly slice's live server logs inputs at `f.core.tick()` (`fly/server.rs:271`) — the same wall-progress shape; fly's Replay itself is clean, as the dossier says of the plane's.
- The bench consequence deserves weight: `kick_bench.rs:68` shares the seam, so the kick bench's digests are wall-derived and A/B comparisons across machines compare different canonical histories, not one history's cost.
