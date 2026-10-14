# Predictions (written before the decisive run)

Question: the smallest promotion between a compact belt body (shipmem `Population` row)
and a live law body, composed from shipped pieces (`Key::darwin` → `Orbit::compile` →
`binding::cartesian` → integer impulse → `Rebinding::from_state` → `Population::scar`),
against a key-space arm (integer ΔE/ΔL on the key's own Q48/Q32 quanta, then
`OrbitKey::from_invariants`).

Cases not tuned on (the bench sweeps them, predictions written blind):

- **P1 (cost, refit arm).** The composed ephemeral promotion costs 60–400 µs/event on
  this Linux box, dominated by `Orbit::compile` + `Rebinding::from_state` (the record's
  exact refit is 75–160 µs; sticky hand-out 486–585 µs). The scar write and the compact
  read (`body(i)`) are each < 1 µs.
- **P2 (bytes).** Standing bytes per event ≤ 12 B amortized (the hot scar batch), i.e.
  ≥ 600× under the shipped sticky promotion's 8,257 B; no RSS growth beyond the batch.
- **P3 (zero-impulse identity).** With no impulse, the refit returns the same `k` (Q48)
  as `OrbitKey::from_invariants` on the body's own birth key for ≥ 99% of bodies at the
  shipped belt band (p ∈ [2048, 4096) M, Rayleigh e σ0.07 cap 0.6); periapsis within
  2⁻²⁰ relative. Failures concentrate where the readout's Q30 velocity rounds (the
  near-circular low-e bulk).
- **P4 (key-space arm, the held-out half).** At belt encounter impulse scale
  Δv/v ≤ 1e-4, the integer key kick lands within ≤ 8 quanta of `k` (Q48) and ≤ 2⁻²⁰
  relative periapsis of the refit for ≥ 95% of bodies; divergence grows sharply by
  Δv/v = 1e-2 (regime boundary: the refit is the truth there).
- **P5 (the 10⁹ read).** The refit arm at the quiet-belt rate (3.6e-5 events/body/game-s
  × 10⁹ = 3.6e4/s) costs 2–15 Linux cores — consistent with the ledger's 8.3-core kick
  wall at 231 µs, i.e. the promotion CPU *is* the kick. The key-space arm costs < 0.01
  cores: if P4 holds, the belt's event stream needs neither the refit nor the compile,
  leaving encounter discovery as the cold rail's only CPU term.
- **P6 (the grade).** The i16 scar delta overflows (Wide records, 40 B) for < 5% of
  kicks at Δv/v ≤ 1e-4; the overflow fraction crosses 50% only at Δv/v ≥ 1e-2.

Kill criterion: if P3 fails below 99% (the law cannot re-derive its own key from its own
readout), the composed path is not a promotion but a law-change detector, and the claim
dies. If P4 fails at 1e-4, the key-space kick is not a promotion substitute at belt
scale and only the refit arm stands.
