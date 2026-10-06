Working...
Done. The patch kept is exactly the one change that survived the digest gate; instrumentation is stripped, tests and the frozen judge are verified against the stashed baseline.

**Claim:** the plane's kick resolver pays one redundant full decode per rebind — `bind_in` throws away `from_state`'s `Residual::between(decoded_event())` — and deleting it (`from_state_lean`, +15/−2 lines) cuts the kick's median cost 14% (made) / 15% (leavers) with all replay and state digests bit-identical across three seeds, while the measured anatomy shows the rest is compile-bound (85% quadrature, ~520 `cos` + ~520 `div_word` per compile at near-hardware-floor primitive rates), so the next 10× is structural: lazy knot compilation, not micro-optimization.
