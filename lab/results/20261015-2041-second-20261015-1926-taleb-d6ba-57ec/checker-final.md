Working...
Check complete. Summary of what I did and found:

**Grade: silver** (`check.md` written; the author's wiki page needed no correction).

**Reproduction — complete.** The runner's `regen.sh` (exit 0) regenerated every dossier number digit-for-digit, and I verified all four digest identities against the published record: belt-48k `f8b52855…` = d6ba's, 10⁵-48k `2109a2e0…` = 1d52's anchor, ctl-burn-20k `5caeb1b6…` = e0f9's anchor, comet-32k variant = ctl (`32ef5b00…`). All derived integers recompute (2,841 B/death, 6.64 promotes/demotion at 607 µs, 28.2 vs 0.196 kicks/ks, 22.2 kB/arc).

**Adversarial, three of my own on the frozen binary:**
1. **Belt 10³ @ 48k** (below the flown range): `pinned_total 86,944 B` byte-identical at a third N — the N-constant floor holds, killing both prior 10⁹ projections (~9 MB and ~9 GB) at once.
2. **Stargraze 100 @ 48k, seed 2**: the standing class is seed-stable — byte-identical 2,558,720 B store, kick-minted-live = 100, records 710.7/body.
3. **Stargraze 100 @ 96k** (the registered depth): killed by the box at ~1,430 s CPU — inconclusive; no surviving 96k record exists anywhere (the author's was deleted by their own cleanup).

**Why not gold:** P1 and P4 failed as registered, and P1's kill clause was written for 96k but fired early at 48k — the registered depth has never been observed. The one gold experiment: fly the 96k cut (plus mixed at its registered 10³) to completion; it has now been lost three times and needs babysitting.

**Also found (missed by the author):** the dead price is seed-dependent (seed 2: 4.2 kB/death vs 2,841 B), so the adoption sentence should price the class, not the seed-1 constant.

The tree is clean (only `lab/results/` untracked; my flight outputs live in `/tmp/check/`).
