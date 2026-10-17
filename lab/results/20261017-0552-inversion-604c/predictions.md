# Predictions (written before the decisive runs)

The question: is the player-scan's read demand O(1) in the crowd around the player, as the promotion
page's census concluded (70.0 candidates a scan at burn, 184 at coast), or was that bound manufactured
by the ladder scenario's own shape — locals capped at 300 (`ladder_locals = (extra/2).min(300)`), none
below 5,200 root units (the player sits at 4,740, Home's low orbit, an empty band), the rest a belt the
radial apsidal filter cuts? The inversion: fly the game's own crowd — a fleet formation on the player's
own circle — and measure the scan.

Cases I have NOT tuned on (the formation's draws are fixed by seed 1 and k before any run; I have not
run the sweep yet):

1. **Candidates scale with the formation, not O(1).** At `form = K` (extra = 0, coast, 10 s, rtf 100),
   I predict mean candidates/scan ≈ K + c with c the unbounded set (planets, moon, player ≈ 5-8):
   K=50 → ~55-60; K=200 → ~205-215; K=1000 → ~1005-1015. The census's 70-184 class does not reappear.
2. **The `bodies/4 + 64` bail-out converts concentration into a full O(N) walk.** The filter bails when
   the kept set exceeds a quarter of ALL registered bodies. With the plane's 28 + K formation bodies, the
   threshold is (28+K)/4 + 64 ≈ K when K ≈ 111. Prediction: at K=50 zero bails (kept ≈ 55 < 70); at
   K=200 nearly every scan bails (`bailed_count` ≈ scans) and the capture loop then walks ALL bodies
   (mean full-walk length ≈ 28+K, not K): ~228 at K=200. The formation thus reads the belt too.
3. **The belt control stays O(1) (the negative control, the census's own case).** At form=0, extra=10⁴
   and extra=10⁵ (10 s, coast): mean candidates/scan within ±20% across the two N (the census's 70-184
   class), zero bails — the radial filter cuts the spread belt exactly as the page recorded.
4. **Held-scan memory becomes crowd-proportional.** Each held scan pins its candidates (`Binding` +
   key each; the probe prints `cand_bytes`). Worst held scans × candidates × cand_bytes at K=1000 should
   reach the MB class per held scan (≥ 1000 × cand_bytes), against ~70 × cand_bytes on the census's
   scene; held_max > 1 for most frames at K ≥ 200 (the answer no longer fits idle time's 750 µs margin:
   the code's own comment prices a ~100-body scan at 30 µs-1.5 ms, so a 1000-body scan is 0.3-15 ms).
5. **The frame itself stays smooth at coast (the design's off-critical-path claim holds) while the scan
   stages swell**: p99 engine ms ≤ 2 ms at K=1000 extra=0 (coast, tiny universe), but the prof stages
   "encounters: capture" and "held scans answered" grow ∝ K per frame (µs/frame at K=1000 in the
   100-1000 µs class, vs ~4 µs at N=0 in the ladder's record).

What would make the O(1) premise survive: if the window's speed term ((v + speed_cap)·h, the only
non-tiny reach term) somehow excludes the player's own bin — it cannot, the window is centred on the
player's r — or if the formation's ships are not registered with ranges (they are: Kind::Ship with a
bounded Kepler tube). If predictions 1-2 fail, the page's O(1) stands on a wider scene than its census
and this dossier reports that.

Kill criterion for my own claim: if candidates/scan at K=1000 stay ≤ ~200 (the census class), the
formation does not swell the near set and the observer half is free after all.
