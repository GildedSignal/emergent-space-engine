# Check — 20261007-2002-library-b2d5

Grade: silver

**Abstract.** Claim: practitioner lessons sharpen the encounters certificate (one structure, pay-per-change, band certificates), backed by a measured candidate-cost law. Both probes reproduce bit-identically (6.8 s / 10.6 s, <200 MB); instrument exact vs brute force at σ_e 0.05 and 0.20; fixed-extent slope 1.0015 in N confirmed on a fresh seed (1.0004). Gain: arithmetic replacing argument for the encounters build; no 10×, no deletion executed — decision support, as the author states. Adversarial checks found the dilution headline confounded (per-band density grew 34× in setup A'; at true fixed per-band density my rerun gives pairs/body slope 0.064 — flat) and the σ_e law missing its regime bound (slope 0.60 and saturating at fixed extent [1,2]). Cost to adopt: small; but adopt the corrected law, not the dossier's wording.

## Reproduction

- Clean tree, scripts copied to scratch (probe.py writes its JSON beside itself): `python3 probe.py` and `python3 probe2.py` outputs **bit-identical** to the author's (`diff` empty on both). Times 6.8 s / 10.6 s vs claimed 7.4 / 10.4; peak RSS 183 MB / 51 MB.
- `work/patch.diff` is empty; no files outside the run folder were touched — consistent with "no crate changes".
- Pre-registration: `predictions.md` mtime 20:07:02 precedes `probe.py` 20:10:37 and both outputs (20:10:48, 20:11:53). The v1→v2 OOM change is disclosed in probe.py's docstring and the pre-registered setup kept as A. Genuine.
- Dossier numbers match the stored outputs throughout (slopes 1.0015, 0.579, 0.9303, 0.9708; 329→333,009; 62→5,139; 1,185,003 control; fleet/belt 0.28; burst 1.21/0.95). One discrepancy: the P2 slope is 0.63 (fit of the three A'-rate points; 0.64 endpoint-to-endpoint), not the dossier's 0.72. Direction (failed ≫ 0.05) unchanged.

## Adversarial cases (mine)

1. **The dilution headline is confounded — demonstrated.** Setup A' (`log` mode) sets AU-extent = n/RHO and spreads n bodies log-uniformly, so per-band density = n/ln(1+n/RHO) itself grows 5,485 → 188,562 (34×) across n = 10³→10⁶; "constant per-band density" is false across N. Rerun at truly fixed per-band density (5,490/ln a, extent exp(n/ρ_b)): pairs/body slope **0.064** (flat), conjunction rate slope 0.14. So the measured 0.58/0.63 slopes and 62→5,139 growth are density-growth artifacts, not extent effects; "the pair tier can never survive dilution" (lesson 5) is unsupported by this probe. The corrected statement is stronger for the design and should replace the dossier's: **at fixed per-band density, entries per body are flat in N; the wall appears only when density is fixed per AU** (band a·e widens with a: the author's own 0.93 slope vs a) **or when bands approach the extent** (below).
2. **The sizing law has an untested regime bound.** σ_e sweep at fixed extent [1,2] (author's P3 used a 21-AU extent): 33.3k → 58.6k → 86.6k → 95.5k for σ_e 0.05 → 0.10 → 0.20 → 0.30 at n = 10⁵ — slope 0.60, saturating toward N (⟨a·σ_e⟩ approaching the extent; everyone crosses everyone). The law "candidates ≈ ρ_band·⟨a(eᵢ+eⱼ)⟩" holds only while ⟨a·e⟩ ≪ extent. A hot belt confined to a narrow radial band (resonance-trapped, exactly a game scene) re-hits the O(N²) wall regardless of the unit chosen. Not in the dossier.
3. **Instrument robustness.** Endpoint count == brute force at σ_e = 0.20 (1,965,698 == 1,965,698). Circular coplanar orbits correctly yield zero partners (the crossing filter is real). Rate formula |Δn|/n̄ differs from the true |Δn|/nᵢ at O(e) — acceptable at σ_e ≤ 0.2. Fixed-extent slope on a fresh seed: 1.0004.

## Novelty

- The O(N²)-at-fixed-distribution confirmation (slope 1.0015) measures the board's own premise (5 October), already the top scaling risk — expected, not new.
- Dilution work-growth was already on record: q-candidate-degree (taste log, 6 Oct) — "strict C·log N impossible for exact discovery under dilution". This run's dilution leg re-measures it with a confound.
- The fleet/belt 0.28 ratio corroborates the 6 Oct co-orbital gold (setup work, not event rate) — the author says so; corroborating, not new.
- Genuinely new: the exact endpoint-count instrument for crossing pairs, and the measured slopes tying the candidate unit to the band (0.93 in a, 0.97 in σ_e, 1.00 in N) — arithmetic the encounters design can use, once bounds from (1) and (2) are attached.

## Goal fit

Aimed at the board's top scaling risk. Respects PRINCIPLES #1 ("the cheapest compute is compute not done"), #14 ("we only care about changes"), #6 (store the generator: next-conjunction entries, not positions). The Asimov lesson is honestly reconciled with "every body real, never averaged" (certificate cashed on surprise, not an averaged population). But lessons 1–3 are inferences from structure, not engine measurements — only the sizing law is measured, and the author says so.

## Predictions

P1/P2 pre-registered, failed, reported as failed with the representation finding (unit = crossing band) — honest and the failure is informative. P3 held (0.97) in its regime; my fixed-extent sweep bounds that regime. P4's first instrument failed (shear confound), the matched-a fix inverted the expectation (0.28 < 2) and the burst index is admitted circular (uniform-phase generator) — all disclosed. Honest reporting throughout; that is why this is silver and not lead.

## The one experiment for gold

Fold my two adversarial legs into the probe and rewrite the dossier around them: (a) dilution at true fixed per-band density (flat, slope 0.064) versus fixed per-AU density (the wall), (b) the ⟨a·e⟩ ≪ extent bound with the saturation sweep. That yields a complete, regime-bounded sizing law for candidate entries — adoptable arithmetic for the encounters build, worth gold as decision support on the top scaling risk.

## What the author missed

- The A' density confound (n/ln n growth), which mislabels the run's headline mechanism ("dilution inflates entries" → actually "per-AU density at wide a inflates entries").
- The regime bound on the sizing law; hot narrow belts are the adversarial game scene and the law silently over-promises there.
- `rate_subsample`'s window (`ecap = min(3·e_max, 0.6)`) stops being a superset when e_max > 0.6 (σ_e ≳ 0.25): rates would undercount hyperbolic partners. Their stored numbers are unaffected (σ_e ≤ 0.2, and P3's slope used exact endpoint counting), but any reuse must fix it.
- "Events per body per orbit" weights outer bodies by their own period; the frame-cost metric is events per unit game time (a⁻¹·⁵-discounted), under which their own log-dilution growth is smaller than reported.
- The P2 slope arithmetic (0.72 vs 0.63).
