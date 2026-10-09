Working...
Check complete. `check.md` written; tree left pristine; nothing else in the run folder touched.

**Grade: lead** (matches the author's own suggestion).

**What I did and found:**

- **Reproduction** — applied `work/patch.diff` to a clean tree, ran the dossier's commands: `ab.sh tune` A 1291/1290 k-ns → B 1229/1238 k-ns (−4.9% total, median −7.1%); `ab.sh heldout` A 2377/2467 → B 2262/2313 (−5.0/−6.2%, median −9.7/−11.1%). Fingerprints `f4bd77fc76c8b072` / `9356db3f24802745` identical A↔B on both populations — the author's −4.7%/−5.3% claims reproduce. 50/50 crate tests in release **and** debug (debug fires `div_word`'s asserts). My first held-out "baseline" was invalid (the patched rebuild swapped the binary mid-run) — discarded and redone properly with the interleaved `ab.sh`.
- **Attack (3+ cases)** — (1) my own extreme bound keys (p_exp −3…40, e up to 0.9999 and Q48-max): fp `326ecca43a0d1207` identical A↔B, refusal patterns matching; (2) photon/null keys b = 2.5…2⁴⁰ through the same `fast_quad` (the wrapped-`a` path the dossier flags): fp `81d2c7ec25166e0f` identical; (3) `div_w64` extracted verbatim, 10,000,836 boundary/adversarial cases vs `(n/d) as u64`: all equal. Bit-identity holds everywhere I could push it.
- **Pre-registration** — predictions.md predates the decisive runs; the honestly **failed P1** (predicted ≥25%, got 5–9%) is the strongest signal it wasn't post-hoc.
- **Why lead** — 0.05×, not 10×; deletes nothing; and the same class of bit-exact single-digit kick speedup already exists in commit `1932f6c` (Sol, 1 Oct, 25.75→23.71 µs), which the dossier doesn't cite. No named experiment on this path reaches gold — P1's own failure bounds division-elimination to a few more percent. Also x86-specific: 5% is below the lab's order-of-magnitude floor and the M1's `udiv` economics are unmeasured.
- **Missed by the author** — the 1932f6c prior-art citation, and a probe of the ~5 µs fixed `Scalar` cost that dominates the weak-key compile (the one non-marginal question visible in their own instrumentation).
