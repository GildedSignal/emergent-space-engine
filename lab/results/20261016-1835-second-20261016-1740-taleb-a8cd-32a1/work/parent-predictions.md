# Predictions (written before the decisive experiments)

Question: why does `cargo test -p xtask` fail 7 tests deterministically on this x86 box
(7559's lead) while the integrator's pre-merge suite runs green on the M1? Machine-dependence
vs red main, decided by mechanism on this box.

Hypothesis H: the B12-family corpus is selected by a float64 chaotic oracle (`handoff::assess`:
crossings ≥ 20, `converged` at CONVERGED tolerance, `closest` vs planet radius) whose inputs
pass through non-correctly-rounded libm calls (`sin_cos`, `powf`, `cbrt`, `hypot`) in the seed
path (`ship()`) and at every oracle step. Last-ulp libm differences flip corpus membership;
membership decides which integer-physics runs the tests judge.

- P1 (failure anatomy): all 7 failures assert quantities that flow through `kept()`'s oracle
  fields (`closest`, `converged`, `crossings`) or through law runs whose *ship selection*
  filters on them; no failure is a corpus-independent integer-law assertion.
- P2 (the 24.4 ship): on x86 the filtered `.take(4)` set in `across_a_kick…` is not the frozen
  (M1) set; the ship that drops out (oracle side) reads ≤ ~5 quanta in `j_run` on this box —
  the integer physics is innocent; the membership is the failure.
- P3 (ulp fragility): perturbing the seed `alpha` by ±1 ulp (one bit) flips at least one kept
  ship's (crossings, converged, judged) triple; I expect several of the 16 to flip.
- P4 (two libms on one box): glibc (std) and musl (the `libm` crate) disagree by ≥ 1 ulp on at
  least one of the drawn seed transcendentals (sin, cos, powf(-0.5) at the drawn r), and the
  musl-seeded corpus differs from the glibc corpus in judged membership.
- P5 (control): the 7 failures reproduce bit-identically across ≥ 3 reruns on this box.

Kill criterion for H: if the failing asserts consume corpora identical to the frozen
expectations (no oracle field moved) and P3/P4 flip nothing, then the corpus hypothesis dies —
the failures are a law-side regression on all machines (a red main), to be confirmed by the
integrator's M1 rerun.
