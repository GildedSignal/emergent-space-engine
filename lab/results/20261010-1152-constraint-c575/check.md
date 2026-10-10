Grade: silver

**Abstract.** Claim: on the plane as it flies, the frame's binding constraint is the view gather — the only unbudgeted, synchronous O(N) cost (a Newton crossing per alive emitter per frame, no floor) — and 63–77% of it at rtf 100 re-reads emitters whose presented appearance moved under half a pixel, so a rate-bounded refresh skin should cut the median frame 3–4×. Reproduced in a clean tree with the patch: gather shares 69.9%/71.2% (author 69.8%/73.5%), digests bit-identical across machines (`41343a14…`, `09e40859…`, `aadaa1c8…`), invisible fractions 0.629/0.773 exact, kick-bench 1158 kicks / 95.5% quantized / 0% exact, `behave --law space` PASS. Not gold: the constraint is already on record (H0210: "the view gather is 83% of a light frame"; representation.md queues r6 and prescribes screen-capped aggregates), and the 3–4× gain is estimated, never measured. Adoption cost: one skin on the existing `ViewCache`.

**Reasons.**

*Reproduction (all commands from the dossier, clean tree + `work/patch.diff`, sequential runs).*
- Benches: rtf 100 gather share 69.9% / engine 17.4% (author 69.8/17.7); rtf 1 paced gather 71.2% / engine 4.5% (author 73.5/5.2). Digest `41343a143a92f956…` matches the author's bit-for-bit.
- Probes: m48 rtf 100 — digest `09e4085904c780e5` in two fresh runs and equal to the author's; gather p50 0.830/0.826 ms (author 0.824); invisible 0.629, sub-pixel 0.841, µs/emitter 13.55 (author 13.50). m400 rtf 100 10 s — digest `aadaa1c81e2bcc49` identical; invisible 0.773, sub-pixel 0.763 exact; overflow 139 vs author's 136 (adjacent-run noise).
- Kick-bench (patch hunk reverted to restore `--kick-bench`, then re-applied): 1158 kicks (same count), leavers 793, quantized memo hit 95.47% (author 95.5%), exact 0%. Kick medians 84.7 µs / leavers 103.3 vs author's 75.8/91.9 — machine noise.
- Instrument artifact: `behave --law space --gates G1,G2,B7` → PASS (256/256, 64/64, 64/64, ≤ 0.06 s), as the dossier says.
- The premise in code is accurate: `gather_with` loops `for i in 0..u.n_bodies()` (`crates/universe/src/view.rs:300`) with no differentiation floor, and `Session::step` runs it on the shipped per-frame path shared by page and benchmark.

*Adversarial cases (mine).*
- rtf 10, m48 (untested by the author): invisible 92.1% — the waste is even larger at low rtf; sub-pixel share only 0.329, so sub-pixel share is strongly rtf/scene-dependent (the dossier reports it as an rtf-100 number without saying so).
- m400 rtf 100, 25 s (1500 frames): invisible 0.623 persists past the first 1000 s — not a dispersal transient; overflow 156/1500.
- Determinism: two fresh m48 probes agree with each other and with the author's digest across machines — the probe never moves a canonical bit, as claimed.

*Predictions.* `predictions.md` file time sits after the two benches it tuned on and before every probe file: pre-registration is genuine. Outcome as the dossier reports: P1 held; P2 half-held; P3 held with the fleet-member miss honestly named; P4's number missed low; P5 broke at m400 and is reported as broken. Honest bookkeeping throughout.

*Why silver, not gold.*
1. **Novelty is partial.** H0210's limitations already record "the view gather is 83% of a light frame" (4 October), H0211 added the gather cache the probe measures through, and representation.md already queues rung r6 ("view. Newton iterations and samples per frame for the gather") and prescribes the fix shape ("Aggregates are one sample each, and the screen caps the work at about one sample per pixel"). The dossier claims "not on the board's list" and never cites these. What is genuinely new: the quantified invisible headroom (63–77%), the no-floor linear N-scaling (~10.5 µs/emitter), the engine's overflow tail at m400 (p99 > 5 ms budget), and the rtf dependence.
2. **No measured gain.** The 3–4× cut is an estimate from the invisible fraction; nothing was built or measured. Gold needs the bottleneck moved, not mapped.
3. **One inflated number.** "View 2.2–3.1× the whole engine per body per second" mixes per-*emitter* view cost with per-*body* engine cost; from the author's own sums the honest per-body ratio is 1.6–2.7× (m48 713 vs 264 µs, m400 517 vs 294, m400-s7 543 vs 345). The direction survives; the stated range does not.

**The one experiment to gold.** Build the rate-bounded refresh skin on `ViewCache` (an angular-motion bound per cached emitter, aggregates for sub-pixel clusters — i.e. r6) and measure the plane's actual median/p99 frame cut and the view's new scaling in N: a measured 3–4× at 63–77% waste confirmed, with digests unchanged, is a gold-sized deletion of the view's N-scaling.

**What the author missed.**
- H0210/H0211/representation.md-r6 as prior record; the run's real contribution is the headroom quantification, and the dossier should have positioned it as such.
- The invisible fraction is non-monotone in rtf (49% at rtf 1 < 63–77% at 100, 92% at 10, 14% at 1000) and the dossier never diagnoses why; at fixed 600 frames the rtf-1 probe samples only the first 10 s of a hot, close battle — the fraction tracks scene age as much as rtf.
- The colour criterion is dead weight: `halfpixel_only` is 0.000 everywhere, so among sub-half-pixel movers the 1/255 colour step essentially never binds — "invisible" is a pure motion metric.
- The probe JSONs come from two instrument revisions (`probe-m400`, `m4`, `rtf1000`, `rtf10000` lack `invisible_refresh`); the m400 invisible claims rest on `m400b`/`m400-s7` only — not disclosed.
- The patch replaces `--kick-bench` rather than purely "adding" `--view-probe`; the kick-bench numbers come from the pre-edit tree.
- The half-pixel floor presumes a 1080p/90° presentation of a 360° gather; the debug page has no FOV culling, so the measurement is fair, but any real renderer's FOV culling changes the denominator the skin would see.
