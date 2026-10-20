# Predictions — the traversed fraction of a fresh mint (mint-knots od 1)

Written before the decisive run. The instrument: a print-only census in
`crates/space/src/orbit.rs` recording, per minted `OrbitShape` (class cycle /
passage), the knot panels the readouts ever land in (`outbound_at` landing and
refine panel, `at_radius` panel, `crossing_state`, passage tail hits) between
the mint and its discard. Coverage = distinct panels touched / (knots − 1).
Controls: the patched binary must reproduce the pristine kick-bench `digest`
and `replay_digest` bit for bit (the census changes no arithmetic); a
synthetic full-walk case (a body read across its whole span) must report
coverage ≈ 1 (the instrument can pass).

Cases not tuned on: a second seed, and the plane's own bodies (made) vs the
handed-out members (leavers) split.

- **P1 (cycles):** median panel coverage < 30%, p90 < 60%. Reason: a cycle
  compiles the whole half-orbit span (0..π) at mint, but the next kick rebinds
  within a fraction of the period (kick cadence ≫ once per period), so the
  walked phase window is a slice of the compiled circle.
- **P2 (passages):** median coverage < 50% but above the cycles' median
  (passage arcs are compiled to the outer radius the body may exit through;
  exit searches bisect across the remaining arc).
- **P3 (shape):** the coverage distribution is bimodal — most mints walk
  little, a minority (boundary crossers, long-lived bindings) walk ≥ 90% and
  own a disproportionate share of all compiled panels.
- **P4 (held-out seed):** medians within ±10 points on a second seed.
- **P5 (the lever):** median eager waste (1 − coverage) ≥ 60% of compiled
  panels per class, i.e. a lazy/streaming compile (pay only walked panels)
  would delete most of the 2.7 µs/knot compile wall.

Kill criterion for the lazy-knots lever: median coverage ≥ 0.8 on both classes
→ no more than 20% of the wall is deletable by laziness; the lever is then the
class-split/cheaper compile, not laziness. If the digest control fails, the run
is VOID regardless of the numbers.
