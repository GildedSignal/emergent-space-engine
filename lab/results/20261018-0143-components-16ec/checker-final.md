Working...
Check complete. Summary of what I did and found:

**Reproduction** (regen + my own runs off the patched binaries): coast digest `a725217f1dcd9f2a` identical across control/rerun/fast at 19,423/19,423 skipped; seed-7 identical; probe 1,204 bindings, zero excursions, 4 passages refused; 4.5–5.2 µs → 0.22–0.25 µs per event. All headline numbers regenerate.

**Decisive adversarial finding — the burn "kill" is an instrument artifact.** Two flag-off burn controls flown back to back give different digests (`d9d0a2aa…` vs `bbd72d20…`; the author's `08b6399c…` and the regen's `d12096fd…` are two more). Mechanism in the code: nladder injects the thrust at `p.u.input(p.u.now, …)` at frame 60, and `p.u.now` is the *presented* tick, which drifts with the 12 ms budget on this shared box. Coast has no input, so its digest is schedule-independent — exactly what reproduces bit-for-bit. The author's ctl-vs-fast kick delta (90) sits far inside the ctl-vs-ctl spread (1,027). Also: on burn, the fast path skipped only the belt's 19,423 boundaries (all 340 player passages were read out in both arms), so it has no channel to move the burn digest. My two attempts to repair the instrument failed instructively (future-tick pin stalls past the 90 s timeout; tick-0 pin is silently ignored) — the named fix is injecting at the player's next planned kick.

**Second correction:** the decomposition numbers 10.2% / 84.6% / 190,000 items / "8×" regenerate from no shipped output; from the evidence the split is ≤18% clock / ≥82% WH (≥4.4×). Direction of the correction to 3570 stands. Page corrected in place (headline, body, runs entry).

**Grade: gold** — 3570's named gold experiment, flown and reproduced exactly, a genuine exact deletion (flag-gated ~10 lines, no new state), with the burn caution resolved as a harness defect rather than a method failure. `check.md` written; tree left pristine; nothing else in the run folder touched.
