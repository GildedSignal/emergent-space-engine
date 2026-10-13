Grade: gold

Checker2, blind: every load-bearing number reproduces on a clean tree. Both write points of the
one-word acceleration readout fail the three frozen motion gates — kick-written 5.07e-2
across-boundary velocity jump, boundary-written 3.85e-2 (bound 1e-4), map-ratio 356x (bound 3x);
clock gates pass; digests bit-identical on plane and strong-field scenes (the strong-field control
supplied by checker2); on the plane the free word is hours stale, err 8.3e-5 = 40% of the term.
The deletion is worth 1.45–1.51x on the gather (four interleaved rounds). 549f's readout premise
is dead: the mid evaluation is load-bearing. Correction: the r=20M scene never clock-steps the
ship (k.clock false at every frame, r=4000 too), so that half measures no readout; page fixed in
place. Adopt: strike 549f's open direction 1; nothing to merge.

## Reasons

**Reproduction (independent, clean tree + work/patch.diff applied by me).**
- Gates, v2 (the patch as shipped): the same three failures —
  `the_readout_at_a_boundary…` ("across a boundary 3.05e-6 of the radius and 3.85e-2 of the
  velocity"; frozen bounds 5e-7 / 1e-4 at motion.rs:526–527), `the_readout_between_kicks_reads_
  the_boundarys_error` ("worst readout 1.45e-4 (raw tube 4.56e-4); worst ratio to the map's error
  356.07x"), `the_readout_error_falls_as_the_step_squared`; clock tests pass. Exact match to the
  dossier and regen.log.
- Gates, v1 (kick write only — **not covered by regen.sh**): I rebuilt v1 by stripping the
  `boundary_clock` refresh hunk: jump 5.07e-2, same three failures. The dossier's v1 number is
  real.
- Digest identity: I built both sides myself from the pristine tree. Plane flights
  (2437d7b2…, c4d3c2e8…, 9d4748f1…) identical wired vs pristine; instrument control reads err
  exactly 0.000e0 on all three flights. **Strong-field control the author omitted**: pristine-tree
  word_strong gives 57d16273… (r=20) and 6bb30c1b… (r=4000), bit-identical to the wired run, with
  identical event counts (4,345,751 / 634,453). The wiring never moves the law.
- Bench: my own fourth interleaved round — base 25,744/12,666 vs wired 17,226/8,761 ns/emitter
  (1.49x scratch, 1.45x memo), inside the author's ranges; regen.log's three rounds agree.
- Staleness arithmetic: err max 8.280e-5 / term max 2.034e-4 = 40.7%; vs the census's 3.031e-9 =
  2.7e4x. Multiplicity 480 reads/window on coast and held-L8, median 2 on the dive (regen.log).

**A finding of mine that strengthens the refutation beyond the dossier.** v1 and v2 give a
bit-identical map-ratio (356.07x) while the across-boundary jump differs (5.07e-2 vs 3.85e-2): the
freshest possible word still jumps at every handover. The continuity break is structural to any
window-constant word, not a staleness effect — the gates freeze a continuity class the word cannot
represent at any write point. That closes the "fresher write" escape route the dossier left open.

**Adversarial case that corrects the run (the one the author left undiagnosed).** I instrumented
word_strong to print the ship's `k.clock`, `k.len`, `tau` and the gate decision per frame. At
r = 4000 M — and by identical construction at r = 20 M — **`k.clock` is false at every sampled
frame (0…11, 240, 479)**: the ship never runs a fictitious clock in this scene at any radius, so
the probe bails at `if !k.clock` and the 0 gated reads never consult the read gate. The dossier's
mechanism ("the read gate rejects every frame-cadence read", "the clock's steps collapse at
r = 20 M", P4 "they collapse by 1e5x") is wrong: there are no clock steps to collapse and no gate
decisions to reject; the ~3e6 events/orbit are non-clock events. The author disclosed the
diagnosis as incomplete and printed the anomalous weak control, but the dossier claim and the wiki
page asserted the gate mechanism anyway. Measurements stand (survival, event counts, digests); the
strong-field readout question is **untested**, not answered — a clock-stepped strong-field scene
was never built. I corrected the page in place (Current best, third Refuted bullet,
Contradictions, Runs line).

**Predictions.** predictions.md (13:27) precedes the decisive v2 runs (~13:28+) and discloses run
order; v1's gate outcome is disclosed as already measured, not predicted. P1 failed as
pre-registered — and its own kill clause ("then the stored word cannot serve the readout at any
write point") is exactly the reported refutation; the author led with it. P2 and P5 held; P3
half-held with honest accounting (1.45x vs 40–60%; 480 vs 2–6); P4's outcome was real but its
reported mechanism (collapse) is wrong per my diagnostic.

**Novelty.** view.md and a-word.md show the lineage: 7b86 priced the slot, 549f priced the word
and proposed the wiring as open direction 1; no prior run wired it against the frozen gates. The
memo-hit artifact of 5 October is a different mechanism (re-timed pending kicks). This is the
integrator-named gold experiment, run to its answer, not a repetition.

**Goal fit.** Kills a proposed representation on frozen gates before anything was built on it —
PRINCIPLES 9 ("a failed experiment kills that configuration, never the method": the two-word
(a, ȧ) successor is named with its price) and 2 (behaviours, not error size: the census's
magnitude metric missed the continuity behaviour the gates freeze). Redirects the shared
view/gravity-news/frame-cost slot to its surviving consumer. The 1.45x and the amortization are
now the standing price for any variant that passes.

**Minor (not grade-affecting).** The claim section says windows are "2.8e9 ticks ≈ 7.7 h" where
the evidence says len = 5.6e9 ticks (≈ 7.7 h is right for 5.6e9 at ~2.03e5 ticks per doll-t);
regen.txt in the run folder holds only the runner's exit status, the full log is regen.log.

## What the author missed

1. The strong-field mechanism: one 60-s diagnostic (print `k.clock` per frame) separates
   non-clock bindings from the gate; the author's own weak control already showed the anomaly
   (0 reads at r = 4000, which has nothing to do with strong field) and the separation was not
   made before writing "the read gate rejects every frame-cadence read" into the dossier and the
   page.
2. The v1/v2 identical map-ratio (356.07x both) is the strongest single fact in the run — it
   proves the break is structural, killing all fresher-write variants at once — and the dossier
   does not use it.
3. The strong-field digest control (pristine-tree word_strong) was never run; I supplied it.
4. A clock-stepped strong-field scene (the actual question 7b86 left: "a strong-field consumer
   that needs a accurately") remains unbuilt — that is the natural next run on this topic, with
   the two-word completion as its candidate.
