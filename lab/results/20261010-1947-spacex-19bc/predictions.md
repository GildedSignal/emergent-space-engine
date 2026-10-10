# Predictions (written before the decisive runs; smoke at rtf 100, 5 s only)

Held-out cases: seeds other than 1, rtf 10× and 10× away from the smoke run at matched game-time,
and the store-size trajectory (never looked at beyond one sample).

- **P1 rtf invariance.** Rates per ship per game-second are properties of the canonical event
  stream, not of the wall: rtf 100 (30 s) and rtf 1000 (3 s), both 3000 game-s, agree within 10%
  per population (plane-made vs fleet members separately). If they disagree more, the wall leaks
  into the law and that is a finding, not noise.
- **P2 fire rate.** ≥ 95% of distinct pending kicks rebind (the sigma-delta carry absorbs a whole
  kick almost never). Smoke: 100%.
- **P3 bits per rebind.** Coarse (conditional entropy of the 24-bit quantized key, per body):
  0.3–3 bits. Exact bracket (first difference of the exact shape key at Q48, p50): 8–20 bits,
  dominated by dk ( periapsis difference ~0 bits). Smoke: 0.58 and 13.7.
- **P4 scale verdict.** With creation in the measured bracket, one hour of play at 10⁹ ships
  creates 3–90 GB of distinction without reabsorption: the "10⁹ in 8 GB" premise survives *only*
  with working reabsorption. Predict reabsorption duty cycle at 10⁹ (pop = 128 packed blocks,
  recompile cost = the measured kick resolver cost) is < 10% of one core.
- **P5 store.** The current store's bytes/body has a positive slope over the run (history
  segments), so the memory idiot index (bytes grown per game-second ÷ bits created per
  game-second) is > 100.

Kill criterion for the whole run: if the replay digest changes between two identical invocations
the harness is unsound and everything above is void.
