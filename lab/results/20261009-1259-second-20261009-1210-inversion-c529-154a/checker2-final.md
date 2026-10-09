Working...
Check complete. `check2.md` written: **Grade: gold**.

**What I did:**

1. **Reproduced everything bit-identically** — `patch.diff` alone carries the full state (its `inversion2.rs` hunk, blob `99d6752`, is byte-identical to `patch2.diff`; regen.sh's second apply is a redundant duplicate that kills the script — the one repro defect). First author's control/heldout, both decisive runs, and both Python audits all match after stripping wall-clock. Every dossier table cell cross-checked against the JSONL, including the 31,305-event oracle claim (d_rank_over4 = 0 everywhere).

2. **Verified pre-registration** — `predictions.md` (13:10:22) predates both decisive runs (13:10:49, 13:11:40); the [H] held-out legs held, soft misses were stated, no kill criterion fired.

3. **Grounded the retraction textually** — pulled the gold's dossier from its branch: it verbatim specifies "rebuild on overtakes", confirming the first author attacked an unspecified frozen-rank watch.

4. **Ran three attack families** (`inversion2 c`, left in the tree): seed re-runs of the single-seed legs (G1b/G1c/E3 — all replicate); ρ-isolation of E1 (2ae/ρ = 20→67→200 makes misses *worse*, 35.7%→50%→66.7%, killing 2ae/ρ as the scalar behind G1c's low miss); σ_e dose-response (rank* 5/6/8, monotone).

5. **One correction for the freeze**: the claimed soundness bound `2·e_scale ≲ k·2π/n` is a rate organizer, not sufficiency — my A6 scene sits 7.7× inside the bound yet still misses 4.5% at rank\*=5 (local λ clumping / Poisson tails), and the author's own E3 already showed the tension. The package's item (iv) — gate on measured rank\*, never the oracle — is the right gate; the bound must be restated as the ~8× rate scaling it is.

The author's `work/` directory is untouched; only `check2.md` was added.
