Working...
Check complete. Final state verified — tree restored, only `check2.md` written and the author's wiki page corrected in place.

**Grade: silver** (`lab/results/20261021-1443-dynamics-99d7/check2.md`)

What the check found:

**Reproduction** — every dossier number regenerates (regen.log + my re-run bit-identical); instrument diffed against cbe6's patch: verbatim as claimed; predictions.md predates the decisive runs.

**Premise break (the load-bearing finding)** — `OrbitSpec.periapsis` is documented "periapsis radius" but `OrbitKey::bound` consumes it as the **semi-latus rectum** (`k = 1/(1+e)`, stored peri = p/(1+e); apoapsis = p/(2k−1) confirms). Verified three ways: osculating fit of the engine's own t=0 state (a_osc = p/(1−e²) to 5 digits), the φ-winding fingerprint (measured windings match 3−(a_p/a_actual)^1.5 exactly — the unexplained ≈−4.6·e offset in the author's own data), and the apoapsis identity. So every e≠0 body drawn at `periapsis = a(1−e)` lands at a/(1+e) — this run's "3:1 zone" arms orbited 2.06–2.45 AU (its e=0.2 "ridge" is actually the 4:1), its "bridge" sat at 6.3–7.5 Hill (already-certified territory), and its "5:2" arm accidentally flew the true 3:1. The shipped `ladder_ship` belt birth and ddeb's census inherit the same displacement.

**Refuted** — "no island anywhere": my deliberate true-placement scan shows |mean e^{iφ}| = 0.905 with stalled winding at exact resonance (island ≈ 0.3× the pendulum width, not "≫10×"), and belt-e-law draws capture within 100 periods, pumping Δe 0.072 — killing the "birth-frozen certificate is safe" reasoning and supplying the zones' real re-derive trigger.

**Survives** — the certificate claim itself: at true placements, the actual 3:1 passes B12 at 16 (1.3–2.2e-5, capture present, pump step-independent, step-3 cliff 14/25 fail) and the actual interior bridge (5.9–6.4 Hill) passes (1.2–1.5e-5). The ≈550× composed headroom stands — checker-flown, one seed, one horizon.

**Gold experiment named** — re-fly both arms at true placements (periapsis = a(1−e²)), two seeds, 400 periods, on the author's own instrument. The wiki page's NEW row, both refuted bullets, and the run line were corrected to what was actually measured, with the OrbitSpec finding folded in as open direction 2.
