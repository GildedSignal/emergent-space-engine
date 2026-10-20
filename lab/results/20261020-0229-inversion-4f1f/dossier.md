# Dossier — 20261020-0229-inversion-4f1f (inversion)

## Claim

The 1d47/4063 contradiction is adjudicated and both halves were mis-attributed: the canonical-cut
digest's schedule-independence is broken by **the decision's anchoring, not by the gate and not by
load per se** — and the defect is in the **shipped play path itself**: `input(now)` anchors the
player's decision at the frame's *delivered* time, which load makes a random variable, so the
shipped engine (no gate, stale = 0) produced **six distinct canonical states in six runs of the
same arm** (10⁵, seed 1, one cut) under box load. With the decision at a canonical tick
(`schedule`), OFF = ON = one digest on the same loaded box (16 fresh runs, 0 flips): the gate
(1d47's all-to-queue) is **digest-neutral** in every arm flown.

## Bottleneck

The board's first (bodies in the flyable engine): the root-burst cure's adoption. 1d47's checker
blocked it ("the digest becomes schedule-dependent at the rungs where the deferral fires"); 4063
unblocked it ("no digest re-freeze on this record") but moved the decision off the play path to do
so. Whichever was right decided whether the gate ships as bookkeeping or as a law change. Neither
was right about the mechanism — and the real defect reaches past the gate into Truth itself
("canonical outcomes are exact and independent of … schedule and hardware", AGENTS.md).

## Evidence

All on this tree (Linux, 8 vCPU, per-run loadavg logged in `work/runs/`): 4063's `cut_digest`
instrument verbatim (its run branch) + this run's two disclosed dials — `ES_DECIDE=frame`
(nladder's own recipe: `input(p.u.now)` at frame 60) and `ES_DECIDE_AT=<tick>` (schedule at an
explicit tick). Scene: shipped nladder burn, seed 1, rtf 1000, 12 ms, threads 1, cut 17,000
game-s, N = 10⁵. Gates from 1d47+4063's patch (`ES_ROOT_SHIPS_TO_QUEUE`, `ES_FIX_PROBE`).
Quiet = loadavg ≤ 2.5; loaded = 6 steady CPU spinners (2 of 8 cores left), loadavg 5–10.

**Canon-anchored decision (schedule at a fixed tick) — stable under load, both arms:**
OFF `581ced1a`/127,671 kicks/1,802 encounters (loaded ×3, plus 4063's record); ON (gate)
`581ced1a` quiet ×5 + loaded ×11 (stale 5,212–5,297, stale_enc 0 in every run). The gate never
moved a digest in any same-tick run.

**Frame-anchored decision (input at the delivered now — nladder, session, the play path) —
multistable under load, OFF included:**

| arm | run | decision tick (canonical 196,926,963) | digest | kicks | encounters |
|---|---|---|---|---|---|
| OFF quiet | ×4 | 196,926,963 (exact) | `0b9930b6` | 127,663 | 1,792 |
| OFF loaded | m1 | 96,134,502 | `c0161c9e` | 127,573 | 1,822 |
| OFF loaded | m2 | 85,983,231 | `ffac19c4` | 127,570 | 1,857 |
| OFF loaded | m3 | 65,011,711 | `fd7b01d5` | 127,547 | 2,060 |
| OFF loaded | m4 | 40,894,955 | `5b1fd8c2` | 127,524 | 2,743 |
| OFF loaded | earlier pair | (two further ticks) | `461b1630`/`079acea1` | 127,575/127,650 | 1,840/1,779 |
| ON loaded | ×2 | 20,971,578 / 41,943,039 | `c2dd7761`/`4cd4c9d3` | 127,515/127,532 | 4,079/2,692 |

One-to-one: every distinct delivered tick is its own universe (stale = 0 throughout in OFF — the
gate's stale-read channel never fires here; the input tick is the only channel).

**Attribution (the APIs are equivalent at the same tick):** `schedule(196,926,963)` → `0b9930b6`
= `input(now)`'s quiet digest exactly; `schedule(196,926,960)` (3 ticks away) → `7b0f2839` with
*equal* kicks/encounters counts — a third universe whose counts coincide, so count-equality is not
digest-equality. Even quiet, the frame loop's per-frame truncation lands ~3 ticks from the
canonical tick (hence `0b9930b6` vs `581ced1a` at the same nominal game-second).

**Mechanism, in shipped code:** `frame_to` sets the presented time to what the budget actually
reached (`self.now = a.horizon`, universe.rs:1121); the served session takes the player's keys at
exactly that time (`self.p.u.input(now, keys)`, xtask/src/universe/session.rs:119; nladder.rs:93,
flight_sweep, frame_cost, kick_bench, throttle/view tests likewise); `input` anchors the decision
at that tick (`t.max(event_time)`, universe.rs:1178–1190). Load → short frames → a load-born
decision tick → a different canonical state after `settle(cut)`. `schedule`'s own doc states the
law the play path breaks: "a decision takes effect at its logged canonical tick, **never at a
wall-derived one**" (law.md, "Ties").

## Predictions

`predictions.md`, written before the decisive arms. **P1 held** (canon-ON quiet ×4 = `581ced1a`).
**P2 held in substance, wrong in attribution** — the loaded frame arms flipped (≥6 digests), but
so did OFF: the predicted gate mechanism (stale reads flipping encounters) never fired
(stale_enc 0 everywhere); the input tick is the channel. **P3 failed, and the failure is the
finding**: OFF under load was *not* stable (2 fresh digests + the m-series' four). **P4 held**
(frame quiet ×4 stable — the deterministic truncation offset). **P5 held** (composition flips).
**P6 held**: every divergent pair differs in encounters/kicks (the state chain, upstream of any
scan).

## What would make it wrong

One scene (10⁵ nladder burn), one seed, one cut, steady-spinner load; bursty shared-box load may
flip at a different rate, and 2×10⁵ is unflown here (1d47-checker's 2×10⁵ bistability is this
channel on its loaded box). The loaded digest multiset is schedule-born by construction — regen
reproduces the *law* (canon-armed stability, frame-armed multistability with the decision tick
printed per run), not my exact ticks; that is the claim. Replays are self-consistent (they re-anchor
at the logged tick, replay.rs) — the coupling bites live flights' cross-run and cross-machine
digest comparison, which is what the lab and the re-freeze do.

## Cost of adoption, fit with PRINCIPLES

The gate (ee4d/1d47/4063's cure) is unblocked on the digest axis: its stale reads flipped nothing
in 16 same-tick runs under load; the "digest re-freeze" debt belongs to input anchoring. But the
re-freeze protocol must pin decisions at canonical ticks or the corpus is a distribution, not a
value — and the shipped session's `step` should anchor a changed key word canonically
(`schedule` at, e.g., the player's next item tick), a one-line-class change the engine already
owns. PRINCIPLES 13 ("errors never compound"): here errors do not compound — they *branch*; Truth
("independent of … schedule") is the line violated, and PRINCIPLES 5 ("the player is the only
wildcard") is the design fact that makes anchoring him canonically the whole fix.

## The lens

Inversion, move 3 (invert a success): 4063's clean 34-run bill assumed a quiet box and a canonical
decision; 1d47-checker's bistability assumed the gate. What the lens may have missed: with every
digest-bearing harness in the tree taking `input(now)`, the record's "bit-identical across reruns"
certificates have been quiet-box luck wherever inputs rode the delivered time — how many prior
"stable OFF" controls were small quiet samples is now a fair question (mine were, until loaded).
