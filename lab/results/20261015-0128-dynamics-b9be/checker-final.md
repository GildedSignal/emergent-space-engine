Working...
Check complete. Final state:

**Grade: silver** (`check.md`, first line exact; 119-word abstract).

**What I did:**

1. **Reproduced exactly.** Independent re-aggregation of all four arms matches every dossier number (classes 54/90/0, 54/90/0, 54/42/48, 50/62/32). My own probe — a separate driver through the same public `build_scene`/`settle`/`alive` boundary — re-ran the full plane arm and reproduced **the identical 48 dead ICs**, with exact death epochs (10.75, 12.0 P) matching the author's 16 P trace. The author's disclosed `aggregate.py` loader fix touches no data path.

2. **Ran the author's deferred deciding experiment, oracle side.** Periapsis-resolved (P/256) oracle over both surfaces — outside the author's tested range: ensemble min **2.89 Rp** (the P/8 sampling missed 10×), yet **zero** oracle trajectories enter the planet or approach the star (min 300 star radii — a flank the author never measured, since the plane also kills at the star). No plane death stands for a real surface hit; the false-death reading survives.

3. **Attributed the deaths.** All 48: `fault=None, refusals=0, handoffs=0`, trajectories never (at P/8) within 46 Rp of the planet or 315 star radii of the star. Rules out handoff, refusal/error, and the system edge; leaves planned-terminal vs unsampled contact open — the one experiment from silver to gold.

4. **Composition correction.** The dossier's 2.5× max-dwell p50 gap is a composition effect; on the same 96 surviving ICs plane vs oracle quantiles are **identical** (13.00/13.00, 512.12/512.12) — preservation is stronger than claimed.

5. **Corrected the page in place:** "1/3 of the chaotic-layer ensemble" → 48/144 of the ensemble (41/48 outer, 7 inside — the concentration claim was 75%, not all); conjunction claim scoped to its two traced deaths; checker evidence folded in; open direction 1 narrowed to the plane-side branch; grade recorded.

Tree restored clean (`git status`: only untracked `lab/results/`); no commits, nothing else in the run folder touched.
