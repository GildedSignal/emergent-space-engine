Working...
Check complete. **Grade: gold** — written to `lab/results/20261009-0709-second-20261009-0621-system-7f97-1eca/check.md`; tree restored (only untracked `lab/results/` remains); nothing else in the run folder touched.

**What reproduced bit-exactly from `work/patch.diff`:**
- Control digest `21c73edc…` (P6); B13 split = shipped text-identical, 60/64, and PLANE_TRACE stderr byte-identical to the author's `trace-split-v3.txt`.
- B17 split: PASS, pump [0.984396, 1.001103], libration 0.981, 34/34, 5/5 — same numbers, same 35.5 s.
- B12 shipped/split: identical text, 44 same replaced draws.
- Belts: 78385→16732 (4.68×) and 78094→10032 (7.79×), digests matching and deterministic on rerun.
- The contrast the claim rests on: uniform-4 cut → B13 **3/64** (reproduced).

**My attacks:** high-e belt (e ≤ 0.5) crossing Giant's band — no losses, deterministic, saving honestly shrinks to 3.0×; env-interaction probe clean; code audit (`constants` has one caller, axis formula mirrors shipped `source()`, power-of-two floor commutes with the shift); unit tests 29/29.

**Defects found (named in check.md, not demoting):** the dossier's split bench digest `bb81ae6e…` does not regenerate — v3 gives `fea07ab3…` (deterministic; the recorded file is a v1-era artifact cited as final); kick-bench absolute counts are load-dependent (the within-session shipped↔split identity does hold); the v1/v2 falsifications are single-harness records, though internally a clean A/B for the ratchet.

**Why gold despite that:** every load-bearing number regenerates; the stale one sits on the scene the dossier itself proves blind; the run deletes the doll-wide Δs constant, corrects a premise (cadence may only refine — measured twice), and is adoptable in one step behind a default-off flag whose off-state is the shipped bits.
