Working...
Check complete. Verdict: **Grade: silver** — written to `lab/results/20261012-1715-q-wiki-coorbital-cert-fd4f/check.md`.

**What I did**

1. **Reproduced**: `regen.sh` PASS twice — 646 branches, 48 grades verified against branches, 13 dead-run classifications, 25 needles, tally 26 gold / 16 silver / 1 lead / 5 missing, exactly as the dossier claims. `predictions.md` (17:24) predates the page (17:34); all six held.

2. **Verified beyond the author's audit**: ~40 numbers at primary sources (74a1's `31,860,946` vs `396,000`, 154a's `0/20810`/`2.3 overtakes/orbit`, 3775's `37 TiB`, 5033's `11.6 TB`, 09b5's `606`/`135×`/`40 TB`/234-of-234 distance-rank…). One false alarm, resolved as comma-formatting. Also independently confirmed the run's own finding: `55a8`'s and `236b`'s check.md are the same git blob `45cf9791` — the "checked twice" rule is not evidenced for that pair.

3. **Three attacks, one outside the author's range**:
   - **All-branch sweep** (author read 83/646): the name-search hole is real — three silvers missing from corpus *and* handoff lists: `9834` (per-pair synodic-strobe record, tested on the gold's own co-orbital workload), `8f99` (per-pair skin slack width), `fe6b` (pair-certificate cascade budget).
   - **Present-state reconciliation**: the page called the build "unreviewed, unmerged", but the run's own base `e164d07f` **contains** merge `92c94b1` (H0216, 21 tests, `phase/pairs/tier.rs` on main) — the page's most action-relevant line was false at compile time. **Corrected in place** (build paragraph + Open direction 1); audit re-passes.
   - **Dossier bookkeeping**: 3036/6534 claimed "on my page" but absent from it (only 384f/4c98 are).

4. **Page and novelty**: seed page empty, no prior compile, taste-log consistent; page faithful everywhere attacked; correctly left open (golds agree on the representation, disagree on every constant).

**Why silver, not gold**: the deliverable is a truth-now page, and its build-status line — the one directing the integrator's next move — was stale; plus the demonstrated coverage hole. One step from gold: reconcile against `origin/main` at compile time and hand the three missed silvers to their topics' compilers.
