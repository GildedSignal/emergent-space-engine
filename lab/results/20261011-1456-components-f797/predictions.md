# Predictions — 20261011-1456-components-f797

Component under the lens: **the kick's generator update** (the per-kick rebind of a body's
tube: `Rebinding::from_state` → `Orbit::compile`), i.e. "generators and certificates" for
the doll-tube bodies (planets, belt ships, the player). The bench:
`cargo run --release -p emergent-universe --example kickbench` (code in
`crates/universe/examples/kickbench.rs`), scenes from strong field to belt scale
(rp 16 M … 2^17 M, e 0 … 0.9), each command well under 60 s.

Cases I have NOT tuned on (the bench is written before any timing run):

- **P1 (the rebind dominates the kick).** For every scene, `Rebinding::from_state` costs
  ≥ 3× one compiled readout (`orbit.state`). If false, the generator is not the kick's
  biggest part and this run's premise is weakened.
- **P2 (every fired kick recompiles).** At every kick size tested (1, 2^8, 2^16 velocity
  quanta), 100% of fired kicks change the `OrbitKey` (the periapsis is a full-precision
  `Scalar`, so any velocity change moves it), and ≥ 99.9% change the exact `ShapeKey`.
  This would re-confirm, from a fresh harness, the 5 October memo-artifact correction
  (exact memo hits 0% on distinct kicks) — the plane pays a full cycle compile per fired
  kick.
- **P3 (the compile share).** `Orbit::compile` is ≥ 50% of `from_state` on belt scenes
  (the rest is `fit_key`'s bracketed root search plus the decode/residual). If it is
  < 50%, then the fit dominates and any jet design must be keyed on (E, L) — which
  removes the root search too — or it buys less than half the win.
- **P4 (the jet floor).** A derivative table update in the crate's own `Scalar`
  arithmetic (2 muls + 2 adds per table component: `(5·knots + 3)` components) costs
  ≤ 1/10 of one `from_state` on belt scenes. Then the law's re-anchored jet
  (0.05 compiles per kick, law.md "Not adopted" note) lands the generator cost per
  fired kick ≥ 5× below today's, and within ~10× of the no-anchor information floor
  (the update alone).

What would make the component choice wrong: P1 false (the readout or the force part
dominates), or the crossing tables so small that `from_state` is already cheap
(< ~1 µs), which would cap the whole engine's gain from this component.
