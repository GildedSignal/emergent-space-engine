topic: formation-family
status: open
closed-by:
valid-while: crates/universe@<this run's tree> + 20261021-0607-components-b560's patch (examples/family_census.rs; no law change)
updated: 20261021-0607-components-b560

# The formation family: one orbit, one integer kick stream, one binding

## Current best

**NEW (b560, components — od 2 executed engine-side: the intern key exists in the engine, and the belt's clock cannot reach it).** Two same-orbit planets at δx = 10⁶ root (the doll split's aligned grid, step.rs:19) **co-fire at ONE calendar key through 383 fires (25,525/25,525 censuses, identical steps 2³⁵; r = 2 AU: 25,526/25,526, 2³⁷)** — only a step change by a factor of 2 forks it. Checker extensions, all confirming: F = 16 families (δx 10³ and 10⁶) co-fire 41,328/41,328 through 1,513 fires; e = 1/20 and synodic drift (planet 1 AU, family 1.3 AU) change nothing; 6,303 fires (16× the horizon) still no fork; and a cross-r pair (1.00/1.15 AU, different orbits) co-fires 99.80% of censuses until its H change forks it at fire ~1,485 — **the sharing class is the (step, anchor), broader than the family.** But 16 same-orbit **ships (chained fictitious clock) hold 16 distinct keys from the FIRST due at every δx = 1–10⁶ root** (below the author's 10² floor too; clone control: one key, 350 fires — instrument valid): `plan_clock` (step.rs:626) derives interval and anchor from each body's own continuous state (no grid), first-due spread 18,415–5.4×10⁸ ticks = 12–36× the light-time separation, growing to 1.9×10¹⁰ after ~300 fires. **The sharing barrier for the calendar is the clock's representation, upstream of a877's word** — w11 shares the kick dv, the aligned grid shares the key, and the engine already runs the latter for doll bodies. Adoption: family-anchored (step-class) grids for root-doll ships (a law change, gated with od 1); payoff F× slots and F× fires per family epoch on the families row — the fire half also needs a calendar-item change: the shipped queue has no intern (`key_of` = (tick, id), keyed by deadline + moved), so co-firing members are still one entry each.

**Prior standing (a877 — the word half, off-engine): certificate Ξ = h·H·δx/(2⁻¹¹·v)** (H the sources' tidal tensor; on `force::acceleration` + `step.rs::quantize` verbatim). The 61-bit word splits every family on every kick; at 11 fraction bits the root doll shares over measured horizons (0 forks to δx 10⁶ at 1 AU, ring included) but not forever (checker: first fork at kick 14,030/57,638 — the truncation straddle forks any δx > 0 at a certified rate). D(t) bounded at every radius; the Fermi fleet doll keeps the planet-doll regime; the tube-family is the root-doll form.

## Refuted

- **NEW — "same-key members fire at the same tick and keep one intern key in the shipped
  calendar, as the construction (shared step size and anchoring) implies" (the page's od-2
  premise): refuted for the shipped clock — root-doll ships share neither step nor anchor nor
  key at any δx > 0 from birth (16 distinct dues at every census, both radii); the intern key
  holds only on the doll split's aligned grid, which ships do not run
  (20261021-0607-components-b560).**
- **"One kick per ship erases the sharing" as a property of the physics (225d's reading):**
  refuted — it is a property of the 61-bit word; at the family width the stream is shared
  (0 forks, 30 synodic periods, 1 AU ring included) (20261020-2158-m2-meso-motion-a877).
- **A position offset at equal velocity as a "formation":** refuted — that is a different
  orbit; Kepler shear separates it at ~n·δx (the family is the same orbit at a phase
  offset) (a877).
- **"Ξ < 2⁻¹⁶ ⇒ bit-identical forever" (a877's own certificate line):** refuted by the checker
  at 10× the horizon — the truncation straddle forks any δx > 0 at a certified rate; the rate
  is certified, the zero is not (a877 + checker).

## Open directions

1. **The gates at the family word** (the adoption question): B13's encounter-phase sensitivity
   vs a bounded 2⁻¹¹·v error; B12/B17/B18 on a w11-family plane. One named experiment — the
   gold experiment. Now sharpened: the plane needs BOTH w11 (the dv) and a family-anchored
   grid (the key) — b560 prices the second alone at F× slots and F× fires.
2. ~~The engine-side key census~~ **Executed (b560): the answer is no for ships, yes for doll
   bodies — see Current best.** The unflown half: `fleet.rs`'s members are doll bodies; do real
   fleet dolls already co-fire on the aligned grid (free interning today)? Checker (code read):
   the queue's keys cannot merge OR share — `key_of` returns (tick, id) and the queue keys by
   deadline + moved, so every body is its own entry; a shared fire needs a calendar-item change.
3. **The fork handler as H_live:** the family's refinement rate on an aligned grid (only a
   step-size factor-2 change forks the key; checker-measured to 6,303 fires at F = 16, still 0;
   the cross-r pair's H change forked at fire ~1,485 and stayed forked) — price it against the
   mint for large F.
4. **Child-doll families** (about planets, inside ~0.1 Hill): the fleet doll owns them; where
   the crossover is (a tube-family at what ρ beats the Fermi frame's lattice cost) is unmeasured.

## Contradictions

None open. a877's word barrier and b560's clock barrier compose (the word gates the dv, the
grid gates the key; neither alone shares the event). cell-rebind's B13 kill remains the nearest
gate neighbour: its error accumulated per kick; the family word's is sigma-delta-bounded —
different error type, same gate.

## Runs

- 20261020-2158-m2-meso-motion-a877 (silver): the family certificate measured — w61 splits at
  100% from kick 0; w11 shares the root doll over measured horizons (0 forks to δx 10⁶ at
  1 AU, ring included) and prices the forks above it; D bounded at the exact resonances;
  planet dolls stay with the fleet doll. Checker: reproduction exact; "forever" falsified at
  10× horizon inside the certified zone; word-width scaling confirmed (w8 0, w16 1,182);
  e = 1/20 Giant changes no verdict.
- 20261021-0607-components-b560 (silver): od 2 engine-side — the aligned grid interns
  (2 planets at δx 10⁶: one key, 383 fires, both radii) and the chained clock cannot (16 keys
  from birth at every δx 10²–10⁶; first dues differ pre-kick by 12–36× the light offset);
  the calendar's sharing barrier is the clock's representation, upstream of the word. Checker:
  reproduction bit-for-bit; domain extended (F = 16, e = 1/20, synodic drift, 6,303 fires,
  δx = 1 root) — all confirm; sharing class is the (step, anchor), not the family.
