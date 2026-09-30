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
| Cloud lab routines (environment `env_01BCjo9H1taF3eduHZyyN6L9`, Haiku hosts). Set a prompt with RemoteTrigger `update` `session_request.events`, then `run`, then read with `get_run_log` | `glm-lab-host` canaries `trig_012YxdRn25mf2h673Uu1NVDs` (session `cse_01JhqfDNthmB2u8vrGSjhTVk`); `glm-lab-redteam` `trig_017XTQzxJsZ1WBEy9mGervpA` (session `cse_019bBBmLQwRtnUqyNuZVXUq8`); `glm-lab-r1` `trig_01VfvZpHwu7yZawZ4PvCSkJi`; `-r2` `trig_01TVq7bRzcCEwmVL91LGGm5n`; `-r3` `trig_01LgS8QKML9YV1KNKY72hKAg` | **Canaries validated.** **The cloud hosts are Claude (Haiku) sessions, so they stop when Claude's weekly limit is hit (it happened at 00:46 on 30 September).** Re-fired on 30 September at 07:32 UTC: r7 (`cse_013Rqhb6GxfzAW41aFTzngSU`), r3 v3 (`cse_01B9B2ujs9yNhaFU5JRob5Zw`), r4 v2 (`cse_0138xisJ9HaAcKK35GbX5SMr`); read with `get_run_log` or from the `claude/lab-20260930-*` branches. **30 September:** r4 v2 KILL (arc kicks). r3 v3 silver (the two-body doll confirmed; its handoff criterion was the integrator's weakness). r8 VOID (out of time), so **r8 v2 runs at 17:45 UTC** (`glm-lab-r8`; adds the hier-bounds candidate; 90 min). The autonomous lab moved to once a day at 22:50 UTC, so that the 17:45 window stays engine-directed and within 3 runs; its six-run review now spans two days. The library lens gave a lead, on AI, which is off focus. **Lab review (approved by Julien, 30 September; the measure is speed to the finished product, and overhead costs the integrator's attention):** no gold yet, and about half the rung verdicts were VOID or DISPUTED (criteria errors, quotas). If the autonomous lab's next six runs give no silver, cut it to once a day and keep GLM on directed probes and pre-freeze red-teams. Red-team silver (H0203). r2 KILL (H0204). r1: DISPUTED and VOID, but Binet m16/m32 pass on the checker's reproduction (H0205). r4 v1: KILL. r3 v2: DISPUTED (precession unjudgeable, the integrator's error; references unconverged; ν 0.98996). **GLM's 5-hour quota was exhausted** at about 21:15 UTC, so the r1 re-run and r4 v2 came back VOID with 429s (H0206). **Scheduled (UTC):** r7 (AI cost) at 00:45 (`trig_01VfvZpHwu7yZawZ4PvCSkJi`; replaces the r1 re-run, since Astra's integer law under behave supersedes it); r3 v3 at 00:47 (`trig_01LgS8QKML9YV1KNKY72hKAg`); r4 v2 at 00:49 (`trig_014CaYySK2KbYhTbvpYuJCh3`); the library lens at 05:50 (`trig_017XTQzxJsZ1WBEy9mGervpA`; `READWISE_TOKEN` is in the environment). **The autonomous lab** `glm-lab-auto` (`trig_01FegVr1kEuaAJDdvkhVDNU9`, cron 10:50/15:50/20:50 UTC) runs `lab/auto.sh`: three rotating free-lens runs per window. The integrator reads only gold | Read the DONE lines (`get_run_log`), then only the check.md abstracts. PASS on r1–r3 means the law begins (Opus); a KILL means re-probe the killed configurations within the rung's budget |
| Lab rung mode, `lab/verdict.py`, canaries | Merged (a3d40e9); worktree and branch deleted | Done | — |
| Astra: `crates/space` | `wt/cycle`: window 1 is b35a67b (G1–G4 and G6 pass, G5 fails); window 3's work in progress is 6d64903 (near-circular local frame, profiler, sweep test; unverified). **Codex weekly limit until 5 October, 12:49** | Opus replaced the in-band map with law `space-darwin16-v1` (9b23fb1): **G1–G6 all pass** (advance 1.15e-6, periods 7.2e-7, G5 32/32); 3 new near-circular tests fail; speed unmeasured. Claude's window ran low, so **Astra took it back at about 08:35 UTC** (`prompt-4.md`, `launch-4.sh`, result `result-4.md`): review, the 3 tests, speed (≤ 50 µs per compile, ≤ 1 µs per crossing), the bound, a public API for Sol's events layer | Review; merge `wt/cycle` and `wt/view` once G1–G6 pass; Astra reviews when Codex returns |
| `xtask engine-judge`: OpenAI's independent judge of Claude's `crates/engine` (E1–E8) | Merged (gpt-6.1-sol); evidence `artifacts/evidence/engine-judge-20260930/` | E1, E2, E5, E6 (4/4 mutants), E8 pass. **E3 fails** (linear epicycle tube, 12.7%; known; fixed by the exact tube with the events layer). **E4 fails** (re-anchor rotation rounds member and tube terms separately: no momentum ledger, so momentum random-walks). **E7 fails** (`Battle::outcome` omits the unanchored frame's parameters: equal digests, different futures) | E7 fixed (815f354). E4 (momentum ledger) and E3 belong to the linear-epicycle stand-in: not patched; the frame's exact tube (after the events layer) must pass both. **Sol's next job is ready:** `artifacts/runs/sol-events/` (dolls, tubes, one queue, handoffs, tides, binaries, judged by B11–B14); launch once `wt/cycle` and `wt/behave2` are merged, from `/private/tmp/emergent-wt-events` on `wt/events` |
| **The flyable slice v0** (`xtask fly`) | Merged (ad250ab, a107f24); run `cargo run --release -p xtask -- fly --seed 1 --c-scale 200` and open http://127.0.0.1:8787/ | Julien flew it: "just a blob", "doppler … feels like a bandaid". Measured: Doppler is −p·u (emergent); the bandaid is painted object colours, and the world is too small | See fly v1 |
| `xtask galaxy` (debug god's view; its seeded families are a debug shortcut, **not** the engine's representation: every body is real) | Merged (39f2fde, Claude Sonnet); `cargo run --release -p xtask -- galaxy`, http://127.0.0.1:8791/ | 10⁹ ships as seeded families: about 8 ms per frame, flat in ship count; 10⁶ tubes: 7.6 ms. **Engine findings:** (1) `Tube` lacks its key and orientation, so the contract is now fixed in `docs/law.md` (key index, periapsis angle, periapsis time; 16 bytes); (2) memo hits need a coarse key: how coarse (E, L) can be while G1–G6 pass is open (Astra); (3) the exact readout costs about 9 µs, so drawing uses a display cache | Align `crates/space`'s Tube at the events review; give the key-width question to Astra |
| `behave` B11–B14 | Merged (Claude Sonnet; 35e4c76). All 13 gates run by default; echo passes all; planted laws fail theirs. B10 flaked (exponent 1.10–1.14 against 1.10) when three full runs shared the machine at load 8 | `wt/events` has the first cut (912816e) merged; merge main into it at review |
| **The events layer, first cut** | Merged (082f352; gpt-6.1-sol) | G1–G6, B7, B9, B10 (exponent 0.987; 10⁹ undisturbed orbits extrapolate to 0.16 core-s per game-s, real-time factor 49 on 8 cores), **B11 binaries PASS**. B12–B14 FAIL: the compiler's envelope stops short of planetary scale (L cap 4096, Q20 periods overflow); no unbound readout, rebinding or integrated tidal arc | Astra's envelope (below), then Sol: rebinding at handoffs, tides with the τ selector (`docs/law.md`), B12–B14 |
| **Ships in memory** (Julien: compress as far as information allows, losslessly, grouped by description — "orange left, right" — laid out by causality, decompression fast; 10⁹ real ships vs 8 GB) | Claude Opus research sub-agent, `/private/tmp/emergent-wt-shipmem` (`wt/shipmem`); `artifacts/runs/opus-shipmem/` | Running (about 14:40 UTC; Claude's 5-hour window at 75%, so it may pause and resume after 17:30 UTC) | Review; fold the representation into the law's contract (Tube, frames, layout) |
| **The compiler at every scale** (envelope to r/M 10¹² with an explicit exponent, unbound passages, exact rebinding that never walks, the Tube contract, key width and memo hit rate) | gpt-6-astra, chained to start at the Codex reset (about 17:38 UTC) in `/private/tmp/emergent-wt-envelope` (`wt/envelope`); `artifacts/runs/astra-envelope/` | Waiting for the reset (Codex's 5-hour window at 95%) | Review; commit if the sandbox blocks it; merge; then launch Sol on rebinding and tides |
| Re-anchoring for battle frames | Merged (542c9e5) | Done. 10 periods at dr/R = 1e-3: 0.44% re-anchored against 19.8% without; random walk 0.96 dr against 332 dr; orders bit-identical | Open: the frame's tube is a linear epicycle (12% drift over 10 periods for drift-free releases), so it needs the parent's exact tube from `crates/space`; near-c bodies refuse Galilean shifts; handed-out bodies get no tide |
| `xtask view`: a behaviour viewer (an HTML page from the integer law) | Built on `wt/view` (8566fd8, which merges `wt/cycle`); page at `/private/tmp/emergent-wt-view/artifacts/view/space-behaviours.html`, sent to Julien | Done. It found near-circular precession off by 1–7% and e = 0 failing to compile; both are queued for Astra's window 3 | Merge with `wt/cycle` once G5 passes |
| Dense order, first cut: `crates/engine` free-fall battle frame | Merged (4837b47, Claude Sonnet) | Done: lockstep and sparse bit-identical on 8 scenes; Clohessy–Wiltshire to 8.6e-5; sparse about 12× faster | Next: re-anchoring (members drift; the linear tide is 2% off after one period at dr/R = 1e-3); OpenAI builds its judge |
| `xtask behave` gates B7/B9/B10 (clocks, cost per body, cost against N) | Merged (7f7ad68); `echo` passes all nine gates; each planted law fails its own gate | Done | — |
| Rung criteria r1–r3 (frozen) | Integrator, `lab/rungs/` | Written and frozen | r5–r7 next; no rung runs before the canaries grade correctly |
| Retired v0 gravity (`wt/geodesic`, `wt/g2run`, `xtask/src/gate/`, `xtask/judge/`) | Archive bundle `retired-v0-gravity-20260929.bundle`; the rest recoverable at fa4b547 | Done | — |

## Headed next (in order; approved by Julien)

The pivot plan: `~/.claude/plans/whimsical-snuggling-graham.md`, reordered by Julien on 30 September to fly early (Skunk Works: the builders sit by the shop floor, reports are minimal, the builder tests its own product, and the product flies early). The design is [representation.md](representation.md) (DRAFT). **No time estimates, ever** (Julien, 30 September): progress is stated as a rough % and principles. **The guard against drift:** a step whose builder passes no new gate across two consecutive work windows stops and is re-derived from the goal.
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
