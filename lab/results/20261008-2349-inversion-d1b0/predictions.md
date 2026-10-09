# Predictions — 20261008-2349-inversion-d1b0 (written before the grid run)

Question: does the train certificate adopted from gold taleb-09b5 (watch k≈4 phase neighbours in a
concentrated clump) survive eccentricity-vector dispersion and clump size, which that gold never
swept (its own "what would make it wrong": one seed family, e~0.001, ϖ within ±0.1, n_c ≤ 800)?

Scenes: one clump, a ∈ 1±1e-5, λ uniform (or bunched σ_λ=0.05 for D), e ~ Rayleigh(σ_e), ϖ uniform
in ±s_p. ρ=1e-4, H=8 orbits of a=1, seed 27. Truth = conservative advancement (truth.rs) on every
pair; method = the two-tier sections pipeline (safety 2.0); at every true closest approach I record
the partner's circular longitude rank (λ-rank) and distance rank (d-rank), 1-based.

Mechanism I commit to in advance: at Δa→0 the synodic phase is frozen, so a pair meets only if born
with mean-longitude offset ≈ the arrival-time offset the crossing arcs demand, which is set by
equation-of-center differences ~ O(e). So the partner at contact sits at λ-distance ~ c·σ_e
(c ~ 2–4), giving **max λ-rank ~ n_c·c·σ_e/2π** — k is not a constant: it grows linearly with clump
size at fixed σ_e, and with σ_e at fixed n_c. ϖ coherence mostly separates d-rank from λ-rank
(coherent: λ-close ⇒ r-close; incoherent: radial breathing ~ e decorrelates them).

- **P1 (control, gold's domain).** A-fleet (σ_e=0.001, s_p=0.1, n=600): max λ-rank ≤ 4 (gold
  reproduced; n_c·4σ_e/2π ≈ 0.4, so 4 is deep tail). Encounter count ≥ 10.
- **P2 (main).** Ranks inflate with σ_e at both ϖ coherences: B1/C1 (σ_e=0.01, n=600) reach max
  λ-rank ≈ 2–8 with some events beyond 4; B2/C2 (σ_e=0.03) reach max λ-rank ≈ 10–40 with ≥ 20% of
  events beyond k=4. A k=4 train drops real encounters in B2/C2.
- **P3 (size axis).** B1x (σ_e=0.01, n=1200) roughly doubles the max λ-rank of B1 (linear in n_c).
  Extrapolation (not measured): at the gold's own 10⁶-ship fleet with σ_e=0.001, k ≳ 600 — the
  O(n_c·k) certificate is O(n_c²·σ_e) when it must not miss.
- **P4 (d-rank vs λ-rank).** In B scenes (ϖ random) d-rank ≫ λ-rank at the same σ_e (distance order
  and phase order decouple); in C scenes (ϖ coherent) they stay within ~2×.
- **P5 (trigger blindness).** The gold's dimensionless trigger (max pairwise Binet distance over
  median eps_u) cannot separate B1 from C1 (same σ_e): both ≈ 100–400, differing by < 2×, while
  their rank behaviour differs qualitatively — the trigger lacks a ϖ-coherence/e-vector axis.
- **P6 (method soundness, two-sided).** The two-tier method's pair-miss rate vs truth is ≈ 0 in B/C
  (transversal crossings have sound windows); any misses concentrate in A/D (near-tangential
  relative motion), reproducing the gold's 4/233 soundness hole at a few percent.

Failure of P2/P3 with ranks staying ≤ 4 everywhere would mean the train certificate is stronger
than the gold's evidence (also a result: confirmation, and the scaling law is wrong).
