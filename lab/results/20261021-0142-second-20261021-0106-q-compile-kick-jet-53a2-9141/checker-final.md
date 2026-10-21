Working...
Check complete — `check.md` written, tree restored to HEAD (patch reverted, nothing committed).

**Grade: silver.**

**Reproduced fully** in a clean tree (applied `work/patch.diff` myself; regen byte-identical to the dossier, idempotent): the honest 535/419/116/0 sweep, the 7-token grade refresh (my own both-directions audit: 0 understating, 0 overstating, df81 branch-absent as claimed), and the byte-identical controls — HEAD's `apply()` reproduces main's inflated 135-line/28-dupe landing; the patched `apply()` lands the 107-line/57-run/0-dupe page. The page delta vs the 1st checker's audited page is exactly the 7 tokens + `updated:` + provenance, so its faithfulness rests on that audit plus a diff I verified, exactly as the dossier argues.

**My adversarial work:**
- Real 4-run publish replayed outside the author's range: my HEAD control reproduces all four pages and the index byte-identical to main; patched apply folds encounters 162→73, frame-cost 104→57 with bodies byte-identical and ids preserved.
- Independent per-line sweep: 134 old tokens leave the page with no same-line citation — "0 LOST" means nothing *orphaned*, not nothing *dropped*; the paragraph-level rescue is easy (any paragraph citing a run in `## Runs` rescues all its dropped tokens).
- Mutation probes still pass (corrupt number, deleted bullet) — the conceded id-and-presence weakness confirmed.

**Why not gold:** `fold_runs` re-implements run 6ccc's mechanism — its +102/−10 single-file patch (superset: fold + heal/defuse/skip + flag fix) applies **clean to current HEAD**, was checker-verified on memory-h-live, and sits as an open adoption direction on the wiki-memory page. The dossier never cites it, and the two patches conflict at the same line with different orderings. One experiment closes it: land this run's page through 6ccc's patch and either withdraw the standalone or justify it by measurement, plus the run's own `## Runs` line.
