Grade: silver

**Abstract.** The named experiment is flown and reproduced: the Passage→Cycle capture compiles
from the fixed nose and after a 180° flip at L5/8/11/15 (checker adds L12) — zero refusals,
clock ≤ 2.4×10⁻¹¹, landings 1−E ≤ 8.4×10⁻⁹, apoapsis 10⁸–10¹⁰ all leave-safe, survival at 2×
with E constant; the seam retires and the parent's "unreachable by a held key" dies in the
letter. But the headline defect is an artifact: my same-tick control (E's input log continued
past the flip) matches G8.3 bit-identically at all 31 shared ticks and shows the held-key
capture is a 1.8×10⁷-tick transient that re-flips and pumps out. One world, no schedule
dependence; the arrival still needs the timed cut. Adoption: page-only, nothing to build.

## Reproduction

- `regen.sh` exit 0 (runner) on base `cb16ccb9`; `work/patch.diff` adds
  `crates/universe/examples/crossing.rs` only (804 lines, no engine change — the probe cannot
  have caused what it reports). All dossier tables verified against `out/`: C5/C8/C11/C15
  brackets (widths 4096/512/64/4), 1−E = 4.97×10⁻¹⁰/1.02×10⁻⁹/8.60×10⁻¹⁰/3.82×10⁻¹⁰, apoapsis
  1.92×10⁹/8.85×10⁸/1.07×10⁹/2.52×10⁹ all SAFE, T8 (6.41×10⁻¹⁰, peri 8.69×10⁷), C8.23/C8.26
  (8.38×10⁻⁹, apo 1.02×10⁸), every capcoast alive and Cycle, `refusals=[1-9]` grep: none.
  B8 digit-for-digit: E = 4.288858767 at t = 287,044,013,625. E8.0–E8.3 capture ticks
  1,040,987,996/863,316,357/774,480,537/730,062,627; dt sweep 729,538,339/731,111,203/735,305,507.
- **Predictions:** `predictions.md` mtime precedes every surviving original output (out/E8.txt)
  and the dossier; P1 honestly falsified in the checker's direction (the mechanism story was
  wrong and owned), P2–P6 held, P7 half. Genuine pre-registration.

## The decisive attack (refutes the headline claim)

**X8.3, my control:** `crossing.rs` copied with one change — `held_trace` does not return on
capture; it keeps E8.3's exact input log (one reverse word at t = 399,761,187, never
re-asserted, never cut) at the fixed 2²⁰ cadence **and reads G8.3's 31 settle ticks**.
Result (`/tmp/xcheck/X8.3.txt`, build+run ≈ 10 s):

- **All 31 G ticks read bit-identically to G8.3** (E−1, r, v, err, k−1/2, events): e.g.
  t = 759,364,739 → E−1 = +3.645978697×10⁻⁸, events 2766; t = 4,630,731,179 →
  E−1 = +1.589330401×10⁻³, events 3735 — exactly G's readings.
- The flip E saw is there too: →Cycle at t = 730,062,627 (E−1 = −1.91×10⁻⁹), then
  **→Passage again at t = 747,888,419** (E−1 = +1.85×10⁻¹⁰).

So there is **one world**: the capture exists in G's world at the same tick; it is a
**transient of 1.78×10⁷ ticks**; the held key pumps the ship back out (past periapsis the
velocity flips ~π — G's own trace shows err −8.8×10⁻³ → −0.478 — so the fixed-nose key becomes
an accelerator). The dossier's "schedule-dependent canonical outcome" (Truth violation) and
"end in different canonical states" are **artifacts of the probe exiting at the first flip**:
it compares a world stopped at 730M with one read to 4.6×10⁹ — never the same tick. The
"capture tick moves with cadence" is each cadence's first tick past one fixed flip event
(dt19/20/21/23 bounds are mutually compatible with a single event tick in
(729,014,051, 729,538,339]). `frame_to`'s contract ("a digest taken after settle(limit) is the
same whatever the frames were") **held**; the code pointers (universe.rs:630, 805-832) chased
an artifact.

