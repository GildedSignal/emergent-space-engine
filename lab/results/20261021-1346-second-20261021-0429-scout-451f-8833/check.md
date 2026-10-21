Grade: silver

**Abstract.** Claim: with the instrument fixed (three fixes, each held to a control), the fleet
doll's linear interior law has exit error err = k·(ξ₀/rp) exactly over one relativistic flyby;
451f's "c₂" was a quadratic fit of that linear law; the checker's open in-plane excess is mostly
IC convention, the exact-IC remainder scaling as M/r. Reproduced bit-identically (`bash regen.sh`
in a clean dir, 2m19s, 11/11 controls PASS, all JSONs byte-equal); ref-451f-flyby.json verified
identical to 451f's branch data. Adversarial: no floor to ξ=1e-6; exact z linear to ξ=0.3; but
M/r bends at 6M (rad 5.8× vs 3×) and rp-independence breaks there. Gain: the 1% certificate
30–50× looser with exact ICs (5.6e-5 → 1.7e-3, β 0.9). Adoption: one sentence per member, no
engine change.

**Reasons.**

1. **Reproduction: exact.** All five modes re-run in a clean directory; control.json, mapcheck.json, flyby.json, flyby2.json, conv.json and analysis.txt are byte-identical to the stored files; all 11 controls PASS. The repro reference is honest: `ref-451f-flyby.json` is bit-identical to `flyby.json` on `origin/claude/lab-20261021-0429-scout-451f`. Spot-verified dossier numbers against the JSONs: k_trunc along 14.59/177.6/666, radial 14.42/35.52/67.82, z 2.421/4.076/7.592; certificate 0.01/k = 6.9e-4/5.6e-5/1.5e-5; exact-IC worst in-plane 1.75e-3 at rp 18M, ~1.1e-2 at 100M. The checker's probes tie (radial 1.064/2.026 at 3e-2, β 0.9/0.95).

2. **Predictions: the decisive fork held, but the record has one misreport.** predictions.md (with addendum) exists; the addendum cleanly predates the exact-IC run (predictions.md 19m, the falsifier edit adding flyby2 and flyby2.err 17m in file times). The decisive pre-registered fork resolved as registered: addendum A failed, C held (k_exact ≪ k_trunc; in-plane excess is convention). Failures #1/#3/#5/#7 are honestly reported and are themselves the finding. But **addendum B ("vrel0_fd with exact ICs scales ξ²") is reported HELD and the run's own data contradicts it**: 5.08e-5 → 6.61e-4 over 300× in ξ (13×, i.e. floor + linear, not ξ²; analysis.txt lines 141–144 even label it "should be xi^2"). Diagnostic only — no headline claim rests on it — but a misreported prediction on the record is what cost 451f its grade. Also, conv.err (23m) predates predictions.md (19m), so prediction #2's "held" may be post-dicted; the first flyby-mode execution (24m) is disclosed only as a timing cell, whose quoted values match the final grid bit-close.

