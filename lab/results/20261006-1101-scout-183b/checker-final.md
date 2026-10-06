Working...
Check written to `lab/results/20261006-1101-scout-183b/check.md` — **Grade: silver**.

What it rests on:

**Reproduced.** C7/C8 bit-identical, C1 identical on all physics fields (author's file predates the `poisson_var_mean` field — code changed after C1, additive only). predictions.md mtime (11:16:05) precedes every decisive run; calibration (smoke, C1) honestly declared. All commands ≤ 12 s.

**Prediction audit.** Honest scoring throughout: exact-zero C3, ×1.18 C5, 0.7% C6 hit; C2/C4 magnitude misses traced to one named error; the failed Poisson control (var/mean 5.15) correctly turned into the finding that killed the event-log cost model.

**My adversarial runs** (author's exact code, extended with the L-key):
- 5× longer chain: saturation holds — log2|kE| 33.84→34.08 over 2000 steps, decelerating (random-walk benchmark would add 1.41 bits; observed +0.65). Seed-robust.
- 10× secondary mass: 18.6% escape the store, survivors bounded at 35.1 bits — the bound survives extremes.
- Mechanism exposed: the belt **empties** (in-belt 0.2% by step 400) — saturation works by evacuating the feeding band, so the "self-limiting rate" is a transient decay, not a steady state. Only the per-body bound transfers.

**Why silver, not gold:** the saturated (kE,kL) pair costs **70.1 bits** (p90 71.8) on the author's own 64-bit-total grid — the 35-bit headline counts E only. 35 bits holds by construction on law.md's 32-bit *joint* (E,L) tube key, which the run never measures. Worst case at 10⁹: 4.4 GB (joint key) vs 8.8 GB (pair) — the key packing alone decides the 8 GB verdict, and the 64-bit Δt_p timing field is unmeasured. One experiment fixes it: re-run the chain with the scar as Δ of the store's native per-band joint key + timing field, making B18's floor representation-native.
