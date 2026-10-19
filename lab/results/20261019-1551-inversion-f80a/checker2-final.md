Working...
Check complete. `check2.md` written, the page corrected in place, tree restored clean.

**Grade: gold** (second blind check, confirming the first).

**What I did:**
- **Reproduced both arms from a clean tree** (c9195bfa + `work/patch.diff`, verified by diff to be e181's patch verbatim + the restored frame-loop `prune()` + disclosed probes): OFF end state exact (hist_total 241,552, gt1 30,065, hist_max 2,017); ON end state exact (866,168 bindings = 28.8/body, RSS 1,457 MB at 419k, held 0, counter identity exact). Probe-level agreement within the run-to-run elastic band (≤134 of ~10⁵–10⁶, ≈0.1%).
- **Three adversarial arms of my own**: K=10⁵ (10× the author's N — outside his range): first-wave saturation of 100,064 bodies, fence identity exact, RSS 511 MB at 59k on channel 2 alone; TTL=64: census exactly tracks TTL=16 (74,733 = 74,733 at 59k) — independence is fence-width-insensitive; plus a determinism rerun and a code audit confirming the claimed keep-window mechanism (`droppable_until + 2·light_distance + 2²⁶`, universe.rs:1252, visited only when ≤ now).
- **Predictions**: pre-registered (mtime 16:01:59 < all flight logs); decisive P3 held inside its bands; the kill criterion did not fire.
- **Page corrections** (bracketed, add-only): "30,064 of 30,028" is an impossible pair (real: 30,065 of 30,076, 99.96%); "IDENTICAL between arms" overstated (max Δ134, and one windows.txt cell is the ON log's value, run-elastic); runs line marked gold twice-checked.

**Noted for the integrator:** the core adoptable sentence is *not* the soft "~15% horizon" (two projections) but the measured one — the fence deletes channel 1 only; channel 2 alone still guard-kills the flight unbounded at every cadence, tree, N, and fence width now flown; the fence's encounter-loss price at rtf 1000 was not re-measured on this tree.
