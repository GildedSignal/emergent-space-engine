Working...
**Grade: gold** — written to `check2.md` (blind to the first check; I never opened `check.md`).

**What I did**

- **Reproduced**: re-applied `work/patch.diff` to the reset tree, rebuilt, and confirmed the runner's regen table: serve_ms p50 1.09→0.18 (10⁴), 10.55→0.16 (10⁵), 33.18→0.14 (3×10⁵); drift ≤ 5.6e-15; audits zero; every END digest **bit-identical to e6c9's published branch logs** (5dc903e6/bd6f9840/82aa152c/c3943af5), and the "142–143 ms at 10⁶, required not optional" quotes verified in e6c9's two checks. Diffed the patch against e6c9's: 118 lines, all gated behind `ES_SKY_SUMS`; the rebuild/ctl path is untouched.
- **Mechanism**: steady `sums_ops` 0–2/frame at 10⁴ and 16–54/frame at 10⁶ (= 2×due+churn, flat in K) — a true deletion, not the relabeling the predictions' kill criterion guarded against.
- **Five adversarial arms of my own** (logs at `/tmp/959a-check2/`), one decade/range beyond the author's: **10⁶** — serve 0.12–0.13 ms/frame vs the 142/143 ms rebuild (~1100×; the extrapolation was conservative), cells_wrong 27/786 is e6c9's known probe-side id-aliasing, present in both arms; **500 frames** (author flew 300 of an announced 500) — serve flat, the standing wrong-cell class persists (5.29/frame at 300–500 vs rebuild's published 2.62, same membership-driven class); **fine floor at 10⁵** — 1.23 ms at 6,284 cells, cost follows cells not K; **the missing fine-floor rebuild control** — 1.71 vs sums 1.20 (parity-class, corroborating the page's 1.74), wire parity 0.002%; serve=0 digest identity.
- **Novelty**: exactly e6c9's checkers' named gold step (a), never before built; the author's wiki page flips the open direction to measured — every line traces to evidence, no correction needed.

**Deductions noted, not grade-fatal**: the unflagged 500→300 grid change; "the record's last objection at scale is gone" overreaches (gold steps (b) id-base widening and (c) ≥10⁴-frame pinning remain open on the record's file, carried honestly by the page); the cancellation corner and the non-Σlum sums in the drift audit stay unflown.
