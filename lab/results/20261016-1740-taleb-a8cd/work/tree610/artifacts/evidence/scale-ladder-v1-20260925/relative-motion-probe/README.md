# Relative-motion probe — 25 September 2026

Single release run on Apple M1 8 GB, baseline `3b0f697` plus the uncommitted law-lab orbit work (engine crate unchanged).
Command: the probe source was temporarily placed at `crates/engine/examples/zz_probe_relative_motion.rs`, run with
`cargo run --release --offline -q -p emergent-engine --example zz_probe_relative_motion`, then removed from the crate.

World: 1e9 ships in G affine lanes (stride 64, radius 1), lanes 1000 units apart, speed along the lane 1/4 + lane*delta.
Parallel lanes cannot touch, so every row must commit 0 events; all did. `axis` is the lane direction.
This is an easy control, not a ladder rung: see [the test ladder](../../../../docs/test-ladder.md).

Finding: with delta = 0 no pair is compared; with any delta > 0 (even 2^-30) every pair of groups is compared
(120 of 120 at G=16, 32,640 of 32,640 at G=256), independent of horizon (1 year to 1e10 years).
Cause (source inspection, `crates/engine/src/runtime.rs` sort-axis selection): the sweep axis is chosen by the spread of box
centres; relative drift over the horizon makes the along-lane spread dominate, so the sweep runs on the axis where all
lanes overlap. Wall times are single-run, warm process, and include setup of the scan.

`population-benchmark-rerun.json` is `cargo run --release --offline -q -p xtask -- bench <dir>` on the same tree.
