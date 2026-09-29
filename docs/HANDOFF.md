# Emergent Space — handoff

Current as of 29 September 2026 (H0197, plus the doc reconciliation on `wt/reconcile`). The previous handoff, with the old engine's status (H0100–H0164), is in git history and in `~/Research/emergent-space-archive/old-lineage/docs/HANDOFF.md`.

## First ten minutes

0. Read "In flight" below first: what is running, where its output lands, and what to do when it finishes.
1. Read [PRINCIPLES.md](PRINCIPLES.md), [AGENTS.md](../AGENTS.md), then this file. Run `cargo xtask history list` and search for entries related to your task.
2. Read the heading card [CARD.md](CARD.md), then preflight.
3. Run `git status --short` and `git log -8 --oneline`. There is one checkout, `~/Research/emergent-space`, on `main`.

## In flight (overwrite when jobs change; the first thing to read after a compaction)

Job files: `artifacts/runs/<id>/` (on disk, not in git). Older prompts and outputs are in `/private/tmp/claude-501/-Users-julien-laurent-Documents-ChatGPT-Emergent-space/3cb5f6e5-821c-4ee2-b72f-493db869d774/scratchpad/` (lost on reboot).

| Job | Who, where | State | When done |
|---|---|---|---|
| Probe 2, the float re-probe of cell-owned steps | GLM (local, the last local run); output `artifacts/runs/gravity-v1-reprobe/out.md`, data `/private/tmp/glm-scratch/gv1b/` | **Done:** no configuration passes; shell crossings inject energy error; a fixed step costs 3–300× too much | Freeze the evidence; re-derive step 2 around generators with multipole kicks (the lab's first question) |
| Prior-art scout: how others own time steps by cell, not body (block steps, asynchronous variational integrators, Wisdom–Holman, patched conics) | GLM, sandboxed; prompt `artifacts/runs/prior-art-timestep/prompt.md`, output `.../out.md` | Running | Read with probe 2's result before choosing the step rule |
| GLM lab (`lab/`): lenses, runner, independent checker | Integrator; cloud routines once Julien's cloud environment holds `ZAI_API_KEY` | Built; waiting for the environment | Create one routine per lens (host model Haiku, `lab/run.sh start <lens>`); read gold abstracts only; log decisions in `lab/board.md` |
| Julien's yes on CARD.md, and his choice on world coordinates (answered 29 September: exact integers set no distance limit; hierarchical local coordinates proposed) | Julien | Asked 29 September | Record it in the register; fold it into universe-quanta.md |
| `crates/geodesic`, the exact evaluator (now oracle material, H0195) | Astra, `/private/tmp/emergent-wt-geodesic` (`wt/geodesic`, parked at 1a8d526) | **Parked, not running.** Window 7 ran 09:00–09:31 and stopped at the Codex limit (`artifacts/runs/astra-geodesic/log-7.txt`) | Not in flight. The integrator decides: keep it as an oracle component or archive it. Do not re-climb G2 |
| `xtask gravity-gate` (the v0 G2 gates) | Merged (H0193); its throwaway adapter lives in `wt/g2run` | Parked | Reuse its watchdog and state recording in `xtask gravity-behave`; then delete `wt/g2run` |

## Headed next (in order)

The design is [representation.md](representation.md) (DRAFT). Each phase has a budget; an overrun means re-deriving the phase from the goal.
0. **Unblock the cloud lab** (Julien sets the `glm-lab-probe` routine's environment). The lenses then attack the design.
1. **The float falsifier ladder** (§7 of the design; about a week, at most a day per rung, kill criteria frozen first). GLM lab plus Sonnet, in the cloud:
   1. rings;
   2. carry width;
   3. many sources;
   4. crossings between levels, and moving sources;
   5. the dense order in a Clohessy–Wiltshire frame;
   6. the view's gather.
2. **The written integer law and its gates** (2–3 days): dolls, rings, the resolver, carries, number forms, with behaviour gates and cost against N up to 10⁹. Claude Opus writes them and Astra reviews while Codex is above 75%.
3. **The core, in one code base for every rung** (about two weeks): one mass, then two, then N, then scale.
   - `es-lattice-relativistic-v1` becomes the resolver, `lattice-event` the sparse order, `lattice-metal` the dense order, and `allocator` the queue.
4. **One engine:** the five modes become the two orders. Ladder v8: physically scaled scenes, the real-time factor, cost against N.
5. **The view** (gather at the past light cone, the spectral table), then **the player slice** (one ship, thrust, save and replay).
6. **AI and populations** (families, seeds), then debris, Kerr and inspiral.

Gates are frozen before their first run, tests take ≤ 60 s, and speed is reported as a real-time factor, measured like the player (heat included, state recorded). The spine (contracts, builds, merges) runs one job at a time; the GLM lab runs in parallel in the cloud.

**Budgets (29 September, 14:35):** Codex weekly 80%, past the 75% line (resets 5 October), so Claude Opus writes the law and Astra reviews. GLM: 5% of its 5-hour window, 1% of its month: badly under-used. Check each provider's usage before assigning (AGENTS.md).

**Decided by Julien (29 September):**
- The law is a cheap, local, fixed integer algorithm. Exact GR is the oracle, not the implementation (H0195).
- Gravity is a field held by cells. Multipoles are the mechanism, including aggregates of ships.
- Observables (clocks, redshift, lensing) are derived on demand, never evolved.
- One engine, not five modes; the chronon survives only as a test judge.
- Behaviour and error type over error size.
- Every statement of his is followed or disproven with evidence ([PRINCIPLES.md](PRINCIPLES.md) register). He owns PRINCIPLES.md.

## What the engine computes

Only surprises. The state is certified generators, compute follows entropy, and priority is least slack. See [engine.md](engine.md).

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
