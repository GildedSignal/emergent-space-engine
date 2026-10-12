Grade: silver

**Abstract.** Claim: H_live (scar-creation rate) measured for a B18b-style belt; at the tube's 32-bit quantum 10⁹ bodies write 180.6 GB/h (rtf 100), so the scar quantum must be coarser than ~2×10⁻⁷ rad. Reproduced bit-identically (`python3 hlive.py`, 45.6 s); seed-stable (±1.2%); approach law α=1.079 confirmed (2-D kinetic cross-check agrees within 1.6×); size law confirmed (measured q32 rate falls 50× without >10-km bodies). But every counted event lies ~700× beyond the pair's Hill radius — the bound includes the deterministic neighbours'-moments channel, so the true scar rate may be far lower; and two reported numbers are buggy (drive 92×; extrapolation pinned to 100 km). Adoptable as an upper bound and as the crossover arithmetic, not yet as the verdict. Next: measure the persistent residual.

## Reasons

**Reproduction.** Clean tree, empty `work/patch.diff` (free components-lens run, not the directed `b-h-live` build — correct, that queue item is a different deliverable). `python3 hlive.py` in a fresh directory: every number bit-identical to `hlive-out.json` except `machine` and `wall_s` (45.6 vs 43.1 s). All headline arithmetic re-derived by hand: 1979/yr → 6.27×10⁻⁵/s → 180.6 GB/h; crossovers 2.4×10⁻⁷ (local) and 7.3×10⁻⁷ (global); contacts 0.23 MB/h; cluster 3.18×10⁻²/s and 91.7 GB/h at 10⁶ ships. ✓

**Predictions.** `predictions.md` mtime precedes `hlive-out.json` by ~10 min; P1 and P3 stake the *opposite* of the result (four orders) and are reported as failures — pre-registration is credible. Held: P2 (α = 1.079; 1.074 at seed 777), P4 (contact channel: 3.18×10⁻² vs 7.8×10⁻¹¹ ≈ 8.6 orders). Failed: P1, P3 (the headline magnitude), P5 (6.8% vs <5%). Three of five held-out calls failed; by this lab's own calibration (taste log, 1 Oct: one failed prediction → silver) gold is not available.

**Adversarial (4 variants + event dump, all on the author's own stream).**
- A1 seed 777: q32 total 6.34×10⁻⁵/s (182.7 GB/h). Stable.
- A2 parabolic sub-grid refinement of b: total +0.7%. The dt=3 d grid is not the issue.
- A3 D 1–10 km: measured q32 rate 1150 → 22.7/yr — the D³ tail is real. But the code's `extrap_smallb` is computed at the fixed 100-km scale (`5e4` hardcoded), so it still adds 829/yr to a belt with no body above 10 km. The extrapolation is 42% of the headline at q32 and is not size-law-aware; the honest uncertainty on 180 GB/h is roughly a factor 2.
- A4 σ_e = 0.3: q32 total drops 5.8× (31 GB/h). Still ≫ 4 GiB, but the crossover quantum moves with the belt's dynamical temperature.
- Event dump: 658 q32 events, median equivalent pair diameter 74.7 km, median b = 0.08 AU, median v_rel 1.3 km/s — **median b/tidal-radius = 695; zero events inside the Hill radius**. Every headline event is a distant conjunction, i.e. the neighbours'-moments regime that law.md's kick sources already include and that the author's own P5 declares "no scars in principle". The unpublished 7-Oct attempt (`20261007-0128-b-h-live-1599`, Grade: missing; its `probe_hlive.py` survives in /tmp) rejected exactly this channel as "artifact of the two-body formula beyond the tidal radius". The truth lies between: distinct partners random-walk rather than cancel, so the rate is not zero — but the deterministic kick layer absorbs the first-order (secular) part, and the irreducible residue is plausibly orders below the bound. The dossier's first wrong-making bullet says this; the claim line does not.

**Number bugs.** (i) `drive_rad_per_body_per_s.mean` = `mean(qmax)·(N−1)/YR` omits the per-pair event rate (0.0109/yr): inflated 92×; the true mean conjunction drive is ~9.2×10⁻³ rad/yr, not 0.85. It is also seed-unstable (mean dominated by the largest event: 2.2×10⁻⁹ at seed 777 vs 2.7×10⁻⁸). (ii) The A3 extrapolation defect above. (iii) Presentation: "spans ~9 orders between belt and battle" holds only belt-contact-scale vs battle (8.6 orders); at a common q32 quantum it is 2.7 orders. The 10⁹ extrapolation silently assumes fixed surface density (same annulus at 10⁹ bodies would be ~1000× worse — direction favours the claim).

**Novelty.** No H_live measurement in HISTORY.md (grep: zero hits), HANDOFF line 70 says "not measured yet", docs/law.md:13 supplies the quote the dossier uses. Closest priors: components-98bc (static program floor, 0.126 bits/body — a different quantity) and H0173 (cluster 4 bits/collision, cited). Novel. ✓

**Goal fit.** Board focus item 5 (10⁹ in 8 GB) and the risk line, via the queue's own `b-h-live` motivation. PRINCIPLES #6/#24/#33 quoted accurately; the per-scale quantum reading of #33 is the run's best idea. ✓

## The one experiment that would make it gold

On the same event stream, replace the counting bound with the **persistent** departure: accumulate each body's signed conjunction impulses against the deterministic secular baseline (Laplace–Lagrange from the same sampled belt, or an exact N-body vs the Kepler program), and count 32-bit-quantum crossings of the *residual*. If the residual still breaks 4 GiB/h at q32, the inversion is the verdict; if the kick layer absorbs the D³ tail, the comfortable reading stands and the design decision collapses to the chaotic fraction. Either way it is one run of the same code plus a signed-impulse ledger.

## What the author missed

- The Hill-radius/tidal criterion: not one headline event is a resolved encounter; the whole verdict lives in the regime the design already treats as deterministic kicks. The 7-Oct predecessor in /tmp posed this objection and went uncited (understandably — it was never published — but the physics had to be answered for the headline to stand).
- The drive statistic was published without the sanity check that its own magnitude (0.85 rad/yr, ~10⁵× the secular precession of a 100-km neighbour) begs for.
- The extrapolation's hardcoded 100-km scale contradicts the dossier's own (correct) D³ sensitivity claim.
- The cluster's rtf-100 and 8 B/scalar reuse (H0173 says 4 bits) inflate the battle headline ~10²×; the per-body rate 3.18×10⁻²/s is the solid number.
- `run.log` is empty — the run's own log line records nothing; predictions timing had to be inferred from mtimes.
