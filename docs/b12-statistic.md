# B12 candidate — finite-horizon error type (not frozen)

Requirement: test errors that accumulate over repeated sphere-of-influence crossings,
without mistaking chaotic changes in the state for error memory. Horizon: 200 planet
periods, 16 recorded ships, nominal and nine-replica median crossing counts ≥20.
The 1e-4 relative Jacobi cap and 1e-12 reporting floor remain unchanged.

## Measurement

Use signed relative Jacobi error. Match each early far-field state to its nearest
unused late state in standardized semimajor axis and eccentricity. One standard
deviation is the recurrence radius; this describes the ship's own state spread.
A gap of two initial synodic periods separates returns. The far-field mask is
3 Hill radii, where the planet/stellar-tide force ratio is 1/27. These scales come from
orbital dynamics and normalization, not measurements of any candidate law.
Fit the signed pair differences through the origin on the two state differences.
Rank the remaining magnitudes against elapsed time. A state gradient is removed
before taking absolute values, preventing a bounded offset from hiding a leak.
At least three usable pairs are needed to distinguish two state gradients and
an exposure term; singular state fits carry no evidence. Above-floor histories
without evidence consume the existing 10% exclusion budget. Missing/junk fails.
Before PASS, add the declared leak to this law's own sampled histories and
require the detector to reject the result. Verify the delivered Jacobi shift at
every sample to the existing floor. A law that hides this leak is **UNSUPPORTED**,
even when its original rank score is quiet. This is a sensitivity gate, not a
threshold fitted to that law, and costs no second physical simulation.

The pooled rank score uses Var(C−D)=n(n−1)(2n+5)/18, the exact independent,
untied-rank variance (checked over every permutation at n=5). GLM's published
per-ship factor 3 omitted sqrt(2); its pooling then inconsistently compensated.
The candidate cutoff is the conventional five-standard-deviation reference,
corresponding to a one-sided Gaussian tail 2.87e-7 **only for that null**.
Temporal dependence and fitted nuisance gradients invalidate an unconditional
confidence claim. This proposal MUST NOT be called a validated certificate until
the red-team addresses this premise; passing the controls does not establish it.
Local-affine slow-state error is a model assumption, not every bounded function.

## Resolution and oracle domain

The requested detectable leak is one existing relative floor quantum per planet
period: 1e-12/P, or 2e-10 across the horizon. The bare leak and that leak composed
with `planted-bounded` are explicit controls. This is the smallest **claimed and
tested** rate, not a universal power bound or proof about smaller leaks, leaks
confounded exactly with state change, rare-ship failures, or future horizons.

`xtask/src/behave/b12_corpus.json` records exact input IEEE words and offline
reference assessments. Selection is law-independent: the first 15 eligible busy
ships and the first eligible busy ship with a perturbation-stable surviving fate.
Each primary reference converges in Jacobi between tolerances 1e-12 and 1e-13.
The gate consumes the recorded assessment, eliminating runtime platform-dependent
search and convergence exclusions; it does not assert identical live trajectories.
Nine replicas are the nominal state plus ±one IEEE quantum in each input word.
Closest approach uses the smaller result of the two tolerance runs per replica.
A surviving fate is judged only if all nine stay outside the real surface.
Split-fate ships instead supply uninterrupted point-mass histories for the growth
measurement (surface radius zero, SOI unchanged); their real-surface fate is not
judged. This scene-domain proposal also requires review before a freeze.

## Reproduction

`cargo test --release -p xtask b12_ -- --nocapture` runs the detector and controls.
The ignored `b12_reference_corpus_batch` regenerates 32 candidate assessments per
invocation with `B12_FIRST=0,32,...,224`; each shard finishes within 60 seconds.
The archived batches, before/after controls, plane results and machine context
live in `artifacts/runs/cx-b12-v2/`; the final receipt is archived with the branch
in `artifacts/evidence/cx-b12-v2/`. The old exponent and rejected ratio remain
in git and their baseline results are preserved. No frozen criterion is rewritten.
