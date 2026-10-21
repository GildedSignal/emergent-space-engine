Working...
Check written; tree restored (only `lab/results/` untracked, as found). Verdict:

**Grade: silver.**

**Reproduced** — patch applied to a clean tree at base `00696555`; all four dossier arms rerun with **identical digests** (`0f13c8bc…`, `265ff6ac…`), bit-identical item counts and tail composition, timings within noise (only single-item draws differ: comb ship max 594-617 µs vs the author's 918).

**Predictions** — P1/P2/P4 held on the author's arms and my new seed×rung arms; P3 held with its disclosed ramp refinement; P5 failed as a window fact, honestly reported, and its quantity is confirmed at rtf 1000 (max served 237-251 ms). File-time evidence for pre-registration was destroyed by `regen.sh` overwriting `out/` — flagged as a harness note; P5's failure signature itself argues the predictions were real.

**Adversarial** — comb 1e5 seed 2: holds (0.92-0.93, 77.1% boundaries). Trickle 3e5 seed 2: holds fully, identical item counts (the locals' stream confirmed). The outside-domain case, **comb at 3e5** (the author flew the comb only at 1e5): mean stays N-flat and p99.9/mean 10.5 holds, but worst-frame correction reads **1.22-1.28 on two digest-identical draws** (not 0.90-0.96) and >p99.9 boundaries drop to **67%** — structural, not load. The "pure arrival pile at mean service" letter and the boundary share are 1e5-scoped.

**Novelty** — real: prior work (3aec/d709/0a46/8365/kick-jet) holds per-kind means and era walls only; the distribution-by-band, correction metric and margin-rule decay pricing are new. Margin rule verified on shipped code (`max(ns, m−m/64)`, universe.rs:1029).

**Page** — corrected in place: comb claims scoped to 1e5 with my 3e5 numbers folded in; budgets hold.

**Gold path** — fly the per-class-quantile margin rule (measured multipliers as predicted overruns) or stage-split the >p99.9 boundary population; either converts the priced law into a moved row. Missed by the author: the comb at the rung they already had; correction's kind-mix vs service-tail conflation (cross-kind mean denominator); the fleet population's 12× seed-dependence at the comb.
