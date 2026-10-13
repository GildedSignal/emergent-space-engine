Working...
Check complete. `check.md` written with **Grade: gold**.

**Reproduction** (base `294215b8` = HEAD, author's `patch.diff` applied): `regen.sh` regenerated every number identically — 0/112 round trips keep the key, 10 refused, negative control passes, fixed-point control rows match `regen.log` digit for digit.

**Premise verified in shipped code**: `universe.rs:743-761 resolve_handout` → `bind_surface` → `bind.rs:266 Rebinding::from_state` on the leaver's state; `identity.rs` is dense-internal only (Chronon vs EventCore, scenes born in-frame); `lab/rungs/` has no r5; `law.md:51`/`representation.md:70` carry the identity claim. The author's framing of the untested seam is exact.

**My attacks** (`crates/space/examples/checker_transit.rs`, left in tree):
- **Walk depth 16** (the author's named first checker experiment): no full-key repeat in ~100 chained transits; at fine words the drift is *directed*, −1 k-ulp per transit at (20, 0.5) — floor-bias, not a random walk. Stronger than claimed.
- **Outside the author's range**: leak persists at p = 10⁵ and 10⁶ (grid stopped at 10³), e = 0.9999, retrograde sense.
- **Unbound passages** (a class never tested): leak persists; at E≈12 the k word is stable yet the full key still walks — a k-only criterion would pass a broken build.
- **Severity calibration**: `reconstruct() == input` everywhere — the residual carry keeps the state exact at each hand-out, confirming the leak sits exactly where the author scoped it (key/Catalogue/event graph), not in the state.

**Flaws recorded**: the dossier says "three decode overflows" — the table holds ten cartesian `Range` refusals; no end-to-end `resolve_handout` scene (disclosed; my coarse-word and galaxy-scale probes bound the omitted rounding from above). Neither changes a conclusion.

**Wiki page corrected in place**: the inverted "moved the OrbitKey on 0/112 probes" (now 112/112), refusal count, and the checker extensions (directed walk, passages, galaxy scale) folded in; open direction 2 now names only the end-to-end scene as open. Nothing else in the run folder touched; no commits made.
