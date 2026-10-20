# Predictions (written before the decisive run)

Question: is the kick's CPU bill and the mint's memory bill the same object — the
exact-quadrature knot vector (`OrbitShape::knots`) that `bind_surface` fills and stores?
If yes, the scoreboard's two gaps (kick ~10^3.3 over floor; live memory ~10^2.6-2.9 over
floor) are one lever: the panel count per compile.

Instrument: `xtask universe --kick-bench` (shipped deterministic kick replay on the plane's
own scene), extended print-only: per timed kick, when the resolver mints a `new_entry`,
record (wall µs, knot count of the minted trajectory, bytes). No behavior change; the
replay digest must equal the shipped arm's on the same seed.

Predictions, held out (not tuned on):

- **P1 (the compile always runs):** a minted `new_entry` appears on essentially every
  fired kick that changes the velocity (share > 95%). Basis: 9edc's 100%-news census.
- **P2 (the CPU bill is the knot filling):** per-kick wall µs and the minted knot count
  correlate (Spearman ρ ≥ 0.5 within one population). Basis: the fit's cost is the
  panel quadrature that fills the knots (b063: bind/refit = 84-89% of a kick); the
  intercept (key fit, turn, residual, decode) is small.
- **P3 (the knot count has real spread on one scene):** the minted knot count spans at
  least a 2× range across the plane's kicks (belt vs locals vs handed-out members),
  because the geometric band cuts follow eccentricity/periapsis. If knots are a constant
  (~43) with no spread, the correlation P2 is untestable on this scene and the run
  reports that.
- **P4 (the memory bill is the same vector):** knots × 88 B are ≥ 60% of the minted
  entry's retained bytes (struct size + Vec contents), on every population.

Kill criterion for the unification: P1 fails, or P2's ρ < 0.3 on both populations, or P4
fails — then the mint's CPU and memory bills are not the one object and the scoreboard's
two rows stay independent.

Controls:
- The shipped (unpatched) kick_bench arm on the same seed must reproduce the patched
  arm's `replay_digest` and `digest` bit for bit (the census is print-only).
- `refused == 0` in both arms.
