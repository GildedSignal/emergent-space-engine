# Predictions (written before the decisive runs)

Question: the player-scan's fallback (`radial.rs::candidates` returns None → `encounter.rs:175` walks `0..bodies.len()`) reads every body in the universe and discards each cross-doll one at `encounter.rs:181` AFTER the `binding_at` read. The per-doll index already holds the doll-local population. A bail therefore costs O(universe) reads to build an O(doll) candidate list.

Fix under test (env `ES_LOCAL_BAIL`, off = pristine path): on a bail, `candidates` returns the doll's own registered population (unbounded + all bins, deduped) instead of None. Off-arm must be bit-identical to pristine main.

Cases not tuned on (held out): the `ladder_digest` frozen case set in full (9 schedule-agreeing cases + 4 wave/belt-crossing cases, including the belt-crossing L10 arms where the player is INSIDE the belt's doll — the seam case, where bails should be the norm); seed differences are covered by the digest set's own four schedules.

P1 (composition): on every flown arm, cross-doll reads dominate the fallback walk whenever a bail fires beside the belt: at N=10⁴ coast, a bail's walk is ≥ 90% belt bodies (the belt lives in Cinder's doll; the player's doll holds ≲ 400). Cross-doll candidates are 0 by construction (`other.doll != me.doll` continues) — I predict the census confirms exactly 0 candidate pushes from cross-doll reads in every arm, i.e. the reads are pure waste.

P2 (yield): bails are common where the pages said: at plane scale (N=0) ~100% of captures bail (604c), and in the belt-crossing arms ~all captures bail. On N=10⁴/10⁵ coast (player in Home's doll, belt in Cinder's) the filter mostly stays on (c439's 186-candidate regime) — I predict a minority of bails there.

P3 (exactness): `ES_LOCAL_BAIL=on` reproduces the off-arm's `ladder_digest` output byte for byte on all 13 cases (the candidate set is equal by construction: index ⊇ retained bindings per doll, and the loop's cheap tests — alive, born, doll match, reach ≠ 0 — are unchanged; a completeness bug in the index registration would show as a digest move).

P4 (cost): with the fix, a bail's read count drops from O(universe) to O(doll): at N=10⁴ from ~9.5k reads per bail to ≲ ~400; capture wall µs per scan drops accordingly; the frame's engine p50/p99 at plane scale and coast arms are unchanged or better (the scan is not the frame's owner there — promotion page's finding); the held-scan pin is untouched (it holds the post-filter candidates, which were already doll-local).

P5 (the deletion): with the doll-local fallback, the bail's threshold (`self.bodies/4 + 64`, the nonlocal knob 604c flagged against PRINCIPLES 15) becomes cost-neutral: both sides of the threshold are O(doll). I predict the threshold's setting no longer moves any measured cost by more than noise (not flown as a knob here; argued from P4's read counts — recorded as an inference, priced by the arm comparison).

Kill criterion: if the on-arm digests differ anywhere, or if cross-doll reads are a minority of the fallback walk on the belt arms (P1 fails), the claim dies and the bail's cost is not the doll partition's artifact.
