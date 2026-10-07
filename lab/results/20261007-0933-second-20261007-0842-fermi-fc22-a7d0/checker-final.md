Working...
Check complete. `check.md` written to the run folder; nothing else changed (verified: `ledger-out.json` still bit-identical, tree clean outside `lab/results/`, no stray processes).

**Grade: gold**

Verification summary:

**Reproduced (clean tree, empty `patch.diff`):**
- `ledger.py` → bit-identical output, also bit-identical to the original silver's committed artifact
- All three `livebelt` rungs → every physical counter bit-identical (270/1133/15178 crossings, kicks, events, `mean_vrel` to 5 digits); m=10¹⁹ rerun took 424 s vs 352 s only because my box was more loaded
- `verify a`, `kick`, plane anchor (28 bodies, 2349 B/body) → all structural counters identical, timings differ under load
- `ledger2.py` arithmetic re-derived by hand (3.1006×10⁻⁸ /body/s → 31.0 writes/s → 209.3 MB/game); model confirmed free of fitted constants
- Timestamps: `predictions.md` 09:45:45 precedes both decisive outputs (09:59:45, 10:00:09)

**Adversarial (5 cases, all supportive):** seed +6%; σ_e×3 → rate −9% (confirms the v_rel-independence/threshold-domination regime claim, the strongest physics in the run); m÷10 → rate ÷11.3 (linear downward, kicks/crossing → 1.18); N=8000 → exponent 1.13 over the octave, mildly super-linear in the conservative direction; far-walk truncation also conservative.

**The result:** the first checker's named experiment is done — the flux model reconciles with a live belt at 1.05–1.47× with no fitted constants, the 32× closes as measured cross-section form (6.0×) × misremembered belt (5.3×), and the original ≤ 1 MB/game claim is refuted ~200× for every planar belt the engine ships (it holds in 3-D with ~50× margin). This corrects the first checker's own attack #5, which had applied the correction in the wrong geometry.

**Flagged in check.md:** the dossier's "16.5–19.6 ms per recertification" exists in no stored artifact (its `kick.json` stores 7.2–7.5 ms — direction unaffected); the 3-D leg remains direction-anchored only; the sim's own `word_writes` counter (8–10× the crossing rate) would make a real element-word store pay more than the crossings×50-bits line.
