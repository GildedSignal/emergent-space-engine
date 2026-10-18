# Predictions (written before the decisive flights)

The experiment: an exact key-range fast path in `boundary_clock` (flag `ES_BOUND_RANGE`),
which deletes the boundary's readout walk when the bound cycle's radial range — widened by
the turn's shear slack and the carried residual, both in position quanta — sits strictly
inside (doll surface, leave radius). The boundary keeps its tick and its anchor write, so
nothing observable can change unless the range test is wrong.

Cases not tuned on, and what I expect there:

- **P1 (digest identity).** `nladder 10000 coast` with the flag off vs on: the canonical
  digest at the same cut tick is bit-identical, on the coast arm and on the burn arm
  (thrust rides kicks, never the boundary's tube read), and on a held-out seed.
- **P2 (skip rate).** ≥ 99% of belt clock boundaries skip (3570 measured 99.88% carry no
  news; the range test is strictly broader than the no-news census because it covers all
  certificates at once for the whole tube lifetime). Passage/plunge tubes (3570: the news
  class) must never skip. Planets and doll-local bodies run `boundary`, not
  `boundary_clock`, and are untouched.
- **P3 (wall).** The skipped boundary costs < 1 µs against the shipped p50 ~25 µs
  (3570's number, this box is Linux/x86 so orders of magnitude only); the belt's boundary
  resolver CPU falls by the skip fraction (expect the ~27.8%-of-resolver-CPU term from
  3570 to collapse to ~0.1× of itself).
- **P4 (exactness probe).** On synthetic bindings swept over their whole cycle (bound
  keys near-circular to e→1, plus passage keys): the readout's radius never leaves
  [lo, hi] as computed by the fast path, and passage keys are always refused (None).
  Adversarial surface/leave placed just inside the range must disable the skip.
- **P5 (kill criterion).** Any digest divergence between arms at the same cut, any
  skipped boundary whose shipped twin kills the body, or any probe t whose readout radius
  falls outside the computed range, kills the fast path as built (not the idea: the bound
  would then be mis-derived and must be re-read from the code, per PRINCIPLES 9).

Risk I name in advance: the ±4-quantum turn slack and the residual margin are my reading
of `bind.rs`/`lorentz.rs` comments ("within two quanta of the rotation"); if the true
deviation is larger the probe's dense sweep is what catches it, which is why P4 sweeps
the whole cycle and not just the flown belt population.
