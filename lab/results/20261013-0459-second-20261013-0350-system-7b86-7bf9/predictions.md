# Predictions — run 20261013-0459 (second author on 7b86)

Written before the decisive run. The experiment: land the deletion (`observe::partial` reads the
tube alone when `TUBE_ONLY_READS` is set — the fresh `force::field` evaluation and the `secondaries`
walk that feeds it are not done), then measure on 7b86's own scenes (same scripts, seed 1, 48
members, paced 8 s at 60 Hz, rtf 100, plus a 400-member dense attack; frames not wall-cut, so the
A/B pair flies bit-identical simulations): the digest, the player-instrument deltas, the gather's
cost/share and the p99 frame. These cases are not tuned on; the bench has not run yet.

1. **Digest:** bit-identical fresh vs tube-only on every scene, including the L15 dive and the dense
   400 flight. The engine's canonical paths read tubes (`root_state_raw`), so the deletion moving an
   observation-only read cannot touch an outcome. *Kill:* any DIFFER — that would mean a canonical
   path reads `partial`, and the deletion is a law change, refuting the claim's safety half.

2. **Instrument deltas (in-engine, per seen body, in root ticks):** p99 ≤ 2×10⁻⁵, max ≤ 3×10⁻⁵ on
   every 48-member scene — the external probe (7b86, quad_slot) bounded the same quantity at
   ≤ 9.8×10⁻⁶ over synthetic read windows; the in-engine windows may differ slightly, so I allow ~3×.
   Zero on plain scenes (coast, L8, brake). Doppler |Δshift| p99 ≤ 10⁻⁵. *Kill:* p99 > 10⁻³ ticks.

3. **Gather gain (fresh/tube, p50):** between **1.3× and 2.5×** on the 48-member scenes. Reasoning:
   the fresh-eval path serves ~43% of body-reads (7b86's census), and on 51bf's scene field
   evaluations were 81% of readout time; each fresh eval is a `secondaries` walk (a Vec allocation +
   a tube decode per source) plus `force::field`. If the gain lands **< 1.1×**, the cost case for the
   deletion fails on these scenes even though the bound holds — I will report that as the claim's
   cost half refuted at 48 members.

4. **Dense 400 scene:** gain ≥ the 48-member gains (I predict 1.5–3×): read multiplicity per body is
   10–17.6 there (the checker's census), so the readout dominates the gather even more.

5. **Frame p99 gain:** strictly smaller than the gather gain on every scene (the engine's share
   dilutes it), between 1.05× and 1.6× at 48 members.

6. **Readouts:** within 2% between fresh and tube-only on every scene (the crossing's Newton solver
   is bracketed; a ≤ 10⁻⁵-tick output change should not move convergence counts materially).
   *Kill:* > 5% — that would mean the deletion changes the view's work pattern, and the timing
   comparison would need readout-normalized numbers to stand.

7. **Gather share of the frame:** ~55–75% fresh (the page's 56–93% band, these are small scenes),
   dropping by roughly the gather gain when the deletion lands.
