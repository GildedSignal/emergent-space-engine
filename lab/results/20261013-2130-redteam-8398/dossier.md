# Dossier — 20261013-2130-redteam-8398 (premise red-team)

## Claim

The two evaluation orders cannot give identical bits as the representation stands: the order
boundary itself — tube → Cartesian member → tube, shipped as `Rebinding::from_state` behind
`resolve_handout` — changes the body's law-level orbit on **112/112** integer probes and is
**not a fixed point**, so the two orders' event graphs differ by a refit event the sparse
order never performs (representation.md §3, law.md:51, gate B8).

## Bottleneck

Not a rate bottleneck: a hole in the truth rule ("canonical outcomes are exact and
independent of … partition", AGENTS). What it blocks once broken: B8's sparse/dense leg
(untestable until the boundary is specified), and the allocator's freedom to move work
between orders without changing outcomes. What fixing it deletes: every boundary crossing
currently mints a new Catalogue entry and pays one compile (5.8–374 µs, kick-jet wiki)
instead of sharing the cycle memo — the same lever frame-cost chases as "sticky promotions"
and "hand-out compile retries".

## Evidence (all integers; commands below, ~6 s total)

Instrument: shipped `crates/space` only — `Orbit::compile`, `binding::cartesian`,
`Rebinding::from_state`. Grid fixed a priori (15 keys p ∈ {7…1000}, e ∈ {0…0.999}, 4 phases
per cycle, two state-word scales: the crate's own 60-bit-headroom convention and a plane-like
coarse word), plus controls. File: `crates/space/examples/transit_roundtrip.rs` (in
`work/patch.diff`); raw table `transit.tsv` in this folder.

1. **Key identity: 0/112.** Every pure-transit round trip (key → decoded integer state →
   refit) moves the `OrbitKey` — including circles (e = 0: dk = 2^19 Q48 ulps ≈ 2^-29
   relative). Mechanism seen directly: decode rounding makes `vr ≠ 0`, the state leaves
   `inverse::circular`'s class, and the general branch lands off the UNIT key — the boundary
   does not even preserve orbit *class*.
2. **No fixed point.** Re-fitting the first fit's own decode moves the key again (12/12
   keys), with periapsis-angle changes up to a full u32 wrap-by-one and residual2 ~10⁻⁹
   relative: repeated transits **walk** (principle 13's compounding error, at the
   representation layer). Contrast: the Lorentz half of the handoff is exact and reaches a
   fixed point (`lorentz.rs` tests) — the leak is purely the tube↔Cartesian fit.
3. **Size, honestly.** At fine words the walk step is ~1 Q48 k-ulp; at plane-scale coarse
   words dk ≈ 2^-28–2^-25 relative and the decoded positions a fraction of a cycle later
   diverge by up to ~24 M at (p 20, e 0.7, inbound 3/4) — a phase mis-anchor near periapsis,
   not uniform noise. Single-transit error is far below any player floor; the player-visible
   risks are the unbounded walk over many crossings (unmeasured beyond step 2) and the
   per-transit compile cost.
4. **Independent corroboration from the shipped plane:** kick-jet run 152f measured the
   exact-key memo hit rate at **0.0 on 3,108 distinct rebinds** — consistent with re-fits
   never landing on the same key, which is this mechanism at the plane's own kick boundary.
5. **Controls.** Negative: one velocity ulp moves the refit (passes). The pre-registered
   positive control (circular keys round-trip exactly) **failed** — reported as the finding
   (i), not an instrument void: the equality tested is the Catalogue's own `Eq`, the
   fixed-point control exercises it computing real differences, and 152f's 0.0 hit rate is
   the plane agreeing. Refusals: 10/122 (separatrix key (7, 0.995) refuses compile — the
   law's own edge; three decode overflows at extreme fine-word choices) — disclosed, not
   hidden.
6. **What survives untouched:** within-order bit-identity (`engine`'s Chronon vs EventCore vs
   Metal digests on battle scenes) and the frame half of handoffs. The premise fails only at
   the seam neither order owns.

Commands (each ≤ 60 s on the shared runner):
```
cargo run -p emergent-space --release --example transit_roundtrip   # full table + controls
```
(`regen.sh` in this folder regenerates everything, ~6 s after a one-time `cargo build`.)

## Predictions

`predictions.md` was written before the run. P1 half-failed in the attack's favour (circles
do **not** round-trip — stronger than predicted); P2 held (residuals small relative);
P3 held in direction (divergence grows with e; the (20, 0.7) inbound row is the worst);
P5's positive control failed as written and is reported as finding (i) above with the
fixed-point control taking its place.

## What would make it wrong

- If the engine's real boundary never re-fits a decoded state. It does:
  `crates/universe/src/bind.rs:265-266` (`Rebinding::ending_at` / `from_state`) behind
  `resolve_handout` (`universe.rs:743`), exercised by every fleet-frame hand-out.
- If the law declared transits eventful (a logged boundary event with canonical rounding).
  Then per-run determinism stands, but B8's letter (same scene, either order, same bits) and
  the allocator's order-freedom still fail as measured.
- If the walk converges after k > 2 transits into a fixed point. Unmeasured; the angle
  wrap-by-one at e = 0.9 suggests not, but this is the first experiment a checker should run.

Cost of adopting the fix: small and local — either carry the tube through the battle doll
(members keep their tube; Cartesian states are transient views for the contact resolver;
kicks apply to (E, L) on the same grid as everywhere), or snap the member state onto the key
grid at entry so the exit fit is idempotent by construction. Either deletes the per-transit
compile and closes the partition dependence.

Fit with PRINCIPLES: "Errors never compound … divergence is not a joke and it compounds"
(13) — the boundary walks; "a fix signals the wrong representation" (19) — the residual
layer is doing rearguard duty at a seam no representation was chosen for; "Laws are
versioned. Canonical outcomes are exact and independent of cache, partition, observation,
schedule and hardware" (AGENTS) — measured partition-dependence at the one boundary the two
orders share.

## The lens

Red-teams overweight exotic cases; ranked by player likelihood this one is *invisible*
per-transit (2^-28 relative) and becomes real only through repetition and cost — I report it
as a law/B8 breach first, player risk second. What this lens may have missed: the checker
should push k > 2 transit iterations (convergence?), a scene through the shipped
`resolve_handout` end-to-end with doll unit conversions (my probe is the *idealized*
boundary — the shipped path adds rounding), and the Knudsen-threshold side (is the order
assignment itself a canonical function of state? If not, the partition is schedule-dependent
before the fit even runs).

## Rung criteria that should have caught it

**None exists.** r5 ("dense order … bit-identical between the sparse and dense orders,
integer, on the existing crates") was never frozen (`lab/rungs/` has no r5); B8 names the
identity but its engine tests stay inside one order's law (`identity.rs` scenes are born
in-frame; no tube crosses in). Freeze r5 with: a body transiting a frame region and back
must return to its exact key (positive: an entry-snapped or tube-carrying build; negative:
the shipped `from_state`, which must fail by ≥ 1 key ulp — the numbers above).
