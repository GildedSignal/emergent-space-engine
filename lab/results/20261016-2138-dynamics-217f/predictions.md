# Predictions (written before the decisive battery runs)

Mechanism under test: `escalation *= 2` at every rollback (alloc.rs:1410), global, no decay;
feeds `speed_factor` → forecast box growth and the regroup island cut. Conflict source: a
post-anchor acceleration (Fermi cannon: light body between closing heavies, ~2× per bounce)
outrunning the per-stride forecast (margin·vmax from the last anchor), meeting another
region's true box within the same window before the planned merge catches it.

Not tuned on: the battery scene is derived, not fitted; these predictions precede its first run.

- **P1 (relativistic quench).** Under `Law::Relativistic`, no body exceeds c = q quanta/chronon,
  so a promise can break only while forecast growth margin·E·vmax + (E−1) < c. Rollbacks
  therefore go extinct once E ≥ E* ≈ c/(margin·vmax + 1). With vh = q/8, margin 2:
  E* = 2 → expect at most 1–2 conflicts total, escalation frozen at 2–4 forever after,
  zero further rollbacks however long the run.
- **P2 (Newtonian ratchet, no fixed point).** Under the Newtonian law the cannon's light body
  accelerates without bound (measured on the bare stepper: 64 → 16384 quanta/chronon within
  200 chronons), so every E is eventually outrun. Expect: rollbacks recur at every ignition,
  escalation climbs monotonically (≈ one doubling per conflict, no decay ever), and the
  partition coarsens with it (forecast boxes ∝ E plan merges ever earlier): region count
  collapses toward few/1 and stays there — a one-way latch, the scan-queue latch's shape
  (69f3) in the allocator.
- **P3 (self-healing contrast).** The AIMD stride (halved on rollback, +1 per accepted stride)
  restores after each conflict (stride p50 back toward the 256-chronon sync grid within a few
  hundred accepted windows), while escalation does not: same controller family, one restores,
  one ratchets — the asymmetry is the missing decay law, not AIMD.
- **P4 (outcome invariance).** Every arm and any scheduling difference leave the final world
  and outcome digests identical (the certificate's union guarantee): the ratchet moves speed,
  never results.
- **P5 (decay arm, patched, env-gated ES_DECAY, off = shipped verbatim).** Halving E per
  conflict-free sync grid (mirror of the rollback doubling) turns the ratchet into a bounded
  cycle: E oscillates near the conflict boundary instead of climbing; region count stays
  finer than the shipped arm at the same tick under the Newtonian battery; digests identical.
- **P6 (throughput cost of the latch).** Under the Newtonian battery the shipped arm's
  region-chronons/wall-second at late stages falls well below (≥2×) the decay arm's on the
  same scene, because the partition has coarsened to fewer regions than workers (idle
  workers: utilisation columns).
