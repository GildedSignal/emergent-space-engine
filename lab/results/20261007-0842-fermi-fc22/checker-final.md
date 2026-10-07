Working...
Check written to `lab/results/20261007-0842-fermi-fc22/check.md`.

**Grade: silver.**

What I verified:
- **Reproduction:** `ledger.py` (copied to /tmp, output path redirected — the author's folder untouched) → bit-identical `ledger-out.json` in 0.61 s. The plane anchor `cargo run --release -p emergent-universe --example plane -- 100` → `bytes/body 2349` exactly. Timestamps put `predictions.md` (08:50) before the decisive run (08:54); `patch.diff` empty; tree clean outside `lab/results/`.
- **Physics spot-checks:** all headline numbers re-derived by hand (diffusive term dominates P1 at 2.7×10⁻¹²; ln Λ = 22; 0.31 collisions; 1.4×10³ flybys; churn 2.7 writes/s at 10⁹); Chandrasekhar relaxation cross-check lands same-order.
- **Five adversarial cases:** threshold self-consistent within 15%; fine quantum everywhere at 10⁹ gives 18 GB/game (only ~2× over — tiering is cheap, not heroic); the combined tight-belt + finer-quantum case does **not** break (0.1 GB/game) — the ledger is flatter than the dossier's own wrong-making row implies; b_min = 1 m is below the physical rock radius, so the script *overestimates* the ledger 1.6× (conservative); the 32× calibration correction still keeps the headline at 0.58 MB/game.

Why silver, not gold: P1/P2 failed by 13–18 orders (honestly disclosed, but the lab's gold bar says predictions held), and the model's only external anchor is r8 v2 at 32× under. Why not lead: H_live was explicitly "not measured yet" in the handoff's risks — this is the first measurement, it kills the per-body event-ledger track, and it hands B18 and the encounters design two concrete numbers (belt-mass threshold 6×10¹⁶ kg/body, ~3 recertifications/s at 10⁹). One experiment to gold: count element-word writes per game-second on a live belt and reconcile against the flux model, closing the 32× gap with engine-side truth. Noted also that the "scar ledger" it kills is partly a strawman — law.md's scars are already current-state differences, not history logs.
