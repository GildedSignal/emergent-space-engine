Grade: silver

**Abstract.** First measurement of H_live (HANDOFF open item: "not measured yet"), reproduced bit-for-bit in 22 s, and robust on a held-out seed (20261008: 109.1 vs 108.8 mean bits/body at 20 yr, p99/mean 1.13, hyper 2.1%, within-Hill 7.1%). Belt proper vs the frozen birth program: ~100 bits/body upper bound by the first full averaging window (~440 play-hours at rtf 100), thin-tailed; the fat tail is the Giant-crossers (293–301/4096 within the Hill radius, 94–104/4096 unbound in 20 yr, dt-limited at the few-% level). Real consequence: B18b's frozen uniform churn (10⁻²/epoch × 12) mis-models the belt; churn is event-quantized in a crossing minority. Not gold: irreducible bits unresolved, and the dossier's synodic-angle absorption mechanism is contradicted by my probe (5% of variance). Cost to adopt: redirect the belt build's churn model; one step.

**Reproduction.** `python3 hlive_probe2.py` in a sandbox copy: every row of `hlive2.json` identical (5 yr 102.51/116.96, 20 yr 108.77/123.17, hyper 94, within-Hill 293, crossmind 0.0045); dt-halving matches `dtcheck.txt` (median |ΔE| 4.325e-3 at both dt; hyper 94→104). patch.diff empty; predictions.md (10:38) predates v1 (10:41) and v2 (10:44) — genuinely pre-registered.

**Attacks (mine).**
1. Held-out seed 20261008: all quoted figures hold (above); one belt body even reaches 144 bits (unbound) — belt tail thin, not zero.
2. dt/2: within-Hill 293→301 (+3%), crossmind halves — the dossier quotes 293 without this sensitivity while giving hyper its 94–104 range; tail counts are few-% numerics-limited.
3. The stated mechanism "the drift is phase-locked to the synodic angle, a function of shared state, not per-body information" is unmeasured in the run; my probe (bin medians over (a, synodic phase), 128×16): absorbs 5.1% of dE variance (null 0.8%) and 0.4% of ϖ — ~1 of the 36 E-col bits. The drift is carried by the per-body free-eccentricity state; both cheap program forms (smooth-in-a, synodic-angle) fail.

**Warts.**
- "Frozen scar at 1 play-hour … measured ≈ 0" contradicts `hlive2.json`: the 1-phr row measures 69.67 bits (scarred 100%). The honest statement — the row is void (coverage 0.003; the mean element needs one full window) — appears only as a parenthetical. "No distinguishing event within a session" holds by construction (law.md: kicks orbit-averaged; first window ≈ 250–570 play-hours), not by a zero measurement.
- `control_mu0_scarred: 0` in v2 is hardcoded (`if False else 0`), not measured. Correct by construction (floors = 2× the μ=0 control's worst deviation, same seed), but presented as a measured field.
- Prose: belt orbit is 248–574 play-hours (P = a^1.5 over 2.0–3.5 AU), not 350–580; synodic 334–1,421, not 440–1,400. Conclusions unaffected.

**Novelty.** HANDOFF open item "Distinctions created per game-second (H_live) … not measured yet"; concept defined in plane.md (outside review, 5 Oct). No prior measurement in HISTORY or the docs. B18b's churn quote is verbatim (frozen 325803f). The v1→v2 rebuild (osculating vs mean columns) is a concrete new instance of "measure what the law stores".

**Fit.** Board focus item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second". P3 ("Nothing is evolved that can be derived"), P22 ("the simulation tells us what's next"), P10 ("A test that cannot fail is a control" — the μ=0 control killed v1, disclosed).

**Why silver, not gold.** Real, reproduced, seed-robust, and it redirects a frozen-gate construct feeding Sol's queued belt build — but no 10×, no deleted component, and the deciding quantity (machinery vs irreducible information) is open. The author knows it: 100 bits is declared an upper bound and the separating experiment is named.

**The one experiment for gold.** The secular-shadow twin: propagate the same birth state under the averaged field alone (a secular propagator over (a, e₀, ϖ₀, φ₀) — the birth generator knows these per body), and measure the residual scar bits vs the full run at 5 and 20 yr, belt proper, plus the resonant minority separately. It decides whether belt H_live is ~0 (program absorbs; 8 GB safe) or ~100 bits (irreducible; the belt needs a secular program in the store). My probe raises its stakes: both cheap absorption forms fail, so nothing can be leaned on until this runs.

**What the author missed.** The synodic-angle mechanism was stated as a finding without a measurement (contradicted above). The within-Hill count's dt sensitivity went unreported while hyper got its range. The scarred-fraction and index overhead (ef = 2 bits at 100% scarred) mean the "frozen program" is strictly worse than 144-bit individuals after ~1 window — worth stating outright, since it kills the frozen-program option at belt scale regardless of the twin's outcome. Belt-belt encounters are excluded by argument only (optical depth), consistent with r8 but unmeasured here.
