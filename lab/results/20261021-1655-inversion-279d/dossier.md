# Dossier — 20261021-1655-inversion-279d (lens: inversion)

## Claim

The engine's canonical digest is schedule-clean at the lab's reported drift point (belt N=10⁴, rtf 6000, budgets 0.5–12 ms: **13 arms, one digest per input log, presented-at-end spanning 0.34–24.4e9 ticks**); both reported "wall-coupled digests" are instrument diseases — digesting the presented tick of an open-ended flight (c8d5), and **example harnesses injecting decisions at the presented tick** (`p.u.input(p.u.now, …)`: `nladder.rs:74`, `wall.rs:16`, `flight_sweep.rs:123`, `frame_cost.rs:35`, `frame_f1.rs:57`, `skew.rs:28`, `kick_bench.rs:68`), which forks the canon 3-ways in 3 reps under a biting budget.

## Bottleneck

Truth, not cost: "Canonical outcomes are exact and independent of … schedule" (PRINCIPLES, line 1). Every lab A/B at belt scale compares flights by digest; if the canon is a coin flip on machine load where the budget bites, those comparisons measure noise. Gain: restores digest identity as a certificate on the ratchet-class scenes (rtf ≥ 6000, N ≥ 10⁴) — it deletes the "digest identity is not an available certificate" caveat (c8d5) for every bench that schedules its inputs canonically, and it deletes the one-line hole in seven harnesses.

## Evidence (all from this tree + `truthprobe.rs`; regenerate with `regen.sh`, ~11 min)

Scene: `scenario::plane_extra` N=10⁴ (belt, 10,050 bodies), seed 1, Order::Sparse, 1 thread, rtf 6000, cut = 20 s game time = 24,363,053,610 ticks, digest after `settle(cut)`; frames flown as the page flies them (`frame_to(1/60, rtf, budget, cut)`).

**Table 1 — clean matrix (coast, no inputs, no gather), 5 arms × 2 reps:**

| arm | digest (16 hex) | kicks | encounters | presented-at-end |
|---|---|---|---|---|
| unlimited ×2 | `8e1882ff94b52566` | 223,607 | 5,843 | 24.36e9 / 24.36e9 |
| events-25 ×2 | `8e1882ff94b52566` | 223,607 | 5,843 | 3.17e9 / 3.17e9 |
| unpaced 12 ms ×2 | `8e1882ff94b52566` | 223,607 | 5,843 | 12.20e9 / 12.35e9 |
| unpaced 0.5 ms ×2 | `8e1882ff94b52566` | 223,607 | 5,843 | 0.34e9 / 0.34e9 |
| paced 12 ms ×2 | `8e1882ff94b52566` | 223,607 | 5,843 | 6.51e9 / 8.60e9 |

Ten flights, one digest, identical kick/encounter counts — while the presented path the wall controls varied 70×. Deferral is the only effect of the budget; counters and canon agree.

**Table 2 — attribution (burn at frame 60; gather every 60 frames):**

| input | reps | distinct digests at cut | kicks | distinct `digest_presented` |
|---|---|---|---|---|
| `presented` (`p.u.input(p.u.now, …)`, the `nladder` line) | 3 | **3** (`fa0d9b03…`, `2991f553…`, `3d3747e1…`) | 219,710 / 219,892 / 219,657 | 3 |
| `scheduled` (`p.u.schedule(canonical tick, …)` before the loop, the shipped `--bench` pattern) | 3 | **1** (`8233751e…`) | 219,845 ×3 | 3 |
| none, gather=60 (coast) | 3 | **1** (`8e1882ff…`, equals Table 1) | 223,607 ×3 | 3 |

- The same binary, same args, same cut: **the decision's tick is the only fork**. Presented-tick injection makes the canon a function of where the wall left the frame budget when the decision landed.
- `digest_presented` (digest where the wall stopped, no settle — c8d5's instrument) is distinct on every rep of every arm, including the fully stable ones: it is not a certificate of anything but the wall.
- Observation is read-only confirmed: gather-in-loop changes no canonical bit (Table 2 row 3 = Table 1).
- Shipped surface control: `xtask universe --bench --seed 1 --rtf 6000 --seconds 20 --engine-ms 12`, run twice → **same digest `2570285099568434`** at cut 24,363,053,611 (11 decisions at canonical ticks) while the presented tick differed by 81M ticks of wall noise (23.796e9 vs 23.877e9) — the shipped player-facing path uses the safe pattern (`canonical_log`) and its digest is a certificate at this scene.

## Predictions

`predictions.md` was written before the clean matrix and extended before Table 2 was read. **P1 held** (all clean arms one digest), **P6 held** (presented forks ≥2 digests, scheduled gives 1), **P7 held** (digest_presented drifts everywhere, digest at cut does not), **P8 held** (gather read-only). P2/P3/P4/P5/P9 (leak mechanisms in the engine, load stress) were not triggered because the engine never leaked; the loaded paced arms were subsumed by the paced pair's own 6.51-vs-8.60e9 presented spread (wall noise entered, canon did not move).

## What would make it wrong

- A scene where resolution order itself leaks (my arms all reach the cut through `settle`): a flight cut mid-encounter or mid-fleet-slice with **no** final settle could still expose queue-order sensitivity; I did not fly one (the design comments claim the cap logic prevents it, and 13 arms never tripped it).
- The presented-tick hole could bite the *shipped* session too (`session.rs:120` injects live keys at `u.now`): for a live player this is arguably the press's own tick and the recorder/replayer pair is self-consistent, but a bench that passes scripted keys through `Session::step` would inherit the fork. `--bench` does not (it schedules); `kick_bench.rs` does.
- c8d5's drift could have a second cause their patched keep-dial introduced; I reproduced and attributed the wall-coupling class on shipped code, not their exact binary.

Cost of adopting: one line per harness (schedule the scripted decision at a canonical tick before the loop — `nladder`, `wall`, `flight_sweep`, `frame_cost`, `frame_f1`, `skew`, `kick_bench`); zero engine change. Fit with PRINCIPLES: "Measure before claiming" and "Agreement is not independence: several results from one harness share its bugs" — the lab's harnesses shared exactly this one.

## The lens

Inversion asked where the engine is *guaranteed* to fail; the measurement says the engine's truth claim holds at the hardest reported point, and the failure was in the instruments — the same presented-tick disease the decision-log page killed in the shipped session (adba97a8), alive in the examples that judge cost and memory at exactly the scenes (rtf ≥ 6000, biting budgets) where those judgments are made. What the lens may have missed: I did not attack the recorder's live-path tick choice itself, nor a cut placed inside an unresolved encounter.
