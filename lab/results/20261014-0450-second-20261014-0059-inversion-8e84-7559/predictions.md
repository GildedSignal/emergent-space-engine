# Predictions — second-author run on 20261014-0059-inversion-8e84

The named experiment (check2): run M-kick and M-prune against the shipped test
suites, the shipped way (`xtask test` = `cargo test --workspace --release
--locked --offline`). If neither suite kills them, the two gate-dark mutants are
guarded nowhere in the repo and the premise-wrong result is total. Written
before any test run in this session; the only inputs are the source of
`observe.rs` (`credit`, `partial`), the test files, and the parent run's record.

## P1 — M-kick (step.rs:440, `Kick.len >> (2·level+1)`) vs the universe suite

**Prediction: the suite does NOT kill it (my probability ~0.55); if it dies, it
dies in `motion.rs`.**

Mechanism for surviving: the ramp (`observe::credit`) and the partial step
(`observe::partial`, validity window `2·k.len`) are the only read paths that
use `Kick.len`, and the running tests that touch between-kick state either
read raw `readout` (origin.rs, motion.rs's map tests) or read at boundary
ticks where `partial` returns the base state (`tau <= 0`); the judge-driven
between-kick tests are ignore-marked (motion.rs:229) or assert relative bounds
over an ensemble.

Mechanism for dying: any running test that calls `ramped`/`root_state` strictly
inside a kick window with an absolute bound (motion.rs:286
`the_readout_between_kicks_is_bounded`, motion.rs:303) sees a first-order error
— halving `len` doubles the ramp's slope over `[m, m+len/2)` and leaves
`[m+len/2, m+len)` on the raw tube, an O(dv) readout error, far above a 1e-4
gate.

## P2 — M-prune (universe.rs:1105, margin `1<<26` → `1<<20`) vs the suites

**Prediction: survives both suites (my probability ~0.8).**

Mechanism: `prune` keeps `min(now − keep, oldest − 2^26)`, and `oldest` is the
oldest resolution any body still owes — pending work pins history regardless of
the margin. The gate already showed `1<<20` and even `1<<2` replay-clean at
48 members; the tests run the same scale. A test could die only if it walks
history further back than any pending resolution (ties.rs's order-equality
reads full histories, but prune cuts all arms equally, so equality survives).

## P3 — controls (must hold for the instrument to be valid)

- Clean baseline: both suites green (only the known ignore-marked tests
  skipped).
- **M-wrap positive control**: the lattice suite FAILS under M-wrap
  (`hit_is_exact_past_the_i128_products`, check2's finding) — the suites have
  teeth where the gate is dark, so a pass under M-kick/M-prune means "guarded
  nowhere", not "instrument broken".
- Restore control (git checkout + touch, the parent run's protocol): both
  suites return to the baseline, bit for bit.

## P4 — scale of the kill, if any (held out)

If M-kick dies, I predict exactly 1–3 tests die, all in `motion.rs` or
`clock.rs` (the readout-path tests), and the physics/digest tests
(ties, replay, flight, origin) stay green — the digest never sees `b.kick`,
so no digest-equality test can die; what dies must read the ramp.
