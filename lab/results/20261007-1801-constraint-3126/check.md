Grade: silver

**Abstract.** Claim: the plane's constraint is the view gather (54–70% of frame CPU; ~1 Newton readout per body per frame while the engine runs at 0.03–0.06 events/body/game-second), and 92.9% of that work at rtf 100 changes the display by under one quantum, so a quantum-driven carry is the exploit. Reproduced exactly where deterministic: all four probe points (0.929/1.000/0.786 sub-quantum, readouts 292/44/400, streaks 2·15/162·599), digests bit-for-bit on all benches, galaxy 31.8 ms @1e9 ships, B13 60/64, B14 timeout exit 1. Absolute ms are unstable (×4.7 same-digest swing), shares robust. Gain: deletes the last O(N)-per-frame piece, ceiling ~10×. Adopt: redirect the queued b-readout-cost build from a cheaper eval to no eval.

**Reproduction** (clean tree, patch applied; shared box, load 0.6–3.0):
- Probe, exact bit-for-bit vs metrics.json: rtf100 m400 — 410 bodies, seen 313/28 bodies, alive 270, readouts p50 292, sub-quantum p50 0.929, streaks median 2 / p90 15; rtf1 m48 — 1.000, 162/599, readouts 44; rtf1000 m400 — 0.786 (p10 0.679), readouts 400; rtf100 m48 — 0.929, 128. All identical.
- Benches: digests match the raws exactly (m48 `09e4…`, m4800 `aada…`, rtf100 `4134…`). view_gather share 0.689 vs 0.693 (paced 30 s), 0.532 vs 0.541 (m4800), unpaced 0.696.
- Galaxy `--ships 1e9`: 31.8 ms median (author 32.1), 200/200 over 16.7 ms, 0.032 ns/ship, identical deterministic counts (13,963 cycles, 1,706,760 samples).
- `behave --law plane`: B13 60/64 worst 2.12e-2 (matches HANDOFF); B14 FAIL timeout 60.1 s, run exits 1, later gates never run; 13 FAIL lines incl. G1–G6/B7 as "FAIL … inf". Both harness-defect reports confirmed.

**Predictions.** Written 18:11:14, before the probe numbers first appear (metrics 18:14:47; benches ran 18:02–18:08 per embedded uptimes; probe stdout itself was not saved to raw/ — audit relies on metrics.json). P1 held (0.929 ≥ 0.6; 10-px 1.000). P2 held (readouts 1.0–1.9× bodies). P3 failed as written (median 2 < 10 at m400) and was honestly reported with a bimodal refinement my m200 rerun makes stark (median 1, p90 135). P4 held (colour 1.000).

**Adversarial** (my own): rtf300 m400 — 0.786, readouts 347: monotone in rtf, no hole. m200 rtf100 — 0.929 (population-determined, not member-count), readouts 155 ≈ alive 140, gather 1.69 ms ⇒ ~10.9 µs/readout, consistent with ~10.5–11 µs across every probe point. Timing attack: five runs at 71–76 bodies gave gather p50 0.73–3.65 ms with identical digests (author's own 30 s run 4.44 ms frame p50 vs their unpaced 0.944 on the same digest) — see below.

**Novelty.** Gather dominance is known: H0210's limitation "the view gather is 83% of a light frame"; H0211 added the warm-start Newton cache; b-readout-cost is queued. New here: the quantified display redundancy (92.9%/100%/78.6%; 242/270 alive beyond first light; readouts ≈ 1/body/frame) and the exploit design — carry display state, re-solve on quantum crossing/emitter event/first light, aberration composed without re-solving. This redirects the queued build, whose brief proposes cheaper evals (ramp, source caching) where this says skip the eval.

**Goal fit.** P3: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" — the view is named, and the run shows it is the one component paying per body per frame instead of per change. Moves a queued board item; no law change (the gather is a pure read).

**Not gold.** It is a measurement plus design, not a built change; the ~10× is a ceiling, never measured post-change (author concedes this). And the headline absolute numbers are machine-state artifacts on this box (below), so the dossier's frame-level projections (p50 5.96→~3 ms) are unverifiable here.

**The one experiment to gold:** build the quantum-driven carry in `gather_with` (re-solve on quantum crossing / emitter event / observer velocity change / first light) and measure `view_gather` share, frame p50/p99 and B13 before/after on the same dashboard — exactly the queued b-readout-cost item, now with its approach redirected.

**What the author missed.**
1. Their own session contains a ×4.7 same-digest swing (paced 4.44 ms vs unpaced 0.944 ms frame p50, same resolved work); the 7.9 µs/body marginal rests on two points from different minutes, and my m48/m4800 reruns bracket it to ≈0–12 µs. The robust form of the fact is the probe's ~10.5–11 µs/readout within one process; the dossier presents 7.9 µs and 4.44 ms without this caveat.
2. The streak pool includes fleet members (the increment sits in the shared sub-quantum branch while `sub_px` counts bodies only), so the median 2 is fleet-churn-dominated; body-only streaks are longer, and P3 as written likely passes for bodies — the reported failure is conservative.
3. metrics.json's whole-plane 0.054 events/body/game-second contradicts its own raw (240.3/(76×100) = 0.032; 0.054 is the m48 figure). Scale-freeness itself holds (0.032–0.055).
4. The 242 alive-but-unseen bodies' evals change nothing displayed, so the display-redundant fraction of Newton work is ~99%, not 92.9% — the claim understates its own case.
5. Probe stdout not archived in raw/; and the dossier's truncated last line (harness defects) duplicates what metrics.json records — fine, but note run.log is empty.
