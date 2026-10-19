# Predictions — 20261019-1452-spacex-396d (the player-seam flight)

Written after the smoke arm's build (no flight output read yet), before the decisive arms.
Instrument: shipped `nladder` flight (`seam` example: the macOS footprint call replaced by /proc, nothing else)
+ print-only `ES_SEAM_CENSUS` in `PlayerNeighbourhood::capture` (one line per scan: doll, radial verdict,
window, candidate count, capture ns). Arms not tuned on: the K sweep and the long horizon below.

The seam: the player burns prograde out of Home, enters the root doll (frame ~948 in prior flights),
crosses the belt's radial band (2–3 AU, doll 0 holds ~K−300 belt bodies in ~10 radial bins).

- **P1 (the bail):** once the player is in doll 0 with the window's bins over the belt, `radial.candidates`
  bails (walk=1): the bin-entry count in the window exceeds `bodies/4 + 64` at every flown K. The walk
  persists after the belt while the window (grown by speed × interval) still covers the belt's bins.
- **P2 (the capture term):** a walk capture costs ~N × 100 ns (c439's binding_at): ~1 ms at 10⁴, ~10 ms at
  10⁵ per scan — the 12 ms budget is crossed between 10⁴ and 10⁵, so `over` grows from ~0 to a large
  fraction during the crossing, or the frame lags instead (frames behind > 0, worst lag grows).
- **P3 (the answer term):** the held scan's answer runs the exact predicate per candidate: at walk=1 the
  candidate list is ~N (belt, doll 0), so one answer costs µs-scale × N (4.4 µs/cand measured by 604c):
  p99/max frames during the crossing spike at 10⁴ already (~40+ ms), and at 10⁵ a single answer is
  ~0.4 s ⇒ held_max pins candidates worth ~N × 192 B each (19 MB at 10⁵).
- **P4 (what breaks first, the ranking):** at 10⁴ the seam is a frame tail (answers in idle room may drain);
  at 10⁵ the answer cannot fit any frame ⇒ the presented time lags unboundedly while the crossing lasts
  (memory second: held candidates). The coast arm (control) shows walk=0 or cheap walks only (player in
  Home's doll; the belt is another doll's index).
- **P5 (the end of the seam):** the walk does not end when the player leaves the belt band: at escape speed
  the window's reach ((v + speed_cap)·h) keeps the belt's bins inside it, so every player item after the
  crossing pays the walk (the permanent-tax reading, 4447's held_scans growth). Kill: if walk=0 returns
  once r_au > 3 + reach, the seam is a transient and P5 is wrong.

Kill criterion for the whole run: if the census shows walk=0 through the crossing at every K (the filter
cuts the belt even inside the band), the seam premise is dead and the dossier says so.
