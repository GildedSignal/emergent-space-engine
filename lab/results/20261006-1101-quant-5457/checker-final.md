Working...
**Grade: silver** — written to `lab/results/20261006-1101-quant-5457/check.md`; tree restored clean.

**What reproduced (everything canonical):**
- All five digests byte-identical to the author's stored runs on a quieter box; L8/L8b identical, doses distinct.
- Exact counters: encounters 132/132/238/238/178 identical; player items 289→3807 (mine ±1); zero hitches in every run, worst frame 12.3 ms.

**Adversarial probes (held stronger than the author tested):**
- `--unpaced` and `--engine-ms 1` at L15: same digest, zero hitches at 5× budget pressure — the deferral claim in its strongest form.
- Seed 3 L15 twice: dose reproduces (3808 items), digests byte-identical — cross-seed determinism the author left untested.
- Resolved their L15 anomaly: my run counts `decisions: 16/16` — transient coalesced count, not a lost input.

**Why not gold:**
- The dossier's L8 `opens` cell (404) contradicts its own stored JSON (86) and my reproduction; the inference "`opens` is wall-dependent, not dose" is backwards — both L8 runs sit at 86 under different overflow while L15 is 404/406. `opens` tracks dose. A log-contradicted number bars gold by the lab's own rule.
- Predictions #1, #3, #6-rtf failed (honestly reported); and the run *confirms* the budget premise rather than moving a bottleneck 10×, deleting a component, or killing a premise.

**Gold experiment:** cut the 13× player-item growth where it lands — extend the components-4643 window-setup deferral to the player path, ≥10× fewer items at L15, digest unchanged, ≥3 seeds; or kill the four-cycled-headings artifact with randomized headings.
