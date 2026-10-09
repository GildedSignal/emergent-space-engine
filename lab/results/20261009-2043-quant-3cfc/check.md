# Check — 20261009-2043-quant-3cfc (quant lens)

Grade: silver

**Abstract.** Claim: the plane's smoothness contract breaks at ~1,600 members (one indivisible `Fleet::advance` exodus slice, 0.6–1.5 s) and 8 GB cannot fly a 10⁵ fleet. Reproduced on a clean tree with the author's patch: 400/10 s digest bit-identical (`aadaa1c8…`), one 630–742 ms fleet item at 3,200–25,600 (`slices: 1`), break confirmed on seeds 2 and 7, at rtf 1, and at 4 threads; RSS 124/315/842 MB exact; 100 k killed at 1.85 GB and climbing. The clamp finding alone unblocks all load testing. Not gold: 3 of 5 held-out predictions failed, and the memory attribution is wrong — I measure 3.87 GB at 25,600 (author est. ~1 GB) and ~150–330 KB/member resident, not 6.5 KB/leaver; the 8 GB ceiling is ≈5×10⁴ members. Cost to adopt: one clamp line plus a fleet-boundary slicing fix, both named.

## Reproduction (clean tree, `git apply work/patch.diff`, rebuilt release)

| dossier claim | author | mine | verdict |
|---|---|---|---|
| 400 members, 10 s: p50/p99 4.8/10.1, overflow 105/600, view_gather 54 % | m1e6.json | 4.76/10.09, 106/600, share 0.54, digest `aadaa1c81e2bcc49…`, cut 203025447 | exact, bit-identical |
| determinism | two runs same digest | det1 = det2 (cut 40605089, `0527ad28…`) | holds |
| 1,600 broken | p99 25.1, overflow 116/120 | 25.96, 118/120 | holds |
| 3,200: one 624 ms slice, 1,269 leavers | s3200 | one item 643 ms, `slices: 1`, 1,329 leavers | holds |
| 6,400: one 645 ms slice, 2,573 leavers | s6400 | one item 630 ms, 2,510 leavers | holds |
| rtf 1 control | 621 ms | 636 ms, still one item | holds |
| 25,600: one 763 ms slice, p99.9 191.6 | s25600 | one item 742 ms, p99.9 168.6, 3,936 leavers | holds |
| RSS at 1,600/3,200/6,400 | 124/315/842 MB | 123.5/315.5/842.0 MB | exact |
| 100 k killed, >2 GB | 4.25 GB at ≥120 s | watchdog kill at 68 s, RSS 1.85 GB still climbing | conclusion holds |

The mechanism is visible in the stats line: at ≥3,200, `items[fleet] = 1` and `slices = 1` carry the whole window — the queue's per-member handout (68c5872, "nine members: 13 ms") sits *after* an atomic fleet-side `run_to` that includes the genesis anchor's mass hand-off. Budget, threads and rtf cannot split it.

## Held-out predictions

Written 20:46:25; every decisive run (s*.json) is 20:53–20:55 — genuinely before. P3 (tail bounded, worst/p50 ≈ 1.9 < 10) and P4 (readout dominates at shipped scale) held. P1 (capacity 10⁵), P2 (linear median growth) and P5 (≤1 GB at 10⁶) failed, each reported as a failure by the author. Honest, informative failures — but the gold rule says "the held-out predictions held"; three of five did not.

## Adversarial cases of my own

1. **Seeds 2 (1,600) and 7 (3,200):** break persists (p99 25.0/29.4; seed 7 one 642 ms item). The single-seed caveat is gone.
2. **`--threads 4` at 3,200:** still one 640 ms fleet item, p99 45.2 — parallelism does not dissolve the indivisible unit.
3. **5 s window at 6,400:** the single item grows to 1,524 ms — the slice is the *window*, worse than reported.
4. **25,600 RSS via `/usr/bin/time -v`: 3.87 GB measured** (author: "~1 GB (est.)"). RSS/member is ~150 KB and linear from 1,600 to 25,600: the 8 GB ceiling is ≈5×10⁴ members, *below* the dossier's 10⁵ headline. The conclusion survives, stronger than claimed.
5. **100 k under a 1.85 GB watchdog:** killed at 68 s, still climbing — ">2 GB at 10⁵" confirmed without wrecking the window budget.

## Novelty

No HISTORY entry load-tests the plane (`xtask universe`/`crates/universe`) above 400 members: H0158's ladder is the old `crates/engine` (p99 ≤ 1.9 ms, different machine path); 68c5872 fixed the universe-side handout at nine members/13 ms and explicitly left the fleet-side slice as one item; H0210–H0214 judge the plane only at the 48/400 defaults. The clamp at 400 (`xtask/src/universe/mod.rs:32`, pre-existing) means "never load-tested above 400" is literally true. The finding is new and it shows foundation 7 of docs/plane.md ("nothing takes an unbounded synchronous claim on the frame") is violated by the fleet boundary at ≥3,200 members — a premise break on the record.

## Goal fit

Board: "Cost at a billion" / B15 / the memory floor. PRINCIPLES 12 ("minimize spike compute…") and 24 ("why do you need so many bytes per entity?") are both measured open: a 0.6–1.5 s spike against a 5 ms budget, and ~150–330 KB resident per member against a 16-byte tube. Queued `b-readout-cost` gets its numbers (gather share 0.54 at the shipped scale).

## Why silver, not gold

1. Three of five held-out predictions failed — the gold rubric's "the held-out predictions held" is not met, whatever the failures' informational value.
2. The memory half of the record is wrong on its own arithmetic: "each handed-out member costs ~6.5 KB" is contradicted by the dossier's own 842 MB row (842 MB / 2,573 leavers = 327 KB; per in-frame member 218 KB); `bytes_per_body` is a live-state metric, not the resident carrier. The 25,600 estimate is off 4×. An integrator planning B15 off "6.5 KB/leaver" would mis-plan by ~50×. The author owned the non-attribution but not the wrong number.

**The one experiment for gold:** attribute the ~150–330 KB/member resident cost — battle member state vs leaver body vs view records (e.g. RSS-diff at fixed members with the `formation` flag already present in `scenes::battle`, which the plane currently passes as `false`) — and correct the memory rows; or demonstrate the named fleet-boundary slicing fix holding p99 ≤ 16.7 ms at 3,200 members. Either completes the record; the second proves the remedy.

## What the author missed

- The formation adversarial was runnable, not speculative: `battle(n, q, seed, speed_div, formation)` exists and the plane hardcodes `false`.
- Threads >1 (tested: no help), and the window-length dependence (5 s → one 1.5 s item).
- Their own 842 MB row already falsified the 6.5 KB/leaver story before I ran anything.
- The linear ~150 KB/member trend puts the 8 GB ceiling at ≈5×10⁴ members — the dossier *understates* its own finding.
- Wording: "400 (default)" — the shipped default is 48 (`mod.rs:20`); 400 is the clamp ceiling.
- The B15 tie-in is loose: B15's 2²⁰ rung runs through `behave`'s galaxy scenes, not this plane's `--members` path; the extrapolation is reasonable but should be labelled one.
