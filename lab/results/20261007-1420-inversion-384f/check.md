Grade: silver

**Abstract.** Claim: the gold's phase-neighbour certificate silently drops all encounters under two other concentration topologies (crossing lanes 247/247, pericentre funnel 413/413 cross-recall 0.000 — structural, reproduced exactly), while the window tier it replaces is forced quadratic by orbit-path intersection alone (candidates exactly C(N,2), ×4.01 per fleet doubling at fixed linear density, bit-for-bit); the repair ranks bodies by arrival time at the orbit-intersection locus (funnel k8 1.000, fresh crossing seeds k8 0.995–1.000). But the gold's own dossier scopes its train to the Binet-clump regime via a regime switch — S2/S3 route to the pairwise tier there (quadratic, not silent drops), so the kill lands on the board's routing summary, as the author concedes. Evidence defects: stored s3.json is empty, the "1.000 fine-seeded" and "0.993 at k=4" numbers do not regenerate (shipped code: 0.8866/0.983), and `invert.py s3` takes 458 s, not "~10 s". One experiment short.

## Reproduction (clean tree, no patch to apply; shared runner, load 0.9–1.8, each process ≪ 2 GB)

- `python3 invert.py s1`: 393 encounters, phase-rank 0.964 (k8 1.000), window 28,680 = 73/enc, conc 48.7× — matches the dossier row exactly (no stored artifact existed).
- `s2`: identical to s2.json on every recall (cross 0.000, internal 0.9855, 79,800 cand = 121/enc, coarse locus cross 0.1012); checks 2257 vs stored 2258 (one pair; recalls identical at 4 decimals).
- `s2scale`: **all 72 counted fields identical** — 270/601/1204 encounters, candidates 19,900/79,800/319,600 (×4.010, ×4.005), 74→133→265 cand/enc, cross recall 0.000 at all n. Only wall-times differ.
- `s2fine`: identical to s2fine.json — cross 0.8866 (k4), total 0.9667 (k8), union 0.9485, 3,009 checks. Note: this contradicts the dossier's table ("1.000 (fine-seeded run)") and claim line; the 1.000/6,391-checks figure came from an earlier script version preserved nowhere (patch.diff is 0 B, folder untracked).
- `s3`: stored s3.json is **empty**. The shipped command does regenerate the row — 413 truth, 55 checks / cross recall 0.000, 12,720 = C(160,2), locus 2,886 checks, k4 **0.983** (dossier says 0.993), k8 1.000, conc 125.7×, mgf 0.019 — but in **458 s**, not the claimed ~10 s (862 locus clusters × per-body golden-section refinement); the author's own final rerun evidently never finished either.
- Truth instrument validated: an independent dense O(N²) brute force (fixed upper-triangle extraction) returns the **set-identical** 413 on S3.

## Predictions

`predictions.md` mtime precedes every decisive artifact (46 min before s2scale, ~40 before s2/s2fine/s3); content shows genuine pre-registration (P1 cand/enc > 300 vs measured 121; P3 > 200 vs 31 — both honestly reported as misses). P1/P2/P3/P5 held; P4 partially held and is honestly qualified — but the table and claim line still cite the unregenerable 1.000. Kill criteria for the attack: not triggered (0.000 cross recall stands).

## My attacks

1. **Seed robustness (S2 seeds 12, 23, correct 2-group element grouping):** phase-rank cross recall 0.000 both (structural); fine-gate locus cross recall k8 0.995 / 1.000 — the repair is real and seed-robust at k8, but k4 sits at 0.846–0.878, so the P4 "≥ 0.95 at k=4" target does not generalize beyond seed 11.
2. **Congestion extreme on the funnel** (tspan 0.03 → 2,735 encounters, phase-rank still 55 checks / 0.000): my independent exact-arrival rank at the one true locus gives **k4 0.22 / k8 0.40** — the fixed-k certificate collapses under jams; k must scale with flux density. Diffuse (tspan 3.0): 1.000 at k4. n=320: 0.63/0.92. "The same O(n·k) trick with k=4 covers all three topologies" overreaches.
3. **No grouping rescues phase rank on the funnel:** forcing all 160 bodies into one orbit group gives recall ≤ 0.24 even at k8 — the miss is not an artifact of the element tolerances.
4. **Truth adjudication** (above): the recall denominators are exact; my first sweep claiming 986 was my own bug (self-pairs from a zeroed triangle), retracted after ultra-fine arbitration.

## Novelty

docs/HISTORY.md, git log, the gold (8d339c5) and q-candidate-degree (eaac72b) contain no locus/arrival-time work. The gold's own dossier already scopes its train to "when a cell's clump number (max pairwise Binet distance / eps_u) ≤ 1" — i.e. shared-orbit concentration — and keeps the pairwise tier elsewhere; the board's taste log ("replaces the quadratic tier, triggered by a dimensionless number") is the summary this run breaks. The new content that survives: two measured topologies outside q-candidate-degree's belt domain where the geometric candidate tier is exactly C(N,2) at fixed density (its "answered for fixed density" was dilution-only), and the arrival-time-at-locus rank as the general certificate form (formation = degenerate locus) — same trick as the Binet-cone Diophantine work's regime question, different mechanism.

## Goal fit

Board risk #1 (candidate work must track real encounters) and a correction to an adopted gold's routing rule; PRINCIPLES #13 "errors never compound — a dropped encounter is not an error, it is a lost event" and #32. The author honestly flags that the frequency of lanes/funnels in the actual game is unmeasured (argued from the goal, not from scenes).

## The experiment that would make it gold

The author's own named one, done certificate-grade: replace the sampling-tolerant locus gate with exact orbit-pair curve intersections (the funnel's locus is exactly the shared pericentre; the lanes' are the two nodes), ship it in `invert.py` regenerable ≤ 60 s (my exact single-locus arrival rank already runs in milliseconds and gives k8 0.998–1.000 across seeds and the default funnel), and measure k against flux density (the jam case needs k ≫ 4) — pre-registered, with `s3.json` actually stored.

## What the author missed

- The decisive S3 artifact was never stored and the S3 command runs 45× over its stated time; a checker following the dossier's commands verbatim (60 s budget) would grade the run's second headline unreproduced.
- The table's "1.000 (fine-seeded run)" is contradicted by the run's own s2fine.json (0.8866/0.9667); P4's prose is honest, the headline is not.
- The k=4 form of the repair fails congestion extremes (0.22 under a jam) — "O(n·k) at the gold's rank" was tested only at one congestion level.
- The attack's framing ("silently drops every encounter") targets the board's summary; under the gold's actual Binet-clump switch those scenes route to the pairwise tier (quadratic, no drops) — the run's value is the routing correction plus the new topologies, not a kill of the gold's certificate in its own regime (S1 control confirms it works there: 0.964/1.000).
- `invert.py` was edited after all stored runs (mtime 4 min before the end, same instant as the empty s3 rerun) with no history to audit what changed; "see run history in git patch" points at an empty patch.diff.
