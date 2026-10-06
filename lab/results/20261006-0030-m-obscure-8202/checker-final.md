Working...
Check complete. **`Grade: silver`** written to `lab/results/20261006-0030-m-obscure-8202/check.md`; nothing else in the folder touched, no git commands run.

**What I did**

- **Reproduced** both probes in a clean directory (patch.diff is empty; scripts self-contained): outputs **bit-identical** to the author's, 7.3 s / 7.1 s, ~214 MB peak. Predictions predate scripts and outputs (00:37 vs 00:47/00:53).
- **Attacked probe A**: re-measured the plateau across k ∈ {16,64,96} × fit {1024,4096} (right order of magnitude everywhere); regenerated the 6-sinusoid instrument control (6.1×10⁻¹²); kill holds at c = 5; **scope verified** — commensurate (P ratio 2) and both-circular incommensurate scenes are low-order (k = 12/8), exactly as the dossier's caveat claims, so the kill covers the generic eccentric-incommensurate case only, honestly.
- **Attacked probe B**: crafted spike, overload (identity survives divergence), 400 randomized traces at D ∈ {0,1,2,5} — **zero** violations of backlog identity, soundness *or* completeness (the certificate is exact, not just sound); regenerated the unshipped `id % 8` strawman (244.2× p99, 96.98 % missed); certificates 26 ms–0.13 s. Multisets: single ≡ rotating shards bit-exactly; steal differs on 10 of 266 930 units at α = 1.5 — the "identical multisets" claim is contradicted by the author's own JSON there.
- **Novelty**: no max-plus/Lindley/network-calculus or Prony/Berlekamp lineage anywhere in HISTORY.md or the docs; the cycle-memo reading is grounded in law.md.

**Why silver, not gold**: physics verified, but the record has the exact 5 October taste-log defect — three quoted numbers (plateau values, sinusoid control, 244× strawman) can't be regenerated from the shipped commands (I regenerated them; they hold), plus the steal overstatement and a dead `--seed`. Neither probe moves a bottleneck 10×; both are simulations, not plane measurements. The named gold experiment: wire W*/M into `xtask universe --bench` on a real battle-scene arrival trace and ship the missing numbers.
