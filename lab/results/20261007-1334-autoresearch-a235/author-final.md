Working...
Run complete: predictions pre-registered, loop logged (4 rounds, stop rule hit), held-out run done, digests bit-identical throughout, 50 tests green, patch saved (`patch.diff`, 17+/9− in `crates/space/src/orbit.rs`), dossier written.

**Claim:** the plane's dominant per-kick cost — the orbit recompile in `Rebinding::from_state` — drops 16% (tuning) / 12.3% (held-out) median ns on a quiet core, bit-identical by digest, by replacing `fast_quad`'s four 128-bit hardware divisions per node with the crate's own exact 128/64 word division wherever its precondition provably holds.
