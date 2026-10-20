# Predictions (written before the decisive flights)

Question: is the belt's contact-driven self-destruction a **first-passage process** —
contacts random-walk osculating e at (near-)conserved body energy, the DK_CAP clamp zone
below r ≈ 2.1q absorbs, and the survival curve follows from a measured per-contact
diffusion constant — or something else (a few bad bodies, a contact-rate runaway, an
unbounded drift)?

Arms (all `beltewalk`, H = 49152 unless noted, m = 800 belt bodies, rings 36–102q):
A thermal ±q/256 seed 1; B cold (thermal 0) seed 1; C thermal seed 2;
D Pass thermal seed 1, H = 8192 (instrument negative, 9b3b's control).
Smoke (H = 4096, seed 1): 1096 contacts, 2 U events, 0 D — calibration only, horizon
chosen for the 10k+ onset class (e3b7's smoke lesson).

- **P1 (causal chain, per body).** For ≥ 80% of bodies with a D event (first r > 250q):
  osculating e rises while per-body k² is still flat (energy conserved by the walk),
  first snapshot with r_p = a(1−e) < 2.1q precedes the first clamped chronon, clamps
  precede U (ε ≥ 0), U precedes or accompanies D. Bodies that never cross r_p < 2.1q
  keep k² within ±10% of their genesis value for the whole flight.
- **P2 (diffusion).** Before the first D in each arm, Var(e) over alive bodies grows
  linearly in mean cumulative contacts per body (R² ≥ 0.9 over ≥ 8 windowed points);
  the per-contact second moment ⟨Δe²⟩/contact agrees across A/B/C within a factor 2.
  If Var(e) grows without contacts (Pass arm) or jumps (not linear), diffusion is dead.
- **P3 (first-passage sizing, held out).** Deaths order by genesis ring: hazard
  monotone in e_c = 1 − 2.1q/a_ring (inner rings first), at roughly equal per-ring
  contact rates (the genesis fills slots ∝ r, so surface density is near-uniform and
  contact rate does not confound the ring order). The median death time of the
  earliest-dying ring in arm A is predicted within a factor 2 by
  (e_c − ē0)²/(2·D̂), with D̂ measured on arm B's early window (cross-arm, held out).
- **P4 (survival shape).** After the onset, ln N_alive(t) is linear in t (constant
  hazard, quasi-stationary residue) in A and C, with the same slope within a factor 2
  across the two seeds; a strongly convex (accelerating) survival would instead
  indicate the contact storm feeds itself and the single-diffusion picture is wrong.
- **P5 (negative control).** Arm D: 0 contacts, 0 U, 0 D, maxk drift < 1%, cumulative
  clamps 0 for all bodies (no body's pericenter enters the zone on a circular-ish
  orbit). Any failure here breaks the instrument, not the law.

Kill criteria: P1 ordering failing on most dead bodies kills the chain reading;
P2 nonlinear kills the diffusion framing; P3 inverted (outer rings first) kills
first-passage sizing; P4 accelerating kills quasi-stationarity and hands the reading
to the storm. Any of these is a result to report, not a reason to re-tune.
