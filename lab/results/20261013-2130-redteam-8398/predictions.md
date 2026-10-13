# Predictions — 20261013-2130-redteam-8398

Target premise: representation.md §3 / law.md:51 / gate B8 — "two evaluation orders of the same
event graph, with identical bits". Untested seam: a body crossing the order boundary changes
representation (tube ↔ Cartesian member); the shipped exit path is `Rebinding::from_state`
(bind.rs:266, `resolve_handout`). Necessary condition: the pure-transit round trip
key → decoded state → refit must return the same law-level orbit, or the two orders' event
graphs differ by a refit event the sparse order never performs.

Instrument: shipped integer code only (`crates/space`: `Orbit::compile`,
`binding::cartesian`, `Rebinding::from_state`). Grid fixed a priori, nothing tuned.

Cases (held-out marked † — not looked at before writing this file's expectations):

- P1 **Key identity.** Circular keys (e = 0) round-trip the key exactly (fit_key has an exact
  circular branch). Eccentric keys: the Q48 k word changes in its low bits on most phases,
  and the mismatch grows with e. †At e ≥ 0.99 I predict the periapsis word also moves on some
  phases (quantization-boundary crossings).
- P2 **Residual.** The fit residual (exact i128 difference at the event) is nonzero on most
  eccentric decodes but small (≤ a few state ulps). If it were huge the instrument is wrong.
- P3 **Future divergence.** Decoding the refit and the original trajectory a quarter cycle
  after the event: differences grow with e; at e ≤ 0.1 they stay within ~tens of position
  quanta (2^-30 M — far below any player floor), at e ≥ 0.99 I predict ≥ 10^3 quanta.
  The breach is law-level (partition-dependence, B8's letter), not player-visible position.
- P4 **Cost corollary** (no new measurement): every mismatched transit mints a new Catalogue
  entry and pays one compile (5.8–374 µs, kick-jet wiki) instead of sharing the memo — the
  "same event graph" claim is also a cost claim.
- P5 **Controls.** Positive: the circular branch returns the identical key (the instrument can
  report identity). Negative: a one-velocity-ulp perturbation must change the refit outcome
  somewhere on the grid (the instrument can detect change). If the positive control fails the
  probe is VOID.

What would make the attack wrong: if from_state returns the exact key on essentially all
eccentric decodes (P1 fails low), the boundary is idempotent as built and the premise stands
on the shipped seam; the dossier then reports a surviving premise with the measurement as its
first certificate.
