Working...
Tests green (66 passed, 0 failed) on the pristine tree; the run folder is complete (`dossier.md`, `log.md`, `predictions.md`, `evidence/` with the re-appliable probe diff and saved JSONs); the tree is restored, so the delivered patch is empty — nothing was worth adopting.

**Claim:** the plane's per-kick cost is structural, not arithmetic — a bit-identical swap of the quadrature's four `u128/u128` divisions for hardware 128÷64 division gains exactly 0%, because 97% of a kick is the rebind, 79% of that is the trajectory compile, and 75% of the compile is the ~70 quadrature panels the EDGE band walk emits per eccentric orbit (the p99 ≈ 390 µs tail is one passage compile at ~374 µs), so the lever is panel count per compile, not per-panel cycles.
