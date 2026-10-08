Working...
Check complete. `check.md` written, tree restored to clean `main` (patch reverted after reproduction).

**Grade: silver.**

**Reproduced** (clean tree, patch applied, release): baseline gather 2.360 ms / 74.0 % of frame (author: 2.37 / 74.2); 1216 bodies → 42.39 ms / 86.7 % (42.55 / 85.2); members-6400 → 24.24 ms (22.56); kick-bench leavers 380.6 µs and memo 0 % on 27 rebinds — exact; rtf-100 engine p99 5.18 ms (5.24), engine share 19.4 % (17.4).

**Adversarial (my own):**
- 4816 star ships (4× the top rung): 117.5 ms gather, 24.4 µs/body — linearity holds past the measured range, so the 2²⁰ extrapolation is sound arithmetic.
- Unseen seed 3 at 1216: 29.5 ms — sits in the cheap-seed band; seed 1 is systematically expensive (42 ms, not load).
- Members confound found: `--members 6400` grows `n_bodies` to ~3050–3230 via handouts, so the "3.9 µs per member" mixes handed-out body crossings into the slope; handed-out bodies are ~10× cheaper than star ships (my rtf-100 rerun: 1.08 ms at 76 mostly-handout bodies).

**Why not gold:** H0210 already recorded "the view gather is 83 % of a light frame", and the fix the dossier elevates (aggregates, one sample per pixel) is already adopted in representation.md §3 — `xtask galaxy` renders 10⁹ ships that way today. The run's real contribution is the quantified wall (24–35 µs/star-ship linear over 12→4816 bodies, 60 Hz ceiling ≈ 480–700 bodies, belt 25–36 s/frame) and the engine-share contrast (1–13 % of frames). Plus one held-out band missed ~2× (members slope 3.9 vs predicted 0.3–2 µs) and a prediction (rtf-100) that was baseline-measured, not held out.

**Gold experiment named:** build the distinction cull behind the gather's interface, measure gather flat in N on a 2²⁰ belt through the plane's one `BodyStore`, view bit-identical for differentiable emitters, aggregates conserve flux.
