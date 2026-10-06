Grade: silver

**Abstract.** Claim: the encounter skin's slack width must be per-pair — re-setup floor at 0.11·a (non-resonant) vs 2.2·a (5:2 resonance), a 55× split. Reproduced bit-for-bit (5 s, <100 MB, deterministic; all dossier numbers match `probe-out.json`); all five library quotes verbatim in the cached corpus. The prescription (width = measured drift per pair, re-estimated at each re-setup; escalate high-drift pairs out of the tier) is sound, cheap and sizes q-skin. But the headline split is confounded: my controls at 2.55/2.85/2.404 (off the strong resonances, same distance from the μ=0.03 perturber) all show the same ~2.2·a floor, and nr's "hard floor" walks linearly (0.11·a at 60 orbits → 0.43·a at 240, e bounded: precession, not amplitude). Adopt the mechanism, not the numbers.

## Reasons

**1. Reproduction: exact.** `python3 slack_probe.py` in a clean tree: every A_free, setup count, per-orbit rate and the convergence number (1.891e-07) identical to the stored JSON; 4.9 s. `patch.diff` empty (self-contained run), so the shipped code regenerates the stored curves — the r4-v3 failure mode is absent. Corpus: 770 books / 4,580 highlights consistent between `readwise.json` and `highlights.tsv`; quotes 1–5 all found verbatim (curly-apostrophe transcription only; lesson 4's second sentence is in the same highlight). Re-fetching needs `READWISE_TOKEN` (no network from the lab), so the cache was verified, not refetched — the dossier marks it cached.

**2. Predictions.** `predictions.md` predates `probe-out.json` (mtime order; `run.log` is empty, so file times are the only record). The author reports the outcomes honestly, including the nr exponent blowing through the predicted [0.3, 1] band. But prediction 1's "zero setups at w ≥ A_nr" holds only inside the 60-orbit window and the dossier hardens it into "the floor sits at the pair's total drift amplitude" — my 240-orbit rerun shows nr's error *walking*: A_free 0.108 → 0.428 (×3.96 for ×4 window, linear), e_max flat at 0.052. That is precession-driven phase drift, not a bounded amplitude: the "floor" is where the crossing period equals the measurement window, so no fixed width ever stops nr's re-setups either. Unreported.

**3. Adversarial cases (all run, ≤13 s total).**
- *e0 = 0* (circular start): split survives (nr 0.081·a vs res 2.09·a). Robust to free eccentricity.
- *Matched-distance controls* — the hit. a = 2.55 (T-ratio 2.75), 2.85 (2.32), 3:1 at 2.404: **all** show A_free ≈ 2.18–2.23·a, indistinguishable from the 5:2 case. There is no bounded point anywhere in 2.4–2.9 at μ = 0.03, while the nr control sits at a = 1 with ~5× weaker tides and sparse commensurabilities. The dossier's reading of its own det case ("the resonant band is at least 2.4% wide … a finite population") is a distance/proximity confound — at this μ the whole zone is resonance-overlap chaos, so "resonant band pairs" is not the population the skin escalates; "strong-field pairs" is.
- *Saturation*: res at 240 orbits has A_q4/A_q1 = 1.00 — the resonant drift *does* saturate at ~2.2·a. That measured saturation is solid and is the part q-skin can actually freeze.
- Split arithmetic: 55× is the absolute-width ratio (5.92/0.108); in a-units it is 20× at a 60-orbit window and 5× at 240. The headline shrinks as the window grows because one side is a walk and the other an amplitude.

**4. Novelty.** Sizing the slack skin is new: no HISTORY entry sizes it, and the skin only became the standing lever on 6 Oct. But the qualitative core is known and already adopted: H0203 ("resonance kills averaging; the design averages only away from resonance"), r4 v2 KILL, B17's resonance gate. H0161 already queried and paraphrased Musk/Taleb for the allocator; the verbatim corpus is the new artifact, and lessons 2–5 are unmeasured prescriptions (the author says so).

**5. Goal fit.** Encounters bottleneck, the lever the 6 Oct gold left standing; sizes q-skin's one free parameter. Fits "Priority is slack, not proximity" (5) and "the simulation tells us what's next not us" (22): the width is re-estimated from measured drift, and my confound result makes that *more* necessary, not less — the escalated population cannot be found by resonance bookkeeping, only by measurement. The escalation targets already exist (rotating binary doll, phase-neighbour certificates), so adoption is one design edit, not a component.

## The one experiment to gold

Rerun the split with matched-field controls and a budget-defined floor: pick μ (or the control's distance) so a bounded pair exists *inside* the strong-perturbation zone, and define the floor at a fixed re-setup budget (e.g. ≤ 1 per 240 orbits) instead of one 60-orbit window. Either a bounded population survives at matched field — then the split, properly measured, sizes the skin tier and the run is gold — or none does, and the freezable law becomes "escalation fraction ≈ strong-field zone fraction, measured per pair". Both outcomes are q-skin-ready; today's 55× is neither.

## What the author missed

- The 60-orbit window artifact (no bounded floor for nr; linear precession walk) — the strongest attack, one cheap rerun away.
- The distance confound: comparing a = 1.0 to a = 2.714 at μ = 0.03 tests field strength and resonance together; the det case was not a diagnostic control.
- The cost metric undercounts: `rate()` slides the scan frontier every ~1.5 synodic periods even at zero setups — ~0.6 window evaluations per orbit for nr, a third of the smallest-width setup rate. "Setups/orbit" is not the skin's whole cost; the 6 Oct gold's finding (92% of evals are window setup) says the slides are the bill.
- `author-final.md` is corrupted at the head (title line merged, lesson 1's quote truncated mid-sentence); `run.log` is empty, leaving mtimes as the only prediction-timing record.
- The 55×/20× unit mixing: the dossier quotes both bodies in ·a units and then the split as an absolute ratio without saying which frame the skin's w lives in.
