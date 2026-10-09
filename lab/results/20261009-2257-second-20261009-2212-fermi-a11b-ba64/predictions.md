# Predictions — 20261009-2257-second (before the decisive runs)

This is a second-author re-measure pass on run 20261009-2212-fermi-a11b. The
checker reproduced the physics but not the record. My decisive runs are the
dossier's stated commands plus the slope points it lacked, all on the shipped
tree (`cargo build --release -p xtask` from a clean checkout, 2026-10-09
22:5x). Predictions are anchored on the checker's reported families, so they
test regeneration and stability, not novelty.

## The commands (all in `evidence/`, one JSON each)

```
xtask universe --kick-bench --seconds 5                       # x3
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 48
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 148
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 248
xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 448   # clamps to 400
xtask universe --bench --rtf 1 --seconds 30 --unpaced --members 48      # transient regime
python3 budget.py                                               # reads evidence/*.json only
```

## Predictions (held-out cases, not tuned on)

1. **kick-bench**: median 40–50 µs across the 3 repeats, p99 60–95 µs,
   23 samples, `exact_hit_rate` 0.0. If any repeat's median leaves that band,
   the "≈44 µs" family claim is regime-dependent and I say so.
2. **Live-store slope** (bytes_per_body vs bodies, 4 points 71→410):
   monotone increasing, 5.1→6.7 KB, slightly convex; two-endpoint marginal
   slope 6.5–7.7 KB/body; a least-squares slope over the 4 points within 15%
   of the two-endpoint one. If the 4 points are not monotone, the "marginal
   ~7 KB" claim needs an error bar bigger than its spread and I report that.
3. **Event rate, consistent full-total aggregation** (kicks+opens+boundaries
   +encounters+decisions+lost+leavers+slices, all divided by game-seconds and
   bodies) at every N: 5–7×10⁻² events/body/game-s at 71 bodies, and
   4.5–5.5×10⁻² at 410 — i.e. mildly declining in N, NOT the 3.9×10⁻² the
   original dossier quoted (that was a kicks+slices+leavers subtotal). If the
   full-total at 410 is below 4.2×10⁻², the original's drop was real and the
   checker's "mostly an artifact" is wrong — that would be a finding.
4. **Transient regime** (rtf 1, 30 game-s, 48 members): per-body rate ≥10×
   the rtf-100 steady state (checker: ~27×). If it is within 3×, the
   "steady-state regime" caveat loses force and the capacity number is
   regime-robust — also a finding, the other way.
5. **Regeneration**: every number my dossier quotes is computed by
   `budget.py` from `evidence/*.json` by path (no hardcoded measurements);
   grep for the two endpoint stats in the JSONs matches. This is the gold
   criterion itself; it cannot partially hold.
6. **Derivations that should not move** (arithmetic, anchored on repo
   numbers): 190-core re-derivation ≈ 175; belt cadence ≈ 0.03 cores;
   10⁹ programs ≈ 16 MB; horizon ≈ 1.14 orbits per 100 h at rtf 100.

## What would break the original claim

- Slope non-monotone or > 2× off the 7 KB family → the 428–446× lever quote
  is unsafe.
- Full-total 410-body rate ≈ 3.9×10⁻² after all → the aggregation objection
  dissolves (fine for the claim, bad for the checker).
- Transient within 3× of steady → drop the regime caveat, not the claim.
