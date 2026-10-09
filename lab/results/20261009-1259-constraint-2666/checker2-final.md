Working...
Blind second check complete. `check2.md` written; tree restored to clean.

**Grade: silver.**

**Reproduced on a clean tree + patch** (all five dossier commands):
- Frame shares: view_gather 68.0%/3.65 ms p50, engine 19.3%, json 8.9%, wire 3.8% — matches the 69.1/18.1/9.1/3.8 table.
- Gather attribution: crossing 2.72 of 2.83 ms (96%), 66.6 readouts/frame, 40.9 µs/readout; same ratios at 417 bodies (96.7%, lt_150m=0.999, overflow 29%, rtf low 0).
- Kick-bench: 46.6 µs median, 0.27% of wall — the flown-frame inversion is real.
- rtf 1000 extrapolation matches to ~0.001 (0.315/0.517/0.716/0.994).
- Predictions were pre-registered (13:03 < patch 13:17); the skip-form refutation was honest.

**Attacks that landed:**
1. The surprise probe anchors on first sight, not the previous frame — but my corrected probe gives 59.1/frame vs the author's 60.2, so the "skipping is dead" conclusion survives the instrument bug.
2. The extrap probe re-anchors every frame, so "96–99.9% replaceable" is a one-frame statistic. My 8-frame staleness variant: lt_150m falls to 0.822 at rtf 100 (18% break the 150 m floor) and 0.283 under rtf 1000 × 417 bodies — the 25–40× headline is a projection; the conservative k=8 gain is ~6–8×.
3. `cargo test -p emergent-universe` is **not** green on this checkout: 3/10 fail with and without the patch (pre-existing step.rs/lattice failures, unrelated to view.rs) — the dossier's claim is false as written.

Silver, not gold: everything measured reproduces, but the load-bearing staleness-vs-floor-vs-rtf cadence curve is unmeasured and my probe shows it binding at exactly the quoted floors. The gold experiment: wire the ViewCache advance scheduler with the 1+n·β refresh selector and measure the shipped gather's ≥10× cut under a stated floor.
