# Dossier — 20261017-0839-second-20261017-0739-taleb-9b46-5d87 (second author, Taleb lens)

## Claim

The allocator's finality-assert crash is a **window-grid defect of chunked batch drivers,
not a live-path hazard**: in frames mode (the game's continuous-publication harness) it
never fired — 18/18 arms spanning 3 seeds, 3 cadences, 864–27,936 bodies, both laws,
rollbacks 0–6 per arm, E to 64, the quiet scene swept to frontier 3,072 (twice the scene
horizon, through the tick range where the quiet *batch* crash fires) and the relativistic
scene to frontier 8,096 — because frames goals and stride ends stay on the 16-chronon
window grid (`goal_tick`'s `.ceil()`, `next_unit`'s `boundary(w + stride)`), so a
completed truth's window set never intersects a later stride's. `run_to(target)` with
`target` off the grid forces every region's stride to end at an interior tick
(`finished()` demands `verified == target`), publishes finality onto that interior tick,
and the next call's strides re-enter the same window (`w0 = w(target) = w(target − 1)`)
and conservatively overlap the published tails: no on-grid chunk target ever crashed
(96, 112, 128 at 864; 512 at 14k — every run, every window), while interior ones crashed
7/11 runs on this box (100-s1 4/4, 104 2/2, 108 1/3, 100-s2 0/2) plus the author's 2/2
and the checker's 2/2 at 100 — interior is necessary, never sufficient (the crash also
needs a spatial hull overlap in the shared window, a per-run draw).

## Bottleneck

Board item 4 (smoothness and the allocator) via the page's open directions 1 and 2. The
gain is deletion: the engine-side fix the page expected ("refuse the advance or hold
publication") is unnecessary — a one-line driver rule (batch `run_to` targets on the
`cfg.window` grid, or one call per process) provably removes the crash, and the crash
drops out of the live path entirely.

## Evidence

Instrument: the author's `ruin.rs` (batch mode unchanged) plus a `frames` subcommand (one
`run_frames` call; public APIs only) and a `rel` prefix switching the scene to
`Law::Relativistic`; patch = that file + the one-line `ES_CAP` min on `escalation *= 2`
(default unbounded = shipped). **Correction to the author's dossier:** the wave/quiet
scenes are **Newtonian** (`World::new` defaults the law; `loose_gas` never calls
`with_law`), so their finality is global-frontier, not light-cone; the `rel` arms are the
light-cone ones. Commands: `regen.sh` (→ `arms.sh` + `arms2.sh`), ≈ 14 min on the shared
box, every process < 2 GB; per-arm traces in `out/`.

**Frames matrix — 18/18 survived, 0 asserts:**

| Arm | wall | present→ | frontier | regions | E | rb |
|---|---|---|---|---|---|---|
| 864 grid ×9 (3 seeds × rate 100/400 × ahead 0.05/0.25/1.0) | 6 s ea | 580–2,393 | ≤2,800 | 1–798 | 1–64 | 0–6 |
| 14k wave s1 | 35 s | 1,024 | 1,024 | 3,061 | 4 | 2 |
| 28k wave s1 | 50 s | 1,392 | 1,392 | 2,912 | 8 | 3 |
| 28k wave s7 | 50 s | 2,416 | 2,416 | 2,615 | 16 | 4 |
| quiet 14k deep | 300 s | 3,072 | 3,072 | 2,839 | 16 | 4 |
| rel 864 ×3 (cadences/seeds) | 20 s ea | to 7,987 | 8,096 | 1–333 | 4–64 | 2–6 |
| rel 14k shallow + deep | 35/45 s | 0 / 192 | 0 / 80 | 1,241 / 1,153 | 8 / 16 | 3 / 4 |

The quiet arm is the checker's own crash scene: it sweeps ticks 0–3,072 in frames with
conflicts (rb = 4, 4,572 merges, 55k promises exceeded) and never asserts, while the same
scene in chunked batch crashes (below). All survivors: `hard_viol = 0`; `accel_drops > 0`
on every loaded scene (the present clamps at the light cone, never the frame rate); the
864 end state ranges 1–798 regions at fixed N — the (rate, ahead) pair is a path knob in
the live path too.

**Batch controls (same box, same tree, same window):**

