Working...
Check complete. `check.md` written to the run folder; nothing else in `lab/results/20261008-2113-components-a9d7/` touched, no commits, tree restored to patch state (md5-verified `hlive.rs`).

**Grade: gold**

Basis, in brief:

- **Exact reproduction.** Patch applied → built → s2 re-run: 219,822 rows, digest `44b95de8…` identical to the author's stored summary. Every dossier table cell verified (fresh s2 run + `analyze.py` over the author's stored s3/inner/outer, including the split a/b rejoin).
- **Predictions held out honestly.** Written 21:21, data 21:25–21:37. Five of eight held; the biggest miss (H(dv) 86 vs 4–14) is the headline finding, correctly attributed to the lattice exponent.
- **Attacks strengthened it.** N-scaling at n=2048 (rate 3.595e-5 vs 3.578e-5 — the extrapolation to 10⁹ is valid, predictions' own invalidation test); hot belt e≤0.9 (rate unchanged, h_dv *worse* at 91.4, growth still ballistic); source-level checks confirm fires-by-construction (`step.rs` returns before rebind when `dvq==0`), the ±2¹⁶ carry bound, and the 2⁻⁷⁴ lattice arithmetic behind the 86-bit figure.
- **Premise correction.** The board says the distinction *rate* decides 10⁹-in-8-GB; measured, the rate is trivially affordable (0.4 MB/s at 10⁹) and the per-distinction lattice cost breaks the budget from the first kick. That redirects B18/shipmem to a deviation-native quantum (~2⁻³³ c, 25–30 bits/kick) — adoptable in one step, with the representation change gated on the named B5/B12 experiment.

Noted misses: the replay/re-derivation objection (scars are deterministic from programs — the 86 bits is a scar-store cost, not an absolute floor), the undisclosed n 4096→512 drift in case definitions, and the 10-year figure being extrapolation over <1 orbit at the belt's outer edge.
