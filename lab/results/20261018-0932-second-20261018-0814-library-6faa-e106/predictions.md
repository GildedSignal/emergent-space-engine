# Predictions (written before the decisive runs)

The wiring is built and unit-verified (instrument only, not the decisive run):
`compile_closed` matches the walked `Orbit::compile` to ≤5.2e-10 relative on all three
increments and ≤7.4e-9 on state readouts over a 24-key ladder (p 2^4–2^18, e 0.05–0.999),
compile 5.8–236 µs → 2.4 µs flat, knot table 180×88 B → 88 B (work/carlson_wiring.json).
Nothing below has been measured yet.

- **P1 (digest identity — the named gate).** With ES_CARLSON=1, the kick-bench's
  `replay_digest` and cut `digest` (a765's harness, seeds 1/7/42) and frame_digest's
  8 flights × 4 schedules will NOT all be bit-identical to the walk arm. Mechanism: the
  closed channels differ from the quadrature by ~3–7e-10 relative, and deadline ticks
  (`fixed_ceil` at the population clock) and boundary classifications inherit that
  error; across ~1,400 rebinds and thousands of reads per seed at least one decision
  sits within that distance of a tick edge. The position channel stays exact (the
  residual absorbs it), so if identity DOES hold, the wiring is an exact duplicate and
  open 1 is adoptable as such — either outcome is the result. My expectation: differ
  (probability ~0.7), because the walk's own certified output quantum (2^-30 ≈ 9e-10)
  is the same scale as the divergence, i.e. the two arms are two different roundings of
  the same continuum, and the outcome channel hashes ticks.
- **P2 (wired rebind cost).** The wired arm's `kick_us` (made bodies, the plane's own
  population) drops by ≥1.5× at the median (compile 52–65 µs → ~2.4 µs; the reads grow
  to 3–20 µs with e), landing the made-kick median ≤ 25 µs; the composed rebind
  (fit_key + compile + at_radius + residual) at plane keys lands at 10–20 µs, inside or
  at the edge of cd6e's 8–19 µs instrument band — the 3.3–9.4× rebind multiple then
  holds as a measurement, not a composition.
- **P3 (the table never allocated).** The rebind's standing knot table per compiled
  cycle drops from 3.8–15.8 KB (43–180 knots × 88 B) to 88 B, measured by the shipped
  per-body estimator on the same keys (already true in the instrument; the bench adds
  the population census).
- **P4 (shipped path untouched).** With the env var unset, the baseline bench digests
  reproduce a765's stored seed-1 clean anchors (replay digest and cut digest
  bit-identical), proving the patch changes nothing when off.

Kill criteria: P1 identity holding on every seed/flight kills my expectation and makes
the wiring an exact win; P2 showing <1.5× on made kicks kills the "plane lever" claim;
baseline digests not reproducing a765 voids the instrument.
