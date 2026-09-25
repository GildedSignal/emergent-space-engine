# v5 quick climb, chronon mode only (25 September 2026)

Command: `./target/release/xtask ladder5 artifacts/evidence/scale-ladder-v5-20260925/chronon-quick-1 --modes=chronon` on an Apple M1 (8 GB), manifest `scenarios/scale-ladder-v5.json` (sha256 `2785cdd3…`), baseline `3b0f697` plus uncommitted work.

Measured under load: three specialist agents were compiling and testing at the same time (load average 6.6, see context.txt). Wall times and unit times are therefore pessimistic. C2 at 16,384 ships passed in 7.0 s in an earlier unloaded scratch run and fails the 8 s cap here (8.9 s).

Runner defect found in this run: a run that exceeded the wall cap between two cap checks while reaching the horizon was marked complete in the earlier scratch run's logic only when no check fell after the cap; C2 16,384 here shows "wall cap … at tick 1024 of 1024". The runner now applies the cap after the loop as well (the frozen rule is "complete within caps"). The rows here are unchanged.
