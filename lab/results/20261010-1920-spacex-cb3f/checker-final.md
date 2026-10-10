Working...
Check written: **`Grade: silver`** at `lab/results/20261010-1920-spacex-cb3f/check.md`. Tree restored to clean; nothing else in the run folder touched.

**What I did:**
- Applied `work/patch.diff` to a clean tree, rebuilt `spacex_probe`/`cost_split` myself (50 s incremental) — every digest in the dossier reproduced bit for bit (`d4413b80…`, `74a3a79f…`, `b1dcf925…`), all timings within shared-box noise: memo 1.03×, scan 30–32% of settle, 56.6→118.5 µs/item slope ≈ 34 ns/body, threads 4 slower, root_state 6.95 µs.
- Four adversarial cases: seed 42 (memo off/on identical), threads 1 vs 8 (identical — schedule independence beyond the author's test), and a 1e11-tick pruning stress where digests stayed identical but the memo turned into an 8% *pessimization* — evidence against adoption stronger than the dossier's own.
- Verified the scan mechanism in source: the O(N) term is the `binding_at` clone per foreign-doll body; the flat ~50 µs intercept is the ~12 same-doll exact pair checks (player in `home_doll`, cohort in the star doll).

**Why silver, not gold:** fully reproduced and honest, but the held-out predictions did not hold (P2, P3, P4-share, P5 all failed; only P1/P6 held), and no board premise was overturned, no component deleted, no 10× delivered — it's a ranked cost ledger plus a killed candidate. The named gold experiment: the provably-safe same-doll rejection pre-filter, judged on zero misses against the exact scan **with a dense same-doll cohort** — the run's cohort never grew the exact tier, which is also the author's main miss: the 10⁶ extrapolation (33 ms/item) covers only foreign-doll bodies; 10⁶ same-doll would be ~4 s/item.
