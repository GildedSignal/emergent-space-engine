# Predictions — 20261019-1906-scout-f2f1 (written BEFORE the decisive runs)

Question: the closed form of the measured leak(E, P, κ) curve (encounters od 3, "the
scout's own named gap"). Mechanism candidate: the book (the tier's scheduled due)
SURVIVES kicks geometrically — each touch kills the book's validity with probability
q(P, κ) — and an event is caught iff its firing touch finds the book alive pointing at
it. Then:

  miss_frac(E) = 1 − [1 − (1−q)^E] / (E·q)      (geometric book-survival)

with q→1 giving the measured 1−1/E at P=1, and q<1 the P=4 dip at small E.
Alternative (the page's "Wiener-mixture"): the due index is a drifted random walk and
the book survives a diffusive boundary first-passage, S(j) ≈ erf(b/(σ√j)) — the census
discriminates the two by shape.

P1 (shape): at (P=4, quantum κ=1e-7, E=1024 arms, seed 20261018) the per-offset
survival S(j) = 1 − misses(j)/events(j) decays LOG-LINEARLY in j (geometric, χ² of the
log-residuals against a line within 3× that of the erf fit), not as erf(b/σ√j).
P2 (law): the single-parameter fit q from j ≤ 8 predicts the measured miss_frac at
E ∈ {16, 64, 256} (1176's grid: 0.86/0.98/1.00 at P=4) within ±0.05 absolute.
P3 (P-dependence): q(P) rises with P; the P=1 arm reads q ≥ 0.8 (near the 1−1/E limit);
the ratio q(16)/q(4) ∈ [1.5, 4].
P4 (κ-dependence): at 2⁻²⁶ (512× weak) q falls by ≥ 4× vs the quantum (the quasi-static
book: δc0 = 0.13w), and the small-E miss dip (measured 0.04–0.09 at E=2) is the same q
inserted in the law, not a separate regime.
P5 (channel split): misses with a FAR book (the pair was unarmed at the arm: flip-in
channel) are ≤ 25% of all misses at the quantum, P=4 — the dominant miss is the stale
book (due moved), not the never-armed pair.
P6 (control): E=1 → 0 misses; dv0 → 0 misses at every offset (j=0 only).
