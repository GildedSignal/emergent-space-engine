Working...
`check.md` is written and the page corrected. Summary of the check:

**Grade: lead** — the work is real, reproduced, and honestly reported, but its headline is already shipped.

**What I did:**
- **Reproduced** `work/binet_refit.py` in a clean scratch tree: `metrics.json` byte-identical, 98 s. All dossier numbers verified (agm advance worst 8.25e-16, m-independent to 1 ulp; period pass 0.457; frozen controls 0.9570/0.9961/1.0000; crossings 4 vs 78).
- **Predictions**: written before the run (mtimes confirm). P3's period half **failed** (median 1.1e-3 vs <1e-5, worst 8.0e-2 vs ≤3e-2) — honestly reported as the finding; P2's sampler magnitude also missed (0.9961 vs predicted 0.70–0.90).
- **Adversarial (4, two outside the author's domain)**: independent RK4 at margins 0.2/0.02 confirms the agm frequency to 6e-12 but the period fails 26–46% there; p=10000 cubic reconstruction exact; e=1e-6 confirms the frozen first-order family the sampler never draws; and — the disclosure gap — the author's own frozen port returns **NOCYCLE at (8.5, 0.9)** (hyperbolic band at event 0, rattles forever) while fe85 measured 1.0e-3 there, never mentioned in dossier or page.
- **Novelty (decisive)**: the "delete the centre, compile the frequency from (E, L)" mechanism is the shipped law — law.md §Motion 2, `space-darwin16-v1`, 30 September (H0208), now `space-darwin16-scaled-v6-plunge` in `crates/space` with `QUADRATURE.md`'s proven bound and `tests/near_circular.rs`/`tests/envelope.rs` coverage, Kerr-extended. The run's advance exactness is by construction (its own admission), and its "next experiment" (Darwin shape word) is already implemented — the period failure belongs to the run's own cosine strawman.
- **Page corrected in place**: priority given to the shipped law; invL bar boundaries fixed (1% bar fails at p≲30–35, not ≈300); "19.5×" scoped to the replaced law; the NOCYCLE contradiction added; the run's line marked lead. The genuinely new rows (refit/1/L² pricing, seam underdetermination, sampler control) are kept.

Genuinely new and kept: the literal refit priced and killed, the frozen r1 text's unstable-band seams shown underdetermined (extended by my probe), and the independent float control matching fe85 exactly on the sampler.
