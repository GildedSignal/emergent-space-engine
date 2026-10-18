Working...
**Grade: gold** — written to `check2.md`.

**Reproduced independently:** applied `work/patch.diff` to the clean tree (the `--3way` fallback regen.sh records is real), built, flew. The OFF control matched bit-for-bit across all three executions (author flights, runner regen, my build): digest `4916c14e0273…`, kicks 34,585, over 68, 75 beats at gaps {8,9}. SECULAR, composed (both scales) and the Table-3 pair all bit-identical; the 6.2× starvation row reproduces (game_s 143.7 vs 898.6, every frame pinned at 11.9 ms).

**My adversarial cases (beyond the author's and the first checker's):**
- **Fat-tailed formation** (±20% in a, 10× e scale — the dossier's own named untested shape): OFF still ruined (max 893/over 68), composed still cures (max 30/over 0/kicks 611). Transfer is not a thin-shape artifact.
- **Seed 2**: cure holds (max 26/over 0/game_s 899.2).
- **2× horizon at 10⁴**: composed flat, no decay (max 31, game_s 1,898.5).
- **K=5×10⁴** (next decade): delete stays N-flat (kicks 539, max_ev 28) but the frame budget breaks (over 32, game_s 750) — the scan channel, not the comb, binds beyond 10⁴; confirms the page's bounding extension independently.

**Blemish named:** the dossier's "every formation-scene number bit-identical" is false for the CHAIN+STAGGER rows (deadline-coupled: kicks 44,207→44,210 / 70,257→69,889, digests move between executions) — disclosed in fix-final and corrected on the page, but the dossier text still overstates. Conclusions unaffected.

The proposed page needed no further correction: every checkable line matches my evidence, and the 5×10⁴ bound is already folded in. My probes (`ES_SEED`, `ES_FAT` in scanprobe/scenario) remain as checker edits for the snapshot.
