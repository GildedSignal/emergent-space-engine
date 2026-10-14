Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-1221-components-0e37/check.md`, with the author's wiki page corrected in place; tree restored pristine.

**What I did**

1. **Reproduced**: applied `work/patch.diff` myself; runner's `regen.sh` exit 0, digests identical pristine↔patched (re-diffed the saved artifacts); my rerun cross-checks the census (gather 10.73 reads/row; cold-gather retired fetches 215,134 = the census's implied cold share of its 309,227).
2. **Held-out check**: `predictions.md` (12:31:21) precedes the decisive run (12:31:43); v2/v3 only extend the instrument, overlapping numbers identical. P1/P2/P4 held; P3's gather half failed as disclosed.
3. **Three adversarial cases**:
   - **3×10⁵ bodies (outside range)**: flight reads 107–191/frame — identical to 10⁵, flat in N; same 672/670 split, 74.3% knots, linear footprint; the wave burst subsides to 109–140.
   - **40,000 game-s (2.5× flight)**: 2.0 tables/body is the steady state (no second wave); regen exact **knot-for-knot for all 300,520 current and retired tables** — closes the author's sampled counts+totals check.
   - **All-path retired counter** (my instrument on `binding_at`'s history branch): **22,605 retired fetches in the author's own flight**, 56,454 over 40k game-s — all from the player's encounter scan (`encounter.rs:180`), none from `state_of`. Rate flat across the wave ⇒ the *belt's* retired tables truly 0-read in flight, but the dossier's universal "every retired-table read comes from the view's gather" and "zero CPU cost" are false (~0.1–1% CPU to recompile).
4. **Novelty**: `ladder.txt:147` named the lever unmeasured; the census/floor/regen/O(1) measurement is new. Page folds in at the right rank.

**Silver, not gold**: the central universal sentence is contradicted by direct measurement in the same scene, and a held-out prediction didn't fully hold. One experiment from gold: fold the all-path counter into the census and restate the claim belt-scoped with the recompile cost — no physics changes; every other number already stands at 3× N and 2.5× flight time.
