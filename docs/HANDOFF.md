# Emergent Space — handoff

Current as of 6 October 2026 (H0214; the "In flight" table below carries the exact time). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

## First ten minutes

0. Read "In flight" below first: what is running, where its output lands, and what to do when it finishes.
1. Read [PRINCIPLES.md](PRINCIPLES.md), [AGENTS.md](../AGENTS.md), then this file. Run `cargo xtask history list` and search for entries related to your task.
2. Read the heading card [CARD.md](CARD.md), then preflight.
3. Run `git status --short` and `git log -8 --oneline`. There is one checkout, `~/Research/emergent-space`, on `main`.

## In flight (overwrite when jobs change; the first thing to read after a compaction)

**Autopilot, 6 to 12 October** (Claude's week is spent until 12 October, 09:00 UTC; Julien: "GLM and gpt should continue to run and not merge to main but still continue producing code ... massively in parallel ... based on bottlenecks"; "tackle real problems leading us towards a full implementation"). **Nothing merges to main while Claude is away.** Every builder works against main on its own branch; the integrator reviews on return, and the tier rule (lower tiers never edit higher-tier work) is relaxed for proposals only: a branch merges only after review by the owning tier.

| Job | Who, where | Lands | On return |
|---|---|---|---|
| **Kerr compiler candidate** | Codex, `/private/tmp/emergent-wt-cx-b-kerr-compiler`, `wt/cx-b-kerr-compiler` | `crates/space/src/kerr.rs`; tests and frozen gate detail lines in `artifacts/runs/cx-b-kerr-compiler/` | Review compiler and native catalogue, then integrate spin into the motion resolver; no merge performed |
| **GLM builds and research** | GitHub Actions `glm-lab`, the GLM job on agonbox (`ssh julien@agonbox`, user glmlab); four slots a window: three directed (`lab/queue.txt`: q-b12-design, then 14 builds `lab/lenses/b-*.md` in bottleneck order: the GR energy register, plunge tubes, the single-surface handoff, rotating holes, news gravity, the Fermi phase 2, the co-orbital certificate, the readout's cost, root-clock keys, the belt, the slack skin, B17 in parallel, γ to 10⁶, H_live), one second author on a recent silver (`second-<run id>`), free lenses when the queue is empty. Waits out GLM's 5-hour window; logs `omp usage` | `origin/claude/lab-*`: each build's code is `lab/results/<id>/work/patch.diff`, graded by an independent GLM checker | Read the DONE subjects (`git for-each-ref refs/remotes/origin/claude/lab-*`), gold first; apply the best patch per item in a worktree, rerun its gates, merge |
| **Codex lanes from 9 October 21:15 UTC** | `artifacts/runs/codex-week/runner.sh astra` and `sol`, started 6 October under `nohup caffeinate` on Julien's Mac (they need it awake on power); queues `queue-astra.txt` (the GR energy register, plunge tubes, rotating holes, root-clock keys) and `queue-sol.txt` (the belt wired to B18b, B12's statistic rebuilt as `b12-v2.md`, the co-orbital certificate, the handoff surface, the slack skin, γ to 10⁶). The same tasks as GLM's builds: two families per item | Branches `wt/cx-<job>`; per-job prompt, log and result in `artifacts/runs/codex-week/<job>/`; progress in `status-<lane>.txt`. On a usage limit a lane waits 45 minutes and resumes the session | Compare each item's Codex branch with GLM's patch; keep the better; rerun gates; merge. If the Mac slept or rebooted, relaunch: `nohup caffeinate -is zsh artifacts/runs/codex-week/runner.sh <lane> &` (done jobs are skipped) |
| **Julien's flight view: merged, green** | Main at 741d05e. The motion law v2's high-speed regression is fixed (Sonnet): the energy register `p_t` is an i128 at the same exponent (coasting digests unchanged), and a held burn caps the first step after a handoff into the root doll. Test: an L15 burn from tick 0 reaches β 0.999 with no refusal. Whole universe suite green; B13 60/64 at step 7. Known limit: braking to rest above a planet gives `NoBoundOrbit` (plunge tubes, `b-plunge-tubes`). Contents: AZERTY labels, control pads, a last-key line, a plain sentence, a stable camera, a loss that says why with R to restart | — | Julien flies it |
| **Method (draft)** | [method.md](method.md), sixth draft: attractors not rules; five states (sketch, flying, load-bearing, frozen, retired); the loop; statistical etiquette; anomalies; unknown unknowns; simplicity; the barbell; its own attractor audit. **Not in force** until Julien validates it; then its 5 changes. Deletion candidates measured on 7 October: `shipmem` and `encounters` used by nothing (about 4,500 lines); `engine`, `lattice-event`, `allocator` and `lattice-metal` reached by the plane through 3 imports plus old judges and fold test-ladder.md in | Claude | Julien reads |
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

## Headed next (from 12 October, when Claude returns; the order is the bottleneck order)

1. **Review the autopilot's branches** (table above): per item, GLM's patch against the Codex branch; keep the better, rerun its gates, merge.
2. **B12 rebuilt and frozen** (GLM `q-b12-design`, Codex `b12-v2`, Sonnet's partial `wt/b12-v2`), red-teamed first; then the plane faces B12–B14 and B17 together.
3. **The motion law v2, finished:** the GR energy register (P3'), plunge and radial tubes, the single-surface handoff (step 3), root-clock event keys (step 4), news gravity at c (`lab/refs/opus-motion/memo.md` §5).
4. **GR's weird effects, in Julien's order:** rotating holes (B19 frozen), then the Fermi frame's phase 2 (E9 frozen), then inspiral (Peters' generator).
5. **Scale:** encounters at N (the co-orbital certificate, the slack skin, candidate work per real encounter), belts and populations in the plane (B18b frozen), distinctions per game-second, B15, the galaxy doll.
6. Julien flies every merge (`cargo run --release -p xtask -- universe --rtf 100`, http://127.0.0.1:8792/). AI stays off the plan.

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
