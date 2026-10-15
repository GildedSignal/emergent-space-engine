Working...
`work/e0f9.patch` was written by the harness at 15:34 (not by me, not by the author) — leaving it untouched. The tracked tree is restored, my patch leftover removed; inside the run folder only `check.md` and the page note were added.

**Check complete — `Grade: gold`.** Written to `lab/results/20261015-1450-second-20261015-1338-quant-1d52-0757/check.md`, plus one bracketed checker note added to the proposed `wiki/nladder.md`.

**What I found and did:**

1. **The runner's regen was contaminated, and I diagnosed it.** Between flights 12 and 13 (15:25:12 → 15:25:38), a sibling lab checkout rebuilt the shared `lab-target-0` example binary (mtime 15:25:32). Flights 13–23 — the 48k hot arm and *every cap probe* — flew a stale 1d52-era binary (`hits 0, retained 0`, old counter format), and `table.py` crashed, so regen.sh printed no table. Flights 1–12 flew the correct binary and match the dossier exactly.
2. **I reproduced everything.** Re-applied the patch, built, froze a private copy of the binary, and re-flew all 11 contaminated arms: every count and digest matches the dossier bit-for-bit (e.g. hot16384@10⁵/20k: 131,751 promotions / 763,190 hits / retained 16,384 / rss 412; burn 10⁴ at 65,536: promotions = demotions = 40,187, zero evicts, hits = global's 584,807).
3. **Adversarial cases beyond the author's domain, all confirming:** N=2×10⁵ (identity, 1.007×dem, rss 793 vs shipped 1,069); seed 7 (identity, 1.005×dem); cap 1 (identity, bound holds); burn 10⁵ (identity; 7.23×dem at cap 16,384 — burn's working set scales with N — and **exactly 1.00×dem, 0 evicts at cap 262,144**). The cap rule holds everywhere; only its constant is scene-bound.
4. **Crate suite:** 0 failed (77/3, not the dossier's 46/2 — bookkeeping slip).
5. **Grade rationale:** the record's checker named this exact experiment ("named, not built"); it is now built, flown, and its certificate survives my attacks; it completes the e0f9→1d52 arc into one adoptable knob (~10³× promotion-bill cut at 10⁹, −41% standing store kept). The one real defect — `fly.sh` flying a shared target dir — is a regeneration hazard, not wrong numbers; the fix (freeze a private binary copy) is noted for adoption.
