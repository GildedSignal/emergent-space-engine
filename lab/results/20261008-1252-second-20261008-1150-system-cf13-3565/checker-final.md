Working...
**Grade: gold.** `check.md` written; nothing else in the run folder touched; scratch removed; no commits.

**What I verified:**

1. **Reproduction** — Built `exp` against the unmodified `crates/encounters` (patch.diff empty, tree clean) and ran every dossier command: all six scenes, `BANDS=1` F2, both `W_SAFETY` boundaries, and all three kick runs. Every counter matches `scenes.jsonl`/`boundary.jsonl` bit-for-bit; only ms differ. Cost numbers re-derived: F1 109.3×, CONVOY 2.69×, TROJANC 7.51×, F2-maximal 41.7×, X 2.11×, B 1.00×.

2. **Predictions** — File times show exactly one clean pass after `predictions.md` was filed (13:06 code → 13:07 predictions → 13:07:50 record, durations matching my own runs). P1–P3, P5 held; P4 held in direction only, disclosed. The original run's hygiene flaw (undisclosed scene resizing) is fixed.

3. **Six adversarial cases of my own, all 0 missed:** a convoy straddling the λ=0/TAU wrap (the hand-rolled wrap branch is correct — never tested by the author); three ultra-cold fleets (σ_e down to 1e-6, e_hi ≪ ρ/r, probing the window constant's missing ρ/r term); a drift-clamped clustered swarm (renewal need ≫ 64); and e = 0.5/0.55 swarms (the "exactness survives, win dies" disclosure, now measured).

4. **Novelty/fit** — The angular window is the first checker's prescribed fix, not in HISTORY or docs; it corrects the silver's record and answers the board's top scaling risk. The understated headline: candidates per real encounter ≈ 4.1 on the convoy — work tracks real encounters, not the N² candidate set.

Residuals (all author-disclosed, non-blocking): the `isolated` gate letter fails on 44 removal-touches (added = 0; deferral policy unmeasured), and the kick test is bookkeeping, not dynamics — the named next rung.
