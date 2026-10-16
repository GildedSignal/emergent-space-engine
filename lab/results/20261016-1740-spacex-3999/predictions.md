# Predictions (written before the probe ran)

The unmeasured case (scan-queue page, cdf0: "the belt-bin regime (the player inside the belt) stays
unmeasured"; radial.rs's own doc names it): the player's neighbourhood scan in the ROOT doll at belt
radius, where the ladder's belt (uniform [2,3) AU = one octave = 16 sixteenth-octave bins, doll 0)
lives. The shipped flights never scan there: the player is born in Home's doll. Instrument: the
shipped `Radial::candidates` and `BodyStore`/binding readouts, print-only, no engine edit; the
belt-bin window is a real belt body's own window (its r, v, step, radius), so every parameter is the
engine's.

Seed 1, extra in {0, 10³, 10⁴, 10⁵}. b = 5 ms (ENGINE_BUDGET_MS), so the latch bar is S ≥ b/2 = 2.5 ms
(69f3: the drain answers only while room ≥ 2·scan_ns, and scan_ns ≥ S's cold answer).

- **P1 (the fallback is NOT the belt's disease).** The `bodies/4 + 64` rule does not trip for an
  in-belt window at any flown N: one bin holds ≈ N/16 bodies (625 at 10⁴, 6.25k at 10⁵) against the
  threshold N/4 + 64. Verdict Some(k) with k within [0.5, 2]× N/16 at 10⁴/10⁵. The fallback stays a
  small-N disease of Home's doll (cdf0), reproduced as a control at small extra.
- **P2 (the answer half latches in-belt at ladder N).** S_answer = kept × per-read. Per-read
  (binding cartesian + exact predicate) 4–9 µs, flat in N (cdf0: 4.5–8.5 µs). So S ≈ 2.5–6 ms at
  10⁴ and 25–56 ms at 10⁵: the drain latches permanently in-belt from N ≈ 5×10³–10⁴ up. The capture
  half (alive/born/binding_at/doll/reach walk) stays ≤ 0.5 µs/body ⇒ never the latch term.
- **P3 (hits ≈ 0, slack lives in angle).** True encounters per in-belt scan ≤ 2 (a 2πr arc at 2.5 AU
  shared by ~N/16 bodies leaves a mean angular gap ~2.4×10³ km against near ≈ 1024·(2 ship radii) ≈
  100 km); reads-per-hit ≥ 10³ at 10⁵. The nearest non-hit's miss distance ≥ 10× reach, and its
  angular separation (|Δλ|·r) is of the same order as its miss (the radial filter already removed the
  radial misses), i.e. an angular certificate can carry the cut.
- **P4 (controls).** (a) Home-doll window at the player's own radius: fallback at extra ≤ 10³
  (cdf0's 95%-of-captures regime; threshold = bodies/4+64 ≤ ~333), Some(small) at 10⁵ (threshold
  25k ≫ Home's population). (b) Hauler windows (doll 0, 0.5–8 AU): Some with counts ∝ local bin
  occupancy, no fallback at 10⁵. (c) A window with h → ∞ (the whole belt in one interval) must
  return None (the fallback fires when it should).
- **P5 (cost shape).** Per-read cost flat in N (no cache-growth term at 10⁵); binding_at per body
  0.1–0.3 µs, also flat.

**Kill criteria for my claim** ("the scan's seam latches inside the belt at ladder N, through the
answer half, with angular slack to spare"):
- kept(10⁵, in-belt) < 100 ⇒ P1's bin-occupancy model is wrong and the apsdial filter is far finer
  than sixteenth-octaves ⇒ the seam does NOT latch and the angular cut is unnecessary at 10⁵.
- hits per in-belt scan > 10 ⇒ the belt is genuinely encounter-dense ⇒ the certificate has no slack
  to take and the representation (per-pair exact answers) is the wrong water, not the cut.
- per-read cost growing ≥ 2× from 10⁴ to 10⁵ ⇒ a memory/cache term I did not price.

What I tuned on: nothing yet — these are written before the first run of the probe.
