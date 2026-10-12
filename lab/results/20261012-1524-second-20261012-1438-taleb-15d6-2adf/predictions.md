# Predictions — second author on 20261012-1438-taleb-15d6

Written before any run of mine. The checker's named experiment: aim the instrument at the
BUILT certificate (`phase.rs` on `wt/cx-b-coorbital-cert`, adce00d6) — soundness AND k-cost.
The checker reported sound-everywhere (0 misses) with window k p50 ≈ 3411 at the gold-e 10⁶
headline. My job: regenerate the record from shipped code, reproduce that, and pin the
diagnosis with the decomposition the checker left terse.

## Reproduction (not held out — must match or the record is broken)

- R1. Author's controls: `redteam control` gives control-jam-loose-e 314 contacts, distance-rank
  313 ≤ 4, one at 5; `redteam pileup` gives jam-tight-s0.375: 757 contacts, 14.4% rank > 4.
- R2. Built cert, six scenes (`checkadv built`): 0 misses each.
- R3. Built cert at scale (`checkadv builtsnap`): 1e6-tight window k p50 ≈ 48; 1e6-gold-e
  k p50 ≈ 3400; window_miss 0.

## Held out (mine — the checker did not report these)

- H1 (reach decomposition). The cert's reach = angular + 2·centre + shear·H/2 (+eps), with
  centre = max-body(e + 2·asin(e/(1+sqrt(1−e²)))) ≈ 2·e_max. At 1e6 gold-e (Rayleigh(1e-3),
  cap 1e-2): e_max ≈ 5.1σ ≈ 5.1e-3 ⇒ EoC term 4·e_max ≈ 0.020 dominates reach (≥ 80% of it);
  angular ≈ ρ = 1e-4; shear term 0 at t0=t1. Predicted reach ∈ [0.018, 0.024] and
  k ≈ reach·n/TAU ∈ [2800, 3900]. At 1e6 tight (Rayleigh(1e-5), cap 1e-4): e_max ≈ 5.1e-5 ⇒
  EoC ≈ 2.0e-4 vs angular ≈ 1e-4 ⇒ EoC ≈ 2/3 of reach, k ≈ 45–55. So BOTH headline cases are
  equation-of-centre-dominated, not density- or ρ-dominated.
- H2 (max-e pathology). The window cost is set by the fleet's WORST eccentricity, not the
  typical one (centre is a max over bodies). Surgical test at 1e6 gold-e: replace the single
  worst-e body's e with the fleet median e (contacts unchanged to first order). Predicted:
  k p50 drops by ≈ e_max/e_median ≈ 5× (to ~600–800), while t=0 contact count changes < 5%.
  One hot body taxes the entire fleet — a max-statistic, exactly the tail quantity the μ-mean
  missed in the original run.
- H3 (the model, not just the decomposition). k_pred = reach·n/TAU (one line, computable
  before any visiting, from quantities the cert already computes) predicts measured k p50
  within ±15% on every scene I run. If true, the integrator's guard is free: refuse the phase
  tier when k_pred exceeds a budget, before paying a single visit.
- H4 (builder's gate never saw this). The wt branch's own scale test uses a sparse fleet:
  its max_k is ≤ 2 (predict 1–2), i.e. the branch's gates never measured a tight formation —
  the cost blowup at the headline was invisible to the builder's own gates.
- H5 (the k=4 premise is stale in text but dead in code). phase.rs verbatim contains the
  header "k is the actual occupancy of a conservative phase window, NEVER an assumed rank of
  four", and `lab/lenses/b-coorbital-cert.md` + board.md still carry "every encounter lies
  within partner rank 4" and "O(n·k)" with k≈4 implied. Both read from the tree/branch, not
  measured.

## Kill criteria for the second-author claim

- Any miss > 0 on a built-cert scene ⇒ "sound but costly" dies, the story reverts to soundness.
- Measured k at gold-e 1e6 ≤ ~100 ⇒ the cost story dies (the cert is as cheap as promised).
- H3 failing by > 2× ⇒ my "free guard" recommendation is not supported; report the gap.

## Time-boxing

Each command ≤ 60 s where possible; 1e6 snaps ≤ 90 s, < 1 GB. The six-scene brute (nc 200)
should stay ≤ 60 s total; if a scene exceeds 120 s I drop to the 3 decisive ones and say so.
