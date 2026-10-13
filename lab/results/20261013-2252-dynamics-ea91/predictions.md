# Predictions (written before the decisive runs)

Question: is the per-body surprise-rate distribution on the shipped plane heavy-tailed and
rank-stable (nladder rule 2: "the live set is a rank"), or light-tailed/churning (the fixed
fraction stands, promotion needs hysteresis)? Open direction 1 of lab/wiki/nladder.md,
never measured. Cases below are NOT tuned on: the 5 s sanity run only checked that the
instrument runs and that the digest is env-independent.

Kill criterion for rule 2 (frozen here): if the top decile of live bodies holds < 30% of
resolved items AND Gini < 0.4 on the author's scene (seed 1, m48, rtf 100), the rank rule
dies and the fixed fraction stands.

- P1 (tail, author scene seed 1 m48 rtf100 30 s): heavy in rank — top decile of live
  bodies holds ≥ 50% of resolved items; Gini ≥ 0.6; Zipf rank-size log-log slope |β| ≤ 1.
- P2 (attribution): the player is the single busiest body (burn waterfall); among the rest,
  the spread is regime-set (kind/native-vs-promoted), roughly geometric across orbit radii,
  not identity noise.
- P3 (rank stability): Spearman ρ between first-half and second-half per-body item counts
  ≥ 0.8 over bodies alive in both halves (if regime-set, ranks barely churn; ρ < 0.5 would
  mean promotion-by-rank thrashes and needs rule-3 hysteresis).
- P4 (intermittency): the aggregate stream is bursty — per-frame event count
  variance/mean > 2 (over-dispersion vs Poisson), and encounter-attributed per-body counts
  churn ranks faster than the deterministic kick-lattice counts.
- P5 (held-out): seed 3 m400 rtf100 55 s, seed 7 m48 rtf100 55 s, and seed 3 m48 rtf1 30 s
  keep P1's top-decile share within ±10 points; the player stays the busiest body.

What would make me wrong: promotion mix dominating the census (bodies born mid-run with
short exposure inflate apparent equality) — handled by also reporting the native-28-only
and full-window-alive subsets separately.
