# Predictions — 20261013-1915-second-...-de99 (written before the decisive run)

The named gap (check2, silver verdict): the cost half was artifact-tainted. This run builds
the honest kernel it asked for: Carlson RF/RC/RD/RJ verbatim from the 1994 paper (arXiv
math/9409227, downloaded and read at source this run), normalized-deviation series, certified
stop rules (2.2)/(2.9)/(2.25)/(2.17) at r = 1e-15, std::hint::black_box on input and output,
delivering all three increments (φ, τ, t) as a drop-in, priced against shipped
`Orbit::compile` on the leaver tail.

Cases below are not tuned on; the kernel code is written from the paper and the τ/t algebra
from orbit.rs source, before any run.

1. **Kernel vs independent truth** (double-exponential quadrature, no shared code): K, E,
   Π, Q and the three closed-form increments agree to < 5e-15 relative for m ≤ 0.95, β ≤ 100.
2. **Cancellation at the e-tail** (predicted, quantified): Π(−β,m) = K + (n/3)·RJ with
   n = −β and β = 2(1−k)/(2k−1) ≈ 2×10⁶ at e = 0.99999 amplifies f64 roundoff by ≈ K/Π ≈
   10³; I predict the t/τ channels' kernel-vs-truth degrades to ~1e-12–1e-11 there (still
   below the walk's own ~1e-9 envelope), not the 1e-15 of moderate keys.
3. **Drop-in vs shipped, strong branch** (q_key > 2⁻¹⁸, k > 1/2, m < 1): advance, period,
   proper_period all agree to ≤ 2×10⁻⁹ relative — the walk's own quantum — on every strong
   key including e = 0.9999, 0.99999 and q_key = 0.2375.
4. **The m→1 edge** (1−m ≈ 3.5×10⁻⁹, arbitrary periapsis keys): check2 measured the
   shipped walk itself 6.7×10⁻⁷ off truth there. I predict kernel-vs-shipped rises to
   ~1e-7…1e-6 exactly there, while kernel-vs-truth stays < 1e-11 — i.e. the disagreement is
   the walk's, visible as a split between the two error columns.
5. **Weak rows** (q_key ≤ 2⁻¹⁸, Taylor branch): disagreement ≈ the branch's own O(q)
   truncation: advance ~3–5×10⁻⁶ at q ≈ 9.5×10⁻⁷ (matches the first run's 4.3×10⁻⁶);
   period/proper_period within ~10⁻⁶…10⁻⁵ for the same reason.
6. **Refusal**: p = 2², e = 0.5 → compile refuses NoBoundOrbit; the closed form's inputs hit
   A ≤ 0 (m ≥ 1) at the same boundary — domain edges coincide.
7. **Iterations** (the honest convergence law): deviation spread contracts by exactly 4 per
   duplication (paper §2 text); with r = 1e-15 the stop rule gives n = 5 for most calls,
   6 at the m→1 and β→10⁶ extremes; inner RC calls n ≤ 3. Series truncation error falls by
   4⁶ = 4096 per extra duplication (paper intro) — final X ≤ ~4×10⁻³.
8. **Honest walls** (black_box, median, this shared box): φ channel (one RF) ≤ 400 ns;
   τ channel (RF+RD+RJ) ≤ 900 ns; t channel (adds a second RJ) ≤ 1.3 µs; all three ≤ 2.5 µs.
   Compile at e = 0.999/0.9999/0.99999 is 191/263/325 µs (reproduced from both checkers),
   so the honest all-three gain on the leaver tail is ≥ 75× and the per-channel φ gain
   ≥ 450×. This is 10²–10³×, NOT the artifact's flat 5×10³×.
9. **Iteration-count law**: measured spread ratio per duplication = 4.0 ± noise on every
   key, confirming (against the first dossier's "quadratic") that the spread contracts
   linearly and the VALUE error is what squares (4⁶/step in the series regime).
10. **What would kill the drop-in claim**: any strong-branch key where kernel-vs-shipped
    exceeds 2×10⁻⁹ while kernel-vs-truth stays small (my algebra wrong), or the m→1 edge
    where kernel-vs-truth itself degrades past 1e-9 (cancellation worse than predicted).
