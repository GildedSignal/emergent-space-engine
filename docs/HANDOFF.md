# Emergent Space — handoff

Current as of 6 October 2026 (H0214; the "In flight" table below carries the exact time). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

## First ten minutes

0. Read "In flight" below first: what is running, where its output lands, and what to do when it finishes.
1. Read [PRINCIPLES.md](PRINCIPLES.md), [AGENTS.md](../AGENTS.md), then this file. Run `cargo xtask history list` and search for entries related to your task.
2. Read the heading card [CARD.md](CARD.md), then preflight.
3. Run `git status --short` and `git log -8 --oneline`. There is one checkout, `~/Research/emergent-space`, on `main`.

## In flight (overwrite when jobs change; the first thing to read after a compaction)

**Back from the autopilot (12 October).** GLM: 557 runs, 100 gold (quality checked: the clock gold reproduced exactly on the M1); its builds failed (8 of 14 ungraded). Codex: 9 jobs on 10 October, 3 clear wins on branches, none merged.

| Job | Who, where | Lands | Next action |
|---|---|---|---|
| **The ship's clock at high γ: merged 12 October** | f7f6d87 (Sonnet): a weak-field hyperbolic key carries its gap with its own exponent; τ takes the exact numerator, so dt/dτ = E to 1e-8 up to E = 10⁶ | main | C1 passes: the ≤ 60 s tests, and the full flight to the leave (`--ignored c1_to_the_leave`, 527 s on the M1: ~3×10⁵ events, a frame-cost signal). Only burns past ~1,200 km/s change digests. **Open limit:** a hyperbolic key is refused (`Range`) when its periapsis is above ~2.7×10⁸ M (about 2.7 AU about the star) even at E = 3: a fast flight far from the star is lost (to the sweep and item 3) |
| **Playability: merged 13 October** | Sonnet (and Codex's plunge arcs): the nose starts prograde; the HUD warns of an impact course minutes ahead and clears; braking to rest is a fall you can burn out of (gate P1: 15/15, zero refusals, worst 1.05e-4); a burn is paid at every kick level (thrust was lost through the Moon's engagement). Sweep: zero refusals in normal flight. **Baselined red (owner: `range`):** a prograde L15 burn's clock drifts past γ≈60 (8.9e-2 at γ=120; the key's k keeps only 21 bits), and a far flight is refused past ~6 AU (`Range`); C1 keeps its frozen +x course | main | Julien flies it |
| **Smooth flight (gate F1)** | Sonnet (13 October) continues in `/private/tmp/emergent-wt-frame` on `wt/frame` from the profiler and probes (b4671d3, unverified) | `wt/frame` | Verify F1 (the sweep at rtf 100, levels 0–15: no frame over 12 ms after the first second, zero lag), digests bit for bit, the suites, B13; resolve its overlap with `wt/play` in step.rs; merge second |
| **The flight recorder** | Sonnet, `/private/tmp/emergent-wt-recorder` on `wt/recorder`; job file `artifacts/runs/recorder/prompt.md` | a commit on `wt/recorder` | Verify: every flight writes `artifacts/flights/*.json` (inputs, seed, commit, losses); `universe --replay` reproduces a digest; `--replay-all` (≤ 60 s) flags a new loss or refusal; then it runs before every merge |
| **GPT: far flybys (gate R1)** | `artifacts/runs/codex-oct13/runner.sh gpt` (gpt-6-astra, job file `artifacts/runs/range/prompt.md`, worktree `/private/tmp/emergent-wt-range`, branch `wt/range` from main). **Julien's GPT hours:** no GPT call 12:45–23:00 Paris (the runner's `quiet`, and `watchdog.sh` stops sessions at 12:45; they resume at 23:00) | `wt/range` | Verify R1 (flybys at 3–100 AU, E 1.001–1000: zero refusals, readout ≤ 1e-6, C1 holds), G1–G6, B19, digests; merge third |
| **B12 v3 (decided 13 October)** | GPT after `range` (gpt-6.1-sol, job file `artifacts/runs/b12v3/prompt.md`, branch `wt/b12v3` from `wt/cx-b12-v2`); spec in law.md's B12 row: 10⁴ periods, per-ship verdicts, the integer Allan rule and the α-profile must agree, controls on both sides | `wt/b12v3` | Queue a GLM premise red-team on the built gate, then freeze at its first run; the plane then faces B12 |
| **Codex wins: merged 12 October** | Kerr compiler (B19 passes, 405b9fb), belt wiring (B18, B18b pass, 1587020), co-orbital tier (92c94b1). `shipmem` and `encounters` are built, not yet wired into the plane | main | Wire them into the plane by bottleneck. Kept for their diagnoses (branches): plunge tubes, encounter skin (5.3×), B12 v2 (needs a red-team), energy register, root keys, handoff surface |
| **The lab wiki** | `lab/wiki/` (Karpathy's pattern: runs are the raw sources, pages the compiled memory), `lab/wiki.py`; publish folds gold and silver pages in three-way and rewrites the index | pushes to main, `lab/wiki/` only | 13 compile jobs head `lab/queue.txt` (`q-wiki-*`). Read `lab/wiki/index.md` instead of dossiers; check the first compiled pages against their runs |
| **GLM lab changes (12 October)** | runner: authors read the wiki and write `regen.sh` (the runner runs it, with one 15-minute fix phase) and their topic page; checkers test outside the author's range and check the page | — | Watch the first window's results for regen failures and page conflicts |
| **Method (draft)** | [method.md](method.md), seventh draft: the method as a causal chain (events, certificates, provenance, hysteresis). Julien's note to fold in: "leverage git fully" (Toyota TPS, Palantir Foundry, SpaceX) | — | Julien reads |
| State of the engine on 6 October | Main: the motion law v2 steps 1–2 (c84f578); gates B18b and B19 frozen; B12's statistic known miscalibrated (redesign in flight); B13 60/64 at step 7 (failures marginal), B17 passes (steps 4–6), G1–G6 and E1–E8 pass, E9 fails phase 1 as expected | — | The bottleneck order is the queue's order |

**Traps that bit us (read before acting):**
- Never chain a merge after tests without stopping on failure (`&&` on the test's exit code): two branches green alone can fail together (6 October, the loss view and the motion law v2).
- When a sandboxed Codex builder can't commit: `git status`, then `git add -A` the whole worktree, build main, then push and remove. Once only `crates/` was added, and an adapter was lost with the worktree.
- GLM's Claude-hosted routines died with Claude's windows (three times): GLM now runs on GitHub Actions, never on a Claude host.
- Codex may fail on "model at capacity" or on its 5-hour limit: resume with `codex exec resume <session id from log.txt>`, never restart.
- Gates are frozen before builds and never sized to a representation. Write criteria passable in principle, with controls on both sides. The integrator's criteria errors (r2, r3, r8 v2, τ) were all caught by checkers.
- Never speak in days; pace by the 5-hour window; AI is off the plan; every body is real (no averaging populations).
- Claude's week, not only its 5-hour window: three parallel Sonnet agents spent 82% of a week in a day and a half. At most two Claude builders at once; research goes to GLM. Agents cut by a limit resume with SendMessage; they commit as they go.
- GLM's 5-hour window: five slots spent it early and killed the runs in flight; four fit. GitHub's scheduled triggers get dropped: the lab chains itself and waits out GLM's limit on agonbox.
- Never edit `.github/workflows/glm-lab.yml` while a window runs without the publish fix in place (result branches are cut from main's tip since 156f4fd); a GLM experiment once took 15 GB (agonbox's runner is capped at 12 GB, OOMPolicy=continue).
- Several lab runs agreeing is not independence when they share a harness (the memo artifact); and a gate can be wrong: check its oracle's domain (B12, B13, B17 all were) before blaming the law.

## Headed next (12 October; Julien: "we want something functional … i just don't want it buggy, fly like the sr 71"; at most two sub-agents)

The to-do list, by importance. Each item lands only when it is green:
1. ~~**The high-γ clock**~~: merged (C1 passes to the leave).
2. **The flight sweep** (`crates/universe/examples/flight_sweep.rs`, 12 October, rtf 100, 20 s a flight): every loss was a crash into Home, because **the ship starts with its nose retrograde** (heading 0 = +x while it orbits along −x), so "forward" burns it into the planet; and from L8 up the frame hits its 12 ms budget and the presented time lags up to 1.6 s (a stutter). No refusals in 20 s flights.
3. **Fix the sweep's findings** (the second sub-agent, after the clock merges: same code): start the nose prograde; the HUD warns of an impact course (the engine already plans the impact); braking to rest (`NoBoundOrbit`, plunges: Codex's partial `wt/cx-b-plunge-tubes`); then rerun the sweep.
4. ~~**Retire the kick jet**~~: done in law.md (not in the shipped code).
5. **The frame's cost** (Sonnet, `wt/frame`, gate F1): the stutter from L8 up; lazy re-keying and the incremental deadline first, bits preserved.
6. **Later:** wire the belt and encounters into the plane; B12 v2 red-teamed, then frozen; the plane faces B12–B14.
7. Julien flies every merge (`cargo run --release -p xtask -- universe --rtf 100`, http://127.0.0.1:8792/). AI stays off the plan.

**Decided by Julien (29 September):**
- The law is a cheap, local, fixed integer algorithm. Exact GR is the oracle, not the implementation (H0195).
- Gravity is a field held by cells. Multipoles are the mechanism, including aggregates of ships.
- Observables (clocks, redshift, lensing) are derived on demand, never evolved.
- One engine, not five modes; the chronon survives only as a test judge.
- Behaviour and error type over error size.
- Every statement of his is followed or disproven with evidence ([PRINCIPLES.md](PRINCIPLES.md) register). He owns PRINCIPLES.md.

## Where we are (6 October)

- **Law** `es-space-v2` (docs/law.md, a draft spec; gates frozen one by one). The compiler: one mass, exact GR, compiled once from (E, L) (G1–G6 pass, B16 moving lenses). Contacts: `es-lattice-relativistic-v1`.
- **The plane** (docs/plane.md): one star system, whole, flying at 100× and more with no hitch in CPU time; the motion law v2 steps 1–2; Lorentz handoffs as integer shears; exact replays; ties; a throttle to 11,561 g with the c metric.
- **Judged:** B13 60/64 (failures marginal), B17 passes in the weak field, E1–E8 pass, E9 fails phase 1 as designed, B18b and B19 frozen ahead of their builds; B12's statistic is miscalibrated.
- **The lab:** GLM on agonbox, continuous; its record and decisions are `lab/board.md`'s taste log.
- Older engine history (modes, ladder v7) is in git and `docs/HISTORY.md`.

## Standing decisions

- **Microstates are canonical.** Entropy only schedules, and observation never changes outcomes.
- **Everything is emergent** ([PRINCIPLES.md](PRINCIPLES.md)). There is no central control, and no object categories: regimes are chosen by dimensionless numbers.
- **The memory floor is information-theoretic** (entropy given shared structure), not bytes × count.

## Risks to attack first

- **Candidate work at scale:** co-orbital concentration (fleets) makes the pairwise tier miss contacts and go quadratic (lab gold 20261006-0346-taleb-09b5); work must track real encounters.
- **Distinctions created per game-second (H_live):** they, not the body count, decide whether 10⁹ fit in 8 GB; not measured yet.
- **The instrument:** B12 cannot yet tell bounded from compounding error on chaotic ships; until it can, the motion law's stability is judged by probes, not a gate.
- **Simultaneity across dolls:** "one tick is the same time in every doll" is false (15–1,400 ticks at a sphere's edge); fast dolls need root-clock event keys.
- **Orbits with no tube:** plunging and near-radial orbits are refused (`NoBoundOrbit`); flying past γ ≈ 2,000 is refused.
- The light cone keeps growing (Julien: "there will always be a point where we cannot handle the universe anymore"). The approved plan's budgets (4 GiB, 30 FPS at 1080p, one hour, 20 GiB) are open, not dropped.

## The machine

A fanless MacBook Air M1, macOS 26.5.2:
- 4 performance cores (12 MB L2) and 4 efficiency cores (4 MB L2);
- a binned 7-core GPU;
- 8 GB of unified memory, with 16 KB pages;
- about 10 GB of disk free.

Swap runs near its 10 GB limit in daily use, and timing swings about 30% with heat. Measure in real conditions, with the state recorded. Eight probes of at most 60 s each are pending, to be run as the player runs, with the state recorded: i128 throughput on performance versus efficiency cores, GPU u32/u64/u128 cost, memory bandwidth, SSD streaming, the GPU round-trip floor, Accelerate/AMX exactness and throughput, Neural Engine latency, and a thermal metronome.

## Where things are

- Frozen evidence: `artifacts/evidence/`. The map for relocated or archived journal paths: [history-evidence-map.json](history-evidence-map.json).
- Remote (private): https://github.com/GildedSignal/emergent-space-engine, `main` only.
- Retired code and the old repository: `~/Research/emergent-space-archive`.
- Original conversations (including the continuation), research and aesthetic references: [reference/](reference/README.md) and `assets/reference/`.
