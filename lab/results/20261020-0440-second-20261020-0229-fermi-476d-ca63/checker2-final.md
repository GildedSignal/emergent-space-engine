Working...
**Grade: gold** — written to `check2.md`, page corrected in place.

**What I verified (blind, independent):**
- **Reproduction:** fresh `gs_analysis.py` run identical to regen.log; tail identity re-derived with my own loader (1.515–1.530 ev/body at 1e5, 1.264–1.280 at 2e5, fence-on same count); all 17 matrix CSVs carry the gs instrument, all 7 shipanchor CSVs are unpatched and reproduce 2d26; patch applies clean at base `5f7ce7a1`; predictions (04:52:51) precede all 15 decisive flights.
- **Four adversarial arms, three outside the author's grid:**
  1. **Fence-2e5 full-window** (author's arm was `covered: False`): tail still 7,084 ms at 1.280/body with the memory channel verifiably deleted (held 386, RSS 1,089 MB) — the tail-is-arrivals kill stands in its strongest form.
  2. **rtf 400** (play cadence, third axis): onset_gs 13,102, wave totals unchanged — the gs lock holds.
  3. **Seed 2:** onset_gs 13,129, eras identical, but the fixed crest window captures only 0.49/body — the 0.98/body constant is registration×seed-bound; per-wave totals (~1.1–1.3/body) are the stable object. Page now carries this caveat.
  4. **3e5 fresh draw:** 14,467 ms / 0.998/body / 48.3 µs/ev — confirms the author's "+26% steepening" and α-disjointness were single-draw artifacts (draws now {1.53, 0.92, 0.90}); crest ≈ K-linear at ~48–50 µs/ev.
- **Page corrections:** wave total 2.56–2.57 → 2.49–2.51 (did not regenerate); added a checker2 bracket with the seed/cadence findings. Topic stays open (not three agreeing golds on this sentence).

Gold because it refutes a standing record premise (476d's "the fence deletes the tail") by deletion, re-anchors the exit table on schedule-invariant quantities, regenerates end-to-end, and costs nothing in code to adopt. The author's own honest scoring of P4/K4 is the result, not a defect. Repo left clean at base; no commits made.
