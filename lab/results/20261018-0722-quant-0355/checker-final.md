Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-0722-quant-0355/check.md`, with the page corrected in place and the tree restored to pristine.

**What I did:**

1. **Diagnosed the regen failure.** `work/patch.diff` is `work/fix.diff` concatenated twice (verified byte-identical halves) — `git apply` fails at orbit.rs:549, so the runner's regen.sh exits 1 from a clean tree. Applying `fix.diff` directly, regen.sh runs in 76 s and reproduces **everything**: digest `d2632de9…` kicks 34537 `DIGEST_NEUTRAL=yes`; census bit-identical (148,996 keys, 37,245/37,230, 1,163 classes, hit 0.9922, exact hits 111,766); exactness bit-identical (C p50 1.949e-6 / p99 1.746e-4, B p50 1.197e-4 → 61.4×, med/pred 0.53); timings within 3.5% (6,090/5,642/420/531 ns); tests green with the patch.

2. **Adversarial probes, two outside the author's domain:**
   - `key mashing` N=3000 (churn): exactness survives and improves (C p50 3.5e-7) but **sharing degrades** — 1,831 classes, stream hit 0.927, unique-stream 0.708. The claim's domain now has a boundary.
   - `belt crossing L10` N=3000: 1,389 classes, hit 0.992, C p50 2.3e-6, split 92% — law is mix-stable.
   - **The readout half** (author's named gap, unmeasured): I probed it via public `state()` at 8 phases on all three mixes — C radius p50 ~1e-6 / p99 ~2e-4 vs B ~1e-4 / ~4e-4. The clock order carries to positions; the author's conditional resolves **in the claim's favour**.

3. **Why silver, not gold:** the shipped record cannot regenerate from a clean tree (the taste log's exact record-defect class), and the decisive prediction P2 missed its letter 50× (1–4×10⁻⁴ predicted, 1.9×10⁻⁶ measured — favourably, honestly reported, but "predictions held" is a gold bar). The one gold experiment: dedup the patch and fold the readout census into the dossier with its own prediction — then the premise is fully resolved on the record and adoptable in one integrator step (one-line `QuantizedMemo::get` wiring + B-gate legality flight).
