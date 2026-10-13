Working...
**Grade: silver** — written to `check2.md`, with the author's wiki page corrected in place.

**What I verified (all reproduced):**
- **grid.txt (18 rows):** the runner's regen is identical on physics columns (re-diffed myself); my independent probe variant reproduced A-L12 and every other spot-checked row bit-identically.
- **The crash rows (the central claim):** grid-d.txt's D L0/L2/L4/L15 block reproduces exactly — hit Home at 7.66/5.35/8.47 km/s at 12:38/8:22/6:03, minR/R 0.9703/0.9464/0.9610; L15 alive at γ 63.99. The Λ ladder, α values, and the pump-tail fit (Δη = 2.065 over 10,495 s ⇒ γ̄ = 1.92, dη/dτ = α) all audit clean.
- **Outside the tested range:** A-L12 at 2^38 crosses at 713,479 s = 4.2× the author's horizon, γ_min 1.0000, pumps to 30.3 — their corrected arithmetic confirmed. off30 (untested angle) crosses at γ 1.323 vs cosh(η₀ sin 31.7°) = 1.46 — same ~10% gravity shave as off45, the ruler holds at a third angle. Forward-thrust-from-orbit L4: no crash — the basin is brake-specific, as the Λ mechanism claims. The cut control rests at γ 1.0004; off45/γ10 gives exactly 9,908 refusals.

**Why silver, not gold:** two record defects, not physics. (1) regen.sh cannot regenerate the crash rows — the committed flight list holds D [5,6,8] only; those four rows came from an unrecorded local edit, while the dossier claims regen.sh regenerates everything. (2) predictions.md's frozen pre-registration text is absent (only the post-run scorecard remains). Both match the historical gold-barrier ("results the shipped code could not regenerate"). One experiment fixes it: commit levels [0,2,4,5,6,8,15] so regen covers all 22 rows, and restore or declare the frozen predictions unrecoverable. Also flagged: the crash basin was already on the record from 0350-second (crash-below-L5, same scene, other nose) — this run's real contribution is the dimensionless Λ ruler, the no-threshold result, and two `range` defect reports; and "Δφ_v = π at every crossing" was contradicted by the author's own off45 row (1.4014) — corrected in the page to "every θ = 0 crossing".

Tree left as found (scratch probe removed; only `lab/results/` untracked).
