Working...
Check complete. `lab/results/20261009-0208-inversion-a937/check.md` written; nothing else in the run folder touched.

**Grade: gold**

**Reproduced:** clean rerun of `python3 train_probe.py --scene all` → bit-identical to the author's `metrics.json` (13/13 rows). Patch empty. Predictions pre-registered (mtimes 02:34:25 < run.log 02:35:26 < metrics 02:38:59); kill criterion fired as written; the one failed prediction (polar pair count) was disclosed with the correct diagnosis.

**Independent verification:** my own brute-force d_min agrees with the analytic truth on all 75 true and 29 near-threshold-false pairs (max deviation 0.001·ρ); dense 201-sample sweeps through each polar contact confirm "missed at any cadence" (min ring rank anywhere: 13); direct simulation of polar ring order-changes gives 39,472/orbit at n=200 ≈ 0.99·n², confirming the quadratic maintenance.

**My attacks strengthened it:** the break is sharp at i = 90° (safe at 80° with full node spread), a 0.02-rad orientation clump still misses 100% at i = 90°, and the sort-key loophole closes — of the three readings of "sort by longitude", inertial azimuth and mean longitude miss 100% on polar while node-phase rescues polar but misses 87.5% on a mixed-orientation swarm: no scalar key is sound inside an orientation-mixed Binet clump, so the trigger must gate on orientation ∩ sense under every reading.

**Handed back:** the proposed guard needs a third term (sort axis bounded away from the polar fold, or per-clump-plane phase) — at exactly i = 90° an orientation clump of any tightness still breaks it; and the "retrograde resurrects the quadratic tier" headline overstates the footnote's honest version (the clash's true events are themselves quadratic, so O(overtakes) ≈ O(events) tracks the optimum; the lasting retro finding is sense-blindness plus the fixed-cadence miss the safe control shares at 94–97%). One adoption-time item for the integrator: the gold's folder isn't published in this tree, so its trigger's exact text should be confirmed — Binet space's blindness to orientation makes the author's reading almost certainly right.
