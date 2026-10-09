Working...
Check complete. `check2.md` written: **Grade: silver.**

**What I did (all ≤ 2 GB, ~20 min):**
- **Reproduced** in a clean tree with `work/patch.diff`: digests bit-for-bit (`06b78c67…` m400 paced and unpaced, `4366e41e…` m4 unpatched-identical → patch is pure instrumentation); gather p50 3.27–3.33 ms vs dossier 3.18; atom 10.4–10.9 µs/readout; kick-bench 48/67 µs vs 43/77. Every dossier table row matches its stored JSON.
- **Predictions:** timestamps confirm `predictions.md` (22:23:15) preceded both held-out runs; 3 of 4 held, the readouts/body miss honestly reported.
- **Four adversarial cases:** fresh seed 42 (holds); rtf 500 (engine saturates its 5 ms budget yet zero hitches > 16.7 ms — the budgeted-vs-unbudgeted asymmetry is structural, but the "engine is not the constraint" claim is only valid in the rtf ≤ 100 band); paced-vs-unpaced under load (3.27 vs 3.25 ms, same digest — the 4× swing is idle-specific as claimed); and the decisive one — **bypassed the `--members 400` clamp** (one-character edit, reverted): at 1,502 bodies gather p50 = 14.35 ms, p99 17.0, frame p50 23.5 ms, atom still 10.92 µs — the headline 1,600-body break-even is real, and I measured what the author only extrapolated.
- **Novelty:** partially anticipated — H0210 already recorded "the view gather is 83% of a light frame" and commissioned the cache (H0211/H0212); representation.md already plans r6 and one-sample-per-pixel aggregation. New: the post-cache atom, the scaling law, the DVFS trap, the foundation-7 framing.
- **Why silver:** reproduced and strengthened, but nothing moved — no lever built, no component deleted; the run measures and names. Gold experiment: the smallest cull/incremental-gather slice, gated on emitted-view invariance.
- **Author misses:** H0210 uncited; the clamp was bypassable in one character (extrapolation left where a 50 s run existed); band edges flatter the claim (measured gather 53–76% vs stated 56–78%; engine tail-weighted share reaches 33% vs stated 22%); rtf > 100 unprobed; DVFS mechanism inferred.

Tree restored to as-found (only untracked `lab/results/` remains); nothing else in the run folder touched; no git commit/push.
