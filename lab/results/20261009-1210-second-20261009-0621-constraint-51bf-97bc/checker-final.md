Working...
**Grade: gold** — written to `check.md`. The tree is restored (patch reverse-applied; only `lab/results/` untracked, as I found it).

What I did, in evidence:

**Reproduce** (clean tree, `work/patch.diff` applied myself):
- Stock: digest `6ce636fa…`, cut 406050894 — exact.
- Mode 0: view digest `cb69811f…` bit-for-bit; sources_tube 151.5 ms of 285.9 partial / 846.6 bodies — the author's anatomy (159.4/300.8/890.1) within load noise.
- Mode 1: digest identical; sources_tube 13.3 ms (**11.4×**), reuse 91.7%, first touches 1199; gather 0.674→0.636 vs engine 0.203→0.226 — matches the author to the third decimal; my mode-1 view digest `cd8bee72…` matches their stored run exactly.
- Mode 2: view digest = mode 0's; Δp 2.980e-8 root units, Δv 1.209e-16, spread 153,624,076 ticks — all exact. Kick-bench (`c8ab26da…`, 35.2/91.7 µs, memo 0.0/926, quantized 94.4924%) and B16 (PASS, 6.93e-8) exact. Interleaved uninstrumented p50 ×1.09–1.15 (author ×1.16).

**Holdout**: predictions 12:28:52 precede every lever run (12:29+); all four held, including the predicted direction of failure.

**Attack**: seed 3 (held out by me) — digest equal, same cut; rtf 10000 — digest equal, no inversion; paced mode-1 — digest equal; engine's five `secondaries` sites in `step.rs` untouched (structural view-only proof); full test suite on the patched tree: 29 passed, 0 failed. I also ran the patch's *undisclosed* `ES_RAW_CROSSING` path: slower (1990 ms) and view-changing — inert by default, and it supports rather than undermines the residual claim.

**Gold rationale**: premise killed with controls — the gather-vs-engine ranking survives its own cheapest named fix (~2.5× short of the bar), residual measured outside `partial`, redirecting to the cell-held-field representation; plus an adoptable digest-clean ×1.16 lever in the same step. Author's misses (undisclosed patch path, uninstrumented residual decomposition, one-doll scene concentration) are logged in the check.
