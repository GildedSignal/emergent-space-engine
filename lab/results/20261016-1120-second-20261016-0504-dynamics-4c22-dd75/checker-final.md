Working...
Check complete. Summary of what I did and found:

**Grade: gold** — written to `check.md` with abstract, reasons, and corrections.

**Reproduction (independent of the author's harness):**
- Applied `work/patch.diff` to a pristine tree myself, built myself; diffed against the original run's patch on its branch — the original declared `attribs` twice and pushed `take()` twice per frame (original data: 198 attributed rows, all even frames), this patch has exactly one of each; `step.rs`/`universe.rs` law bytes identical to the original run's.
- Re-parsed every raw row file with my own parser: every dossier number holds — worst-12 (217.1: d2+d3 211.0 = 97.2%, d0 0.0, residue 6.1), frame 3173 attsum = 334 (100%), whole flight 23,690/19,702 (83.2%) with d2 k9,824/b9,711/c24 + d3 143, stag/phase/N=0/20-s splits all exact, d0 zero in all 8 files, both parities attributed.
- Digests for all three arms identical to the original run's stored record (only wall-times differ). My own re-flight reproduces the stored event and attribution columns exactly.

**Adversarial (mine):** 120-s horizon — holds stronger (98.8%, plus a new pure-boundary beat at exactly 2×3173); **burn** — the 328-event storm stays one-doll-dominated (72.7%) but the residue is 27% and **d0 carries 40 events**: the 97%/d0-zero letter is coast-scoped (dossier scoped it honestly; the page did not).

**Page defects corrected in place:** the author's conflict resolution had deleted three sibling runs (components-4534's grid-translate lever, c840's B13 kill of the armed stagger, system-e070's isolation control) — paragraphs and append-only Runs entries. Restored, and the composition claim scoped to coast with the burn numbers.

Tree left pristine; only `check.md` and `wiki/nladder.md` in the run folder touched.
