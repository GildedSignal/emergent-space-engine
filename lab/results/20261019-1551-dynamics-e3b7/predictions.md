# Predictions — gravity-held belt (written before the decisive ladder)

Scene: e56b's mixed fleet×belt with the container replaced by an integer 1/r² central
field via the shipped `Kickable::kick` hook (`crates/lattice/examples/gravitybelt.rs`).
Q = 2^20, `RelativisticV1`, MU = 70·2^52 (v_circ(70q) = q/16), belt = 800 bodies on
rings 36–102q, fleet = 800-body coherent stream at 0.25 q/ch (≈1.9× v_esc(36q), 3.6×
v_esc(102q)). Smoke runs (H ≤ 4096, calibration only): cold belt stable (esc 0,
contacts 0.21/ch, rattle 0); fleet arm shows ejection (esc 1327/1600 by t=4096) plus a
contact core rising to ~1300/ch, 60% rattle.

Arms: G = fleet+gravity (s1 H=49152, s2 H=16384), C = cold gravity control (s1 H=49152,
s2 H=16384), GW = fleet+gravity+walls at ±150q (s1 H=24576). Held-out axes I did NOT
tune on: seed (s2), longer horizon (H > 4096), the walls arm (GW), cold stability past
2048 ch.

- **P1 (cold control must hold; kill branch).** C s1/s2: esc = 0 for the whole run,
  n_in = 800, and the late mean per-64-ch contact rate (last quarter of the run) stays
  within 3× its first-quarter mean. If the cold belt self-heats past that, the field
  wiring is unusable as a control and every other number here is VOID.
- **P2 (season).** G arms: a crossing season exists before the storm; its peak 64-ch
  window is ≥ 20× the cold control's mean window. (Smoke suggests far more; the point
  is the order, not the peak.)
- **P3 (the attractor; three branches, mechanism-argued).** After the season, gravity
  confinement does NOT hold a wall-style plateau: the mass leaves (esc fraction ≥ 70%
  of n at H=16384). Then either
  - **(a) quench:** the storm's late mean rate (last 8192 ch at H=49152) is ≤ 1/3 of
    its peak 1024-ch block mean — the bound core drains through contact ejections
    (v_esc is small inside 40q, so core contacts keep unbinding one partner per pair);
  - **(b) grinder:** late rate ≥ 2/3 of peak — a self-sustaining contact attractor
    worse than the wall plateau (a gate the belt wiring lacks); or
  - **(c) evaporation:** late rate ≤ the cold control's rate — total self-destruction.
  Prior: (a), on the ejection-drain argument above.
- **P4 (walls flip it back; the one-knob contrast).** GW s1: esc ≈ 0 (walls contain),
  n_in ≈ 1600, and the late mean per-64-ch window is ≥ 10× the cold control — the
  e56b-style plateau returns on the same scene when walls hold the energy. If GW also
  decays/evaporates, e56b's "persistence is the confinement's" does not transfer to a
  belt on orbits, and the plateau needs the wall's *reflection geometry*, not mere
  energy containment.
- **P5 (energy honesty; kill branch for the clamp).** All arms: maxk is constant after
  the first fleet contacts (smoke: 739345 from t ≤ 512, never larger), and ke_all never
  rises by > 10% after its season peak. Growth ⇒ the inner clamp (r < 2.2q) or rounding
  injects energy: report as instrument defect, downgrade the run.

What would make the whole run wrong: the fleet's 21-row stream geometry (not a square
block like e56b) changing the season's structure; the every-chronon revision from
gravity kicks inflating rattle-dependent counts (priced by the rattle column, and the
cold control carries the same inflation); the belt being colder (±q/256) than e56b's
cloud (±q/16), so the cold baseline is lower here.
