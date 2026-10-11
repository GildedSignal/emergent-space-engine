# Predictions — 20261011-0517-quant-d7bd (written before the decisive experiment)

Question: what does one player event cost as the player's doll fills, and how much of that
wake is the exact encounter scan (`PlayerNeighbourhood::find`, run after **every** resolved
player item, `crates/universe/src/universe.rs:587`) against the kick itself?

Machine: GitHub Actions Linux x86, i7-4790, load ~0.7, 16 GB. Orders of magnitude only;
the integrator re-measures on the M1.

Cases held out (not tuned on): the slope of scan cost vs body count N; the player item's
cost share at N ≈ 2×10³; the crossing N where one player event alone exceeds a 16.67 ms
frame; the waste fraction (scans returning no encounter); the non-player control.

- **P1 (shape and slope).** `find` cost is linear in total body count N (it clones a
  `Binding` per body, then `cartesian` for same-doll bodies). Slope s ∈ [0.5, 8] µs per
  body on this box.
- **P2 (attribution).** In live flight at RTF 100 with a held burn, the player's mean item
  cost at K = 2,000 added doll orbiters is ≥ 5× its K = 0 cost, and ≥ 80% of it is the
  scan. The mean cost of a non-player ship item changes < 30% from K = 0 to K = 2,000
  (control: only the player pays the scan).
- **P3 (capacity).** One player event alone crosses 16.67 ms at total N between 5×10³ and
  5×10⁴. Below that the seam holds; a belt or handed-out fleet in the player's doll at
  ~10⁴–10⁶ breaks the frame per player kick.
- **P4 (waste).** The scan returns zero encounters on ≥ 99% of calls in these scenes: the
  player's neighbourhood is empty almost always, so the linear cost buys nothing almost
  every time ("compute only surprises", PRINCIPLES 3).
- **P5 (contract controls).** (a) Calling `Universe::start()` a second time immediately
  after `plane()` (before any advance) is digest-neutral at K = 0 — otherwise the live
  K > 0 runs are invalid and the claim shrinks to the sweep. (b) Frames resolved one item
  per `advance` give the same digest as unlimited-budget frames at the same K (the budget
  moves when, never what).
- **P6 (cadence).** With a held level-4 burn the player resolves O(10²)–O(10⁴) items per
  game-second (kick step = 2^7 per radial period and the burn re-keys it), so the scan is
  paid per kick at a rate that multiplies the slope: surveillance cost per game-second
  ≈ cadence × N × s.

Kill criteria (frozen before the run):
- If s < 0.05 µs/body, the exact seam holds past N ≈ 3×10⁵: the premise "the seam breaks
  at fleet/belt scale" is killed and the result is a lead (no action needed before the
  Binet cone lands).
- If the player's live item cost at K = 2,000 is < 3× its K = 0 cost, the scan is not
  what a player event costs; I report the attribution honestly and claim nothing about
  capacity from the live run.
- If either contract control in P5 fails, the live numbers are void for K > 0 and only
  the direct sweep stands.
