Working...
All suites green (space: 40 passed; universe: 25 passed, 1 ignored). Run complete — predictions, log, held-out digests and dossier are in `lab/results/20261011-0836-autoresearch-469c/`.

**Claim:** on the plane's deterministic kick replay, a fleet member's kick costs ~120 µs of which 87% is the rebind — 57% the `OrbitShape` quadrature and 36% of all kick time `Passage::compile` alone, with the exact shape memo hitting 0% — so no bit-identical micro-optimisation of the compiler reaches 10% (the one kept change, a deleted duplicate `cos` in `node()`, is digest-identical on every held-out case and buys ≈0.8%), and the lever the measurement names is the *number* of passage compiles per kick, not their constant factor.
