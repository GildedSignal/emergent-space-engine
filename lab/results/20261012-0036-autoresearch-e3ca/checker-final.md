Working...
Check complete. `check.md` written to `lab/results/20261012-0036-autoresearch-e3ca/`; tree restored (patch reverted, bench copies and /tmp scratch removed).

**Grade: lead.**

What I did and found:

- **Reproduced** from the dossier's commands in a clean tree with `work/patch.diff` applied, using interleaved A/B of separately-built baseline/candidate binaries: output hashes match the dossier exactly on both corpora (`7932a7d0…780f2` main, `1d3ac911…617e2` heldout) and are identical base↔candidate in every round — bit-identity holds. Per-compile −3…6%, kernel −23…27%, p99 main −5.5% — all within the shared box's noise of the author's numbers. 50/50 crate tests including `every_cycle_is_the_compiled_one`.
- **Attacked beyond the author's corpus**: perfect/near-perfect squares at every root width, 2^k±1 for k=40…127, the 2^40 branch boundary, u128::MAX, 3M full-width randoms — both isqrt versions agree *and* each satisfies the exact floor invariant r² ≤ x < (r+1)² per case. The CSE is bit-identical by inspection (`x(psi)` is verbatim the folded expression). The f64 margin (r·2⁻⁴⁰+16 vs error r·2⁻⁵²+1) is sound across the whole u128 range.
- **Reproduced the missing division evidence**: `__udivti3` ≈30 ns < `div_word` ≈38 ns on x86-64 — the div_word rejection stands.
- **Predictions**: written before the decisive run (timestamps verified); the load-bearing bit-identity prediction held exactly; speed magnitudes failed and the stop rule fired — honestly reported.
- **Not silver**: no named follow-up reaches gold from here — the run's own attribution (3 wide divisions ≈90+ ns of ~225 ns/node) caps micro-optimization short of 10×; the real levers (cadence, `word_root` proof) are already the board's queue. The 18-line patch remains adoptable as a free exact win (precedent: "cheaper kicks, exactly", 1932f6c8), which the abstract notes for the integrator.
- **Author's misses**: "all widths" overstated (125–128 and squares absent from the shipped corpus), the div timings and stage-counter attribution are not regenerable from shipped code, and heldout p99 −5.1% sits inside box noise.
