Working...
Check complete. `check.md` written: **Grade: silver.**

**What held (reproduced + extended):**
- regen.sh re-run in a clean /tmp tree: every number byte-identical to the stored outputs. The target quote is verbatim in `docs/representation.md` thesis 2; novelty confirmed (no wiki page, no H entry, no rung tests trapping statistics vs an oracle).
- The decisive dwell arm is robust well outside the author's domain: K=1.0 → 9.6% permanent spurious traps (true 0%, noise 0.8%); K=1.4 → 38.7%; still 2.0% at Q=3×10⁻⁵ (a decade finer than swept); and the design's own r2 reading — only the kick quantized, exact integer momentum, x never rounded — still yields 3.1% permanent traps at Q=10⁻³. The "exact-native integers" defense fails at game-relevant Q.

**What fell:** the supporting "no shadow bound in the sea" arm. My cat-map control (Anosov ⇒ provably shadowable) shows the identical torus-scale decorrelation signature under the author's noise protocol — deviation-from-same-IC-reference measures mixing, not shadowing. Retired; the wiki page is corrected in place (twice over: it also asserted "actions preserved at O(Q)", never measured). The stronger argument the author missed: the dwell data itself shows the permanently-trapped quantized orbits are unshadowable — no sampled true orbit of the band survives past 1.7×10⁴.

**Silver, not gold:** half the headline claim retired, held-out predictions did not hold as a set (failures honestly reported), and the model→shipped-law gap remains. One experiment to gold: the dwell arm on `es-space-v2`'s dense order around a co-orbital island at engine Q, with a refinement-based shadow instrument replacing the noise test.

Minor record notes: the dossier's "2.25" isn't printed by the shipped code (regen median 2.28), contradicting author-final's "byte-identical"; `shadow_falsifier.py`'s own dwell arm is dead code (p50=0). All my processes stayed under 100 MB and ~2 min.
