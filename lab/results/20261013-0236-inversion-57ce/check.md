Grade: silver

Abstract (for the integrator). The in-flight E→1 crossing — the page's named unmeasured regime —
is measured safe on shipped code: the Cycle→Passage flip lands at E−1 ∈ [5.6×10⁻¹¹, 6.5×10⁻¹⁰]
at every level L5–L15, clock relerr ≤ 6.5×10⁻¹⁴, zero refusals, and the Home→root doll handoff
compiles at E−1 down to 1.8×10⁻⁶. The losses are beside the seam: L1–L4 die silently at Home's
surface (r < 1.1306×10⁹, fault=None, zero refusals), and a held reverse never captures (E rises
to 1.13 / 4.29 / 196 at L5/L8/L15). Reproduced digit-for-digit; five adversarial flights (L1, L6,
B5, B15, seed 2) all support or sharpen. Gain: closes the topic's named hole and redirects
attention to the silent-loss faults. Cost to adopt: nothing in the engine; page facts plus the
one-tag `fault` proposal the page's open direction 4 already names.

## Reproduction

- regen.sh exit 0 (runner); every number in regen.log matches dossier and out/.
- I applied work/patch.diff myself in the restored tree, built, and reran A8 and A5: digit-for-
  digit identical to the author's out/ (wall times stripped). B8's tail E = 4.288858767 at
  t = 287,044,013,625 matches exactly.
- Code claims verified in the tree: `step.rs::boundary_clock` kills at `r < surface` and at
  `r > 2^leave_log2` with `alive=false` and no fault field (the "silent" attribution is right);
  `thrust::word` packs keys in bits 0–3 (forward/reverse) as the probe assumes; gate C1's oracle
  (`tests/clock.rs:90-92`) is the same `u^t = 1/√(f − vr²/f − vt²)` the probe uses.
- Predictions pre-registered: predictions.md mtime 02:44:42, original out/ ≈ 02:53, dossier
  03:11. P2 (clock ≤ 10⁻⁵, no spike), P3 (zero refusals), P5 held; P1 and P4 falsified and
  reported as falsified, in the informative direction (the crossing lands inside the band the
  author guessed was dangerous and is safe; the capture is never reached at all).

## Attacks (mine, beyond the author's grid)

1. A6, the untested gap level: crossing safe — E−1 = 7.014×10⁻¹⁰, relerr 1.2×10⁻¹³, handoff at
   E−1 = 2.949×10⁻⁶, zero refusals. Supports.
2. A1, below the author's range: also dies silently at the surface (event_time 1.122×10⁸,
   r_at_death 1.0516×10⁹ < surface, fault=None, zero refusals); death ticks stay monotone
   L1→L4. The crash regime is the whole gentle half, not L2–L4. Sharpens.
3. B5 and B15, the capture probe outside the author's single level (B8): no capture at either —
   E rises to 1.126 (L5) and 196.2 (L15), zero refusals, alive, fault=None. "The pump owns the
   arrival maneuver" generalizes across the throttle. (My first B15 was killed by my own 90 s
   timeout; rerun at 200 s completed.)
4. Seed 2: the player's flight is bit-identical to seed 1 (A5 brackets and the A4 death match to
   the last digit). Not luck: `scenario.rs::plane_with` spends its lcg only on the 23 free ships;
   the player's and the planets' orbits are fixed literals. The seed axis is null for this probe.
5. The dossier's "zero refusals, alive" for the pump tail was not printed by the probe; I reran
   B8 with the record printed: refusals=0, events=5109, alive=true, fault=None. Confirmed, no
   longer just inferred.

## Novelty

The published page names "the E→1 crossing *in flight*" as not measured (Domain line), and its
open directions name neither the crash threshold nor capture-from-passage. The near-rest pump
(γ ≈ 1.2) is dynamics-1890's; the arrival-maneuver pump, the L4/L5 threshold and the
fault=None indistinguishability are this run's. No H entry covers the in-flight crossing.

## Why silver, not gold

Real, reproduced, adversarially robust and honestly reported — but the gold bar is "held-out
predictions held" plus a 10× move, a deletion, or a refuted premise. Two of five predictions were
falsified (P1, P4); the run's own dossier says "not a 10× mover"; and the page's standing premise
("the parabolic edge is safe") is *confirmed in flight*, not overturned. The run closes a hole
and adds facts; it deletes nothing and breaks no premise. The author agrees ("nothing to adopt in
the engine").

The one experiment that would make it gold: fly the downward crossing — the Passage→Cycle
capture — with a scripted, timed flip burn (reverse near periapsis, flip at apoapsis, bracket the
flip back to Cycle), the page's own named next experiment. That measures the last unmeasured
quarter of the seam and either exposes a defect at the true capture or retires the whole seam;
either outcome is a verdict, not another safety confirmation.

## What the author missed

- The seed axis cannot move the player in `plane` (rng spent only on free ships; verified
  bit-identical on seed 2). "One seed" understates the coverage; the live untested axes are the
  nose (wt/play), other scenes, and non-forward input patterns — worth saying on the page, where
  I have corrected it.
- L1 and L6 were one cheap flight each and complete the picture: crash regime = L1–L4 (all of the
  gentle half), crossing safe at L6 too.
- The pump's level scaling (E→1.13/4.29/196 at L5/L8/L15) — the no-capture claim is level-
  independent, and the pump strengthens with level; the page now carries it in the Runs line.
- The bracket's lo rows print post-flip states (both rows of every bracket show the new family),
  so the last pre-flip Cycle state was never measured. Harmless here — E−1 is constant across the
  pair (the burn's quantum) — but the "bracket" is a pair of adjacent post-flip samples, and the
  dossier's column header ("E−1 at first Passage state") is the honest description of it.
