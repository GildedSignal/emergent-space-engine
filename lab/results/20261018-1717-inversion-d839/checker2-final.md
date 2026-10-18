Working...
Check complete. Summary of the second-checker verdict on `20261018-1717-inversion-d839`:

**Grade: silver** — written to `check2.md`, with my arms folded into the run's `wiki/nladder.md`; tree restored pristine; no commits.

**What I did:**
- **Reproduced**: verified every dossier number against the runner's regen log (waves 13.5–14.5k/27.5–28.5k/41–43.5k; RSS 148→149 and 477→479 through kick₂; kicks 131,047/271,047; catalogue constant; counters bit-identical). Applied `work/patch.diff` myself — print-only, as claimed. Both code-mechanism claims are verbatim in the shipped tree (`universe.rs:1248` prune horizon, `fleet.rs:169` kick-mid/boundary-end).
- **Predictions**: pre-registered before the flights; P2–P5 held, P1 wrong in kind and honestly reported (it fixed the record's "next kick at ~2×" misreading: the step is ~27.6k gs).
- **Three adversarial arms, all outside the author's grid**:
  1. 3×10⁴ coast → **75,898 gs** — crosses boundary₂ *and* the third kick wave: RSS +1 MB, bpb back to 1,417, catalogue constant. The author's "[inference beyond two waves]" is now flown through five belt-wide waves.
  2. **3×10⁵** (next decade) — same 2.0× build-to-steady, ~5.0 KB/body steady: the per-body constant carries up.
  3. **Burn 3×10⁴/45.5k** (the author's named-unflown arm) — per-body terms hold (bpb 1,477), but resident memory ratchets 150→571 MB in the mint channel (2403's law): the coast scope is load-bearing.

**Why silver, not gold**: the run *secures* the wall (4 GiB at 1.7×10⁶) rather than moving it; the "~11×" rate correction is convention-dependent (same-N it's ~7.4×; order and mechanism unambiguous); and the headline needs the checker's burn arm to be safe from misreading. The gold experiment — burn through ≥2 steps at ladder scale — was flyable inside the author's own budget (~20 s wall, 571 MB).
