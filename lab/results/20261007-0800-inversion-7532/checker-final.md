Working...
Check complete. `lab/results/20261007-0800-inversion-7532/check.md` written — **Grade: silver**.

**Reproduction (exact).** Built and reran the harness from the dossier's commands (empty patch, public crate API only, 119 s, < 200 MB): `fleet-out.jsonl` identical except the timing field; `events.csv` md5-identical; every dossier number matches, including the D cross-type ranks re-derived from the raw rows (fleet-fleet 1/0.5%, fleet-belt 8/73.7%) and 87.3% = 9427/10796. Predictions genuinely pre-registered (08:06 vs outputs 08:14).

**Why not gold — the headline is a definition artifact.** The gold's branch is one `git show` away in this repo; its own pre-registration defines rank "**by current distance, min of both directions**", and its blind second checker already held r_max ≤ 4 at e-spread 1000×ρ with a true-longitude instrument. I rebuilt the author's exact scenes (same seeds, same `truth_pair`) and re-ranked at closest approach: **distance rank and true-longitude rank are med 0 with 0.000% > 4 at σ_e = 0.02 and 0.05** — the 60–88% misses exist only in mean-longitude order, the very axis the gold's dossier diagnosed as blind (lesson 6). The A-control couldn't expose this: at e≈0 all three orderings coincide.

**What survives, definition-robust:** the shear break (one-orbit-stale *distance* watch misses 1.2% tight / 44.7% loose — the rebuild rate the gold's O(n·k) claim omitted and its checker called unmeasured) and the routing hole (87.3% fleet×belt, rank-independent). The gold-making experiment: build the gold's actual k-nearest-distance watch with rebuild-on-overtake and measure misses + rebuilds across the σ_e sweep, shear scene and bath; my numbers predict zero misses everywhere, so the correction lands on routing + churn-scaled rebuild, and the "element coherence gates misses" condition dies.

Folder state: only `check.md` added; scratch in `/tmp` removed; no git commands beyond read-only `show`/`ls-tree`.
