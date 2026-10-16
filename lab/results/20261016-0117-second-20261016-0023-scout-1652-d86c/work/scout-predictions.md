# Predictions (written before the decisive run)

Run: 20261016-0023-scout-1652. Scene: the ladder belt (`scenario::plane_extra`, seed 1, 48 fleet,
N as run), coast, cuts at 15k / 20k / 32k / 48k game-s (the first kick wave lands 13,051–14,534
game-s; the belt's kick interval is the doll grid, 28,141.5 s median, 3294/f82a).

**The claim under test:** the history stack's `h.len() > 1` floor (`PlainBodies::prune`) pins one
retired `Segment` per body forever, although the engine's own prune rule certifies a binding
forgettable at `keep = 2·light_distance + 2²⁶` ticks; so the standing stack is almost entirely
outside every reader's reach.

Held-out expectations (not tuned on; the census instrument is written before any run):

- **P1 (the duty cycle).** At the 32k and 48k cuts (past the wave, before/after the second), the
  fraction of bodies whose newest retired binding is still inside `keep` is **under 15%** (the
  light window ~1.3–2.3 k s against the 28.1 ks interval ⇒ ~5–8% steady state). At 20k (≈6 ks
  after the wave) it is **under 3%**. At 15k (inside/just after the wave) it is **over 50%** —
  the transient the window exists for.
- **P2 (the standing pin).** At 32k and 48k, bodies with history ≥ 95% of those with any history
  sit past the window (398f's 1.04 segments/body is floor-pinned, not window-needed).
- **P3 (the read instrument).** The deepest past read any retired segment ever serves
  (`until − t`, cumulative over the whole flight) is **below the belt's median keep window**
  (~1.3–2.3 k s) and far below the interval (28.1 ks). If max-depth approaches the interval,
  the floor is load-bearing and the claim dies.
- **P4 (dead weight composition).** Dead bodies (if any at coast) hold segments at the same
  ~1/body rate; the belt's pinned bytes at the measured standing widths compose 10⁹ to the
  same order as 398f's 1.0–1.3 TB record stack.
- **P5 (control).** The locals/moons near Home (short periods, frequent kicks) show small ages
  and histories that the existing prune already shortens below 1.04/body — the floor's cost is
  concentrated where kicks are rare relative to the light window (the belt).

Kill criterion: if P3 fails (reads routinely need eras older than keep), the floor is a real
requirement and this run reports it as such (a lead, not a lever).
