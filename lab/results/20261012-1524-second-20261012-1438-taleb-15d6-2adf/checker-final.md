Working...
Check complete. `check.md` written; tree restored to its pre-patch state (only `lab/results/` untracked, as at start); no commits.

**Grade: gold.**

What I did and found, briefly:

**Reproduction** — Applied `work/patch.diff` in the clean tree; verified `phase.rs`/`tier.rs` sha256-identical to `wt/cx-b-coorbital-cert` (adce00d6). Every number regenerated bit-identically: controls (314/757/249/705 contacts, rank stats), `built` (0 misses × 6 scenes), `builtsnap` (k p50 3411, 3,409,495,373 visits, 0 window misses — run twice, deterministic), `decomp` (EoC 99.5%, k_pred/p50 0.999), `surgery` (−3.7%/−10%), `scaling` (exponent 2.04), treefall (C(10⁵,2) exactly — my initial "off by 45,000" was a comma miscount on my part).

**Adversarial** — Four probes of my own: seam-centred clump (3 seeds, full-horizon brute, ~2300 contacts each: 0 misses); honest refusal at wide a-spread; tree tier exactly C(n,2) at n=2000/8000; and a contacts-scaling probe that sharpens the story — contacts are **also** quadratic in the uniform-λ construction (×10.02/×10.07 per decade), visits/contact flat at ~1380, so the defect is the 853× constant (4·e_max order statistic vs the k≈4 promise), not a tier-specific exponent. I also confirmed the mechanism analytically: e_max = σ√(2 ln n) to 1.3%.

**Predictions** — Written before the decisive runs; H1/H4/H5 held, H2 missed and self-reported (sharpening). One blemish: H3's pre-registered "±15% on every scene" failed on clumps (0.006/0.045) and the Predictions summary quietly narrows it to "uniform fleets" — disclosed in Evidence, mislabeled in the summary. Named in the check; doesn't sink the claim since the delivered guard is the exact two-pointer, which I verified.

**Novelty** — Headline confirms the first checker's 3d (openly cited); the decomposition, surgery, gate-blindness proof, and treefall are new and measured here first. On the board's top scaling risk, at the pending b-coorbital-cert freeze, adoptable in one step.
