Working...
Second blind check complete. `check2.md` written; nothing else in the run folder touched, `check.md` unread, no git operations.

**Grade: gold**

**Reproduction** — every command from the dossier regenerated bit-for-bit: `selftest`, all four singles (`cal`/`h1`/`h2`/`h3`), `scenep cal/h3`, `scener h1`, and the 166 s `mixedp` headline (ladder identical; rulePA 47,714 total kicks, cut 1.0301; rulePB 75,279, 0.6529; 192/192 held). No dossier number fails to regenerate.

**Three adversarial cases of mine:**
1. **Horizon (200 orbits on h2):** the fixed1 "pass" (5.9% at 48 orbits) inverts to FAIL (14.1%) while fixed4 flips to PASS (0.5%) — the author's fluke warning is confirmed and sharpened: robust minima are horizon-specific (8 → 4), which the dossier never tests.
2. **Overbreadth (radially spread belt, a ∈ [0.5,6], D=25 — same defined family, untested by the author):** rulePB transfers (40/40) and cuts 1.67× vs robust global fixed 32 — above every cut in the author's scenes, still below the pre-registered 2× kill line. The kill survives its most favourable untested case.
3. **Budget sensitivity:** slope_true spans 4 decades across scenes, but the measured margins (33–44% failures, 1.4–30× over-spend) are far beyond any budget-line wobble.

**Named for the integrator:** the mixed scene's kill criterion was structurally unpassable (oracle ceiling ≈1.28× from its own ladder), so the 1.03× headline measures the scene; the real kill evidence is the singles' transfer failures and over-spend; "cuts nothing" should read "under 2× everywhere measured, up to 1.67× in spread belts"; P8 is a failed prediction not called out by name. All documented in `check2.md`.
