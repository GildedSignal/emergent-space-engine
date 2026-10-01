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
| **Deep research** (Julien runs it) | Prompts in `artifacts/runs/deep-research/prompts.md` (6, ranked) | Waiting for Julien | Save results beside the prompts; the integrator reads them against the plane's bottlenecks |
| Done and merged (details in git and the journal) | — | The judge: B11–B14 and B16–B18 with amendments (Sonnet). Debug views: `xtask fly` (port 8787) and `xtask galaxy` (8791; its seeded families are a debug shortcut, not the engine's representation). Events: events2 merged; events3 (`wt/events3`) and the binary doll (`wt/events4`) killed, and their lesson is the law's compiled drift plus kicks | —. Also merged: the compiler at every scale (Astra), its hardening and native light (Sol), Metal frames and the Metal pairs fix (Sonnet), the encounter research crate (Binet cone, Opus) | — |
| Cloud lab routines (environment `env_01BCjo9H1taF3eduHZyyN6L9`, Haiku hosts). Set a prompt with RemoteTrigger `update` `session_request.events`, then `run`, then read with `get_run_log` | `glm-lab-host` canaries `trig_012YxdRn25mf2h673Uu1NVDs` (session `cse_01JhqfDNthmB2u8vrGSjhTVk`); `glm-lab-redteam` `trig_017XTQzxJsZ1WBEy9mGervpA` (session `cse_019bBBmLQwRtnUqyNuZVXUq8`); `glm-lab-r1` `trig_01VfvZpHwu7yZawZ4PvCSkJi`; `-r2` `trig_01TVq7bRzcCEwmVL91LGGm5n`; `-r3` `trig_01LgS8QKML9YV1KNKY72hKAg` | **Canaries validated.** **The cloud hosts are Claude (Haiku) sessions, so they stop when Claude's weekly limit is hit (it happened at 00:46 on 30 September).** Re-fired on 30 September at 07:32 UTC: r7 (`cse_013Rqhb6GxfzAW41aFTzngSU`), r3 v3 (`cse_01B9B2ujs9yNhaFU5JRob5Zw`), r4 v2 (`cse_0138xisJ9HaAcKK35GbX5SMr`); read with `get_run_log` or from the `claude/lab-20260930-*` branches. **1 October:** r9 KILL (averaged tides: precession right only below τ₀ = 0.0036; tori 4.6%); r4 v3 KILL (normal forms); the law's red-team silver (adopted: B16–B18 and amendments); the autonomous lab reached silver, so it stays daily at 22:50. **Scheduled:** r8 v3 (independent check of the Binet cone) at 09:05 (`glm-lab-r8`). **Lab review (approved by Julien, 30 September; the measure is speed to the finished product, and overhead costs the integrator's attention):** no gold yet, and about half the rung verdicts were VOID or DISPUTED (criteria errors, quotas). If the autonomous lab's next six runs give no silver, cut it to once a day and keep GLM on directed probes and pre-freeze red-teams. Red-team silver (H0203). r2 KILL (H0204). r1: DISPUTED and VOID, but Binet m16/m32 pass on the checker's reproduction (H0205). r4 v1: KILL. r3 v2: DISPUTED (precession unjudgeable, the integrator's error; references unconverged; ν 0.98996). **GLM's 5-hour quota was exhausted** at about 21:15 UTC, so the r1 re-run and r4 v2 came back VOID with 429s (H0206). **Scheduled (UTC):** r7 (AI cost) at 00:45 (`trig_01VfvZpHwu7yZawZ4PvCSkJi`; replaces the r1 re-run, since Astra's integer law under behave supersedes it); r3 v3 at 00:47 (`trig_01LgS8QKML9YV1KNKY72hKAg`); r4 v2 at 00:49 (`trig_014CaYySK2KbYhTbvpYuJCh3`); the library lens at 05:50 (`trig_017XTQzxJsZ1WBEy9mGervpA`; `READWISE_TOKEN` is in the environment). **The autonomous lab** `glm-lab-auto` (`trig_01FegVr1kEuaAJDdvkhVDNU9`, cron 10:50/15:50/20:50 UTC) runs `lab/auto.sh`: three rotating free-lens runs per window. The integrator reads only gold | Read the DONE lines (`get_run_log`), then only the check.md abstracts. PASS on r1–r3 means the law begins (Opus); a KILL means re-probe the killed configurations within the rung's budget |
| `xtask engine-judge`: OpenAI's independent judge of Claude's `crates/engine` (E1–E8) | Merged (gpt-6.1-sol); evidence `artifacts/evidence/engine-judge-20260930/` | E1, E2, E5, E6 (4/4 mutants), E8 pass. **E3 fails** (linear epicycle tube, 12.7%; known; fixed by the exact tube with the events layer). **E4 fails** (re-anchor rotation rounds member and tube terms separately: no momentum ledger, so momentum random-walks). **E7 fails** (`Battle::outcome` omits the unanchored frame's parameters: equal digests, different futures) | E7 fixed (815f354). E4 (momentum ledger) and E3 belong to the linear-epicycle stand-in: not patched; the frame's exact tube (after the events layer) must pass both. **Sol's next job is ready:** `artifacts/runs/sol-events/` (dolls, tubes, one queue, handoffs, tides, binaries, judged by B11–B14); launch once `wt/cycle` and `wt/behave2` are merged, from `/private/tmp/emergent-wt-events` on `wt/events` |
| Reuse what the pivot retired | Merged (4756bbc; Sonnet; `artifacts/runs/sonnet-archive/result.md`): the certified bank (212,408 Arb answers) is a regression example (`cargo run --release -p emergent-space --example certified_bank -- RUNG --out DIR`); bound orbits 99.97% within behaviour, capture never wrong; its one panic is fixed | **Found:** passages lose precision silently beyond window/periapsis 10⁹ (a Q62 phase word, a Q48 k); the whirl cliff is in the inverse fit (`fit_key` near a double root); refusals at exact ties (E = 1, circles at r = 4M); near-ISCO plunges not supplied. **Reuse queue, pulled when the plane's bottleneck asks:** (1) the Arb judge scripts (python-flint is still in `.venv`); (2) Astra's v0 plunge, radial and horizon charts (law item 7; large; highest value); (3) the exact near-double-root inverse; (4) exact tie predicates; (5) save and load | — |
| **Engine judge update** | Sol, `wt/judge2` (1c45cad, pushed; not merged) | E1 with Metal, run by the integrator outside the sandbox: **FAIL, 6156/6480**, a real GPU-against-CPU divergence that Sonnet's own tests missed (the fix is running, below). E6's mutant renamed to tide-row. E1/E3 kept as Newtonian fixtures. **E9 (the GR tide) built but unfrozen:** its red-team runs on GLM (lens `redteam-e9`, `glm-lab-redteam-e9` at 10:12 UTC) | After the red-team: freeze E9, run it on the engine; merge with the Metal fix |
| **GLM re-fired** (the hosts died at 10:21 UTC with Claude's 5-hour window): r10 at 14:10 (`glm-lab-r10`), the E9 red-team at 14:12 (`glm-lab-redteam-e9`), r8 v3 at 14:14 (`glm-lab-r8`) | cloud | Scheduled | r10 decides the plane's motion bullet; E9 freezes after its red-team; r8 v3 verifies the Binet cone |
| **Ships in memory** | Merged (research crate `crates/shipmem`, Claude Opus); `artifacts/runs/opus-shipmem/result.md` | Program plus scars wins for exact programs (convoy: 488 B per 10⁶ ships; 1/100 kicked: 0.62 bits per ship); packed blocks otherwise (realistic non-program populations: 16–30 bits per ship); random traders and battle members: 150–210 bits (19–25 GB at 10⁹). No cliff. Not built: handoffs, merges, the SSD tier. **Julien decides:** do independently born ships keep a stable identity (17.7 bits each)? | Fold into the engine when populations meet the events layer; the SSD tier with causal prefetch |
| The Fermi frame, phase 1 | Merged (aa207c3; Claude Sonnet; `artifacts/runs/sonnet-fermiframe/result.md`) | Engine-judge E1–E8 PASS: E3 12.7% → 0.28% (shape 0.53%), E4 momentum delta → 0. (1) The lattice rebase-revision bug is **fixed** (aa1c6ea: one rule in all three steppers; the workaround is deleted). **Open:** (2) `crates/space`'s remainder is not a transport law (4000 rebindings drifted 36,000 units; a carried sub-quantum rotation gives 21) (Astra); (3) the epoch angle shrank to 2^-8 (4× kicks): a fourth-order force-gradient kick is the cure; (4) for the judge's owner (Sol): E1 and E3's scenes run frames at 0.24c and "16c", so they are not GR-consistent; E6's "coriolis" mutant now means a corrupted tide row | Phase 2 (Schwarzschild tide, geodetic precession; E9) per `artifacts/runs/next-fermiframe/contract.md` |

## Headed next (in order; approved by Julien)

The pivot plan: `~/.claude/plans/whimsical-snuggling-graham.md`, reordered by Julien on 30 September to fly early (Skunk Works: the builders sit by the shop floor, reports are minimal, the builder tests its own product, and the product flies early). The design is [representation.md](representation.md) (DRAFT). **No time estimates, ever** (Julien, 30 September): progress is stated as a rough % and principles. **The guard against drift:** a step whose builder passes no new gate across two consecutive work windows stops and is re-derived from the goal.
**Now: the plane flies** (f77c660, H0210; [plane.md](plane.md)). Fly it with `cargo run --release -p xtask -- universe --rtf 100` at http://127.0.0.1:8792/, or measure with `--bench`. **The measured bottlenecks, in order, drive the next jobs:**
1. The fleet battle is stepped forever: leavers are never handed into the doll, and the frame's origin takes no parent tide. Sonnet (`artifacts/runs/sonnet-plane2/`).
2. The view gather is 83% of a light frame. Cache per emitter: Newton from the last frame's crossing. Sonnet, same job.
3. A kick costs 29 µs, 15 of them in rebinding fit and compile. Sol (`artifacts/runs/sol-kick/`).
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

Gates are frozen before their first run, tests take ≤ 60 s, and speed is reported as a real-time factor, measured like the player (heat included, state recorded). The spine (contracts, builds, merges) runs one job at a time; the GLM lab runs in parallel in the cloud.

**Budgets (30 September):** Codex reset to 0%; `gpt-6.1-sol` is the default OpenAI model (close to Astra, about 5× cheaper), with Astra kept for the hardest exact problems. GLM: 1%, cloud only. Claude: lean; the integrator reads verdict lines and gold abstracts only. Check each provider's usage before assigning (AGENTS.md).

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
