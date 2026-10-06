Working...
Check complete. `check.md` written, tree restored to pristine.

**Grade: silver.**

**Reproduced (this box, clean tree + applied `work/patch.diff`):**
- **Bit identity, full:** all six digests (replay + state, seeds 1–3) match the author's `predictions.md` exactly; my adversarial held-out seed 7 also bit-identical; refused=0 everywhere.
- **Tests:** 0 failed, 1 ignored (99 passed — author said 67; verdict same, count differs).
- **Frozen judge:** `behave --law plane` on both binaries — every verdict and number identical; only timestamps and B13 wall time differ, exactly the author's own diff.
- **Primitives:** cos 46.7–47.1 ns, div_word 18.5 ns (author: 47.7/18.0) — the ~25% micro ceiling arithmetic holds.

**Correction found by attack:** interleaving both built binaries (6 alternations, seeds 1/7) gives made 34.9→31.6 µs (**−9.5%**) and leavers **−3.7/−5.1%** — not the claimed −14/−15%. The author's baselines were measured in post-build machine state; I reproduced that bias (same binary: 34.9 µs interleaved vs 36.7 µs post-build). Their own predicted bands (−5–10%, −3–6%) are what actually held.

**Novelty:** Sol's 1932f6c already ran one bit-identical kick-cheapening pass on this bottleneck; this redundancy is distinct and unremoved. The lazy-knot lever is new but unbuilt.

**Gold path:** build the lazy psi-window compilation prototype and measure the compile term's collapse at identical digests.

**Misses named:** timing-protocol control, test count, and an unnamed tail risk — `from_state_lean` can bind where full `from_state` refuses if the internal `decoded_event()` range-errors (narrow window, never exercised).
