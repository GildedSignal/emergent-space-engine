Grade: silver

**Abstract.** Claim: the frame's constraint is the view gather — a synchronous, unbudgeted, uncalled `for i in 0..n_bodies()` Newton light-cone scan per frame — not the engine. Reproduced in a clean tree (patch applied): gather 2.36 ms = 74.0 % of a 3.28 ms frame at 39 bodies; 42.4 ms (86.7 %) at 1216; linear at 24–35 µs per star ship, held at my adversarial 4816 bodies (117.5 ms) and unseen seed 3 (29.5 ms); members ~3.9 µs each; engine 1–13 % of the same frames. Wall: 60 Hz caps at ~480–700 bodies, 2²⁰ belt 25–36 s/frame. Gain: names a 10²–10³× wall before any scale-up. Cost to adopt: none (measurement); the cull it points to is one design step. Silver because the dominance was already recorded (H0210: 83 % of a light frame) and the fix is already adopted (representation.md §3).

**Reasons.**

*Reproduction (clean tree at `a838a28`, patch applied, release, 8-vCPU shared runner):*
- `universe --bench` (paced 30 s): gather p50 2.360 ms / share 74.0 % / frame CPU 3.28 ms; author 2.37 / 74.2 % / 3.30. Engine share 4.5 % both.
- `ES_SHIPS=1200 --bench --unpaced --seconds 4`: gather p50 42.39 ms, share 86.7 %; author 42.55 / 85.2 %.
- `--members 6400`: gather p50 24.24 ms; author 22.56 (bodies 3229 vs their 3054 — handout counts drift with scheduling).
- `--kick-bench`: leavers 380.6 µs (author 384), exact memo hit 0.0 % on 27 rebinds, quantized 3.7 % — matches exactly.
- `--bench --rtf 100`: engine p99 5.18 ms (author 5.24), engine share 19.4 % (17.4), overflow 53/1800 (36) — same orders, load differs.

*Adversarial cases (mine):*
1. **4816 star ships, 2 s unpaced** — 4× beyond the author's top rung: gather p50 117.5 ms = 24.4 µs/body, share 87.8 %. Linearity and the slope band hold well past the measured range, so the belt extrapolation is sound arithmetic.
2. **Seed 3 at 1216** (unseen): 29.5 ms, share 88.6 % — sits in the cheap-seed band with 7 and 42; seed 1 is systematically the expensive one (~42 ms), not a load artifact (my seed-1 rerun reproduced 42.4).
3. **Members decomposition**: the author's own `--members 6400` JSON carries `bodies: 3054` (mine 3229) — handouts become bodies, so the "3.9 µs per member" slope mixes handed-out body crossings with the fleet loop. Handed-out bodies are far cheaper than star ships (my rtf-100 rerun: 1.08 ms at 76 bodies, mostly handouts ≈ 14 µs/head). Both terms remain linear O(N); the precise split is not what the dossier implies.

*Held-out predictions.* `predictions.md` predates every scaling JSON (file times: 5 m before listing vs 4–1 m for the scale runs; baselines at 9–7 m are quoted inside it, correctly, as already measured). Prediction 1 held (24–35 µs inside the 20–90 band). Prediction 2's band was **missed by ~2×** (measured ≈3.9 µs vs predicted 0.3–2 µs; direction and ordering held) — honestly reported. Prediction 3 was baseline-measured before the predictions were written, so it is not held out.

*Novelty.* H0210 (30 September) already records "the view gather is 83 % of a light frame" with the gather cache as next work (H0211 built it); representation.md §3 (adopted at the pivot) already fixes the representation: "Aggregates are one sample each, and the screen caps the work at about one sample per pixel", and `xtask galaxy` already renders 10⁹ ships as seeded families, one sample per pixel — the billion-scale view does not route through this gather. What is genuinely new: the quantified wall (linear 24–35 µs/star-ship over 12→4816 bodies, 4 seeds; ~3.9 µs/member; 60 Hz ceiling 480–700 bodies; 2²⁰ → 25–36 s/frame; `view_json`'s O(N) tail measured at 11.7 ms p50 at 4816), and the engine-vs-view share contrast that sizes the board's engine work at 1–13 % of the plane's frames. The dossier never cites H0210 or representation.md.

*Goal fit.* Bottleneck 4, and a real contract violation: plane.md foundation 7 — "Nothing takes an unbounded synchronous claim on the frame" — is exactly what the gather is (grows with N, no budget, hardest deadline per representation.md §4). P3/P14 quoted correctly. Against it: Julien's register (30 September) — "don't focus too much on the visualization though, it's just for debug" — which the dossier never confronts; its counterargument (the gather is physics-observation, foundation 5, not visuals) goes unstated. Not gold: no 10× moved, nothing deleted, no premise overturned (the dominance was known; the fix already adopted), one prediction band missed.

**The one experiment for gold.** Build the distinction cull behind the gather's interface — doll-tree walk, per-doll differentiation budget, aggregates below one quantum (P6), cull before `seen.push` — and measure it on a 2²⁰-body belt fed through the plane's `BodyStore`: gather time flat in N (the 3 orders of magnitude), with the view bit-identical for every emitter the player can differentiate at that resolution and the aggregate's flux/luminosity conserved. That is adoptable in one step and answers the "what would make it wrong" bullet (whether the belt scope really routes around this gather or inherits it through the one `BodyStore`).

**What the author missed.**
- No novelty accounting: H0210's 83 % line and representation.md's adopted fix (aggregates, screen cap, OC#30) predate this run; the dossier presents the elevation as if new. The run's true contribution is the wall's size and shape, and it should say so.
- The members ladder is confounded by handouts growing `n_bodies` (3054 at `--members 6400`); the dossier's tables omit the body counts its own JSONs carry, and the per-body/per-member cost split is kind-dependent (star ships 24–35 µs, handed-out members ~2–14 µs) — the "24–35 µs per body" band is a star-ship number.
- The claim's "engine 1.3–7.8 % of the same frames" is the ships ladder only; the author's own members runs show 8.5–13.2 % and rtf 100 shows 17–19 %. The table discloses it; the claim sentence does not.
- Julien's "just for debug" steering line, unquoted, is the strongest objection to view work and belongs in "what would make it wrong"; the answer (foundation 7's unbounded-claim ban) is the run's best goal-fit argument and is left implicit.
- B14's timeout (60.1 s) under window load killed the gate run before B17 — the author notes the instrument is marginal but does not record this window's load next to it; my reruns saw load 2.4–7.9, and absolute µs moved with it (orders of magnitude only, per the lab rules).
