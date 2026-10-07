Working...
Check complete and written to `lab/results/20261007-1801-constraint-3126/check.md`. Tree restored (patch reversed, only `lab/results/` untracked); nothing else in the run folder touched.

**Grade: silver.**

What I did, and what it showed:

**Reproduced exactly (deterministic):**
- All four probe points bit-for-bit vs metrics.json: sub-quantum 0.929/1.000/0.786 (rtf100 m400 / rtf1 m48 / rtf1000 m400), readouts 292/44/400, streaks 2·15 / 162·599.
- Bench digests match the author's raws on every config; galaxy at 10⁹ ships: 31.8 ms (author 32.1), 200/200 over budget, identical compile counts.
- Both harness defects confirmed by rerun: B14 times out at 60.1 s, `exit=1`, later gates never run; old gates print `FAIL … inf` (13 FAIL lines). B13 60/64 matches HANDOFF.

**Adversarial:** rtf300 (0.786, monotone in rtf) and m200 (0.929, readouts 155 ≈ alive 140, ~10.9 µs/readout) — no hole. The prediction-timing order holds (predictions 18:11, probe numbers 18:14, benches 18:02–18:08).

**The one real weakness:** absolute timings. The author's own paced 30 s run (frame p50 4.44 ms), their unpaced run (0.944 ms) and my paced rerun (0.945 ms) share one digest — same resolved work, ×4.7 swing. The 7.9 µs/body marginal is two points from different minutes on a shared box; my reruns bracket it 0–12 µs. The robust form is the probe's ~10.5–11 µs/readout. Shares (54–70% gather) held in every run — that is the load-bearing evidence and it stands.

**Not gold because** it's a measured design, not a built change; the ~10× is a ceiling. The gold experiment is building the quantum-driven carry and measuring it on the same dashboard — which is exactly the queued `b-readout-cost` item, now redirected: the run shows the answer is *not re-solving at all*, not a cheaper solve (the lens brief's ramp/source-caching proposals). Novelty caveat: gather dominance itself was already recorded (H0210, H0211); the quantified redundancy and the carry design are the new part.
