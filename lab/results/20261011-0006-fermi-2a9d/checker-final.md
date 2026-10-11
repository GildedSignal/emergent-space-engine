Grade: silvCheck complete. `Grade: silver` — written to `lab/results/20261011-0006-fermi-2a9d/check.md`.

**Reproduction (all clean, in /tmp sandbox):**
- `budget.py` → exact match with `budget-out.txt`
- `sweep.py` → bit-for-bit match with `sweep.json` (6.08/5.64/4.76/3.76 bits)
- `h_live.py` main run → bit-for-bit, 14/14 checkpoints plus all summary entropies (`H_delta = 2.10479…`)
- `patch.diff` empty; predictions.md (00:15) predates all outputs (00:29+); the two failed prediction constants' corrected arithmetic verified from the author's own points (330 predicted vs ~335 measured crossing)
- All three repo claims verified: law.md line 13 ("+62 bits per kick and −60 per reabsorption"), `program.rs:284` return-to-base-only reabsorption, `shelf.rs::compact` repack-without-deleting

**Adversarial breaks (3 cases run):**
1. **Realistic 1/b² encounter tail** (same median jump, E[Δ²]=6.6×10⁶ vs author's 10⁴): slope steepens from 0.5 to ~1.36 bits/doubling (max-jump-dominated pre-asymptotics); the 16-bit deadline moves from 1.2×10⁷ to ~10⁴ orbits — the "decision is not urgent" verdict inverts.
2. **Fleet formation (their named kill case)**: does *not* break the quantile floor (2.85 bits at m=4096) — but the label term sits flat at 12.7 bits, above the frozen scar throughout.
3. **Totals from the author's own raw points**: re-fit total (residual+label) ≥ frozen total at every t and both densities (17.1 vs 10.8 bits at t=8192; 15.3 vs 8.2 at λ=32, exactly scar+log₂32). The headline "bounded iff re-fit" is refuted by its own data — boundedness needs canonical relabelling of unobserved bodies, an undecided law point, and the budget table's 4.34-vs-7.75 GB contrast pits entropy coding against fixed-width records rather than re-fit against frozen.

**What stands:** first H_live measurement (board: "not measured yet"); the +62-bits line corrected to record cost with true birth ≈ log₂(4.13σ) ≈ 2.1 bits/kick; the m-sweep resolution-vs-information methodology; the shipmem mechanism gap. Gold is one experiment away: the totals comparison (re-fit + relabelling vs entropy-coded frozen) under the 1/b² tail.
