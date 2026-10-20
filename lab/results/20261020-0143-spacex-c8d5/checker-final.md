Working...
Check complete. **Grade: silver** — written to `lab/results/20261020-0143-spacex-c8d5/check.md`, with the author's wiki page corrected in place where it overstated.

**What reproduced** (regen, exit 0, plus 4 adversarial arms of my own):
- Completeness is keep-independent everywhere: worst seen stock-equal in all 12 arms across both runs — 10,048/10,050 at N=10⁴, **30,048/30,050 at N=3×10⁴** (the scene predictions declared but the author never flew), 10,046 both at 184k game-s coast, 10,045/10,046 at 237–279k game-s burn. No dial-attributable loss at any depth, N, or staleness.
- The shipped-view defect is real and verified in code: `view.rs:202` (`eval(t)?`) aborts `crossing` on one None; `view.rs:339` drops the emitter for the whole gather. It **grows with depth** (2 → 4 → ~5 missing), keep-independent.
- The dial is arithmetically the shipped expression when unpinned, at both prune sites.

**What did not reproduce** (both stated as findings in the dossier):
- The −8% segment delete: regen coast flips to **+9%** (stock alone spans 2.16–2.41 body⁻¹ across runs); my coast and N=3×10⁴ arms read 0%. At one-wave depth the delete is zero inside noise.
- Burn nones ×22 (12→262): regen gives 183→0 — reversed. Noise.

**New, outside the author's range:** at ratchet-depth burn (`every=300`, ~40 s — the "unreachable in 60 s" claim was wrong) the halving is real (34.8→13.9 segments/body, RSS −45%, dashboard −53%) **but** one-leg pays None probes ×40 and ~18% slower frames. The keep is free at bench cadence, not at the depth where it pays — the exact experiment gap between this and gold: re-fly that arm with the missing ids logged and the None-clamp fix.