| Driver | targets | grid? | result |
|---|---|---|---|
| `run_to` ×13/×11 | 96, 112, 128 (864) | on | **SURVIVE** (digests in `out/b-864-chunk{96,112,128}-s1.txt`) |
| `run_to` ×3 | 512 (14k) | on | SURVIVES |
| `run_to` ×12 | 100 (864, s1) | interior | **CRASH** "from 96 … published tick 100" (4/4 this box; author 2/2; checker 2/2) |
| `run_to` ×12 | 104 (864) | interior | **CRASH** "from 96 … published tick 104" (2/2) |
| `run_to` ×12 | 108 (864) | interior | crash 1/3 ("from 80 … published tick 108"), survive 2/3 |
| `run_to` ×12 | 100 (864, s2) | interior | survives (0/2) |
| `run_to` ×3 | 504 (14k); 500 (14k, 28k); 250 (28k, checker) | interior | survive — no spatial overlap in the shared window |
| `run_to` ×1 | 1200/1500 | interior | survives (nothing re-enters after the last publish) |
| `run_to` ×10 | 150 (quiet 14k) | interior | **CRASH** "region 13279 from 112 … published tick 150" — the checker's exact crash, 1/1 |

**Mechanism (all code lines on the shipped tree, `alloc.rs`):** `certify` (1086–1108)
checks a completing stride's hull against truths **keyed by window** — a truth from stride
[s, t] lives in windows w(s)..w(t−1), and a clash fires on hull overlap in any shared
window, even when the two hulls' time spans are disjoint (conservative in time). Stride
ends are always window boundaries (`next_unit`, 767) **except** when the batch goal
truncates them: `finished()` (1666) forces every region's `verified == target`, so a
non-multiple-of-16 target ends strides mid-window; `run_to` then forces a publish
(1937–38) landing `fin_hi` on that interior tick; the next call's strides start there,
re-enter that same window, and every published tail in it is a potential conservative
clash with `s0 < fin_hi` → the assert at 1451. Frames mode cannot manufacture an interior
stride end (goal caps round up to grid, 560–564), and in continuous publication `fin_hi ≤
frontier ≤` any concurrent stride's start, so the assert is structurally out of reach —
which is why 18 arms with rollbacks never tripped it. Every observed crash message has
`published tick` = the interior chunk target and `from` = an earlier stride start in the
same window.

## Predictions

`predictions.md` predates the matrix (scorecard appended there). **P1 killed in its
pre-registered no-direction**: no frames arm crashed — the kill criterion I wrote down
("no arm crashes anywhere → batch-driver-only") fired; the explaining grid mechanism
arrived after the first probes. P2 wrong in every part (no frames crash; conflict rate
does not predict it). P3 held vacuously. P4 held on `hard_viol = 0` and `accel_drops >
0`, half-failed on end states (cadence-drawn, 1–798 regions at fixed N). P5 wrong
(relativistic frames survived everywhere; light-cone lead does not open the window — the
grid, not the frontier, is the guard). The failures are again the finding: my mechanism
prior (rollback-inherited `fin_hi` + re-clash, cadence-agnostic) was the wrong channel.

## What would make it wrong

- The frames safety is measured on one scene family (wave row + archipelago, margin 0.5,
  `min_region: 1`) and derived on the window-grid argument, which is code-level and
  scene-independent; what could break it is a stride end that is interior by another
  path — none exists in `next_unit` today, but a future change to `goal_tick`'s rounding
  would silently reintroduce the hazard: write the driver rule down anyway.
- The restored-lineage channel remains open in principle: `rollback` → `make_region(…
  Some(fin))` lets a restored region inherit `fin_parts` above its replay point; it never
  fired here (18 arms, rb up to 6), but I did not prove it unreachable — only that the
  observed channel (forced interior publish) is closed by grid-aligned targets.
- Crash/survive verdicts replicated across three windows (author, checker, this run)
  wherever the same arm ran; walls and counters are one shared box, orders of magnitude
  only — and draws (two identical-args interior-108 runs disagree).

## Cost of adoption, and fit

One line of driver discipline (targets on the `cfg.window` grid — `xtask/src/regions.rs`
and any replay/checkpoint driver), and the page's expected engine-side fix is deleted.
PRINCIPLES: "the cheapest compute is compute not done" (a rule replaces a mechanism);
"Measure before claiming, and never strawman" (the live-path-crash reading was one
measured batch shape away from being adopted as an engine defect); "a failed experiment
kills that configuration, never the method" — the killed configuration is interior chunk
targets, not the finality assert, which is the certificate doing its job.

## The lens

The Taleb lens looks for ruin and found safety; the risk is I under-attacked the negative
(the quiet arm now covers the whole horizon and the relativistic arm carries light-cone
load, but a truly adversarial scene — engineered interior alignment under frames, if one
can exist — is not in this battery). The cadence-drawn end states in frames mode are a
fresh Extremistan surface this run measured (1–798 regions at fixed N across (rate,
ahead)) but did not characterize; I did not open them.
