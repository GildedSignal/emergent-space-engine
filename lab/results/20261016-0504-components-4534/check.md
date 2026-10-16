Grade: silver

**Abstract.** The locals' standing storm (335 events/frame, N-flat 600–10⁵) is the shared block-step grid, not the shared clock begin. Reproduced bit-exact: BEGIN (the page's conjectured cure) leaves max 335 with the same storm frames; the per-body grid translate gives 141/129 flat in N (2.4×, seed 1) and 359→177 at held-out seed 7. Checker extensions hold: 176 at 10⁵×seed 7 and 143 at 3×10⁵ (storm and cure both N-flat); burn composes (p99 96→75 ms, the burn's own monster untouched); OFF equals a pristine-physics build column-for-column. Adoption blocked, as the author states: event totals +6/+73%, all of it fleet-battle slices, gates unflown, and the author's own >150 kill bar fired at seed 7. One named experiment from gold.

## Reasons

**Reproduction (clean tree, `git apply work/patch.diff`, fresh build).** Every deterministic column of the dossier's table reproduces exactly, twice (my flights and the runner's regen.log): OFF 600/1e4/1e5 seed 1 all 335/229/28, kicks 17,209, events 35,660, stats identical (bit-identical across N, as claimed); BEGIN 600 max 335, storm frames 317/634 unchanged, frame 79 → 290, events +26; GRID 600/1e4/1e5 141/131→129/52, kicks 17,257–17,260; seed 7: 359/244/51 → 177/168/114, events 45,277 → 78,254, slices 12,837 → 45,751. A GRID repeat is identical. The ms column is box-load and does not reproduce at the digit (regen's own worst OFF is 16.4 ms against the dossier's 12.9) — disclosed in the dossier ("orders of magnitude only"), and the deterministic columns carry the claim.

**Gate neutrality (P3).** Main's `nladder` example does not *link* on Linux at all (`proc_pid_rusage`), so P3's "pristine-main build" was never literally executable on this box. I flew the honest equivalent — main's `step.rs`/`universe.rs` byte-pristine plus the patch's print-only Linux port — and it reproduces the OFF arm's columns exactly at N=600 and 1e4 (335/229/28; 17,209; 35,660; storm frames 317/475/79). The claim stands; the dossier's "pre-patch binary" wording should have said this.

**Predictions.** P0, P1, P3 held. P2 half-held and the misses are named, including the seed-7 max 177 breaching the author's own pre-registered kill bar ("GRID leaves max > 150") — reported, not tuned away. Pre-registration is credible: predictions.md predates dossier.md/regen.sh by ~5 min of file times, and a post-hoc author would not have written a kill bar the result then fails. Residual record weakness: run.log is empty and no raw author logs are kept (the numbers regenerate, which the rules accept).

**Adversarial cases (mine; three, one beyond the flown domain).**
1. *10⁵ × seed 7* (outside the author's grid, which held seed 7 only at 600): OFF is bit-identical to N=600 seed 7 (359/244/51; 45,277) — the storm is N-flat on the held-out seed too; GRID lands at 176/170/115, events 78,536 (+73%), slices 46,029. Flattening and caveat both extend.
2. *N = 3×10⁵ seed 1* (3× the author's maximum): OFF columns bit-identical (335/229/28; 17,209; 35,660); GRID max 143, p99 130, kicks 17,256, events 37,939 — 2.34× cut, max events/frame flat in N (141→143). Peak RSS 748 MB, inside budget.
3. *Burn* (the author's named unflown risk): OFF p99 96.1 ms / max 305.2 ms / worst-event frame 719 (frame 60); GRID p99 75.4 / max 260.1 / 747 at the same frame. The lever composes — no refusals, no deaths, player alive, kicks +0.26% — softens the locals' storm frames (382→376 class), and correctly does nothing to the burn's own monster (a different population, per 6138/4487).
   Control: N=0 with GRID on is *not* N=0 OFF (max 60→47, kicks 2,382→2,380): the staggered class `doll != 0 && Ship` includes the plane's own doll≠0 ships, so the lever's class is broader than "the 300 locals" — unremarked in the dossier.

**Novelty.** The attacked letter is the standing wiki open direction 1 ("the same one-step first-kick spread … one law, one lever", ed3a dir 3 / 917c dir 1); BEGIN refutes it bit-exactly, and no prior run, wiki page or H entry translates the block-step grid per body. The begin-lock/grid-lock discrimination is new and measured on both sides (BEGIN null, GRID flattens), which is what makes it evidence rather than a story.

**Goal fit.** Board item 1 (the furthest gap): the locals' storm is the frame's binding N-independent term (917c's checker correction: the 12-ms letter extrapolates to ≈6×10⁵, locals-driven); this run halves that term and kills the conjectured free cure. PRINCIPLES #12 ("i care about the p95/99 results i want the game to be smooth") — max and p99 are what moved; #19 (a fix signals the wrong representation — the begin-stagger was the bandaid, the translate is on the law's own grid). Cost of adopting: ~30 lines, env-gated, OFF bit-identical — but not adoptable yet, and the author says so.

**The page.** Faithful: the current-best paragraph, the Refuted entry, the direction-1 annotation and the Runs entry all match the evidence; no overstatement found. I appended a checker block with my extensions and the two adoption notes.

## Why silver, not gold

Real, reproduced, and it corrects a standing premise — but the positive half is 2.0–2.4×, under the 10× bar; the refuted premise is the lab's own conjecture, not a shipped one; and the lever is not adoptable within one step (the author's own words), because the seed-7 event-total inflation is undiagnosed and the B13/B14-class legality gates are unflown. The pre-registered kill bar firing at seed 7 is itself grounds to withhold gold.

**The one experiment to gold:** diagnose the slice inflation under the shifted phases — my arithmetic shows it is exactly the fleet battle being advanced in more, smaller pieces (+32,914 of +32,977 events at seed 7 are slices; a slice is one `battle.run_to` advance, fleet.rs), so the next run should test whether a coarser offset lattice (per doll, or per octave) or a slice-merging rule removes it — then re-fly with the legality gates. If max ≤ ~150 holds at held-out seeds with totals within a few percent, the locals term is halved and adoptable: gold.

## What the author missed

- The inflation's mechanism is one reading away, not "undiagnosed": the growth is entirely `slices`, and a slice is the fleet battle's advance quantum — spreading event phases across frames multiplies the number of (smaller) advances. Named, this shrinks the gold step.
- The staggered class includes the plane's own doll≠0 ships (N=0 GRID ≠ N=0 OFF); the "locals" framing hides that the lever retimes the plane's own fleet machinery too.
- GRID gives up `aligned`'s cross-body invariant ("every pair shares boundaries") for arbitrary pairs — the doc-comment property that makes stubs realign. No consumer of the invariant was found in this pass, but it is a law-level change that belongs in "what would make it wrong", next to burn and gates.
- P3's "pristine-main build" control cannot exist on Linux (the example does not link); the honest control is main's physics plus the print-only port, and it passes.
- The dossier's worst-frame ms (12.9→6.7) understates this box's own regen (16.4→7.0); the ratio survives, the digits do not — ms should have been quoted as ratios only.
