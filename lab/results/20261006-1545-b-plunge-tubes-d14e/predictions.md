# Predictions — plunge and radial tubes (20261006-1545-b-plunge-tubes-d14e)

Written before the decisive experiment. The change: a third trajectory kind in
`crates/space` — `Plunge`, a one-way compiled arc in a radial phase from the binding
event to a terminal radius (the doll's surface), for states whose osculating orbit has
no outer turning point (barrier positive) or no angular momentum (L = 0, inbound).
The terminal event (arrival t, Δφ, Δτ at the surface) is compiled exactly by the same
adaptive integer panels as `light::Capture`. Refused kicks in the plane (`NoBoundOrbit`
→ dropped kick) become rebindings onto plunge tubes; the crash item fires at the
arrival tick.

Baselines measured today (this machine, before any edit):

- `behave --law space --gates G1..G6`: all PASS (G1 256/256 worst 6.6e-4; G4 0/10 misclassified).
- `behave --law plane --gates B13`: FAIL at every step. Step 6: 41/64 (worst 8.5e-2), 1 draw with refusals;
  step 7: 60/64 (worst 2.12e-2), 1 draw (2 refused); step 8: 62/64 (worst ΔL 4.39e-1), 4 draws (up to 51);
  step 9: 58/64 (worst ΔL 1.28e0), 8 draws; step 10: 53/64 (worst ΔL 1.62e1), 11 draws (up to 555 refused).
- `behave --law plane --gates B17`: passes at steps 4–6 (HANDOFF; re-measured before the decisive run).
- `xtask engine-judge`: E1,E2,E3,E4,E5,E7,E8 PASS; E6 FAIL for a missing prepared-mutants artifact
  (lab machine has no frozen mutant binary — environmental, unrelated); E9 FAIL phase 1 as designed.
- `cargo test -p emergent-universe` motion tests: the ensemble Jacobi test passes its frozen bound with
  refused kicks present (the note in motion.rs).

## Held-out predictions

1. **B13 refusals vanish.** After the change, at every step 6–10, the per-draw
   `refused` counts go to 0 (every kick rebinds; a momentary plunging heliocentric
   osculating orbit is carried by a plunge tube for one kick interval and re-fitted at
   the next kick).
2. **B13 failures that were refusal-driven recover.** The step-8 draws with 5–51
   refusals (worst ΔL 4.39e-1) and the step-10 draws (worst 1.62e1) come back within
   1e-2 or close to it; I predict step 7 improves from 60/64 to 62–64/64, step 10 from
   53/64 to ≳60/64. I do NOT predict B13 necessarily reaches 64/64 (the bar): the
   failures at step 7 that are not refusal-driven (≈3 marginal draws) are untouched
   physics, and one of them may stay above 1e-2.
3. **No regression elsewhere in B13.** Draws that never see a plunge binding produce
   bit-identical answers (the kick cadence of the motion law v2 depends on the state,
   not the tube kind; the drift interpolation only changes for draws that were refused
   before).
4. **G1–G6 hold unchanged** (the bound/passage fit path is not touched; `captured`
   classification reads `from_invariants`, which still refuses capture orbits with
   `NoBoundOrbit`).
5. **B17 holds at its passing steps** (its ships never plunge; the new crash-item
   insertion only fires for plunge bindings).
6. **E1–E8 hold** (the engine's one `from_state` call site passes a surface of `None`
   and its orbits are bound cycles; behavior identical).
7. **The plunge tubes are right against a float64 geodesic oracle** (new tests, each
   < 60 s): for a radial fall from rest at r₀ (closed-form t and τ), for the critical-L
   skimming plunge, for near-radial L ≪ 1 and for E = 1 plunges, the compiled arrival
   (t, Δφ, Δτ) and intermediate sampled states agree to better than 1e-5 relative
   (the panels adapt to 2^-32).
8. **Held-out hard cases** (not tuned on): (a) a plunge with L within 1e-6·L_crit of
   the separatrix — I predict the adaptive panels still converge (more of them), the
   arrival still within 1e-5; (b) a window starting at r₀ = 10⁶ M down to r = 2.1 M —
   the phase-15/16 panel ladder keeps relative information; arrival within 1e-5;
   (c) a plunge state whose fitter sees the barrier predicate within one arithmetic
   quantum of zero (a near-separatrix bound orbit) — the existing weak-branch
   behaviour is preserved (it must still fit a cycle, not a plunge), else G1 would
   move.

## What would make this wrong

- Riding a momentary plunge tube during a flyby is a *different* drift than the stale
  old tube; if the plunge arc's curvature over one kick interval is much worse than
  the stale tube's (it points at the star), the recovered draws could stay above 1e-2.
  That would show as: refusals 0 but errors unchanged.
- The crash item at the arrival tick: if a momentary plunge's stale crash item fires
  while the ship is on a later bound orbit, the readout re-check must clear it; if the
  re-check reads past a *plunge* window (Range), the ship is inside the surface by
  construction — if instead a stale item kills a healthy ship, B13 draws would be lost
  (answer None), visible as excluded/lost counts.
- If the barrier predicate's exactness differs between `fit_key`'s Scalar arithmetic
  and the compile's node checks (a plunge whose radial speed squared dips negative at
  a node = a turning point inside the window), the compile must refuse (`Topology`),
  never silently integrate across a forbidden band.
