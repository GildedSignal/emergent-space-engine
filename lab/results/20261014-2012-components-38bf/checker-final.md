Working...
Check complete. `check.md` written, the author's page corrected in place, tree restored to pristine.

## Verdict: **Grade: silver**

**What reproduced** (runner's regen + my 8 flights on the applied patch): every physics counter (kicks 225,949; encounters; decisions), the P1/P2 digest identity `c2b834bb…` (bf21's certificate re-derived independently), input cost 0.15–0.37 ms in every run, always ≤ 2 events resolved, max frame ≤ 12.7 ms against 1.3–1.9 s uncapped monsters.

**Adversarial cases (5, one outside the author's range):**
1. **The uncapped input control** — the one flight that tests "the exposure is real as a mechanism": it never fires. 0.154 ms at rtf 100, 0.158 ms at rtf 200, cap unset, even with the uncapped engine's frame monsters at 1.6 s. The scheduled pulls keep the ship lane tiled to the player's key, so `input` finds ≤ 2 due items regardless. The claim's *conclusion* (bounded, no deferral machinery) survives; its stated *basis* does not.
2. **The key-changing decision** (the run's own named untested arm): 0.20 ms at 2×10⁵; 657 of them every frame at 3×10⁵ hold max frame 11.97 ms. Open direction 0 is answered affirmatively.
3. **3×10⁵** (author tested 2×10⁵ only): 0.161 ms, 12.1 ms max, 1.38 GB RSS; the wave window is N-independent (`belt_first`).
4. **P4 repeat** (the author's own reproduction test): encounters +2, not the claimed "exactly one" — their criterion resolves to "the instrument is unstable at this margin."
5. **Digest stability**: the dossier's P3 digest never regenerated — three runs, three digests at the same frame; decision-bearing digests at the 16 k cut are wall-unstable (4487's direction 12), while counters stay fixed.

**Why not gold**: two quoted numbers cannot regenerate (P3 digest; "exactly one encounter"), the central mechanism claim was asserted from code reading rather than measured (and my control shows it doesn't manifest), `session.rs:118` doesn't exist in the tree, and prediction P4 failed (informatively, honestly reported). The gain is a de-risking of bf21's adoption plus a design-option deletion — real, novel (nobody had measured the input path; checker-2-bf21 named it the open exposure), and adoptable at zero cost — but the 118× monster kill is bf21's, re-derived. The gold-making experiment is named in `check.md` and already flown by this check.

**Page corrections**: "real as a mechanism" → bounded with or without the cap; "exactly one encounter" → +1 to +2 pace-dependent; Refuted entry rewritten; direction 0 marked answered; checker italics with all held-out numbers; run grades restored from the truncated merge tail the author's resolve script dropped (6138 silver, 7f99 gold, a2c1/0e37/effb/3071 silver).
