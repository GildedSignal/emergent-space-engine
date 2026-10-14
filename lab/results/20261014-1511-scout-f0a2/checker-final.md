Working...
`check.md` written: **Grade: gold**.

Verification trail:

- **Reproduction**: `regen.sh` green in a clean tree (17 s); all deterministic fields of both seed scans bit-identical to the runner's copies — only the inherently timed `bench_ns_per_pair` moved (1.13 vs 1.02 ms/pair).
- **Anchor verified in shipped code**: `lib.rs` `Key::new` stores E absolutely in Q48 on scale 1 → one quantum = 319.3 m²/s². Hand-recomputed K, D* (318.9 ≈ q), n_large (6.72×10⁵), Dcrit (34.2 km), the 129× wake cut, and the 0.031/0.153/0.612-core routing row from the JSON.
- **The 0b81 dispute adjudicated from 0b81's own branch**: its `gate.py` tests `dEi = 2*dvi/vi` (relative δE/|E|) against absolute `2.0**-48` — binding-relative, ~10⁸× tighter than the shipped key's flip threshold (2⁻⁴⁸/|1−E| ≈ 7×10⁻⁷). f0a2's reading supersedes; 0b81's miss-model correction survives. Recorded as a sub-bullet in the page's Contradictions.
- **Adversarial probes** (own harness, `/tmp/probe.c`): Δa/a = 10⁻⁴ (below the author's grid) and σ_e = 0.3 (stirred) — gate deletable 1.00000 everywhere; the sound all-longitudes floor screen deletes 0.9984–1.000, so the author's 0.99897 proxy is fair.
- **Predictions**: pre-registered; three held, three failed informatively and each failure is disclosed — P1's failure is the finding itself.

Flagged in the check: the routing-core number assumes mass-aware candidate generation (post-filter form would be 0.4–0.8 cores — still under budget but 10–25× the stated figure), a ≤2× v_rep speed slop, and the unpriced phase-tier lane. None bounds the empty-tier finding; the doll-unit/D*/L-channel caveats are the author's own.