3. **Attack (4 cases, 3 outside the author's range):**
   - **ξ = 1e-6/1e-5 (below the grid):** truncated channels flat (err/u = 35.52/177.6/4.076 to 4 digits) — "no floor" extends a decade below the claim. Exact channels flat below 1e-5 with a tiny numerical floor (err ≈ 4.5e-6 at ξ=1e-6), negligible at any certificate-relevant ξ. Holds.
   - **rp = 6M, β 0.9 (stronger field than any exit-grid point):** converged flat 4000→8000 steps, but the exact-IC channel bends off M/r: rad k = 15.9 vs 3×2.73 = 8.2 predicted (5.8×), z 8.31 vs 7.0 (3.6×); truncated along breaks rp-independence (96 vs 178 at rp 18). The M/r and rp-independence sentences are true only on the swept [18,100]M; the dossier/page did not state that domain (page now corrected).
   - **β = 0.99 (γ = 7.1 vs 3.2):** truncated z keeps γ² (36.2 vs 37.3 predicted from β 0.95), along keeps γ⁴ (1.6e4); exact rad/z rise ×2.3 from β 0.95 — beyond the stated "weak (0.3–1.7)". Domain limit, not a kill.
   - **ξ = 0.1/0.3 (beyond the top):** exact z linear to ±4% at 0.3, exact rad ±25%; truncated along bends non-monotonically (178→217→103). The law's reach is if anything understated for exact ICs.

4. **The "physical channel" reading is not earned by the run's own standard.** The dossier convicts the truncated channel by its τ-linear growth fingerprint ("an initial-velocity error free-drifting") — and the exact-IC channel shows the **same exactly-linear shape** (rad, rp 18 β 0.9: 0.025/0.057/0.107/0.255/0.503/0.751 at τ/T = 0.02…0.75), where a periapsis-decaying tidal force would front-load (≈0.19/0.47/0.73 by the same kernel estimate). The author discloses this in "What would make it wrong" but headlines k_exact as "the physical channel" in the dossier, analysis.txt and the page. Od 1 (the closed-form Marck/Manasse–Misner second-order Fermi force) is correctly named and not done.

5. **Novelty: yes.** The page's record: 288f refuted the letter's Newtonian tensor; 4c79 (gold) certified the linear coefficients; 451f (silver) read a z c₂ now shown to be a fit artifact. The linear law err = k·u, the IC-convention split, the exact-IC channel and the certificate numbers are new on the topic; nothing in docs/HISTORY.md covers the doll interior at second order. Three gold runs do not agree on this best (4c79 is the linear level; this is the first run at this level), so the page stays open.

6. **Page:** corrected in place (overstatements): "spread ≤ 7%" → ≤ 9.2% (along, β 0.95; the run's own table); "92–99.5% of the in-plane channel" → 95–100% for rad/π4/3π8/along, π/8 at rp 18 β 0.9 only 57% convention; "2.4–5.7" → 2.0–5.7 (3π/8 = 1.96); added the swept domain (18–100M, β 0.5–0.95, ξ 1e-4–3e-2) with the 6M/0.99 bends, and flagged k_exact's mechanism as open. Budgets hold (current best 14 lines, page 62 lines).

7. **Goal fit: yes.** Board row "families and formations: how long a member's certificate lasts against its separation" — answered for the extent half with a one-line rule (err = k·u, k by channel and IC convention), and it deletes the naive refine-at-5.6e-5 requirement in favour of one parallel transport per member (pricing is od 2). PRINCIPLES 33: "a body resolves only the influences that are significant at its own scale" — the certificate is exactly where the linear scale stops resolving. P2 (error type over size): the in-plane failure was a type (IC convention), killed by representation. P26: the exact-IC launch is the EMRI community's osculating bookkeeping — stealing from skin in the game.

**The one experiment for gold:** od 1 as written — compute the closed-form second-order Fermi force (Marck/Manasse–Misner cubic terms) and check it reproduces k_exact (2.0–5.7 in-plane, ∝ M/r, along suppressed ~10×) or exposes it as residual convention; the τ-shape test above says the latter is a live possibility. With that settled and the headline numbers stated at their true spread/domain, the certificate sentence is adoptable as-is either way (it is mechanism-independent).

**What the author missed.**
- The exact-IC channel's τ-linear growth (their own drift fingerprint) argues against calling it physical; they measured it and still headlined "physical channel".
- Three headline overstates vs their own tables: spread ≤ 7% (9.2% at rp 100 β 0.95 along), "92–99.5% of the in-plane channel" (π/8 at rp 18 β 0.9 is 57%), "2.4–5.7" (1.96 at 3π/8).
- Addendum B misreported HELD (data: floor + linear).
- Domain limits unstated until probed: M/r bends at 6M, truncated along rp-independence breaks at 6M, β-ratio reaches 2.3 at β 0.99.
- Minor: the K-table header says "over u in [1e-3,3e-2]" but `kread` uses [1e-4,3e-2] (immaterial to the numbers); the certificate's strength — that it holds to ξ=0.3 in exact z — was there to be claimed and wasn't.
