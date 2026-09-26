# Spacetime-geometry unification — 2026-09-12 user steering

Portable record of later explicit user direction. Read with the [handoff](HANDOFF.md) and the [2026-09-12 requirements review](requirements-review-20260912.md). Journaled as [H0031](HISTORY.md).

## Authority

This is **later user steering**. It governs the physics completeness criterion when it conflicts with earlier journal Next fields, including H0024 elliptic/Kerr and the review’s “complete tiny causal law then map” queue as a substitute for a shared evolving geometry.

It is **not** a G2 pass, engine completion, production-law selection, map implementation, or threshold change. Frozen G2 evidence remains `1dac658` / `99764b4`. Keep that snapshot distinct from HEAD. Do not wire gravity into the canonical engine.

The requirements review remains useful inspection: combining retarded, Euler and Schwarzschild labels does not define one law; another stationary compact predicate does not fill a missing evolution. This note does not rewrite H0001–H0029. Independent GEM CONS/aberration review ([H0029](HISTORY.md)) is still a no-go on `advance_map` until a spec patch.

## User unification ask

Adopted gist of the user’s direction:

> Gravity is part of spacetime, a consequence of it. In GR, freely falling bodies follow geodesics; light and clocks use the same geometry.
>
> Unification: sources establish shared geometry; ships and light traverse it; mass/energy feed back; the compiler reuses solutions while the assumptions hold.
>
> Gravity is intrinsic to the spacetime compiler. Computation must be amortized. Isolated formulas will not close the loop.

The intended product is one shared geometric object that motion, null arrival and proper time read from, not a pile of separately passing oracles.

## Proposed patch experiment

The next physics experiment is **one small evolving spacetime patch**, not Kerr and not more disconnected oracles:

- two massive bodies
- a test ship
- a light ray
- a clock

A controlled source change must produce mutually consistent ship motion, light arrival and elapsed proper time **from that patch’s geometry**. Then subdivision and caching must preserve the result (direct versus subdivided/cached canonical parity).

Specify and freeze that experiment using **one metric object**. Completeness is the closed loop on that patch: shared geometry, consistent observables after a source change, and compiler reuse that does not change the answer. Isolated monopole, coupled-Euler, compact-class, Schwarzschild-classifier or GEM-formula checks do not by themselves satisfy this criterion.

## Binding consequences

1. Physics next work is to specify and freeze the patch experiment above. Keep two masses, ship, ray, clock, a controlled source change, and cache/subdivision parity in the freeze. Use one metric object.
2. The CONS/GEM spec patch required by [H0029](HISTORY.md) is still required before `advance_map`. Do not implement a map in this steering turn. Do not stub authored worldtubes as a substitute for evolution.
3. Do not start Kerr, elliptic turning-root, or further stationary compact oracles as the default physics next step. Those remain useful only if tied to an identified obligation of this patch.
4. Do not wire the experiment into the engine. Laboratory law `es-inertial-causal-v1` stays inertial. `production_law` remains null. G2 still FAIL.
5. The compiler exception-profile track ([H0030](HISTORY.md)) stays parallel and is not gravity. Amortized reuse belongs in the patch experiment’s cache/subdivision parity, not as a claim that the 1k-exception fixture is gravitational work.

## What this does not change

Qualification thresholds, frozen `1dac658` evidence, and the prohibition on weakening gates after seeing candidate results are unchanged. Fermi estimates still identify probes; they are not feasibility or qualification oracles. Sibling work on the GEM spec patch and the exception journal is separate from this steering record.
