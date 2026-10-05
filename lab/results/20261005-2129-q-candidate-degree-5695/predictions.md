# Predictions (written before the decisive scaling runs)

Setup: the tiered candidate structure (envelope tree over Binet (U,V,W) + analytic arming with the
exact integer first-hit; exact machinery only on armed pairs). Horizon 100 orbits, sigma_e = 1e-2,
a in [1, 1.5]. Two series: *dilute* (rho = 1e-4 x 1e4/N, the r8 convention: encounter rate per body
fixed) and *fixed* (rho = 1e-4: the belt densifies, real encounters per body grow ~ N).
Cases already tuned on: N = 600 (truth), 1e3, 1e4 dilute, fleet/narrow/densified held-outs.
Cases NOT tuned on (these predictions): 1e5 and 1e6 in both series, the kick experiment, tree
traversal counts.

1. **Misses = 0 everywhere**: the tiered event set equals the base event set (same exact machinery,
   armed is a superset) at 1e5 and 1e6 dilute and fixed. Prediction: holds. If it fails, the fast
   linear window on Wide arcs is unsound for some high-e pair and must be dropped (the fleet
   held-out is the adversarial case; it passed at 1e4).

2. **Candidate degree per body grows ~ linearly with N in both series** (measured 48 at 1e3 to 450
   at 1e4 dilute; expect ~8.6k at 1e5, ~86k at 1e6 in both series — the cone candidate set is set
   by the eccentricity spread, not by rho).

3. **Fires per body per horizon**: dilute ~ constant (~2.3 per body per 100 orbits, matching the
   r8-convention 0.04/orbit); fixed ~ x10 per decade of N (2.3 at 1e3... i.e. proportional to N).

4. **Armed tracks fires, not candidates**: armed/fires stays in [3, 6] at every N and rho
   (measured 4.2-5.0 on tuned cases). Prediction: 1e5 and 1e6 stay in [3, 6].

5. **The touch is irreducible per candidate**: arm tests per fire = candidates/fires. Dilute: grows
   ~ N (26 at 1e3 -> ~190 at 1e4 -> ~1.9k at 1e5 -> ~19k at 1e6), so per-body arm work grows ~ N
   while fires stay flat: the strict C log N gold is NOT met under dilution. Fixed: candidates/fires
   stays ~ constant (150-220), so total work stays proportional to the real encounter rate: the
   gold's first clause IS met at fixed distribution. This asymmetry is the central predicted fact:
   the arming touch is one O(1) integer test per crossing pair per horizon, and no sound
   certificate above the pair can skip it (the firing set is pseudo-random in the pair phases).

6. **Per-fire cost**: tiered us/fire in [4, 12] across all cases (dominated by ~1.4 us/arm-test x
   candidates/fires + exact checks); base us/fire similar within a factor 2 (speedup 1.1-1.5x only,
   because the base's real cost is already the Wide-section numeric windows, which armed pairs still
   pay once per horizon). Prediction: speedup stays below 2x: the win is in the *structure*
   (armed 4-5x fires, zero misses, O(log N) kicks), not yet in wall clock.

7. **Kicks (player burn, eps in 1e-7..1e-3, N = 1e4, 1e5)**: base re-setup costs ~ (candidates per
   body) x ~4 us, growing ~ N (measured by r8: O(N) re-setups per burn). Tiered: path refresh
   O(log N) node recomputes (~15-17) + slack-guarded re-arming that skips > 90% of pairs at
   eps <= 1e-5 with ZERO skip violations at factor 1.5 (their kick experiment measured skippable
   fractions; mine re-derives the slack from the first-hit time). At eps = 1e-3 (a real burn) more
   pairs re-arm but still << all. Prediction: tiered kick speedup > 5x at eps <= 1e-5 and > 2x at
   1e-3; skip_violations = 0 (if not, the slack factor must rise and I report it as a fail).

8. **Tree (envelope cone between groups)**: in the belt, pruning is weak (the (V,W) spread of any
   large node ~ the belt's whole eccentricity spread, so node tests ~ a small multiple of N log N
   and leaf-pair tests ~ the sweep): node_tests_per_body grows ~ log N (10-30). On the fleet
   held-out, envelopes prune sharply (fleet vs far belt nodes separate in U): node tests drop far
   below the belt case. Prediction: belt prune_frac < 0.5; fleet prune_frac > 0.8.
