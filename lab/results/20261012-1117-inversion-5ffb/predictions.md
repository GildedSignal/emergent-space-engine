# predictions.md — 20261012-1117-inversion-5ffb

Written before the decisive `cost` run and before the `bounds` audit finished.
Already run (harness validation, not decisive): one `fuzz` pass — 32 scenes,
20,396 refined sampled contacts, zero certificate misses, zero emit misses,
zero tree-control misses. That pass validated the truth machinery (controls
on both sides: `tight` home regime found k=2–3 and ~110 contacts; the tree
control agreed everywhere).

Target: the co-orbital phase certificate as built on `wt/cx-b-coorbital-cert`
(`crates/encounters/src/phase.rs`), the built form of lab gold
20261006-0346-taleb-09b5.

## Held-out predictions for `invert cost` (not yet run)

The certificate is chosen by `group_events` whenever `Neighbours::new`
succeeds, i.e. whenever `reach < pi`. `reach = angular + 2*centre +
(nhi-nlo)*H/2`. For a group with one shared period (drift term exactly 0)
and eccentricity spread, `2*centre` alone can sit anywhere in (0, pi), so
the certificate stays active with window occupancy k = n * reach/TAU.

- P1 (home regime, control): shared-shape ring e=0.02, rho = 1.5*TAU/n:
  pairs == n, k == 1 at n = 10^4, 10^5, 10^6 (their own gate, re-derived).
- P2 (mild spread, e in [0.05, 0.30], "battered fleet", shared period):
  reach ≈ 1.22, cert_pairs ≈ 0.195 * n^2, growth exponent ≈ 2.00.
- P3 (wide spread, e in [0.05, 0.65], still reach < pi): reach ≈ 2.56,
  cert_pairs ≈ 0.41 * n^2, exponent ≈ 2.00, k ≈ 0.41 * n.
- P4 (tree control on the same scenes): candidate count grows
  subquadratically (exponent < 1.3), wall time per window far below the
  certificate's once n >= 4000.
- P5 (cost ratio): t_cert / t_tree at n = 8000 exceeds 10; per the
  pair-count ratios I expect tens to hundreds.
- P6 (identical results): cert and tree emit the same contact set at every
  n (the seam is cost only, not correctness).
- P7 (self-refusal): a-spread belt (a in [0.4, 2.2], e in [0.05, 0.65]):
  reach >= pi, phase=false, tree used, no blowup.

## Held-out prediction for `invert bounds` (audit still running)

- P8: `centre = e + 2 asin(e/(1+sqrt(1-e^2)))` is a true upper bound on
  max|f - M| for all e in (0,1): slack >= 0 everywhere.
- P9: its |f-E| component `2 asin(e/(1+sqrt(1-e^2)))` is NOT an upper
  bound on max|f - E| — I derive analytically that it is exceeded for
  e ≳ 0.35 (true max at tan(E/2) = 1/k, k = sqrt((1+e)/(1-e))): violation
  ≈ 0.002 rad at e = 0.5, ≈ 0.003 rad at e = 0.9. It is masked in `centre`
  by the slack in |E - M| <= e. If that masking fails anywhere (audit
  decides), the certificate is unsound — the fuzz says it does not fail
  in practice.
- P10: `scale = (1+e)^{3/2}/sqrt(1-e)` >= max_E dM/df exactly (it is the
  closed-form max at apoapsis): slack ≈ 0.

## What would make the run valuable

If P2/P3/P5 hold, the certificate's trigger has a cost blind side: it is
correctness-only (`reach < pi`), never cost-aware, and the "O(n*k)" claim
is vacuous in the transition zone because k = Theta(n) there — the adopted
gold re-opens the O(N^2) scaling risk exactly for concentrated-but-eccentric
groups (fleets after eccentricity excitation, eccentric rings), silently,
while the tree tier it already contains would have stayed near-linear.
