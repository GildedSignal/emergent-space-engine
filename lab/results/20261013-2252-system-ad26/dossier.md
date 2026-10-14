# Dossier — 20261013-2252-system-ad26 (whole system)

**Claim.** On one shipped scene at battle scale, every event-carrying item class pays the same
wall — the tube rebind (`bind_surface`) — for 41–65% of its wall (80% of the promotion, the N
ladder's first break), the coarser-word retry alone is 18–39% of the bind, and the record's
four verified-but-unmerged levers (009b word fix, 7055 hand-out memo, 5eb6/8b43 fixed tier,
de99 Carlson kernel) compose to 22% of today's resolved-battle cost — a ~10⁵-member battle
ceiling — so the bodies gap and the kick gap are one adoption queue, not four problems.

**Bottleneck.** The board's furthest gap (28 vs 10⁹ bodies) and the kick gap (~10³·³) are
recorded as separate topics (nladder, frame-cost, kick-jet). This run measures, on one scene
and one clock, that they share one mechanism, and prices the composite of the levers each
topic produced in isolation. Expected gain: the adoption queue's total (4.5× on the battle
cost; ~10⁵-member ceiling), and the deletion it implies: no new engine mechanism is needed
between today and 10⁵ battles + 10⁹ quiet belts (1.08 cores of event work at Carlson-priced
30 µs/event).

**Evidence** (Linux/x86 shared runner, threads 1, 8 wall-seconds per arm, orders of magnitude
only; every number regenerable via `regen.sh`, ~4 min cold).

The census (shipped `prof` feature, printed by a 12-line probe patch; the `--members` clamp
lifted env-gated to 20,000 — both in `work/patch.diff`):

| arm | members | seed | rtf | D ms | bind ms | bind/D | retry/bind | hand-out bind | ev/m/gs |
|---|---|---|---|---|---|---|---|---|---|
| m48 | 48 | 1 | 1 | 7.8 | 0.2 | 2.8% | – | – | 1.35 (slices) |
| m400 | 400 | 1 | 1 | 19.3 | 0.1 | 0.3% | – | – | 0.16 |
| m1500 | 1,500 | 1 | 1 | 217.0 | 111.3 | **51.3%** | 39.0% | 79.6% | 0.091 |
| m1500 held-out | 1,500 | 7 | 1 | 202.2 | 98.7 | **48.8%** | 39.2% | 81.1% | 0.082 |
| m4000 | 4,000 | 1 | 1 | 1,536.3 | 1,001.5 | **65.2%** | 38.5% | 80.0% | 0.179 |
| m12000 held-out | 12,000 | 3 | 1 | 2,269.0 | 1,479.4 | **65.2%** | 32.2% | 66.9% | 0.126 |
| m400 flying | 400 | 1 | 100 | 1,277.4 | 519.9 | 40.7% | 18.1% | 72.0% | 0.043 |

D = process + handout + f_adv + p_decide (every item class that carries events; the hand-out
is timed outside the fleet item — `f_adv` 169 ms against `handout` 1,104 ms at m4000, so the
sum is a clean partition). bind = FIT + FIT2 (`bind_surface`'s two `bind_in` passes). Anatomy
at m4000: hand-out 510 µs each (bind 408 = 80%, replan 91 = 18%), kick 248.6 µs each (bind
≈112 = 45%), fixed tier (rekey+requeue+take_due, 1.33 M requeue calls) 322 ms = 21% of D.
The m4000 arm reproduces 367f's scene exactly (2,163 hand-outs, 1,058 kicks, digest
`5c8fe1a8e439221d`) — cross-run anchor, not independence.

The endgame arithmetic (`endgame.py`, cited factors only): D = 192 ms/game-s at 4,000 members
→ word fix deletes the retry (bind 125.2 → 77.0) → hand-out memo −31% of hand-out bind
(→ 42.8) → Carlson ×10 on 70% of the survivor (→ 15.8) → fixed tier deleted → **D = 42.3
ms/game-s = 22% of today**, slope 10.6 µs/member/game-s, resolved-battle ceiling
**≈ 9.5×10⁴ members** at 25% of 4 cores (today's break: 10³–10⁴); the quiet 10⁹ belt needs

**1.08 cores** of event work at a Carlson-priced 30 µs/event (a4ed's 29 µs figure holds).
Repeat (regen.sh, second run of the same arms): counts bit-stable where the budget resolves
everything (m4000: 1,058/2,163 again), shares within ±2 points; the flying-pace arm's share
straddles 40% (39.1–40.7%) and the 12,000-member arm's counts move with the wall (5,856 vs
6,016 hand-outs — the settle resolves wall-dependent leftovers there), per-event costs stable.

**Predictions** (`predictions.md`, written before the runs): held — one-wall share ≥ 40%
everywhere with the kill criterion (< 40% at 2+ counts) not triggered; hand-out bind ≥ 50%
(67–81%); held-out seed 7 within ±2.5 points; 12,000 members preserves the ordering; rtf 100
keeps kick shares (hand-outs fall to 374 in 800 game-s). **Failed as stated** — the one-wall
share is 41–65%, not ≥ 60% at every member count (1,500-member arms sit at 49–51%; the kick's
own bind share is 45%, the rest is forces/readout/planning); and the event rate at 4,000
measured 0.179 ev/m/gs against the predicted 0.03–0.15 band (367f's 0.041 counted binding-term
events only; strict kicks+leavers here give 0.101). The retry's share was flat-to-falling in
members (39% → 32%), not rising.

**What would make it wrong.** The census is one scene (the plane's battle) at one pace pair;
a scene where kicks dominate and binds are made-class (≈35 µs binds, not 112–408 µs) would
shrink the one-wall share toward the kick's 45%. The endgame line is arithmetic on cited
factors, not a build: the levers must land bit-identically together (009b and 7055 touch the
same retry path; 7055's memo assumes the retry still exists — adopting both needs the memo
re-priced against the word-fixed bind, likely smaller than −31%). The Carlson factor is the
conservative end of de99's 42–2378×, applied to 70% of a bind whose compile share was measured
on other scenes. The 12,000-member arm is 100% overflow frames: its census counts what the
budget resolved, not what the scene wanted. Cost of adopting: the four merges are already
individually verified; the composite is not — one behave suite run on the stacked build decides
it. Fit with PRINCIPLES: "A fix signals the wrong representation" and "the best part is no
part" — the retry is a repair of the word choice, deleted by choosing before compiling; and
"bottlenecks as much as possible" — the interlock means one adoption queue moves two
scoreboard rows.

**The lens.** The whole-system lens sees one wall because it looks for mechanisms that are
secretly one; it may have missed the kick's non-bind 55% (forces, readout, planning) — at
made-class bind costs that half dominates, and the unification weakens to "the promotion and
the leaver kick share the bind". The 10⁵ ceiling is a projection, not a measurement; the M1
re-measure and the stacked build are the integrator's.

## Commands

```
bash lab/results/20261013-2252-system-ad26/regen.sh   # ~4 min cold: builds with --features
                                                      # emergent-universe/prof, runs 7 arms,
                                                      # prints census.txt and endgame.txt
```
