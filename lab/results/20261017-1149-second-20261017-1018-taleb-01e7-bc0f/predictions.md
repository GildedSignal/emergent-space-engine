# Predictions — second-author run bc0f (written before any run of this session)

The checker named three falsified arms. I re-run each under the page's own protocol
(`allocator-ratchet` open direction 4: ≥ 3 seeds, ≥ 2 replicates, i.e. ≥ 6 draws with
same-seed repeats), on fresh processes, and predict outcomes before running them.

Prior record I am predicting from (not tuning on):
- batch single-call: checker 4/4 crashed (horizons 1792 on-grid, 1800/1808 off-grid;
  seeds 11×2, 15; panic values per seed stable, s11 → 32→48); the author's one draw
  survived. Incidence unknown at ≥ 6 draws.
- vmax-16 frames: pooled 1/16 draws crashed (1104→1184, regen s11); checker's fresh
  seeds 16–21: 0/6, survivors rb 0–2.
- n=480 (arg n=240, 960 bodies) vmax 2 frames: checker 0/3, rb 144–166 — above the
  n=240 crashing band (57–95) yet surviving.

## A. Single-call batch, on- vs off-grid horizon (vmax 2, n 120→240 bodies)

Arms: horizon 1792 (= 112×16, on-grid) and 1800 (off-grid); seeds {11, 15, 21} × 2
replicates each → 6 draws per horizon class, 12 total.

- **A1 (incidence):** each horizon class crashes ≥ 4/6. The crash happens at scene
  start (s0 ≈ 32, fin_hi ≈ 48), far below both horizons, so horizon class cannot
  matter. "One call per process" (5d87's second limb) is dead in the churn class.
- **A2 (values vs race):** panic values per seed are stable across replicates
  (s11 → 32→48 expected, matching frames/chunks/batch everywhere); crash vs survive
  is itself a wall-clock race — at least one same-seed replicate pair is expected to
  split (one crashes, one survives) somewhere in the 12 draws.
- **A3 (held-out seed):** seed 21 (never run before in any record) crashes ≥ 1/2.

Falsifier for the arm: if either horizon class survives ≥ 4/6, the single-call channel
is weaker than the checker's 4/4 and the driver rule's second limb needs re-opening.

## B. vmax-16 incidence (frames, r600, seeds {22,23,24} × 2 replicates = 6 fresh draws)

- **B1:** 0–1 crashes in 6 draws — "rare, not never" holds. ≥ 2/6 crashes falsifies
  the dispersion story (vmax 16 would then be a real crash class, not a quiet one).
- **B2:** survivors sit at rb ≤ 4 (gas dispersed and quiet).

## C. n=480 bodies at vmax 2 (frames, r600, arg n=240, seeds {11,12,13} × 2 = 6 draws)

- **C1:** 0–2 crashes in 6 draws while survivor rb stays ≈ 130–180 — rb remains an
  in-band correlate, not a separator, beyond n=240. ≥ 3/6 crashes at high rb would
  instead restore rb as separator and kill the load-band reading.
- **C2:** any crash is at scene start (chronon < 200), same channel as n=240.

## Core arms (re-run for the corrected table; expectations = the standing record)

frames vmax 2 (seeds 11–19): 2–5 crashes of 9, panics at chronons 32–96, survivor
rb ≈ 57–95 with E = 2^rb. chunk 128: 1–3 crashes of 3, same panic values as frames
per seed. min_region 32: 0/3, rb exactly 0. window 32: 0/3, rb ≈ 79–110. wave 0/5,
crossing 0/4, vmax 8 0–1/6, r300-v8 0/3, n240-v8 0/3. Deviations reported as found.
