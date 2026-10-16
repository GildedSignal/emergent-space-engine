# Predictions (written before the decisive flights)

Context: the checker proved run 20261016-0504's ES_ATTRIB instrument was duplicated (a shadowed
`attribs` Vec and two `take()` pushes per frame), so row *i* carried frame *i*/2's counters and every
odd row read zeros. This run re-flies everything with the deduplicated instrument (verified: rows
attributed on both parities, 147 even / 155 odd; worst-6 = d2 k26–32 b135–197, frames
198/396/594/793/991/1189 — the ~330-game-s beats). Held-out below = numbers the checker's 20-s
baseline flight did NOT report.

- **P1 (headline identity, control).** The dedup touches instrumentation only, so the author's table
  regenerates exactly: baseline N=10³ 60 s max 334 / p99 136 / envelope 198·192·178·210 / ev/gs 4.02;
  stag 260/136/4.02; phase 53/25/4.78; N=0 max 51; N=600 and N=10⁴ 20 s identical (240/136/5.82);
  digests: OFF = the frozen record bit-for-bit (4b822570 / 6895ce06 / ddd5b1cc, kicks 1530/3767/3767),
  stag e5e9bea5 (3750), phase 708f7d82 (3932).
- **P2 (the decisive one: corrected composition at 60 s).** The worst-12 frames' mean total stays
  217.1 (events are untouched), but the planet-doll share (d2+d3) rises from the author's 71.4 to
  **≥ 190 (~88%)**, residue ≤ ~27 — one population (Home's doll), no second delivery lane. The worst
  frames' composition is d2 k≈26–32, b≈135–200, d3 ≈ 3.
- **P3 (N=0 floor, held out).** The author's N=0 split (tot 40.6, planet-dolls 4.8, "fleet" 35.8)
  was the same artifact. Corrected: tot stays ≈ 40.6 and **d2+d3 ≥ 20 (~50%)** of it — the floor is
  the dolls' own traffic (planets' boundaries), not an unattributable fleet.
- **P4 (phase arm's post-collapse shape, held out).** The author's (32.1, 5.5, 26.6) corrected to
  d2+d3 ≈ 15–30 of the same 32.1: after the collapse the worst frames are the same doll traffic the
  N=0 plane shows (P3's composition), so "the collapse leaves the N=0 plane's shape" survives with
  corrected numbers.
- **P5 (what the residue is).** Of the worst-12 residue (tot − d2 − d3), d0 (the player's own doll)
  carries **< 8 events/frame** at N=10³; the remainder is events `resolve_body`'s first-item
  attribution never sees (doll-level work), not a body population.
- **P6 (N-independence of the corrected split).** base_n600_20s and base_n1e4_20s corrected splits
  equal base_n1e3_coast's (177.6 tot / ~165 d2+d3 / ~13 residue) — the comb and its composition are
  N-independent, not just its totals.
