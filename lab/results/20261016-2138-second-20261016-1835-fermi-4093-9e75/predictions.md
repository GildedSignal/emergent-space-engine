# Predictions — 20261016-2138-second-…-9e75 (written before the decisive flights)

The question the checker named: the freeze **duration** has never been directly measured — the
printed `lag` saturates at rtf/60 (`frame_to` sets `target = presented + want` each frame, so it
reads 29.8 at rtf 1800 and exactly 60.000 at rtf 3600 regardless of freeze length). Arms (all
shipped `nladder`, patched only with the Linux `footprint()` fallback and an additive `freeze:`
print — no law touched): **F1** 10⁵ coast 40 s rtf 1800, **F2** 3×10⁵ coast 40 s rtf 1800,
**F3** 3×10⁵ **burn** 40 s rtf 1800 (the dossier's untested risk), **F4** 3×10⁵ coast 30 s rtf
3600 (the checker's own arm, re-read with the new metric). 10⁶ cannot fly here: the build alone
is 2,340 B/body ≈ 2.34 GB > the 2-GB process cap; its crest is priced from measured linearity
instead. Metrics: `spell` = longest run of consecutive frames (after the first second) with
`target − presented > 0`; `spell_wall_s = spell_frames/60` (real-pacing wall; per-frame work is
budget-capped so pacing does not change the frame count); `deficit_s` = Σ(target−presented)·
TICK_SECONDS over all frames; `E_spell` = events resolved inside the spell; `Ĉ = spell_ms/E_spell`.

- **P1 (drain).** In F2 the crest fully drains inside the 40-s flight: the spell closes (deficit
  returns to 0) before the last frame, and is one contiguous run of 1,400–2,000 frames.
  `E_spell` ≈ 340–420k events, dominated by kicks (window kicks ≈ 330–345k, matching the
  checker's 338,539 at rtf 3600).
- **P2 (the law, same-run constants).** `spell_wall_s ≈ E_spell·Ĉ/0.72` within **1.25×** at both
  F1 and F2, with Ĉ taken from the same run (predicted 7–10 s at 10⁵, 26–32 s at 3×10⁵).
  The residual is the non-trivial content: if it exceeds 1.25× the crest is not the whole spell
  (held scans, view, or a post-crest tail) and I report which.
- **P3 (N-scaling).** `E_spell(3×10⁵)/E_spell(10⁵)` = **2.8–3.6** (linear in belt bodies ⇒ the
  crest is one first kick per body, not a pairwise term). Then 10⁶ = 3.33× F2's spell ⇒
  spell_wall(10⁶) ≈ 90–110 s per 28,141.5-game-s interval at real pacing; at 10⁹, ≥ 19 h
  (kicks-only floor) stands or moves with the measured Ĉ.
- **P4 (the metric replaces the lag).** In F4 the lag prints its ceiling (60.000) while
  `E_spell`/`spell_frames` match F2 within 10% (rtf-independent: the crest's work does not
  change with the asked-for rate) and `deficit_s(F4) ≈ 2× deficit_s(F2)` (deficit ∝ want = rtf/60).
  If instead the spell lengthens with rtf, the crest is not genesis-locked arrival work but
  queue growth — a different mechanism, and I say so.
- **P5 (burn).** F3's spell_wall within **1.2×** of F2's (3294: coast/burn fire rates identical;
  the held scans are the player's own and second-order), `held_max` larger, same `E_spell` ±10%.
- **P6 (a9d7 confrontation).** With measured E and Ĉ, the 10⁹ crest at rtf 100 needs
  ~10⁵ s of engine time per 2.814e4-game-s interval (120–190 cores sustained, or the freeze):
  a9d7's "the rate is trivially affordable" (memory-h-live L314) is true only of the average,
  false of the crest the player feels.

Kill criteria: P2 residual > 1.25× at either N, or P3 ratio outside 2.8–3.6, kills the
"crest = one event per body, budget-clamped at Ĉ" model and the 10⁹ arithmetic built on it; the
honest report is then the measured residual and what it contains.
