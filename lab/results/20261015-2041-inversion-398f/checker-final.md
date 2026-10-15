Working...
**Grade: gold** — written to `lab/results/20261015-2041-inversion-398f/check.md`; scratch tree removed, run folder otherwise untouched.

What I did, and what held:

- **Reproduction.** Clean clone at the run's base `abfebaa0`, patch applies (8b89 verbatim + the read-only `history_census`); the runner's regen numbers all reconcile with the flights, and the anchor digest `5e8c9e24…5fbab6f` reproduced bit-exact in my own tree.
- **Mechanism from source, not story.** `key_prune` keeps `2·light_distance + 2²⁶`; the scene's own print puts comets at ~10⁴ AU (1 AU ≈ 1.013e8 units, r0 1.037e12), giving a ~10⁷ game-s retention horizon — the prune provably cannot fire at any flown cut, while the belt's ~2.8k game-s horizon drains each settle. The class law is the light cone's.
- **Four adversarials beyond the author's domain, all confirming:** belt 192k (2× deepest flown) reads 1.039 seg/body, rss 49 MB, ctl==all digests; comet seed 7 (never flown) lands within 0.2% of seed 3 with the same 1.99× doubling; the untested 48k midpoint hits 31,727 segments against 31,722 linear.
- **Novelty.** The page itself named "the comet-class floor at depth" open; d6ba had the belt arcs and one comet cut. This run contributes the measured growth law, the mechanism, and the certificate consequence — no repetition.
- **Premise shown wrong:** the adoption one flight from gold (ALL + `ES_RETAIN_HOT`, "close it in one flight") cannot be certified at ≤ 20k cuts; the finding is adoptable at zero code cost as a certificate clause (depth + far class), plus the 10⁹ ledger charge: crossings × 336 B, retained 2·r/c per body.

Misses noted in check.md (none grading): the exempt player class is unmeasured, "~15 seg/1k game-s" is per census body (per comet ~26), "4× deepest prior identity cut" counts the ALL arm only, and the killed N=100 64k leg is unauditable from artifacts. The author's wiki fold is faithful; no corrections needed.
