# Predictions (written before the post-fix sweep)

The fix under test: term 3b (crossing-longitude drift, window centre shift ≤ 2δ/q, capped at
the arc traversal), added to the three q-skin slack terms, plus the width inversion
w/(1−2δ/g) for Cross windows (tangency, saturating at 2δ/g ≥ 1/2). Tuned on exactly one
configuration: belt, ε = 1e-4, κ = 0.3, s = 4·eps_u (15 misses there before the fix).

Held-out cases (not tuned on), with my expectations:

1. **belt ε = 1e-4, s = 16·eps_u**: skin still 0 missed (term 3b scales with drift δ, which
   now reaches s/2 = 8·eps_u; the widening grows linearly in δ, so exactness should hold),
   but setups/kick rises toward `always` as the trigger fires less and the saturation cap
   (pi/4) bites: I predict sat_resets > 0 and setups/kick within 2× of the s = 4 value.
2. **belt ε = 1e-6 (the plane's kick size), s = 4·eps_u**: 0 missed, and setups/kick cut
   ≥ 5× vs always (q-skin measured 12.6× at this size; the added widening only adds
   proposals, not setups, so the cut should survive; false_cand_frac below 5%).
3. **belt ε = 1e-8, s = 4·eps_u**: 0 missed; the skin now almost never re-setups
   (setups/kick < 5 vs always ~140); checks/kick may rise vs ε = 1e-6 (widening accumulates
   over the whole run since triggers fire ~100× later), but still ≤ always's checks.
4. **ring ε = 1e-4** (held out; ring was only run at 1e-6 pre-fix): 0 missed. The ring is
   Wide/Full-heavy; term 3b's cap is the arc traversal, so I expect no tangency blow-up;
   if anything breaks here it will be a Wide-section window shift — my terms cover it by
   the same 2δ/q, but this is the least-derived regime.
5. **fleet ε = 1e-6 and 1e-4** (held out; clustered near-identical orbits, Full-heavy):
   0 missed; setups/kick cut smaller than the belt (q-skin: 2.3×) because Full sections
   saturate under period drift; sat_resets dominate the skin's resets.
6. **The control**: `always` shows 0 missed / 0 false on every case above; if it does not,
   the harness is void, not the skin.

Failure expectations (what would falsify the fix): any miss at ε ≤ 1e-6 would falsify the
claim that the plane regime is sound; a miss on Wide sections at ε = 1e-4 with drift
below the cap would falsify the cap argument; setups/kick at ε = 1e-6 within 3× of always
would falsify the economic point of the skin.
