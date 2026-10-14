# Predictions (written before the decisive experiment)

Question: can Carlson's symmetric kernels (RF/RC/RD, and RJ if the source yields
it) run in pure Q62 integer arithmetic (u128 adds/shifts/mults + exact floor
isqrt only) and hold the compile's 2^-30 output quantum on the strong-branch
operand domain, and what is the integer tax against the f64 kernel
(de99: phi 129 ns flat, all-three 2.9 us) and against the shipped walk
(3.2-307 us compile)?

Held-out cases (not tuned on; the grid corners where the record says the walk
itself degrades):
- P1 (error): integer RF/RD agree with mpmath 50-dps truth to <= 2^-30 relative
  on every strong operand set from the key grid (q 1e-6..0.24, e to 0.99999,
  m to 0.99999999), including the m->1 corner where the walk drifts to 6.7e-7.
  Fail mode if wrong: the floored isqrt roundings amplify instead of damping
  (contraction argument wrong).
- P2 (tax): rf_int / rf_f64 wall ratio lands in [3x, 15x] on this x86 box
  (isqrt- and u128-division-dominated); if > 30x the port is not the lever and
  the f64 kernel plus an output quantizer stays the cheaper law-native route.
- P3 (channel): the integer advance (q*(2K(m)/sqrt(A) - pi), K = integer RF)
  matches the shipped walk's increments[0] to <= 6e-10 relative on every strong
  key (both hold their own quanta; the wiki's f64 number was 3.0-4.8e-10).
- P4 (series): a second-order deviation series after duplication to spread
  ~2^-16 keeps P1 (if not, three more duplications is the named fallback; the
  no-series variant that iterates to bit-equal operands costs ~30 duplications
  and I predict it fails P2 by > 5x).
- P5 (RJ): reconstructing Carlson's RJ iteration from memory fails its mpmath
  control (>= 50% odds); then RJ-in-integers stays open and only RF/RC/RD are
  claimed. The tau/t closed-form composition (needs RJ + the squared pole) is
  fenced either way: this run prices the kernels, not the composition.

Kill rule: the port is dead for the law if P1 fails on any strong operand set,
or if the integer tax exceeds the walk's own cost on the cheap end (e < 0.5).
