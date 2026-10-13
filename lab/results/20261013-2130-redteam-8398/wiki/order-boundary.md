topic: order-boundary
status: open
closed-by:
valid-while:
updated: 20261013-2130-redteam-8398

# The order boundary: tube ↔ Cartesian member, "identical bits"

## Current best

**The boundary between the sparse and dense orders changes the body's law-level orbit, so
"both orders give identical bits" (representation.md §3, law.md:51, gate B8) fails at the one
seam the orders share (20261013-2130-redteam-8398).** The shipped exit path
(`Rebinding::from_state` / `ending_at` behind `resolve_handout`, bind.rs:265-266) was probed
on shipped `crates/space` integers: the pure-transit round trip key → decoded state → refit
moved the `OrbitKey` on **112/112** probes (0/112 kept the key; 15 keys, p 7–1000, e 0–0.999,
four phases, two word scales), including circles (e = 0 → dk = 2^19 Q48 ulps: decode rounding
pushes the state out of `inverse::circular`'s exact class, so even class is not preserved),
and the fit map is **not a fixed point** (second-transit refits moved the key again on all
11 keys that ran — three high-eccentricity keys refuse silently in the control loop —
periapsis-angle wrap-by-one at e = 0.9, residual2 ~10⁻⁹ relative): repeated transits walk
(principle 13). Step size ~1 Q48 k-ulp at fine words, 2⁻²⁸–2⁻²⁵ relative at plane-scale
words (the (p 20, e 0.7, inbound 3/4) coarse row drifts 655665 Q48 ulps ≈ 2⁻²⁸·⁷); the
worst fine-word future divergence in the stored table is 1.92×10¹¹ position ulps at
(p 8, e 0.99, inbound 3/4) — phase mis-anchor near periapsis, not uniform noise.
Single-transit error is below any player floor; the live risks are the unbounded walk
(checkers, check.md and check2.md: no full-key repeat in chained transits to depth 16 and to
depth 64 on six configurations, and at fine words the drift is one-signed — a directed walk,
−1 k-ulp per transit, floor-bias; at coarse words the drift is +7.0×10⁷ ulps over 64
transits) and the per-transit cost (each crossing mints a Catalogue entry + one compile,
5.8–374 µs — the same lever as frame-cost's sticky promotions and hand-out retries).
Corroboration from the shipped plane: the exact-key memo hit rate is 0.0 on 3,108 distinct
rebinds (152f, kick-jet) — re-fits never land on the same key. What survives untouched:
within-order identity (Chronon vs EventCore vs Metal digests, engine `identity.rs` /
`metal_identity.rs`) and the Lorentz half of handoffs (exact, fixed point after one trip,
`lorentz.rs` tests) — the leak is purely the representation fit.

**Domain.** Idealized boundary (no doll unit conversions — the shipped path adds rounding);
the (7, 0.995) separatrix key refuses compile and ten fine-word e ≥ 0.99 encodes refuse
(`Range`). Checker extensions (check.md, check2.md): the leak persists at p = 10⁴–10⁷,
e = 0.9999, retrograde sense, and unbound passages (where k can be stable while the full key
still walks); no convergence to depth 64. Still unmeasured: the Knudsen-threshold canonicity
of the order assignment itself, and an end-to-end `resolve_handout` scene with doll units.

## Refuted

- "The order boundary is representation-transparent / both orders give identical bits as
  built": 0/112 keys survive a pure transit; no fixed point (20261013-2130-redteam-8398).
- "Circular orbits keep their exact-circular key through a transit": decode rounding leaves
  the circular class (same run).

## Open directions

1. **Specify the boundary and freeze r5** (never frozen; B8's engine tests compare the two
   orders but never across a hand-out — `identity.rs` scenes are born in-frame): either carry
   the tube through the battle doll (members keep their tube, Cartesian
   states are transient for the contact resolver, kicks hit (E, L) on the one grid), or snap
   the member state onto the key grid at entry so the exit fit is idempotent by
   construction. Either deletes the per-transit compile and closes the partition
   dependence. Negative control ready: the shipped `from_state` must fail by ≥ 1 key ulp.
2. **An end-to-end scene through `resolve_handout` with doll unit conversions.** (The walk's
   convergence depth is measured: none to depth 64, directed at fine words — check.md,
   check2.md.)
3. **Is the order assignment itself canonical?** If the sparse/dense split is a measured
   Knudsen number, verify it is a deterministic function of state (else the partition is
   schedule-dependent before the fit even runs).

## Contradictions

None open. 152f read its 0.0 memo hit rate as a cost observation; this page reads the same
number as the identity mechanism — compositional, not in conflict.

## Runs
- 20261013-2130-redteam-8398 (awaiting grade): order boundary leaks: 0/112 keys survive a
  pure transit, no fixed point; circles lose their class; r5 absent.
