Working...
Check complete. **`Grade: silver`** written to `lab/results/20261013-0350-components-c914/check.md`; two overstatements corrected in the run's `wiki/kick-jet.md`; tree restored to the clean base I found it in (the runner had already reverted the patch — I applied it myself and verified my orbit.rs hunk matched `work/patch.diff` byte-for-byte).

**Reproduction (all from the author's exact patch, clean tree at `cb16ccb9`):**
- Division floor: 30.28 / 34.99 / 31.09 (divq, 1.03×, 0 mismatches) / 31.48 ns (Newton, 1.04×, 1 mismatch at d=3) — matches dossier within noise; checksums byte-identical in every run; 63/63 tests.

**Attacks (three of my own, one outside the author's range):**
1. **Extreme grid** (e 0.001–0.999, octaves −8…26, beyond the tested e ≤ 0.99 / −6…24): shares hold by total (div −19.4%, cos −12.0%, sqrt −6.7%) — inside the claimed bands, low end. The *median* compile is unmoved (cuts land on the tail), so the shares are aggregate.
2. **Identity vs the truly unpatched tree** (hacks stripped, rebuilt): checksums identical — the probe changes no shipped bits.
3. **Divisor trace** (instrumented `fast_quad`): every shipped divisor ≥ 2^51 — Newton's "0 mismatches on the domain" covers real operands; one edge found: `ONE+root` hits exactly 2^63, outside the documented [2^20, 2^63). Plus: a **div+cos pair arm** (author never ran) confirms shares add only to first order (−54% ≈ sum of singles; sqrt adds ~2.5 pts on top vs 11.6% alone), and source confirms all four divisors are psi-dependent, so the wiki's cached-reciprocal variant is structurally dead.

**Why silver, not gold:** the pre-registered predictions did not all hold (Newton's 8–18 ns predicted → 31.5 measured; the ordering flipped by the author's own criterion; per-node above band — all disclosed honestly), and the kill is x86-only while the goal machine is the fanless M1 (aarch64, no 128/64 divide — the one place the reciprocal could win). **The one experiment:** run the shipped `div_bench` probe on arm64 (hosted runner or the integrator's M1); if Newton loses there too, this is gold.

**Page corrections:** "no cheaper exact division *exists*" → none *was found among the three variants tested*; and the "~1.4× even at a 2× division win" arithmetic fixed (2× win ⇒ ~1.1×; ~1.4× is the all-three-ingredients ceiling; free divisions ⇒ ~1.2×, the dossier's own number).
