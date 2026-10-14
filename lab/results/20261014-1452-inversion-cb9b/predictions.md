# Predictions — 20261014-1452-inversion-cb9b (written before the decisive runs)

The inversion: 2df1's row-set deletion made the flyable map frame ~1-3 ms p50 flat in N **in
coast**, and its dossier names the burn as unmeasured ("the burn burst (vo changes every row's
aberration at once) is unmeasured and named open"). The view page's open direction 3. The player
is the only wildcard (PRINCIPLES #5); smoothness is judged on tails (#12). These predictions are
written after one smoke run at N=28 (mechanics only: the input path, the burn window, the stats
lines) and **before** any N-scoped or level-scoped run.

Mechanism: a burn changes the observer's vo, so every row's aberrated `direction` (and its
Doppler `shift`/`closing`/`color`) changes; the sky's quantum is polar, arc = r·Δβ, so a row at
radius r re-serves when r·Δβ ≥ 0.5 px. The map's quantum (`offset`) is root-frame geometry with
no vo in it, so the map should behave like the turn (free). Expected per-frame served rate in
the sky during a burn ≈ Σᵢ 2·rᵢ·Δβ/frame ≈ (432 px · Δβ/frame) · N averaged over the disc.

1. **Sky, L8 (cruise), 10³-10⁵:** the burn window's served median rises from the coast's ≤0.4%
   of rows to a steady ~1-3% of N per frame (the aberration quantum), gather p50 during the burn
   several times the coast steady but < 50 ms at 10⁴; audit stays clean (rows re-serve at the
   half-pixel, the audit fails at a whole one).
2. **Sky, L15 (slam), 10³-10⁴:** served median ≈ a large fraction of N **every frame** (Δβ/frame
   large enough that rim rows cross the half-pixel each frame); gather p50 during the burn
   returns to the coast's linear gather (~10-11 µs/row): ≥ 100 ms/frame at 10⁴, ≥ 1 s at 10⁵ —
   the collapse the deletion deleted, back for the duration of the burn, exactly when the player
   acts.
3. **Map, fit and belt, L8 and L15:** served stays at the coast level (the turn's behaviour):
   the map's quantum carries no vo. The burn's engine-side cost (the kick waterfall) shows in
   engine p99 but is not this run's claim (GPT's T1 job).
4. **Map audit during burn:** px violations grow versus the same-scene coast control — the
   observer accelerates, so every row's drift rate changes under the wheel's feet and the ×4
   slack undershoots (the belt-zoom residue mechanism, now triggered game-wide by the burn);
   concentrated at the burn's start while the wheel re-learns.
5. **The turn control at the same scene** (input path, no vo change): served and gather stay at
   the coast level — proving the burn's growth is vo, not the input plumbing.

Falsifier for the whole frame: if the burn window's served median at L15 in the sky stays ≤ the
coast's, the deletion's collapse is burn-robust and this run is a negative result (a control that
passed).
