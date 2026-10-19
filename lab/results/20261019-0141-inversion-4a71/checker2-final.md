Working...
Check complete. **Verdict: `Grade: gold`** — written to `lab/results/20261019-0141-inversion-4a71/check2.md`, blind to the first checker.

**What I did:**
- **Reproduced** from `work/patch.diff` in a clean tree: the deterministic core matches — pins 3.00/5.04 retained/body, RSS 281/383 MB, `now − oldest` = D to the digit, ctrl bpb 1,417. Timing digits (over-frames, ctrl max gap 1,655.1 vs 2,302.5) are elastic on the shared box and disclosed as such.
- **Three adversarial arms, all outside the author's grid** (`logs-check2/`):
  - **D=6×10¹⁰** (a decade past the author's largest pin): census climbs monotonically in play time, no saturation (1,564 → 148k retained, RSS 204→381 MB), and at equal elapsed equals the 1.2×10¹⁰ arm — the law is really 1 + ⌊min(D, elapsed)/27.6k gs⌋: unbounded in play time, the ratchet's strongest form.
  - **K=10³** (a rung below the grid): ratchet reproduced at 8.5× RSS; per-binding constant 2.3 KB — N-independent.
  - **Code mechanism**: verified the certificate's proof in shipped code (`deadline_of` = t + light distance; presented time = min deadline − 1) and the every-frame `prunable` walk (`at = droppable_until + keep < now` while pinned).
- **Novelty**: d839's own Open directions named this exact probe as unflown; no HISTORY entry. Genuine extension, corrects the standing current best's domain.
- **Page**: faithful fold-in; corrected one overstatement in place ("byte-identical no-op" → inert by mechanism `keep ≥ 2²⁶`, logs not byte-comparable) and appended my second-checker note to both `entry.md` and the built `nladder.md`.

**Main flaw found**: the `hist_max` held-out prediction (control ≤ ~2 vs measured 69) is a real miss filed only as an instrument note, and the staircase's correct form is linear in play time, not a function of D alone. Neither touches the claim. Tree restored to arrival state; nothing committed or pushed.
