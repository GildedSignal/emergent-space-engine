# Emergent Space — handoff

Current as of 29 September 2026 (H0197, plus the doc reconciliation on `wt/reconcile`). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

## First ten minutes

0. Read "In flight" below first: what is running, where its output lands, and what to do when it finishes.
1. Read [PRINCIPLES.md](PRINCIPLES.md), [AGENTS.md](../AGENTS.md), then this file. Run `cargo xtask history list` and search for entries related to your task.
2. Read the heading card [CARD.md](CARD.md), then preflight.
3. Run `git status --short` and `git log -8 --oneline`. There is one checkout, `~/Research/emergent-space`, on `main`.

## In flight (overwrite when jobs change; the first thing to read after a compaction)

Job files: `artifacts/runs/<id>/` (on disk, not in git: prompt, launch or resume script, log, result). As of 5 October, 10:30 UTC. **Codex is out until Friday 9 October, 21:14 UTC (99% of its week)**: no Sol or Astra until then; Claude and GLM carry the work. The off-time lab (1–5 October) gave 39 results; the decisions are in `lab/board.md`'s taste log.

| Job | Who, where, how to resume | State | When it lands |
|---|---|---|---|
| **The plane judged by the frozen gates** | GLM directed build `q-plane-judge` (first in `lab/queue.txt`, window 10:20 UTC); its patch comes back in `lab/results/<id>/work/patch.diff`; the integrator reviews it and applies it in `/private/tmp/emergent-wt-plane-judge` (`wt/plane-judge`). Also a test of GLM as a builder (Julien asked how GLM compares with Sol) | The API exists now (masses with a mantissa, the origin's fall, `add_body_state`) | Review the patch, rerun the sweep on the M1, merge. If B12 fails at every step, the changeover is re-derived (Astra, after 9 October) |
| **The plane's frame tails** | Sonnet (same background agent, resumed; it notifies), `/private/tmp/emergent-wt-plane3` (`wt/plane3`) | Merged before this job (795c005, H0213): masses with a mantissa and the origin's fall (a physics fix; digests changed), exact replays, ties, the relativistic gather cache. Its regression, measured A/B under equal load: 3–5 hitches per run (worst 33–51 ms) where main had 0–1; the engine's worst frame 17.5 → 29.7 ms; fleet kicks +38%. Now: bound the bursts (foundation 7), the gather's worst frame, and the +38% | Interleaved A/B again; merge if hitches are back to 0 with the digest unchanged across budgets |
| **GLM (cloud; it never notifies)** | GitHub Actions `glm-lab`, every 5 hours (`gh run list --workflow glm-lab.yml`); results on `origin/claude/lab-*` | Queue (`lab/queue.txt`): r8 v3 again (120 min), q-cadence (a per-body cadence from dimensionless numbers), the phase-2 tide reference and red-team (second authors); then the lens rotation | Read the DONE subjects (`git for-each-ref refs/remotes/origin/claude/lab-*`), gold abstracts first |
| **The belt (Julien: "ok for the belt")** | Sol's belt on `wt/belt` (a2b777c, pushed). Sonnet's judge, B18b, on `wt/b18-belt` (af07b33, pushed; runs only when named until frozen: freeze = add `B18b` to `select::ALL` and drop the explicit-name guard in `judge_only`); interface `Law::belt_birth`, `belt_restore`, `Belt::{body, store, bytes_used, scar, form}` | The judge fails the lab's original 2¹²-cell table on tails (0 of 105 extreme e), as Julien feared; Sol's port changed the table (it reports 3.3σ worst). Open for the red-team: "the program's information" is self-declared | After the GLM red-team (window 10:20): settle it, freeze B18b, write the thin adapter from crates/shipmem's belt to the interface, judge `wt/belt`; merge both only if it passes |
| **Rotating holes (Julien: "especially rotating black holes")** | Gate B19 in law.md; its judge: Sonnet (background agent; `/private/tmp/emergent-wt-b19-kerr`, `wt/b19-kerr`; `artifacts/runs/sonnet-b19-kerr/`); its red-team and a float reference compiler (`q-kerr-compile`): GLM queue | Running. The compiler itself is Astra's, from 9 October 21:14 UTC, in crates/space, starting from GLM's reference | Freeze B19 after its red-team; brief Astra with the reference; χ = 0 must keep every Schwarzschild digest |
| **Gravity at c (Julien: "we can't get lazy here")** | law.md "Gravity travels at c" (gravity is news); GLM falsifier `q-gravity-at-c` (queue) | Waiting on the falsifier | With B12's measurement, it defines the motion law v2 (news, a reversible integer handoff, the cadence), Astra's after the compiler |
| Next, not started | — | **The Fermi frame's phase 2:** E9 (frozen, merged) fails the phase-1 tide at r_p/M ≤ 1000 (eccentric), ≤ 100 (circles), while E1–E8 pass; the closed form is lab q-fermi2-tide, with its second author queued. Encounters (q-skin: a slack skin is exact in its regime and cuts setups per kick 12.6×; the literal skin is killed; lab taleb-3ec1: 99% of setup work lands on dormant pairs, defer it); Fermi phase 2 after E9 (closed form from q-fermi2-tide) | Pick by the plane's measured bottleneck |
| Done (details in git and the journal) | — | The plane (H0210, H0211); the compiler at every scale, its hardening and native light (B16); the judge B9–B18; Metal frames; Fermi frame phase 1 (E1–E8); ships in memory (`crates/shipmem`); encounters research; the certified bank; GLM's own host (H0211) | — |

**Traps that bit us (read before acting):**
- When a sandboxed Codex builder can't commit: `git status`, then `git add -A` the whole worktree, build main, then push and remove. Once only `crates/` was added, and an adapter was lost with the worktree.
- GLM's Claude-hosted routines died with Claude's windows (three times): GLM now runs on GitHub Actions, never on a Claude host.
- Codex may fail on "model at capacity" or on its 5-hour limit: resume with `codex exec resume <session id from log.txt>`, never restart.
- Gates are frozen before builds and never sized to a representation. Write criteria passable in principle, with controls on both sides. The integrator's criteria errors (r2, r3, r8 v2, τ) were all caught by checkers.
- Never speak in days; pace by the 5-hour window; AI is off the plan; every body is real (no averaging populations).

## Headed next (in order; approved by Julien)

The pivot plan: `~/.claude/plans/whimsical-snuggling-graham.md`, reordered by Julien on 30 September to fly early (Skunk Works: the builders sit by the shop floor, reports are minimal, the builder tests its own product, and the product flies early). The design is [representation.md](representation.md) (DRAFT). **No time estimates, ever** (Julien, 30 September): progress is stated as a rough % and principles. **The guard against drift:** a step whose builder passes no new gate across two consecutive work windows stops and is re-derived from the goal.
**Now: the plane flies** (f77c660, H0210; [plane.md](plane.md)). Fly it with `cargo run --release -p xtask -- universe --rtf 100` at http://127.0.0.1:8792/, or measure with `--bench`. **The measured bottlenecks, in order, drive the next jobs:**
1. The fleet battle is stepped forever: leavers are never handed into the doll, and the frame's origin takes no parent tide. Sonnet (`artifacts/runs/sonnet-plane2/`).
2. The view gather is 83% of a light frame. Cache per emitter: Newton from the last frame's crossing. Sonnet, same job.
3. A kick costs 29 µs, 15 of them in rebinding fit and compile. Sol (`artifacts/runs/sol-kick/`, worktree `wt/kick`). It hit an OpenAI "model at capacity" error mid-run, and `resume.sh` retries every 3 minutes. Its uncommitted work also touches `xtask/src/universe/` (a kick bench), so expect a merge with Sonnet's `wt/plane2`.
4. The player's encounter check costs 190 µs per item. The Binet-cone seam (`crates/encounters`) comes after (3).

Open from the first flight: readouts between kicks carry the pending half kick (Jacobi 6e-3; an ignored test); a doll's far time lacks its centre's rate (about 1e-8); kick sources are a function, not a trait; there is no lensing or retarded gravity.
0. **The lab:** done.
1. **The float falsifier ladder:** r1 and r2 done; r3 v3, r4 v2, r7 running; r8 queued. Only r3 and r4 gate the law.
2. **The law** `docs/law.md` (`es-space-v2`) and gates B0–B14. The freeze comes once the space law passes its gates, r3 and r4 are judged, and the GLM red-team is answered.
3. **The core, one mass:** `crates/space`, the exact cycle compiler (Opus now).
4. **The events layer:** dolls, tubes, one queue, handoffs, tides, binaries, judged by B11–B14 (Sol next).
5. **Debug views only** (Julien, 30 September: "the only goal is the engine/compiler to work with GR natively"; the real visualization comes later). `xtask fly` (merged) and `xtask galaxy` (minimal, for scale measurements) exist to see the engine, not to polish. Known for the real view: objects carry painted colours; the emergent version is one scatter of starlight, −p·u twice.
6. **Scale,** in parallel with the slice: encounters and contacts (r8), N bodies, B10 on the M1, the dense order on Metal.
7. **AI: not now.** Julien is still ideating on AI (30 September), so no AI work in this phase. r7, already running, is filed when it lands, and nothing is built from it.
8. **Retirement and ladder v8,** last, once B8 digests match across orders, threads, CPU/GPU and sabotage.

**Decided by Julien (29 September):**
- The law is a cheap, local, fixed integer algorithm. Exact GR is the oracle, not the implementation (H0195).
- Gravity is a field held by cells. Multipoles are the mechanism, including aggregates of ships.
- Observables (clocks, redshift, lensing) are derived on demand, never evolved.
- One engine, not five modes; the chronon survives only as a test judge.
- Behaviour and error type over error size.
- Every statement of his is followed or disproven with evidence ([PRINCIPLES.md](PRINCIPLES.md) register). He owns PRINCIPLES.md.

## Where we are

- **Law.** `es-lattice-relativistic-v1` (H0174): exact integer special relativity with contacts, walls, carries and an exact Newtonian limit. Q ≤ 2^20 today; the target is 2^40 ([universe-quanta.md](universe-quanta.md)). Worldlines are straight between events: no gravity, no thrust, no player input yet.
- **Gravity.** The v1 contract is a draft ([gravity-law.md](gravity-law.md)).
  - GLM's red-team found the draft lacked its own equations, had two vacuous gates (B4 capture, B5) and a determinism clash with cell clipping. All are folded in.
  - Probe 1 passed precession, capture and deflection at 1%, and killed the per-body step rule on energy growth (evidence: `artifacts/evidence/gravity-v1-freeze-20260929/`).
  - The v0 exact evaluator agreed exactly wherever it answered, but ran 1,600× over budget (H0194). It is now oracle material.
- **Modes.** chronon (reference), event, metal (H0179: the 1M v1 gas takes 8.0 s per 1,024 chronons), hybrid (H0181) and regions (H0176). All five are to merge into one engine (step 4).
- **Ladder v7** (H0180–H0181). No correctness flag is false anywhere. Failing gates:
  - gas_one_million and galaxy_one_million (at the cap);
  - useful_work for event (0.48);
  - smooth for metal, hybrid and regions.
- **GR oracle** (H0178, H0183). Periapsis advance, light bending, geodetic precession, clock rates, Shapiro delay, bound periods and 1PN two-body motion, two methods each. It shares no code with `crates/`, and currently exits 1 because of the retained e = 0.5 two-body failure. Before rung 2 uses it, a new protocol is frozen on unseen cases.
- **Real-time factors.**
  - The ladder gas is a stress test: about 10⁻⁸× real time at 83 ps chronons.
  - A realistic 1M-ship battle is estimated at 10–100× real time. That is a Fermi estimate, not yet measured.
- **Done before this plan:** a clean countertop (H0182), the oracle (H0183), the step 3 premise probe (H0190), and the judge's frozen floors (H0192).

**Candidates from the polymath scan** (GLM, 28 September):
- commutative-monoid messages between regions;
- largest-remainder splits;
- choosing the error-feedback kernel by its low-frequency error;
- a replay-bisect tool for divergences;
- an LSM or CRAM-style body store for the memory floor.

## Standing decisions

- **Microstates are canonical.** Entropy only schedules, and observation never changes outcomes.
- **Everything is emergent** ([PRINCIPLES.md](PRINCIPLES.md)). There is no central control, and no object categories: regimes are chosen by dimensionless numbers.
- **The memory floor is information-theoretic** (entropy given shared structure), not bytes × count.

## Risks to attack first

- **What cells add for many sources.** Moments add; the flow does not (β ∝ √M). The β rule must be curl-free for static sources and pass 1PN.
- **A cell-owned step rule** with bounded energy error that bends distant light: this is the re-probe.
- **Cost at a billion.** A billion ships all in 90-minute orbits would need about 190 cores at B9's rates (the red-team's 0.19 core per million, times 1,000; a Fermi estimate). B10 must show where a real scene sits, and events per orbit or cost per event may need to fall 10–100×.
- Contacts between curved paths, and retarded moments across very different scales.
- The light cone keeps growing (Julien: "there will always be a point where we cannot handle the universe anymore").
- The approved plan's budgets (4 GiB, 30 FPS at 1080p, one hour, 20 GiB) are open, not dropped. 20 GiB exceeds the free disk.

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
