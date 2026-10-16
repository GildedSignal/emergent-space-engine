# Predictions (written before the decisive flight)

The plan pass's interior (`step::replan`, 28.2 µs/body at 10⁵ per 404b's checker) is unattributed.
Code read: `plan_interval_inner` → `open(t,0,h)` → `Ctx::secondaries(d, t, i)` recomputes every
source planet's state at `t` per body (plus a Vec alloc), and `plan_terminal` may bisect for an
impact. At birth all bodies sit at tick 0, so for every belt body (not itself a source)
`secondaries` returns the identical vector: per-body recomputation of per-tick shared state.

Cases not tuned on: held-out seed 7, and N=10⁵ (the author flies 10⁴ first).

1. **Secondaries share:** `secondaries` (planet readouts + alloc) is >50% of `replan`'s 28 µs/body
   at birth on the belt (10⁴ and 10⁵, seeds 1 and 7). Kill: <25%.
2. **Hoist cut:** a (doll, tick, except)-memo active only inside `Universe::start` cuts the plan
   pass by the same share (predicted: plan 32.5–33.5 → <18 µs/body), digest identical at the
   canonical start state.
3. **Terminal search:** `plan_terminal` (terminal_tick + next_impact bisection) is <10% of replan
   at birth on the belt (periapses above the surface; no plunge arcs) — i.e. the "irreducible
   exact search" is NOT the birth bill; the bill is shared-state recomputation.
4. **Calls law:** secondaries calls per body ≈ 1 at birth (belt bodies: one `open`, level 0);
   planets' calls ≈ sources+1 each. If calls/body is ≫2, prediction 1's mechanism is wrong.
5. **Scaling:** the share is flat in N (10⁴ → 10⁵) because it is per-body work, not superlinear.
