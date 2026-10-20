# Predictions — v4: the disarm channel as an exactly-safe publish floor

Written before the decisive runs. Setup: 541d's patch (da23's `stride_gate` + v3 + the
PRE/HAZ/RB/FIRE instrument) plus this run's v4 change: under `stride_gate`, the frontier
advance publishes up to `floor0 = min(oldest kept snapshot, oldest kept truth start)`
instead of being removed (v3) or unbounded (shipped). `ESE_V3=1` recovers the v3 arm
from the same build. Arms: shipped `gate=0`, gated `gate=1`.

The claim under test: no rollback can restore below floor0 (every restore reads a kept
snapshot or a kept truth start, both ≥ floor0, and floor0 is monotone), so publication at
floor0 cannot fire the assert, while it breaks the v3 starvation loop (present ← finality,
compute ← goal_tick(present)) because floor0 advances with prune as the frontier moves.

## Held-out cases (not tuned on)

The battle protocol is the one 541d/da23 flew, but the *load axis* (the checker's crush)
and the seed set are mine: seeds 11..25 odd (541d flew 11..31; 21/23/25 are outside my
tuning set — I only ever ran s19 before registering these), plus one 4-way crush block.

## P1 — the reproducer, s19 (galaxy 8704/24, rate 2400, margin 0.5, 4.5 s)

- shipped arm: fires (exit 101 with `FIRE ... fin_hi=976`-class state) or runs clean at
  present 800-1500; the fire is a wall-clock race, so either outcome is consistent with
  541d — the arm must NOT be strictly worse than the 43-141 starvation band.
- v3 arm (`ESE_V3=1`): starves, present ≤ 250 (541d measured 43-141 on 5/8 seeds).
- v4 arm: present ≥ 0.5 × the shipped arm's present on the same seed and window
  (the starvation is broken), and no fire.

## P2 — the paired protocol, 8 seeds × both arms

- fires: v4 0/8. shipped: 0-4/8 (the race; bf83 pooled 4/62, c749 6/6 pooled — I predict
  at least one shipped fire lands in a hot window, but 0 shipped fires does not refute
  anything: the wall clock owns incidence).
- present: v4 ≥ 0.5 × shipped on every seed; median ratio ≥ 0.7. The lag I expect is
  O(sync + window) ≈ 144 chronons behind the shipped frontier advance, which matters
  only when compute outruns the rate.
- the equality law holds under v4: every `RB` line has m ≤ 0.

## P3 — the crush block (4 concurrent draws, same seeds both arms)

The checker's adverse case killed da23's gate by load (present 72 vs 529 shipped).
Prediction: v4 present ≥ 0.3 × shipped under the same crush (the floor0 channel is not
load-coupled the way the coalesce is; it needs only prune, not aloneness).

## Kill criteria

- **Any `FIRE` on a v4 draw kills v4's exactness claim** (the floor0 argument is wrong in
  practice, not just imprecise).
- v4 present < 2× v3's present on ≥ 4 of 8 battle seeds kills the disarm channel (it did
  not break the loop).
- A v4 draw with `final lead` pinned at 0 for the whole draw while shipped advances:
  the channel is load-coupled after all.

## What I would count as "held" vs "failed" honestly

P1-v4, P2-fires(v4), P2-present(median), P3 are the load-bearing ones. P2-shipped-fires
is explicitly a race observation, not a prediction that can fail the run.