**Corroboration (the author's own named falsification, run by me):** G8.1 pumps past 10⁻³ at
4.76×10⁹; **G8.2 dies at event_time 1,315,545,753 — F8.2's exact event_time** (same relight
444,179,097, same log as E8.2): "capture" (E8.2), "pump" (F8.2) and "death" (G8.2) are **one
world at three read horizons**. A captured-forever ship cannot die at the planet, so E8.2's
capture is transient too. The F8.2 death itself is real and stays on the page.

## Other adversarial cases (outside the author's range)

- **C12** (untested level inside the claimed L5–L15): captures (1−E = 3.98×10⁻¹⁰, apo
  2.42×10⁹ SAFE, 0 refusals, capcoast alive) — but clock relerr **5.7×10⁻¹¹**, above the
  claimed ≤ 2.4×10⁻¹¹; the clock bound is a 4-level sample, not a property of the range.
- **E11.3** (held key at L11, not just L8): crosses and flips (capture observed at
  240,045,125) — with the transient caveat above.

## Novelty

The live page (commit cb16ccb9, the parent run) holds "the downward E→1 crossing in flight is
unreachable by a held key; … stays unmeasured"; docs/HISTORY.md has no seam retirement. The
retirement, the letter-refutation, the transient mechanism, and the planet-crossing silent
death are all new. Not a repetition.

## The page

Corrected in place (the author's overstatements): the seam bullet now carries the transient
(uncut held keys re-flip and pump out; C/T cut after the flip — the arrival needs the timed
cut); the "canonical outcome depends on the settle schedule (open defect)" bullet is replaced
by the one-world control with the bit-identity numbers; the two Refuted entries no longer say
"the pump is schedule-dependent"/"the ladder, not the key" (the pump is the law under a held
key; the ladder hid the transient); Open direction 1 is now the playability consequence plus
the probe rule (never exit on the first family flip); Domain records my extensions; the Runs
entry graded. No three-gold agreement — topic stays open.

## Goal fit

Closes the board's #1 topic's named hole with the gold-grade answer (measured, safe, nothing
to fix in the engine). PRINCIPLES: #2 "'Exact' means deterministic and reproducible" — the
engine upheld it; the probe did not; #10 "Measure before claiming" — the parent's held-key
sentence was one sampler's view; #34 "the oracles are guards, not shepherds". Not a 10× mover
(the author concedes this); its value is the closed seam plus a corrected wrong sentence.

## Why silver, and the one experiment for gold

The experimental work is real, reproduced and pre-registered, and the seam retirement is
adoptable as-is. But the run's central *new* claim — the schedule-dependent canonical outcome,
a Truth violation — is refuted by the control above, and the dossier's E8.x table presents
transient captures as end-states ("end in different canonical states"). A run that reports a
false engine defect on the most sensitive axis cannot be gold. The gold-making experiment was
the same-tick control; I ran it, and it inverted the claim. The next run on this topic takes
the corrected record now on the page (or the playability question of the timed cut); a
re-flown dossier with the transient documented and the defect claim dropped, plus one more
regime (a second scene's arrival angle through the turn tier), is what gold would look like.

## What the author missed

1. The control was one `return` away: `held_trace` exiting at the flip made "different
   canonical states" a comparison of different horizons, not different worlds.
2. The E8.2/F8.2 identity (same relight; G8.2's death at F8.2's exact event_time) was already
   in reach of the shipped modes.
3. The mechanism was readable off G's own trace (the err jump = the periapsis velocity flip
   turning the brake into an accelerator).
4. "Every throttle level L5–L15" overstates a 4-level sample (L12: clock 5.7×10⁻¹¹).
5. "E constant to the printed digit": true for E at 9 digits; the printed E−1 moves at L15
   (−3.819 → −3.821×10⁻¹⁰) — immaterial, but the sentence overstates.
6. The `held dt = 2^0x100000 … (log2 = 20)` print formats the value, not the log — cosmetic.

Attack outputs: `/tmp/xcheck/{X8.3,G8.1,G8.2,C12,E11.3}.txt`; probe = `crossing.rs` + mode X
(continuation without early exit, G's tick list); commands as in regen.sh with
`--example xcheck`. Page corrections are in `wiki/high-gamma-clock.md` in this folder.
