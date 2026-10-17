# Predictions — 20261017-0739-taleb-9b46 (written before the decisive runs)

Tuned ONLY at N=864 (24-cell row, 8×6 archipelago, per=12, m=0.5, cannon=128, quiet=1):
the conflict regime appears there (E=4, 2 rollbacks by tick 100, px≈100, wasted≈1.2k) and the
chunked-`run_to` panic fires. Nothing at 14k/28k or seed 7 has been run.

Held-out cases and predictions, frozen 17 October 08:0x, before the matrix:

- **P1 (E grows with N — the page's law).** E(14k) ≥ 8 and E(28k) ≥ E(14k), in the page's
  2⁵–2⁸ band (their 14,080-body draw latched 64–256).
- **P2 (the latch couples the archipelago).** Quiet cells (vmax 1 quantum) couple when
  promise reach (0.5E+E−1)·(1/256)·1500 ≥ spacing 200 ⇒ E ≳ 22. So at 28k shipped ends with
  < 200 regions (≪ 2,296 cells); at 14k near-threshold (prediction: hundreds, not thousands).
  Quiet control (cannon=1, no wave): E stays 1, regions stay many, wall < 30 s — the coupling
  is the latch, not physics.
- **P3 (cap control).** ES_CAP=64 at 28k keeps ≥ 10× shipped's region count and finishes
  ≤ shipped's wall; shipped at 28k DNFs at 240 s or grinds ≥ 2× cap64's wall. Digests per
  size identical across shipped/cap64 wherever both finish (scheduling moves speed, never
  results).
- **P4 (the panic scales).** The chunked-run_to panic (`rollback … would revise its
  published tick`, alloc.rs:1456) reproduces at 14k with chunk 500.
- **P5 (walls).** At equal finished chronons, wall(shipped 28k) / wall(14k) > 2 if the
  one-region collapse deepens superlinearly in N (page: 82 → 10 chronons/s from 14k → 28k).

Failure of P2/P3 would refute the "latch couples quiet regions" channel in this scene and
point back at physics-only coupling (page's contradiction, the other way).
