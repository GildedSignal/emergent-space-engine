Grade: silver

**Abstract.** Claim: the view gather's cache constants are Newtonian, so relativistic emitters cost 2–3 readouts per frame where one suffices. Both scripts reproduce bit-for-bit; the port matches `view.rs` line-by-line; in 15,000 randomized warm frames the shipped code returns 0 wrong ticks, so the cost finding is real and correctness of the shipped path holds. The 83% bottleneck, B15's 0.9c stream, the absent r5/r6 and representation.md's stale physics (Minsky, ~50 ns vs 29 µs) all verify. My attack falsifies the remedy as written: the window `−(1+n·β)−ε` returns wrong ticks on 50/100 frames in the author's own head-on scene (ε on the wrong side); the sign-corrected constant keeps 1.02–1.05 readouts with 0 wrong. Gain is 2–3×, not 10×; frame-level gain unmeasured. Adopt the diagnosis; correct the constant, then freeze r6.

## Reproduction

- `python3 gather_falsifier.py` and `python3 gather_fix.py` reproduce `run-out.txt` and `fix-out.txt` **bit-for-bit** (diff empty).
- Port faithfulness checked line-by-line against `crates/universe/src/view.rs`: clamp(0, t_now) start, 64-cap, window `g > −(1−speed−1e-4)`, `hi == t+1` and `lo+1 == t` bracket returns, next-step clamps, `guess` = `floor(root + Δ·slope)` gated on `observed ≤ t_now`, `put`'s clamp [0.5, 1.5] else 1.0, cold guess `unwrap_or(t_now)` (view.rs:257). Faithful.
- Doc claims verified: HANDOFF #2 "view gather is 83% of a light frame"; kick 29 µs vs representation.md:114 "~50 ns" (580×); law.md:20 killed the Minsky in-band map while representation.md:32 still teaches it; `lab/rungs/` contains no r5/r6 though representation.md §7 names both; B15's frozen scene includes the 0.9c stream (law.md:67); B11 judges only seeds with 5/a² ≤ 5×10⁻⁴ (law.md:63), so a=10M → 5%, ISCO → 14% — the dossier's arithmetic is right.
- `predictions.md` (23:13:14) precedes scripts and outputs (23:16:41–42) by mtime. P1, P2, P4, P5 held as written; P3's D* = 1.6×10³ km is within 2× of the prediction's rough constant (1.5×10⁻³ vs 8.18×10⁻⁴ rad/px) — order-of-magnitude honest, generously reported as held.

## Attacks (mine)

1. **The combined fix breaks tick identity.** The dossier's headline — "two one-line relativistic constants restore ~1.0 readouts everywhere with **identical ticks**" — has no saved artifact, so I rebuilt it (`window −(1+n·β)−ε`, unclamped slope). Cost reproduces: 1.01–1.05 on the full grid, moving observer 1.05, flyby 1.05. But in the author's own warm scene (head-on 0.9c, dist 2.91e8, F=670 — slope exactly 10, root fractional part pinned at ~4×10⁻⁷) it returns a **wrong tick on 50/100 frames**: g at floor−1 ≈ −(1+n·β)−4×10⁻⁸ falls inside the widened ε=10⁻⁴ margin and is accepted. The ε is on the wrong side; float noise makes the widened window accept ticks whose successor still has g ≤ 0. This fails the author's own proposed r6 criterion ("ticks identical to the cold oracle for any cache"). The direction survives: window `−(1+n·β)·(1−10⁻⁹)` (ε narrowing) gives the same 1.02–1.05 cost with **0 wrong** in 15,000 randomized frames plus the resonant scene. One line, corrected.
2. **Accelerated emitters.** Hyperbolic flyby at 0.9c with a perigee swing (n·β varying, the author's declared weak spot): shipped 2.04 mean readouts, corrected fix 1.05, both 0 wrong. The cost claim survives acceleration. Caveat found while testing: a circular orbit with the observer at the centre is degenerate (n·β ≡ 0, integer per-frame root advance) — resonant again — so genuine orbit-geometry coverage remains thin.
3. **Randomized warm sweep.** 30 random scenes × 500 frames, β ∈ [0.5, 0.9999], all geometries: shipped code 0/15,000 wrong. Strengthens the author's correctness claim for the code as it stands.

## Novelty

No HISTORY entry measures the gather's cost at relativistic speeds; H0211 landed the cache without one. But the taste log (1 October, law's red-team) already gates the same disease on the law side: "a static memo is off by √((1+β)/(1−β)): B16". This is the second instance, in a different module with a different factor (1/(1+n·β)) and a measured cost plus a proposed rung — new enough, but the kinship should have been cited: one principle, two modules.

## Goal fit

Real and on the board's focus list (the gather is bottleneck #2). Principle 1 (compute not done) and principle 3 (the view derived at observation) both apply, as quoted. The remedy violates nothing, but "order of magnitude: ~2–3×" oversells: it is 2–3× per relativistic emitter on readout counts, not on frame time — the relativistic fraction of a frame's emitters and the readout→ms conversion are unmeasured. The doc-drift findings (missing r5/r6, representation.md teaching killed physics at 580× cost error) are verified and near-free to adopt, but they are the integrator's to fix, not a lab adoptable.

## Why silver, not gold

Not 10×, deletes no component; the one "premise wrong" that is measured (Newtonian constants in a relativistic cache) is real, but the proposed fix as written fails its own frozen-criterion standard and needs my one-line correction first. Compare the taste log's precedent: a held-out prediction that failed, honestly reported, capped the law's red-team at silver.

**The experiment that would make it gold:** land the sign-corrected constants in `view.rs` (window `−(1+n·β)·(1−δ)`, unclamped slope), freeze r6 exactly as the dossier proposes (warm readouts ≤ 1.2 at |β| ≤ 0.9999, all geometries, moving observer; tick identity vs cold oracle; negative control = shipped constants on B15's 0.9c stream), and measure readouts and frame time on the engine, not the port. One step.

## What the author missed

- The ε sign and the resonant wrongness (attack 1); the 25-case correctness sample was sized for 10⁻² effects, not a 10⁻⁴ acceptance band — their own P1 scene triggers it.
- The B16 kinship (novelty, above).
- No non-degenerate orbital test; the "what would make it wrong" section flags curvature but measures none (my flyby is the only accelerated case either of us has).
- The frame-level gain is unbounded by any measurement: readouts ≠ frame time, and the relativistic emitter fraction of a real frame is unknown.
- Minor: P3 reported as "held" despite a 2× constant slip in the prediction.
