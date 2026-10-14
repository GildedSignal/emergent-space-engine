# Predictions (written before the decisive run)

Question (the checker's named experiment, cheapest decisive part): can the readout's
re-integration — the 2.8–2.9 partial-panel quads + 1.9 Newton rate evals per time→state
readout — be replaced by an **incomplete-Carlson closed form for the t channel** that holds
the walk's own contract at the brackets the plane actually reads, and what does it cost?
Plus the record fix: `R_QUADS`/`AR_QUADS` were declared and consumed by the example's
summary but never bumped by the hooks, so regen printed "build 73–75%" against the
dossier's 31/69–34/66. I fix the two bumps; the record must then print its own split.

- **P1 (the record fix regenerates the split).** With `R_QUADS` bumped at the readout's
  `quad(a, psi)` and `AR_QUADS` at `at_radius`'s `quad(base.psi, psi)`, the example's own
  summary line prints build/read splits within ±2 points of the hand-recomputed 31/69
  (400 members) and 34/66 (1,500), and every other counter and the digest `b1feb4bf…` are
  unchanged (the bumps are additive counters; no arithmetic touched).
- **P2 (the closed form honors the walk's acceptance at the walk's own ψ).** On every
  captured readout of the shipped plane arms (strong/fast/weak branches), the closed-form
  t-channel T(ψ) evaluated at the walk's accepted ψ satisfies |T(ψw) − target| ≤ the
  walk's own quantum band in ≥ 99.9% of readouts, with the worst tail ≤ 4× the band (the
  fast path's u64-isqrt floor is itself ~2⁻³⁰ relative — the named contract).
- **P3 (inverted ψ agreement, the 2⁻³⁰-in-ψ contract).** Newton on the closed form from
  the same bracket/fraction start lands within 2⁻³⁰·2π of the walk's ψ (normalized) on
  ≥ 99% of readouts; the tail is bounded by the acceptance band width (both answers lie
  inside a band whose half-width is the clock's information floor), never by a divergent
  root.
- **P4 (the price).** The closed-form readout (2 RJ + 1 RD-class incomplete forms + one
  Newton polish, f64) prices ≤ 400 ns per readout on this box against the walk's measured
  ~1–2 µs per readout on the same stream (the frame-cost page's 4.6 µs includes the bracket
  walk and state read) — a ≥ 5× readout-side cut, deleting 100% of read-side integrand
  point-evals.
- **P5 (digest identity is unpassable by construction — the honest negative).** The walk's
  acceptance is a band, not a point: any ψ with |t − target| ≤ quantum is accepted, the band
  is ~10⁷–10⁸ ψ-ulps wide, and the digest hashes ψ ulps. No closed form can be pinned to
  the walk's integer quadrature bit-for-bit, so "deleted digest-identically" as literally
  written cannot pass; the passable certificate is the quantum contract (P2/P3), the same
  standard the kick-jet page already uses for the complete forms (de99: agreement to the
  walk's 2⁻³⁰, not bits). I predict the measured band width to exceed the ψ disagreement
  by ≥ 10×, making the swap a law-level adoption (6c47 precedent), not a bit-identical
  deletion.

If P2/P3 fail on the fast path beyond 4× band: the fast path's integer floor is coarser
than the closed form's f64 precision and the swap would *tighten* the readout — report the
direction of every violation (error type over error size).
