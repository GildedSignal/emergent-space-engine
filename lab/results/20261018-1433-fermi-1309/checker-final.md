Working...
Check complete. **Grade: lead** — the run's headline finding is refuted by the primary source.

**What I did:**

1. **Reproduced the author's work**: `regen.sh` exit 0 and bit-identical on re-run; `compose_check.py` regenerates its table; all quoted cells match 686f/ef63's published tables (fetched from their branches); predictions.md (14:40) precedes the decisive script (14:44) and dossier (14:45); shipped-code constants verified (scenario.rs planet literals, `step_log2: 7`).

2. **Ran the author's own named falsifier** — both `compose_rung.py` scripts from the run branches (which the author flagged as unavailable to them). Both compute the 10⁹ lazy+RES row with `belt_deleted_res` (708/712 deleted) at `rtf = 100`, same as the 10⁷ row: the 10⁹ cells close **exactly** (0.607–1.019 s/s; 18.1–31.4×), as does ef63's 10⁸ row. The claimed "legality flip between rows" does not exist — the 10⁷/10⁹ contrast is exactly the 100× in N.

3. **Found the flaw in the author's inference**: stream and wave see the 10⁹ row only through the product rtf×s, so their "closes only under s=61%" fit (imposing rtf=1 on that row alone, uncited) is degenerate with the script's (rtf=100, s=0.56%) — differing by exactly the 8.5% residual they attributed to an unfitted cost band. Their corrected 10⁹ row also mixes conventions (rtf-1 stream beside ef63's rtf-100 re-kick 0.55 s/s).

4. **Adversarial checks**: exact window-union integration of the geometry exposed a bug — `belt_a()` draws a∈[2,5), not the ladder's 2–3 AU belt; the author's 58.4%/75.0% reproduce only under the wrong range (true belt: 48.7% period-space, 66.7% a-space, seed-independent). Also noted S_FROZEN = 434/712 is mislabeled (frozen survival is 438/712).

5. **Salvage** (below adoption weight): the RES-legality probe extension (434-class at ≥14,167 gs, beyond 7fcf's horizons) and the 10⁹ rtf-convention question — the substance that the 10⁷ pass leans on the unproven RES delete is already 686f's own assumption (i) and the wiki's standing adoption debt.

Wrote `check.md` (lead, with reasons and what the author missed) and corrected the author's wiki page in three places (the NEW paragraph, the Refuted bullet, the Runs line) where it stated the flip as fact. Nothing else in the run folder was changed.
