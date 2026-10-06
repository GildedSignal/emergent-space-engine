# Predictions (written before the decisive patched runs)

Baseline (this machine, `xtask universe --kick-bench --seconds 55`, seed 1, rtf 1):
made kicks median 51.4 µs (n=25), leavers 364 µs (n=12), 37 samples; exact shape sharing 0/31;
replay digest `989892a426b5ac4e7313a9ac3da8ccff8e8a13be7524c4da9e842ed42e927667`.

Cases I have NOT tuned on, and what I expect there:

1. **Profile split of one kick.** I expect the rebind to dominate: fit_key's arithmetic
   (norms, reciprocals, a 128-step bisection with witness) plus `Orbit::compile`/`Passage::compile`
   together > 50% of a made-body kick on this box, and an even larger share of a leaver kick
   (leavers rebind into passages and cost ~7×). I expect the proper-time bookkeeping
   (`orbit_state(t)` and `orbit_state(event_time)`, two full decodes) to be 5–15%.
2. **Exact shape memo wired into the plane's rebind path** (`ShapeMemo`, keyed by
   `ShapeKey {k, compactness}` with the weak-branch collapse q ≤ 2^WEAK_EXPONENT):
   hit rate ≈ 0% on this scene, because the plane's kicked bodies sit in child dolls where
   compactness is far above the weak cutoff, so exact sharing never fires. If it does fire, the
   kick median must still be bit-identical (pure function of the key) and the replay digest
   unchanged — that is the falsifier for "memoization changes the law".
3. **Caching the binding's decode at its own event_time** (a constant per binding, decoded twice
   per rebind today): replay digest unchanged, kick median down by the share prediction 1 gives
   it (I expect a small cut, 3–10%, not a step change).
4. **If the profile shows the secondary/tide gather (decoding other bodies' tubes per kick) above
   20%**, that is the next exact deletion (per-doll, per-epoch cache); I predict it is below 20%
   here because the scene has few secondaries.

Kill criteria: any digest difference kills the patch (law change); a profile that contradicts
prediction 1 (rebind < 50%) kills my premise that the compile is where the kick's money goes.
