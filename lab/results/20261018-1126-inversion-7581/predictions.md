# Predictions (written before any formation flight; patches applied, code read, nothing flown)

Scene: the 604c formation (form ships co-orbital with the player on Home's low circle,
±2% in a, doll = home_doll ≠ 0, plain ships, not fleet members), flown by scanprobe
(600 frames, rtf 100, 12-ms budget), arms from f134's env-gated patch verbatim.

Context predictions rest on, all measured on other scenes:
- 4fa8: CHAIN alone is inert for one-tick births; the cure needs CHAIN+STAGGER.
- 2e42: the formation's over-budget frames are 98%+ comb (ev=1002-class beats), the
  worst frames are the wave frames, and rtf does not de-phase them.
- 1a46: ES_SECULAR deleted 85.8% of in-situ locals by r9's tide bound against sources.

## P1 (control): OFF reproduces the record.
form=1000: max_ev ≈ 1002-class (the fleet's shared-period wave frames), p99_ms tens of
ms (52.5 ms was 604c's record; load-dependent order of magnitude), over ≈ 60-70 of 540
late frames. form=200+extra=10⁴: worse (the pair's walks), over higher.

## P2 (the transfer question): CHAIN+STAGGER alone does NOT cure the formation.
The stagger de-phases the *first* interval of each ship's plan; but the formation is
born with the scenario at build time — if the ships' first plan is their creation-time
plan (replan, first=true), the de-phase should hold exactly as for the locals, and the
comb collapses to the no-locals floor class (~50-class). The risk this fails: the
formation ships share one circle and step_log2 — after any event that re-anchors on the
absolute grid (a handoff, a scan-driven re-plan, a stub), the offset is re-absorbed
under the *shipped* anchor; CHAIN prevents that. So my prediction: CHAIN+STAGGER
collapses the formation comb like it collapsed the locals' (max_ev → ≤ 100-class, not
the 51 floor, because 1,000 de-phased ships still each contribute events; over → near 0).
If instead the comb stands (max_ev unchanged), the composed law's letter does not
transfer to the game's crowd scene and the frame ruin is scene-owned.

## P3 (the delete question): ES_SECULAR deletes most of the formation — and that is the
danger, not the cure.
The formation ships are tide-legal (a/a_Moon ≈ 0.0173 ⇒ τ ≈ 2e-7 ≪ τ₀) and the
resonance exclusion tests only the doll's *sources* (the Moon), not co-orbital *peers*:
(a/a_Moon)^1.5 ≈ 0.0023 is not within 2% of any q/r ≤ 8, so no exclusion fires.
Prediction: SECULAR deletes ≥ 90% of the formation ships from the metronome
(max_ev collapses below CHAIN+STAGGER's), at zero legality cost in the engine's own
ledger — but the ships' mutual conjunctions (taleb-09b5's real-encounter class, the
encounters gold's exact ruin scene) are invisible to this deletion rule by construction:
the delete's exclusion list has no peer term. The digest will differ (a law change), as
it did on the ladder.

## P4: composed (all three) ≈ SECULAR's ledger (delete dominates) with the spared
residual de-phased by CHAIN+STAGGER; max_ev ≤ CHAIN+STAGGER's alone.

## Kill criteria
- If OFF does not reproduce the ev≈1000-class beat (P1 fails), the instrument is
  broken: VOID everything until understood.
- If CHAIN+STAGGER collapses the comb AND SECULAR deletes it, the composed law
  transfers; the run's content is then P3's legality hole (peer-blind delete) and the
  measured domain row.
- If any arm *worsens* max_ev or p99 vs OFF, that is a result (the cure backfires on
  the crowd scene), not noise: re-run once to confirm.
