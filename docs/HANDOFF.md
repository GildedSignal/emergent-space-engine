# Emergent Space — handoff

Current as of 13 October 2026 (H0217; the "In flight" table below carries the exact time). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

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
| **Merged 13 October (the integrator)** | `wt/frame` (smooth flight, partial: F1 green to L8, the player's scan off the critical path, bit for bit), `wt/recorder` (every served flight in `artifacts/flights/`; `universe --replay-all`), contacts exact (`lattice::law::hit` in 512 bits past `i128`: it wrapped on 16-58% of a burn's pairs), a decision logged at the tick it takes effect (`Universe::input`) | main | `universe --replay-all` before every merge (0 regressions now; the three flights changed digest with the law) |
| **The N ladder (gate N1): running** | Claude Sonnet (the one Claude builder), `wt/nladder`, worktree `/private/tmp/emergent-wt-nladder`, job `artifacts/runs/nladder/prompt.md`: the plane with N real bodies, 10² up, until a rung breaks; name the first break and its exponent; fix it if it is the plane's own (or the smallest compact-store promotion) | `wt/nladder`, `artifacts/runs/nladder/ladder.txt` | Verify N1 (score before/after; N = 0 bit for bit; the suite) and merge; the first break orders the next jobs |
| **GPT: far flybys (gate R1)** | `artifacts/runs/codex-oct13/runner.sh gpt` (pid in `ps`; gpt-6-astra; job file `artifacts/runs/range/prompt.md`; worktree `/private/tmp/emergent-wt-range`, branch `wt/range` from main). GPT's quota ran out at 08:30 on 13 October; **Julien's GPT hours: no GPT call 12:45–24:00 Paris** (`quiet`, `watchdog.sh`); the session resumes at 23:00; queue `range`, then `burst` (gpt-6.1-sol, `artifacts/runs/burst/prompt.md`: the burn's centred payment and geometric cadence; gates T1, frozen in `crates/universe/tests/t1_burn.rs`, and F1), then `b12v3` | `wt/range` | Verify R1 (flybys at 3–100 AU, E 1.001–1000: zero refusals, readout ≤ 1e-6, C1 holds), the two baselined reds (prograde L15 clock past γ≈60; refusal past ~6 AU), G1–G6, B19, digests |
| **B12 v3 (decided 13 October)** | GPT after `range` (gpt-6.1-sol, job file `artifacts/runs/b12v3/prompt.md`, branch `wt/b12v3` from `wt/cx-b12-v2`); spec in law.md's B12 row: 10⁴ periods, per-ship verdicts, the integer Allan rule and the α-profile must agree, controls on both sides | `wt/b12v3` | Queue a GLM premise red-team on the built gate, then freeze at its first run; the plane then faces B12 |
| **Codex wins: merged 12 October** | Kerr compiler (B19 passes, 405b9fb), belt wiring (B18, B18b pass, 1587020), co-orbital tier (92c94b1). `shipmem` and `encounters` are built, not yet wired into the plane | main | Wire them into the plane by bottleneck. Kept for their diagnoses (branches): plunge tubes, encounter skin (5.3×), B12 v2 (needs a red-team), energy register, root keys, handoff surface |
| **The lab wiki** | `lab/wiki/` (Karpathy's pattern: runs are the raw sources, pages the compiled memory), `lab/wiki.py`; publish folds gold and silver pages in three-way and rewrites the index | pushes to main, `lab/wiki/` only | 13 compile jobs head `lab/queue.txt` (`q-wiki-*`). Read `lab/wiki/index.md` instead of dossiers; check the first compiled pages against their runs |
| **GLM lab changes (12 October)** | runner: authors read the wiki and write `regen.sh` (the runner runs it, with one 15-minute fix phase) and their topic page; checkers test outside the author's range and check the page | — | Watch the first window's results for regen failures and page conflicts |
| **Method (draft)** | [method.md](method.md), seventh draft: the method as a causal chain (events, certificates, provenance, hysteresis). Julien's note to fold in: "leverage git fully" (Toyota TPS, Palantir Foundry, SpaceX) | — | Julien reads |
| GLM directed queue | `lab/queue.txt`: `q-wiki-kick-jet-close` (resolve the page's merge conflict, close the topic); then free lenses on the least-explored topics | `lab/wiki/` | Read `lab/wiki/index.md` |

**Traps that bit us (read before acting):**
- **The Mac froze at 00:26 on 14 October** (a watchdog reset under a night job, swap near full): `/private/tmp` and every worktree went with it; only uncommitted work was lost (B12 v3's first 23 minutes). Worktrees now live in `~/Research/emergent-wt/`; the GPT runner compiles with two jobs and waits for 15% free memory. Builders commit as they go.
- Never chain a merge after tests without stopping on failure (`&&` on the test's exit code): two branches green alone can fail together (6 October, the loss view and the motion law v2).
- When a sandboxed Codex builder can't commit: `git status`, then `git add -A` the whole worktree, build main, then push and remove. Once only `crates/` was added, and an adapter was lost with the worktree.
- GLM's Claude-hosted routines died with Claude's windows (three times): GLM now runs on GitHub Actions, never on a Claude host.
- Codex may fail on "model at capacity" or on its 5-hour limit: resume with `codex exec resume <session id from log.txt>`, never restart.
- Gates are frozen before builds and never sized to a representation. Write criteria passable in principle, with controls on both sides. The integrator's criteria errors (r2, r3, r8 v2, τ) were all caught by checkers.
- Never speak in days; pace by the 5-hour window; AI is off the plan; every body is real (no averaging populations).
- Claude's week, not only its 5-hour window: three parallel Sonnet agents spent 82% of a week in a day and a half. One Claude builder at a time (Julien, 13 October: too many stopped mid-job and had to be re-cached); research goes to GLM. Agents cut by a limit resume with SendMessage; they commit as they go.
- GLM's 5-hour window: five slots spent it early and killed the runs in flight; four fit. GitHub's scheduled triggers get dropped: the lab chains itself and waits out GLM's limit on agonbox.
- Never edit `.github/workflows/glm-lab.yml` while a window runs without the publish fix in place (result branches are cut from main's tip since 156f4fd); a GLM experiment once took 15 GB (agonbox's runner is capped at 12 GB, OOMPolicy=continue).
- Several lab runs agreeing is not independence when they share a harness (the memo artifact); and a gate can be wrong: check its oracle's domain (B12, B13, B17 all were) before blaming the law.

## Headed next (13 October; Julien: "we want something functional … i just don't want it buggy, fly like the sr 71"; one Claude sub-agent; the integrator orchestrates, it does not build; GPT is Julien's from 12:45 to 23:00 Paris)

The to-do list, by importance; each item lands only green, through the same checks (suites, the item's gate, B13 not worse, G1–G6, the sweep):
1. **Merge in order as they land:** `wt/nladder` (Sonnet, gate N1: the furthest gap, and the order of the next ones), `wt/range` (GPT, gate R1: far flybys; owns the two baselined reds), `wt/burst` (GPT, gates T1 and F1: the stutter above L8), `wt/b12v3` (GPT; then a GLM red-team, then freeze; then the plane faces B12-B14). `wt/frame` and `wt/recorder` merged 13 October.
2. **Julien flies** the merged plane (`cargo run --release -p xtask -- universe --rtf 100`, http://127.0.0.1:8792/); his flights are the regression suite once the recorder lands.
3. **Integration, the next bottleneck:** wire into the plane what is built beside it: rotating holes (`crates/space/src/kerr.rs`) into the motion resolver; the belt (`crates/shipmem`) with bodies held compact and promoted to live only when something happens to them; the encounter tiers (`crates/encounters`).
4. **Gravity at c** (law.md "gravity is news": a cursor plus a version ring): from design to the engine; the foundation Julien insisted on.
5. **Scale to 10⁹ on the M1:** the frame's per-body cost (F1's sequel), the kick at ~1,800× its floor (the refit stays exact: the jet is retired), memory ~2× over in the worst case (a driven belt at 126 bits/body; the quanta decide, `lab/wiki/memory-h-live.md`).
6. **Then:** the Fermi frame's phase 2 (E9), inspiral (Peters' generator), the motion law v2 steps 3–4 (single-surface handoff, root-clock keys: Codex's attempts failed, kept on branches).

**The scoreboard (13 October; Julien: "tackle what's the furthest behind … without just asymptoting"):**

| What | Goal | Now | Gap |
|---|---|---|---|
| Real bodies in the flyable engine | 10⁹ | 28 GR bodies + ≤ 400 flat fleet members | 10^6.4 |
| Encounter work at 10⁹ (cone tier with the skin, cells of 10⁴) | a few cores | ~10³-10⁴ cores (`lab/wiki/encounters.md`) | ~10^3 |
| One kick (an exact refit) | ~42-55 ns floor | 75-160 µs | ~10^3.3 |
| Stored bits per body at 10⁹ (8 GB machine) | ≤ ~48 | 21-40 (phase-locked belt), 126 (driven belt, worst) | ≤ 10^0.4 |
| Smooth flight (F1, levels 0-15) | all 16 | L0-L8; 1-2% of frames late above | the burst (`burst` job) |
| GR, one body / many bodies | exact behaviours | G1-G6, B16, C1, P1 pass / B13 60/64, B17 pass, B12 being built, B14 times out | ~85% / ~45% |
| Rotating holes, gravity at c, tides, inspiral | in the flight | compiled not wired; designed; ~25%; ~5% | not wired |

The gaps interlock: CPU at 10⁹ = bodies × kick rate × kick cost + encounter work; memory = bodies × bits + live bodies × ~1.3 KB. Climbing the bodies in the plane (the N ladder) exposes the 10³ gaps in the order they bite, so it goes first. Overall, about 35% of the finished engine (a judgement ±10).

**Decided by Julien (29 September):**
- The law is a cheap, local, fixed integer algorithm. Exact GR is the oracle, not the implementation (H0195).
- Gravity is a field held by cells. Multipoles are the mechanism, including aggregates of ships.
- Observables (clocks, redshift, lensing) are derived on demand, never evolved.
- One engine, not five modes; the chronon survives only as a test judge.
- Behaviour and error type over error size.
- Every statement of his is followed or disproven with evidence ([PRINCIPLES.md](PRINCIPLES.md) register). He owns PRINCIPLES.md.

## Where we are (13 October)

- **Law** `es-space-v2` (docs/law.md): the compiler exact in GR for one mass, bound, unbound, plunge and light (G1–G6, B16, P1), the clock exact in E (C1), rotating holes compiled (B19), belts (B18, B18b); the jet retired; B12 v3 decided.
- **The plane** (docs/plane.md): one star system, flyable: the nose starts prograde, impacts are warned, braking is a fall, zero refusals in the sweep; stutter from L8 up (F1 in flight). B13 60/64 (baselined red), B17 passes at step 6, E9 fails phase 1 as designed, B14 times out.
- **The lab:** GLM on agonbox, continuous, with its memory in `lab/wiki/` (topic pages compiled from the runs, certificates, an index); read the index before any dossier.
- Older history is in git and `docs/HISTORY.md` (H0216 for the week's review).

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
