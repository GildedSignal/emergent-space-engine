Grade: silver

**Abstract.** Claim: at 10⁹ bodies, dynamics-side distinctions (H_live) write ≤ ~1 MB per 300-h game, so the term that breaks 10⁹-in-8 GB is the store's uniform tube precision (16 GB raw, 2.35 TB as measured), not event history — memory work goes to quantum tiering, and the scar/event-ledger track dies. Reproduced: `ledger.py` bit-identical (0.61 s), plane anchor `bytes/body 2349` exact (N = 28). First measurement of the handoff's unmeasured risk; belt-mass constraint 6×10¹⁶ kg/body; far-certificate churn ≈ 2.7/s at 10⁹. Not gold: P1/P2 failed by 13–18 orders (honestly disclosed), and the model carries an uncalibrated 32× gap to r8 v2's measured belt. Cost to adopt: none (a kill plus two gate numbers).

## Reproduction

- `python3 lab/results/20261007-0842-fermi-fc22/ledger.py`, copied to /tmp with only the output path redirected (the checker must not touch the author's folder): output **bit-identical** to `ledger-out.json`, 0.61 s.
- `cargo run --release -p emergent-universe --example plane -- 100` → `bytes/body 2349`, 28 bodies — exact match with the dossier's anchor. The 16-B tube word matches law.md §"Tube".
- Timestamps: `predictions.md` 08:50:32 → `ledger.py` 08:53:23 → `ledger-out.json` 08:54:27 → `dossier.md` 08:55:23. Predictions were held out before the decisive run. `work/patch.diff` is empty; the tree is clean outside `lab/results/`.
- Spot-checked the physics by hand: b* = 19 km ≪ H for P1, diffusive term dominates (D/q² = 2.7×10⁻¹² ✓); ln Λ = 22 ✓; collision count 0.31 ✓; fleet 1.4×10³ events ✓; P5 throughput 1.67×10⁴ kicks/s at 0.39 AU ✓; churn 2.7e-12 × 10⁹ = 2.7 writes/s ✓. Chandrasekhar cross-check: t_relax·(q/v)² ≈ 1.9×10¹¹ s vs the script's 3.7×10¹¹ s — same order.

## Predictions

P1 (≤ 10⁻³⁰/body/s) and P2 (threshold > 10³⁰ kg) failed by 13–18 orders; P3 (1–100 collisions) came in below range at 0.31; P4, P5, P6, P7 held (P7 evaluated at the tube floor its own text specifies, 4.0 GB ≤ 6 GB — fair, not cherry-picked). The failures are disclosed as the run's headline lesson. Honest, but by the lab's own bar ("the held-out predictions held") this alone blocks gold.

## Attack (five adversarial cases)

1. **Threshold consistency:** `total_rate(6.09e16 kg)` = 8.5×10⁻⁹ /body/s against the 10⁻⁸ target (15% off, from ln Λ shrinking with b90) — the m² interpolation holds; at 4.5×10¹⁷ kg the rate gives 22 bits/body/game.
2. **Fine quantum everywhere at 10⁹** (no tiering, q = 10⁻⁹ v_kep): 18.2 GB/game — breaks 8 GB by ~2.3×, not catastrophically. Tiering is cheap, not heroic; worth stating.
3. **Combined worst case** (30× tighter belt at q = 10⁻⁷): 0.1 GB/game — does **not** break. The ledger is flatter than the dossier's "what would make it wrong" implies; only the quantum, not geometry, can break it.
4. **b_min = 1 m is below the physical radius** of the modeled 10¹⁵-kg rock (≈ 4.6 km): the true rate is 1.67×10⁻¹², i.e. the script *overestimates* the ledger 1.6× — conservative in the safe direction.
5. **32× calibration correction applied to the headline:** P1 ledger → 0.58 MB/game; the "≤ 1 MB per game" claim survives the declared calibration gap at the base geometry.

## Novelty

The handoff's risks list (6 Oct) says H_live is "not measured yet"; no H entry measures it. What is **not** new: storing belts as programs is adopted (gold components-98bc, law.md — the Tube is already "the logical view", not stored per body), so "the store's uniform tube precision breaks" restates the premise of shipmem from the measured side. The new, adoptable parts are the rates (crossing 2.7×10⁻¹², collisions 0.31, flybys 1.4×10³), the belt-mass constraint, and the ≈ 3/s churn number for the encounters design.

## Goal fit

Board item "fitting 10⁹ in 8 GB… decided by distinctions created per game-second": directly measured. Deletes a design track; gives B18's "event records" term its expected size. Respects PRINCIPLES: "The memory floor is information-theoretic" — the floor it finds is births + player inputs; "Delete before optimizing" — the ledger track deletes itself.

## The one experiment to gold

Count element-word writes and recertifications per game-second **on a live belt** (the plane or `crates/shipmem` at 10⁶ bodies, far quantum in force), and reconcile against the flux model — closing the 32× gap with an engine-side measurement instead of r8 v2 geometry transfer. That converts the ledger from a calibrated model to a measured gate input.

## What the author missed

- law.md's scars are already *current-state* differences, not history logs; the killed "per-body scar log" is partly a strawman. What the rates actually bound is B18's "event records" term.
- Labeling slips: "30 bits/body (10⁻⁸ crossings/body/s)" is 0.46 bits/body at 50 bits/event (the true 30-bit threshold is ≈ 4.5×10¹⁷ kg — conclusion unchanged); player inputs at 10 bits/s are 1.35 MB/game, not ~4 MB; "two orders below the far quantum" is three (0.019 vs 9.5×10⁻⁶ m/s).
- The sheet-saturation switch at b90 > H makes the rate non-monotonic in mass (2.5×10⁵ /body/s at 10²⁴ kg vs 4.8×10⁻³ at 10²⁷ kg) — defensible regime switch, undocumented.
- The two Monte Carlos validate the script's arithmetic (x⁻² tail, D/q² first passage), not the physics against an external truth; only r8 v2 anchors it, at 32× under.
