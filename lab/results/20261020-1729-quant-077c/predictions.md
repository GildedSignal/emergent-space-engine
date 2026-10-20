# Predictions — 20261020-1729-quant-077c (written 17:52, before every decisive flight)

The adjudication: 7fd3's census (belt: compile 26% of the rebind, "the fit is the 74%") vs a765's
stage timings (plane: compile 84–87%, fit_key 6%, tail ~8%). One instrument, both scenes, plus a
controlled e-grid. My stage split: FIT = `fit_key` (root witnesses, word choice), COMPILE =
`Orbit::compile`/`Passage::compile`, ANCHOR = `at_radius` + orientation arithmetic, RESIDUAL =
`decoded_event` readout + `Residual::between`. 7fd3's "fit 74%" bucket = my FIT+ANCHOR+RESIDUAL;
a765's "tail" ≈ my ANCHOR+RESIDUAL.

- **P1 (reproduction, plane).** `universe --kick-bench` with ES_REBIND_AUDIT: COMPILE share ≥ 75%
  of `from_state` wall; FIT ≤ 15%. (a765: 84–87% at 4,553 rebinds.)
- **P2 (reproduction, belt).** `nladder 30000 coast 60 1800`: COMPILE share ≤ 40%; FIT+ANCHOR+
  RESIDUAL ≥ 55%. (7fd3: 74/26 at 10⁴.)
- **P3 (the adjudication).** On the e-grid at fixed radius, COMPILE µs rises monotonically in e
  and crosses the FIT+ANCHOR+RESIDUAL stack inside e ∈ [0.1, 0.99]: both censuses are correct in
  their own regime; neither instrument is wrong. The record's "contradiction" is regime, not
  instrument.
- **P4 (instrument control).** Timer overhead bounded: audit-on wall ≤ audit-off bare wall + 0.5 µs
  at every grid cell (four `Instant` reads a call, the ladder's own 20–30 ns/call lesson).
- **P5 (print-only).** ES_REBIND_AUDIT set vs unset: kick-bench `replay_digest`/`digest` identical;
  nladder deterministic fields (bodies, frames, kicks/events per body-gs, refusals, dead,
  truncated) identical.
- **P6 (the belt's unnamed 74%, relocated).** At belt e ≤ 0.4: ANCHOR+RESIDUAL (the two readouts on
  a fresh compile) > FIT (the root search). If instead FIT dominates, the "cheap exact fit / key
  reuse" program is confirmed directly at the belt. Either outcome relocates the 74% to a named
  stage — the decision the frame-cost page waits on.
- **P7 (capacity).** e = 0.99 compile ≥ 10× the e ≤ 0.1 compile (cd6e's e-monotone law, orders of
  magnitude on Linux/x86).

Kill criteria: if P1 or P2 fails under the one instrument, the instrument differs from a765/7fd3
in a load-bearing way — no adjudication claim until the difference is named. If P4 fails at any
cell, the shares are timer-polluted and the run reports walls only.

Held-out for the checker: seeds/rtf other than mine, N=10⁴ vs 3×10⁴ belt, burn vs coast, and the
grid's radii I did not fly.
