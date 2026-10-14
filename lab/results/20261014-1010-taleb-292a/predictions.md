# Predictions — 20261014-1010-taleb-292a (written before the decisive run)

Question: the adopted ephemeral-promotion design (demote at commit; b29a's composed path)
multiplies compact↔live crossings. The compact row (`shipmem::Body`) holds only
(p, e, w, t) — the live side's `Residual` (up to 4×65 bits, binding.rs:74) has no home
there. Does one crossing's error stay bounded (a fixed point or small cycle in column
space), or does it walk (compounding, principle 13)? 8398 measured the KEY-level transit
(no fixed point on 112/112); the state/column-level cycle with the doll-unit rounding is
unmeasured (the page's named gap).

Cases I have NOT tuned on (the run measures them first time):

- P1 (control, must hold): `Rebinding::reconstruct()` is an exact left inverse on every
  probe state (residual carried ⇒ within-order identity). If this fails my harness is
  broken, not the engine.
- P2 (control, must fail): a real kick (velocity perturbed by 2^-10 of |v|) moves the key
  by ≫ 4 Q48 k-ulps — the instrument sees physics.
- P3: single crossing at fine words (units = the state's own scale): key moves on most
  probes (8398 control, expect ~100%), one-shot |residual| ≤ 2 position quanta.
- P4 (the decision): at fine words the chained crossing WALKS one-signed (8398's
  −1 k-ulp/transit directed drift) — unique keys ≈ depth, |Δk| grows ≈ linearly, no
  repeat to depth 64. At coarse words (+8 exponents) the walk drowns in the word: small
  cycle or bounded jitter (unique ≪ depth). So "bounded vs compounding" is decided by
  the doll's word scale, not by the fit.
- P5: the non-unity doll (μ ≠ 1, one extra `to_tube` position rounding per crossing,
  `in_tube_units`) adds at most ~1 quantum to the per-crossing residual and does not
  change the bounded/walking class.
- P6: cost per crossing (compile + readout + cartesian + from_state) is 20–80 µs, i.e.
  the same class as b29a's refit arm (21 µs) — the crossing is affordable per event; the
  question is the error, not the CPU.
- P7: high-e (0.99) and circle (e = 0) configs refuse or leave their class on a minority
  of probes (8398 saw 3/15 silent refusals, circles leave the exact class); refusals are
  counted, not silently dropped.

Kill criterion for the "bounded" hope: if ≥ half of the fine-word chains have unique
keys = depth with one-signed Δk, the seam compounds at fine words and the integrator
must carry the residual (or the columns must widen) before demote-at-commit lands.
