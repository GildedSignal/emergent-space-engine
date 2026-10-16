# Predictions — 20261016-0612-taleb-2b03 (written before the adjudication run)

Scene: b9be's verbatim (`restricted::JUPITER`, 144 ICs, horizon 512 P, plane step_log2 7,
oracle rtol 1e-12). New instrument: the tracking oracle (bisected true closest approach) from
the plane's own pre-death state, plus the death channel read from the engine's plan
(`What::Crash` vs kick/boundary surface check vs system edge). Controls: a planted grazer at
3 Rp must die in the from-state machinery (else the instrument is broken and the run is VOID).

- **P1 (the sampled-oracle artifact, b9be's own caveat):** over all 144 ICs, the tracking
  oracle's true minimum planet distance stays ≥ 10 Rp. If any IC truly dips under ~1 Rp, some
  of the 48 "deaths the oracle never has" were sampling artifacts and the false-death class
  softens before any adjudication.
- **P2 (the verdict mix):** both classes are present — at least 10 of the 48 are FALSE (the
  continuum of the engine's own pre-death state clears both surfaces for the whole remaining
  horizon) and at least 10 are HONEST (that continuum hits the planet's surface within 8 P of
  the death, or the star's). My shape guess, held out: false deaths concentrate at
  |du| ∈ {0.85, 1.05} (the layer's inner edge, weakest scatter) and honest ones at
  |du| ≥ 1.25. A 48–0 verdict either way fails this prediction.
- **P3 (the channel):** the majority of deaths fire a `What::Crash` plan item at the death
  tick (the planned-impact channel), not a kick/boundary surface check; the refused delta is 0
  on every death (reproducing b9be's refused=0 trace reading).
- **P4 (controls):** the grazer control kills (closest < 1 Rp); every live ship's from-IC
  closest is ≥ 10 Rp (same instrument, other side).

Kill criteria: grazer control passes ⇒ the instrument can kill; the run is VOID if it cannot.
The classes table (54/42/48) must reproduce b9be bit-for-bit in counts, else the ensemble
drifted and the adjudication is off its anchor.
