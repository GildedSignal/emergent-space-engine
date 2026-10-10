Working...
Run complete. Artifacts in `lab/results/20261010-1920-quant-9464/` (dossier.md, predictions.md with disclosed postscript, sweep scripts, all raw bench JSONs, table.md); the one-line tree edit (`--members` clamp 400 → 2²¹, `xtask/src/universe/mod.rs:32`) is saved as this run's patch.

**Claim:** the plane's population dial was silently clamped at 400 members, and with the clamp lifted its 60 Hz capacity is ~10³ members — bound first by the readout (~3.4 µs/member/frame, 24× the engine's share, with JSON+wire over half of it and a 2.4× cache-cold tax when paced) and then by the frame's own extent rule, which hands members out above ~10³ and degrades the plane to a non-60 Hz universe by ~8×10³, while threads and the cache hierarchy never get a vote at any reachable size.
