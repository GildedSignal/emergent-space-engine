Working...
Check complete. `Grade: lead` written to `lab/results/20261016-2138-inversion-58be/check.md`; the author's wiki page corrected in place; tree left clean (patch reverted).

**Verdict, in brief:**

- **Reproduction: clean.** regen exits 0; deterministic columns bit-exact (kicks 496,161; boundaries 449,317; catalogue 100,076; wave 13,234–14,900); plateau 4,753 vs. dossier's 4,754.
- **Novelty is the kill.** The premise "the wall had no flight behind it" is false: **b30b** (20261014-2248) flew the plateau — 4.85–5.06 kB/B, slope 0.00 B/B/wave over waves 2–4, N up to 2×10⁵, both seeds, the same 3.4× dashboard under-report — and **7dc6** held 25 wave periods (700k game-s) flat. The letter's own sentence on the nladder page names "b30b's 4.85–5.06 kB/B plateau" as its constant. This run re-derives it at rtf 100; a repetition, not a new best.
- **Adversarial cases:** coast holds everywhere I pushed it — seed 3 (4,750 B/B) and N=3×10⁵ (4,737 B/B, outside the author's range). But the **burn arm — a flag wired into the author's own `memwalk` and left unflown — grows monotonically**: 5,043 → 19,430 B/B over 40k game-s (~57× the author's own kill criterion), `held` climbing 0→117. "No grower in any reachable channel" (author-final) is refuted by the author's own tool; 625b already knew the class.
- **A log-contradicted number:** the dossier's "1.68×10⁻⁵ kicks/B/game-s confirmed in flight" matches neither its own raw (four crests at ~14k/42k/70k/~95k, ~28k spacing, all-body rate 5.049×10⁻⁵), nor the page's identity (2⁷/P_Cinder = 3.32×10⁻⁵), nor b30b's decomposition (3.48×10⁻⁵ belt + 1.54/s baseline).
- **Worth keeping:** the `nladder` Linux footprint port (unblocks ladder flights on the lab machines), the 400-member battle-dissolution narrowing of d3fe, and the N=0 churn saturation — all named in check.md as the adoptable residue.
