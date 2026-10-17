# Predictions (written before the decisive conflict-wave runs S2/S3; only the 44-body smoke
# and the stagger-300 control above had run)

Scene: the prior gold run's Fermi-cannon battery (`tax`, verbatim), stagger 30 (the conflict
wave) and stagger 300 (the no-conflict control, already run: 0 rollbacks, escal 1, 354 regions
end at 1,408 bodies). Arms: shipped (verbatim ratchet), `ES_CAP=16`, `ES_CAP=64`. The cap keeps
the ratchet's permanence (no decay) and bounds the latch: `escalation = min(escalation*2, cap)`.

Known going in (not predictions): the wiki's latch band at 14,080 bodies is 2⁶–2⁸ (64–256,
one draw at 128); shipped finishes 6k chronons there in ~74 s at ~82 c/s on the prior box;
the decay/local mirrors wedge there. This box is ~3× slower than that one (the stagger-300
control: 76 c/s vs 248–287), so absolute walls are only comparable within this window.

## The cases I have not tuned on, and what I expect

- **P1 (certificate, both sizes):** every arm that finishes yields the same world and log
  digests as shipped. The cap touches only forecast margins (scheduling), never results.
- **P2 (cap16 at 14,080 bodies — below the measured latch band):** the cap binds before the
  wave's quench threshold; conflicts recur instead of quenching. Expected: rollbacks ≥ 5×
  shipped's (which was 6–8 there), and either DNF (the mirror's wedge inherited — the run
  burns all workers with no frontier progress) or a finish slower than shipped's collapse
  (> 2× shipped's wall). This is the kill case for a fixed low cap.
- **P3 (cap64 at 14,080 bodies — the band's floor):** quench still reached (rollbacks within
  ~2× shipped's), escal_max = 64, no wedge, wall within 2× of shipped; the scene still ends
  few-to-one region (the row's sweep-coupling is physics, not margin). I.e. safe, and it buys
  ~nothing at this size — the collapse is the wave's, not the latch's.
- **P4 (1,408 bodies, stagger 30):** all three arms finish, no wedge, digests identical;
  shipped collapses toward one region (its known faster state at this size), the caps latch
  ≤ cap. Throughput separations here are within 2× (the collapse and the many-region regime
  are both viable at 1,408).
- **P5 (recurrence signature):** if an arm wedges, its last completed stage shows rollbacks
  still growing with stage index (no quench); if it quenches, rollbacks flatten to a constant
  per stage. I will dump the per-stage TSV (`TAX_STAGES=1`) for any DNF arm to name the cycle.

## Kill criteria (frozen)

- **Killed at a size** if: DNF where shipped finishes, or a digest mismatch (that would also
  falsify P1 and be reported as a certificate break, the worst outcome here).
- **Adoptable as a bounded tail** only if at 14,080 bodies it finishes with escal_max ≤ cap
  and wall ≤ 2× shipped's.
- If cap64 passes and cap16 fails: a fixed cap is safe only above the scene's quench
  threshold, which scales with the wave — so no constant cap is adoptable at 10⁹ bodies; the
  honest reading is the cap trades the latch for the wedge below threshold and is inert above.
